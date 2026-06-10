# Paperclip과 번역 프로젝트 튜토리얼 v0.3

## Translation Director + A/B Manager 운영 구조

**문서명:** Paperclip과 번역 프로젝트 튜토리얼  
**버전:** v0.3  
**기준 매뉴얼:** 문헌 번역 AI 협업 워크플로우 매뉴얼 v0.3  
**목적:** Paperclip을 이용해 불교문헌 번역용 AI 다중 에이전트 작업환경을 실제로 구축·운영하는 방법 안내  
**핵심 변경:** 단일 Translation PM 구조를 `Translation Director + A/B Manager` 구조로 개편  
**범위:** 설치, 프로젝트 폴더 구성, 에이전트 조직도, Issue 템플릿, Batch 운영, 2차 자동 생산 모드, 3차 확정 모드  
**제외:** 출판, 웹 등록, 디자인, 온톨로지, 지식그래프, Entity 구조화

---

# 0. v0.3 튜토리얼의 핵심 변경점

v0.2 튜토리얼은 `Translation PM Agent` 1명이 전체 작업을 관리하는 구조였다. 이 구조는 단일 문서 실습이나 소규모 작업에는 충분하지만, 실제 운영에서 다음 문제가 생긴다.

```text
사용자가 오늘 10개 문헌을 2차 번역까지 완료하라고 지시하면,
문서별 작업을 draft2_done까지 밀어주는 생산관리 역할이 필요하다.

그러나 draft2_done 이후에는 인간검수, 용어 확정, 각주 확정, 해석 확정,
3차 번역 반영, 최종스캔 관리가 필요하다.

이 두 업무는 성격이 다르다.
하나는 생산관리이고, 다른 하나는 확정관리이다.
```

따라서 v0.3에서는 Paperclip 조직도를 다음처럼 바꾼다.

```text
Human Editor / 사용자
└─ Translation Director Agent
   ├─ Draft Production Manager Agent
   │  └─ A. 2차 자동 생산 모드 관리
   └─ Editorial Confirmation Manager Agent
      └─ B. 3차 확정 모드 관리
```

핵심 원칙은 다음이다.

```text
A 매니저는 많은 문서를 안전하게 2차까지 올린다.
B 매니저는 사람이 확정한 판단만 정확히 3차 이후에 반영시킨다.
Translation Director는 A와 B의 균형을 조정한다.
Human Editor는 용어·각주·해석·최종 문체의 최종 판단권을 가진다.
```

---

# 1. Paperclip의 역할

Paperclip은 번역 AI 자체가 아니다. Paperclip은 여러 AI 에이전트를 “회사 조직”처럼 관리하는 오픈소스 오케스트레이션 도구다. Paperclip 공식 README는 Paperclip을 “AI agent team을 위한 open-source orchestration”으로 설명하고, OpenClaw가 직원이라면 Paperclip은 회사라고 비유한다.[^paperclip-github]

번역 프로젝트에서는 다음처럼 대응시킨다.

```text
Paperclip Company
= 불교문헌 번역 편집실

Company Goal
= 특정 문헌군의 번역·감수·탈고 완료

Org Chart
= Human Editor, Translation Director, A/B Manager, 단계별 작업 에이전트

Ticket / Issue
= 특정 문서의 특정 단계 작업

Approval / Governance
= 인간 편집자의 승인·확정·보류·반려

Budget
= 에이전트별 토큰·비용 제한

Dashboard / Audit Log
= 전체 번역 프로젝트 진행판과 작업 기록
```

Paperclip은 Bring Your Own Agent 방식이다. 즉 Paperclip 설치만으로 번역 에이전트가 자동 생성되는 것이 아니라, 실제 번역을 수행할 AI 런타임, 프롬프트, CLI, Codex, Claude Code, OpenClaw, Bash, HTTP agent 등을 연결해야 한다.[^paperclip-github]

따라서 OL 번역 프로젝트에서 Paperclip의 역할은 다음 한 문장으로 정리된다.

```text
Paperclip은 번역을 대신 끝내는 도구가 아니라,
번역 에이전트들이 정해진 파일을 읽고,
정해진 파일을 만들고,
정해진 승인 지점에서 멈추게 하는 운영판이다.
```

---

# 2. 설치 전 준비

## 2.1 필수 환경

Paperclip Quickstart는 Node.js 20 이상과 pnpm 9.15 이상을 전제로 안내한다.[^paperclip-quickstart]

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

## 2.2 권장 작업 환경

```text
운영체제: macOS, Linux, Windows WSL 권장
편집기: VS Code
버전관리: Git
작업 폴더: ~/Projects/buddhavamsa-translation-lab
AI 실행 주체: Codex CLI, Claude Code, OpenClaw, Cursor, Bash/HTTP agent 등
```

초기에는 Paperclip 전체 자동화를 목표로 하지 말고, **T001 단일 문서 실습 → 3개 문서 반복 → 10개 문서 Batch** 순서로 늘린다.

---

# 3. Paperclip 설치

