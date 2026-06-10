# OL DESK 개발기획안 v0.2

**문서명:** OL DESK 개발기획안
**버전:** v0.1-revised
**기준일:** 2026-06-06
**프로젝트명:** AI에이전트 번역도량 — OL DESK
**관련 체계:** Paperclip 기반 불교문헌 번역 프로덕션
**핵심 목적:** 인간 감수자가 1·2차 에이전트 번역안과 후보 용어·각주·태그를 검토하고, **3차 가번역 섹션**과 **4차 최종원고 섹션**에서 직접 수정·신규 생성·확정 작업을 수행하며, 그 결과를 Paperclip 에이전트가 반영할 수 있는 구조화 데이터로 저장하는 Astro 기반 로컬 검수 대시보드 개발

---

## 0. 한 줄 정의

**OL DESK는 Paperclip 번역도량에서 인간 감수자가 원문과 1·2차 에이전트 번역안을 참고하면서, 3차 가번역 섹션에서 3차 반영용 수정·신규 용어·신규 각주·신규 태그를 작성하고, 이후 3차 생산물이 확정되면 4차 최종원고 섹션에서 최종 탈고를 수행하는 로컬 편집 대시보드이다.**

---

## 1. 개발 배경

기존 `문헌 번역 AI 협업 워크플로우 매뉴얼 v0.3`은 문서별 통합 원고 1파일 방식을 기본값으로 삼지 않고, 원본·정규화 원문·참고 번역·1차·2차·3차·최종본을 목적별 폴더로 분리하며, 용어집·각주집·해석집은 프로젝트 단위로 누적 관리하는 구조를 제안했다. 

또한 `Paperclip과 번역 프로젝트 튜토리얼 v0.3`은 단일 PM 구조가 아니라, 2차 생산을 담당하는 A라인과 3차 확정을 담당하는 B라인을 분리하는 구조를 제안했다. 이 구조에서 A매니저는 많은 문서를 2차까지 올리고, B매니저는 사람이 확정한 판단만 3차 이후에 반영한다. 

OL DESK는 이 구조를 계승하되, 인간 감수자의 실제 작업 공간을 더 명확히 만든다.

기존 구상에서 모호했던 부분은 다음과 같다.

```text
1. 인간 감수자가 실제로 어느 번역 차수를 수정하는가?
2. 1·2차 에이전트 산출물은 수정 대상인가, 참조 대상인가?
3. 3차 번역은 에이전트가 바로 생산하는가, 인간 감수자의 가번역 작업 공간을 거치는가?
4. 최종 원고는 3차 번역과 같은 영역인가, 별도 4차 영역인가?
5. 신규 용어·각주·태그를 인간 감수자가 직접 생성할 수 있는가?
```

이번 수정본은 이 질문에 대해 다음과 같이 확정한다.

```text
1. 1차·2차 에이전트 번역안은 보기 전용이다.
2. 인간 감수자의 직접 수정 영역은 3차 가번역 섹션이다.
3. 3차 가번역 섹션의 초기값은 에이전트가 만든 2차 번역문과 동일하다.
4. 인간 감수자는 3차 가번역 섹션에서 번역문을 직접 수정한다.
5. 인간 감수자는 신규 용어·신규 각주·신규 태그를 직접 생성할 수 있다.
6. 기존 에이전트가 생산한 용어·각주·태그 후보를 확정·보류·폐기할 수 있다.
7. 3차 반영 에이전트가 이를 반영해 3차 생산물을 만들면 3차 가번역 섹션은 잠금 처리된다.
8. 이후 4차 최종원고 영역이 생성되고, 인간 감수자는 이 영역에서 최종 탈고를 수행한다.
```

---

## 2. 전체 시스템 구도

프로젝트 폴더에는 세 가지 층위가 존재한다.

```text
1. OL DESK 코드층
   - Astro 기반 ol-desk 애플리케이션 코드
   - GitHub으로 관리

2. 번역 데이터층
   - ol-translation-lab/
   - 원문, 번역 차수, 용어, 각주, 태그, 검수 데이터 저장

3. Paperclip 에이전트 지침층
   - paperclip/
   - 에이전트별 지침문서군
   - AGENTS.md, HEARTBEAT.md, SOUL.md, TOOLS.md
```

