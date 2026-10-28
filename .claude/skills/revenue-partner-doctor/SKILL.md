---
name: revenue-partner-doctor
description: Find out why the Revenue Partner has gone quiet in Slack and get it going again — check the simple things, then open its Orgo computer in the browser and restart its gateway with Jesse's yes. Use when Jesse says "it's gone quiet", "no drafts this morning", "it's not replying", "restart the Revenue Partner", or after an upgrade it can't find its new skills.
---

# Revenue Partner doctor

The Revenue Partner lives on an Orgo computer and talks to Slack through a "gateway" (Hermes's connection to Slack). On Oct 13 the gateway stopped and nothing told anyone. This is the fix that worked then, done for Jesse. Read before you change anything, and restart only with his yes.

## 1. The quick checks (no browser yet)
Ask Jesse, one at a time:
1. "Send it a one-word message in your DM, like 'ping'. Did it answer within a couple of minutes?" If yes: it's alive; ask what made him think it was quiet (no drafts this morning? It might be a credit or schedule problem; go to 3).
2. "Did anything change: a new laptop, a password change, Slack logged you out, Orgo sent an email?"

## 2. Open its computer
1. Use the browser built into the Claude app (or Claude in Edge). Open https://www.orgo.ai and let **Jesse log in himself** if asked. Never type his password.
2. Open the workspace with the Revenue Partner's computer and open that computer's **terminal**. If the computer shows as stopped or asleep, ask: "Its computer is switched off. Want me to start it? It just boots the computer; nothing gets sent. Reply yes or no." Start it only on yes, then wait for it to come up.

## 3. Look (read only)
Type these in the Orgo terminal and read the answers:
- `hermes gateway --help` (to see which commands this version has)
- `hermes profile list` (there are several profiles; the Revenue Partner is the one connected to Slack)
- `hermes -p <that profile> gateway status` (or `hermes gateway status` if there's only one)
- `hermes cron list` (are `daily-partner-drafts` and `partner-reply-check` there and active?)
- `tail -n 40 ~/.hermes/logs/gateway.log` (if that file exists; look for "credit", "401", "429", "disconnected")

Tell Jesse in two lines what you found, e.g. "The gateway is stopped. Everything else looks fine." Common causes:
| You see | It means | Fix |
|---|---|---|
| Gateway stopped / not running | The Slack connection died | Restart (step 4) |
| "insufficient credits", 402, OpenRouter errors | The OpenRouter credit ran out | Jesse tops up at openrouter.ai → Credits; then restart |
| 401 / "invalid_auth" from Slack | The Slack app lost its token | Justin's team; don't touch |
| Cron jobs paused | Someone paused the morning drafts | Ask Jesse; resume only on his yes with `hermes cron resume <name>` |

## 4. Restart (only on Jesse's yes)
Ask: "Want me to restart its Slack connection? It takes about a minute and nothing gets sent. Reply yes or no."
On yes: `hermes -p <profile> gateway restart` (if the help showed no `restart`, use `stop` then `start`). Wait a minute, run the status command again, then ask Jesse to send "ping" again.

## 5. If it's still quiet
Stop. Don't try other fixes. Write Jesse a short note to send Justin: what you checked, what each command said (no keys or tokens; cut anything that looks like one), and what's still wrong. Suggest he sends it with a voice note.

## Never
- Type a password, key or token, or copy one out of the computer.
- Delete or edit files on the Orgo computer, change its config, or install anything.
- Change cron jobs other than resuming the two existing outreach jobs on Jesse's yes.
- Restart more than once in one go.
