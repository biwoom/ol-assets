# 01_OL-DESK_개발기획

## OL-DESK-CREW Astro UX 개발 기획

**문서명:** OL-DESK 개발기획  
**버전:** v0.2  
**작성일:** 2026-06-06  
**문서 성격:** OL-DESK-CREW의 인간 감수자 UX 및 기능 설계 문서  
**상위 문서:** `00_OL-CREW_전체기획.md`  
**관련 후속 문서:** `02_Contents-Asset_데이터구조기획.md`, `03_AI-Agent_운영기획.md`, `04_번역워크플로우_운영매뉴얼.md`  

---

# 1. 한 줄 정의

**OL-DESK는 불교전문문헌 번역 프로젝트에서 인간 감수자가 원문과 1·2·3·4차 번역본을 확인하고, 3차 가번역과 4차 최종원고를 직접 수정하며, 용어·각주·태그를 확정하고, 교정·검수 메모와 AI 에이전트 반영 지시를 관리하는 Astro 기반 로컬 편집 대시보드이다.**

OL-DESK는 Paperclip을 대체하지 않는다. Paperclip 또는 기타 에이전트 실행 환경은 AI-Agent 층이고, OL-DESK는 Contents-Asset을 읽고 쓰는 Human UX이다.

---

# 2. 개발 목표

OL-DESK의 v0.1 개발 목표는 다음이다.

```text
1. 프로젝트 선택과 전환
2. 원본문헌 리스트와 진행상태 확인
3. 1차·2차·3차·4차 번역본 보기
4. 원문과 번역본 병렬 비교
5. 3차 가번역 수정
6. 4차 최종원고 수정
7. 용어·각주·태그 추가·수정·삭제
8. 3차 반영 handoff JSON 생성
9. Agent 완료 로그 확인
10. Git 변경 이력 기반 변경비교
11. 주요 페이지별 감수자 메모 작성
12. 개별·전체 번역본 Markdown 내보내기
```

초기 버전에서 하지 않는 것은 다음이다.

```text
- 클라우드 배포
- 다중 사용자 권한 관리
- Paperclip API 직접 연동
- AI CLI 내장 호출
- 자동 GitHub 업로드
- 출판용 최종 배포
```

---

# 3. 기술 방향

OL-DESK는 Astro 기반 로컬 앱으로 구현한다.

```text
Astro
= 라우팅, 레이아웃, 대시보드 UI, 콘텐츠 표시

Node API
= 로컬 파일 읽기/쓰기, JSON 저장, handoff 생성, Git diff 조회

Contents-Asset
= 원고, JSON 데이터, 에이전트 로그, handoff 파일 저장소
```

정적 사이트가 아니라 로컬 서버 기반 편집 앱으로 개발한다.

권장 실행 방식:

```bash
cd ol-desk
npm run dev
```

브라우저 접속:

```text
http://localhost:4321
```

---

# 4. 전체 폴더 관계

OL-DESK-CREW의 기본 프로젝트 구조는 다음이다.

```text
ol-desk-crew/
├─ ol-desk/
│  ├─ package.json
│  ├─ astro.config.mjs
│  ├─ src/
│  └─ README.md
│
├─ contents-asset/
│  ├─ projects/
│  └─ shared/
│
└─ ai-agent/
   ├─ company/
   └─ agents/
```

OL-DESK는 `contents-asset/`을 단일 데이터 소스로 읽고 쓴다.

---

# 5. 데이터 원칙

OL-DESK는 다음 저장 원칙을 따른다.

```text
1. 1차·2차·3차·4차 번역본은 Markdown으로 저장한다.
2. 원문 정리본과 참고번역도 Markdown으로 저장한다.
3. 원고 자체를 제외한 수정정보, 후보, 상태, 로그, 메모, handoff 데이터는 JSON으로 저장한다.
4. 인간 감수자는 Astro UX에서 JSON 데이터를 확인하고 수정한다.
5. Paperclip API를 읽지 않고 Contents-Asset의 표준 JSON과 Markdown을 읽는다.
6. 개별 번역본과 전체 번역본 내보내기 산출물은 Markdown으로 생성한다.
```

## 5.1 Markdown 대상

```text
source/normalized/
manuscripts/draft1/
manuscripts/draft2/
manuscripts/draft3/
manuscripts/draft4/
references/
outputs/exports/individual/
outputs/exports/all/
```

## 5.2 JSON 대상

