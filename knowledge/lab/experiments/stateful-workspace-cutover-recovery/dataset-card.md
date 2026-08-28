# Dataset and environment card

## Classification

- Artifact class: deterministically resettable synthetic evaluation-task draft
  plus HUD-shaped task-family catalog.
- Not: raw operational archive, reconstructed private episode, deployed HUD
  environment, accepted Terminal-Bench dataset, or validated simulator.
- Evaluation unit: one terminal code-repair episode using a separate Harbor
  verifier and low-privilege candidate subprocess.
- Candidate catalog: 12 future-train, 4 development-evaluation, and 4 visible
  evaluation HUD v6 rows. The actor/verifier templates and profiles are not yet implemented.
- Canaried evaluation: the Terminal-Bench-format package is evaluation-only.

## Provenance

The task's causal pattern came from a private Codex task in which terminal
tooling was attached to an empty isolated state while a populated local
authority remained intact. Only the abstract invariants were retained:
lineage continuity, active-operation safety, fail-closed cutover, per-device
credential hashing, revision CAS, and pull-back verification. The private task
identifier and payload are retained outside Git.

Every fixture and implementation file in this package is newly authored and
synthetic. No literal source-session rows, product code, secrets, names,
amounts, timestamps, or identifiers were copied.

## Splits and contamination policy

| Surface | Count | Training allowed | Notes |
|---|---:|---|---|
| HUD train candidates | 12 | no, pending EF-03 | future grouped-rollout designs |
| HUD dev | 4 | no | development evaluation only |
| HUD visible evaluation | 4 | no | profiles and seeds are public; not sealed |
| Terminal-Bench package | 1 | no | v3 canary; evaluation compatibility |

The public Terminal-Bench 3.0 corpus and this canaried evaluation package must
not be used for training. No row in the current catalog is admitted to training.
A later rights-approved build must physically separate its train manifest and
trusted profile registry. A checkpoint trained on visible evaluation, oracle,
hidden tests, or the canaried package is contaminated and cannot support a
benchmark claim.

## Reward and verifier

The primary reward is binary. Diagnostic axes include:

- semantic continuity and source immutability;
- active-operation preservation;
- migration/head/device preconditions;
- export-before-mutation ordering;
- credential token non-disclosure;
- exactly one revision `0 -> 1` transition;
- pull-back semantic hash equality;
- authority switch ordering;
- idempotency and fault handling;
- mutation-kill rate.

Any integrity or secrecy failure forces primary reward zero. The diagnostic
vector may be used for task debugging, but shaped RL rewards require a new
frozen verifier version and exploitation audit.

## RLVR readiness

The mechanics are suitable for verifiable reward rollouts: disposable state,
terminal actions, deterministic transition, separate verifier, numeric reward,
and repeatable reset. The current artifact is not yet sufficient evidence for
fine-tuning because no model rollouts, token captures, within-group reward
spread, advantage distribution, or training/heldout lift have been measured.

Before training, require:

1. Have a second operator adversarially reproduce the candidate-isolation probe and Harbor oracle/nop results.
2. Implement the HUD actor, authoritative verifier, and frozen profile registry; prove candidate transfer end to end.
3. EF-03 accepts a superseding receipt and a fail-closed train-only loader.
4. Two operators reproduce container baseline/oracle/mutation results and digest-equality replay receipts.
5. Repeated frozen-sampling groups estimate pass probability and reward spread for named weak/strong models.
6. Train/dev/sealed-evaluation fixture generators and image digests are physically separated and frozen.
7. Base, harness-only, SFT, and RLVR arms are compared across at least three
   seeds with the holdout opened once.
