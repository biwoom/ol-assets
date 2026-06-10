# Paperclip 과 번역 프로젝트 튜토리얼 v0.1

아래는 **문헌 번역 AI 협업 워크플로우 v0.2**를 Paperclip 위에서 실제로 구현·학습하기 위한 튜토리얼입니다. 전제는 “Paperclip 자체가 번역 AI가 아니라, 여러 AI 에이전트에게 일을 배정하고 진행상황·예산·승인·이력을 관리하는 오케스트레이션/작업관리판”이라는 점입니다. Paperclip 공식 README도 “Node.js server + React UI로 AI 에이전트 팀을 조율하고, 목표·작업·비용을 대시보드에서 관리한다”고 설명합니다. ([GitHub][1])

---

# 1. Paperclip을 번역 프로젝트에 쓰는 방식

Paperclip의 기본 은유는 “회사”입니다. 그래서 번역 프로젝트에서는 다음처럼 대응시키면 됩니다.

```text
Paperclip Company
= 문헌 번역 편집실

Goal / Initiative
= 특정 문헌군 번역 완성

Project
= 번역 묶음, 예: 붓다전기 1장, 니까야 10경, 삼론현의 총서

Issue / Task
= 문서 하나 또는 문서 묶음의 번역 단계

Agent
= 기초작업, 용어집, 1차 번역, 원문대조, 각주·해석, 2차 번역, 3차 반영 에이전트

Human Board / Approval
= 사용자 최종 검수·승인
```

중요한 점은 Paperclip이 “에이전트가 어떻게 사고하는지”를 직접 설계하는 프레임워크가 아니라, 이미 존재하는 Claude Code, Codex, Cursor, Bash, HTTP bot 같은 런타임을 조직도·태스크·예산·승인 구조 안에서 운용하는 “control plane”에 가깝다는 점입니다. 공식 README도 Paperclip이 Claude Code, Codex, Cursor, Bash, HTTP 등을 연결할 수 있고 “If it can receive a heartbeat, it’s hired”라고 설명합니다. ([GitHub][1])

---

# 2. 설치 전 준비

## 2.1 필요 조건

공식 Quickstart 기준 요구사항은 다음입니다.

```bash
node --version
pnpm --version
```

Paperclip 공식 README는 **Node.js 20+**, **pnpm 9.15+**를 요구한다고 명시합니다. 또한 수동 설치 시 `git clone`, `pnpm install`, `pnpm dev`로 실행하며, API 서버는 기본적으로 `http://localhost:3100`에서 시작되고 embedded PostgreSQL이 자동 생성된다고 설명합니다. ([GitHub][1])

Mac 기준 설치 확인:

```bash
node --version
pnpm --version
git --version
```

pnpm이 없다면:

```bash
npm install -g pnpm
```

## 2.2 사용할 AI 런타임 준비

Paperclip은 “Bring Your Own Agent” 방식입니다. 즉 Paperclip만 설치한다고 번역 에이전트가 자동으로 생기는 것이 아니라, Claude Code, Codex CLI, Cursor, Bash script, HTTP bot 등 실제 작업을 수행할 실행 주체가 필요합니다. Paperclip README도 “Any agent, any runtime, one org chart”라고 설명합니다. ([GitHub][1])

처음 학습용으로는 아래 중 하나만 있어도 됩니다.

```text
1. Claude Code 또는 Codex CLI
2. Bash 기반 간단한 스크립트 에이전트
3. HTTP로 호출 가능한 로컬/원격 LLM 에이전트
```

처음에는 **하나의 범용 CLI 에이전트**를 Paperclip에 연결하고, 역할별 프롬프트만 다르게 주는 방식이 가장 단순합니다.

---

# 3. Paperclip 설치

## 3.1 가장 쉬운 설치: onboard

공식 Quickstart는 다음 명령을 제시합니다. ([GitHub][1])

