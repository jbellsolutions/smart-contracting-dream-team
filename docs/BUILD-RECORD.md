# Build record

This record keeps what's specified, what's built and what's actually running separate, and honest. Justin's team updates this file; the bots never do. The Revenue Partner keeps the live list of what's switched on in `~/.hermes/scdt/routines-on.md`.

**Where it stands (2026-10-27): built and checked here; not installed.** Everything below exists as files in this repo. Nothing is installed on the Revenue Partner's computer or switched on for Jesse until the upgrade is installed (`START-HERE.md`) and the agent reads back what it created.

## Status by piece

- **Specified:** the job is written down.
- **Built in repo:** the file the bot uses exists here (and, for code, its tests pass here).
- **Active:** it's running on Jesse's account and has been read back.

| Piece | Specified | Built in repo | Active |
|---|---|---|---|
| Project charter, approvals, data rules | Yes | `PROJECT_CHARTER.md`, `policies/` | Not yet |
| Revenue Partner upgrade (charter, 10 skills, 5 paused routines) | Yes | `agents/01-revenue-partner.md`, `skills/revenue-partner/`, `routines/` | Not yet |
| Partner ledger tool, with the send-once outbox | Yes | `tools/partner_ledger.py`; 27 tests pass on macOS, Python 3 (`tools/test_partner_ledger.py`) | Not yet; not yet run on the Orgo computer |
| Credit check | Yes | `tools/credit_check.py`; prints the balance, never the key. Checked here only with no key present | Not yet; not yet run against their OpenRouter key |
| Installer and upgrade zip | Yes | `install/`, `scripts/build_pack.py`, `dist/` | Not yet; dry-run against a throwaway Hermes home only |
| Partner program documents | Yes | `program/` | n/a (documents) |
| Workshop (Claude Code): menu and 7 skills | Yes | `CLAUDE.md`, `.claude/skills/` | Not yet; Facebook lane not yet proven with Jesse's account |
| Ops agent, LeadConnector link, quote reactivation | Reserved | `agents/90–92` | Later milestones |

## Sources

| Source | Date (NZ) | Transcript | Digest |
|---|---|---|---|
| Kick-off call | Sep 16 (US date) | Read AI | `source/digests/2026-09-16.md` |
| Call | Sep 17 | Read AI | `source/digests/2026-09-17.md` |
| Call | Sep 18 | Read AI recording errored: no transcript | none |
| Call | Sep 23 | Read AI | `source/digests/2026-09-23.md` |
| Call | Sep 30 | Read AI | `source/digests/2026-09-30.md` |
| Call | Oct 7 | Read AI | `source/digests/2026-10-07.md` |
| Call | Oct 13 | Read AI | `source/digests/2026-10-13.md` |
| #mike-and-jesse-drainage (Slack Connect) | Sep 16 to Oct 28 | Full export, credentials redacted | `source/slack/channel-timeline.md`; Slack digest parts |
| Drafts shared in Slack (one-pager, daily routine and pipeline, reply and phone playbook) | Oct 9 | `source/slack/files/` | used for `program/` |

(Paths above are in the client folder, outside this repo.)

## Platform facts this build relies on

| Fact | Status |
|---|---|
| Hermes caches documents sent in a Slack DM (any extension up to 20 MB, `.zip` and `.md` included) | Verified in Hermes source (Slack adapter, document cache); **unverified on their Hermes version**: the upload test (`dist/canary.md`) checks it first |
| Hermes loads skills from category folders (`~/.hermes/skills/<category>/<skill>/SKILL.md`) | Seen live on their box (`go-to-market/smart-contracting-outreach`) |
| `/reload-skills` re-scans skills without a restart | Verified in Hermes source; may not exist on their version (fallback: gateway restart via the doctor) |
| `hermes [-p <profile>] gateway status|restart`, `hermes cron list` | Verified in Hermes source; the doctor checks `--help` first |
| The Revenue Partner runs as root with the project in `/root/revenue-partner-relaunch` | Seen live (Oct 13 call, Slack) |
| Claude Code's WebFetch/WebSearch can't read Facebook, Reddit, PropertyTalk, Builderscrack or MetService | Measured in this build |
| Claude Code project `settings.json` permissions apply after the folder is trusted | Claude Code docs |
| OpenRouter `/api/v1/credits` and `/api/v1/key` report remaining credit | OpenRouter docs; unverified with their key |
| Hermes keeps `OPENROUTER_API_KEY` out of tool subprocesses | Verified in Hermes source; so `credit_check.py` reads `~/.hermes/.env` inside its own process |
| Cron jobs run in `HERMES_TIMEZONE`, then config.yaml `timezone`, then the server clock; their existing jobs show UTC (7:30 AM NZDT appears as 18:30) | Order verified in Hermes source; UTC seen in their cron list. Each routine carries `CRON:` (UTC) and `CRON_NZ:`; START-HERE Step 4 picks one read-only |
| `hermes cron` can create a job paused and deliver to `origin` | Verified in Hermes source; may differ on their version, so Step 5 stops if it can't |