전체 관계는 다음과 같다.

```text
프로젝트 루트/
├─ ol-desk/                 ← Astro 코드, GitHub 관리
├─ ol-translation-lab/      ← 번역 데이터 폴더
└─ paperclip/               ← 에이전트별 초기 지침문서군
```

Paperclip 튜토리얼은 기존에 `batch-plans/`, `batch-reports/`, `queues/`, `manager-logs/`를 추가한 번역 프로젝트 폴더 구조를 제안했다. 
OL DESK 수정본에서는 이 구조를 `ol-translation-lab/` 내부로 수용한다.

---

## 3. OL DESK의 역할

OL DESK는 Paperclip을 대체하지 않는다.

```text
Paperclip
= 에이전트 채용
= 작업 지시
= Issue 기반 로그
= A라인 1·2차 생산
= B라인 3차 반영 및 최종스캔

OL DESK
= 인간 감수자 UI
= 문서 진행상태 확인
= 원문·1차·2차·3차·4차 비교
= 3차 가번역 직접 수정
= 신규 용어·각주·태그 생성
= 기존 후보 확정·보류·폐기
= 4차 최종원고 직접 수정
```

Paperclip 기존 기획에서는 AI 에이전트가 초안 작성, 후보 제안, 누락 검사, 문체 편집 보조, Batch 진행 관리, 확정 반영 점검을 담당하고, 최종 용어·각주·해석·최종 원고 탈고는 인간 편집자가 담당한다고 규정했다. 
OL DESK는 바로 이 인간 편집자 영역을 실제 작업 화면으로 구현한다.

---

## 4. 번역 차수 모델 수정

기존 v0.1에서는 `1차 → 2차 → 3차 → final` 구조를 중심으로 보았다. 수정본에서는 인간 감수자의 실제 작업 흐름을 반영하여 다음과 같이 재정의한다.

```text
원문
↓
1차 에이전트 번역안
↓
2차 에이전트 번역안
↓
3차 가번역 섹션
  - 초기값: 2차 번역문과 동일
  - 인간 감수자가 직접 수정
  - 신규 용어·각주·태그 생성 가능
  - 기존 후보 확정 가능
↓
3차 생산물
  - B2-3차반영-정반 에이전트가 생성
  - 생성 완료 후 3차 가번역 섹션 잠금
↓
4차 최종원고 영역
  - 인간 감수자가 직접 수정
  - 최종 탈고용
↓
final.md
```

---

## 5. 인간 감수자의 수정 권한

## 5.1 보기 전용 영역

다음은 인간 감수자가 볼 수 있지만 직접 수정하지 않는다.

```text
원문
1차 에이전트 번역문
2차 에이전트 번역문
에이전트 생성 용어 후보 원본
에이전트 생성 각주 후보 원본
에이전트 생성 태그 후보 원본
```

이 영역은 비교와 판단의 기준 자료이다.

---

## 5.2 직접 수정 영역 1 — 3차 가번역 섹션

3차 가번역 섹션은 인간 감수자의 핵심 작업 공간이다.

```text
초기값:
- 2차 번역문과 동일한 텍스트

수정 가능:
- 세그먼트별 번역문 직접 수정
- 신규 용어 추가
- 신규 각주 추가
- 신규 태그 추가
- 기존 용어 후보 확정
- 기존 각주 후보 확정
- 기존 태그 후보 확정
- 보류 / 폐기 처리
```

3차 가번역 섹션은 “3차 생산물”이 아니다. 이는 **3차 반영 에이전트에게 넘길 인간 감수 원고**이다.

---

## 5.3 직접 수정 영역 2 — 4차 최종원고 영역

B2-3차반영-정반 에이전트가 3차 생산물을 생성하면, 3차 가번역 섹션은 완료 상태가 된다.

```text
3차 가번역 섹션 상태 변화:
editing
→ ready_for_draft3
→ draft3_generated
→ locked
```

이후 3차 생산물을 바탕으로 4차 최종원고 영역이 생성된다.

