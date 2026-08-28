# Terminal-Bench 3.0, HUD v6, and Frogstar RLVR task packaging

Status: divergent primary-source research plus an implemented synthetic pilot;
not canonical company truth.

Research date: 2026-08-28 Asia/Seoul.

## Decision summary

1. Reproduce Terminal-Bench 3.0 from immutable tag `v3.0.0`, not the moving
   default branch. V3 is a 74-task Harbor dataset at commit
   `2b0442c3c583b710ca8da14c8e601b99f2f1f244`; v4.0.0 was already current on
   the research date.
2. Import the environment/package contract: agent Docker environment,
   declared artifacts, oracle, separate verifier image, explicit reward files,
   nop/oracle controls, and adversarial verification.
3. Do not use the official Terminal-Bench corpus as training data. Its canary
   excludes benchmark payload from training, and doing so would contaminate
   evaluation.
4. For HUD, use current v6 `Environment`, `Task`, `Taskset`,
   `EvaluationResult`, `Task.verifier`, runtime, trace, and `TrainingClient`
   surfaces. Do not build on the archived v5 `hud-vf-gym` adapter.
5. Separate the canaried evaluation package from any future rights-cleared
   training rows. A single executable task is a benchmark seed, not evidence
   that RLVR fine-tuning works.

## Implemented artifact

The pilot lives at
[`knowledge/lab/experiments/stateful-workspace-cutover-recovery/`](../../lab/experiments/stateful-workspace-cutover-recovery/).
It packages a pattern-derived synthetic stateful recovery/cutover task with:

- a Terminal-Bench 3.0 package executed by Harbor 0.18 with oracle `1.0` and nop `0.0`;
- a separate-verifier mode, low-privilege candidate worker, and one-file artifact boundary;
- binary reward plus diagnostic output;
- no-op, oracle, determinism, and mutation controls;
- 20 HUD v6 schema-valid catalog rows whose templates/profiles are `NOT YET` implemented;
- explicit `NOT YET` boundaries for HUD deployment and training lift.

## Primary sources

- [Terminal-Bench v3.0.0 release](https://github.com/harbor-framework/terminal-bench/releases/tag/v3.0.0)
- [Terminal-Bench v3 tree](https://github.com/harbor-framework/terminal-bench/tree/v3.0.0)
- [Terminal-Bench v3 contribution guide](https://github.com/harbor-framework/terminal-bench/blob/v3.0.0/CONTRIBUTING.md)
- [Harbor v0.18.0](https://github.com/harbor-framework/harbor/releases/tag/v0.18.0)
- [Harbor v0.18 verifier parser](https://github.com/harbor-framework/harbor/blob/v0.18.0/src/harbor/verifier/verifier.py)
- [Official Terminal-Bench 3.0 mirror](https://huggingface.co/datasets/harborframework/terminal-bench-3.0)
- [HUD Python stable v0.6.15](https://github.com/hud-evals/hud-python/releases/tag/v0.6.15)
- [HUD v6 task reference](https://docs.hud.ai/v6/reference/tasks)
- [HUD v6 grader reference](https://docs.hud.ai/v6/reference/graders)
- [HUD v6 training reference](https://docs.hud.ai/v6/reference/training)
- [HUD verifier environments](https://docs.hud.ai/v6/experimental/verifier-environments)
- [Archived HUD Verifiers adapter](https://github.com/hud-evals/hud-vf-gym)

## Unresolved questions

- Does the task produce useful within-group reward spread on a named base
  model, or only all-zero/all-one groups?
- Can 20 profile rows be implemented and physically split without teaching a
  future sealed evaluation set?
- Does a HUD v6 actor/verifier deployment reproduce the local Harbor verifier
  result at pinned image and SDK digests?
- Does RLVR outperform a harness-only or SFT baseline on the held-out composite
  cases across multiple seeds?
