# 02_Contents-Asset_데이터구조기획

## OL-DESK-CREW 데이터 저장 구조와 파일 규칙

**문서명:** Contents-Asset 데이터구조기획  
**버전:** v0.2  
**작성일:** 2026-06-06  
**문서 성격:** OL-DESK-CREW의 Markdown/JSON 저장 구조와 파일 규칙 정의  
**상위 문서:** `00_OL-CREW_전체기획.md`  
**관련 문서:** `01_OL-DESK_개발기획.md`, `03_AI-Agent_운영기획.md`, `04_번역워크플로우_운영매뉴얼.md`  

---

# 1. 한 줄 정의

**Contents-Asset은 OL-DESK-CREW에서 원문, 번역 원고, 수정정보, 후보 데이터, 감수자 메모, 에이전트 로그, handoff 지시, Markdown 내보내기 산출물을 저장하는 단일 데이터 소스이다.**

OL-DESK는 Contents-Asset을 읽고 쓴다. Paperclip API나 특정 에이전트 서비스의 내부 기록에 직접 의존하지 않는다.

---

# 2. 핵심 저장 원칙

```text
1. 사람이 직접 읽는 원고는 Markdown으로 저장한다.
2. 수정정보, 상태, 후보, 로그, 감수자 메모, handoff 데이터는 JSON으로 저장한다.
3. 1차·2차·3차·4차 번역본은 Markdown으로 저장한다.
4. 용어·각주·태그는 프로젝트별 JSON으로 저장한다.
5. shared에는 공통 지침과 템플릿만 둔다.
6. 프로젝트별 용어·각주·태그·해석 판단은 shared에 두지 않는다.
7. 에이전트는 각 단계 완료 시 표준 agent-log JSON을 남긴다.
8. 개별 번역본과 전체 번역본 내보내기 산출물은 Markdown으로 생성한다.
```

---

# 3. 전체 구조

OL-DESK-CREW의 Contents-Asset 구조는 `00_OL-CREW_전체기획.md`의 공통 구조를 번역 프로젝트에 맞게 구체화한 것이다.

```text
contents-asset/
├─ projects/
│  └─ {project_id}/
│     ├─ assets/
│     │  ├─ source/
│     │  │  ├─ raw/
│     │  │  └─ normalized/
│     │  └─ references/
│     │
│     ├─ outputs/
│     │  ├─ manuscripts/
│     │  │  ├─ draft1/
│     │  │  ├─ draft2/
│     │  │  ├─ draft3/
│     │  │  └─ draft4/
│     │  └─ exports/
│     │     ├─ individual/
│     │     └─ all/
│     │
│     ├─ data/
│     │  ├─ documents.json
│     │  ├─ segments/
│     │  ├─ status/
│     │  ├─ terms/
│     │  ├─ annotations/
│     │  ├─ tags/
│     │  ├─ revisions/
│     │  ├─ notes/
│     │  └─ agent-evaluations/
│     │
│     ├─ handoff/
│     │  ├─ draft3/
│     │  └─ revision/
│     │
│     ├─ logs/
│     │  └─ agent-logs/
│     │
│     └─ archive/
│
└─ shared/
   ├─ principles/
   ├─ rules/
   ├─ templates/
   └─ agent-guides/
```

---

# 4. 폴더별 책임

## 4.1 assets/

`assets/`는 번역 작업의 입력 자산을 보관한다.

```text
assets/source/raw/
= 원본 보존 폴더

assets/source/normalized/
= 번역 작업용 정리 원문

assets/references/
= 참고번역 또는 참고자료
```

원본은 임의로 수정하지 않는다. 정리본은 문단 ID, 줄바꿈, OCR 오류 수정, 참고번역 분리 등 작업 편의를 위한 정리만 허용한다.

## 4.2 outputs/

`outputs/`는 사람이 읽을 수 있는 번역 산출물을 보관한다.

```text
outputs/manuscripts/draft1/
= 1차 번역본. 보기 전용.

outputs/manuscripts/draft2/
= 2차 번역본. 보기 전용.

outputs/manuscripts/draft3/
= 3차 번역본. B라인 생성본.

outputs/manuscripts/draft4/
= 4차 최종원고. 인간 최종 탈고본.

outputs/exports/individual/
= 개별 문서 단위 Markdown 내보내기 산출물.

outputs/exports/all/
= 프로젝트 전체 번역본 일괄 Markdown 내보내기 산출물.
```

## 4.3 data/

`data/`는 OL-DESK가 읽고 쓰는 구조화 데이터 폴더이다.