```text
4차 최종원고 영역:
- 인간 감수자가 직접 수정
- 최종 문체 조정
- 최종 탈고
- final.md 생성의 기준
```

---

## 6. 신규 생성 기능

인간 감수자는 OL DESK에서 다음 항목을 새로 생성할 수 있어야 한다.

```text
1. 신규 번역 용어
2. 신규 각주
3. 신규 태그
4. 세그먼트별 3차 가번역 수정문
5. 4차 최종원고 수정문
```

### 6.1 신규 용어 생성

```json
{
  "term_id": "human-term-gcb-004-001",
  "created_by": "human",
  "segment_id": "004-001",
  "source_term": "dukkha",
  "source_language": "pali",
  "human_translation": "괴로움",
  "alternatives": ["고통", "불만족"],
  "usage_note": "사성제 문맥에서는 기본적으로 괴로움으로 번역",
  "status": "approved",
  "apply_to_cumulative_glossary": true
}
```

### 6.2 신규 각주 생성

```json
{
  "annotation_id": "human-anno-gcb-004-002",
  "created_by": "human",
  "segment_id": "004-002",
  "target_text": "도솔천",
  "human_note": "도솔천은 욕계 육천 가운데 하나로, 보살이 인간계에 태어나기 전 머무는 하늘로 설명된다.",
  "annotation_type": "용어 설명",
  "status": "approved",
  "apply_to_cumulative_annotations": true
}
```

### 6.3 신규 태그 생성

```json
{
  "tag_id": "human-tag-gcb-004-001",
  "created_by": "human",
  "segment_id": "004-001",
  "tag": "인물:붓다",
  "status": "approved"
}
```

---

## 7. 기존 후보 확정 기능

에이전트가 생성한 용어·각주·태그 후보는 인간 감수자가 다음 상태 중 하나로 처리한다.

```text
candidate      후보
approved       채택
held           보류
rejected       폐기
conflict       기존 항목과 충돌
needs_source   출처 확인 필요
```

인간 감수자는 후보를 그대로 승인할 수도 있고, 텍스트를 수정한 뒤 승인할 수도 있다.

중요한 점은 “에이전트 후보 원본”과 “인간 수정·확정본”을 분리하는 것이다.

```text
agent_candidate_text
= 에이전트가 제안한 원문

human_edited_text
= 인간 감수자가 수정한 최종 검수 텍스트
```

---

## 8. 레이아웃 설계

## 8.1 전체 레이아웃

```text
┌──────────────────────────────────────────────────────────────┐
│ 상단 바: 프로젝트명 / 현재 문서 / 저장 상태 / 3차 반영 요청 │
├──────────────┬─────────────────────────────────┬─────────────┤
│ 문서 리스트   │ 원문·번역 비교 및 편집 영역       │ 검토 패널    │
│ 진행상태      │ 탭 + 병렬 비교 + 세그먼트 편집    │ 용어/각주/태그│
└──────────────┴─────────────────────────────────┴─────────────┘
```

---

## 8.2 상단 탭 구조

원문·번역 비교 영역의 기본 구조는 탭이다.

```text
[1차 번역] [2차 번역] [3차 번역] [4차 번역]
```

기본값은 다음과 같다.

```text
기본 선택 탭: 3차 번역
기본 표시: 3차 가번역 1단 표시
```

---

## 8.3 병렬 보기 구조

감수자는 체크박스를 통해 2단 또는 3단 병렬 보기로 전환할 수 있다.

```text
비교 선택:
[ ] 원문
[ ] 1차 번역
[ ] 2차 번역
[x] 3차 가번역
[ ] 4차 최종원고
```

예시 1 — 기본값:

```text
┌─────────────────────┐
│ 3차 가번역           │
│ 직접 수정 가능       │
└─────────────────────┘
```

예시 2 — 2단 병렬:

```text
┌─────────────────────┬─────────────────────┐
│ 2차 번역 보기 전용   │ 3차 가번역 수정 가능 │
└─────────────────────┴─────────────────────┘
```

예시 3 — 3단 병렬:

```text
┌─────────────────────┬─────────────────────┬─────────────────────┐
│ 원문 보기 전용       │ 2차 번역 보기 전용   │ 3차 가번역 수정 가능 │
└─────────────────────┴─────────────────────┴─────────────────────┘
```

예시 4 — 최종 탈고 단계:

```text
┌─────────────────────┬─────────────────────┐
│ 3차 생산물 보기 전용 │ 4차 최종원고 수정 가능│
└─────────────────────┴─────────────────────┘
```

---

## 8.4 섹션 잠금 규칙

```text
1차 번역:
- 항상 보기 전용

2차 번역:
- 항상 보기 전용

3차 가번역:
- draft3_generated 이전까지 수정 가능
- draft3_generated 이후 수정 버튼 숨김
- locked 상태로 표시

3차 생산물:
- 보기 전용
- 필요 시 “4차 최종원고로 가져오기” 버튼 제공

4차 최종원고:
- final_done 이전까지 수정 가능
- final_done 이후 잠금 가능
```

---

## 9. 데이터 구조 수정

## 9.1 프로젝트 전체 폴더 구조

```text
ol-desk-project/
├─ ol-desk/
│  ├─ package.json
│  ├─ astro.config.mjs
│  ├─ src/
│  └─ README.md
│
├─ ol-translation-lab/
│  ├─ data/
│  ├─ sources/
│  ├─ translations/
│  ├─ reviews/
│  ├─ handoff/
│  ├─ markdown/
│  ├─ queues/
│  ├─ batch-plans/
│  ├─ batch-reports/
│  └─ manager-logs/
│
└─ paperclip/
   ├─ company/
   │  └─ initial-task.md
   └─ agents/
      ├─ CEO-총괄디렉터-법장/
      │  ├─ AGENTS.md
      │  ├─ HEARTBEAT.md
      │  ├─ SOUL.md
      │  └─ TOOLS.md
      ├─ A-관리매니저-선행/
      │  ├─ AGENTS.md
      │  ├─ HEARTBEAT.md
      │  ├─ SOUL.md
      │  └─ TOOLS.md
      ├─ A1-기초정리-정안/
      ├─ A2-참고번역분리-분명/
      ├─ A3-용어후보-명해/
      ├─ A4-1차번역-초역/
      ├─ A5-대조감수-조견/
      ├─ A6-각주-해의/
      ├─ A7-2차번역-윤문/
      ├─ B-확정매니저-결정/
      ├─ B2-3차반영-정반/
      └─ B3-최종스캔-무루/
```

기존 에이전트 명칭 문서는 CEO, A라인, B라인의 한국어 명칭과 법명을 정리하고 있다. 
수정본에서는 이 명칭을 `paperclip/agents/` 폴더명으로 그대로 사용한다.

---

## 9.2 `drafts/{doc_id}.drafts.json`

```json
[
  {
    "segment_id": "004-001",
    "source_text": "...",
    "draft1_agent_text": "...",
    "draft2_agent_text": "...",
    "draft3_preliminary_text": "...",
    "draft3_generated_text": "",
    "draft4_final_working_text": "",
    "final_text": "",
    "draft3_preliminary_status": "editing",
    "draft4_status": "not_started"
  }
]
```

여기서 핵심은 다음이다.

```text
draft1_agent_text
= 보기 전용

draft2_agent_text
= 보기 전용

draft3_preliminary_text
= 인간 감수자 직접 수정 영역
= 초기값은 draft2_agent_text와 동일

draft3_generated_text
= B2 에이전트가 생성한 3차 생산물
= 보기 전용

draft4_final_working_text
= 인간 감수자 최종 원고 작업 영역
```

---

## 9.3 `reviews/{doc_id}.review.json`

```json
{
  "doc_id": "gcb-src-004",
  "review_status": "in_progress",
  "active_stage": "draft3_preliminary",
  "segment_reviews": [
    {
      "segment_id": "004-001",
      "draft3_preliminary_text": "...",
      "revision_note": "",
      "status": "editing"
    }
  ],
  "term_reviews": [],
  "annotation_reviews": [],
  "tag_reviews": [],
  "human_created_terms": [],
  "human_created_annotations": [],
  "human_created_tags": [],
  "updated_at": "2026-06-06"
}
```

