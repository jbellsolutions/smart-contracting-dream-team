# Jesse's AI team: the partner program, done for you

This folder gives Smart Contracting's Revenue Partner the whole partner program, from the first warm reply to the partner's payout: call cards with what to say, signing partners up, their campaigns (about one partner campaign a month across the program), every referral, the 5% fee worked out properly, a payout list each month and a scoreboard on Fridays that Mike can read. It also gives Jesse a workshop on his own PC: a homeowner lead radar that reads the local Facebook groups he's already in, partner packs, call coaching, and one-message fixes when the Revenue Partner goes quiet. Nothing to sign up for, nothing to learn.

**Platform:** Hermes overlay (the Revenue Partner, already running on Orgo) plus Claude Code on Jesse's PC.

## How to start
- **Jesse:** open this folder in the Claude app's **Code** tab and say "set me up". Then "upgrade the Revenue Partner". The plain-English guide is [`docs/GUIDE.md`](docs/GUIDE.md).
- **The Revenue Partner:** [`START-HERE.md`](START-HERE.md) (arrives inside `dist/revenue-partner-upgrade.zip`).
- **Justin's team, installing from Orgo instead:** put this repo at `~/smart-contracting-dream-team` on the Orgo computer, run `bash ~/smart-contracting-dream-team/install/install.sh revenue-partner`, then send the agent the message it prints.

## What's inside

| Path | What |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | The Workshop's menu and rules (Claude Code reads this) |
| [`docs/GUIDE.md`](docs/GUIDE.md) | Jesse's guide |
| [`PROJECT_CHARTER.md`](PROJECT_CHARTER.md) | Why, objectives, the team, rules, who keeps which record, milestones |
| `agents/` | One charter per part of the team (90+ are later milestones) |
| `skills/` | The Revenue Partner's new skills (`scdt-…`) |
| `routines/` | Its scheduled jobs. All are created paused |
| `tools/partner_ledger.py` | The only place partner fees and payouts are worked out, and the send-once outbox for partner emails (tested: `python3 tools/test_partner_ledger.py`) |
| `tools/credit_check.py` | Prints the remaining OpenRouter credit without ever showing the key |
| `program/` | The partner program: terms, scripts, emails, campaign templates, one-pagers, agreement draft, NZ rules |
| `.claude/skills/` | The Workshop's 7 skills: getting started, lead radar, partner prospects, partner pack, call coach, upgrade, doctor |
| `radar/` | Radar groups, search terms, storm-day plan |
| `dist/` | The upgrade zip and the upload test file |
| [`policies/APPROVALS.md`](policies/APPROVALS.md) | What each part may do alone, and the plain-English rule |
| [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md) | What only Jesse can answer |
| [`docs/BUILD-RECORD.md`](docs/BUILD-RECORD.md) | What's specified, built and actually running |

## For Justin's team: rebuilding the zip
After changing anything the Revenue Partner uses, run `python3 scripts/build_pack.py` on a Mac or Linux machine and commit `dist/revenue-partner-upgrade.zip`. `python3 scripts/build_pack.py --check` fails if the zip is stale.

Built by Justin's team with the client-build system (2026-10-27).
