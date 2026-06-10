# Paperclip과 번역 프로젝트 튜토리얼 v0.2

## 문헌 번역 AI 협업 워크플로우 v0.3 기반

**문서명:** Paperclip과 번역 프로젝트 튜토리얼
**버전:** v0.2
**기준 매뉴얼:** 문헌 번역 AI 협업 워크플로우 매뉴얼 v0.3
**목적:** Paperclip을 이용해 불교문헌 번역용 AI 다중 에이전트 작업환경을 실제로 구축·운영하는 방법 안내
**범위:** 설치, 프로젝트 폴더 구성, 에이전트 조직도, Issue 템플릿, 단계별 운영법
**제외:** 출판, 웹 등록, 디자인, 온톨로지, 지식그래프, Entity 구조화

---

# 0. v0.2 튜토리얼의 핵심 변경점

이전 튜토리얼 v0.1은 v0.2 번역 매뉴얼의 “문서별 통합 원고 파일” 구조를 기준으로 작성되었다. 그러나 새 매뉴얼 v0.3은 다음처럼 바뀌었다.

```text
문서별 통합 원고 1파일 방식 폐기
원본·정규화 원문·참고번역·1차·2차·3차·최종본을 목적별 폴더에 분리
문서 연결성은 doc_id와 metadata 파일로 유지
master-checklist.md로 전체 진행 관리
용어집·각주집·해석집은 프로젝트 단위로 누적
```

v0.3 매뉴얼은 문서별 통합 파일 대신, 원본·정규화 원문·참고 번역·차수별 번역본·검토 결과를 목적별 폴더에 나누고, 전체 진행을 `master-checklist.md`와 문서별 metadata 파일로 관리하도록 설계한다. 

따라서 Paperclip 튜토리얼 v0.2의 목표도 바뀐다.

```text
Paperclip이 문서 하나를 통째로 관리하는 것이 아니라,
각 단계별 파일을 정확히 읽고,
정해진 위치에 산출물을 생성하며,
사람의 승인 이후 다음 단계로 넘기는 운영판이 되도록 구성한다.
```

---

# 1. Paperclip의 역할

Paperclip은 번역 AI 자체가 아니다. Paperclip은 여러 AI 에이전트를 “회사 조직”처럼 관리하는 오픈소스 오케스트레이션 도구다. 공식 README는 Paperclip을 Node.js 서버와 React UI로 구성된 앱이며, 여러 AI 에이전트에게 목표를 부여하고 작업·비용을 대시보드에서 추적할 수 있다고 설명한다. ([GitHub][1])

번역 프로젝트에서는 다음처럼 대응시킨다.

```text
Paperclip Company
= 불교문헌 번역 편집실

Company Goal
= 특정 문헌군의 번역·감수·탈고 완료

Agent
= 기초작업, 참고번역 분리, 용어집, 1차 번역, 원문대조, 각주·해석, 2차 번역, 3차 반영, 최종스캔 담당자

Task / Issue
= 특정 문서의 특정 단계 작업

Approval
= 인간 편집자의 승인·확정·보류·반려

Budget
= 에이전트별 토큰·비용 제한

Dashboard
= 전체 번역 프로젝트 진행판
```

Paperclip은 OpenClaw, Claude Code, Codex, Cursor, Bash, HTTP 같은 다양한 실행 주체를 연결할 수 있는 “Bring Your Own Agent” 방식을 지원한다. 즉 Paperclip 설치만으로 번역 에이전트가 자동 생성되는 것이 아니라, 실제 작업을 수행할 AI 런타임 또는 스크립트가 필요하다. ([GitHub][1])

---

# 2. 설치 전 준비

## 2.1 필수 환경

Paperclip 공식 Quickstart는 다음을 요구한다.

```text
Node.js 20+
pnpm 9.15+
```

공식 문서에서도 Node.js 20 이상과 pnpm 9.15 이상을 전제하고, `npx paperclipai onboard --yes`를 가장 빠른 설치 경로로 안내한다. ([Paperclip][2])

확인 명령어:

```bash
node --version
pnpm --version
git --version
```

pnpm이 없다면:

```bash
npm install -g pnpm
```

---

# 3. Paperclip 설치

## 3.1 Quickstart 설치

```bash
npx paperclipai onboard --yes
```

