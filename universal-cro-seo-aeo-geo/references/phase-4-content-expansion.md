# PHASE 4 — CONTENT EXPANSION (the 50–100 page play)

Build clusters in parallel. Every page follows the Phase 2 content
recipe (in scope), ships with correct schema, passes the 3.8 Design QA
gate, and maps to the gate-G2-approved URL/IA tree and keyword map.
Apply the Site-Type Overlay: clusters below marked with their default
applicability. Quality gate: on a low-authority domain, ship clusters
in batches of ~10, verify indexing + impressions in GSC before the
next batch — scaled thin content is a policy risk, not a growth hack.
Run the Vibe-Coding Hygiene Sweep before presenting the change set
(this phase multiplies hygiene defects ×50 pages).

## 4.1 Service / offering hub (all site types)
One deep page per [PRIMARY_SERVICES] entry (5–10 pages).
Template: what it is → who it is for → how it works → included → not
included → pricing band → outcomes → FAQ → CTA.
Schema: Service + Offer + FAQPage + Breadcrumb.

## 4.2 Location hub (LOCAL_SERVICE; others see overlay)
One page per [TARGET_LOCATIONS] (10–20 pages if local).
Template: local intro naming real landmarks + neighborhoods + local
statistics → service list → local case study → local FAQ → local CTA +
directions/map.
Schema: LocalBusiness scoped to the area + Service + FAQPage.
SAAS replaces with integrations + use-case pages; ECOMMERCE with
category/collection architecture + buying guides; CONTENT_MEDIA with
topic hubs.

## 4.3 Answer hub (all site types)
10–20 answer pages (one per buyer question from Phase 0.1).
Template: TL;DR → direct answer → nuance → related answers → CTA.
Schema: FAQPage or QAPage or HowTo (whichever fits) + Article +
Person(author) + Breadcrumb.

## 4.4 Comparison hub (LOCAL_SERVICE / SAAS / B2B; overlay for others)
3–8 head-to-head pages ("[SITE_NAME] vs [Competitor]").
Template: TL;DR verdict → side-by-side table → when to pick the other
guy (this is the trust move that AI models reward) → switching guide →
CTA.
Schema: Article + Breadcrumb (do not use Review schema for competitor
comparisons — it violates guidelines).

## 4.5 Case studies (4–10 pages)
Template: client (anonymized if needed) → problem → what we did →
named metrics → quoted testimonial → related service.
Schema: Article + Person + Organization (client) + Breadcrumb.

## 4.6 Glossary (10–30 entries)
Template: term → definition → how [SITE_NAME] uses it → related terms.
Schema: DefinedTerm inside DefinedTermSet.

## 4.7 Expertise / authors page
Real people, credentials, sameAs LinkedIn, photo, bio.
Schema: Person (one node per author).

## 4.8 Internal linking mesh
- Every service page links to: its location variants (or overlay
  equivalent), its matching answer pages, its comparison pages,
  related case studies, and the glossary.
- Every location page links back to every service.
- Footer contains a compact site map that ensures no page is more
  than 3 clicks from the homepage.

## 4.9 Keyword-cluster map
- Maintain a single spreadsheet or markdown file: URL → primary
  keyword → intent tier → secondary keywords → target monthly volume
  (only from a real data source per Phase 0.0; else "NO DATA") →
  status.
- No URL ships without a row in this file. No two URLs share a
  primary keyword.
- This file was approved at gate G2; material changes to it go back
  to the human.
