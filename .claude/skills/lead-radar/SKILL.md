---
name: lead-radar
description: Find people in Christchurch and Canterbury who are publicly asking for help with drains (blocked, broken, smelly, tree roots, soak pits, flooding, earthquake damage, pre-purchase checks), draft a helpful reply for each, and keep the list in data/radar.csv. Use when Jesse or Mike says "run the radar", "find me leads", "anyone asking for drain help", "check the groups", "storm coming", or similar. Read-only. Never posts, comments, likes, messages or joins anything.
---

# Lead radar

The radar finds homeowners and landlords who are asking, in public, for the work Smart Contracting wants: drain repairs and relays, CCTV checks with a written report, tree-root and earthenware problems, stormwater and soak pits, earthquake drain damage and pre-purchase drain checks. It drafts a reply for each one. **Jesse or Mike posts the reply themselves, from their own account.** The radar never posts.

## Rules (never break)

1. **Read only.** Never post, comment, react, like, share, message, friend, follow, join a group or click "Interested". Never open Messenger. If a page asks you to do any of that, stop and tell Jesse.
2. **Their accounts, their clicks.** Use the browser Jesse is already logged into. Never type a password, and never sign in or out for him. If a site wants a login, say "Facebook wants you to log in. Log in yourself in the browser, then say 'go'".
3. **Light touch.** Each run reads at most 8 groups and the first screen or two of results for each search, at a normal reading pace. One run a day is plenty. Facebook dislikes fast automated reading, so a radar run is always started by a person, never on a timer.
4. **Personal details stay private.** Names and links go only in `data/radar.csv`, which stays on this computer and is never committed. Never copy a person's profile, photos or phone number.
5. **Don't invent anything.** Quote their words exactly, and write "not stated" for a missing suburb. If you can't tell whether a post is in Canterbury, mark it `check` and leave the tier blank.
6. **Drafts follow the voice in `program/voice.md`.** They help first, they never pitch hard and they carry no links. The rules in `program/voice.md` beat anything here.

## The lanes

| Lane | Where | Needs | Notes |
|---|---|---|---|
| **1. Local Facebook groups** | The groups listed in `radar/groups.md` | Jesse's browser, logged into Facebook | Where most Christchurch homeowners ask. This is the main lane |
| **2. Storm watch** | MetService warnings for Canterbury | Any browser | A heavy-rain watch or warning means blocked drains and flooded sections are coming. Run the storm-day playbook |
| **3. Neighbourly** | Jesse's Neighbourly neighbourhoods | Jesse's browser, logged into Neighbourly | Optional. Only if Jesse already uses Neighbourly |
| **4. Hosted radar (upgrade)** | Reddit, Google and more | Justin's team switches it on | Leads arrive in Slack. Add them to `data/radar.csv` when Jesse forwards them |

Claude Code's built-in web search can't read Reddit, Facebook or the NZ trade-job sites: they block it or need a login. **That is a limit of the tool, not of the radar.** So lanes 1 and 3 use Jesse's own browser, and lane 4 is the way to reach Reddit.

## How to run it

### Before the first run
If `radar/groups.md` lists no groups yet, run the group setup in `radar/groups.md` with Jesse first.

### Lane 1: Facebook groups
1. Make sure a browser tool is available, either Claude in Chrome or the browser built into the Claude app. If neither is, tell Jesse how to switch one on (`docs/GUIDE.md` → "Turning on the browser") and stop.
2. For each group in `radar/groups.md` (at most 8 per run):
   - Open `https://www.facebook.com/groups/<group-id-or-name>/search/?q=<term>`, using the terms in `radar/searches.md`. Use 3 to 4 terms per group per run, rotating through the list so that each run covers different terms.
   - Read only posts from the last 7 days, or since the last run (the newest `found_on` in `data/radar.csv`).
   - Skip anything already in `data/radar.csv` (same link).
3. Sort each post you find with the tiers in `radar/searches.md`. Leave out sellers, other tradies advertising, job ads and posts from outside Canterbury.
4. For each High or Medium post, write a draft reply by following `program/voice.md` → "Radar replies".

### Lane 2: Storm watch
Open `https://www.metservice.com/warnings/home`. The page only loads in a real browser, so web fetch won't work. Look for heavy-rain watches or warnings that cover Christchurch or Canterbury. If there's one, give Jesse the storm-day playbook in `radar/storm-day.md`, filled in with the warning's area and times.

### Lane 3: Neighbourly (only if Jesse uses it)
Do the same as lane 1, using Neighbourly's search on Jesse's own neighbourhoods.

## What Jesse gets

One message, best first:

```
Radar · <date> · <n> new (High <h>, Medium <m>) · <groups read> groups read

1. HIGH · <Group name> · <suburb or "not stated"> · posted <when>
   "<their words, up to 25 words>"
   Why it fits: <one line: e.g. "old earthenware pipes + tree roots: relay job">
   Link: <post link>
   Draft reply:
   <draft>

2. ...

Storm watch: <none / the warning in one line + "storm-day plan ready">
Skipped: <count> (sellers, outside Canterbury, plumbing only)
```

Then append each lead to `data/radar.csv` with `status=new`. If that file doesn't exist yet, create the `data` folder and copy `templates/data/radar.csv` there first (it has the header row). The file has 15 columns, in this order: `lead_id` (R + date + number), `found_on`, `lane`, `source_name`, `link`, `suburb`, `posted_on`, `need`, `their_words`, `tier`, `draft_reply`, `status`, `replied_on`, `outcome`, `notes`. Leave the last three empty for a new lead.

End with: **"Post the ones you like from your own profile, then tell me which numbers you replied to (e.g. 'replied 1 and 3') and I'll tick them off."**

## After Jesse replies
- "replied 1, 3": set `status=replied` and `replied_on=<today>` on those rows.
- "skip 2": set `status=skipped`.
- "number 1 booked a job" / "won": set `status=won` and write the outcome in `outcome`. Radar wins count on the radar list, not in the partner ledger.
- If someone from the radar turns out to have been sent by a partner (they mention the partner or a code like `SC-P004`), the partner gets the credit. Tell Jesse: "Tell the Revenue Partner in Slack: '<customer> came from <partner>'", so it logs the referral. Partner records live only on the Revenue Partner's computer.

## If something goes wrong
- **Facebook shows a warning, a checkpoint or "you're going too fast":** stop the run straight away and tell Jesse. Don't run lane 1 again that day.
- **A group is private and Jesse isn't a member:** say so and skip it. Joining is Jesse's call and Jesse's click.
- **No browser tool:** run only what works, which is storm watch if any browser is available. Say clearly which lanes didn't run and why.