이 명령은 기본 설정 파일을 만들고, 외부 데이터베이스 없이 embedded PostgreSQL을 설정하며, 로컬 파일 저장소와 Paperclip 서버를 시작한다. 공식 Quickstart에 따르면 서버가 시작되면 UI와 API가 기본적으로 `http://localhost:3100`에서 열린다. ([Paperclip][2])

브라우저에서 접속:

```text
http://localhost:3100
```

## 3.2 수동 개발 설치

저장소를 직접 받아 실행할 수도 있다.

```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev
```

Paperclip 공식 저장소의 AGENTS 문서도 개발 실행 시 `pnpm install`, `pnpm dev`를 사용하며, API와 UI가 `http://localhost:3100`에서 실행된다고 안내한다. ([GitHub][3])

## 3.3 기본 점검

```bash
curl http://localhost:3100/api/health
```

Paperclip Quickstart도 서버 상태 확인용으로 `/api/health` 호출을 제시한다. ([Paperclip][2])

문제가 생기면:

```bash
paperclipai doctor
```

---

# 4. 번역 프로젝트 폴더 만들기

v0.3 매뉴얼의 폴더 구조를 그대로 만든다. v0.3은 프로젝트 초기화 단계에서 `docs-meta/`, `sources/raw/`, `sources/normalized/`, `references/`, `translations/draft1/`, `translations/draft2/`, `translations/draft3/`, `translations/final/`, `reviews/source-review/`, `reviews/human-review/`, `reviews/final-scan/` 등을 생성하도록 정의한다. 

예시:

```bash
mkdir -p ~/Projects/buddhist-translation-lab
cd ~/Projects/buddhist-translation-lab

mkdir -p docs-meta
mkdir -p sources/raw sources/normalized
mkdir -p references
mkdir -p translations/draft1 translations/draft2 translations/draft3 translations/final
mkdir -p reviews/source-review reviews/human-review reviews/final-scan
mkdir -p workbench

touch project-index.md
touch master-checklist.md
touch style-guide.md
touch editorial-decisions.md
touch cumulative-glossary.md
touch cumulative-annotations.md
touch cumulative-interpretations.md
```

결과 구조:

```text
buddhist-translation-lab/
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

---

# 5. Paperclip Company 만들기

Paperclip UI에서 새 Company를 만든다.

## Company 이름

```text
Buddhist Translation Desk
```

또는:

```text
불교문헌 번역 편집실
```

## Company Goal

```text
불교 경전·논서·주석서·전기문헌을 원문 보존, 용어 일관성, 원문대조 감수, 각주·해석 검토, 인간 최종 탈고 원칙에 따라 번역한다.

AI 에이전트는 초안 작성, 후보 제안, 누락 검사, 문체 편집 보조를 담당한다.

최종 용어 확정, 각주 확정, 해석 확정, 최종 원고 탈고는 인간 편집자가 수행한다.

이번 프로젝트에서는 텍스트 번역과 원고 탈고에 집중하며, 출판·웹 등록·디자인·온톨로지·지식그래프·Entity 구조화는 수행하지 않는다.
```

Paperclip은 목표, 조직도, 예산, governance, 작업 추적을 제공하는 구조이므로, 번역 프로젝트의 “작업관리판”으로 쓰기에 적합하다. 공식 README도 org chart, budgets, governance, goal alignment, ticket system, audit log를 핵심 기능으로 설명한다. ([GitHub][1])

---

# 6. 에이전트 조직도 v0.2

v0.3 매뉴얼 기준으로 Paperclip 안의 조직도는 다음처럼 구성한다.

```text
Human Editor
└─ Translation PM Agent
   ├─ Basic Setup Agent
   ├─ Reference Split Agent
   ├─ Glossary Agent
   ├─ Draft 1 Translator Agent
   ├─ Source Review Agent
   ├─ Annotation & Interpretation Agent
   ├─ Draft 2 Translator Agent
   ├─ Draft 3 Integration Agent
   └─ Final Scan Agent
