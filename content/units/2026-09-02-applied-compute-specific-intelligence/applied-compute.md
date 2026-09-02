---
title: "Applied Compute: 기업은 모델이 아니라 학습 루프를 소유한다"
owner_principal: environment-foundry
domain_project: datafooding
channel: rldr
format: short-plus-long-form
source_checked_at: 2026-09-02
canonical_url: https://datafooding.ai/research/appliedcompute
---

# Applied Compute: 기업은 모델이 아니라 학습 루프를 소유한다

## #RLDR

Applied Compute는 2026년 4월 누적 투자 1억 6,000만 달러와 13억 달러 post-money valuation을 발표했습니다. 회사 발표를 읽으면 이 자금은 또 하나의 범용 foundation model보다 기업별 model factory와 agent workforce를 위한 platform과 전문성 확장으로 향합니다.

1. Specific Intelligence는 회사 공식 설명상 LLM weights와 runtime context에 존재합니다. 이를 agent harness, grader, production feedback까지 결합한 system으로 해석할 수 있습니다.

2. 기업 데이터의 핵심은 문서보다 판단 기준입니다. 좋은 답을 판별하는 eval이 없으면 RL은 일을 배우지 못합니다. 오히려 틀린 reward를 더 빠르게 최적화합니다.

3. Applied Compute는 pure SaaS보다 forward-deployed model factory에 가깝습니다. AC2 platform, dedicated inference, FDE와 Applied Research Engineer, managed training과 serving을 함께 팝니다.

4. 배포가 끝이 아니라 다음 학습의 시작입니다. Production trace가 self-distillation, preference optimization, RL로 돌아옵니다. 다만 한 번 배포하면 저절로 계속 좋아지는 agent는 아직 roadmap입니다.

5. Moat는 model access가 아니라 feedback loop의 소유권입니다. Frontier API는 누구나 살 수 있습니다. 같은 업무를 실행하고, 결과를 재현하고, 전문가 판단을 reward로 바꾸는 loop는 회사마다 다릅니다.

범용 모델 경쟁 다음은 각 회사가 자기 업무의 학습 루프를 얼마나 잘 소유하느냐의 경쟁입니다.

## Specific Intelligence for your business란 무엇인가

Applied Compute는 이를 회사 안에 흩어진 잠재 지식과 판단을 custom model과 agent workforce로 바꾸는 것으로 설명합니다. 새롭게 정립된 학술 분류라기보다 회사가 만든 제품 언어입니다. 회사는 Specific Intelligence가 LLM weights와 runtime context에 존재한다고 정의합니다. 이 글은 그 지능이 실제 업무에서 작동하는 system을 다음 다섯 요소의 결합으로 해석합니다.

### 1. Weights

Open-weight base model을 특정 task에 post-train합니다. 모든 회사가 foundation model을 처음부터 훈련하라는 뜻이 아닙니다. 회사가 필요한 quality, latency, cost의 한 점을 맞추는 specialized model을 소유하자는 주장입니다.

### 2. Context

모든 지식이 weights에 들어가지는 않습니다. Applied Compute의 Context Engine은 문서, SaaS, 과거 작업과 agent trace를 Remember, Refine, Retrieve합니다. 회사는 이를 살아 있는 조직 지식의 encoding으로 설명합니다.

Mercor의 APEX-Agents 외부 benchmark에서 법률 71개, IB 68개, 컨설팅 69개, 총 208개 과제를 Applied Compute 자체 harness로 평가했습니다. 회사는 GPT-5.4 medium에 Contextbase를 붙였을 때 44.2%에서 51.7%로 절대 +7.5%p, 상대 +16.9% 개선됐다고 보고했습니다. GDPVal에서는 개선 폭이 더 작았고 높은 reasoning budget에서는 일부 이득이 사라졌습니다. Context가 항상 이기는 것이 아니라 task 간 지식 재사용 가능성과 baseline saturation, context 품질에 달려 있다는 뜻입니다.

### 3. Harness

