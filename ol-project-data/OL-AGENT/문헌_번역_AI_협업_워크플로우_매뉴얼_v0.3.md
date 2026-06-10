# 문헌 번역 AI 협업 워크플로우 매뉴얼 v0.3

## 다중문서·대량문헌 운영형 — 차수별 번역본 분리 구조

**문서명:** 문헌 번역 AI 협업 워크플로우 매뉴얼  
**버전:** v0.3  
**적용 범위:** 불교 경전·논서·주석서·전기문헌 등 다중 문서 번역 프로젝트  
**작업 방식:** 1인 제작자 + AI 다중 에이전트 협업  
**핵심 목표:** 문서가 100개, 500개 이상으로 늘어나도 관리 가능한 번역·감수·용어집·각주·해석·탈고 체계 구축  
**이번 버전의 초점:** 텍스트 번역, 원문 대조, 인간 검수, 최종 원고 탈고  
**제외 범위:** 출판, 웹 등록, 디자인, 온톨로지, 지식그래프, 엔티티 구조화, 콘텐츠 배포 파이프라인

---

# 0. v0.3의 핵심 변경점

v0.2는 문서 수가 많아질 때 산출물 폭증을 막기 위해 “문서별 통합 원고 파일” 방식을 제안했다. 그러나 실제 원본 소스 파일을 검토하면, 하나의 파일 안에 원문·1차 번역·2차 번역·3차 번역·최종본·감수 요약을 모두 넣는 방식은 긴 문헌에서 다시 문제가 된다.

v0.3에서는 다음 원칙으로 바꾼다.

```text
문서별 통합 원고 1파일 방식을 기본값으로 삼지 않는다.
원본, 정규화 원문, 참고 번역, 1차 번역, 2차 번역, 3차 번역, 최종본을 목적별 폴더에 분리한다.
용어집·각주집·해석집은 프로젝트 단위로 누적 관리한다.
전체 진행 상태는 master-checklist.md에서 관리한다.
문서 연결성은 doc_id와 가벼운 metadata 파일로 유지한다.
검색·AI·온톨로지용 entities 구조화는 이번 매뉴얼에서 다루지 않는다.
```

즉, v0.3의 기본 구조는 다음이다.

```text
프로젝트 공통 파일
+ 문서별 metadata 파일
+ 원본 보존 폴더
+ 차수별 번역본 폴더
+ 검토 결과 폴더
+ 필요 시 임시 작업 폴더
```

이 구조의 핵심은 “기계적 연결성”이 아니라 “실제 번역 작업의 가독성과 지속 가능성”이다. AI와 사람 모두가 특정 단계의 파일만 열어 작업할 수 있어야 한다.

---

# 1. 전체 폴더 구조

```text
translation-project/
├─ project-index.md
├─ master-checklist.md
├─ style-guide.md
├─ editorial-decisions.md
├─ cumulative-glossary.md
├─ cumulative-annotations.md
├─ cumulative-interpretations.md
│
├─ docs-meta/
│  ├─ gcb-094-39b-sakka-questions.meta.md
│  └─ kabc-k0802-t060.meta.md
│
├─ sources/
│  ├─ raw/
│  │  ├─ gcb-094-39b-sakka-questions.md
│  │  └─ kabc-k0802-t060.md
│  └─ normalized/
│     ├─ gcb-094-39b-sakka-questions.src.md
│     └─ kabc-k0802-t060.src.md
│
├─ references/
│  ├─ kabc-k0802-t060.korean-reference.md
│  └─ ...
│
├─ translations/
│  ├─ draft1/
│  │  ├─ gcb-094-39b-sakka-questions.draft1.md
│  │  └─ kabc-k0802-t060.draft1.md
│  ├─ draft2/
│  │  ├─ gcb-094-39b-sakka-questions.draft2.md
│  │  └─ kabc-k0802-t060.draft2.md
│  ├─ draft3/
│  │  ├─ gcb-094-39b-sakka-questions.draft3.md
│  │  └─ kabc-k0802-t060.draft3.md
│  └─ final/
│     ├─ gcb-094-39b-sakka-questions.final.md
│     └─ kabc-k0802-t060.final.md
│
├─ reviews/
│  ├─ source-review/
│  │  ├─ gcb-094-39b-sakka-questions.source-review.md
│  │  └─ kabc-k0802-t060.source-review.md
│  ├─ human-review/
│  │  ├─ gcb-094-39b-sakka-questions.human-review.md
│  │  └─ kabc-k0802-t060.human-review.md
│  └─ final-scan/
│     ├─ gcb-094-39b-sakka-questions.final-scan.md
│     └─ kabc-k0802-t060.final-scan.md
│
└─ workbench/
   ├─ gcb-094-39b-sakka-questions.translation-alternatives.md
   ├─ kabc-k0802-t060.glossary-conflict.md
   └─ ...
```

`workbench/`는 선택 사항이다. 임시 리포트, 여러 번역안 비교, 난해 구문 분석 등 정식 산출물로 남기기 애매한 작업만 보관한다.

---

# 2. 산출물 설계 원칙

## 2.1 반드시 보존할 산출물

대량 문헌 번역에서 반드시 필요한 산출물은 다음이다.

```text
1. master-checklist.md
2. cumulative-glossary.md
3. cumulative-annotations.md
4. cumulative-interpretations.md
5. docs-meta/{문서ID}.meta.md
6. sources/raw/{문서ID}.md
7. sources/normalized/{문서ID}.src.md
8. translations/draft1/{문서ID}.draft1.md
9. translations/draft2/{문서ID}.draft2.md
10. translations/draft3/{문서ID}.draft3.md
11. translations/final/{문서ID}.final.md
```

