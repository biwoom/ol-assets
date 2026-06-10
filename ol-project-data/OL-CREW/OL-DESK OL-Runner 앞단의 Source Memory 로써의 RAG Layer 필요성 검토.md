# OL-DESK OL-Runner 앞단의 Source Memory 로써의 RAG Layer 필요성 검토

## 질의

OL-Runner 기능 앞에서 작동할 Source Collection Layer 를 담당할 RAG 중심 로컬AI에이전트가 필요할지 여부를 객관적이고 중립적 입장에서 제3자의 관점에서 이 프로젝트를 분석하여 조언해줘.

---

## 검토결과

문서를 숙지한 뒤 제3자 관점에서 평가하면, 결론은 다음과 같습니다.

**Source Collection Layer 앞단에 RAG 중심 로컬 AI 에이전트는 필요하다. 다만 초기부터 ‘자율 에이전트’로 만들기보다, 먼저 `로컬 Source Retrieval / Indexing Layer`로 구현하고, 이후 OL-Runner의 `source-collect`, `toc-extract`, `event-index`, `theme-index`, `source-align` 단계와 결합하는 방식이 더 안전하다.**

문서 자체가 OL-DESK를 단순 번역 도구가 아니라 “여러 원천자료를 수집·분류·비교·발췌·통합”하는 창작 책상으로 정의하고 있고, OL-Runner도 원천자료 정리, 목차·사건·주제 추출, 원문 근거 보존, 의미 후보 생성, 표현 후보 확장, 검증 로그를 담당하는 로컬 실행기로 규정합니다.  또한 새 계층 구조에서 Source Collection Layer는 “원천자료 수집, 분류, 상세 목차, 사건·주제 index”를 담당하고, Synthesis Layer는 다중 원천자료 비교·발췌·통합을 담당하도록 설계되어 있습니다. 

## 1. 객관적 판단: “필요하다” 쪽이 더 강하다

이 프로젝트가 단일 원문 번역 도구라면 RAG 에이전트는 선택 사항입니다. 파일 하나를 읽고 세그먼트별 번역·감수·출력만 한다면 굳이 별도 RAG 계층을 만들 필요가 없습니다.

그러나 이 문서의 OL-DESK는 단일 원전 번역기가 아닙니다. 문서가 제시하는 방향은 다음입니다.

> 원문 / 기초 번역
> → 원천자료 수집
> → 목차·사건·주제 비교
> → 새 목차와 서사 구조 설계
> → 원천 발췌와 통합
> → 의미 해석
> → 창조적 번역
> → 해설글·에세이·대본·OL-TOON/OL-STUDIO 기초 원고

이 구조에서는 “어떤 자료가 어디에 있고, 어떤 사건·주제·인물·교리와 연결되는가”를 계속 찾아야 합니다. 문서도 Source Collection Layer의 임무로 원천자료 목록화, 자료 성격 분류, 언어·시대·전승·문체·신뢰도 기록, 상세 목차 추출, 사건 단위 추출, 주제와 교리 단서 추출, 중복·차이·누락 표시를 제시합니다. 

이 정도의 기능은 단순 파일 탐색이나 폴더 구조만으로는 장기적으로 감당하기 어렵습니다. 따라서 RAG 중심 로컬 AI 계층은 **기능적 필요성**이 있습니다.

## 2. 단, “RAG 에이전트”라는 이름은 조심해야 한다

중립적으로 보면, 위험도 있습니다.

RAG를 “AI가 알아서 자료를 찾고 판단하고 목차까지 만든다”는 식의 자율 에이전트로 설계하면, 초기에 프로젝트가 지나치게 복잡해집니다. 문서도 이미 위험 요소로 범위 확대, 원문 이탈, UI 과밀화, 완료 기준 불명확, 창작과 번역의 혼동, 원천자료 통합의 왜곡을 지적하고 있습니다. 

따라서 초기 구현에서 필요한 것은 “자율 판단 에이전트”가 아니라 다음에 가까운 것입니다.

**로컬 자료 색인·검색·근거제시 계층**

즉, RAG는 처음부터 인간 편집장을 대신하는 에이전트가 아니라, OL-Runner가 Source Collection Layer 작업을 할 때 필요한 **근거 검색 엔진**이어야 합니다.

