#!/usr/bin/env python3
"""Fail-closed structural validator for the Environment Foundry Company OS."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge/wiki"
TYPED_DIRS = (
    "entities",
    "missions",
    "theses",
    "hypotheses",
    "experiments",
    "concepts",
    "operating-patterns",
    "partners",
    "products",
    "decisions",
    "queries",
    "comparisons",
)
REQUIRED = {
    "title",
    "created",
    "updated",
    "type",
    "status",
    "visibility",
    "confidence",
    "contested",
    "sources",
    "source_paths",
    "valid_from",
    "valid_until",
    "superseded_by",
    "tags",
    "aliases",
}
ALLOWED_TYPES = {
    "entity",
    "mission",
    "thesis",
    "hypothesis",
    "experiment",
    "concept",
    "operating-pattern",
    "partner",
    "product",
    "decision",
    "query",
    "comparison",
}
ALLOWED_STATUS = {"draft", "candidate", "active", "needs-review", "superseded", "archived"}
STATE_VALUES = {"not-started", "active", "blocked", "gate-review", "complete", "stopped"}
SECRET_PATTERNS = {
    "OpenAI key": re.compile(r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"),
    "GitHub token": re.compile(r"gh[pousr]_[A-Za-z0-9]{20,}"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def parse_page(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    if not text.startswith("---\n") or text.count("---") < 2:
        raise ValueError("missing YAML frontmatter")
    _, raw, body = text.split("---", 2)
    return yaml.safe_load(raw) or {}, body.lstrip()


def wiki_pages() -> list[Path]:
    return [path for dirname in TYPED_DIRS for path in sorted((WIKI / dirname).glob("*.md"))]


def validate_wiki(errors: list[str]) -> None:
    pages = wiki_pages()
    slugs = {path.stem for path in pages}
    index = (WIKI / "index.md").read_text()
    active_missions = 0
    for path in pages:
        try:
            meta, body = parse_page(path)
        except Exception as exc:
            errors.append(f"{path.relative_to(ROOT)}: {exc}")
            continue
        missing = REQUIRED - set(meta)
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: missing {sorted(missing)}")
        if meta.get("type") not in ALLOWED_TYPES:
            errors.append(f"{path.relative_to(ROOT)}: invalid type {meta.get('type')}")
        if meta.get("status") not in ALLOWED_STATUS:
            errors.append(f"{path.relative_to(ROOT)}: invalid status {meta.get('status')}")
        expected_directory = {
            "thesis": "theses",
            "hypothesis": "hypotheses",
            "operating-pattern": "operating-patterns",
        }.get(str(meta.get("type")), f"{meta.get('type')}s")
        if path.parent.name != expected_directory:
            errors.append(f"{path.relative_to(ROOT)}: type/directory mismatch")
        if meta.get("type") == "mission" and meta.get("status") == "active":
            active_missions += 1
        if f"[[{path.stem}]]" not in index:
            errors.append(f"{path.relative_to(ROOT)}: not linked from wiki index")
        for target in re.findall(r"\[\[([^\]|#]+)", body):
            if target not in slugs:
                errors.append(f"{path.relative_to(ROOT)}: broken wikilink [[{target}]]")
        if meta.get("type") == "hypothesis" and meta.get("status") in {"active", "candidate"}:
            for heading in ("## Test", "## Threshold", "## Stop rule"):
                if heading not in body:
                    errors.append(f"{path.relative_to(ROOT)}: missing {heading}")
        if meta.get("type") == "experiment" and meta.get("status") in {"active", "candidate"}:
            for term in ("hypothesis", "baseline", "task contract", "grader", "rights", "outcome window", "next decision"):
                if term.lower() not in body.lower():
                    errors.append(f"{path.relative_to(ROOT)}: experiment missing {term}")
    if active_missions != 1:
        errors.append(f"expected exactly 1 active mission, found {active_missions}")


def validate_workstreams(errors: list[str]) -> None:
    root = ROOT / "knowledge/workstreams"
    for directory in sorted(root.glob("[0-9][0-9]-*")):
        for name in ("brief.md", "status.md"):
            if not (directory / name).exists():
                errors.append(f"{directory.relative_to(ROOT)}: missing {name}")
        status_path = directory / "status.md"
        if status_path.exists():
            match = re.search(r"^- State: ([a-z-]+)$", status_path.read_text(), re.MULTILINE)
            if not match or match.group(1) not in STATE_VALUES:
                errors.append(f"{status_path.relative_to(ROOT)}: invalid or missing state")


def validate_json_schemas(errors: list[str]) -> None:
    for path in sorted((ROOT / "knowledge/lab/schemas").glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
            continue
        if data.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{path.relative_to(ROOT)}: wrong JSON Schema draft")


def validate_secrets(errors: list[str]) -> None:
    excluded_parts = {".git", ".venv", "__pycache__"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in excluded_parts for part in path.parts):
            continue
        if path.suffix.lower() not in {".md", ".py", ".toml", ".json", ".yaml", ".yml", ".txt", ""}:
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"{path.relative_to(ROOT)}: possible {label}")


def validate_markdown_links(errors: list[str]) -> None:
    excluded_parts = {".git", ".venv", "__pycache__"}
    for path in ROOT.rglob("*.md"):
        if any(part in excluded_parts for part in path.parts):
            continue
        text = path.read_text()
        for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "/")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(ROOT)}: broken markdown link {raw_target}")


def validate_okf_export(errors: list[str]) -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/export_okf.py")], check=True)
    wiki_count = len(wiki_pages())
    export_count = len(list((ROOT / "knowledge/okf/slices/canonical-wiki").glob("*/*.md")))
    if wiki_count != export_count:
        errors.append(f"canonical OKF count mismatch: wiki={wiki_count}, export={export_count}")


def main() -> int:
    errors: list[str] = []
    validate_wiki(errors)
    validate_workstreams(errors)
    validate_json_schemas(errors)
    validate_secrets(errors)
    validate_okf_export(errors)
    validate_markdown_links(errors)
    if errors:
        print("Company OS validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Company OS validation: PASS ({len(wiki_pages())} canonical pages, 6 workstreams)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