Agent가 실제로 일하는 환경입니다. Filesystem, tool, state, permission, timeout, reset이 들어갑니다. AC2는 고객이 기존 agent stack을 버리지 않고 model API와 rollout lifecycle adapter만 연결하는 Bring Your Own Harness를 제시합니다.

### 4. Evals

좋은 결과가 무엇인지 기계가 판별할 수 있게 만드는 기준입니다. Test, rubric, human preference, business outcome이 reward가 됩니다. Applied Compute가 고객 현장에 researcher를 보내는 가장 큰 이유도 data를 모으기 위해서만이 아니라 전문가의 판단을 task와 grader로 번역하기 위해서입니다.

### 5. Production feedback

실제 사용자 입력, 모델 응답, tool output, token-level signal을 다음 training에 넣습니다. 오늘의 traffic이 내일의 checkpoint가 되는 loop입니다. 이 경험의 소유권이 Applied Compute가 말하는 장기 moat입니다.

## 어떤 비즈니스를 하는가

공개 자료를 종합하면 네 가지가 묶여 있습니다.

- AC2: open model의 training, serving, improvement를 잇는 private-beta platform
- Dedicated inference: 고객별 endpoint, 관찰 가능성, 새 checkpoint 배포
- FDE와 Applied Research Engineer: 고객 업무를 task, environment, grader로 바꾸는 현장팀
- Managed training과 serving: 학습 recipe뿐 아니라 production support까지 담당

순수 SaaS라기보다 Palantir식 forward deployment와 frontier lab식 post-training의 결합에 가깝습니다. 공개 가격과 계약 단위, 서비스 매출 비중, 고객당 투입 인력은 없습니다. 고객 현장에 깊이 들어가는 실행력이 강점이면서 scale과 margin의 부담이 될 수 있습니다.

## 기술적인 접근

Applied Compute가 반복해서 다루는 병목은 model architecture 하나가 아닙니다.

- Environment fidelity: training sandbox가 실제 업무와 다르면 모델이 그 차이를 shortcut으로 학습합니다.
- Reward design: 잘못된 penalty는 거부나 무행동을 만들고, timeout filtering은 timeout 유도를 만들 수 있습니다.
- Async RL: rollout의 heavy tail로 GPU가 쉬는 문제를 줄이는 대신 stale policy data를 관리해야 합니다.
- Agentic inference: multi-turn tool use는 KV cache, scheduler, tool latency, 긴 꼬리 분포를 함께 봐야 합니다.
- Context and memory: weights에 넣을 지식과 runtime에 검색할 지식을 분리하고 함께 평가합니다.
- Online improvement: production trace를 self-distillation, preference optimization, RL에 다시 사용합니다.

## 확인된 고객 결과와 증거 경계

- DoorDash: 중요 메뉴 오류가 기준선 대비 상대적으로 30% 감소하고 1,000시간 이상 절약됐다고 회사 case study가 보고했습니다.
- Cognition: Windsurf Quick Review의 특정 harness에서 bug detection이 10배 빨라졌다고 보고했습니다.
- Harvey Review Table: Applied Compute는 Harvey와 GLM-5.2 기반 별도 Review Table model을 production harness 안에서 post-train했습니다.
- Context Engine: APEX에서는 상대 16.9% 개선을 보고했지만 GDPVal에서는 개선 폭이 작았습니다.

모두 공개된 회사 또는 고객 case study의 범위입니다. 독립적인 보편 benchmark로 확대하지 않습니다.

## Harvey Tenet에서 실제로 맡은 역할

Harvey Tenet core는 Harvey와 Fireworks가 Kimi K3를 post-train한 open-weight legal model입니다. Applied Compute가 Tenet을 훈련했다고 쓰면 공식 자료와 어긋납니다.

Applied Compute는 Harvey의 별도 Review Table capability에서 GLM-5.2를 production harness 안에 post-train했습니다. Harvey의 Tenet 발표는 Applied Compute를 acknowledgement의 파트너로 언급합니다. Fireworks Research와 Harvey의 Tenet core training, Applied Compute의 Review Table collaboration은 다른 작업입니다.

