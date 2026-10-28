---
name: cms-page-builder
description: >-
  Design and build a block-based visual CMS for editing a project's front-end
  pages — a drag-to-canvas page builder with a typed block model, container
  nesting, live preview, draft/publish versioning with immutable published
  snapshots, merge-token/data binding, and an isomorphic block-render registry.
  Use when a project needs non-developers (or an LLM) to visually create and
  edit website/landing/marketing pages, when adding a "page builder", "visual
  editor", "content editor", "block editor", or "headless CMS front-end", or
  when extending an existing builder with a new block type, a new renderer
  target (web / PDF / email), or a publish workflow.
---

# CMS Page Builder — Architecture & Implementation Skill

This skill is a complete, reusable blueprint for building a **block-based visual
CMS** that lets people (and LLMs) edit the front-end pages of a project:
drag-to-canvas editing, immutable versioned snapshots, an isomorphic renderer
that can target an on-screen preview and other outputs such as PDF or email,
merge-token interpolation, and interactive/data-bound blocks.

Read this top-to-bottom before writing code. The **Golden Rules** and
**Hard-Won Pitfalls** sections encode failures that are expensive to rediscover.

---

## 1. When to use this skill

Use it when any of these are true:

- A project has hard-coded front-end pages (hero, features, pricing, about,
  landing pages) and non-developers need to edit them without touching code.
- You are asked to add a "page builder", "visual editor", "content editor",
  "block/section editor", "landing-page builder", or a "front-end CMS".
- You need editable pages that still render inside the project's own design
  system (not an iframe of a third-party builder), with the same components the
  developers already ship.
- You are extending an existing builder: adding a **new block type**, a **new
  render target** (web page, PDF export, email), a **publish/preview workflow**,
  **localization**, or **A/B variants**.

Do **not** reach for a heavyweight third-party page builder if the project just
needs 2–3 editable text fields — a keyed key/value content table is simpler. Use
this skill when authors need *layout* control (adding/removing/reordering
sections), not just copy edits.

---

## 2. Core mental model (the 6 pillars)

1. **A page is an ordered tree of typed blocks.** Not HTML, not a WYSIWYG blob.
   Each block has a `block_type`, a typed `content_json`, optional `style_json`,
   and a position (`sort_order` + `parent_id` for nesting). This is the single
   source of truth.
2. **One block registry drives everything.** A block type is defined *once*
   (schema + default content + editor form + renderer) and every surface
   (editor canvas, live site, preview, PDF/email export) reads from that same
   registry. Adding a block = adding one registry entry, not editing five files.
3. **Isomorphic rendering.** The same block tree renders in the editor (with
   selection chrome and inline editing) and on the published site (clean). The
   renderer is a pure function `render(blockTree, dataContext) -> UI`.
4. **Draft/edit is mutable; published is an immutable snapshot.** Authors edit a
   working draft. Publishing **freezes a full copy** of the resolved content
   into a versioned, read-only snapshot. The live site serves the snapshot, so
   editing a draft never mutates what visitors see, and every publish is
   auditable and instantly rollback-able.
5. **Content can be static or data-bound.** Blocks may hold literal content
   (a paragraph) or **bind to data** via merge tokens (`{{site.phone}}`) and
   **dynamic/collection blocks** (e.g. "latest 3 blog posts"). Binding resolves
   at render time against a typed data context.
6. **Interactivity is declared, validated server-side, and never trusted from
   the client.** Forms, CTAs, and any block that captures input declare their
   fields in the block model; the server re-derives what is required from the
   snapshot and validates independently of the client.

If you internalize only one thing: **typed block tree + one registry + immutable
published snapshot.**

---

## 3. Data model

Two storage shapes work; pick based on query needs.

### 3.1 Option A — Row-per-block (best for querying/reordering at scale)

`page_blocks` (the authoring/draft tree; authoritative while editing):

