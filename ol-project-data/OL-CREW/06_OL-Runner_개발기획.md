# 06_OL-Runner_개발기획

## 로컬 번역 파이프라인 실행기 개발 기획

**문서명:** OL-Runner 개발기획  
**버전:** v0.1  
**작성일:** 2026-06-07  
**문서 성격:** Paperclip 의존을 줄이고 로컬 CLI 기반 번역 실행기로 전환하기 위한 기획 문서  
**상위 문서:** `00_OL-CREW_전체기획.md`  
**관련 문서:** `01_OL-DESK_개발기획.md`, `02_Contents-Asset_데이터구조기획.md`, `04_번역워크플로우_운영매뉴얼.md`, `05_OL-DESK_개발로드맵.md`, `VSCode에서 직접 AI 오케스트레이션 구성안 평가.md`

---

# 1. 한 줄 정의

**OL-Runner는 불교전문문헌 번역 프로젝트에서 Paperclip의 조직형 에이전트 실행을 대체하고, 로컬 환경에서 AI CLI/API 모델을 호출하여 Contents-Asset 표준 산출물과 한국어 작업 로그를 생산하는 경량 번역 파이프라인 실행기이다.**

OL-Runner의 목표는 “AI 에이전트 회사를 재현하는 것”이 아니다. 목표는 인간 감수자가 통제 가능한 방식으로 원문 정리, 용어 후보, 초벌 번역, 원문 대조, 각주 후보, 2차 원고 생성, 최종 산출물 export를 빠르고 예측 가능하게 실행하는 것이다.

---

# 2. 배경과 문제의식

현재 구조는 다음 세 계층으로 구성되어 있다.

```text
Paperclip 에이전트 층
Contents-Asset 데이터 층
OL-DESK Astro 대시보드 층
```

Paperclip을 통해 총괄 디렉터, A라인 매니저, B라인 매니저, 세부 에이전트 체계를 테스트한 결과 다음 문제가 확인되었다.

```text
- 실행 속도가 느리다.
- 토큰 소비가 크다.
- 에이전트 간 위임과 보고가 실제 번역 생산보다 더 큰 오버헤드를 만든다.
- 매니저/디렉터 조직 은유가 로컬 생산 파이프라인에는 과하다.
- 산출물은 결국 Contents-Asset에 남으므로 Paperclip 내부 대화 기록의 필요성이 낮다.
- 인간 감수자는 에이전트 조직도보다 원고, 상태, 후보, 수정, handoff를 더 중요하게 본다.
```

초기 탐색 단계에서는 Paperclip이 유용했다. 역할 분장, 산출물 구조, 로그 필요성, 인간 감수 UX의 필요성을 빠르게 드러냈기 때문이다. 그러나 실제 생산 단계에서는 조직형 에이전트 계층보다 로컬 실행 파이프라인이 더 단순하고 효율적일 가능성이 높다.

---

# 3. 기본 판단

## 3.1 Paperclip 의존 제거 방향

OL-Runner 방향에서는 Paperclip을 필수 계층으로 유지하지 않는다.

Paperclip이 담당하던 기능은 다음 방식으로 대체한다.

```text
에이전트 역할 분장
= OL-Runner의 stage/task 정의

작업 지시와 위임
= 로컬 job queue, config, 상태 전이 규칙

대화형 로그
= Contents-Asset 표준 JSON 로그와 OL-DESK 표시용 한국어 요약

팀원 평가
= agent-evaluations 또는 runner-evaluations JSON
```

따라서 장기 구조는 다음과 같이 단순화한다.

```text
OL-Runner
  = 로컬 번역 파이프라인 실행기

Contents-Asset
  = 단일 데이터 저장소

OL-DESK
  = 인간 감수자 편집·검토·승인 UI
```

## 3.2 총괄디렉터/매니저 체계 폐기

총괄디렉터와 두 매니저 체계는 Paperclip의 조직형 오케스트레이션 안에서는 이해하기 쉬운 구조였다. 그러나 로컬 실행기에서는 불필요한 복잡도다.

OL-Runner에서는 다음을 기준으로 관리한다.

```text
- 문서 상태
- 단계별 입력 파일
- 단계별 출력 파일
- 상태 전이 규칙
- 실패와 재시도 기록
- 인간 승인 게이트
```

즉, “누가 누구에게 위임했는가”보다 “현재 문서가 어떤 상태이고 다음에 어떤 stage를 실행할 수 있는가”가 중요하다.

---

# 4. 유지할 것과 버릴 것

## 4.1 버릴 것

