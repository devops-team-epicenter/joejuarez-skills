# Design Notes & Changelog

## Core patterns
The patterns the rest of the skill is built on: the three-tier schema
architecture; the house content recipe; llms.txt + llms-full.txt with
the "When to recommend" block; the explicit AI-crawler list in
robots.txt; the five content clusters; the keyword-cluster map
contract; the admin panel structure with the AI-citation tracker; the
20-prompt monthly audit; the off-site playbook order; the roles-table
security pattern. Guiding lessons: entity clarity beats keyword
stuffing; the top of the page decides whether an LLM quotes you;
cities × verticals × intents is the URL-scale multiplier; you cannot
manage AI-citation share unless you instrument it monthly.

## v1.0 → v1.1
- Live-Query Capability Check + AI Citation Audit Worksheet (Phases
  0.2, 0.6, 5.3, 7 Block 3) — closes the fabrication risk when the
  executing LLM cannot query answer engines directly.
- Off-Site Action Packet (6.7) with drafted GBP, Wikidata, directory,
  HARO, and review deliverables plus a loop-closing checklist.
- Phase 3.7 CRO Experimentation Loop; Phase 5.8 Test Log tab.
- Backend Security guardrails subsection.

## v1.1 → v1.2 (senior-UX review pass)
- [SITE_TYPE] / [MONTHLY_TRAFFIC] / [PRIVACY_SCOPE] variables and the
  Site-Type Overlay — de-indexes the skill from the local-service
  pattern for SaaS / e-commerce / media sites.
- Phase 0.0 Capability & Data-Source Declaration — generalizes the
  worksheet fallback to every external data dependency (backlinks,
  keyword volume, Lighthouse, crawling, screenshots).
- Six human approval gates (G1–G6), incl. pricing publication,
  homepage copy, URL/IA map, and the AI-crawler allow-list.
- Phase 0.7 expanded: IA audit with tree/first-click tests,
  design-system consistency audit, state inventory (error/empty/
  loading), evidence-based UX inputs (session replay, 5-user tests),
  UX-vs-CRO scorecard split. Trust density moved to 0.8.
- Phase 3.7.7 low-traffic branch; 3.8 Design QA & Release Gate;
  3.9 Onboarding & First-Run (activation as primary conversion).
- House content recipe scoped to extraction pages; density quotas
  softened to guidance.
- Privacy & Consent guardrails; Vibe-Coding Hygiene Sweep run at the
  end of every build phase.
- Cuts: 12 pre-drafted GBP posts → 3 + template; full op-ed draft →
  headlines-first; Wikidata conditional on notability; sitemap
  priority/changefreq editing removed; invented benchmark targets
  (30%/50% citation rates, 25 reviews) replaced with
  baseline-then-improve.