| column | type | notes |
|---|---|---|
| `id` | uuid pk | |
| `tenant_id` | uuid | multi-tenant scope (drop if single-tenant) |
| `page_id` | uuid fk | the page this block belongs to |
| `block_type` | text (enum) | one of the registered block types |
| `sort_order` | int | order **within the same parent** |
| `parent_id` | uuid null | null = top level; else a container block |
| `container_kind` | text | `section` \| `row` \| `column` \| `content` |
| `content_json` | jsonb | typed per `block_type` (see §4) |
| `style_json` | jsonb | spacing, background, per-block overrides |
| `layout_json` | jsonb | container layout (ratios, gap, stack-on-mobile) |
| `visibility_rules_json` | jsonb | optional conditional display rules |
| `created_by` / `created_at` / `updated_at` | | audit |

### 3.2 Option B — JSON document per page (simplest; great default)

`pages.draft_content_json` holds the entire block tree as one JSON array
(`[{ id, block_type, sort_order, parent_id, container_kind, content_json,
style_json, layout_json, children? }]`). Fewer rows, trivial snapshotting,
atomic saves. Prefer this unless you need SQL-level block queries. The source
system uses row-per-block for authoring **and** serializes the whole tree into a
single `content_snapshot_json` on publish — a common, pragmatic hybrid.

### 3.3 Pages and revisions

`pages`:

| column | notes |
|---|---|
| `id`, `tenant_id` | |
| `slug` / `path` | URL path; unique per tenant/site + locale |
| `title`, `seo_json` | meta title/description, OG image, canonical, robots |
| `status` | `draft` \| `published` \| `scheduled` \| `archived` |
| `draft_content_json` (Option B) | current editable tree |
| `current_revision_id` | fk → the live published revision |
| `locale` / `variant` | i18n + A/B (optional) |

`page_revisions` (immutable, one row per publish):

| column | notes |
|---|---|
| `id`, `page_id`, `tenant_id` | |
| `revision_no` | monotonic per page |
| `content_snapshot_json` | **frozen full block tree, with data bindings resolved as far as is safe** (see §7.3) |
| `content_hash` | hash of the snapshot for integrity + change detection |
| `rendered_html` (optional) | pre-rendered HTML/ISR cache key |
| `published_at`, `published_by` | |
| `status` | `published` \| `superseded` \| `rolled_back` |

**Immutability is enforced, not conventional.** Use a DB trigger/constraint so a
published revision's `content_snapshot_json` and `content_hash` can never be
updated. Editing produces a *new* draft → a *new* revision. This is the single
most important safety property, so enforce it in the database rather than
trusting application code.

### 3.4 Supporting tables

- `media_assets` — uploaded images/files (storage path, mime, dimensions, alt).
- `content_types` / `entries` — for dynamic/collection blocks (blog, team, FAQ).
- `page_events` — audit log (`created`, `edited`, `published`, `rolled_back`,
  `previewed`), with actor + payload. Invaluable for debugging "why does the
  live page show X" and for a visible activity feed.

---

## 4. The block model

### 4.1 Block type catalog (generalized for websites)

Start from this catalog; it maps the source document blocks onto page-building
needs. Each is one registry entry.

**Structure / layout**
- `section` — full-width band; holds background, vertical padding, max content
  width. Top-level rhythm of a page.
- `row` — horizontal flex/grid of columns; carries `ratios`, `gap`,
  `stackOnMobile`.
- `column` — vertical stack inside a row; carries `ratio`, `hideOnMobile`.
- `spacer` — vertical gap (`height_px`, responsive variants).
- `divider` — horizontal rule.

**Content**
- `heading` — `text`, `level` (1–6), `align`. Supports merge tokens.
- `paragraph` — plain text + `align`. Supports merge tokens.
- `rich_text` — sanitized HTML (from a TipTap/ProseMirror-style editor).
  Supports merge tokens **and inline field/token spans** (see §6.3).
- `bullet_list` / `numbered_list` — `items[]`.
- `image` — `asset_id`/`storage_path`, `alt`, `caption`, `width_mode`
  (`small|medium|large|full_width`), `align`, optional `overlay` (positioned
  HTML + scrim for hero text over an image), `rounded`.
