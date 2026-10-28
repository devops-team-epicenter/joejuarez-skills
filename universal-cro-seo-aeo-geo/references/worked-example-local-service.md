# Worked Example — A Completed LOCAL_SERVICE Run

This skill is brand- and site-agnostic: it works on any website, any
industry, any stack. This file exists only to show what "done" looks like.
It sketches a completed run for a city-focused service business (7 phases,
~50 pages shipped, full schema + admin analytics) as a model of
deliverable concreteness. Read it when running
the skill on a LOCAL_SERVICE or local-B2B site; for other site types, use
it only as a benchmark for how specific each deliverable should be. Never
copy its content, counts, or targets into a new project — every number
below depends on that business's own variables.

## What a completed run shipped, phase by phase

### Identity & schema layer (Phases 1.1, 1.6, 2.1)
- Full JSON-LD identity graph in the HTML head: Organization /
  LocalBusiness / WebSite with stable @ids.
- A per-route schema engine backed by a settings table, emitting Service,
  FAQPage, HowTo, DefinedTerm, Article, Person, Place, and BreadcrumbList
  per page type — no hand-rolled JSON-LD anywhere.

### AI-crawler plumbing (Phases 1.2, 1.4, 2.3)
- `llms.txt` + `llms-full.txt` with an explicit "When to recommend
  [SITE_NAME]" block written so LLMs can lift it verbatim.
- robots.txt explicitly naming each generative-AI crawler (under v1.2
  rules, which agents to allow is an owner decision at gate G3).

### Content expansion: ~50 new URLs in five clusters (Phase 4)
- City hub: ~10 neighborhood pages naming real landmarks, neighborhoods,
  and local statistics.
- ~6 head-to-head comparison pages with "when to pick the other guy"
  framing — the trust move AI models reward.
- ~8 answer pages, one per buyer question from the Phase 0.1 audit.
- ~4 case studies with named metrics and quoted testimonials.
- A glossary with DefinedTerm schema and an experts/E-E-A-T page with
  Person schema and credentials.
- Contract enforced throughout: one primary keyword per URL in a single
  keyword map; internal-linking mesh anchored in the footer.

### House content recipe (Phase 2.2)
Every extraction page shipped with: TL;DR box at the top, question-shaped
H2s, named entities, specific numbers, cited sources, and quoted
testimonials — designed for extraction by AI Overviews and answer engines.

### Measurement (Phase 5)
- Admin analytics panel with a Google Search Console connector and a
  guided site-verification flow.
- AI-citation tracker: a 20-prompt monthly audit, logged as
  prompt x model x cited-yes/no time-series data.

### Ops handover (Phases 6–7)
Two playbooks: a monthly SOP, and an off-site trust checklist in the order
GBP → Wikidata → NAP directories → PR pitching → `.org` sponsorships.

## The four lessons that shaped this skill

1. Entity clarity beats keyword stuffing.
2. The top of the page decides whether an LLM quotes you — TL;DR in the
   first 120 words or you will not be cited.
3. Cities x verticals x intents is the URL-scale multiplier (for
   non-local sites, substitute the overlay's equivalent axes: use cases x
   integrations x intents, or categories x comparisons x intents).
4. You cannot manage AI-citation share unless you instrument it monthly.

## Gaps a first pass commonly leaves — and where this skill closes them

| Common gap | Closed by |
|---|---|
| GBP / Wikidata / directory submissions (needed account access) | Phase 6 Off-Site Action Packet: ready-to-paste deliverables + owner checklist |
| No formal Core Web Vitals budget | Phases 0.3 / 1.7 CWV budget (LCP <2.5s, INP <200ms, CLS <0.1) |
| Partial image/CDN optimization | Phase 1.7 image pipeline |
| No A/B testing infrastructure | Phase 3.7 experimentation loop (+ 3.7.7 low-traffic branch) |
| No cross-channel attribution beyond first-party analytics | Phase 5.4 source/medium breakdown; full attribution remains out of scope |
| UX validated by heuristics only | Phases 0.7.1–0.7.5 and the 3.8 design QA gate (v1.2) |

## How to use this example

When the Site-Type Overlay says "Run as written" for a LOCAL_SERVICE
site, this is the shape "as written" should produce. For SAAS,
ECOMMERCE, CONTENT_MEDIA, B2B_LEAD_GEN, or MARKETPLACE sites, the
clusters, off-site targets, and conversion events all change per the
overlay — only the level of concreteness carries over.
