# 문헌 번역 AI 협업 워크플로우 매뉴얼 v0.2

## 다중문서·대량문헌 운영형

**문서명:** 문헌 번역 AI 협업 워크플로우 매뉴얼
**버전:** v0.2
**적용 범위:** 불교 경전·논서·주석서·전기문헌 등 다중 문서 번역 프로젝트
**작업 방식:** 1인 제작자 + AI 다중 에이전트 협업
**핵심 목표:** 문서가 100개, 500개 이상으로 늘어나도 관리 가능한 번역·감수·용어집·각주·해석·탈고 체계 구축
**제외 범위:** 출판, 웹 등록, 디자인, 온톨로지, 콘텐츠 배포 파이프라인

---

# 0. v0.2의 핵심 변경점

v0.1은 하나의 짧은 문헌을 세밀하게 처리하는 데 적합했으나, 다수의 경전·문서에는 산출물이 지나치게 많아지는 문제가 있었다.

v0.2에서는 다음 원칙으로 바꾼다.

```text
문서마다 16개 산출물을 만들지 않는다.
문서마다 하나의 통합 원고 파일을 둔다.
용어집·각주집·해석집은 프로젝트 단위로 누적 관리한다.
전체 진행 상태는 하나의 마스터 체크리스트에서 관리한다.
중간 산출물은 필요한 경우에만 임시로 만들고, 확정 내용만 누적 파일에 반영한다.
```

즉, v0.2의 기본 구조는 다음이다.

```text
프로젝트 공통 파일
+ 문서별 통합 원고 파일
+ 필요 시 임시 작업 파일
```

---

# 1. 전체 구조

```text
translation-project/
├─ project-index.md
├─ master-checklist.md
├─ style-guide.md
├─ editorial-decisions.md
├─ cumulative-glossary.md
├─ cumulative-annotations.md
├─ cumulative-interpretations.md
├─ documents/
│  ├─ T001.md
│  ├─ T002.md
│  ├─ T003.md
│  └─ ...
└─ workbench/
   ├─ T001-temp-review.md
   ├─ T002-temp-glossary.md
   └─ ...
```

단, `workbench/`는 선택 사항이다.
임시 리포트나 실험 번역을 따로 보관할 필요가 있을 때만 사용한다.

---

# 2. 산출물 설계 원칙

## 2.1 반드시 보존할 산출물

대량 문헌 번역에서 반드시 필요한 산출물은 다음이다.

```text
1. master-checklist.md
2. cumulative-glossary.md
3. cumulative-annotations.md
4. cumulative-interpretations.md
5. documents/{문서ID}.md
```

여기에 보조적으로 다음 파일을 둔다.

```text
6. project-index.md
7. style-guide.md
8. editorial-decisions.md
```

## 2.2 선택 산출물

다음은 반드시 파일로 남길 필요가 없다.

```text
1차 번역 에이전트의 중간 설명
원문대조 감수의 상세 리포트
각주 후보 생성 과정
2차 번역 수정 과정
3차 번역 변경 로그
```

다만 다음 경우에는 별도 임시 파일로 남길 수 있다.

```text
오역 후보가 많아 상세 검토가 필요한 문서
여러 번역안 비교가 필요한 문서
교학적 쟁점이 큰 문서
용어 충돌이 많은 문서
사람이 나중에 다시 검토해야 할 문서
```

---

# 3. 프로젝트 공통 파일

## 3.1 `project-index.md`

프로젝트의 기본 정보를 기록하는 파일이다.

```markdown
# 번역 프로젝트 인덱스

## 1. 프로젝트 정보

- 프로젝트명:
- 문헌군:
- 작업 범위:
- 기준 원문:
- 보조 원문:
- 참고 번역:
- 목표 독자:
- 목표 문체:
- 작업 시작일:
- 현재 버전:

## 2. 번역 원칙

- 원문 의미 보존을 우선한다.
- 원문에 없는 해석은 본문에 넣지 않는다.
- 교학 용어는 가능한 한 일관되게 번역한다.
- 필요한 설명은 각주 또는 해설로 분리한다.
- 최종 판정은 인간 편집자가 한다.

## 3. 문서 ID 규칙

예:
T001, T002, T003 ...
또는
MN-001, DN-001, BS-01-001 등
```