- `hero` — composed block: background image/video + eyebrow/title/subtitle +
  CTA(s). (In the source this is `cover` + `image.overlay`; expose as one block
  for authors.)
- `gallery` / `carousel` — array of assets.
- `video_embed` / `embed` — provider URL or raw embed (sanitized/allow-listed).

**Interactive / conversion**
- `cta` / `button` — label, href, style variant, target.
- `form` — declared fields (see §6.4 & §8); submissions handled server-side.
- `accordion` / `tabs` — nested content groups.

**Dynamic / data-bound**
- `collection` — render N entries of a content type with a chosen layout
  ("latest 3 posts", "all team members"). Query + template, resolved at render.
- `merge_token` — inline single value (`{{site.phone}}`).
- Domain blocks (source has `pricing_block`, `service_summary`,
  `coverage_summary`, `payment_terms`) — **project-specific data-bound blocks**.
  These are the template for any "pull structured data from the app and render a
  formatted table/summary" block.

**Page meta / chrome**
- `seo_meta` — title, description, OG, canonical, robots (usually a page-level
  panel rather than an in-canvas block).
- `nav` / `footer` — often global/shared blocks referenced by many pages.

Keep the enum in one place (`BLOCK_TYPES`) and derive labels
(`BLOCK_LABEL`) and defaults (`defaultContentFor`) from it.

### 4.2 Typed content per block

Give every block type a `content_json` TypeScript type. Make **all fields
optional** so partial content survives schema evolution and round-trips; supply
defaults at render time. Example shape (mirrors the source):

```ts
export const BLOCK_TYPES = [
  "section","row","column","spacer","divider",
  "heading","paragraph","rich_text","bullet_list","numbered_list",
  "image","hero","gallery","embed",
  "cta","form","accordion","tabs",
  "collection","merge_token","seo_meta",
] as const;
export type BlockType = (typeof BLOCK_TYPES)[number];

export type HeadingContent   = { text?: string; level?: 1|2|3|4|5|6; align?: "left"|"center"|"right" };
export type ImageContent     = { asset_id?: string; alt?: string; caption?: string;
                                 width_mode?: "small"|"medium"|"large"|"full_width";
                                 align?: "left"|"center"|"right";
                                 overlay?: { html?: string; position?: string; scrim?: boolean }; rounded?: boolean };
export type CtaContent       = { label?: string; href?: string; variant?: "primary"|"secondary"|"link"; target?: "_self"|"_blank" };
export type CollectionContent= { content_type?: string; limit?: number; sort?: string; layout?: string; filter?: Record<string, unknown> };
// ...one per block type

export function defaultContentFor(t: BlockType): Record<string, unknown> {
  switch (t) {
    case "heading": return { text: "New heading", level: 2, align: "left" };
    case "cta":     return { label: "Learn more", href: "#", variant: "primary", target: "_self" };
    // ...
    default:        return {};
  }
}
```

### 4.3 Container nesting model

Four container kinds compose arbitrary layouts:
`section > row > column > (content blocks)`. Rules:

- A block's children are ordered by `sort_order` **within that parent**.
- Legacy/flat pages: rows with `parent_id = null` and
  `container_kind = "content"` are treated as a flat top-level list and wrapped
  implicitly. Support this so you can migrate incrementally.
- Build the tree once (`buildTree(blocks)`): sort by `sort_order`, index by
  `id`, attach each block to `byId.get(parent_id).children` else push to roots.
- `layout_json` lives on containers: `RowLayout { ratios, gap, stackOnMobile }`,
  `ColumnLayout { ratio, hideOnMobile }`, `SectionLayout { maxWidth }`.

Keep nesting depth bounded (section→row→column→content is enough for 95% of
pages). Deeper nesting explodes editor complexity for little gain.

---

## 5. The render registry (isomorphic)

