# 00_OL-CREW_전체기획

## 인간 중심 AI 협업 콘텐츠 제작 프레임워크

**문서명:** OL-CREW 전체기획  
**버전:** v0.3  
**작성일:** 2026-06-06  
**문서 성격:** OL-CREW 상위 프레임워크 및 공통 운영 원칙 기획서  
**우선 구현체:** OL-DESK-CREW  
**후속 문서:** `01_OL-DESK_개발기획.md`, `02_Contents-Asset_데이터구조기획.md`, `03_AI-Agent_운영기획.md`, `04_번역워크플로우_운영매뉴얼.md`  

---

# 1. 한 줄 정의

**OL-CREW는 인간 창작자와 감수자가 중심이 되어, AI 에이전트 오케스트레이션과 협업하며 불교 콘텐츠를 제작·검수·수정·확정하는 OL 프로젝트의 AI 협업 창작 프레임워크이다.**

OL-CREW는 특정 AI 에이전트 서비스나 특정 오케스트레이션 도구에 종속되지 않는다. Paperclip은 현재 사용할 수 있는 주요 오케스트레이션 도구이지만, OL-CREW의 본질은 Paperclip 자체가 아니라 다음 세 가지에 있다.

```text
1. 인간 중심 창작 UX
2. 콘텐츠 자산 중심 데이터 구조
3. 도구 독립적인 AI-Agent 운영 지침
```

---

# 2. 명칭과 범위

기존 `OL번역원` 개념은 폐기한다. 새 상위 개념은 `OL-CREW`로 한다.

```text
OL번역원
= 번역 중심 단일 프로덕션 개념

OL-CREW
= 번역, 글쓰기, 이미지, 영상 등 불교 콘텐츠 창작 전반을 포괄하는 AI 협업 프레임워크
```

OL-CREW는 OL 프로젝트 소속이며, OL 프로젝트의 철학과 콘텐츠 방향성을 계승한다.

---

# 3. 세부 Crew 프로젝트

OL-CREW는 여러 세부 Crew 프로젝트로 확장된다.

```text
OL-DESK-CREW
= 불교전문문헌 번역 중심 Crew

OL-WRITER-CREW
= 텍스트 중심 불교 콘텐츠 창작 Crew

OL-TOON-CREW
= 이미지·만화 중심 불교 콘텐츠 창작 Crew

OL-STUDIO-CREW
= 영상 중심 불교 콘텐츠 창작 Crew
```

현재 단계에서는 `OL-DESK-CREW`를 첫 구현체로 개발한다. OL-DESK의 구조가 안정되면 같은 프레임워크를 응용하여 `OL-WRITER-CREW`, `OL-TOON-CREW`, `OL-STUDIO-CREW`를 순차적으로 개발한다.

---

# 4. Crew 공통 3층 구조

각 Crew 프로젝트는 다음 세 층으로 구성한다.

```text
1. Human UX
2. Contents-Asset
3. AI-Agent
```

## 4.1 Human UX

Human UX는 인간 창작자와 감수자가 실제로 작업하는 화면이다. OL-CREW의 UX는 Astro 웹빌더 기반 로컬 앱을 기본 구현 방식으로 삼는다.

```text
공통 역할:
- 콘텐츠 확인
- 비교
- 직접 수정
- 후보 생성
- 확정
- 최종 창작물 완료
- 변경 이력 확인
```

OL-CREW에서 최종 판단은 Human UX에서 이루어진다. AI 에이전트는 산출물을 제안하고 보조하지만, 인간은 UX에서 실제 내용을 확인하고 수정하고 확정한다.

## 4.2 Contents-Asset

Contents-Asset은 AI와 인간이 협업하여 생산한 창작 자산과 구조화 데이터를 저장하는 단일 데이터 소스이다.

```text
공통 역할:
- 원본 자산 보관
- 중간 산출물 보관
- 인간 수정본 보관
- 확정 산출물 보관
- 수정정보 JSON 보관
- 감수자 메모 JSON 보관
- 에이전트 완료 로그 JSON 보관
- handoff JSON 보관
- 개별·전체 Markdown 내보내기 산출물 보관
```