---

## 3.2 `master-checklist.md`

전체 진행 상황을 관리하는 핵심 파일이다.

```markdown
# 전체 문서 진행 체크리스트

| ID | 문서명 | 원문정리 | 1차번역 | 원문대조 | 각주/해석 | 2차번역 | 인간검수 | 3차번역 | 최종스캔 | 탈고 | 비고 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T001 | 제1문서 | [x] | [x] | [x] | [x] | [x] | [ ] | [ ] | [ ] | [ ] | 용어 확정 대기 |
| T002 | 제2문서 | [x] | [x] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | 원문대조 필요 |
| T003 | 제3문서 | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | 미착수 |
```

문서 수가 많을 경우 상태값을 간단히 줄일 수도 있다.

```markdown
| ID | 문서명 | 상태 | 다음 작업 | 담당 | 비고 |
|---|---|---|---|---|---|
| T001 | 제1문서 | 2차번역 완료 | 인간검수 | 사람 | 용어 3개 확정 필요 |
| T002 | 제2문서 | 원문대조 대기 | 감수 실행 | AI |  |
```

권장 상태값은 다음과 같다.

```text
not_started
source_ready
draft1_done
source_review_done
annotation_done
draft2_done
human_review_done
draft3_done
final_scan_done
final_done
hold
```

---

## 3.3 `style-guide.md`

번역 문체와 형식 규칙을 저장한다.

```markdown
# 번역 문체 가이드

## 1. 번역 비율

### 1차 번역
- 직역 7 + 의역 3
- 원문 구조 보존 우선
- 한국어가 다소 딱딱해도 허용

### 2차 번역
- 직역 3 + 의역 7
- 자연스러운 한국어 독서문체
- 단, 원문에 없는 해석 삽입 금지

### 3차 번역
- 확정 용어집 반영
- 확정 각주·해석 반영
- 의미 재해석 금지
- 2차 번역의 문체 유지

## 2. 용어 원칙

- 핵심 교학 용어는 누적 용어집을 우선 따른다.
- 미확정 용어는 원어 또는 한자를 병기한다.
- 새 용어는 문서 내부 후보표에 등록한다.

## 3. 각주 원칙

- 첫 출현 용어에는 필요한 경우 짧은 각주를 둔다.
- 본문 흐름을 방해하는 긴 해석은 해설로 분리한다.
- 출처가 불확실한 설명은 확정 각주로 넣지 않는다.

## 4. 해석 원칙

- 해석은 본문 번역과 구분한다.
- 특정 전통의 해석을 본문에 단정적으로 삽입하지 않는다.
- 해석 후보는 사람이 승인한 뒤 반영한다.
```

---

## 3.4 `editorial-decisions.md`

사람이 내린 중요한 판단을 누적한다.

```markdown
# 편집 결정 기록

## 2026-06-04

### 결정 1
`dukkha`는 기본적으로 “괴로움”으로 번역한다.

- 이유:
- 적용 범위:
- 예외:

### 결정 2
`deva`는 서사 문맥에서는 “천신”으로 번역한다.

- 이유:
- 적용 범위:
- 예외:
```

이 파일은 나중에 프로젝트 전체의 일관성을 유지하는 데 매우 중요하다.

---

## 3.5 `cumulative-glossary.md`

프로젝트 전체에서 확정된 용어를 누적한다.

```markdown
# 누적 용어집

| 원문 | 확정 번역어 | 대안 | 사용 원칙 | 최초 확정 문서 | 비고 |
|---|---|---|---|---|---|
| dukkha | 괴로움 | 고통, 불만족 | 사성제·교학 문맥 기본 번역어 | T001 | 신체적 pain은 고통 가능 |
| dhamma | 법 | 가르침 | 교학 핵심어는 법, 설법 내용은 가르침 가능 | T001 | 문맥 판단 |
| bodhisatta | 보살 | 구도자 | 성도 이전 싯다르타 문맥 | T001 | 첫 출현 시 주석 |
```

