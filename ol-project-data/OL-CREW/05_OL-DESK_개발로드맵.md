# 05_OL-DESK_개발로드맵

## OL-DESK Astro 대시보드 구현 로드맵

**문서명:** OL-DESK 개발로드맵  
**버전:** v0.1  
**작성일:** 2026-06-06  
**문서 성격:** OL-DESK-CREW의 Astro 대시보드 구현 순서와 검증 기준 문서  
**상위 문서:** `01_OL-DESK_개발기획.md`  
**관련 문서:** `00_OL-CREW_전체기획.md`, `02_Contents-Asset_데이터구조기획.md`, `03_AI-Agent_운영기획.md`, `04_번역워크플로우_운영매뉴얼.md`

---

# 1. 한 줄 정의

**OL-DESK 개발로드맵은 Contents-Asset에 실제로 생산된 documents, status, source, segments, agent-log 데이터를 Astro 대시보드의 CREW, 진행, 번역, 용어, 각주, 태그, 관리 페이지로 연결하기 위한 단계별 구현 계획이다.**

이 문서는 `01_OL-DESK_개발기획.md`의 UX 목표를 계승하되, Paperclip 운영점검과 A01 테스트 번역 과정에서 실제로 확인된 산출물 구조를 반영한다.

---

# 2. 현재 확인된 운영 상태

## 2.1 Paperclip 팀 구성과 로그

현재 `buddhavamsa` 프로젝트에서 Paperclip 팀 구성과 온보딩 점검이 완료되었고, 다음 성격의 로그가 생산되었다.

```text
- 총괄 디렉터 초기 리뷰 로그
- A00 A라인 intake bootstrap 로그
- A00 A라인 온보딩 검토 로그
- A00 A라인 온보딩 재검증 로그
- B00 B라인 온보딩 및 대기 조건 검토 로그
- A00 테스트 문서 kickoff 검토 로그
- A00 테스트 문서 source_normalized 완료 검토 로그
- A01 테스트 문서 source_normalized 수행 로그
```

확인된 로그 수는 13개이며, 현재 로그의 주요 stage는 다음이다.

```text
source_ready_bootstrap
line_review
agent_onboarding_review
agent_onboarding_recheck
director_review
line_review_followup
onboarding_review
source_normalized
```

현재 로그는 두 계층으로 나뉜다.

```text
운영 로그
= bootstrap, director, manager 단위의 조직·큐·온보딩·차단 사유 로그

문서 단위 생산 로그
= logs/agent-logs/{doc_id}/ 아래에 저장되는 실제 작업 완료 로그
```

OL-DESK는 두 로그를 모두 읽어야 하지만, 화면에서의 역할은 다르게 둔다.

```text
운영 로그
= CREW/관리 페이지에서 조직 상태, blocker, next action, issue 흐름 표시

문서 단위 생산 로그
= 진행/번역/CREW 페이지에서 문서별 단계 이력, 산출물 검증, 에이전트 평가 대상 표시
```

## 2.2 A01 테스트 문서 상태

테스트 문서:

```text
project_id: buddhavamsa
doc_id: gcb-src-007-the-renunciaton-of-sumedha
raw: assets/source/raw/gcb-src-007-the-renunciaton-of-sumedha.md
```

A01 테스트에서 확인된 산출물:

```text
assets/source/normalized/gcb-src-007-the-renunciaton-of-sumedha.md
data/segments/gcb-src-007-the-renunciaton-of-sumedha.json
data/status/gcb-src-007-the-renunciaton-of-sumedha.json
logs/agent-logs/gcb-src-007-the-renunciaton-of-sumedha/2026-06-06_A01_source_normalized.json
```

현재 상태:

```text
current_status: source_normalized
display_status: 원문정리완료
current_owner: A01-기초 정리 에이전트-정안
next_action: reference split 또는 term candidate 검토
blocked: false
```

A01 단계 완료 조건은 `04_번역워크플로우_운영매뉴얼.md`의 `source_normalized` 기준과 일치한다.

```text
- assets/source/normalized/{doc_id}.md 존재
- data/segments/{doc_id}.json 존재
- A01 agent-log 존재
```

## 2.3 테스트에서 새로 확인된 리스크

A01 로그는 작업 성공과 별개로 다음 리스크를 기록했다.

```text
원문 누락 가능성
문단 경계 불확실
OCR 의심
```

특히 raw 원문이 짧고 중간에서 끝나는 형태이므로, OL-DESK는 단순히 `source_normalized` 상태만 보여주면 안 된다. 문서 상세 화면과 진행 목록에서 agent-log의 issue를 읽어 품질 경고를 함께 표시해야 한다.

## 2.4 A라인 draft2 완료 테스트 문서 상태

추가 검증 문서:

```text
project_id: buddhavamsa
doc_id: gcb-src-004-salutation-and-intention
raw: assets/source/raw/gcb-src-004-salutation-and-intention.md
```