---

## 9.4 `handoff/draft3/{doc_id}.draft3-instructions.json`

B2-3차반영-정반 에이전트에게 전달할 핵심 파일이다.

```json
{
  "doc_id": "gcb-src-004",
  "title": "Salutation and Intention",
  "created_by": "OL DESK",
  "reviewer": "human_editor",
  "status": "ready_for_draft3",
  "instructions": {
    "principle": "3차 가번역 섹션의 인간 수정문과 approved 처리된 용어·각주·태그만 반영한다.",
    "do_not": [
      "1차·2차 에이전트 번역문을 임의 수정하지 말 것",
      "held/rejected 항목을 반영하지 말 것",
      "새 용어를 임의 확정하지 말 것",
      "원문에 없는 해석을 본문에 삽입하지 말 것"
    ]
  },
  "segment_revisions": [
    {
      "segment_id": "004-001",
      "source_text": "...",
      "draft2_agent_text": "...",
      "draft3_preliminary_text": "...",
      "status": "approved_for_draft3",
      "note": "인간 감수자가 3차 가번역 섹션에서 수정한 문장"
    }
  ],
  "approved_terms": [],
  "approved_annotations": [],
  "approved_tags": [],
  "human_created_terms": [],
  "human_created_annotations": [],
  "human_created_tags": []
}
```

---

## 9.5 `handoff/final/{doc_id}.final-instructions.json`

4차 최종원고 작업을 별도로 관리하기 위해 추가한다.

```json
{
  "doc_id": "gcb-src-004",
  "created_by": "OL DESK",
  "status": "ready_for_final_export",
  "base_text": "draft3_generated_text",
  "final_working_segments": [
    {
      "segment_id": "004-001",
      "draft3_generated_text": "...",
      "draft4_final_working_text": "...",
      "status": "approved_for_final"
    }
  ]
}
```

---

## 10. Paperclip 에이전트 지침문서 초기 세팅

## 10.1 GitHub 관리 원칙

에이전트용 지침과 기본 디렉토리 구조 세팅은 GitHub으로 관리한다.

```text
관리 대상:
- ol-desk 코드
- ol-translation-lab 기본 폴더 템플릿
- paperclip 에이전트별 지침문서
- 초기 task 문서
- 공통 규칙 문서
```

## 10.2 `paperclip/agents/` 구조

각 에이전트 폴더에는 다음 네 문서가 들어간다.

```text
AGENTS.md
HEARTBEAT.md
SOUL.md
TOOLS.md
```

### AGENTS.md

```text
역할, 책임 범위, 입력 파일, 출력 파일, 금지 사항, 상태값 규칙을 기록한다.
```

### HEARTBEAT.md

```text
에이전트가 작업 중 주기적으로 확인해야 할 운영 리듬을 기록한다.
예: 작업 시작 전 확인, 산출물 생성 후 확인, 오류 발생 시 보고 방식.
```

### SOUL.md

```text
에이전트의 작업 철학과 판단 기준을 기록한다.
예: 원문 보존, 인간 확정 우선, 무리한 해석 금지, 불확실성 표시.
```

### TOOLS.md

```text
에이전트가 사용할 수 있는 도구, 명령어, 파일 접근 범위, 금지된 작업을 기록한다.
```

기존 매뉴얼은 모든 에이전트에게 “원문을 임의로 수정하지 말라, 확정되지 않은 용어를 확정된 것처럼 쓰지 말라, 최종 판정은 인간 편집자가 한다”는 공통 지시를 제시한다. 
이 공통 지시는 각 에이전트의 `SOUL.md`와 `AGENTS.md`에 반복 포함한다.

---

## 11. 에이전트 조직

기존 조직은 유지하되, OL DESK 도입에 맞게 일부 역할을 조정한다.

## 11.1 유지

```text
CEO-총괄디렉터-법장
A-관리매니저-선행
A1-기초정리-정안
A2-참고번역분리-분명
A3-용어후보-명해
A4-1차번역-초역
A5-대조감수-조견
A6-각주-해의
A7-2차번역-윤문
B-확정매니저-결정
B2-3차반영-정반
B3-최종스캔-무루
```

