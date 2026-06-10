# 07_OL-DESK_의미중심_전환기획

## 번역 도구에서 원문 기반 의미 창작 환경으로의 전환 기획

**문서명:** OL-DESK 의미중심 전환기획  
**버전:** v0.1  
**작성일:** 2026-06-07  
**문서 성격:** OL-DESK와 OL-Runner의 목적을 단순 번역 생산에서 원문 기반 의미 해석·재표현·창작 환경으로 전환하기 위한 상위 기획 문서  
**상위 문서:** `00_OL-CREW_전체기획.md`  
**관련 문서:** `01_OL-DESK_개발기획.md`, `02_Contents-Asset_데이터구조기획.md`, `05_OL-DESK_개발로드맵.md`, `06_OL-Runner_개발기획.md`

---

# 1. 한 줄 정의

**OL-DESK는 단순히 원문을 1:1로 옮기는 번역 도구가 아니라, 여러 원천자료를 수집·분류·비교·발췌·통합하고, 그 위에 인간 최고편집장의 해석과 문체를 더해 현대 독자에게 전달 가능한 최종 원고와 파생 콘텐츠 기초 원고를 제작하는 창작 책상이다.**

OL-Runner는 이 과정에서 기계적 번역 생산기가 아니라, 원천자료 정리, 목차·사건·주제 추출, 원문 근거 보존, 의미 후보 생성, 표현 후보 확장, 검증 로그 생성을 담당하는 로컬 실행기이다.

OL-DESK의 장기 역할은 OL-프로젝트 전체 콘텐츠 생산의 중심이 되는 것이다. 즉, 다양한 원전과 참고자료를 모아 새로운 목차와 원고 구조를 설계하고, 기초 번역과 의미 해석을 바탕으로 창조적 번역, 해설글, 에세이, 대본, 그리고 `OL-TOON`, `OL-STUDIO`를 위한 기초 원고까지 생산하는 원고 제작 허브가 되어야 한다.

---

# 2. 전환의 문제의식

현재까지의 OL-DESK와 OL-Runner 논의는 주로 다음 흐름을 전제했다.

```text
원문
→ 정리 원문
→ 1차 번역
→ 2차 번역
→ 인간 감수
→ 3차 반영
→ 4차 최종원고
→ export
```

이 구조는 번역 생산 관리에는 적합하다. 상태 전이, 산출물 관리, 로그 추적, 인간 감수 흐름을 안정적으로 만들 수 있다.

그러나 이 구조만으로는 OL-프로젝트의 더 깊은 목적을 담기 어렵다. 사용자의 핵심 관심은 “말을 충실하게 옮기는 것”이 아니라 “뜻을 드러내는 것”이다.

따라서 다음 문제의식이 생긴다.

```text
- 나는 단순히 원문을 충실하게 옮기는 번역가인가?
- 나는 말보다 뜻에 관심이 있고, 가치를 그 지점에 두는 사람인가?
- OL-DESK가 단순 번역 도구가 되면 오래 지속될 수 있는가?
- OL-프로젝트의 취지는 기계적 번역인가, 원문 기반의 의미 창작인가?
- OL-DESK는 최종 원고를 쓰는 책상인가, 단순히 번역 상태를 보는 대시보드인가?
- OL-TOON과 OL-STUDIO는 어디에서 원고를 공급받아야 하는가?
- 하나의 원전에 충실한 번역이 아니라 여러 원천자료를 통합한 새 원고를 만들려면 무엇을 먼저 정리해야 하는가?
- 부처님 전기처럼 다양한 전승이 있는 주제에서 목차, 사건, 주제, 정서 흐름을 어떻게 새롭게 재구성할 것인가?
```

이 질문에 대한 답이 “말이 아니라 뜻”이라면 OL-DESK의 방향은 바뀌어야 한다.

---

# 3. 기본 전환 방향

기존 방향:

```text
원문을 충실히 옮기는 번역 생산 시스템
```

새 방향:

```text
여러 원천자료에 근거하여 뜻과 사건과 주제를 해석하고, 현대 독자에게 전달 가능한 새로운 원고 구조와 표현으로 재구성하는 의미 창작 시스템
```

확장 방향:

```text
원문 / 기초 번역
→ 원천자료 수집
→ 목차·사건·주제 비교
→ 새 목차와 서사 구조 설계
→ 원천 발췌와 통합
→ 의미 해석
→ 창조적 번역
→ 해설글
→ 에세이
→ 대본
→ OL-TOON / OL-STUDIO 기초 원고
```

이 전환은 번역을 버린다는 뜻이 아니다. 번역은 여전히 필요하다. 다만 번역은 최종 목적이 아니라 의미 작업의 한 층위가 된다.

새 구조에서 번역은 다음 역할을 한다.

```text
- 원문 근거 확인
- 의미 단위 추출
- 해석의 출발점
- 표현 후보 중 하나
- 최종 창작물이 원문에서 벗어나지 않도록 하는 안전장치
```

---

# 4. 핵심 원칙

새 방향의 핵심 원칙은 다음 네 문장으로 정리한다.