```text
documents.json
segments/
status/
terms/
annotations/
tags/
revisions/
notes/
agent-logs/
handoff/
agent-evaluations/
```

상세 파일 구조와 JSON 스키마는 `02_Contents-Asset_데이터구조기획.md`에서 정의한다.

---

# 6. 사용자와 권한

OL-DESK의 기본 사용자는 인간 감수자이다.

```text
인간 감수자 권한:
- 3차 가번역 수정
- 4차 최종원고 수정
- 신규 용어 생성
- 신규 각주 생성
- 신규 태그 생성
- 후보 채택·보류·폐기
- 교정·검수 메모 작성
- 최종 승인
- 에이전트 활동 평가
- 번역본 Markdown 내보내기
```

보기 전용 영역:

```text
- 원문
- 1차 번역본
- 2차 번역본
- 에이전트 원본 후보
- 에이전트 완료 로그
```

직접 수정 영역:

```text
- 3차 가번역
- 4차 최종원고
- 용어 JSON
- 각주 JSON
- 태그 JSON
- revision JSON
- 감수자 메모 JSON
- 에이전트 평가 JSON
```

---

# 7. 주요 메뉴

OL-DESK는 대시보드형 UI로 구성한다.

기본 메뉴:

```text
CREW
진행
번역
용어
각주
태그
관리
```

상단 헤더에는 현재 프로젝트 선택, 현재 문서명, 저장 상태, Git 상태를 표시한다.

---

# 8. CREW 페이지

CREW 페이지는 에이전트 활동 기록과 평가를 관리한다.

## 8.1 기능

```text
- 에이전트 목록 표시
- 에이전트별 완료 로그 표시
- 문서별 참여 에이전트 표시
- Issue 또는 작업 단위별 완료 여부 표시
- 인간 감수자의 에이전트 활동 평가 기록
- 재작업 사유 기록
- 지침 개선 아이디어 기록
```

## 8.2 Agent Performance Loop

CREW 페이지는 다음 루프를 지원한다.

```text
작업 수행
→ 완료 로그 저장
→ 인간 검토
→ 에이전트 활동 평가
→ 지침 수정 아이디어 기록
→ 다음 작업 품질 개선
```

## 8.3 평가 항목

```text
- 원문 이해 정확도
- 누락 감지 능력
- 후보 제안 품질
- 인간 지시 준수 여부
- 불필요한 파일 생성 여부
- 확정권 침범 여부
- 재작업 발생 여부
```

---

# 9. 진행 페이지

진행 페이지는 프로젝트별 원본문헌과 진행상태를 보여준다.

## 9.1 기능

```text
- 프로젝트별 문헌 목록 표시
- 원본 소스 디렉토리 표시
- 준비중, 진행중, 감수필요, 완료됨 상태 필터
- 문서 ID, 제목, 현재 상태, 다음 작업 표시
- 개별 문헌 클릭 시 번역 페이지로 이동
```

## 9.2 상태 표시

UX에는 한글 상태를 표시한다.

```text
준비전
원본준비
AI작업중
검수대기
사람수정중
AI반영요청
AI수정반영중
최종검토
승인완료
수정요청
보관
보류
오류
```

번역 특화 상태값은 `04_번역워크플로우_운영매뉴얼.md`에서 정의한다.

---

# 10. 번역 페이지

번역 페이지는 OL-DESK의 핵심 화면이다.

## 10.1 기본 역할

```text
- 원문 보기
- 1차 번역본 보기
- 2차 번역본 보기
- 3차 번역본 보기
- 4차 최종원고 보기
- 3차 가번역 수정
- 4차 최종원고 수정
- 병렬 비교
- 변경비교
- 감수자 메모
- Markdown 내보내기
- handoff JSON 생성
```

## 10.2 탭 구성

```text
1차 번역
2차 번역
3차 번역
4차 원고
병렬보기
변경비교
메모
내보내기
```

각 탭의 의미:

```text
1차 번역
= 에이전트 초벌 번역 보기 전용

2차 번역
= 에이전트 윤문 번역 보기 전용

3차 번역
= 인간이 수정한 3차 가번역과 B라인이 생성한 3차 번역본 확인

4차 원고
= 인간 최종 탈고 영역

병렬보기
= 원문, 1차, 2차, 3차, 4차 중 선택하여 나란히 비교

변경비교
= GitHub history처럼 원본과 수정 부분을 겹쳐서 비교

메모
= 현재 문서, 세그먼트, 탭, 작업 단계에 감수자 메모를 댓글처럼 남김

내보내기
= 1차·2차·3차·4차 번역본을 개별 또는 전체 Markdown으로 생성
```