The registry is the heart of the system. **Define each block once**; render it
everywhere.

```ts
type RenderCtx = {
  mode: "edit" | "published" | "preview";
  data: DataContext;                 // merge-token + binding source (§6)
  resolveAsset: (id: string) => string | null;
  registerField?: (f: FieldSpec) => void; // interactive blocks
};

type BlockDef<C> = {
  type: BlockType;
  label: string;
  defaultContent: () => C;
  schema: ZodSchema<C>;              // validate on save + before publish
  EditorForm: React.FC<{ value: C; onChange: (c: C) => void }>; // properties panel
  Render: React.FC<{ content: C; block: Block; ctx: RenderCtx }>; // canvas + site
  // optional capabilities:
  isContainer?: boolean;
  isInteractive?: boolean;          // contributes fields to forms
  supportsMergeTokens?: boolean;
  category: "structure"|"content"|"media"|"interactive"|"dynamic";
};

export const REGISTRY: Record<BlockType, BlockDef<any>>;
```

### 5.1 Render targets

The same tree feeds multiple renderers. Keep the **tree walk** shared; vary only
the leaf primitives:

- **Web (editor + published)** — React + the project's design system
  (Tailwind/shadcn). One component tree, `mode` flag toggles selection chrome and
  inline editing.
- **PDF / print export (optional)** — a separate primitive set (e.g.
  `@react-pdf/renderer`), because a browser DOM renderer and a PDF layout engine
  do not share primitives. **Do not try to render HTML strings in a PDF engine**
  — convert rich text to the PDF library's primitives (see Pitfalls).
- **Email (optional)** — table-based/MJML primitives.

Model this as: `renderTree(blocks, ctx, primitives)` where `primitives` is the
target-specific leaf set. The registry's `Render` is the web target;
alternate targets provide their own render map keyed by `block_type`.

### 5.2 Editor vs published rendering

Same components, two modes:

- `mode: "edit"` — wrap each block with selection outline, drag handle, hover
  toolbar (duplicate/delete/move), empty-state placeholders, and click-to-select
  that opens the properties panel. Inline-edit text where possible.
- `mode: "published"` — clean output, no chrome, SSR/SSG friendly, hydrate only
  interactive blocks (islands).

Never fork the two into separate component trees — that is how the preview drifts
from the live site. Gate chrome with the `mode` flag inside one component.

---

## 6. Content binding: merge tokens, dynamic data, inline fields

### 6.1 Merge tokens (`{{namespace.key}}`)

Text-bearing blocks (`heading`, `paragraph`, `rich_text`, lists, `hero`,
`cta.label`, etc.) support `{{token}}` interpolation resolved against a typed
**data context**.

Implement a single pure `interpolate(text, data)`:

- Resolve `{{a.b.c}}` by walking the data object.
- **Mapped-but-empty → empty string** (a known key whose value is null/empty
  renders `""`, not the literal token and not a placeholder). This precise rule
  is what stops sample values like "123 Main St" leaking into published pages.
- **Unmapped/unknown token →** either the registry's example value (author-time
  preview) or `""` (published). Decide per `mode` and be consistent.
- Keep a **token registry** (`{ token, label, exampleValue, group }`) that powers
  an insert-token menu and author-time previews.

### 6.2 Dynamic / collection blocks

A `collection` block stores a *query*, not results: `{ content_type, filter,
sort, limit, layout }`. At render time the server resolves the query against the
entries store and renders `limit` items with the chosen `layout` sub-template.
Cache per revision. This is how you get "latest posts" without freezing stale
data into the snapshot (see §7.3 for the freeze-vs-live tradeoff).

### 6.3 Inline fields/tokens inside rich text (advanced)

Rich-text blocks can embed inline, individually-addressable spans (tokens or
interactive fields) rather than only whole-block fields:

```html
<span data-fid="f1" data-ftype="text" data-label="Title"
      data-required="true" data-assign="visitor"
      data-fillable-field="true">placeholder</span>
```