```text
documents.json
= 프로젝트 문헌 목록과 기본 metadata

segments/
= 문서별 세그먼트 정보

status/
= 문서별 현재 상태

terms/
= 프로젝트별 용어 후보와 확정 용어

annotations/
= 프로젝트별 각주 후보와 확정 각주

tags/
= 프로젝트별 태그 후보와 확정 태그

revisions/
= revision cycle과 인간 수정정보

notes/
= 인간 감수자의 교정·검수 메타데이터 메모

agent-evaluations/
= 인간 감수자의 에이전트 활동 평가
```

## 4.4 handoff/

`handoff/`는 Human UX에서 AI-Agent로 넘기는 지시 데이터를 저장한다.

```text
handoff/draft3/
= 3차 반영 지시 JSON

handoff/revision/
= 완료본 수정 후 새 revision cycle 지시 JSON
```

## 4.5 logs/

`logs/`는 에이전트 작업 완료 로그를 저장한다.

```text
logs/agent-logs/{doc_id}/
= 문서별 에이전트 완료 로그
```

이 로그는 Paperclip API를 대체하는 OL-CREW 표준 진행 기록이다.

## 4.6 shared/

`shared/`에는 프로젝트별 판단 데이터를 두지 않는다.

```text
shared/principles/
= 공통 창작 원칙

shared/rules/
= 공통 편집 규칙

shared/templates/
= 공통 파일·JSON 템플릿

shared/agent-guides/
= 공통 에이전트 운영 지침
```

---

# 5. 파일명 규칙

## 5.1 문서 ID

문서 ID는 프로젝트 안에서 고유해야 한다.

예:

```text
gcb-src-007-the-renunciaton-of-sumedha
kabc-k0802-t060
t001-test
```

## 5.2 Markdown 파일명

Markdown 파일은 같은 문서 ID를 유지하고, 단계 정보는 폴더가 담당한다.

```text
assets/source/raw/{doc_id}.md
assets/source/normalized/{doc_id}.md
assets/references/{doc_id}.md
outputs/manuscripts/draft1/{doc_id}.md
outputs/manuscripts/draft2/{doc_id}.md
outputs/manuscripts/draft3/{doc_id}.md
outputs/manuscripts/draft4/{doc_id}.md
outputs/exports/individual/{doc_id}-{stage}.md
outputs/exports/all/{project_id}-{stage}-all.md
```

파일명에 `draft1`, `draft2`, `final` 같은 단계명을 반복하지 않는다.

## 5.3 JSON 파일명

문서별 JSON은 `{doc_id}.json`을 기본으로 한다.

```text
data/segments/{doc_id}.json
data/status/{doc_id}.json
data/revisions/{doc_id}.json
data/notes/{doc_id}.json
```

에이전트 로그는 시간과 단계가 드러나게 작성한다.

```text
logs/agent-logs/{doc_id}/2026-06-06_A07_draft2_done.json
```

---

# 6. documents.json

`data/documents.json`은 프로젝트 문헌 목록의 기준 파일이다.

```json
{
  "project_id": "buddhavamsa",
  "project_title": "Buddhavamsa Translation Project",
  "updated_at": "2026-06-06T00:00:00+09:00",
  "documents": [
    {
      "doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
      "title": "The Renunciaton of Sumedha",
      "source_language": "english",
      "current_status": "source_ready",
      "source_path": "assets/source/raw/gcb-src-007-the-renunciaton-of-sumedha.md",
      "normalized_path": "assets/source/normalized/gcb-src-007-the-renunciaton-of-sumedha.md",
      "has_reference": false,
      "tags": [],
      "notes": ""
    }
  ]
}
```

---

# 7. segments JSON

`data/segments/{doc_id}.json`은 원문과 번역본을 세그먼트 단위로 연결하기 위한 파일이다.

```json
{
  "doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
  "updated_at": "2026-06-06T00:00:00+09:00",
  "segments": [
    {
      "segment_id": "001",
      "source_start": "",
      "source_end": "",
      "notes": ""
    }
  ]
}
```

번역문 자체는 JSON에 중복 저장하지 않는다. 번역문은 Markdown에 저장하고, 세그먼트 JSON은 연결과 표시를 돕는다.

---

# 8. status JSON

`data/status/{doc_id}.json`은 문서의 현재 워크플로우 상태를 저장한다.

```json
{
  "doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
  "current_status": "source_ready",
  "display_status": "원본준비",
  "current_owner": "A00-2차 생산 관리 매니저-선행",
  "next_action": "원문정리",
  "blocked": false,
  "blocker_reason": "",
  "updated_at": "2026-06-06T00:00:00+09:00"
}
```