---

## 3.6 `cumulative-annotations.md`

확정된 각주를 누적한다.

```markdown
# 누적 각주집

| ID | 대상어 | 확정 각주 | 적용 원칙 | 최초 사용 문서 | 비고 |
|---|---|---|---|---|---|
| ANNO-001 | 보살 | 여기서 보살은 성불 이전의 구도자로서의 bodhisatta를 가리킨다. | 첫 출현 시 사용 | T001 | 대승 보살 일반과 구분 |
| ANNO-002 | 도솔천 | 도솔천은 욕계 육천 가운데 하나로, 보살이 인간계에 태어나기 전 머무는 하늘로 설명된다. | 첫 출현 시 사용 | T001 |  |
```

---

## 3.7 `cumulative-interpretations.md`

확정된 해석 방향을 누적한다.

```markdown
# 누적 해석집

| ID | 주제 | 확정 해석 요지 | 사용 방식 | 최초 사용 문서 | 비고 |
|---|---|---|---|---|---|
| INT-001 | 보살의 하강 | 보살의 하강은 중생 세계로 들어가는 자비의 결단으로 해석할 수 있다. | 해설문 | T001 | 본문 삽입 금지 |
| INT-002 | 태몽 서사 | 태몽은 성자의 탄생을 상징화하는 불전 서사 장치로 볼 수 있다. | 해설 또는 각주 | T002 | 표현 주의 |
```

---

# 4. 문서별 통합 원고 파일

각 문서는 하나의 파일로 관리한다.

```text
documents/T001.md
documents/T002.md
documents/T003.md
```

문서 파일 안에 원문, 번역, 감수 요약, 용어 후보, 각주 후보, 해석 후보, 인간 검수, 3차 번역, 최종 원고를 통합한다.

---

## 4.1 문서 파일 템플릿

```markdown
# {{문서ID}} {{문서명}}

## 0. Metadata

- ID:
- 문서명:
- 문헌군:
- 원문 출처:
- 작업 상태:
- 최종 탈고 여부:
- 비고:

---

## 1. Source

원문을 입력한다.

---

## 2. Prefix / Segment

| 문단 ID | 원문 시작어 | 비고 |
|---|---|---|
| 001 |  |  |
| 002 |  |  |

---

## 3. New Glossary Candidates

| 확인 | 원문 | 제안 번역어 | 대안 | 문단 | 상태 | 비고 |
|---|---|---|---|---|---|---|
| [ ] |  |  |  |  | candidate |  |

---

## 4. Draft 1 — 직역 7 + 의역 3

1차 번역을 입력한다.

---

## 5. Source Review Summary

| 항목 | 결과 | 비고 |
|---|---|---|
| 원문 누락 |  |  |
| 의미 추가 |  |  |
| 오역 후보 |  |  |
| 용어 불일치 |  |  |

### 재검토 문단

- 

---

## 6. New Annotation Candidates

| 확인 | 문단 | 대상어 | 주석 후보 | 상태 | 비고 |
|---|---|---|---|---|---|
| [ ] |  |  |  | candidate |  |

---

## 7. New Interpretation Candidates

| 확인 | 문단 | 주제 | 해석 후보 | 반영 방식 | 상태 | 비고 |
|---|---|---|---|---|---|---|
| [ ] |  |  |  | 각주/해설/미반영 | candidate |  |

---

## 8. Draft 2 — 직역 3 + 의역 7

2차 번역을 입력한다.

---

## 9. Human Review

### 9.1 확정 신규 용어

| 완료 | 원문 | 확정 번역어 | 누적 용어집 반영 |
|---|---|---|---|
| [ ] |  |  | [ ] |

### 9.2 확정 신규 각주

| 완료 | 대상어 | 처리 | 누적 각주집 반영 |
|---|---|---|---|
| [ ] |  | 채택/보류/삭제 | [ ] |

### 9.3 확정 신규 해석

| 완료 | 주제 | 처리 | 누적 해석집 반영 |
|---|---|---|---|
| [ ] |  | 채택/보류/삭제 | [ ] |

---

## 10. Draft 3 — 확정 자료 반영본

3차 번역을 입력한다.

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

최종 탈고본을 입력한다.
```