여기에 보조적으로 다음 파일을 둔다.

```text
12. project-index.md
13. style-guide.md
14. editorial-decisions.md
15. reviews/source-review/{문서ID}.source-review.md
16. reviews/human-review/{문서ID}.human-review.md
17. reviews/final-scan/{문서ID}.final-scan.md
```

## 2.2 선택 산출물

다음은 반드시 파일로 남길 필요가 없다.

```text
1차 번역 에이전트의 중간 설명
2차 번역의 모든 수정 과정
3차 번역 변경 로그 전체
각주 후보 생성 과정 전체
해석 후보 생성 과정 전체
```

다만 다음 경우에는 `workbench/`에 별도 임시 파일로 남길 수 있다.

```text
오역 후보가 많아 상세 검토가 필요한 문서
여러 번역안 비교가 필요한 문서
교학적 쟁점이 큰 문서
용어 충돌이 많은 문서
사람이 나중에 다시 검토해야 할 문서
```

## 2.3 v0.3에서 하지 않는 것

이번 매뉴얼은 콘텐츠 1차 생산, 번역 품질, 원고 탈고에 집중한다. 따라서 다음은 다루지 않는다.

```text
entities 구조화
triple 관계 추출
온톨로지 설계
지식그래프 구축
검색 인덱스 최적화
Astro frontmatter 연동
OL HOME 등록
OL BOOK 출판
```

이 항목들은 모든 문서의 1차 생산과 탈고 경험이 쌓인 뒤 별도 매뉴얼에서 검토한다.

---

# 3. 프로젝트 공통 파일

## 3.1 `project-index.md`

프로젝트의 기본 정보를 기록하는 파일이다.

```markdown
# 번역 프로젝트 인덱스

## 1. 프로젝트 정보

- 프로젝트명:
- 문헌군:
- 작업 범위:
- 기준 원문:
- 보조 원문:
- 참고 번역:
- 목표 독자:
- 목표 문체:
- 작업 시작일:
- 현재 버전:

## 2. 번역 원칙

- 원문 의미 보존을 우선한다.
- 원문에 없는 해석은 본문에 넣지 않는다.
- 교학 용어는 가능한 한 일관되게 번역한다.
- 필요한 설명은 각주 또는 해설로 분리한다.
- 최종 판정은 인간 편집자가 한다.

## 3. 문서 ID 규칙

예:
T001, T002, T003 ...
또는
MN-001, DN-001, BS-01-001, GCB-094-39B 등
```

---

## 3.2 `master-checklist.md`

전체 진행 상황을 관리하는 핵심 파일이다.

```markdown
# 전체 문서 진행 체크리스트

| ID | 문서명 | 원문정리 | 1차번역 | 원문대조 | 각주/해석 | 2차번역 | 인간검수 | 3차번역 | 최종스캔 | 탈고 | 비고 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gcb-094-39b-sakka-questions | 삭카의 질문 | [x] | [x] | [x] | [x] | [x] | [ ] | [ ] | [ ] | [ ] | 용어 확정 대기 |
| kabc-k0802-t060 | 불본행집경 권60 | [x] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | 참고번역 분리 필요 |
```

문서 수가 많을 경우 상태값을 간단히 줄일 수도 있다.

```markdown
| ID | 문서명 | 상태 | 다음 작업 | 담당 | 비고 |
|---|---|---|---|---|---|
| gcb-094-39b-sakka-questions | 삭카의 질문 | draft2_done | 인간검수 | 사람 | 신규 용어 5개 확정 필요 |
| kabc-k0802-t060 | 불본행집경 권60 | source_ready | 1차번역 | AI | KABC 참고번역 있음 |
```

권장 상태값은 다음과 같다.

```text
not_started
raw_collected
source_ready
reference_ready
glossary_candidate_done
draft1_done
source_review_done
annotation_candidate_done
draft2_done
human_review_done
draft3_done
final_scan_done
final_done
hold
```

---

## 3.3 `style-guide.md`

번역 문체와 형식 규칙을 저장한다.

```markdown
# 번역 문체 가이드

## 1. 번역 비율

### 1차 번역
- 직역 7 + 의역 3
- 원문 구조 보존 우선
- 한국어가 다소 딱딱해도 허용

### 2차 번역
- 직역 3 + 의역 7
- 자연스러운 한국어 독서문체
- 단, 원문에 없는 해석 삽입 금지

### 3차 번역
- 확정 용어집 반영
- 확정 각주·해석 반영
- 의미 재해석 금지
- 2차 번역의 문체 유지

## 2. 용어 원칙

- 핵심 교학 용어는 누적 용어집을 우선 따른다.
- 미확정 용어는 원어 또는 한자를 병기한다.
- 새 용어는 신규 용어 후보표에 등록한다.

## 3. 각주 원칙

- 첫 출현 용어에는 필요한 경우 짧은 각주를 둔다.
- 본문 흐름을 방해하는 긴 해석은 해설로 분리한다.
- 출처가 불확실한 설명은 확정 각주로 넣지 않는다.

## 4. 해석 원칙

- 해석은 본문 번역과 구분한다.
- 특정 전통의 해석을 본문에 단정적으로 삽입하지 않는다.
- 해석 후보는 사람이 승인한 뒤 반영한다.
```

---

## 3.4 `editorial-decisions.md`

사람이 내린 중요한 판단을 누적한다.