`gcb-src-004`는 A라인 전체가 진행되어 `draft2_done`까지 산출물이 실제로 생성되었다.

확인된 산출물:

```text
assets/source/normalized/gcb-src-004-salutation-and-intention.md
data/segments/gcb-src-004-salutation-and-intention.json
data/status/gcb-src-004-salutation-and-intention.json
data/terms/terms.json
data/annotations/annotations.json
data/revisions/gcb-src-004-salutation-and-intention.json
outputs/manuscripts/draft1/gcb-src-004-salutation-and-intention.md
outputs/manuscripts/draft2/gcb-src-004-salutation-and-intention.md
logs/agent-logs/gcb-src-004-salutation-and-intention/2026-06-06_A01_source_normalized.json
logs/agent-logs/gcb-src-004-salutation-and-intention/2026-06-06_A02_reference_split.json
logs/agent-logs/gcb-src-004-salutation-and-intention/2026-06-06_A03_term_candidates.json
logs/agent-logs/gcb-src-004-salutation-and-intention/2026-06-06_A04_draft1_done.json
logs/agent-logs/gcb-src-004-salutation-and-intention/2026-06-06_A05_source_review_done.json
logs/agent-logs/gcb-src-004-salutation-and-intention/2026-06-06_A06_annotation_candidates.json
logs/agent-logs/gcb-src-004-salutation-and-intention/2026-06-06_A07_draft2_done.json
```

현재 상태:

```text
current_status: draft2_done
display_status: 2차번역완료
current_owner: B01-인간검수 준비 에이전트-청문
next_action: 인간검수 준비
blocked: false
```

이번 테스트로 다음이 실제 데이터로 검증되었다.

```text
- draft1, draft2 탭에 필요한 Markdown 산출물
- terms/annotations 후보 페이지에 필요한 JSON 산출물
- source review 결과를 담는 revisions JSON
- A01~A07 단계별 agent-log
- draft2_done 이후 인간 검수 준비 상태 전환
```

## 2.5 운영 절차 provenance 이슈

`gcb-src-004`는 산출물 자체는 유효하지만, 운영 절차상 이슈가 별도로 확인되었다.

확인된 내용:

```text
- A00 completion log가 "executed the full A-line chain"이라고 직접 기록함
- 동일 문서에 A01~A07 명의의 로그와 산출물은 존재함
- 그러나 A00 하위 단계별 child issue 위임 기록은 확인되지 않음
- 이후 A00 process correction log가 manager self-production을 프로세스 오류로 판정함
```

따라서 OL-DESK는 다음 두 사실을 동시에 다뤄야 한다.

```text
산출물 유효성
= 파일과 로그가 단계 완료 조건을 충족하는가

운영 절차 provenance
= 해당 산출물이 올바른 위임 체계 아래 생산되었는가
```

---

# 3. 개발 원칙

## 3.1 Contents-Asset 우선

OL-DESK는 Paperclip API를 직접 호출하지 않는다.

```text
읽기:
- contents-asset/projects/{project_id}/data/documents.json
- contents-asset/projects/{project_id}/data/status/
- contents-asset/projects/{project_id}/assets/source/
- contents-asset/projects/{project_id}/outputs/manuscripts/
- contents-asset/projects/{project_id}/data/segments/
- contents-asset/projects/{project_id}/data/terms/
- contents-asset/projects/{project_id}/data/annotations/
- contents-asset/projects/{project_id}/data/tags/
- contents-asset/projects/{project_id}/data/revisions/
- contents-asset/projects/{project_id}/data/notes/
- contents-asset/projects/{project_id}/handoff/
- contents-asset/projects/{project_id}/logs/agent-logs/
```

Paperclip이 내부에 가진 agent id, instruction bundle 경로, issue 상태는 agent-log에 기록된 경우에만 OL-DESK가 표시한다.

## 3.2 표준 필드 우선, 확장 필드 허용

실제 A01 로그는 표준 agent-log 필드 외에 확장 필드를 포함했다.

표준 필드:

```text
log_id
project_id
doc_id
agent_id
agent_name
stage
input_files
output_files
summary
issues
requires_human_review
next_recommended_action
created_at
```

확장 필드 예:

```text
timestamp
inputs
outputs
normalization_scope
remaining_issues
completion_comment
queue_summary
verification
reviewed_documents
blocked_documents
error_documents
human_decisions_needed
```

구현 원칙:

```text
1. 표준 필드만 필수 파싱한다.
2. 확장 필드는 있으면 표시한다.
3. 확장 필드가 없어도 화면이 깨지지 않아야 한다.
4. issue는 `issue.type`과 `issue.category`를 모두 허용한다.
5. logs/agent-logs/bootstrap, logs/agent-logs/director 같은 운영 로그도 읽되 문서 단위 로그와 구분한다.
6. 운영 로그 안의 process_audit, manager_role_gap, corrective_rule 같은 provenance 이슈를 별도 경고로 분류한다.
```

