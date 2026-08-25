# 시뮬레이션 전략과 투자자 지도

> 작성일: 2026-07-23 · 작성: Hermes (Kimi) · 1차 출처 기반 (논문·투자 발표·VC 공개 발언)

## 1. 시뮬레이션 — 상업 플레이어 4종의 접근

| 회사 | 접근 | 규모 | 출처 |
|---|---|---|---|
| **Mechanize** | 'digital office' — 소수의 고품질 RL 환경. 코딩부터. 환경 빌더 연봉 $500K | $9.1M (NFDG·Collison·Dean). Anthropic과 협업 중(2명 소스) | TechCrunch 2025-09 · NYT |
| **AfterQuery** | 'worlds' — 금융·법률·코딩 오프더셸프 세계. SFT 데이터→RL 환경→도메인 벤치마크 3계층. 전문가 ~10만 명 | $30M @ $300M (Altos 리드). **$100M 연환산 매출, 미국 프론티어 랩 전원 고객** | Sacra · Forbes |
| **micro1 'Roots'** | 모의 지주회사 — 금융 서비스·캘린더 관리를 연습하는 가상 기업. "실세계 노이즈가 정확한 테스트에 필요" | $35M @ $500M (01 Advisors). ARR $7M→$50M | Forbes · TechCrunch |
| **Fleet AI** | 엔터프라이즈 SW의 충실한 복제(드롭다운·버벅거림까지). Anthropic·xAI·Jane Street 출신 40명 | $45M @ ~$750M (병도). Sequoia·Menlo·SVA·Bain | YesPress · fleetai.com |

**공통 설계 패턴**: (a) 실패가 싼 방에서 반복 + 결정론적 채점, (b) 예측 불가한 행동도 포착하는 견고한 환경, (c) 벤치마크 출판이 수요 엔진(AfterQuery의 Terminal-Bench·FinanceQA).

## 2. 학계의 시뮬레이션 회사 — 1차 증거

- **TheAgentCompany** (arXiv:2412.14161): 가상 소프트웨어 회사 + LLM 시뮬레이션 동료, 175개 태스크. 최고 모델도 완주 24% — 행정·재무·HR에서 특히 취약. 시뮬레이션 회사가 실제 역량 격차를 노출한다는 증거.
- **Generative Agents** (arXiv:2304.03442): 25명의 기억·반성·계획 에이전트가 신뢰할 만한 집단 행동을 창발.
- **1,000명 시뮬레이션** (arXiv:2411.10109): 2시간 인터뷰로 만든 에이전트가 본인의 2주 후 자기 답변 재현율 대비 **정규화 정확도 0.85**, 사회실험 효과크기 상관 r=0.98 — **calibration의 표준 방법론: 본인 자기일관성 대비 정규화 정확도.**

## 3. 시뮬레이션이 실제를 예측하게 만드는 조건 — 4개의 1차 법칙

1. **결정론적·검증 가능한 보상** (모든 상업 플레이어의 공통 전제; Ross Taylor의 반례: "공개 환경 대부분 수정 없이는 작동 안 함").
2. **변동성 분포가 현실을 덮는다** — Domain Randomization (Tobin 2017, arXiv:1703.06907): 현실을 충실히 모사하는 것보다 변동의 분포가 현실을 포함하는 것이 핵심. 조직 버전: 인원·정책·장애·상대방 유형의 주입.
3. **실제 데이터 피드백 폐루프** — SimOpt (Chebotar 2019, arXiv:1810.05687): 소량의 실제 궤적으로 시뮬레이션 파라미터를 주기적 재보정. 실제 episode가 있어야 calibration이 수렴한다 — **frogstar의 살아있는 episode가 시뮬레이터의 연료**.
4. **calibration의 수치화** — Park et al.의 정규화 정확도 방식: 시뮬레이션 상대방이 실제 사람의 반응을 얼마나 재현하는지 자기일관성 대비로 측정.

**반례 메모**: Sherwin Wu(OpenAI)는 환경 스타트업에 "숏", Karpathy는 "환경엔 강세, RL 자체엔 약세". 시뮬레이터는 검증되기 전까지 판매 문서가 아니라 가설이다 (foundry proof-ladder Gate 6과 일치).

## 4. 투자자 지도 — 누가 얼마를, 어떤 논리로

