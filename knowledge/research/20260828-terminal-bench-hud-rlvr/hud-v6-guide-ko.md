# HUD v6에서 RLVR 태스크를 보는 법

2026-08-28 기준 지원 중심은
[`hud-evals/hud-python`](https://github.com/hud-evals/hud-python) v6이며,
stable은 [`0.6.15`](https://github.com/hud-evals/hud-python/releases/tag/v0.6.15)다.
명시적으로 “Reinforcement Learning through Verifiers”라고 불렸던
[`hud-vf-gym`](https://github.com/hud-evals/hud-vf-gym)은 archived이고 제거된
v5 API를 사용하므로 새 구현 기준이 아니다.

HUD의 portable task row는 다음 join key와 실행/검증 메타데이터를 가진다.

```text
Task(env, id, args, slug, validation, agent_config,
     columns, runtime_config, verifier)
```

여러 row는 `Taskset`으로 묶이고 JSON/JSONL로 이동할 수 있다. `verifier`
필드는 actor와 별도의 agent-less authoritative task를 지정한다. 이 단계의
grade가 actor의 provisional grade를 대체하므로 hidden truth나 rights-sensitive
검증을 분리하기 좋다. 정확한 필드는
[HUD task reference](https://docs.hud.ai/v6/reference/tasks)와
[verifier environments](https://docs.hud.ai/v6/experimental/verifier-environments)를
따른다.

Reward는 단일 숫자뿐 아니라 `EvaluationResult`와 weighted `SubScore` tree로
감사 가능하게 분해할 수 있다. Training은 graded `Run`, trace ID, 또는
token-level `TrajectoryPayload`를 `TrainingClient`에 전달한다. `group`은
GRPO-style group advantage의 반복 수이고, 실제 policy loss는
importance sampling, PPO, CISPO, DRO 등 별도 선택이다. 모든 rollout이 0이나
1인 group은 advantage가 없으므로, 학습 전 reward spread를 먼저 확인해야
한다. 공식 설명은 [HUD training reference](https://docs.hud.ai/v6/reference/training)에 있다.

이번 pilot은 20개 JSONL row를 만들었지만 HUD actor/verifier 이미지를
deploy하지 않았고 모델 rollout도 하지 않았다. 따라서 `Taskset manifest
created`는 `RLVR dataset validated`와 다르다.

