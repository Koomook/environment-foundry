# Team Attention × Environment Foundry 법인·파이프라인 구조 의사결정 메모

기준일: 2026-07-23  
상태: research memo, non-canonical  
범위: 한국 커뮤니티·교육 → 권리 유효한 eval/environment 사업, 한국/미국 법인, 투자, 개인정보·영업비밀, 다중 frontier-lab ambassador 역할  
주의: 이 문서는 구조 선택을 위한 리서치다. 설립·flip·계약·국외이전 전에는 한국/미국 변호사와 세무사의 서면 검토가 필요하다.

## 결론

**지금은 한국 단일 운영법인 안에서 Community/Education과 Data/Eval Lab을 계약·회계·저장소·접근권한으로 분리해 검증한다.**

미국 투자자 또는 미국 고객이 실제 문서로 미국 법인을 요구하고, 권리 유효한 상품과 buyer demand가 확인되면 **`Delaware C-corp parent → 한국 100% OpCo`**로 전환한다.

다음 구조는 기본안으로 권하지 않는다.

```text
정구봉 개인
├─ Team Attention 한국법인
└─ Environment Foundry 미국법인
```

이 형제법인 구조에서는 미국법인 투자자가 한국법인의 Ralphthon 브랜드, 교육 파이프라인, 계약, IP, 데이터 권리를 소유하지 않는다. 두 회사 사이의 기회 배분, IP 가격, 리드와 데이터 이전이 계속 related-party 거래가 되고, 창업자 개인의 이해상충도 남는다.

다만 정구봉이 Team Attention의 주주·대표가 아니라 직원일 뿐이라면, 기존 법인을 새 미국 모회사 아래 넣는 것도 임의로 결정할 수 없다. 이 경우 현실적인 장기 구조는 세 법인일 수 있다.

```text
Team Attention Korea
  └─ Ralphthon·교육·커뮤니티 운영
          │ 명시적 referral / program / rights agreement
          ▼
Environment Foundry, Inc. (Delaware parent)
  └─ Environment Foundry Korea (OpCo / private data plane)
```

Team Attention은 자동 데이터 공급자가 아니라 독립적인 교육·채널 파트너다. Environment Foundry는 별도 opt-in 프로젝트에서만 데이터를 처리한다.

## 사업을 연결하는 올바른 파이프라인

사용자의 직관 중 맞는 부분은 Ralphthon과 교육이 대표를 설득하고 좋은 회사를 발견하는 강한 채널이 될 수 있다는 점이다. 수정해야 할 부분은 교육 참가자의 활동을 곧바로 판매 가능한 데이터로 보는 것이다.

```text
콘텐츠
→ 공개 Ralphthon / vendor-specific workshop
→ 대표 교육: 즉시 쓸 수 있는 회사 개선 가치 제공
→ 회사별 문제 발견
→ 별도 Founder Eval Lab 제안
→ 회사·직원·고객 권리를 확인한 bounded workflow 선택
→ paid design pilot + rights receipt + DPA/data license
→ 한국 private data plane에서 task/grader/environment 생성
→ buyer별 acceptance test
→ 제한된 eval/environment access 또는 검토된 파생 산출물 판매
→ 원천 회사에 대가·성과·철회권 환류
```

교육 등록 동의는 Data Lab 동의가 아니다. 회사 대표도 직원, 고객, 대화 상대방, 공동저작자, 플랫폼의 모든 권리를 대신 줄 수 없다.

권리는 최소 다음처럼 분리한다.

1. 원본 열람·복제
2. 운영 개선
3. 가명·익명처리
4. task/eval/environment 생성
5. 특정 모델 평가
6. 모델 학습·fine-tuning
7. 특정 buyer 제공
8. 국외이전·재이전
9. 파생물·모델 가중치·평가결과의 소유
10. 재판매·sublicense
11. 보존·철회·삭제 propagation
12. 감사·침해통지·배상