```bash
npx paperclipai onboard --yes
```

로컬에서 먼저 실험할 경우 이 방식이 가장 좋습니다. 공식 README에 따르면 이 quickstart는 빠른 첫 실행을 위해 trusted local loopback mode를 기본으로 사용합니다. ([GitHub][1])

LAN이나 tailnet 접근이 필요하면 공식 README에 있는 방식처럼 bind preset을 명시합니다. ([GitHub][1])

```bash
npx paperclipai onboard --yes --bind lan
```

또는:

```bash
npx paperclipai onboard --yes --bind tailnet
```

처음 학습 단계에서는 외부 접근을 열 필요가 없으므로 `--bind lan`이나 `--bind tailnet`은 나중에 검토하는 편이 안전합니다.

## 3.2 수동 설치

공식 README의 수동 설치 방식은 다음입니다. ([GitHub][1])

```bash
git clone https://github.com/paperclipai/paperclip.git
cd paperclip
pnpm install
pnpm dev
```

실행 후 브라우저에서 다음 주소를 엽니다.

```text
http://localhost:3100
```

## 3.3 개인정보·원고 보안 주의

Paperclip 공식 README에 따르면 익명 사용 텔레메트리가 기본 활성화되어 있으며, `PAPERCLIP_TELEMETRY_DISABLED=1`, `DO_NOT_TRACK=1`, 또는 설정 파일에서 `telemetry.enabled: false`로 비활성화할 수 있습니다. README는 프롬프트·파일 경로·시크릿·이슈 내용은 수집하지 않는다고 설명하지만, 불교 원고·미공개 번역문을 다루는 경우에는 처음부터 끄는 것이 좋습니다. ([GitHub][1])

실행 전 터미널에서:

```bash
export PAPERCLIP_TELEMETRY_DISABLED=1
export DO_NOT_TRACK=1
```

zsh를 사용한다면 `~/.zshrc`에 추가할 수 있습니다.

```bash
echo 'export PAPERCLIP_TELEMETRY_DISABLED=1' >> ~/.zshrc
echo 'export DO_NOT_TRACK=1' >> ~/.zshrc
source ~/.zshrc
```

---

# 4. 번역 프로젝트 폴더 만들기

Paperclip 설치 폴더와 번역 원고 폴더는 분리하는 것이 좋습니다.

예시:

```bash
mkdir -p ~/Projects/buddhist-translation-lab
cd ~/Projects/buddhist-translation-lab
```

v0.2 매뉴얼 기준 폴더를 만듭니다.

```bash
mkdir -p documents workbench
touch project-index.md
touch master-checklist.md
touch style-guide.md
touch editorial-decisions.md
touch cumulative-glossary.md
touch cumulative-annotations.md
touch cumulative-interpretations.md
```

초기 구조:

```text
buddhist-translation-lab/
├─ project-index.md
├─ master-checklist.md
├─ style-guide.md
├─ editorial-decisions.md
├─ cumulative-glossary.md
├─ cumulative-annotations.md
├─ cumulative-interpretations.md
├─ documents/
└─ workbench/
```

---

# 5. Paperclip 안에 “번역 편집실” 만들기

Paperclip UI가 열리면 새 Company를 만듭니다.

## Company 이름

```text
Buddhist Translation Desk
```

또는 한국어로:

```text
불교문헌 번역 편집실
```

## Company Goal

다음처럼 입력합니다.

```text
불교 원전 문헌을 원문 보존, 용어 일관성, 원문대조 감수, 각주·해석 검토, 인간 최종 탈고 원칙에 따라 번역한다. 
AI 에이전트는 초안·검출·제안만 수행하고, 최종 용어·각주·해석·탈고 판단은 인간 편집자가 수행한다.
```

Paperclip은 목표-작업 연결을 중시합니다. README도 모든 작업이 회사 미션과 목표 ancestry를 통해 “왜 이 일을 하는지”를 알 수 있게 한다고 설명합니다. ([GitHub][1])

