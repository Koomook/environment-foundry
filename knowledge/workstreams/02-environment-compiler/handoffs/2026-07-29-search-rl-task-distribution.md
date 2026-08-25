# Search RL 환경·질문 분포 인사이트 핸드오프

- 워크스트림 ID: EF-02
- 작성일: 2026-07-29
- 대체 문서: 없음
- 현재 게이트: 태스크 선택 전 워크플로 감사
- 영향을 받는 그래프 간선: 외부 Search RL 사례 → task distribution 설계 가설 → held-out transfer 실험
- 산출물 경로: `knowledge/research/20260729-search-rl-task-distribution/README.md`
- 검증 방법: Trillion Labs 블로그를 S3 공개 코드·모델 카드·데이터셋 카드, 원 SearchGym ACL 논문, mission spine, simulator boundary와 대조
- 검증 결과: 질문 분포가 어떤 검색 행동이 reward를 얻는지 결정한다는 설계 논리를 확인했으나, 질문 단독 인과효과와 일반 전이는 확인하지 못함
- 관찰: 연구팀 설정에서 S3 학습 후 Semantic Scholar 기반 LitQA2와 Google Search 기반 GAIA 성능 향상이 보고됨. 공개 모델 카드는 LitQA2 평가가 작고 사후 checkpoint 선택을 사용했으며 paper-finder 성능은 평평했다고 명시
- 결정: 출처를 비정본 연구 입력으로 보존하고, `좋은 질문 세트`를 독립 해법으로 승격하지 않음. 환경 감사 단위를 observation/action surface, task distribution, grader와 reward의 공동 설계로 유지
- 가설: 실제 업무에서 필요한 상태 구별·근거 확인·복구·중단을 요구하는 episode distribution은 쉽게 노출된 단서 중심 분포보다 held-out policy transfer를 높임
- 승격 요청 atomic claim: 없음
- 모순·실패·누락 증거: SearchGym 원 논문은 양의 전이를 보고하지만 Trillion Labs 재현은 실패를 보고함. question-only ablation, 독립 재현, GAIA 신뢰구간, Company Foundry 업무 태스크 결과가 없음
- 개인정보·권리 확인: 공개 URL과 내부 안전 요약만 저장함. 글 전문, 이미지, 데이터셋 payload, 모델 가중치, credentials를 Git에 복사하지 않음
- 다음 반증 가능 게이트: 첫 bounded task에서 동일한 observation/action/grader 위에 두 task distribution을 동결하고 frozen held-out episode 및 prospective shadow outcome의 policy ranking을 비교
- 담당자: EF-02 owner
- 중단 규칙: 현실적 분포가 단순 분포와 기준선을 안정적으로 이기지 못하거나 grader exploit만 늘리면 task-distribution 가설을 기각하거나 재설계