## 3.1 Quickstart 설치

```bash
npx paperclipai onboard --yes
```

Quickstart 문서는 이 명령으로 기본 설정을 만들고, embedded PostgreSQL과 로컬 파일 저장소를 설정하며, Paperclip 서버를 시작하는 흐름을 안내한다.[^paperclip-quickstart]

브라우저 접속:

```text
http://localhost:3100
```

## 3.2 저장소 직접 설치

```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev
```

## 3.3 기본 점검

```bash
curl http://localhost:3100/api/health
```

문제가 생기면:

```bash
paperclipai doctor
```

---

# 4. 번역 프로젝트 폴더 만들기

v0.3 튜토리얼은 번역 매뉴얼 v0.3의 폴더 구조에 다음 네 종류의 운영 폴더를 추가한다.

```text
batch-plans/
batch-reports/
queues/
manager-logs/
```

전체 구조는 다음과 같다.

```bash
mkdir -p ~/Projects/buddhavamsa-translation-lab
cd ~/Projects/buddhavamsa-translation-lab

mkdir -p docs-meta
mkdir -p sources/raw sources/normalized
mkdir -p references
mkdir -p translations/draft1 translations/draft2 translations/draft3 translations/final
mkdir -p reviews/source-review reviews/human-review reviews/final-scan
mkdir -p workbench
mkdir -p batch-plans batch-reports
mkdir -p queues
mkdir -p manager-logs/draft-production manager-logs/editorial-confirmation manager-logs/director

touch project-index.md
touch master-checklist.md
touch style-guide.md
touch editorial-decisions.md
touch cumulative-glossary.md
touch cumulative-annotations.md
touch cumulative-interpretations.md

touch queues/today-queue.md
touch queues/human-review-queue.md
touch queues/hold-queue.md
touch queues/error-queue.md
touch queues/final-ready-queue.md
```

결과 구조:

```text
buddhavamsa-translation-lab/
├─ project-index.md
├─ master-checklist.md
├─ style-guide.md
├─ editorial-decisions.md
├─ cumulative-glossary.md
├─ cumulative-annotations.md
├─ cumulative-interpretations.md
│
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
├─ workbench/
│
├─ batch-plans/
├─ batch-reports/
├─ queues/
│  ├─ today-queue.md
│  ├─ human-review-queue.md
│  ├─ hold-queue.md
│  ├─ error-queue.md
│  └─ final-ready-queue.md
└─ manager-logs/
   ├─ draft-production/
   ├─ editorial-confirmation/
   └─ director/
```

---

# 5. Paperclip Company 만들기

Paperclip UI에서 새 Company를 만든다.

## 5.1 Company 이름

```text
Buddhist Translation Desk
```

또는:

```text
불교문헌 번역 편집실
```

## 5.2 Company Goal

```text
불교 경전·논서·주석서·전기문헌을 원문 보존, 용어 일관성,
원문대조 감수, 각주·해석 검토, 인간 최종 탈고 원칙에 따라 번역한다.

AI 에이전트는 초안 작성, 후보 제안, 누락 검사, 문체 편집 보조,
Batch 진행 관리, 확정 반영 점검을 담당한다.

최종 용어 확정, 각주 확정, 해석 확정, 최종 원고 탈고는 인간 편집자가 수행한다.

이번 프로젝트에서는 텍스트 번역과 원고 탈고에 집중하며,
출판·웹 등록·디자인·온톨로지·지식그래프·Entity 구조화는 수행하지 않는다.
```

## 5.3 Governance 원칙

```text
1. AI는 draft2_done까지 자동 생산할 수 있다.
2. 인간검수 없이 draft3_done으로 넘어가지 않는다.
3. 신규 용어·각주·해석 확정권은 Human Editor에게 있다.
4. Final Manuscript는 Human Editor 전용 산출물이다.
5. Production 속도보다 원문 누락 방지가 우선이다.
6. 확정관리 단계에서는 사람의 결정만 반영한다.
```

---

# 6. 에이전트 조직도 v0.3

## 6.1 최종 권장 조직도

```text
Human Editor
└─ Translation Director Agent
   ├─ Draft Production Manager Agent
   │  ├─ Basic Setup Agent
   │  ├─ Reference Split Agent
   │  ├─ Glossary Agent
   │  ├─ Draft 1 Translator Agent
   │  ├─ Source Review Agent
   │  ├─ Annotation Candidate Agent
   │  └─ Draft 2 Translator Agent
   │
   └─ Editorial Confirmation Manager Agent
      ├─ Human Review Preparation Agent
      ├─ Draft 3 Integration Agent
      ├─ Final Scan Agent
      └─ Final Handoff Agent
```

## 6.2 단계적 도입 순서

처음부터 모든 에이전트를 활성화하지 않는다.

```text
1단계: Translation Director + Draft Production Manager만 활성화
2단계: T001~T003 실험 후 Editorial Confirmation Manager 활성화
3단계: 10개 문헌 Batch 운영 시 A/B 매니저 완전 분리
```

