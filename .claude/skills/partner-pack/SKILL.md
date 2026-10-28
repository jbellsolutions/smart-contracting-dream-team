---
name: partner-pack
description: Make a ready-to-send partner one-pager or info pack (PDF-ready page) for a specific partner type or person who asked, using the program documents. Use when Jesse says "partner pack", "one-pager", "they want a PDF", "send them some info", or names a partner who asked for information or pricing.
---

# Partner pack

On Oct 7 a real-estate and property office asked for "a PDF with information and pricing to keep on file", and Jesse wasn't ready. This makes that pack in a minute.

## Steps
1. Ask (one question): "Who's it for? Name and business, and what are they: building inspector, real estate, property manager, or a trade?" Use what he already said if he said it.
2. Start from `program/one-pagers/<type>.html` (`real-estate`, `building-inspectors`, `property-managers`, `trades`). Copy it to `data/packs/<YYYY-MM-DD>-<business-slug>.html`. Never edit the original.
3. Personalise only the marked spots: their name or business in the greeting line, and one sentence on why it suits their customers, from `program/partner-types.md`. Nothing else changes.
4. **Pricing.** Don't put prices in it unless Jesse gives them to you for this pack. If the person asked for pricing, add the line from `program/reply-and-phone-scripts.md` on how pricing works (every drain is different; CCTV first; written report and quote). If Jesse gives you a starting price, use exactly his words and "+ GST" if he says so.
5. **The fee.** The one-pager carries the fee line ("5% of the job value, paid once the customer's invoice is settled in full"). If the GST basis is still a placeholder, ask Jesse: "The fee line doesn't say yet whether the 5% is before GST or including GST. Which is it? Reply 'before GST' or 'including GST', or 'leave it out'." Use his answer, and remind him once: "Tell the Revenue Partner the same in Slack, so it works the fee out the same way." If he says leave it out, delete that placeholder and keep "5% of the job value".
6. **Nothing unfinished goes out.** Before you show it, search the pack for `[` and `placeholder`. Every gap (areas covered, his partner email address, the GST basis) is either filled from Jesse's answer or its whole line is taken out. Ask about all the gaps in one message.
7. Open it in the browser so he can see it. Then tell him: "Press Ctrl+P, choose 'Save as PDF', and attach it to your reply. Want me to write the reply email too?"
8. If he wants the email: draft 3 to 5 lines in his voice (`program/voice.md`), with the PDF attached by him. He sends it himself, or he asks the Revenue Partner in Slack to send it. You don't send email.

## Never
- Invent prices, turnaround times, guarantees, reviews or past jobs.
- Change the fee wording.
- Leave a `[...]` placeholder in a pack he'll send.
- Put another partner's or customer's name in a pack.
