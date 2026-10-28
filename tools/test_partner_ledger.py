#!/usr/bin/env python3
"""Tests for partner_ledger.py. Run: python3 tools/test_partner_ledger.py"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import partner_ledger as pl  # noqa: E402


class LedgerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = self.tmp.name
        self.run_ok("init")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cmd(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = pl.main(["--dir", self.dir, *args])
        return code, out.getvalue(), err.getvalue()

    def run_ok(self, *args):
        code, out, err = self.run_cmd(*args)
        self.assertEqual(code, 0, f"{args} failed: {err}")
        return out

    def run_fails(self, *args):
        code, out, err = self.run_cmd(*args)
        self.assertNotEqual(code, 0, f"{args} should have failed but printed: {out}")
        return err

    def rows(self, name):
        return pl.Ledger(Path(self.dir)).read(name)

    def signed_partner(self, gst="yes"):
        self.run_ok("partner", "add", "--business", "Northside Inspections", "--type", "building inspector",
                    "--email", "hello@example.com", "--status", "signed", "--gst", gst)

    def confirm_terms(self, basis="ex_gst", partner_gst="add_if_registered"):
        self.run_ok("terms", "set", "--basis", basis, "--partner-gst", partner_gst, "--confirm", "--by", "Jesse")

    def approve(self, total):
        self.run_ok("payouts", "approve", "--total", total, "--by", "Jesse")

    # -- setup -----------------------------------------------------------------
    def test_init_is_idempotent_and_terms_start_unconfirmed(self):
        out = self.run_ok("init")
        self.assertIn("nothing", out)
        terms = json.loads(self.run_ok("terms", "show"))
        self.assertFalse(terms["confirmed"])
        self.assertEqual(terms["fee_rate"], "0.05")
        self.assertEqual(terms["fee_basis"], "unset")

    def test_confirm_needs_a_basis_and_a_name(self):
        self.run_fails("terms", "set", "--confirm", "--by", "Jesse")
        self.run_fails("terms", "set", "--basis", "ex_gst", "--confirm")

    def test_duplicate_partner_rejected(self):
        self.signed_partner()
        err = self.run_fails("partner", "add", "--business", "northside inspections")
        self.assertIn("already in the ledger", err)

    # -- fees ------------------------------------------------------------------
    def test_no_fee_until_terms_confirmed_then_recalc(self):
        self.signed_partner()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "A Homeowner", "--job", "CCTV + relay")
        out = self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "12,000", "--paid-on", "2026-11-04")
        self.assertIn("No fee worked out", out)
        self.assertEqual(self.rows("referrals.csv")[0]["fee_status"], "terms_not_set")
        self.confirm_terms("ex_gst")
        self.run_ok("recalc")
        ref = self.rows("referrals.csv")[0]
        self.assertEqual((ref["fee_nzd"], ref["fee_gst_nzd"], ref["fee_status"]), ("600.00", "90.00", "owed"))

    def test_fee_on_amount_including_gst(self):
        self.signed_partner(gst="no")
        self.confirm_terms("incl_gst")
        self.run_ok("referral", "add", "--partner", "Northside", "--customer", "B Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "10000")
        ref = self.rows("referrals.csv")[0]
        self.assertEqual((ref["fee_nzd"], ref["fee_gst_nzd"]), ("575.00", "0.00"))

    def test_rounding_to_cents(self):
        self.signed_partner(gst="no")
        self.confirm_terms()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "C Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "$1,234.57")
        self.assertEqual(self.rows("referrals.csv")[0]["fee_nzd"], "61.73")

    def test_fee_fields_cannot_be_set_by_hand(self):
        self.signed_partner()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "D Homeowner")
        for field in ("fee_nzd=999", "fee_status=paid", "invoice_ex_gst=1", "payout_id=X"):
            self.run_fails("referral", "set", "R0001", field)

    def test_bad_status_rejected(self):
        self.signed_partner()
        self.run_fails("partner", "set", "P001", "status=married")

    # -- payouts ---------------------------------------------------------------
    def test_payout_cycle(self):
        self.signed_partner(gst="yes")
        self.confirm_terms()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "E Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "8000", "--paid-on", "2026-11-10")
        out = self.run_ok("payouts", "propose", "--month", "2026-11")
        self.assertIn("460.00", out)  # 400 fee + 60 GST
        self.assertIn("SC-P001-2026-11", out)
        payout_id = self.rows("payouts.csv")[0]["payout_id"]
        self.run_fails("payouts", "paid", payout_id)  # not approved yet
        self.run_fails("payouts", "approve", "--total", "999.00", "--by", "Jesse")  # not what Jesse saw
        self.approve("460.00")
        self.run_ok("payouts", "paid", payout_id, "--on", "2026-12-02", "--how", "bank transfer")
        self.assertEqual(self.rows("referrals.csv")[0]["fee_status"], "paid")
        self.assertEqual(self.rows("payouts.csv")[0]["status"], "paid")
        out = self.run_ok("payouts", "propose", "--month", "2026-12")
        self.assertIn("Nothing owed", out)

    def test_repropose_does_not_double_count(self):
        self.signed_partner(gst="no")
        self.confirm_terms()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "F Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "5000", "--paid-on", "2026-11-01")
        self.run_ok("payouts", "propose", "--month", "2026-11")
        self.run_ok("payouts", "propose", "--month", "2026-12")
        payouts = self.rows("payouts.csv")
        self.assertEqual(len(payouts), 1)
        self.assertEqual(payouts[0]["total_nzd"], "250.00")

    def test_unknown_gst_and_unsigned_partner_are_held(self):
        self.run_ok("partner", "add", "--business", "Maybe Realty", "--status", "talking")
        self.signed_partner(gst="unknown")
        self.confirm_terms()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "G Homeowner")
        self.run_ok("referral", "add", "--partner", "P002", "--customer", "H Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "3000", "--paid-on", "2026-11-02")
        self.run_ok("referral", "paid", "R0002", "--invoice-ex-gst", "3000", "--paid-on", "2026-11-02")
        out = self.run_ok("payouts", "propose", "--month", "2026-11")
        self.assertIn("never signed up", out)
        self.assertIn("GST status", out)
        self.assertEqual(self.rows("payouts.csv"), [])
        # the GST answer arrives; the next proposal picks it up without a manual recalc
        self.run_ok("partner", "set", "P002", "gst_registered=yes")
        out = self.run_ok("payouts", "propose", "--month", "2026-11")
        self.assertIn("172.50", out)

    def test_second_payout_same_month_gets_its_own_id(self):
        self.signed_partner(gst="no")
        self.confirm_terms()
        for i, customer in enumerate(("I Homeowner", "J Homeowner"), start=1):
            self.run_ok("referral", "add", "--partner", "P001", "--customer", customer)
            self.run_ok("referral", "paid", f"R000{i}", "--invoice-ex-gst", "2000", "--paid-on", "2026-11-03")
            self.run_ok("payouts", "propose", "--month", "2026-11")
            self.approve("100.00")
        ids = [p["payout_id"] for p in self.rows("payouts.csv")]
        self.assertEqual(len(ids), len(set(ids)))

    # -- cards, scoreboard, dashboard, check ------------------------------------
    def test_call_card_dedupe(self):
        self.run_ok("card", "add", "--name", "Sam", "--business", "Westside PM", "--email", "sam@example.com")
        self.run_fails("card", "add", "--name", "Sam", "--email", "SAM@EXAMPLE.com")
        self.assertTrue(json.loads(self.run_ok("card", "seen", "sam@example.com"))["seen"])

    def test_scoreboard_empty_and_filled(self):
        self.assertIn("nothing recorded yet", self.run_ok("scoreboard"))
        self.signed_partner()
        numbers = json.loads(self.run_ok("scoreboard", "--format", "json", "--period", "month"))
        self.assertEqual(numbers["partners_active"], 1)
        self.assertEqual(numbers["partner_revenue_paid_ex_gst"], "")  # unknown is not zero
        self.assertIn("Partners: 1 signed/active", self.run_ok("scoreboard"))
        self.confirm_terms()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "K Homeowner")
        self.run_ok("referral", "set", "R0001", "status=won")
        self.run_ok("referral", "set", "R0001", "notes=deposit in")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "1000")
        numbers = json.loads(self.run_ok("scoreboard", "--format", "json"))
        self.assertEqual(numbers["jobs_won"], 1)  # counted once, not again when paid or edited

    def test_dashboard_embeds_data_safely(self):
        self.run_ok("partner", "add", "--business", "Evil </script><b>Co", "--status", "signed")
        out_file = Path(self.dir) / "board.html"
        self.run_ok("dashboard", "--out", str(out_file))
        html = out_file.read_text()
        self.assertEqual(html.count("</script>"), Path(pl.__file__).resolve().parent.parent.joinpath(
            "dashboard", "dashboard.template.html").read_text().count("</script>"))
        start = html.index('<script id="dash-data" type="application/json">') + len('<script id="dash-data" type="application/json">')
        data = json.loads(html[start:html.index("</script>", start)])
        self.assertEqual(data["partners"][0]["business"], "Evil </script><b>Co")

    def test_check_reports_unconfirmed_terms(self):
        self.assertIn("terms not confirmed", self.run_ok("check"))
        self.run_ok("terms", "set", "--basis", "ex_gst", "--confirm", "--by", "Jesse")
        self.assertIn("GST-registered partners", self.run_ok("check"))
        self.confirm_terms()
        self.assertIn("ok", self.run_ok("check"))

    # -- review fixes ------------------------------------------------------------
    def test_correcting_a_proposed_invoice_never_pays_twice(self):
        self.signed_partner(gst="no")
        self.confirm_terms()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "L Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "12000", "--paid-on", "2026-11-03")
        self.run_ok("payouts", "propose", "--month", "2026-11")
        out = self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "14000", "--paid-on", "2026-11-03")
        self.assertIn("cancelled", out)
        self.assertEqual(self.rows("payouts.csv"), [])
        self.run_fails("payouts", "approve", "--total", "600.00", "--by", "Jesse")
        self.run_ok("payouts", "propose", "--month", "2026-11")
        self.approve("700.00")
        self.run_ok("payouts", "propose", "--month", "2026-12")
        self.assertEqual([(p["status"], p["total_nzd"]) for p in self.rows("payouts.csv")], [("approved", "700.00")])

    def test_partner_gst_rule_is_jesses(self):
        self.signed_partner(gst="yes")
        self.run_ok("terms", "set", "--basis", "ex_gst", "--confirm", "--by", "Jesse")  # GST rule still unset
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "M Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "1000")
        self.assertEqual(self.rows("referrals.csv")[0]["fee_gst_nzd"], "")  # held, not guessed
        self.confirm_terms(partner_gst="never")
        self.run_ok("recalc")
        self.assertEqual(self.rows("referrals.csv")[0]["fee_gst_nzd"], "0.00")

    def test_changing_terms_clears_confirmation(self):
        self.confirm_terms()
        self.run_ok("terms", "set", "--basis", "incl_gst")
        self.assertFalse(json.loads(self.run_ok("terms", "show"))["confirmed"])

    def test_custom_rate_still_needs_confirmed_terms(self):
        self.signed_partner(gst="no")
        self.run_ok("partner", "set", "P001", "fee_rate=0.06", "fee_basis=ex_gst")
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "N Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "1000")
        self.assertEqual(self.rows("referrals.csv")[0]["fee_status"], "terms_not_set")

    def test_gst_on_the_rounded_fee(self):
        self.signed_partner(gst="yes")
        self.confirm_terms()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "O Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "10013.93")
        ref = self.rows("referrals.csv")[0]
        self.assertEqual((ref["fee_nzd"], ref["fee_gst_nzd"]), ("500.70", "75.11"))

    def test_bad_inputs_are_refused(self):
        self.signed_partner(gst="no")
        self.confirm_terms()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "Q Homeowner")
        self.run_fails("referral", "paid", "R0001")
        self.run_fails("referral", "paid", "R0001", "--invoice-ex-gst", "-5000")
        self.run_fails("referral", "paid", "R0001", "--invoice-ex-gst", "5000", "--paid-on", "4 Nov")
        self.run_fails("partner", "set", "P001", "fee_rate=7")
        self.run_fails("partner", "set", "P001", "gst_registered=maybe")
        self.run_fails("card", "seen")

    def test_ended_partner_still_paid(self):
        self.signed_partner(gst="no")
        self.confirm_terms()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "R Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "2000", "--paid-on", "2026-11-05")
        self.run_ok("partner", "set", "P001", "status=ended")
        self.assertIn("100.00", self.run_ok("payouts", "propose", "--month", "2026-11"))

    def test_notes_append_and_second_job_allowed(self):
        self.signed_partner(gst="no")
        self.run_ok("partner", "set", "P001", "notes=custom deal per Jesse")
        self.run_ok("partner", "set", "P001", "notes=checked in")
        self.assertIn("custom deal per Jesse", self.rows("partners.csv")[0]["notes"])
        self.confirm_terms()
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "S Homeowner")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "1000")
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "S Homeowner")  # a second job later

    def test_outbox_sends_once(self):
        self.run_ok("outbox", "add", "--kind", "welcome", "--to", "kate@example.com", "--subject", "Welcome aboard",
                    "--approved-ref", "Jesse: send welcome")
        self.run_fails("outbox", "add", "--kind", "welcome", "--to", "KATE@example.com", "--subject", "welcome aboard",
                       "--approved-ref", "again")
        self.run_ok("outbox", "sent", "O0001")
        self.run_fails("outbox", "sent", "O0001")
        self.assertIn("sent", self.run_ok("outbox", "check", "kate@example.com"))

    def test_outbox_failed_send_needs_new_words(self):
        self.run_ok("outbox", "add", "--kind", "thanks", "--to", "kate@example.com", "--subject", "Thanks",
                    "--approved-ref", "send thanks 10:01")
        self.run_ok("outbox", "failed", "O0001", "--why", "Graph error, not in Sent Items")
        self.run_fails("outbox", "add", "--kind", "thanks", "--to", "kate@example.com", "--subject", "Thanks",
                       "--approved-ref", "send thanks 10:01")
        self.run_ok("outbox", "add", "--kind", "thanks", "--to", "kate@example.com", "--subject", "Thanks",
                    "--approved-ref", "send thanks 10:20")

    def test_approve_total_accepts_how_people_write_money(self):
        self.run_ok("terms", "set", "--basis", "ex_gst", "--partner-gst", "add_if_registered", "--confirm", "--by", "Jesse")
        self.run_ok("partner", "add", "--business", "Westside PM", "--type", "property manager", "--status", "signed")
        self.run_ok("partner", "set", "P001", "gst_registered=no")
        self.run_ok("referral", "add", "--partner", "P001", "--customer", "Cust A", "--job", "relay")
        self.run_ok("referral", "paid", "R0001", "--invoice-ex-gst", "24690", "--paid-on", "2026-10-10")
        self.assertIn("1,234.50", self.run_ok("payouts", "propose", "--month", "2026-10").replace("1234.50", "1,234.50"))
        self.run_fails("payouts", "approve", "--total", "1234.51", "--by", "Jesse")
        self.run_ok("payouts", "approve", "--total", "$1,234.5", "--by", "Jesse")


if __name__ == "__main__":
    unittest.main(verbosity=1)
