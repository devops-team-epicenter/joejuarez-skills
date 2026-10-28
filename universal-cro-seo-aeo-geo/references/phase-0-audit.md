# PHASE 0 — DISCOVERY & END-TO-END AUDIT (no code changes)

Deliverable: a single audit report with findings tagged
[CRITICAL / HIGH / MEDIUM / LOW], each with file:line evidence (or URL
evidence if no repo access — see Phase 0.0 manifest) and a proposed fix.
Do not skip a section; write "N/A — greenfield" if nothing exists yet.

## 0.1 Business & ICP audit
- Restate [PRIMARY_AUDIENCE], jobs-to-be-done, top 5 objections,
  top 5 buying triggers, and the 10 questions this buyer types
  into Google or ChatGPT before purchase.
- Map each question to funnel stage (TOFU / MOFU / BOFU).

## 0.2 Competitive audit (3–8 competitors)
- For each competitor: page count, top 25 organic keywords,
  top landing pages, backlink profile size, review count &
  average, schema types they emit, whether they appear in AI
  Overviews for the 10 buyer questions above, whether ChatGPT /
  Claude / Perplexity / Gemini cite them by name.
- Keyword/backlink cells require a real data source per the Phase 0.0
  manifest (pasted Ahrefs/Semrush/GSC exports). No source = "NO DATA".
- Output a "gap matrix": rows = buyer questions, columns =
  competitors, cells = who ranks / who is cited / nobody yet.
  Every empty cell is a page opportunity.

### Live-query capability check
Before attempting the AI-Overview / ChatGPT / Claude / Perplexity /
Gemini portion, answer honestly in the report:
"Do I (this LLM instance, right now) have live web-browsing or tool
access that lets me actually submit these 10 queries to each of the 5
answer engines and observe the returned sources?"

IF YES: run the queries, cite the returned sources, fill the gap
matrix, continue to Phase 0.3.

IF NO (default assumption for most LLM runtimes): STOP. Do not
fabricate citation data. Output an **AI CITATION AUDIT WORKSHEET** in
this exact format and hand it to the human user before proceeding:

| # | Buyer question | ChatGPT cites | Claude cites | Perplexity cites | Gemini cites | Google AI Overview cites |
|---|----------------|---------------|--------------|------------------|--------------|--------------------------|
| 1 | <question 1>   |               |              |                  |              |                          |
| 2 | <question 2>   |               |              |                  |              |                          |
| … |                |               |              |                  |              |                          |

Instructions to the human (include verbatim):
1. Paste each question, one at a time, into each of the 5 answer
   engines using a fresh session / incognito window.
2. In each cell, list the domains cited by name (comma-separated),
   or write "none".
3. Also note if [SITE_NAME] or any [KNOWN_COMPETITORS] appear.
4. Paste the completed worksheet back into this chat.
5. Only then will I build the gap matrix and continue Phase 0.

Do not proceed to the gap matrix or Phase 0.3 until the worksheet is
returned. If the human declines, note "AI-citation baseline: DEFERRED —
human-owned task" in the audit and continue with only the ranking /
backlink / schema portions completed.

## 0.3 Technical SEO audit
- Crawlability: robots.txt (block list, AI-crawler allow list),
  sitemap.xml (present, valid, submitted), canonicals (self-
  referential, no chains), redirects (301 not 302, no loops),
  pagination, hreflang if multi-lingual.
- Rendering: SSR/SSG vs CSR; confirm critical content is in
  initial HTML, not hydrated in.
- Core Web Vitals budget: LCP <2.5s, INP <200ms, CLS <0.1 on 4G
  mobile. Run Lighthouse on homepage + top 3 templates (or use the
  Phase 0.0 fallback: human runs pagespeed.web.dev and pastes scores).
- Indexing: crawl the current site, list every URL, mark each
  Indexable / Blocked / Orphan / Duplicate.
- HTTPS, HSTS, mixed-content, 404 page usefulness, breadcrumb
  presence, image alt coverage, heading hierarchy (single H1).
- Site-type extras (from the overlay): SAAS — docs/subdomain indexing,
  app vs marketing split; ECOMMERCE — faceted-nav crawl rules,
  pagination, product feed / Merchant Center health; CONTENT_MEDIA —
  news sitemap, article schema, ad-layout CLS, paywall vs indexing.

