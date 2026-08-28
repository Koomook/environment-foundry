# 벤치마크 점수와 모델 성능을 실제로 올리는 데이터 — 실전 리서치

작성: 2026-07-23 / 대상: Morphospace(Environment Foundry) 사업 설계
원칙: 모든 주장에 2024–2026 1차 출처(논문/랩 블로그) URL 첨부. 범위 밖 기초 문헌(InstructGPT 등)은 최소화.

---

## 1. 학습 데이터 유형 7종: 입력 / 출력 / 한계 / 1차 출처

### 1.1 SFT trace (시연·추론 궤적 모사)
- **입력**: (프롬프트, 고품질 완성) 쌍. 최신 레시피는 강한 교사 모델(R1, o1급)의 **장문 추론 trace를 distill**하고 정답 검증으로 필터링.
- **출력**: 모방 학습된 정책. 벤치마크 상승은 빠르고 저렴하지만, 상한은 교사+베이스 모델에 묶임.
- **한계**: ① 분포 밖 일반화가 약함 — SWE-RL 논문에서 같은 시드 데이터로 SFT한 모델은 OOD 태스크에서 **평균 성능이 오히려 하락**한 반면 RL 모델은 상승 (arXiv:2502.18449, https://arxiv.org/abs/2502.18449). ② "SFT는 암기, RL은 일반화" 계열 실험과 일치. ③ trace 품질=교사 품질; 검증 없이 distill하면 오류도 복제됨.
- **1차 출처**:
  - s1 (1,000개 trace SFT): https://arxiv.org/abs/2501.19393
  - OpenThoughts (114k→1.2M trace, 검증 파이프라인): https://arxiv.org/abs/2506.04178 , 데이터 카드 https://huggingface.co/datasets/open-thoughts/OpenThoughts-114k
  - Tülu 3 (SFT 939k + preference + RLVR 4단계 완전 공개 레시피): https://allenai.org/blog/tulu-3-technical , https://arxiv.org/abs/2411.15124

### 1.2 Preference data (선호도 쌍 → DPO/보상모델)
- **입력**: (프롬프트, chosen, rejected) 쌍 — 인간 라벨, AI 피드백(RLAIF), 또는 온폴리시 샘플링+자동 채점으로 생성.
- **출력**: 선호 정렬된 정책(DPO) 또는 보상모델(RM). 도움됨·무해·스타일 등 **정답이 없는 차원**을 다루는 주 수단.
- **한계**: ① 오프폴리시 데이터는 정책이 변하면 금방 stale — Tülu 3는 온폴리시 선호 데이터가 우수함을 실증 (위 블로그의 preference 섹션). ② 보상 과적합/과최적화(Goodhart): RM 프록시를 과도하게 최적화하면 실제 선호는 하락. ③ "어떤 일을 잘했는가"가 아니라 "어떻게 말하는가"를 주로 가르침 → 추론 능력 자체 향상에는 RLVR보다 약함.
- **1차 출처**:
  - Tülu 3 DPO 온/오프폴리시 실험: https://allenai.org/blog/tulu-3-technical
  - UltraFeedback (AI 피드백 선호 데이터셋 대중화): https://arxiv.org/abs/2310.01377
  - RLAIF / Constitutional AI (AI 피드백으로 인간 라벨 대체): https://arxiv.org/abs/2212.08073
  - HelpSteer2 (멀티속성 인간 선호 1만 건 → RewardBench SOTA급 오픈 RM): https://arxiv.org/abs/2406.08673

### 1.3 Verifier / Process Reward Model (단계별 채점기)
- **입력**: (문제, 중간 추론 단계, 단계별 정오 라벨). PRM800K는 인간 라벨 80만 개, Math-Shepherd는 MC 샘플링으로 자동 라벨.
- **출력**: 단계 단위 점수 → Best-of-N 재순위, 가이드 서치, 또는 RL의 dense 보상.
- **한계**: ① 도메인 이식성이 나쁨 — 대부분의 오픈 PRM은 GSM8K/MATH에서만 학습되어 OOD(OlympiadBench 등)에서 F1이 붕괴 (R-PRM 논문 Table 1, https://aclanthology.org/2025.emnlp-main.679.pdf). ② 라벨 비용: PRM800K급 인간 라벨링은 프론티어 랩 외에는 비현실적. ③ dense 보상을 RL에 직접 쓰면 reward hacking에 취약해 outcome 보상 혼합이 실무 표준이 됨.
- **숫자**: "Let's Verify Step by Step" — 프로세스 감독이 MATH 대표 서브셋에서 78% 정답률로 outcome 감독을 상회, PRM800K 공개 (https://arxiv.org/abs/2305.20050). Math-Shepherd — Mistral-7B GSM8K 77.9→84.1, MATH 28.6→33.0 (검증기 결합 시 89.1/43.5) (https://arxiv.org/abs/2312.08935, 수치 인용: https://www.opentrain.ai/blog/process-reward-models-vs-outcome-reward-models/).
- **최신**: R-PRM (추론형 PRM, ProcessBench에서 GPT-4o 대비 +8.5 F1): https://arxiv.org/abs/2503.21295

### 1.4 Outcome trajectory (결과 검증된 궤적 → STaR/ReST 계열)
- **입력**: 모델이 스스로 생성한 다수 샘플 + 결과 검증기(정답 체커/테스트). 정답 맞은 궤적만 남겨 SFT (rejection sampling / RFT).
- **출력**: 자기 데이터로 개선된 정책. 반복하면 자기 개선 루프.
- **한계**: ① 베이스가 아예 못 푸는 문제(0% pass rate)에서는 데이터가 생성되지 않음 → 쉬운 문제에 편향. ② 우연히 정답을 맞힌 잘못된 추론도 통과(양성 편향). ③ 반복 시 다양성 붕괴 위험.
- **1차 출처**: STaR https://arxiv.org/abs/2203.14465 · ReST https://arxiv.org/abs/2308.08998 · ReST^EM (self-training 스케일링) https://arxiv.org/abs/2312.06585 · DeepSeekMath RFT+GRPO (7B가 MATH 51.7→88.2, 이 계열의 결정판) https://arxiv.org/abs/2402.03300

### 1.5 Environment rollout (환경 상호작용 궤적)
- **입력**: 실행 가능한 환경(웹/OS/코드런타임/게임) + 초기 상태 + 태스크. 모델이 멀티턴으로 행동하고 환경이 상태와 보상을 반환.
- **출력**: (상태, 행동, 보상) 트라젝토리 → SFT(성공 궤적) 또는 멀티턴 RL.
- **한계**: ① 환경 구축·유지 비용이 데이터 유형 중 최고. ② 멀티턴 RL의 고유 불안정성 — RAGEN이 보고한 **"Echo Trap"**: 보상 분산 붕괴·엔트로피 하락·그래디언트 스파이크를 동반한 반복 템플릿 수렴 (https://arxiv.org/abs/2504.20073). ③ 세밀한 보상 없이는 추론이 사라지고 얕은 전략/환각적 사고만 남음 (동 논문 Finding 3). ④ 같은 데이터로 SFT가 RL보다 단기 성적이 좋은 경우도 있음(RAGEN 부록 C) — 환경은 "RL용"이어야 가치가 극대화됨.
- **1차 출처**: SWE-Gym (2,438개 실행 가능 SWE 태스크 환경, 최대 +19%p 절대 상승) https://arxiv.org/abs/2412.21139 · WebRL (온라인 커리큘럼 RL) https://arxiv.org/abs/2411.02337 · RAGEN/StarPO https://arxiv.org/abs/2504.20073

### 1.6 Synthetic curriculum (합성 문제 + 난이도 커리큘럼)
- **입력**: 시드 문제/페르소나/스킬 그래프 → LLM이 문제를 생성·난이도 조절·자가 채점.
- **출력**: 사실상 무한 확장 가능한 학습 분포. "베이스 모델이 못 푸는 문제"가 없도록 난이도를 정책 수준에 맞춤.
- **한계**: ① 합성 분포와 실제 분포의 갭(다양성·현실성). ② 자가 생성 문제는 검증기도 합성이 되어 라벨 노이즈가 누적. ③ 모델 붕괴 리스크 관리 필요.
- **1차 출처**: PersonaHub (10억 페르소나로 합성 데이터 다양화) https://arxiv.org/abs/2406.20094 · Magpie (정렬된 모델에서 프롬프트 없이 instruction 데이터 자가 합성) https://arxiv.org/abs/2406.08464 · Phi-4 (합성 데이터 중심 학습, 14B) https://arxiv.org/abs/2412.08905 · Absolute Zero (문제 생성+풀이를 하나의 RL 루프로) https://arxiv.org/abs/2505.03335 · Light-R1 (커리큘럼 SFT→DPO→RL 3단계) https://arxiv.org/abs/2503.10460

### 1.7 RLVR (검증 가능 보상 강화학습)
- **입력**: (프롬프트, 프로그램적 검증기) — 수학 정답 매칭, 코드 테스트, 형식 체크. **인간 라벨 불요**.
- **출력**: 정답률이 실제로 오른 정책. R1-Zero가 SFT 없이 RL만으로 추론을 형성함을 보인 이후 post-training의 주축.
- **출력의 본질(중요)**: RLVR은 주로 베이스 모델에 이미 있는 추론 패턴을 **샤프닝**한다 — pass@k 실험에서 k가 크면 베이스 모델이 RL 모델을 역전 (Yue et al., NeurIPS 2025 Oral, https://arxiv.org/abs/2504.13837). 단, NVIDIA ProRL은 장기 RL로 경계 확장 사례를 보고 (https://arxiv.org/abs/2505.24864) — 결론: "새 능력 창출"은 어렵지만 "가능성 공간의 밀도 상승"은 확실하며, distillation과 역할이 다름.
- **한계**: ① 검증 가능한 도메인으로 사실상 국한(수학/코드/형식) — **Morphospace의 기회 지점**. ② Qwen 계열에서는 랜덤 보상으로도 MATH-500이 +21.4%p 오르는 "Spurious Rewards" 현상 — 벤치마크 게인이 진짜 능력 향상이 아닐 수 있음을 보여주는 경계 사례 (https://arxiv.org/abs/2506.10947). ③ 베이스 모델 사전학습 분포에 강하게 의존.
- **1차 출처**: DeepSeek-R1 https://arxiv.org/abs/2501.12948 · DAPO (오픈 소스 대규모 RL 시스템) https://arxiv.org/abs/2503.14476 · Tülu 3 RLVR https://allenai.org/blog/tulu-3-technical

---

## 2. 소형 오픈웨이트 모델(0.5B–8B) 개선 사례 + 비용 (구체 숫자)

| 사례 | 모델 | 결과 | 데이터 | GPU/비용 | 출처 |
|---|---|---|---|---|---|
| **TinyZero** | Qwen2.5-3B(베이스) | Countdown 게임에서 자기검증·탐색 행동 자발 발생(R1-Zero 재현) | 합성 countdown 문제 (검증기=산수 체커) | **~$30**, 소규모 GPU | https://github.com/Jiayi-Pan/TinyZero , https://cybersecuritynews.com/tinyzero/ |
| **DeepScaleR** | R1-Distill-Qwen-1.5B | AIME24 pass@1 **43.1%** (o1-preview 상회) | 40k 수학 문제, 컨텍스트 8k→16k→24k 점진 확장 | **3,800 A100시간 ≈ $4,500** | https://pretty-radio-b75.notion.site/DeepScaleR-Surpassing-O1-Preview-with-a-1-5B-Model-by-Scaling-RL-19681902c1468005bed8ca303013a4e2 |
| **Light-R1** | Qwen2.5-7B/32B(장문 CoT를 스크래치부터) | Light-R1-7B-DS AIME24 59.1 / AIME25 44.3 / GPQA-D 49.4 | 커리큘럼 SFT 2단계→DPO→RL | **12×H800, ≤6시간 ≈ $1,000** | https://arxiv.org/abs/2503.10460 , https://github.com/Qihoo360/Light-R1 |
| **OpenThinker-7B** | Qwen2.5-7B-Instruct | AIME24 31.3, MATH500 83.0, LCB 39.9 (동급 오픈데이터 SOTA) | **OpenThoughts-114k** (R1 distill + 정답 검증) | LLaMA-Factory 3 epoch, 16k ctx | https://huggingface.co/datasets/open-thoughts/OpenThoughts-114k , https://bespokelabs.ai/blog/scaling-up-open-reasoning-with-openthinker-32b |
| **WebRL** | Llama-3.1-8B, GLM-4-9B | WebArena-Lite 성공률 **4.8%→42.4%**, **6.1%→43%** (GPT-4o 13.9%, GPT-4-Turbo 17.6% 크게 상회) | 자기진화 온라인 커리큘럼 RL + outcome 보상모델 | 멀티 GPU RL (논문 부록) | https://arxiv.org/abs/2411.02337 |
| **SWE-Gym** | Qwen2.5-Coder 계열 | SWE-bench Verified 최대 **+19%p 절대 상승**, verifier 결합 시 32.0% (당시 오픈웨이트 SOTA) | 2,438 실행 가능 태스크 환경 + 에이전트 궤적 | 환경+SFT+verifier 학습 | https://arxiv.org/abs/2412.21139 |
| **Qwen2.5-Math-7B** | 자체 7B | MATH 85.3 (TIR), 72B급 상회 | 합성 SFT + GRPO RLVR | Qwen 남부 | https://arxiv.org/abs/2409.12122 |
| **DeepSeekMath-7B** | 7B | MATH 51.7→88.2 (GRPO+RFT) | 120만 수학 instruction + rejection sampling | DeepSeek 남부 | https://arxiv.org/abs/2402.03300 |
| **s1-32B** (참고: 32B) | Qwen2.5-32B-Instruct | AIME24 50%→57% (budget forcing 결합), o1-preview 상회 | **s1K = 1,000개** 고난도·다양·고품질 trace | 16×H100 26분 학습 (병행 복제 실험에서 수십 달러 클라우드 비용으로 병기됨) | https://arxiv.org/abs/2501.19393 |

**패턴 요약**: ① 수학/코드/웹 등 **검증기가 있는 도메인에서는 $30~$4,500이면 0.5B–8B 모델의 측정 가능한 벤치마크 상승을 재현 가능**하다. ② 비용의 대부분은 데이터가 아니라 **rollout 생성 컴퓨트**다. ③ 성공 사례 전부 "검증 가능한 환경/검증기"를 전제로 한다 — 검증기가 없는 도메인(경영 판단 등)의 데이터는 구조적으로 공백이다.

---

## 3. RLVR 최신 실전 지식 (2024–2026)

### 3.1 Reward 설계
- **규칙 기반 이진 보상이 기본값**: 정답 1 / 오답 0(+형식 페널티). DeepSeek-R1은 정확도 보상+형식 보상만 사용했고, 학습된 보상모델은 reward hacking 때문에 RLVR에서 기피한다고 명시 (https://arxiv.org/abs/2501.12948).
- **형식 보상은 보조 수단**: 포맷 페널티(RAGEN은 -0.1)로 파싱 가능성만 확보하고, 형식 보상이 정확도 보상을 압도하면 "포맷만 맞는 빈 응답"으로 해킹됨.
- **길이 편향 제거가 핵심 튜닝 포인트**: vanilla GRPO는 긴 응답의 토큰 기여도가 희석되는 길이 편향과, 문제별 표준편차 정규화의 난이도 편향이 있음 → Dr. GRPO(정규화 제거), DAPO(token-level loss, overlong soft penalty, clip-higher)로 수정. (https://arxiv.org/abs/2503.14476 , 정리: https://magazine.sebastianraschka.com/p/the-state-of-llm-reasoning-model-training)
- **난이도 큐레이션이 보상 설계만큼 중요**: pass rate 0%(전원 오답)나 100%(전원 정답)인 프롬프트는 GRPO 어드밴티지가 0 → 학습 신호 없음. DAPO의 dynamic sampling, RAGEN의 분산 기반 필터링(고분산 프롬프트만 유지, 25% 유지율 디폴트)이 표준 핵심. (https://arxiv.org/abs/2504.20073)

### 3.2 Reward hacking 방지
- **Spurious Rewards 교훈**: Qwen 계열에서 랜덤 보상조차 MATH-500 +21.4%p (ground-truth +29.1%p의 73%) — GRPO의 클리핑 편향이 사전학습 고확률 행동(코드 추론 등)을 증폭하기 때문. **같은 레시피가 Llama3/OLMo2에서는 통하지 않음** → 모델 패밀리별 검증 필수, 벤치마크 게인만으로 보상 설계를 판단하면 안 됨. (https://arxiv.org/abs/2506.10947 , 해설: https://www.interconnects.ai/p/reinforcement-learning-with-random)
- **실무 방어**: ① 보상을 프로그램적 검증기에 고정하고 학습 가능한 프록시(RM)를 혼합하지 않기; ② 이상 고보상 rollout을 정기 감사해 해킹 택소노미 구축(Rubric Anchors 논문의 절차, https://arxiv.org/abs/2508.12790); ③ 길이/반복 지표 모니터링(길이 급증·엔트로피 붕괴는 해킹 전조, RAGEN Echo Trap); ④ 홀드아웃 검증기(채점기와 다른 경로의 평가)로 교차 확인.
- **멀티턴 환경 특유의 해킹**: outcome 보상만 있으면 추론 길이가 학습과 함께 감소하고 "시행착오로 우연히 성공"한 궤적이 강화됨 → 중간 단계 보상(shaping)이 필요하다는 RAGEN Finding 3 (https://arxiv.org/abs/2504.20073).

### 3.3 pass@k와 "RL은 새 능력을 만드는가" 논쟁
- **Yue et al. (2504.13837)**: k가 크면(수백) 베이스 모델의 pass@k가 RL 모델을 추월 → RLVR은 샘플링 효율을 올릴 뿐 추론 경계를 확장하지 못한다. 6개 주요 RL 알고리즘이 모두 베이스 모델 상한에 크게 못 미침. distillation은 실제로 새 패턴을 주입. (https://arxiv.org/abs/2504.13837)
- **ProRL (NVIDIA, 2505.24864)**: 충분히 긴 RL(prolonged)은 베이스가 pass@k에서도 못 푸는 문제를 풀게 되는 경계 확장 사례 보고 → "짧은 RL은 샤프닝, 긴 RL은 확장 가능"이 현재 합의에 가까움. (https://arxiv.org/abs/2505.24864)
- **실무 함의**: 환경/데이터 제공자 입장에서, 베이스 모델이 가끔 성공하는(중간 난이도) 태스크가 RL 학습 신호를 극대화하는 지점 = "pass rate 20–80% 구간의 태스크를 많이 확보하는 것"이 데이터 상품의 핵심 스펙.

### 3.4 커리큘럼
- **난이도 커리큘럼**: DeepScaleR는 컨텍스트(사고 길이)를 8k→16k→24k로 점진 확장(리소스 대비 효율 ↑), Light-R1은 SFT 2단계(쉬움→어려움)→DPO→RL 순서. (위 §2 출처)
- **온라인 커리큘럼**: WebRL은 정책이 못 푸는 태스크를 자동 필터링해 다음 에포크의 학습 태스크로 재구성(자기진화 커리큘럼). (https://arxiv.org/abs/2411.02337)
- **다양성 유지**: 프롬프트당 응답 수를 줄이고 태스크 다양성을 늘리는 것(4 responses/prompt)이 일반화에 유리 (RAGEN Table 2); rollout 신선도(Online-1, 매 업데이트 재생성)가 수렴 속도와 일반화를 모두 개선. (https://arxiv.org/abs/2504.20073)

---

## 4. "회사 운영 판단" 같은 검증 어려운 도메인에서 보상 만들기 — 선례

Morphospace에 직접 해당하는 영역. 2024–2026 선례는 5가지 경로로 정리된다.

### 4.1 인스턴스별 전문가 루브릭 → 보상 (가장 직접적 선례)
- **Rubrics as Rewards (RaR, 2507.17746)**: 태스크 인스턴스마다 구조화된 루브릭(가중 체크리스트)을 만들고 LLM 채점기로 루브릭 충족도를 점수화해 온폴리시 RL 보상으로 사용. 단순 Likert LLM-judge 보상 대비 **HealthBench +31% 상대, GPQA-Diamond +7% 상대**. 작은 채점기에서도 분산이 줄고 정렬이 잘 됨 → **"전문가가 케이스별 루브릭을 쓰면 그것이 그대로 RL 보상이 된다"**는 것의 첫 실증. (https://arxiv.org/abs/2507.17746)
- **Rubric Anchors (2508.12790)**: 루브릭 기반 RL의 해킹 패턴 분류와 방어. (https://arxiv.org/abs/2508.12790)
- **OpenRubrics (2510.07743)**: 루브릭을 합성으로 대량 생성해 보상모델 학습 — 루브릭 작성 비용의 스케일링 핵. (https://arxiv.org/abs/2510.07743)
- **Kimi K2 (2507.20534)**: 검증 불가 태스크에는 **self-critique rubric reward** — 정책이 자기 출력을 루브릭 기반 pairwise 비교로 채점하고, 비검증 태스크의 critic 판단력은 검증 가능 태스크에서 강화(K2 이슈 #44에서 비검증 태스크에만 적용 확인). (https://arxiv.org/abs/2507.20534 , https://github.com/MoonshotAI/Kimi-K2/issues/44)

### 4.2 Pairwise 전문가 비교 + 캘리브레이션된 LLM-judge
- **Zheng et al., MT-Bench (2306.05685)**: GPT-4 judge가 인간 간 일치도와 **80% 이상** 일치함을 보이며 LLM-as-judge의 타당성 확립; 위치 편향·장황성 편향·자기우호 편향을 정량화하고 완화법(스왑, 참조답, 수학 제외) 제시 — judge 캘리브레이션의 사실상 표준 절차. (https://arxiv.org/abs/2306.05685)
- **JudgeBench (2410.12784)**: 어려운 쌍에서는 강한 judge도 크게 약해짐 → 쉬운 벤치로 judge를 검증하면 안 된다는 경고. (https://arxiv.org/abs/2410.12784)
- **Prometheus / Prometheus 2 (KAIST, 2310.08491 / 2405.01535)**: GPT-4 생성 피드백+커스텀 루브릭 데이터셋(Feedback Collection)으로 **오픈소스 전용 채점기**를 학습 — 인간 상관 0.897(Pearson), pairwise 인간 일치 72–85%. **한국 랩이 만든 선례**: "전문가 루브릭 → 강한 모델로 채점 데이터 대량화 → 자체 judge 학습" 파이프라인의 원조. (https://arxiv.org/abs/2405.01535 , https://github.com/prometheus-eval/prometheus-eval)
- **GDPval (OpenAI, 2025-09)**: 44개 직업 1,320개 태스크에서 모델 산출물과 인간 전문가 산출물을 **업계 전문가가 블라인드 pairwise 비교** — "실무자의 원래 산출물을 기준답으로 삼는 채점"의 대규모 상업적 선례. (https://openai.com/index/gdpval/)

### 4.3 "매니저의 원래 결정/실제 결과값"을 보상으로
- **SWE-Lancer (OpenAI, 2502.12115)**: Upwork 실제 과제에 **실제 지급된 달러 금액(총 $1M 상당)**을 태스크 가치로 사용. "실제 회사가 실제로 지불한 결정의 경제적 가치"가 그대로 스칼라 보상이 된 선례 — Morphospace의 "실제 운영 사건의 실제 결과" 개념과 동일한 설계 원리. (https://arxiv.org/abs/2502.12115)
- **MLE-bench (OpenAI, 2410.07095)**: Kaggle 실제 대회의 메달 컷(인간 리더보드 분포)을 채점 기준으로 사용 — "당시 인간 집단의 실제 평가"를 검증기로 고정. (https://arxiv.org/abs/2410.07095)
- **TheAgentCompany (2412.14161)**: 실무형 에이전트 벤치마크에서 체크포인트 기반 부분 점수 — 최종 성공 0/1이 아니라 중간 산출물을 채점해 보상 밀도를 확보하는 설계. (https://arxiv.org/abs/2412.14161)

### 4.4 멀티속성 인간 라벨 → 보상모델 (rubric의 RM 버전)
- **HelpSteer2 (NVIDIA, 2406.08673)**: 도움됨·정확성·일관성·복잡성·장황성 5속성 인간 라벨 ~1만 건으로 RM 학습 → RewardBench에서 당시 오픈 SOTA. 속성별 점수는 "경영 판단 루브릭 축"(리스크, 비용, 컴플라이언스 등)으로 재해석 가능. (https://arxiv.org/abs/2406.08673)

### 4.5 종합 판단 (사업 설계 관점)
검증 어려운 도메인의 보상은 2025년 들어 **"정답"이 아니라 "구조화된 심사 인프라"**로 수렴 중이다: ① 케이스별 전문가 루브릭(RaR), ② 실제 과거 결정/결과값(SWE-Lancer·GDPval), ③ 캘리브레이션된 judge + 해킹 감사 루프. 이 셋을 묶을 수 있는 주체가 필요하며, 현재 이를 **데이터 상품으로** 파는 곳은 없다(벤치마크로만 존재). 학습용(labeled trace, rubric corpus, calibrated judge)으로 전환하는 것이 명확한 갭.

---

## 5. 한국어 / 한국 기업 맥락 데이터 희소성 — 증거

### 5.1 웹 코퍼스 점유율
- **CulturaX** (167개 언어, mC4+OSCAR 통합 대표 다언어 코퍼스): 한국어 20.6M 문서, 24.8B 토큰 = **전체 토큰의 0.39%** (영어는 과반). (https://huggingface.co/datasets/uonlp/CulturaX)
- Common Crawl의 언어 분포는 지수적으로 붕괴 — 100개 언어가 0.1% 미만 (UnifiedCrawl, https://arxiv.org/html/2411.14343v1). 한국어는 상위 10위권 언어지만 절대량은 영어의 수십 분의 1 수준.

### 5.2 한국 대형 랩들이 "자체 한국어 코퍼스"를 짓는다는 사실 자체가 희소성의 증거
- **HyperCLOVA X (Naver)**: 한국어/영어/코드 균형 코퍼스를 자체 구축하고, 한국어 샘플 비율 ablation을 통해 한국어 성능이 데이터 비율에 민감함을 정량화 — 공개 코퍼스로는 부족하기 때문. (https://arxiv.org/abs/2404.01954)
- **EXAONE (LG AI Research)**: 3.0(7.8B)부터 한영 이중언어를 표방하며 자체 한국어 데이터 파이프라인 구축, K-EXAONE에서는 어휘의 3/6을 한국어에 배분하는 등 토크나이저 수준에서 한국어 엔지니어링. (https://arxiv.org/html/2601.01739v1)
- **Upstage Solar, SKT A.X, Naver** 등이 KMMLU 상위권을 사실상 한국 랩이 점유 — 글로벌 모델들은 한국어 데이터 투자가 얇아 한국어 네이티브 맥락에서 뒤처짐. (KMMLU 리더보드 정리: https://github.com/daekeun-ml/evaluate-llm-on-korean-dataset)

### 5.3 평가·정렬 데이터는 있지만 "학습용 궤적/환경"은 부재
- 한국어 벤치마크: KMMLU(35,030 문항, https://arxiv.org/abs/2402.11548), HAE-RAE Bench, CLIcK(문화), KoBALT 등 — 전부 **정적 지식/문화 평가**.
- 한국어 **SFT/preference 정렬 데이터**: KoAlpaca, KULLM, KoInstruct 등 커뮤니티 수준(수만 건, 품질 검증 약함). Prometheus(KAIST)가 만든 Feedback Collection조차 영어 중심.
- **한국어 agentic 환경/rollout 데이터, 한국 기업 운영 맥락의 검증 가능 태스크: 공개 사례 0건** (조사 범위 내). 글로벌 벤치마크 12종(TheAgentCompany, CRMArenaPro 등) 전부 영어·미국 기업 맥락. 즉 한국어/한국 기업 맥락은 ① 사전학습 코퍼스도 얇고(0.39%), ② post-training 궤적 데이터는 사실상 전무하며, ③ 벤치마크조차 지식형에 한정 — 3중 공백.

### 5.4 해석
한국어는 "저자원 언어"는 아니지만 **"학습 신호가 있는 데이터(검증 가능 태스크, 선호 쌍, 운영 궤적) 기준으로는 극저자원"**이다. 한국 기업 운영 사건을 RL 환경으로 컴파일하는 상품은 글로벌 유일 카테고리일 뿐 아니라, 한국어 reasoning/agentic 데이터를 원하는 국내 랩(Naver·LG·Upstage·SKT·삼성)과 "한국 시장 맥락 agentic 능력"을 원하는 프론티어 랩 양쪽에 팔 수 있는 이중 수요가 있다.

---

## 부록: 핵심 1차 출처 인덱스
- RLVR/추론: DeepSeek-R1 https://arxiv.org/abs/2501.12948 · DeepSeekMath https://arxiv.org/abs/2402.03300 · DAPO https://arxiv.org/abs/2503.14476 · pass@k 한계 https://arxiv.org/abs/2504.13837 · ProRL https://arxiv.org/abs/2505.24864 · Spurious Rewards https://arxiv.org/abs/2506.10947
- 데이터 레시피: Tülu 3 https://allenai.org/blog/tulu-3-technical · OpenThoughts https://arxiv.org/abs/2506.04178 · s1 https://arxiv.org/abs/2501.19393 · Light-R1 https://arxiv.org/abs/2503.10460
- 환경/에이전트: SWE-Gym https://arxiv.org/abs/2412.21139 · SWE-RL https://arxiv.org/abs/2502.18449 · WebRL https://arxiv.org/abs/2411.02337 · RAGEN https://arxiv.org/abs/2504.20073
- 비검증 도메인 보상: RaR https://arxiv.org/abs/2507.17746 · Kimi K2 https://arxiv.org/abs/2507.20534 · Prometheus2 https://arxiv.org/abs/2405.01535 · SWE-Lancer https://arxiv.org/abs/2502.12115 · GDPval https://openai.com/index/gdpval/ · MT-Bench judge https://arxiv.org/abs/2306.05685
- 한국어: CulturaX https://huggingface.co/datasets/uonlp/CulturaX · HyperCLOVA X https://arxiv.org/abs/2404.01954 · K-EXAONE https://arxiv.org/html/2601.01739v1 · KMMLU https://arxiv.org/abs/2402.11548