## Satya Nadella와의 대담이 보여주는 영향력

Applied Compute는 Yash Patil과 Satya Nadella의 32분 40초 fireside chat을 공식 채널에 공개했습니다. Satya의 핵심 문장은 다음과 같습니다.

> There should be as many models in the world as there are firms.

공식 podcast feed라기보다 enterprise AI와 model ownership을 다룬 긴 대담입니다. Applied Compute가 제안하는 범주가 Microsoft CEO와 장시간 논의할 만큼 중요한 의제가 됐다는 신호는 맞습니다. 공개 자료에서 Microsoft의 투자나 독점 제휴를 확인할 근거는 없습니다.

## 회사가 그리는 미래

모든 회사가 자기 Specific Intelligence와 계속 학습하는 agent workforce를 소유합니다. 모델 선택보다 model factory와 누적 experience가 경쟁 우위가 됩니다. Ari라는 사내 AI research agent는 현재 trace 분석, reward hacking 탐지, 실험 기억과 보고서 생성을 수행한다고 회사가 설명합니다. 실험 설계와 실행, 모니터링, 추천까지 연구 loop 전체를 맡는 것은 roadmap입니다.

가장 큰 반론도 분명합니다. Specific Intelligence의 구성 요소는 fine-tuning, RAG, context engineering, agent orchestration, eval infrastructure, managed deployment의 결합으로 설명할 수 있습니다. 새 algorithm 하나보다 통합 운영 모델에 가깝습니다. Reward가 틀리면 모델은 더 효율적으로 틀린 행동을 학습하고, 고객별 environment와 grader를 만드는 비용은 scale을 어렵게 할 수 있습니다.

Applied Compute의 강점은 이 반론 안에 있습니다. 새로운 이름보다 기존 조각을 실제 고객 업무 안에서 빠르게 하나의 학습 loop로 묶는 실행력이 제품입니다.

---

# 영상 1. Efficient Reinforcement Learning

Rhythm Garg, Linden Li / AI Engineer / 20:19

## #RLDR

1. Enterprise RL은 한 번의 거대한 run이 아니라 고객별 업무를 며칠 안에 학습하는 반복 생산 시스템입니다.
2. 긴 응답 몇 개가 전체 batch를 붙잡는 straggler를 비동기 sampling과 training으로 줄입니다.
3. 그 대가로 오래된 policy가 만든 rollout이 쌓이는 staleness가 생깁니다.
4. 마지막 60% speed-up은 production 실측이 아니라 조건부 simulation입니다.

## 00:22 연구소의 RL을 고객별 생산 공정으로

수학 문제 네 개를 각각 100번 풀게 하는 예시로 RL을 설명한 뒤, 실제 목표를 기업별 업무로 바꿉니다. 범용 모델이 낯설어하는 OOD 업무를 고객 분포로 끌어오고, 사용량을 다시 학습 신호로 넣습니다.

Frontier lab의 수주 단위 run과 달리 고객별 학습은 며칠 안에 끝나야 합니다. GPU 비용과 학습 시간의 분산을 함께 관리해야 합니다.

## 04:06 마지막 1%가 전체 GPU를 세운다

동기식 RL은 batch의 모든 rollout이 끝나야 다음 step으로 넘어갑니다. 발표자의 Qwen-30B 내부 측정에서는 99%가 약 40초 안에 끝났지만 마지막 1%가 추가 80초를 썼습니다. Checkpoint, hardware, sampling 설정이 공개되지 않은 내부 사례입니다.

PipelineRL은 sampling GPU와 training GPU를 분리하고 끝난 rollout을 queue에 넣습니다. Trainer는 batch가 모이면 바로 학습하고 새 weights를 sampler에 전달합니다. 다만 weights 수신 과정에서 짧은 inference pause가 생길 수 있습니다.