## 10.3 3차 번역 탭

3차 번역 탭은 두 상태를 가진다.

```text
3차 가번역
= 인간 감수자가 직접 수정하는 영역

3차 생성본
= B라인 에이전트가 인간 확정 판단을 반영해 생성한 번역본
```

3차 가번역은 2차 번역본을 초기값으로 삼는다.

상태:

```text
editing
ready_for_draft3
draft3_requested
draft3_generated
locked
```

## 10.4 4차 원고 탭

4차 원고 탭은 인간 최종 탈고 영역이다.

```text
역할:
- 최종 문체 조정
- 최종 원고 수정
- 최종 승인
- final_done 처리
```

4차 원고는 3차 번역본을 바탕으로 생성된다.

## 10.5 병렬보기

병렬보기는 다음 조합을 지원한다.

```text
원문 + 1차
원문 + 2차
원문 + 3차
2차 + 3차
3차 + 4차
원문 + 2차 + 3차
원문 + 2차 + 3차 + 4차
```

## 10.6 변경비교

변경비교 탭은 Git 변경 이력을 활용한다.

```text
기능:
- 원본 보기
- 수정본 보기
- 병렬 diff 보기
- 겹쳐 보기
- 변경된 세그먼트만 보기
- revision cycle별 변경 보기
```

## 10.7 감수자 메모

감수자 메모는 본문 해석 메모가 아니라 교정과 검수를 위한 메타데이터이다.

```text
UX 원칙:
- GitHub 댓글처럼 본문만 빠르게 입력한다.
- OL-DESK가 현재 프로젝트, 문서, 세그먼트, 탭, 단계, 작성 시각을 자동 연결한다.
- 메모는 본문, 용어, 각주, 태그에 자동 반영되지 않는다.
- handoff에는 인간이 명시적으로 포함시킨 메모만 들어간다.
```

저장 위치:

```text
data/notes/{doc_id}.json
```

---

# 11. 용어 페이지

용어 페이지는 프로젝트별 용어 데이터를 관리한다.

```text
기능:
- 프로젝트 전체 누적 용어 확인
- 신규 용어 추가
- 기존 용어 수정
- 용어 삭제 또는 비활성화
- 후보 채택·보류·폐기
- 용어 변경 이력 확인
- 용어별 감수자 메모 작성
```

용어 데이터는 shared에 저장하지 않는다. 프로젝트별 `data/terms/`에 저장한다.

---

# 12. 각주 페이지

각주 페이지는 프로젝트별 각주 데이터를 관리한다.

```text
기능:
- 프로젝트 전체 누적 각주 확인
- 신규 각주 추가
- 기존 각주 수정
- 각주 삭제 또는 비활성화
- 후보 채택·보류·폐기
- 각주 변경 이력 확인
- 각주별 감수자 메모 작성
```

각주 데이터는 프로젝트별 `data/annotations/`에 저장한다.

---

# 13. 태그 페이지

태그 페이지는 프로젝트별 태그 데이터를 관리한다.

```text
기능:
- 프로젝트 전체 누적 태그 확인
- 신규 태그 추가
- 기존 태그 수정
- 태그 삭제 또는 비활성화
- 후보 채택·보류·폐기
- 태그 변경 이력 확인
- 태그별 감수자 메모 작성
```

태그 데이터는 프로젝트별 `data/tags/`에 저장한다.

---

# 14. 관리 페이지

관리 페이지는 프로젝트 설정과 운영 보조 기능을 담당한다.

```text
기능:
- 프로젝트 추가
- 프로젝트 전환
- 원본 소스 디렉토리 지정
- Contents-Asset 경로 확인
- 에이전트 활동 평가 정보 관리
- OL-DESK 코드 업데이트 아이디어 기록
- 관리문서 생성
- 이전 관리문서 저장소
- GitHub 업로드 또는 Git 연동 기능
- 개별·전체 Markdown 내보내기 관리
```

초기 버전에서는 GitHub 자동 업로드보다 로컬 Git 상태 확인과 diff 표시를 우선한다.

---

# 15. Handoff 기능

OL-DESK는 인간 수정과 확정 판단을 AI-Agent가 읽을 수 있는 JSON으로 저장한다.

대표 handoff:

```text
draft3 handoff
= 3차 반영 에이전트에게 넘기는 지시 데이터

revision handoff
= 완료본 수정 후 새 revision cycle을 요청하는 지시 데이터
```