## 6.3 왜 두 매니저인가

```text
Draft Production Manager
= 생산관리자
= 많은 문서를 draft2_done까지 올리는 책임

Editorial Confirmation Manager
= 확정관리자
= 사람이 확정한 판단을 draft3/final-scan에 정확히 반영하는 책임
```

두 매니저를 분리하면 속도와 품질 통제가 서로 섞이지 않는다.

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

정해진 입력 파일만 읽고, 정해진 출력 경로에만 산출물을 만든다.
산출물 생성 후 master-checklist.md 업데이트안을 제안한다.
```

---

# 8. 매니저 에이전트 역할 프롬프트

## 8.1 Translation Director Agent

```text
너는 불교문헌 번역 프로젝트의 총괄 편집장 에이전트다.

역할:
- Draft Production Manager와 Editorial Confirmation Manager를 감독한다.
- 오늘의 운영 목표가 생산 중심인지, 검수 중심인지 판단한다.
- draft2_done 문서가 너무 많이 쌓이면 생산량을 줄인다.
- human-review-queue가 길어지면 확정관리 모드를 우선한다.
- 용어 충돌이 많아지면 신규 생산을 일시 중지하도록 지시한다.
- Paperclip Issue와 Batch 진행 상황을 전체 관점에서 보고한다.
- Human Editor에게 필요한 판단 요청을 간결하게 정리한다.

입력:
- project-index.md
- master-checklist.md
- batch-plans/
- batch-reports/
- queues/today-queue.md
- queues/human-review-queue.md
- queues/hold-queue.md
- queues/error-queue.md
- queues/final-ready-queue.md
- manager-logs/

출력:
- 오늘의 운영 판단
- A/B 매니저 우선순위 지시
- 사용자 보고문
- manager-logs/director/{날짜}.director-log.md

금지:
- 직접 번역하지 말 것
- 용어·각주·해석을 확정하지 말 것
- 인간검수 없이 3차 번역을 승인하지 말 것
- Final Manuscript를 작성하지 말 것
```

---

## 8.2 Draft Production Manager Agent

```text
너는 불교문헌 번역 프로젝트의 2차 자동 생산 모드 관리자다.

목표:
- 여러 문서를 draft2_done까지 안전하게 진행한다.

책임 범위:
- not_started
- raw_collected
- source_ready
- reference_ready
- glossary_candidate_done
- draft1_done
- source_review_done
- annotation_candidate_done
- draft2_done

역할:
- 사용자의 일일 목표를 batch plan으로 변환한다.
- master-checklist.md에서 오늘 처리 가능한 문서를 고른다.
- 각 문서의 현재 상태를 확인한다.
- Basic Setup, Reference Split, Glossary, Draft 1, Source Review, Annotation Candidate, Draft 2 Agent에게 작업을 배정한다.
- 각 단계의 출력 파일이 실제 생성되었는지 확인한다.
- 오류 문서는 hold-queue 또는 error-queue로 보낸다.
- draft2_done 문서는 human-review-queue로 넘긴다.
- batch report를 작성한다.

입력:
- master-checklist.md
- docs-meta/{문서ID}.meta.md
- project-index.md
- style-guide.md
- cumulative-glossary.md
- batch-plans/{날짜}-draft2-batch.md

출력:
- batch-reports/{날짜}-draft2-batch-report.md
- queues/human-review-queue.md 업데이트안
- queues/hold-queue.md 업데이트안
- queues/error-queue.md 업데이트안
- manager-logs/draft-production/{날짜}.draft-production-log.md

금지:
- 신규 용어 확정 금지
- 각주 확정 금지
- 해석 확정 금지
- draft3 실행 금지
- final 파일 작성 금지
- 목표 수량을 맞추기 위해 원문대조 생략 금지
```

---

## 8.3 Editorial Confirmation Manager Agent

```text
너는 불교문헌 번역 프로젝트의 3차 확정 모드 관리자다.

목표:
- draft2_done 문서를 인간검수 이후 draft3_done, final_scan_done까지 안정적으로 진행한다.

책임 범위:
- draft2_done
- human_review_done
- draft3_done
- final_scan_done
- final_ready

역할:
- human-review-queue에서 검수 대기 문서를 정리한다.
- 사람이 검토해야 할 신규 용어·각주·해석 후보를 요약한다.
- Human Editor가 확정한 판단만 확인한다.
- cumulative-glossary.md, cumulative-annotations.md, cumulative-interpretations.md 반영 여부를 점검한다.
- Draft 3 Integration Agent에게 3차 번역 작업을 배정한다.
- Final Scan Agent에게 최종 원문대조를 배정한다.
- final-ready 문서를 Human Editor에게 넘긴다.

입력:
- queues/human-review-queue.md
- reviews/human-review/{문서ID}.human-review.md
- translations/draft2/{문서ID}.draft2.md
- cumulative-glossary.md
- cumulative-annotations.md
- cumulative-interpretations.md
- editorial-decisions.md
- style-guide.md