Critical rules learned the hard way:

- **One composite key format, everywhere.** Address inline items by
  `"{blockId}#{fid}"` and use that identical key in (a) the editor's value map,
  (b) server persistence, and (c) the renderer's substitution. A mismatch between
  any two silently drops values. Standardize before writing the second consumer.
- **Substitute before flattening.** When a target can't render HTML (PDF), first
  replace each inline span with its resolved value in the HTML string, *then*
  convert to that target's primitives. Otherwise inline values vanish and you
  ship blank placeholders.
- **Validation is snapshot-authoritative.** Compute "required and empty" from the
  frozen snapshot's inline `data-required` attributes, not from a separate
  persisted list that may be missing rows for older content.

### 6.4 Interactive blocks (forms)

Interactive blocks declare their inputs in the block model. On the editor side
they render inputs; on submit, the **server** re-derives the required set from the
published snapshot and validates independently. Assign each field an owner where
relevant (e.g. author-prefilled vs visitor-filled). Never let the client decide
what is required or persist arbitrary keys — enumerate expected fields from the
snapshot and reject the rest.

---

## 7. Draft / preview / publish / rollback

### 7.1 Lifecycle

`draft → (preview) → published → (edit → new draft) → published(v2) → …`
with `rollback(vN)` and `archive`.

- **Draft**: the mutable working tree. Autosave or explicit save; keep it cheap.
- **Preview**: render the *draft* behind a short-lived, unguessable **preview
  token** (never a public URL; never put secrets in query strings). Preview uses
  the live renderer in `mode: "preview"` so authors see exactly the published
  output.
- **Publish**: freeze the draft into a new immutable `page_revisions` row, set
  `pages.current_revision_id`, bump `revision_no`, write a `published` event, and
  invalidate/rebuild any HTML/ISR cache. Publishing is the *only* action that
  changes what visitors see.
- **Rollback**: point `current_revision_id` at an earlier revision (optionally
  copy it into a new draft to continue editing). Because revisions are immutable,
  rollback is instant and lossless.

### 7.2 Concurrency & integrity

- Guard saves with an optimistic version/`updated_at` check to avoid clobbering a
  concurrent editor; surface a conflict rather than silently overwriting.
- Validate every block against its `schema` on save, and validate the whole tree
  again at publish (fail closed — never publish an invalid tree).
- Store `content_hash` and verify it when serving; a mismatch means corruption or
  tampering.

### 7.3 Freeze vs. live data — the key snapshot decision

When you publish, decide **per binding** whether to freeze the resolved value or
keep it live:

- **Freeze** content that must be stable/auditable at publish time (legal copy,
  the exact price shown, campaign wording). Store the resolved value in the
  snapshot.
- **Keep live** content that should always reflect current data (a phone number
  from settings, "latest posts", inventory counts). Store the *binding/query* in
  the snapshot and resolve at request time.

Make this explicit in each block's schema (e.g. `binding_mode: "freeze" | "live"`)
rather than implicit. Getting this wrong is a top source of "why is the site
showing old/new data" confusion.

---

## 8. Server / API contract

Expose a small, typed, auth-guarded API (server functions / REST / RPC). Minimum
surface:

**Authoring (auth required, tenant-scoped, permission-checked):**
- `listPages`, `getPage(id)` → returns draft tree + current revision meta.
- `createPage`, `updatePageMeta` (slug, title, SEO).
- `saveDraft(pageId, blockTreeOrPatch, expectedVersion)` — validates each block
  vs schema; optimistic-concurrency checked.
- Block ops if row-per-block: `addBlock`, `updateBlock`, `moveBlock`
  (reparent + reorder), `duplicateBlock`, `deleteBlock`.
- `previewToken(pageId)` → short-lived token for the preview route.
- `publish(pageId)` → freezes revision, flips `current_revision_id`, invalidates
  cache, logs event. Idempotent-ish; safe to retry.
- `rollback(pageId, revisionId)`, `listRevisions(pageId)`, `diffRevisions(a,b)`.
- `uploadAsset` / `listAssets`.

