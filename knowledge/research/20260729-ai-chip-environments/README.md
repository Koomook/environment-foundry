# AI chip-design environments: five-iteration research packet

Date: 2026-07-29
Status: divergent research; not canonical company truth
Owner: EF-02 Environment Compiler
Question: What simulator and data would let AI improve chip design, and is a
Korean semiconductor SME a better first partner than a software company?

## Executive decision

`HYPOTHESIS`: Environment Foundry should not begin by acquiring a generic
corpus of Korean chip-company files. It should compile one rights-valid,
executable decision loop inside a partner boundary.

Two layers should remain distinct:

1. **Public mechanics pilot — RTL regression repair.** Use Icarus or Verilator,
   cocotb or formal checks, hidden regression, and Yosys synthesis to prove the
   observation/action/transition/grader/reset contract.
2. **Partner-value pilot — reference-design signoff closure.** With a design
   house that owns a non-customer test vehicle, allow only bounded
   constraint/config/Tcl actions in a partner-side OpenROAD or commercial flow.
   Grade final routed timing, DRC, congestion, runtime, and engineer active time.

The first partner hypothesis is a Korean design house with an internal,
non-customer reference design. A configurable IP vendor is the next environment;
an equipment OEM's internal test-rig diagnostic task is a strong parallel option.
Actual partner willingness, rights, task volume, and budget are `NOT YET`.

## First-principles decomposition

Chip design is a constrained search problem under partial observation,
multi-fidelity transitions, and delayed outcomes.

The objective is not one scalar:

```text
valid =
  functional_tests_pass
  AND formal_properties_pass
  AND no_unwaived_DRC
  AND LVS_match
  AND timing_within_threshold
  AND IR_drop_within_limit

score(valid design) =
  Pareto(PPA, verification effort, tool runtime, test cost)
```

A corpus supplies states. An environment must supply:

- decision-time observation boundary;
- typed actions and legal preconditions;
- a transition engine that actually runs the tool;
- explicit termination and budgets;
- protected public/hidden/downstream graders;
- deterministic or tolerance-bounded reset/replay;
- field-level access, operation, evaluation, training, derivative, resale,
  export, retention, revocation, deletion, and publication rights.

The scarce unit is therefore not an RTL or GDS file. It is a rights-valid
episode:

```text
versioned state
→ typed engineering action
→ pinned tool + PDK + seed + constraints
→ machine result and failure cause
→ accept / revert / waive
→ downstream outcome
```

## Simulator and data stack

| Layer | Transition engines | Required decision data | Grader | Main reality gap |
|---|---|---|---|---|
| Architecture/workload | gem5, FireSim, Timeloop/Accelergy | workload binary/trace, memory/stall counters, configuration, FPGA/silicon counters | correctness, latency, throughput, energy/area estimate, held-out workload | architecture model may mis-rank RTL or silicon |
| HLS/compiler | XLS, CIRCT HLS, Vitis HLS | executable reference, C/DSL, pragma, schedule, generated RTL | equivalence, II/latency/resource, post-P&R | HLS estimates can diverge downstream |
| RTL | Icarus, Verilator; VCS/Xcelium/Questa in commercial flow | spec, RTL, reference model, test/assertion, seed, waveform, bug-patch history | compile, public/hidden simulation, formal, coverage, synthesisability | visible-test gaming; incomplete X/Z or SystemVerilog fidelity |
| Formal/verification | cocotb, SymbiYosys; commercial formal/UVM | requirement-to-property trace, counterexamples, waivers, escaped bugs | proof, mutation detection, overconstraint, held-out assertions | agent can weaken tests or assumptions |
| Logic synthesis | Yosys/ABC; Design Compiler/Genus | RTL, SDC, libraries, recipe/action sequence, equivalence, downstream P&R | equivalence hard gate, mapped area/delay, routed PPA | AIG/cell proxies may mis-rank route |
| Physical design | OpenROAD/ORFS/KLayout; Innovus/Fusion | LEF/DEF/Liberty/SDC, floorplan, Tcl actions, rollback, route reports | completion, DRC, WNS/TNS, congestion, power proxy, runtime | open-node result is not advanced-node signoff |
| Signoff/analog | OpenSTA, KLayout, ngspice; foundry-qualified commercial stack | corners, parasitics, deck, waiver, ECO, Monte Carlo | DRC/LVS/timing/IR/EM/analog yield | deck/model rights and certification |
| DFT/test/silicon | OpenROAD DFT, Fault; ATPG/ATE stack | scan, fault/pattern, test bins, diagnosis, silicon telemetry | modeled coverage/cost, then actual defect escape/yield | modeled faults are not production defects |

