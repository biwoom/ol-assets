# OL DESK 개발기획안 v0.1

**문서명:** OL DESK 개발기획안
**버전:** v0.1
**기준일:** 2026-06-06
**프로젝트명:** AI에이전트 번역도량 — OL DESK
**관련 체계:** Paperclip 기반 불교문헌 번역 프로덕션
**핵심 목적:** 인간 감수자가 원문·번역 차수·용어·각주·태그를 검토·수정·확정하고, 그 결과를 Paperclip 3차 반영 에이전트에게 전달하는 로컬 검수 대시보드 개발

---

## 0. 한 줄 정의

**OL DESK는 Paperclip 번역도량에서 인간 감수자가 문단 단위로 원문, 1차 번역, 2차 번역, 3차 번역, 최종 원고, 용어, 각주, 태그를 검토·수정·확정하고, 그 결과를 `B2-3차반영-정반` 에이전트가 읽을 수 있는 구조화된 3차 반영 지시 파일로 저장하는 Astro 기반 로컬 편집 대시보드이다.**

---

## 1. 개발 배경

기존 `문헌 번역 AI 협업 워크플로우 매뉴얼 v0.3`은 대량 문헌 번역을 위해 원본, 정규화 원문, 참고 번역, 1차·2차·3차 번역, 최종본을 목적별 폴더에 분리하고, 용어집·각주집·해석집을 프로젝트 단위로 누적 관리하는 구조를 제안했다. 

또한 `Paperclip과 번역 프로젝트 튜토리얼 v0.3`은 단일 Translation PM 구조를 넘어, **2차 자동 생산 모드**와 **3차 확정 모드**를 분리하는 `Translation Director + A/B Manager` 구조를 제안했다. 이 구조에서 A라인은 많은 문서를 `draft2_done`까지 밀어 올리고, B라인은 인간이 확정한 판단만 3차 이후에 반영한다. 

그러나 실제 운영 단계에서는 다음 문제가 발생한다.

```text
1. Markdown 파일이 많아지면 인간 감수자가 전체 상태를 파악하기 어렵다.
2. Paperclip Issue 기록과 별도 Markdown 보고 파일이 중복될 수 있다.
3. 인간 감수자가 용어·각주·태그·번역문 수정 사항을 파일별로 직접 찾아 수정하기 어렵다.
4. 2차 번역을 보고 3차 반영용 수정 지시를 문단 단위로 만들 수 있는 전용 UI가 필요하다.
5. 3차 반영 에이전트가 읽을 수 있는 구조화된 지시 파일이 필요하다.
```

따라서 OL DESK는 기존 워크플로우를 대체하는 것이 아니라, **기존 Paperclip 번역 프로덕션의 인간 감수·확정 계층**으로 추가된다.

---

## 2. 기본 구도

```text
Paperclip Server
= AI 에이전트 조직 운영
= Issue 기반 작업 배정
= A라인 1차·2차 생산
= B라인 3차 반영 및 최종스캔

OL DESK SERVER
= 인간 감수자용 로컬 웹 대시보드
= 문서 리스트와 진행상태 표시
= 원문·번역 차수 비교
= 용어·각주·태그 검토 및 수정
= 3차 반영 지시 파일 생성

Translation Project Data
= JSON 원장
= Markdown 최종 산출
= Git 이력 추적
```

OL DESK는 Paperclip을 대체하지 않는다. Paperclip은 계속 **에이전트 실행·작업 배정·Issue 기록**을 담당한다. OL DESK는 **인간 감수자 판단과 수정 데이터의 입력·저장·전달**을 담당한다.

---

## 3. OL DESK의 핵심 원칙

### 3.1 Paperclip과 역할 분리

```text
Paperclip
- AI 에이전트 실행
- Issue 생성과 작업 로그 관리
- A라인 생산 관리
- B라인 반영 작업 실행

OL DESK
- 인간 감수자 UI
- 문서 상태 확인
- 문단 단위 번역 비교
- 용어·각주·태그 수정 및 확정
- 3차 반영 지시 파일 생성
```

