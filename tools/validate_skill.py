#!/usr/bin/env python3
"""Validate the distributable manage-obsidian-project-kb Skill without dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
FRONTMATTER_FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$")
UI_FIELD_RE = re.compile(r'^  ([a-z_]+):\s*"([^"]*)"\s*$', re.MULTILINE)
RESOURCE_RE = re.compile(r"`((?:assets|references)/[^`]+)`")
START_MARKER = "<!-- kb:agents-bridge:start -->"
END_MARKER = "<!-- kb:agents-bridge:end -->"


def _read(path: Path, errors: list[str]) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"cannot read UTF-8 file {path}: {exc}")
        return ""


def _frontmatter(text: str, errors: list[str]) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        errors.append("SKILL.md must start with YAML frontmatter")
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        errors.append("SKILL.md frontmatter is not closed")
        return {}

    fields: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = FRONTMATTER_FIELD_RE.match(line)
        if not match:
            errors.append(f"unsupported frontmatter line: {line!r}")
            continue
        key, value = match.groups()
        fields[key] = value.strip('"\'')
    return fields


def validate(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_dir = skill_dir.resolve()
    skill_file = skill_dir / "SKILL.md"
    text = _read(skill_file, errors)
    if not text:
        return errors

    fields = _frontmatter(text, errors)
    unexpected = sorted(set(fields) - {"name", "description"})
    if unexpected:
        errors.append(f"unexpected SKILL.md frontmatter fields: {', '.join(unexpected)}")

    name = fields.get("name", "")
    description = fields.get("description", "")
    if not NAME_RE.fullmatch(name):
        errors.append("name must use 1-64 lowercase letters, digits, or hyphens")
    if name and skill_dir.name != name:
        errors.append(f"directory name {skill_dir.name!r} must match skill name {name!r}")
    if not description:
        errors.append("description is required")
    elif len(description) > 1024:
        errors.append(f"description exceeds ZCode's 1024-character limit: {len(description)}")
    if len(text.encode("utf-8")) > 100_000:
        errors.append("SKILL.md exceeds ZCode's 100 KB body limit")
    if len(text.splitlines()) > 500:
        errors.append("SKILL.md exceeds the recommended 500-line context budget")

    required = [
        "agents/openai.yaml",
        "assets/AGENTS-bridge.md",
        "references/markdown-templates.md",
    ]
    for relative in required:
        if not (skill_dir / relative).is_file():
            errors.append(f"missing required resource: {relative}")

    for relative in sorted(set(RESOURCE_RE.findall(text))):
        if not (skill_dir / relative).is_file():
            errors.append(f"SKILL.md references missing resource: {relative}")

    bridge = _read(skill_dir / "assets/AGENTS-bridge.md", errors)
    if bridge:
        if bridge.count(START_MARKER) != 1 or bridge.count(END_MARKER) != 1:
            errors.append("AGENTS bridge must contain exactly one start and one end marker")
        if bridge.find(START_MARKER) > bridge.find(END_MARKER):
            errors.append("AGENTS bridge markers are reversed")
        if not re.search(r"<!-- kb:agents-bridge:version=\d+ -->", bridge):
            errors.append("AGENTS bridge version marker is missing")
        if name and f"${name}" not in bridge:
            errors.append("AGENTS bridge must explicitly invoke this skill")

    required_protocol_tokens = [
        "Schema_Version",
        "/kb-doctor",
        "{Project_Root}/AGENTS.md",
        "AGENTS.override.md",
        "git rev-parse --git-path info/exclude",
    ]
    for token in required_protocol_tokens:
        if token not in text:
            errors.append(f"SKILL.md is missing release protocol token: {token}")

    templates = _read(skill_dir / "references/markdown-templates.md", errors)
    for heading in [
        "## Project Dashboard",
        "## Current Sprint",
        "## Permanent atomic note",
        "## Shared atomic note",
        "## Daily Worklog",
        "## Saved Worklog report",
    ]:
        if templates and heading not in templates:
            errors.append(f"markdown templates are missing section: {heading}")
    for marker in [
        "<!-- kb:progress:start -->",
        "<!-- kb:daily-summary:start -->",
        '<!-- kb:worklog:event:start id="{Event_ID}" -->',
    ]:
        if templates and templates.count(marker) != 1:
            errors.append(f"markdown template marker must occur once: {marker}")

    ui_text = _read(skill_dir / "agents/openai.yaml", errors)
    ui_fields = dict(UI_FIELD_RE.findall(ui_text))
    for field in ["display_name", "short_description", "default_prompt"]:
        if not ui_fields.get(field):
            errors.append(f"agents/openai.yaml is missing quoted interface.{field}")
    short_description = ui_fields.get("short_description", "")
    if short_description and not 25 <= len(short_description) <= 64:
        errors.append("interface.short_description must contain 25-64 characters")
    default_prompt = ui_fields.get("default_prompt", "")
    if name and default_prompt and f"${name}" not in default_prompt:
        errors.append("interface.default_prompt must explicitly mention $skill-name")

    for path in skill_dir.rglob("*"):
        if path.is_file() and path.name in {"README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md"}:
            errors.append(f"repository documentation must stay outside the Skill package: {path.name}")

    return errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_skill.py <skill-directory>", file=sys.stderr)
        return 2
    skill_dir = Path(argv[1])
    if not skill_dir.is_dir():
        print(f"error: not a directory: {skill_dir}", file=sys.stderr)
        return 2
    errors = validate(skill_dir)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"OK: {skill_dir} is a valid distributable Skill")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