```text
- Paperclip 회사형 에이전트 조직
- 총괄디렉터/매니저/팀원 채용 흐름
- 에이전트 간 긴 대화형 위임
- 이슈 채팅을 통한 상태 진행
- 생산 단계마다 전체 컨텍스트를 반복 전달하는 구조
```

## 4.2 유지할 것

```text
- Contents-Asset 저장 구조
- A01~A07, B01~B04에서 정리된 단계별 책임
- Markdown/JSON 산출물 계약
- 상태 전이 규칙
- 인간 감수 게이트
- agent-log 또는 runner-log 스키마
- OL-DESK의 읽기/수정/승인 UX
- 에이전트 또는 stage 평가 데이터
```

핵심은 “에이전트 조직”을 유지하는 것이 아니라, 그동안 정리한 “번역 워크플로우 계약”을 유지하는 것이다.

---

# 5. OL-Runner의 역할

OL-Runner는 다음 기능을 담당한다.

```text
1. 프로젝트와 문서 상태 읽기
2. 실행 가능한 stage 판정
3. AI CLI/API 모델 호출
4. 단계별 산출물 생성
5. 한국어 작업 로그 기록
6. 상태 파일 업데이트
7. 실패 시 재시도 또는 중단 기록
8. 비용, 시간, 토큰 사용량 추적
9. OL-DESK가 즉시 읽을 수 있는 형태로 결과 저장
```

OL-Runner는 사람이 직접 읽고 판단하는 최종 권한을 갖지 않는다. 인간 판단이 필요한 용어 확정, 각주 확정, 3차 원고 수정, 4차 최종 승인, revision reopen은 OL-DESK에서 수행한다.

---

# 6. 파이프라인 단계 설계

OL-Runner의 단계는 Paperclip 에이전트 이름을 그대로 모방하지 않고, 실행 가능한 task/stage로 정의한다.

권장 stage:

```text
normalize-source
split-reference
extract-terms
translate-draft1
review-source-alignment
propose-annotations
polish-draft2
prepare-human-review
generate-draft3
review-final-scan
save-draft4
export-final
```

기존 A라인과 대응하면 다음과 같다.

```text
A01 기초 정리
= normalize-source

A02 참고번역 분리
= split-reference

A03 용어 후보
= extract-terms

A04 1차 번역
= translate-draft1

A05 원문대조 감수
= review-source-alignment

A06 각주 후보
= propose-annotations

A07 2차 번역
= polish-draft2
```

B라인은 인간 감수 이후의 반영과 최종 원고 처리로 재정의한다.

```text
B01 인간감수 준비
= prepare-human-review

B02 3차 반영
= generate-draft3

B03 최종 스캔
= review-final-scan

B04 최종 출력
= export-final
```

---

# 7. 병렬화 원칙

OL-Runner의 가장 큰 효율 개선 지점은 병렬화다. 다만 모든 단계를 무조건 병렬화하면 번역 품질이 깨질 수 있다.

## 7.1 병렬화에 적합한 작업

```text
- 문서별 원문 정리
- 세그먼트별 초벌 번역
- 세그먼트별 원문 대조
- 세그먼트별 각주 후보 추출
- 여러 문서의 독립 실행
```

## 7.2 병렬화에 주의할 작업

```text
- 문체 통일
- 용어 일관성 확정
- 장 전체의 구조적 흐름 판단
- 최종 원고 탈고
- 인간 감수 반영 판단
```

번역 품질을 위해 `translate-draft1`은 세그먼트 병렬화를 활용할 수 있지만, `polish-draft2`와 `review-source-alignment`에서는 문서 전체 맥락을 다시 확인해야 한다.

권장 흐름:

```text
1. 원문 전체 구조 파악
2. 용어 후보와 문체 가이드 준비
3. 세그먼트 병렬 번역
4. 병합
5. 문서 전체 문체 통일
6. 원문 대조
7. 인간 감수 대기
```

---

# 8. 모델 라우팅 원칙

OL-Runner는 모든 작업에 같은 모델을 쓰지 않는다. 작업 성격에 따라 모델을 분리한다.

예시 원칙:

```text
가벼운 구조화 작업
= 빠르고 저렴한 모델

세그먼트 초벌 번역
= 비용 대비 품질이 좋은 중간 모델

원문 대조, 문체 통일, 최종 검토
= 품질 우선 모델

인간 수정 반영과 민감한 판단
= 고품질 모델 또는 인간 직접 판단
```

모델명은 구현 시점의 사용 가능 모델과 비용 정책에 따라 결정한다. 기획 문서에서는 특정 모델에 고정하지 않는다.