---

# 6. 에이전트 조직도 설계

처음부터 너무 많은 에이전트를 만들면 운영이 복잡해집니다. v0.2 워크플로우 기준으로 7개 에이전트를 추천합니다.

```text
Human Editor
└─ Translation PM Agent
   ├─ Basic Setup Agent
   ├─ Glossary Agent
   ├─ Draft 1 Translator Agent
   ├─ Source Review Agent
   ├─ Annotation & Interpretation Agent
   ├─ Draft 2 Translator Agent
   └─ Draft 3 Integration Agent
```

Paperclip에서는 사람이 board/operator 역할을 하고, 실제 에이전트들에게 task를 배정하는 형태로 생각하면 됩니다. 공식 README도 Paperclip에 org chart, roles, reporting lines, permissions, budgets가 있다고 설명합니다. ([GitHub][1])

---

# 7. 각 에이전트 역할 프롬프트

아래 내용은 Paperclip에서 에이전트를 만들 때 “job description / instructions”에 넣을 수 있는 초안입니다.

## 7.1 Translation PM Agent

```text
너는 불교문헌 번역 프로젝트의 작업관리 에이전트다.

목표:
- master-checklist.md를 기준으로 문서별 진행상태를 관리한다.
- 각 문서가 v0.2 워크플로우 순서를 따르도록 태스크를 분배한다.
- AI 에이전트가 확정 권한을 넘지 않도록 감시한다.
- 최종 판정이 필요한 항목은 반드시 Human Editor에게 넘긴다.

금지:
- 최종 번역어 확정 금지
- 최종 각주·해석 확정 금지
- 최종 원고 탈고 금지

주요 입력:
- project-index.md
- master-checklist.md
- style-guide.md
- documents/{문서ID}.md

주요 출력:
- 다음 작업 제안
- master-checklist.md 업데이트 제안
- Human Editor에게 필요한 승인 요청
```

## 7.2 Basic Setup Agent

```text
너는 기초작업 에이전트다.

역할:
- 원문 문서를 documents/{문서ID}.md 템플릿에 맞게 정리한다.
- Metadata, Source, Prefix / Segment 영역을 작성한다.
- 문단 ID를 부여한다.
- master-checklist.md 업데이트안을 제안한다.

원칙:
- 원문을 수정하지 않는다.
- 번역하지 않는다.
- 해석하지 않는다.
- 원문 보존이 최우선이다.

출력:
- documents/{문서ID}.md의 0~2번 영역
- master-checklist.md 업데이트 제안
```

## 7.3 Glossary Agent

```text
너는 용어집 에이전트다.

역할:
- cumulative-glossary.md를 먼저 확인한다.
- 문서 Source에서 신규 용어 후보를 추출한다.
- documents/{문서ID}.md의 New Glossary Candidates 영역을 작성한다.
- 누적 용어집과 충돌하는 번역 후보를 표시한다.

금지:
- 신규 번역어를 확정하지 않는다.
- cumulative-glossary.md를 직접 확정 갱신하지 않는다.
- 확정되지 않은 용어를 확정된 것처럼 쓰지 않는다.

출력 형식:
| 확인 | 원문 | 제안 번역어 | 대안 | 문단 | 상태 | 비고 |
```

## 7.4 Draft 1 Translator Agent

```text
너는 1차 번역 에이전트다.

역할:
- Source를 바탕으로 Draft 1 — 직역 7 + 의역 3을 작성한다.
- 원문 구조와 의미 대응을 우선한다.
- 한국어가 다소 딱딱해도 좋다.
- 불확실한 구문은 표시한다.
- 미확정 용어는 원어 또는 후보 번역어를 병기한다.

금지:
- 문학적 윤문을 과도하게 하지 않는다.
- 원문에 없는 해석을 본문에 넣지 않는다.
- 각주나 해석을 본문 번역에 섞지 않는다.

입력:
- Source
- Prefix / Segment
- cumulative-glossary.md
- New Glossary Candidates
- style-guide.md

출력:
- documents/{문서ID}.md의 Draft 1 영역
```

