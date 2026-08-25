# 진짜 회사를 운영하는 AI는 어떻게 측정할까

진행자: 안녕하세요. 이 팟캐스트의 두 목소리는 모두 인공지능으로 생성되었습니다. 오늘 질문은 꽤 도발적입니다. 이메일을 보내고 CRM을 조회하는 AI가 아니라, 사람이 보기에 “회사를 운영한다”고 할 만한 AI를 우리는 실제로 측정할 수 있을까요?

연구자: 쉬운 비유부터 해보죠. 계산기 시험에서 만점을 받은 학생이 곧바로 회사를 잘 운영하는 CEO는 아닙니다. 도구를 정확히 쓰는 능력, 여러 업무를 끝내는 능력, 불확실한 상황에서 판단하는 능력, 그리고 그 판단이 몇 달 뒤 매출과 신뢰에 어떤 결과를 남기는지는 서로 다른 층입니다. 이번 연구의 첫 결론은 이 층들을 한 점수로 뭉치면 안 된다는 것입니다.

진행자: 그렇지만 요즘 agent benchmark가 굉장히 많습니다. 툴을 호출하고, 웹을 쓰고, 코드를 짜고, 여러 앱을 오가는 benchmark도 있잖아요. “없다”는 결론을 먼저 정해놓고 찾은 것 아닌가요?

연구자: 그래서 논문 표만 읽지 않았습니다. CRMArenaPro, TheAgentCompany, Gaia2라는 세 후보의 실제 repository와 dataset을 내려받았습니다. 각 source에서 세 episode씩 직접 열어 schema를 확인했고, 총 아홉 개를 공통 normalized episode schema로 변환했습니다. 아홉 개 모두 validator를 통과했습니다. 즉, 이름이나 마케팅 문구가 아니라 실제 파일과 코드의 reset, action, grader를 근거로 판단했습니다.

진행자: 그 공통 schema라는 게 또 억지로 이름만 맞춘 형식일 수 있죠. 원래 benchmark가 가진 정보를 잃어버리면 비교가 의미 없지 않습니까?

연구자: 맞습니다. 그래서 원본 payload는 그대로 보존하고, 비교 가능한 최소 계약만 밖으로 뽑았습니다. Task objective와 policy, initial observation과 state reference, typed action space, grader와 terminal condition, reset semantics와 source revision입니다. Episode는 prompt 한 줄이 아니라 이 여섯 가지가 함께 있는 실행 계약입니다. 원본을 버리고 평평한 instruction-answer JSON으로 바꾸지 않았습니다.

진행자: 그럼 capability ladder를 구체적으로 설명해주시죠. 단계가 많으면 결국 복잡한 말로 도망가는 것처럼 들릴 수 있습니다.

연구자: 다섯 단계입니다. 첫째, tool call입니다. 올바른 API와 argument, authorization을 보는 단계죠. 둘째, bounded workflow입니다. 여러 관찰과 행동을 거쳐 정의된 일을 끝내는가를 봅니다. 셋째, cross-functional operation입니다. 여러 앱과 상태, 동료 역할, 시간 의존성을 함께 다룹니다. 넷째, judgment under uncertainty입니다. 정보가 불완전할 때 정책, 인간 관계, 위험과 abstention을 어떻게 다루는지 봅니다. 다섯째, longitudinal company outcome입니다. 판단 뒤의 매출, 신뢰, 피해, 생존, 미래 기회가 어떻게 바뀌었는지를 봅니다.

진행자: 단계가 높다고 아래 단계가 자동으로 포함됩니까?

연구자: Agent surface라는 의미에서는 누적적으로 설계할 수 있지만, 증거는 자동으로 누적되지 않습니다. 특히 simulated multi-app task에서 성공했다고 실제 회사의 장기 결과를 예측한다고 말할 수 없습니다. 이번 연구에서 자주 쓰는 문장은 이겁니다. “L3 simulated surface는 Gate 3 business evidence가 아니다.”

진행자: CRMArenaPro부터 보죠. Salesforce라는 실제 기업용 제품 위에서 움직이니 가장 회사 운영에 가까운 것 아닙니까?

연구자: 실제 제품 표면을 닮았고, 데이터도 상당히 구체적입니다. 공개 B2B JSON에 2,140행, B2C에 2,140행이 있고, 논문은 4,280개의 unique query를 보고합니다. 19개 task와 confidentiality 항목이 있고, 공개 환경의 action은 Salesforce query를 실행하는 execute와 최종 답을 내는 respond입니다. 하지만 중요한 한계가 있습니다. 검사한 execute 경로는 읽기 중심이고, ChatEnv reset은 task와 action history를 바꾸지만 공유 Salesforce org 자체를 원상복구하지 않습니다. 완전한 mutable business simulator라고 부르기 어렵습니다.