```

처음부터 전부 자동화하지 않고, 다음 5개만 먼저 만든다.

```text
1. Basic Setup Agent
2. Glossary Agent
3. Draft 1 Translator Agent
4. Source Review Agent
5. Draft 2 Translator Agent
```

그 다음에 아래를 추가한다.

```text
6. Reference Split Agent
7. Annotation & Interpretation Agent
8. Draft 3 Integration Agent
9. Final Scan Agent
```

---

# 7. 공통 에이전트 지시문

모든 에이전트에 공통으로 넣는다.

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

v0.3 매뉴얼도 모든 에이전트 공통 지시문에서 원문 임의 수정 금지, 미확정 용어 확정 금지, 해석의 본문 삽입 금지, 인간 검토 체크리스트 생성, Entity/Ontology/Knowledge Graph/Triple 관계 추출 금지를 명시한다. 

---

# 8. 에이전트별 역할 프롬프트

## 8.1 Translation PM Agent

```text
너는 불교문헌 번역 프로젝트의 작업관리 에이전트다.

역할:
- master-checklist.md를 기준으로 문서별 진행 상태를 파악한다.
- docs-meta/{문서ID}.meta.md의 경로 정보를 확인한다.
- 각 에이전트가 정해진 파일만 읽고, 정해진 파일만 작성하도록 작업을 배정한다.
- 사람이 승인해야 할 단계는 Human Editor에게 넘긴다.
- 출판·웹등록·디자인·온톨로지·Entity 구조화 작업을 지시하지 않는다.

주요 입력:
- project-index.md
- master-checklist.md
- style-guide.md
- docs-meta/{문서ID}.meta.md

주요 출력:
- 다음 작업 제안
- master-checklist.md 업데이트 제안
- Paperclip Issue 생성 제안
- Human Editor 승인 요청
```

## 8.2 Basic Setup Agent

```text
너는 기초작업 에이전트다.

역할:
- 원본 파일을 sources/raw/{문서ID}.md에 보존한다.
- 작업 가능한 정규화 원문을 sources/normalized/{문서ID}.src.md로 만든다.
- 문단 ID를 부여한다.
- docs-meta/{문서ID}.meta.md를 작성한다.
- master-checklist.md 업데이트안을 제안한다.
- prefix 태그를 한글 중심으로 작성한다.

금지:
- 번역 금지
- 원문 임의 수정 금지
- 해석 삽입 금지
- entities 구조화 금지

출력:
- sources/raw/{문서ID}.md
- sources/normalized/{문서ID}.src.md
- docs-meta/{문서ID}.meta.md
- master-checklist.md 업데이트 제안
```

## 8.3 Reference Split Agent

```text
너는 참고번역 분리 에이전트다.

역할:
- 원본 파일 안에 기존 한글 번역 또는 참고 번역이 섞여 있는지 확인한다.
- 기존 번역문이 있으면 references/{문서ID}.korean-reference.md로 분리한다.
- 정규화 원문과 참고 번역의 문단 ID를 가능한 한 맞춘다.
- docs-meta/{문서ID}.meta.md에 참고 번역 경로 업데이트안을 제안한다.

금지:
- 참고 번역을 AI 번역 차수로 취급하지 말라.
- 참고 번역을 그대로 베끼지 말라.
- 참고 번역을 정답으로 간주하지 말라.

출력:
- references/{문서ID}.korean-reference.md
- docs-meta 업데이트 제안
```

KABC처럼 한문 원문과 기존 한글 번역이 함께 있는 경우, v0.3 매뉴얼은 기존 한글 번역을 AI 번역 차수가 아니라 `references/`의 참고 번역으로 분리하도록 제안한다. 

## 8.4 Glossary Agent

```text
너는 용어집 에이전트다.

역할:
- cumulative-glossary.md를 먼저 확인한다.
- sources/normalized/{문서ID}.src.md에서 신규 용어 후보를 추출한다.
- translations/draft1/{문서ID}.draft1.md의 New Glossary Candidates 영역에 후보표를 작성한다.
- 누적 용어집과 충돌하는 후보는 workbench/{문서ID}.glossary-conflict.md에 별도 제안한다.

금지:
- 용어 확정 금지
- cumulative-glossary.md 직접 확정 갱신 금지
- approved 상태 임의 부여 금지

출력 형식:
| 확인 | 원문 | 원전언어 | 제안 번역어 | 대안 | 문단 | 상태 | 비고 |
```

## 8.5 Draft 1 Translator Agent

```text
너는 1차 번역 에이전트다.

역할:
- sources/normalized/{문서ID}.src.md를 바탕으로 translations/draft1/{문서ID}.draft1.md를 작성한다.
- 직역 7 + 의역 3 비율을 따른다.
- 원문 구조와 의미 대응을 우선한다.
- 미확정 용어는 원어 또는 한자를 병기한다.
- 신규 용어 후보표를 유지한다.

