# PHASE 5 — ANALYTICS + SEO/CRO ADMIN PANEL

Gate G5 first: build-vs-buy. A custom in-product panel is weeks of
software; a Looker Studio dashboard + the keyword map spreadsheet +
this phase's table specs achieves ~70% of the value in days. Present
both options sized against client budget and [STACK]; the human
chooses. If "buy/lightweight" wins, implement every tab below as a
Looker Studio page or spreadsheet tab using the same columns.

Every tab below ships with designed empty, loading, and error states
(0.7.3) — a failed GSC fetch renders a designed error state, never a
blank screen. Run the Vibe-Coding Hygiene Sweep before presenting.

## 5.1 Search performance tab
- Google Search Console connector (OAuth or service account).
- 28-day rolling: clicks, impressions, CTR, avg position.
- Top 25 queries, top 25 landing pages, biggest movers.
- Alert if any URL: CTR <2% at >500 impressions, position dropped >3
  spots WoW, indexed=false.

## 5.2 Site verification tab
- Guided flow to verify GSC + Bing Webmaster Tools via meta tag;
  write the tag to <head> automatically.

## 5.3 AI citation tracker tab
- Table of the 20 monitored prompts (seeded from Phase 0.1 buyer
  questions + 10 evergreen prompts you never change).
- Monthly log: prompt × model (ChatGPT / Claude / Perplexity / Gemini /
  Google AI Overviews) → cited yes/mentioned/no → snippet stored.
- Chart: citation rate over time per model. Establish the baseline in
  month 1 and target monotonic improvement — do not invent percentage
  targets.

### Data-input mode
The tracker supports TWO ingest modes and must expose both:
(A) Automated — only if the deploying LLM/agent has verified live
    browsing/API access to each answer engine. Runs on the 1st of each
    month, writes results directly.
(B) Manual worksheet — the default. Admin panel renders the empty
    Worksheet (same format as Phase 0.2) as a downloadable/printable
    table. The human owner runs the 20 prompts across the 5 engines,
    pastes results back via a paste-CSV / paste-markdown input, and the
    tracker parses and stores them. The chart never plots fabricated
    data; missing months render as gaps.

## 5.4 Conversion analytics tab
- Funnel view for each conversion path with drop-off %. For SAAS/
  MARKETPLACE the funnel extends past signup to the Phase 3.9
  activation event.
- CTA click heatmap by page.
- Form completion rates by step.
- Source/medium/campaign breakdown of primary conversions.

## 5.5 Content health tab
- Every URL with: last updated, word count, schema types emitted,
  internal links in, internal links out, indexable yes/no, Core Web
  Vitals score.
- Flag URLs untouched in >180 days.

## 5.6 Sitemap manager tab
- Add/edit/remove URLs with lastmod. Republish sitemap.xml on save.
  Ping GSC + Bing. (No priority/changefreq editing — Google ignores
  both fields.)

## 5.7 SEO settings tab
- Sitewide identity fields (name, legalName, phone, address, geo,
  sameAs[]) that drive the Organization JSON-LD.
- Toggles for each schema type.
- OG image manager.

## 5.8 CRO Test Log tab
Single source of truth for every experiment run under Phase 3.7.
Columns:
- test_name
- linked friction-point ID from Phase 0.8
- hypothesis (full "If … then … because …" sentence)
- page(s) / component under test
- method (A/B, feature flag, before/after, DIRECTIONAL per 3.7.7)
- variant A description / variant B description
- start_date / end_date (nullable while running)
- visitors A / visitors B
- conversions A / conversions B
- conversion rate A / B
- guardrail-metric deltas (bounce, scroll_75, secondary conv, error
  rate, rage-click rate)
- statistical confidence or Bayesian probability-to-beat
- status: RUNNING / INCONCLUSIVE / WINNER_A / WINNER_B / DIRECTIONAL
- decision (what was shipped and why; what was learned)
- links to any artifacts (screenshots, follow-up tests)
Filters: active tests, completed this quarter, by page, by
friction-point severity. Export to CSV for stakeholder review.
