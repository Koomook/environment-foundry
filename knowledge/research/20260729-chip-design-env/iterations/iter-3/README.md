# Iteration 3 — 충실도 상승: 제네릭 프록시 vs Nangate45 매핑

- 날짜: 2026-07-29 · 상태: `OBSERVED`
- 산출물: `synth/lib/` (런타임 다운로드, git 미포함) + 비교 분석
- 원시 결과: `results/iteration-3.json`

## 가설

제네릭 셀 수 프록시는 실제 셀 라이브러리 매핑 대비 **순위를 왜곡할 수 있다** —
그 현실 간극(reality gap)은 P&R 이전, 합성 단계에서 이미 관측 가능하다.

## 만든 것

- Nangate45 open cell library (`NangateOpenCellLibrary_typical.lib`)를
  OpenROAD-flow-scripts 공개 미러에서 런타임 다운로드 (라이선스 upstream, git 미커밋)
- 5개 디자인 × 2개 플로우(제네릭 `abc -g simple` / `abc -liberty` 매핑) 비교:
  ALU compact/verbose(v1 재사용, read-only), seqdet binary/onehot/equiv_enc

## 결과

| 디자인 | 제네릭 셀 | 제네릭 깊이 | Nangate45 면적 | 매핑 깊이 |
|---|---|---|---|---|
| alu_compact_w4 | 36 | 8 | 29.79 | 5 |
| alu_verbose_w4 | 41 | 9 | 30.32 | 5 |
| seqdet_binary | 12 | 8 | 8.512 | 6 |
| seqdet_onehot | 22 | 14 | 13.034 | 12 |
| seqdet_equiv_enc | 7 | 3 | 3.990 | 7 |

관측 1 — **방향은 유지, 크기는 왜곡**: ALU 쌍의 순위( compact < verbose )는
매핑에서도 유지되지만 격차는 14% → 1.8%로 축소. 프록시가 품질 차이를
**~7.7배 과장**.

관측 2 — **동등류 노이즈 플로어**: 행동이 완전히 동일한 두 디자인
(binary vs equiv_enc)이 매핑 면적에서 **2.13배** 차이. 즉 이 스케일에서
품질 지표의 "의미 있는 최소 차이"는 최소 ~2배. 그 이하의 delta로 후보를
순위 매기는 것은 노이즈를 학습하는 것.

관측 3 — **지연 순위 반전 실측**: 동등 쌍에서 제네릭 깊이는 equiv가 우위
(3 vs 8)인데 매핑 깊이는 gold가 우위(6 vs 7). **프록시가 순위의 방향 자체를
뒤집는 사례**를 합성 단계에서 확인.

## 배운 것 / 고친 것

- 정답 게이트(행동 동등)가 품질 순위보다 **반드시 먼저**여야 하는 이유가
  정량화됨: 동등류 **내부에서** 품질 지표는 최대 2배까지 흔들린다.
- 제네릭 셀 수는 "같은 패밀리 안에서의 거친 신호"로만 사용 가능.
- (수정 이력) 첫 실행에서 `ltp -n 1` 옵션 오류로 깊이 파싱 실패 → `ltp`의
  실제 출력 형식(`length=N`) 확인 후 파서 수정, 재실행으로 확정.

## 한계와 다음 단계

- 매핑 면적/깊이도 여전히 **pre-P&R**: 배치/배선/기생/DRC/전력/사인오프/실리콘 아님.
- 남은 충실도 단계는 RTL-to-GDS (ORFS 또는 파트너 측 플로우). 비용 추정:
  ORFS 로컬 구동은 Docker 기반 수 GB / 수 시간 — 이번 아크 범위 밖,
  90일 계획의 Days 15–30 항목으로 이관. `NOT YET`.
