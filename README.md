# Environment Foundry

> Working name. No trademark or domain claim has been made.

Environment Foundry turns authorized company operations into bounded environments in which AI can observe, act, and be evaluated. It is an independent company repository and a file-native Company OS for humans and coding agents.

## Start here

1. Read [AGENTS.md](AGENTS.md).
2. Read the small [mission spine](knowledge/okf/slices/mission-spine/index.md).
3. Use [the workstream registry](knowledge/workstreams/registry.md) for current execution.
4. Use [the canonical wiki](knowledge/wiki/index.md) for durable claims and decisions.

## Current truth

- Mission: compile rights-valid operating events into AI learning and evaluation environments.
- Current evidence: schemas, synthetic fixtures, and validators exist in the predecessor research; live utility, held-out transfer, paid demand, locality lift, and training lift are not yet proven.
- Current wedge: post-event commitment reconciliation is a leading candidate, not a permanently selected first market.
- Near-term proof: select one bounded workflow, validate its grader and baselines, run rights-valid shadow episodes, and obtain buyer-written specifications or a paid design pilot.

## Repository map

- `company/` — identity, operating model, roadmap, proof ladder
- `functions/` — every company function and its outputs
- `products/` — executable product surfaces; code may later move to dedicated repos
- `knowledge/wiki/` — source-backed canonical truth
- `knowledge/okf/` — compact progressive-disclosure reading layer
- `knowledge/workstreams/` — scope, live status, immutable handoffs
- `knowledge/lab/` — rights-cleared task, trajectory, grader, and eval artifacts
- `private-plane/` — policy only; private payload stays outside Git

## Validate

```bash
uv run python scripts/validate_company_os.py
git diff --check
```

## V2 benchmark adapter

The V2 research adapter preserves upstream artifacts outside Git, projects
them into a versioned normalized episode schema, and provides an explicitly
local/offline baseline and evaluator:

```bash
uv sync --extra parquet --group dev
uv run pytest
uv run environment-foundry-v2 decode \
  --source crmarena-pro \
  --path /path/to/CRMArenaPro/tasks_b2b.json \
  --revision 8c055f5 \
  --split b2b \
  --limit 3
```

Research brief and evidence ledger:
`knowledge/research/20260723-environment-foundry-v2/README.md`.
