# Work Log

## 2026-06-13 (Explicit Draft-3 Editing Rule)

- Updated Codex operating role again to match the user's latest requested workflow.
  - Codex remains outside primary 1st/2nd draft production.
  - When the user provides a specific BuddhaStory document path and asks for `3차번역작업 시작` or equivalent 3rd-stage work, Codex should edit that specified draft-3 file directly.
  - Active paths now follow the UBTF layout: `translation/en-kr/BuddhaStory/`, `term/en-kr/BuddhaStory/`, `term/cumulative/`, `log/en-kr/BuddhaStory/`, and `outputs/manuscripts/en-kr/BuddhaStory/`.
  - Draft-3 reviewer notes and terminology decisions should be written into the target document's `[review]...[/review]` block.
  - Separate final-review documents, draft-3 term-file recommendations, and final Korean-only extraction are no longer default parts of Codex 3rd-stage work.
- Updated `AGENTS.md`, `.agents/context/current-state.md`, and `.agents/context/decisions.md` to make this rule the active default.
- Added the explicit draft-3 style rule: write for ordinary Korean readers, use natural modern Korean, and replace Buddhist technical terms with everyday Korean by default unless doctrinal precision requires retention.

## 2026-06-13 (Codex Role Realignment)

- Updated Codex operating role to match the revised BuddhaStory workflow.
  - Codex CLI is now a human-review consultation and final-polishing assistance agent.
  - Codex no longer participates directly in 1st, 2nd, or 3rd production workflows by default.
  - Gemini / existing production pipeline remains responsible for 1st draft, 2nd draft, draft-3 copy, workflow validation, and final Korean-only extraction.
  - Human reviewer remains responsible for comparing draft-1 and draft-2 and writing the final 3rd draft.
  - Direct Codex edits to draft files, term files, review logs, or final outputs require an explicit user request.
- Updated `AGENTS.md`, `.agents/context/current-state.md`, and `.agents/context/decisions.md` to remove obsolete Codex-led draft-3 production assumptions.

## 2026-06-13 (Continued - Workflow Overhaul & Heading Translation & Korean Extraction)