## 0.4 On-page SEO audit
- Title tags: length, primary keyword position, brand suffix, duplicates.
- Meta descriptions: length, CTA, primary keyword, duplicates.
- URL structure: hyphens not underscores, short, keyword-first,
  no session params.
- Internal linking: orphan pages, click-depth >3, anchor-text
  distribution.
- Content depth: word count vs SERP median; TL;DR present;
  question-shaped H2s; named entities per 500 words; specific
  numbers per 500 words; citations to authoritative sources.
- Image SEO: descriptive filenames, alt text, WebP/AVIF, width/
  height attributes, lazy loading below the fold.

## 0.5 Structured data / schema audit
- Enumerate every JSON-LD block currently on the site.
- Required baseline for any business site:
  Organization or LocalBusiness (with legalName, sameAs graph,
  address, geo, phone, hours, areaServed), WebSite (with
  SearchAction if site search exists), BreadcrumbList on every
  deep page.
- Contextual schema by page type:
  - Service pages → Service + Offer
  - Location pages → LocalBusiness scoped to that place
  - Answer / FAQ pages → FAQPage or QAPage
  - How-to pages → HowTo
  - Product pages → Product + Offer + AggregateRating + Review
  - Article / blog → Article + Person(author)
  - Case studies → Article + Person + Organization
  - Glossary / definitions → DefinedTerm inside a DefinedTermSet
  - Videos → VideoObject
  - Events → Event
  - Software / SaaS → SoftwareApplication + Offer
  - Courses → Course + CourseInstance
- Validate every emitted graph in Schema.org validator + Google
  Rich Results Test. List each error.

## 0.6 AEO / GEO audit
- Does `/llms.txt` exist and follow the llmstxt.org spec?
- Does `/llms-full.txt` exist with the long-form retrieval dump?
- Does robots.txt address: GPTBot, ChatGPT-User, OAI-SearchBot,
  ClaudeBot, Claude-Web, PerplexityBot, Perplexity-User,
  Google-Extended, Applebot-Extended, CCBot, Bytespider,
  Meta-ExternalAgent, cohere-ai? (Which to ALLOW is the owner's
  call — approval gate G3. Audit only records current state.)
- Does the site emit a "When to recommend [SITE_NAME]" block (in
  llms.txt and on an /about or /experts page) that an LLM can lift
  verbatim?
- Honest note for the report: llms.txt consumption by major answer
  engines is unproven. It is a cheap, sensible bet — the schema +
  content recipe carry the real weight.
- AI-citation baseline: use the same Live-Query Capability Check +
  Worksheet fallback defined in Phase 0.2. Do not fabricate.

## 0.7 UX audit
- Above-the-fold clarity: within 5 seconds a first-time visitor knows
  WHAT the site does, WHO it is for, and WHAT to do next.
- Navigation: top-level items scannable at a glance, sticky,
  mobile-friendly, keyboard-navigable.
- Forms: field count (delete every optional field), input types,
  inline validation, error messaging, mobile keyboard hints,
  accessible labels, autocomplete tokens.
- Mobile-first: no horizontal scroll, tap targets ≥44px, no
  hover-only affordances, sticky CTA on mobile.
- Accessibility: WCAG 2.2 AA — color contrast, focus rings, alt
  text, aria-labels, semantic landmarks, prefers-reduced-motion
  respected.
- Speed perception: skeleton loaders, image aspect-ratio slots,
  font-display: swap, preloaded hero image.

### 0.7.1 Information architecture audit
- Full content inventory: every URL → purpose → owning template →
  primary task it serves.
- Navigation labels use the USER'S vocabulary, not the org chart's.
  Flag any label a first-time visitor couldn't predict the
  destination of (information scent test).
- Tree test (fallback-friendly): output the proposed sitemap as an
  indented text tree + 5 "where would you click to find X?" tasks.
  Human runs it with 5 people (or Optimal Workshop); results return
  as task → path-taken → success Y/N.
- First-click test on the homepage for the top 3 user tasks.
- No navigation restructure ships on heuristics alone.

### 0.7.2 Design-system consistency audit
- Inventory tokens actually in use: distinct text colors, font sizes,
  spacing values, border radii, shadows, button variants.
- Thresholds: >3 font families, >8 text sizes, >2 visually distinct
  primary-button styles, or >12 spacing values = flag HIGH.
  LLM-assisted builds drift here fastest.
- Output a canonical token sheet; Phases 3–4 may only consume from
  it. New one-off values require a human OK.