진행자: 게다가 라이선스도 걸리죠?

연구자: 그렇습니다. 코드와 데이터의 공개 repository에는 research-only 문구가 있고, dataset은 CC BY-NC 4.0입니다. 연구와 비교에는 유용하지만 상업적 seed asset으로 그대로 사용할 수 없습니다. 라이선스는 모델 성능과 별개의 제품 제약입니다.

진행자: TheAgentCompany는 어떤가요?

연구자: 이것은 simulated software company에 가깝습니다. 검사한 repository에는 175개의 task directory가 있었습니다. RocketChat, GitLab, Plane, OwnCloud, 파일과 shell 같은 여러 surface를 씁니다. 각 task에 evaluator가 있고 Docker task image가 초기 상태를 준비합니다. 그래서 cross-app operation을 테스트하기에는 CRMArenaPro보다 강한 부분이 있습니다. 하지만 여전히 한 task 안의 synthetic company입니다. 실제 회사의 제도적 역사나 몇 달 뒤 경제적 결과를 관찰하지 않습니다.

진행자: Gaia2는 scheduled event가 있다는 점이 다르다고 들었습니다.

연구자: 맞습니다. 공개 mini validation Parquet에는 160행이 있고, 각 data cell 안에 전체 JSON scenario와 app state, scheduled event가 들어 있습니다. 첫 번째로 decode한 scenario에는 scheduled event가 14개 있었습니다. Scenario JSON을 다시 import할 수 있어 reset 의미도 더 강합니다. 다만 이것 역시 synthetic scenario이고 leaderboard는 self-reported입니다. Judge calibration과 real outcome은 별도 문제입니다.

진행자: 현재 점수는 어떻게 비교했습니까? 투자자라면 누가 제일 높은지 궁금할 텐데요.

연구자: 비교하지 않았습니다. CRMArenaPro의 single-turn과 multi-turn, TheAgentCompany의 resolved와 score, Gaia2의 pass@1은 interaction mode, split, harness, grader가 다릅니다. 숫자만 한 차트에 올리는 순간 잘못된 leaderboard가 됩니다. 예를 들어 CRMArenaPro 논문 설정의 Gemini 2.5 Pro B2C single-turn All과 multi-turn All은 서로 다른 setting입니다. Gaia2의 공식 leaderboard 코드에 있는 점수도 self-reported라는 조건을 함께 기록해야 합니다.

진행자: 그러면 기업들은 실제로 어떤 전략을 공개하고 있습니까? OpenAI, Anthropic, Google, Microsoft, NVIDIA, Salesforce, Sierra, Palantir까지 모두 같은 environment 전쟁을 하는 건가요?

연구자: 공개 증거상 그렇지 않습니다. OpenAI는 PaperBench 같은 환경과 grader를 공개하고, 채용 공고에서도 agent post-training, frontier evals, environments를 하나의 feedback loop로 연결합니다. Anthropic은 Bloom으로 behavioral evaluation을 자동 생성하고 contamination을 명시적으로 경고하며, production telemetry에서는 privacy-preserving autonomy 측정을 합니다. NVIDIA의 NeMo Gym은 가장 명시적입니다. Environment를 dataset, agent harness, verifier, per-task state로 정의하고 rollout collection에서 SFT, DPO, RL로 이어지는 공개 도구와 tutorial을 제공합니다.

진행자: 나머지는요?

연구자: Salesforce는 CRMArena를, Sierra는 tau-bench와 그 확장을 공개해 policy와 state가 있는 customer-service evaluation을 만듭니다. Palantir의 공개 AIP Evals는 production function test, exact 또는 LLM judge, repeated run, trace, model과 prompt grid search에 가깝습니다. Microsoft는 외부 상태가 계속 바뀌는 monitoring agent benchmark를 공개했습니다. Google DeepMind는 interactive agent evaluation과 world model research를 공개하지만, 우리가 검사한 자료만으로 business-process environment가 production model post-training에 어떻게 섞이는지는 알 수 없습니다. 공개되지 않은 내부 전략은 추측으로 표시해야 합니다.

진행자: 이제 학습으로 넘어가죠. “benchmark 점수를 올리는 데이터”란 실제로 무엇입니까?