handoff JSON에는 다음 정보가 들어간다.

```text
- project_id
- doc_id
- source_revision
- target_stage
- human_modified_segments
- approved_terms
- approved_annotations
- approved_tags
- rejected_candidates
- pending_items
- included_notes
- instruction_summary
- created_at
```

감수자 메모는 handoff의 기본 구성요소가 아니다. 특정 메모를 AI-Agent가 참고해야 할 때만 인간 감수자가 명시적으로 선택하여 `included_notes`에 연결한다.

세부 스키마는 `02_Contents-Asset_데이터구조기획.md`에서 정의한다.

---

# 16. Revision Cycle UX

완료본이라도 수정이 발생하면 단순히 과거 상태로 되돌리지 않는다. 새 revision cycle을 연다.

OL-DESK는 다음 흐름을 지원해야 한다.

```text
final_done
→ revision_needed
→ draft3_preliminary_reopened
→ draft3_requested
→ draft3_generated
→ final_review
→ final_done
```

UX 표시:

```text
최종완료
→ 수정필요
→ 3차가번역 재개
→ 3차반영 요청
→ 3차번역 생성
→ 최종검토
→ 최종완료
```

---

# 17. API 초안

초기 API는 파일 읽기/쓰기 중심으로 제한한다.

```text
GET  /api/projects
GET  /api/projects/:project_id/documents
GET  /api/projects/:project_id/documents/:doc_id
POST /api/projects/:project_id/documents/:doc_id/draft3/save
POST /api/projects/:project_id/documents/:doc_id/final/save
POST /api/projects/:project_id/documents/:doc_id/handoff/draft3
GET  /api/projects/:project_id/documents/:doc_id/notes
POST /api/projects/:project_id/documents/:doc_id/notes
PATCH /api/projects/:project_id/documents/:doc_id/notes/:note_id
POST /api/projects/:project_id/documents/:doc_id/export
POST /api/projects/:project_id/export/all
GET  /api/projects/:project_id/documents/:doc_id/diff
GET  /api/projects/:project_id/agents/logs
POST /api/projects/:project_id/agents/evaluations
```

API는 Contents-Asset 파일을 읽고 쓴다. Paperclip API를 직접 호출하지 않는다.

---

# 18. v0.1 구현 우선순위

## 18.1 1단계

```text
- 프로젝트 목록
- 진행 목록
- 문서 상세 데이터 로딩
- 1차·2차 번역 보기
- 3차 가번역 편집
- 저장 기능
- 감수자 메모 작성과 목록 표시
```

## 18.2 2단계

```text
- 용어·각주·태그 패널
- 후보 채택·보류·폐기
- draft3 handoff JSON 생성
- Agent 완료 로그 표시
```

## 18.3 3단계

```text
- 4차 최종원고 편집
- Git diff 기반 변경비교
- revision cycle 지원
- 에이전트 활동 평가
- 개별·전체 Markdown 내보내기
```

---

# 19. 완료 기준

OL-DESK v0.1은 다음 조건을 만족하면 완료로 본다.

```text
1. 프로젝트를 선택할 수 있다.
2. 문헌 목록과 상태를 볼 수 있다.
3. 문서별 1차·2차 번역을 볼 수 있다.
4. 3차 가번역을 수정하고 저장할 수 있다.
5. 용어·각주·태그 후보를 확인하고 판단할 수 있다.
6. draft3 handoff JSON을 생성할 수 있다.
7. 에이전트 완료 로그를 볼 수 있다.
8. Paperclip API 없이 Contents-Asset만으로 작동한다.
9. 주요 페이지에서 감수자 메모를 댓글처럼 작성하고 JSON으로 저장할 수 있다.
10. 개별 문서와 전체 문서의 번역본을 Markdown으로 내보낼 수 있다.
```

---

# 20. 최종 원칙

```text
OL-DESK는 OL-DESK-CREW의 Human UX이다.
인간 감수자는 OL-DESK에서 수정하고 확정한다.
AI 에이전트는 Contents-Asset에 Markdown 원고와 JSON 로그를 남긴다.
OL-DESK는 Paperclip API가 아니라 Contents-Asset을 읽는다.
1차·2차는 보기 전용, 3차·4차는 인간 수정 가능 영역이다.
원고는 Markdown, 수정정보는 JSON이다.
Git 변경 이력은 번역 페이지의 변경비교 탭에서 활용한다.
```