## Review findings

An independent reviewer (a fresh Opus subagent given the transcripts, digests, Slack export and this repo, not the builder's summary) looked for missing asks, invented facts, unsafe outward actions and install steps that would fail cold. Everything it confirmed is below.

| # | Finding | What was done |
|---|---|---|
| H1 | Correcting a paid invoice after payouts were proposed could pay the fee twice | `referral paid` now cancels the open proposal and says so; approved or paid fees are locked. Test added |
| H2 | A bare "yes" could approve the wrong email, and nothing recorded what was sent | Every email has its own thread and reply words (**send welcome**, **send reply**, **send to partner**, **send thanks**, **send remittance**, **send check-in**); a bare "yes" approves nothing new. Each send is recorded in the ledger's outbox first and goes once, then is marked sent, or failed after checking Sent Items. Payouts are approved with the exact total (**approve 460.00**) |
| H3 | Call cards assumed a 30-minute reply check and a replies file | The reply check was cut to twice a day on Oct 9 to save credit. Call cards now read replies wherever `sources.md` says (a folder, a file or the tracker's columns) and stop with one message if that's unknown. Cadence text fixed everywhere |
| H4 | Routines were written in NZ time, the box runs crons in UTC, and the installer suggested changing the clock | Each routine has a UTC `CRON:` and a `CRON_NZ:`; Step 4 reads the time-zone setting without changing it; the clock suggestion is gone. Call cards check for an NZ weekend themselves |
| M1 | Jobs could be created live and paused afterwards, or put in the system crontab | Created paused in the same call, delivered to `origin`; a failure stops the install; never the system crontab |
| M2 | A re-run would duplicate jobs, re-ask the GST question and edit SOUL.md and memory | Step 5 updates existing `scdt-` jobs in place; Step 6 skips the question when terms are confirmed; no SOUL.md or memory edits (see "Deviations") |
| M3 | The installer told the agent to skip the inventory even when it hadn't run | It now says "Step 1, then Steps 3 to 6" while `sources.md` still has UNKNOWN paths |
| M4 | `grep -c` returning 1 would abort the install under `set -e` | `|| true` |
| M5–M9 | Ledger: GST worked on the unrounded fee; no rule for partners who add GST; changed terms stayed confirmed; a custom rate skipped confirmation; negative amounts and bad dates accepted; paused or ended partners' fees held; a customer's second job blocked; notes overwritten | Each fixed in `tools/partner_ledger.py` with a regression test |
| M9 | The storm-day plan pointed at a partners file the Workshop doesn't keep; a partner pack could state a GST basis the ledger didn't share | Storm day asks the Revenue Partner who's signed; the pack reminds Jesse to tell the Revenue Partner the same GST answer |
| M10 | Packs and emails could go out with `[...]` placeholders still in them | Both now refuse: fill from Jesse or take the line out |
| M11 | "Not interested" on a call card never reached the never-email list | It runs the outreach skill's own decline step (name and address match) |
| M12 | Ask #22 and the charter said a `verifalia-daily-max` job is running; Slack never shows one | #22 is open; Step 1 checks |
| M13 | Partner emails could go without Jesse's required sign-off | `scdt-business-context` "Sending an email" adds it every time |
| Credit | The credit skill would have had the model read the key, which Hermes also keeps out of subprocesses | `tools/credit_check.py` reads it inside its own process and prints only the balance |
| Low | `/reload-skills` is typed by Jesse, not the agent; the inventory didn't give the `sources.md` line format or `send_with`; a Hermes home outside `~/.hermes` would install where nothing looks; the ask-ledger posted to a scoreboard that never loads it; call cards posted before recording; the overlay sync could later overwrite a file it never wrote; Windows `explorer.exe` reports an error when it works; the upgrade message had a literal path placeholder; the radar's list template had 15 columns but the skill named 12; the Claude Code deny list missed `wget`, `curl.exe`, `Invoke-RestMethod`, `iwr`, `irm`; the zip left out `radar/storm-day.md`, which two program docs cite | All fixed |
| Asks | Attribution: rows 3, 17, 42, 60 and 66 were raised by the build or Justin, not the client; row 2 came from Jesse's Sep 23 emails; #39 also came up on Oct 5. Missing: no second email to anyone contacted (Oct 14), name-matching suppression (Oct 20), counting "we're covered" replies (Oct 21), report what was actually sent (Oct 20), Slack access to all chats (Sep 16 call) | Sources corrected; rows 68–72 added; the scoreboard now counts "covered" replies and actual sends |
| Second pass | A failed send could never be re-sent, even on Jesse's new reply words; payout totals typed as "$1,234.5" were untested; routine headers, the charter and the Mike scoreboard question still used a bare "yes" or the 30-minute wording | The outbox allows a re-send only with new reply words (test added); a test proves `$`, commas and a missing cent are accepted and a wrong total refused; wording fixed (Mike: **send Mike weekly**) |
| Not adopted | A suggested Justin promise at the Oct 13 call [09:50] | Checked the transcript: it describes Orgo's new interface, not a promise. Not added |

**Deviations from the package standard**
- **Profile kept in a skill, not SOUL.md.** The standing role is in `scdt-business-context` ("Who you are in this work"). Their agent's memory was full on Oct 20 and it has approvals that changed what it does; editing its persona would touch the one file the overlay promises to leave alone.
- **Cold test.** The planned cold run with `claude -p` couldn't start (the CLI wasn't logged in on this Mac). A fresh subagent read the repo cold instead and followed `START-HERE.md` and `CLAUDE.md` as written; its findings are in the table above. A real install on their Hermes version is still the first true run.

## Open items and who owns them

| Item | Owner | Next action |
|---|---|---|
| GST basis of the 5% (Q1, Q2) | Jesse | Answer the Revenue Partner's question after install |
| Jesse's refined playbook and one-pager (Q3) | Jesse | Drop them in Slack; Justin's team swaps them into `program/` |
| Logins-and-keys check-up (Q7) | Justin's team | Details in the private client notes, not in this repo |
| Gateway watchdog | Justin's team | Add a supervisor that restarts the gateway and posts once |
| Hosted radar for Christchurch | Justin's team | Switch on; leads to Slack |
| Upload test and first install | Jesse (with Claude Code) | `upgrade-revenue-partner` |
| First Facebook radar run | Jesse (with Claude Code) | "set me up", then "run the radar" |
| Send stagger: approved emails went out close together on Oct 21 and again on Oct 28 (four within about two minutes, per the agent's log), against the staggered sending Jesse asked for on Oct 20 (Justin's 5–15 minute gap; the agent's own rule says 15+ minutes) | Justin's team | Check the existing sending skill; the upgrade doesn't touch it |
| A separate Verifalia job (#22) | Justin's team | Confirm whether the daily run uses the free checks every day |
| How the agent sends one email (`send_with`) | Justin's team | Fill it in `sources.md` if the inventory can't; until then partner emails are shown to Jesse to copy into Outlook |
| Slack access to all their chats (#72) | Justin's team | Slack app scopes, if Jesse still wants it |
| "No home channel" notice back on Oct 28 | Justin's team | Set the home channel on the Revenue Partner's computer |
| Memory filling up (Oct 20) | Justin's team | Review the agent's memory settings |
| Standing command approvals on the Revenue Partner's computer | Justin's team | List them; narrow any that are broader than intended |
| Pricing gaps in the playbook (Q11) | Jesse | Answer; then swap the placeholders in `program/` |

## What Justin owes

See [`OPEN_QUESTIONS.md`](../OPEN_QUESTIONS.md) → "Owed by Justin's team".

## Change log

| Date | Change | Asks |
|---|---|---|
| 2026-10-27 | First build | #1–#67 |
| 2026-10-27 | Independent review applied (table above) | #68–#72 added; #22 reopened |