출력:
- translations/draft3/{문서ID}.draft3.md 생성 지시
- reviews/final-scan/{문서ID}.final-scan.md 생성 지시
- queues/final-ready-queue.md 업데이트안
- batch-reports/{날짜}-confirmation-report.md
- manager-logs/editorial-confirmation/{날짜}.editorial-confirmation-log.md

금지:
- 사람 대신 용어 확정 금지
- 사람 대신 각주 채택 금지
- 사람 대신 해석 채택 금지
- draft2 내용을 임의로 재해석 금지
- final 원고를 독자적으로 확정 금지
```

---

# 9. 작업 에이전트 역할 프롬프트

## 9.1 Basic Setup Agent

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
```

## 9.2 Reference Split Agent

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
```

## 9.3 Glossary Agent

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
```

## 9.4 Draft 1 Translator Agent

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
```

## 9.5 Source Review Agent

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
```

## 9.6 Annotation Candidate Agent

```text
너는 각주 및 해석 후보 에이전트다.

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
```

## 9.7 Draft 2 Translator Agent

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
```

## 9.8 Human Review Preparation Agent

```text
너는 인간검수 준비 에이전트다.

역할:
- draft2_done 문서의 신규 용어 후보, 각주 후보, 해석 후보를 사람이 보기 좋게 정리한다.
- Human Editor가 확정해야 할 항목을 체크리스트로 만든다.
- 후보가 너무 많으면 우선순위를 제안한다.

출력:
- reviews/human-review/{문서ID}.human-review.md 정리안
- Human Editor 검수 요청 요약

금지:
- 후보를 확정하지 말 것
- cumulative-* 파일을 직접 확정 갱신하지 말 것
```

## 9.9 Draft 3 Integration Agent

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
```

## 9.10 Final Scan Agent

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
```

## 9.11 Final Handoff Agent

```text
너는 최종탈고 인계 에이전트다.

역할:
- final_scan_done 문서를 Human Editor에게 넘기기 위한 요약을 작성한다.
- final-scan에서 남은 문제를 정리한다.
- 최종 탈고 시 확인할 항목을 체크리스트로 만든다.
- queues/final-ready-queue.md 업데이트안을 작성한다.

금지:
- final 파일 작성 금지
- 최종 문체 확정 금지
- 인간 편집자의 판단 대체 금지
```

---

# 10. A. 2차 자동 생산 모드 운영법

## 10.1 사용자가 주는 명령 예시

```text
오늘 gcb 계열 문헌 10개를 draft2_done 상태까지 진행해줘.
source_ready 또는 draft1_done 상태 문서 중 우선순위 높은 문서를 골라.
오류가 있는 문서는 hold-queue로 넘기고,
완료된 문서는 human-review-queue로 넘겨.
마지막에 batch report를 작성해줘.
```

## 10.2 Draft Production Manager의 실행 흐름

```text
1. master-checklist.md 확인
2. 작업 가능한 문서 후보 목록 작성
3. 오늘의 목표 수량 결정
4. batch-plans/{날짜}-draft2-batch.md 작성
5. 문서별 현재 상태 확인
6. 필요한 하위 에이전트 배정
7. 각 단계 산출물 생성 확인
8. 오류 문서 분류
9. draft2_done 문서 human-review-queue 등록
10. batch-reports/{날짜}-draft2-batch-report.md 작성
```

## 10.3 Batch Plan 템플릿

경로:

```text
batch-plans/2026-06-05-draft2-batch.md
```

내용:

```markdown
# 2026-06-05 Draft2 Batch Plan

## 1. 목표

- 오늘 목표: 문헌 10개를 draft2_done까지 진행
- 대상 범위: gcb 계열 문헌
- 우선순위: source_ready > draft1_done > raw_collected

## 2. 대상 문서

| 순번 | doc_id | 현재 상태 | 목표 상태 | 비고 |
|---|---|---|---|---|
| 1 |  | source_ready | draft2_done |  |
| 2 |  | draft1_done | draft2_done |  |

## 3. 중단 조건

- 원문 구조 불명확
- 참고번역 분리 실패
- 원문대조에서 대량 누락 발견
- 용어 충돌 다수
- 문서가 너무 길어 추가 분할 필요

## 4. 완료 조건

- translations/draft2/{문서ID}.draft2.md 생성
- reviews/source-review/{문서ID}.source-review.md 생성
- reviews/human-review/{문서ID}.human-review.md 후보 영역 작성
- master-checklist.md 상태 draft2_done 업데이트안 작성
- queues/human-review-queue.md 등록
```

## 10.4 Batch Report 템플릿

경로:

```text
batch-reports/2026-06-05-draft2-batch-report.md
```

내용:

```markdown
# 2026-06-05 Draft2 Batch Report

## 1. 요약

- 목표 문서 수:
- draft2_done 완료:
- hold 처리:
- error 처리:
- human-review-queue 등록:

## 2. 완료 문서

| doc_id | 시작 상태 | 완료 상태 | 주요 이슈 | 다음 작업 |
|---|---|---|---|---|
|  | source_ready | draft2_done |  | 인간검수 |

