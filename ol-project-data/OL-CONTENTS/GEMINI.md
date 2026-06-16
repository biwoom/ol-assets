# Antigravity IDE Rules for BuddhaStory Translation Project

You are operating within the BuddhaStory Translation Project repository. As an AI Agent, you must strictly follow the translation workflow, terminology control, frontmatter syntax, and logging rules defined below.

---

## 📖 Mandatory Reading

Before performing any translation or text modification tasks, you MUST read the primary instruction manual:
* Primary Reference: [UBTF-GLOBAL-MANUAL.md](file:///Users/damjin/Projects/ol-project/github/ol-assets/ol-project-data/OL-CONTENTS/UBTF-GLOBAL-MANUAL.md)
* Language Reference: [lang-en.md](file:///Users/damjin/Projects/ol-project/github/ol-assets/ol-project-data/OL-CONTENTS/translation/translation-guides/lang-en.md)
* Project Reference: [PROJECT-GUIDE.md](file:///Users/damjin/Projects/ol-project/github/ol-assets/ol-project-data/OL-CONTENTS/translation/en-kr/BuddhaStory/PROJECT-GUIDE.md)

---

## 📜 Core Workflow Rules

### 1. Pre-task Planning Requirement
- **CRITICAL**: Before beginning any translation or document modification task, you MUST establish a detailed step-by-step implementation plan (Plan) based on the manuscript production workflow and present it to the user.
- Proceed to execution only after aligning the plan with the user.

### 2. File Modification Constraints
- **NEVER** edit files in `source/raw/en/BuddhaStory/src-01-gcb-revised/` (Read-only source) or `translation/en-kr/BuddhaStory/draft-3/` (Human review path).
- Modify files in `translation/en-kr/BuddhaStory/draft-1/` for 1st drafts, and `translation/en-kr/BuddhaStory/draft-2/` for 2nd drafts.

### 3. Translation Paragraph Structure & Style
- Keep the original English paragraph intact.
- Place the Korean translation immediately below the corresponding English paragraph. The structure must be a strict 1:1 paragraph-by-paragraph mapping.
- **Heading Translation**: You MUST translate the main title and all subheadings (h1~h5: `#`, `##`, `###`, `####`, `#####`) inside a `[KO]...[/KO]` block immediately below the original English heading. For the main document title, reference the official Korean translation in `BuddhaStory/toc/gcb-kr-TOC.md`.
- **Translation Extraction Tags**: Wrap the Korean translation paragraph inside `[KO]` and `[/KO]` markers on separate lines, like so:
  ```markdown
  Original English paragraph here.

  [KO]
  한국어 번역 문단은 여기에 위치합니다.
  [/KO]
  ```
- **Translation Guidelines by Stage**:
  - **1st Draft (Academic/Scholarly Translation)**: Target audience is Buddhist experts and scholars. Not a simple word-for-word translation, but a translation prioritizing academic and doctrinal rigor. Allows full use of Buddhist terminology. Translates English sentence flow into natural Korean expressions and sentences without translationese. All headings (h1-h5) in the body must be translated, with the main title referenced against `gcb-kr-TOC.md`.
  - **2nd Draft (Everyday/Readable Translation)**: Target audience is the general public in Korea (high school level and above). Minimal Buddhist terminology; jargon is replaced with everyday Korean. Focuses on readability and ease of understanding rather than the academic rigor of the original text. All headings must also be translated in a highly readable everyday Korean format.
- Replace legacy Wiki-style footnotes (e.g., `[*1]`, `{{주석}}`) with standard markdown footnotes (`[^1]`) placed at the bottom of the file.
- **Footnote Identifiers Inside Integrated [KO] Block**: To prevent footnote link loss during Korean-only manuscript extraction, you must wrap all Korean footnotes inside a single `[KO]...[/KO]` block at the bottom of the file. Inside this block, include the footnote identifiers (e.g., `[^1]:`) for each footnote. To ensure rendering compatibility and readability, maintain a single blank line between each footnote definition.

  Example:
  ```markdown
  [^1]: Original English footnote 1.
  [^2]: Original English footnote 2.

  [KO]
  [^1]: 한국어 번역 1.

  [^2]: 한국어 번역 2.
  [/KO]
  ```


### 4. Vocabulary Control & Verification Process
- Do NOT perform pre-translation glossary extraction. Instead, proceed with the translation directly while adhering to the existing cumulative glossary `gcb-revised-term.md`.
- **New Term Extraction**: Prior to translating, extract any new terms (personal names, places, scriptures, or concepts not yet in `gcb-revised-term.md`) from the source document. Save these terms in a new markdown document at `term/en-kr/BuddhaStory/[filename]-term.md`.
- **Autonomous Progress**: Once the new term document is created, do NOT wait for user approval. Proceed immediately to translate the rest of the manuscript and execute the remaining workflow using both the cumulative glossary and your newly extracted terms.
- If you establish any new terms or better translation alternatives during translation, apply them to the manuscript directly and summarize them in the post-translation self-validation log under `log/en-kr/BuddhaStory/draft-1/` or `draft-2/`.
- Once human reviewers approve the log, the new/updated terms will be merged into `gcb-revised-term.md`.

### 5. Tagging & Aliasing Convention
- Use YAML Frontmatter with double-quoted, hyphenated tags:
  ```yaml
  tags:
    - "인물/고따마-부처님"
    - "장소/강가-강"
  ```
- Map alternate names, Pali, Sanskrit, English, and Hanja translations using `tagAliases` to ensure high searchability:
  ```yaml
  tagAliases:
    "인물/고따마-부처님": ["Gotama", "Gautama", "Gotama Buddha", "석가모니", "釋迦牟尼"]
  ```
- **CRITICAL**: Do not remove diacritics or simplify letters in `tagAliases` (e.g., keep `Dīpaṅkara`, `Paṭiññā`). Use the original casing and diacritics.

### 6. Self-Validation & Korean Logging
- **1st Draft Validation & Tool Automation (Required)**:
  Before submitting or finishing any 1st draft translation, you MUST execute:
  1. **Pre-processing**: Run `run_pipeline.py --preprocess` on the target draft file to normalize markdown footnotes.
     `python3 scripts/run_pipeline.py --preprocess <file_path>`
  2. **Verification & Log Generation**: Run `run_pipeline.py --validate` to perform both the glossary compliance check and the structural 5-step checklist, which automatically generates the mandatory log file under `log/en-kr/BuddhaStory/draft-1/[filename]-log.md`.
     `python3 scripts/run_pipeline.py --validate <file_path>`
- **2nd Draft Validation & Tool Automation (Required)**:
  Before finalizing any 2nd draft (윤문) translation, you MUST execute:
  1. **Environment Setup & Term Polishing**: Run `run_pipeline.py --init-draft2` to copy the 1st draft to `draft-2/` and add 2nd draft term recommendation templates in `term/en-kr/BuddhaStory/[filename]-term.md`.
     `python3 scripts/run_pipeline.py --init-draft2 <draft1_file_path>`
  2. **Verification & Log Generation (and draft-3 copy)**: Run `run_pipeline.py --validate-draft2` to perform the 2nd draft checklist, generate the mandatory log file under `log/en-kr/BuddhaStory/draft-2/[filename]-draft2-log.md`, and copy the validated file to the `draft-3/` directory for human review.
     `python3 scripts/run_pipeline.py --validate-draft2 <draft2_file_path>`
  3. **Workflow Self-Evolution**: Run `run_pipeline.py --upgrade-workflow` on the generated draft2 log file to automatically apply structural feedback to rule manuals.
     `python3 scripts/run_pipeline.py --upgrade-workflow log/en-kr/BuddhaStory/draft-2/<draft2_log_file_path>`
- **3rd Draft Finalization & Tool Automation (Required)**:
  Before finalizing any 3rd draft translation, you MUST execute:
  1. **Final Korean Extraction**: Run `run_pipeline.py --extract-final` on the finalized `draft-3` file to extract the clean Korean-only manuscript directly to `outputs/manuscripts/en-kr/BuddhaStory/`.
     `python3 scripts/run_pipeline.py --extract-final <draft3_file_path>`

### 7. Large File Splitting Rules
- For large documents that may exceed model context limits or cause translation omission, you MUST physically split the manuscript into separate sub-files before translation and establish a detailed plan for them.
- Save the split files with sequential suffixes: e.g., `-1`, `-2`, `-3`.
  - Original: `gcb-kr-005-the-rare-appearance-of-a-buddha.md`
  - Split: `gcb-kr-005-1-the-rare-appearance-of-a-buddha.md`, `gcb-kr-005-2-the-rare-appearance-of-a-buddha.md`, `gcb-kr-005-3-the-rare-appearance-of-a-buddha.md`

### 8. Empty File Translation Exception (Bypass) Rule
- **Exception for Empty Files**: If a source document has no actual body text and only contains a title (e.g., `# Chapter 2 - ...`), the `## 본문` header, and a cross-reference line (e.g., `[For the Anudīpanī on this chapter...]`), you MUST bypass the translation.
- **Automated Exception Logging**: To ensure no documents are mistakenly bypassed without record, you MUST run the helper script `run_pipeline.py --validate <file_path>`. The script will automatically detect the empty content, bypass the translation and helper processes, and generate the mandatory validation log file under `log/en-kr/BuddhaStory/draft-1/[filename]-log.md` with the bypass reason (e.g., "본문 내용이 없는 빈 문서이므로 번역 예외 처리함").

### 9. Workflow Self-Evolution (자가 진화 규칙)
- **Rule Adaptation**: You MUST record any formatting constraints, parsing bugs, or style exceptions discovered during translation under `## 8. 워크플로우 개선 및 시스템 자가 업그레이드 사항` in your `draft2-log.md`.
- **System Patches**: By executing `run_pipeline.py --upgrade-workflow`, the pipeline will automatically parse your feedback. Rule changes marked as `[룰문서]` will be appended to rule manuals (`GEMINI.md`, `UBTF-GLOBAL-MANUAL.md`, `SKILL.md`) in a dedicated `Self-Upgrade History` section. You must actively run this workflow upgrade step to ensure the system evolves iteratively.

## 🔄 워크플로우 자가 개정 이력 (Self-Upgrade History)

- **[2026-06-12]** (from `gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha-draft2-log.md`):
  - 2차 윤문 검증 시 다구(Pali) 단어 뒤 괄호 병기 생략 예외 추가

- **[2026-06-12]** (from `gcb-1.1.2.2-Bodhisatta (a future Buddha)-draft2-log.md`):
  - 2차 윤문 환경 세팅 시 1차에서 추출된 신규 용어집에 반드시 2차 번역어(2차 :)를 작성한 후 번역에 반영할 것

- **[2026-06-12]** (from `gcb-1.1.1.0-Salutation & Intention-draft2-log.md`):
  - 2차 윤문 시 교학설명 외의 서사 문맥에서 Dhamma는 '법' 외에 '가르침' 또는 '가르침(Dhamma)'으로 유연하게 번역할 수 있음

- **[2026-06-12]** (from `gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha-draft2-log.md`):
  - 2차 윤문 검증 시 복합어(예: brother-in-law) 혹은 인명의 일부(예: Pakudha Kaccāyana)가 단독 단어 용어집 검사에서 오탐지로 경고를 발생시킬 경우 예외로 허용함

- **[2026-06-13]** (from `gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha-draft2-log.md`):
  - 2차 윤문 검증 시 복합어(예: brother-in-law) 혹은 인명의 일부(예: Pakudha Kaccāyana)가 단독 단어 용어집 검사에서 오탐지로 경고를 발생시킬 경우 예외로 허용함
