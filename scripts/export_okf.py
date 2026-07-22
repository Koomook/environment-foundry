#!/usr/bin/env python3
"""Export canonical wiki pages into a generated OKF-compatible reading slice."""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "knowledge/wiki"
OUT = ROOT / "knowledge/okf/slices/canonical-wiki"
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


def split_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    _, raw, body = text.split("---", 2)
    return yaml.safe_load(raw) or {}, body.lstrip()


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    links: list[str] = []
    for dirname in TYPED_DIRS:
        for source in sorted((WIKI / dirname).glob("*.md")):
            meta, body = split_frontmatter(source.read_text())
            target = OUT / dirname / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            okf_meta = {
                "type": str(meta["type"]),
                "title": str(meta["title"]),
                "description": next(
                    (line.strip() for line in body.splitlines() if line.strip() and not line.startswith("#")),
                    str(meta["title"]),
                )[:240],
                "resource": f"../../../../wiki/{dirname}/{source.name}",
                "tags": meta.get("tags", []),
                "timestamp": str(meta["updated"]),
                "visibility": meta.get("visibility", "internal-only"),
                "confidence": meta.get("confidence", "low"),
                "sources": meta.get("sources", []),
                "source_paths": meta.get("source_paths", []),
            }
            rendered = "---\n" + yaml.safe_dump(okf_meta, sort_keys=False, allow_unicode=True) + "---\n\n"
            rendered += f"# {meta['title']}\n\nCanonical source: [{source.name}]({okf_meta['resource']})\n"
            target.write_text(rendered)
            links.append(f"- [{meta['title']}]({dirname}/{source.name})")
    index = "# Generated canonical wiki slice\n\nDo not hand edit.\n\n" + "\n".join(links) + "\n"
    (OUT / "index.md").write_text(index)
    print(f"exported {len(links)} canonical pages to {OUT}")


if __name__ == "__main__":
    main()