## 7.5 Source Review Agent

```text
너는 원문대조 감수 에이전트다.

역할:
- Source와 Draft 1을 대조한다.
- 원문 누락, 의미 추가, 오역 후보, 부정문·조건문·인과관계 오류, 주어·목적어 혼동, 용어 불일치를 점검한다.
- documents/{문서ID}.md의 Source Review Summary 영역을 작성한다.

금지:
- 문체 취향으로 번역을 고치지 않는다.
- 최종 오역 판정을 단정하지 않는다.
- 수정은 권고로만 제시한다.

출력:
| 항목 | 결과 | 비고 |
```

## 7.6 Annotation & Interpretation Agent

```text
너는 각주 및 해석 제안 에이전트다.

역할:
- cumulative-annotations.md와 cumulative-interpretations.md를 먼저 확인한다.
- 신규 각주 후보를 작성한다.
- 신규 해석 후보를 작성한다.
- documents/{문서ID}.md의 New Annotation Candidates, New Interpretation Candidates 영역을 작성한다.

금지:
- 본문 번역을 직접 수정하지 않는다.
- 각주와 해석을 확정하지 않는다.
- 출처 불확실한 설명을 단정하지 않는다.
- 특정 전통의 해석을 본문에 강제로 삽입하지 않는다.

출력:
1. 신규 각주 후보 체크리스트
2. 신규 해석 후보 체크리스트
```

## 7.7 Draft 2 Translator Agent

```text
너는 2차 번역 에이전트다.

역할:
- Draft 1과 Source Review Summary를 바탕으로 Draft 2 — 직역 3 + 의역 7을 작성한다.
- 한국어 독서 문체를 자연스럽게 만든다.
- 원문대조 감수의 경고사항을 반영한다.
- 확정되지 않은 용어·각주·해석은 임의로 확정 반영하지 않는다.

금지:
- 원문에 없는 정서나 교훈을 본문에 추가하지 않는다.
- 해석 후보를 본문 번역에 섞지 않는다.
- 확정되지 않은 용어를 고정하지 않는다.

출력:
- documents/{문서ID}.md의 Draft 2 영역
```

## 7.8 Draft 3 Integration Agent

```text
너는 3차 번역 통합 반영 에이전트다.

역할:
- Human Review에서 확정된 신규 용어, 각주, 해석만 반영한다.
- cumulative-glossary.md, cumulative-annotations.md, cumulative-interpretations.md를 따른다.
- Draft 2의 문체를 유지하면서 Draft 3을 작성한다.
- 확정 각주는 지정된 위치에 반영한다.
- 확정 해석은 본문이 아니라 각주 또는 해설 영역에 반영한다.

금지:
- 새 용어를 임의 확정하지 않는다.
- 새 각주를 임의 추가하지 않는다.
- 새 해석을 임의 추가하지 않는다.
- 의미를 재해석하지 않는다.

출력:
- documents/{문서ID}.md의 Draft 3 영역
```

---

# 8. Paperclip 프로젝트/이슈 설계

Paperclip 안에서는 “문서 하나 = 이슈 하나”로 만들 수도 있고, “단계 하나 = 이슈 하나”로 만들 수도 있습니다. 대량 문헌에서는 다음 방식을 권합니다.

## 8.1 처음 학습용: 문서 하나 = 프로젝트 하나

처음에는 작은 테스트 문서 1개만 씁니다.

```text
Project: T001 번역 실험
Issues:
1. T001 기초작업
2. T001 용어 후보 추출
3. T001 1차 번역
4. T001 원문대조 감수
5. T001 각주·해석 후보 작성
6. T001 2차 번역
7. Human Review: 용어·각주·해석 확정
8. T001 3차 번역
9. T001 최종 스캔
10. Human Final: 최종 탈고
```

