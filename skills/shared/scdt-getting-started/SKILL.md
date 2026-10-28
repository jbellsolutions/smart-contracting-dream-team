---
name: scdt-getting-started
description: The intake interview. Use when Jesse says his basic facts changed (phone, areas, who gets copied), or when a skill needs a fact that `context/owner.md` doesn't have. Not part of the install. It confirms what the build already knows, asks only what's missing, one question at a time, and writes Jesse's facts and the team config.
---

# Getting started: the intake

## Inputs
- `~/smart-contracting-dream-team/client-context/CLIENT-CONTEXT.template.md`: the headings.
- The private client context, if Justin's team sent it (a file called `owner.md`). Save it to `~/.hermes/scdt/context/owner.md` before you ask anything.
- `~/smart-contracting-dream-team/OPEN_QUESTIONS.md`: the questions that are waiting.

## Steps
1. If `context/owner.md` exists, read it back in one message: "Here's what I know. Is anything wrong?" Fix only what Jesse corrects.
2. Ask each line still marked `ASK`, then the OPEN_QUESTIONS rows that this milestone needs:
   - one question per message;
   - short enough to answer on a phone;
   - offer choices when there are only a few.
3. Write each answer in place of its `ASK`, with today's date. Write the team's settings to `context/config.json`. A required field nobody knows yet stays `REQUIRED`; never guess it.
4. The GST question for the partner fee comes first if `partner_ledger.py check` says the terms aren't confirmed (wording in `scdt-partner-program`).
5. Fill in anything you can look up yourself (Slack member IDs, the sending mailbox from `context/sources.md`), then confirm it with Jesse.
6. Done: no `ASK` is left that the current milestone needs. Jesse has said "right" to the readback.

## Never
- Ask for a password, key or token in chat.
- Invent a fact to fill a gap.
- Ask two questions in one message.
