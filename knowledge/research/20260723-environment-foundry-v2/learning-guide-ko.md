# 회사 운영 AI 벤치마크 3층 학습 가이드

## 1층 — 고등학생에게

AI에게 회사를 운영시킨다는 것은 “메일 보내기 버튼을 잘 누르나?”만 보는
문제가 아니다.

축구로 비유하면 이렇다.

- 버튼을 누르는 것은 패스를 한 번 정확히 하는 시험이다.
- 한 업무를 끝내는 것은 세트피스를 성공시키는 시험이다.
- 여러 팀과 도구를 넘나드는 것은 실제 한 경기를 운영하는 시험이다.
- 불확실한 상황에서 사람과 돈을 고려하는 것은 감독의 판단 시험이다.
- 몇 달 뒤 회사가 좋아졌는지는 한 시즌의 결과다.

지금 공개된 최고의 시험도 대체로 “한 경기”까지다. 실제 고객 신뢰,
재구매, 직원 이탈, 현금흐름이 몇 달 뒤 어떻게 바뀌었는지까지 보는 공개
시험은 거의 없다.

실제 CRMArenaPro 데이터 한 줄은 대략 다음 모양이다.

```json
{
  "idx": 0,
  "task": "lead_qualification",
  "query": "이 리드는 자격이 있는가?",
  "metadata": {"required": "통화 기록과 정책을 확인"},
  "persona": "품질을 중시하는 사용자",
  "answer": ["Authority"],
  "reward_metric": "exact_match"
}
```

이 한 줄은 좋은 시험 문제지만, 회사의 한 달이 담긴 기록은 아니다.

## 2층 — 창업자에게

사업 기회는 “기업 데이터가 많다”가 아니다. 다음 계약을 반복해서 만들 수
있는가다.

```text
권리가 명확한 사건
→ 의사결정 당시 관찰
→ 허용 행동과 안전 경계
→ 실제 상태 변화
→ 즉시·지연 결과
→ 독립 grader
→ held-out 재검증
```

공개 benchmark 공급자로 가면 빠르게 기존 점수에 기여할 수 있지만,
차별화는 task 품질과 verifier 견고성에 갇힌다. 새로운 company-operation
category를 만들면 훨씬 어렵지만, “실제 결과를 닫는 능력”이 해자가 될 수
있다.

현재 가장 좋은 30일 wedge는 회사 전체가 아니라 하나의 낮은 위험
의사결정이다. 예: 이벤트 후 약속의 owner/due date/evidence를 정리하고,
사람이 발송 전에 승인하며, 7/30일 뒤 실제 이행 여부를 회수한다.

죽이는 기준은 간단하다. generic model + retrieval + 좋은 workflow보다
성과가 낫지 않거나, 결과 회수 비용이 절감액보다 크거나, 권리 계약이
학습·평가 사용을 허용하지 않으면 environment supplier 가설을 닫는다.

## 3층 — ML 엔지니어에게

Normalized episode V2는 원본을 대체하지 않는다. upstream raw row와
revision을 보존하면서 다음 인터페이스를 추가한다.

```text
source/split
task
observation boundary
typed action space
transition + reset semantics
termination/truncation
grader + hidden reference
rights
raw_ref + provenance
limitations
```

학습 데이터는 benchmark test row가 아니다.

| 데이터 | 입력 | 출력 | 용도 | 핵심 위험 |
|---|---|---|---|---|
| SFT trace | 관찰·도구 결과 | 좋은 다음 행동/응답 | 형식·정책·기본 전략 학습 | 한 정답 모방, test leakage |
| Preference | 같은 상태의 후보 쌍 | 선호/거부 | taste·safety·trade-off | annotator policy를 진실로 오인 |
| Verifier data | trajectory + state | grade/failure vector | reward model·grader 보정 | reward hacking |
| Outcome trajectory | 당시 관찰→행동→나중 결과 | attribution + uncertainty | delayed outcome 예측 | 한 정책 경로, confounding |
| Environment rollout | reset state + policy | 여러 trajectory와 reward | exploration/RL | simulator bias |
| Synthetic curriculum | task generator | 난이도별 tasks | coverage 확대 | generator artifact |
| RLVR | prompt/state | verifiable reward가 있는 rollout | verifier가 강할 때 policy 개선 | benchmark 최적화, 좁은 reward |

현재 artifact에는 SFT가 RLVR보다 정당하다. 이유는 공개 CRMArenaPro row가
정적 task specification이고 local adapter가 Salesforce transition을
재현하지 않기 때문이다. 정답 형식과 정책 거부를 학습하는 SFT toy run은
정직하지만, 이를 “회사 운영 RL”이라고 부를 수 없다.

최소 실험은 다음을 한 episode에서 눈으로 보여줘야 한다.

```text
system/user chat template
→ Qwen tokenizer
→ causal LM logits
→ target token cross-entropy
→ optimizer step
→ 같은 prompt의 output
→ deterministic format/policy grader
```

loss 감소만으로 정책이 좋아졌다고 말하지 않는다. frozen held-out episode,
task reward, hard failure, abstention calibration을 함께 본다.