| 투자자 | 딜 | 논리 |
|---|---|---|
| **NFDG + Collison, Dean, Patel, Douglas** | Mechanize ($9.1M) | "모든 일의 완전 자동화" TAM 베팅 |
| **Sequoia · Menlo · SVA · Bain** | Fleet AI $45M @ ~$750M (병도) | "에이전트가 일하기 전에 일하는 법을 배우는 체육관" |
| **Altos(리드) · Raine · YC · 랩 엔젤들** | AfterQuery $30M @ $300M | $100M run-rate의 속도 베팅 |
| **01 Advisors (Costolo·Bain)** | micro1 $35M @ $500M | 전문가 네트워크 + Roots 시뮬레이션 |
| **Founders Fund · Menlo · Karpathy** | Prime Intellect $15M→$130M @ $1B (병도) | "RL 환경의 Hugging Face" (2,500+ 환경 허브) |
| **a16z (Jennifer Li)** | 카테고리 옵저버 | "모든 빅 랩이 사내 구축 중이지만 서드파티를 찾고 있다" |
| **YC** | AfterQuery·HUD·Idler·Maingen·Traverse 등 | 배치 차원의 반복 펀딩 = 사실상 thesis |
| 수요 앵커 | Anthropic $1B+ 지출 논의 | The Information |

카테고리 프레임: **"Scale AI for environments"** — 데이터 레이블링이 챗봇 시대를 동력화했듯 환경이 에이전트 시대를 동력화한다.

## 5. 이 카테고리 투자자가 묻는 5개 질문과 요구 증거

1. **"랩이 사내에서 만들면 되지 않나?"** → 랩이 못 만드는 것(도메인 전문가 네트워크, 실제 회사 접근권, 한국 기업 환경) + 실제 랩 계약.
2. **"reward hacking과 환경 품질을 어떻게 보증하나?"** → 결정론적 채점기, 전문가 검증 파이프라인, 모델별 성능 계층 실측(Surge 방식), 해킹 감사 루프.
3. **"매출 집중 리스크"** → 소수 랩 집중이 이 카테고리의 숙명. 다년 계약·멀티 도메인·엔터프라이즈 2차 시장으로 완화.
4. **"확장성"** → RL 훈련 컴퓨트는 고비용. run-rate 성장(AfterQuery $100M, micro1 7→50M)이 답.
5. **"방어력"** → 재사용 루브릭·환경 템플릿·도메인 플레이북의 축적 + SOC 2/ISO(엔터프라이즈 조달 게이트).

## 6. 한국·아시아 자본 경로

- **Altos Ventures** — 한국계 미국 VC, 이 카테고리 최대 교두보(AfterQuery 리드). 가장 현실적인 미국 구조 연결.
- **Naver D2SF** — thesis에 "Proprietary Data(버티컬·비정형 전문 데이터)" 명시. 사무실이 NAVER D2SF 안에 있다는 것은 우연이 아니다.
- **SBVA** — 2025년 투자의 44%가 AI, 39%가 미국 집행 — 한·미 크로스오버 성향.
- **Hashed** — 초기 소액 티켓.
- **정책자금** — 국민성장펀드 포함 $1.5B+ 펀드오브펀즈, 2026 상반기 한국 AI 투자 2.685조 원(+485% YoY).
- **현실 경로**: 이 카테고리 표준 라운드는 미국 VC+랩 엔젤 구조. 아시아 자본은 ① Altos 경유 미국 구조 ② D2SF/SBVA 크로스오버 ③ 싱가포르 기반 자본.

## 7. frogstar를 위한 조합 전략

1. **시뮬레이터를 먼저 팔지 않는다** — 판매 단위는 episode+grader 데이터이고, 시뮬레이터는 그 데이터로 보정되는 Gate 6 이후의 상품. SimOpt 루프의 "실제 궤적"이 우리가 갖는 것이다.
2. **투자자 미팅의 증거 순서**: ① 랩이 못 만드는 것(한국 살아있는 회사 접근권 + 권리 아키텍처) ② 결정론적 grader + 해킹 감사 ③ gold trajectory 100개와 난이도 분포 ④ 첫 buyer spec. 이 넷이 "지도"가 아니라 "미팅을 얻는 패키지"다.
3. **엔젤 타겟**: 랩 출신 엔젤(AfterQuery 라운드의 DeepMind/OpenAI/Anthropic 엔젤 패턴) — 연구 신뢰와 buyer 소개를 동시에 준다. 코파욷더 탐색과 같은 풀에서 일어난다.
