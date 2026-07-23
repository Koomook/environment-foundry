# Environment Foundry V2 — Executable Proof

Date: 2026-07-23

Status: candidate / internal

Canonical promotion: pending EF-06 evidence review

## One-line company

Environment Foundry turns a company's rights-cleared operating history into an environment in which AI can repeatedly act, be graded, and learn from delayed business outcomes.

## What changed from V1

V1 defined the company thesis, boundaries, proof ladder, and operating system. V2 adds the first reproducible artifact: a public, synthetic Ralphthon release-readiness environment that another person can clone, run, inspect, and rebuild. This is evidence that we can package a bounded company task as data, actions, state transitions, and a deterministic grader. It is not yet evidence that the environment represents a real company, improves a live business, transfers across companies, or creates training lift.

## The IR spine

### 1. Problem

Business AI lacks the equivalent of code's shared executable test environment. Company records are fragmented, rights-constrained, path-dependent, and affected by outcomes that may appear months later.

### 2. Mission

Build the engine that can take a company and produce an AI-learnable company environment: rights-aware trajectories, bounded tasks, graders, replay, and eventually counterfactual simulation.

### 3. What exists today

- Public environment repository: https://github.com/Koomook/ralphthon-release-env
- Release: `v0.1.2`
- Public commit: `2e9f70b5d134673b1f7157af78c41e14552de112`
- Public artifact set: 126 files
- `SHA256SUMS` hash: `b9bb795fa2c482330d2aca3182fd20c7409ac0e782cad8df53761a6c307ff3ee`
- Public dataset: https://huggingface.co/datasets/bong-9/ralphthon-release-readiness
- Dataset commit: `31f3d9a40e24ffc760f05d13d7c7796e3c8599c3`
- Dataset boundary: 36 synthetic fixtures with a frozen 16/10/10 split and provenance receipts
- Runtime: deterministic reset/step/state API, bounded actions, and a release-readiness grader

Independent reproducibility checks passed from a fresh HTTPS clone: dependency lock sync, 123 tests, demo reward `1.0`, deterministic rebuild checksum, and HTTP `/reset` response `200`.

### 4. What this proves

We can convert one narrowly bounded operational decision into a distributable environment with explicit inputs, action space, state, reward, provenance, and regression tests. The artifact is independently executable rather than only a pitch or schema.

### 5. What this does not prove

- No Slack or other private historical source was used.
- No live company action or business outcome was measured.
- No causal or counterfactual business simulator exists.
- No cross-company transfer, buyer demand, reward robustness, or rights-valid historical ingestion has been proven.
- A Qwen 0.5B LoRA run improved parsing and removed one hard failure, but held-out action accuracy remained zero; therefore there is no training-lift claim.

### 6. Why Ralphthon ICML matters next

Ralphthon ICML contains real operational history and delayed decisions, but it can become research evidence only after official results, permissions, retention, rewards, participant notification, and provenance are closed. We will not confuse possession of records with the right to train on or publish them.

### 7. Evidence cadence to V7

| Date | Version | Gate |
|---|---|---|
| Jul 24 | V3 — Grader Trust | Independent review and reward-hacking tests |
| Jul 25 | V4 — Prospective Validity | New frozen synthetic cohort with no leakage |
| Jul 26 | V5 — Workflow & Rights | One workflow selected; rights and deletion test specified |
| Jul 27 | V6 — Shadow Pilot PRE-GO | Operators, reviewers, outcomes, and private plane frozen |
| Jul 28 | V7 — Company Review | Evidence ledger, 30/90-day decision, stop/continue call |

If a gate does not pass, that day's version records an honest `HOLD`; the version number measures learning, not marketing progress.

### 8. Decisions now required

1. Close the Ralphthon ICML operating ledger before using any event record as evidence.
2. Decide whether the first real workflow has enough rights-clear, outcome-bearing episodes to justify a pilot.
3. Validate grader reliability before collecting more data.
4. Select a realistic paper route and freeze the paper's claim before launching a research community.

## Stop rule and next gate

Stop expanding the vision if an independent reviewer can game the grader, if source rights cannot survive deletion/revocation, or if the environment cannot produce stable held-out rankings. The next gate is V3: prove that the grader measures the intended operational quality rather than superficial compliance.
