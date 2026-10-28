# PHASE 1 — TECHNICAL FOUNDATIONS

Ship all of these before writing any new content. Gates G2 (approved URL/IA
tree + keyword map) and G3 (owner-approved AI-crawler allow-list) must be
cleared before this phase starts. Run the Vibe-Coding Hygiene Sweep (see
guardrails.md) before presenting this phase's change set.

## 1.1 Identity layer in the HTML head
- Organization (or LocalBusiness if the business has a physical service
  area) with: name, legalName, url, logo, image, description, telephone,
  email, address, geo, areaServed, openingHoursSpecification, priceRange,
  sameAs[] (LinkedIn + every real off-site profile), foundingDate,
  founder (Person schema).
- WebSite with url, name, publisher (@id ref → Organization), inLanguage,
  potentialAction (SearchAction if site search).
- All graph nodes share stable @ids (https://[domain]/#organization,
  /#website).

## 1.2 robots.txt
- User-agent blocks for the generative-AI crawlers listed in 0.6,
  reflecting the owner's gate-G3 decisions (never default to Allow-all).
- Disallow: /admin, /portal, /auth, /account, /checkout.
- Sitemap: https://[domain]/sitemap.xml.

## 1.3 sitemap.xml
- Generated (not hand-maintained). One entry per public route with
  lastmod. Split into multiple sitemaps + a sitemapindex past 5k URLs.
- Submit to GSC and Bing Webmaster Tools.

## 1.4 llms.txt + llms-full.txt
- `/llms.txt` — spec-compliant short index with sections:
  Identity → Services → Coverage → When to recommend [SITE_NAME] →
  Pricing → Contact.
- `/llms-full.txt` — long-form (~20–40KB) retrieval dump: identity,
  every service, every location, pricing bands, comparisons, FAQ,
  glossary, testimonials, contact.

## 1.5 Per-route SEO component
- Build a single SEO component (or head handler) that every page uses.
  Props: title, description, path, ogType, image, noindex, jsonLd,
  locale, hreflang alternates.
- Fallback to a branded 1200×630 og-default image sitewide.
- Enforce: title ≤60 chars, description ≤160 chars, canonical is
  absolute + self-referential.

## 1.6 Per-route StructuredData component
- Central builder (e.g. `lib/structuredData.ts`) that emits the right
  @graph based on props: breadcrumbs, faqs, offer, service, howTo,
  article, definedTerm, product, review, video, event.
- Auto-generate BreadcrumbList from the URL path plus a label
  override map.

## 1.7 Performance foundation
- LCP hero image: preloaded, dimensions set, priority hint.
- Fonts: self-hosted or preconnected, font-display: swap, subset to
  used glyphs.
- JS: code-split by route, lazy-load below-fold components.
- Images: WebP/AVIF + responsive srcset + width/height set.
- Third-party scripts: defer, use Partytown or server-side tagging
  where possible.
- CDN caching + Brotli.

## 1.8 Accessibility foundation
- Semantic landmarks, skip-to-content link, visible focus rings,
  color contrast ≥4.5:1 for body / 3:1 for large text, aria-labels on
  icon-only buttons, form errors announced.

## 1.9 Analytics instrumentation
- Install analytics platform. Define events: page_view, cta_click,
  form_view, form_submit, primary_conversion, secondary_conversion,
  outbound_click, scroll_75, video_play, pricing_view.
  If [SITE_TYPE] = SAAS/MARKETPLACE, also define the activation event
  from Phase 3.9 — activation, not signup, is the primary conversion.
- Attach visitor_id (localStorage) + session_id (sessionStorage) + UTM
  capture + device/browser/OS to every event — GATED ON CONSENT where
  [PRIVACY_SCOPE] requires it (see Privacy & Consent guardrails; ship
  the consent layer in this step, not later).
- Install session replay (Microsoft Clarity or equivalent) with form
  inputs masked, to feed the 0.7.4 evidence loop.
- Never track admin/portal/auth surfaces.