---

# 5. AI 에이전트 역할

## 5.1 기초작업 에이전트

### 역할

```text
- 문서 ID 생성
- prefix 태그 생성
- 문단 분절
- 문서 파일 기본 틀 작성
- master-checklist.md 갱신
```

### 입력

```text
원문 전체 또는 문서 목록
project-index.md
style-guide.md
```

### 출력

```text
documents/{문서ID}.md의 Metadata, Source, Prefix / Segment 영역
master-checklist.md 업데이트 제안
```

### 주의

기초작업 에이전트는 번역하지 않는다.
원문을 고치지 않는다.

---

## 5.2 용어집 에이전트

### 역할

```text
- cumulative-glossary.md 확인
- 해당 문서의 신규 용어 후보 추출
- 문서 파일의 New Glossary Candidates 영역 작성
- 누적 용어집과 충돌하는 후보 표시
```

### 입력

```text
documents/{문서ID}.md
cumulative-glossary.md
style-guide.md
```

### 출력

```text
문서 내부 New Glossary Candidates 영역
필요 시 누적 용어집 충돌 메모
```

### 주의

용어집 에이전트는 용어를 확정하지 않는다.
후보만 제안한다.

---

## 5.3 1차 번역 에이전트

### 역할

```text
- 직역 7 + 의역 3 비율의 1차 번역 작성
- 원문 구조 보존
- 미확정 용어는 원어 병기 또는 후보 번역어 병기
```

### 입력

```text
documents/{문서ID}.md의 Source 영역
cumulative-glossary.md
문서 내부 New Glossary Candidates
style-guide.md
```

### 출력

```text
문서 내부 Draft 1 — 직역 7 + 의역 3 영역
```

### 주의

1차 번역은 아름다운 문체보다 원문 대응성을 우선한다.

---

## 5.4 원문대조 감수 에이전트

### 역할

```text
- 원문 누락 여부 점검
- 의미 추가 여부 점검
- 오역 후보 탐지
- 용어 불일치 탐지
- 문서 내부 Source Review Summary 작성
```

### 입력

```text
Source
Draft 1
cumulative-glossary.md
New Glossary Candidates
```

### 출력

```text
문서 내부 Source Review Summary 영역
```

### 별도 상세 리포트가 필요한 경우

다음 경우에만 `workbench/{문서ID}-source-review-detail.md`를 만든다.

```text
- 오역 후보가 많음
- 원문 구문이 매우 난해함
- 문헌학적 쟁점이 있음
- 인간 검토가 길어질 가능성이 있음
```

---

## 5.5 각주 및 해석 제안 에이전트

### 역할

```text
- cumulative-annotations.md 확인
- cumulative-interpretations.md 확인
- 해당 문서의 신규 각주 후보 작성
- 해당 문서의 신규 해석 후보 작성
- 문서 내부 New Annotation Candidates, New Interpretation Candidates 영역 작성
```

### 입력

```text
Source
Draft 1 또는 Draft 2
cumulative-annotations.md
cumulative-interpretations.md
cumulative-glossary.md
style-guide.md
```

### 출력

```text
문서 내부 New Annotation Candidates 영역
문서 내부 New Interpretation Candidates 영역
```

### 주의

이 에이전트는 본문을 직접 수정하지 않는다.
각주와 해석은 모두 후보로만 제시한다.

---

## 5.6 2차 번역 에이전트

### 역할

```text
- 직역 3 + 의역 7 비율의 2차 번역 작성
- 한국어 문체 정리
- 원문대조 감수 결과 반영
- 단, 확정되지 않은 용어·각주·해석은 임의 반영하지 않음
```