```markdown
# 편집 결정 기록

## 2026-06-04

### 결정 1
`dukkha`는 기본적으로 “괴로움”으로 번역한다.

- 이유:
- 적용 범위:
- 예외:

### 결정 2
`deva`는 서사 문맥에서는 “천신”으로 번역한다.

- 이유:
- 적용 범위:
- 예외:
```

이 파일은 프로젝트 전체의 일관성을 유지하는 데 중요하다.

---

## 3.5 `cumulative-glossary.md`

프로젝트 전체에서 확정된 용어를 누적한다.

```markdown
# 누적 용어집

| 원문 | 원전언어 | 확정 번역어 | 대안 | 사용 원칙 | 최초 확정 문서 | 비고 |
|---|---|---|---|---|---|---|
| dukkha | pali | 괴로움 | 고통, 불만족 | 사성제·교학 문맥 기본 번역어 | gcb-094-39b | 신체적 pain은 고통 가능 |
| dhamma | pali | 법 | 가르침 | 교학 핵심어는 법, 설법 내용은 가르침 가능 | gcb-094-39b | 문맥 판단 |
| bodhisatta | pali | 보살 | 구도자 | 성도 이전 싯다르타 문맥 | T001 | 첫 출현 시 주석 |
```

---

## 3.6 `cumulative-annotations.md`

확정된 각주를 누적한다.

```markdown
# 누적 각주집

| ID | 대상어 | 확정 각주 | 적용 원칙 | 최초 사용 문서 | 비고 |
|---|---|---|---|---|---|
| ANNO-001 | 보살 | 여기서 보살은 성불 이전의 구도자로서의 bodhisatta를 가리킨다. | 첫 출현 시 사용 | T001 | 대승 보살 일반과 구분 |
| ANNO-002 | 도솔천 | 도솔천은 욕계 육천 가운데 하나로, 보살이 인간계에 태어나기 전 머무는 하늘로 설명된다. | 첫 출현 시 사용 | T001 |  |
```

---

## 3.7 `cumulative-interpretations.md`

확정된 해석 방향을 누적한다.

```markdown
# 누적 해석집

| ID | 주제 | 확정 해석 요지 | 사용 방식 | 최초 사용 문서 | 비고 |
|---|---|---|---|---|---|
| INT-001 | 보살의 하강 | 보살의 하강은 중생 세계로 들어가는 자비의 결단으로 해석할 수 있다. | 해설문 | T001 | 본문 삽입 금지 |
| INT-002 | 태몽 서사 | 태몽은 성자의 탄생을 상징화하는 불전 서사 장치로 볼 수 있다. | 해설 또는 각주 | T002 | 표현 주의 |
```

---

# 4. 문서별 metadata 파일

각 문서의 파일 연결 정보와 작업 상태는 `docs-meta/{문서ID}.meta.md`에 기록한다. 이 파일은 온톨로지나 지식그래프용 파일이 아니라, 번역 작업자가 파일 경로를 잃지 않기 위한 작업용 안내 파일이다.

```text
docs-meta/gcb-094-39b-sakka-questions.meta.md
docs-meta/kabc-k0802-t060.meta.md
```

## 4.1 metadata 파일 템플릿

```markdown
---
doc_id: "gcb-094-39b-sakka-questions"
title_ko: "삭카의 질문"
title_original: "Sakka’s Questions"
source_language: "english"
base_text_language: "pali-related english retelling"
status: "draft1_done"
created: "2026-06-04"
updated: "2026-06-04"
tags:
  - "문헌:삭카빤하숫따(sakka-pañha-sutta)"
  - "인물:삭카(sakka)"
  - "인물:빤짜시카(pañcasikha)"
  - "장소:인다살라 동굴(indasāla guhā)"
  - "언어:영어"
  - "전통:상좌부"
---

# gcb-094-39b-sakka-questions metadata

## 1. 파일 경로

| 구분 | 경로 |
|---|---|
| 원본 | sources/raw/gcb-094-39b-sakka-questions.md |
| 정규화 원문 | sources/normalized/gcb-094-39b-sakka-questions.src.md |
| 참고 번역 | 없음 |
| 1차 번역 | translations/draft1/gcb-094-39b-sakka-questions.draft1.md |
| 2차 번역 | translations/draft2/gcb-094-39b-sakka-questions.draft2.md |
| 3차 번역 | translations/draft3/gcb-094-39b-sakka-questions.draft3.md |
| 최종본 | translations/final/gcb-094-39b-sakka-questions.final.md |
| 원문대조 | reviews/source-review/gcb-094-39b-sakka-questions.source-review.md |
| 인간검수 | reviews/human-review/gcb-094-39b-sakka-questions.human-review.md |
| 최종스캔 | reviews/final-scan/gcb-094-39b-sakka-questions.final-scan.md |

## 2. 작업 메모

- 
```

## 4.2 KABC 한문 파일 metadata 예시

KABC처럼 한문 원문과 기존 한글 번역이 함께 있는 경우, 기존 한글 번역은 AI 번역 차수가 아니라 `references/`의 참고 번역으로 둔다.