## 3.3 상태는 status JSON을 기준으로 한다

문서의 현재 상태는 agent-log가 아니라 `data/status/{doc_id}.json`을 기준으로 한다.

```text
status JSON
= 현재 상태, 표시 상태, 현재 담당자, 다음 작업, blocker 여부

agent-log JSON
= 상태에 도달한 근거, 작업 요약, 산출물, 이슈, 다음 권장 조치
```

진행 페이지는 `documents.json + status/`를 주 데이터로 사용하고, 로그는 보조 경고와 이력 표시로 붙인다.

## 3.4 revisions JSON은 두 용도를 모두 허용한다

실제 운영에서는 `data/revisions/{doc_id}.json`이 두 종류의 데이터를 담을 수 있음이 확인되었다.

```text
human revision cycle 데이터
= draft3/final 단계에서 인간이 직접 수정한 기록

agent review carry-forward 데이터
= A05 source review처럼 후속 단계와 인간 검토에 넘길 판단 보류 메모
```

구현 원칙:

```text
1. revisions parser는 단일 고정 스키마만 가정하지 않는다.
2. `current_revision` 중심 구조와 `revisions[].items[]` 중심 구조를 모두 허용한다.
3. created_by가 `human`이면 human revision, `A05` 같은 agent면 review note로 분류한다.
4. 번역 페이지에서는 두 데이터를 같은 탭에 섞지 않고 구분 표시한다.
5. handoff 생성 시에는 human revision 데이터만 기본 대상으로 삼는다.
```

## 3.5 OL 홈페이지 스타일 계승

OL-DESK는 OL 홈페이지와 같은 디자인 언어를 사용한다. 현재 OL 홈페이지에서 사용 중인 스타일 코드는 `ol-desk-crew/manual/styles/` 아래에 보관되어 있으며, OL-DESK Astro 앱은 이 스타일을 초기 디자인 시스템으로 가져온다.

스타일 소스:

```text
ol-desk-crew/manual/styles/global.css
ol-desk-crew/manual/styles/tokens.css
ol-desk-crew/manual/styles/ol-components.css
```

역할:

```text
global.css
= Tailwind, basecoat-css, OL token, OL component style의 import 진입점

tokens.css
= 색상, 타이포그래피, radius, shadow, spacing, dark mode token

ol-components.css
= .ol- prefix 기반 header, nav, button, card, badge, section, layout component
```

OL-DESK 구현 원칙:

```text
1. OL-DESK는 별도 디자인 토큰을 새로 만들지 않는다.
2. CSS 변수는 `--ol-*` 토큰을 우선 사용한다.
3. 공통 UI class는 `.ol-*` 컴포넌트 스타일을 우선 사용한다.
4. 대시보드 전용 스타일이 필요하면 `.ol-desk-*` prefix로 확장한다.
5. 기존 OL 홈페이지 스타일 파일은 원본 기준으로 보존하고, 앱 내부에서는 복사 또는 import 전략을 명확히 둔다.
6. Tailwind와 basecoat-css를 사용할 때도 색상·간격·radius는 OL token과 충돌하지 않게 맞춘다.
```

Astro 적용 기준:

```text
src/styles/global.css 또는 앱의 전역 스타일 진입점에서 다음 순서를 유지한다.

1. tailwindcss
2. basecoat-css
3. tokens.css
4. ol-components.css
```

디자인 검증 기준:

```text
- 헤더, 내비게이션, 버튼, 카드, 배지의 기본 외형이 OL 홈페이지와 일관된다.
- CREW, 진행, 번역, 관리 화면은 같은 token scale을 사용한다.
- 문서 리스크 배지, 상태 배지, agent-log 카드도 `.ol-badge`, `.ol-card`, `.ol-btn` 계열을 우선한다.
- 대시보드 특화 테이블, split pane, log timeline만 OL-DESK 전용 class로 확장한다.
```

---

# 4. 페이지별 구현 로드맵

## 4.1 공통 데이터 계층

우선 구현할 공통 데이터 계층과 스타일 계층:

```text
ProjectRepository
= contents-asset/projects 하위 프로젝트 목록을 읽는다.

DocumentRepository
= documents.json과 data/status/{doc_id}.json을 결합한다.

SourceRepository
= raw, normalized, segments JSON을 읽는다.

ManuscriptRepository
= draft1, draft2, draft3, draft4 Markdown 존재 여부와 본문을 읽는다.

AgentLogRepository
= logs/agent-logs 하위의 운영 로그와 문서 단위 로그를 정규화한다.

IssueRiskMapper
= agent-log issues를 대시보드 경고, blocker, 품질 리스크로 분류한다.

StyleSystem
= manual/styles의 OL 홈페이지 스타일을 Astro 앱 전역 스타일로 연결한다.
```

