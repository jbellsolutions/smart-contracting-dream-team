#!/usr/bin/env python3
"""Smart Contracting partner ledger: the one place partner records live, and the only code that does the sums.

The Revenue Partner calls this tool; it never works out a fee, a payout or a scoreboard number in its head.
Standard library only. Data lives in plain CSV files in the ledger folder (default ~/PartnerDesk), so Jesse,
Justin's team or a spreadsheet can read them. Every change is appended to actions.log.

  partner_ledger.py init
  partner_ledger.py terms show | terms set --basis ex_gst --partner-gst add_if_registered --confirm --by Jesse
  partner_ledger.py partner add --business "..." --type "real estate" [--contact .. --email .. --phone .. --suburb .. --status signed]
  partner_ledger.py partner set P001 status=active next_campaign=2026-11
  partner_ledger.py partner list [--status signed,active] | partner find "text"
  partner_ledger.py referral add --partner P001 --customer "..." --suburb "..." --job "CCTV + relay" --how "phone intro"
  partner_ledger.py referral set R0001 status=quoted quote_ex_gst=8400
  partner_ledger.py referral paid R0001 --invoice-ex-gst 12000 --paid-on 2026-11-04
  partner_ledger.py referral list [--status owed]
  partner_ledger.py payouts propose --month 2026-11 | payouts approve --total 690.00 --by Jesse
  partner_ledger.py payouts paid Y2026-11-P001 --on 2026-12-02 --how "bank transfer"
  partner_ledger.py campaign add --partner P001 --month 2026-11 --theme "pre-sale drain check" | campaign set C001 status=sent ...
  partner_ledger.py card seen <email> | card add --name .. --business .. --email .. --source .. | card set K001 status=called
  partner_ledger.py outbox add --kind welcome --to kate@example.com --subject "..." --approved-ref "<Jesse's yes>" | outbox sent O0001
  partner_ledger.py scoreboard [--period week|month|last-month] [--format md|json]
  partner_ledger.py dashboard --out ~/PartnerDesk/scoreboard.html
  partner_ledger.py check
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
from contextlib import contextmanager
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

try:  # the Revenue Partner's computer is Linux; the lock is skipped where fcntl doesn't exist
    import fcntl
except ImportError:  # pragma: no cover
    fcntl = None

GST_RATE = Decimal("0.15")  # New Zealand GST
TZ_NAME = "Pacific/Auckland"

SCHEMAS = {
    "partners.csv": ["partner_id", "business", "partner_type", "contact_name", "email", "phone", "suburb", "status",
                     "signed_on", "fee_rate", "fee_basis", "gst_registered", "ref_code", "list_size",
                     "next_campaign", "last_contacted", "notes", "updated_on"],
    "referrals.csv": ["referral_id", "date_in", "partner_id", "customer_name", "suburb", "job_type", "how", "status",
                      "quote_ex_gst", "invoice_ex_gst", "invoice_paid_on", "fee_nzd", "fee_gst_nzd", "fee_status",
                      "payout_id", "won_on", "notes", "updated_on"],
    "payouts.csv": ["payout_id", "month", "partner_id", "referral_ids", "fee_nzd", "gst_nzd", "total_nzd", "status",
                    "approved_by", "approved_on", "paid_on", "paid_how", "reference"],
    "campaigns.csv": ["campaign_id", "partner_id", "month", "theme", "status", "copy_file", "partner_sent_on",
                      "customers_reached", "replies", "bookings", "jobs_won", "revenue_ex_gst", "notes", "updated_on"],
    "cards.csv": ["card_id", "created_on", "name", "business", "email", "source", "status", "notes", "updated_on"],
    "outbox.csv": ["outbox_id", "created_on", "kind", "to_email", "subject", "body_file", "approved_by", "approved_ref",
                   "status", "sent_on", "notes"],
}
STATUSES = {
    "partners.csv": {"talking", "signed", "active", "paused", "ended"},
    "referrals.csv": {"new", "quoted", "won", "lost", "done"},
    "campaigns.csv": {"idea", "drafted", "partner_approved", "sent", "done", "dropped"},
    "cards.csv": {"card_sent", "called", "campaign_agreed", "partner_signed", "not_now", "no_answer"},
    "outbox.csv": {"approved", "sent", "failed", "cancelled"},
}
CHOICES = {"fee_basis": {"", "ex_gst", "incl_gst"}, "gst_registered": {"yes", "no", "unknown"}}
DATE_FIELDS = {"signed_on", "last_contacted", "partner_sent_on", "won_on", "next_campaign"}
DEFAULT_TERMS = {
    "fee_rate": "0.05",
    "fee_basis": "unset",          # ex_gst | incl_gst | unset
    "trigger": "invoice_paid_in_full",
    "partner_gst": "unset",        # add_if_registered | never | unset (until Jesse answers, GST-registered partners are held)
    "cap_nzd": "",
    "confirmed": False,
    "confirmed_by": "",
    "confirmed_on": "",
    "source": "Jesse's own wording (Sep 23 emails, Oct 9 one-pager): 5% of the job value, "
              "paid once the customer's invoice is settled in full.",
}


# Fields only the tool itself writes: fees come from `referral paid`, `recalc` and `payouts`, never by hand.
LOCKED_FIELDS = {"fee_nzd", "fee_gst_nzd", "fee_status", "payout_id", "invoice_paid_on", "invoice_ex_gst"}


class LedgerError(Exception):
    pass


def count(value: str) -> int:
    try:
        return int(str(value).strip() or 0)
    except ValueError:
        return 0


def today() -> str:
    try:
        from zoneinfo import ZoneInfo
        return dt.datetime.now(ZoneInfo(TZ_NAME)).date().isoformat()
    except Exception:  # zoneinfo or tzdata missing: fall back to the box clock
        return dt.date.today().isoformat()


def money(value: str | Decimal | None) -> Decimal | None:
    if value is None:
        return None
    text = str(value).replace("$", "").replace(",", "").replace("NZD", "").strip()
    if not text:
        return None
    try:
        return Decimal(text)
    except InvalidOperation as exc:
        raise LedgerError(f"not an amount: {value!r}") from exc


def iso_date(value: str, what: str) -> str:
    text = (value or "").strip()
    try:
        return dt.date.fromisoformat(text).isoformat()
    except ValueError as exc:
        raise LedgerError(f"{what} must be a date like 2026-11-04, got {value!r}") from exc


def cents(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def fmt(value: Decimal | None) -> str:
    return "" if value is None else f"{cents(value):.2f}"


class Ledger:
    def __init__(self, folder: Path):
        self.dir = folder.expanduser()

    # -- storage -----------------------------------------------------------
    @contextmanager
    def lock(self):
        self.dir.mkdir(parents=True, exist_ok=True)
        with open(self.dir / ".lock", "w") as handle:
            if fcntl:
                fcntl.flock(handle, fcntl.LOCK_EX)
            try:
                yield
            finally:
                if fcntl:
                    fcntl.flock(handle, fcntl.LOCK_UN)

    def read(self, name: str) -> list[dict]:
        path = self.dir / name
        if not path.exists():
            raise LedgerError(f"{path} is missing: run `partner_ledger.py init` first")
        with open(path, newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            for key in SCHEMAS[name]:
                row.setdefault(key, "")
        return rows

    def write(self, name: str, rows: list[dict]) -> None:
        path = self.dir / name
        tmp = path.with_suffix(".tmp")
        with open(tmp, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=SCHEMAS[name], extrasaction="ignore")
            writer.writeheader()
            for row in rows:
                writer.writerow({k: row.get(k, "") for k in SCHEMAS[name]})
        os.replace(tmp, path)

    def log(self, line: str) -> None:
        with open(self.dir / "actions.log", "a", encoding="utf-8") as handle:
            handle.write(f"{dt.datetime.now().isoformat(timespec='seconds')} · {line}\n")

    def terms(self) -> dict:
        path = self.dir / "terms.json"
        if not path.exists():
            raise LedgerError(f"{path} is missing: run `partner_ledger.py init` first")
        return json.loads(path.read_text(encoding="utf-8"))

    # -- helpers -----------------------------------------------------------
    @staticmethod
    def next_id(rows: list[dict], key: str, prefix: str, width: int) -> str:
        nums = [int(r[key][len(prefix):]) for r in rows if r.get(key, "").startswith(prefix) and r[key][len(prefix):].isdigit()]
        return f"{prefix}{(max(nums) + 1 if nums else 1):0{width}d}"

    def find_partner(self, ref: str) -> dict:
        partners = self.read("partners.csv")
        exact = [p for p in partners if p["partner_id"].lower() == ref.lower()]
        if exact:
            return exact[0]
        needle = ref.lower()
        hits = [p for p in partners if needle in " ".join([p["business"], p["contact_name"], p["email"], p["ref_code"]]).lower()]
        if len(hits) == 1:
            return hits[0]
        if not hits:
            raise LedgerError(f"no partner matches {ref!r}. Run `partner list` or `partner add` first")
        raise LedgerError(f"{ref!r} matches {len(hits)} partners: " + ", ".join(f"{p['partner_id']} {p['business']}" for p in hits))

    @staticmethod
    def apply_fields(row: dict, pairs: list[str], name: str) -> list[str]:
        changed = []
        for pair in pairs:
            if "=" not in pair:
                raise LedgerError(f"expected field=value, got {pair!r}")
            key, value = pair.split("=", 1)
            key = key.strip()
            if key not in SCHEMAS[name] or key == SCHEMAS[name][0]:
                raise LedgerError(f"{key!r} isn't a field you can set in {name}")
            if name == "referrals.csv" and key in LOCKED_FIELDS:
                raise LedgerError(f"{key} is worked out by the tool: use `referral paid`, `recalc` or `payouts`")
            if key == "status" and name in STATUSES and value not in STATUSES[name]:
                raise LedgerError(f"status must be one of {sorted(STATUSES[name])}")
            value = value.strip()
            if key in ("quote_ex_gst", "invoice_ex_gst", "revenue_ex_gst") and value:
                amount = money(value)
                if amount is None or amount < 0:
                    raise LedgerError(f"{key} must be an amount of zero or more")
                value = fmt(amount)
            if key == "fee_rate" and value:
                rate = money(value)
                if rate is None or not Decimal("0") < rate < Decimal("1"):
                    raise LedgerError("fee_rate must be a fraction like 0.05 (for 5%)")
            if key in CHOICES and value not in CHOICES[key]:
                raise LedgerError(f"{key} must be one of {sorted(c for c in CHOICES[key] if c)}")
            if key in DATE_FIELDS and value:
                value = value if key == "next_campaign" and len(value) == 7 else iso_date(value, key)
            if key == "notes" and row.get("notes") and value:
                value = f"{row['notes']} | {today()}: {value}"
            row[key] = value
            changed.append(f"{key}={value}")
        return changed

    # -- fees --------------------------------------------------------------
    def fee_for(self, referral: dict, partner: dict, terms: dict) -> tuple[str, str, str]:
        """Return (fee_nzd, fee_gst_nzd, fee_status) for a referral whose invoice is paid."""
        rate_text = partner.get("fee_rate") or terms.get("fee_rate", "")
        basis = partner.get("fee_basis") or terms.get("fee_basis", "unset")
        if not terms.get("confirmed"):  # even a custom rate waits for Jesse's confirmed terms
            return "", "", "terms_not_set"
        if basis not in ("ex_gst", "incl_gst"):
            return "", "", "terms_not_set"
        invoice = money(referral.get("invoice_ex_gst"))
        if invoice is None:
            return "", "", "held"
        rate = money(rate_text)
        if rate is None or rate <= 0 or rate >= 1:
            raise LedgerError(f"fee rate {rate_text!r} must be a fraction like 0.05")
        base = invoice if basis == "ex_gst" else invoice * (1 + GST_RATE)
        fee = base * rate
        cap = money(terms.get("cap_nzd"))
        if cap is not None and fee > cap:
            fee = cap
        fee = cents(fee)  # GST is worked out on the rounded fee, as on the partner's own invoice
        policy = terms.get("partner_gst", "unset")
        gst_flag = (partner.get("gst_registered") or "unknown").lower()
        if gst_flag == "no" or policy == "never":
            gst = "0.00"
        elif gst_flag == "yes" and policy == "add_if_registered":
            gst = fmt(fee * GST_RATE)
        else:
            gst = ""  # unknown is not zero: held until the partner's GST status and Jesse's GST rule are known
        return fmt(fee), gst, "owed"


# -- commands ----------------------------------------------------------------

def cmd_init(led: Ledger, args) -> str:
    led.dir.mkdir(parents=True, exist_ok=True)
    made = []
    for name, cols in SCHEMAS.items():
        path = led.dir / name
        if not path.exists():
            led.write(name, [])
            made.append(name)
    terms_path = led.dir / "terms.json"
    if not terms_path.exists():
        seed = dict(DEFAULT_TERMS)
        if args.terms_seed and Path(args.terms_seed).exists():
            seed.update(json.loads(Path(args.terms_seed).read_text(encoding="utf-8")))
        terms_path.write_text(json.dumps(seed, indent=2) + "\n", encoding="utf-8")
        made.append("terms.json")
    (led.dir / "actions.log").touch()
    led.log(f"init · created {', '.join(made) or 'nothing (already there)'}")
    return f"Ledger ready at {led.dir}. Created: {', '.join(made) or 'nothing, it was already there'}."


def cmd_terms(led: Ledger, args) -> str:
    terms = led.terms()
    if args.action == "show":
        return json.dumps(terms, indent=2)
    before = {k: terms.get(k) for k in ("fee_rate", "fee_basis", "partner_gst", "cap_nzd")}
    if args.rate is not None:
        rate = money(args.rate)
        if rate is None or not Decimal("0") < rate < Decimal("1"):
            raise LedgerError("--rate must be a fraction like 0.05 (for 5%)")
        terms["fee_rate"] = str(rate)
    if args.basis:
        terms["fee_basis"] = args.basis
    if args.partner_gst:
        terms["partner_gst"] = args.partner_gst
    if args.cap is not None:
        terms["cap_nzd"] = args.cap
    if before != {k: terms.get(k) for k in before} and not args.confirm:
        terms.update(confirmed=False, confirmed_by="", confirmed_on="")
    if args.confirm:
        if not args.by:
            raise LedgerError("--confirm needs --by <who said yes>")
        if terms.get("fee_basis") not in ("ex_gst", "incl_gst"):
            raise LedgerError("set --basis ex_gst or incl_gst before confirming")
        terms.update(confirmed=True, confirmed_by=args.by, confirmed_on=today())
    (led.dir / "terms.json").write_text(json.dumps(terms, indent=2) + "\n", encoding="utf-8")
    led.log(f"terms set · {json.dumps(terms)}")
    return "Terms saved:\n" + json.dumps(terms, indent=2)


def cmd_partner(led: Ledger, args) -> str:
    rows = led.read("partners.csv")
    if args.action == "add":
        dupes = [p for p in rows if p["business"].lower() == args.business.lower()
                 or (args.email and p["email"].lower() == args.email.lower())]
        if dupes:
            raise LedgerError(f"already in the ledger as {dupes[0]['partner_id']} ({dupes[0]['business']})")
        if args.gst and args.gst not in CHOICES["gst_registered"]:
            raise LedgerError("--gst must be yes, no or unknown")
        pid = Ledger.next_id(rows, "partner_id", "P", 3)
        status = args.status or "talking"
        if status not in STATUSES["partners.csv"]:
            raise LedgerError(f"status must be one of {sorted(STATUSES['partners.csv'])}")
        row = {"partner_id": pid, "business": args.business, "partner_type": args.type or "", "contact_name": args.contact or "",
               "email": args.email or "", "phone": args.phone or "", "suburb": args.suburb or "", "status": status,
               "signed_on": today() if status in ("signed", "active") else "", "gst_registered": args.gst or "unknown",
               "ref_code": f"SC-{pid}", "list_size": args.list_size or "", "notes": args.notes or "", "updated_on": today()}
        rows.append(row)
        led.write("partners.csv", rows)
        led.log(f"partner add · {pid} · {args.business} · {status}")
        return f"Added {pid}: {args.business} ({status}). Ref code {row['ref_code']}."
    if args.action == "set":
        partner = next((p for p in rows if p["partner_id"] == args.id), None)
        if not partner:
            raise LedgerError(f"no partner {args.id}")
        changed = Ledger.apply_fields(partner, args.fields, "partners.csv")
        if any(c.startswith("status=signed") or c.startswith("status=active") for c in changed) and not partner["signed_on"]:
            partner["signed_on"] = today()
        partner["updated_on"] = today()
        led.write("partners.csv", rows)
        led.log(f"partner set · {args.id} · {' '.join(changed)}")
        return f"Updated {args.id}: {', '.join(changed)}."
    if args.action == "find":
        partner = led.find_partner(args.text)
        return json.dumps(partner, indent=2)
    wanted = set(args.status.split(",")) if args.status else None
    shown = [p for p in rows if not wanted or p["status"] in wanted]
    if not shown:
        return "No partners yet." if not rows else "No partners with that status."
    return "\n".join(f"{p['partner_id']} · {p['business']} · {p['partner_type'] or '—'} · {p['status']} · "
                     f"next campaign {p['next_campaign'] or '—'}" for p in shown)


def cmd_referral(led: Ledger, args) -> str:
    rows = led.read("referrals.csv")
    if args.action == "add":
        partner = led.find_partner(args.partner)
        dupes = [r for r in rows if r["partner_id"] == partner["partner_id"]
                 and r["customer_name"].lower() == args.customer.lower() and r["status"] in ("new", "quoted", "won")]
        if dupes:
            raise LedgerError(f"already logged as {dupes[0]['referral_id']} on {dupes[0]['date_in']}")
        rid = Ledger.next_id(rows, "referral_id", "R", 4)
        rows.append({"referral_id": rid, "date_in": today(), "partner_id": partner["partner_id"], "customer_name": args.customer,
                     "suburb": args.suburb or "", "job_type": args.job or "", "how": args.how or "", "status": "new",
                     "fee_status": "not_due", "notes": args.notes or "", "updated_on": today()})
        led.write("referrals.csv", rows)
        led.log(f"referral add · {rid} · {partner['partner_id']}")
        return f"Logged {rid}: {args.customer} from {partner['business']} ({partner['partner_id']})."
    if args.action == "set":
        ref = next((r for r in rows if r["referral_id"] == args.id), None)
        if not ref:
            raise LedgerError(f"no referral {args.id}")
        changed = Ledger.apply_fields(ref, args.fields, "referrals.csv")
        if ref["status"] == "won" and not ref["won_on"]:
            ref["won_on"] = today()
        ref["updated_on"] = today()
        led.write("referrals.csv", rows)
        led.log(f"referral set · {args.id} · {' '.join(changed)}")
        return f"Updated {args.id}: {', '.join(changed)}."
    if args.action == "paid":
        ref = next((r for r in rows if r["referral_id"] == args.id), None)
        if not ref:
            raise LedgerError(f"no referral {args.id}")
        if ref["fee_status"] in ("approved", "paid"):
            raise LedgerError(f"{args.id}'s fee is already {ref['fee_status']}; change it by hand only with Jesse's OK")
        amount = money(args.invoice_ex_gst)
        if amount is None or amount <= 0:
            raise LedgerError("--invoice-ex-gst must be the whole job's invoice before GST, more than zero")
        paid_on = iso_date(args.paid_on, "--paid-on") if args.paid_on else today()
        voided = ""
        if ref["fee_status"] == "proposed":  # the open proposal showed the old figure: cancel it
            payouts = [p for p in led.read("payouts.csv") if p["status"] != "proposed"]
            for other in rows:
                if other["fee_status"] == "proposed":
                    other["fee_status"], other["payout_id"] = "owed", ""
            led.write("payouts.csv", payouts)
            voided = " The open payout proposal included the old figure, so it's cancelled: run `payouts propose` again."
        ref["invoice_ex_gst"] = fmt(amount)
        ref["invoice_paid_on"] = paid_on
        if ref["status"] in ("new", "quoted", "won"):
            ref["won_on"] = ref["won_on"] or paid_on
            ref["status"] = "done"
        partner = led.find_partner(ref["partner_id"])
        fee, gst, status = led.fee_for(ref, partner, led.terms())
        ref.update(fee_nzd=fee, fee_gst_nzd=gst, fee_status=status, updated_on=today())
        led.write("referrals.csv", rows)
        led.log(f"referral paid · {args.id} · invoice {ref['invoice_ex_gst']} ex GST · fee {fee or '-'} · {status}")
        if status == "terms_not_set":
            return (f"Recorded the paid invoice for {args.id}. No fee worked out: the partner terms aren't confirmed "
                    f"(fee on the amount before or after GST?). Ask Jesse, then run `terms set ... --confirm --by Jesse` "
                    f"and `recalc`.{voided}")
        gst_note = {"": " GST: not known yet (is the partner GST registered, and does Jesse add GST to partner fees?).",
                    "0.00": " No GST on top."}.get(gst, f" Plus GST {gst} if they invoice it.")
        return (f"{args.id}: invoice {ref['invoice_ex_gst']} ex GST paid {ref['invoice_paid_on']}. "
                f"Fee owed to {partner['business']}: {fee}.{gst_note}{voided}")
    wanted = args.status
    shown = [r for r in rows if not wanted or r["status"] == wanted or r["fee_status"] == wanted]
    if not shown:
        return "No referrals yet." if not rows else "None with that status."
    return "\n".join(f"{r['referral_id']} · {r['date_in']} · {r['partner_id']} · {r['customer_name']} · {r['job_type'] or '—'} · "
                     f"{r['status']} · fee {r['fee_nzd'] or '—'} ({r['fee_status']})" for r in shown)


def cmd_recalc(led: Ledger, args) -> str:
    rows = led.read("referrals.csv")
    terms = led.terms()
    changed = []
    for ref in rows:
        if ref["invoice_paid_on"] and ref["fee_status"] in ("terms_not_set", "held", "owed"):
            fee, gst, status = led.fee_for(ref, led.find_partner(ref["partner_id"]), terms)
            if (fee, gst, status) != (ref["fee_nzd"], ref["fee_gst_nzd"], ref["fee_status"]):
                ref.update(fee_nzd=fee, fee_gst_nzd=gst, fee_status=status, updated_on=today())
                changed.append(f"{ref['referral_id']} → {status} {fee}")
    led.write("referrals.csv", rows)
    led.log(f"recalc · {len(changed)} changed")
    return "Recalculated: " + ("; ".join(changed) if changed else "nothing changed.")


def cmd_payouts(led: Ledger, args) -> str:
    payouts = led.read("payouts.csv")
    refs = led.read("referrals.csv")
    partners = {p["partner_id"]: p for p in led.read("partners.csv")}
    if args.action == "propose":
        month = args.month
        # A proposal is a draft: only one is open at a time, and a new one replaces it.
        payouts = [p for p in payouts if p["status"] != "proposed"]
        for ref in refs:
            if ref["fee_status"] == "proposed":
                ref["fee_status"], ref["payout_id"] = "owed", ""
        terms = led.terms()
        held = []
        for ref in refs:  # pick up GST or terms changes made since the invoice was recorded
            if ref["invoice_paid_on"] and ref["fee_status"] in ("owed", "held", "terms_not_set") and ref["partner_id"] in partners:
                try:
                    fee, gst, status = led.fee_for(ref, partners[ref["partner_id"]], terms)
                except LedgerError as exc:
                    held.append(f"{ref['referral_id']}: {exc}")
                    ref.update(fee_nzd="", fee_gst_nzd="", fee_status="held")
                    continue
                ref.update(fee_nzd=fee, fee_gst_nzd=gst, fee_status=status)
        waiting = [r["referral_id"] for r in refs if r["fee_status"] == "terms_not_set"]
        owed = [r for r in refs if r["fee_status"] == "owed" and r["invoice_paid_on"] and r["invoice_paid_on"][:7] <= month]
        taken = {p["payout_id"] for p in payouts}
        lines = []
        by_partner: dict[str, list[dict]] = {}
        for ref in owed:
            partner = partners.get(ref["partner_id"])
            if not partner or not partner["signed_on"]:  # paused or ended partners are still paid for their referrals
                held.append(f"{ref['referral_id']}: partner {ref['partner_id']} never signed up")
                continue
            if ref["fee_gst_nzd"] == "":
                held.append(f"{ref['referral_id']}: GST status of {partner['business']} unknown")
                continue
            by_partner.setdefault(ref["partner_id"], []).append(ref)
        for pid, items in sorted(by_partner.items()):
            fee = sum(money(r["fee_nzd"]) for r in items)
            gst = sum(money(r["fee_gst_nzd"]) or Decimal("0") for r in items)
            payout_id, n = f"Y{month}-{pid}", 2
            while payout_id in taken:
                payout_id, n = f"Y{month}-{pid}-{n}", n + 1
            taken.add(payout_id)
            payouts.append({"payout_id": payout_id, "month": month, "partner_id": pid,
                            "referral_ids": " ".join(r["referral_id"] for r in items), "fee_nzd": fmt(fee),
                            "gst_nzd": fmt(gst), "total_nzd": fmt(fee + gst), "status": "proposed",
                            "reference": f"SC-{pid}-{month}"})
            for ref in items:
                ref["fee_status"], ref["payout_id"] = "proposed", payout_id
            lines.append(f"| {partners[pid]['business']} | {len(items)} | {fmt(fee)} | {fmt(gst)} | {fmt(fee + gst)} | SC-{pid}-{month} |")
        led.write("payouts.csv", payouts)
        led.write("referrals.csv", refs)
        led.log(f"payouts propose · {month} · {len(lines)} partners · {len(held)} held")
        total = sum((money(p["total_nzd"]) for p in payouts if p["status"] == "proposed"), Decimal("0"))
        table = ["| Partner | Jobs | Fee (ex GST) | GST | Total | Bank reference |", "|---|---|---|---|---|---|"] + lines
        out = [f"Partner payouts · {month}", ""] + (table if lines else ["Nothing owed this month."])
        out += ["", f"Total to pay: {fmt(total)} NZD"]
        if lines:
            out += [f"To approve exactly this list: payouts approve --total {fmt(total)} --by Jesse"]
        if held:
            out += ["Held back:"] + [f"- {h}" for h in held]
        if waiting:
            out += [f"Waiting on the partner terms (before or after GST?): {', '.join(waiting)}"]
        return "\n".join(out)
    if args.action == "approve":
        proposed = [p for p in payouts if p["status"] == "proposed"]
        shown = money(args.total)
        if shown is None:
            raise LedgerError("give --total: the 'Total to pay' Jesse saw, so nothing else gets approved")
        now_total = sum((money(p["total_nzd"]) for p in proposed), Decimal("0"))
        if not proposed:
            raise LedgerError("there's no payout proposal open: run `payouts propose` first")
        if cents(now_total) != cents(shown):
            raise LedgerError(f"the open proposal now totals {fmt(now_total)}, not the {fmt(shown)} Jesse approved. "
                              f"Show him the current list again")
        approved_ids = set()
        for p in proposed:
            p.update(status="approved", approved_by=args.by, approved_on=today())
            approved_ids.add(p["payout_id"])
        for ref in refs:
            if ref["fee_status"] == "proposed" and ref["payout_id"] in approved_ids:
                ref["fee_status"] = "approved"
        led.write("payouts.csv", payouts)
        led.write("referrals.csv", refs)
        led.log(f"payouts approve · {fmt(shown)} · {len(approved_ids)} by {args.by}")
        return (f"Approved {len(approved_ids)} payout(s), total {fmt(shown)} (by {args.by}). "
                f"Nothing is paid until Jesse pays it and says so.")
    if args.action == "paid":
        payout = next((p for p in payouts if p["payout_id"] == args.id), None)
        if not payout:
            raise LedgerError(f"no payout {args.id}")
        if payout["status"] != "approved":
            raise LedgerError(f"{args.id} is {payout['status']}; only an approved payout can be marked paid")
        payout.update(status="paid", paid_on=iso_date(args.on, "--on") if args.on else today(), paid_how=args.how or "")
        for ref in refs:
            if ref["payout_id"] == args.id:
                ref["fee_status"] = "paid"
        led.write("payouts.csv", payouts)
        led.write("referrals.csv", refs)
        led.log(f"payouts paid · {args.id} · {payout['paid_on']} · {args.how or ''}")
        return f"Marked {args.id} paid on {payout['paid_on']}."
    return "\n".join(f"{p['payout_id']} · {p['status']} · {p['total_nzd']}" for p in payouts) or "No payouts yet."


def cmd_campaign(led: Ledger, args) -> str:
    rows = led.read("campaigns.csv")
    if args.action == "add":
        partner = led.find_partner(args.partner)
        cid = Ledger.next_id(rows, "campaign_id", "C", 3)
        rows.append({"campaign_id": cid, "partner_id": partner["partner_id"], "month": args.month or "", "theme": args.theme or "",
                     "status": "idea", "notes": args.notes or "", "updated_on": today()})
        led.write("campaigns.csv", rows)
        led.log(f"campaign add · {cid} · {partner['partner_id']}")
        return f"Campaign {cid} for {partner['business']} ({args.month or 'month not set'}) added as an idea."
    if args.action == "set":
        row = next((r for r in rows if r["campaign_id"] == args.id), None)
        if not row:
            raise LedgerError(f"no campaign {args.id}")
        changed = Ledger.apply_fields(row, args.fields, "campaigns.csv")
        row["updated_on"] = today()
        led.write("campaigns.csv", rows)
        led.log(f"campaign set · {args.id} · {' '.join(changed)}")
        return f"Updated {args.id}: {', '.join(changed)}."
    return "\n".join(f"{r['campaign_id']} · {r['partner_id']} · {r['month']} · {r['theme']} · {r['status']}" for r in rows) or "No campaigns yet."


def cmd_card(led: Ledger, args) -> str:
    rows = led.read("cards.csv")
    if args.action == "seen":
        if not args.email:
            raise LedgerError("card seen needs the email address: card seen <email>")
        hit = [r for r in rows if r["email"] and r["email"].lower() == args.email.lower()]
        return json.dumps({"seen": bool(hit), "cards": hit})
    if args.action == "add":
        if args.email and any(r["email"].lower() == args.email.lower() for r in rows):
            raise LedgerError(f"a call card for {args.email} already exists: don't post it twice")
        kid = Ledger.next_id(rows, "card_id", "K", 3)
        rows.append({"card_id": kid, "created_on": today(), "name": args.name or "", "business": args.business or "",
                     "email": args.email or "", "source": args.source or "", "status": "card_sent", "updated_on": today()})
        led.write("cards.csv", rows)
        led.log(f"card add · {kid}")
        return f"Card {kid} recorded."
    if args.action == "set":
        row = next((r for r in rows if r["card_id"] == args.id), None)
        if not row:
            raise LedgerError(f"no card {args.id}")
        changed = Ledger.apply_fields(row, args.fields, "cards.csv")
        row["updated_on"] = today()
        led.write("cards.csv", rows)
        led.log(f"card set · {args.id} · {' '.join(changed)}")
        return f"Updated {args.id}: {', '.join(changed)}."
    return "\n".join(f"{r['card_id']} · {r['created_on']} · {r['business']} · {r['status']}" for r in rows) or "No call cards yet."


def cmd_outbox(led: Ledger, args) -> str:
    """The send-once record for every email the scdt- skills send: approved before sending, sent after."""
    rows = led.read("outbox.csv")
    if args.action == "add":
        if not (args.to and args.subject and args.approved_ref):
            raise LedgerError("outbox add needs --to, --subject and --approved-ref (Jesse's words or message link)")
        same = [r for r in rows if r["to_email"].lower() == args.to.lower() and r["subject"].strip().lower() == args.subject.strip().lower()]
        live = [r for r in same if r["status"] in ("approved", "sent")]
        if live:
            r = live[-1]
            raise LedgerError(f"{r['outbox_id']} to {args.to} with that subject is already {r['status']} ({r['sent_on'] or r['created_on']}). "
                              f"Don't send it again")
        # A failed send can go again only on Jesse's new reply words, never on the yes that approved the failed one.
        failed = [r for r in same if r["status"] == "failed"]
        if failed and failed[-1]["approved_ref"].strip().lower() == args.approved_ref.strip().lower():
            raise LedgerError(f"{failed[-1]['outbox_id']} to {args.to} failed. Check Sent Items first; if it isn't there, "
                              f"ask Jesse again and record his new reply words")
        oid = Ledger.next_id(rows, "outbox_id", "O", 4)
        rows.append({"outbox_id": oid, "created_on": dt.datetime.now().isoformat(timespec="seconds"), "kind": args.kind or "",
                     "to_email": args.to, "subject": args.subject, "body_file": args.body_file or "", "approved_by": args.by or "Jesse",
                     "approved_ref": args.approved_ref, "status": "approved"})
        led.write("outbox.csv", rows)
        led.log(f"outbox add · {oid} · {args.kind or ''}")
        return f"{oid} recorded as approved. Send it once, then run: outbox sent {oid}"
    if args.action in ("sent", "failed", "cancel"):
        row = next((r for r in rows if r["outbox_id"] == args.id), None)
        if not row:
            raise LedgerError(f"no outbox item {args.id}")
        if row["status"] != "approved":
            raise LedgerError(f"{args.id} is already {row['status']}")
        if args.action == "sent":
            row.update(status="sent", sent_on=dt.datetime.now().isoformat(timespec="seconds"))
        else:
            row.update(status="failed" if args.action == "failed" else "cancelled", notes=args.why or "")
        led.write("outbox.csv", rows)
        led.log(f"outbox {args.action} · {args.id}")
        return f"{args.id}: {row['status']}."
    if args.action == "check":
        if not args.id:
            raise LedgerError("outbox check needs an email address")
        hits = [r for r in rows if r["to_email"].lower() == args.id.lower()]
        return json.dumps(hits, indent=2) if hits else f"Nothing in the outbox for {args.id}."
    return "\n".join(f"{r['outbox_id']} · {r['created_on'][:10]} · {r['kind']} · {r['to_email']} · {r['status']}" for r in rows) or "Outbox empty."


def scoreboard_numbers(led: Ledger, period: str) -> dict:
    now = dt.date.fromisoformat(today())
    if period == "week":  # the last 7 days, so a Friday post never misses the weekend
        start = now - dt.timedelta(days=6)
    elif period == "last-month":
        now = now.replace(day=1) - dt.timedelta(days=1)
        start = now.replace(day=1)
    else:
        start = now.replace(day=1)
    in_period = lambda d: bool(d) and start.isoformat() <= d[:10] <= now.isoformat()
    partners = led.read("partners.csv")
    refs = led.read("referrals.csv")
    camps = led.read("campaigns.csv")
    cards = led.read("cards.csv")
    won = [r for r in refs if in_period(r["won_on"])]
    paid_in = [r for r in refs if in_period(r["invoice_paid_on"])]
    revenue = sum(((money(r["invoice_ex_gst"]) or Decimal("0")) for r in paid_in), Decimal("0"))
    owed = sum(((money(r["fee_nzd"]) or Decimal("0")) for r in refs if r["fee_status"] in ("owed", "proposed", "approved")), Decimal("0"))
    return {
        "period": period, "from": start.isoformat(), "to": now.isoformat(),
        "partners_active": sum(p["status"] in ("signed", "active") for p in partners),
        "partners_talking": sum(p["status"] == "talking" for p in partners),
        "call_cards": sum(in_period(c["created_on"]) for c in cards),
        "calls_made": sum(c["status"] in ("called", "campaign_agreed", "partner_signed") and in_period(c["updated_on"]) for c in cards),
        "referrals_in": sum(in_period(r["date_in"]) for r in refs),
        "jobs_won": len(won),
        "partner_revenue_paid_ex_gst": fmt(revenue) if paid_in else "",
        "fees_owed": fmt(owed),
        "fees_waiting_on_terms": sum(r["fee_status"] == "terms_not_set" for r in refs),
        "campaigns_sent": sum(c["status"] in ("sent", "done") and in_period(c["partner_sent_on"]) for c in camps),
        "campaign_bookings": sum(count(c["bookings"]) for c in camps if in_period(c["partner_sent_on"])),
        "empty_ledger": not (partners or refs or camps or cards),
    }


def cmd_scoreboard(led: Ledger, args) -> str:
    n = scoreboard_numbers(led, args.period)
    if args.format == "json":
        return json.dumps(n, indent=2)
    if n["empty_ledger"]:
        return "Partner desk: nothing recorded yet (no partners, referrals, campaigns or call cards in the ledger)."
    label = {"week": "Last 7 days", "month": "This month so far", "last-month": "Last month"}[args.period]
    revenue = f"${n['partner_revenue_paid_ex_gst']}" if n["partner_revenue_paid_ex_gst"] else "— (no paid partner invoices yet)"
    lines = [
        f"*Partner desk · {label}* ({n['from']} to {n['to']})",
        f"• Partners: {n['partners_active']} signed/active · {n['partners_talking']} talking",
        f"• Replies turned into call cards: {n['call_cards']} · calls made: {n['calls_made']}",
        f"• Partner campaigns sent: {n['campaigns_sent']} · bookings from them: {n['campaign_bookings']}",
        f"• Referrals in: {n['referrals_in']} · jobs won: {n['jobs_won']}",
        f"• Partner revenue (paid, ex GST): {revenue}",
        f"• Fees owed to partners: ${n['fees_owed']}",
    ]
    if n["fees_waiting_on_terms"]:
        lines.append(f"• {n['fees_waiting_on_terms']} fee(s) waiting on the partner terms (before or after GST?)")
    return "\n".join(lines)


def cmd_dashboard(led: Ledger, args) -> str:
    template = Path(args.template).expanduser() if args.template else Path(__file__).resolve().parent.parent / "dashboard" / "dashboard.template.html"
    html = template.read_text(encoding="utf-8")
    marker_open = '<script id="dash-data" type="application/json">'
    start = html.index(marker_open) + len(marker_open)
    end = html.index("</script>", start)
    data = {
        "updated": dt.datetime.now().strftime("%a %d %b %Y, %H:%M"),
        "month": today()[:7],
        "partners": led.read("partners.csv"), "referrals": led.read("referrals.csv"),
        "payouts": led.read("payouts.csv"), "campaigns": led.read("campaigns.csv"),
        "radar": [], "milestones": json.loads(Path(args.milestones).read_text()) if args.milestones else [],
    }
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out = Path(args.out).expanduser()
    out.write_text(html[:start] + "\n" + payload + "\n" + html[end:], encoding="utf-8")
    return f"Dashboard written to {out}"


def cmd_check(led: Ledger, args) -> str:
    problems = []
    partners = led.read("partners.csv")
    ids = [p["partner_id"] for p in partners]
    if len(ids) != len(set(ids)):
        problems.append("duplicate partner IDs")
    known = set(ids)
    for ref in led.read("referrals.csv"):
        if ref["partner_id"] not in known:
            problems.append(f"{ref['referral_id']} points at unknown partner {ref['partner_id']}")
        if ref["fee_status"] == "owed" and not ref["invoice_paid_on"]:
            problems.append(f"{ref['referral_id']} has a fee owed but no paid invoice")
    terms = led.terms()
    if not terms.get("confirmed"):
        problems.append("partner terms not confirmed yet (before or after GST?)")
    if terms.get("partner_gst", "unset") == "unset":
        problems.append("not decided yet whether GST-registered partners add GST on top of their fee (their payouts are held)")
    return "Ledger check: ok" if not problems else "Ledger check:\n" + "\n".join(f"- {p}" for p in problems)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Smart Contracting partner ledger")
    parser.add_argument("--dir", default=os.environ.get("SCDT_LEDGER_DIR", "~/PartnerDesk"))
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--terms-seed")

    p = sub.add_parser("terms")
    p.add_argument("action", choices=["show", "set"])
    p.add_argument("--rate")
    p.add_argument("--basis", choices=["ex_gst", "incl_gst"])
    p.add_argument("--partner-gst", choices=["unset", "add_if_registered", "never"])
    p.add_argument("--cap")
    p.add_argument("--confirm", action="store_true")
    p.add_argument("--by")

    p = sub.add_parser("partner")
    p.add_argument("action", choices=["add", "set", "list", "find"])
    p.add_argument("id", nargs="?")
    p.add_argument("fields", nargs="*")
    for flag in ("--business", "--type", "--contact", "--email", "--phone", "--suburb", "--status", "--gst", "--list-size", "--notes", "--text"):
        p.add_argument(flag)

    p = sub.add_parser("referral")
    p.add_argument("action", choices=["add", "set", "paid", "list"])
    p.add_argument("id", nargs="?")
    p.add_argument("fields", nargs="*")
    for flag in ("--partner", "--customer", "--suburb", "--job", "--how", "--notes", "--invoice-ex-gst", "--paid-on", "--status"):
        p.add_argument(flag)

    sub.add_parser("recalc")

    p = sub.add_parser("payouts")
    p.add_argument("action", choices=["propose", "approve", "paid", "list"])
    p.add_argument("id", nargs="?")
    p.add_argument("--month", default=today()[:7])
    p.add_argument("--total")
    p.add_argument("--by")
    p.add_argument("--on")
    p.add_argument("--how")

    p = sub.add_parser("campaign")
    p.add_argument("action", choices=["add", "set", "list"])
    p.add_argument("id", nargs="?")
    p.add_argument("fields", nargs="*")
    for flag in ("--partner", "--month", "--theme", "--notes"):
        p.add_argument(flag)

    p = sub.add_parser("card")
    p.add_argument("action", choices=["seen", "add", "set", "list"])
    p.add_argument("id", nargs="?")
    p.add_argument("fields", nargs="*")
    for flag in ("--name", "--business", "--email", "--source"):
        p.add_argument(flag)

    p = sub.add_parser("outbox")
    p.add_argument("action", choices=["add", "sent", "failed", "cancel", "check", "list"])
    p.add_argument("id", nargs="?")
    for flag in ("--kind", "--to", "--subject", "--body-file", "--approved-ref", "--by", "--why"):
        p.add_argument(flag)

    p = sub.add_parser("scoreboard")
    p.add_argument("--period", choices=["week", "month", "last-month"], default="week")
    p.add_argument("--format", choices=["md", "json"], default="md")

    p = sub.add_parser("dashboard")
    p.add_argument("--out", required=True)
    p.add_argument("--template")
    p.add_argument("--milestones")

    sub.add_parser("check")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    led = Ledger(Path(args.dir))
    if args.cmd == "partner" and args.action == "find":
        args.text = args.text or args.id
    if args.cmd == "card" and args.action == "seen":
        args.email = args.id
    if args.cmd == "payouts" and args.action == "approve" and not args.by:
        print("payouts approve needs --by <who approved>", file=sys.stderr)
        return 2
    handlers = {"init": cmd_init, "terms": cmd_terms, "partner": cmd_partner, "referral": cmd_referral,
                "recalc": cmd_recalc, "payouts": cmd_payouts, "campaign": cmd_campaign, "card": cmd_card,
                "outbox": cmd_outbox, "scoreboard": cmd_scoreboard, "dashboard": cmd_dashboard, "check": cmd_check}
    try:
        with led.lock():
            print(handlers[args.cmd](led, args))
    except LedgerError as exc:
        print(f"Not done: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
