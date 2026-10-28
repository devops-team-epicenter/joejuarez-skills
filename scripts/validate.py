#!/usr/bin/env python3
"""Validate every skill folder in this repo.

Checks, for each top-level folder that contains a SKILL.md:
  - SKILL.md starts with YAML frontmatter on line 1
  - `name` exists and matches the folder name (lowercase, hyphenated)
  - `description` exists and is under claude.ai's 1024-character limit
  - only frontmatter keys claude.ai accepts are used
  - SKILL.md stays under ~500 lines (move bulk into references/)

Usage:  python3 scripts/validate.py        (exit code 1 on any error)
Requires PyYAML:  pip install pyyaml
"""
import re
import sys
from pathlib import Path

import yaml

ALLOWED_KEYS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_DESCRIPTION = 1024
MAX_LINES = 500

root = Path(__file__).resolve().parent.parent
errors, warnings = [], []

for skill_md in sorted(root.glob("*/SKILL.md")):
    folder = skill_md.parent.name
    text = skill_md.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        errors.append(f"{folder}: SKILL.md must start with '---' frontmatter on line 1")
        continue
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        errors.append(f"{folder}: frontmatter is not valid YAML ({e})")
        continue

    extra = set(fm) - ALLOWED_KEYS
    if extra:
        errors.append(f"{folder}: frontmatter keys claude.ai rejects: {sorted(extra)}")
    name = fm.get("name")
    if name != folder:
        errors.append(f"{folder}: name {name!r} must equal the folder name")
    elif not NAME_RE.match(name):
        errors.append(f"{folder}: name must be lowercase and hyphenated")
    desc = fm.get("description")
    if not desc or not str(desc).strip():
        errors.append(f"{folder}: description is missing")
    elif len(str(desc)) > MAX_DESCRIPTION:
        errors.append(f"{folder}: description is {len(str(desc))} chars (limit {MAX_DESCRIPTION})")

    lines = text.count("\n") + 1
    if lines > MAX_LINES:
        warnings.append(f"{folder}: SKILL.md is {lines} lines; consider moving material into references/")

for w in warnings:
    print("WARN ", w)
for e in errors:
    print("ERROR", e)
count = len(list(root.glob("*/SKILL.md")))
print(f"{count} skill(s) checked, {len(errors)} error(s), {len(warnings)} warning(s)")
sys.exit(1 if errors else 0)
