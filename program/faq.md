# Questions and answers

Part 1 is written so it can be pasted straight to a partner. Part 2 is for Jesse, Mike and the team only.

---

## Part 1: for partners

**What is this, in a sentence?**
You let your customers know about Smart Contracting, usually with one short email or text to your list. We look after anyone who gets in touch, and for any job that comes from it you get 5% of the job value, paid once the customer's invoice is settled in full.

**Who is Smart Contracting?**
A local Christchurch drainage team. We lay and relay drains (old earthenware to modern plastic), repair damaged and blocked drains, and look after sewer and stormwater laterals. Every inspection is done with a CCTV camera and comes with a written report.

**Why would my customers need it?**
Plenty of older Christchurch homes still have earthenware drains, and many were cracked in the quakes. Nobody knows, because it's underground. A drain check tells the owner where they stand, whether they're selling, buying, renting the place out or renovating.

**What do I have to do?**
Check and approve a short email we write for you, then send it from your own email or text system to your customers. That's about it.

**Do I have to hand over my customer list?**
No. You keep your list. You send the email yourself, and we never see the list. The only people we hear from are the ones who choose to get in touch.

**Do I get a say in what's sent?**
Yes. Nothing goes to your customers without your approval. Change anything that doesn't sound like you.

**Who can I send it to?**
Only people you're already allowed to email or text, such as clients who've signed up to hear from you. Keep the unsubscribe line in, and take people off your list if they ask.

**How often?**
One campaign at a time, when it suits you. We'll suggest a month and a theme, and you decide.

**What's the fee, and when is it paid?**
5% of the job value, paid once the customer's invoice is settled in full. [GST basis: to confirm with Jesse] Fees are worked out monthly and paid by bank transfer, with a reference you can match. [payout timing after approval: to confirm with Jesse]

**How do you know a customer came from me?**
You get your own reference code. It's in your campaign, so customers quote it or mention your business when they call. If you introduce someone directly, let Jesse know (with their OK).

**What if two people refer the same customer?**
The first introduction recorded with a reference code counts.

**What if my customer already knew about Smart Contracting?**
If they were already in touch with us before your introduction, it isn't a referral. That's the "first introduction" rule working both ways.

**Do I get paid if the customer only gets a quote?**
No. The fee is on jobs that go ahead, once the customer's invoice is settled in full.

**What does a drain check cost my customer?**
Every property is different, so we quote per job after a CCTV check. Your customer can call Jesse on 03 567 0876 to talk it through.

**What if the job goes wrong?**
The job is between the customer and Smart Contracting, not you. If anything isn't right, they come to us. [what we say about workmanship or a guarantee: to confirm with Jesse]

**Do I have to tell my clients about the fee?**
Some professions have rules about telling clients when you receive a referral fee (real-estate agents, for example). If yours do, please do.

**Can I still recommend other drainage companies?**
Yes. This doesn't tie you to us.

**How do I stop?**
Just email Jesse. Either of us can end it at any time.

**Can I have the terms in writing?**
Yes. Jesse can put the terms in writing for you. [written partner agreement: to confirm with Jesse]

**Who do I talk to?**
Jesse McGimpsey, Smart Contracting, 03 567 0876. [partner email address: to confirm with Jesse]

---

## Part 2: for the team

**Who approves what?**
Jesse says yes to everything before it goes out: cold emails, replies, welcome emails, campaign copy, remittance notes. The partner approves anything that goes to their customers. A yes counts only in Jesse's own words, about the exact item shown.

**Can the fee go in a cold email?**
Never. No 5%, no "pay", "money" or "commission". It's for the call, the one-pager (only to people who have replied), and signed partners. Jesse set this on 14 Oct.

**Who works out the fee?**
The ledger tool (`tools/partner_ledger.py`). The Revenue Partner never works out a fee, payout or total in its head. If the tool can't do it, the agent says so and stops.

**Who pays?**
Jesse. The tool proposes the month's payouts, Jesse checks and approves them, Jesse pays by bank transfer with the reference `SC-<partner id>-<YYYY-MM>` (for example `SC-P001-2026-11`), then tells the Revenue Partner, which records it and drafts the remittance note. The agent never moves money.

**Is the 5% before or after GST?**
Not decided. Jesse's call. Until then everything says "5% of the job value" and shows `[GST basis: to confirm with Jesse]`. Never guess. The same goes for whether GST-registered partners add GST to their fee.

**Do we email our own customers about partners?**
Only for a partner whose work genuinely suits our customers, and only on Jesse's yes for that partner. Never as part of the standard pitch. Check `compliance-nz.md` first.

**A partner wants a different deal. What now?**
Only Jesse agrees a different deal, in his own words. It's recorded against that partner in the ledger with his words in the notes.

**What if someone says "not interested" or "stop"?**
One polite reply, then onto the suppression list for good, matched on name as well as address. Never contacted again unless they get in touch first.

**How many partners do we need?**
The Oct 9 routine draft says 3 to 5 active partners with decent lists (500 to 1,000 past clients is a good size) is enough to start. Keep it to what the crews can handle; the aim is the bigger repair work, not a flood of small jobs.

**How often does each partner send?**
About once every three months each. The aim is one partner campaign going out each month across all partners, so no list gets tired of hearing from us. Jesse can change the rhythm for any partner.

**Real-estate agents and the fee?**
Agents may have to tell their clients about a referral fee. Check with the agent before agreeing one (see `compliance-nz.md`).

**Where's the agreement?**
`agreement-DRAFT.md`. It's a draft for the lawyer. Don't send it to anyone to sign until the lawyer has checked it; send the one-pager instead.

**Jesse's refined versions of the scripts?**
Jesse said on 12 Oct he'd refined the Oct 9 docs. When he shares them, they replace `reply-and-phone-scripts.md` and the one-pager wording.
