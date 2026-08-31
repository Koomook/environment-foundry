# datafooding migration pointer

datafooding은 Environment Foundry의 데이터 입력 엔진이다.

- canonical target: `/Users/bong/environment-foundry/products/datafooding`
- current working tree: `/Users/bong/team-attention/code-repos/datafooding`
- source repository: `https://github.com/Koomook/datafooding.git`
- recoverable branch: `codex/agent-session-vault`
- validated commit: `555d360 feat: build private agent session vault`
- migration state: `recoverable-branch-physical-move-deferred`

현재 구현은 커밋·원격 branch로 복구 가능하며 로컬 테스트, 실제 GCS
보관/복원/삭제, macOS LaunchAgent, localhost annotation, private Harbor draft
경계까지 검증되었다. 원본 세션·키·운영 식별자는 이 저장소에 들어오지 않는다.

물리 이동은 아직 하지 않는다. 현재 독립 Git 저장소를 Environment Foundry
monorepo 안에 중첩할지, submodule/역사 import로 흡수할지, 또는 독립 저장소를
canonical code root로 유지하고 이 포인터만 둘지에 대한 repository-ownership
결정이 먼저 필요하다. 결정 전에는 기존 경로와 remote를 유지하고, 새 구현은 위
branch/commit을 기준으로 검증한다.