---

# 9. 로그 설계 원칙

## 9.1 한국어 로그 우선

OL-Runner가 생산하는 로그는 인간 감수자가 바로 이해할 수 있어야 한다. 따라서 UI에 직접 노출되는 핵심 필드는 한국어로 작성한다.

권장 로그 표기:

```text
작업명
작업 단계
문서 ID
현재 상태
처리 결과
생성 산출물
주의 사항
다음 작업
실패 사유
재실행 가능 여부
인간 확인 필요 여부
```

기계 처리를 위한 key는 영어 snake_case를 유지할 수 있다. 다만 값과 요약문은 한국어를 우선한다.

예:

```text
stage: translate-draft1
stage_label: 1차 번역 생성
summary_ko: 12개 세그먼트의 1차 번역을 생성했습니다.
issues:
  - type: term_uncertainty
    label_ko: 용어 판단 필요
    detail_ko: Paṭiññā의 번역어는 인간 감수에서 확정해야 합니다.
next_action_ko: 원문 대조 검토를 실행하세요.
```

## 9.2 로그는 대화가 아니라 실행 기록

Paperclip의 대화형 로그와 달리 OL-Runner 로그는 실행 기록이어야 한다.

필수 성격:

```text
- 짧고 확인 가능해야 한다.
- 입력 파일과 출력 파일이 명확해야 한다.
- 실패한 경우 어디서 멈췄는지 알 수 있어야 한다.
- OL-DESK 진행/번역/관리 페이지에서 바로 요약 가능해야 한다.
```

---

# 10. Contents-Asset 통합 원칙

OL-Runner는 Contents-Asset을 단일 데이터 소스로 사용한다.

필수 출력 대상:

```text
data/status/{doc_id}.json
assets/source/normalized/{doc_id}.md
data/segments/{doc_id}.json
outputs/manuscripts/draft1/{doc_id}.md
outputs/manuscripts/draft2/{doc_id}.md
outputs/manuscripts/draft3/{doc_id}.md
outputs/manuscripts/draft4/{doc_id}.md
data/terms/terms.json
data/annotations/annotations.json
data/tags/tags.json
data/revisions/{doc_id}.json
data/notes/{doc_id}.json
logs/agent-logs/{doc_id}/{date}_{stage}.json
handoff/draft3/{doc_id}.json
handoff/revision/{doc_id}.json
outputs/exports/individual/{doc_id}.md
```

기존 `agent-logs` 폴더명은 당장 변경하지 않는다. 다만 내부 로그에는 `runner_id`, `runner_version`, `stage_label`, `summary_ko` 같은 필드를 추가할 수 있다.

장기적으로는 다음 중 하나를 검토한다.

```text
안 A: logs/agent-logs 유지
장점: 기존 OL-DESK와 호환 쉬움

안 B: logs/runner-logs 추가
장점: Paperclip 산출물과 OL-Runner 산출물 구분 쉬움
```

초기 MVP에서는 안 A를 권장한다.

---

# 11. 상태 전이 원칙

OL-Runner는 상태 전이를 임의로 건너뛰지 않는다.

기본 상태 흐름:

```text
source_ready
source_normalized
reference_ready
term_candidates_done
draft1_done
source_review_done
annotation_candidates_done
draft2_done
human_review_ready
human_editing
draft3_handoff_ready
draft3_requested
draft3_generated
final_scan_done
final_review
final_done
revision_needed
```

상태 전이 시 확인할 것:

```text
- 이전 단계 산출물이 존재하는가
- 현재 단계 입력이 충분한가
- 출력 파일이 정상 생성되었는가
- JSON 파싱 가능한가
- 인간 판단이 필요한 항목을 자동 확정하지 않았는가
- 실패 시 상태를 잘못 완료 처리하지 않았는가
```

---

# 12. 코드 설계 원칙

이 문서는 구현 코드를 상세히 정의하지 않는다. 다만 다음 설계 원칙은 반드시 지킨다.

```text
1. stage는 작고 명확한 단위로 나눈다.
2. 각 stage는 입력, 출력, 상태 전이를 명시한다.
3. 같은 stage를 다시 실행해도 데이터가 파괴되지 않아야 한다.
4. 원본 raw 파일은 절대 수정하지 않는다.
5. 파일 저장은 임시 파일 작성 후 교체 방식으로 안전하게 처리한다.
6. JSON은 항상 schema validation 또는 최소 구조 검사를 거친다.
7. LLM 호출 결과는 곧바로 확정하지 않고 검증 단계를 거친다.
8. 비용, 시간, 토큰 사용량을 stage별로 기록한다.
9. 실패한 stage는 재실행 가능해야 한다.
10. 인간 승인 게이트를 자동으로 통과시키지 않는다.
```

