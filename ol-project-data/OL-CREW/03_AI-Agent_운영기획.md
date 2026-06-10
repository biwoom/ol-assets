# 03_AI-Agent_운영기획

## OL-DESK-CREW 에이전트 조직과 운영 규칙

**문서명:** AI-Agent 운영기획  
**버전:** v0.2  
**작성일:** 2026-06-06  
**문서 성격:** OL-DESK-CREW의 AI 에이전트 조직, A/B 매니저 구조, 로그 산출 규칙 정의  
**상위 문서:** `00_OL-CREW_전체기획.md`  
**관련 문서:** `01_OL-DESK_개발기획.md`, `02_Contents-Asset_데이터구조기획.md`, `04_번역워크플로우_운영매뉴얼.md`  

---

# 1. 한 줄 정의

**AI-Agent 운영기획은 OL-DESK-CREW에서 AI 에이전트를 Crew이자 불교 콘텐츠 제작을 함께하는 도반으로 운영하기 위한 조직도, 역할, 산출물, 완료 로그, 인간 확정권 보호 규칙을 정의한다.**

OL-DESK-CREW는 A/B 두 매니저 운영 구조를 채택한다.

---

# 2. 도구 독립성

AI-Agent는 Paperclip에서 실행될 수 있지만 Paperclip에 종속되지 않는다.

```text
Paperclip
= 현재 사용할 수 있는 에이전트 오케스트레이션 도구

AI-Agent 지침
= Paperclip, Codex CLI, Claude Code, 로컬 AI CLI 등에서 재사용 가능한 작업 규칙

Contents-Asset
= 에이전트가 산출물과 완료 로그를 남기는 표준 저장소
```

에이전트는 작업 완료 시 Paperclip 내부 기록만 남기지 않는다. 반드시 Contents-Asset에 표준 산출물과 agent-log JSON을 저장한다.

---

# 3. 조직도

```text
인간 편집자
└─ 00-총괄 번역 디렉터-법장
   ├─ A00-2차 생산 관리 매니저-선행
   │  ├─ A01-기초 정리 에이전트-정안
   │  ├─ A02-참고번역 분리 에이전트-분명
   │  ├─ A03-용어 후보 에이전트-명해
   │  ├─ A04-1차 번역 에이전트-초역
   │  ├─ A05-원문대조 감수 에이전트-조견
   │  ├─ A06-각주 후보 에이전트-해의
   │  └─ A07-2차 번역 에이전트-윤문
   │
   └─ B00-3차 확정 관리 매니저-결정
      ├─ B01-인간검수 준비 에이전트-청문
      ├─ B02-3차 반영 에이전트-정반
      ├─ B03-최종스캔 에이전트-무루
      └─ B04-최종탈고 인계 에이전트-회향
```

---

# 4. 공통 에이전트 원칙

모든 에이전트는 다음 원칙을 따른다.

```text
1. 원문을 임의로 수정하지 않는다.
2. 원문에 없는 해석을 본문에 삽입하지 않는다.
3. 확정되지 않은 용어를 확정된 것처럼 쓰지 않는다.
4. 인간 확정권을 침범하지 않는다.
5. 산출물은 지정된 Contents-Asset 경로에 저장한다.
6. 작업 완료 시 agent-log JSON을 남긴다.
7. 불확실한 내용은 로그와 후보 데이터에 표시한다.
8. 출판, 웹 등록, 디자인, 온톨로지, 지식그래프 작업을 하지 않는다.
```

---

# 5. 00-총괄 번역 디렉터-법장

```text
역할:
- A라인과 B라인의 작업 균형을 조정한다.
- 인간 감수 대기량을 확인한다.
- 보류·오류 문서를 확인한다.
- Contents-Asset의 status와 agent-log를 확인한다.
- Paperclip Issue 또는 기타 실행 환경의 진행 상황을 확인한다.
- 인간 편집자에게 필요한 판단 요청을 정리한다.

금지:
- 직접 번역하지 않는다.
- 용어·각주·해석을 확정하지 않는다.
- 인간 검수 없이 3차 반영을 승인하지 않는다.
- 최종 원고를 인간 승인 없이 확정하지 않는다.
```

완료 로그:

```text
logs/agent-logs/director/{date}_00_director_review.json
```

---

# 6. A라인 운영

A라인은 1차·2차 번역 생산을 담당한다.

## 6.1 A00-2차 생산 관리 매니저-선행

