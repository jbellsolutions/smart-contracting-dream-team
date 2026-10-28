---
name: scdt-partner-campaign
description: Run a partner's email campaign to their own customer list — draft it from the template for their partner type, get Jesse's yes, send it to the partner to approve, then track what came of it. Use when Jesse says "let's do a campaign with <partner>", when a partner's next_campaign month arrives, or when a partner says they've sent it.
---

# A partner campaign

Load `scdt-business-context` first. If `~/.hermes/scdt/state/PARTNER_CAMPAIGNS_PAUSED` exists, say "Partner campaigns are paused (<reason>). Say 'go again' to restart." and stop.

Justin's rule of thumb (Oct 7 call): one partner campaign a month across the program is all you need; with three or four good partners, each one sends about once every three months. One campaign to a list of a few hundred is worth more than lots of cold email. Get every "yes" to a dated send.

## Steps
1. `ledger partner find "<partner>"` (ledger = `python3 ~/smart-contracting-dream-team/tools/partner_ledger.py`). They must be `signed` or `active`. If they're `talking`, tell Jesse they need to say yes first.
2. Find or add the campaign: `ledger campaign list`; if none for this month, `ledger campaign add --partner <P…> --month <YYYY-MM> --theme "<theme>"`. Pick the theme from `program/campaign-calendar.md` for this month, or Jesse's idea.
3. **Draft** from `program/campaigns/<partner type>.md`: fill `[partner_name]`, `[partner_business]`, `[partner_contact]`, `[ref_code]` and `[offer]` (the offer is what Jesse agreed for this partner; if none, leave the template's default line). Save the filled draft to `~/PartnerDesk/campaigns/<C…>-<partner>.md` (create the folder if it's missing) and `ledger campaign set <C…> status=drafted copy_file=campaigns/<C…>-<partner>.md`.
4. **Jesse's yes.** Fill every `[...]` gap first. Post the whole campaign email in its own thread: "This is the email <partner> would send to their customers. Want me to send it to <contact> to check and approve? Reply **send to partner**, or tell me what to change."
5. **Partner's approval.** On those words, email the partner the brief from `program/emails.md` ("Campaign brief") with the campaign email below it, following "Sending an email" in `scdt-business-context` (kind `campaign-brief`). The partner sends it from their own system to their own list; we never get their list and never send to it.
6. When the partner approves: `ledger campaign set <C…> status=partner_approved`. When they say it's gone out: `ledger campaign set <C…> status=sent partner_sent_on=<YYYY-MM-DD> customers_reached=<number if they say>`, and `ledger partner set <P…> status=active`.
7. **Afterwards.** Replies from that partner's customers come in with the ref code or the partner's name: those are referrals (`scdt-referrals`). After two weeks *(starting value)* ask Jesse once: "Any bookings from <partner>'s campaign? I've logged <n> referrals with their code." Record `ledger campaign set <C…> replies=<n> bookings=<n>` from his answer, then `status=done`.

## Never
- Send anything to a partner's customers. The partner sends; we only send to the partner.
- Change the campaign text after Jesse's yes without showing him again.
- Put the referral fee in the customer-facing email.
- Start a campaign while the pause file exists.
