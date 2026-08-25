# 칩 설계 시뮬레이터 지도 & AI-for-Chip-Design 연구 조사

> 작성일: 2026-07-29 / 작성: Hermes 리서치 에이전트
> 목적: Environment Foundry의 칩 설계 도메인 확장 전략 수립을 위한 사전 조사
> 핵심 질문: **"AI가 칩을 잘 설계하려면 어떤 시뮬레이터와 데이터가 필요한가?"**
> 원칙: arXiv ID와 핵심 수치는 직접 검색으로 검증, 확인 불가 수치는 (미확정) 표기

---

# 파트 1: 시뮬레이터 계층 지도

칩 설계 파이프라인은 추상화 계층이 올라갈수록 정확도↓ 속도↑이다. RL 환경 설계 관점에서 가장 중요한 변수는 **"보상 1회 계산 비용"**이다. SPICE급(회로)은 사실상 RL 학습 루프에 못 넣고, RTL/가속기 모델링/물리설계(프록시 보상) 계층이 RL에 실제로 쓰인다.

## 1.1 RTL 시뮬레이션

| 항목 | 내용 |
|---|---|
| **Verilator** | 역할: synthesizable Verilog/SystemVerilog → C++ 변환 컴파일형 시뮬레이터 (cycle-based, 2-state). 입출력: RTL → 컴파일된 실행 바이너리, 파형(VCD/FST). 라이선스: **LGPL-3.0** (https://github.com/verilator/verilator). 실행 비용: 오픈소스 중 가장 빠름 — 초당 수백만~수억 사이클, 대규모 디자인도 분 단위 부팅. RL 환경 사례: RTL 생성 LLM의 문법/기능 검증 루프, cycle-accurate 보상 계산에 사용. 이벤트 기반이 아니라 testbench 타이밍 검증에는 부적합. |
| **Icarus Verilog** | 역할: 이벤트 구동 인터프리터형 시뮬레이터, 4-state, 지연/타이밍 시뮬레이션 가능. 입출력: RTL+testbench → 시뮬 결과/파형. 라이선스: **GPL-2.0** (https://github.com/steveicarus/iverilog). 실행 비용: Verilator보다 1~2자릿수 느리지만, 소규모 벤치마크 문제당 초 단위. RL/LLM 환경 사례: **VerilogEval, RTLLM, RTLFixer의 공식 채점기**(기능 정확도 pass@k 평가). |
| **상용 (언급만)** | Synopsys **VCS**, Cadence **Xcelium**, Siemens **Questa**: 산업 표준, UVM/SystemVerilog 전체 지원, 고가 좌석 라이선스. 오픈 RL 환경 구축에는 비용상 사실상 불가. |

## 1.2 아키텍처 시뮬레이션

| 항목 | 내용 |
|---|---|
| **gem5** | 역할: cycle-level full-system CPU/SoC 시뮬레이터 (ISA 수준 동작 + 마이크로아키텍처 타이밍). 입출력: 설정(파이썬 스크립트)+바이너리 → 성능 통계(CPI, 캐시 미스, 사이클). 라이선스: **BSD-3-Clause** (https://github.com/gem5/gem5). 실행 비용: 느림 — 벤치마크 1회 분~수 시간 (KIPS~MIPS 수준). RL 환경 사례: **ArchGym(arXiv 2306.08888)이 gem5를 gymnasium 인터페이스로 감싸 ML 기반 아키텍처 DSE 환경화**. |
| **SST** | 역할: 병렬 이산 이벤트 시뮬레이션 프레임워크, 프로세서~인터커넥트~HBM까지 멀티스케일 구성. 라이선스: BSD-3-Clause (https://github.com/sstsimulator). 실행 비용: HPC급 구성에서 시간 단위. RL 사례: 드묾(미확정). |
| **DRAMSim 계열** | DRAMSim3, Ramulator(2), DRAMSys: 메모리 컨트롤러/DRAM 타이밍·에너지 모델. 입력: 메모리 트레이스 → 출력: 지연/대역폭/에너지. 라이선스: DRAMSim3 MIT(미확정), Ramulator2 MIT(미확정). 실행 비용: 트레이스당 초~분. 주로 gem5/SST에 플러그인으로 결합. |

## 1.3 DNN 가속기 모델링 (RL 친화도 최상위 계층)

| 항목 | 내용 |
|---|---|
| **Timeloop / Accelergy** | 역할: DNN 가속기의 매핑(dataflow/타일링) 공간 탐색(Timeloop) + 에너지 추정(Accelergy). 입력: workload(레이어) + 아키텍처 기술 + 매핑 → 출력: 사이클 수, 에너지(액션별 분해). 라이선스: **MIT** (https://github.com/NVlabs/timeloop). 실행 비용: 매핑 1회 평가 초~분. RL 환경 사례: **ArchGym(2306.08888)의 대표 환경 중 하나**로 감싸져 있음. |
| **SCALE-Sim** | 역할: systolic array(TPU류) 사이클 시뮬레이터. 입력: 네트워크 토폴로지 + array 크기/dataflow → 출력: 사이클, utilization, 대역폭 요구량. 라이선스: **MIT** (ARM 공개, https://github.com/ARM-software/SCALE-Sim). 실행 비용: 초~분 — 분석적이어서 RL 에피소드 보상으로 적합. |
| **MAESTRO** | 역할: dataflow 중심 분석적 비용 모델 (성능/에너지/면적). 라이선스: MIT(미확정) (https://github.com/maestro-project). 실행 비용: 밀리초~초. |
| **gem5-Aladdin** | 역할: pre-RTL 가속기를 SoC 맥락에서 모델링 (C → 동적 그래프 → 사이클/에너지/면적 추정). 라이선스: BSD 계열 (https://github.com/harvard-acc/gem5-aladdin). 실행 비용: 분 단위. RL 사례: 드묾. |

## 1.4 물리 설계 (placement / routing) — AI 연구의 주 묘지

| 항목 | 내용 |
|---|---|
| **OpenROAD** | 역할: 오픈소스 RTL-to-GDS 통합 디지털 플로우 (synthesis 제외 배치/CTS/라우팅/검증). 입출력: gate-level netlist + PDK/lib → 배치·라우팅된 레이아웃 + 타이밍/PPA 리포트. 라이선스: **BSD-3-Clause** (https://github.com/The-OpenROAD-Project/OpenROAD). 실행 비용: 중간 규모 블록 배치+라우팅 수 분~수 시간. RL 환경 사례: **Circuit Training이 OpenROAD 기반**, ChiPBench의 end-to-end 평가 엔진, ORFS-agent 등. |
| **OpenLane** | 역할: OpenROAD + Yosys + Magic 등을 묶은 완전 자동 RTL→GDSII 플로우. 라이선스: **Apache-2.0** (https://github.com/The-OpenROAD-Project/OpenLane). 실행 비용: SKY130 소형 디자인 수 분. RL 사례: ChatEDA 계열 에이전트의 executor로 사용. |
| **DREAMPlace** | 역할: GPU 가속 analytical global/detailed placement (ePlace를 PyTorch로). 입출력: netlist → 배치 좌표 + HPWL 등. 라이선스: BSD 계열 permissive (3.0부터, https://github.com/limbo018/DREAMPlace). 실행 비용: CPU 대비 **~30배 가속**(논문 주장, DAC 2019) — GPU에서 대형 디자인도 분 단위. RL/최적화 사례: **AutoDMP의 placement 엔진**, ChiPBench 실험, diffusion placement(2407.12282). |
| **iEDA** | 역할: 중국 주도 오픈소스 EDA 인프라 + RTL-to-GDS 툴체인 (AiEDA: AI-native 라이브러리 포함). 라이선스: **Mulan PSL-2.0** (ASP-DAC 2024 논문, https://github.com/OSCC-Project/iEDA). 실행 비용: OpenROAD 유사(미확정). |
| **상용 (언급만)** | Cadence **Innovus**, Synopsys **Fusion Compiler**: 산업 표준 P&R. 중요한 것은 이 위에 돌아가는 AI 레이어 — **Cadence Cerebrus**(2021, ML 기반 PPA 최적화), **Synopsys DSO.ai**(RL 기반 설계공간 탐색). |

## 1.5 회로 시뮬레이션 (트랜지스터 레벨)

| 항목 | 내용 |
|---|---|
| **ngspice** | 역할: 오픈소스 SPICE (아날로그/혼성신호, 트랜지스터 레벨 정밀 시뮬). 입출력: netlist+모델 → 파형/측정값. 라이선스: **BSD-3-Clause** (http://ngspice.sourceforge.net/). 실행 비용: 트랜지스터 수에 지수적으로 증가 — 수백 트랜지스터 넘어가면 RL 루프 실용성 급감. 소규모 아날로그 셀 최적화 RL에는 사용 사례 있음. |
| **Xyce** | 역할: Sandia의 병렬 대규모 SPICE. 라이선스: **GPL-3.0** (https://github.com/Xyce/Xyce). 실행 비용: MPI 병렬로 ngspice보다 큰 회로 가능하나 여전히 무거움. |
| **FastSPICE (언급만)** | Synopsys PrimeSim/FineSim, Cadence Spectre X: 근사화+파티셔닝으로 SPICE 대비 수백~수천 배 가속. 상용. RL 환경 직접 사용은 비용상 어려움. |

## 1.6 검증 (verification)

- **UVM**: SystemVerilog 기반 표준 검증 방법론. constrained-random testbench + coverage 구동. 상용 시뮬레이터(VCS/Xcelium/Questa) 사실상 필요. 업계 통념상 설계 공수의 **50~70%가 검증**(널리 인용되는 수치, 출처별 상이 — 미확정).
- **Formal (코너케이스)**: SVA(SystemVerilog Assertion) 속성을 수학적으로 증명/반례 탐색 (Synopsys VC Formal, Cadence JasperGold). 시뮬레이션이 못 닿는 코너케이스 커버. 오픈소스로는 SymbiYosys(Yosys 기반, ISC 라이선스).
- **Coverage**: code/functional coverage를 수집해 "무엇을 아직 검증 안 했나"를 정량화. AI 진입점: **coverage 홀에서 test를 자동 생성하는 LLM/RL**이 2024년 이후 활발한 연구 주제 (파트 2.8 참조).

## 1.7 PDK 접근성 — AI 연구에서 실제로 쓰이는 것

| PDK | 노드 | 라이선스/접근성 | AI 연구 사용 실태 |
|---|---|---|---|
| **SkyWater SKY130** | 130nm | **Apache-2.0**, Google 후원 완전 공개, 실제 fab 가능(TinyTapeout, OpenMPW 셔틀) | 오픈소스 플로우의 사실상 표준. tapeout 가능한 유일한 묵직한 오픈 PDK. |
| **GF180MCU** | GlobalFoundries 180nm | Apache-2.0 | SKY130 다음가는 오픈 fab 가능 옵션. |
| **ASAP7** | predictive 7nm | 학술용 물리키트, **비상업 연구 전용**, 실제 fab 불가 | **DREAMPlace/AutoDMP/ChiPBench 등 placement 연구의 주력 벤치 PDK** (최신 노드에 가까운 난이도). |
| **Nangate45** | 45nm (FreePDK45 기반) | 오픈, 제약 적음 | **Circuit Training, ChiPBench, OpenROAD 튜토리얼의 기본 테스트베드**. 규모가 작아 빠른 실험에 적합. |

---

# 파트 2: AI-for-Chip-Design 연구

## 2.1 AlphaChip (Google) — placement RL의 원조

- **핵심 아이디어**: 매크로 placement를 순차 결정 문제(MDP)로 정식화. netlist를 그래프로 인코딩(edge-based GNN), 정책망이 매크로를 하나씩 배치하고, 보상은 wirelength+congestion+density의 프록시 조합. 경험이 쌓일수록(사전학습) 새 블록을 더 빨리 해결.
- **검증된 출처**: 2020 프리프린트 **arXiv 2004.10746**; Nature 2021 (Vol 594, DOI 10.1038/s41586-021-03544-w, https://pubmed.ncbi.nlm.nih.gov/34108699/); 2023 Nature Addendum(사전학습 공개·방어) — https://scalingintelligence.stanford.edu/pubs/gpm/ (논문+addendum 링크 모음).
- **시뮬레이터/데이터**: 상용 EDA 툴 리포트로 최종 보상 산출, Google TPU 블록 데이터 (비공개 — 완전 외부 재현 불가가 논쟁의 핵심).
- **정량 결과**: 6시간 미만에 인간 전문가 수준 이상의 floorplan 생성 (논문 주장); addendum에서는 사전학습이 성능을 더 끌어올리고 다수 TPU 세대의 생산 블록에 사용되었다고 주장.
- **한계/논쟁**: UCSD 진영의 **"The False Dawn"(arXiv 2306.09633, ISPD 2023)**이 공개 벤치에서 simulated annealing·상용 툴이 RL 코드보다 우수하다고 반박. Google은 **"That Chip Has Sailed"(arXiv 2411.10053)**로 재반박(투명성·독립 재현 사례·생산 사용 근거 제시). 교훈: **비공개 데이터 + 프록시 보상 조합은 재현성 논쟁에 취약**하다.

## 2.2 Circuit Training & ChiPBench

- **Circuit Training (Google 오픈소스)**: AlphaChip 방법론의 오픈소스 재구현 — 분산 심층 RL 프레임워크(TF-Agents), OpenROAD 기반 환경, Ariane RISC-V / Nangate45 등 공개 테스트케이스. https://github.com/google-research/circuit_training . 확장성 분석 논문: DAC 2022 (DOI 10.1145/3505170.3511478). 한계: 사전학습 모델은 미공개("training from scratch"만 지원, CT repo FAQ 인용 — 2306.09633에서 확인).
- **ChiPBench (arXiv 2407.15026, 검증 완료)**: placement AI의 **중간 프록시 지표(HPWL 등)가 최종 end-to-end PPA(타이밍·전력·면적)와 상관관계가 약하다**는 것을 OpenROAD end-to-end 플로우로 실증한 벤치마크. 기존 AI placement 알고리즘 6종을 20개 디자인에서 재평가. Environment Foundry 시사점: **보상을 프록시에 두면 오버피팅된다 — end-to-end 보상 파이프라인이 곧 환경의 품질**이다.

## 2.3 AutoDMP & DREAMPlace 기반 방법들

- **AutoDMP** (ISPD 2023, DOI 10.1145/3569052.3578923 — arXiv 버전은 검색으로 확인되지 않음(미확정); NVIDIA+UT Austin, https://developer.nvidia.com/blog/autodmp-optimizes-macro-placement-for-chip-design-with-ai-and-gpus/):
  - 핵심: DREAMPlace(GPU analytical placer)를 엔진으로 쓰고, 그 하이퍼파라미터/초기 조건 공간을 **다목적 베이지안 최적화**로 탐색해 매크로+표준셀 동시 배치. RL이 아니라 BO이지만 "시뮬레이터를 배치해서 대량 병렬 탐색"한다는 점에서 환경 설계의 좋은 선례.
  - 데이터: ISPD 2015/2016 벤치 + ASAP7 현대 디자인. GPU 1대로 수백 후보를 병렬 평가.
  - 정량: 논문에서 상용 툴 및 Nature RL 대비 동급 이상의 PPA를 더 짧은 시간에 달성했다고 보고(세부 수치는 ISPD 논문 본문 참조 — 미확정).
  - 한계: 디자인당 탐색 비용이 여전히 크고, 학습된 정책의 이전(transfer)은 RL류보다 약함.
- **후속**: DAS-MP(arXiv 2505.16445), Chip Placement with Diffusion Models(**arXiv 2407.12282** — RL 대신 guided sampling diffusion으로 placement, 검증 완료) 등 DREAMPlace 계보가 placement AI의 사실상 표준 토대.

## 2.4 MaskPlace, GraphPlanner — 후속 placement 학습

- **MaskPlace (arXiv 2211.13382, NeurIPS 2022, 검증 완료)**:
  - 핵심: placement를 **픽셀 레벨 시각 표현 학습** 문제로 재정식화. 캔버스에 모듈을 하나씩 놓되 position mask로 **겹침 제로를 구조적으로 보장**. 고해상도 캔버스+대규모 행동 공간을 CNN 기반 정책으로 처리.
  - 정량: 기존 RL 대비 **60~90% wirelength 감소, zero overlap**, 수 시간 내 유효 레이아웃 (논문 초록 명시).
  - 한계: 아칙한 벤치(ISPD 2005류) 중심, end-to-end PPA 미평가(ChiPBench가 이후 지적한 바로 그 지점).
- **GraphPlanner** (ACM TODAES 2022, DOI 10.1145/3555804, arXiv 버전 미확인 — 검색 결과 TODAES만 확인):
  - 핵심: variational GCN으로 회로 연결성→물리 wirelength 매핑을 학습하고, 추론으로 floorplan을 직접 생성. 순차 RL이 아니라 **한 번의 그래프 추론**이라 빠름. mixed-size placer와 결합해 후처리.
  - 한계: RL 대비 탐색 능력은 낮고 초기 floorplan 품질에 의존.

## 2.5 RTL 생성 LLM — NVIDIA 진영의 체계적 라인업

| 연구 | arXiv (검증) | 핵심 | 정량 결과 | 한계 |
|---|---|---|---|---|
| **VeriGen** (Thakur et al.) | [2308.00708](https://arxiv.org/abs/2308.00708) | 오픈소스 CodeGen-16B를 Verilog 코퍼스로 파인튜닝 (모델 공개: HF shailja) | fine-tuned CodeGen-16B가 GPT-3.5-turbo 대비 전체 정확도 +1.1%p (초록 명시) | 문제 규모가 HDLBits급, 대형 디자인 일반화 한계 |
| **VerilogEval** (NVIDIA) | [2309.07544](https://arxiv.org/abs/2309.07544) (ICCAD 2023) | HDLBits 156문제, **Icarus Verilog 기반 기능 정확도 자동 채점** 프레임워크 | LLM 생성 합성 문제-코드 쌍으로 SFT 시 성능 개선 시연 (v1의 GPT-4 수치 오류는 v2에서 정정 공지) | 벤치마크 자체는 환경이 아니라 평가기 — RL 보상으로 전환한 것이 후속 연구 |
| **RTLLM** (HKUST) | [2308.05345](https://arxiv.org/abs/2308.05345) (ASP-DAC 2024) | 자연어 명세→design RTL 생성의 오픈 벤치마크 (30개 디자인; RTLLM 2.0은 50개, ICCAD 2024) | GPT 계열 포함 LLM들의 design-level 성능 기준선 제시 | syntax pass와 기능 pass의 괴리 큼 |
| **RTLFixer** (NVIDIA) | [2311.16543](https://arxiv.org/abs/2311.16543) | **RAG + ReAct 프롬프팅으로 LLM 생성 Verilog의 syntax 오류 자동 수정** (컴파일러 에러 메시지를 피드백으로 반복) | LLM 생성 Verilog 오류의 **~55%가 syntax 관련**; VerilogEval 유래 212개 오류 구현 중 **~98.5%의 컴파일 오류 수정** (초록 명시) | syntax만 고침 — 기능(semantic) 오류는 별개 문제 |
| **ChipNeMo** (NVIDIA) | [2311.00176](https://arxiv.org/abs/2311.00176) | LLaMA2의 **도메인 적응 4종 세트**: 도메인 토크나이저, continued pretraining, 도메인 SFT, 도메인 적응 retrieval. 유스케이스: 엔지니어링 챗봇 / EDA 스크립트 생성 / 버그 요약·분석 | **ChipNeMo-70B가 GPT-4를 3개 유스케이스 중 2개(챗봇, EDA 스크립트)에서 상회**, 버그 요약은 대등 (초록 명시) | 모델·데이터 비공개; RTL '설계'가 아니라 생산성 도구 중심 |

- 시사점: 이 라인업의 공통 구조가 곧 RL 환경 설계 패턴이다 — **생성(LLM) → 실행(Icarus/Verilator 채점) → 에러 피드백 → 재생성**. RTLFixer/VerilogEval은 이미 "시뮬레이터를 보상으로 쓰는 루프"의 축소판이다.

## 2.6 ChatEDA & EDA 에이전트 계열

- **ChatEDA (arXiv 2308.10204, TCAD 2024, 검증 완료)**: LLM 컨트롤러(AutoMage)가 작업 계획을 세우고 **EDA 툴을 executor로 호출**해 RTL→GDS 플로우를 자율 운용. "자연어 지시 → 플로우 파라미터/스크립트 생성 → 툴 실행"의 에이전트 패턴 확립. 코드 공개: https://github.com/wuhy68/ChatEDA .
- **계보**: EDAid, ORFS-agent(OpenROAD-flow-scripts 운용 에이전트, Agentic EDA 서베이에 수록), DRC-Coder(멀티에이전트 VLM으로 DRC 체커 코드 생성) 등. 종합 서베이: **"The Dawn of Agentic EDA" (arXiv 2512.23189)** — 자율 디지털 설계 에이전트를 PRT(프롬프트 추론)/SFT/멀티에이전트/파울데이션모델 4축으로 분류.

## 2.7 2024–2026 최신 동향

- **Circuit Foundation Model (CFM)**: 칩 설계 전용 파울데이션 모델 구축 움직임. 종합 서베이 **arXiv 2504.03711** ("A Survey of Circuit Foundation Model", 130+ 작업 커버, 검증 완료). 대표 사례: **AnalogSeeker (arXiv 2508.10409)** — 아날로그 회로 설계용 오픈소스 파울데이션 언어 모델.
- **구글**: AlphaChip addendum(2023) + "That Chip Has Sailed"(2411.10053)로 방어 완료, 생산 TPU 사용 및 외부(MediaTek 등) 확산 주장. Circuit Training은 유지보수 지속.
- **NVIDIA**: ChipNeMo 이후 ChipNeMo-70B 업데이트(v5), AutoDMP 산업 블로그 전개, Synopsys와 Grace Blackwell 기반 EDA 가속 협력 발표(2025, PRNewswire 복수 매체 확인).
- **Synopsys**: **Synopsys.ai Copilot**(2023-11-15 최초 발표 — Microsoft Azure OpenAI 협업, 본지 확인) → 2025-09-03 assistive/creative 기능 확장 발표(고객 워크플로우 "days→hours", 엔지니어 온병닝 30% 단축·생산성 35% 향상 주장 — https://news.synopsys.com/2025-09-03-Synopsys-Announces-Expanding-AI-Capabilities-for-its-Leading-EDA-Solutions). DSO.ai는 RL 기반 설계공간 최적화로 2020년부터 상용.
- **Cadence**: **Cerebrus**(2021, ML 기반 PPA 최적화 — AnandTech 본지 확인), JedAI 플랫폼, Allegro X AI(배치·배선 자동화)로 "AI-driven flow" 상용화.
- **벤치마크 전선 확장**: ChipBench(**arXiv 2601.21448**, 2026 — "AI-aided chip design에서 LLM 성능을 평가하는 next-step 벤치마크", 검증 완료) 등 LLM 에이전트 평가 인프라가 빠르게 표준화 중.

## 2.8 검증(verification) 쪽 AI

- **AssertLLM (arXiv 2402.00386, 검증 완료)**: 설계 스펙 문서 전체를 입력받아 **SVA(SystemVerilog Assertion)를 자동 생성**하는 멀티-LLM 프레임워크. bug avoidance(설계 전)와 bug hunting(검증 중) 양쪽 커버.
- **AssertLLM2 (arXiv 2605.27472, 검증 완료)**: bug-prevention + bug-hunting을 통합한 종합 assertion 생성 벤치마크 (2026).
- **LLM-Aided Testbench & Bug Detection (arXiv 2406.17132)**: GPT-3.5/4로 FSM 디자인의 testbench 생성·버그 탐지 가능성 탐구.
- **방향성**: coverage 홀 분석 → 테스트/어서션 자동 생성 → 시뮬레이션 실행 → coverage 피드백 루프가 verification의 RL/에이전트 환경 구조로 수렴 중. 서베이: CUHK "LLM-Assisted Circuit Verification" (ASP-DAC 2026 강연 자료, https://www.cse.cuhk.edu.hk/~byu/papers/C312-ASPDAC2026-Verif-slides.pdf).

---

# 부록 A: Environment Foundry 관점 종합 — "어떤 시뮬레이터와 데이터가 필요한가"

1. **보상 계층의 선택이 전부다.** ChiPBench(2407.15026)의 교훈: HPWL 프록시 보상은 최종 PPA와 어긋난다. 환경 품질 = 보상의 end-to-end 정도.
2. **실행 비용별 RL 적합성**: ① DNN 가속기 모델링(Timeloop/SCALE-Sim, 초~분) = 에피소드 대량 반복 가능, ArchGym이 선례. ② RTL 시뮬(Icarus/Verilator, 초~분) = 생성-검증 루프의 검증된 표준(VerilogEval/RTLFixer). ③ 물리 설계(OpenROAD/DREAMPlace, 분~시간) = GPU 가속(DREAMPlace) 또는 프록시 보상 계층화 필수, AutoDMP/CT 선례. ④ SPICE(시간~일) = RL 루프 직접 편입 비현실적.
3. **묣로 전체 스택 구축 가능**: SKY130/GF180(fab 가능) 또는 Nangate45/ASAP7(연구용) + OpenLane/OpenROAD/DREAMPlace + Yosys + Verilator/Icarus. 라이선스 벽 없음 — 데이터(실제 디자인 코퍼스, 벤치 넷리스트)가 진짜 해자.
4. **에이전트 패턴의 표준화**: ChatEDA(툴 호출 에이전트), RTLFixer(에러 피드백 루프), ArchGym(gym 인터페이스) — 세 패턴 모두 "시뮬레이터를 환경으로 컴파일"한다는 회사 테제와 정확히 일치한다.

# 부록 B: 검증된 출처 일람

| 항목 | 검증된 ID/URL |
|---|---|
| AlphaChip preprint | arXiv 2004.10746 |
| AlphaChip Nature 2021 | DOI 10.1038/s41586-021-03544-w, https://pubmed.ncbi.nlm.nih.gov/34108699/ |
| AlphaChip addendum 정리 페이지 | https://scalingintelligence.stanford.edu/pubs/gpm/ |
| That Chip Has Sailed (Google 반박) | arXiv 2411.10053 |
| The False Dawn (UCSD 비판) | arXiv 2306.09633 |
| Circuit Training | https://github.com/google-research/circuit_training , DAC 2022 DOI 10.1145/3505170.3511478 |
| ChiPBench | arXiv 2407.15026 |
| AutoDMP | ISPD 2023 DOI 10.1145/3569052.3578923, https://developer.nvidia.com/blog/autodmp-optimizes-macro-placement-for-chip-design-with-ai-and-gpus/ |
| Diffusion placement | arXiv 2407.12282 |
| MaskPlace | arXiv 2211.13382 (NeurIPS 2022) |
| GraphPlanner | ACM TODAES DOI 10.1145/3555804 |
| ArchGym | arXiv 2306.08888 |
| ChipNeMo | arXiv 2311.00176 |
| VerilogEval | arXiv 2309.07544 |
| RTLLM | arXiv 2308.05345 |
| RTLFixer | arXiv 2311.16543 |
| VeriGen | arXiv 2308.00708 |
| ChatEDA | arXiv 2308.10204 |
| Agentic EDA 서베이 | arXiv 2512.23189 |
| Circuit Foundation Model 서베이 | arXiv 2504.03711 |
| AnalogSeeker | arXiv 2508.10409 |
| ChipBench (2026) | arXiv 2601.21448 |
| AssertLLM | arXiv 2402.00386 |
| AssertLLM2 | arXiv 2605.27472 |
| LLM testbench/bug detection | arXiv 2406.17132 |
| Synopsys.ai Copilot 확장 | https://news.synopsys.com/2025-09-03-Synopsys-Announces-Expanding-AI-Capabilities-for-its-Leading-EDA-Solutions |
| Cadence Cerebrus (2021) | https://www.anandtech.com/show/16836/cadence-cerebrus-to-enable-chip-design-with-ml-ppa-optimization-in-hours-not-months |
| iEDA 라이선스 (Mulan PSL-2.0) | ASP-DAC 2024 논문 https://www.cse.cuhk.edu.hk/~byu/papers/C196-ASPDAC2024-iEDA.pdf |

*(미확정) 표기 항목: AutoDMP arXiv 버전 존재 여부, MAESTRO/DRAMSim3 라이선스 세부, DREAMPlace 30배 가속 수치(논문 주장 인용), 검증 공수 50~70% 수치.*