특히 중단 후 재개와 중복 실행 방지는 필수다. 번역 작업은 긴 실행이므로 한 번의 실패로 전체 문서가 망가지면 안 된다.

---

# 13. OL-DESK UI/UX 재검토 과제

OL-Runner 도입은 OL-DESK UI/UX에도 큰 변화를 요구한다.

현재 OL-DESK는 Contents-Asset을 읽고 상태, 원고, 후보, 로그를 보여주는 대시보드로 출발했다. 그러나 인간 감수자의 실제 집중도와 효율을 높이려면 번역 화면은 더 근본적으로 바뀌어야 한다.

## 13.1 번역 화면의 중심 전환

현재 번역 화면은 원고 단계별 탭과 보조 패널 중심이다. 앞으로는 다음 UX가 필요하다.

```text
원문 세그먼트
번역문 세그먼트
수정 입력
용어 후보
각주 후보
감수 메모
상태 판단
```

이를 문단/세그먼트 단위로 한 화면에서 볼 수 있어야 한다.

권장 방향:

```text
왼쪽: 원문 세그먼트
가운데: 현재 번역문 또는 수정 가능한 원고
오른쪽: 해당 세그먼트의 용어·각주·메모·리스크
```

또는 좁은 화면에서는 다음 방식으로 전환한다.

```text
세그먼트 카드
  원문
  번역문
  수정 입력
  용어/각주/메모
```

## 13.2 즉시 수정 가능한 원고 UX

인간 감수자는 전체 Markdown textarea보다 문단 단위 수정이 더 효율적일 수 있다.

검토 과제:

```text
- draft3/draft4 전체 편집과 세그먼트별 편집을 어떻게 병행할 것인가
- 세그먼트별 수정이 최종 Markdown에 어떻게 반영되는가
- 원문-번역문 대응이 깨졌을 때 어떻게 표시할 것인가
- 수정 전/후 diff를 어떻게 보여줄 것인가
- 감수자가 보류한 항목을 어떻게 눈에 띄게 유지할 것인가
```

## 13.3 실행과 감수의 분리

OL-DESK에 OL-Runner 실행 버튼을 붙일 수는 있지만, UI의 중심은 실행이 아니라 감수여야 한다.

권장 원칙:

```text
- 실행 버튼은 진행/관리 화면에 둔다.
- 번역 상세 화면은 읽기, 비교, 수정, 판단에 집중한다.
- 실행 로그는 필요할 때 접어서 본다.
- AI 평가도 원고 작업을 방해하지 않도록 보조 패널에 둔다.
```

---

# 14. OL-Runner와 OL-DESK 통합 방향

OL-Runner와 OL-DESK는 직접 강하게 결합하지 않는다.

```text
OL-Runner
= Contents-Asset에 쓴다.

OL-DESK
= Contents-Asset을 읽고 쓴다.
```

이 구조를 유지하면 다음 장점이 있다.

```text
- OL-Runner 구현 언어를 바꿔도 OL-DESK 영향이 작다.
- Paperclip 산출물과 OL-Runner 산출물을 같은 화면에서 비교할 수 있다.
- 테스트 실행과 실제 감수 작업을 분리할 수 있다.
- Git diff로 모든 변화가 추적된다.
```

OL-DESK에 추가할 통합 기능:

```text
- 실행 가능한 다음 stage 표시
- stage 실행 요청 버튼
- 실행 전 입력/출력 프리뷰
- 실행 중 상태 표시
- 실패 로그 표시
- 재실행 버튼
- 비용/시간 요약
- 한국어 로그 요약
- 세그먼트별 원문/번역/수정 패널
```

---

# 15. 위험 요소

## 15.1 품질 일관성 저하

세그먼트 병렬 번역은 빠르지만 문체와 용어 일관성을 해칠 수 있다.

대응:

```text
- 문서 단위 용어 후보를 먼저 만든다.
- 문체 가이드를 stage 입력으로 제공한다.
- 병렬 번역 이후 문서 전체 polish 단계를 둔다.
- 인간 감수 단계에서 보류 용어를 명확히 표시한다.
```

## 15.2 로컬 실행기 복잡도 증가

Paperclip을 제거하면 실행기 유지보수 책임이 로컬 시스템으로 온다.

대응:

