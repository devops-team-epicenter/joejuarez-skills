# JoeJuarez-Skills

A personal library of [Claude Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/) — reusable instruction packs that Claude loads on demand in Claude Code, the Claude desktop app, and claude.ai.

Each skill lives in its own folder with a `SKILL.md` at the root. Claude reads the frontmatter (`name` + `description`) to decide *when* to use a skill, and the Markdown body for *how*.

## Skills

| Skill | What it does | Trigger phrases |
|-------|--------------|-----------------|
| [`chat-recap`](chat-recap/) | Rebuilds orientation in a long or branching conversation: reconstructs thread statuses, surfaces open decisions, recommends a focus, assesses context efficiency, and prepares a checkpoint for compaction or a fresh session. Deliberately does **not** execute unfinished work on its own. | `Chat-Recap`, `recap this chat`, `where were we`, `what's still open`, `help me refocus` — plus modifiers like `Chat-Recap, quick`, `Chat-Recap, checkpoint`, `Chat-Recap on [topic]` |

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
git clone https://github.com/<owner>/JoeJuarez-Skills.git ~/JoeJuarez-Skills
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
4. Validate the frontmatter before committing:

   ```bash
   python3 - <<'EOF'
   import re, yaml, sys
   t = open("my-skill/SKILL.md", encoding="utf-8").read()
   m = re.match(r"^---\n(.*?)\n---\n", t, re.S) or sys.exit("no frontmatter")
   fm = yaml.safe_load(m.group(1)); assert fm["name"] == "my-skill"; print("OK", fm["name"])
   EOF
   ```

5. Add a row to the **Skills** table above.

## Layout

```
JoeJuarez-Skills/
├── README.md
├── .gitignore
└── chat-recap/
    └── SKILL.md
```

Optional per-skill subfolders: `scripts/`, `references/`, `assets/`. Eval workspaces (`<skill>-workspace/`) and packaged `.skill` files are git-ignored — regenerate them, don't commit them.
