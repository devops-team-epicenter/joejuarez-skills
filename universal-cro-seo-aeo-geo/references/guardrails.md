# GUARDRAILS

Read this file before Phase 1. The Vibe-Coding Hygiene Sweep at the
bottom runs at the END of Phases 1, 2, 3, 4, and 5 — before each
phase's change set is presented for review.

## Content & SEO guardrails
- Never invent facts, numbers, testimonials, credentials, phone
  numbers, addresses, or reviews. Ask the user or leave a TODO (and
  the Hygiene Sweep catches any TODO before it ships).
- Never write pages that don't map to a primary keyword in the
  keyword-cluster map.
- Never ship a page without <title>, meta description, canonical, OG
  tags, JSON-LD, and a sitemap entry.
- Never use hover-only affordances, or tap targets <44px on mobile.
- Never change the AI-crawler allow/block list without owner approval
  (gate G3) — allowing or blocking training crawlers is a
  content-licensing decision, not a technical default.
- Never bypass the schema engine by hand-writing
  `<script type="application/ld+json">` in a component. Extend the
  engine.
- Never mark a finding "fixed" without reading the code that
  addresses it.
- Never fabricate AI-citation results, keyword volumes, backlink
  counts, or CWV scores. If you can't obtain the data (Phase 0.0
  manifest), emit the worksheet/fallback and wait.

## Backend security guardrails
Applies to any [STACK] with authenticated surfaces, admin panels,
databases, or public forms writing server-side. Treat as
non-negotiable regardless of framework.

- Roles live in a dedicated store (e.g. a `user_roles` table with a
  strict foreign key to the user id), never as an `is_admin` flag on
  a profile/users row, and are checked server-side on every request.
  (On Supabase/Postgres-RLS stacks, use a security-definer function;
  on other stacks, the equivalent server-side middleware/policy
  check.) Profile-row admin flags are a known privilege-escalation
  pattern.
- Never expose API keys, service-role keys, or third-party secrets
  client-side. Anon/publishable keys only in the browser bundle;
  every privileged call goes through a server or edge function that
  reads the secret from environment/secret storage.
- Every public form (contact, quote request, signup, comment, review
  submission) has server-side rate limiting — per IP, per session,
  and per email — plus a bot-defense layer (invisible CAPTCHA,
  honeypot field, or platform-native equivalent).
- Every field written to the database is validated AND sanitized
  server-side before insert (length caps, type checks, allow-list for
  enums, HTML/script stripping for free-text that will be
  re-rendered). Client-side validation is UX, not security.
- Every admin/portal/dashboard route enforces authentication AND
  authorization on the server (RLS policy, middleware guard, or
  edge-function check) — never rely on hiding a nav link or a
  client-side redirect. Direct URL access returns 401/403.
- Never track admin/portal/auth surfaces in the analytics layer, and
  never index them (robots.txt, Phase 1.2).

## Privacy & consent guardrails
- If [PRIVACY_SCOPE] includes the EU/UK (or is unknown): no analytics
  identifiers, visitor_id, or UTM persistence before explicit
  consent. Ship a consent layer in Phase 1.9, not after.
- Honor Global Privacy Control signals where CCPA/CPRA applies.
- The site ships with a real privacy policy naming every processor
  (analytics, chat, forms, session replay). No placeholder policy.
- Session replay masks all form inputs by default.
- IP handling: truncate/anonymize where the analytics platform
  allows. First-party analytics tables count as personal data — they
  get a retention limit (≤14 months default) and a deletion path.
- Never A/B test consent UI toward higher acceptance (dark pattern;
  unlawful in several EU jurisdictions).

## Vibe-coding hygiene sweep
Run at the END of Phases 1, 2, 3, 4, and 5, before the phase's change
set is presented for review. LLM-assisted builds reliably accumulate
the defects below; sweeping once at the end of the project is too
late because Phase 4 multiplies them ×50 pages.

### Catastrophic-in-this-context (check first, every time)
- Staging artifacts in prod: leftover `noindex` meta/header, a
  template robots.txt still blocking all crawlers, or a `Disallow: /`
  from development. Any one of these silently zeroes the entire SEO
  program. Verify with a fresh fetch of robots.txt + spot-check the
  rendered <head> on 5 URLs.
- Placeholder content shipped: lorem ipsum, "TODO", fake phone
  numbers / addresses / testimonials left from scaffolding. This
  violates the first content guardrail in production. Grep for:
  lorem, TODO, FIXME, 555-, example.com, "John Doe", placeholder.
- Duplicate or hand-rolled JSON-LD: components copy-pasted with their
  own `<script type="application/ld+json">` emit conflicting graphs.
  Grep for ld+json outside the schema engine; count blocks per
  rendered page (expect exactly one @graph).
- Copy-pasted meta: identical <title> or description across pages
  cloned from a template. Diff titles sitewide; duplicates = HIGH.

### Code hygiene
- Dead code: unused components, unused deps (npx depcheck / knip),
  commented-out blocks, unreferenced assets. Delete, don't keep "just
  in case" — the git history is the just-in-case.
- Duplicate components: Button + ButtonNew + Button2, Hero +
  HeroFinal. Consolidate to one, wired to the 0.7.2 token sheet.
- Orphan routes: pages that lost their nav link but still render, get
  crawled, and get indexed. Cross-check the route table against the
  sitemap and nav; orphans are removed or 301'd.
- Debug residue: console.log / print / debug flags / verbose error
  output in prod builds. Grep and strip.
- Secrets: scan the client bundle and repo history for API keys
  (gitleaks or equivalent). Anything privileged found client-side is
  CRITICAL and gets rotated, not just removed.
- Suppression debt: count @ts-ignore / any / eslint-disable added
  this phase. More than a handful of new ones = stop and fix, not
  annotate.
- Error boundaries / try-catch on every external call (GSC connector,
  form posts). A failed fetch renders a designed error state (0.7.3),
  never a blank screen.
- Broken internal links after route renames: run a link check (crawl
  or linkinator) before the phase closes.
- Dependency audit: npm audit / equivalent; lockfile committed; no
  dependency added for one function a stdlib call covers.
- DB/migration drift: schema changes exist as committed migrations,
  not hand-edits to a live database.

The sweep's output is a one-page checklist appended to the phase's
"what changed" report. No phase is "done" with an unswept box.