정규화된 문서 모델:

```json
{
  "project_id": "buddhavamsa",
  "doc_id": "gcb-src-007-the-renunciaton-of-sumedha",
  "title": "IV: The Renunciaton of Sumedha",
  "current_status": "source_normalized",
  "display_status": "원문정리완료",
  "current_owner": "A01-기초 정리 에이전트-정안",
  "next_action": "reference split 또는 term candidate 검토",
  "paths": {
    "raw": "assets/source/raw/gcb-src-007-the-renunciaton-of-sumedha.md",
    "normalized": "assets/source/normalized/gcb-src-007-the-renunciaton-of-sumedha.md",
    "segments": "data/segments/gcb-src-007-the-renunciaton-of-sumedha.json"
  },
  "available_assets": {
    "raw": true,
    "normalized": true,
    "segments": true,
    "draft1": false,
    "draft2": false,
    "draft3": false,
    "draft4": false
  },
  "latest_agent_stage": "source_normalized",
  "risk_count": 3
}
```

## 4.2 CREW 페이지

CREW 페이지는 가장 먼저 구현한다. 현재 로그만으로도 실제 데이터를 표시할 수 있기 때문이다.

필수 기능:

```text
- 에이전트별 로그 목록
- stage별 로그 필터
- 운영 로그와 문서 로그 구분
- issue.type별 경고 목록
- next_recommended_action 표시
- A01 테스트 문서 수행 이력 표시
- 에이전트 평가 작성 진입점
```

현재 표시 가능한 데이터:

```text
- 00-총괄 번역 디렉터-법장 로그
- A00-2차 생산 관리 매니저-선행 로그
- B00-3차 확정 관리 매니저-결정 로그
- A01-기초 정리 에이전트-정안 로그
- A01-A07 instruction bundle 검증 결과
- B라인 대기 사유
- raw completeness risk
```

CREW 페이지의 핵심 UI 블록:

```text
Agent Activity Timeline
= created_at 역순 로그 타임라인

Agent Matrix
= 에이전트별 로그 수, 최근 stage, 최근 issue, 평가 상태

Issue Board
= blocker, raw risk, missing output, permission issue 분류 표시

Document Activity
= doc_id별 참여 에이전트와 완료 단계
```

## 4.3 진행 페이지

진행 페이지는 `documents.json + status/`를 기준으로 구현한다.

필수 기능:

```text
- 프로젝트별 문헌 목록
- 문서 ID, 제목, 현재 상태, 표시 상태
- 현재 담당자와 다음 작업
- 상태 필터
- 산출물 존재 여부 배지
- agent-log issue 기반 경고 배지
- 클릭 시 번역 페이지 이동
```

상태 필터 초기안:

```text
준비
= not_started, source_ready

A라인 진행
= source_normalized, reference_ready, term_candidates_done, draft1_done, source_review_done, annotation_candidates_done, draft2_done

인간 감수
= human_review_ready, human_editing, draft3_handoff_ready

B라인 진행
= draft3_requested, draft3_generated, final_scan_done, final_review

완료
= final_done, archived

주의
= blocked, error, revision_needed 또는 agent-log issue 존재
```

테스트 문서 표시 예:

```text
문서: gcb-src-007-the-renunciaton-of-sumedha
상태: 원문정리완료
담당: A01-기초 정리 에이전트-정안
다음 작업: reference split 또는 term candidate 검토
산출물: raw, normalized, segments, A01 log
주의: 원문 누락 가능성, 문단 경계 불확실, OCR 의심
```

## 4.4 번역 페이지

번역 페이지는 단계별로 점진 구현한다.

### 4.4.1 A01 기반 초기 번역 화면

A01 테스트 산출물만으로 구현 가능한 화면:

```text
- raw 원문 보기
- normalized 원문 보기
- raw/normalized 병렬 보기
- segments JSON 기반 세그먼트 목록
- 문단 ID [001], [002] 기반 이동
- A01 agent-log 요약 표시
- raw completeness risk 경고 표시
```

이 단계에서 아직 구현하지 않는 것:

```text
- draft1 보기
- draft2 보기
- 3차 가번역 편집
- 4차 최종원고 편집
- handoff 생성
```

### 4.4.2 A04-A07 이후 번역 화면

A04-A07 테스트가 끝나면 다음을 추가한다.

```text
- draft1 보기
- source review 결과 표시
- annotation candidates 표시
- draft2 보기
- 원문 + draft1 병렬 보기
- 원문 + draft2 병렬 보기
- draft2 기반 3차 가번역 초기화
```

### 4.4.3 인간 감수 화면

`human_review_ready` 이후 구현 대상:

