# Handoff — stateful workspace cutover recovery benchmark

- Date: 2026-08-28
- From: Terminal-Bench 3.0 / HUD v6 research and synthetic lab implementation
- To: EF-02 Environment Compiler; EF-03 Rights OS
- Status: evidence intake, not canonical promotion
- Graph edge affected: private failure pattern -> rights-bounded synthetic task -> executable verifier -> candidate RLVR task family
- Research artifact: `knowledge/research/20260828-terminal-bench-hud-rlvr/`
- Experiment artifact: `knowledge/lab/experiments/stateful-workspace-cutover-recovery/`

## Atomic claims proposed for review

1. `OBSERVED`: a newly authored synthetic stateful recovery task now has an
   agent environment, oracle, separate low-privilege verifier, declared artifact
   boundary, deterministic reset, binary reward file, and split-scoped rights
   receipt.
2. `OBSERVED`: the buggy no-op baseline failed 11 of 12 hidden tests; the oracle
   passed 12 of 12 twice; seven behavior-changing mutants were rejected.
3. `OBSERVED`: the task passed every non-LLM Terminal-Bench 3.0 static shell
   check from tag `v3.0.0`; Harbor 0.18 returned oracle `1.0` and nop `0.0`
   without exceptions.
4. `OBSERVED`: HUD 0.6.15 parses a 20-row draft catalog with 12 future-train
   candidates, 4 development-evaluation rows, and 4 visible-evaluation rows.
   The referenced templates and profile registry are not implemented.
5. `HYPOTHESIS`: grouped model rollouts over this task family can produce
   non-saturated verifiable reward and teach data-lineage safety that transfers
   to held-out composite cases.
6. `NOT YET`: a deployed HUD actor/verifier, executable profile registry,
   model calibration, trajectory/token capture, RLVR training lift, prospective
   ranking, partner utility, company transfer, or foundry economics.

## Decisions

- Preserve Terminal-Bench 3.0 only as a reproducibility target; its v3 canary
  surface remains evaluation-only.
- Use current HUD v6 Task/Taskset/verifier concepts rather than archived
  `hud-vf-gym` APIs.
- Keep any future rights-cleared training build distinct from the canaried task,
  visible evaluation rows, and a future sealed evaluation build.
- Call the artifact a deterministic replay task and task-family manifest, not a
  simulator or completed RLVR dataset.

## Verification

```bash
uv run python knowledge/lab/experiments/stateful-workspace-cutover-recovery/validate_task.py
uv run python knowledge/lab/experiments/stateful-workspace-cutover-recovery/rlvr/validate_taskset.py
uv run python scripts/validate_company_os.py
git diff --check
```

Local controls, Docker image builds, a verifier-access security probe, and exact
Harbor 0.18 oracle/nop runs passed. The retained receipt is
`knowledge/lab/experiments/stateful-workspace-cutover-recovery/results/verification-receipt.json`.
Repository-wide validation is separately blocked by pre-existing
`private-plane/.../node_modules` link/secret-scan noise; project tests pass.

## Privacy, provenance, and rights

The private Codex task was evidence intake only. Its locator and payload remain
outside Git. The committed package contains no raw task message, credential,
personal record, actual source database, screenshot, real identifier, or source
product code. Fixtures, tokens, rows, paths, and implementations are synthetic.
The pending receipt denies all rollout collection and training. Visible
evaluation and canaried surfaces are evaluation-only. EF-03 must accept a
superseding receipt before trajectories are collected or described as
rights-valid training data.

## Next falsifiable gate

After a second operator reproduces the Harbor receipt, implement and test the
HUD actor/verifier plus frozen profile registry. Obtain EF-03 approval and a
physically separated train manifest before calibrating repeated grouped attempts
with weak and strong named model anchors. Freeze digests and create a genuinely
sealed evaluation set before a base/harness/SFT/RLVR protocol is fixed.

## Stop rule

Stop or redesign before training if Docker reset is nondeterministic, a mutant
survives, rights review fails, future train/evaluation leakage is found, or grouped rewards
are uniformly zero/one. Reject the RLVR hypothesis if multiple seeded runs fail
to beat the harness-only and SFT baselines on a future sealed evaluation set.