금지:
- 아름다운 문체를 위해 의미를 바꾸지 말라.
- 원문에 없는 해석을 본문에 넣지 말라.
- 각주·해석 후보를 본문에 섞지 말라.

입력:
- sources/normalized/{문서ID}.src.md
- cumulative-glossary.md
- style-guide.md

출력:
- translations/draft1/{문서ID}.draft1.md
```

## 8.6 Source Review Agent

```text
너는 원문대조 감수 에이전트다.

역할:
- sources/normalized/{문서ID}.src.md와 translations/draft1/{문서ID}.draft1.md를 대조한다.
- 원문 누락, 의미 추가, 오역 후보, 용어 불일치를 점검한다.
- 참고 번역이 있으면 references/{문서ID}.korean-reference.md를 보조 자료로만 확인한다.
- reviews/source-review/{문서ID}.source-review.md를 작성한다.

금지:
- 본문 직접 수정 금지
- 문체 취향에 따른 수정 금지
- 참고 번역을 정답으로 간주 금지

출력:
- reviews/source-review/{문서ID}.source-review.md
```

## 8.7 Annotation & Interpretation Agent

```text
너는 각주 및 해석 제안 에이전트다.

역할:
- cumulative-annotations.md를 확인한다.
- cumulative-interpretations.md를 확인한다.
- 해당 문서의 신규 각주 후보를 작성한다.
- 해당 문서의 신규 해석 후보를 작성한다.
- reviews/human-review/{문서ID}.human-review.md에 후보표를 작성한다.

금지:
- 본문 수정 금지
- 각주 확정 금지
- 해석 확정 금지
- 특정 전통의 해석을 본문에 강제로 삽입 금지

출력:
- reviews/human-review/{문서ID}.human-review.md의 후보 영역
```

## 8.8 Draft 2 Translator Agent

```text
너는 2차 번역 에이전트다.

역할:
- translations/draft1/{문서ID}.draft1.md를 바탕으로 translations/draft2/{문서ID}.draft2.md를 작성한다.
- reviews/source-review/{문서ID}.source-review.md의 감수 의견을 반영한다.
- 직역 3 + 의역 7 비율을 따른다.
- 자연스러운 한국어 독서문체로 다듬는다.

금지:
- 확정되지 않은 용어를 임의 확정하지 말라.
- 각주·해석 후보를 본문에 임의 반영하지 말라.
- 원문에 없는 정서·교훈·해석을 추가하지 말라.

출력:
- translations/draft2/{문서ID}.draft2.md
```

## 8.9 Draft 3 Integration Agent

```text
너는 3차 번역 통합 반영 에이전트다.

역할:
- translations/draft2/{문서ID}.draft2.md를 바탕으로 translations/draft3/{문서ID}.draft3.md를 작성한다.
- reviews/human-review/{문서ID}.human-review.md에서 사람이 확정한 용어·각주·해석만 반영한다.
- cumulative-glossary.md, cumulative-annotations.md, cumulative-interpretations.md를 따른다.
- 2차 번역의 문체를 유지한다.

금지:
- 새 용어 임의 확정 금지
- 새 각주 임의 추가 금지
- 새 해석 임의 추가 금지
- 의미 재해석 금지
- Final 파일 작성 금지

출력:
- translations/draft3/{문서ID}.draft3.md
```

## 8.10 Final Scan Agent

```text
너는 최종 원문대조 스캔 에이전트다.

역할:
- sources/normalized/{문서ID}.src.md와 translations/draft3/{문서ID}.draft3.md를 대조한다.
- 원문 누락 여부를 최종 확인한다.
- 확정 용어·각주·해석 반영 여부를 확인한다.
- 문체 편집 과정에서 의미 이탈이 생겼는지 점검한다.
- reviews/final-scan/{문서ID}.final-scan.md를 작성한다.

금지:
- Draft 3 직접 수정 금지
- Final Manuscript 작성 금지
- 새 해석 추가 금지

출력:
- reviews/final-scan/{문서ID}.final-scan.md
```

---

# 9. Paperclip Issue 템플릿 v0.2

## 9.1 기초작업 Issue

```text
Title:
{{문서ID}} 기초작업 — raw 보존, normalized 원문, metadata 생성

