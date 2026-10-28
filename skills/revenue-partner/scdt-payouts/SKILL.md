---
name: scdt-payouts
description: The monthly partner payout run — propose who is owed what (worked out by the ledger tool), get Jesse's approval, draft the remittance emails, and record what Jesse paid. Use from the monthly-payouts routine, or when Jesse asks "what do we owe partners?", says "approve the payouts" or "I've paid <partner>".
---

# Partner payouts

Load `scdt-business-context` first. Tool: `ledger` = `python3 ~/smart-contracting-dream-team/tools/partner_ledger.py`. **You never pay anyone.** Jesse pays from the business bank account and tells you.

## 1. Propose (monthly routine, or when asked)
1. `ledger payouts propose --month <YYYY-MM>` — the month just finished (in the routine: last month).
2. Post exactly what the tool printed to Jesse, in its own thread, with one line on top:
   "Partner payouts for <month>. These are worked out by the ledger from paid invoices only. Approving doesn't pay anyone. Reply **approve <total>** (for example approve 460.00) to approve exactly this list, or tell me which to hold."
3. If it printed "Nothing owed", post nothing; log `NO_CHANGE`.
4. If it lists anything "Held back" or "Waiting on the partner terms", ask the one question that unblocks it (a partner's GST status, or the GST basis from `scdt-partner-program`). Never pay around it.

## 2. Approve
On Jesse's "approve <total>" in that thread: `ledger payouts approve --total <the total he wrote> --by Jesse`. If the tool says the total doesn't match, the list has changed since he saw it: run propose again, post the new list, and ask again. A bare "approve" or "yes": ask "Approve the payouts totalling <total>? Reply **approve <total>**." Reply: "Approved. Pay them with the bank reference shown (SC-P…-YYYY-MM). Tell me when each is paid and I'll send the remittance note."
"Hold <partner>" means: don't approve. Re-run propose after he's sorted it; the tool replaces the draft.

## 3. Paid
When Jesse says "paid <partner>" (or "paid them all"):
1. `ledger payouts paid <Y…> --on <YYYY-MM-DD> --how "bank transfer"` for each one he names.
2. Draft the remittance note from `program/emails.md` ("Payout remittance") with the amount and reference exactly as the tool printed. Post it in a thread of its own: "Want me to send <partner> this remittance note? Reply **send remittance**." Send it following "Sending an email" in `scdt-business-context` (kind `remittance`).

## Never
- Pay, transfer, or log into a bank.
- Change an amount. If Jesse wants a different amount, ask him to check the invoice figure; the referral is fixed with `ledger referral paid` by Jesse's word, not by editing the payout.
- Tell a partner an amount before it's approved.