## 3. 보류 문서

| doc_id | 보류 사유 | 필요한 조치 |
|---|---|---|
|  |  |  |

## 4. 오류 문서

| doc_id | 오류 내용 | 재시도 가능 여부 |
|---|---|---|
|  |  |  |

## 5. 인간 편집자 확인 필요

- 신규 용어 충돌:
- 각주 후보 과다:
- 해석 후보 주의:
- 문서 분할 필요:
```

---

# 11. B. 3차 확정 모드 운영법

## 11.1 사용자가 주는 명령 예시

```text
human-review-queue에 있는 문서 중 3개를 골라
내가 확정한 용어·각주·해석만 반영하여 draft3_done까지 진행해줘.
최종스캔까지 마치고 final-ready-queue로 넘겨줘.
```

또는:

```text
이제 gcb-094-39b 문서의 인간검수 결과를 반영해서
3차 번역과 최종스캔까지 진행해줘.
확정되지 않은 후보는 반영하지 마.
```

## 11.2 Editorial Confirmation Manager의 실행 흐름

```text
1. queues/human-review-queue.md 확인
2. reviews/human-review/{문서ID}.human-review.md 확인
3. Human Editor가 확정한 항목만 식별
4. 누적 용어집·각주집·해석집 반영 여부 확인
5. Draft 3 Integration Agent에 작업 배정
6. translations/draft3/{문서ID}.draft3.md 생성 확인
7. Final Scan Agent에 작업 배정
8. reviews/final-scan/{문서ID}.final-scan.md 생성 확인
9. 문제가 없으면 queues/final-ready-queue.md 등록
10. confirmation report 작성
```

## 11.3 Confirmation Report 템플릿

경로:

```text
batch-reports/2026-06-05-confirmation-report.md
```

내용:

```markdown
# 2026-06-05 Confirmation Report

## 1. 요약

- 처리 문서 수:
- draft3_done 완료:
- final_scan_done 완료:
- final-ready 등록:
- Human Editor 재확인 필요:

## 2. 처리 문서

| doc_id | human_review 상태 | draft3 | final_scan | 다음 작업 |
|---|---|---|---|---|
|  | 완료 | 완료 | 완료 | 인간 최종탈고 |

## 3. 반영된 확정 사항

| doc_id | 용어 | 각주 | 해석 | 비고 |
|---|---|---|---|---|
|  |  |  |  |  |

## 4. 미반영 사항

| doc_id | 항목 | 미반영 사유 |
|---|---|---|
|  |  | 확정되지 않음 |

## 5. 최종탈고 전 확인

- 문체 불균형:
- 원문대조 잔여 이슈:
- 주석 분량 조정 필요:
- 해석문 위치 조정 필요:
```

---

# 12. Queue 파일 운영법

## 12.1 today-queue.md

```markdown
# Today Queue

| 우선순위 | doc_id | 현재 상태 | 목표 상태 | 담당 매니저 | 비고 |
|---|---|---|---|---|---|
| 1 |  | source_ready | draft2_done | Draft Production Manager |  |
```

## 12.2 human-review-queue.md

```markdown
# Human Review Queue

| 등록일 | doc_id | draft2 파일 | 검수 필요 항목 | 우선순위 | 비고 |
|---|---|---|---|---|---|
| 2026-06-05 |  | translations/draft2/... | 용어 5, 각주 2 | 높음 |  |
```

## 12.3 hold-queue.md

```markdown
# Hold Queue

| 등록일 | doc_id | 보류 사유 | 필요한 조치 | 재개 조건 |
|---|---|---|---|---|
|  |  | 원문 구조 불명확 | 사람이 원문 확인 | source_ready 재작성 |
```

## 12.4 error-queue.md

```markdown
# Error Queue

| 등록일 | doc_id | 오류 단계 | 오류 내용 | 재시도 여부 |
|---|---|---|---|---|
|  |  | Draft 1 | 파일 경로 없음 | 가능 |
```

## 12.5 final-ready-queue.md

```markdown
# Final Ready Queue

| 등록일 | doc_id | draft3 | final-scan | 최종탈고 확인 항목 |
|---|---|---|---|---|
|  |  | translations/draft3/... | reviews/final-scan/... | 문체 리듬 조정 |
```

---

# 13. Paperclip Issue 템플릿 v0.3

## 13.1 Draft2 Batch 운영 Issue

```text
Title:
2026-06-05 Draft2 Batch — 문헌 10개 2차 자동 생산

Assignee:
Draft Production Manager Agent

Description:
오늘의 목표는 master-checklist.md에서 작업 가능한 문헌 10개를 골라 draft2_done까지 진행하는 것이다.

입력:
- master-checklist.md
- project-index.md
- style-guide.md
- cumulative-glossary.md
- docs-meta/

작업:
1. batch-plans/2026-06-05-draft2-batch.md 작성
2. 대상 문서 10개 선정
3. 문서별 현재 상태 확인
4. 필요한 하위 에이전트에게 작업 배정
5. draft2 산출물 생성 확인
6. hold/error 문서 분류
7. human-review-queue 등록
8. batch report 작성