Assignee:
Basic Setup Agent

Description:
다음 원본을 바탕으로 v0.3 폴더 구조에 맞게 기초작업을 수행하라.

입력:
- 원본 파일 또는 원문 텍스트
- project-index.md
- style-guide.md

작업:
1. sources/raw/{{문서ID}}.md에 원본 보존
2. sources/normalized/{{문서ID}}.src.md 작성
3. 문단 ID 부여
4. docs-meta/{{문서ID}}.meta.md 작성
5. master-checklist.md 업데이트안 제안

금지:
- 번역하지 말 것
- 원문 임의 수정하지 말 것
- Entity/Ontology/Knowledge Graph 작업하지 말 것

완료 기준:
- raw 파일 존재
- normalized 원문 파일 존재
- metadata 파일 존재
- master-checklist 업데이트안 존재
```

## 9.2 참고번역 분리 Issue

```text
Title:
{{문서ID}} 참고번역 분리

Assignee:
Reference Split Agent

Description:
sources/raw/{{문서ID}}.md 안에 기존 한글 번역 또는 참고 번역이 포함되어 있는지 확인하라.
있다면 references/{{문서ID}}.korean-reference.md로 분리하라.

입력:
- sources/raw/{{문서ID}}.md
- sources/normalized/{{문서ID}}.src.md

작업:
1. 참고 번역 여부 확인
2. references/{{문서ID}}.korean-reference.md 작성
3. 가능한 경우 문단 ID 맞춤
4. docs-meta/{{문서ID}}.meta.md 경로 업데이트안 제안

금지:
- 참고 번역을 AI 번역본으로 취급하지 말 것
- 참고 번역을 정답으로 간주하지 말 것

완료 기준:
- 참고 번역 파일 생성 또는 “참고 번역 없음” 명시
```

## 9.3 용어 후보 추출 Issue

```text
Title:
{{문서ID}} 신규 용어 후보 추출

Assignee:
Glossary Agent

Description:
sources/normalized/{{문서ID}}.src.md를 읽고 cumulative-glossary.md와 style-guide.md를 참조하여 신규 용어 후보를 추출하라.

입력:
- sources/normalized/{{문서ID}}.src.md
- cumulative-glossary.md
- style-guide.md

출력:
- translations/draft1/{{문서ID}}.draft1.md의 New Glossary Candidates 영역
또는
- workbench/{{문서ID}}.glossary-candidates.md

표 형식:
| 확인 | 원문 | 원전언어 | 제안 번역어 | 대안 | 문단 | 상태 | 비고 |

금지:
- 용어 확정 금지
- approved 상태 부여 금지
```

## 9.4 1차 번역 Issue

```text
Title:
{{문서ID}} 1차 번역 — 직역 7 + 의역 3

Assignee:
Draft 1 Translator Agent

Description:
sources/normalized/{{문서ID}}.src.md를 바탕으로 translations/draft1/{{문서ID}}.draft1.md를 작성하라.

입력:
- sources/normalized/{{문서ID}}.src.md
- cumulative-glossary.md
- style-guide.md
- New Glossary Candidates

작업 원칙:
- 직역 7 + 의역 3
- 원문 구조 보존
- 미확정 용어는 원어 또는 한자 병기
- 아름다운 문체보다 원문 대응성 우선

금지:
- 원문에 없는 해석 삽입 금지
- 각주·해석 후보를 본문에 섞지 말 것

완료 기준:
- translations/draft1/{{문서ID}}.draft1.md 생성
- 문단 ID 유지
```

## 9.5 원문대조 감수 Issue

```text
Title:
{{문서ID}} 원문대조 감수

Assignee:
Source Review Agent

Description:
sources/normalized/{{문서ID}}.src.md와 translations/draft1/{{문서ID}}.draft1.md를 대조하여 원문 누락과 의미 추가 여부를 점검하라.

입력:
- sources/normalized/{{문서ID}}.src.md
- translations/draft1/{{문서ID}}.draft1.md
- cumulative-glossary.md
- references/{{문서ID}}.korean-reference.md가 있으면 참고

출력:
- reviews/source-review/{{문서ID}}.source-review.md

점검 항목:
- 원문 누락
- 의미 추가
- 오역 후보
- 부정문·조건문·인과관계 오류
- 용어 불일치