### 입력

```text
Draft 1
Source Review Summary
cumulative-glossary.md
New Glossary Candidates
style-guide.md
```

### 출력

```text
문서 내부 Draft 2 — 직역 3 + 의역 7 영역
```

---

## 5.7 인간 편집자

### 역할

```text
- 신규 용어 확정
- 신규 각주 채택·보류·삭제
- 신규 해석 채택·보류·삭제
- cumulative-glossary.md 갱신
- cumulative-annotations.md 갱신
- cumulative-interpretations.md 갱신
- master-checklist.md 갱신
```

### 작업 위치

```text
문서 내부 Human Review 영역
프로젝트 공통 누적 파일
master-checklist.md
editorial-decisions.md
```

### 원칙

사람이 확정하지 않은 후보는 3차 번역에 확정 자료로 반영하지 않는다.

---

## 5.8 3차 번역 에이전트

### 역할

```text
- 확정 신규 용어집 반영
- 확정 신규 각주 반영
- 확정 신규 해석 반영
- 2차 번역의 문체를 유지하며 3차 번역본 작성
```

### 입력

```text
Draft 2
Human Review
cumulative-glossary.md
cumulative-annotations.md
cumulative-interpretations.md
Source Review Summary
style-guide.md
```

### 출력

```text
문서 내부 Draft 3 — 확정 자료 반영본
```

### 금지

```text
새 용어 임의 확정 금지
새 각주 임의 추가 금지
새 해석 임의 추가 금지
본문에 해석을 과도하게 삽입 금지
의미 재해석 금지
```

---

## 5.9 최종 원문대조 스캔 에이전트

### 역할

```text
- Draft 3 기준 최종 원문 누락 검사
- 확정 용어 반영 여부 검사
- 확정 각주 반영 여부 검사
- 확정 해석 반영 여부 검사
- 문체 편집 과정에서 의미가 이탈했는지 확인
```

### 입력

```text
Source
Draft 3
Human Review
cumulative-glossary.md
cumulative-annotations.md
cumulative-interpretations.md
```

### 출력

```text
문서 내부 Final Scan Summary 영역
```

상세 리포트는 문제가 있을 때만 별도로 만든다.

---

## 5.10 인간 최종 탈고

### 역할

```text
- Draft 3을 바탕으로 4차 최종 원고 작성
- 문장 리듬 조정
- 주석 분량 조정
- 해석문 위치 조정
- 최종 문체 확정
- master-checklist.md에서 탈고 완료 표시
```

### 출력

```text
문서 내부 Final Manuscript 영역
```

---

# 6. 작업 흐름

## 6.1 프로젝트 초기화

```text
1. project-index.md 작성
2. style-guide.md 작성
3. cumulative-glossary.md 생성
4. cumulative-annotations.md 생성
5. cumulative-interpretations.md 생성
6. editorial-decisions.md 생성
7. master-checklist.md 생성
8. documents/ 폴더 생성
```

---

## 6.2 문서별 작업 흐름

```text
1. 기초작업 에이전트
   → 문서 파일 생성
   → 원문 입력
   → 문단 ID 부여
   → master-checklist 갱신

2. 용어집 에이전트
   → 신규 용어 후보 작성

3. 1차 번역 에이전트
   → Draft 1 작성

4. 원문대조 감수 에이전트
   → Source Review Summary 작성

5. 각주 및 해석 제안 에이전트
   → 신규 각주 후보 작성
   → 신규 해석 후보 작성

6. 2차 번역 에이전트
   → Draft 2 작성

7. 인간 편집자
   → Human Review 작성
   → 누적 용어집·각주집·해석집 갱신

8. 3차 번역 에이전트
   → Draft 3 작성

9. 최종 원문대조 스캔 에이전트
   → Final Scan Summary 작성

10. 인간 최종 탈고
   → Final Manuscript 작성
   → master-checklist에서 탈고 완료 표시
```

---

# 7. 산출물 생성 기준