**Delivery (public, read-only):**
- `getPublishedPage(slugOrPath, locale)` → returns the current revision's
  snapshot (+ resolves live bindings). Cacheable (ETag = `content_hash`).
- `renderPage(...)` for SSR/SSG, or emit static HTML at publish time.
- `submitForm(pageId, blockId, values)` → server validates against the snapshot's
  declared fields; never trusts client-declared requiredness.

**Guardrails baked into the API layer:**
- Every authoring call re-checks tenant membership and role server-side.
- Published/immutable rows reject writes at the DB level, not just the app.
- Public delivery endpoints never expose author-only fields, tokens, or
  unpublished drafts.

---

## 9. Editor UX specification

The editor is three panes plus a top bar:

- **Left — block palette.** Grouped by category (Structure, Content, Media,
  Interactive, Dynamic). Drag onto the canvas or click to insert at selection.
- **Center — canvas.** Renders the block tree in `edit` mode with selection
  outlines, drag handles, hover toolbars (duplicate/delete/move up-down), empty
  drop zones, and a page-frame that mirrors published width. Support
  **responsive preview** (desktop/tablet/mobile toggles) driven by the same
  breakpoints the site uses. Inline-edit text directly in the canvas where
  practical; open the properties panel for structured fields.
- **Right — properties panel.** Renders the selected block's `EditorForm`
  (spacing, background, alignment, per-type fields) + a link to page-level SEO.
- **Top bar.** Undo/redo, Add page/section, device toggles, **Save draft**,
  **Preview**, **Publish**, and a status chip (Draft / Published / Unsaved).

Must-haves:

- **Undo/redo** over tree mutations (command stack or immutable snapshots).
- **Drag-and-drop** with valid drop targets only (a `column` accepts content;
  `section` accepts rows; enforce via `container_kind`).
- **Dirty-state tracking** and an unload guard so authors don't lose edits.
- **Keyboard**: arrow-move selection, delete, duplicate (Cmd/Ctrl+D), save
  (Cmd/Ctrl+S).
- **Empty states** and inline guidance ("Add your first section").
- **Gated primary actions** with reasons: disable Publish until the tree is valid
  and required page meta (slug/title) is set; on hover, say *why* it's disabled.
  (For example, a tooltip such as "Add a page title before publishing". Never a
  dead button with no explanation.)

---

## 10. Multi-tenancy, security & permissions

- **Row-level security** on every table keyed by `tenant_id`; the app resolves
  the caller's tenant server-side and never trusts a client-supplied tenant.
- **Roles**: at minimum `admin` (publish, settings), `editor` (draft + publish),
  `contributor` (draft only, no publish), `viewer`. Enforce publish/rollback as
  privileged.
- **Sanitize all HTML** from rich-text and embeds (allow-list tags/attrs) at save
  and again at render. Treat any author HTML and any embed URL as untrusted.
- **Assets**: serve via signed URLs or a CDN with correct content-types; validate
  uploads (mime, size, dimensions); never execute uploaded files.
- **Preview/links**: short-lived, unguessable tokens; nothing sensitive in query
  strings; immutable published snapshots so a leaked draft link can't alter live
  content.
- **Audit** every publish/rollback with actor + hash in `page_events`.

---

## 11. Accessibility, SEO & performance

- **Accessibility**: headings render as real `<h1..h6>` (enforce one h1/page;
  warn on skipped levels), images require `alt` (block validation), interactive
  blocks are keyboard-navigable, color/contrast handled by the design system.
- **SEO**: page-level `seo_meta` → `<title>`, meta description, canonical, robots,
  Open Graph/Twitter, and JSON-LD where relevant; clean slugs; sitemap generated
  from published pages; server-render published pages so crawlers get full HTML.
- **Performance**: prefer SSG/ISR — render published HTML at publish time and
  serve static, revalidating on publish. Hydrate only interactive "islands".
  Lazy-load below-the-fold images/embeds; set explicit image dimensions to avoid
  layout shift.

