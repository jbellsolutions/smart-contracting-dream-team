---
name: scdt-ask-ledger
description: Keep the list of everything Jesse has asked for. Use whenever Jesse sends a new idea, request or "it would be cool if", or asks "what's still open?". Every ask becomes a numbered row, with where it's solved, so nothing gets lost.
---

# Ask ledger

## Inputs
- `~/.hermes/scdt/context/asks.md`: the ledger. At setup, copy it from the build's `ASKS.md` if Justin's team attached one. Otherwise start it from `~/smart-contracting-dream-team/OPEN_QUESTIONS.md`.

## When Jesse asks for something new
1. Check whether it's already a row. If it is, add today's date to that row's **When** and tell Jesse where it stands.
2. If it's new, append a row:
   - number: the last number + 1;
   - their words, quoted;
   - today's date and where it came from;
   - a status from the key at the top of the file;
   - where it's solved: a bot, routine or skill that already does it, or "new: needs Justin's team".
3. Reply in one line, for example: "Added as #61. That's new work for Justin's team. Want me to write it up for them?"
4. New builds are tier 3. Write a request in `~/.hermes/scdt/requests/`. Never build or turn on something new without Jesse's yes.

## When Jesse asks "what's open?"
Reply in three lines:
- how many asks are open;
- the three oldest that wait on Jesse;
- anything that moved since he last asked.

Only when he asks. The Friday scoreboard stays about results.

## Never
- Renumber rows.
- Drop an ask.
- Mark something done without evidence that it ran.