This is a fidelity ladder, not a shopping list for one universal simulator.
Cheap tools generate episodes. Expensive tools test whether cheap ranking
predicts reality.

## Data acquisition priority

### Tier A — compile now

- versioned spec/RTL/testbench/assertions;
- CI regression input/output, seed, compile/simulation log;
- bug patch and before/after failure;
- synthesis/P&R config and machine-readable report;
- accept/revert label and source receipt.

### Tier B — partner-side only by default

- commercial simulator/formal/P&R/signoff episodes;
- proprietary libraries, PDK locators, IP abstracts;
- rejected attempts, ECOs, waivers, coverage closure;
- cross-stage link from RTL change to routed/signoff impact.

### Tier C — prospective outcome interface, not first corpus

- wafer sort/final test, yield and diagnosis;
- silicon performance, power and thermal;
- RMA/field failures and process correlations.

Raw customer RTL/GDS, full PDK/rule deck, real-name lot/wafer maps, fab recipes,
material formulations, engineer chat, and screen recordings default to
collection and training denied.

## Five executed iterations

The executable package is
`knowledge/lab/experiments/ai-chip-foundry/`.

| Iteration | Hypothesis and artifact | Observed result | New hypothesis |
|---|---|---|---|
| 1 | A compiler transition can reject invalid RTL. Icarus compile over four candidates. | The injected syntax error failed; three parseable candidates compiled. | Compilation cannot establish behavior. |
| 2 | A few visible examples accept a wrong implementation. Three disclosed smoke tests. | A visible-test gamer and both correct implementations passed. | Hidden behavior is required before quality optimization. |
| 3 | Exhaustive hidden behavior catches the exploit. Width-4 ALU, 1,024 combinations. | The gamer failed 828 combinations; both correct candidates passed all. | Correctness must be a hard gate before synthesis quality. |
| 4 | Frozen generic synthesis can rank equivalent RTL. Yosys recipe. | Verbose implementation used 41 generic cells; compact used 36. | Test whether the ranking survives a held-out parameter and higher fidelity. |
| 5 | The environment contract transfers to held-out width 5. 4,096 combinations plus synthesis. | Both stayed correct; compact used 46 cells versus verbose 52. | Next test is another block family and routed PPA correlation. |

An independently authored saturating-adder fixture exhaustively checked 65,536
input pairs and rejected a wraparound bug. This strengthens reproduction across
a second synthetic task, but does not establish company or chip-family transfer.

`OBSERVED`: a deterministic local replay environment can reject syntax errors,
detect visible-test gaming, gate correctness, compute a frozen synthesis proxy,
and replay at a held-out parameter.

`NOT YET`: formal robustness, final-route PPA correlation, commercial-node
transfer, company-data utility, prospective live ranking, foundry economics, or
silicon outcome.

## Korean SME partner wedge

### 1. Design house reference-design closure

- Start state: immutable internal reference/test-chip block, licensed
  tool/PDK locator, floorplan, SDC, previous reports.
- Observation: slack histogram, critical paths, congestion/DRC/IR summaries,
  warnings, action history.
- Action: allowlisted constraint patch, density/utilization, floorplan or
  bounded Tcl/ECO.
- Transition: partner-side deterministic synthesis/P&R/STA/DRC.
- Grader: equivalence and hard signoff gates, then PPA, runtime, active engineer
  time, and human rework.
- 20-episode path: at least five independent blocks across four checkpoints or
  constraint regimes; parameter sweeps alone do not count as transfer.
- Gate hypothesis: on held-out blocks, no increase in hard violations and at
  least 20% lower closure iteration or active engineer time. The partner must
  rewrite the threshold.

### 2. Configurable IP regression triage

Use a synthetic integration harness, minimized failure slice, configuration
manifest, and compile/lint/CDC/protocol regression. Hide the customer top-level
and protect golden vectors. Grade target failure removal, new regression escape,
patch minimality, runtime, and engineer review.

### 3. Equipment OEM internal test-rig diagnostics

Use internal rig alarm/event windows and injected faults, not a fab customer's
production recipe. V0 may recommend the next safe diagnostic step but may not
control equipment. Grade confirmed cause, time to diagnosis, first-time fix,
parts cost, and unsafe recommendation as a hard failure.

The strongest reason this market thesis can fail is rights fragmentation:
small-company data can still be owned jointly by the customer, foundry, EDA
vendor, IP vendor, and export-control regime. The second is episode scarcity;
one tape-out split into many parameter runs is not many independent decisions.
The third is incumbent EDA: an LLM/RL layer that cannot beat a human recipe,
random search, and Bayesian optimization under equal tool-hours has little
incremental value.

