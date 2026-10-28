# Agent charter: LeadConnector link (reserved)

**Bot name:** LeadConnector link (a skill set for the Revenue Partner, not a new bot) · **Account:** business · **Milestone:** M2 · **Reports to:** Jesse

Reserved. Not installed by this package.

## Role

Connects the Revenue Partner to LeadConnector (GoHighLevel), Smart Contracting's CRM, calls and texts, so a partner reply becomes a contact, gets tracked on a list and Jesse is notified there (Oct 7 call [1:16:40]).

## Mission

Keep partners and partner-referred customers in the CRM the office already uses, without ever setting off the customer texts that fire when records change.

## What triggers it

- **Their web and CRM contractor hears about it first** (name in `~/.hermes/scdt/context/owner.md`). They look after the website, call board and LeadConnector, and asked (Oct 13) that the AI start as "look but don't touch", because texts to customers fire when records change.
- Jesse creates a private integration token in LeadConnector; Justin's team types it into the Revenue Partner's computer in a hidden terminal prompt.

## What it will own

| Step | What | Asks |
|---|---|---|
| M2a: look only | Read contacts, pipelines and tags; report which automations fire on which changes; write nothing | #54 |
| M2b: one safe write | With the contractor's and Jesse's yes: add partners (not customers) as contacts with a tag that no automation listens to | #54 |
| M2c: referrals | Partner-referred customers added with the partner's ref code, only after the contractor confirms no text fires | #54 |

## What it needs first

- The contractor's OK, and a list of the automations that fire on contact changes ([OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md) Q10).
- The token, never pasted in chat.

## Profile

```
Reserved for milestone M2. Not active.
```