---

## 12. Testing strategy

- **Pure units** for the risky pure functions: `interpolate` (mapped-empty vs
  unmapped vs nested), `buildTree` (flat legacy, deep nesting, orphaned parent),
  reorder/reparent math, required-field derivation from a snapshot, and any
  formatter (trim trailing zeros, currency, dates) — **use one shared formatter
  and test it once**, don't re-implement per surface.
- **Registry contract test**: every `BlockType` in the enum has a registry entry
  with `defaultContent`, `schema`, `EditorForm`, and `Render`; `defaultContent`
  passes its own `schema`. This catches "added an enum value, forgot the
  renderer".
- **Snapshot/immutability test**: publishing freezes; a published revision cannot
  be mutated; rollback restores byte-identical output.
- **Renderer parity**: the same tree renders without throwing in every target
  (web + PDF/email if present); realistic fixtures (nested containers, an image,
  rich text with inline tokens, a data-bound block, a drawn signature/asset).
- **Import-boundary test** (if you have a heavy/native renderer): assert that no
  request/SSR path statically imports the heavy renderer (see Pitfall 6).
- **Server validation**: forms/interactive submits reject fields not declared in
  the snapshot and enforce snapshot-derived requiredness.

Keep tests green and typecheck clean on every change; treat a red suite as "not
done".

---

## 13. How an LLM should ADD A NEW BLOCK TYPE (recipe)

This is the most common extension. Do exactly this, in order:

1. **Add the enum value** to `BLOCK_TYPES` and a human label to `BLOCK_LABEL`.
2. **Define `content_json` type** (all fields optional) + a `zod` schema.
3. **Add `defaultContentFor(type)`** returning schema-valid defaults.
4. **Write `EditorForm`** (properties-panel form) — controlled inputs calling
   `onChange`.
5. **Write `Render`** for the **web** target, honoring `ctx.mode` (edit chrome vs
   clean) and `supportsMergeTokens` (run `interpolate`).
6. **Add alternate-target renderers** if the project exports PDF/email — map the
   block to that target's primitives; **never** pass HTML to a non-HTML engine.
7. **Register** the block in `REGISTRY` with its `category` and capability flags.
8. **If interactive/data-bound**: declare fields/bindings; extend server
   validation and the data-context resolver.
9. **Tests**: registry contract (auto-covers it), a render-parity fixture, and
   any new pure logic.
10. **Typecheck + run the full suite; verify in the editor and in a preview.**

If any surface renders `[BlockType]`/placeholder text or a blank where content
should be, you missed step 5/6 substitution or a key-format match (§6.3).

---

## 14. Hard-won pitfalls (do not rediscover these)

1. **WYSIWYG-HTML-blob CMS is a trap.** Storing a page as one HTML string makes
   layout edits, theming, targeting, and data binding nearly impossible. Use the
   typed block tree.
2. **A non-HTML export engine cannot render HTML strings.** PDF/email layout
   engines have their own primitives. Convert rich text → primitives, and
   **substitute inline tokens/fields into the string before flattening**, or the
   values disappear and you ship blank placeholders.
3. **Interactive/inline values silently drop when the key format differs across
   layers.** The editor, the persistence layer, and the renderer must use the
   *identical* addressing key (e.g. `blockId#fid`). Standardize first.
4. **Requiredness/validation must come from the frozen snapshot**, not a
   side-table that can be missing rows for older content. Derive it from what the
   viewer actually sees.
5. **"Mapped-but-empty" tokens must resolve to empty string**, not the literal
   `{{token}}` and not an example placeholder. Otherwise fake sample data
   (addresses, names) leaks into published pages.
6. **Heavy/native renderers must not be imported on the request path.** If a
   block renderer pulls in a WASM/native lib that a server/edge runtime can't
   load, importing it *anywhere reachable from a request* throws at module load
   and takes down the page — even inside a `try/catch`, because the failure is at
   import time. Keep such renderers behind dynamic, client-only or worker-only
   imports; add an import-audit test; provide a graceful fallback.