## 3. 권장 역할: RAG는 ‘OL-Runner 앞단의 Source Memory’가 되어야 한다

제가 권장하는 구조는 다음입니다.

```text
Local Source Library
= 원문, 참고서, 현대 연구서, 기존 번역, 메모, 목차 파일

↓ ingest / parse / chunk / metadata

Source Collection RAG Layer
= 검색, 유사 구절 탐색, 사건·주제 후보 검색, 근거 패킷 생성

↓ structured output

OL-Runner
= source-profile, toc-extract, event-index, theme-index,
  source-align, chapter-dossier-build 실행

↓ display / edit

OL-DESK Source Board
= 인간 최고편집장이 확인·수정·승인
```

이때 RAG Layer는 독립 AI라기보다 **OL-Runner가 호출하는 로컬 지식 검색·근거 패킷 생성 모듈**에 가깝습니다.

## 4. RAG Layer가 담당해야 할 일

초기 RAG Layer의 역할은 다음 정도가 적절합니다.

```text
1. 로컬 원천자료 색인화
2. 자료별 메타데이터 저장
   - 제목
   - 언어
   - 시대
   - 전승
   - 저자/역자
   - 자료 유형
   - 신뢰도 메모
3. 문단·장·절 단위 chunk 생성
4. 원문 위치 보존
5. 키워드 검색 + 의미 검색
6. 특정 사건·인물·장소·교리어 관련 구절 검색
7. 새 목차 항목별 관련 원천자료 후보 제시
8. chapter dossier에 들어갈 source packet 후보 생성
9. 검색 결과마다 source_basis 제공
10. OL-DESK에서 확인 가능한 한국어 요약 로그 생성
```

문서가 강조하는 `chapter dossier`는 “새 목차의 한 항목에 대응하는 모든 원천자료 발췌, 요약, 차이, 누락, 보강점, 해석 메모를 묶은 작업 패킷”입니다.  RAG Layer는 바로 이 `chapter dossier`의 원재료를 찾아주는 역할에 적합합니다.

## 5. RAG Layer가 담당하지 말아야 할 일

초기에는 다음 역할까지 맡기면 위험합니다.

```text
- 최종 해석 확정
- 전승 간 우열 판단
- 새 목차 최종 확정
- 특정 교리 해석의 정통성 판정
- 창조적 번역문 최종 작성
- 각색의 허용 범위 최종 결정
```

문서의 핵심 원칙은 “OL-DESK의 주체는 AI가 아니라 인간 최고편집장”이며, “AI는 원고를 대신 결정하지 않고 의미와 표현 후보를 제공하는 조수”로 남아야 한다는 점입니다.  따라서 RAG Layer도 결정자가 아니라 **근거를 찾아오는 서지·자료 조수**로 제한해야 합니다.

## 6. RAG가 없을 때 생길 문제

RAG 없이 Source Collection Layer를 만들면 초기에는 단순합니다. 그러나 프로젝트가 커질수록 다음 문제가 생깁니다.

첫째, 자료가 많아질수록 사람이 직접 검색하고 대조해야 하는 시간이 급증합니다. 부처님 전기처럼 마하붓다왐사, 불본행집경, 붓다짜리타, 니까야·아함, 주석서, 현대 연구서가 함께 들어오면 사건·주제·인물의 대응 관계를 수동으로 관리하기 어렵습니다.

둘째, OL-Runner의 `source-align`, `event-index`, `theme-index`, `chapter-dossier-build` 단계가 매번 모델의 문맥창 안에서만 작동하게 됩니다. 그러면 작업마다 자료 기억이 끊기고, 동일 사건이나 용어를 다시 찾아야 합니다.

셋째, 원문 근거 보존이 약해집니다. 문서가 강조하는 `grounding_level`, `creative_distance`, `source_basis` 같은 메타데이터를 제대로 운영하려면, 표현 후보가 어떤 원문·의미 단위·해석 ID에 근거하는지 추적되어야 합니다.  이 추적에는 RAG 또는 그에 준하는 로컬 색인 체계가 유리합니다.

## 7. RAG가 있을 때의 위험

반대로 RAG를 도입하면 다음 문제가 있습니다.

