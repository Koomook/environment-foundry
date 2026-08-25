# AI chip-foundry pilot v2 — sequential, mutation, fidelity

Status: `OBSERVED` local replay experiment; `NOT YET` a validated chip-design simulator.

v1 (`../ai-chip-foundry/`) proved the environment contract on two
*combinational* blocks (parameterized ALU, saturating adder) across five
iterations. v2 asks the next three questions, which are also the "proposed
next gate" of the 2026-07-29 handoff, minus RTL-to-GDS (documented as
`NOT YET` with cost estimate):

1. **Sequential transfer.** Does the same observation/action/transition/grader
   contract hold for a block with internal state, where exhaustive *input*
   testing is insufficient and sequences matter?
2. **Grader validation (mutation audit).** Is the hidden grader itself strong?
   Inject N mutations of the gold design; every behavior-changing mutant must
   be rejected. Survivors expose grader blind spots (or equivalent mutants).
3. **Fidelity step-up.** Does a real cell-library mapping (Nangate45 open
   library) rank designs the same as the generic cell-count proxy? If not,
   the proxy's reality gap is observable already at synthesis — before P&R.

## Environment boundary

- Observation: public-safe spec, candidate Verilog, tool diagnostics, metrics
  revealed by the current iteration.
- Typed action: select / submit a candidate RTL implementation.
- Transition: compile and simulate with Icarus Verilog 13; synthesize with
  Yosys 0.67 (generic, and liberty-mapped with Nangate45).
- Termination: compile failure, functional failure, budget exhaustion, pass.
- Grader: deterministic compile, visible sequences, hidden exhaustive
  sequence replay (2^14 sequences x 14 bits, cycle-accurate golden model),
  mutation audit, synthesis metrics.
- Reset/replay: fresh temp build directory; immutable checked-in fixtures.
- Rights: all RTL/TB in this package are synthetic, authored for this
  experiment. The Nangate45 liberty is fetched at runtime from the public
  OpenROAD-flow-scripts mirror and is NOT committed (see `.gitignore`).

Run:

```bash
uv run python knowledge/lab/experiments/ai-chip-foundry-v2/run_v2.py
```

Outputs under `results/`.

## Provenance

- `../ai-chip-foundry/rtl/correct_{compact,verbose}.v` are re-used read-only
  for the fidelity comparison (synthetic, authored for v1).
- Nangate45 `NangateOpenCellLibrary_typical.lib` source:
  <https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts>
  (platforms/nangate45/lib). Downloaded at runtime; license remains upstream.

## Evidence boundary

Liberty-mapped area/delay is a stronger proxy than generic cell count but is
still pre-P&R: no placement, routing, parasitics, DRC, signoff, power, or
silicon. RTL-to-GDS correlation (ORFS or partner-side flow) remains `NOT YET`.
