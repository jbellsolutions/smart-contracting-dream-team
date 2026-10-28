---
name: scdt-partner-nurture
description: Keep signed partners warm — find the ones who've gone quiet or whose campaign month has arrived, and draft one short, human check-in each for Jesse's yes. Use from the partner-nurture routine, or when Jesse asks "who should I chase?" or "who's gone quiet?".
---

# Partner nurture

Load `scdt-business-context` first. If `~/.hermes/scdt/state/PARTNER_CAMPAIGNS_PAUSED` exists, only list who's due (no drafts) and stop.

## Who's due
From `python3 ~/smart-contracting-dream-team/tools/partner_ledger.py partner list --status signed,active` and `campaign list`:
- signed but no campaign sent yet, signed more than 2 weeks ago *(starting value)*;
- `next_campaign` is this month and that campaign isn't `sent`;
- active, but nothing sent and no referral for 6 weeks *(starting value)*;
- a referral of theirs was paid this month (a thank-you, not a chase).
Also card status `called` with a partner still `talking` for more than a week: a nudge to Jesse to call back, not an email.

## Drafts
At most 3 drafts a run, oldest first. For each, use "Quiet-partner check-in" (or "Thank you") from `program/emails.md`; two to four lines, about them, not about us; one concrete next step (a campaign month, a quick call). Jesse's in-person idea is welcome: if they're local, offer "or a coffee if you're round <suburb>". No fee talk unless it's a thank-you with a paid referral.

Fill every `[...]` gap first. Post each in its own thread: "<partner> has been quiet since <date>. Want me to send this check-in? Reply **send check-in**." (For a thank-you: **send thanks**.) Send it following "Sending an email" in `scdt-business-context` (kind `check-in` or `thanks`), then `ledger partner set <P…> last_contacted=<YYYY-MM-DD>`.

If nobody is due, post nothing and log `NO_CHANGE`.

## Never
- Send more than one chase to a partner in two weeks (check `last_contacted`).
- Chase someone whose status is `paused` or `ended`, or who is on the suppression list.
