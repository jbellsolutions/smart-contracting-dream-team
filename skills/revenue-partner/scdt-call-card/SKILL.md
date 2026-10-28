---
name: scdt-call-card
description: Turn each warm partner reply into a call card for Jesse (who they are, what they said, their number, what to say first, a ready reply) and record how the call went. Use from the call-cards routine, when Jesse says "any replies?", or when he reports a call ("called Sam, keen", "no answer", "not now").
---

# Call cards

Load `scdt-business-context` first. Jesse's dream: "get the reply and get on the phone". The card does the thinking so he can just ring.

## Where replies come from (read only)
Your existing reply check already reads the inbox and logs each reply. **Don't read the inbox again.** Read replies from where `~/.hermes/scdt/context/sources.md` says (line `replies:`): a replies folder or file, or the reply columns of the outreach tracker itself. Use the tracker (line `tracker:`) for who each person is. Never edit either. If `replies:` is UNKNOWN, tell Jesse once: "Call cards can't run yet: I don't know where replies are logged. Justin's team can point me at it." Then stop.

## Each run
1. Collect replies received since the last run (time in `~/.hermes/scdt/state/call-cards-last-run`; first run: the last 3 days).
2. Keep only **warm** ones: interested, a question, "send me info", "call me", a time to talk. Skip out-of-office, bounces, "no thanks" and unsubscribes (the existing skills handle those).
3. For each warm reply:
   a. `python3 ~/smart-contracting-dream-team/tools/partner_ledger.py card seen <their email>`. If `"seen": true`, skip it: a card never goes twice.
   b. Build the card (format below). Pick "What to say first" from `program/reply-and-phone-scripts.md` for what they asked. If they asked for pricing or a PDF, use the price answer from the scripts and offer the one-pager for their partner type (`program/one-pagers/<type>.html`).
   c. Record it first: `partner_ledger.py card add --name "<name>" --business "<business>" --email "<email>" --source "<where the email came from>"`. If that fails, skip this reply and log why (so a card can never go twice).
   d. Post the card to Jesse in Slack, in its own thread. Also email it to Jesse's own address (from `context/owner.md`) with the subject `Call card: <name>, <business>`. Messages to Jesse himself need no approval and no outbox record.
4. Write the run time to `state/call-cards-last-run`. If there were no warm replies, post nothing and log `NO_CHANGE`.
5. At most 6 cards a run. More than that: send the 6 freshest and one line "and N more waiting, say 'more cards'".

## The card
```
📞 Call card: <Name>, <Business> (<partner type>)
They said: "<one or two lines of their reply, exact>"
Number: <phone from their signature, or "not in the email: ask for it">
Who they are: <one line from the tracker: suburb, how we found them>
Say first: <one or two lines from the scripts>
If they ask about money: <the fee line from program/terms.md, only for a call, never in an email>
Ready reply (if you'd rather email first): "<a 2–4 line reply that asks for their number or a time to talk; no fee>"
Reply in this thread: called · send reply · not now · not interested · book Justin
```
Keep it phone-sized. No fee in the "Ready reply".

## When Jesse answers in the card's thread
| He says | You do |
|---|---|
| **send reply** | Send exactly the ready reply shown, following "Sending an email" in `scdt-business-context` (kind `reply`). Then `card set <K…> notes="reply sent"` (the status stays `card_sent` until he calls). A bare "yes": ask "Send the ready reply to <name>? Reply **send reply**." |
| "called", "spoke to them", "keen" | `card set <K…> status=called notes="<his words>"`. If keen: `partner add --business … --status talking` (skip if `partner find` already has them). The welcome is a separate item: when he says they're in, `scdt-partner-signed` drafts it in a new thread |
| "they're in", "signed" | Hand to `scdt-partner-signed` |
| "not now" | `card set <K…> status=not_now notes="<his words>"`. Don't contact them again unless Jesse says so |
| "not interested", "they said no" | `card set <K…> status=not_now notes="declined: <his words>"`, then run your outreach skill's own decline step so they go on the never-email list (matched by name as well as address, Jesse's rule) |
| "no answer" | `card set <K…> status=no_answer`. Offer the text from the scripts ("Want me to draft a text you can send?"); you don't send texts yourself |
| "book Justin" | Post in this thread: "Noted: Justin to join the call with <Name>. Send him the time and I'll put this card in the message." Draft that message to Justin for Jesse to forward |

## Never
- Mention the fee in an email.
- Treat a bare "yes" as approval to send.
- Send anything other than the exact reply Jesse saw.
- Read the inbox yourself, or write to the tracker or suppression list.
- Card the same email twice.