```markdown
---
doc_id: "kabc-k0802-t060"
title_ko: "불본행집경 권60"
title_original: "佛本行集經卷第六十"
source_language: "classical_chinese"
reference_language: "korean"
status: "source_ready"
created: "2026-06-04"
updated: "2026-06-04"
tags:
  - "문헌:불본행집경(佛本行集經)"
  - "인물:마니루타(摩尼婁陀)"
  - "인물:아난다(阿難陀)"
  - "장소:파라내성(波羅柰城)"
  - "언어:한문"
  - "언어:한국어"
---

# kabc-k0802-t060 metadata

## 1. 파일 경로

| 구분 | 경로 |
|---|---|
| 원본 | sources/raw/kabc-k0802-t060.md |
| 정규화 원문 | sources/normalized/kabc-k0802-t060.src.md |
| 참고 번역 | references/kabc-k0802-t060.korean-reference.md |
| 1차 번역 | translations/draft1/kabc-k0802-t060.draft1.md |
| 2차 번역 | translations/draft2/kabc-k0802-t060.draft2.md |
| 3차 번역 | translations/draft3/kabc-k0802-t060.draft3.md |
| 최종본 | translations/final/kabc-k0802-t060.final.md |
| 원문대조 | reviews/source-review/kabc-k0802-t060.source-review.md |
| 인간검수 | reviews/human-review/kabc-k0802-t060.human-review.md |
| 최종스캔 | reviews/final-scan/kabc-k0802-t060.final-scan.md |
```

---

# 5. 메타데이터 태그 규칙

## 5.1 기본 원칙

메타데이터 태그는 한글 중심으로 작성한다. 모든 태그는 prefix 방식을 사용한다. 한자·빨리어·범어 용어는 한글 표제 뒤 괄호 안에 원전언어를 병기한다.

```text
한글 중심
prefix 사용
한글(원전언어) 병기
빨리어·범어 로마나이즈는 소문자
태그는 표시용·작업용 키워드로만 사용
entities 구조화는 하지 않음
```

## 5.2 prefix 표준

우선 다음 prefix만 사용한다.

```text
인물:
장소:
문헌:
교리:
수행:
사건:
비유:
전통:
언어:
시대:
장르:
상태:
작업:
```

필요할 때만 새 prefix를 추가하고, 추가한 prefix는 `style-guide.md`에 기록한다.

## 5.3 원전언어 병기 규칙

```text
빨리어: 한글(소문자 로마나이즈)
범어: 한글(소문자 로마나이즈)
한문: 한글(漢字)
티베트어: 한글(wylie)
영어 원본: 한글(english term)
```

예시:

```text
인물:아난다(ānanda)
인물:삭카(sakka)
인물:아난다(阿難陀)
장소:라자가하(rājagaha)
장소:파라내성(波羅柰城)
문헌:삭카빤하숫따(sakka-pañha-sutta)
문헌:불본행집경(佛本行集經)
교리:연기(paṭiccasamuppāda)
교리:연기(緣起)
수행:사념처(satipaṭṭhāna)
언어:빨리어
언어:한문
전통:상좌부
장르:불전
상태:1차번역완료
```

## 5.4 로마나이즈 소문자 원칙

메타데이터와 태그에서는 빨리어·범어 로마나이즈를 소문자로 통일한다.

```text
Ānanda → ānanda
Sakka → sakka
Rājagaha → rājagaha
Dhamma → dhamma
Bodhisattva → bodhisattva
Paṭiccasamuppāda → paṭiccasamuppāda
```

본문 번역문 안에서는 문장 첫머리, 고유명사 표기, 인용문 관례에 따라 대문자를 쓸 수 있다. 소문자 통일은 메타데이터와 태그에만 적용한다.

## 5.5 태그 사용 범위

태그는 다음 용도로만 사용한다.

```text
문서 검색 보조
작업 묶음 구분
주요 인물·장소·문헌·교리 확인
문서 상태 확인
작업자가 빠르게 문맥을 파악하기 위한 표시
```

태그를 관계 구조로 해석하지 않는다. 예를 들어 아래 태그들은 단지 이 문서와 관련된 키워드일 뿐이다.

```yaml
tags:
  - "인물:아난다(ānanda)"
  - "인물:붓다(buddha)"
  - "장소:라자가하(rājagaha)"
```

위 태그만으로 “아난다가 붓다의 시자이다” 또는 “라자가하에서 특정 사건이 일어났다”와 같은 관계를 만들지 않는다. 그런 작업은 훗날 별도 검토한다.

---

# 6. 파일별 템플릿

## 6.1 정규화 원문 파일

경로:

```text
sources/normalized/{문서ID}.src.md
```

템플릿:

```markdown
---
doc_id: ""
title_ko: ""
title_original: ""
source_language: ""
status: "source_ready"
tags:
  - ""
---

# {{문서명}} — 정규화 원문

## 1. Source Note

- 원본 출처:
- 원본 파일:
- 정규화 기준:
- 생략·수정 여부:

---

## 2. Segment Index

| 문단 ID | 원문 시작어 | 비고 |
|---|---|---|
| 001 |  |  |
| 002 |  |  |

---

## 3. Source Text

### [001]
원문을 입력한다.

### [002]
원문을 입력한다.
```

정규화 원문은 원본을 임의로 고치는 파일이 아니다. 줄바꿈, 문단 번호, OCR 오류 수정, 한문·번역문 분리처럼 작업 편의를 위한 정리만 한다.

---

## 6.2 참고 번역 파일

경로:

```text
references/{문서ID}.korean-reference.md
```

템플릿:

```markdown
---
doc_id: ""
title_ko: ""
reference_source: ""
reference_language: "korean"
status: "reference_ready"
tags:
  - "언어:한국어"
---

# {{문서명}} — 참고 번역

## 1. Reference Note

- 참고 번역 출처:
- 번역자:
- 수집일:
- 사용 원칙:

이 파일은 AI 번역 차수가 아니다.
원문 대조와 표현 참고를 위한 보조 자료이다.

---

## 2. Reference Translation

### [001]
참고 번역문을 입력한다.

### [002]
참고 번역문을 입력한다.
```