## 8.2 운영용: Batch 하나 = 프로젝트 하나

문서가 많아지면 10~20개 단위로 Batch를 만듭니다.

```text
Project: Batch 01 — T001~T020

Milestones:
1. 원문 정리 완료
2. 용어 후보 추출 완료
3. 1차 번역 완료
4. 원문대조 감수 완료
5. 각주·해석 후보 완료
6. 2차 번역 완료
7. 인간 검수 완료
8. 3차 번역 완료
9. 최종 스캔 완료
```

이 방식이 대량 번역에는 더 적합합니다.

---

# 9. 첫 실습: T001 하나만 돌려보기

## 9.1 원고 파일 만들기

```bash
cd ~/Projects/buddhist-translation-lab
touch documents/T001.md
```

`documents/T001.md`에 최소 템플릿을 넣습니다.

```markdown
# T001 테스트 문서

## 0. Metadata

- ID: T001
- 문서명: 테스트 문서
- 문헌군:
- 원문 출처:
- 작업 상태: source_ready
- 최종 탈고 여부: 미완료
- 비고:

---

## 1. Source

여기에 원문을 입력한다.

---

## 2. Prefix / Segment

| 문단 ID | 원문 시작어 | 비고 |
|---|---|---|
| 001 |  |  |

---

## 3. New Glossary Candidates

| 확인 | 원문 | 제안 번역어 | 대안 | 문단 | 상태 | 비고 |
|---|---|---|---|---|---|---|

---

## 4. Draft 1 — 직역 7 + 의역 3

---

## 5. Source Review Summary

| 항목 | 결과 | 비고 |
|---|---|---|
| 원문 누락 |  |  |
| 의미 추가 |  |  |
| 오역 후보 |  |  |
| 용어 불일치 |  |  |

---

## 6. New Annotation Candidates

| 확인 | 문단 | 대상어 | 주석 후보 | 상태 | 비고 |
|---|---|---|---|---|---|

---

## 7. New Interpretation Candidates

| 확인 | 문단 | 주제 | 해석 후보 | 반영 방식 | 상태 | 비고 |
|---|---|---|---|---|---|---|

---

## 8. Draft 2 — 직역 3 + 의역 7

---

## 9. Human Review

### 9.1 확정 신규 용어

| 완료 | 원문 | 확정 번역어 | 누적 용어집 반영 |
|---|---|---|---|

### 9.2 확정 신규 각주

| 완료 | 대상어 | 처리 | 누적 각주집 반영 |
|---|---|---|---|

### 9.3 확정 신규 해석

| 완료 | 주제 | 처리 | 누적 해석집 반영 |
|---|---|---|---|

---

## 10. Draft 3 — 확정 자료 반영본

---

## 11. Final Scan Summary

| 항목 | 결과 | 비고 |
|---|---|---|
| 원문 누락 없음 | [ ] |  |
| 확정 용어 반영 | [ ] |  |
| 확정 각주 반영 | [ ] |  |
| 확정 해석 반영 | [ ] |  |
| 의미 이탈 없음 | [ ] |  |

---

## 12. Final Manuscript
```

## 9.2 Paperclip Issue 만들기

Paperclip UI에서 새 Issue를 만듭니다.

```text
Title:
T001 용어 후보 추출

Description:
documents/T001.md의 Source를 읽고, cumulative-glossary.md와 style-guide.md를 참조하여 New Glossary Candidates 영역을 작성하라.
신규 용어는 candidate 상태로만 제안하고, 확정하지 말라.
```

담당 에이전트:

```text
Glossary Agent
```

완료 기준:

```text
- documents/T001.md의 New Glossary Candidates 표가 채워져 있다.
- 누적 용어집과 충돌하는 항목이 표시되어 있다.
- 어떤 용어도 approved로 확정하지 않았다.
```