```text
창조는 허용하되, 근거를 잃지 않는다.
표현은 자유롭되, 해석 책임은 기록한다.
원문 대응은 목적이 아니라 안전장치다.
최종 산출물은 번역본 하나가 아니라 독자에게 전달되는 의미 표현이다.
OL-DESK의 주체는 AI가 아니라 인간 최고편집장이다.
AI는 원고를 대신 결정하지 않고, 의미와 표현 후보를 제공하는 조수로 남는다.
```

이 원칙은 OL-DESK, OL-Runner, Contents-Asset, UI/UX, 로그 설계 전체에 적용한다.

---

# 5. 기존 번역 중심 구조의 한계

현재 구조는 다음에 강하다.

```text
- 원문과 번역문 대조
- 단계별 번역본 관리
- 번역 상태 전이
- 용어·각주·태그 후보 관리
- 인간 감수 메모
- handoff와 export
```

그러나 다음에는 약하다.

```text
- 의미 단위 중심의 작업
- 직역, 의역, 해석, 재표현의 층위 구분
- 해석 근거 기록
- 불확실성과 대안 해석 관리
- 원문과 최종 표현 사이의 거리 표시
- 독자 대상과 표현 목적 설정
- 교리적 맥락과 수행적 의미 연결
- 최종 산출물을 여러 표현 형식으로 확장하는 구조
```

따라서 기존 `draft1~draft4` 중심 구조만으로는 새 목적을 담기 어렵다.

---

# 6. 새 계층 구조

새 OL-DESK는 다음 다섯 계층으로 재정의한다.

```text
Source Collection Layer
= 원천자료 수집, 분류, 상세 목차, 사건·주제 index

Source Layer
= 원문, 세그먼트, 직역, 원문 근거

Synthesis Layer
= 다중 원천자료 비교, 발췌, 통합, 새 목차와 서사 구조

Meaning Layer
= 뜻, 해석, 교리적 맥락, 핵심 주장, 불확실성

Rendering Layer
= 현대어 표현, 창조적 번역, 해설글, 에세이, 대본, 매체용 기초 원고

Review Layer
= 인간 판단, 메모, 승인, 보류, revision

Export Layer
= 최종 산출물
```

이 구조에서 OL-DESK는 단순 대시보드가 아니라 원천자료 기반 창작 편집실이 된다.

---

# 7. Source Collection Layer

Source Collection Layer는 원고 작업의 첫 단계다. 하나의 원전만 읽고 쓰는 방식은 원전 충실 번역에는 적합하지만, 새로운 해석적 창작과 대중적 원고 제작에는 부족할 수 있다.

특히 부처님 전기처럼 다양한 원전과 전승이 존재하는 주제에서는 여러 원천자료를 모으고, 상세 목차와 사건과 주제를 비교한 뒤, 새 원고의 구조를 설계해야 한다.

예시 원천자료:

```text
- 마하붓다왐사
- 불본행집경
- 붓다짜리타
- 니까야/아함 관련 단편
- 주석서와 해설서
- 현대 연구서
- 기존 전기/해설/대중서
```

Source Collection Layer에서 해야 할 일:

```text
- 원천자료 목록화
- 자료 성격 분류
- 언어, 시대, 전승, 문체, 신뢰도 기록
- 상세 목차 추출
- 사건 단위 추출
- 주제와 교리 단서 추출
- 중복과 차이 표시
- 누락과 보강 가능성 표시
```

이 단계의 목적은 곧바로 번역하는 것이 아니라 “창작 재료의 지도”를 만드는 것이다.

필요한 관점:

```text
TOC Map
= 각 자료의 목차 구조

Event Map
= 사건, 인물, 장소, 시간, 전승 차이

Theme Map
= 교리, 수행 의미, 정서, 핵심 메시지

Source Profile
= 각 자료의 성격, 문체, 강점, 한계
```

---

# 8. Source Layer

Source Layer는 원문 근거를 보존한다.

포함 데이터:

```text
- raw source
- normalized source
- segments
- literal rendering
- 원문 용어
- 문법적 단서
- 참고번역
- 원문 리스크
```

Source Layer의 목적은 창조적 재표현을 제한하는 것이 아니라, 재표현이 완전히 공중에 뜨지 않도록 근거를 제공하는 것이다.

필요한 UI:

```text
- 원문 세그먼트 보기
- 세그먼트별 직역 보기
- 원문-번역 대응 확인
- 원문 리스크 표시
- 참고번역과의 차이 확인
```

---

# 9. Synthesis Layer

Synthesis Layer는 여러 원천자료를 새 원고 구조로 통합하는 층위다.

이 단계는 단순히 발췌문을 이어 붙이는 것이 아니다. 덜어낼 부분은 덜어내고, 보강할 부분은 보강하고, 순서를 재정리하고, 사건을 통합하고, 문체와 의미 방향을 새 원고의 목적에 맞게 정렬하는 작업이다.

권장 흐름:

