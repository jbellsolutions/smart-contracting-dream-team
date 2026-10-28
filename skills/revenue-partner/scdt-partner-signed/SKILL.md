---
name: scdt-partner-signed
description: Sign up a new partner after Jesse's call — add them to the partner ledger, give them a reference code, ask the two money questions, draft the welcome email and pencil in their first campaign. Use when Jesse says someone is "in", "signed", "keen to do it", or "add <business> as a partner"; also to update a partner's details or status.
---

# A partner says yes

Load `scdt-business-context` first. Tool: `python3 ~/smart-contracting-dream-team/tools/partner_ledger.py` (below: `ledger`).

## Steps
1. **Find or add them.** `ledger partner find "<business or email>"`.
   - Not there: `ledger partner add --business "<business>" --type "<building inspector | real estate | property manager | trade | other>" --contact "<name>" --email "<email>" --phone "<phone>" --suburb "<suburb>" --status signed`
   - There: `ledger partner set <P…> status=signed`
   Take every detail from Jesse's message, the call card or the reply. Leave out what you don't know; never guess.
2. **The two questions Jesse may not have asked on the call.** Ask in one message, phone-sized:
   "Two quick ones for <business>: 1) Are they GST registered? (yes / no / don't know) 2) Roughly how many customers are on their email list?"
   Record: `ledger partner set <P…> gst_registered=<yes|no|unknown> list_size=<number>`.
3. **Draft the welcome email** from `program/emails.md` ("Welcome"), filled with their name, their reference code (the `ref_code` the tool gave, like `SC-P004`) and the question about a first campaign month. Fill every `[...]` gap first (ask Jesse for anything you don't know). Post it to Jesse in a new thread of its own: "Want me to send this welcome to <name> at <email>? Reply **send welcome** to send it." On those words, send it following "Sending an email" in `scdt-business-context` (kind `welcome`).
4. **Pencil in the first campaign.** Suggest a month in the welcome. When the partner or Jesse names one: `ledger partner set <P…> next_campaign=<YYYY-MM>` and `ledger campaign add --partner <P…> --month <YYYY-MM> --theme "<theme from program/campaign-calendar.md>"`.
5. **The agreement.** If Jesse wants it in writing, attach `program/agreement-DRAFT.md` only after Jesse confirms their lawyer has checked it. Until then, say: "The agreement is still a draft for your lawyer. Want to send the one-pager instead?"
6. Reply to Jesse in one line: "<business> is in as <P…> (ref <code>). Welcome email ready for your yes. First campaign: <month or 'not set'>."

## Changing a partner
`ledger partner set <P…> field=value …` for any of: status (talking, signed, active, paused, ended), contact_name, email, phone, suburb, gst_registered (yes, no or unknown), list_size, next_campaign (YYYY-MM), last_contacted (YYYY-MM-DD), notes (each note is added to the earlier ones, never replaces them). Status `active` once their first campaign has gone out. `ended` when Jesse says they're done; their owed fees still get paid.

## Never
- Promise a fee different from `program/terms.md`, or a custom deal, unless Jesse tells you the exact terms. A custom rate goes in with `ledger partner set <P…> fee_rate=<0.0x> fee_basis=<ex_gst|incl_gst>` and Jesse's words in `notes`.
- Send the welcome or the agreement without Jesse's exact reply words.
- Add someone as signed who only said "maybe" — that's `talking`.