### 3.2 직접 수정하되 원본을 덮어쓰지 않는다

OL DESK에서 인간 감수자는 신규 용어, 각주, 태그, 2차 번역 수정안, 3차 번역 재수정안, 최종 원고 후보를 직접 수정할 수 있다.

그러나 이 수정은 원본 파일이나 2차 번역 파일을 즉시 덮어쓰는 방식이 아니다.

```text
원문 / 1차 / 2차 / 3차 / 최종 원고
= 원본 산출물 또는 차수별 산출물

OL DESK 수정 정보
= 별도 decision layer
= 3차 반영 지시 파일
= human revision data
```

즉, OL DESK의 수정은 **원본 변경**이 아니라 **인간 감수자의 확정·수정 지시 데이터 작성**이다.

### 3.3 JSON 원장 + Markdown 산출

운영 데이터는 JSON을 기본 원장으로 삼는다.

```text
AI가 읽고 쓰는 자료: JSON
OL DESK가 표시하는 자료: JSON → UI 렌더링
인간이 최종 보존하는 자료: final.md, review-summary.md, editorial-decisions.md
Git으로 추적하는 자료: JSON + final Markdown
```

기존 매뉴얼은 `master-checklist.md`, `cumulative-glossary.md`, `cumulative-annotations.md`, `cumulative-interpretations.md`, `docs-meta`, 차수별 번역본, 리뷰 파일을 보존 산출물로 제안했다. 
OL DESK 도입 이후에는 이 구조를 유지하되, 내부 운영 원장은 JSON으로 전환하고 Markdown은 최종 산출 또는 보고 산출로 제한한다.

---

## 4. 개발 목표

## 4.1 v0.1의 목표

OL DESK v0.1의 목표는 완전 자동화가 아니다. 첫 번째 목표는 다음이다.

```text
인간 감수자가 하나의 브라우저 화면에서
문서 진행상태를 확인하고,
원문·1차·2차 번역을 비교하고,
세그먼트별 3차 반영용 수정안을 작성하고,
신규 용어·각주·태그를 수정·확정한 뒤,
B2-3차반영 에이전트에게 넘길 JSON 지시 파일을 생성한다.
```

## 4.2 v0.1에서 하지 않는 것

```text
1. Paperclip API 완전 연동
2. 실시간 양방향 동기화
3. 다중 사용자 권한 관리
4. 복잡한 GitHub diff 완전 재현
5. Entity / ontology / triple 자동 추출
6. OL BOOK / ATLAS 출판 자동화
7. 클라우드 서버 운영
```

---

## 5. 사용자 시나리오

### 5.1 기본 시나리오

```text
1. Paperclip A라인 에이전트들이 원문 정리, 1차 번역, 원문대조, 2차 번역, 용어·각주·태그 후보를 생성한다.
2. OL DESK가 이 산출물을 읽어 문서 리스트에 표시한다.
3. 인간 감수자가 문서 리스트에서 하나의 원본문서를 클릭한다.
4. 화면에 원문, 1차 번역, 2차 번역, 3차 번역, 최종 원고 영역이 표시된다.
5. 인간 감수자는 1차·2차 번역을 비교하면서 세그먼트별 3차 반영용 수정안을 작성한다.
6. 신규 용어, 신규 각주, 신규 태그를 확인하고 채택 / 보류 / 폐기 처리한다.
7. 필요한 경우 용어 번역어, 각주 텍스트, 태그명을 직접 수정한다.
8. 검수가 끝나면 “3차 반영 지시 파일 생성” 버튼을 누른다.
9. OL DESK는 `handoff/draft3/{doc_id}.draft3-instructions.json` 파일을 생성한다.
10. Paperclip의 B라인, 특히 `B2-3차반영-정반` 에이전트가 이 파일을 읽고 3차 번역을 생성한다.
```

---