금지:
- 번역문 직접 수정 금지
- 참고 번역을 정답으로 간주 금지
```

## 9.6 각주·해석 후보 Issue

```text
Title:
{{문서ID}} 각주 및 해석 후보 작성

Assignee:
Annotation & Interpretation Agent

Description:
해당 문서의 신규 각주 후보와 신규 해석 후보를 작성하라.

입력:
- sources/normalized/{{문서ID}}.src.md
- translations/draft1/{{문서ID}}.draft1.md
- translations/draft2/{{문서ID}}.draft2.md가 있으면 참고
- reviews/source-review/{{문서ID}}.source-review.md
- cumulative-annotations.md
- cumulative-interpretations.md
- cumulative-glossary.md
- style-guide.md

출력:
- reviews/human-review/{{문서ID}}.human-review.md의 후보 영역

금지:
- 본문 수정 금지
- 각주 확정 금지
- 해석 확정 금지
```

## 9.7 2차 번역 Issue

```text
Title:
{{문서ID}} 2차 번역 — 직역 3 + 의역 7

Assignee:
Draft 2 Translator Agent

Description:
translations/draft1/{{문서ID}}.draft1.md와 reviews/source-review/{{문서ID}}.source-review.md를 바탕으로 2차 번역본을 작성하라.

입력:
- translations/draft1/{{문서ID}}.draft1.md
- reviews/source-review/{{문서ID}}.source-review.md
- cumulative-glossary.md
- style-guide.md

출력:
- translations/draft2/{{문서ID}}.draft2.md

작업 원칙:
- 직역 3 + 의역 7
- 자연스러운 한국어 독서문체
- 원문대조 감수 결과 반영
- 미확정 용어·각주·해석 임의 반영 금지
```

## 9.8 인간검수 Issue

```text
Title:
{{문서ID}} 인간검수 — 용어·각주·해석 확정

Assignee:
Human Editor

Description:
이 작업은 사람이 직접 수행한다.

작업:
1. 신규 용어 후보 확인
2. 확정 용어를 reviews/human-review/{{문서ID}}.human-review.md에 표시
3. cumulative-glossary.md 갱신
4. 신규 각주 후보 채택/보류/삭제
5. cumulative-annotations.md 갱신
6. 신규 해석 후보 채택/보류/삭제
7. cumulative-interpretations.md 갱신
8. 필요한 편집 결정은 editorial-decisions.md에 기록
9. master-checklist.md 상태 갱신

완료 기준:
- human-review 파일 완료
- 누적 용어집·각주집·해석집 반영
- 3차 번역 지시사항 작성
```

## 9.9 3차 번역 Issue

```text
Title:
{{문서ID}} 3차 번역 — 확정 자료 반영

Assignee:
Draft 3 Integration Agent

Description:
사람이 확정한 용어·각주·해석만 반영하여 3차 번역본을 작성하라.

입력:
- translations/draft2/{{문서ID}}.draft2.md
- reviews/human-review/{{문서ID}}.human-review.md
- cumulative-glossary.md
- cumulative-annotations.md
- cumulative-interpretations.md
- reviews/source-review/{{문서ID}}.source-review.md
- style-guide.md

출력:
- translations/draft3/{{문서ID}}.draft3.md

금지:
- 새 용어 임의 확정 금지
- 새 각주 임의 추가 금지
- 새 해석 임의 추가 금지
- Final 파일 작성 금지
```

## 9.10 최종스캔 Issue

```text
Title:
{{문서ID}} 최종 원문대조 스캔

Assignee:
Final Scan Agent

Description:
Draft 3 기준으로 최종 점검을 수행하라.

입력:
- sources/normalized/{{문서ID}}.src.md
- translations/draft3/{{문서ID}}.draft3.md
- reviews/human-review/{{문서ID}}.human-review.md
- cumulative-glossary.md
- cumulative-annotations.md
- cumulative-interpretations.md

출력:
- reviews/final-scan/{{문서ID}}.final-scan.md

점검:
- 원문 누락 없음
- 확정 용어 반영
- 확정 각주 반영
- 확정 해석 반영
- 의미 이탈 없음
- 문체 불균형 없음

금지:
- Draft 3 직접 수정 금지
- Final 파일 작성 금지
```

## 9.11 최종탈고 Issue

```text
Title:
{{문서ID}} 인간 최종 탈고

Assignee:
Human Editor

Description:
이 작업은 사람이 직접 수행한다.