```text
- 처음부터 범용 에이전트 프레임워크로 만들지 않는다.
- buddhavamsa 프로젝트의 한 문서 처리에 집중한 MVP로 시작한다.
- stage별 입출력 계약을 먼저 고정한다.
- 실패/재시도/중단 후 재개를 초기 설계에 포함한다.
```

## 15.3 자동화 과신

AI가 생성한 번역문과 후보를 자동 확정하면 프로젝트 품질이 무너질 수 있다.

대응:

```text
- 용어, 각주, 태그는 기본값 candidate 또는 hold로 둔다.
- approved는 인간만 부여한다.
- final_done은 인간 승인 없이는 발생하지 않는다.
- 로그에 인간 확인 필요 여부를 명확히 남긴다.
```

## 15.4 OL-DESK UI 과밀화

실행, 로그, 원문, 번역문, 용어, 각주, 태그, 메모가 한 화면에 몰리면 감수 집중도가 떨어진다.

대응:

```text
- 번역 화면은 원문/번역/수정에 집중한다.
- 실행과 운영 진단은 진행/관리 화면으로 분리한다.
- 보조 정보는 접힘 패널과 세그먼트별 컨텍스트로 제한한다.
```

---

# 16. 검토해야 할 과제

OL-Runner 설계 확정 전 확인할 과제는 다음이다.

```text
1. stage별 필수 입력과 출력 정의
2. 현재 Contents-Asset 스키마의 보완 필요성
3. runner-log와 agent-log 통합 방식
4. 한국어 로그 필드 표준
5. 모델 라우팅 기준
6. 세그먼트 분할 기준
7. 세그먼트 병렬 번역 후 문체 통일 방식
8. 비용/토큰 측정 방식
9. 실패 후 재개 방식
10. OL-DESK에서 실행 버튼을 둘 위치
11. 세그먼트별 원문/번역/수정 UI 구조
12. Paperclip 산출물과 OL-Runner 산출물 구분 방식
```

---

# 17. 개발 로드맵

## Phase 0. 기획 정리

```text
- Paperclip 제거 방향 확정
- OL-Runner stage 목록 확정
- 기존 A01~A07/B01~B04 문서를 stage spec으로 재정리
- 한국어 로그 필드 초안 작성
- OL-DESK 세그먼트 중심 번역 UX 재설계
```

## Phase 1. 읽기 전용 Runner 프로토타입

```text
- 프로젝트와 문서 상태 읽기
- 실행 가능한 다음 stage 계산
- dry-run 로그 생성
- OL-DESK 관리/진행 화면에서 dry-run 결과 확인
```

## Phase 2. A01~A04 최소 실행

```text
- normalize-source
- split-reference
- extract-terms
- translate-draft1
- 표준 산출물 저장
- 한국어 runner-log 생성
- Paperclip 산출물과 품질/시간/비용 비교
```

## Phase 3. A05~A07 확장

```text
- review-source-alignment
- propose-annotations
- polish-draft2
- draft2_done 상태 전이
- OL-DESK에서 세그먼트별 원문/번역 비교
```

## Phase 4. Human Review 통합

```text
- draft3 수정 흐름 정리
- 세그먼트별 수정 UI 도입
- 용어/각주/태그 승인 UX 개선
- draft3 handoff 생성 고도화
```

## Phase 5. B라인/최종 산출물

```text
- generate-draft3
- review-final-scan
- draft4 저장
- final_done 승인
- exports 생성
- revision handoff 추적
```

## Phase 6. 운영 안정화

```text
- 실패 재시도
- 중단 후 재개
- 비용/토큰 대시보드
- runner evaluation
- 스키마 validation
- 전체 프로젝트 배치 실행
```

---

# 18. 결론

OL-Runner는 Paperclip 기반 실험에서 얻은 역할 정의와 데이터 구조를 버리지 않으면서, 실제 번역 생산 단계의 속도와 비용 문제를 해결하기 위한 다음 단계다.

핵심 방향은 다음이다.

```text
Paperclip 회사형 에이전트 구조는 폐기한다.
Contents-Asset 산출물 계약은 유지한다.
OL-DESK는 인간 감수자 중심 UX로 계속 발전시킨다.
OL-Runner는 로컬에서 빠르고 예측 가능한 번역 실행을 담당한다.
로그와 경고는 한국어 중심으로 기록해 인간 감수자가 바로 판단할 수 있게 한다.
```

최종 목표는 AI가 조직처럼 행동하는 시스템이 아니다. 최종 목표는 인간 감수자가 원문과 번역문을 더 정확하고 빠르게 검토할 수 있는 로컬 번역 운영체제다.