## 6. 화면 구성

## 6.1 전체 레이아웃

```text
┌─────────────────────────────────────────────────────────────┐
│ 상단 바: 프로젝트명 / 현재 문서 / 저장 상태 / 3차 반영 요청 │
├───────────────┬───────────────────────────────┬─────────────┤
│ 문서 리스트    │ 원문·번역 비교 영역             │ 검토 패널    │
│ 진행상태       │ 세그먼트별 편집                 │ 용어/각주/태그│
│ 필터/검색      │ diff 보기                       │ 확정/보류/폐기│
└───────────────┴───────────────────────────────┴─────────────┘
```

---

## 6.2 문서 리스트 화면

첫 화면은 원본문서 리스트와 진행상태판이다.

### 표시 컬럼

```text
doc_id
문서명
원문 언어
현재 상태
1차 번역 상태
2차 번역 상태
인간검수 상태
3차 반영 상태
최종스캔 상태
최종 원고 상태
미확정 용어 수
미확정 각주 수
미확정 태그 수
마지막 수정일
다음 작업
```

### 상태값

```text
not_started              시작 전
source_ready             원문 준비
draft1_done              1차 완료
source_review_done       원문대조 완료
draft2_done              2차 완료
human_review_in_progress 인간검수 중
human_review_done        인간검수 완료
draft3_requested         3차 반영 요청
draft3_done              3차 완료
final_scan_done          최종스캔 완료
final_done               최종 완료
hold                     보류
error                    오류
```

---

## 6.3 문서 상세 화면

문서 리스트에서 특정 문서를 클릭하면 다음 영역이 열린다.

```text
1. 문서 메타정보
2. 원문 영역
3. 1차 번역문 영역
4. 2차 번역문 영역
5. 3차 번역문 영역
6. 최종 원고 영역
7. 검토된 용어 영역
8. 검토된 각주 영역
9. 검토된 태그 영역
```

---

## 7. 영역별 기능

## 7.1 원문 영역

```text
기본 성격: 읽기 전용
예외 기능: 원문 정정 제안 작성
```

원문 자체를 직접 덮어쓰지 않는다. OCR 오류, 문단 분할 오류, 줄바꿈 오류 등은 “원문 정정 제안”으로 기록한다.

예시:

```json
{
  "segment_id": "004-003",
  "correction_type": "ocr_fix",
  "original_text": "...",
  "proposed_source_text": "...",
  "reason": "OCR 오류 수정",
  "status": "approved_by_human"
}
```

---

## 7.2 1차 번역문 영역

```text
기본 성격: 비교·참조용
v0.1 수정 기능: 검토 메모 작성
```

1차 번역은 직역 중심의 기준 자료이므로 v0.1에서는 직접 수정 기능을 제한한다. 필요한 경우 세그먼트별 메모만 남긴다.

---

## 7.3 2차 번역문 영역

```text
핵심 기능: 3차 반영용 인간 수정안 작성
```

인간 감수자는 2차 번역을 보고 각 세그먼트별로 3차 반영용 수정 문장을 작성한다.

예시:

```json
{
  "segment_id": "004-003",
  "draft2_text": "기존 2차 번역문",
  "human_revision_for_draft3": "인간 감수자가 수정한 3차 반영용 문장",
  "revision_note": "용어를 '서원'에서 '발원'으로 수정",
  "status": "approved"
}
```

---

## 7.4 3차 번역문 영역

```text
기본 성격: B2 에이전트 생성 결과 확인
기능: post-draft3 재수정 지시 작성
```

B2 에이전트가 생성한 3차 번역을 OL DESK에서 다시 확인할 수 있다. 필요한 경우 인간 감수자는 재수정 지시를 작성한다.

예시:

```json
{
  "segment_id": "004-003",
  "draft3_text": "B2 에이전트가 생성한 3차 번역",
  "human_post_draft3_revision": "인간이 다시 고친 문장",
  "status": "needs_reintegration"
}
```