---

# 10. Human Review 단계 운영법

Paperclip의 장점은 사람이 중간 승인자로 개입할 수 있다는 점입니다. 공식 README도 governance 기능으로 승인, 전략 override, agent pause/terminate, audit logging을 제공한다고 설명합니다. ([GitHub][1])

Human Review Issue는 AI에게 맡기지 말고 사용자 본인의 수동 태스크로 둡니다.

```text
Title:
Human Review — T001 용어·각주·해석 확정

Description:
다음 항목을 사람이 직접 판정한다.
1. New Glossary Candidates에서 확정할 용어 선택
2. New Annotation Candidates에서 채택할 각주 선택
3. New Interpretation Candidates에서 채택할 해석 선택
4. cumulative-glossary.md, cumulative-annotations.md, cumulative-interpretations.md 갱신
5. documents/T001.md의 Human Review 영역 표시
```

완료 기준:

```text
- 확정 용어가 Human Review에 표시되어 있다.
- cumulative-glossary.md가 갱신되어 있다.
- 채택 각주가 cumulative-annotations.md에 반영되어 있다.
- 채택 해석이 cumulative-interpretations.md에 반영되어 있다.
- Draft 3 Integration Agent에게 넘길 준비가 되었다.
```

---

# 11. Paperclip 운영 시 주의점

## 11.1 대량 이슈를 한꺼번에 만들지 않기

처음부터 500개 문서를 Paperclip에 넣지 마십시오. Paperclip GitHub Issues를 보면 2026년 6월 현재 고용량 issue export나 heartbeat-run 관련 이슈들이 활발히 올라와 있습니다. 즉 프로젝트가 빠르게 발전 중이지만, 대량 운영에서는 아직 버전별 안정성 검증이 필요합니다. ([GitHub][2])

추천 순서:

```text
1단계: T001 하나만 실험
2단계: T001~T003 3개 문서 실험
3단계: T001~T010 Batch 실험
4단계: 20개 단위 Batch 운영
```

## 11.2 에이전트에게 파일 수정 권한을 너무 넓게 주지 않기

처음에는 모든 파일을 수정하게 하지 말고, 문서별로 담당 영역을 제한합니다.

예:

```text
Glossary Agent:
documents/T001.md의 New Glossary Candidates만 수정

Draft 1 Translator:
Draft 1 영역만 수정

Source Review Agent:
Source Review Summary 영역만 수정
```

## 11.3 Final Manuscript는 AI 수정 금지

최종 탈고 영역은 인간 전용으로 두는 것을 권합니다.

```text
Final Manuscript 영역은 인간 편집자만 작성한다.
AI는 Draft 3까지만 작성한다.
```

---

# 12. 권장 학습 순서

## Day 1 — 설치와 기본 실행

```text
1. Node.js, pnpm 확인
2. npx paperclipai onboard --yes 실행
3. http://localhost:3100 접속
4. 테스트 Company 생성
5. 에이전트 1개만 만들어보기
```

## Day 2 — v0.2 폴더 구조 연결

```text
1. buddhist-translation-lab 폴더 생성
2. 공통 파일 생성
3. documents/T001.md 생성
4. Paperclip Project 생성
5. Basic Setup Issue 생성
```

## Day 3 — 용어집·1차 번역 실험

```text
1. Glossary Agent 실행
2. Draft 1 Translator Agent 실행
3. 문서 파일에 결과가 잘 들어가는지 확인
4. 문제 있으면 프롬프트 수정
```

## Day 4 — 감수·각주·2차 번역 실험

```text
1. Source Review Agent 실행
2. Annotation & Interpretation Agent 실행
3. Draft 2 Translator Agent 실행
4. 각 에이전트가 자기 영역만 수정하는지 확인
```

## Day 5 — Human Review와 3차 번역

