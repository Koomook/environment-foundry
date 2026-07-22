# Environment Foundry — Company OS

This repository is the operating system of an independent company. The working name is Environment Foundry. Do not import Team Attention's mission, people, customers, or claims as this company's truth.

## Mission

We build an engine that repeatedly compiles authorized company operating events into rights-valid bounded task environments where AI can observe, act, and be evaluated.

We are not currently building an autonomous company, a perfect company digital twin, a generic AX consultancy, a raw-data brokerage, or a company-specific foundation model.

## Read protocol

1. Start at `knowledge/okf/slices/mission-spine/index.md`.
2. Follow only the concepts needed for the task.
3. Verify durable claims in `knowledge/wiki/` and its cited sources.
4. Read `knowledge/workstreams/registry.md` and the relevant `status.md` for current execution.
5. Treat research, briefs, status pages, session transcripts, and decks as non-canonical until an atomic claim is promoted.

## Knowledge layers

- `knowledge/wiki/` is the only canonical knowledge write target.
- `knowledge/okf/` is a compact reading/export layer, never independent evidence.
- `knowledge/workstreams/` coordinates execution; a handoff is evidence intake, not automatic truth.
- `knowledge/lab/` contains rights-cleared, inspectable experiment artifacts, not raw company archives.
- Private messages, recordings, faces, contacts, credentials, client payloads, and person-level records remain outside Git.

## Knowledge graph

```text
Mission → Thesis → Hypothesis → Decision → Experiment
→ Trial/Trajectory → Outcome + Grade → Dataset/Eval version
→ System change → Regression result → Thesis update
```

Every active initiative must name its current graph position, next falsifiable gate, owner, evidence artifact, and stop rule.

## Write protocol

1. Preserve a public or internal-safe source receipt with provenance. Never copy private payload into Git.
2. Put divergent analysis in `knowledge/research/`.
3. Submit atomic claims through a workstream handoff.
4. The `06-memory-compiler` owner checks provenance, privacy, duplication, contradiction, graph fit, evidence, and freshness.
5. Promote accepted claims into one typed wiki page; update `knowledge/wiki/index.md` and `knowledge/wiki/log.md` atomically.
6. Update the mission-spine OKF slice only when the canonical wiki changes materially.

Never silently rewrite a reviewed handoff. Add a superseding handoff.

## Evidence language

Use these labels when they prevent confusion:

- `OBSERVED` — inspectable result exists.
- `HYPOTHESIS` — falsifiable claim with threshold and stop rule.
- `VISION` — desired future, not evidence.
- `OPTION` — gated path that is not active.
- `NOT YET` — explicitly unproven.

Do not call a corpus an environment without an observation boundary, typed actions, transition behavior, termination, grader, reset/replay semantics, and rights/provenance. Do not call replay a simulator until its ranking predicts prospective live outcomes.

## Company execution

- Current execution lives in `knowledge/workstreams/*/status.md`.
- Functional ownership and expected outputs live in `functions/`.
- Command decisions live in canonical decision pages after evidence review.
- The founder owns priority, budget, publication, external commitments, acquisition, fundraising, and stop/continue decisions.
- Agents may draft and test internally but must not contact people, publish, purchase, fundraise, acquire, or run live interventions without explicit authorization.

## Privacy and rights

Rights are product semantics, not paperwork. Separate access, operations, evaluation, training, derivative, resale, export, retention, revocation, and deletion rights. Ambiguity fails closed.

`internal-only` never means raw private data may enter Git. Use opaque locators in `private-plane/` and store payload in an approved external private system.

## Validation

After structural or canonical changes run:

```bash
uv run python scripts/validate_company_os.py
git diff --check
```

Completion means the real artifact exists, validators pass, evidence boundaries are stated, and the relevant status/handoff is updated.