---

## 7.5 최종 원고 영역

```text
기본 성격: 최종 탈고 후보 확인 및 수정
주의: B2 에이전트 반영용이 아니라 인간 최종 산출용
```

최종 원고 영역은 3차 반영용 수정안과 분리한다.

```text
3차 반영용 수정안
= B2 에이전트에게 전달

최종 원고 수정
= 인간 최종 탈고 산출물
```

---

## 7.6 용어 영역

### 기능

```text
신규 용어 후보 보기
번역어 수정
대안 번역어 수정
사용 원칙 작성
상태 선택
누적 용어집 반영 여부 표시
```

### 상태값

```text
candidate      후보
approved       채택
held           보류
rejected       폐기
conflict       기존 용어와 충돌
needs_source   출처 확인 필요
```

### 예시 데이터

```json
{
  "term_id": "term-gcb-004-001",
  "source_term": "dukkha",
  "source_language": "pali",
  "suggested_translation": "괴로움",
  "human_translation": "괴로움",
  "alternatives": ["고통", "불만족"],
  "usage_note": "사성제 문맥에서는 기본적으로 괴로움으로 번역",
  "status": "approved",
  "apply_to_cumulative_glossary": true
}
```

---

## 7.7 각주 영역

### 기능

```text
각주 후보 보기
각주 본문 수정
각주 위치 확인
처리 선택: 채택 / 보류 / 폐기
각주 유형 선택
누적 각주집 반영 여부 표시
```

### 각주 유형

```text
용어 설명
출전 설명
교학 설명
번역 주석
문헌 비교
기타
```

### 예시 데이터

```json
{
  "annotation_id": "anno-gcb-004-002",
  "segment_id": "004-002",
  "target_text": "도솔천",
  "candidate_note": "도솔천은 욕계 육천 가운데 하나이다.",
  "human_note": "도솔천은 욕계 육천 가운데 하나로, 보살이 인간계에 태어나기 전 머무는 하늘로 설명된다.",
  "annotation_type": "용어 설명",
  "status": "approved",
  "apply_to_cumulative_annotations": true
}
```

---

## 7.8 태그 영역

태그는 검색·필터·작업 보조용으로만 사용한다. 기존 매뉴얼에서도 태그는 문서 검색 보조, 작업 묶음 구분, 주요 인물·장소·문헌·교리 확인, 상태 확인을 위한 표시용으로 제한되어 있으며, 태그만으로 관계 구조를 만들지 않는다고 규정되어 있다. 

### v0.1 prefix

```text
문헌:
인물:
장소:
교리:
사건:
전통:
```

### 기능

```text
태그 후보 보기
태그 추가
태그 수정
태그 삭제
상태 선택: 채택 / 보류 / 폐기
누적 태그집 반영 여부 표시
```

### 예시 데이터

```json
{
  "tag_id": "tag-gcb-004-001",
  "segment_id": "004-001",
  "tag": "인물:붓다",
  "status": "approved"
}
```

### 금지

```text
태그만으로 관계를 추론하지 않는다.
Entity를 자동 생성하지 않는다.
triple을 자동 생성하지 않는다.
ontology 구조화를 수행하지 않는다.
```

---

## 8. 데이터 구조

## 8.1 권장 폴더 구조

```text
ol-translation-lab/
├─ paperclip/
│  ├─ initial-task.md
│  └─ agents/
│
├─ desk/
│  ├─ config.json
│  └─ ui-state.json
│
├─ data/
│  ├─ documents.json
│  ├─ segments/
│  │  └─ {doc_id}.segments.json
│  ├─ drafts/
│  │  └─ {doc_id}.drafts.json
│  ├─ reviews/
│  │  └─ {doc_id}.review.json
│  ├─ glossary/
│  │  └─ glossary.json
│  ├─ annotations/
│  │  └─ annotations.json
│  ├─ tags/
│  │  └─ tags.json
│  └─ events/
│     └─ {doc_id}.events.jsonl
│
├─ handoff/
│  └─ draft3/
│     └─ {doc_id}.draft3-instructions.json
│
├─ markdown/
│  ├─ final/
│  │  └─ {doc_id}.final.md
│  └─ reports/
│     └─ {doc_id}.review-summary.md
│
└─ sources/
   ├─ raw/
   └─ normalized/
```

