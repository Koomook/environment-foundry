# HUD v6 RLVR draft catalog

This directory targets the portable HUD v6 `Task`/`Taskset` row contract at
stable SDK `hud==0.6.15`. It does not use the archived `hud-vf-gym` v5 adapter.

[`taskset.jsonl`](taskset.jsonl) contains 20 schema-valid rows with stable
slugs, typed arguments, split/rights facets, bounded agent configuration, and
an intended authoritative verifier task. It is a design catalog, not a manifest
that may be passed to `Taskset.run()` or `TrainingClient`. The rows refer to two
templates that do not yet exist:

- actor: environment `stateful-workspace-cutover`, template `repair-cutover`;
- verifier: environment `stateful-workspace-cutover-verifier`, template
  `verify-cutover`.

The Terminal-Bench-format package supplies locally executable mechanics, but it
does not implement the HUD actor/verifier templates or the 20 profile variants.
The stable SDK can parse these rows; it cannot execute them. Under the current
pending receipt, do not set `HUD_API_KEY`, enable telemetry/file tracking, call
a remote model API, sync, deploy, upload, collect rollouts, or train.

After a superseding rights receipt and real templates exist, calibrate repeated
complete groups with frozen sampling. Retain reward, task slug, `group_id`,
group size/order, trace ID, prompt/output token IDs, output logprobs, model and
sampling configuration, stop reason, task/profile/image digests, SDK version,
and rights receipt. HUD's training-time mask is not a captured rollout field.
Define timeout handling so groups remain complete. Physically separate future
train, dev, and sealed-evaluation manifests before any training use.

Validate the manifest locally:

```bash
uv run python knowledge/lab/experiments/stateful-workspace-cutover-recovery/rlvr/validate_taskset.py
```
