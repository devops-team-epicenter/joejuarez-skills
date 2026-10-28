# PHASE 6 — OFF-SITE, E-E-A-T, TRUST

Owner-executed (the LLM usually cannot log into GBP, Wikidata, or
directory sites). But the LLM MUST NOT hand-wave these tasks — for each
item below it generates a ready-to-paste deliverable so the human's
only job is copy → paste → click submit. All of it lands in one packet
described at 6.7.

Timing (v1.2): the Off-Site Action Packet may be emitted any time
after Phase 1 — for most small clients it has the highest ROI-per-hour
in this program. Do not hold it hostage to Phases 3–5; run it in
parallel.

Site-Type Overlay applies: sections 6.1–6.3 as written are the
LOCAL_SERVICE / local-B2B pattern.
- SAAS: replace with G2 + Capterra + Product Hunt profiles (drafted
  listing copy, screenshots list, review-request flow for happy
  customers), StackShare, integration-partner directory pages.
- ECOMMERCE: replace with Google Merchant Center feed health, review
  syndication (Trustpilot/Bazaarvoice), UGC program.
- CONTENT_MEDIA: replace with Google Publisher Center, Apple News,
  syndication partnerships.
Sections 6.4–6.6 apply to all site types.

## 6.1 Google Business Profile — LLM deliverable
Regardless of account access, output:
- Primary category recommendation (1) and secondary categories (up
  to 9), each justified in one line based on [INDUSTRY] and
  [PRIMARY_SERVICES].
- 750-character business description (uses [BRAND_VOICE], names
  [TARGET_LOCATIONS], names ≥3 [PRIMARY_SERVICES], includes one
  specific number, ends with a soft CTA — no keyword stuffing).
- Services list: name + 300-char description per service.
- 10 photo prompts / captions the owner should upload.
- 3 GBP post drafts + a reusable monthly post prompt template the
  owner fills with that month's real news. (Not 12 pre-drafted posts —
  they go stale on arrival.)
- Q&A seed set: 10 owner-authored Q&A pairs to pre-populate.
- Review-response templates: 4 versions (5★ / 4★ / 3★ / ≤2★ recovery).
Owner cadence: respond to reviews within 24h; set a realistic Q1
review-count goal WITH the owner based on actual customer volume.

## 6.2 Wikidata entry — LLM deliverable (CONDITIONAL)
Only produce this if the business plausibly meets notability: ≥2
independent third-party sources (press, licensing bodies) already
exist. Otherwise mark "SKIPPED — notability not yet established" and
move the effort to 6.4. If produced, draft:
- Label: [SITE_NAME]; aliases: legal entity name, common
  misspellings, DBA names.
- Description (≤250 chars, neutral tone, names industry + primary
  location).
- Statements: instance of (P31) → business; industry (P452);
  country (P17); headquarters location (P159); inception (P571);
  founder (P112); official website (P856); owned by (P127) if
  applicable.
- External identifiers (P2013 Facebook, P2003 Instagram, P2002 X,
  P4264 LinkedIn, P1320 OpenCorporates, P3417 Quora) — populate every
  one that resolves; omit the rest.
- References: at least 2 independent third-party URLs per contested
  statement — Wikidata rejects unsourced claims.

## 6.3 NAP-consistent directory submissions — LLM deliverable
Canonical NAP block (Name / Address / Phone) written ONCE at the top
of the packet — the owner pastes it byte-identically into every
directory. Then, per directory, output:
- Login URL
- Category to select (best match from that directory's taxonomy)
- Short description (≤160 chars, directory-appropriate voice)
- Long description (≤500 chars)
- Services / tags to check
- Photo count required + prompts
Directories at minimum: Google Business Profile (6.1), Bing Places,
Apple Business Connect, Yelp, BBB, Facebook Business Page, LinkedIn
Company Page, industry-specific associations (list ≥3 by name for
[INDUSTRY]), local Chamber of Commerce, top data aggregators
(Data Axle, Localeze, Foursquare).

## 6.4 PR / backlinks — LLM deliverable
- 3–5 HARO / Qwoted / Featured / Help a B2B Writer pitch templates,
  each tailored to one [DIFFERENTIATORS] angle, each with: subject
  line, 90-word body, expert bio blurb, headshot placeholder, contact
  block. Owner personalizes per query.
- A list of 10 realistic outreach targets (podcasts, industry blogs,
  local business journals) with a one-line "why they'd care about
  [SITE_NAME]" hook per target.
- Quarterly bylined op-ed pitch: 3 headline ideas. (Draft the full
  piece only when a publication expresses interest.)
- Local sponsorship shortlist: 5 nonprofits / civic orgs in
  [TARGET_LOCATIONS] worth sponsoring for `.org` backlinks (local
  site types only).

## 6.5 Review velocity — LLM deliverable
- Post-conversion review-request email (subject + body + CTA) with a
  direct review link placeholder.
- SMS review-request template (≤160 chars).
- In-product review prompt copy (for SaaS / DTC).
- Response templates for 5★ / 4★ / 3★ / ≤2★.
- Reviewer objection playbook: 5 common negative-review patterns +
  how to respond publicly without escalating.

## 6.6 Crawler-access monitoring — LLM deliverable
- A ready-to-run server-log grep / SQL query (parameterized to
  [STACK]'s log format) that surfaces monthly hit counts per
  user-agent for: GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot,
  PerplexityBot, Google-Extended, Applebot-Extended, CCBot.
- Threshold to alert on: any intentionally-allowed agent at 0 hits
  for >30 days.

## 6.7 THE OFF-SITE ACTION PACKET
Bundle everything above into ONE deliverable — a single markdown
document titled "[SITE_NAME] — Off-Site Action Packet" — with this
structure and a checklist column so the owner can mark progress and
report back:

| # | Task | Ready-to-paste content | Where it goes | Owner marks: DONE / SKIPPED / NEEDS_HELP | Date completed | Notes back to LLM |
|---|------|------------------------|---------------|------------------------------------------|----------------|-------------------|
| 1 | GBP profile setup | (link to §6.1) | business.google.com | ☐ | | |
| 2 | GBP first 3 posts | (link to §6.1) | GBP → Updates | ☐ | | |
| 3 | Wikidata entry (if eligible) | (link to §6.2) | wikidata.org/wiki/Special:NewItem | ☐ | | |
| 4 | Bing Places listing | (link to §6.3) | bingplaces.com | ☐ | | |
| 5 | Apple Business Connect | (link to §6.3) | businessconnect.apple.com | ☐ | | |
| 6 | Yelp listing | (link to §6.3) | biz.yelp.com | ☐ | | |
| 7 | … one row per directory in §6.3 … | | | ☐ | | |
| N | HARO pitch #1 sent | (link to §6.4) | helpareporter.com | ☐ | | |
| … | Review-request automation live | (link to §6.5) | email / SMS / product | ☐ | | |
| … | Server-log crawler query scheduled | (link to §6.6) | infra / cron | ☐ | | |

Loop-close rule: when the owner returns the packet with statuses
filled in, the LLM ingests it and updates Phase 7 monthly SOP inputs
(a NEEDS_HELP row becomes a Phase 7 Block 5 agenda item; a DONE row
triggers a follow-up citation check next month).
