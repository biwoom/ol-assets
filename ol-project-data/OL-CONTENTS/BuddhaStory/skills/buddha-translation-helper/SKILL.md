# Skill: buddha-translation-helper

이 스킬은 붓다왐사 번역 작업 중 마크다운 각주 변환, 용어집 검사, 번역 품질 검증, 작업 로그 생성 및 시스템 가이드라인 규칙의 자가 업그레이드(진화)를 하나의 통합 관리 도구(`run_pipeline.py`)로 일원화하여 실행할 수 있는 자동화 도구 모음입니다.

---

## 📂 스킬 구조 및 파일

이 스킬은 `BuddhaStory/skills/buddha-translation-helper/` 하위에 위치하며 다음과 같이 구성됩니다.

1. **`SKILL.md`** (본 문서): 스킬 정의 및 통합 가이드
2. **`scripts/run_pipeline.py`**: 전처리, 최종 검증 및 자가 업그레이드 단계를 일괄 제어하는 원스톱 파이프라인 관리자
3. **`scripts/format_footnotes.py`**: 위키 주석 변환 및 한국어 각주 통합 래핑 전처리 도구
4. **`scripts/lint_glossary.py`**: `gcb-revised-term.md` 용어집 준수 검사 린터
5. **`scripts/validate_translation.py`**: 1차 및 2차 정렬/각주 검증 및 자가 검증 로그 생성기

---

## 🚀 워크플로우별 실행 가이드

번역 에이전트는 통합 관리 도구(`run_pipeline.py`)를 사용하여 번역 단계별 라이프사이클을 관리합니다.

### [1차 번역 라이프사이클]

#### 1단계: 번역 전처리 (--preprocess)
번역 대상 파일에 대해 레거시 주석(`[*1]`, `{{주석}}`)을 표준 마크다운 각주(`[^1]`)로 자동 교정하고 하단의 각주 정의부 포맷을 정형화합니다.
```bash
python3 BuddhaStory/skills/buddha-translation-helper/scripts/run_pipeline.py --preprocess BuddhaStory/edit/gcb-kr/draft-1/[대상파일명].md
```
*참고: 입력 파일에 실제 본문이 없는 빈 문서로 판명되면, 실행 즉시 바이패스가 감지되어 `log/draft-1/` 폴더에 즉시 예외 처리 로그를 자동 생성하고 처리를 완료합니다.*

#### 2단계: 번역 수행
1차 번역 규칙에 따라 영어 문단 바로 아래에 `[KO]` 번역 문단을 1:1로 추가합니다.

#### 3단계: 통합 검증 및 로그 생성 (--validate)
번역 완료 후 용어집 검사(린팅)와 구조 정합성 검수를 일괄 처리하고, 이상 없을 시 1차 자가 검증 로그 파일(`BuddhaStory/log/draft-1/[대상파일명]-log.md`)을 자동 생성합니다.
```bash
python3 BuddhaStory/skills/buddha-translation-helper/scripts/run_pipeline.py --validate BuddhaStory/edit/gcb-kr/draft-1/[대상파일명].md
```

---

### [2차 윤문 라이프사이클]

#### 1단계: 2차 윤문 환경 세팅 및 용어 고도화 (--init-draft2)
1차 번역 파일을 `draft-2/`로 복사하고 용어집 파일(`term/[대상파일명]-term.md`)에 `2차 :` 서식을 추가해 템플릿화합니다.
```bash
python3 BuddhaStory/skills/buddha-translation-helper/scripts/run_pipeline.py --init-draft2 BuddhaStory/edit/gcb-kr/draft-1/[대상파일명].md
```

#### 2단계: 2차 윤문 수행
`draft-2/` 폴더에 생성된 원고의 `[KO]` 마크업 내부를 2차 문체 가이드라인에 맞춰 유려하게 수정합니다.

#### 3단계: 2차 통합 검증, 2차 로그 생성 및 draft-3 복사 (--validate-draft2)
2차 원고의 포맷을 검수하고, 2차 전용 자가 검증 로그 파일(`BuddhaStory/log/draft-2/[대상파일명]-draft2-log.md`)을 자동 생성합니다. 또한 검증 성공 시 인간 감수자의 최종 검토를 위해 원고를 `BuddhaStory/edit/gcb-kr/draft-3/` 폴더로 자동 복사합니다.
```bash
python3 BuddhaStory/skills/buddha-translation-helper/scripts/run_pipeline.py --validate-draft2 BuddhaStory/edit/gcb-kr/draft-2/[대상파일명].md
```

#### 4단계: 워크플로우 자가 업그레이드 (--upgrade-workflow)
2차 자가 검증 로그 내의 피드백 사항을 분석하여 룰 문서(`GEMINI.md`, 매뉴얼 등)를 스스로 개정/갱신합니다.
```bash
python3 BuddhaStory/skills/buddha-translation-helper/scripts/run_pipeline.py --upgrade-workflow BuddhaStory/log/draft-2/[대상파일명]-draft2-log.md
```

## 🔄 워크플로우 자가 개정 이력 (Self-Upgrade History)

- **[2026-06-12]** (from `gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha-draft2-log.md`):
  - 2차 윤문 검증 시 다구(Pali) 단어 뒤 괄호 병기 생략 예외 추가

- **[2026-06-12]** (from `gcb-1.1.2.2-Bodhisatta (a future Buddha)-draft2-log.md`):
  - 2차 윤문 환경 세팅 시 1차에서 추출된 신규 용어집에 반드시 2차 번역어(2차 :)를 작성한 후 번역에 반영할 것

- **[2026-06-12]** (from `gcb-1.1.1.0-Salutation & Intention-draft2-log.md`):
  - 2차 윤문 시 교학설명 외의 서사 문맥에서 Dhamma는 '법' 외에 '가르침' 또는 '가르침(Dhamma)'으로 유연하게 번역할 수 있음

- **[2026-06-12]** (from `gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha-draft2-log.md`):
  - 2차 윤문 검증 시 복합어(예: brother-in-law) 혹은 인명의 일부(예: Pakudha Kaccāyana)가 단독 단어 용어집 검사에서 오탐지로 경고를 발생시킬 경우 예외로 허용함
