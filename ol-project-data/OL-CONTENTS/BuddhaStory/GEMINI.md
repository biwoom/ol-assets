# Antigravity IDE Rules for BuddhaStory Translation Project

You are operating within the BuddhaStory Translation Project repository. As an AI Agent, you must strictly follow the translation workflow, terminology control, frontmatter syntax, and logging rules defined below.

---

## 📖 Mandatory Reading

Before performing any translation or text modification tasks, you MUST read the primary instruction manual:
* Primary Reference: [translation-agent-manual.md](file:///Users/damjin/Projects/ol-project/OL-Project-매뉴얼/CONTENTS/BuddhaStory/translation-agent-manual.md)

---

## 📜 Core Workflow Rules

### 1. Pre-task Planning Requirement
- **CRITICAL**: Before beginning any translation or document modification task, you MUST establish a detailed step-by-step implementation plan (Plan) based on the manuscript production workflow and present it to the user.
- Proceed to execution only after aligning the plan with the user.

### 2. File Modification Constraints
- **NEVER** edit files in `BuddhaStory/source/raw/src-01-gcb/` (Read-only source) or `BuddhaStory/edit/gcb-kr/draft-3/` (Human review path).
- Modify files in `BuddhaStory/edit/gcb-kr/draft-1/` for 1st drafts, and `BuddhaStory/edit/gcb-kr/draft-2/` for 2nd drafts.

### 3. Translation Paragraph Structure & Style
- Keep the original English paragraph intact.
- Place the Korean translation immediately below the corresponding English paragraph. The structure must be a strict 1:1 paragraph-by-paragraph mapping.
- **Translation Extraction Tags**: Wrap the Korean translation paragraph inside `[KO]` and `[/KO]` markers on separate lines, like so:
  ```markdown
  Original English paragraph here.

  [KO]
  한국어 번역 문단은 여기에 위치합니다.
  [/KO]
  ```
- **Translation Guidelines by Stage**:
  - **1st Draft (Current)**: Focus on preserving the original structure and meaning as a verifiable base draft. Follow these rules:
    1. Preserve the original information order and logical structure as much as possible.
    2. Long sentences can be split into two, but do not alter relationships (causal, modifying, subject-verb).
    3. Do not arbitrarily modernize Buddhist terminology, names, places, or scriptures.
    4. Limit word order adjustments to cases where Korean is highly unnatural.
    5. Record uncertain translations in the work log instead of guessing.
    6. Preserve meaningful repetitive expressions.
    7. Translate negatives, conditionals, comparatives, and causals with extra care.
    8. Use modern written Korean with `~다` endings as the default style.
    9. Honorifics can be used for Buddha, Bodhisattvas, Elders, Sayadaws, etc., without adding excessive embellishments.
  - **2nd Draft (Future)**: Shift to a contextual refinement (70% contextual and 30% literal translation ratio) for enhanced readability and flow.
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
- **New Term Extraction**: Prior to translating, extract any new terms (personal names, places, scriptures, or concepts not yet in `gcb-revised-term.md`) from the source document. Save these terms in a new markdown document at `BuddhaStory/term/[filename]-term.md`.
- **Autonomous Progress**: Once the new term document is created, do NOT wait for user approval. Proceed immediately to translate the rest of the manuscript and execute the remaining workflow using both the cumulative glossary and your newly extracted terms.
- If you establish any new terms or better translation alternatives during translation, apply them to the manuscript directly and summarize them in the post-translation self-validation log under `BuddhaStory/log/draft-1/` or `draft-2/`.
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
     `python3 BuddhaStory/skills/buddha-translation-helper/scripts/run_pipeline.py --preprocess <file_path>`
  2. **Verification & Log Generation**: Run `run_pipeline.py --validate` to perform both the glossary compliance check and the structural 5-step checklist, which automatically generates the mandatory log file under `BuddhaStory/log/draft-1/[filename]-log.md`.
     `python3 BuddhaStory/skills/buddha-translation-helper/scripts/run_pipeline.py --validate <file_path>`
- **2nd Draft Validation & Tool Automation (Required)**:
  Before finalizing any 2nd draft (윤문) translation, you MUST execute:
  1. **Environment Setup & Term Polishing**: Run `run_pipeline.py --init-draft2` to copy the 1st draft to `draft-2/` and add 2nd draft term recommendation templates in `term/[filename]-term.md`.
     `python3 BuddhaStory/skills/buddha-translation-helper/scripts/run_pipeline.py --init-draft2 <draft1_file_path>`
  2. **Verification & Log Generation (and draft-3 copy)**: Run `run_pipeline.py --validate-draft2` to perform the 2nd draft checklist, generate the mandatory log file under `BuddhaStory/log/draft-2/[filename]-draft2-log.md`, and copy the validated file to the `draft-3/` directory for human review.
     `python3 BuddhaStory/skills/buddha-translation-helper/scripts/run_pipeline.py --validate-draft2 <draft2_file_path>`
  3. **Workflow Self-Evolution**: Run `run_pipeline.py --upgrade-workflow` on the generated draft2 log file to automatically apply structural feedback to rule manuals.
     `python3 BuddhaStory/skills/buddha-translation-helper/scripts/run_pipeline.py --upgrade-workflow BuddhaStory/log/draft-2/<draft2_log_file_path>`

### 7. Large File Splitting Rules
- For large documents that may exceed model context limits or cause translation omission, you MUST physically split the manuscript into separate sub-files before translation and establish a detailed plan for them.
- Save the split files with sequential suffixes: e.g., `-1`, `-2`, `-3`.
  - Original: `gcb-kr-005-the-rare-appearance-of-a-buddha.md`
  - Split: `gcb-kr-005-1-the-rare-appearance-of-a-buddha.md`, `gcb-kr-005-2-the-rare-appearance-of-a-buddha.md`, `gcb-kr-005-3-the-rare-appearance-of-a-buddha.md`

### 8. Empty File Translation Exception (Bypass) Rule
- **Exception for Empty Files**: If a source document has no actual body text and only contains a title (e.g., `# Chapter 2 - ...`), the `## 본문` header, and a cross-reference line (e.g., `[For the Anudīpanī on this chapter...]`), you MUST bypass the translation.
- **Automated Exception Logging**: To ensure no documents are mistakenly bypassed without record, you MUST run the helper script `run_pipeline.py --validate <file_path>`. The script will automatically detect the empty content, bypass the translation and helper processes, and generate the mandatory validation log file under `BuddhaStory/log/draft-1/[filename]-log.md` with the bypass reason (e.g., "본문 내용이 없는 빈 문서이므로 번역 예외 처리함").

### 9. Workflow Self-Evolution (자가 진화 규칙)
- **Rule Adaptation**: You MUST record any formatting constraints, parsing bugs, or style exceptions discovered during translation under `## 8. 워크플로우 개선 및 시스템 자가 업그레이드 사항` in your `draft2-log.md`.
- **System Patches**: By executing `run_pipeline.py --upgrade-workflow`, the pipeline will automatically parse your feedback. Rule changes marked as `[룰문서]` will be appended to rule manuals (`GEMINI.md`, `translation-agent-manual.md`, `SKILL.md`) in a dedicated `Self-Upgrade History` section. You must actively run this workflow upgrade step to ensure the system evolves iteratively.

## 🔄 워크플로우 자가 개정 이력 (Self-Upgrade History)

- **[2026-06-12]** (from `gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha-draft2-log.md`):
  - 2차 윤문 검증 시 다구(Pali) 단어 뒤 괄호 병기 생략 예외 추가

- **[2026-06-12]** (from `gcb-1.1.2.2-Bodhisatta (a future Buddha)-draft2-log.md`):
  - 2차 윤문 환경 세팅 시 1차에서 추출된 신규 용어집에 반드시 2차 번역어(2차 :)를 작성한 후 번역에 반영할 것

- **[2026-06-12]** (from `gcb-1.1.1.0-Salutation & Intention-draft2-log.md`):
  - 2차 윤문 시 교학설명 외의 서사 문맥에서 Dhamma는 '법' 외에 '가르침' 또는 '가르침(Dhamma)'으로 유연하게 번역할 수 있음

- **[2026-06-12]** (from `gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha-draft2-log.md`):
  - 2차 윤문 검증 시 복합어(예: brother-in-law) 혹은 인명의 일부(예: Pakudha Kaccāyana)가 단독 단어 용어집 검사에서 오탐지로 경고를 발생시킬 경우 예외로 허용함