KABC처럼 원문과 한글 번역이 함께 있는 경우, 한글 번역은 이 파일로 분리한다. AI는 이것을 “정답”으로 간주하지 않고 참고 자료로만 사용한다.

---

## 6.3 1차 번역 파일

경로:

```text
translations/draft1/{문서ID}.draft1.md
```

템플릿:

```markdown
---
doc_id: ""
title_ko: ""
draft_stage: "draft1"
status: "draft1_done"
tags:
  - "작업:1차번역"
---

# {{문서명}} — 1차 번역

## 1. Translation Principle

- 직역 7 + 의역 3
- 원문 구조 보존
- 미확정 용어는 원어 또는 한자 병기
- 아름다운 문체보다 원문 대응성 우선

---

## 2. Draft 1

### [001]
1차 번역을 입력한다.

### [002]
1차 번역을 입력한다.

---

## 3. New Glossary Candidates

| 확인 | 원문 | 원전언어 | 제안 번역어 | 대안 | 문단 | 상태 | 비고 |
|---|---|---|---|---|---|---|---|
| [ ] |  |  |  |  |  | candidate |  |
```

---

## 6.4 원문대조 감수 파일

경로:

```text
reviews/source-review/{문서ID}.source-review.md
```

템플릿:

```markdown
---
doc_id: ""
review_type: "source_review"
status: "source_review_done"
tags:
  - "작업:원문대조"
---

# {{문서명}} — 원문대조 감수

## 1. Summary

| 항목 | 결과 | 비고 |
|---|---|---|
| 원문 누락 |  |  |
| 의미 추가 |  |  |
| 오역 후보 |  |  |
| 용어 불일치 |  |  |

## 2. 재검토 문단

| 문단 ID | 문제 유형 | 설명 | 제안 |
|---|---|---|---|
|  |  |  |  |
```

---

## 6.5 각주 및 해석 후보 파일

각주 및 해석 후보는 문서별로 필요할 때만 만든다. 문서 규모가 작으면 인간검수 파일 안에 함께 작성해도 된다.

경로:

```text
reviews/human-review/{문서ID}.human-review.md
```

템플릿 일부:

```markdown
## New Annotation Candidates

| 확인 | 문단 | 대상어 | 주석 후보 | 상태 | 비고 |
|---|---|---|---|---|---|
| [ ] |  |  |  | candidate |  |

## New Interpretation Candidates

| 확인 | 문단 | 주제 | 해석 후보 | 반영 방식 | 상태 | 비고 |
|---|---|---|---|---|---|---|
| [ ] |  |  |  | 각주/해설/미반영 | candidate |  |
```

---

## 6.6 2차 번역 파일

경로:

```text
translations/draft2/{문서ID}.draft2.md
```

템플릿:

```markdown
---
doc_id: ""
title_ko: ""
draft_stage: "draft2"
status: "draft2_done"
tags:
  - "작업:2차번역"
---

# {{문서명}} — 2차 번역

## 1. Translation Principle

- 직역 3 + 의역 7
- 자연스러운 한국어 독서문체
- 원문대조 감수 결과 반영
- 확정되지 않은 용어·각주·해석은 임의 확정하지 않음

---

## 2. Draft 2

### [001]
2차 번역을 입력한다.

### [002]
2차 번역을 입력한다.
```

---

## 6.7 인간검수 파일

경로:

```text
reviews/human-review/{문서ID}.human-review.md
```

템플릿:

```markdown
---
doc_id: ""
review_type: "human_review"
status: "human_review_done"
tags:
  - "작업:인간검수"
---

# {{문서명}} — 인간검수

## 1. 확정 신규 용어

| 완료 | 원문 | 원전언어 | 확정 번역어 | 누적 용어집 반영 | 비고 |
|---|---|---|---|---|---|
| [ ] |  |  |  | [ ] |  |

## 2. 확정 신규 각주

| 완료 | 대상어 | 처리 | 누적 각주집 반영 | 비고 |
|---|---|---|---|---|
| [ ] |  | 채택/보류/삭제 | [ ] |  |

## 3. 확정 신규 해석

| 완료 | 주제 | 처리 | 누적 해석집 반영 | 비고 |
|---|---|---|---|---|
| [ ] |  | 채택/보류/삭제 | [ ] |  |

## 4. 3차 번역 지시사항

- 
```

---

## 6.8 3차 번역 파일

경로:

```text
translations/draft3/{문서ID}.draft3.md
```

템플릿:

```markdown
---
doc_id: ""
title_ko: ""
draft_stage: "draft3"
status: "draft3_done"
tags:
  - "작업:3차번역"
---

# {{문서명}} — 3차 번역

## 1. Translation Principle

- 확정 신규 용어집 반영
- 확정 신규 각주 반영
- 확정 신규 해석 반영
- 2차 번역의 문체 유지
- 의미 재해석 금지

---

## 2. Draft 3

### [001]
3차 번역을 입력한다.

### [002]
3차 번역을 입력한다.
```

---

## 6.9 최종스캔 파일

경로:

```text
reviews/final-scan/{문서ID}.final-scan.md
```

템플릿:

```markdown
---
doc_id: ""
review_type: "final_scan"
status: "final_scan_done"
tags:
  - "작업:최종스캔"
---

# {{문서명}} — 최종스캔

| 항목 | 결과 | 비고 |
|---|---|---|
| 원문 누락 없음 | [ ] |  |
| 확정 용어 반영 | [ ] |  |
| 확정 각주 반영 | [ ] |  |
| 확정 해석 반영 | [ ] |  |
| 의미 이탈 없음 | [ ] |  |
| 문체 불균형 없음 | [ ] |  |
```

---

## 6.10 최종본 파일

경로:

```text
translations/final/{문서ID}.final.md
```

템플릿:

```markdown
---
doc_id: ""
title_ko: ""
draft_stage: "final"
status: "final_done"
tags:
  - "작업:최종본"
---

# {{문서명}}

최종 탈고본을 입력한다.
```

최종본 파일에는 가능한 한 독자가 읽을 본문만 둔다. 긴 검토 메모, 변경 과정, 후보표는 넣지 않는다.

---

# 7. AI 에이전트 역할

## 7.1 기초작업 에이전트

### 역할

```text
- 문서 ID 생성
- raw 원본 파일 보존
- normalized 원문 파일 작성
- 문단 ID 부여
- metadata 파일 작성
- master-checklist.md 갱신 제안
- prefix 태그 생성
```

### 입력

```text
원본 소스 파일
project-index.md
style-guide.md
```

### 출력

```text
sources/raw/{문서ID}.md
sources/normalized/{문서ID}.src.md
docs-meta/{문서ID}.meta.md
master-checklist.md 업데이트 제안
```

### 주의

기초작업 에이전트는 번역하지 않는다. 원문을 고치지 않는다. 원문과 참고 번역이 섞여 있으면 분리만 한다.

---

## 7.2 참고번역 분리 에이전트

### 역할

```text
- 원본 파일 안에 포함된 기존 번역문 식별
- 기존 번역문을 references/로 분리
- 원문과 참고번역의 문단 ID를 가능한 한 맞춤
```

### 입력

```text
sources/raw/{문서ID}.md
sources/normalized/{문서ID}.src.md
```

### 출력

```text
references/{문서ID}.korean-reference.md
metadata 파일의 참고 번역 경로 업데이트 제안
```

### 주의

참고 번역은 AI 번역 차수가 아니다. 참고 번역을 그대로 베끼지 않는다.

---

## 7.3 용어집 에이전트

### 역할

```text
- cumulative-glossary.md 확인
- 해당 문서의 신규 용어 후보 추출
- 1차 번역 파일 또는 별도 후보표에 New Glossary Candidates 작성
- 누적 용어집과 충돌하는 후보 표시
```

### 입력

```text
sources/normalized/{문서ID}.src.md
cumulative-glossary.md
style-guide.md
```

### 출력

```text
translations/draft1/{문서ID}.draft1.md의 New Glossary Candidates 영역
필요 시 workbench/{문서ID}.glossary-conflict.md
```

### 주의

용어집 에이전트는 용어를 확정하지 않는다. 후보만 제안한다.

---

## 7.4 1차 번역 에이전트

### 역할

```text
- 직역 7 + 의역 3 비율의 1차 번역 작성
- 원문 구조 보존
- 미확정 용어는 원어 병기 또는 후보 번역어 병기
```

### 입력

```text
sources/normalized/{문서ID}.src.md
cumulative-glossary.md
New Glossary Candidates
style-guide.md
```

### 출력

```text
translations/draft1/{문서ID}.draft1.md
```

### 주의

1차 번역은 아름다운 문체보다 원문 대응성을 우선한다.

---

## 7.5 원문대조 감수 에이전트

### 역할

```text
- 원문 누락 여부 점검
- 의미 추가 여부 점검
- 오역 후보 탐지
- 용어 불일치 탐지
- source-review 파일 작성
```

### 입력

```text
sources/normalized/{문서ID}.src.md
translations/draft1/{문서ID}.draft1.md
cumulative-glossary.md
references/{문서ID}.korean-reference.md가 있으면 참고
```

### 출력

```text
reviews/source-review/{문서ID}.source-review.md
```

상세 리포트는 문제가 있을 때만 `workbench/`에 만든다.

---

## 7.6 각주 및 해석 제안 에이전트

### 역할

```text
- cumulative-annotations.md 확인
- cumulative-interpretations.md 확인
- 해당 문서의 신규 각주 후보 작성
- 해당 문서의 신규 해석 후보 작성
- human-review 파일에 후보표 작성
```

### 입력

```text
sources/normalized/{문서ID}.src.md
translations/draft1/{문서ID}.draft1.md 또는 translations/draft2/{문서ID}.draft2.md
reviews/source-review/{문서ID}.source-review.md
cumulative-annotations.md
cumulative-interpretations.md
cumulative-glossary.md
style-guide.md
```

### 출력

```text
reviews/human-review/{문서ID}.human-review.md의 후보 영역
```

### 주의

이 에이전트는 본문을 직접 수정하지 않는다. 각주와 해석은 모두 후보로만 제시한다.

---

## 7.7 2차 번역 에이전트

### 역할

```text
- 직역 3 + 의역 7 비율의 2차 번역 작성
- 한국어 문체 정리
- 원문대조 감수 결과 반영
- 단, 확정되지 않은 용어·각주·해석은 임의 반영하지 않음
```

### 입력

```text
translations/draft1/{문서ID}.draft1.md
reviews/source-review/{문서ID}.source-review.md
cumulative-glossary.md
New Glossary Candidates
style-guide.md
```

### 출력

```text
translations/draft2/{문서ID}.draft2.md
```

