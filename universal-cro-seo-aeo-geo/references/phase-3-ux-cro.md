# PHASE 3 — UX & CRO IMPLEMENTATION

Gate G4 applies: homepage hero copy (3.1) and any pricing publication (3.6)
require human approval before shipping. Gate G6 applies: nothing in this
phase ships without the 3.8 Design QA sign-off. Run the Vibe-Coding Hygiene
Sweep before presenting the change set.

## 3.1 Homepage rewrite
- Above the fold: outcome-focused H1, one-sentence subhead, primary +
  secondary CTA, single hero image or product frame, trust bar (logos
  or review count).
- Section order that converts: problem → solution → how it works
  (3 steps) → proof (case studies + testimonials) → objections (FAQ) →
  pricing or price band → final CTA.
- H1/hero copy is presented for approval (G4) before it ships.

## 3.2 Forms
- Cut every optional field. Ask for name + [PRIMARY_CONVERSION-relevant
  field] + contact only. If a stakeholder (e.g. sales) needs a field,
  they defend it in one line or it goes.
- Multi-step for anything >4 fields; show a progress bar.
- Inline validation, correct input types, mobile keyboard hints,
  autocomplete tokens, accessible labels.
- Success state: what happens next + expected timing + calendar/link
  to book.

## 3.3 Trust density
- Testimonials with photo + full name + company + specific result.
- Case studies with named metrics.
- Third-party reviews widget (Google, Trustpilot, G2, Capterra —
  whichever fits [SITE_TYPE]).
- Certifications / partner logos.
- Guarantee (money-back, SLA, uptime) prominently placed.

## 3.4 Objection handling
- FAQ block within one scroll of every primary CTA, answering: how
  much, how long, why you, what if it doesn't work, is my situation
  supported, what happens after I click.

## 3.5 Conversion widgets — per Site-Type Overlay
- LOCAL_SERVICE / B2B_LEAD_GEN: sticky mobile CTA, live chat or
  scheduling widget as fits [PRIMARY_CONVERSION].
- SAAS: in-app prompts; NO exit-intent on docs or app surfaces.
- ECOMMERCE: cart-recovery flows beat exit-intent popups.
- CONTENT_MEDIA: inline newsletter units; no exit-intent.
Exit-intent capture is opt-in per site type, never a default.

## 3.6 Pricing transparency
Publish a price band, a starting-at price, or a self-serve calculator.
If the business truly cannot publish price, publish the pricing METHOD
and 3–5 named example scenarios with numbers. Publishing price is a
business strategy decision — obtain gate-G4 approval first.

## 3.7 CRO experimentation loop
Purpose: turn every CRITICAL / HIGH friction point from Phase 0.8 into
a tracked test. No opinion-driven changes; every change is a hypothesis
with a measured outcome.

### 3.7.1 Formal hypothesis per CRITICAL/HIGH item
"If we change [X on page Y], then [conversion metric] will
[increase / decrease] by [expected magnitude] because [buyer-behavior
reasoning]."
Example: "If we cut the quote form from 7 fields to 3, then form_submit
rate will increase by ≥20% because reducing perceived effort lowers
abandonment in high-intent traffic."

### 3.7.2 Test method, in order of preference by stack capability
(a) Native A/B split via the framework or an installed experiment
    platform (GrowthBook, PostHog, Statsig, VWO, Optimizely, or a
    first-party feature-flag table).
(b) Feature flag with 50/50 cookie-based bucketing written into the
    app (bucket assignment stored on visitor_id, rendered server-side
    to avoid CLS/flicker).
(c) Sequential before/after test when no A/B infra exists: measure
    baseline ≥2 weeks, ship the change, measure ≥2 weeks. Only valid
    when traffic sources are stable.

### 3.7.3 Minimum sample size / duration before declaring a winner
- ≥100 conversions per variant, OR ≥2 weeks of runtime, whichever is
  LONGER. Never call a winner early on "trending" numbers.
- Test spans at least one full weekly business cycle (Mon–Sun).
- If confidence < 95% (or Bayesian probability-to-beat < 95%) at the
  stopping point, declare INCONCLUSIVE and either extend runtime or
  ship the simpler/cheaper variant.

### 3.7.4 Logging
Every test is logged in the Phase 5.8 Test Log table. No test exists
that isn't in the log.

### 3.7.5 Guardrail metrics
For every test, also watch bounce_rate, scroll_75, and
secondary_conversion — plus the UX scorecard (0.7.5): error rate and
rage-click rate. A "winner" on primary conversion that tanks a
guardrail metric is not a winner — investigate before shipping.

### 3.7.6 On completion
Shipped variant becomes the new baseline. Losing variant's insight is
logged into the Test Log's "decision" column for institutional memory.

### 3.7.7 LOW-TRAFFIC BRANCH (mandatory check before any test)
Estimate monthly primary conversions from [MONTHLY_TRAFFIC] × baseline
rate. If a 50/50 test cannot reach ≥100 conversions per variant within
6 weeks:
- Do NOT run A/B tests. Do not build A/B infra. A permanently
  INCONCLUSIVE test log is process theater.
- Instead: ship evidence-backed best-practice changes in batches,
  annotate the ship date in analytics, review the before/after
  direction monthly — labeled DIRECTIONAL, never "winner".
- Reallocate testing effort to research: 0.7.4 session replays and the
  5-user task test find more lift below ~5k sessions/month than any
  split test can detect.
- Re-check this branch quarterly; graduate to 3.7.2 when traffic
  supports it.

## 3.8 DESIGN QA & RELEASE GATE (no Phase 3–4 page ships without this)

### 3.8.1 Responsive matrix
Render every new/changed template at 360, 390, 768, 1024, 1280,
1536+ px. Check: no horizontal scroll, no clipped text, tap targets
≥44px, images not distorted, sticky elements don't cover content.

### 3.8.2 Cross-browser
Chrome, Firefox, Edge, AND Safari — desktop + iOS. Safari is where
LLM-generated CSS breaks.

### 3.8.3 Content-stress test
Longest real service name, a 40-char surname, a 3-line testimonial, an
empty optional field. No truncation without ellipsis, no layout
breakage.

### 3.8.4 Keyboard & assistive pass
Keyboard-only pass on every conversion path; visible focus at every
stop. Screen-reader spot-check on forms.

### 3.8.5 Visual regression
Capture baseline screenshots per template per breakpoint (Playwright
if available; manual folder if not). Diff before every subsequent
release.

### 3.8.6 Human sign-off (gate G6)
Present screenshots at 3 widths per changed template. A human approves.
If the runtime cannot screenshot (see Phase 0.0), the human captures
them. This gate is NEVER self-certified by the LLM.

## 3.9 ONBOARDING & FIRST-RUN EXPERIENCE
(Runs when [SITE_TYPE] = SAAS or MARKETPLACE, or whenever
[PRIMARY_CONVERSION] creates an account. Otherwise mark N/A.)

- Define the activation event — the first moment of real value (first
  report generated, first item listed) — with the human. Instrument it
  in 1.9. Activation, not signup, is the primary conversion; the Phase
  5.4 funnel must extend to it.
- Map signup → activation in ≤5 steps. Every step: what the user must
  do, what could confuse them, what the empty state teaches. Empty
  states are onboarding surfaces — every one shows what-goes-here + a
  one-click way to add it.
- First-run checklist (3–5 items max) with progress indicator.
- Day-0 / day-3 / day-7 lifecycle emails keyed to activation state
  (drafted copy is an LLM deliverable, like Phase 6).
- Log time-to-activation as a Phase 5 metric; treat drops as CRITICAL
  friction points feeding 3.7.