---

## 8.2 `documents.json`

문서 리스트와 진행상태를 관리한다.

```json
[
  {
    "doc_id": "gcb-src-004",
    "title": "Salutation and Intention",
    "source_language": "english",
    "status": "draft2_done",
    "draft1_status": "done",
    "draft2_status": "done",
    "human_review_status": "pending",
    "draft3_status": "not_started",
    "final_status": "not_started",
    "pending_terms": 5,
    "pending_annotations": 2,
    "pending_tags": 4,
    "updated_at": "2026-06-06"
  }
]
```

---

## 8.3 `segments/{doc_id}.segments.json`

원문 세그먼트를 관리한다.

```json
[
  {
    "doc_id": "gcb-src-004",
    "segment_id": "004-001",
    "source_text": "...",
    "source_note": "",
    "order": 1
  }
]
```

---

## 8.4 `drafts/{doc_id}.drafts.json`

차수별 번역문을 관리한다.

```json
[
  {
    "segment_id": "004-001",
    "draft1": "...",
    "draft2": "...",
    "draft3": "",
    "final": ""
  }
]
```

---

## 8.5 `reviews/{doc_id}.review.json`

OL DESK에서 인간 감수자가 작성하는 검토 데이터를 저장한다.

```json
{
  "doc_id": "gcb-src-004",
  "review_status": "in_progress",
  "segment_revisions": [
    {
      "segment_id": "004-001",
      "human_revision_for_draft3": "",
      "revision_note": "",
      "status": "pending"
    }
  ],
  "term_reviews": [],
  "annotation_reviews": [],
  "tag_reviews": [],
  "source_corrections": [],
  "updated_at": "2026-06-06"
}
```

---

## 8.6 `handoff/draft3/{doc_id}.draft3-instructions.json`

B2-3차반영 에이전트에게 전달할 핵심 파일이다.

```json
{
  "doc_id": "gcb-src-004",
  "title": "Salutation and Intention",
  "created_by": "OL DESK",
  "reviewer": "human_editor",
  "status": "ready_for_draft3",
  "source_file": "sources/normalized/gcb-src-004.src.md",
  "draft1_file": "translations/draft1/gcb-src-004.draft1.md",
  "draft2_file": "translations/draft2/gcb-src-004.draft2.md",
  "instructions": {
    "principle": "인간 감수자가 approved 처리한 수정만 반영한다. held/rejected 항목은 반영하지 않는다.",
    "do_not": [
      "새 용어를 임의 확정하지 말 것",
      "새 각주를 임의 추가하지 말 것",
      "원문에 없는 해석을 본문에 삽입하지 말 것"
    ]
  },
  "segment_revisions": [
    {
      "segment_id": "004-001",
      "draft2_text": "...",
      "human_revision_for_draft3": "...",
      "status": "approved",
      "note": "문체 수정 및 용어 통일"
    }
  ],
  "approved_terms": [],
  "approved_annotations": [],
  "approved_tags": [],
  "held_items": [],
  "rejected_items": []
}
```

---

## 9. 에이전트 조직 재편

현재 `OL-Desk Agent Name.md` 문서는 CEO/총괄 디렉터, A라인 생산 모드, B라인 확정 모드의 명칭을 정리하고 있으며, A2·B1·B4는 다른 에이전트와 통합 검토 대상으로 명시되어 있다. 

OL DESK 도입 후 권장 조직은 다음과 같다.

## 9.1 유지