```text
- 3차 가번역 편집
- 감수자 메모 작성
- 용어·각주·태그 후보 채택/보류/폐기
- draft3 handoff JSON 생성
- 수정 내용 revision JSON 저장
```

### 4.4.4 B라인 이후 화면

B라인 로그와 산출물이 생긴 뒤 구현 대상:

```text
- draft3 생성본 보기
- draft3 가번역과 생성본 비교
- final_scan_done 결과 확인
- draft4 최종원고 편집
- final_done 처리
```

## 4.5 용어 페이지

용어 페이지는 A03 이후 실데이터가 생기면 본격 구현한다.

초기 구현:

```text
- data/terms/terms.json 로딩
- candidate, approved, hold, rejected, deprecated 필터
- doc_id, first_doc_id, source_term 검색
- 후보 없음 상태 표시
```

A03 테스트 후 추가 검증:

```text
- A03 agent-log와 terms.json 변경이 연결되는가
- 후보가 인간 승인 없이 approved가 되지 않는가
- 기존 approved 용어와 신규 candidate 충돌이 표시되는가
```

## 4.6 각주 페이지

각주 페이지는 A06 이후 실데이터가 생기면 본격 구현한다.

초기 구현:

```text
- data/annotations/annotations.json 로딩
- 후보/승인/보류/폐기 상태 필터
- target_text, annotation_type, first_doc_id 검색
- 후보 없음 상태 표시
```

A06 테스트 후 추가 검증:

```text
- A06 agent-log와 annotations.json 변경이 연결되는가
- A06이 각주 후보만 생성했는가
- 교리 해설문을 본문 확정처럼 생성하지 않았는가
```

## 4.7 태그 페이지

태그 페이지는 후보 데이터가 생성되기 전에도 기본 골격을 만들 수 있다.

초기 구현:

```text
- data/tags/tags.json 로딩
- 문서별 태그 필터
- segment_id별 태그 표시
- 신규 태그 생성 UI
```

후속 검증:

```text
- 태그가 검색과 분류를 위한 표시 데이터로만 사용되는가
- 태그가 관계 구조나 온톨로지처럼 과도하게 확장되지 않는가
```

## 4.8 관리 페이지

관리 페이지는 운영 로그와 파일 상태를 기반으로 먼저 구현할 수 있다.

필수 기능:

```text
- Contents-Asset 경로 확인
- 프로젝트 목록과 현재 프로젝트 표시
- documents/status/raw/normalized/segments/logs 개수 표시
- 누락 산출물 검사
- agent-log JSON 파싱 오류 검사
- raw completeness risk 문서 목록
- Git 상태 요약
```

현재 즉시 표시 가능한 점검 항목:

```text
- documents.json 문서 수
- raw markdown 수
- status JSON 수
- source_normalized 문서 수
- 문서별 agent-log 수
- JSON 파싱 오류
- issue.type 분포
```

---

# 5. API 구현 로드맵

## 5.1 1차 API

대시보드 읽기 중심 API를 먼저 만든다.

```text
GET /api/projects
GET /api/projects/:project_id/summary
GET /api/projects/:project_id/documents
GET /api/projects/:project_id/documents/:doc_id
GET /api/projects/:project_id/documents/:doc_id/source
GET /api/projects/:project_id/documents/:doc_id/segments
GET /api/projects/:project_id/documents/:doc_id/logs
GET /api/projects/:project_id/agents/logs
GET /api/projects/:project_id/risks
```

## 5.2 2차 API

인간 감수와 메모 저장 기능을 추가한다.

```text
GET  /api/projects/:project_id/documents/:doc_id/notes
POST /api/projects/:project_id/documents/:doc_id/notes
PATCH /api/projects/:project_id/documents/:doc_id/notes/:note_id
POST /api/projects/:project_id/agents/evaluations
```

## 5.3 3차 API

번역 수정과 handoff 생성을 추가한다.

```text
POST /api/projects/:project_id/documents/:doc_id/draft3/save
POST /api/projects/:project_id/documents/:doc_id/final/save
POST /api/projects/:project_id/documents/:doc_id/handoff/draft3
GET  /api/projects/:project_id/documents/:doc_id/diff
POST /api/projects/:project_id/documents/:doc_id/export
POST /api/projects/:project_id/export/all
```

---

# 6. 구현 단계

## 6.1 Phase 0: 데이터 인덱서

목표:

```text
Contents-Asset을 읽어 대시보드에서 사용할 정규화 모델을 만들고, OL 홈페이지 스타일을 OL-DESK 앱에 연결한다.
```

작업:

```text
- manual/styles/global.css, tokens.css, ol-components.css 확인
- Astro 앱 전역 스타일 진입점 구성
- OL token과 .ol-* component class 사용 기준 확정
- 프로젝트 목록 스캔
- documents.json 파싱
- status JSON 결합
- raw/normalized/segments/manuscripts 존재 여부 검사
- agent-log 전체 파싱
- 운영 로그와 문서 로그 분리
- issue.type 정규화
- risk severity 계산
```

