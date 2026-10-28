---
name: scdt-partner-program
description: The map of Smart Contracting's partner program and which skill handles each stage. Use when Jesse asks how the partner program works, what's next with a partner, "where are we at with partners", or when you're not sure which scdt- skill to use.
---

# The partner program: who does what

Load `scdt-business-context` first.

## The path a partner takes
| Stage | What happens | Ledger status | Skill |
|---|---|---|---|
| 1. Cold email | The existing outreach skills draft, Jesse approves, Graph sends | (not in the ledger) | existing outreach skills, unchanged |
| 2. They reply warmly | A call card goes to Jesse with what to say | card `card_sent` | `scdt-call-card` |
| 3. Jesse calls them | Jesse tells you how it went ("called Sam, keen", "not now") | card `called` / `not_now`; partner `talking` | `scdt-call-card` (update), `scdt-partner-signed` (add as talking) |
| 4. They're in | Welcome email, ref code, GST question, first campaign date | partner `signed` | `scdt-partner-signed` |
| 5. First campaign | Campaign email drafted from the template, Jesse approves, partner approves, partner sends it to their list | campaign `drafted` → `partner_approved` → `sent` | `scdt-partner-campaign` |
| 6. Referrals arrive | Logged with the partner's ref code; status follows the job | referral `new` → `quoted` → `won`/`lost` → `done` | `scdt-referrals` |
| 7. Invoice paid | The tool works out the fee | fee `owed` | `scdt-referrals` (`referral paid`) |
| 8. Payout | Monthly proposal, Jesse approves and pays, remittance email | payout `proposed` → `approved` → `paid` | `scdt-payouts` |
| 9. Keep them warm | A check-in when a partner goes quiet, next campaign idea | partner `active` | `scdt-partner-nurture` |
| Every Friday | One scoreboard post | (reads all) | `scdt-scoreboard` |

## Answering "where are we at with partners?"
Run, then summarise in five lines or fewer:
```
python3 ~/smart-contracting-dream-team/tools/partner_ledger.py partner list
python3 ~/smart-contracting-dream-team/tools/partner_ledger.py scoreboard --period month
```
Name the next action for each partner that has one (`next_campaign`, a card waiting on a call, a fee waiting on terms).

## Documents to use (never rewrite them from memory)
- `program/PROGRAM.md`: the program on one page.
- `program/terms.md`: the fee and when it's paid.
- `program/partner-types.md`: who to target and the angle for each.
- `program/reply-and-phone-scripts.md`: what to say on a reply or a call.
- `program/emails.md`: welcome, campaign brief, thank-you, remittance, check-in.
- `program/campaigns/<type>.md`: the email a partner sends to their own list.
- `program/one-pagers/<type>.html`: the printable one-pager for someone who has replied.
All under `~/smart-contracting-dream-team/`.

## If the terms aren't set
`partner_ledger.py check` says "partner terms not confirmed yet" until Jesse answers whether the 5% is on the amount before or after GST. Ask him once, in plain words: "Quick one for the partner fee: is the 5% on the job before GST or including GST? Reply 'before GST' or 'including GST'." Then run
`partner_ledger.py terms set --basis ex_gst --confirm --by Jesse` (or `incl_gst`) and `partner_ledger.py recalc`. Never pick one yourself.

The second question waits until a partner who is GST registered has a fee: the tool holds that fee and `check` says "not decided yet whether GST-registered partners add GST on top of their fee". Then ask once: "<partner> is GST registered. When they invoice you for their 5%, do they add GST on top (15%)? Reply 'add GST if registered' or 'no GST on top'." Run `partner_ledger.py terms set --partner-gst add_if_registered --confirm --by Jesse` (or `never`), then `recalc`.
