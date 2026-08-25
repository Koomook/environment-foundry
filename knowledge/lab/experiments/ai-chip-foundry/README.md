# AI chip-foundry pilot

Status: `OBSERVED` local replay experiment; `NOT YET` a validated chip-design simulator.

This package tests the smallest useful environment wedge: repair or improve a
bounded RTL block while preserving behavior. It deliberately stops before
physical design, proprietary PDK use, tape-out, and live company data.

## Environment boundary

- Observation: a public-safe specification, candidate Verilog, tool diagnostics,
  and metrics revealed by the current iteration.
- Typed action: select a candidate RTL implementation for evaluation.
- Transition: compile and simulate with Icarus Verilog; synthesize with Yosys.
- Termination: compile failure, functional failure, budget exhaustion, or a
  passing candidate.
- Grader: deterministic compile, visible smoke tests, hidden exhaustive tests,
  synthesis cell count, exploit checks, and held-out-width transfer.
- Reset/replay: each run uses a fresh temporary build directory and immutable
  checked-in fixtures.
- Rights: all RTL and tests in this package are synthetic and authored for this
  experiment. Tool licenses remain upstream.

Run the five-iteration ALU ladder:

```bash
uv run python knowledge/lab/experiments/ai-chip-foundry/run_iterations.py
```

Outputs are written under `results/`. The iterations are research gates, not
five claims that the agent improved itself:

1. Can the environment distinguish parseable from broken RTL?
2. Can it distinguish plausible output from exhaustive functional correctness?
3. Can hidden behavior reject an implementation that games visible examples?
4. Can it rank functionally equivalent candidates by a reproducible synthesis
   proxy?
5. Does the task contract transfer to a held-out bit width?

An independent `fixtures/sat-add8/` task exercises the same environment shape
on an unsigned saturating adder. Its exhaustive grader covers all 65,536 input
pairs and rejects the injected wraparound bug. It is a second synthetic task,
not evidence of transfer to a real company workflow.

```bash
uv run python knowledge/lab/experiments/ai-chip-foundry/fixtures/sat-add8/evaluate.py \
  knowledge/lab/experiments/ai-chip-foundry/fixtures/sat-add8/gold.v
```

## Evidence boundary

Cell count from generic Yosys synthesis is an early area proxy only. It is not
power, timing, congestion, DRC, signoff, yield, or silicon outcome. Crossing that
boundary requires an RTL-to-GDS flow, a rights-valid PDK/tool setup, frozen
constraints, and prospective correlation against later-stage or measured
outcomes.
