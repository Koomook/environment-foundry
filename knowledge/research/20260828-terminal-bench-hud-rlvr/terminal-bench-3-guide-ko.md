# Terminal-Bench 3.0 태스크 가이드

Terminal-Bench 3.0은 “프롬프트 + 테스트 데이터”가 아니라 Harbor가 실행할
수 있는 하나의 패키지다. 정확한 재현 기준은 2026-07-23의
[`v3.0.0`](https://github.com/harbor-framework/terminal-bench/releases/tag/v3.0.0),
commit `2b0442c3c583b710ca8da14c8e601b99f2f1f244`, Harbor `0.18.0`이다.

```text
tasks/<slug>/
├── instruction.md
├── task.toml
├── environment/Dockerfile
├── solution/solve.sh
└── tests/
    ├── Dockerfile
    └── test.sh
```

V3의 핵심은 separate verifier다. Agent가 작업한 컨테이너는 종료되고,
`task.toml`의 root `artifacts` allowlist에 선언된 결과만 신뢰된 verifier
컨테이너로 넘어간다. Hidden test와 oracle은 agent 이미지에 들어가면 안
된다.

Verifier는 `/logs/verifier/reward.json`을 먼저 읽고, 없으면
`reward.txt`를 읽는다. Shell exit code만으로는 보상이 되지 않는다.
실패도 정상적인 학습 신호로 쓸 경우 유효한 `0` reward 파일을 남겨야
하며, reward 파일 자체가 없거나 깨지면 task 실패가 아니라 verifier
오류가 된다. 자세한 동작은
[Harbor verifier source](https://github.com/harbor-framework/harbor/blob/v0.18.0/src/harbor/verifier/verifier.py)에 고정돼 있다.

공식 검증 순서는 대략 다음과 같다.

```bash
harbor run -p tasks/<slug> -a oracle  # reward 1
harbor run -p tasks/<slug> -a nop     # reward < 1
harbor run -p tasks/<slug> -a <agent> -m <model>
```

새 태스크는 instruction의 모든 요구사항이 verifier에서 검증되어야 하며,
oracle 반복 실행, nop, 실제 agent failure analysis, reward-hacking/cheat
검토가 필요하다. V3 공식 corpus의 canary는 training을 금지한다. RLVR은
동일한 패키지 해부학을 사용하는 별도 rights-cleared train split에서
수행하고, 공식/봉인된 태스크는 평가로 남겨야 한다.