Contents-Asset은 앱 코드가 아니며, 특정 오케스트레이션 도구의 내부 기록도 아니다. 실제 콘텐츠 자산과 그 콘텐츠를 재현·검수·수정하는 데 필요한 데이터만 저장한다.

## 4.3 AI-Agent

AI-Agent 층은 에이전트에게 역할, 금지사항, 산출물 위치, 완료 조건을 알려주는 지침 체계이다.

```text
공통 역할:
- 에이전트 조직 구성
- 단계별 작업 지침
- 완료 산출물 규칙
- Asset 로그 저장 규칙
- 인간 확정권 보호 규칙
- Agent Performance Loop 운영
```

AI-Agent 지침은 Paperclip 전용 문서가 아니다. Paperclip, Codex CLI, Claude Code, 로컬 AI CLI 등 다양한 실행 환경에서 재사용할 수 있어야 한다.

---

# 5. 도구 독립성 원칙

OL-CREW는 AI 오케스트레이션을 활용하지만 특정 서비스 API에 종속되지 않는다.

Paperclip API를 직접 활용해 로그와 상태를 끌어오는 구조는 편리하지만, 특정 에이전트 서비스에 대한 종속성을 만든다. 따라서 OL-CREW의 기본 구조는 다음과 같이 잡는다.

```text
Paperclip / Codex CLI / Claude Code / 로컬 AI CLI
= 에이전트 실행 환경

Contents-Asset
= 각 과정 완료 시 에이전트가 남기는 표준 산출물과 로그의 저장소

Human UX
= Contents-Asset에 저장된 산출물과 로그를 읽어 사람이 수정·확정하는 화면
```

즉, OL-CREW의 앱은 특정 오케스트레이션 API가 아니라 Contents-Asset의 표준 파일을 읽는다.

---

# 6. 공통 운영 원칙

## 6.1 인간 확정 우선

```text
AI 에이전트
= 생산, 후보 제안, 대조, 반영, 점검

인간 창작자/감수자
= 수정, 확정, 보류, 폐기, 최종 완료
```

용어, 해석, 문체, 최종 산출물의 확정 판단은 인간에게 있다. AI 에이전트는 Crew이자 불교 콘텐츠 제작을 함께하는 도반이다. 사람이 중심이 되어 결과를 평가하고 확정하지만, AI 에이전트와 Crew이자 도반의 관계를 형성한다.

## 6.2 생산 라인과 확정 라인 분리

OL-CREW 공통 원칙은 생산 라인과 확정 라인을 분리하는 것이다.

```text
생산 라인
= 원본을 바탕으로 초안, 후보, 중간 산출물을 만드는 흐름

확정 라인
= 인간 판단을 반영하고 최종 산출물에 가까운 상태로 정리하는 흐름
```

OL-DESK-CREW에서는 이 원칙이 A/B 매니저 구조로 구현된다.

```text
A라인
= 1차·2차 번역 생산

B라인
= 인간 감수 이후 3차 반영과 최종스캔
```

다른 Crew에서는 A/B라는 명칭을 그대로 쓰지 않아도 된다. 다만 생산과 확정은 반드시 분리한다.

## 6.3 Markdown + JSON 경계

OL-CREW는 다음 저장 원칙을 따른다.

```text
사람이 직접 읽는 원고와 창작물
= Markdown 또는 해당 콘텐츠 포맷

수정정보, 상태, 후보, 로그, handoff 데이터
= JSON
```

OL-DESK-CREW에서는 1차·2차·3차·4차 번역본은 Markdown으로 저장하고, 원고 자체를 제외한 수정정보와 구조화 데이터는 JSON으로 저장한다.

개별 번역본과 전체 번역본 일괄 내보내기 산출물은 사람이 읽고 배포 전 검토할 수 있도록 Markdown으로 생성한다. 내보내기 결과는 원고의 파생 산출물이며, 상태·후보·로그·메모 데이터는 계속 JSON으로 관리한다.