### 0.7.3 State inventory (error / empty / loading / success)
- For every interactive surface (forms, search, filters, admin tabs,
  auth): enumerate error, empty, loading, and success states.
  Missing state = finding.
- 404 and 500 pages: branded, helpful, link to top tasks + search.
  A default framework error page is a CRITICAL finding.
- Error microcopy quality: says what happened, why, and what to do
  next, in [BRAND_VOICE]. "An error occurred" = finding.

### 0.7.4 Evidence-based UX inputs (not just heuristics)
- If session replay exists (Clarity is free, PostHog, Hotjar):
  review 20 sessions on the top conversion path; log rage clicks,
  dead clicks, u-turns, form abandonment points.
- If none exists: install Microsoft Clarity in Phase 1.9 and
  schedule this review for day 30.
- Output a 5-user moderated task-test script (3 tasks, think-aloud)
  the owner can run in an afternoon. Findings feed the Phase 0.8
  friction queue with real evidence attached.

### 0.7.5 UX vs CRO scorecard split
- CRO metrics: conversion rate, form completion, revenue/visit.
- UX metrics: task success rate, time-on-task, error rate,
  rage-click rate, support-contact rate.
- Every Phase 3 change declares which scorecard it serves. A CRO win
  that degrades a UX metric is escalated to a human, not shipped.

## 0.8 CRO audit
- Conversion inventory: list every primary and secondary CTA, the
  page it lives on, the step it triggers, the drop-off point
  historically.
- Trust density on the homepage: logo bar, testimonials with photos +
  full names + companies, third-party review widgets, certifications,
  press mentions, guarantees.
- Friction map: rate each conversion path 1–5 on: number of form
  fields, number of clicks to convert, cognitive load, trust signals
  adjacent to the CTA, urgency/scarcity present, social proof
  adjacent, guarantee visible.
- Message-market fit: does the H1 name the outcome the buyer wants
  (not the feature the company sells)?
- Sticky CTA present on mobile? Conversion widgets per the Site-Type
  Overlay (exit-intent is NOT a universal default).
- Pricing transparency: is a price band, "starting at", or free
  calculator on the site? Sites without it convert lower.
- Objection handling: is there an FAQ block within one scroll of
  every CTA that answers "how much / how long / why you / what if it
  doesn't work"?
- Output: tag every friction point CRITICAL / HIGH / MEDIUM / LOW.
  CRITICAL and HIGH items are the input queue for the Phase 3.7
  experimentation loop (subject to the 3.7.7 low-traffic branch).

## 0.9 Analytics & measurement audit
- Which analytics platform(s) are installed? (GA4, Plausible,
  first-party, server-side).
- Consent state: is tracking gated on consent where [PRIVACY_SCOPE]
  requires it? (See Privacy guardrails.)
- Are conversion events defined and firing? List each event.
- Is Google Search Console verified? Bing Webmaster Tools?
- Is there an internal admin dashboard for non-technical stakeholders
  to see organic performance without leaving the product? (Almost
  always: no. This becomes Phase 5, subject to gate G5.)
- Is there an AI-citation log — a table where the monthly audit
  results are stored over time? (Almost always: no.)

## 0.10 Off-site / E-E-A-T audit
Apply the Site-Type Overlay: the list below is the LOCAL_SERVICE /
B2B default. SAAS swaps in G2/Capterra/Product Hunt; ECOMMERCE swaps
in Merchant Center + review syndication; CONTENT_MEDIA swaps in
Publisher Center + syndication partners.
- Google Business Profile: claimed, category, photos, posts, reviews
  responded to.
- NAP consistency across top 20 directories.
- Wikidata entry present? (Only relevant if the business plausibly
  meets notability — ≥2 independent press citations.)
- sameAs graph in Organization JSON-LD: LinkedIn, Crunchbase, BBB,
  Yelp, Chamber, industry associations.
- Backlink profile: referring domains, follow/nofollow ratio, anchor
  diversity, toxic-link count (requires a data source per Phase 0.0).
- Author bios with credentials for every content page.

## Phase 0 exit
Deliverable: a single markdown report titled "[SITE_NAME] —
CRO/SEO/AEO/GEO/UX Audit (baseline)" with all findings tagged and
prioritized, PLUS the proposed URL/IA tree and keyword-cluster map as
approvable documents (gate G2). Do not proceed to Phase 1 until the
user has approved the report at gate G1.