```text
1. 각 원천자료의 상세 목차 추출
2. 목차 간 상호 비교
3. 사건 단위 index 생성
4. 주제와 정서 흐름 추출
5. 새 목차 후보 작성
6. 새 목차 항목별 source packet 생성
7. 원천별 발췌와 요약 정리
8. 충돌·중복·누락·보강점 표시
9. 통합 방향 결정
10. 기초 통합 원고 작성
```

여기서 중요한 개념은 `chapter dossier`다.

```text
chapter dossier
= 새 목차의 한 항목에 대응하는 모든 원천자료 발췌, 요약, 차이, 누락, 보강점, 해석 메모를 묶은 작업 패킷
```

`chapter dossier`는 최종 원고가 아니다. 인간 최고편집장이 새 원고를 쓰기 위한 자료 묶음이다.

Synthesis Layer의 핵심 산출물:

```text
- 새 목차 후보
- 사건 통합표
- 주제 통합표
- source packet
- chapter dossier
- composition plan
- narrative architecture
```

---

# 10. Meaning Layer

Meaning Layer는 새 방향의 핵심이다.

포함 데이터:

```text
- 의미 단위
- 핵심 뜻
- 해석 후보
- 대안 해석
- 교리적 맥락
- 수행적 의미
- 불확실성
- 해석 근거
- 인간의 최종 해석 판단
```

기존 세그먼트는 문단 또는 원문 구조 단위다. 그러나 의미 작업에서는 세그먼트와 의미 단위가 항상 일치하지 않는다.

예:

```text
하나의 세그먼트 안에 여러 의미 단위가 있을 수 있다.
여러 세그먼트가 하나의 의미 단위를 구성할 수 있다.
원문 용어 하나가 문헌 전체의 핵심 주장을 형성할 수 있다.
```

따라서 `segments/`와 별개로 `meaning-units/`가 필요할 수 있다.

---

# 11. Rendering Layer

Rendering Layer는 뜻을 독자에게 전달 가능한 표현으로 바꾸는 층위다.

여기서 산출물은 하나의 번역본만이 아니다.

가능한 표현 형식:

```text
- 직역형
- 자연스러운 현대어형
- 창조적 번역형
- 해설형
- 수행 지침형
- 에세이형
- 강의 대본형
- 출판 원고형
- toon 기초 원고
- studio 기초 원고
- 짧은 요약형
- 독자별 버전
```

각 rendering은 다음 정보를 가져야 한다.

```text
- 어떤 의미 단위에 근거하는가
- 원문과의 거리는 어느 정도인가
- 어떤 독자를 상정하는가
- 어떤 문체를 사용하는가
- 인간이 승인했는가
- 어떤 해석 판단을 반영했는가
- 어떤 후속 제작 도구에서 사용할 수 있는가
```

Rendering Layer의 산출물 유형은 다음처럼 구체화한다.

```text
literal_translation
= 원문 구조를 최대한 보존한 직역형 표현

creative_translation
= 원문의 뜻을 살리되 현대 독자가 읽을 수 있도록 재구성한 창조적 번역

commentary
= 독자의 이해를 돕는 해설형 원고

essay
= 원문에서 발견한 의미를 주제 중심으로 확장한 글

script
= 강의, 오디오, 영상, 대화형 콘텐츠를 위한 대본

toon_source
= OL-TOON에서 컷, 장면, 대사, 내레이션으로 전환하기 위한 기초 원고

studio_source
= OL-STUDIO에서 영상, 음성, 장면 연출, 인터랙션으로 확장하기 위한 기초 원고
```

각 산출물은 원문과의 관계를 명확히 표시해야 한다.

```text
grounding_level:
  direct       = 원문 직접 근거
  interpretive = 해석을 거친 표현
  expanded     = 독자 이해를 위해 확장한 표현
  adapted      = 매체 제작을 위해 각색한 표현

creative_distance:
  low
  medium
  high
```

이 표시는 원문 기반 번역, 해석, 창조적 재표현, 매체 각색을 혼동하지 않기 위한 안전장치다.

---

# 12. Review Layer

Review Layer는 인간 감수와 해석 책임을 기록한다.

기존의 감수 메모보다 더 넓은 범위를 다룬다.

포함 항목:

```text
- 이 해석을 선택한 이유
- 보류한 대안
- 원문 근거
- 표현을 바꾼 이유
- 독자 이해를 위해 추가한 설명
- 원문에서 멀어진 부분
- 인간이 책임지는 최종 판단
```

Review Layer의 핵심은 “AI가 만든 것을 승인”하는 것이 아니다. 핵심은 인간이 의미와 표현의 책임을 명시하는 것이다.

---

# 13. Export Layer

Export Layer는 최종 결과물을 만든다.

기존 export:

```text
- 개별 문서 Markdown
- 전체 프로젝트 Markdown
```

새 방향에서 추가될 수 있는 export:

```text
- 원문+직역 대조본
- 의미 해석 노트
- 해설형 원고
- 현대어 재표현 원고
- 강의용 원고
- 에세이형 글
- 창조적 번역 원고
- 영상/오디오 대본
- OL-TOON 기초 원고
- OL-STUDIO 기초 원고
- 용어 해설집
- 주제별 발췌본
```

