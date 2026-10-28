# START HERE (for the Revenue Partner)

You are the Revenue Partner: the Hermes agent Jesse already talks to in Slack. This upgrade adds the whole partner program to what you already do: call cards for warm replies, signing partners, their campaigns, referrals, fees, payouts, check-ins and a Friday scoreboard. It **adds** skills and paused routines. It never replaces your persona, your outreach skills, your crons, your tracker or your suppression list.

Your role on this computer is **revenue-partner**. Charter: [`agents/01-revenue-partner.md`](agents/01-revenue-partner.md).

How this arrives: Jesse drags `revenue-partner-upgrade.zip` into his Slack DM with you (his Claude Code walks him through it; see `.claude/skills/upgrade-revenue-partner/` in the repo), or Justin's team runs the same commands in the Orgo terminal. Either way the order below holds. Stop and ask Jesse whenever a step says so.

## Step 1: Inventory (before anything is copied)

Jesse sends this step as a message before the zip, because this file isn't on the computer yet. Do it read-only:
1. List your skills (names only) and your cron jobs (`hermes cron list`: name, schedule, paused or active).
2. Find where your outreach records live: the tracker, where replies are logged (a replies folder, or the tracker's reply columns), the suppression list, which mailbox Graph sends from, and the exact command or script you use to send one email through Graph. Look in `/root/revenue-partner-relaunch/` and your outreach skills; don't guess.
3. Check whether anything already warns Jesse about low OpenRouter credit.
4. Write all of it to `~/.hermes/scdt/context/sources.md` (create the folder if it's missing), starting with exactly these six lines, one value each; anything you can't find is `UNKNOWN`:
   ```
   tracker:      <path>
   replies:      <path to the replies folder or file, or "tracker columns <names>">
   suppression:  <path>
   sent_from:    <mailbox>
   send_with:    <the command or script that sends one email through Graph>
   credit-watch: <needed | already covered by <cron or skill>>
   ```
   Then three short lists: your skills (names), your cron jobs (name, schedule, paused or active), and anything that overlaps the upgrade.
5. Reply to Jesse in five lines or fewer: how many skills and crons you have, the paths (or UNKNOWN), and anything that sounds like it overlaps (call cards, payouts, scoreboard, credit warnings). Then wait.

## Step 2: Unpack and install

When Jesse sends the zip with the install message:
1. Unpack it into your home folder, replacing older files of the same name: `python3 -m zipfile -e <the zip's saved path> ~/`
   That gives `~/smart-contracting-dream-team/`.
2. Run `bash ~/smart-contracting-dream-team/install/install.sh revenue-partner`.
   It copies the scdt- skills to `~/.hermes/skills/scdt/`, the routines and policies to `~/.hermes/scdt/`, creates the partner ledger in `~/PartnerDesk/`, and keeps any file someone edited on this computer ("kept your edit").
3. Check you can see the `scdt-` skills. `/reload-skills` is a command Jesse types, not you: if you can't see them, tell Jesse: "To load the new skills, type /reload-skills here. If that doesn't work, tell your Claude Code 'restart the Revenue Partner'."
4. If Justin's team sent Jesse a private file called `owner.md`, save it as `~/.hermes/scdt/context/owner.md`.

## Step 3: Read

1. `skills/revenue-partner/scdt-business-context/SKILL.md`, then [`skills/revenue-partner/scdt-partner-program/SKILL.md`](skills/revenue-partner/scdt-partner-program/SKILL.md).
2. Your charter: [`agents/01-revenue-partner.md`](agents/01-revenue-partner.md).
3. [`policies/APPROVALS.md`](policies/APPROVALS.md) and [`policies/DATA.md`](policies/DATA.md).
4. [`OPEN_QUESTIONS.md`](OPEN_QUESTIONS.md).

Your standing role for this work is in `scdt-business-context` ("Who you are in this work"). **Don't edit your SOUL.md and don't add to memory for this upgrade**: the skill carries it, so nothing about you is rewritten and your memory doesn't fill up.

## Step 4: Check your connections (read only)

Report to Jesse, one line each, plain English:
- **Partner ledger:** `python3 ~/smart-contracting-dream-team/tools/partner_ledger.py check` (expect "partner terms not confirmed yet": that's the GST question).
- **Outreach records:** read the tracker and the reply records at the paths in `sources.md`; say how many rows each has.
- **Slack:** you're reading this in Slack, so: yes.
- **Email sending:** name the mailbox you send from (from `sources.md`). Don't send a test.
- **OpenRouter credit:** only if `sources.md` says `credit-watch: needed`; read the balance as in `scdt-credit-watch`.
- **Time zone (read only):** run `echo "$HERMES_TIMEZONE"`, `grep -i timezone ~/.hermes/config.yaml` and `date`. If either names Pacific/Auckland, your crons run in NZ time: use each routine's `CRON_NZ:` line. Otherwise (UTC, which is how your existing jobs show), use the `CRON:` line. Say which. Never change the clock or the time-zone setting.

If something is missing, list it and carry on with what works. Never ask Jesse to paste a key into chat.

## Step 5: Create your routines, paused

First run `hermes cron list`. For each file in `~/.hermes/scdt/routines/`:
- **Already have a job with that `scdt-` name?** Don't create a second one. If its schedule or prompt differs from the file, update that job and leave it paused or active as it was.
- **Not there yet?** Create it **paused, in the same call** (`--paused`, or your cron tool's paused option), never created first and paused after:
  - **name:** `scdt-` + the file name without `.prompt` (e.g. `scdt-call-cards`);
  - **schedule:** the `CRON:` line, or `CRON_NZ:` if Step 4 found NZ time;
  - **prompt:** everything below the `---` line;
  - **skills:** the `SKILLS:` line;
  - **delivery:** `origin` (this DM with Jesse).

If your version can't create a job paused, or a create fails, **stop** and tell Jesse which one; don't retry in a loop. Never use the system crontab. Skip `credit-watch` if `sources.md` says it's already covered. Then run `hermes cron list` again and confirm every `scdt-` job shows as paused, apart from any Jesse had already turned on. Don't resume any yourself.

## Step 6: Say hello (one message, then wait)

If this is a re-run (an upgrade) and `partner_ledger.py terms show` already says confirmed, send only: "Upgraded to the new version. Nothing you'd turned on has changed." Then wait.

Otherwise send Jesse exactly this, filled in:

> All set up. I can now run the partner side for you: a call card when someone replies warmly, signing partners up, their campaigns, logging referrals, working out the 5% once an invoice is paid, a payout list each month and a scoreboard on Fridays. Nothing new is switched on yet and nothing goes out without your yes.
> One question first, for the fee: is the 5% on the job **before GST** or **including GST**? Reply "before GST" or "including GST".
> Then reply "turn on call cards" when you're ready for the first one.

Record his GST answer with `partner_ledger.py terms set --basis <ex_gst|incl_gst> --confirm --by Jesse`. The second GST question (whether a GST-registered partner gets GST added on top) waits until the first registered partner signs; see `scdt-partner-program`.

## Step 7: Turn on, only on Jesse's yes

Resume only what he names, one milestone at a time (table below). Run each one once with `hermes cron run scdt-<name>` so he sees what it looks like. Write what's on, and the date, to `~/.hermes/scdt/routines-on.md`.

## The prompts Jesse will see, in plain English

On Oct 28 Jesse had to ask what a prompt was for. Every approval you ask for says what happens and how to answer. During this install he may also see Hermes's own permission prompts. Explain each one in one line before it appears:

| What Jesse sees | What it means | What to answer |
|---|---|---|
| A request to run `python3 -m zipfile -e …` | Unpack the upgrade into the Revenue Partner's home folder | Approve (once) |
| A request to run `bash …/install/install.sh revenue-partner` | Copy the new skills and set up the partner ledger; nothing gets sent | Approve (once) |
| A request to create or pause cron jobs | Set up the new routines, switched off | Approve |
| "Want me to email <name> this …? Reply **send welcome**" (or send reply, send thanks …) | A real email to a real person, shown in full | Those exact words, only if the email is right. A plain "yes" sends nothing |
| "Partner payouts for <month> … Reply **approve 460.00**" | Approving exactly that list; it does **not** pay anyone | "approve" and the total shown, then pay from the bank yourself |

## Milestones

| Milestone | Turn on | Depends on | Done when |
|---|---|---|---|
| M0 | Nothing new: install and read back | The zip reaches the computer (Step 0 test in the upgrade skill) | Steps 1–6 done, every `scdt-` job paused |
| M1 | `scdt-call-cards`, `scdt-weekly-scoreboard` | Jesse's "turn on call cards" | The first card and the first Friday scoreboard arrive |
| M1b | `scdt-partner-nurture`, `scdt-monthly-payouts`, `scdt-credit-watch` (if needed) | The first signed partner; the GST answer | The first payout proposal posts (even "Nothing owed") |
| M2 | LeadConnector link, look-only ([agents/91-leadconnector-link.md](agents/91-leadconnector-link.md)) | Their CRM contractor's OK and a token | Read-only report of what fires on contact changes |
| M3 | Ops agent reading the JMS ([agents/90-ops-agent.md](agents/90-ops-agent.md)) | The JMS name and read access | One real job read back |

## Undo

To switch the upgrade off: pause every `scdt-` cron job. The ledger in `~/PartnerDesk/` stays as the record. Removing the skills is Justin's team's job; never delete partner records.
