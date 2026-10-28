---
name: scdt-scoreboard
description: One short weekly scoreboard so Jesse and Mike see results at a glance — outreach sent and replies, call cards, partners, campaigns, referrals, jobs and fees — plus the partner board page. Use from the weekly-scoreboard routine, or when Jesse or Mike ask "how are we going?", "where are the results?" or "send Mike the numbers".
---

# Scoreboard

Load `scdt-business-context` first. Every number names where it came from. A number you couldn't read is UNKNOWN, never 0.

## Build it
1. Partner numbers (from the ledger, never worked out by you):
   `python3 ~/smart-contracting-dream-team/tools/partner_ledger.py scoreboard --period week`
   On the first Friday of a month, also run it with `--period month` and post that instead.
2. Outreach numbers (read only) from the outreach tracker at the path in `~/.hermes/scdt/context/sources.md` (`tracker:`): emails actually sent this week (sent, not drafted or approved: Jesse's "what have you sent is only what matters"), replies this week and how many of those said they're already covered or not looking for a supplier, people suppressed this week, and **drafts waiting on Jesse's yes right now** (every draft not yet sent or rejected, however old; Jesse asked "how many drafts do you have ready to send all up" on Oct 28). Count rows; quote the file and the time you read it. If you can't read it: "Outreach: UNKNOWN (couldn't read the tracker)".
3. Credit: if `scdt-credit-watch` is on, add one line with the last balance it recorded.

## Post it
One Slack message to Jesse, phone-sized, no more than 10 lines:
```
📊 Week to Fri <date>
Outreach: <n> emails sent · <n> replies (<n> "we're covered") · <n> drafts waiting on your yes (<tracker file>, read <time>)
<the ledger tool's lines, as printed>
Next up: <one line: the oldest call card not called, or the next campaign, or a fee waiting on terms>
```
Then, only the first time: "Want me to send Mike this scoreboard every Friday too? Reply **send Mike weekly**." On those words (a bare "yes" doesn't count), record Mike's preferred channel in `context/owner.md` and send it to him each week after (a standing approval for this exact report; record it in `context/standing-approvals.md` with Jesse's words).

## The board (optional)
When Jesse asks for "the board" or "the whiteboard":
`python3 ~/smart-contracting-dream-team/tools/partner_ledger.py dashboard --out ~/PartnerDesk/partner-board.html`
and attach the HTML file to the Slack message. It opens in any browser.

## If nothing happened
Still post the scoreboard on Fridays (Mike wants to see it), but keep it to three lines.