```text
CEO-총괄디렉터-법장
A-관리매니저-선행
A1-기초정리-정안
A3-용어후보-명해
A4-1차번역-초역
A5-대조감수-조견
A6-각주-해의
A7-2차번역-윤문
B-확정매니저-결정
B2-3차반영-정반
B3-최종스캔-무루
```

## 9.2 조건부 유지

```text
A2-참고번역분리-분명
```

참고 번역이 원문에 섞여 있는 경우에만 별도 실행한다. 일반 문서에서는 A1-기초정리-정안의 하위 기능으로 통합할 수 있다.

## 9.3 OL DESK로 흡수

```text
B1-인간검수-청문
B4-최종인계-회향
```

B1의 “인간검수 준비” 기능은 OL DESK UI가 담당한다.
B4의 “최종인계” 기능은 독립 에이전트보다 보고 템플릿 또는 최종 상태 변경 기능으로 전환한다.

## 9.4 신설

```text
A1.5-태그후보-표지
```

역할:

```text
문서 또는 세그먼트 단위로 3~6개 prefix 태그 후보를 제안한다.
태그는 검색·필터·검수 보조용으로만 사용한다.
관계 추론, Entity 생성, triple 생성은 하지 않는다.
```

---

## 10. OL DESK v0.1 기능 범위

## 10.1 필수 기능

```text
1. 로컬 JSON 데이터 읽기
2. 문서 리스트 표시
3. 문서별 진행상태 표시
4. 문서 클릭 시 상세 화면 표시
5. 원문·1차·2차 번역 병렬 표시
6. 세그먼트별 3차 반영용 수정안 작성
7. 신규 용어 후보 수정·채택·보류·폐기
8. 신규 각주 후보 수정·채택·보류·폐기
9. 태그 후보 수정·채택·보류·폐기
10. review.json 저장
11. draft3-instructions.json 생성
```

## 10.2 권장 기능

```text
1. draft1 ↔ draft2 간단 diff 표시
2. 미확정 용어/각주/태그 수 표시
3. 저장 전 변경사항 경고
4. 최근 수정일 자동 갱신
5. 상태 필터: draft2_done / 검수중 / 3차요청 / 완료
6. 검색: doc_id, 제목, 태그, 용어
```

## 10.3 후순위 기능

```text
1. Paperclip API 직접 호출
2. Git commit 자동 생성
3. GitHub Issue 자동 댓글
4. 최종 Markdown 자동 편집기
5. 복잡한 diff 병합 UI
6. 멀티 검수자 기능
```

---

## 11. 기술 스택

## 11.1 기본 스택

```text
Framework: Astro
UI: OL HOME 디자인 토큰 계승
Runtime: 로컬 개발 서버
Data: JSON file
Version Control: Git
Agent Orchestration: Paperclip
```

OL HOME은 이미 Astro 기반 정적 사이트이며, 콘텐츠 컬렉션과 GitHub Pages 배포 구조를 갖춘 포털로 정리되어 있다. 
OL DESK는 OL HOME의 공개 포털 성격과 분리하되, 디자인 철학과 스타일 코드는 계승한다.

## 11.2 저장소 분리 권장

```text
ol-home
= 공개 포털

ol-desk
= 로컬 번역 검수 대시보드

translation-lab
= 실제 번역 프로젝트 데이터

paperclip
= AI 에이전트 오케스트레이션 서버
```

---

## 12. 디자인 원칙

OL DESK는 OL HOME의 디자인 철학을 계승한다.

기존 OL 브랜드 정의서는 OL을 불교 경전과 논서를 디지털 환경에 최적화된 인터랙티브 웹북으로 재구축하는 불교 콘텐츠 스튜디오로 정의하고, 디자인에서는 최소주의, 유기성, 개방성을 강조한다. 

OL DESK도 다음 원칙을 따른다.

```text
1. 무채색 기반
2. 충분한 여백
3. 강한 장식 배제
4. 긴 문헌을 읽기 좋은 행간과 폭
5. 버튼보다 텍스트의 위계 우선
6. 검수자의 피로를 줄이는 조용한 UI
7. 진행률 과시보다 상태 명료성 우선
```