## 11.2 기능 조정

```text
B1-인간검수-청문
= OL DESK UI 기능으로 흡수 가능
= 단, 초기에는 검수 요약 생성 보조 에이전트로 유지 가능

B4-최종인계-회향
= 4차 최종원고 export와 final.md 생성 단계로 기능 전환
```

## 11.3 신설 후보

```text
A1.5-태그후보-표지
= 태그 후보 생성 전담
= 관계 추론, Entity 생성, triple 생성 금지
```

---

## 12. 개발 단계 수정본

사용자 구상에 맞추어 개발 단계를 다음처럼 재정리한다.

---

## 12.1 1단계 — 프로젝트 폴더 설정과 Paperclip 설치

목표:

```text
프로젝트 루트 폴더를 만들고,
그 안에 ol-desk, ol-translation-lab, paperclip 세 층위를 준비한다.
Paperclip을 터미널로 설치·실행하고,
에이전트 팀 채용까지 완료한다.
```

실행 흐름:

```bash
mkdir -p ~/Projects/ol-desk-project
cd ~/Projects/ol-desk-project

mkdir -p ol-desk
mkdir -p ol-translation-lab
mkdir -p paperclip/agents

npx paperclipai onboard --yes
```

기존 튜토리얼도 Paperclip 설치를 위해 `npx paperclipai onboard --yes` 명령을 사용하고, 기본 접속 주소를 `http://localhost:3100`으로 안내한다. 

이 단계 산출물:

```text
Paperclip 서버 실행
Paperclip Company 생성
에이전트 팀 채용
paperclip/agents/ 하위 지침문서 배치
ol-translation-lab/ 기본 데이터 폴더 생성
```

---

## 12.2 2단계 — Astro 설치와 OL DESK 구현 시작

목표:

```text
ol-desk/ 폴더에 Astro 프로젝트를 설치하고,
OL DESK UI 개발을 시작한다.
```

실행 흐름:

```bash
cd ~/Projects/ol-desk-project/ol-desk
npm create astro@latest .
npm install
npm run dev
```

구현 우선순위:

```text
1. 문서 리스트 화면
2. 문서 상세 화면
3. 탭 구조
4. 3차 가번역 편집 영역
5. 용어·각주·태그 검토 패널
```

---

## 12.3 3단계 — OL DESK 프로토타입 완성 후 1차 번역 워크플로우 실행

목표:

```text
Paperclip 에이전트를 가동하여 실제 산출물을 ol-translation-lab/에 생성하고,
Astro 개발 서버가 이 폴더의 JSON/Markdown 산출물을 읽어 OL DESK 대시보드에 반영한다.
```

실행 흐름:

```text
1. Paperclip A라인 가동
2. A4-1차번역-초역 실행
3. A7-2차번역-윤문 실행
4. A3/A6/A1.5 후보 생성
5. 산출물 ol-translation-lab/에 저장
6. OL DESK 개발 서버가 산출물 감지
7. 문서 리스트와 상세 화면에 반영
```

v0.1 프로토타입의 완료 기준:

```text
1. 1개 문서가 문서 리스트에 표시된다.
2. 문서를 클릭하면 원문·1차·2차 번역이 표시된다.
3. 3차 가번역 섹션이 2차 번역과 동일한 초기값으로 생성된다.
4. 인간 감수자가 3차 가번역을 수정할 수 있다.
5. 신규 용어·각주·태그를 추가할 수 있다.
6. 기존 후보를 확정·보류·폐기할 수 있다.
7. draft3-instructions.json이 생성된다.
```

---

## 12.4 4단계 — 실제 번역 반복과 OL DESK·Paperclip 지침 동시 개선

목표:

```text
원문을 계속 번역하면서,
OL DESK 코드와 Paperclip 에이전트 지침을 반복적으로 수정한다.
```

반복 사이클:

```text
1. 새 원문 추가
2. Paperclip A라인 번역 실행
3. OL DESK에서 인간 감수
4. draft3-instructions.json 생성
5. Paperclip B2가 3차 생산물 생성
6. OL DESK에서 4차 최종원고 편집
7. 문제 발견 시:
   - OL DESK 코드 수정
   - 에이전트 AGENTS.md 수정
   - HEARTBEAT.md 운영 리듬 수정
   - SOUL.md 판단 기준 수정
   - TOOLS.md 도구 권한 수정
8. 다시 테스트
```

이 단계에서 OL DESK는 완성품이라기보다 **번역 프로덕션과 함께 성장하는 로컬 편집 도구**로 운영한다.

---

## 13. v0.1 필수 기능 수정본

```text
1. 문서 리스트 표시
2. 문서별 진행상태 표시
3. 원문·1차·2차·3차·4차 탭 구조
4. 기본값: 3차 번역 탭, 3차 가번역 1단 표시
5. 체크 선택에 따른 2단·3단 병렬 보기
6. 1차·2차 번역 보기 전용
7. 3차 가번역 직접 수정
8. 신규 용어 생성
9. 신규 각주 생성
10. 신규 태그 생성
11. 기존 용어 후보 확정·보류·폐기
12. 기존 각주 후보 확정·보류·폐기
13. 기존 태그 후보 확정·보류·폐기
14. draft3-instructions.json 생성
15. 3차 생산물 생성 후 3차 가번역 잠금
16. 4차 최종원고 영역 생성
17. 4차 최종원고 직접 수정
18. final.md export 준비
```

---

## 14. 성공 기준 수정본

OL DESK v0.1-revised의 성공 기준은 다음이다.

```text
1. Paperclip 설치와 에이전트 팀 세팅이 프로젝트 루트에서 가능하다.
2. paperclip/agents/ 아래 에이전트별 AGENTS.md, HEARTBEAT.md, SOUL.md, TOOLS.md가 존재한다.
3. Astro 기반 ol-desk 개발 서버가 실행된다.
4. ol-translation-lab/의 산출물을 OL DESK가 읽는다.
5. 문서 리스트에서 원문별 진행상태를 볼 수 있다.
6. 문서 상세 화면에서 1차·2차 에이전트 번역안을 볼 수 있다.
7. 3차 가번역 섹션이 2차 번역문과 동일한 초기값으로 생성된다.
8. 인간 감수자가 3차 가번역 섹션에서 번역문을 직접 수정할 수 있다.
9. 인간 감수자가 신규 용어·각주·태그를 직접 생성할 수 있다.
10. 기존 에이전트 후보를 확정·보류·폐기할 수 있다.
11. 3차 반영 지시 파일을 생성할 수 있다.
12. B2-3차반영-정반 에이전트가 이 지시 파일을 읽고 3차 생산물을 생성할 수 있다.
13. 3차 생산물 생성 후 3차 가번역 섹션은 잠긴다.
14. 4차 최종원고 영역이 생성된다.
15. 인간 감수자가 4차 최종원고 영역에서 최종 탈고를 수행할 수 있다.
```

---

## 15. 핵심 결론

수정된 OL DESK v0.1의 핵심은 다음이다.

> **OL DESK는 1·2차 에이전트 번역안을 수정하는 도구가 아니다. 1·2차 번역안은 인간 감수자가 판단하기 위한 참조 자료이다. 인간 감수자의 실제 편집 공간은 3차 가번역 섹션과 4차 최종원고 섹션이다.**

전체 흐름은 다음과 같이 확정한다.

```text
Paperclip A라인
원문 정리 → 1차 번역 → 2차 번역 → 용어·각주·태그 후보 생성

OL DESK
1·2차 보기 → 3차 가번역 직접 수정 → 신규 용어·각주·태그 생성 → 후보 확정

Paperclip B라인
3차 가번역 지시 반영 → 3차 생산물 생성 → 최종스캔

OL DESK
3차 생산물 확인 → 4차 최종원고 생성 → 인간 최종 탈고

최종 산출
final.md
```

이 구조는 기존 v0.3의 “속도는 A매니저, 품질 통제는 B매니저, 최종 판단은 인간 편집자”라는 원칙을 유지하면서, 인간 감수자의 실제 편집 행위를 OL DESK 안에 명확히 배치하는 방식이다. 