감수자 메모는 본문 해석이나 자동 반영 지시가 아니라 인간 감수자가 교정·검수 과정에서 남기는 메타데이터이다. UX에서는 GitHub 댓글처럼 간단히 입력하되, 저장 시에는 대상 문서, 세그먼트, 페이지, 단계, 작성 시각을 JSON으로 자동 연결한다.

## 6.4 shared 폴더 원칙

`shared/`에는 공통 지침과 템플릿만 둔다.

```text
shared/에 둘 수 있는 것:
- 공통 창작 원칙
- 공통 편집 규칙
- 공통 템플릿
- 공통 UI 표시 규칙
- 공통 에이전트 운영 원칙

shared/에 두지 않는 것:
- 프로젝트별 용어집
- 프로젝트별 각주집
- 프로젝트별 태그집
- 프로젝트별 해석 결정
- 프로젝트별 창작 판단
```

용어, 각주, 태그, 해석 결정은 프로젝트 성격에 따라 달라지므로 프로젝트별 Contents-Asset 안에서 관리한다.

---

# 7. Contents-Asset 공통 구조

OL-CREW 전체에서 사용할 Contents-Asset의 공통 구조는 다음과 같이 잡는다.

```text
contents-asset/
├─ projects/
│  └─ {project_id}/
│     ├─ assets/
│     ├─ outputs/
│     ├─ data/
│     ├─ handoff/
│     ├─ logs/
│     └─ archive/
│
└─ shared/
   ├─ principles/
   ├─ rules/
   ├─ templates/
   └─ agent-guides/
```

각 폴더의 공통 의미는 다음이다.

```text
assets/
= 원본 자료와 작업 입력 자산

outputs/
= 사람이 읽거나 확인할 중간·최종 산출물

data/
= 상태, 후보, 수정정보, 구조화 데이터

handoff/
= 인간 UX에서 AI-Agent로 넘기는 작업 지시 데이터

logs/
= 에이전트 완료 로그와 평가 기록

archive/
= 폐기하지 않지만 현재 작업 흐름에서는 제외된 자료
```

OL-DESK-CREW의 번역 전용 세부 구조는 `02_Contents-Asset_데이터구조기획.md`에서 정의한다.

---

# 8. 공통 상태 모델

OL-CREW는 각 Crew의 콘텐츠 종류와 무관하게 다음 공통 상태 모델을 사용한다.

```text
not_started
source_ready
agent_processing
human_review_ready
human_editing
agent_handoff_ready
agent_revision_processing
review_ready
approved
revision_requested
archived
blocked
error
```

UX에서는 이 상태를 프로젝트 성격에 맞는 한글로 표시한다.

예:

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

OL-DESK-CREW의 번역 특화 상태값은 `04_번역워크플로우_운영매뉴얼.md`에서 정의한다.

---

# 9. Revision Cycle 원칙

완료본이라도 수정이 발생하면 단순히 과거 상태로 되돌리지 않는다. 새 revision cycle을 연다.

공통 revision cycle은 다음과 같다.

```text
approved
→ revision_requested
→ human_editing
→ agent_handoff_ready
→ agent_revision_processing
→ review_ready
→ approved
```

OL-DESK-CREW에서는 이 구조가 다음 번역 상태로 특화된다.

```text
final_done
→ revision_needed
→ draft3_preliminary_reopened
→ draft3_requested
→ draft3_generated
→ final_review
→ final_done
```

Revision cycle은 OL-CREW의 핵심이다. 콘텐츠는 한 번 완료된 뒤에도 수정될 수 있으며, 수정은 추적 가능한 새 주기로 관리한다.

---

# 10. Agent Performance Loop

OL-CREW는 AI 에이전트를 단순 실행 도구가 아니라 함께 일하는 Crew이자 도반으로 운영한다.

따라서 각 Crew는 Agent Performance Loop를 가진다.