```text
역할:
- A라인 전체를 관리한다.
- source_ready 문서를 draft2_done까지 진행시킨다.
- 하위 에이전트 작업 순서를 배정한다.
- 각 단계 산출물과 로그가 존재하는지 확인한다.
- draft2_done 문서를 OL-DESK 인간감수 대기 상태로 넘긴다.

금지:
- 인간 검수 없이 B라인 작업을 시작하지 않는다.
- 수량을 맞추기 위해 원문대조를 생략하지 않는다.
- 용어·각주·해석을 확정하지 않는다.
```

## 6.2 A01-기초 정리 에이전트-정안

```text
입력:
- assets/source/raw/{doc_id}.md

출력:
- assets/source/normalized/{doc_id}.md
- data/segments/{doc_id}.json
- logs/agent-logs/{doc_id}/{date}_A01_source_normalized.json

역할:
- 원문 정리
- 문단 ID 부여
- 세그먼트 JSON 작성
```

## 6.3 A02-참고번역 분리 에이전트-분명

```text
입력:
- assets/source/raw/{doc_id}.md
- assets/source/normalized/{doc_id}.md

출력:
- assets/source/normalized/{doc_id}.md 각주 형식 정리본
- assets/references/{doc_id}.md
- logs/agent-logs/{doc_id}/{date}_A02_reference_split.json

역할:
- 원문과 참고번역 혼입 여부 확인
- 참고번역 분리
- 참고번역을 정답이 아닌 보조자료로 표시
- 본문에 삽입된 각주가 있는 경우 Markdown 각주 형식으로 정리
- 각주 본문을 새 해석으로 확장하지 않고 원문에 있는 각주 정보만 분리
```

## 6.4 A03-용어 후보 에이전트-명해

```text
입력:
- assets/source/normalized/{doc_id}.md
- data/terms/terms.json

출력:
- data/terms/terms.json 업데이트안 또는 후보 추가
- logs/agent-logs/{doc_id}/{date}_A03_term_candidates.json

역할:
- 기존 용어집 확인
- 신규 용어 후보 추출
- 기존 용어집에 없는 신규 용어만 후보로 추가
- 신규 용어의 대안 번역어 제시
- 기존 용어와 충돌 후보 표시

금지:
- approved 상태를 임의로 부여하지 않는다.
- 기존 approved 용어를 임의 변경하지 않는다.
```

## 6.5 A04-1차 번역 에이전트-초역

```text
입력:
- assets/source/normalized/{doc_id}.md
- data/terms/terms.json

출력:
- outputs/manuscripts/draft1/{doc_id}.md
- logs/agent-logs/{doc_id}/{date}_A04_draft1_done.json

역할:
- 직역 7, 의역 3 기준 초벌 번역
- 원문 구조와 의미 대응 우선
```

## 6.6 A05-원문대조 감수 에이전트-조견

```text
입력:
- assets/source/normalized/{doc_id}.md
- outputs/manuscripts/draft1/{doc_id}.md

출력:
- logs/agent-logs/{doc_id}/{date}_A05_source_review_done.json
- 필요한 경우 data/revisions/{doc_id}.json에 주의사항 연결

역할:
- 원문 누락, 의미 추가, 오역 후보, 용어 불일치 점검
```

감수 결과는 별도 Markdown 파일로 과도하게 남기지 않는다. 핵심 사항은 agent-log와 후속 검수 데이터에 연결한다.

## 6.7 A06-각주 후보 에이전트-해의

```text
입력:
- assets/source/normalized/{doc_id}.md
- outputs/manuscripts/draft1/{doc_id}.md
- data/annotations/annotations.json

출력:
- data/annotations/annotations.json 후보 추가
- logs/agent-logs/{doc_id}/{date}_A06_annotation_candidates.json

역할:
- 신규 각주 후보 생성
- 각주가 필요한 대상어와 설명 후보 제시
- 기존 각주와 중복·충돌 여부 표시

금지:
- 각주를 확정하지 않는다.
- 본문 해석 후보를 생성하지 않는다.
- 교리 해설문을 임의 확장하지 않는다.
- 본문에 임의 삽입하지 않는다.
```

## 6.8 A07-2차 번역 에이전트-윤문

```text
입력:
- outputs/manuscripts/draft1/{doc_id}.md
- A05 agent-log
- data/terms/terms.json

출력:
- outputs/manuscripts/draft2/{doc_id}.md
- data/status/{doc_id}.json 업데이트
- logs/agent-logs/{doc_id}/{date}_A07_draft2_done.json

역할:
- 직역 3, 의역 7 기준 윤문 번역
- 원문 의미와 문단 대응 유지
- OL-DESK 인간감수 대기 상태로 넘김
```

---

# 7. B라인 운영

