# 칩 설계 AI를 위한 데이터 아티팩트 & 공개 데이터셋 조사

- 작성일: 2026-07-29
- 목적: Environment Foundry의 칩 설계 도메인 확장 전략 수립. "AI가 칩을 잘 설계하려면 어떤 데이터가 필요한가?"에 답하고, 각 데이터가 회사의 환경 요건(observation boundary, typed actions, transition, termination, grader, reset/replay, rights/provenance)을 갖추려면 무엇이 필요한지 분석한다.
- 모든 수치는 출처 URL 병기. 확인 불가 수치는 (미확정) 표기.

---

## 파트 1. 설계 단계별 데이터 아티팩트 카탈로그

칩 설계 파이프라인은 spec → 아키텍처 → RTL → 검증 → 합성 → 물리설계 → 테이프아웃 → 실리콘 검증 순으로 진행되며, 각 단계는 고유한 파일/로그/리포트를 생성한다. 민감도는 후반 단계로 갈수록(특히 PDK 종속 데이터와 GDSII) 급격히 높아진다.

### 1.1 Spec / 요구사항 단계

| 항목 | 내용 |
|---|---|
| 아티팩트 | 제품 요구사항 문서(PRD/MRD), ISA 명세, 인터페이스 프로토콜 명세(AMBA AXI/AHB 등), 파워/성능/면적(PPA) 목표치 |
| 형식 | PDF/Word/Confluence, 일부 구조화된 경우 YAML/IP-XACT |
| 일반 크기 | 수십 페이지 텍스트 (미확정) |
| 민감도 | **중간** — 제품 로드맵·시장 전략이 노출될 수 있으나 설계 구현 정보는 적음 |
| AI 활용 | spec→RTL 생성의 입력(LLM 프롬프트). RTLLM이 "natural language instruction → design RTL" 과제로 정형화한 것이 이 경계 (https://arxiv.org/pdf/2308.05345). spec 문서 자체는 거의 공개되지 않아 데이터셋의 가장 큰 공백 지대 |

### 1.2 아키텍처 / 마이크로아키텍처 단계

| 항목 | 내용 |
|---|---|
| 아티팩트 | 블록 다이어그램, 파이프라인 다이어그램, 메모리 맵, C/SystemC 사이클 근사 모델, 성능 시뮬레이션 로그(gem5 등) |
| 형식 | Visio/drawio 다이어그램, C++/SystemC 소스, 시뮬레이션 트레이스(텍스트/JSON) |
| 일반 크기 | 시뮬레이터 소스 수백 KB~수 MB, 트레이스 GB 단위 가능 (미확정) |
| 민감도 | **높음** — 마이크로아키텍처(파이프라인 깊이, 캐시 구조, 스케줄링) 자체가 핵심 IP |
| AI 활용 | 설계 공간 탐색(DSE) 학습 데이터. 공개 사례: RISC-V 기반 Chipyard 생성기 프레임워크(https://github.com/ucb-bar/chipyard)가 아키텍처 파라미터→RTL 컴파일 경로를 제공해 "아키텍처 환경"의 후보가 됨 |

### 1.3 RTL 설계 단계

| 항목 | 내용 |
|---|---|
| 아티팩트 | Verilog/SystemVerilog/VHDL 소스, 패키지/인터페이스 정의, 파라미터화 템플릿, lint 리포트 |
| 형식 | .v/.sv/.vhd 텍스트, lint 로그(텍스트) |
| 일반 크기 | 모듈당 수백 B~수십 KB; SoC 전체 수 MB (미확정) |
| 민감도 | **높음** — RTL은 설계 IP의 원천. 단, 오픈소스 하드웨어(OpenCores, OpenTitan, RISC-V 코어)는 공개 가능 |
| AI 활용 | 가장 데이터가 풍부한 단계. 코드 생성 학습(RTLCoder-Data 80K instruction-code 샘플, https://zhiyaoxie.com/files/ICCAD24_OpenLLM.pdf), 코드 완성(RTL-Repo), 합성 지표 예측(MetRex 25,868 모듈, https://github.com/scale-lab/MetRex) |

### 1.4 검증(Verification) 단계

| 항목 | 내용 |
|---|---|
| 아티팩트 | UVM 테스트벤치, 테스트케이스, 어설션(SVA), 커버리지 리포트(functional/code coverage), 시뮬레이션 로그, 파형(FSDB/VCD), 버그 리포트 |
| 형식 | SystemVerilog/UVM 소스, 텍스트 로그, VCD/FSDB 바이너리 파형, UCIS 커버리지 DB |
| 일반 크기 | 파형은 GB~TB 단위 가능 (미확정); 커버리지 DB 수백 MB (미확정) |
| 민감도 | **중간~높음** — 테스트벤치는 RTL 구조를 간접 노출; 버그 리포트는 설계 약점 정보 |
| AI 활용 | 어설션 생성(RTLLM 2.0의 FPV용 어설션 생성 벤치마크, https://github.com/hkust-zhiyao/RTLLM), 테스트 생성, 커버리지 클로저 예측. 검증은 전체 설계 공수의 과반을 차지한다고 널리 알려짐(업계 통례, 미확정 수치)에도 공개 데이터셋이 극히 적은 공백 지대 |

### 1.5 논리합성(Synthesis) 단계

| 항목 | 내용 |
|---|---|
| 아티팩트 | 게이트 레벨 넷리스트, 합성 스크립트(recipe), 타이밍/면적/파워 리포트(QoR), AIG/기술 매핑 결과 |
| 형식 | .v(게이트 넷리스트), .tcl 스크립트, .rpt 텍스트 리포트, .aig/.bench |
| 일반 크기 | 디자인당 넷리스트 수 MB~수백 MB (미확정) |
| 민감도 | **중간** — 넷리스트는 역공학 가능하나 RTL보다 정보 밀도 낮음. PDK 라이브러리(Nangate 45nm 등 공개 PDK 사용 시) 종속 |
| AI 활용 | **가장 성숙한 공개 데이터 단계.** OpenABC-D: 29개 오픈소스 IP × 1,500개 합성 recipe = 870,000 샘플 (https://github.com/NYU-MLDA/OpenABC, https://animeshbchowdhury.gitlab.io/papers/2021_OpenABCD.pdf). 합성 recipe 최적화는 상태전이가 명확해 RL 환경화에 유리 |

### 1.6 물리설계(Physical Design) 단계

| 항목 | 내용 |
|---|---|
| 아티팩트 | 플로어플랜/배치(DEF), 배선 결과, 혼잡도(congestion) 맵, DRC 위반 리포트, IR drop 맵, STA 리포트, LEF/DEF/Liberty |
| 형식 | .def/.lef/.lib/.sdc 텍스트, 혼잡도/IR 맵(그리드 행렬/이미지), 리포트 텍스트 |
| 일반 크기 | 디자인당 DEF 수백 MB 가능 (미확정); CircuitNet은 샘플당 feature map 세트로 구성 |
| 민감도 | **매우 높음** — 상용 PDK(TSMC N7 등) 기반 데이터는 NDA로 묶임. 공개 데이터는 사실상 Nangate45/SKY130/ASAP7 등 오픈 PDK로 제한됨 |
| AI 활용 | CircuitNet: 혼잡도/DRC/IR drop 예측용 최초의 오픈소스 데이터셋 (https://github.com/circuitnet/CircuitNet, http://scis.scichina.com/en/2022/227401.pdf). ChiPBench/ChiPBench-D: DEF/LEF/Liberty/Verilog/SDC 표준 포맷의 배치 벤치마크 데이터셋 (https://huggingface.co/datasets/MIRA-Lab/ChiPBench-D, https://arxiv.org/html/2407.15026v1) |

### 1.7 테이프아웃 단계

| 항목 | 내용 |
|---|---|
| 아티팩트 | GDSII/OASIS 최종 레이아웃, LVS/DRC 최종 signoff 리포트, DFM 리포트, 넷리스트-레이아웃 대조 결과 |
| 형식 | .gds/.oas 바이너리, signoff 리포트 |
| 일반 크기 | GDS는 수백 MB~수 GB (미확정) |
| 민감도 | **극히 높음** — GDS는 칩 전체의 완전한 청사진. 파운드리 PDK NDA + 설계 IP 이중 민감 |
| AI 활용 | 공개 데이터 사실상 전무. 오픈소스 shuttle(Google/efabless SKY130 MPW)의 GDS 일부가 공개되어 있으나 규모 작음 (미확정) |

### 1.8 실리콘 검증(Post-silicon) 단계

| 항목 | 내용 |
|---|---|
| 아티팩트 | 테스터(ATE) 로그, shmoo plot, 수율 데이터, fail bin 분석, 리베그(ring-back)/디버그 로그 |
| 형식 | STDF(Standard Test Data Format) 바이너리, CSV, 이미지 |
| 일반 크기 | STDF는 로트당 GB 단위 가능 (미확정) |
| 민감도 | **극히 높음** — 수율·결함 데이터는 제조 역량의 핵심 기밀 |
| AI 활용 | 공개 데이터셋 사실상 없음. pre-silicon과의 상관관계 분석 수요는 크나 데이터 장벽이 가장 높은 단계 |

### 1.9 단계별 요약: 데이터 가용성 지도

```
공개 데이터 풍부 ◀──────────────────────────────▶ 공개 데이터 전무
 [합성][RTL][물리설계-오픈PDK]   [검증][spec][아키텍처]   [테이프아웃][실리콘]
민감도 낮음 ◀────────────────────────────────────────▶ 민감도 극심
```

Environment Foundry 관점 함의: **합성~물리설계(오픈 PDK) 구간**은 데이터와 툴(오픈소스 EDA)이 모두 공개되어 있어 환경화의 진입점으로 최적. spec/검증/실리콘 구간은 데이터를 직접 생성(합성 데이터 또는 고객 협업)해야 한다.

---

## 파트 2. 공개 데이터셋 전수 조사

### 2.1 합성(Synthesis) 단계

#### OpenABC-D
- **규모**: 29개 오픈소스 하드웨어 IP × 1,500개 합성 recipe = 870,000 데이터 샘플
- **내용**: 원본/합성 .bench 파일, 기술 매핑 후 로그 리포트, GraphML 그래프, PyTorch-Geometric 호환 데이터, Nangate 15nm 라이브러리, AIG 통계(면적/지연/노드 수/깊이), 디자인별 맞춤 합성 스크립트 1,500개
- **라이선스**: GitHub 저장소 공개 (https://github.com/NYU-MLDA/OpenABC); 개별 IP의 라이선스는 원저작권자 규정을 따라야 함
- **다운로드**: GitHub README의 링크 경유 (NYU 호스팅, https://ultraviolet.library.nyu.edu/records/mw6q2-a8p15)
- **한계**: 29개 IP로 다양성 제한; yosys-abc 오픈소스 툴체인 결과라 상용 합성기 QoR과 갭; AIG 중심이라 상위 RTL 맥락 부재
- 출처: https://animeshbchowdhury.gitlab.io/papers/2021_OpenABCD.pdf, https://arxiv.org/pdf/2310.10560

### 2.2 물리설계 단계

#### CircuitNet
- **규모**: RISC-V 디자인 기반 다수 샘플 (구체적 샘플 수 미확정; 버전별 상이)
- **내용**: 혼잡도(congestion), DRC 위반, IR drop 예측용 feature map과 레이블. 백엔드 설계의 cross-stage 예측 태스크 지원
- **라이선스**: 오픈소스 (GitHub 공개)
- **다운로드**: https://github.com/circuitnet/CircuitNet (데이터 링크 저장소 내 안내), 튜토리얼 https://circuitnet.github.io/tutorial/experiment_tutorial.html
- **한계**: 오픈 PDK 기반이라 상용 노드 일반화 불가; 예측 태스크(지도학습)용이지 의사결정(환경)용이 아님
- 출처: http://scis.scichina.com/en/2022/227401.pdf, https://ar5iv.labs.arxiv.org/html/2208.01040

#### ChiPBench / ChiPBench-D (2024, NeurIPS 2025 poster)
- **규모**: 20개 디자인(미확정), DEF/LEF/Liberty/Verilog/SDC 표준 포맷
- **내용**: AI 배치(placement) 알고리즘의 **최종 PPA 기준 종단간 평가**를 위한 벤치마크. 중간 프록시 지표가 아닌 전체 플로 실행 결과로 채점하도록 설계
- **라이선스**: HuggingFace 공개 (https://huggingface.co/datasets/MIRA-Lab/ChiPBench-D)
- **다운로드**: HuggingFace datasets
- **한계**: 배치 단계 특화; 평가에 상용 EDA 플로 필요(완전 오픈소스 재현 제약)
- 출처: https://arxiv.org/html/2407.15026v1, https://openreview.net/forum?id=gDkQ5iesrI

#### Google Circuit Training (AlphaChip)
- **규모**: 프레임워크 + 사전학습 체크포인트 공개; Ariane RISC-V 적용 예제 포함
- **내용**: 분산 심층 RL로 칩 플로어플랜/매크로 배치를 생성하는 **환경 그 자체** (netlist+canvas → 배치 액션 → 코스트 함수). 데이터셋이라기보다 RL 환경의 공개 레퍼런스
- **라이선스**: Apache-2.0 (미확정 — GitHub 라이선스 파일 확인 필요)
- **다운로드**: https://github.com/google-research/circuit_training
- **한계**: "An Updated Assessment of RL for Chip Placement"(https://arxiv.org/html/2302.11014v3) 등 재현성 논쟁 존재; 나이 버전 의존성 이슈
- 출처: https://github.com/google-research/circuit_training

#### ORFS (OpenROAD-flow-scripts) 공개 결과물
- **규모**: 16개 내장 샘플 디자인(nangate45/aes 등) + 다중 PDK(sky130hd, nangate45, asap7 등) (https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/discussions/2238)
- **내용**: 완전 자율 RTL→GDSII 플로. 실행 시 디자인별 logs/objects/reports/results 디렉토리에 합성~라우팅 전 단계의 리포트와 중간 산출물 생성 (https://github.com/The-OpenROAD-Project/OpenROAD-flow-scripts/blob/master/docs/tutorials/FlowTutorial.md)
- **라이선스**: 오픈소스 (BSD 계열, 미확정)
- **다운로드**: https://github.com/the-openroad-project/openroad-flow-scripts
- **한계**: 데이터셋이 아니라 **생성 인프라** — 데이터가 필요하면 직접 플로를 돌려 만들어야 함. 오히려 이 점이 환경 구축에는 강점(아래 파트 3)
- 출처: https://openroad-flow-scripts.readthedocs.io/

### 2.3 RTL 코드 생성/평가 데이터셋

#### VerilogEval / VerilogEval v2 (NVIDIA, 2023–2024)
- **규모**: v1 156 문제(HDLBits 출처); v2는 코드 완성 + spec-to-RTL 태스크 지원
- **내용**: Verilog 코드 생성 평가 벤치마크. Makefile 기반 평가 인프라(시뮬레이션 pass/fail 자동 채점)
- **라이선스**: 오픈 (GitHub/HuggingFace); NTU 패치본 https://huggingface.co/datasets/AS-SiliconMind/VerilogEval-v2-NTU
- **다운로드**: GitHub (NVlabs) — 검색 결과 상 경로 미확정, v2 논문 https://arxiv.org/html/2408.11053v2
- **한계**: HDLBits 유사 교육용 소형 문제 위주 — 실제 설계 복잡도와 갭. 테스트 데이터 오염 가능성 지적됨
- 출처: https://huggingface.co/papers/2309.07544, https://dl.acm.org/doi/10.1145/3718088

#### RTLLM / RTLLM 2.0 (HKUST, 2024)
- **규모**: v1 30개 → v2 50개 디자인
- **내용**: 자연어 instruction → design RTL 생성 벤치마크. 디자인별 spec 문서, 골든 RTL, 테스트벤치, (v2) FPV용 어설션 생성 태스크 포함
- **라이선스**: 오픈소스 (GitHub)
- **다운로드**: https://github.com/hkust-zhiyao/RTLLM
- **한계**: 50개로 규모 작음; pass/fail 채점은 제공되나 부분 점수(grader granularity) 없음
- 출처: https://arxiv.org/pdf/2308.05345, https://dl.acm.org/doi/10.1109/ASP-DAC58780.2024.10473904

#### RTLCoder-Data / OpenLLM-RTL (HKUST, ICCAD 2024)
- **규모**: 80K raw instruction-code 샘플 + 7K 검증된 고품질 샘플
- **내용**: 자동화된 데이터 생성 플로(GPT 기반 instruction 생성 + 기능 검증)로 만든 RTL 학습 데이터. 다양성 지표(CR, CR:POS) 공개
- **라이선스**: 오픈소스
- **다운로드**: https://github.com/hkust-zhiyao/RTL-Coder (`dataset/`, `data_generation/` 폴)
- **한계**: GPT 합성 데이터 — GPT 스타일 편향, 오류 패턴이 생성기를 닮음; 80K raw는 미검증
- 출처: https://zhiyaoxie.com/files/ICCAD24_OpenLLM.pdf, https://arxiv.org/html/2312.08617v4

#### 기타 RTL 계열 (요약)
| 데이터셋 | 규모 | 특징 | 출처 |
|---|---|---|---|
| RTL-Repo | 대규모 실제 RTL 프로젝트 | GitHub 실제 프로젝트 기반 코드 완성(레포 수준 컨텍스트) | https://arxiv.org/abs/2405.17378 (OpenLLM-RTL 논문 인용) |
| MG-Verilog | 11,000+ 샘플 (미확정) | 다중 세분도 자연어 설명-코드 쌍 | https://arxiv.org/abs/2407.01910, https://responsible.computing.gatech.edu/mg-verilog-won-the-best-paper-award-at-the-first-workshop-on-llm-aided-design/ |
| Goh et al. labelled Verilog | 68,122 엔트리 | 모듈 + LLM 생성 설명 | https://dl.acm.org/doi/full/10.1145/3736167 |
| MetRex | 25,868 디자인 | Verilog + 합성 후 지표(면적/지연/정적파워) + 자연어 추론 템플릿 | https://github.com/scale-lab/MetRex, https://arxiv.org/pdf/2411.03471 |
| OriGen | 코드-투-코드 증강 | self-reflection 기반 RTL 생성 개선 | https://arxiv.org/abs/2409 (ICCAD24 인용, arXiv 2409 계열, 미확정) |
| CVDP (NVIDIA, 2025) | 783 문제, 13개 태스크 카테고리 | RTL 생성+검증+디버깅+명세 정합성+Q&A, 전문가 작성, 에이전트 평가 인프라 | https://arxiv.org/html/2506.14074v1, https://openreview.net/forum?id=Xobl2VHyVb |
| CraftRTL (NVIDIA) | 합성 데이터 생성기 | correct-by-construction 비텍스트 표현 + targeted code repair | https://www.researchgate.net/publication/384245633 |
| EDA Corpus | OpenROAD 상호작용 특화 | EDA 툴 사용 대화/스크립트 데이터 | https://github.com/Thinklab-SJTU/Awesome-LLM4EDA (21번 항목) |

### 2.4 전통 벤치마크 & 오픈소스 IP

#### OpenCores
- **규모**: 수백 개 오픈소스 IP 프로젝트 (정확한 수 미확정)
- **내용**: 프로세서, 인터페이스, 암호화 코어 등의 RTL(Verilog/VHDL) + 일부 테스트벤치
- **라이선스**: 프로젝트별 상이 (GPL/LGPL/BSD 등) — **사용 시 개별 확인 필수**
- **다운로드**: https://opencores.org
- **한계**: 품질 편차 큼, 검증 수준 불균일, 문서 부실한 프로젝트 다수
- 출처: IWLS 2005 벤치마크가 OpenCores 출처 디자인을 다수 포함 (https://ddd.fit.cvut.cz/www/prj/Benchmarks/)

#### Chipyard (UC Berkeley)
- **규모**: RISC-V SoC 생성 프레임워크 (Rocket, BOOM 등 코어 생성기 포함)
- **내용**: 파라미터화된 Chisel 생성기 → RTL 컴파일 + 시뮬레이션 + VLSI 플로(Hammer) 통합
- **라이선스**: BSD-3-Clause (미확정)
- **다운로드**: https://github.com/ucb-bar/chipyard
- **한계**: 생성기 프레임워크라 "데이터셋"이 아니라 "데이터 팩토리" — 학습 코퍼스로 쓰려면 파라미터 스윕 실행 필요
- 출처: https://github.com/ucb-bar/chipyard

#### EPFL Combinational Benchmark Suite
- **규모**: 23개 네이티브 조합 회로 (산술 10개 + random/control + MtM)
- **내용**: Verilog/VHDL/BLIF/AIGER 4종 포맷으로 배포되는 로직 최적화 챌린지 회로
- **라이선스**: 오픈 (Zenodo 배포)
- **다운로드**: https://github.com/lsils/benchmarks, https://zenodo.org/records/2572934
- **한계**: 조합 회로만, 순차 회로·시스템 수준 없음. 로직 합성 알고리즘 평가용
- 출처: https://www.epfl.ch/labs/lsi/page-102566-en-html/benchmarks/

#### IWLS 2005 Benchmarks
- **규모**: 84개 디자인, 최대 185,000 레지스터 / 900,000 게이트
- **내용**: ISCAS/ITC/OpenCores 출처 회로를 Verilog/VHDL/BLIF로 수집
- **라이선스**: 학술 사용 목적 공개 (개별 원저작권 유의)
- **다운로드**: https://iwls.org/iwls2005/benchmarks.html, 미러 https://ddd.fit.cvut.cz/www/prj/Benchmarks/
- **한계**: 2005년 데이터라 현대 디자인 스타일(SoC, NoC, 저전력 기법) 미반영
- 출처: https://iwls.org/iwls2005/benchmarks.html

### 2.5 ChipGPT / 중국 계열 및 기타

#### ChipGPT-FT (aichipdesign, DAC 2024)
- **규모**: 자동화 데이터 증강 프레임워크로 생성한 Verilog-자연어 정렬 데이터 (정확한 샘플 수 미확정)
- **내용**: "Data is all you need" — Verilog AST 증강 기반 고품질 instruction-code 데이터 생성 + EDA 스크립트
- **라이선스**: GitHub 공개
- **다운로드**: https://github.com/aichipdesign/chipgptft
- **한계**: 합성 데이터 의존, 벤치마크 외 일반화 검증 제한
- 출처: https://arxiv.org/pdf/2403.11202, https://dl.acm.org/doi/10.1145/3649329.3657356

#### QiMeng (중국과학원) — "Tianhe-LLM" 계열 언급의 유력 후보
- "Tianhe-LLM"이라는 정확한 명칭의 칩 설계 데이터셋은 확인되지 않음 (미확정). 유사 맥락에서 중국과학원의 QiMeng 프로젝트(LLM 기반 전자동 CPU 설계, "세계 최초 AI 설계 프로세서" 주장)가 오픈소스 full-stack 칩 설계 프로젝트로 병행 공개됨
- 출처: https://www.tomshardware.com/pc-components/cpus/china-claims-to-have-developed-the-worlds-first-ai-designed-processor-llm-turned-performance-requests-into-cpu-architecture
- **한계**: 주장의 독립 검증 부족, 데이터셋 형태의 공개 여부 불명확 (미확정)

#### ACE-RTL (2026)
- CVDP 기반 agentic context evolution 접근, 14개 베이스라인 대비 최대 44.87% pass rate 개선 보고 — 2026년 시점 에이전트 평가의 최신 레퍼런스
- 출처: https://arxiv.org/html/2602.10218v1

---

## 파트 3. '데이터'에서 '환경'으로 — 갭 분석

Environment Foundry의 환경 요건: ① observation boundary ② typed actions ③ transition behavior ④ termination ⑤ grader ⑥ reset/replay semantics ⑦ rights/provenance.

### 3.1 요걸별 평가 프레임

| 환경 요건 | 정적 데이터셋이 제공하는 것 | 환경이 되기 위해 추가로 필요한 것 |
|---|---|---|
| observation boundary | 입력 파일 자체(spec, RTL, netlist) | 에이전트가 "무엇을 볼 수 있는가"의 명시적 컷 — 전체 파일 vs 요약 리포트 vs 파싱된 지표. 관측 스키마 정의 필요 |
| typed actions | 없음 (데이터는 수동적) | 액션 타입 정의: `edit_rtl(hunk)`, `set_synthesis_recipe(list)`, `run_tool(cmd)`, `place_macro(id,x,y)` 등 |
| transition behavior | 없음 | **시뮬레이터/툴 실행이 곧 transition.** 합성기, 시뮬레이터, STA 등 외부 툴이 상태전이 함수 역할 |
| termination | 없음 | 종료 조건: pass/fail 도달, 리소스(스텝/시간/토큰) 소진, QoR 목표 달성 |
| grader | 일부 (골든 RTL, 테스트벤치, QoR 레이블) | 부분 점수·다목적 점수(기능 정확성 × PPA)로의 확장, 채점 자동화 하네스 |
| reset/replay | 데이터 자체는 결정적 | 툴 실행의 결정성 확보(버전 고정, 시드 고정), 캐시/체크포인트, 컨테이너화 |
| rights/provenance | 라이선스 문서 | IP 계보 추적(원본 IP → 파생 데이터 → 학습 산출물), PDK NDA 분리, 재배포 가능 여부 감사 |

### 3.2 아티팩트/데이터셋별 환경화 난이도

| 데이터 | observation | actions | transition | termination | grader | reset/replay | rights | **환경화 판정** |
|---|---|---|---|---|---|---|---|---|
| OpenABC-D | ✅ 그래프+통계 | △ recipe 선택 액션으로 정의 가능 | ❌ **yosys-abc 재실행 필요** | △ recipe 길이 고정 | ✅ QoR 레이블 | ✅ 툴 오픈소스 | ✅ 공개 IP | **중간** — 오프라인 RL(로그 기반)은 바로 가능, 온라인 환경은 합성기 부착 필요 |
| CircuitNet | ✅ feature map | ❌ 없음 | ❌ **물리설계 툴 필요** | ❌ | ✅ 맵 레이블 | ✅ | ✅ | **낮음(예측 과제)** — 지도학습 데이터일 뿐, 액션 공간이 정의되지 않아 그 자체로 환경 불가 |
| ChiPBench-D | ✅ 표준 파일 | △ 배치 액션 | △ 플로 실행 | ✅ PPA 목표 | ✅ 종단 PPA | △ 상용 툴 의존 | ✅ HF 공개 | **중상** — 종단 채점 설계가 grader 요건에 부합 |
| Circuit Training | ✅ | ✅ 배치 액션 | ✅ 내장 시뮬 | ✅ | ✅ 코스트 함수 | ✅ | ✅ Apache | **이미 환경** — 유일하게 7요건을 거의 충족하는 공개 레퍼런스 |
| VerilogEval/RTLLM | ✅ spec | △ 코드 생성 1스텝 | ✅ 시뮬레이터(iverilog/VCS) | ✅ pass/fail | ✅ 테스트벤치 | ✅ | ✅ | **상(1스텝 환경)** — 단, 에피소드가 1액션이라 "환경"이라기보다 "채점기 붙은 태스크". 멀티스텝화(디버깅 루프)가 환경화의 핵심 |
| RTLCoder-Data/MG-Verilog | ✅ | ❌ | ❌ | ❌ | △ 골든 코드 | ✅ | △ GPT 합성 데이터 provenance 이슈 | **낮음** — SFT 코퍼스이지 환경 아님. 환경화하려면 샘플별 테스트벤치 자동 생성 필요 |
| ORFS | ✅ 리포트/로그 | ✅ tcl/config 액션 | ✅ 실제 툴체인 | ✅ 플로 완료/실패 | ✅ QoR 리포트 | ✅ 컨테이너 | ✅ 오픈 PDK | **최상의 환경 기반** — 데이터가 아니라 실행 가능한 플로 자체가 transition engine. 파트1의 "합성~물리설계 구간이 진입점" 결론의 근거 |
| Chipyard | ✅ | ✅ 아키텍처 파라미터 | ✅ 생성기+시뮬레이터 | ✅ | △ (성능 측정 별도 구성) | ✅ | ✅ BSD | **상** — 아키텍처 DSE 환경의 직접적 후보 |
| EPFL/IWLS 벤치마크 | ✅ 회로 | △ 최적화 명령 시퀀스 | ❌ **abc 등 툴 부착 필요** | △ | ✅ QoR | ✅ | ✅ | **중간** — OpenABC-D와 같은 방식으로 환경화된 선례 존재 |
| spec/검증/실리콘 데이터 | ❌ 공백 | — | — | — | — | — | ❌ NDA | **해당 없음** — 데이터 자체가 없어 합성 생성 또는 고객 협업 필요 |

### 3.3 핵심 판별: 시뮬레이터가 반드시 붙어야 하는가?

**그렇다. 정적 데이터만으로는 환경이 성립하지 않으며, transition function = 툴 실행이다.** 세 가지 유형으로 분류된다:

1. **로그 재생형(오프라인 RL 가능)**: OpenABC-D처럼 (상태, 액션, 결과) 튜플이 이미 기록된 데이터는 시뮬레이터 없이 model-based/오프라인 학습 가능. 단, **데이터에 없는 액션을 취할 수 없어** 탐색이 데이터 분포에 갇힘. 진정한 환경이 되려면 결국 yosys-abc를 다시 붙여야 함.
2. **예측 과제형(환경 불가)**: CircuitNet, MetRex는 입력→레이블 매핑일 뿐 액션과 상태전이가 없다. 이들은 환경의 **grader를 학습하는 서로게이트 모델** 재료로는 유용(예: 실제 P&R 대신 혼잡도 예측 모델로 빠른 보상 계산)하나 환경 그 자체는 아님.
3. **실행 인프라형(즉시 환경 후보)**: ORFS, Circuit Training, Chipyard는 툴체인 자체가 공개되어 transition을 실제로 계산할 수 있다. **칩 설계 도메인에서 "환경 = 오픈소스 EDA 툴체인 + 태스크 정의 + 채점기"이며, 데이터셋은 그 위의 에피소드 시드 역할**을 한다.

### 3.4 Environment Foundry를 위한 시사점

1. **진입점**: ORFS + 오픈 PDK(sky130/nangate45/asap7) + 공개 IP(OpenCores/IWLS/Chipyard 생성물) 조합이 7요건을 모두 충족할 수 있는 유일한 완전 공개 스택. Circuit Training이 선례.
2. **grader 차별화 기회**: 기존 벤치마크(VerilogEval, RTLLM)는 pass/fail 이진 채점. PPA 다목적 점수 + 부분 점수 + 종단(종단간 PPA, ChiPBench 방식) 채점을 환경 표준으로 만들면 벤치마크 대비 우위.
3. **공백 시장**: spec 단계 데이터, 검증(UVM/어설션) 환경, 실리콘 상관관계 데이터는 공개 자산이 거의 없다. 고객의 사내 이벤트/로그를 환경으로 컴파일한다는 회사 모델과 정확히 맞닿는 지점 — 단, PDK NDA와 IP 계보(rights/provenance) 관리가 계약의 핵심 조항이 되어야 함.
4. **rights 파이프라인 필수**: OpenCores의 프로젝트별 라이선스 혼재, GPT 합성 데이터(RTLCoder, ChipGPT-FT)의 provenance 불명확성은 학습 산출물의 라이선스 오염 리스크. 환경에 번들되는 모든 데이터에 대해 원천 IP → 파생물 계보 추적이 요건 ⑦의 실무적 내용이 된다.

---

## 부록. 주요 출처 일람

- OpenABC-D: https://github.com/NYU-MLDA/OpenABC / https://animeshbchowdhury.gitlab.io/papers/2021_OpenABCD.pdf
- CircuitNet: https://github.com/circuitnet/CircuitNet / http://scis.scichina.com/en/2022/227401.pdf
- ChiPBench: https://arxiv.org/html/2407.15026v1 / https://huggingface.co/datasets/MIRA-Lab/ChiPBench-D
- Circuit Training: https://github.com/google-research/circuit_training
- ORFS: https://github.com/the-openroad-project/openroad-flow-scripts / https://openroad-flow-scripts.readthedocs.io/
- VerilogEval: https://huggingface.co/papers/2309.07544 / https://arxiv.org/html/2408.11053v2
- RTLLM: https://github.com/hkust-zhiyao/RTLLM / https://arxiv.org/pdf/2308.05345
- RTLCoder/OpenLLM-RTL: https://github.com/hkust-zhiyao/RTL-Coder / https://zhiyaoxie.com/files/ICCAD24_OpenLLM.pdf
- MetRex: https://github.com/scale-lab/MetRex / https://arxiv.org/pdf/2411.03471
- CVDP: https://arxiv.org/html/2506.14074v1
- ChipGPT-FT: https://github.com/aichipdesign/chipgptft / https://arxiv.org/pdf/2403.11202
- EPFL Benchmarks: https://github.com/lsils/benchmarks / https://zenodo.org/records/2572934
- IWLS 2005: https://iwls.org/iwls2005/benchmarks.html
- Chipyard: https://github.com/ucb-bar/chipyard
- Awesome-LLM4EDA (종합 목록): https://github.com/Thinklab-SJTU/Awesome-LLM4EDA
- LLM4EDA 서베이: https://dl.acm.org/doi/full/10.1145/3736167 / https://arxiv.org/html/2501.09655v1