최종 산출물은 “번역본” 하나에 갇히지 않는다.

---

# 14. Contents-Asset 변경 방향

현재 Contents-Asset 구조는 번역 생산물 저장에 맞춰져 있다. 새 방향에서는 의미 작업 데이터를 추가해야 한다.

추가 검토 폴더:

```text
data/source-collections/
= 하나의 창작 프로젝트에 포함된 모든 원천자료 목록

data/source-profiles/
= 각 원천자료의 시대, 언어, 전승, 문체, 신뢰도, 용도 기록

data/source-tocs/
= 각 원천자료의 상세 목차

data/event-index/
= 사건, 인물, 장소, 시간, 전승 차이 index

data/theme-index/
= 주제, 교리, 정서, 핵심 메시지 index

data/alignment-map/
= 서로 다른 자료의 목차, 사건, 구절 대응표

data/excerpt-pools/
= 새 목차에 배치할 원천별 발췌 후보

data/outline-drafts/
= 새 목차 후보와 구성안

data/chapter-dossiers/
= 새 목차 항목별 source packet과 통합 메모

data/composition-plan/
= 최종 원고 구성 전략, 정서 흐름, 독자 경험 설계

data/meaning-units/
= 세그먼트와 별개로 의미 단위를 저장

data/interpretations/
= 의미 해석, 대안 해석, 불확실성, 근거 저장

data/claims/
= 문헌 또는 의미 단위가 말하는 핵심 주장 저장

data/doctrinal-links/
= 교리 개념, 관련 용어, 문헌 간 연결 저장

data/renderings/
= 직역형, 현대어형, 해설형, 에세이형 등 표현 후보 저장

data/manuscript-desk/
= 인간 최고편집장이 직접 탈고하는 최종 원고 작업 데이터

data/grounding/
= 표현과 원문 근거의 연결 저장

data/reader-profiles/
= 독자 대상과 표현 수준 정의

data/style-guides/
= 문체, 어조, 표현 밀도 기준 정의

data/media-sources/
= OL-TOON, OL-STUDIO 등 후속 제작 도구로 넘길 기초 원고 저장
```

`data/renderings/` 또는 `data/media-sources/`에는 다음 메타데이터를 포함하는 것을 검토한다.

```text
rendering_type
= literal_translation, creative_translation, commentary, essay, script, toon_source, studio_source

target_reader
= 일반 독자, 수행자, 연구자, 청소년, 영상 시청자 등

grounding_level
= direct, interpretive, expanded, adapted

creative_distance
= low, medium, high

source_basis
= 연결된 source segment, meaning_unit, interpretation ID

editor_decision
= 인간 최고편집장의 승인, 보류, 수정 필요 판단
```

기존 폴더는 폐기하지 않는다.

```text
source/
segments/
draft1~draft4/
terms/
annotations/
tags/
revisions/
notes/
handoff/
logs/
exports/
```

이들은 Source Layer와 Review Layer의 기반으로 유지한다.

---

# 15. OL-Runner 변경 방향

기존 OL-Runner 기획은 로컬 번역 파이프라인 실행기를 목표로 했다.

새 방향에서는 OL-Runner를 다음처럼 재정의한다.

```text
기존:
로컬 번역 파이프라인 실행기

전환:
원문 근거 기반 의미 해석·표현 후보 생성 실행기
```

새 stage 후보:

```text
source-collect
source-profile
toc-extract
event-index
theme-index
source-align
outline-generate
excerpt-assemble
chapter-dossier-build
composition-plan
source-map
literal-render
meaning-extract
context-map
doctrinal-link
interpretive-claim
rendering-generate
style-transform
grounding-check
meaning-risk-scan
export-compose
```

기존 번역 stage와의 관계:

```text
normalize-source
= Source Layer 유지

translate-draft1
= literal-render 또는 basic-render로 재정의

polish-draft2
= reader-facing-render 또는 style-transform으로 확장

review-source-alignment
= grounding-check로 확장

propose-annotations
= interpretation-note 또는 reader-support-note로 확장
```

---

# 16. OL-Runner의 새 역할

OL-Runner는 다음을 수행한다.

```text
1. 여러 원천자료의 목록과 성격 정리
2. 각 원천자료의 상세 목차 추출
3. 사건, 인물, 장소, 주제 index 생성
4. 목차·사건·주제 간 대응표 생성
5. 새 목차와 narrative architecture 후보 생성
6. 새 목차 항목별 source packet과 chapter dossier 생성
7. 원문 세그먼트와 의미 단위 후보 생성
8. 직역 또는 기본 번역 후보 생성
9. 핵심 의미 후보 추출
10. 교리적 맥락 후보 제안
11. 대안 해석 생성
12. 독자별 표현 후보 생성
13. 표현과 원문 근거 연결
14. 원문에서 멀어진 부분 경고
15. 인간이 판단할 수 있는 한국어 로그 작성
16. OL-DESK가 읽을 수 있는 구조화 데이터 저장
```

