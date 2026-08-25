# AI가 칩 설계를 어떻게 배우는가 — 공개 교육물 연구 패킷

Date: 2026-07-30
Status: divergent research; not canonical company truth
Visibility: public-safe synthesis
Question: 사업 계획을 공개하지 않고, AI가 칩 설계를 배우는 원리를 어떻게
실행 가능하고 이해하기 쉽게 설명할 수 있는가?

## 공개 thesis

> AI는 칩 설계 파일을 많이 읽는 것만으로 칩 설계를 배우지 않는다.
> 설계안을 내고, 실행 가능한 도구로 돌려 보고, 기능과 물리 조건을
> 통과했는지 채점받는 반복 속에서 배운다.

필요한 세 요소는 다음과 같다.

```text
Simulator × Decision Data × Protected Feedback
= Learning Environment
```

- **Simulator**: 행동의 결과를 돌려주는 실행 세계
- **Decision data**: `상태 → 변경 → 도구 결과 → 채택/되돌림`이 연결된 경험
- **Protected feedback**: 기능과 안전 조건을 먼저 통과시킨 뒤 품질을
  비교하는 채점

## 다섯 번의 연구 iteration

### Iteration 1 — “칩을 밑에서부터 이해하면 AI의 목표가 보일 것이다”

사용자 제공 영상
[Chip design from the bottom up – Reiner Pope](https://www.youtube.com/watch?v=oIk3R-sMX5o)
의 전체 자막과 chapter를 검토했다.

`OBSERVED`: 영상은 논리게이트에서 MAC, 데이터 이동, systolic array,
pipeline, FPGA/ASIC, cache/scratchpad로 올라간다. AI 설계 자동화의 증거는
아니지만, 채점표가 계산량 하나가 아니라 precision, local reuse, memory
hierarchy, communication을 봐야 하는 이유를 설명한다.

`NEW HYPOTHESIS`: architecture 지식을 읽히는 것만으로는 부족하며, AI가
선택을 바꾸고 workload 결과를 관찰하는 실행 환경이 필요하다.

### Iteration 2 — “빠른 architecture simulator면 충분할 것이다”

[Timeloop/Accelergy](https://timeloop.csail.mit.edu/),
[FireSim](https://docs.fires.im/en/latest/FireSim-Basics.html),
[Verilator](https://github.com/verilator/verilator),
[OpenROAD](https://openroad.readthedocs.io/en/latest/)의 서로 다른 fidelity와
출력 경계를 비교했다.

`OBSERVED`: 한 도구는 workload·architecture·RTL·physical·silicon 전체를
재현하지 않는다. 빠른 모델은 많은 시도를 가능하게 하고, 느린 도구는 그
순위가 현실에서도 유지되는지 교정한다.

`NEW HYPOTHESIS`: 가장 좋은 환경은 만능 simulator가 아니라
RTL simulation → formal → synthesis → place-and-route → FPGA/emulation →
silicon의 fidelity ladder다.

### Iteration 3 — “많은 설계 파일과 공개 테스트를 주면 학습할 것이다”

공개 4-bit ALU 실험에서 후보를 컴파일하고, 보이는 예제와 숨은 입력
조합으로 나누어 실행했다.

`OBSERVED`: 보이는 예제 세 개에서는 잘못된 지름길 후보와 일반 규칙 후보가
모두 3/3을 통과했다. 숨은 1,024개 입력 조합에서는 지름길 후보가 828개를
실패했다.

`NEW HYPOTHESIS`: 학습 데이터는 완성 파일보다 action–outcome episode여야
하고, 평가는 visible test와 분리된 protected grader를 가져야 한다.

### Iteration 4 — “기능과 PPA를 하나의 점수로 섞으면 될 것이다”

[VerilogEval](https://arxiv.org/abs/2309.07544)은 실행 가능한 기능 평가의
가치를 보여 주고,
[ChiPBench](https://papers.nips.cc/paper_files/paper/2025/hash/1cba8502063fab9df252a63968691768-Abstract-Datasets_and_Benchmarks_Track.html)는
placement surrogate가 최종 PPA와 어긋날 수 있음을 보고한다.

`OBSERVED`: 문법 통과, 기능 통과, 합성 proxy, 최종 physical result는
서로 다른 문이다. 약한 가중합은 기능을 조금 버리고 proxy 점수를 높이는
후보를 허용할 수 있다.

`NEW HYPOTHESIS`: 기능·안전·물리 규칙은 hard gate로 두고, 통과한
후보 안에서만 전력·속도·면적을 비교해야 한다.

### Iteration 5 — “기술적으로 정확하면 대중에게도 전달될 것이다”

기존 연구의 공개 경계를 감사하고, 쉬운 단어에서 기술명으로 내려가는
interactive curriculum을 설계했다. 구체적인 회사, 국가, 데이터 획득,
파트너, 가격, 90일 계획은 모두 제외했다.

`OBSERVED`: 공개 가능한 핵심은 세 재료 조립, 여섯 단계 fidelity ladder,
reward-hacking 미니 실험, trajectory 데이터, 공개 질문이다. 사용자가
공유한 영상은 원리를 이해하는 보조 교재로 연결할 수 있다.

`RESULTING HYPOTHESIS`: 대중용 교육물도 정답을 읽게 하기보다 사용자가
채점의 빈틈과 현실 간극을 직접 클릭해 발견하게 해야 한다.

## 영상에서 유지한 핵심과 버린 일반화

공개 설명에 유지한 다섯 항목:

1. AI workload의 중요한 계산 primitive로서 matrix multiply-accumulate
2. 연산기 자체뿐 아니라 data movement와 local reuse의 비용
3. systolic/spatial array가 communication을 amortize하는 방식
4. clock, pipeline register, latency 사이의 trade-off
5. cache와 software-managed memory의 flexibility/predictability trade-off

일반화하지 않은 항목:

- 특정 세대 FP4가 FP8보다 항상 정확히 몇 배 빠르다는 주장
- FPGA가 ASIC보다 항상 정확히 몇 배 비효율적이라는 주장
- 특정 첫 칩의 고정 비용 숫자
- “GPU는 작은 TPU의 묶음”이라는 표현을 기술적 동일성으로 해석하는 것

조건 의존 숫자는 제품 형식, sparsity, workload, 공정, NRE에 따라 달라진다.
세부 감사는 [eda-video-audit.md](./eda-video-audit.md)에 있다.

## 공개 콘텐츠 경계

포함:

- 공개 도구와 논문으로 재현 가능한 원리
- synthetic educational RTL 실험의 관찰값
- simulator/data/feedback의 쉬운 정의
- proxy와 현실 결과 사이의 한계
- `OBSERVED`와 `NOT YET` 구분

제외:

- 회사명과 사업 thesis
- 한국 또는 특정 회사에 대한 접근 가설
- 회사 데이터의 획득 대상과 계약 방식
- 파트너 순서, buyer, 가격, pilot, stop rule
- 90일 계획과 내부 실행 일정

세부 편집 경계는 [public-boundary.md](./public-boundary.md), 화면 명세는
[web-learning-spec.md](./web-learning-spec.md)에 있다.

## Evidence boundary

`OBSERVED`: 공개 도구로 작은 RTL 후보를 실행해 문법 오류를 거르고, 보이는
테스트의 빈틈을 숨은 입력으로 드러내고, 기능 통과 뒤 합성 proxy를 비교하는
루프를 만들 수 있다.

`NOT YET`: 실제 공정, 상용 signoff, 생산 수율, silicon 성능, 회사 데이터의
학습 효용, 인간 전문가나 다른 탐색 방법 대비 우위는 이 교육물이 증명하지
않는다.

## Source and rights receipt

이 패킷은 사용자가 제공한 공개 YouTube 링크, 공개 논문, 공개 공식 문서,
오픈소스 저장소, synthetic RTL과 로컬 도구 결과만 사용한다. 영상 전체나
장문의 transcript를 저장소에 복제하지 않았다. 비공개 회사 payload, PDK,
고객 설계, 연락처, 자격증명, 개인 기록을 포함하지 않는다.