따라서 초기 상품명도 “한국 회사 데이터 판매”보다 다음이 적합하다.

- Korean Company Agent Eval Lab
- Korean-language / culture / workflow benchmark
- rights-cleared company task environment
- private, buyer-specific evaluation and post-training environment

## 비교사례

정확히 같은 성공사례는 찾지 못했다. 특히 **대표 교육 커뮤니티의 일상적 행동 데이터를 모아 frontier lab에 재판매한 신뢰받는 사업**의 강한 공개 선례는 없었다. 가까운 사례들은 모두 상업 데이터가 만들어지는 별도 경계를 둔다.

| 사례 | 실제 연결 방식 | Team Attention에 주는 교훈 |
|---|---|---|
| Scale AI / Outlier / Remotasks | 교육·vetting 후 별도의 유료 contractor task에서 training data와 eval을 생성 | 교육 참석이 아니라 명시적 paid work가 데이터의 원천이다. [Scale Experts](https://scale.com/experts), [Outlier terms](https://outlier.ai/legal/terms-of-use) |
| Appen / CrowdGen / Figure Eight | 다국어 contributor를 교육하고 계약된 annotation·RLHF·agent trajectory를 납품 | 교육→자격→유료 task→고객 deliverable의 가장 성숙한 선례다. [Appen AI Data](https://www.appen.com/ai-data), [Figure Eight acquisition](https://www.appen.com/press-release/appen-to-acquire-figure-eight) |
| CrowdWorks | 한국에서 데이터 라벨러 교육·자격과 AI data project를 한 회사가 운영 | 한국에서도 한 법인 내 두 사업은 가능하지만 역할·계약 전환이 명시적이다. [CrowdWorks Academy](https://www.crowdworks.ai/data/academy) |
| Selectstar / CashMission / Datumo | project-specific worker 교육, 데이터 구축, red-team/eval 서비스를 연결 | Ralphthon 이후 별도 eval challenge를 설계하는 가장 가까운 한국형 패턴이다. [Selectstar](https://selectstar.ai/), [CashMission](https://selectstar.ai/cashmission/) |
| Kaggle | 회사가 문제·데이터·metric·competition rules를 정하고 커뮤니티가 제출 | 커뮤니티를 raw data source가 아니라 governed challenge/eval network로 쓴다. [Kaggle host deck](https://www.kaggle.com/static/slides/meetkaggle.pdf) |
| Palantir AIP Bootcamp | 실제 고객 문제와 고객 데이터 위에서 5일 안에 use case를 만들고 software rollout로 전환 | 교육은 강력한 enterprise sales/design-pilot surface가 될 수 있다. 고객 데이터를 제3자에게 파는 모델은 아니다. [AIP Bootcamp](https://www.palantir.com/platforms/aip/bootcamp), [Palantir 10-K](https://investors.palantir.com/files/2024%20FY%20PLTR%2010-K.pdf) |
| Hugging Face | open community와 public/private/gated repository를 분리하고 enterprise infrastructure를 판매 | 커뮤니티와 상업 사업은 공존할 수 있지만 data plane과 license가 명확해야 한다. [Enterprise](https://huggingface.co/enterprise), [Terms](https://huggingface.co/terms-of-service) |
| Reforge | 전문가 지식을 계약된 교육 콘텐츠로 만들고 membership/team software를 판매 | 대표 교육은 그 자체로 좋은 사업·신뢰망이 될 수 있다. 학습자의 private data를 파는 증거는 아니다. [Reforge](https://www.reforge.com/) |

사례가 주는 공통 원칙은 하나다.

> Community is the trust and qualification layer. A separately consented and compensated task is the commercial data/eval layer.

## 개인정보·데이터 권리

### 가명정보는 여전히 개인정보다

한국 개인정보 보호법상 가명정보는 추가정보 없이는 개인을 알아볼 수 없도록 처리한 개인정보다. 시간·비용·기술을 합리적으로 고려해 다른 정보와 결합해도 개인을 더 이상 알아볼 수 없는 익명정보만 법 적용 밖이다. 이름과 회사명을 지우는 것으로 충분하지 않다. 대표의 희귀한 사건, 직함, 의사결정 시계열, 성과, 대화 내용은 재식별 가능성이 크다. [개인정보 보호법](https://www.law.go.kr/법령/개인정보보호법), [PIPC 가명정보 안내](https://m.pipc.go.kr/eng/user/lgp/bnp/pseudonymization.do)

AI 모델 성능 개선을 위한 체계적 연구가 가명정보의 과학적 연구에 포함될 수는 있다. 그러나 이는 불특정 buyer에게 무제한 재판매할 포괄적 권리가 아니다. 특정 목적, recipient, 환경, 보존기간, 재제공 제한을 설계해야 한다.

### 미국법인은 PIPA 우회로가 아니다

한국 법인이 보유한 개인정보를 미국 parent가 조회·보관·수탁·제공받으면 국외이전이다. 가명정보도 개인정보이므로 같다. 2026년 개인정보위는 빗썸의 실제 해외 recipient와 고지·동의 flow가 맞지 않은 국외이전에 과징금 2.1억 원과 시정명령을 부과했다. [PIPC 국외이전 설명](https://www.pipc.go.kr/np/default/page.do?mCode=D060040010), [빗썸 제재](https://m.pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS074&mCode=C020010000&nttId=12196)

스캐터랩 ‘이루다’ 사건은 같은 회사 안에서도 기존 서비스의 대화를 별도 AI 학습에 쓰면 목적 외 이용이 될 수 있음을 보여준다. 법인을 하나로 합쳐도 권리가 자동 생기지 않는다. [PIPC 스캐터랩 제재](https://www.pipc.go.kr/np/cop/bbs/selectBoardArticle.do?bbsId=BS074&mCode=C020010000&nttId=7298)

### 개인정보 외 권리

회사 운영 데이터에는 개인정보 외에도 영업비밀, 업무상저작물, 데이터베이스 제작자 권리, NDA, 고객 계약, 플랫폼 약관이 겹친다. 한국 부정경쟁방지법은 비공지·경제적 가치·비밀관리성을 갖춘 기술·경영상 정보를 영업비밀로 보호한다. [부정경쟁방지법](https://www.law.go.kr/LSW/lsInfoP.do?ancYnChk=&chrClsCd=010202&efYd=20260528&lsiSeq=271245&urlMode=lsInfoP)

“개인정보 제거”가 영업비밀과 저작권 라이선스를 해결하지 않는다.

## 두 구조 시뮬레이션

### 시나리오 A — 한국 단일법인

```text
Team Attention Korea
├─ Community / Education cost center
└─ Data / Eval Lab cost center
```

| 18개월에 생기는 상황 | 결과 |
|---|---|
| 미국 buyer demand가 없음 | 고정비·관리비가 가장 낮아 A가 압도적으로 유리 |
| 한국 교육·pilot 매출만 발생 | 국내 계약·세금계산서·고용·정부 프로그램을 한 체계로 운영 가능 |
| 1개 미국 buyer가 생김 | 한국법인이 직접 계약하고 buyer별 국외이전·DPA를 처리할 수 있음 |
| 미국 lead VC가 등장 | flip 또는 미국 parent 설립이 필요할 수 있어 시간·평가·주주동의 비용 발생 |
| 개인정보 사고 또는 교육 품질 문제 | 같은 법인과 브랜드에 책임·평판이 결합 |

장점은 검증 속도와 낮은 관리 복잡성이다. 단점은 미국 VC 표준성과 장기적인 책임 분리다.

현재 Team Attention 한국법인이 사업자등록·계좌·세금계산서 운영을 아직 완전히 닫지 못한 상태라면, 두 번째 국가의 법무·회계 스택을 얹기 전에 이 기본 운영을 먼저 완성하는 편이 합리적이다.

### 시나리오 B — 한국법인과 미국법인을 창업자가 나란히 보유

```text
Founder
├─ Team Attention Korea
└─ Environment Foundry, Inc.
```

| 18개월에 생기는 상황 | 결과 |
|---|---|
| 미국 buyer demand가 없음 | 두 나라 법무·회계·세무·은행·보험 비용만 남음 |
| 미국 VC가 EF에 투자 | 투자자는 Team Attention의 커뮤니티·브랜드·계약·데이터 권리를 소유하지 못해 diligence red flag |
| Team Attention이 EF에 리드를 독점 제공 | related-party 가격·충실의무·corporate opportunity·계약 지속성 문제 |
| 한국 데이터를 EF로 보냄 | 새로운 국외이전과 intercompany DPA/license/이전가격이 추가 |
| 한 회사가 매각되거나 관계가 깨짐 | 교육→데이터 flywheel이 분리될 수 있음 |
| 다중 ambassador conflict가 발생 | 같은 개인이 두 역할을 하므로 법인 분리만으로 중립성 문제가 해결되지 않음 |

형제법인은 **두 사업이 서로 없이도 독립적으로 살아야 하고, 장기적으로 별도 매각할 의도**가 있을 때만 적합하다.

### 시나리오 B의 수정안 — Delaware parent + 한국 OpCo

```text
Environment Foundry, Inc. (Delaware)
└─ Environment Foundry Korea
```

미국 VC·글로벌 고객이 실제 주력이라면 이 구조가 가장 financeable하다. 하나의 parent security가 한국 운영, IP, 글로벌 매출과 exit를 포괄한다. Coupang과 WEBTOON은 Delaware parent와 한국 핵심 운영 자회사 구조를 SEC 공시로 확인할 수 있다. Sendbird는 California parent와 한국 자회사를 사용해 Delaware가 법적 필수는 아니라는 반례다. [Coupang 10-K](https://www.sec.gov/Archives/edgar/data/1834584/000183458426000024/cpng-20251231.htm), [WEBTOON S-1](https://www.sec.gov/Archives/edgar/data/1997859/000119312524151708/d396527ds1.htm), [Sendbird subprocessors](https://sendbird.com/sub-processors)

반대로 Lunit은 한국 parent가 Lunit USA를 100% 보유하고, Gravity는 한국 법인 자체로 Nasdaq ADS에 접근했다. 한국 parent도 글로벌 사업과 미국 자본시장 접근이 불가능한 것은 아니다. [Lunit Annual Report](https://www.lunit.io/en/wp-content/uploads/2025/11/Annual-Report_EN_FNL.pdf), [Gravity 20-F](https://www.sec.gov/Archives/edgar/data/1313310/000162828025019782/grvy-20241231.htm)

## 투자 관점

### 미국 투자를 우선하면

Delaware C-corp parent가 유리하다.

- NVCA 표준 preferred financing·governance 문서와 맞는다. [NVCA model documents](https://nvca.org/model-legal-documents/)
- SAFE가 parent에 전환되어 그룹 전체 가치를 포괄한다. [SEC startup securities](https://www.sec.gov/resources-small-businesses/capital-raising-building-blocks/common-startup-securities)
- founder restricted stock의 83(b)는 이전 후 30일 기한이 있다. 한국 거주자의 한국 세금은 별도다. [IRS Form 15620](https://www.irs.gov/pub/irs-pdf/f15620.pdf)
- QSBS는 미국 domestic C-corp stock을 전제로 하지만, 한국 거주 창업자에게 실제 세효과가 있는지는 별도 검토가 필요하다. [IRC §1202](https://uscode.house.gov/view.xhtml?edition=2023&num=0&req=granuleid%3AUSC-2023-title26-section1202)

### 한국 투자를 우선하면

한국 parent가 유리하다.

- 한국 VC·정책자금·TIPS·고용·국내 계약과의 연결이 단순하다.
- 미국 sales subsidiary는 나중에 붙일 수 있다.
- 다만 가치와 주주가 늘어난 뒤 flip하면 주식평가, 주주동의, 외환신고, 과세, 옵션·RCPS·IP 이전이 복잡해진다.

### 투자자가 법인보다 먼저 볼 것

정구봉이 Team Attention의 직원일 뿐이라면 다음이 해결되지 않는 한 Delaware 법인도 투자받기 어렵다.

1. 근로계약의 겸업·경업·외부활동 제한
2. 발명·저작물·코드·curriculum IP 귀속
3. Ralphthon 브랜드·참가자 관계·사업기회의 소유자
4. 고용주 confidential information의 사용 금지
5. Team Attention 이사회/대표의 서면 waiver와 related-party 승인
6. 언제 Environment Foundry에 full-time commitment를 할지

VC diligence에서 clean IP chain of title와 founder commitment는 관할보다 앞선다.

## 다중 ambassador 구조

OpenAI는 Codex Ambassadors를 지역 workshop·builder meetup·learning asset·community feedback 역할로 공개하고, credits·honorarium 등을 지원한다. 그러나 공개 페이지는 경쟁사 동시 ambassadorship, participant data commercialization, Team Attention을 OpenAI 파트너로 표시할 권한을 허용하지 않는다. 실제 계약의 서면 확인이 필요하다. [Codex Ambassadors](https://developers.openai.com/community/codex-ambassadors)

Anthropic의 공개 education 자료로는 Campus Ambassador outreach를 확인할 수 있지만 경쟁사·기밀·상업 활동 조건은 확인되지 않았다. Devin과 Kimi도 신뢰할 수 있는 공개 ambassador 약관을 찾지 못했다. “공개 금지조항을 못 찾았다”는 허가가 아니다.

세 역할을 분리한다.

| Hat | 하는 일 | 금지 |
|---|---|---|
| 개인 lab ambassador | 해당 제품 workshop, 학습자료, 해당 lab 피드백 | lab의 영업대리인·공식 파트너처럼 표시 |
| Team Attention educator | 관계를 공개한 vendor-neutral 교육, lab-specific track | 이해관계 미공개 비교추천, 참가자 정보 우대 제공 |
| Environment Foundry evaluator | 계약된 blind eval, buyer-specific environment | ambassador 채널의 비공개 정보·credits·roadmap을 competitor eval에 사용 |

미국 FTC와 한국 공정위 모두 경제적 관계를 명확하고 눈에 띄게 공개하는 방향이다. OpenAI 브랜드 가이드도 관계를 과장하거나 endorsement를 암시하는 사용을 금지한다. [FTC Endorsement Guides](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking), [KFTC 안내](https://www.ftc.go.kr/www/selectBbsNttView.do?bordCd=1&key=5&nttSn=33198&pageIndex=9&pageUnit=10&searchCnd=all&searchCtgry=2), [OpenAI brand guidelines](https://openai.com/ko-KR/brand/)

모든 프로그램에 서면으로 확인할 항목:

- 경쟁사 ambassador·컨설팅·투자·referral compensation 허용 여부
- 다른 lab 관계 공개 의무
- confidentiality·early access·feedback IP·work product
- curriculum·녹화·attendee list·product feedback 소유
- 유료 교육·sponsor·비교평가·상업 고객 모집 허용 여부
- 이름·로고·title·co-brand 승인
- 제공 credits의 상업적 사용 가능 여부
- 관계가 개인인지 법인인지

## 중국·다국가 판매

미국법인이 글로벌 판매의 만능 hub는 아니다. 미국 DOJ Data Security Program은 2025-04-08부터 미국인이 중국·홍콩·마카오 등 country of concern에 bulk U.S. sensitive personal data나 정부 관련 데이터를 제공하는 일정 거래를 금지·제한한다. 한국어 데이터가 자동으로 금지되는 것은 아니지만 Delaware parent는 U.S. person이므로 data nationality, type, volume, buyer ownership, onward transfer를 분류해야 한다. [DOJ Data Security Program](https://www.justice.gov/nsd/data-security)

BIS의 advanced computing·AI model weights·military/WMD end-use 규제도 별개다. 데이터셋만 파는 것과 compute, model weights, technical support를 함께 제공하는 것은 위험이 다르다.

따라서 초기에는 중국 buyer를 열지 말고 다음을 통과한 상품만 검토한다.

- 개인·회사 영업비밀을 제거했거나 목적 제한 계약을 체결
- 미국 covered data가 없음을 문서화
- buyer·실소유자·최종사용자·재이전 국가 screening
- model weights·compute·technical support 포함 여부 검토
- 한국 PIPA와 외국환·수출·조세 검토

## 전환 게이트

### 지금부터 90일

1. Team Attention 한국법인의 사업자등록·계좌·세금계산서 운영을 완료한다.
2. 정구봉의 고용·IP·겸업·ambassador 계약을 한 표로 정리하고 서면 waiver를 받는다.
3. Community/Education과 Data Lab의 데이터 저장소·접근권한·계약·cost center를 분리한다.
4. 교육 참가 기본약관과 Founder Eval Lab 별도 opt-in을 만든다.
5. 회사 한 곳과 개인정보 없는 bounded workflow로 paid design pilot을 실행한다.
6. frontier lab 세 곳에서 buyer-written task·grader·rights·acceptance specification을 받는다.

### 미국 parent 검토를 여는 gate

다음 중 2개 이상이 문서로 생길 때만 설립/flip을 검토한다.

- 미국 lead investor가 Delaware parent를 term sheet 조건으로 명시
- 미국 고객이 미국 vendor를 procurement 조건으로 명시
- 한 건의 paid design pilot이 완전원가를 충당
- 세 buyer가 task·tool·grader·rights·acceptance specification을 작성
- 미국 핵심 임직원과 현지 의사결정 실질을 둘 계획
- 그룹 IP를 미국 parent에 두어야 할 구체적 M&A·라이선스 이유

### 중단 규칙

- 대표들이 교육은 원하지만 별도 Data Lab에는 참여하지 않는다.
- buyer가 raw data만 원하고 rights-valid environment의 비용을 지불하지 않는다.
- 권리 확보 비용이 pilot revenue를 지속적으로 초과한다.
- independent eval이 ambassador 관계 때문에 신뢰받지 못한다.
- generic model + private context/harness가 별도 dataset보다 같은 효용을 낸다.

이 경우 데이터 판매 가설을 중단하고, 교육·enterprise design pilot·private eval software 중 실제로 돈을 내는 사업에 집중한다.

## 최종 선택

| 시점 | 권고 |
|---|---|
| 지금 | 한국 단일 운영법인 + 강한 내부/계약 분리 |
| 미국 수요가 가설일 때 | 미국법인 보류 |
| 한국 투자·정책자금이 18–24개월 중심 | 한국 parent + 필요 시 미국 sales sub |
| 미국 VC·frontier-lab 계약이 실제 주력 | Delaware parent + 한국 100% OpCo |
| Team Attention과 EF가 독립 회사여야 할 때 | arm’s-length channel agreement; 자동 data/IP 이전 금지 |
| 창업자 소유 한국/미국 sister companies | 기본적으로 제외 |

가장 중요한 결론은 다음이다.

> Ralphthon과 교육은 회사 데이터를 얻는 법적 장치가 아니라, 신뢰를 만들고 좋은 문제와 principal을 발견하는 distribution이다. 판매 가능한 자산은 그 다음 단계에서 별도의 대가·권리·task·grader·outcome을 가지고 새로 만들어야 한다.