```text
- 개발 복잡도 증가
- chunking 기준 설계 필요
- 한문·팔리어·산스크리트·영어·한국어 혼합 검색 문제
- 유사 검색 결과의 오판 가능성
- 원전 간 전승 차이를 AI가 임의로 평준화할 위험
- 벡터 검색 결과를 “근거”로 오해할 위험
```

특히 불교문헌에서는 “비슷한 단어가 나온다”는 것과 “같은 교리적 의미를 가진다”는 것이 다릅니다. 그러므로 RAG 검색 결과는 항상 “후보”로 표시해야 하며, `확정 근거`가 아니라 `검토 대상 근거`로 다루어야 합니다.

## 8. 권장 결론: ‘필요하지만, 작게 시작해야 한다’

가장 균형 잡힌 판단은 다음입니다.

```text
RAG 중심 로컬 AI 에이전트는 장기적으로 필요하다.
그러나 Phase 1~2에서는 독립 에이전트가 아니라
로컬 Source Index + 검색 UI + source packet 생성기로 시작하는 것이 좋다.
```

즉, 처음부터 “RAG 에이전트”라고 크게 부르기보다 다음 이름이 더 적절합니다.

```text
OL-Source Index
OL-Source Memory
OL-Source RAG
Source Collection Assistant
Source Packet Builder
```

이 중 프로젝트 구조상 가장 정확한 명칭은 **`OL-Source RAG`** 또는 **`Source Packet Builder`**입니다.

## 9. 단계별 도입안

문서의 로드맵에 맞추면 이렇게 배치하는 것이 자연스럽습니다.

### Phase 1: 데이터 구조 초안 단계

이때는 RAG를 만들기보다 스키마부터 정해야 합니다.

```text
data/source-collections/
data/source-profiles/
data/source-tocs/
data/event-index/
data/theme-index/
data/alignment-map/
data/chapter-dossiers/
data/grounding/
```

문서도 Phase 1에서 이 데이터 구조 초안을 먼저 잡도록 제안합니다. 

### Phase 2: Source Board MVP 단계

이때는 수동 등록 중심이어야 합니다.

```text
- 원천자료 등록
- 목차 직접 입력 또는 AI 추출 결과 붙여넣기
- 자료 성격 메모
- 사건·주제 후보 수동 확인
```

### Phase 4: OL-Runner 자료 정리 MVP 단계

이때 RAG Layer를 본격 연결하는 것이 좋습니다. 문서도 Phase 4에서 `source-profile`, `toc-extract`, `event-index`, `theme-index`, `source-align`, `outline-generate`, `chapter-dossier-build`, 한국어 source-log 생성을 제시합니다. 

이 단계가 바로 RAG가 가장 필요한 지점입니다.

## 10. 최종 조언

제3자 관점에서 보면, 이 프로젝트는 이미 단순 번역 앱의 범위를 넘어섰습니다. 목표가 “원문 기반 의미 창작 환경”이라면, Source Collection Layer는 프로젝트의 뿌리입니다. 이 뿌리가 약하면 이후 Meaning Layer, Rendering Layer, OL-TOON, OL-STUDIO까지 모두 근거가 불안정해집니다.

따라서 **RAG 중심 로컬 AI 계층은 필요합니다.**
다만 그 정체성은 다음처럼 제한해야 합니다.

```text
나쁜 방향:
AI가 알아서 자료를 해석하고 통합 원고를 결정하는 자율 에이전트

좋은 방향:
로컬 원천자료를 색인하고,
관련 구절을 찾아오고,
source packet을 만들고,
근거 위치와 불확실성을 표시하며,
인간 최고편집장의 판단을 돕는 자료 조수
```

최종 권고안은 다음 한 문장으로 정리할 수 있습니다.

**OL-Runner 앞단에 `Source Collection RAG Layer`를 두는 것은 타당하다. 그러나 초기에는 독립적 판단 에이전트가 아니라, 로컬 자료 색인·검색·근거 패킷 생성 모듈로 작게 시작하고, OL-Runner의 source-profile / toc-extract / event-index / source-align / chapter-dossier-build 단계와 점진적으로 결합하는 것이 가장 안전하고 현실적이다.**

---