연구자: 최소 여섯 종류를 구분해야 합니다. SFT trace는 observation과 tool history에서 expert next action을 모방합니다. Preference data는 같은 context에서 두 rollout의 순위를 배웁니다. Verifier는 task와 rollout을 scalar나 vector reward로 바꿉니다. Outcome trajectory는 decision-time state와 action 뒤의 delayed consequence를 연결합니다. Interaction rollout은 reset state에서 action과 observation의 연속을 수집합니다. Synthetic curriculum은 difficulty를 통제해 새 train task를 만듭니다. RLVR은 반복 rollout의 verifiable reward로 policy를 업데이트합니다.

진행자: 결국 RLVR이 가장 강력해 보이는데 왜 이번에는 하지 않았나요?

연구자: RL이라는 이름을 붙이는 것보다 reward가 믿을 만한지가 먼저입니다. 현재 public synthetic train projection은 16개뿐입니다. 이 규모에서는 policy gradient의 안정적인 효과를 주장하기 어렵고, reward hacking과 seed variance를 키울 가능성이 큽니다. 그래서 prompt-masked LoRA SFT만 실행했습니다. Dev는 monitoring에 쓰고 frozen test는 마지막 측정에만 썼습니다. Public benchmark test data는 학습에 넣지 않았습니다.

진행자: 실행 결과를 숫자로 말해주시죠.

연구자: Qwen2.5-0.5B-Instruct의 revision을 고정했습니다. Apple M5, 32기가 unified memory에서 MLX-LM으로 두 layer LoRA, batch 1, learning rate 1e-5, 12 iteration을 돌렸습니다. Training wall time은 5.40초, peak memory는 1.281기가바이트, 추가 비용은 0달러였습니다. Adapter의 SHA-256도 receipt에 남겼습니다.

진행자: 성능은 좋아졌습니까?

연구자: 반은 좋아졌고 핵심은 안 좋아졌습니다. Base model은 frozen dev와 test에서 valid JSON을 하나도 만들지 못했고 hard failure rate가 100퍼센트였습니다. SFT 뒤에는 parse validity가 100퍼센트가 되고 hard failure는 0퍼센트가 됐습니다. 그러나 exact action match와 decision category accuracy는 0퍼센트 그대로였습니다. 형식과 safe serialization은 회복했지만 올바른 판단은 배우지 못했습니다.

진행자: Loss는 내려갔나요?

연구자: Training loss는 첫 iteration 4.000에서 마지막 1.334로, dev loss는 5.547에서 4.069로 내려갔습니다. 하지만 loss 감소는 optimization evidence일 뿐 policy evidence가 아닙니다. 이 negative result를 지우지 않는 것이 중요합니다. 작은 모델이 JSON을 잘 쓰게 된 것과 회사를 잘 운영하게 된 것은 완전히 다른 주장입니다.

진행자: 비용 관점에서는 어떻습니까? 더 큰 Qwen을 GPU로 돌리면 바로 답이 나오지 않을까요?

연구자: 7B QLoRA 정도는 24기가 GPU 한 장에서도 가능하지만, 데이터가 16개라면 GPU를 키우는 것이 핵심 병목을 해결하지 않습니다. 2026년 7월 23일 공식 가격 기준으로 A100 80기가는 Hugging Face에서 시간당 2.50달러, Modal은 초당 요금을 환산하면 약 2.50달러입니다. H100 80기가는 RunPod PCIe 2.89달러, Lambda PCIe 3.29달러, Modal 약 3.95달러 수준입니다. NVIDIA의 9B GRPO reference tutorial은 80기가 GPU 여덟 장과 3에서 5시간을 요구합니다. 지금 그 비용을 쓰는 것은 정당하지 않습니다.

진행자: 유료 API model과 비교는 왜 하지 않았습니까?

연구자: 사용자가 유료 API와 외부 GPU 지출은 승인하지 않았기 때문입니다. 먼저 episode 수, 최대 turn, input과 output token, tool fee, retry ceiling을 고정해 비용을 계산한 뒤 승인받아야 합니다. 이번에는 무료 local dry run과 negative control까지만 실행했습니다.

진행자: 이제 사업 가설을 정면으로 보죠. 한국과 일본 기업의 운영 사건을 rights-valid RL environment로 compile하면 frontier lab에 가치가 있을까요?