상태 전환 규칙은 `04_번역워크플로우_운영매뉴얼.md`에서 정의한다.

---

# 9. terms JSON

용어 데이터는 프로젝트별로 관리한다.

권장 파일:

```text
data/terms/terms.json
```

구조:

```json
{
  "project_id": "buddhavamsa",
  "updated_at": "2026-06-06T00:00:00+09:00",
  "terms": [
    {
      "term_id": "term-gcb-007-001",
      "source_term": "dukkha",
      "source_language": "pali",
      "translation": "괴로움",
      "alternatives": ["고통", "불만족"],
      "status": "approved",
      "created_by": "human",
      "first_doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
      "usage_note": "사성제 문맥에서는 기본적으로 괴로움으로 번역",
      "updated_at": "2026-06-06T00:00:00+09:00"
    }
  ]
}
```

상태값:

```text
candidate
approved
hold
rejected
deprecated
```

---

# 10. annotations JSON

각주 데이터는 프로젝트별로 관리한다.

권장 파일:

```text
data/annotations/annotations.json
```

구조:

```json
{
  "project_id": "buddhavamsa",
  "updated_at": "2026-06-06T00:00:00+09:00",
  "annotations": [
    {
      "annotation_id": "anno-gcb-007-001",
      "target_text": "도솔천",
      "annotation_text": "도솔천은 욕계 육천 가운데 하나로 설명된다.",
      "annotation_type": "용어 설명",
      "status": "approved",
      "created_by": "human",
      "first_doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
      "updated_at": "2026-06-06T00:00:00+09:00"
    }
  ]
}
```

---

# 11. tags JSON

태그 데이터는 프로젝트별로 관리한다.

권장 파일:

```text
data/tags/tags.json
```

구조:

```json
{
  "project_id": "buddhavamsa",
  "updated_at": "2026-06-06T00:00:00+09:00",
  "tags": [
    {
      "tag_id": "tag-gcb-007-001",
      "tag": "인물:붓다",
      "status": "approved",
      "created_by": "human",
      "scope": "document",
      "doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
      "segment_id": "001",
      "updated_at": "2026-06-06T00:00:00+09:00"
    }
  ]
}
```

태그는 검색과 분류를 위한 표시 데이터이다. 태그만으로 관계 구조나 온톨로지를 만들지 않는다.

---

# 12. revisions JSON

`data/revisions/{doc_id}.json`은 인간 수정과 revision cycle을 저장한다.

```json
{
  "doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
  "current_revision": "rev-001",
  "revisions": [
    {
      "revision_id": "rev-001",
      "base_stage": "draft2",
      "target_stage": "draft3",
      "status": "human_editing",
      "created_by": "human",
      "created_at": "2026-06-06T00:00:00+09:00",
      "modified_segments": [
        {
          "segment_id": "001",
          "base_text_path": "outputs/manuscripts/draft2/gcb-src-007-the-renunciaton-of-sumedha.md",
          "human_text": "",
          "change_note": ""
        }
      ]
    }
  ]
}
```

---

# 13. handoff JSON

`handoff/draft3/{doc_id}.json`은 B라인 에이전트에게 넘기는 3차 반영 지시이다.

```json
{
  "handoff_id": "handoff-draft3-gcb-007-rev-001",
  "project_id": "buddhavamsa",
  "doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
  "revision_id": "rev-001",
  "target_stage": "draft3",
  "human_modified_segments": [],
  "approved_terms": [],
  "approved_annotations": [],
  "approved_tags": [],
  "rejected_candidates": [],
  "pending_items": [],
  "instruction_summary": "인간 확정 판단만 반영할 것.",
  "created_at": "2026-06-06T00:00:00+09:00"
}
```

handoff는 인간 판단의 전달 문서이다. handoff에 없는 후보를 B라인이 임의로 확정 반영하지 않는다.

---

# 14. agent-log JSON

에이전트는 각 단계 완료 시 표준 로그를 남긴다.

위치:

```text
logs/agent-logs/{doc_id}/{date}_{agent_id}_{stage}.json
```

구조:

```json
{
  "log_id": "2026-06-06_A07_draft2_done",
  "project_id": "buddhavamsa",
  "doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
  "agent_id": "A07",
  "agent_name": "A07-2차 번역 에이전트-윤문",
  "stage": "draft2_done",
  "input_files": [],
  "output_files": [],
  "summary": "",
  "issues": [],
  "requires_human_review": true,
  "next_recommended_action": "human_review",
  "created_at": "2026-06-06T00:00:00+09:00"
}
```

