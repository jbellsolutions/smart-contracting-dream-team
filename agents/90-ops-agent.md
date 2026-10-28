# Agent charter: Ops agent (reserved)

**Bot name:** Ops agent · **Account:** business · **Milestone:** M3 · **Reports to:** Jesse and Mike

Reserved. Not installed by this package.

## Role

Reads Smart Contracting's job management system: jobs, quotes, failed quotes and notes. Mike's ask from the first call: "the JMS… has got all our jobs, our quotes, what quotes have failed… everything it needs to start… helping us create revenue" (Sep 16 call [44:41]). Later it can take on the other jobs Justin offered on Oct 13, "one or two things at once": quote processing, a phone agent for missed calls, follow-up texts.

## Mission

Give the team a read of the work already in the business, so that failed quotes, repeat customers and partner-referred jobs are visible without Mike digging for them.

## What triggers it

- Milestone M3: Jesse names the JMS and Justin's team gets read-only access (an API key or an export), set up in a hidden terminal prompt, never in chat.
- It starts read-only. Anything it writes back to the JMS is a separate yes from Jesse and Mike.

## What it will own

| Job | Notes | Asks |
|---|---|---|
| Read jobs, quotes and failed quotes | Read only | #52 |
| Match partner referrals to real invoices | Feeds `scdt-referrals` the paid amount instead of Jesse typing it | #2, #10 |
| Failed-quote list for reactivation | Handed to charter 92 | #53 |
| Missed-call phone agent, quote processing, follow-up texts | One at a time, each its own milestone | #55 |

## What it needs first

- The JMS's name and how it exports data ([OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md) Q9).
- Mike's view of what "a failed quote" is and how old is too old.

## Profile

```
Reserved for milestone M3. Not active.
```
