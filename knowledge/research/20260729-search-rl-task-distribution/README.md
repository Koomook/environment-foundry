# Search RL에서 환경과 질문 분포가 함께 만드는 학습 행동

작성일: 2026-07-29

상태: 발산 연구 / 공개 출처 / 비정본

연결 워크스트림: EF-02 Environment compiler

## 한눈에 보는 결론

Trillion Labs의 Search RL 사례는 검색 백엔드나 코퍼스를 로컬에 복제하는
것만으로는 실제 환경에 전이되는 정책을 만들 수 없다는 유용한 사례다.
학습 환경에서 어떤 질문과 태스크를 풀게 하는지가 어떤 행동을 연습하고
보상받는지를 결정한다.

그러나 이 사례를 `좋은 질문 세트만 만들면 전이가 생긴다`는 증거로 읽으면
안 된다. SearchGym에서 Simulated Scholar Search(S3)로 바뀌는 동안
코퍼스의 규모와 성격, 검색 도구, 질문 분포, reward/judge가 함께 바뀌었다.
현재 공개 결과는 다음의 공동 설계 가설을 지지하는 예비 증거다.

> `HYPOTHESIS`: 실제 환경에서 유효한 행동이 시뮬레이션 안에서도
> 유리하도록 observation/action surface, task distribution, grader를 함께
> 맞추면, 검색 결과 자체를 똑같이 복제하지 않아도 일부 정책 행동이
> held-out search surface로 전이될 수 있다.

## 출처 영수증

### 핵심 출처

- 제목: 검색 엔진 없이 Deep Search RL하기
- 저자: 이세규, 석주영
- 게시자: Trillion Labs Research
- 게시일: 2026-07-27
- 조회일: 2026-07-29
- URL:
  <https://blog.trillionlabs.co/posts/search-rl-without-search-engine/>
- 출처 성격: 연구팀의 자체 실험 보고와 해설
- 권리·보존 경계: 공개 URL과 내부 요약만 저장한다. 글 전문, 이미지,
  모델 가중치, 데이터셋 payload는 이 저장소에 복사하지 않는다.

### 교차검증 출처

- S3 공개 코드와 환경 구성:
  <https://github.com/trillion-labs/SimScholarSearch>
- S3 Qwen3-4B 모델 카드:
  <https://huggingface.co/trillionlabs/sim-scholar-qwen3-4b>
- S3 공개 데이터셋 카드:
  <https://huggingface.co/datasets/trillionlabs/SimScholar-RL>
- 원 SearchGym 논문:
  <https://aclanthology.org/2026.acl-long.848/>

## 글이 보고한 결과

### SearchGym 재현

- SearchGym 내부 reward는 상승했다.
- Trillion Labs가 평가한 Bamboogle, MuSiQue, GAIA 평균 성능은 학습
  초반 상승 뒤 하락했고, 일부 구간에서는 base model보다 낮았다.
- 연구팀은 약 3,600개 문서의 작은 검색 공간에서 넓은 쿼리와 반복 확인이
  보상되는 shortcut을 원인으로 제시했다.

이 결과는 `simulation reward 상승 = 실제 검색 능력 상승`으로 간주할 수
없다는 사례다. 다만 원 SearchGym 논문은 양의 sim-to-real transfer를
보고했으므로, Trillion Labs의 재현 결과 하나로 SearchGym 자체가
일반적으로 실패했다고 결론 내릴 수는 없다.

### S3

S3는 약 112만 편의 전산학 논문과 논문·본문 검색, 인용 탐색, 본문 읽기
등의 도구를 제공한다. 질문은 단순 조회뿐 아니라 다음 행동을 요구하도록
구성됐다.

- 검색어를 구체화해 후보를 좁힌다.
- 비슷하지만 틀린 문서를 비교한다.
- 본문의 수치와 설정을 확인한다.
- 인용·피인용 관계를 따라간다.
- 같은 결과를 반복 확인하는 대신 새로운 근거를 찾는다.

검색 행동에 직접 점수를 주기보다, 이런 행동을 해야 최종 답을 맞힐 수
있도록 질문과 환경을 구성했다는 점이 핵심이다.

### 실제 검색으로의 전이

글은 다음 결과를 보고한다.

| 학습 | 평가 | 보고된 변화 |
|---|---|---:|
| S3의 전산학 논문 로컬 검색 | Semantic Scholar API 기반 LitQA2 생물학 논문 검색 | Qwen3-4B `0.173 → 0.453`; Gravity 30B `0.347 → 0.480` |
| S3의 논문 검색 | Google Search 기반 GAIA web-only 103문항 | Gravity 30B `0.282 → 0.369` |