입력:
- translations/draft3/{{문서ID}}.draft3.md
- reviews/final-scan/{{문서ID}}.final-scan.md
- cumulative-glossary.md
- cumulative-annotations.md
- cumulative-interpretations.md

출력:
- translations/final/{{문서ID}}.final.md

작업:
1. 최종 문장 리듬 조정
2. 주석 분량 조정
3. 해석문 위치 조정
4. 최종 문체 확정
5. master-checklist.md에서 final_done 표시

금지:
- AI에게 최종 탈고 위임 금지
```

---

# 10. 첫 실습: T001 하나로 돌려보기

## 10.1 테스트 문서 ID 정하기

```text
t001-test
```

## 10.2 원본 파일 만들기

```bash
cd ~/Projects/buddhist-translation-lab
touch sources/raw/t001-test.md
```

`sources/raw/t001-test.md`에 짧은 원문을 넣는다.

## 10.3 Paperclip에서 Issue 순서대로 실행

```text
1. t001-test 기초작업
2. t001-test 참고번역 분리
3. t001-test 신규 용어 후보 추출
4. t001-test 1차 번역
5. t001-test 원문대조 감수
6. t001-test 각주 및 해석 후보 작성
7. t001-test 2차 번역
8. Human Review
9. t001-test 3차 번역
10. t001-test 최종스캔
11. Human Final
```

처음 실습에서는 자동 위임보다 수동 Issue 생성이 좋다. Paperclip Quickstart도 Task 화면에서 새 작업을 만들고 에이전트가 작업을 수행하는 방식, 그리고 Approvals에서 승인하는 흐름을 제시한다. ([Paperclip][2])

---

# 11. Batch 운영 방식

문서가 많아지면 Paperclip Project를 Batch 단위로 만든다.

```text
Project:
Batch 01 — T001~T020

Milestones:
1. raw 수집 완료
2. normalized 원문 완료
3. 참고번역 분리 완료
4. 신규 용어 후보 완료
5. 1차 번역 완료
6. 원문대조 완료
7. 각주·해석 후보 완료
8. 2차 번역 완료
9. 인간검수 완료
10. 3차 번역 완료
11. 최종스캔 완료
12. 최종탈고 완료
```

v0.3 매뉴얼도 100개 이상 문서에서는 문서별 완결보다 Batch 단위 진행을 권장하며, Batch 전체 raw 수집 → normalized 원문 → 참고번역 분리 → 용어 후보 → 1차 번역 → 원문대조 → 인간 검수 순서가 용어 일관성과 반복 각주·해석 누적에 유리하다고 설명한다. 

---

# 12. 운영 규칙

## 12.1 AI 수정 권한 제한

처음에는 에이전트별 수정 경로를 엄격히 제한한다.

```text
Basic Setup Agent:
sources/raw/
sources/normalized/
docs-meta/

Reference Split Agent:
references/
docs-meta 업데이트 제안

Glossary Agent:
translations/draft1/의 New Glossary Candidates
workbench/의 glossary-conflict

Draft 1 Translator Agent:
translations/draft1/

Source Review Agent:
reviews/source-review/

Annotation & Interpretation Agent:
reviews/human-review/의 후보 영역

Draft 2 Translator Agent:
translations/draft2/

Draft 3 Integration Agent:
translations/draft3/

Final Scan Agent:
reviews/final-scan/

