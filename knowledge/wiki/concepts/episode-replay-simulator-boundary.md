---
title: Episode, Replay, and Simulator Boundary
created: 2026-07-22
updated: 2026-07-22
type: concept
status: active
visibility: internal-only
confidence: high
contested: false
sources: []
source_paths: [knowledge/research/20260722-origin/README.md]
valid_from: 2026-07-22
valid_until:
superseded_by:
tags: [concept, simulator, evaluation]
aliases: []
---
# Episode, Replay, and Simulator Boundary

1. Episode reconstruction links decision-time observations, actual action, later outcome, and provenance.
2. Replay/sandbox lets a bounded action change reproducible state and receive a grade.
3. Validated simulator is allowed only when offline policy ranking predicts prospective live ranking and survives exploitation tests.

Plausible role-play and hindsight reconstruction do not cross this boundary. Links: [[environment-not-data-asset]], [[delayed-outcome-trajectory]].