완료 기준:
- batch plan 존재
- 완료 문서가 draft2_done 상태로 정리됨
- human-review-queue 업데이트안 존재
- batch report 존재

금지:
- 인간검수 없이 draft3 진행 금지
- 용어·각주·해석 확정 금지
- 원문대조 생략 금지
```

## 13.2 Human Review Preparation Issue

```text
Title:
{{문서ID}} 인간검수 준비 — 후보 정리

Assignee:
Human Review Preparation Agent

Description:
draft2_done 문서를 사람이 검수하기 쉽도록 정리하라.

입력:
- translations/draft2/{{문서ID}}.draft2.md
- reviews/source-review/{{문서ID}}.source-review.md
- reviews/human-review/{{문서ID}}.human-review.md
- cumulative-glossary.md
- cumulative-annotations.md
- cumulative-interpretations.md

작업:
1. 신규 용어 후보 요약
2. 각주 후보 요약
3. 해석 후보 요약
4. Human Editor가 결정해야 할 항목 정리
5. human-review 파일 정리안 작성

완료 기준:
- Human Editor가 바로 검수할 수 있는 체크리스트 존재

금지:
- 후보 확정 금지
- 누적 파일 확정 갱신 금지
```

## 13.3 Confirmation Batch 운영 Issue

```text
Title:
2026-06-05 Confirmation Batch — 인간검수 완료 문서 3차 반영

Assignee:
Editorial Confirmation Manager Agent

Description:
human_review_done 문서를 대상으로, 사람이 확정한 용어·각주·해석만 반영하여 draft3_done 및 final_scan_done까지 진행하라.

입력:
- queues/human-review-queue.md
- reviews/human-review/{문서ID}.human-review.md
- translations/draft2/{문서ID}.draft2.md
- cumulative-glossary.md
- cumulative-annotations.md
- cumulative-interpretations.md
- editorial-decisions.md

작업:
1. 처리 대상 문서 선정
2. 사람 확정 항목만 식별
3. Draft 3 Integration Agent 작업 배정
4. Final Scan Agent 작업 배정
5. final-ready-queue 업데이트안 작성
6. confirmation report 작성

완료 기준:
- translations/draft3/{문서ID}.draft3.md 생성
- reviews/final-scan/{문서ID}.final-scan.md 생성
- final-ready-queue 등록
- confirmation report 작성

금지:
- 사람 대신 확정 금지
- 미확정 후보 반영 금지
- final 파일 작성 금지
```

## 13.4 Translation Director Daily Review Issue

```text
Title:
2026-06-05 Translation Director Daily Review

Assignee:
Translation Director Agent

Description:
오늘의 생산 모드와 확정 모드 진행 상황을 종합하고, 내일의 우선순위를 제안하라.

입력:
- master-checklist.md
- batch-reports/
- queues/today-queue.md
- queues/human-review-queue.md
- queues/hold-queue.md
- queues/error-queue.md
- queues/final-ready-queue.md

작업:
1. draft2_done 누적량 확인
2. human-review 대기열 길이 확인
3. hold/error 원인 확인
4. final-ready 문서 수 확인
5. 내일의 운영 모드 제안

출력:
- manager-logs/director/2026-06-05.director-log.md

보고 형식:
- 오늘의 성과
- 현재 병목
- 내일 권장 모드
- Human Editor가 먼저 봐야 할 문서
```

---

# 14. 단일 문서 Issue 템플릿

기존 v0.2 템플릿은 계속 사용할 수 있다. 다만 담당 매니저만 명확히 나눈다.

```text
기초작업 Issue → Draft Production Manager 산하
참고번역 분리 Issue → Draft Production Manager 산하
용어 후보 추출 Issue → Draft Production Manager 산하
1차 번역 Issue → Draft Production Manager 산하
원문대조 감수 Issue → Draft Production Manager 산하
각주·해석 후보 Issue → Draft Production Manager 산하
2차 번역 Issue → Draft Production Manager 산하
인간검수 준비 Issue → Editorial Confirmation Manager 산하
3차 번역 Issue → Editorial Confirmation Manager 산하
최종스캔 Issue → Editorial Confirmation Manager 산하
최종탈고 Issue → Human Editor 전용
```

## 14.1 2차 번역 Issue

```text
Title:
{{문서ID}} 2차 번역 — 직역 3 + 의역 7

Assignee:
Draft 2 Translator Agent

Parent:
Draft Production Manager Agent

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

## 14.2 3차 번역 Issue