7. **Editing must never mutate what visitors see.** If drafts and live share one
   record, an autosave changes the live site. Immutable published snapshots
   prevent this — enforce immutability at the DB layer.
8. **Re-publishing/regenerating can invalidate shared links/caches.** Be explicit
   about cache invalidation on publish, and warn authors when an action replaces
   something already shared (the source learned this with signing links —
   generalize it to preview links and CDN cache).
9. **Silent best-effort steps hide failures.** If publish-time rendering, image
   processing, or cache warmup can fail, **record the failure as an event** and
   surface it — don't only `console.error`. Undiagnosable "it just doesn't work"
   comes from swallowed errors.
10. **One formatter, one source of truth.** Duplicated number/date/currency
    formatting across preview/site/PDF drifts (e.g. `9.50` vs `9.5`). Centralize
    and test once.
11. **Dead buttons frustrate.** Gate actions with computed conditions and show
    the reason on hover; auto-populate obvious inputs (e.g. seed a page's author
    or a form's default recipient) instead of forcing manual entry.
12. **Deliverability/config lives outside the app.** If the CMS sends email
    (form notifications, publish alerts), authenticate the sending domain
    (SPF/DKIM/DMARC) — an app bug is often actually a DNS/auth problem.

---

## 15. Phased implementation checklist

**Phase 0 — Foundations**
- [ ] Decide storage (Option A row-per-block vs Option B JSON-per-page).
- [ ] Create `pages`, `page_revisions` (+ `page_blocks` if Option A), `media_assets`, `page_events`.
- [ ] Enforce revision immutability at the DB level.
- [ ] Stand up RLS + roles.

**Phase 1 — Block model + registry**
- [ ] `BLOCK_TYPES`, `BLOCK_LABEL`, typed `content_json`, `zod` schemas, `defaultContentFor`.
- [ ] `REGISTRY` with `EditorForm` + web `Render` for a starter set
      (section/row/column, heading, paragraph, rich_text, image, cta, spacer, divider).
- [ ] `buildTree` + shared tree-walk renderer; registry contract test.

**Phase 2 — Editor**
- [ ] Three-pane editor, drag-to-canvas, selection, properties panel.
- [ ] Undo/redo, dirty-state guard, keyboard shortcuts, responsive preview.
- [ ] Save draft (optimistic concurrency) + block CRUD/reorder/reparent.

**Phase 3 — Binding & dynamic content**
- [ ] `interpolate` + token registry + insert-token menu.
- [ ] `collection`/dynamic blocks + data-context resolver.
- [ ] Freeze-vs-live decision per binding.

**Phase 4 — Publish pipeline**
- [ ] Validate-then-freeze publish; `current_revision_id`; revision list/diff/rollback.
- [ ] Preview route with short-lived token.
- [ ] Public delivery endpoint + SSR/SSG + cache invalidation on publish.

**Phase 5 — Hardening**
- [ ] HTML/embed sanitization; asset validation; SEO/a11y validation on publish.
- [ ] Alternate render targets (PDF/email) if needed, with import-boundary safety.
- [ ] Full test suite (units, registry contract, snapshot immutability, renderer parity, server validation) green + typecheck clean.

---

## 16. Glossary

- **Block** — a typed unit of content/layout with `content_json`.
- **Block tree** — the ordered, nested set of blocks that composes a page.
- **Registry** — the single map from `block_type` → schema/default/editor/render.
- **Isomorphic renderer** — one renderer that serves editor, preview, and site.
- **Snapshot / revision** — an immutable frozen copy of a page's content at publish.
- **Merge token** — `{{namespace.key}}` resolved against the data context.
- **Data context** — the typed object bindings resolve against at render time.
- **Binding mode** — per-field choice to freeze the value at publish or keep it live.
- **Container kind** — `section | row | column | content`; drives nesting + layout.