---

## 7.8 인간 편집자

### 역할

```text
- 신규 용어 확정
- 신규 각주 채택·보류·삭제
- 신규 해석 채택·보류·삭제
- cumulative-glossary.md 갱신
- cumulative-annotations.md 갱신
- cumulative-interpretations.md 갱신
- editorial-decisions.md 갱신
- master-checklist.md 갱신
```

### 작업 위치

```text
reviews/human-review/{문서ID}.human-review.md
프로젝트 공통 누적 파일
master-checklist.md
editorial-decisions.md
```

### 원칙

사람이 확정하지 않은 후보는 3차 번역에 확정 자료로 반영하지 않는다.

---

## 7.9 3차 번역 에이전트

### 역할

```text
- 확정 신규 용어집 반영
- 확정 신규 각주 반영
- 확정 신규 해석 반영
- 2차 번역의 문체를 유지하며 3차 번역본 작성
```

### 입력

```text
translations/draft2/{문서ID}.draft2.md
reviews/human-review/{문서ID}.human-review.md
cumulative-glossary.md
cumulative-annotations.md
cumulative-interpretations.md
reviews/source-review/{문서ID}.source-review.md
style-guide.md
```

### 출력

```text
translations/draft3/{문서ID}.draft3.md
```

### 금지

```text
새 용어 임의 확정 금지
새 각주 임의 추가 금지
새 해석 임의 추가 금지
본문에 해석을 과도하게 삽입 금지
의미 재해석 금지
```

---

## 7.10 최종 원문대조 스캔 에이전트

### 역할

```text
- Draft 3 기준 최종 원문 누락 검사
- 확정 용어 반영 여부 검사
- 확정 각주 반영 여부 검사
- 확정 해석 반영 여부 검사
- 문체 편집 과정에서 의미가 이탈했는지 확인
```

### 입력

```text
sources/normalized/{문서ID}.src.md
translations/draft3/{문서ID}.draft3.md
reviews/human-review/{문서ID}.human-review.md
cumulative-glossary.md
cumulative-annotations.md
cumulative-interpretations.md
```

### 출력

```text
reviews/final-scan/{문서ID}.final-scan.md
```

상세 리포트는 문제가 있을 때만 별도로 만든다.

---

## 7.11 인간 최종 탈고

### 역할

```text
- Draft 3을 바탕으로 최종 원고 작성
- 문장 리듬 조정
- 주석 분량 조정
- 해석문 위치 조정
- 최종 문체 확정
- master-checklist.md에서 탈고 완료 표시
```

### 출력

```text
translations/final/{문서ID}.final.md
```

---

# 8. 작업 흐름

## 8.1 프로젝트 초기화

```text
1. project-index.md 작성
2. style-guide.md 작성
3. cumulative-glossary.md 생성
4. cumulative-annotations.md 생성
5. cumulative-interpretations.md 생성
6. editorial-decisions.md 생성
7. master-checklist.md 생성
8. docs-meta/ 폴더 생성
9. sources/raw/ 폴더 생성
10. sources/normalized/ 폴더 생성
11. references/ 폴더 생성
12. translations/draft1/ draft2/ draft3/ final/ 폴더 생성
13. reviews/source-review/ human-review/ final-scan/ 폴더 생성
14. workbench/ 폴더 생성 여부 결정
```

---

## 8.2 문서별 작업 흐름

```text
1. 기초작업 에이전트
   → raw 원본 보존
   → normalized 원문 생성
   → metadata 파일 생성
   → 문단 ID 부여
   → master-checklist 갱신

2. 참고번역 분리 에이전트
   → 기존 한글 번역 또는 참고 번역이 있으면 references/로 분리

3. 용어집 에이전트
   → 신규 용어 후보 작성

4. 1차 번역 에이전트
   → translations/draft1/{문서ID}.draft1.md 작성

5. 원문대조 감수 에이전트
   → reviews/source-review/{문서ID}.source-review.md 작성

6. 각주 및 해석 제안 에이전트
   → reviews/human-review/{문서ID}.human-review.md에 후보 작성

7. 2차 번역 에이전트
   → translations/draft2/{문서ID}.draft2.md 작성

8. 인간 편집자
   → 신규 용어·각주·해석 확정
   → 누적 용어집·각주집·해석집 갱신
   → editorial-decisions.md 갱신

9. 3차 번역 에이전트
   → translations/draft3/{문서ID}.draft3.md 작성

10. 최종 원문대조 스캔 에이전트
   → reviews/final-scan/{문서ID}.final-scan.md 작성

11. 인간 최종 탈고
   → translations/final/{문서ID}.final.md 작성
   → master-checklist에서 탈고 완료 표시
```

---

# 9. 산출물 생성 기준

## 9.1 항상 생성하는 것

```text
docs-meta/{문서ID}.meta.md
sources/raw/{문서ID}.md
sources/normalized/{문서ID}.src.md
translations/draft1/{문서ID}.draft1.md
master-checklist.md 갱신
```

## 9.2 단계 진행에 따라 생성하는 것

```text
references/{문서ID}.korean-reference.md
reviews/source-review/{문서ID}.source-review.md
reviews/human-review/{문서ID}.human-review.md
translations/draft2/{문서ID}.draft2.md
translations/draft3/{문서ID}.draft3.md
reviews/final-scan/{문서ID}.final-scan.md
translations/final/{문서ID}.final.md
```

## 9.3 확정 시 갱신하는 것

```text
cumulative-glossary.md
cumulative-annotations.md
cumulative-interpretations.md
editorial-decisions.md
```

