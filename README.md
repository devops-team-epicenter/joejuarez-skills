# JoeJuarez-Skills

A personal library of [Claude Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/) — reusable instruction packs that Claude loads on demand in Claude Code, the Claude desktop app, and claude.ai.

Each skill lives in its own folder with a `SKILL.md` at the root. Claude reads the frontmatter (`name` + `description`) to decide *when* to use a skill, and the Markdown body for *how*.

## Skills

| Skill | What it does | Trigger phrases |
|-------|--------------|-----------------|
| [`chat-recap`](chat-recap/) | Rebuilds orientation in a long or branching conversation: reconstructs thread statuses, surfaces open decisions, recommends a focus, assesses context efficiency, and prepares a checkpoint for compaction or a fresh session. Deliberately does **not** execute unfinished work on its own. | `Chat-Recap`, `recap this chat`, `where were we`, `what's still open`, `help me refocus` — plus modifiers like `Chat-Recap, quick`, `Chat-Recap, checkpoint`, `Chat-Recap on [topic]` |
| [`tracking-linear`](tracking-linear/) | Keeps development work tied to Linear from request to release: finds or creates the matching issue, classifies it (Bug / UX Improvement / Feature), links every PR, writes a plain-language brief and fix summary, and reconciles merge, deployment and QA status only from verified evidence. Configure team, statuses, labels and environments per repository (see §1 of the skill). | `--linear`, e.g. `--linear Fix checkout when a discount code has expired.`, `--linear ABC-123 Implement the requested changes.`, `--linear Reconcile this PR with its ticket.` |
| [`prep-handoff`](prep-handoff/) | Writes a short conversation summary plus a copy-paste re-entry prompt before you `/compact` or `/clear`, so work resumes cleanly in a fresh context. Lighter than `chat-recap`'s checkpoint mode: use it when you already know you're about to reset. | `prep a handoff`, `save context`, `write a re-entry prompt`, `snapshot where we are` |
| [`cms-page-builder`](cms-page-builder/) | Architecture blueprint for a block-based visual CMS / page builder: typed block model, container nesting, isomorphic render registry, draft/publish with immutable snapshots, merge tokens, and a list of hard-won pitfalls. | `page builder`, `visual editor`, `block editor`, `headless CMS front-end`, adding a block type or renderer target |
| [`universal-cro-seo-aeo-geo`](universal-cro-seo-aeo-geo/) | Phased audit-and-build program for CRO, SEO, AEO/GEO (visibility in AI answer engines) and UX on any site type or stack, with human approval gates and a site-type overlay. Phase detail lives in `references/`. | `review my site`, `SEO strategy`, `get cited by ChatGPT`, `make this page convert`, `new site for my business` |

## Install

### Claude Code

Skills load from one of two directories. Copy (or symlink) the skill folder into whichever fits:

```bash
# Project-scoped — commit it so collaborators get it too
mkdir -p .claude/skills
cp -r /path/to/JoeJuarez-Skills/chat-recap .claude/skills/

# Personal — available in every project on this machine
mkdir -p ~/.claude/skills
cp -r /path/to/JoeJuarez-Skills/chat-recap ~/.claude/skills/
```

Or clone once and symlink so `git pull` keeps every machine current:

```bash
git clone https://github.com/devops-team-epicenter/joejuarez-skills.git ~/JoeJuarez-Skills
ln -s ~/JoeJuarez-Skills/chat-recap ~/.claude/skills/chat-recap
```

Once installed the skill appears in the `/` menu as `/chat-recap`.

### claude.ai, desktop app, and cloud sessions

Personal `~/.claude/skills` entries do **not** reach Cowork or cloud sessions — those use skills enabled on your claude.ai account. Package the folder and upload it:

```bash
# A .skill file is a zip containing the skill folder (chat-recap/SKILL.md inside the zip)
cd JoeJuarez-Skills && zip -r chat-recap.skill chat-recap -x '*.DS_Store' '*/__pycache__/*'
```

Then upload `chat-recap.skill` under **Customize** in the desktop app sidebar, or in claude.ai's skills settings. Claude.ai only accepts these frontmatter keys: `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools` — anything else fails with "Unexpected key(s)".

Reference: [Claude Code skills docs](https://code.claude.com/docs/en/skills).

## Adding a new skill

1. Create a folder whose name **is** the skill name — lowercase, hyphenated (`my-skill/`).
2. Add `my-skill/SKILL.md` starting with frontmatter on line 1:

   ```yaml
   ---
   name: my-skill
   description: >
     What it does AND when Claude should reach for it. Put the key use case
     first and include the exact phrases that should trigger it.
   ---
   ```

3. Write the body in the imperative. Explain *why* each rule matters rather than stacking ALL-CAPS musts; keep `SKILL.md` under ~500 lines and move bulk material into `references/`, deterministic helpers into `scripts/`, templates into `assets/`.
4. Validate every skill before committing (checks frontmatter keys claude.ai accepts, name/folder match, description length, and SKILL.md size):

   ```bash
   pip install pyyaml   # once
   python3 scripts/validate.py
   ```

5. Add a row to the **Skills** table above.

## Layout

```
JoeJuarez-Skills/
├── README.md
├── LICENSE
├── .gitignore
├── scripts/
│   └── validate.py            # frontmatter + size checks for every skill
├── chat-recap/
│   └── SKILL.md
├── prep-handoff/
│   └── SKILL.md
├── cms-page-builder/
│   └── SKILL.md
├── universal-cro-seo-aeo-geo/
│   ├── SKILL.md
│   └── references/            # one file per phase, guardrails, worked example
└── tracking-linear/
    ├── SKILL.md
    └── references/
        └── release-and-qa.md
```

Optional per-skill subfolders: `scripts/`, `references/`, `assets/`. Eval workspaces (`<skill>-workspace/`) and packaged `.skill` files are git-ignored — regenerate them, don't commit them.

## License

[MIT](LICENSE). Use, adapt, and redistribute freely.