## 90-day falsifiable plan

### Days 0–14 — buy a task specification, not data

- Interview partner archetypes only after founder authorization for outreach.
- Ask for recent independent decision loops, replayability, grader, rights chain,
  tool/license automation, and the economic price of one iteration or engineer
  hour.
- Gate: three buyer-written specifications or one cost-covering paid design
  pilot.

### Days 15–30 — complete the public skeleton

- Expand RTL repair to five open or synthetic blocks.
- Add formal/mutation protection and a protected test surface.
- Add two small ORFS designs and final-route grading.
- Reproduce with two operators and run a revocation/deletion drill.

### Days 31–60 — 20 partner-side shadow episodes

- Execute in the partner enclave; raw RTL/PDK/log stays there.
- Export only fields explicitly granted, such as episode ID, typed action,
  scalar grader, runtime, and receipt.
- Freeze project/block/time holdouts.

### Days 61–90 — test ranking and demand

- Compare human, rule, random/Bayesian, generic-model, and agent baselines at
  equal compute/tool-hour budgets.
- Test whether offline ranking predicts prospective shadow ranking.
- Stop the segment if an eight-week 20-episode path, protected grader,
  prospective correlation, or buyer-written price does not exist.

## Central thesis and strongest objection

Selected thesis: the defensible asset is not a Korean chip corpus but a reusable
compiler that turns partner-authorized chip-design decisions into bounded,
graded, revocable environments. Korea may improve access and field integration;
it is `NOT YET` evidence of model-performance locality.

Strongest objection: a customer-specific on-prem integration may never become a
cross-customer data flywheel. If training and derivative rights remain denied
and each environment is rebuilt from scratch, the business may collapse into
EDA integration or consulting. The proof is gate 8 of the company proof ladder:
the second adapter must be measurably faster and cheaper while preserving
predictive evaluation.

## Primary-source ledger

- [OpenROAD documentation](https://openroad.readthedocs.io/en/latest/)
- [OpenROAD Flow Scripts](https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts)
- [Verilator documentation](https://verilator.org/guide/latest/overview.html)
- [cocotb simulator support](https://docs.cocotb.org/en/stable/simulator_support.html)
- [Yosys repository](https://github.com/YosysHQ/yosys)
- [gem5](https://www.gem5.org/about/)
- [FireSim](https://docs.fires.im/en/latest/FireSim-Basics.html)
- [Timeloop/Accelergy](https://timeloop.csail.mit.edu/)
- [CircuitNet](https://github.com/circuitnet/CircuitNet)
- [CircuitNet 3.0, ICLR 2026](https://openreview.net/pdf?id=lEDb4gQ4dB)
- [ChiPBench, end-to-end placement evaluation](https://papers.neurips.cc/paper_files/paper/2025/hash/1cba8502063fab9df252a63968691768-Abstract-Datasets_and_Benchmarks_Track.html)
- [AlphaChip addendum](https://www.nature.com/articles/s41586-024-08032-5)
- [ngspice documentation](https://ngspice.sourceforge.io/docs.html)
- [Synopsys VCS](https://www.synopsys.com/verification/simulation/vcs.html)
- [Synopsys VC Formal](https://www.synopsys.com/verification/static-and-formal-verification/vc-formal.html)
- [Ansys semiconductor analysis](https://www.ansys.com/products/semiconductors)
- [Korean MOTIE system-semiconductor support center](https://motie.go.kr/kor/article/ATCL8764a1224/155118734/view)
- [ADTechnology turnkey flow](https://www.adtek.co.kr/en/m21.php)
- [GAONCHIPS](https://www.gaonchips.com/en/)
- [OPENEDGES](https://www.openedges.com/interconnect)
- [Korean Semiconductor Layout-Design Act](https://law.go.kr/LSW/lsInfoP.do?chrClsCd=010204&lsiSeq=168005)
- [Korean Industrial Technology Protection Act](https://law.go.kr/LSW/lsInfoP.do?ancYnChk=0&chrClsCd=010202&efYd=20250722&lsiSeq=268583&urlMode=lsInfoP)

## Source and rights receipt

The report uses public official documentation, public repositories, original
papers, government pages, company public product pages, synthetic RTL, and
locally generated tool output. It contains no private company payload,
proprietary PDK, customer design, contact record, credential, or person-level
data. Vendor marketing supports product-surface claims only, not independent
performance claims or willingness to partner.