```text
Title:
{{문서ID}} 3차 번역 — 확정 자료 반영

Assignee:
Draft 3 Integration Agent

Parent:
Editorial Confirmation Manager Agent

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

---

# 15. 첫 실습: T001 하나로 돌려보기

## 15.1 테스트 문서 ID 정하기

```text
t001-test
```

## 15.2 원본 파일 만들기

```bash
cd ~/Projects/buddhavamsa-translation-lab
touch sources/raw/t001-test.md
```

`sources/raw/t001-test.md`에 짧은 원문을 넣는다.

## 15.3 Paperclip에서 Issue 순서대로 실행

처음에는 Batch가 아니라 단일 문서 흐름으로 테스트한다.

```text
1. t001-test 기초작업
2. t001-test 참고번역 분리
3. t001-test 신규 용어 후보 추출
4. t001-test 1차 번역
5. t001-test 원문대조 감수
6. t001-test 각주 및 해석 후보 작성
7. t001-test 2차 번역
8. Human Review Preparation
9. Human Editor 검수
10. t001-test 3차 번역
11. t001-test 최종스캔
12. Human Final
```

처음 실습에서는 자동 위임보다 수동 Issue 생성이 좋다.

---

# 16. 3개 문서 반복 실습

T001 단일 문서가 성공하면 T001~T003으로 확장한다.

```text
목표:
T001~T003을 draft2_done까지 진행한다.

운영:
Draft Production Manager만 사용한다.

검수:
Human Editor는 세 문서의 human-review 후보표를 비교한다.

확정:
공통 용어가 반복되면 cumulative-glossary.md에 확정한다.
```

이 단계에서 확인할 점:

```text
1. 문단 ID가 유지되는가
2. draft1과 draft2가 분리되는가
3. source-review가 실제로 오역 후보를 잡는가
4. human-review 후보표가 사람이 보기 쉬운가
5. master-checklist 상태값이 일관되는가
```

---

# 17. 10개 문서 Batch 실습

T001~T003 실습 후 10개 문서 Batch를 실행한다.

## 17.1 Draft2 Batch

```text
명령:
오늘 T001~T010을 draft2_done까지 진행해줘.
완료 문서는 human-review-queue에 등록하고,
문제가 있는 문서는 hold-queue 또는 error-queue에 등록해줘.
```

## 17.2 Human Review Day

다음 날 또는 별도 시간에 Human Editor가 검수한다.

```text
작업:
- human-review-queue에서 우선순위 높은 문서 선택
- 신규 용어 확정
- 각주 후보 채택/보류/삭제
- 해석 후보 채택/보류/삭제
- cumulative-* 파일 갱신
- human_review_done 상태 표시
```

## 17.3 Confirmation Batch

```text
명령:
human_review_done 문서 중 3개를 draft3_done과 final_scan_done까지 진행해줘.
미확정 후보는 반영하지 말고,
최종탈고 대기 문서는 final-ready-queue에 등록해줘.
```

---

# 18. 운영 규칙

## 18.1 AI 수정 권한 제한

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

Annotation Candidate Agent:
reviews/human-review/의 후보 영역

Draft 2 Translator Agent:
translations/draft2/

Human Review Preparation Agent:
reviews/human-review/ 정리안

Draft 3 Integration Agent:
translations/draft3/

Final Scan Agent:
reviews/final-scan/

Final Handoff Agent:
queues/final-ready-queue.md 업데이트안

Human Editor:
cumulative-*
editorial-decisions.md
master-checklist.md
translations/final/
```

## 18.2 Final은 사람만 작성

```text
translations/final/{문서ID}.final.md
```

이 파일은 인간 편집자 전용으로 둔다.

AI가 작성할 수 있는 최종 지점은 다음까지다.

```text
translations/draft3/{문서ID}.draft3.md
reviews/final-scan/{문서ID}.final-scan.md
queues/final-ready-queue.md 업데이트안
```

## 18.3 생산량 제한

초기 권장 수량:

```text
초기 테스트: 1개 문서
반복 테스트: 3개 문서
소규모 Batch: 5개 문서
표준 Batch: 10개 문서
대규모 Batch: 20개 문서 이상은 비권장, 안정화 후 검토
```

## 18.4 병목 관리

```text
human-review-queue가 20개 이상 쌓이면 신규 draft2 생산을 줄인다.
hold-queue가 증가하면 원문 정규화 규칙을 재검토한다.
error-queue가 반복되면 에이전트 프롬프트 또는 파일 경로 규칙을 고친다.
용어 충돌이 많아지면 신규 생산보다 glossary 정리를 우선한다.
```

---

# 19. Paperclip 예산 제한

Paperclip은 에이전트별 예산과 비용 추적, budget hard-stop, audit log 등을 지원한다고 설명한다.[^paperclip-github]

번역 프로젝트에서는 다음처럼 낮게 시작한다.

```text
Translation Director Agent: 낮음
Draft Production Manager Agent: 중간
Editorial Confirmation Manager Agent: 낮음~중간
Glossary Agent: 낮음
Draft 1 Translator Agent: 중간
Source Review Agent: 중간
Draft 2 Translator Agent: 중간
Draft 3 Integration Agent: 낮음~중간
Final Scan Agent: 낮음
```

긴 문헌을 한 번에 맡기지 말고, 5~20문단 단위 또는 문서 1개 단위로 시작한다.

---

# 20. 학습 순서 v0.3