## 9.4 필요할 때만 생성하는 것

```text
workbench/{문서ID}-source-review-detail.md
workbench/{문서ID}-translation-alternatives.md
workbench/{문서ID}-doctrinal-issue.md
workbench/{문서ID}-glossary-conflict.md
```

---

# 10. 문서 상태 관리 규칙

문서 상태는 `master-checklist.md`와 `docs-meta/{문서ID}.meta.md`에 함께 기록한다.

권장 상태값:

```text
not_started
raw_collected
source_ready
reference_ready
glossary_candidate_done
draft1_done
source_review_done
annotation_candidate_done
draft2_done
human_review_done
draft3_done
final_scan_done
final_done
hold
```

metadata 예시:

```yaml
---
doc_id: "gcb-094-39b-sakka-questions"
title_ko: "삭카의 질문"
status: "draft2_done"
tags:
  - "문헌:삭카빤하숫따(sakka-pañha-sutta)"
  - "상태:2차번역완료"
---
```

---

# 11. 대량 문서 운영 방식

## 11.1 100개 이상 문서의 경우

문서별 작업을 처음부터 끝까지 하나씩 완성하기보다, 묶음 단위로 진행하는 것이 좋다.

```text
Batch 01: T001–T020
Batch 02: T021–T040
Batch 03: T041–T060
```

작업 흐름:

```text
Batch 01 전체 raw 수집
→ Batch 01 전체 normalized 원문 작성
→ Batch 01 전체 참고번역 분리
→ Batch 01 전체 용어 후보 추출
→ Batch 01 전체 1차 번역
→ Batch 01 전체 원문대조
→ Batch 01 전체 인간 검수
```

장점:

```text
용어 일관성이 높아진다.
비슷한 문맥을 한꺼번에 처리할 수 있다.
반복되는 각주·해석을 누적하기 쉽다.
특정 차수의 파일만 열어 비교할 수 있다.
```

## 11.2 문서별 완결 방식이 적합한 경우

다음 경우에는 한 문서씩 완결하는 방식이 좋다.

```text
문서마다 주제가 매우 다를 때
길이가 긴 문서일 때
교학 쟁점이 많은 문서일 때
초기 테스트 단계일 때
```

## 11.3 긴 문서의 추가 분할

하나의 문서가 지나치게 길면 문서 내부를 장·절 단위로 다시 나눌 수 있다.

```text
gcb-094-39b-sakka-questions-01-introduction
gcb-094-39b-sakka-questions-02-pancasikha-songs
gcb-094-39b-sakka-questions-03-sakka-enters
```

단, 지나친 분할은 관리 부담을 늘린다. 원칙은 다음이다.

```text
AI가 한 번에 안정적으로 처리할 수 없는 길이면 나눈다.
사람이 한 번에 검수하기 어려우면 나눈다.
그러나 의미상 하나의 독립 단위가 아니면 억지로 나누지 않는다.
```

---

# 12. AI에게 주는 공통 지시문

모든 에이전트에게 공통으로 들어갈 기본 지시문은 다음과 같다.

```text
너는 불교문헌 번역 작업을 보조하는 AI 에이전트다.

원문을 임의로 수정하지 말라.
확정되지 않은 용어를 확정된 것처럼 쓰지 말라.
원문에 없는 해석을 본문에 삽입하지 말라.
불확실한 내용은 반드시 표시하라.
사람이 검토해야 할 항목은 체크리스트로 남겨라.
최종 판정은 인간 편집자가 한다.

이번 작업의 목표는 텍스트 번역과 원고 탈고이다.
entities, ontology, knowledge graph, triple 관계 추출은 수행하지 말라.
메타데이터 태그는 한글 중심 prefix 태그로만 작성하라.
빨리어·범어 로마나이즈는 태그와 메타데이터에서 소문자로 통일하라.
```

---

# 13. v0.3 최종 요약

v0.3 방식은 다음 한 문장으로 요약할 수 있다.

```text
원본·참고번역·1차·2차·3차·최종본을 목적별 폴더에 분리하고,
용어집·각주집·해석집은 프로젝트 단위로 누적하며,
전체 진행은 master-checklist와 문서별 metadata 파일로 관리한다.
```

이 구조의 장점은 다음과 같다.

```text
긴 문서에서도 파일 하나가 비대해지지 않는다.
사람과 AI가 특정 차수 파일만 열어 작업할 수 있다.
1차·2차·3차 번역을 비교하기 쉽다.
원본 파일이 오염되지 않는다.
KABC 기존 한글 번역처럼 참고 번역을 AI 번역 차수와 구분할 수 있다.
문서가 100개, 500개로 늘어나도 작업 단계를 추적할 수 있다.
번역과 탈고라는 본질에 집중할 수 있다.
```

최종 권장 구조는 다음이다.

```text
translation-project/
├─ project-index.md
├─ master-checklist.md
├─ style-guide.md
├─ editorial-decisions.md
├─ cumulative-glossary.md
├─ cumulative-annotations.md
├─ cumulative-interpretations.md
├─ docs-meta/
├─ sources/
│  ├─ raw/
│  └─ normalized/
├─ references/
├─ translations/
│  ├─ draft1/
│  ├─ draft2/
│  ├─ draft3/
│  └─ final/
├─ reviews/
│  ├─ source-review/
│  ├─ human-review/
│  └─ final-scan/
└─ workbench/
```

`workbench/`는 필요할 때만 둔다.

이것이 v0.3의 기본 매뉴얼이다.
