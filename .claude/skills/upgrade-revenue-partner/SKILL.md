---
name: upgrade-revenue-partner
description: Walk Jesse through installing (or updating) the partner-program upgrade on the Revenue Partner, using only Slack drag-and-drop — a test file first, then a read-only check of what it already has, then the upgrade zip. Use when Jesse says "upgrade the Revenue Partner", "install the partner stuff", "set up the partner program" or "Justin sent a new version".
---

# Upgrade the Revenue Partner

Jesse doesn't need a terminal for this. He drags two files into his Slack DM with the Revenue Partner and pastes messages you give him. You check each answer he pastes back. Do one step per message and wait for him.

The full agent-side steps are in `START-HERE.md`. The files are `dist/canary.md` and `dist/revenue-partner-upgrade.zip`.

## Step 0: Check the files
1. Confirm both files exist in `dist/`. Use the zip exactly as Justin's team shipped it: don't rebuild it on this PC (Windows line endings would break the install scripts on the Revenue Partner's Linux computer).
2. Open the folder for him: run `explorer.exe dist` (on a Mac: `open dist`). Explorer reports an error code even when the window opened fine; ignore it and ask Jesse whether he can see the folder.
3. Tell Jesse: "I've opened the folder with the two files. Next we test that a file reaches the Revenue Partner. Nothing gets installed yet."

## Step 1: The upload test
Tell Jesse, as one message:
> In Slack, open your direct messages with **Revenue Partner**. Drag **canary.md** from the folder I opened into the message box, then type this and send it:
> `Where did you save that file? Reply with the full path only. Don't do anything else with it.`
> Paste its answer back here.

Check what he pastes:
- **A path** (something like `/root/.hermes/cache/documents/…canary.md`): files arrive. Note the folder. Go to Step 2.
- **It can't see a file / no reply / an error:** stop. Say: "Slack isn't passing files to it, so we'll have Justin's team install it from their side. I'll write the message for you." Draft a short message to Justin: what was tried and what the Revenue Partner said. Then stop.

## Step 2: What it already has (read only)
Give Jesse this to paste in the same DM:
> Before I give you an upgrade, please check what you already have. Read only, change nothing:
> 1) List your skills (names only) and your cron jobs with `hermes cron list` (name, schedule, paused or active).
> 2) Find where you keep the outreach tracker, where replies are logged (a replies folder, or the tracker's reply columns), the never-email-again list, which mailbox you send from, and the exact command or script you use to send one email. Don't guess.
> 3) Check whether anything already warns me when the OpenRouter credit is low.
> 4) Write it to ~/.hermes/scdt/context/sources.md (make the folder if it's missing), starting with these six lines, one value each, UNKNOWN for anything you can't find: `tracker:` `replies:` `suppression:` `sent_from:` `send_with:` `credit-watch:` (needed, or already covered by …). Then list your skills, your cron jobs and anything that overlaps.
> 5) Reply in five lines or fewer.

Check his paste:
- Look for `daily-partner-drafts` in the cron list. If it's missing, tell Jesse that Justin's team should look before the upgrade; stop. A separate `partner-reply-check` may be gone (the reply check was cut back in October to save credit): that's fine as long as the paste says where replies are logged.
- If the tracker or replies path is UNKNOWN, carry on but tell Jesse: "Call cards and the scoreboard will wait until it finds those. Justin's team can point it at them."
- If `send_with` is UNKNOWN, carry on but tell Jesse: "Until it knows how it sends, it'll show you partner emails to copy into Outlook yourself. Justin's team can sort that."
- If something already does call cards, payouts or a scoreboard, stop and tell Jesse: two things doing one job would double up. Draft a note to Justin.
- If a credit warning already exists, note it: the credit-watch routine stays off.

## Step 3: Install
If Justin's team sent Jesse a private file called `owner.md` (his business details for the Revenue Partner), have him drag that into the DM first with: `Save this as ~/.hermes/scdt/context/owner.md. Don't share it.`

Then tell Jesse:
> Drag **revenue-partner-upgrade.zip** into the same DM, then send this:
> `Install this upgrade. 1) Unpack the zip I just sent, using the full path where you saved it: python3 -m zipfile -e (that path) ~/ 2) Run: bash ~/smart-contracting-dream-team/install/install.sh revenue-partner 3) Read ~/smart-contracting-dream-team/START-HERE.md and do Steps 3 to 6. Create every routine paused. Explain anything you need me to approve in plain English.`

Before he sends it, explain the prompts he may see (from `START-HERE.md`, "The prompts Jesse will see"):
- "It may ask to run a `python3 -m zipfile` command: that unpacks the upgrade. Approve it."
- "It may ask to run `install.sh`: that copies the new skills and sets up the partner ledger. Nothing gets sent. Approve it."
- "It may ask to create or pause cron jobs: those are the new routines, switched off. Approve."
- "Anything else, paste it here first and I'll tell you what it is."

## Step 4: Check it worked
Ask Jesse to paste the Revenue Partner's hello message. It should say it's set up, nothing new is switched on, and ask the GST question. Check:
- It mentions every `scdt-` job as paused (call-cards, weekly-scoreboard, partner-nurture, monthly-payouts, and credit-watch unless covered).
- It asked whether the 5% is before or after GST. Tell Jesse: "That one's your call. 'Before GST' means 5% of the price without GST."
- If it says it can't find the new skills: run `revenue-partner-doctor` (a gateway restart fixes it).

Then: "Done. When you're ready, tell it 'turn on call cards' and it'll start carding warm replies. Everything else stays off until you say."

## Updating later
When Justin's team sends a newer zip, do Steps 0, 3 and 4. The installer keeps any file someone edited on that computer and says "kept your edit".

## Never
- Paste anything into Slack for Jesse or click Send. He sends every message himself.
- Ask Jesse for a password or key, or have him paste one anywhere.