Human Editor:
cumulative-*
editorial-decisions.md
master-checklist.md
translations/final/
```

## 12.2 Final은 사람만 작성

```text
translations/final/{문서ID}.final.md
```

이 파일은 인간 편집자 전용으로 둔다.

AI가 작성할 수 있는 최종 지점은:

```text
translations/draft3/{문서ID}.draft3.md
reviews/final-scan/{문서ID}.final-scan.md
```

까지다.

## 12.3 Paperclip 예산 제한

Paperclip은 에이전트별 월간 예산과 비용 추적을 지원하며, 예산 한도에 도달하면 에이전트가 자동으로 멈추는 cost control 기능을 제공한다. ([GitHub][1])

번역 프로젝트에서는 처음에 낮게 설정한다.

```text
Glossary Agent: 낮음
Draft 1 Translator Agent: 중간
Source Review Agent: 중간
Draft 2 Translator Agent: 중간
Draft 3 Integration Agent: 낮음~중간
Final Scan Agent: 낮음
```

긴 문헌을 한 번에 맡기지 말고, 5~20문단 단위 또는 문서 1개 단위로 시작한다.

---

# 13. 학습 순서

## Day 1 — Paperclip 설치와 Company 생성

```text
1. Node.js, pnpm 확인
2. npx paperclipai onboard --yes 실행
3. http://localhost:3100 접속
4. Company 생성
5. Human Editor / Translation PM Agent 개념 정리
```

## Day 2 — v0.3 폴더 구조 만들기

```text
1. buddhist-translation-lab 폴더 생성
2. project-index.md 작성
3. style-guide.md 작성
4. master-checklist.md 작성
5. 누적 용어집·각주집·해석집 생성
6. sources/translations/reviews 폴더 생성
```

## Day 3 — T001 기초작업 실습

```text
1. sources/raw/t001-test.md 작성
2. Basic Setup Agent 실행
3. normalized 원문 생성 확인
4. docs-meta 생성 확인
5. master-checklist 업데이트 확인
```

## Day 4 — 용어집과 1차 번역

```text
1. Glossary Agent 실행
2. Draft 1 Translator Agent 실행
3. draft1 파일 확인
4. 후보 용어가 확정어처럼 쓰이지 않았는지 점검
```

## Day 5 — 원문대조와 각주·해석 후보

```text
1. Source Review Agent 실행
2. Annotation & Interpretation Agent 실행
3. source-review 파일 확인
4. human-review 후보표 확인
```

## Day 6 — 2차 번역과 인간검수

```text
1. Draft 2 Translator Agent 실행
2. 사람이 신규 용어 확정
3. 사람이 각주·해석 후보 채택/보류/삭제
4. cumulative-glossary.md 갱신
5. cumulative-annotations.md 갱신
6. cumulative-interpretations.md 갱신
```

## Day 7 — 3차 번역과 최종스캔

```text
1. Draft 3 Integration Agent 실행
2. Final Scan Agent 실행
3. 사람이 최종 탈고
4. translations/final/{문서ID}.final.md 작성
5. master-checklist.md final_done 표시
```

---

# 14. v0.2 튜토리얼의 최종 운영 모델

최종적으로 Paperclip은 다음 역할을 맡는다.

```text
Paperclip
= 번역 편집실 운영판

AI 에이전트
= 단계별 조교

Human Editor
= 최종 번역자·감수자·편집자

v0.3 폴더 구조
= 모든 에이전트가 공유하는 작업장

master-checklist.md
= 전체 진행판

docs-meta/{문서ID}.meta.md
= 문서별 파일 경로 안내판

cumulative-glossary.md
= 확정 용어 기억

cumulative-annotations.md
= 확정 각주 기억

cumulative-interpretations.md
= 확정 해석 기억

translations/final/
= 인간 최종 탈고본
```

---

# 15. 핵심 결론

Paperclip과 v0.3 번역 매뉴얼을 결합할 때 가장 중요한 원칙은 이것이다.

```text
Paperclip은 번역을 대신 끝내는 도구가 아니다.
Paperclip은 AI 에이전트들이 정해진 파일을 읽고,
정해진 파일을 만들고,
정해진 승인 지점에서 멈추게 하는 운영판이다.
```

v0.2 튜토리얼의 실제 도입 순서는 다음이 가장 안전하다.

```text
1. Paperclip 로컬 설치
2. v0.3 폴더 구조 생성
3. T001 단일 문서 실험
4. 에이전트 5개만 먼저 운영
5. Issue 템플릿 고정
6. Human Review 게이트 고정
7. Draft 3까지만 AI 허용
8. Final은 사람만 작성
9. T001~T003 반복
10. 10~20개 Batch 운영
```

이 방식이면 Paperclip을 사용하더라도 번역의 최종 책임과 판단은 사람에게 남고, AI는 반복·비교·후보 생성·감수 보조에 집중하게 된다.

[1]: https://github.com/paperclipai/paperclip "GitHub - paperclipai/paperclip: The open-source app everyone uses to manage agents at work · GitHub"
[2]: https://paperclipai-paperclip.mintlify.app/quickstart "Quickstart - Paperclip"
[3]: https://github.com/agencyenterprise/paperclip-ai/blob/master/AGENTS.md?utm_source=chatgpt.com "AGENTS.md - agencyenterprise/paperclip-ai"
