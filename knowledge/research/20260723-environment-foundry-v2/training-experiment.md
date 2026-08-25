# Small-model experiment — Qwen 0.5B, train-only SFT

Status: executed locally on 2026-07-23; negative result retained.

## Why SFT, not RLVR

The public Ralphthon release-readiness environment has a deterministic grader,
but only 16 train projections. It is enough to test serialization and a
supervised format intervention, not enough to estimate a stable policy-gradient
effect. RLVR would invite reward hacking and seed noise before there is a
validated reward distribution. The justified experiment is prompt-masked LoRA
SFT on the train split, with dev for monitoring and frozen test for one final
measurement.

## The data path

```text
public synthetic train projection
  → Qwen chat template
  → prompt tokens masked to -100
  → next-token logits
  → cross-entropy on assistant JSON only
  → LoRA parameter update
  → generated typed action
  → Pydantic validation
  → frozen environment step
  → frozen GradeVector / hard-failure measurement
```

One episode asks the model to inspect a release state and emit exactly one
typed next action. The target is not prose: it is JSON such as a `submit`
action with `decision` and `reason_codes`. Invalid JSON never reaches the
environment. A valid action is executed once, then the unchanged grader
measures correctness and hard failure.

## Frozen run receipt

| Field | Value |
|---|---|
| Model | `Qwen/Qwen2.5-0.5B-Instruct` |
| Revision | `7ae557604adf67be50417f59c2c2f167def9a775` |
| License | Apache-2.0 |
| Hardware | Apple M5, 32 GiB unified memory |
| Framework | MLX 0.32.0 / MLX-LM 0.31.3 |
| Algorithm | LoRA SFT, 2 layers, batch 1, learning rate `1e-5` |
| Splits | train 16, dev 10, frozen test 10 |
| Iterations / seed | 12 / 20260723 |
| Train wall time / peak memory | 5.40 s / 1.281 GiB |
| Local marginal cost | $0 |
| Adapter SHA-256 | `c2aa992d4001b6c9d92d3bc6201539081794d2642de8d4391226ce12bce3220c` |

The repeat base run matched the first base run. On both dev and test:

| Metric | Base | Post-SFT |
|---|---:|---:|
| parse validity | 0.0 | 1.0 |
| hard-failure rate | 1.0 | 0.0 |
| exact action match | 0.0 | 0.0 |
| decision/action-category accuracy | 0.0 | 0.0 |

Training loss fell from 4.000 at iteration 1 to 1.334 at iteration 12; dev loss
fell from 5.547 to 4.069. That is optimization evidence, not policy evidence.
The only held-out improvement is valid/safe serialization. The model did not
learn the right decision. The experiment therefore falsifies the claim that
this tiny SFT already creates useful company judgment.

The full result receipt remains outside Git under the operator's private cache
at `training/results-sft-ef-v2-20260723-r2.json`.
No benchmark test examples were used in training.

## What each training-data type actually contains

| Method | Input → target/reward | Legitimate use | Main limit |
|---|---|---|---|
| SFT trace | observation + tool history → expert next action/answer | learn format and demonstrated behavior | imitates mistakes and cannot exceed missing coverage |
| Preference data | same context + two rollouts → ranking | style, safety, trade-off preference | ranking may not identify causally better action |
| Verifier/grader | task + rollout/state → scalar/vector score | evaluation and RL reward | exploitable proxy; must be reliability-tested |
| Outcome trajectory | decision-time state + action → later outcome | connect behavior to real consequence | confounding and delayed credit remain |
| Interaction rollout | reset state + action/observation sequence → terminal score | teach recovery and long-horizon behavior | expensive; simulator mismatch |
| Synthetic curriculum | generator + difficulty controls → new tasks/solutions | broaden train coverage | generator bias and duplicated test patterns |
| RLVR | sampled rollouts + verifiable reward → policy update | optimize where reward is reliable and repeatable | sparse reward, reward hacking, high variance |

Public benchmark gold/test rows are evaluation assets, not training supply.
Putting them into SFT is leakage, not capability improvement.

## Hardware and spend gate

Prices were checked on official pages on 2026-07-23. They are planning
estimates, not quotes.

| Option | Practical model/technique | Minimum useful memory | Expected wall time for a 1k–10k-example pilot | Compute estimate |
|---|---|---:|---:|---:|
| Apple Silicon local | 0.5B–3B MLX LoRA | 16–32 GiB unified | minutes to a few hours | sunk hardware; marginal $0 |
| 1×24 GB GPU | 7B QLoRA/SFT | 24 GB | roughly 1–6 h | provider rate × time |
| 1×A100 80 GB | 7B–14B LoRA or heavier rollouts | 80 GB | roughly 1–6 h | HF $2.50/h; Modal $2.4984/h; provider overhead extra |
| 1×H100 80 GB | 7B–14B faster training/rollout | 80 GB | roughly 0.5–4 h | RunPod $2.89/h PCIe; Lambda $3.29/h PCIe; Modal $3.9492/h |
| 8×80 GB | 9B GRPO reference scale | 640 GB | NVIDIA tutorial says 3–5 h | at least tens to >$100, before storage/API |

Modal hourly values are its published per-second rates multiplied by 3,600.
RunPod availability and community/secure prices vary. NVIDIA's official
Workplace Assistant GRPO tutorial calls for 8×80 GB GPUs; that scale is
unjustified for the current 16-example asset.

No paid API or GPU call was made. Before an API baseline, freeze the number of
episodes, maximum turns and tokens, multiply by the provider's dated input,
cached-input, output and tool fees, add a 20% retry ceiling, and ask for
approval.

## Next falsification

Collect at least 100 rights-valid train episodes and a separate prospective
holdout. Run base, SFT and retrieval/harness controls with at least three seeds.
Only consider RLVR after grader exploitation tests and when base rollouts show
non-zero reward variance. Promote a result only if decision accuracy and
outcome-adjusted performance improve, not merely JSON validity.

## Cost sources

- <https://www.runpod.io/pricing>
- <https://lambda.ai/instances>
- <https://modal.com/pricing>
- <https://huggingface.co/docs/hub/main/spaces-overview>
- <https://docs.nvidia.com/nemo/gym/latest/training-tutorials/nemo-rl-grpo/>