OL-DESK는 이 로그를 읽어 문서 진행, 에이전트 활동, 평가 대상을 표시한다.

---

# 15. agent-evaluations JSON

인간 감수자는 에이전트 활동을 평가할 수 있다.

권장 위치:

```text
data/agent-evaluations/{agent_id}.json
```

구조:

```json
{
  "agent_id": "A07",
  "agent_name": "A07-2차 번역 에이전트-윤문",
  "evaluations": [
    {
      "evaluation_id": "eval-A07-2026-06-06-001",
      "doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
      "stage": "draft2_done",
      "accuracy": 4,
      "instruction_following": 5,
      "usefulness": 4,
      "issues": [],
      "improvement_note": "",
      "created_by": "human",
      "created_at": "2026-06-06T00:00:00+09:00"
    }
  ]
}
```

---

# 16. notes JSON

`data/notes/{doc_id}.json`은 인간 감수자가 OL-DESK에서 남긴 교정·검수 메모를 저장한다.

감수자 메모는 본문 해석 메모가 아니며, 본문·용어·각주·태그에 자동 반영되지 않는다. UX에서는 GitHub 댓글처럼 본문만 빠르게 입력하고, OL-DESK가 문맥 정보를 자동 연결한다.

권장 위치:

```text
data/notes/{doc_id}.json
```

구조:

```json
{
  "doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
  "updated_at": "2026-06-06T00:00:00+09:00",
  "notes": [
    {
      "note_id": "note-gcb-007-001",
      "body": "이 단락은 4차에서 문체를 다시 확인할 것.",
      "context": {
        "page": "translation",
        "tab": "draft3",
        "stage": "human_editing",
        "segment_id": "001",
        "target_type": "manuscript",
        "target_id": "outputs/manuscripts/draft3/gcb-src-007-the-renunciaton-of-sumedha.md"
      },
      "status": "open",
      "created_by": "human",
      "created_at": "2026-06-06T00:00:00+09:00",
      "updated_at": "2026-06-06T00:00:00+09:00"
    }
  ]
}
```

상태값:

```text
open
resolved
archived
```

handoff에는 기본적으로 메모를 포함하지 않는다. 특정 메모를 AI-Agent가 참고해야 할 때만 인간 감수자가 명시적으로 선택해 handoff의 `included_notes`에 연결한다.

---

# 17. Markdown 내보내기 산출물

Markdown 내보내기는 OL-DESK 화면에서 확인한 번역본을 사람이 읽기 쉬운 형태로 묶어내는 기능이다.

위치:

```text
outputs/exports/individual/
outputs/exports/all/
```

개별 문서 내보내기:

```text
outputs/exports/individual/{doc_id}-draft1.md
outputs/exports/individual/{doc_id}-draft2.md
outputs/exports/individual/{doc_id}-draft3.md
outputs/exports/individual/{doc_id}-draft4.md
```

전체 문서 일괄 내보내기:

```text
outputs/exports/all/{project_id}-draft1-all.md
outputs/exports/all/{project_id}-draft2-all.md
outputs/exports/all/{project_id}-draft3-all.md
outputs/exports/all/{project_id}-draft4-all.md
```

내보내기 산출물은 원고의 파생 결과이다. 수정정보, 상태, 후보, 로그, 메모를 내보내기 Markdown 안에 중복 저장하지 않는다.

---

# 18. Git 변경 비교 데이터

Git 변경 비교는 기본적으로 Git 자체의 diff를 사용한다. 다만 OL-DESK 화면 표시를 위해 revision JSON에 다음 정보를 연결할 수 있다.

```json
{
  "revision_id": "rev-001",
  "base_commit": "",
  "current_commit": "",
  "changed_files": [],
  "changed_segments": []
}
```

Git diff 결과 자체를 별도 JSON으로 과도하게 중복 저장하지 않는다. 필요한 경우 화면 표시 캐시만 둘 수 있다.

---

# 19. 최종 원칙

```text
Contents-Asset은 OL-DESK-CREW의 단일 데이터 소스이다.
원고와 내보내기 산출물은 Markdown으로, 수정정보와 메모는 JSON으로 저장한다.
Paperclip API에 의존하지 않고 에이전트 완료 로그 JSON을 활용한다.
shared에는 공통 지침만 두고 프로젝트별 판단 데이터는 프로젝트 안에 둔다.
JSON은 OL-DESK가 읽고 쓰기 쉬워야 하며, Markdown은 사람이 읽기 쉬워야 한다.
```