```text
1. 사람이 신규 용어 확정
2. 사람이 신규 각주·해석 확정
3. 누적 파일 갱신
4. Draft 3 Integration Agent 실행
5. Final Scan 실행
```

## Day 6 — 운영 템플릿 정리

```text
1. 에이전트 프롬프트 개선
2. Issue 템플릿 고정
3. master-checklist 상태값 고정
4. T002에 반복 적용
```

---

# 13. 가장 먼저 만들 Paperclip 템플릿 5개

처음에는 7개 에이전트 전부보다 Issue 템플릿 5개가 더 중요합니다.

## 13.1 용어 후보 추출 템플릿

```text
Title:
{{문서ID}} 용어 후보 추출

Description:
documents/{{문서ID}}.md의 Source를 읽고 cumulative-glossary.md와 style-guide.md를 참조하라.
New Glossary Candidates 영역에 신규 용어 후보를 표 형식으로 작성하라.
확정하지 말고 candidate 상태로만 남겨라.
```

## 13.2 1차 번역 템플릿

```text
Title:
{{문서ID}} 1차 번역

Description:
documents/{{문서ID}}.md의 Source, Prefix / Segment, New Glossary Candidates를 참조하여 Draft 1 영역을 작성하라.
비율은 직역 7 + 의역 3이다.
원문 구조를 보존하고, 불확실한 구문은 표시하라.
```

## 13.3 원문대조 감수 템플릿

```text
Title:
{{문서ID}} 원문대조 감수

Description:
Source와 Draft 1을 대조하여 Source Review Summary 영역을 작성하라.
원문 누락, 의미 추가, 오역 후보, 용어 불일치를 점검하라.
본문을 직접 수정하지 말고 리포트만 작성하라.
```

## 13.4 각주·해석 후보 템플릿

```text
Title:
{{문서ID}} 각주·해석 후보 작성

Description:
cumulative-annotations.md, cumulative-interpretations.md를 확인한 뒤,
documents/{{문서ID}}.md의 New Annotation Candidates와 New Interpretation Candidates 영역을 작성하라.
본문을 수정하지 말라.
후보는 candidate 상태로만 남겨라.
```

## 13.5 3차 번역 템플릿

```text
Title:
{{문서ID}} 3차 번역 — 확정 자료 반영

Description:
Draft 2, Human Review, cumulative-glossary.md, cumulative-annotations.md, cumulative-interpretations.md를 참조하여 Draft 3 영역을 작성하라.
확정된 용어·각주·해석만 반영하라.
새로운 용어·각주·해석을 임의로 추가하지 말라.
```

---

# 14. 결론

Paperclip을 문헌 번역에 도입할 때의 핵심은 “AI가 번역을 알아서 끝내게 하는 것”이 아닙니다.

```text
Paperclip = 번역 편집실 운영판
AI 에이전트 = 역할별 조교
Human Editor = 최종 번역자·감수자·편집자
```

가장 안전한 도입 순서는 다음입니다.

```text
1. 로컬 설치
2. T001 단일 문서 실험
3. 에이전트 5~7개 역할 고정
4. Issue 템플릿 고정
5. Human Review 게이트 고정
6. T001~T003 반복
7. 10~20개 Batch 운영
```

처음부터 자동화 범위를 넓히지 말고, **“AI는 Draft 3까지만, Final Manuscript는 사람만”**이라는 경계를 유지하는 것이 좋습니다. 이 경계만 지키면 Paperclip은 문헌 번역의 생산성을 높이면서도 원전 번역의 책임성과 신중함을 보존하는 도구로 활용할 수 있습니다.

[1]: https://github.com/paperclipai/paperclip "GitHub - paperclipai/paperclip: The open-source app everyone uses to manage agents at work · GitHub"
[2]: https://github.com/paperclipai/paperclip/issues?utm_source=chatgpt.com "Issues · paperclipai/paperclip"
