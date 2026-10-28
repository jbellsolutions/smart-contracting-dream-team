---
name: partner-prospects
description: Find fresh partner prospects in Christchurch and Canterbury (building inspectors, real-estate offices, property managers, trades) from their own public websites, with the published work email and the page it came from, as a CSV Jesse drags into the Revenue Partner's DM to top up its sourcing. Use when Jesse says "find more partners", "we need more leads for the emails", "top up the list", or the drafts are running thin.
---

# Partner prospects

On Oct 21 Jesse said "for now i really need the 10 a day minimum", and the drafts ran at 2 to 4 a day. The Revenue Partner says clean, verified leads are what's scarce, not credits. This adds fresh, well-sourced names to its pool. The Revenue Partner still owns the outreach: it dedupes, verifies with Verifalia, drafts and waits for Jesse's tick, as now.

## Rules
1. **Public business pages only.** The firm's own website (Contact, Team, About pages) or its listing on a professional body's public register. No LinkedIn scraping, no Facebook, no paid lead databases or enrichment services, no guessing email patterns.
2. **Work addresses that the business publishes** for enquiries, with the exact page you found it on in `source_url`. This matters under NZ law: an address a business publishes on its own site, with no "no marketing" note, is the basis for emailing it (`program/compliance-nz.md`). If the page says "no unsolicited emails" or similar, leave that business out.
3. **No personal emails** (gmail, xtra and similar for a named person) unless the business publishes it as its enquiry address.
4. **Canterbury only,** and only the partner types in `program/partner-types.md`.
5. **25 rows a run at most** *(starting value)*. Quality over count.
6. Don't invent anything. A missing field is blank.

## Steps
1. Ask Jesse (one question): "Which kind this time: building inspectors, real estate, property managers or trades? And any suburbs to focus on?"
2. Search (WebSearch) for that type in Christchurch and nearby towns (Rolleston, Rangiora, Kaiapoi, Lincoln, Selwyn), then open each firm's own site (WebFetch) to find its published contact email and a named person where the site shows one.
3. Skip any firm already in `data/prospects-*.csv` from an earlier run.
4. Write `data/prospects-<YYYY-MM-DD>.csv` with columns:
   `business,partner_type,contact_name,role,email,phone,suburb,website,source_url,found_on,notes`
5. Show Jesse a short summary (count by type, and the five best with one line each on why).
6. Tell him how to hand it over:
   > Drag **prospects-<date>.csv** into your DM with the Revenue Partner and send:
   > `Add these to your partner sourcing pool. Skip anyone already in your tracker or on the never-email list. Verify with Verifalia as usual and draft them for my tick. Don't send anything without my yes.`

## Never
- Email, message or contact anyone.
- Write to the Revenue Partner's tracker or suppression list (it does that itself).
- Use a paid data service, or get around a site's block or login.