```text
작업 수행
→ 완료 로그 저장
→ 인간 검토
→ 에이전트 활동 평가
→ 지침 수정
→ 다음 작업 품질 개선
```

에이전트 평가에는 다음이 포함된다.

```text
- 원본 이해 정확도
- 누락 감지 능력
- 후보 제안 품질
- 인간 지시 준수 여부
- 불필요한 파일 생성 여부
- 확정권 침범 여부
- 재작업 발생 여부
```

이 루프는 OL-CREW를 단순 자동화 도구가 아니라 지속적으로 개선되는 협업 프레임워크로 만든다.

---

# 11. Human UX 공통 원칙

모든 Crew의 UX는 다음 원칙을 따른다.

```text
1. 첫 화면은 실제 작업 대시보드여야 한다.
2. 인간이 수정할 수 있는 영역과 볼 수만 있는 영역을 명확히 구분한다.
3. 후보는 채택, 보류, 폐기 상태를 가져야 한다.
4. 원본과 수정본을 비교할 수 있어야 한다.
5. 변경 이력을 볼 수 있어야 한다.
6. 최종 확정은 인간이 명시적으로 수행해야 한다.
7. AI 에이전트의 활동과 품질을 평가할 수 있어야 한다.
8. 모든 주요 화면에서 감수자 메모를 댓글처럼 빠르게 남길 수 있어야 한다.
```

OL-DESK-CREW에서는 이 원칙이 원문, 1차·2차·3차·4차 번역본, 용어, 각주, 태그, 감수자 메모, 변경비교, Markdown 내보내기 화면으로 구현된다.

---

# 12. 첫 구현체: OL-DESK-CREW

OL-DESK-CREW는 OL-CREW의 첫 구현체이다.

```text
대상:
불교전문문헌 번역

핵심 UX:
OL-DESK

핵심 Asset:
원문, 1차·2차·3차·4차 번역본, 용어, 각주, 태그, revision, 감수자 메모, agent-log, Markdown 내보내기 산출물

핵심 Agent:
00-총괄 번역 디렉터-법장
A00-2차 생산 관리 매니저-선행
B00-3차 확정 관리 매니저-결정
그리고 A/B 라인 하위 에이전트
```

OL-DESK-CREW의 상세 설계는 다음 문서에서 다룬다.

```text
01_OL-DESK_개발기획.md
02_Contents-Asset_데이터구조기획.md
03_AI-Agent_운영기획.md
04_번역워크플로우_운영매뉴얼.md
```

---

# 13. 후속 문서 체계

OL-CREW 기획을 구체화하기 위해 다음 문서를 순차적으로 작성한다.

```text
00_OL-CREW_전체기획.md
= 전체 프레임워크와 공통 운영 원칙

01_OL-DESK_개발기획.md
= OL-DESK-CREW의 Astro UX와 기능 설계

02_Contents-Asset_데이터구조기획.md
= Markdown/JSON 저장 구조와 파일 규칙

03_AI-Agent_운영기획.md
= 에이전트 조직, A/B 매니저 구조, 로그 산출 규칙

04_번역워크플로우_운영매뉴얼.md
= 실제 번역 작업 순서와 상태 전환 규칙
```

---

# 14. 최종 원칙

```text
OL-CREW는 도구가 아니라 프레임워크다.
OL-DESK-CREW는 OL-CREW의 첫 구현체다.
인간은 Human UX에서 수정하고 확정한다.
AI 에이전트는 Crew이자 도반으로 작업하고 완료 로그를 남긴다.
원고와 창작물은 사람이 읽을 수 있는 포맷으로, 수정정보는 JSON으로 관리한다.
특정 에이전트 API에 종속되지 않고 Contents-Asset을 표준 데이터 소스로 삼는다.
공통 지침은 shared에 두되, 프로젝트별 판단 데이터는 각 프로젝트 안에서 관리한다.
완료본도 수정될 수 있으며, 수정은 새 revision cycle로 처리한다.
```
