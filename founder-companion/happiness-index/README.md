# Jung Goobong Life Index

Status: `HYPOTHESIS`; founder-private measurement experiment, not an enacted
Constitution article.

The working Korean name is **정구봉 행복 인덱스**. The index asks whether the
founder's life is becoming better across the things that matter, without
letting one visible success erase hidden debt elsewhere.

## Output contract

Every review keeps both:

1. a vector of separately visible dimensions and floor violations; and
2. one experimental headline index for comparison over time.

The headline number is never sufficient on its own. A gain in company results
or cash cannot compensate for a breached safety, health, family, consent, or
trust floor. Another person's happiness is never inferred from the founder's
observation; it requires that person's direct, authorized input.

## Candidate model under review

Deep Thought evidence changed the draft from a flat list into three layers:

- lived outcomes: aliveness and presence, protected family life, meaningful
  creation and value, reciprocal relationships, and self-alignment;
- compounding stocks: sustainable compounding and returned time, usable
  capacity, learning, exercisable optionality, and economic sufficiency; and
- non-compensable floors: consent and trust, protected family time,
  sleep/health recovery, and essential cash obligations.

These are candidates, not settled truths. Review exactly one item at a time:

```bash
uv run python founder-companion/happiness-index/review.py show
```

An explicit founder answer is preserved as an append-only private review event
with a source locator and idempotency key. Meaning is confirmed before
measurement, and measurement before weight.

Weights, normalization functions, baselines, and floors remain versioned
hypotheses. They are revised from observed outcomes, not tuned to make the
headline score look better.

## Review cadence

- Daily: the local collector reads authorized passive sources and stores one
  immutable private snapshot. The founder does not fill a daily form.
- Weekly: inspect the vector, floor breaches, transition failures, and one
  small reversible intervention. If passive evidence cannot resolve felt
  well-being, energy, or presence, ask at most one short voice check-in rather
  than a multi-field form.
- Monthly: calculate the comparable headline index and review weights,
  double-counting, missing dimensions, and Goodhart effects.
- Quarterly: decide whether the index predicts better lived outcomes or
  should be revised, narrowed, or killed.

Run the collector on demand with:

```bash
uv run python founder-companion/happiness-index/collector.py --days 7
```

Every non-dry run writes an immutable, hashed snapshot and updates only a
pointer receipt in the private plane. Missing or stale sources remain unknown;
they never become zero or a favorable default.

## Automatic sources

- Monologue note metadata and summaries, fetched directly from the Monologue
  CLI;
- primary Google Calendar events through the local authenticated `gog` CLI;
- local Codex session activity and artifact-event receipts;
- Git commit and dirty-path counts from the configured local repositories;
- read-only Context Ledger counts, with an explicit freshness gate;
- version receipts for the registered Deep Thought context, without copying
  its contents;
- the read-only Health & Training OS dashboard projection when current entries
  exist.

Calendar time is not proof of attendance or presence. Agent activity is not
meaningful output. Founder speech does not establish another person's
happiness. Cash remains unknown until an authorized financial source is
connected.

## Private evidence and routing

Raw Monologue notes, Codex history, family or health material, observations,
scores, and formula versions belong only under:

```text
../../private-plane/payload/founder-companion/happiness-index/
```

The Environment Foundry Command Center may dispatch bounded work to the
dedicated Life Index Codex task. It receives back only task status and private
artifact locators. The company operating system may consume only the sanitized
fields allowed by
[`company/operating-system/founder-capacity-interface.md`](../../company/operating-system/founder-capacity-interface.md),
never the happiness score or its personal evidence.

This experiment is not a company workstream, company objective function,
validated life simulator, medical score, or claim about what another person
wants.