완료 기준:

```text
- OL-DESK 화면이 OL 홈페이지 스타일 토큰과 컴포넌트 class를 사용한다.
- 헤더, 버튼, 카드, 배지 기본 스타일이 `.ol-*` 계열로 구성된다.
- buddhavamsa 프로젝트가 목록에 표시된다.
- 208개 문서가 로딩된다.
- gcb-src-007 문서가 source_normalized로 표시된다.
- A01 로그의 issue 3개가 risk로 표시된다.
- JSON 파싱 오류가 화면에 표시된다.
```

## 6.2 Phase 1: CREW + 진행 MVP

목표:

```text
현재 생산된 로그와 status만으로 실제 운영 현황을 볼 수 있게 한다.
```

작업:

```text
- 대시보드 레이아웃
- 프로젝트 선택
- 진행 목록
- 상태 필터
- CREW 로그 타임라인
- 에이전트별 로그 요약
- issue board
- 문서별 로그 연결
- 산출물 유효성 경고와 provenance 경고 분리
```

완료 기준:

```text
- A00, B00, 디렉터, A01 로그가 에이전트별로 보인다.
- bootstrap/director 로그와 doc_id 로그가 구분된다.
- gcb-src-007 클릭 시 문서 상세로 이동한다.
- source_normalized 상태와 raw risk가 같이 표시된다.
- gcb-src-004에서 `draft2_done` 유효성과 `manager self-production` provenance 경고가 분리 표시된다.
```

## 6.3 Phase 2: 번역 A01 뷰

목표:

```text
원문 수집과 정리 원문 품질을 인간이 확인할 수 있게 한다.
```

작업:

```text
- raw Markdown 뷰어
- normalized Markdown 뷰어
- raw/normalized 병렬 보기
- segments 목록
- 세그먼트 클릭 이동
- A01 로그 패널
- raw completeness risk 경고
```

완료 기준:

```text
- gcb-src-007 raw와 normalized를 나란히 볼 수 있다.
- [001]-[005] 세그먼트가 표시된다.
- 원문 누락 가능성 경고가 상단에 표시된다.
- A01 normalization_scope와 remaining_issues를 볼 수 있다.
```

## 6.4 Phase 3: A라인 생산 산출물 확장

목표:

```text
A02-A07 이후 생기는 산출물을 번역 페이지와 진행 페이지에 연결한다.
```

작업:

```text
- references Markdown 표시
- terms 후보 표시
- draft1 Markdown 표시
- source review 로그 표시
- annotations 후보 표시
- draft2 Markdown 표시
- source_normalized 이후 상태 전이 표시
```

완료 기준:

```text
- draft1_done 문서는 draft1 탭이 활성화된다.
- draft2_done 문서는 draft2 탭이 활성화된다.
- terms/annotations 후보가 인간 확정 전 candidate로 표시된다.
- A라인 각 단계의 agent-log 존재 여부가 진행 페이지에 표시된다.
- gcb-src-004의 draft1, draft2, terms, annotations, revisions, A01~A07 로그가 실데이터로 연결된다.
```

## 6.5 Phase 4: 인간 감수 UX

목표:

```text
인간 감수자가 3차 가번역을 수정하고, 메모와 handoff를 생성할 수 있게 한다.
```

작업:

```text
- draft2 기반 draft3 preliminary 생성
- 3차 가번역 편집기
- notes JSON 작성/수정/해결
- terms/annotations/tags 후보 판단
- revision JSON 생성
- draft3 handoff JSON 생성
```

완료 기준:

```text
- 인간 수정 내용이 revisions JSON에 저장된다.
- 메모가 data/notes/{doc_id}.json에 저장된다.
- handoff/draft3/{doc_id}.json이 생성된다.
- handoff에는 인간이 선택한 메모만 included_notes로 연결된다.
```

## 6.6 Phase 5: B라인 및 최종 원고 UX

목표:

```text
B라인 산출물과 4차 최종원고 편집을 OL-DESK에 연결한다.
```

작업:

```text
- draft3 generated 보기
- draft3 preliminary와 generated 비교
- final_scan_done 로그 표시
- draft4 편집기
- final_review/final_done 상태 처리
- revision cycle 재개
```

완료 기준:

```text
- draft3_generated 문서가 3차 생성본 탭에 표시된다.
- final_review 문서가 4차 원고 탭에서 편집 가능하다.
- final_done 이후 revision_needed 흐름을 열 수 있다.
```

---

# 7. 화면별 데이터 매핑

## 7.1 CREW

```text
주 데이터:
- logs/agent-logs/**
- data/agent-evaluations/

보조 데이터:
- data/documents.json
- data/status/

표시 항목:
- agent_name
- stage
- doc_id
- summary
- issues
- next_recommended_action
- created_at
- evaluation status
- provenance warning
```

