# Where the Revenue Partner's existing records live

Written by the Revenue Partner in START-HERE Step 1 (the inventory), before anything is installed. The scdt- skills read these paths and never write to the files they point at. `UNKNOWN` means it couldn't find it; a skill that needs an UNKNOWN path stops and says so.

```
tracker:      UNKNOWN   # the outreach tracker (who was emailed, when, status)
replies:      UNKNOWN   # where your reply check logs replies: a folder, a file, or "tracker columns <names>"
suppression:  UNKNOWN   # the never-email-again list
sent_from:    UNKNOWN   # the mailbox Graph sends from
send_with:    UNKNOWN   # the command or script that sends one email through Graph (the scdt- skills use the same one)
credit-watch: UNKNOWN   # "needed", or "already covered by <cron or skill>"
```

## Existing skills (names only)

UNKNOWN

## Existing cron jobs (name, schedule, paused or active)

UNKNOWN

## Anything in the upgrade that overlaps an existing skill or cron

UNKNOWN