- Implemented workflow overhaul as requested:
  - Redefined Stage 1 (Rigorous academic translation for experts) and Stage 2 (Everyday translation for ordinary readers).
  - Modified rule manuals (`AGENTS.md`, `translation-agent-manual.md`, `GEMINI.md`) to integrate these new guidelines.
  - Rewrote Section 7 (1차 번역 규칙) and Section 8 (2차 윤문 규칙) in `translation-agent-manual.md` to fully reflect the experts-only scholarly translation standard and the high-school-level everyday translation standard.
  - Required translation of all titles and headings (h1-h5) in the document body, using official mappings from `gcb-kr-TOC.md`.
  - Created UBTF framework specification documents [UBTF-ARCHITECTURE.md](file:///Users/damjin/Projects/ol-project/github/ol-assets/ol-project-data/OL-CONTENTS/UBTF-ARCHITECTURE.md) and [UBTF-WORKFLOW.md](file:///Users/damjin/Projects/ol-project/github/ol-assets/ol-project-data/OL-CONTENTS/UBTF-WORKFLOW.md) at the root of `OL-CONTENTS/` to define the multi-project layout and multi-language translation pipeline guidelines.
  - Shifted final output directory from `outputs/manuscripts/gcb-kr/final/` to `outputs/manuscripts/gcb-kr/` directly.
  - Implemented and updated `extract_korean.py` to parse bilingual draft-3 documents and generate clean Korean-only markdown manuscripts (preserving YAML, `#`/`##` headings, and Korean footnote definitions, while filtering out English h1-h5 headings).
  - Integrated `--extract-final` command-line mode into `run_pipeline.py`.
  - Updated `.agents/skills/` configurations for `buddha-final-manuscript`, `buddha-draft3-workflow`, and `buddha-draft3-revision`.
  - Validated the new pipeline successfully on `gcb-1.1.1.0-Salutation & Intention.md` and `gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha.md`.

## 2026-06-13 (Earlier)

- Ran full 3rd-stage workflow for `gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha.md`.
  - Revised draft-3 Korean blocks for ordinary-reader readability while preserving source and `[KO]` structure.
  - Added draft-3 terminology recommendations to `BuddhaStory/term/gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha-term.md`.
  - Created reviewer note at `BuddhaStory/log/final-review/gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha-review.md`.
  - Created 4th-stage human-review handoff manuscript at `BuddhaStory/outputs/manuscripts/gcb-kr/final/gcb-1.1.2.1-Singular Opportunity of Living in an Age when a Buddha.md`.
  - Human-review focus: `육사외도` vs `여섯 외도 스승`, `micchādhimokkha` as `미혹된 확신`, and source typo `Pukdha Kaccāyana`.
- Ran full 3rd-stage workflow for `gcb-1.1.2.2-Bodhisatta (a future Buddha).md`.
  - Revised draft-3 Korean blocks for doctrinal clarity and readability, including the incomplete `될 수.` sentence.
  - Added draft-3 terminology recommendations to `BuddhaStory/term/gcb-1.1.2.2-Bodhisatta (a future Buddha)-term.md`.
  - Created reviewer note at `BuddhaStory/log/final-review/gcb-1.1.2.2-Bodhisatta (a future Buddha)-review.md`.
  - Created 4th-stage human-review handoff manuscript at `BuddhaStory/outputs/manuscripts/gcb-kr/final/gcb-1.1.2.2-Bodhisatta (a future Buddha).md`.
  - Human-review focus: `Sammā-Sambodhi`, `Pacceka-Bodhi`, `Vimuttiparipācanīyā Dhamma`, and duplicate source footnotes 11/12.
- Created translation progress checklist at `BuddhaStory/list-check/translation-completion-checklist.md` using `BuddhaStory/edit/gcb-kr/draft-1/` as the source list.

## 2026-06-12

- Ran full 3rd-stage workflow for `gcb-1.1.1.0-Salutation & Intention.md`.
  - Revised draft-3 manuscript for ordinary-reader readability while preserving source and `[KO]` structure.
  - Added draft-3 terminology recommendations to `BuddhaStory/term/gcb-1.1.1.0-Salutation & Intention-term.md`.
  - Created reviewer note at `BuddhaStory/log/final-review/gcb-1.1.1.0-Salutation & Intention-review.md`.
  - Created 4th-stage human-review handoff manuscript at `BuddhaStory/outputs/manuscripts/gcb-kr/final/gcb-1.1.1.0-Salutation & Intention.md`.
  - Human-review focus: `Dhamma` as `가르침` vs `법`, `Path/Fruition` as plain Korean vs `도/과`, and `Dīpaṅkarā`/`Dīpaṅkara` spelling policy.
- Created OL-CONTENTS Codex operating structure under `.agents/`.
- Added project-level `AGENTS.md` for Codex role, safety rules, path conventions, and BuddhaStory workflow.
- Added context documents:
  - `.agents/context/current-state.md`
  - `.agents/context/decisions.md`
  - `.agents/context/work-log.md`
- Created BuddhaStory-specific Codex skills:
  - `$buddha-draft3-revision`
  - `$buddha-term-review`
  - `$buddha-review-log`
  - `$buddha-final-manuscript`
- Created `BuddhaStory/log/final-review/` as the location for Codex reviewer-facing notes.
- Added `$buddha-draft3-workflow` as the orchestration skill for "specific document + 3차 작업 시작" requests.
- Updated AGENTS.md and BuddhaStory skills to require `BuddhaStory/translation-agent-manual.md` before translation, terminology, or handoff decisions.
- Added draft-3 special rules: near-final manuscript standard, ordinary-reader target, plain Korean preference, minimal Buddhist jargon, smooth Korean prose, whole-document coherence, and traceability for original terms.

## Follow-Ups

- Maintain `.agents/skills/` under the explicit draft-3 editing rule: a specific document path plus `3차번역작업 시작` or equivalent wording triggers direct in-place draft-3 work.
- During Codex 3rd-stage work, write reviewer-facing comparison, terminology decisions, and unresolved questions into the target file's `[review]...[/review]` block.
- Do not create separate final-review files, draft-3 term recommendation files, or final Korean-only outputs unless the user explicitly requests those actions.
- Treat `outputs/manuscripts/en-kr/BuddhaStory/` as the current final Korean-only extraction target when extraction is explicitly requested.
- Before any GitHub upload from this repository, review `git status` and avoid including unrelated `.obsidian` workspace changes unless explicitly requested.