연구자: 지지하는 근거는 있습니다. Public benchmark가 실제 enterprise data 부족을 명시하고, NVIDIA와 OpenAI가 environment와 grader를 post-training loop의 중요한 구성요소로 공개하고 있습니다. 한국과 일본의 언어, 제도, 관계 맥락이 generic benchmark에 덜 담겨 있을 가능성도 있습니다. 하지만 반대 근거가 더 중요합니다. 기업의 차이는 model weight가 아니라 private retrieval, workflow, distribution, customer relationship, eval harness에 남을 수 있습니다. 그리고 historical log만으로는 counterfactual이나 delayed causal credit을 해결하지 못합니다.

진행자: 그럼 이 사업의 빈 공간을 어떻게 정확히 정의합니까?

연구자: 기존 benchmark가 놓치는 것은 세 가지의 결합입니다. 첫째, decision-time에 권리와 동의가 유효한 observation. 둘째, authority와 policy가 명시된 replayable action environment. 셋째, 나중에 닫히는 real outcome으로 offline grader ranking을 검증하는 prospective loop입니다. 데이터셋만 있거나 synthetic simulator만 있는 것으로는 부족합니다.

진행자: 사업 경로는 둘이라고 했죠?

연구자: 첫째는 기존 benchmark 점수를 올리는 공급자입니다. Adapter, rollout, verifier, harness optimization을 제공합니다. Demonstration이 빠르고 고객과 대화하기 쉽지만 proprietary moat가 약할 수 있습니다. 둘째는 새로운 company-operation environment category입니다. Rights, replay, grader, prospective outcome을 함께 공급합니다. 차별성은 크지만 validity와 판매 비용이 높습니다.

진행자: 어떤 길을 추천합니까?

연구자: 지금은 둘째 길의 가장 작은 단위를 30일 안에 반증하는 것을 추천합니다. Category를 크게 선언하는 게 아니라, low-risk decision task 하나를 선택합니다. 반복성, rights, decision-time cutoff, typed action, delayed outcome이 있는 task여야 합니다.

진행자: 30일 계획을 구체적으로 말해보죠.

연구자: 첫 5일에는 task contract, rights, observation cutoff, grader를 freeze합니다. 6일에서 15일까지 최소 20개의 rights-valid shadow episode를 capture합니다. 16일에서 23일까지 human-only, generic model, retrieval 또는 harness, environment-trained 혹은 rehearsed policy 네 arm을 같은 held-out setting에서 비교합니다. 24일에서 30일에는 delayed outcome을 닫고 다른 operator에게 transfer되는지 봅니다.

진행자: Kill gate는 무엇입니까? 실패해도 계속 “데이터가 더 필요하다”고 말할 수 있잖아요.

연구자: 네 가지입니다. Simple baseline과 동률이면 중단하거나 redirect합니다. Offline ranking이 seed나 grader 변화에 따라 불안정하면 중단합니다. Delayed outcome을 닫을 수 없으면 simulator claim을 중단합니다. Held-out operator transfer가 없으면 company-general asset이라는 주장을 중단합니다. “어렵다”가 계속할 이유가 되어서는 안 됩니다.

진행자: 마지막으로 지금 알게 된 사실, 아직 모르는 것, 다음 반증 실험을 한 문장씩 정리해주시죠.

연구자: 알게 된 사실은 공개 benchmark가 multi-app state, simulated colleague, temporal event, privacy policy와 executable grader까지는 실제로 제공한다는 것입니다. 아직 모르는 것은 rights-valid 한국 또는 일본의 operating context가 generic model plus retrieval and harness를 실제 outcome에서 이기는가입니다. 다음 반증 실험은 한 decision environment를 freeze하고 최소 20개의 prospective shadow episode로 네 arm을 비교하는 것입니다.

진행자: 그러면 오늘의 결론은 “새 benchmark가 있다”도 아니고 “없으니 우리가 만들면 된다”도 아니군요.

연구자: 맞습니다. 새 benchmark를 선언하지 말고, 한 decision environment를 반증해야 합니다. 그 실험이 prospective lift와 transfer를 보여줄 때만 category와 사업을 확장합니다. 그 전까지 buyer demand, live validity, outcome lift, transfer는 모두 아직 증명되지 않았습니다.

진행자: 오늘은 실제 파일, 실행된 작은 모델, 그리고 실패를 포함한 증거로 “회사를 운영하는 AI”의 측정 문제를 살펴봤습니다. 유료 compute보다 먼저 필요한 것은 더 큰 문장이 아니라 더 좋은 episode와 더 엄격한 kill gate라는 결론입니다. 들어주셔서 감사합니다.