---

## 13. 개발 단계

## Phase 0 — 데이터 샘플 준비

```text
목표:
- 하나의 테스트 문서에 대해 source, draft1, draft2, terms, annotations, tags JSON 샘플 준비

산출:
- documents.json
- segments/{doc_id}.segments.json
- drafts/{doc_id}.drafts.json
- reviews/{doc_id}.review.json
```

---

## Phase 1 — 문서 리스트와 상세 화면

```text
목표:
- 문서 리스트 표시
- 문서 클릭 시 상세 화면 표시
- 원문·1차·2차 번역 병렬 표시

산출:
- /desk 문서 목록 화면
- /desk/{doc_id} 문서 상세 화면
```

---

## Phase 2 — 인간 수정 입력

```text
목표:
- 세그먼트별 3차 반영용 수정안 작성
- 용어·각주·태그 상태 변경
- 수정 내용 review.json 저장

산출:
- segment revision editor
- term review panel
- annotation review panel
- tag review panel
```

---

## Phase 3 — 3차 반영 지시 파일 생성

```text
목표:
- 검수 완료 버튼
- approved 항목만 추출
- draft3-instructions.json 생성

산출:
- handoff/draft3/{doc_id}.draft3-instructions.json
```

---

## Phase 4 — Paperclip B라인 수동 연동

```text
목표:
- B-확정매니저-결정 또는 B2-3차반영-정반에게 전달할 task 문서 생성
- Paperclip Issue에 붙여넣기 가능한 요약 생성

산출:
- paperclip-task/{doc_id}.draft3-task.md
```

---

## Phase 5 — 후속 확장

```text
목표:
- Paperclip API / Issue 연동
- Git commit 자동화
- final.md export
- 대량 문서 batch review
```

---

## 14. 성공 기준

OL DESK v0.1의 성공 기준은 다음이다.

```text
1. 하나의 문서를 OL DESK에서 열 수 있다.
2. 원문·1차·2차 번역을 세그먼트별로 비교할 수 있다.
3. 인간 감수자가 2차 번역을 보고 3차 반영용 수정안을 작성할 수 있다.
4. 용어 후보를 수정하고 채택/보류/폐기할 수 있다.
5. 각주 후보를 수정하고 채택/보류/폐기할 수 있다.
6. 태그 후보를 수정하고 채택/보류/폐기할 수 있다.
7. 검수 결과가 review.json에 저장된다.
8. B2 에이전트가 읽을 수 있는 draft3-instructions.json이 생성된다.
9. 생성된 지시 파일만 보고도 B2 에이전트가 3차 번역을 수행할 수 있다.
```

---

## 15. v0.1 최종 결론

OL DESK v0.1은 “번역 대시보드”가 아니라 **인간 감수자가 3차 번역 반영을 위한 확정 데이터를 작성하는 검수·편집 인터페이스**이다.

기존 Paperclip v0.3 구조는 유지한다. 다만 B라인의 인간검수 준비 기능과 최종인계 기능은 OL DESK로 흡수하고, Paperclip은 AI 에이전트 실행과 3차 반영 작업에 집중한다.

최종 구조는 다음과 같다.

```text
A라인 Paperclip
원문 정리 → 1차 번역 → 원문대조 → 2차 번역 → 후보 생성

OL DESK
문서 리스트 → 원문/번역 비교 → 인간 수정 → 용어/각주/태그 확정 → 3차 반영 지시 파일 생성

B라인 Paperclip
3차 반영 → 최종스캔 → final 준비

인간 편집자
최종 탈고 → final.md 확정
```

이 기획안의 핵심 문장은 다음과 같다.

> **OL DESK는 Paperclip 번역도량의 인간 감수석이며, AI가 생산한 2차 번역을 인간의 교학적·문체적 판단으로 검토하여 3차 반영 가능한 구조화 지시로 전환하는 로컬 대시보드이다.**
