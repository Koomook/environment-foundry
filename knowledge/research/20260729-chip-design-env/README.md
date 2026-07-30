# AI 칩 설계 환경 — 리서치 패키지 (2026-07-29)

**질문**: AI가 칩을 잘 설계하려면 어떤 시뮬레이터와 데이터가 필요한가? 그리고
한국 중소 칩 회사(삼성/하이닉스 제외)의 데이터가 Environment Foundry의 첫
wedge가 될 수 있는가?

**한 문장 결론**: 필요한 것은 거대 시뮬레이터도 대량 파일도 아니라, 보상 1회
비용이 초~분인 실행 가능한 충실도 사다리(Icarus/Verilator → Yosys → OpenROAD →
Timeloop, 전부 오픈소스) 위에서 돌연변이 감사로 검증된 히든 채점기와 권리
유효 결정 에피소드이며, 한국 wedge는 디자인하우스(세미파이브/에이직랜드 류)
2개사 POC다.

## 산출물 인덱스

| 산출물 | 경로 | 상태 |
|---|---|---|
| 종합 결론 | `synthesis-and-recommendation.md` | ✅ |
| 10문장 원페이저 | `onepager.md` | ✅ |
| 골맵 | `goal-map.md` | ✅ |
| 리서치: 시뮬레이터+AI 연구 | `research/simulators-and-ai-methods.md` | ✅ |
| 리서치: 데이터+데이터셋 | `research/data-artifacts-and-datasets.md` | ✅ |
| 리서치: 한국 회사 지도 | `research/korea-chip-company-map.md` | ✅ |
| 이터레이션 문서 3종 | `iterations/iter-{1,2,3}/README.md` | ✅ |
| 실험 코드+결과 | `../../../lab/experiments/ai-chip-foundry-v2/` | ✅ OBSERVED |
| HTML 덱 3종 | `decks/deck{1,2,3}-*.html` | ✅ 시각 검증 완료 |
| 인터랙티브 WebUI | `webui/index.html` | ⏳ |
| 팟캐스트 대본+오디오 | `podcast/` (MP4 11.63분, gitignore) | ✅ |
| YouTube (private) | https://youtu.be/Om0f0V9AoxE | ✅ |

## 관련 선행 작업

- `../../20260729-ai-chip-environments/README.md` — 5회 이터레이션 패킷 (v1,
  조합 블록 계약). 본 패키지의 v2 3회 이터레이션은 그 "proposed next gate"를 실행.
- 핸드오프: `../../../workstreams/02-environment-compiler/handoffs/2026-07-29-ai-chip-environment.md`

## 증거 언어

- `OBSERVED`: v1+v2 8게이트 환경 계약(컴파일→히든 행동→뮤테이션 감사→프록시
  충실도), 프록시 왜곡 3종(7.7배 과장, 동등쌍 2.13배, 지연 순위 반전)
- `HYPOTHESIS`: 디자인하우스 reference-design closure가 최우선 wedge
- `NOT YET`: RTL-to-GDS 상관, prospective 순위 예측, 파트너 실사, 상용 노드 전이