## 7.1 항상 생성하는 것

```text
documents/{문서ID}.md
master-checklist.md 갱신
```

## 7.2 확정 시 갱신하는 것

```text
cumulative-glossary.md
cumulative-annotations.md
cumulative-interpretations.md
editorial-decisions.md
```

## 7.3 필요할 때만 생성하는 것

```text
workbench/{문서ID}-source-review-detail.md
workbench/{문서ID}-translation-alternatives.md
workbench/{문서ID}-doctrinal-issue.md
workbench/{문서ID}-glossary-conflict.md
```

---

# 8. 문서 상태 관리 규칙

문서 상태는 `master-checklist.md`와 문서 파일의 Metadata에 함께 기록한다.

권장 상태값:

```text
not_started
source_ready
glossary_candidate_done
draft1_done
source_review_done
annotation_candidate_done
draft2_done
human_review_done
draft3_done
final_scan_done
final_done
hold
```

예시:

```markdown
## 0. Metadata

- ID: T001
- 문서명: 제1문서
- 작업 상태: draft2_done
- 최종 탈고 여부: 미완료
- 비고: 신규 용어 3개 확정 필요
```

---

# 9. 대량 문서 운영 방식

## 9.1 100개 이상 문서의 경우

문서별 작업을 처음부터 끝까지 하나씩 완성하기보다, 묶음 단위로 진행하는 것이 좋다.

```text
Batch 01: T001–T020
Batch 02: T021–T040
Batch 03: T041–T060
```

작업 흐름:

```text
Batch 01 전체 원문 정리
→ Batch 01 전체 용어 후보 추출
→ Batch 01 전체 1차 번역
→ Batch 01 전체 원문대조
→ Batch 01 전체 인간 검수
```

장점:

```text
용어 일관성이 높아진다.
비슷한 문맥을 한꺼번에 처리할 수 있다.
반복되는 각주·해석을 누적하기 쉽다.
```

## 9.2 문서별 완결 방식이 적합한 경우

다음 경우에는 한 문서씩 완결하는 방식이 좋다.

```text
문서마다 주제가 매우 다를 때
길이가 긴 문서일 때
교학 쟁점이 많은 문서일 때
초기 테스트 단계일 때
```

---

# 10. AI에게 주는 공통 지시문

모든 에이전트에게 공통으로 들어갈 기본 지시문은 다음과 같다.

```text
너는 불교문헌 번역 작업을 보조하는 AI 에이전트다.

원문을 임의로 수정하지 말라.
확정되지 않은 용어를 확정된 것처럼 쓰지 말라.
원문에 없는 해석을 본문에 삽입하지 말라.
불확실한 내용은 반드시 표시하라.
사람이 검토해야 할 항목은 체크리스트로 남겨라.
최종 판정은 인간 편집자가 한다.
```

---

# 11. v0.2 최종 요약

v0.2 방식은 다음 한 문장으로 요약할 수 있다.

```text
문서별로 하나의 통합 원고 파일을 만들고,
용어집·각주집·해석집은 프로젝트 단위로 누적하며,
전체 진행은 마스터 체크리스트 하나로 관리한다.
```

이 구조의 장점은 다음과 같다.

```text
문서가 100개, 500개로 늘어나도 관리 가능하다.
단계별 산출물이 폭증하지 않는다.
AI 작업 결과를 필요한 만큼만 보존할 수 있다.
확정 용어·각주·해석이 프로젝트 전체에 축적된다.
사람은 최종 판정과 탈고에 집중할 수 있다.
```

최종 권장 구조는 다음이다.

```text
translation-project/
├─ project-index.md
├─ master-checklist.md
├─ style-guide.md
├─ editorial-decisions.md
├─ cumulative-glossary.md
├─ cumulative-annotations.md
├─ cumulative-interpretations.md
└─ documents/
   ├─ T001.md
   ├─ T002.md
   ├─ T003.md
   └─ ...
```

`workbench/`는 필요할 때만 둔다.

이것이 v0.2의 기본 매뉴얼이다.