## 07:11 더 빠른 비동기는 더 오래된 데이터를 만든다

Rollout을 만든 behavior policy와 현재 target policy가 달라집니다. Importance ratio가 차이를 보정할 수 있지만 정확한 확률비와 support 조건이 필요합니다. Clipping과 근사 ratio는 bias를 만들 수 있습니다.

시스템은 GPU 예산, training batch, sampling latency, training throughput을 함께 봅니다. KV cache에 따라 memory-bound와 compute-bound 구간이 바뀌며 roofline 형태의 latency curve로 병목을 추정합니다.

## 12:53 최적 GPU 비율은 고정값이 아니다

Simulator에 response-length distribution을 넣고 sampling 생산률과 trainer 소비율이 맞는 정상 상태를 찾습니다. Training GPU가 너무 많으면 queue가 비고, sampling GPU가 너무 많으면 staleness가 커집니다.

발표의 약 60% speed-up은 이 조건의 simulation입니다. 자동자막의 throughput 식도 교정해야 합니다. Batch latency 기준 처리량은 batch size를 latency로 나눈 값 또는 tokens/sec입니다.

### 자막 교정

- GPOSS는 GPT-OSS
- RO/R0 training은 RL training
- stillness는 staleness
- 60%는 simulated speed-up

[영상](https://www.youtube.com/watch?v=o15AaYl7Wu0) / [PipelineRL](https://arxiv.org/abs/2509.19128) / [DeepSeekMath](https://arxiv.org/abs/2402.03300)

---

# 영상 2. Learning on the Job

Raymond Feng / AI Engineer / 18:20

## #RLDR

1. Post-training의 단위가 Q&A에서 environment, 실제 agent harness로 이동합니다.
2. 실제 harness는 fidelity를 높이지만 같은 고객 반응을 replay할 수 없습니다.
3. Bring Your Own Harness는 기존 stack의 model call을 proxy해 trajectory를 학습에 연결합니다.
4. 한 번 배포한 agent가 매 interaction에서 스스로 학습한다는 결말은 roadmap입니다.

## 00:00 Q&A에서 실제 업무 환경으로

발표는 post-training을 Q&A, synthetic environment, custom harness, 모든 interaction에서 계속 배우는 agent의 네 단계로 놓습니다. Agentic task에는 task specification, filesystem, tool schema, sandbox, reset이 들어갑니다.

## 04:34 Environment의 작은 거짓말도 학습한다

Reset 가능한 environment에서는 같은 시작점에서 여러 rollout을 만들고 GRPO로 상대적으로 나은 trajectory를 강화할 수 있습니다. 그러나 tool call이 10% 실패하는 내부 사례에서는 응답이 짧아졌습니다. Timeout rollout을 제거했더니 모델이 timeout을 유도한 사례도 듭니다. 특정 run의 관찰이며 일반 법칙이 아닙니다.

Environment fidelity는 실제와 학습 환경의 일치 문제이고 reward hacking은 보상이나 환경의 허점을 이용하는 행동입니다. 연결되지만 같은 개념은 아닙니다.

## 09:23 기존 agent stack을 버리지 않는다

Bring Your Own Harness는 completion endpoint와 rollout lifecycle에 adapter를 둡니다. Context, tool execution, state management는 고객 stack에 남습니다. NVIDIA의 Polar도 harness를 black box로 보고 API call을 proxy해 token-level trajectory를 재구성합니다.

고객이 다른 답변을 봤다면 어떻게 반응했을지 직접 재관측할 수 없습니다. 이것이 non-replayability입니다. 과거 policy data를 새 policy가 학습하는 off-policy 문제와 관련되지만 같은 말은 아닙니다.

## 13:22 Deploy once는 roadmap이다

Self-distillation, automated data pipeline, qualitative feedback ingestion을 연구 방향으로 제시합니다. Knowledge distillation 자체는 오래된 방법입니다. 한 번 배포된 agent가 OOD 업무를 처리하고 계속 weights를 갱신하는 미래는 현재 검증된 제품 기능이 아닙니다.

[영상](https://www.youtube.com/watch?v=k35LeKZEhiE) / [Polar](https://arxiv.org/abs/2605.24220) / [Bring Your Own Harness](https://www.appliedcompute.com/platform/bring-your-own-harness-to-ac2)

---

# 영상 3. Specific Intelligence at Scale

Yash Patil / Modal / 22:15

## #RLDR

1. Frontier model은 출발점이고 회사별 eval이 목적지를 정합니다.
2. Agent harness, evaluation system, improvement loop가 고객마다 다릅니다.
3. DoorDash 30%, Cognition 10배는 각 고객 harness의 회사 case study입니다.
4. 주관적이고 장기적인 업무에서는 domain expert와 reward 설계가 병목입니다.

## 00:36 범용 지능을 빌리는 것과 회사 지능을 만드는 것

Yash Patil은 기업 내부 지식과 workflow, 전문가 판단을 모델에 축적해야 한다고 주장합니다. Specific Intelligence는 그 판단을 weights와 agent behavior로 바꾸고 고객이 소유하게 하는 제품 언어입니다.

## 03:06 Frontier model은 시작점이다

OpenAI, Anthropic, Gemini, xAI와 open-weight model을 사용하되 차이는 회사별 평가 기준에서 생깁니다. DoorDash는 메뉴 QA 기준을 grader와 RL reward로 만들었습니다. 공식 case study는 중요 메뉴 오류를 상대적으로 30% 줄이고 1,000시간 이상 절약했다고 보고합니다.

Cognition은 Windsurf Quick Review에 특화된 model로 bug detection을 10배 빠르게 했다고 보고합니다. 모든 code benchmark의 우위가 아니라 해당 production harness의 quality, speed, cost 결과입니다.

## 06:53 기업 데이터의 진짜 단위는 판단이다

Data dump만으로는 post-training이 되지 않습니다. Context, tool, environment, reward가 연결되어야 합니다. Coding과 math는 자동 검증이 쉽지만 고객 만족, fraud, 법률 위험은 장기적이고 주관적입니다. Applied researcher가 전문가 판단을 task와 rubric으로 바꾸는 일이 먼저 옵니다.

## 10:48 수천 번 실패해도 되는 환경

Agent는 sandbox에서 tool을 부르고 state를 바꿉니다. Training은 이 episode를 반복하므로 reset 가능한 environment가 필요합니다. Modal의 일반 sandbox snapshot과 GPU snapshot은 지원 범위와 제약이 다릅니다. 수천 rollout과 1~3시간 장기 task는 발표자의 시스템 설명이며 공개 benchmark가 아닙니다.

## 15:19 Reward hacking은 잘못 정의된 회사 지식이다

Train-test mismatch가 있으면 agent는 production이 아니라 simulator의 허점을 배웁니다. 환불을 많이 승인하면 단기 만족도가 오르는 예시는 설명용 일화입니다. 자동 검증이 쉬운 task에서 시작하고 주관적인 결과는 human expert와 함께 reward를 설계해야 합니다.

### 자막 교정

- Yash Patel은 Yash Patil
- Merck는 Mercor
- soda model은 원음만으로 small 또는 SOTA를 확정할 수 없어 인용 제외

[영상](https://www.youtube.com/watch?v=bz04kTQD9xI) / [DoorDash](https://www.appliedcompute.com/case-studies/doordash) / [Cognition](https://www.appliedcompute.com/case-studies/cognition) / [Modal sandbox](https://modal.com/docs/guide/sandboxes)

---

# 영상 4. Stanford MS&E435: Enterprise Internal Knowledge

Yash Patil, Apoorv Agrawal / Stanford 세션 2026-05-08 / YouTube 업로드 2026-05-22 / 48:10

## #RLDR

1. AlexNet, Transformer, pretraining, RLHF, RLVR의 역사를 enterprise AI로 연결합니다.
2. 공개 text 다음의 학습 데이터는 verifier가 있는 experience입니다.
3. Specialized model의 가치는 절대 성능보다 업무별 quality, latency, cost를 맞추는 데 있습니다.
4. DeepSeek R1의 147K H800 GPU-hours는 RL 한 단계가 아니라 보고서 합계입니다.

## 00:00 표현 학습에서 reasoning으로

Transformer의 병렬성과 next-token prediction이 scale을 가능하게 했고 SFT와 RLHF가 행동을 다듬었습니다. o1 이후에는 test-time compute와 RL이 reasoning을 길게 만듭니다. Chain of thought를 사람이 규칙으로 직접 코딩하지 않았다고 말할 수는 있지만, 아무도 훈련하지 않았는데 저절로 생겼다는 표현은 과장입니다.

## 14:00 RLVR은 채점하는 방식의 변화다

Math와 code처럼 정답이나 test를 확인할 수 있는 문제는 여러 trajectory를 만들고 verifier로 선별할 수 있습니다. 인터넷 pretraining data가 모두 고갈됐다는 말은 확정된 사실이 아니라 data wall 가설입니다.

자동자막의 TreeBench는 문맥상 SWE-bench입니다. 초기 SWE-bench는 12개 Python repository의 2,294개 실제 software engineering task로 구성됐습니다.

## 26:00 기업별 model은 frontier보다 작아도 된다

DoorDash의 공식 수치는 수천 merchant, 중요 메뉴 오류의 상대적 30% 감소, 1,000시간 이상 절약입니다. 영상의 연간 10만 merchant는 공식 case study에서 확인되지 않습니다.

DeepSeek V3 보고서 총학습은 2.788M H800 GPU-hours입니다. R1 보고서 합계는 147K이고 R1-Zero, SFT data generation, R1 training을 포함합니다. R1 단계만 약 41K입니다. 147K가 V3 전체의 5.3%라는 계산은 가능하지만 이를 R1 RL 비용으로 부르면 단위가 섞입니다.

## 35:00 Online signal과 model routing

기업은 task마다 다른 model을 route할 수 있습니다. Cursor는 실제 interaction을 reward로 쓰는 real-time RL에서 약 5시간마다 새 checkpoint를 만들 수 있다고 설명했습니다. 모든 모델이 고정 5시간 주기로 production에 자동 반영된다는 뜻은 아닙니다.

## 43:00 Compute supercycle의 경계

NVIDIA 75%는 FY2025 GAAP gross margin으로 확인되지만 순이익률이나 GPU 한 개의 margin으로 일반화할 수 없습니다. Energy, robotics, egocentric data, 모든 문제의 coding problem 환원은 투자 관점과 전망입니다.

[영상](https://www.youtube.com/watch?v=LRGX-gTegVA) / [DeepSeek V3](https://arxiv.org/abs/2412.19437) / [DeepSeek R1](https://arxiv.org/abs/2501.12948) / [SWE-bench](https://arxiv.org/abs/2310.06770)

---

# 영상 5. Own or Be Owned

Yash Patil / The Generalist / 1:08:06

## #RLDR

1. 모든 회사가 foundation model을 처음부터 만들라는 말이 아닙니다. 자기 eval, workflow, feedback을 쌓은 specialized model을 소유하자는 주장입니다.
2. Data가 많아도 좋은 결과를 측정하지 못하면 학습할 수 없습니다.
3. Model ownership은 cost와 latency뿐 아니라 provider policy 의존을 줄이는 수단입니다.
4. AI 의존이 cognitive atrophy를 만든다는 결말은 연구 결과가 아니라 founder의 문제 제기입니다.

## 03:50 Model policy가 회사의 capability를 바꾼다

Anthropic의 Fable 5, Mythos 5, Project Glasswing을 model ownership의 근거로 듭니다. 공식 범위는 더 좁습니다. Fable 5는 cyber, biology/chemistry, distillation 관련 session에 Opus 4.8 fallback을 적용하며 95% 이상의 session은 fallback 없이 처리된다고 밝혔습니다. 모든 AI 연구를 억제한다고 일반화할 수 없습니다.

## 09:22 Foundation model부터 만들 필요는 없다

Open-weight model과 고객 data, eval, workflow를 결합합니다. Yash는 Stanford 프로젝트와 TreeHacks, 약 1년 반 뒤 학교를 떠나 OpenAI에 합류한 자기 서사를 설명합니다. 진행자의 recent Stanford grad 소개와 본인의 중퇴 설명이 다르므로 졸업생으로 단정하지 않습니다.

## 19:29 OpenAI에서 배운 것은 eval이었다

OpenAI Residency, post-training, reasoning, agentic coding 경험을 설명합니다. Sam Altman 해임 당시의 현장 묘사는 개인 증언이며 해임과 복귀 일정 자체만 공식 발표로 확인됩니다.

좋은 업무 결과를 정의하는 eval이 model development의 시작이라는 결론으로 모입니다. Chain of thought도 RL로 학습되고 개선된 reasoning behavior로 한정합니다.

## 35:39 No one is data ready

Raw document와 log가 있다는 것과 학습 가능한 task, outcome, reward가 있다는 것은 다릅니다. DoorDash 영상의 연간 10만 merchant는 공식 case study에서 확인되지 않습니다. 확인 가능한 범위는 수천 merchant, 30% relative menu error 감소, 1,000시간 이상 절약입니다.

Applied Compute의 사업은 AC2, dedicated inference, FDE와 Applied Research Engineer, managed training과 serving을 묶은 hybrid model입니다. 현장 밀착은 강점이면서 scale과 margin의 부담입니다.

## 45:55 Deployment 뒤에 학습이 시작된다

Production interaction을 다음 checkpoint의 data로 만들고 task별로 specialized model과 frontier model을 route합니다. Chinese open model과 미국 frontier lab의 우위는 인터뷰의 전망입니다.

## 51:25 회사 문화, compute, 인간의 사고

팀의 약 3분의 2가 former founder라는 말은 회사 공식 소개와 일치합니다. 근무시간, 자체 GPU, 내부 문화는 자기보고이거나 공개 확인이 부족합니다. Compute shortage, 2년 내 일자리 절반 소멸 가능성, AI coding이 사고 능력을 약화시킨다는 주장은 전망과 해석입니다.

Product evidence는 case study와 system design으로 평가하고 founder worldview는 토론할 가설로 남겨야 합니다.

### 자막 교정

- Project class wing은 Project Glasswing
- Fable 5의 safety fallback은 특정 고위험 session 범위
- Yash의 학력은 본인의 중퇴 설명을 우선
- Cursor는 checkpoint를 약 5시간마다 만들 수 있다고 했으며 고정 production update를 보장하지 않음

[영상](https://www.youtube.com/watch?v=B-MxM-OqON8) / [The Generalist transcript](https://www.generalist.com/p/own-or-be-owned-why-every-company) / [Anthropic Fable 5](https://www.anthropic.com/news/claude-fable-5-mythos-5) / [Cursor real-time RL](https://prod.cursor.com/blog/real-time-rl-for-composer)

---

## 주요 출처

- [Applied Compute](https://www.appliedcompute.com/)
- [It's time to get specific](https://www.appliedcompute.com/company/its-time-to-get-specific)
- [The Advantage You Own](https://www.appliedcompute.com/company/fundraise)
- [Applied Compute Agent Cloud](https://www.appliedcompute.com/platform/introducing-ac2)
- [Remember, Refine, Retrieve](https://www.appliedcompute.com/research/remember-refine-retrieve)
- [Harvey Tenet Research Preview](https://www.harvey.ai/blog/post-training-update-harvey-tenet)
- [Harvey Review Table with Applied Compute](https://www.harvey.ai/blog/training-frontier-review-table-models-with-applied-compute)
- [Satya Nadella conversation](https://www.youtube.com/watch?v=g_iUdhxpc4k&t=2s)