OL-Runner는 최종 의미 판단을 확정하지 않는다. 확정은 인간이 한다.

---

# 17. 한국어 로그 원칙

새 방향에서는 로그가 더 중요해진다. 단순히 “작업 완료”를 알리는 로그가 아니라, 인간이 해석 책임을 판단할 수 있게 도와야 한다.

OL-Runner가 생산하는 로그는 한국어 중심이어야 한다.

예시 필드:

```text
작업 단계
의미 작업 유형
원천자료
목차 항목
사건/주제 index
원문 근거
참조한 source packet
생성한 해석 후보
표현 후보
불확실성
원문에서 멀어진 지점
인간 확인 필요 항목
다음 권장 작업
```

기계 처리용 key는 영어를 쓸 수 있지만, OL-DESK에 표시되는 값은 한국어를 우선한다.

예:

```text
stage: meaning-extract
stage_label: 의미 후보 추출
summary_ko: 원문 세그먼트 001-003에서 핵심 의미 후보 2개를 추출했습니다.
human_check_required: true
human_check_reason_ko: 핵심 용어의 해석 범위가 넓어 인간 판단이 필요합니다.
grounding_note_ko: 표현 후보 2번은 원문보다 현대적 설명을 추가했습니다.
```

---

# 18. OL-DESK UI/UX 전환 방향

현재 OL-DESK는 번역 원고 탭 중심이다.

```text
1차원고
2차원고
3차원고
4차원고
비교해보기
```

새 방향에서는 “원고 탭”만으로 부족하다. 중심은 세그먼트와 의미 단위가 되어야 한다.

더 근본적으로 OL-DESK의 UX는 두 가지 핵심 모드로 재정의한다.

```text
Desk Mode
= 인간 최고편집장이 최종 원고를 탈고하는 Zen 스타일의 빈 책상

Source Board Mode
= 원천자료를 수집, 분류, 목차화, 사건화, 주제화하는 자료 보드

Meaning Board Mode
= 원문, 의미, 표현 후보, 용어, 각주, 메모, 근거를 한 번에 정리하는 보드판
```

두 모드는 단순 테마가 아니라 작업 성격의 차이다.

```text
Desk Mode
= 쓴다
= 문장, 리듬, 호흡, 의미 전달에 집중한다

Board Mode
= 판단한다
= 원문 근거, 해석, 대안, 표현 후보, 제작 자료를 비교한다

Source Board Mode
= 수집하고 분류한다
= 여러 원천자료의 목차, 사건, 주제, 발췌 후보를 비교한다
```

## 18.1 Desk Mode: Zen Writing Desk

Desk Mode는 “텅 빈 책상 위에 원고 하나만 올라가 있는” 경험을 목표로 한다.

목적:

```text
- 최종 원고 탈고
- 창조적 번역문 작성
- 해설글 작성
- 에세이 작성
- 대본 작성
- toon/studio 기초 원고 정리
```

UI 원칙:

```text
- 원고 본문을 화면 중심에 둔다.
- 로그, 상태표, 파일 경로, 토큰 정보는 숨긴다.
- 상단에는 문서명, 저장 상태, 산출물 유형, 모드 전환만 둔다.
- 보조 정보는 필요할 때 접힘 패널로 연다.
- 타이포그래피, 줄 간격, 여백은 장시간 읽기와 쓰기에 맞춘다.
- 원고 저장과 버전 관리는 조용하게 동작한다.
```

Desk Mode에서 보여줄 수 있는 원고 유형:

```text
- 창조적 번역
- 해설글
- 에세이
- 대본
- OL-TOON 기초 원고
- OL-STUDIO 기초 원고
```

Desk Mode에서 피해야 할 것:

```text
- 에이전트 로그 상시 노출
- JSON 필드 노출
- 과도한 배지와 상태 정보
- 여러 패널의 동시 노출
- 원고보다 UI가 더 강하게 보이는 구성
```

## 18.2 Source Board Mode: Multi-source Board

Source Board Mode는 모든 원고 작업의 첫출발인 레퍼런스 수집과 원천자료 정리를 담당한다.

목적:

```text
- 여러 원천자료 수집
- 자료 성격 분류
- 상세 목차 추출
- 사건과 주제 index 생성
- 목차 간 상호 비교
- 새 목차 후보 작성
- source packet과 chapter dossier 생성
```

권장 레이아웃:

```text
왼쪽: 원천자료 목록과 source profile
가운데: TOC Map / Event Map / Theme Map
오른쪽: 새 목차 후보와 chapter dossier
하단: 충돌, 중복, 누락, 보강점, 정서 흐름 메모
```

Source Board Mode에서 필요한 view:

```text
TOC View
= 원천자료별 상세 목차 비교

Event View
= 같은 사건이 여러 원천에서 어떻게 등장하는지 비교

Theme View
= 교리, 수행 의미, 정서, 핵심 메시지 비교

Narrative Arc View
= 새 원고의 정서적 곡선과 독자 경험 설계
```

## 18.3 Meaning Board Mode: Meaning Board