따라서 `OBSERVED`라고 부를 수 있는 범위는 **연구팀의 해당 평가 설정에서
실제 API와 다른 도메인으로 일부 성능 전이가 보고됐다**는 것이다. 모든
검색 환경으로 전이된다는 주장은 `NOT YET`이다.

## “검색 능력은 질문이 만든다”의 정확한 해석

질문은 단순한 콘텐츠 묶음이 아니라 policy가 최적화되는 상황의 분포다.
질문에서 정답 문서의 이름을 주면 직접 조회가 유리하다. 여러 조건,
본문에만 있는 세부 정보, 인용 관계를 단서로 주면 쿼리 수정, 후보 비교,
관계 탐색이 필요해진다.

따라서 질문 분포는 다음을 결정한다.

1. 어떤 상태를 구별해야 하는가.
2. 어떤 행동 순서가 reward를 얻는가.
3. 어떤 shortcut이 허용되는가.
4. 실패 뒤 복구와 중단 판단이 필요한가.
5. 학습된 행동이 held-out 환경에서도 유리할 가능성이 있는가.

보다 정확한 설계 단위는 다음과 같다.

```text
corpus와 observation surface
× typed action과 transition
× task/question distribution
× grader와 reward
× termination과 reset
→ 학습에서 유리해지는 policy behavior
```

## 증거의 한계와 모순

- **질문 단독 ablation이 없다.** SearchGym에서 S3로 가며 코퍼스 규모,
  합성 문서와 실제 논문의 차이, 검색 도구, 질문 유형, grader가 함께
  바뀌었다.
- **LitQA2 결과는 예비적이다.** 공개 모델 카드는 full-text subset
  `n=75`의 checkpoint curve를 본 뒤 step 120을 선택했으므로 unbiased
  final benchmark가 아니라 diagnostic result라고 명시한다.
- **능력 범위가 제한될 수 있다.** 같은 모델 카드에서 AstaBench
  paper-finder 성능은 대체로 평평했고, 향상이 QA-like task에 국한될 수
  있다고 밝힌다.
- **GAIA 표본이 작다.** web-only 103문항의 단일 비교이며 공개 글에는
  seed, 신뢰구간, 유의성 검정, paired error analysis가 없다.
- **독립 재현이 아니다.** S3 전이 결과는 현재 연구팀 자체 보고다.
- **SearchGym 원 논문과 재현 결과가 충돌한다.** 원 논문은 strong
  sim-to-real generalization을 보고했다. 원 논문의 후속 alignment 단계와
  Trillion Labs 재현 절차가 완전히 같은지는 블로그만으로 확인되지 않는다.

## Environment Foundry로의 번역

이 출처는 기존 정본의 `environment-not-data-asset`과
`episode-replay-simulator-boundary`를 바꾸는 새 정본 주장이 아니라,
EF-02 태스크 계약을 더 엄격하게 감사하게 만드는 연구 입력이다.

후보 적용:

1. 태스크 계약에 목표 행동과 금지 shortcut을 명시한다.
2. training episode distribution이 어떤 행동을 보상하는지 기록한다.
3. 같은 reward를 얻는 exploitative policy를 사전에 열거하고 시험한다.
4. frozen held-out task에서 policy ranking을 비교한다.
5. offline reward가 prospective live ranking을 예측하기 전에는
   `simulator`라고 부르지 않는다.

## 다음 반증 가능 게이트

EF-02가 첫 bounded task를 선택하면 최소 두 개의 task distribution을
동일한 observation/action/grader 위에서 비교한다.

- `A`: 쉽게 노출된 단서로 정답을 찾을 수 있는 분포
- `B`: 실제 업무에서 필요한 상태 구별, 근거 확인, 복구 또는 중단 판단을
  요구하는 분포

두 분포로 rehearsal 또는 학습한 정책을 frozen held-out episode와
prospective shadow outcome에서 비교한다. `B`가 단순 기준선과 `A`를
안정적으로 이기지 못하거나 grader exploit만 늘리면 이 가설을 기각하거나
task distribution 설계를 수정한다.

## 정본과의 관계

- `OBSERVED`: 공개 블로그와 모델 카드에 위 실험 결과와 한계가 기록돼 있다.
- `HYPOTHESIS`: 현실과 같은 행동을 유리하게 만드는 task distribution이
  held-out transfer를 높일 수 있다.
- `NOT YET`: 질문 설계의 독립 인과효과, S3 결과의 독립 재현, 일반 검색
  환경 전이, Company Foundry 업무 태스크에서의 효용.
- 승격 요청 atomic claim: 없음.
