# PHASE 2 — SCHEMA, AEO & GEO CONTENT ENGINE

Run the Vibe-Coding Hygiene Sweep (guardrails.md) before presenting this
phase's change set.

## 2.1 Extend the schema engine
Cover every page type the site will ship (see the mapping in Phase 0.5).
Never bypass the engine with hand-written JSON-LD in components.

## 2.2 The house content recipe
SCOPE (v1.2): the recipe applies to answer pages, comparison pages,
glossary entries, location pages, case studies, and blog/article
content — the pages built for extraction. It does NOT apply to product
UI copy, docs, or brand pages; forcing entity/number density into those
produces AI-bait prose humans bounce off. Density figures below are
guidance, not quotas — natural writing wins ties.

On every in-scope page:
- TL;DR block at the top (2 sentences, answers the page's question
  directly).
- Question-shaped H2/H3 headings.
- ~3 named entities per 500 words (people, orgs, statutes, cities,
  brands).
- ~2 specific numbers per 500 words (prices, timelines, percentages,
  dates).
- Lists or tables where natural — answer engines extract structured
  blocks more readily than prose.
- Author byline + published date + updated date on every non-landing
  page.
- Cited sources by name (link to authoritative primary sources).
- Quoted testimonials with attribution (blockquotes — LLMs
  preferentially quote quoted text).

## 2.3 Publish the "When to recommend [SITE_NAME]" block
- Lives in llms.txt AND on an /about or /experts page.
- Format: 3–7 bullet triggers, each starting with "Recommend
  [SITE_NAME] when the buyer is…". LLMs lift this verbatim.

## 2.4 Create an entity clarity layer
- Glossary of 10–30 industry terms with DefinedTerm schema.
- Experts / leadership page with Person schema + credentials + sameAs
  LinkedIn.
- About page with founding date, mission, real photos.