## 7.2 진행

```text
주 데이터:
- data/documents.json
- data/status/{doc_id}.json

보조 데이터:
- logs/agent-logs/{doc_id}/
- assets/source/
- outputs/manuscripts/

표시 항목:
- doc_id
- title
- display_status
- current_owner
- next_action
- blocked
- available assets
- latest log stage
- risk badges
- process audit badge
```

## 7.3 번역

```text
주 데이터:
- assets/source/raw/{doc_id}.md
- assets/source/normalized/{doc_id}.md
- data/segments/{doc_id}.json
- outputs/manuscripts/draft1/{doc_id}.md
- outputs/manuscripts/draft2/{doc_id}.md
- outputs/manuscripts/draft3/{doc_id}.md
- outputs/manuscripts/draft4/{doc_id}.md

보조 데이터:
- logs/agent-logs/{doc_id}/
- data/notes/{doc_id}.json
- data/revisions/{doc_id}.json

표시 항목:
- raw text
- normalized text
- draft1-4 text
- segment navigation
- document risks
- agent timeline
- notes
- review notes vs human revisions
```

## 7.4 용어·각주·태그

```text
주 데이터:
- data/terms/terms.json
- data/annotations/annotations.json
- data/tags/tags.json

보조 데이터:
- logs/agent-logs/{doc_id}/
- data/notes/{doc_id}.json

표시 항목:
- candidate/approved/hold/rejected/deprecated
- first_doc_id
- segment_id
- created_by
- updated_at
- related notes
```

## 7.5 관리

```text
주 데이터:
- contents-asset filesystem scan
- git status
- logs/agent-logs/**

표시 항목:
- project count
- document count
- raw/status/normalized/segments/manuscript count
- JSON parse errors
- missing required outputs
- issue type distribution
- git modified/untracked files
```

---

# 8. 리스크와 대응

## 8.1 Raw 원문 품질 리스크

확인된 사례:

```text
gcb-src-007-the-renunciaton-of-sumedha
= raw file is only 16 lines and ends mid-section
```

대응:

```text
- agent-log issue에 raw completeness risk가 있으면 진행 목록에 경고 배지를 표시한다.
- 번역 페이지 상단에 "원문 누락 가능성" 경고를 표시한다.
- A02 이후 진행 전 재수집 또는 인간 확인 필요 상태를 제안한다.
- 원문 보존 파일은 OL-DESK가 직접 수정하지 않는다.
```

## 8.2 로그 스키마 확장 리스크

확인된 사례:

```text
일부 로그는 표준 agent-log 필드만 가진다.
일부 로그는 verification, queue_summary, normalization_scope 같은 확장 필드를 가진다.
일부 운영 로그는 doc_id가 없거나 bootstrap/director를 doc_id처럼 사용한다.
일부 로그는 issues[].type 대신 issues[].category를 사용한다.
```

대응:

```text
- log parser는 표준 필드 중심으로 정규화한다.
- 확장 필드는 optional details로 보관한다.
- doc_id가 없으면 operational log로 분류한다.
- doc_id가 bootstrap/director인 경우 문서 목록에 섞지 않는다.
- issue key는 `type ?? category`로 정규화한다.
```

## 8.3 상태와 문서 목록 불일치 리스크

현재 A01 테스트 문서는 status가 `source_normalized`로 갱신되었다. 이후 다른 단계에서도 `documents.json.current_status`와 `data/status/{doc_id}.json.current_status`가 어긋날 수 있다.

대응:

```text
- 화면의 현재 상태는 status JSON을 우선한다.
- documents.json의 current_status는 보조 정보로만 사용한다.
- 불일치가 있으면 관리 페이지에 data consistency warning을 표시한다.
```

## 8.4 인간 확정권 침범 리스크

용어·각주·태그 후보는 인간 확정 전 `approved`가 되면 안 된다.

대응:

```text
- created_by가 agent인 항목이 approved이면 경고한다.
- A03/A06 로그와 후보 JSON을 연결해 후보 생성자를 표시한다.
- 승인/보류/폐기는 OL-DESK에서 인간이 수행한다.
```

## 8.5 프로세스 provenance 리스크

확인된 사례:

```text
gcb-src-004-salutation-and-intention
= 산출물은 유효하지만, A00가 child delegation 없이 전체 A라인 체인을 직접 수행한 것으로 감사 로그에 기록됨
```

대응:

```text
- 산출물 유효성과 운영 절차 provenance를 분리 표시한다.
- process_audit, manager_role_gap, corrective_rule 이슈를 별도 배지로 노출한다.
- 문서 상태를 무효화하지는 않되, CREW/관리 페이지에 audit warning을 남긴다.
- 이후 생산 작업의 품질 평가에는 provenance 위반 여부를 별도 항목으로 반영한다.
```

