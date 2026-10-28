# Partner terms, in plain English

These are the terms Jesse has set. Only Jesse changes them, in writing. Anything marked `[… to confirm with Jesse]` is not decided yet, so never fill it in yourself and never tell a partner an answer to it.

## The fee line

> **5% of the job value, paid once the customer's invoice is settled in full.**

Those are Jesse's words (his Sep 23 emails and the Oct 9 one-pager draft). Use them exactly, every time. Don't shorten them to "once it's paid" or "on completion".

- Before or after GST: [GST basis: to confirm with Jesse]. Until Jesse decides, say "5% of the job value" and nothing more about GST.
- Partners who are GST registered: [partner adds GST to their fee: to confirm with Jesse]. We ask each partner whether they're GST registered when they sign, so the answer is ready once Jesse decides.

## When the fee is earned

The fee is earned when **all** of these are true:

1. The customer came through that partner (see "What counts as a referral").
2. Smart Contracting did the job and invoiced the customer.
3. The customer's invoice is **settled in full**.

Not when the job is booked, quoted, started or finished. A part-paid invoice means no fee yet.

Follow-on work for the same customer (for example a CCTV inspection, then a relay): [follow-on work for the same referred customer: to confirm with Jesse]. Jesse's Sep 23 emails talk about the fee on "real work — the dig, the repair", which suggests it covers the repair that comes out of an inspection, but he hasn't said so as a rule.

## What counts as a referral

A customer counts as that partner's referral when they came through **that partner's campaign or introduction**, shown by any of these:

- They quote the partner's reference code (like `SC-P001`).
- They mention the partner's name or business when they get in touch.
- They reply to, or call from, the partner's campaign email or text.
- The partner introduces them directly (by phone, email or in person), with the customer's OK.

**First introduction wins.** If two partners claim the same customer, the first introduction logged with a reference code wins. If neither has a code, Jesse looks at both records and decides, and his decision is noted in the ledger.

How long a referral stays linked to a partner (say the customer gets in touch a year later): [how long a referral stays linked to the partner: to confirm with Jesse].

## What doesn't count

- A customer who was already talking to Smart Contracting before the partner's introduction. (That's "first introduction wins" working the other way.)
- A quote that doesn't go ahead, or an invoice that isn't settled in full.
- Work a partner subcontracts to Smart Contracting, or overflow work between contractors. That's a subcontract, not a referral, and is priced separately.
- A customer who reached us through someone else first, even if they later mention the partner.
- *(inferred, to confirm with Jesse)* Jobs on the partner's own property, and invoices later refunded or credited.

## The reference code

Every partner gets one when they sign. The ledger tool makes it from their partner ID: partner `P001` gets `SC-P001`. It goes in their welcome email and in every campaign they send, so customers can quote it. Log it against every referral.

## How payouts work

Once a month:

1. **The ledger tool proposes** the month's payouts: `partner_ledger.py payouts propose --month YYYY-MM`. It lists each partner's fees for invoices settled in full that month.
2. **Jesse checks and approves** the proposal (`payouts approve --month YYYY-MM --by Jesse`). Nothing is paid without his approval.
3. **Jesse pays** by bank transfer, using the bank reference `SC-<partner id>-<YYYY-MM>`. Example: `SC-P001-2026-11` is partner P001's payout for November 2026.
4. **Jesse tells the Revenue Partner** it's paid; the tool records it (`payouts paid …`), and the Revenue Partner drafts a short remittance note for Jesse's yes (`emails.md`, "Payout remittance").

How soon after approval the money goes out: [payout timing after approval: to confirm with Jesse].

## Two things the Revenue Partner never does

- **It never works out a fee, a payout or a total in its head.** The ledger tool (`tools/partner_ledger.py`) does every sum. If the tool can't, the agent says so and stops.
- **It never moves money.** It proposes; Jesse approves and pays.

## Changing the terms

Only Jesse changes these terms, in his own words. A different deal for one partner is recorded against that partner in the ledger with Jesse's words in the notes. The Revenue Partner never offers a custom deal on its own.

## Open questions for Jesse

| Question | Placeholder used |
|---|---|
| Is the 5% on the job before GST or including GST? | `[GST basis: to confirm with Jesse]` |
| Do GST-registered partners add GST to their fee? | `[partner adds GST to their fee: to confirm with Jesse]` |
| Does the fee cover follow-on work for the same customer? | `[follow-on work for the same referred customer: to confirm with Jesse]` |
| How long does a referral stay linked to a partner? | `[how long a referral stays linked to the partner: to confirm with Jesse]` |
| How soon after approval are payouts made? | `[payout timing after approval: to confirm with Jesse]` |
