# 1차 원고 자가 검증 로그 - gcb-1.1.1.0-Salutation & Intention.md

## 1. 사전 계획(Plan) 수행 상태 (Pass / Fail)

| 단계 | 계획 내용 | 수행 상태 | 비고 / 세부 조치 |
|---|---|---|---|
| Step 1 | `gcb-1.1.1.0-Salutation & Intention.md` 입력 파일 구조 및 용어 매핑 분석 | **Pass** | `gcb-revised-term.md` 용어집 사전 분석 및 매핑 설계 완료 |
| Step 2 | YAML Frontmatter 및 tagAliases 작성 | **Pass** | 이중 인용부호, 하이픈이 들어간 표준 접두사 태그 및 diacritics 유지한 앨리어스 작성 완료 |
| Step 3 | 1차 번역 본문 수행 및 문단별 1:1 `[KO]` 적용 | **Pass** | 본문 7개 문단에 대해 1:1 대응하여 `[KO]...[/KO]` 개별 줄 래핑 완료 |
| Step 4 | 하단 각주 통합 `[KO]` 래핑 및 각주 정의 간 단일 빈 줄 적용 | **Pass** | 신규 각주 규칙에 따라 한국어 번역 각주를 파일 맨 아래 단일 `[KO]` 블록으로 통합하고 정의 사이에 빈 줄 적용 완료 |
| Step 5 | AI 모델 자체검증 체크리스트 수행 및 로그 생성 | **Pass** | 5단계 체크리스트 검증을 통과하여 본 로그 파일을 생성함 |

---

## 2. 5단계 자체 검증 체크리스트

### Step 1: 1:1 문단 정렬 (1:1 Paragraph Alignment)
- [x] 영어 원문 문단과 한국어 번역 문단이 1:1로 대응되고 누락이 없는가?
  - 본문 총 7개 단락(Anudīpanī 안내, 장 제목 주석, 불법승 예경 3개 단락, 서원 1개 단락, 축원 1개 단락) 모두 1:1로 배치됨.

### Step 2: `[KO]` 감쌈 마크업 준수 ([KO] Wrap Markers)
- [x] 한국어 번역이 `[KO]`와 `[/KO]` 마커로 올바르게 감싸져 있는가?
- [x] 마커가 각각 단독 줄을 차지하고 있는가?
  - 본문 각 한국어 단락이 단독 줄에 기재된 `[KO]`와 `[/KO]`로 올바르게 래핑됨.

### Step 3: 용어집 준수 여부 (Glossary Compliance)
- [x] `gcb-revised-term.md`에 정의된 공식 용어들이 올바르게 사용되었는가?
  - `Salutation & Intention` -> `부처님께 올리는 예경과 이 책을 쓰는 뜻`
  - `Mahā Buddhavaṃsa` -> `마하 붓다왐사(Mahā Buddhavaṃsa, 위대한 부처님들의 연대기)`
  - `Dhamma` -> `법(Dhamma)`
  - `Sangha` -> `승가(Sangha)`
  - `definite prophecy` -> `확정적 예언(수기)`
  - `Hermit Sumedha` -> `수메다(Sumedha) 수행자`
  - `Buddhavaṃsa` -> `붓다왐사(Buddhavaṃsa)`
  - `morality (*sīla*)` -> `지계(*sīla*)`
  - `concentration (*samādhi*)` -> `선정(*samādhi*)`
  - `insight (*paññā*)` -> `지혜(*paññā*)`

### Step 4: 태그 및 앨리어스 형식 (Tag & Alias Formats)
- [x] YAML Frontmatter의 `tags` 및 `tagAliases` 형식이 규정에 맞는가?
  - 다중 태그와 앨리어스가 하이픈(`-`) 구분 및 이중 인용부호(`"`)로 적절히 감싸져 있음. Pāli 표기의 diacritics(`Dīpaṅkara`, `Buddhavaṃsa`, `paṭiññā`)도 임의 제거 없이 원형 그대로 유지함.

### Step 5: 각주 변환 및 통합 래핑 검증 (Footnote Check)
- [x] 기존 레거시 각주(`[*Note on chapter title]`, `[2]~[8]`)가 마크다운 각주(`[^2]~[^8]`)로 제대로 교체되었는가?
  - 장 제목 주석은 문단 수준으로 변환하여 번역하고, 본문 내 참조와 하단 각주 번호 `[^2]~[^8]`가 정확히 1:1로 대응됨.
- [x] 한국어 각주 전체가 파일 하단에 단 하나의 `[KO]...[/KO]`로 통합 래핑되었는가?
- [x] `[KO]` 통합 블록 내부에 각주 식별 기호(`[^2]:` 등)가 정상 포함되어 있는가?
- [x] 각 각주 정의 사이에 단일 빈 줄이 유지되어 있는가?
  - 모든 항목 검증 통과 완료.

---

## 3. 신규 및 변경 용어 후보 정리

* 특이사항 없음. 용어집 규격 준수함.

## 4. 해석이 모호하거나 보완이 필요한 부분

* **Adoration / Obeisance**: `With most respectful adoration, I pay obeisance to`를 1차 번역의 의미 보존 원칙에 따라 지나친 미사여구 없이 "가장 공경하는 마음으로 예경을 올리며, 나는 ~에 절을 올립니다"로 직역에 준하여 번역하였습니다.
* **Ganges [6] 각주**: 원문의 Pāli 게송 중 `Gaṅgā` 부분의 diacritics가 누락되어 `Ganga`로 된 부분을 주석 내에서 교정하고 주석 번역을 자연스럽게 반영하였습니다.
