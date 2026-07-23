# Environment Foundry V2 — 발표자 스크립트

## 1. 아직 하나의 점수가 아니다

오늘 답하려는 질문은 단순합니다. “진짜 회사를 운영하는 AI”를 재는
benchmark가 있는가? 결론부터 말하면, 부분은 있지만 전체를 방어 가능한
한 점수로 재는 benchmark는 찾지 못했습니다. 그래서 논문 표가 아니라
실제 repository와 dataset 파일을 열었습니다.

## 2. Capability ladder

Tool call, bounded workflow, cross-functional operation, judgment, longitudinal
company outcome을 분리해야 합니다. 아래 단계에서 높은 점수가 위 단계를
증명하지 않습니다. 특히 simulated multi-app surface는 real business
outcome evidence가 아닙니다.

## 3. 직접 확인한 artifact

TheAgentCompany에는 175개 task directory가 있었습니다. CRMArenaPro에는
4,280개의 query가 있습니다. 세 upstream에서 세 episode씩 직접 decode해
9개 모두 공통 schema validator를 통과시켰습니다.

## 4. 세 후보의 차이

CRMArenaPro는 실제 Salesforce 형태를 닮았지만 공개 execute action은
query 중심이고 reset이 org를 복구하지 않습니다. TheAgentCompany는
여러 app과 evaluator가 있는 Docker task입니다. Gaia2는 scheduled event와
scenario re-import가 있습니다. 라이선스와 reset semantics도 달라 점수를
같은 leaderboard처럼 비교하면 안 됩니다.

## 5. Episode 계약

Episode는 prompt가 아닙니다. Task, initial state, typed action, grader,
reset/replay provenance가 있어야 합니다. 원본 payload를 그대로 보존하고,
비교에 필요한 최소 필드만 normalization 했습니다.

## 6. Qwen 실행 결과

Qwen2.5 0.5B를 Apple M5에서 12 step LoRA SFT했습니다. 5.4초, peak
1.281GiB, 추가 비용은 0달러였습니다. Frozen test에서 JSON parse는
0에서 100%로, hard failure는 100에서 0%로 좋아졌지만 정답 decision은
0% 그대로였습니다. Loss 감소를 회사 판단 능력 향상으로 부르면 안 됩니다.

## 7. 학습 데이터의 역할

SFT trace는 모방, preference는 ranking, verifier는 reward, outcome
trajectory는 뒤늦은 결과, rollout은 transition, RLVR은 verified reward
update를 제공합니다. 각자 해결하는 문제가 다릅니다. 지금 규모에서는
RLVR보다 grader와 data coverage가 먼저입니다.

## 8. 두 사업 경로

첫 경로는 기존 benchmark 점수를 올리는 adapter·rollout·verifier
공급자입니다. 빨리 증명할 수 있지만 moat가 약합니다. 둘째는
rights-valid company-operation category입니다. 더 차별화되지만
validity 비용이 높습니다. 두 경로를 동시에 열지 않습니다.

## 9. 30일 wedge

한 low-risk decision을 freeze하고, 20개 이상 rights-valid shadow
episode를 모읍니다. Human-only, generic model, retrieval/harness,
environment policy를 frozen setting에서 비교합니다. 마지막에는 delayed
outcome과 held-out operator transfer를 닫습니다. Simple baseline tie,
unstable ranking, no outcome, no transfer 중 하나면 중단하거나 redirect합니다.

## 10. 의사결정

새 category를 선언할 단계가 아닙니다. 지금 승인할 것은 benchmark
marketing이 아니라 한 decision environment를 반증하는 capture design입니다.
유료 API와 GPU는 episode·turn·token budget을 먼저 고정한 뒤 별도 승인받습니다.
