# The lead radar

Finds homeowners and landlords in Christchurch and Canterbury who are asking, in public, for the drain work Smart Contracting wants, and drafts a helpful reply for each. Jesse posts the replies himself. Run it from Claude Code: "run the radar". The skill is [`.claude/skills/lead-radar/SKILL.md`](../.claude/skills/lead-radar/SKILL.md).

| File | What |
|---|---|
| [`groups.md`](groups.md) | The Facebook groups it reads (only ones Jesse is already in, up to 8) |
| [`searches.md`](searches.md) | What it looks for, in tiers: bigger repairs first |
| [`storm-day.md`](storm-day.md) | What to do when MetService warns of heavy rain |
| `../data/radar.csv` | The list it keeps. Stays on Jesse's PC |

## No sign-ups, nothing to pay
It uses Jesse's own browser and the Facebook account he already has. Nothing is installed, no new accounts.

## What it can't reach yet, and the upgrade
Claude Code's own web tools can't read Reddit, Facebook or the NZ trade-job sites (they block it or need a login). That's the tool's limit, which is why Facebook goes through Jesse's browser. Reddit, wider Google searches and a daily schedule (without Jesse's PC being on) come with **Justin's hosted radar**, which Justin's team switches on for Smart Contracting's area. Its leads arrive in Slack; tell Claude Code "add these to the radar list" to keep everything in one place.
