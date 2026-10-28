---
name: scdt-referrals
description: Log every job a partner sends in and follow it to a paid invoice, so the partner fee is right. Use when Jesse says a partner sent someone ("<name> from <partner> rang about their drains"), when a customer mentions a partner or a ref code like SC-P004, when a referred job is quoted, won or lost, and when its invoice is paid.
---

# Referrals

Load `scdt-business-context` first. Tool: `ledger` = `python3 ~/smart-contracting-dream-team/tools/partner_ledger.py`.

## A referral comes in
1. Work out the partner: the ref code (`SC-P…`), the partner's name, or Jesse's words. `ledger partner find "<code or name>"`. If it matches more than one, ask Jesse which.
2. `ledger referral add --partner <P…> --customer "<customer name>" --suburb "<suburb>" --job "<what they need>" --how "<phone, email, campaign C…, intro>"`
   The tool refuses a duplicate while the first referral for that customer is still open (new, quoted or won). If it does, tell Jesse it's already logged as R… and stop. A customer whose earlier job is done or lost can be logged again for a new job.
3. Reply in one line: "Logged R0007: <customer> from <partner>." If the partner hasn't been thanked for a referral before, offer the thank-you from `program/emails.md` in a thread of its own: "Want me to send <partner> this quick thanks (below)? Reply **send thanks**." Send it following "Sending an email" in `scdt-business-context` (kind `thanks`).

## The job moves on
| Jesse says | Run |
|---|---|
| "quoted <customer>, 8,400" | `ledger referral set <R…> status=quoted quote_ex_gst=8400` (ask "is that before GST?" if he doesn't say) |
| "won it", "going ahead" | `ledger referral set <R…> status=won` |
| "lost it", "they went elsewhere" | `ledger referral set <R…> status=lost notes="<his words>"` |
| "<customer>'s invoice is paid, 12,000 before GST" | `ledger referral paid <R…> --invoice-ex-gst 12000 --paid-on <YYYY-MM-DD>` |
| "that invoice was actually 11,500" | Run `referral paid` again with the right figure. If that month's payouts were only proposed, the tool cancels the proposal and says so: run `scdt-payouts` propose again. Once approved or paid, the tool refuses: tell Jesse and Justin's team |

**The paid amount comes from Jesse (or Mike) only, before GST, for the whole job.** If he gives a figure including GST, ask: "Is that including GST? I need the amount before GST." Never divide by 1.15 yourself, never estimate.

Say what the tool printed, word for word for any money. If it says the terms aren't confirmed, ask Jesse the GST-basis question from `scdt-partner-program` once.

## Who referred whom
If two partners claim the same customer, the first logged introduction with a ref code wins (`program/terms.md`). Show Jesse both records and let him decide; note his decision in the referral's `notes`.

## Never
- Work out or change a fee yourself. Fee fields are written only by the tool.
- Mark an invoice paid on anyone's word but Jesse's or Mike's.
- Tell a partner a fee amount before Jesse has approved that month's payouts.