Meaning Board Mode는 “최종 원고를 위해 필요한 의미와 표현 정보를 정리한 보드판”이다.

목적:

```text
- 원문 근거 확인
- 의미 단위 정리
- 대안 해석 비교
- 용어/각주/태그 판단
- 창조적 표현 후보 비교
- 원문에서 멀어진 표현 확인
- toon/studio 제작용 장면·대본 단서 정리
```

권장 레이아웃:

```text
왼쪽: 원문과 직역
가운데: 의미 해석과 인간 판단
오른쪽: 표현 후보와 제작 메모
하단: 용어, 각주, 태그, 근거, 불확실성, 로그
```

Meaning Board Mode는 정보량이 많아도 되지만 무질서해서는 안 된다. 중심은 항상 현재 선택된 `meaning_unit` 또는 원고 구간이어야 한다.

## 18.4 번역 화면의 새 중심

권장 레이아웃:

```text
왼쪽: 원문 세그먼트와 직역
가운데: 의미 해석과 인간 판단
오른쪽: 표현 후보와 최종 문장
```

또는 카드형:

```text
의미 단위 카드
  - 원문
  - 직역
  - 핵심 뜻
  - 대안 해석
  - 표현 후보
  - 최종 표현
  - 근거 강도
  - 불확실성
  - 관련 용어/각주/태그
```

## 18.5 즉시 수정 가능한 UX

감수자는 전체 Markdown textarea만으로 작업하기 어렵다. 문단 또는 의미 단위별로 바로 수정할 수 있어야 한다.

필요한 기능:

```text
- 원문 세그먼트 옆에서 번역문 바로 수정
- 의미 해석 후보 선택 또는 수정
- 표현 후보 중 선택
- 최종 표현 직접 작성
- 수정 전/후 비교
- 원문 근거 확인
- 해석 메모 추가
- 보류 판단 유지
```

## 18.6 감수 집중도

OL-DESK는 기능을 많이 보여주는 도구가 아니라 집중을 돕는 작업실이어야 한다.

UI 원칙:

```text
- 원문과 최종 표현을 가장 크게 보여준다.
- 로그와 실행 정보는 접어서 둔다.
- AI 평가와 운영 진단은 보조 화면으로 보낸다.
- 의미 판단에 필요한 용어, 각주, 메모만 세그먼트별로 보여준다.
- 감수자가 지금 해야 할 다음 행동을 명확히 보여준다.
```

## 18.7 모드 전환 원칙

Desk Mode, Source Board Mode, Meaning Board Mode는 서로 대체 관계가 아니라 왕복 관계다.

```text
Source Board Mode에서 원천자료와 새 목차를 정리한다.
Meaning Board Mode에서 근거와 후보를 판단한다.
Desk Mode에서 최종 문장으로 쓴다.
다시 Meaning Board Mode에서 원문 근거와 창작 거리를 확인한다.
Desk Mode에서 원고를 탈고한다.
```

따라서 OL-DESK는 현재 원고 구간 또는 meaning_unit을 유지한 채 두 모드를 전환할 수 있어야 한다.

---

# 19. 새로운 작업 단위

기존 작업 단위:

```text
document
segment
draft
status
```

새 작업 단위:

```text
source_collection
source_profile
source_toc
event
theme
alignment
excerpt
source_packet
chapter_dossier
outline_draft
composition_plan
document
segment
meaning_unit
interpretation
claim
rendering
grounding
review_decision
export_version
```

이 중 초기 창작 단계에서는 `source_collection`, `event`, `chapter_dossier`, `outline_draft`가 중요하다. 의미 해석 단계에서는 `meaning_unit`이 중요하다. OL-DESK가 단순 번역 도구에서 창작 편집 책상으로 바뀌려면, 원천자료 수집 단위와 의미 단위를 모두 중심 작업 단위로 다룰 수 있어야 한다.

---

# 20. 기존 시스템과의 관계

기존 시스템을 즉시 폐기하지 않는다.

유지:

```text
- Contents-Asset 기본 폴더
- 원문/정리본/세그먼트
- draft1~draft4
- terms/annotations/tags
- notes/revisions
- handoff/export
- OL-DESK Astro 구조
- OL-Runner 로컬 실행 방향
```

변경:

```text
- 단일 원전 중심에서 다중 원천자료 통합 중심으로 확장
- 번역본 중심에서 의미 단위 중심으로 이동
- agent-log 중심에서 meaning-log 중심으로 확장
- draft 중심 UI에서 자료/원문/뜻/표현/원고 5층 UI로 전환
- Paperclip 조직형 에이전트 구조는 장기적으로 폐기
```

---

# 21. OL-TOON / OL-STUDIO와의 관계

OL-DESK는 OL-TOON과 OL-STUDIO의 후속 제작을 위한 기초 원고 생산지 역할을 맡을 수 있다.

관계 정의:

```text
OL-DESK
= 원문 기반 의미 해석, 최종 원고, 창조적 번역, 해설글, 에세이, 대본, media source 생산

OL-TOON
= OL-DESK의 toon_source를 바탕으로 컷, 장면, 대사, 내레이션, 시각적 흐름 제작

OL-STUDIO
= OL-DESK의 studio_source를 바탕으로 영상, 오디오, 강의, 인터랙션, 장면 연출 제작
```

OL-DESK가 생산해야 할 후속 제작용 기초 원고:

```text
toon_source
  - 장면 단위 요약
  - 컷 후보
  - 대사 후보
  - 내레이션 후보
  - 핵심 이미지
  - 원문 근거

studio_source
  - 영상/오디오 대본
  - 장면 구성
  - 진행자 또는 내레이션 문장
  - 강조할 의미 단위
  - 시각·청각 연출 메모
  - 원문 근거
```

주의할 점:

```text
- OL-TOON/OL-STUDIO용 원고는 원문 번역이 아니라 매체 각색일 수 있다.
- 각색 단계에서는 creative_distance가 높아질 수 있다.
- 그러므로 source_basis와 grounding_level을 반드시 남긴다.
- 후속 제작 도구는 OL-DESK 원고를 근거로 삼되, 원문 직접 해석 권한을 대신하지 않는다.
```

---

# 22. 단계적 전환 로드맵

## Phase 0. 개념 정리

```text
- OL-DESK의 새 목적 정의
- 다중 원천자료 기반 창작 흐름 정의
- Meaning Layer 개념 확정
- 의미 단위와 세그먼트의 관계 정의
- 목차, 사건, 주제, 정서 흐름의 관계 정의
- 창조적 재표현의 허용 범위 정의
- 원문 근거 보존 원칙 정의
```

## Phase 1. 데이터 구조 초안

```text
- data/source-collections/ 초안
- data/source-tocs/ 초안
- data/event-index/ 초안
- data/theme-index/ 초안
- data/alignment-map/ 초안
- data/chapter-dossiers/ 초안
- data/meaning-units/ 초안
- data/interpretations/ 초안
- data/renderings/ 초안
- data/grounding/ 초안
- 한국어 meaning-log 필드 초안
```

## Phase 2. OL-DESK Source Board MVP

```text
- 원천자료 등록
- 상세 목차 추출 결과 보기
- TOC View / Event View / Theme View
- 새 목차 후보 작성
- chapter dossier 생성 화면
```

## Phase 3. OL-DESK 의미 단위 뷰

```text
- 원문 세그먼트와 번역문 병렬 보기
- 의미 후보 패널
- 표현 후보 패널
- 세그먼트/의미 단위별 수정 UI
- 보류/확정/재검토 상태 표시
```

## Phase 4. OL-Runner 자료 정리 MVP

```text
- source-profile
- toc-extract
- event-index
- theme-index
- source-align
- outline-generate
- chapter-dossier-build
- 한국어 source-log 생성
```

## Phase 5. OL-Runner 의미 보조 MVP

```text
- meaning-extract
- literal-render
- rendering-generate
- grounding-check
- 한국어 로그 생성
- OL-DESK 표시 연동
```

## Phase 6. 창작형 산출물

```text
- 현대어 재표현 원고
- 해설형 원고
- 에세이형 원고
- 강의용 원고
- 창조적 번역 원고
- OL-TOON 기초 원고
- OL-STUDIO 기초 원고
- 독자별 export
```

## Phase 7. 품질과 책임 체계

```text
- 원천자료별 근거 표시
- 원문 근거 강도 표시
- 원문에서 멀어진 표현 경고
- source conflict 표시
- 인간 해석 승인 기록
- 대안 해석 보존
- revision cycle 확장
```

## Phase 8. Desk / Board Mode 구현

```text
- Desk Mode 원고 집중 화면
- Source Board Mode 자료 보드 화면
- Meaning Board Mode 의미 보드 화면
- 같은 meaning_unit을 유지한 모드 전환
- 창작 거리와 원문 근거 표시
- 산출물 유형별 원고 편집 UX
```

## Phase 9. OL-TOON / OL-STUDIO 연계

```text
- toon_source 스키마
- studio_source 스키마
- media source export
- 장면/컷/대본 후보 생성
- 후속 제작 도구에서 읽을 수 있는 구조화 출력
```

---

# 23. 위험 요소

## 23.1 범위 확대

의미 창작 환경은 단순 번역 도구보다 훨씬 넓다.

대응:

```text
- 한 문서, 한 세그먼트, 한 의미 단위부터 시작한다.
- 기존 draft 생산 기능을 완전히 버리지 않는다.
- Meaning Layer를 작은 실험으로 추가한다.
```

## 23.2 원문 이탈

뜻을 드러내려는 과정에서 원문에 없는 것을 과도하게 추가할 수 있다.

대응:

```text
- 모든 표현 후보에 원문 근거를 연결한다.
- 원문과의 거리 또는 근거 강도를 표시한다.
- 인간이 창조적 확장을 승인했는지 기록한다.
```

## 23.3 UI 과밀화

원문, 직역, 의미, 해석, 표현, 메모, 로그를 모두 보이면 화면이 복잡해진다.

