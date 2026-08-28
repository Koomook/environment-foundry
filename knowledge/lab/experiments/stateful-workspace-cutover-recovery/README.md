# Stateful workspace cutover and recovery

Status: `OBSERVED` Harbor 0.18-executable, deterministically resettable
synthetic evaluation task; `NOT YET` a validated simulator, accepted
Terminal-Bench contribution, deployed HUD environment, or
evidence of RLVR training lift.

This package turns a private-session failure pattern into a public-safe task:
a newly added terminal interface appears healthy but starts on an empty,
isolated database instead of the existing authority. The candidate must repair
continuity while an operation is active, then implement a guarded one-time
cutover with an immutable export, per-device credential digest, revision CAS,
fresh-cache pull-back, and semantic-hash verification.

No source-session payload, repository code, credential, personal record,
actual activity count, product name, or real database is included. All code,
SQLite rows, identifiers, tokens, and failure injection are synthetic and were
authored for this experiment.

## Artifact surfaces

- [`terminal-bench/stateful-workspace-cutover/`](terminal-bench/stateful-workspace-cutover/)
  is a Terminal-Bench 3.0 / Harbor 0.18-executed evaluation package with the
  required benchmark canary. It is a holdout and must not enter training.
- [`rlvr/taskset.jsonl`](rlvr/taskset.jsonl) contains a 20-row HUD v6 catalog:
  12 future-train candidates, 4 development-evaluation rows, and 4 visible
  evaluation rows. These rows parse as Tasks but are not executable cases until
  the referenced templates and trusted profile registry exist.
- [`task-contract.json`](task-contract.json) and
  [`rights-receipt.json`](rights-receipt.json) define the environment and
  split-specific rights boundary.
- [`validate_task.py`](validate_task.py) runs the no-op control, oracle,
  deterministic repeats, and behavior-changing mutation audit.

## Environment boundary

- Observation: instruction, buggy Python runtime, synthetic SQLite source and
  isolated stores, redacted state/status commands, mock remote state, and
  visible smoke tests.
- Action: inspect the sandbox, edit `/app/workspace_runtime.py`, run local
  commands/tests, recover local authority, attempt a cutover, or fail closed.
- Transition: local filesystem and SQLite state change through the candidate
  runtime; the remote is a deterministic local mock.
- Termination: verifier success, timeout, a hard integrity/secrecy failure, or
  explicit candidate completion.
- Grader: a separate verifier runs submitted Python through a low-privilege
  black-box worker; hidden sources and reward paths are root-only. Reward is
  binary with auditable per-gate results.
- Reset: every test creates a fresh randomized fixture in a temporary directory.
  Digest-equality replay receipts are `NOT YET`.

## Run locally

```bash
uv run python knowledge/lab/experiments/stateful-workspace-cutover-recovery/validate_task.py
uv run python knowledge/lab/experiments/stateful-workspace-cutover-recovery/rlvr/validate_taskset.py
```

For byte-compatible Terminal-Bench 3.0 checks, use tag `v3.0.0` at commit
`2b0442c3c583b710ca8da14c8e601b99f2f1f244` with Harbor `0.18.0`. The package
also includes separate agent and verifier Dockerfiles. The retained
[`results/verification-receipt.json`](results/verification-receipt.json) records
Harbor oracle `1.0`, nop `0.0`, image IDs, and artifact digests. Publishing, running a
paid model trial, or contacting Terminal-Bench/HUD maintainers is outside this
artifact and requires founder authorization.

## Evidence boundary and next gate

The package proves that one synthetic task can be built and run by Harbor,
reset, solved by its oracle, rejected by a no-op baseline, and protected against
selected mutations and a basic verifier-access probe. It does
not prove that current models find the task difficult, that within-group reward
has useful variance, that the 20 rows are independent training environments,
or that policy optimization improves held-out performance.

Next gate: independently audit verifier isolation, build the HUD templates/profile registry,
obtain EF-03 approval, and have a second operator reproduce the Harbor receipt. Only then calibrate
repeated groups with frozen weak/strong model anchors. Stop before training if
rewards saturate, remain uniformly zero, hidden mutants survive, or evaluation
fixtures are reachable from the future train build.
