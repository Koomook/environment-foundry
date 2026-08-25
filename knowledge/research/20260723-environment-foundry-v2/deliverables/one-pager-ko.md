# Environment Foundry V2 — one-pager

## 한 문장

공개 benchmark는 multi-app simulated work와 policy-sensitive workflow까지
측정하지만, rights-valid real-company decision과 delayed outcome을 함께
측정하지 못한다. Environment Foundry의 기회는 그 빈 공간을 prospective
evidence로 검증하는 데 있다.

## 이번에 실제로 확인한 것

- CRMArenaPro, TheAgentCompany, Gaia2의 pinned code/data를 로컬 검사했다.
- upstream row/episode 3개씩, 총 9개를 decode했고 공통 schema validation
  9/9를 통과했다.
- loader, offline adapter, baseline, evaluator, CLI와 tests를 구현했다.
- Qwen2.5-0.5B LoRA SFT를 Apple M5에서 실행했다: 5.40초, 1.281GiB peak,
  추가비용 $0.
- Frozen test에서 parse validity는 0→1, hard failure는 1→0이었으나
  exact decision accuracy는 0→0이었다. 이는 format recovery이지 판단
  향상이 아니다.

## 무엇을 주장하지 않는가

- Simulated L3 surface를 real-company proof로 부르지 않는다.
- Historical log만으로 delayed causal credit를 해결했다고 하지 않는다.
- Public benchmark test data를 학습에 넣고 “성능 향상”이라 하지 않는다.
- Loss 감소를 policy 또는 business outcome lift로 바꾸어 말하지 않는다.

## 두 사업 경로

1. 기존 benchmark 개선 공급자: adapter, rollout, verifier. 빠른 demo,
   낮은 validity burden, 약한 moat.
2. company-operation environment category: rights, replay, grader, prospective
   outcome. 높은 차별성, 높은 proof cost.

추천은 30일 동안 두 번째 경로의 최소 단위를 반증하는 것이다.

## 30일 wedge

- D1–5: low-risk decision task, rights, decision-time cutoff, typed action,
  grader를 freeze한다.
- D6–15: 최소 20개 rights-valid shadow episode를 capture한다.
- D16–23: human-only, generic model, retrieval/harness, environment policy를
  동일한 held-out setting에서 비교한다.
- D24–30: delayed outcome을 닫고 held-out operator transfer를 측정한다.

Kill gate: simple baseline tie, unstable ranking, outcome closure 실패,
held-out transfer 실패.

## 승인 경계

공개 코드와 공개 synthetic adapter는 release 가능하다. 민감 데이터
업로드와 유료 API/GPU 지출은 승인되지 않았으며 별도 spend gate가 필요하다.
