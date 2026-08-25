# 영상 기술 감사: AI가 칩 설계를 배우기 위한 simulator·data·feedback loop

> 상태: 비정규 연구 메모. canonical company truth가 아니다.
> 작성일: 2026-07-30
> 감사 대상: [Chip design from the bottom up – Reiner Pope](https://www.youtube.com/watch?v=oIk3R-sMX5o), [공식 transcript](https://www.dwarkesh.com/p/reiner-pope-2)
> 범위: 영상의 핵심 기술 주장과, 그 주장으로부터 도출되는 AI 칩 설계 학습 환경. 사업 계획, 파트너 확보, 실행 로드맵은 다루지 않는다.
> 출처 정책: 영상은 감사 대상일 뿐 검증 근거로 사용하지 않았다. 검증에는 공식 문서, 공식 프로젝트 페이지, 원 논문만 사용했다.

## 한 문장 결론

영상의 가장 중요한 통찰은 대체로 맞다. AI 칩 설계는 MAC 개수를 키우는 문제가 아니라 **정확도 제약 아래에서 연산 정밀도, 데이터 재사용, 메모리 계층, 공간 배열, 파이프라인, 물리 PPA를 함께 최적화하는 문제**다.

따라서 AI에게 필요한 것은 정적 RTL 모음 하나가 아니라 다음을 잇는 multi-fidelity closed loop다.

```text
workload + accuracy target
  → architecture/dataflow simulator
  → executable reference model
  → HLS/RTL implementation
  → functional verification
  → synthesis/place-and-route/signoff
  → FPGA or silicon measurement
  → simulator calibration + next design action
```

낮은 fidelity simulator는 후보를 많이 탐색하고, 높은 fidelity 결과는 낮은 단계의 순위가 현실에서도 유지되는지를 채점해야 한다.

## 공개 설명에 쓸 수 있는 핵심 5개

아래 다섯 문장은 공개 콘텐츠에서 사용해도 될 만큼 1차 자료의 지지가 강하다. 단, 링크된 단서까지 함께 유지해야 한다.

### PUBLIC CORE 1/5 — AI 가속기의 기본 계산은 matrix multiply-accumulate이며, 입력과 누산 정밀도는 분리될 수 있다

**공개 문장**

> 현대 AI 가속기는 행렬 곱의 multiply-accumulate를 대량 병렬화한다. 낮은 정밀도의 입력을 더 높은 정밀도로 누산하는 mixed-precision 설계가 일반적이므로, AI는 비트 수뿐 아니라 정확도·처리량·메모리 사용량의 공동 trade-off를 배워야 한다.

**검증**

- Google의 1세대 TPU 논문은 핵심 연산부를 65,536개의 8-bit MAC matrix multiply unit으로 설명한다: [In-Datacenter Performance Analysis of a Tensor Processing Unit](https://research.google/pubs/in-datacenter-performance-analysis-of-a-tensor-processing-unit/).
- NVIDIA 공식 문서는 Tensor Core가 `D = A × B + C`를 수행하고, FP16 입력 product를 FP32로 accumulate할 수 있다고 설명한다: [NVIDIA mixed precision guide](https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html), [Turing Tensor Core operations](https://docs.nvidia.com/cuda/archive/11.8.0/turing-tuning-guide/index.html).
- 최신 TensorRT 문서도 입력 정밀도와 accumulation precision을 별도로 제어하며, accumulation range가 입력 이상이어야 한다고 설명한다: [TensorRT precision control](https://docs.nvidia.com/deeplearning/tensorrt/10.x.x/inference-library/precision-control.html).

**단서**

영상의 작은 unsigned-integer multiplier에서 보이는 `bit width²` gate-count 직관은 유용하지만, 실제 FP4/FP8 product throughput을 그대로 예측하는 공식은 아니다. exponent, format scaling, sparsity 조건, accumulator, memory bandwidth, non-matrix operations가 개입한다.

### PUBLIC CORE 2/5 — 데이터 이동과 재사용은 연산기 자체만큼 중요하다

**공개 문장**

> AI 칩의 효율은 MAC 수만으로 결정되지 않는다. 같은 데이터를 가까운 메모리에서 얼마나 재사용하고, 비싼 원거리 이동을 얼마나 줄이는지가 성능과 에너지의 핵심이다.

**검증**

- MIT의 Eyeriss 원 연구는 on-chip/off-chip data movement가 computation보다 더 큰 energy cost를 만들 수 있으며, local reuse로 이를 줄이는 것이 핵심이라고 설명한다: [Eyeriss JSSC/프로젝트 설명](https://www.rle.mit.edu/eyeriss-an-energy-efficient-reconfigurable-accelerator-for-deep-convolutional-neural-networks/), [ISCA paper](https://people.csail.mit.edu/emer/media/papers/2016.06.isca.eyeriss_architecture.pdf).
- NVIDIA의 Timeloop 원 논문은 dataflow와 memory hierarchy의 공동 설계가 accelerator energy efficiency에 결정적이라고 보고한다: [Timeloop: A Systematic Approach to DNN Accelerator Evaluation](https://research.nvidia.com/publication/2019-03_timeloop-systematic-approach-dnn-accelerator-evaluation).
- NVIDIA 공식 mixed-precision guide는 arithmetic intensity를 FLOPs/input byte로 정의하며, 이 값이 낮으면 Tensor Core peak에 도달하기 전에 memory-bound가 된다고 설명한다: [Increasing arithmetic intensity](https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html).

**단서**

“데이터 이동이 항상 연산보다 N배 비싸다” 같은 고정 배수는 node, voltage, SRAM/DRAM/HBM, layout, access pattern에 따라 달라진다. AI 환경은 고정 상수가 아니라 실제 technology/library와 workload로 characterization해야 한다.

### PUBLIC CORE 3/5 — systolic/spatial array의 가치는 local reuse와 communication amortization에 있다

**공개 문장**

> Systolic 또는 spatial array는 행렬 연산을 공간에 펼치고 데이터와 partial sum을 가까이 재사용해, 연산 하나마다 중앙 register file이나 외부 메모리를 왕복하는 비용을 줄인다.

**검증**

- Google TPU 원 논문은 65,536 8-bit MAC matrix unit과 28 MiB software-managed on-chip memory를 함께 사용했다고 보고한다: [TPU ISCA 2017](https://research.google/pubs/in-datacenter-performance-analysis-of-a-tensor-processing-unit/).
- Eyeriss는 spatial array, local scratchpads, configurable multicast NoC를 사용해 filter, image, partial sum의 local reuse를 높였다: [Eyeriss ISSCC paper](https://dspace.mit.edu/bitstream/handle/1721.1/101151/eyeriss_isscc_2016.pdf).
- Timeloop은 architecture topology만이 아니라 workload를 어떤 dataflow와 tile로 mapping할지도 함께 탐색한다: [Timeloop paper/project page](https://research.nvidia.com/publication/2019-03_timeloop-systematic-approach-dnn-accelerator-evaluation).

**단서**

영상의 “가장 효율적인 것으로 알려진 matrix-multiply circuit”이라는 표현은 너무 절대적이다. 최적 구조는 workload shape, sparsity, precision, memory capacity/bandwidth, utilization, programmable flexibility에 따라 달라진다.

### PUBLIC CORE 4/5 — 더 빠른 clock과 더 많은 pipeline register는 공짜가 아니다

**공개 문장**

> 파이프라인을 깊게 하면 stage당 critical path를 줄여 더 높은 clock을 노릴 수 있지만, latency와 register area·power가 늘어난다. feedback loop가 있는 연산은 feed-forward logic보다 재타이밍하기 어렵다.

**검증**

- Google XLS 공식 scheduler 문서는 pipeline의 경쟁 목적을 stage 수/latency 최소화, stage 최대 delay 최소화/clock 향상, pipeline register 최소화로 명시한다: [XLS pipeline scheduling](https://google.github.io/xls/scheduling/).
- XLS delay methodology는 지나치게 보수적인 timing estimate가 불필요한 pipeline stage와 flop을 만들어 area와 power를 증가시킨다고 설명한다: [XLS delay estimation](https://google.github.io/xls/delay_estimation/).
- XLS는 target process에 대해 operation delay를 EDA synthesis로 characterize하고, 그 모델로 cycle scheduling을 수행한다: [XLS delay-model characterization](https://google.github.io/xls/adding_ir_operation/).

**단서**

clock frequency만 높다고 chip throughput이 높아지는 것은 아니다. utilization, work/cycle, memory stalls, pipeline bubbles, voltage/power/thermal 제한을 함께 측정해야 한다.

### PUBLIC CORE 5/5 — cache와 software-managed memory는 다른 predictability/flexibility trade-off를 만든다

**공개 문장**

> Hardware-managed cache는 범용성과 평균 성능을 높이지만 실행시간 변동을 만들 수 있다. Software-managed on-chip memory는 compiler가 이동 시점을 명시해 예측 가능성을 높일 수 있지만, scheduling 부담을 software로 옮긴다.

**검증**

- Google의 TPU 원 논문은 28 MiB software-managed on-chip memory와 deterministic execution model을 설명하며, CPU/GPU의 cache, out-of-order execution, multithreading 등 time-varying optimization과 비교한다: [TPU ISCA 2017](https://research.google/pubs/in-datacenter-performance-analysis-of-a-tensor-processing-unit/).
- Timeloop은 memory hierarchy에 데이터를 언제 어디에 stage할지를 mapping 문제의 일부로 취급한다: [Timeloop](https://research.nvidia.com/publication/2019-03_timeloop-systematic-approach-dnn-accelerator-evaluation).

**단서**

cache miss의 변동은 “cache 안의 random-number generator” 하나로 설명되지 않는다. replacement policy, address mapping, interference, prefetching, coherence, OS activity 등 여러 원인이 있다. 또한 scratchpad도 DMA contention, network, bank conflict, compiler schedule에 따라 시스템 수준의 변동이 생길 수 있다.

## 영상 주장별 기술 감사

| 영상의 핵심 주장 | 판정 | 공개 시 필요한 수정 |
|---|---|---|
| AI chip의 주요 primitive는 matrix MAC이다 | `SUPPORTED WITH SCOPE` | dense linear/conv에서 강하다. attention의 softmax, normalization, routing, communication 등 non-MAC work도 포함해야 한다. |
| 낮은 input precision과 높은 accumulation precision을 함께 쓴다 | `SUPPORTED` | NVIDIA mixed-precision 문서와 TPU 계열 설계가 지지한다. accuracy gate가 반드시 필요하다. |
| 작은 integer multiplier의 area는 bit width에 대략 quadratic하게 증가한다 | `PEDAGOGICALLY USEFUL` | 특정 multiplier construction의 gate-count 직관이다. floating-point block 전체나 product throughput의 보편 법칙으로 쓰지 않는다. |
| data movement logic/cost가 arithmetic logic보다 클 수 있다 | `SUPPORTED WITH TECHNOLOGY DEPENDENCE` | Eyeriss/Timeloop이 방향을 지지한다. 고정 배수는 사용하지 않는다. |
| systolic array는 weights/data를 local하게 유지해 communication을 amortize한다 | `SUPPORTED` | weight-stationary는 여러 dataflow 중 하나다. workload에 따라 output/row/other-stationary가 나을 수 있다. |
| AI chip의 주요 결정은 array와 register-file 크기 같은 sizing이다 | `SUPPORTED BUT INCOMPLETE` | precision, NoC, HBM interface, sparsity, pipeline, compiler, yield/thermal/reliability도 공동 변수다. |
| global clock과 pipeline register가 timing을 정한다 | `SUPPORTED` | multi-clock, asynchronous logic, clock gating 등의 예외가 있다. |
| pipeline을 깊게 하면 clock은 빨라지지만 area/latency cost가 생긴다 | `SUPPORTED` | throughput은 frequency만이 아니라 utilization과 work/cycle의 함수다. |
| FPGA는 ASIC보다 대략 10배 비효율적이고 최초 비용은 각각 특정 금액이다 | `DO NOT GENERALIZE` | workload, FPGA family, process, volume, NRE, packaging에 따라 크게 달라진다. 공개 핵심 숫자로 사용하지 않는다. |
| FPGA LUT와 programmable routing이 flexibility overhead를 만든다 | `SUPPORTED IN PRINCIPLE` | 실제 FPGA는 LUT 크기, carry chain, DSP/BRAM/hard IP가 다양해 단순 gate count보다 복잡하다. |
| cache가 CPU latency nondeterminism의 중요한 원인이다 | `SUPPORTED WITH CAVEAT` | cache만이 원인은 아니며 replacement가 반드시 random인 것도 아니다. |
| CPU core가 GPU core보다 큰 이유는 branch predictor다 | `PARTIAL` | branch prediction은 한 요인이다. OoO scheduling, rename, speculation, cache/coherence, wide decode와 GPU SIMT execution도 포함해야 한다. |
| “GPU는 작은 TPU 여러 개다” | `RHETORICAL, NOT PRECISE` | Tensor Cores와 matrix units의 유사성을 설명하는 비유로만 사용하고 architecture identity로 말하지 않는다. |

## 공식 수치와 충돌하거나 조건이 빠진 부분

### FP4 대 FP8가 “정확히 3배”라는 표현

영상은 B300 세대에서 FP4가 FP8보다 3배 빠르다는 취지의 설명을 한다. 공식 DGX B300 사양은 다음처럼 조건을 분리한다.

- FP4 Tensor Core: 144 PFLOPS sparse / 108 PFLOPS dense
- FP8 Tensor Core: 72 PFLOPS sparse, dense는 그 절반

출처: [NVIDIA DGX B300 specifications](https://www.nvidia.com/en-sg/data-center/dgx-b300/).

어떤 sparse/dense 열을 비교하는지에 따라 비율이 달라진다. 따라서 공개 설명은 “낮은 정밀도는 더 높은 peak throughput과 더 작은 memory footprint를 가능하게 하지만 실제 배수는 format과 sparsity 조건, workload utilization에 의존한다”로 제한해야 한다.

### FPGA 대 ASIC의 “10배”와 최초 비용

방향은 맞지만 보편 수치가 아니다.

- FPGA의 LUT, programmable routing, configuration memory가 overhead를 만든다는 설명은 타당하다.
- 그러나 efficiency ratio와 NRE는 target node, die size, package, mask set, IP, verification, volume, chosen FPGA에 따라 달라진다.
- 이 영상의 숫자를 public fact나 환경의 reward coefficient로 사용하면 안 된다.

### “systolic array가 가장 효율적인 circuit”

Systolic/spatial design은 중요한 family이나 유일한 최적해가 아니다. Timeloop과 Eyeriss 연구 자체가 architecture와 dataflow를 workload별로 함께 탐색해야 함을 보여준다. 공개 문구는 “행렬 연산에서 널리 쓰이는 효율적 구조”가 안전하다.

## 이 영상이 암시하는 학습 문제의 정확한 정의

AI의 task는 “칩 그림을 생성”하는 것이 아니다.

```text
Given:
  workload distribution W
  correctness / model-quality floor Q
  technology and library T
  package / memory / bandwidth constraints M
  power, area, latency, throughput budgets B

Choose:
  architecture A
  mapping/compiler schedule S
  precision policy P
  RTL / physical implementation I

Such that:
  functional_correctness(I, W) = true
  model_quality(P, W) >= Q
  signoff(I, T) = pass
  objectives(I, S, W) lie on a useful Pareto frontier
```

하나의 weighted score로 너무 빨리 압축하면 안 된다. correctness, model accuracy, timing, DRC 같은 것은 hard gate로 두고, valid design 사이에서 latency, throughput, energy, area, cost를 Pareto 비교하는 편이 안전하다.

## AI가 관측해야 하는 data

### 1. Workload와 software semantics

- model/operator graph
- tensor shape와 dynamic-shape distribution
- batch, sequence length, context growth
- precision별 model accuracy 또는 numerical-error result
- sparsity pattern과 실제 nonzero distribution
- kernel trace, operator frequency, dependency
- latency SLO, throughput target, deployment scenario

공개 workload baseline으로 [MLPerf Inference](https://docs.mlcommons.org/inference/)를 사용할 수 있다. MLPerf는 model, dataset, accuracy target, latency scenario를 함께 정의한다. 다만 공개 benchmark 하나가 특정 고객 workload를 대표한다고 가정하면 안 된다.

### 2. Architecture state

- PE/MAC array shape와 count
- supported data types와 accumulator
- register file/SRAM/HBM capacity와 ports
- memory hierarchy와 bandwidth/latency
- dataflow, tiling, loop order, multicast/reduction
- NoC topology와 link width
- pipeline stages와 target clock
- cache/scratchpad policy
- utilization, stalls, traffic, reuse distance

### 3. Implementation state

- HLS/IR/RTL
- testbench, assertion, golden reference model
- synthesis netlist와 constraints
- floorplan, placement, routing, clock tree
- PPA and signoff reports
- tool/version/PDK/library/seed/command

### 4. Outcome and decision

- 후보가 왜 accept/reject되었는지
- 어떤 constraint를 위반했는지
- simulator prediction과 RTL/P&R/FPGA/silicon measurement의 차이
- 실패한 action과 rollback
- 다음 iteration에서 바꾼 변수

정적 최종 design보다 이 transition record가 학습에 더 중요하다.

## AI가 취할 수 있는 typed action

action은 자유 shell이 아니라 계층별로 제한해야 한다.

### Architecture action

- array rows/columns 변경
- SRAM/register-file capacity/ports 변경
- dataflow와 tiling 선택
- precision/accumulator 선택
- NoC/link width 변경
- cache/scratchpad 선택

### Microarchitecture/HLS action

- pipeline stage/clock target
- unroll, pipeline, dataflow directive
- buffer placement와 banking
- operator fusion
- sparsity support

### RTL/verification action

- scoped RTL patch
- assertion/test 추가
- stimulus/seed 선택
- waveform probe 선택

### Physical action

- utilization/density/floorplan
- macro placement
- synthesis/P&R recipe
- buffer/resize/CTS configuration

각 action에는 allowed range, compute budget, rights, rollback이 있어야 한다.

## 필요한 simulator stack

단일 simulator가 전체 질문에 답하지 못한다.

### Layer 1 — analytical architecture/dataflow model

**목적**

많은 architecture와 mapping 후보를 빠르게 거른다.

**도구**

- [Timeloop](https://research.nvidia.com/publication/2019-03_timeloop-systematic-approach-dnn-accelerator-evaluation): architecture, workload, mapping을 받아 performance/energy projection과 mapping search를 수행.
- [Accelergy](https://accelergy.mit.edu/): user-defined component와 action에 대한 architecture-level energy/area estimator.
- [gem5](https://www.gem5.org/about/): CPU/memory/full-system 또는 syscall-emulation 수준 architecture simulation.

**관측/출력**

- cycles, utilization
- memory traffic by level
- energy estimate
- mapping/tiling
- bandwidth bottleneck

**한계**

- technology characterization와 implementation detail이 부정확하면 ranking도 틀릴 수 있다.
- analytical estimate는 signoff가 아니다.

### Layer 2 — executable functional model와 numerical grader

**목적**

precision, quantization, scheduling change가 model quality와 functional semantics를 보존하는지 확인한다.

**필요한 것**

- framework reference model
- golden tensor inputs/outputs
- tolerances
- task-level accuracy dataset
- edge-case and held-out vectors

**grader**

- exact 또는 tolerance-based equivalence
- end-task accuracy
- overflow/underflow/saturation
- nondeterminism

architecture simulator가 빠르더라도 이 layer를 통과하지 못하면 invalid다.

### Layer 3 — HLS/RTL cycle simulation

**목적**

cycle-level protocol, state, pipeline, control, corner case를 검증한다.

**도구**

- [XLS](https://google.github.io/xls/): HLS, scheduling, Verilog generation, IR/netlist equivalence와 delay model.
- [Verilator](https://verilator.org/guide/latest/overview.html): SystemVerilog를 executable C++/SystemC model로 compile하며 lint, waveform, coverage를 지원.
- [cocotb](https://docs.cocotb.org/en/stable/): Python reference/testbench와 HDL simulator를 연결.

**grader**

- compile/elaboration
- public + hidden tests
- assertions
- code/toggle/functional coverage
- reference-model equivalence
- protocol/latency contract

**한계**

Verilator는 모든 signoff timing/analog/mixed-signal behavior의 대체물이 아니다. 공식 language 문서도 SystemVerilog/AMS, specify/timing check 등에 제한을 명시한다: [Verilator language support](https://verilator.org/guide/latest/languages.html).

### Layer 4 — FPGA-accelerated full-system simulation

**목적**

RTL에서 긴 software workload, OS, I/O, memory timing을 실행한다.

**도구**

- [FireSim](https://docs.fires.im/en/latest/FireSim-Basics.html): open-source FPGA-accelerated full-system simulation. 공식 문서는 tens-to-hundreds of MHz 실행, ASIC RTL과 cycle-accurate I/O model의 co-simulation을 설명한다.
- Golden Gate의 host decoupling은 target simulation을 deterministic하게 만들고 memory/I/O timing model을 분리한다: [FireSim overview](https://docs.fires.im/en/1.21.0/Golden-Gate/Overview.html).

**grader**

- software boot/pass
- long workload correctness
- cycle counts와 counters
- memory/NoC behavior
- reference ISA/model trace comparison

**한계**

FPGA prototype의 host timing을 ASIC timing으로 오인하면 안 된다. FireSim 자체도 FPGA prototype과 target-decoupled simulation을 구분한다.

### Layer 5 — synthesis와 physical implementation

**목적**

architecture proxy가 실제 cell, wire, congestion, timing, power로 구현 가능한지 확인한다.

**도구**

- [OpenROAD/ORFS](https://openroad.readthedocs.io/en/latest/main/README.html): 공개 RTL-to-GDSII flow와 Tcl/Python control.
- Yosys/OpenROAD/KLayout 기반 공개 flow 또는 고객 권리 경계 안의 상용 synthesis/P&R/signoff flow.

**grader**

- logic equivalence
- flow completion
- WNS/TNS와 target frequency
- area
- routed power estimate
- congestion/DRC
- IR-drop와 physical verification
- runtime/tool cost

**한계**

public PDK/OpenROAD 결과가 advanced-node commercial signoff의 ground truth는 아니다.

### Layer 6 — silicon feedback

**목적**

simulator ranking이 현실을 예측하는지 확인한다.

**data**

- benchmark latency/throughput
- power/energy/thermal
- hardware counters
- voltage/frequency corners
- yield/test/failure data

**grader**

- predicted vs measured error
- candidate ranking preservation
- constraint violations missed by simulation

silicon이 없어도 lower layers는 만들 수 있지만, prospective silicon 또는 high-fidelity commercial reference가 없으면 “현실을 예측하는 simulator”라는 주장은 `NOT YET`이다.

## Feedback loop

### Episode schema

```yaml
episode:
  initial_state:
    workload_hash: ...
    architecture: ...
    implementation_commit: ...
    technology_locator: ...
    toolchain_digest: ...
    seed: ...
  action:
    type: resize_sram
    parameters:
      from_kib: 1024
      to_kib: 1536
  cheap_transition:
    simulator: timeloop+accelergy
    metrics:
      latency_cycles: ...
      dram_reads: ...
      estimated_energy: ...
  implementation_transition:
    simulator: rtl+openroad
    metrics:
      tests_passed: ...
      wns: ...
      area: ...
      routed_power: ...
  high_fidelity_outcome:
    source: fpga_or_silicon
    metrics: ...
  decision:
    accepted: false
    reason: timing_failure
```

### 학습 loop

1. workload와 hard constraints를 sample한다.
2. agent가 한 계층의 typed action을 제안한다.
3. cheap simulator가 invalid/weak candidate를 제거한다.
4. reference model이 numerical/functional correctness를 채점한다.
5. RTL과 physical flow가 cycle accuracy와 PPA를 채점한다.
6. 일부 candidate만 FPGA, commercial signoff, silicon으로 승격한다.
7. prediction error와 rank inversion을 저장한다.
8. simulator calibration과 agent policy를 분리해 업데이트한다.
9. held-out workload/design/technology에서 다시 평가한다.

### reward 구조

```text
if functional failure or accuracy below floor:
    invalid
elif timing/DRC/signoff failure:
    invalid
else:
    Pareto(latency, throughput, energy, area, memory, tool-runtime)
```

초기부터 모든 metric을 하나의 숫자로 합치면 agent가 proxy를 악용하기 쉽다. hard gate와 Pareto frontier를 유지한 뒤 특정 deployment contract에서만 scalarization해야 한다.

## simulator 간 calibration

### 반드시 저장할 오차

- Timeloop cycles vs RTL cycles
- Accelergy energy vs gate-level/power-tool estimate
- HLS delay vs synthesis STA
- pre-route timing vs post-route timing
- RTL/FireSim counters vs silicon counters
- public benchmark ranking vs held-out workload ranking

### calibration metric

- absolute/relative error
- Spearman rank correlation
- constraint violation false-negative rate
- candidate top-k recall
- design family/node 이동 시 error drift

실무적으로 가장 중요한 것은 숫자 하나의 오차보다 **좋은 후보의 순위가 high-fidelity 단계에서도 유지되는가**다.

## dataset 구성

### 공개 seed data

- [MLPerf Inference](https://docs.mlcommons.org/inference/): workload, dataset, accuracy와 latency constraints.
- [CircuitNet](https://circuitnet.github.io/intro/overview.html): congestion, DRC violation, IR-drop, net-delay를 위한 backend multi-modal features.
- 공개 RTL과 ORFS designs: 기능/물리 flow bootstrap에 사용하되 design별 license를 확인.

### 실제로 학습 가치가 높은 trajectory data

- architecture config → mapping → simulator report
- precision change → model accuracy delta
- HLS/RTL change → tests/coverage/cycles
- synthesis/P&R action → final routed PPA
- rejected design과 rollback reason
- proxy prediction → higher-fidelity result
- human accept/waive/escalate decision

정적 성공작만 모으면 counterfactual과 failure boundary를 배울 수 없다.

## evaluation split

random file split은 leakage를 만들기 쉽다.

- unseen workload family
- unseen tensor shapes
- unseen RTL block/design family
- unseen PDK/library 또는 technology corner
- unseen memory budget
- chronological split
- hidden numerical edge cases
- hidden downstream signoff corner

동일 design의 작은 parameter variant가 train과 test에 동시에 들어가지 않도록 group split해야 한다.

## 공개 설명에서 피할 표현

- “AI는 회로도만 보면 최적 칩을 설계할 수 있다.”
- “하나의 simulator가 실제 chip 성능을 정확히 예측한다.”
- “MAC 수가 많으면 빠르다.”
- “데이터 이동은 항상 연산보다 정확히 N배 비싸다.”
- “FP4는 FP8보다 항상 3배 빠르다.”
- “FPGA는 ASIC보다 항상 10배 느리거나 비싸다.”
- “GPU는 작은 TPU들의 묶음이다.”
- “OpenROAD 결과가 production signoff다.”
- “공개 RTL corpus만 있으면 산업용 chip-design agent를 학습할 수 있다.”

## 공개 설명에 적합한 최종 요약

> AI가 칩 설계를 배우려면 세 종류의 피드백이 함께 필요하다. 첫째, 실제 모델과 tensor shape를 실행해 정확도와 성능을 측정하는 workload 피드백. 둘째, dataflow·memory hierarchy·precision·pipeline을 빠르게 탐색하는 architecture simulator. 셋째, RTL 검증과 physical implementation, FPGA 또는 silicon으로 simulator의 예측을 교정하는 high-fidelity 피드백이다. 학습 단위는 최종 RTL 파일이 아니라, 어떤 설계 상태에서 무엇을 바꾸었고 각 fidelity 단계에서 어떤 결과가 나왔는지를 연결한 episode다.

## 주요 1차 출처

- 영상 transcript: <https://www.dwarkesh.com/p/reiner-pope-2>
- Google TPU ISCA 2017: <https://research.google/pubs/in-datacenter-performance-analysis-of-a-tensor-processing-unit/>
- NVIDIA Tensor Core mixed precision: <https://docs.nvidia.com/deeplearning/performance/mixed-precision-training/index.html>
- NVIDIA B300 official specifications: <https://www.nvidia.com/en-sg/data-center/dgx-b300/>
- Eyeriss project/JSSC summary: <https://www.rle.mit.edu/eyeriss-an-energy-efficient-reconfigurable-accelerator-for-deep-convolutional-neural-networks/>
- Eyeriss ISCA paper: <https://people.csail.mit.edu/emer/media/papers/2016.06.isca.eyeriss_architecture.pdf>
- Timeloop original paper/project page: <https://research.nvidia.com/publication/2019-03_timeloop-systematic-approach-dnn-accelerator-evaluation>
- Accelergy: <https://accelergy.mit.edu/>
- XLS scheduling: <https://google.github.io/xls/scheduling/>
- XLS delay estimation: <https://google.github.io/xls/delay_estimation/>
- gem5: <https://www.gem5.org/about/>
- Verilator: <https://verilator.org/guide/latest/overview.html>
- cocotb: <https://docs.cocotb.org/en/stable/>
- FireSim: <https://docs.fires.im/en/latest/FireSim-Basics.html>
- OpenROAD: <https://openroad.readthedocs.io/en/latest/main/README.html>
- MLPerf Inference: <https://docs.mlcommons.org/inference/>
- CircuitNet: <https://circuitnet.github.io/intro/overview.html>