## 8.6 revisions 구조 이질성 리스크

확인된 사례:

```text
gcb-src-004의 revisions JSON은 human draft revision이 아니라 A05 carry-forward review note 구조로 저장되었다.
```

대응:

```text
- revisions parser는 structure sniffing으로 유형을 판별한다.
- human revision과 agent review note를 다른 UI 그룹으로 나눈다.
- handoff 생성은 human-authored revision 데이터만 기본 입력으로 사용한다.
```

---

# 9. 테스트 계획

## 9.1 현재 통과한 테스트

```text
테스트명: A01 source_normalized 테스트
문서: gcb-src-007-the-renunciaton-of-sumedha
결과: 통과
확인:
- raw 존재
- normalized 생성
- segments 생성
- status source_normalized 전환
- A01 agent-log 생성
- A00 completion review 생성
주의:
- raw completeness risk 존재
```

## 9.2 다음 테스트

### A03 용어 후보 테스트

목표:

```text
terms JSON 후보 생성과 CREW/용어 페이지 연결 검증
```

확인할 것:

```text
- data/terms/terms.json 생성 또는 갱신
- 후보 status가 candidate 또는 hold인지 확인
- A03 agent-log 존재
- 진행 페이지에서 term_candidates_done 표시
- 용어 페이지에서 후보 표시
```

### gcb-src-004 draft2_done 검증

목표:

```text
실제 A라인 전체 산출물과 번역/용어/각주/진행 페이지 데이터 연결 검증
```

확인할 것:

```text
- draft1, draft2 Markdown 표시
- terms/annotations 후보 표시
- revisions JSON을 review note로 파싱
- A01~A07 로그 타임라인 표시
- process provenance 경고 분리 표시
```

### A04 draft1 테스트

목표:

```text
첫 번역 Markdown 산출물과 번역 페이지 draft1 탭 검증
```

확인할 것:

```text
- outputs/manuscripts/draft1/{doc_id}.md 생성
- A04 agent-log 존재
- status draft1_done 전환
- 원문 + draft1 병렬 보기 가능
```

### A07 draft2 테스트

목표:

```text
인간 감수 진입 전 A라인 완료 상태 검증
```

확인할 것:

```text
- outputs/manuscripts/draft2/{doc_id}.md 생성
- A07 agent-log 존재
- status draft2_done 또는 human_review_ready 전환
- 3차 가번역 초기화 가능
```

### Handoff 테스트

목표:

```text
OL-DESK가 인간 판단을 B라인으로 넘기는 JSON 생성 검증
```

확인할 것:

```text
- data/revisions/{doc_id}.json 생성
- data/notes/{doc_id}.json 생성
- handoff/draft3/{doc_id}.json 생성
- included_notes는 인간이 선택한 메모만 포함
```

---

# 10. v0.1 완료 기준

OL-DESK v0.1은 다음 조건을 만족하면 완료로 본다.

```text
1. 프로젝트 목록과 buddhavamsa 프로젝트를 표시할 수 있다.
2. 208개 문서를 documents/status 기준으로 목록화할 수 있다.
3. gcb-src-007 문서의 source_normalized 상태와 산출물을 표시할 수 있다.
4. gcb-src-004 문서의 draft1, draft2, terms, annotations, revisions, A01~A07 로그를 표시할 수 있다.
5. raw, normalized, segments를 번역 페이지에서 볼 수 있다.
6. agent-log를 CREW 페이지에서 에이전트별, 문서별로 볼 수 있다.
7. agent-log issue를 진행 목록과 번역 페이지 경고로 표시할 수 있다.
8. process provenance 경고를 산출물 유효성과 분리해 표시할 수 있다.
9. notes JSON을 생성하고 수정할 수 있다.
10. A라인 draft1/draft2 산출물이 생기면 자동으로 탭이 활성화된다.
11. terms/annotations/tags 후보가 생기면 각 페이지에서 표시하고 인간 판단을 저장할 수 있다.
12. Paperclip API 없이 Contents-Asset만으로 동작한다.
```

---

# 11. 최종 구현 원칙

```text
OL-DESK는 Paperclip 실행기가 아니라 Contents-Asset 편집 대시보드이다.
OL-DESK는 OL 홈페이지 스타일 토큰과 컴포넌트 스타일을 계승한다.
현재 상태는 status JSON을 기준으로 한다.
작업 근거와 품질 리스크는 agent-log를 기준으로 한다.
원고 본문은 Markdown에서 읽고, JSON에는 본문을 중복 저장하지 않는다.
운영 로그와 문서 단위 생산 로그를 구분한다.
확장 로그 필드는 허용하되 표준 필드 파싱이 우선이다.
인간 확정이 필요한 판단은 OL-DESK에서만 확정한다.
raw 품질 리스크는 번역 전에 숨기지 않고 화면에 노출한다.
```