## Day 1 — Paperclip 설치와 Company 생성

```text
1. Node.js, pnpm 확인
2. npx paperclipai onboard --yes 실행
3. http://localhost:3100 접속
4. Company 생성
5. Human Editor / Translation Director / A/B Manager 개념 정리
```

## Day 2 — v0.3 폴더 구조 만들기

```text
1. buddhavamsa-translation-lab 폴더 생성
2. project-index.md 작성
3. style-guide.md 작성
4. master-checklist.md 작성
5. 누적 용어집·각주집·해석집 생성
6. sources/translations/reviews 폴더 생성
7. batch-plans, batch-reports, queues, manager-logs 생성
```

## Day 3 — T001 기초작업 실습

```text
1. sources/raw/t001-test.md 작성
2. Basic Setup Agent 실행
3. normalized 원문 생성 확인
4. docs-meta 생성 확인
5. master-checklist 업데이트 확인
```

## Day 4 — 2차 자동 생산 모드 단일 문서 실습

```text
1. Glossary Agent 실행
2. Draft 1 Translator Agent 실행
3. Source Review Agent 실행
4. Annotation Candidate Agent 실행
5. Draft 2 Translator Agent 실행
6. Draft Production Manager가 draft2_done 상태 확인
```

## Day 5 — 인간검수 준비

```text
1. Human Review Preparation Agent 실행
2. Human Editor가 신규 용어 확정
3. Human Editor가 각주·해석 후보 채택/보류/삭제
4. cumulative-glossary.md 갱신
5. cumulative-annotations.md 갱신
6. cumulative-interpretations.md 갱신
```

## Day 6 — 3차 확정 모드 실습

```text
1. Editorial Confirmation Manager 실행
2. Draft 3 Integration Agent 실행
3. Final Scan Agent 실행
4. final-ready-queue 등록 확인
```

## Day 7 — 3개 문서 반복

```text
1. T001~T003을 draft2_done까지 진행
2. human-review-queue 확인
3. 용어 충돌 확인
4. 1개 문서만 3차 확정 모드까지 진행
```

## Day 8 이후 — 10개 문서 Batch 운영

```text
1. Draft2 Batch Plan 작성
2. 10개 문서 draft2_done 진행
3. Batch Report 확인
4. Human Review Day 별도 운영
5. Confirmation Batch 별도 운영
```

---

# 21. 최종 운영 모델

v0.3의 최종 운영 모델은 다음이다.

```text
Paperclip
= 번역 편집실 운영판

Human Editor
= 최종 번역자·감수자·편집자

Translation Director Agent
= 전체 흐름을 조절하는 편집장

Draft Production Manager Agent
= 2차 자동 생산 모드 관리자

Editorial Confirmation Manager Agent
= 3차 확정 모드 관리자

작업 에이전트들
= 단계별 조교

v0.3 폴더 구조
= 모든 에이전트가 공유하는 작업장

master-checklist.md
= 전체 진행판

docs-meta/{문서ID}.meta.md
= 문서별 파일 경로 안내판

queues/
= 오늘 작업, 인간검수, 보류, 오류, 최종탈고 대기열

batch-plans/
= 일일·주간 작업 계획

batch-reports/
= 생산 및 확정 결과 보고서

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

# 22. 핵심 결론

Paperclip과 OL 번역 매뉴얼 v0.3을 결합할 때 가장 안전한 구조는 단일 PM이 아니라 다음 구조다.

```text
Human Editor
└─ Translation Director Agent
   ├─ Draft Production Manager Agent
   └─ Editorial Confirmation Manager Agent
```

이 구조의 의미는 다음과 같다.

```text
속도는 A 매니저가 확보한다.
품질 통제는 B 매니저가 확보한다.
전체 균형은 Translation Director가 본다.
최종 판단은 Human Editor가 한다.
```

따라서 v0.3 튜토리얼의 핵심은 다음 한 문장이다.

```text
Paperclip은 AI가 번역을 마음대로 끝내는 자동 공장이 아니라,
AI 에이전트들이 정해진 파일·정해진 권한·정해진 승인 지점 안에서
번역 생산과 확정 반영을 나누어 수행하게 하는 편집실 운영판이다.
```

---

# 23. 다음 업데이트 후보

v0.4에서 추가할 수 있는 항목은 다음이다.

```text
1. 실제 Paperclip 화면 기준 Company 생성 예시
2. Agent별 설정값 예시
3. Codex CLI 또는 Claude Code와 연결하는 실습
4. T001 샘플 문서로 실제 파일 생성 실습
5. batch report 자동 생성 스크립트
6. master-checklist 상태값 자동 점검 스크립트
```

단, v0.4에서도 출판·웹 등록·디자인·온톨로지·지식그래프·Entity 구조화는 다루지 않는다. 우선 목표는 번역 원고 생산과 탈고 경험의 안정화다.

---

[^paperclip-github]: https://github.com/paperclipai/paperclip
[^paperclip-quickstart]: https://paperclipai-paperclip.mintlify.app/quickstart