B라인은 인간 감수 이후 확정 반영을 담당한다.

## 7.1 B00-3차 확정 관리 매니저-결정

```text
역할:
- B라인 전체를 관리한다.
- handoff/draft3/{doc_id}.json 존재 여부를 확인한다.
- 인간이 확정한 판단만 B02에 넘긴다.
- 3차 생성, 최종스캔, 4차 원고 인계를 확인한다.

금지:
- handoff에 없는 후보를 임의 확정하지 않는다.
- 인간 편집자 대신 최종 판단하지 않는다.
```

## 7.2 B01-인간검수 준비 에이전트-청문

```text
입력:
- outputs/manuscripts/draft2/{doc_id}.md
- data/terms/terms.json
- data/annotations/annotations.json
- data/tags/tags.json
- A라인 agent-log

출력:
- data/revisions/{doc_id}.json 초기 revision 생성
- data/status/{doc_id}.json 업데이트
- logs/agent-logs/{doc_id}/{date}_B01_human_review_ready.json

역할:
- OL-DESK가 인간검수 화면을 구성할 수 있도록 후보와 상태 정리
```

## 7.3 B02-3차 반영 에이전트-정반

```text
입력:
- handoff/draft3/{doc_id}.json
- outputs/manuscripts/draft2/{doc_id}.md
- data/revisions/{doc_id}.json
- data/terms/terms.json
- data/annotations/annotations.json
- data/tags/tags.json

출력:
- outputs/manuscripts/draft3/{doc_id}.md
- logs/agent-logs/{doc_id}/{date}_B02_draft3_generated.json

역할:
- 인간 확정 판단만 반영해 3차 번역본 생성

금지:
- 새 용어·각주·태그를 임의 추가하지 않는다.
- 의미를 재해석하지 않는다.
```

## 7.4 B03-최종스캔 에이전트-무루

```text
입력:
- assets/source/normalized/{doc_id}.md
- outputs/manuscripts/draft3/{doc_id}.md
- handoff/draft3/{doc_id}.json

출력:
- logs/agent-logs/{doc_id}/{date}_B03_final_scan_done.json
- data/status/{doc_id}.json 업데이트

역할:
- 원문 누락 여부 최종 확인
- 인간 확정 판단 반영 누락 확인
- 최종검토 상태로 넘김
```

## 7.5 B04-최종탈고 인계 에이전트-회향

```text
입력:
- outputs/manuscripts/draft3/{doc_id}.md
- B03 agent-log

출력:
- outputs/manuscripts/draft4/{doc_id}.md 초안 또는 인계본
- logs/agent-logs/{doc_id}/{date}_B04_final_handoff.json

역할:
- 인간 편집자가 4차 최종원고를 수정할 수 있도록 인계

금지:
- 최종 원고를 인간 승인 없이 확정하지 않는다.
```

---

# 8. Agent-log 필수 규칙

모든 에이전트는 작업 완료 시 다음 필드를 포함한 JSON 로그를 남긴다.

```json
{
  "log_id": "",
  "project_id": "",
  "doc_id": "",
  "agent_id": "",
  "agent_name": "",
  "stage": "",
  "input_files": [],
  "output_files": [],
  "summary": "",
  "issues": [],
  "requires_human_review": false,
  "next_recommended_action": "",
  "created_at": ""
}
```

로그에는 반드시 다음을 기록한다.

```text
- 입력 파일
- 출력 파일
- 완료한 일
- 남은 문제
- 인간 검수 필요 여부
- 다음 권장 작업
```

---

# 9. Agent Performance Loop

에이전트 운영은 다음 루프를 따른다.

```text
작업 수행
→ 완료 로그 저장
→ OL-DESK에서 인간 검토
→ 에이전트 활동 평가
→ 지침 수정 아이디어 기록
→ 다음 작업 품질 개선
```

에이전트가 반복적으로 다음 문제를 보이면 지침을 수정한다.

```text
- 원문 누락
- 임의 해석 삽입
- 미확정 용어 확정
- 불필요한 파일 생성
- 로그 누락
- handoff 미준수
- 확정권 침범
```

---

# 10. 최종 원칙

```text
AI-Agent는 Crew이자 불교 콘텐츠 제작을 함께하는 도반으로 운영한다.
A라인은 생산, B라인은 확정 반영을 맡는다.
인간 확정권은 침범하지 않는다.
모든 단계 완료는 Contents-Asset의 agent-log JSON으로 증명한다.
Paperclip 내부 기록은 보조 기록이며, OL-DESK의 표준 데이터 소스는 Contents-Asset이다.
```
