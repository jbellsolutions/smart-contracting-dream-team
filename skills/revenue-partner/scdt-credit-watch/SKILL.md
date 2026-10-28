---
name: scdt-credit-watch
description: Warn Jesse once before the OpenRouter credit runs out, so the Revenue Partner never goes dark mid-week again (it ran dry on Oct 9). Use from the credit-watch routine, or when Jesse asks "how much credit is left?". Only switched on if this agent doesn't already warn about low credit.
---

# Credit watch

## Before turning this on
At install, check whether you already warn about low OpenRouter credit (a cron, a skill, or a memory note about "$3"). If you do, write `credit-watch: already covered by <name>` to `~/.hermes/scdt/context/sources.md` and leave the `scdt-credit-watch` routine paused for good.

## Each run
1. Run exactly:
   `python3 ~/smart-contracting-dream-team/tools/credit_check.py --warn-under 3`
   *(3 = US$3, the threshold promised on Oct 12; Jesse's to change.)* The script reads the key itself and prints one line, for example `remaining_usd=2.40 WARN`. Never open, print or search `~/.hermes/.env` yourself.
2. If the line ends in `WARN`, tell Jesse once:
   "Heads up: OpenRouter credit is down to about $<amount>. I'll stop working when it hits zero. Top up at openrouter.ai → Credits."
   The script only says WARN once per NZ day, so you never repeat it.
3. If it ends in `OK`, post nothing and log `NO_CHANGE`.
4. If it starts with `FAILED`, log the line. Tell Jesse only if `log/runs-<YYYY-MM>.md` shows three FAILED credit-watch runs in a row.

When Jesse asks "how much credit is left?", run the same command without `--warn-under` and tell him the amount.

## Never
- Buy credit, change the key's limit, or turn on auto top-up.
- Read, print or post the key, or any part of it.
