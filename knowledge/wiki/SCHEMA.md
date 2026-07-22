# Canonical wiki schema

`knowledge/wiki/` is the only canonical knowledge target.

## Layers

1. `raw/public/` and `raw/internal-safe/`: immutable, Git-safe source receipts.
2. Typed directories: maintained synthesis pages.
3. `SCHEMA.md`, `index.md`, `log.md`: rules, navigation, change memory.

Private raw payload never enters this tree.

## Page types

`entity`, `mission`, `thesis`, `hypothesis`, `experiment`, `concept`, `operating-pattern`, `partner`, `product`, `decision`, `query`, `comparison`.

## Required frontmatter

```yaml
---
title: Page title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: mission
status: draft | candidate | active | needs-review | superseded | archived
visibility: internal-only | publishable | public
confidence: high | medium | low
contested: false
sources: []
source_paths: []
valid_from: YYYY-MM-DD
valid_until:
superseded_by:
tags: []
aliases: []
---
```

## Gates

- Exactly one mission may be active.
- Every active thesis links to the active mission and at least one falsifiable hypothesis.
- Every active/candidate hypothesis states a test, threshold, and stop rule.
- Every active/candidate experiment states hypothesis, baseline, task contract, grader, rights gate, outcome window, and next decision.
- Every typed page appears in `index.md`; every wikilink resolves by slug.
- `confidence: high` requires canonical evidence or multiple independent sources.
- A session, deck, report, brief, status, or handoff is not canonical by existence.
- Contradictions remain visible; superseded positions retain their history.
- A simulator claim requires prospective correlation between offline policy ranking and live outcome ranking.