대응:

```text
- 기본 화면은 원문/뜻/표현만 보여준다.
- 로그와 운영 정보는 접는다.
- 세그먼트 또는 의미 단위별로 필요한 정보만 보여준다.
```

## 23.4 완료 기준 불명확

창작형 작업은 끝이 없을 수 있다.

대응:

```text
- 각 meaning_unit에 상태를 둔다.
- interpretation 확정 여부를 둔다.
- rendering 승인 여부를 둔다.
- export 목적별 완료 기준을 둔다.
```

## 23.5 창작과 번역의 혼동

창조적 번역, 해설글, 에세이, toon/studio 기초 원고가 모두 같은 화면에서 생성되면 사용자가 산출물의 성격을 혼동할 수 있다.

대응:

```text
- 모든 산출물에 rendering_type을 명시한다.
- 원문 근거 수준과 창작 거리를 표시한다.
- Desk Mode에서도 현재 원고가 번역인지, 해설인지, 대본인지 명확히 보여준다.
- export 시 산출물 유형을 파일명과 메타데이터에 남긴다.
```

## 23.6 원천자료 통합의 왜곡

여러 원천자료를 통합할 때 서로 다른 전승의 차이를 무리하게 하나로 합치면 원천자료 고유의 의미가 왜곡될 수 있다.

대응:

```text
- source_profile에 각 자료의 성격과 한계를 기록한다.
- event alignment에서 충돌, 누락, 중복을 명시한다.
- 새 목차에 반영된 자료와 제외된 자료를 기록한다.
- 통합 원고와 원천자료 발췌를 분리한다.
- chapter dossier에는 원천별 차이를 보존한다.
```

## 23.7 대중적 소구와 원전 근거의 긴장

감동을 자아내는 원고를 만들기 위해 사건 순서, 표현, 장면성을 조정할 수 있다. 그러나 대중적 소구만 앞세우면 원전 근거와 수행적 의미가 약해질 수 있다.

대응:

```text
- narrative arc와 source grounding을 함께 본다.
- 각 장의 emotional_function과 source_basis를 같이 기록한다.
- 각색은 adapted로 표시한다.
- 인간 최고편집장이 창작적 변경을 명시적으로 승인한다.
```

---

# 24. 새 방향의 성공 기준

OL-DESK가 새 방향으로 성공하려면 다음 질문에 답할 수 있어야 한다.

```text
이 문장은 원문 어디에 근거하는가?
이 구절의 핵심 뜻은 무엇인가?
다른 해석 가능성은 무엇인가?
왜 이 표현을 선택했는가?
이 표현은 원문보다 얼마나 확장되었는가?
이 장면은 어떤 원천자료들에 근거하는가?
서로 다른 원천자료의 차이를 어떻게 처리했는가?
이 사건은 새 목차에서 왜 이 위치에 배치되었는가?
이 장의 정서적 기능은 무엇인가?
어떤 독자를 위해 쓴 문장인가?
인간은 어디에 책임 판단을 남겼는가?
최종 산출물은 번역인가, 해설인가, 재표현인가?
이 원고는 OL-TOON/OL-STUDIO 제작에 바로 넘길 수 있는가?
이 문장은 원문 기반 표현인가, 해석적 확장인가, 매체 각색인가?
```

이 질문에 답할 수 없다면 OL-DESK는 여전히 단순 번역 도구에 머문다.

---

# 25. 결론

OL-DESK의 장기적 가치는 번역 자동화에 있지 않다. 단순 번역 자동화는 시간이 지나면 흥미를 잃고, 프로젝트의 본래 취지와도 멀어질 수 있다.

OL-DESK의 장기적 가치는 다음에 있다.

```text
여러 원천자료를 수집하고 정리하며
목차, 사건, 주제, 정서 흐름을 비교하고
새로운 원고 구조를 설계하며
원문을 근거로 뜻을 발견하고
그 뜻을 인간이 책임 있게 해석하며
현대 독자에게 살아 있는 표현으로 다시 구성하는 것
그리고 그 표현을 OL-TOON, OL-STUDIO 같은 후속 제작 환경으로 이어질 수 있는 기초 원고로 만드는 것
```

따라서 OL-DESK는 번역 도구에서 의미 작업 환경으로 전환해야 한다.

OL-Runner는 번역 생산기가 아니라 의미 해석과 표현 생성을 돕는 로컬 실행기가 되어야 한다.

Contents-Asset은 번역 산출물 저장소를 넘어 Source Collection, Source, Synthesis, Meaning, Rendering, Review, Export를 담는 창작 작업 저장소가 되어야 한다.

OL-DESK의 UX는 두 가지 중심 모드를 가져야 한다.

```text
Desk Mode
= Zen 스타일의 빈 책상 위 최종 원고

Board Mode
= 원천자료, 원문, 의미, 표현, 근거, 제작 자료를 정리하는 보드판
```

이 전환은 프로젝트를 더 어렵게 만들지만, 동시에 OL-프로젝트의 본래 취지에 더 가깝게 만든다.
