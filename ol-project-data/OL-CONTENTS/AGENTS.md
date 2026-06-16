# AGENTS.md

## Project

This directory is `OL-CONTENTS`, the OL project workspace for Buddhist content production, translation assets, manuscript editing, terminology control, and reviewer handoff material.

- Content root: `/Users/damjin/Projects/ol-project/github/ol-assets/ol-project-data/OL-CONTENTS`
- Active project: `BuddhaStory`
- Active language pair: `en-kr`
- Active text family: `gcb-revised`
- Current Codex role: requested draft-3 editor and human-review preparation assistant

## Core Role

Codex CLI is not the primary 1st or 2nd draft producer. Gemini or the existing production pipeline may create and validate draft-1 and draft-2 files.

When the user provides a specific BuddhaStory document path and asks for `3차번역작업 시작`, `3차 작업 시작`, `3차 감수 시작`, `draft-3 작업`, or equivalent wording, Codex should perform the requested 3rd-stage work on that specific file.

In that explicit 3rd-stage workflow, Codex:

- Reads the governing workflow documents before translation or terminology judgment.
- Compares the target draft-3 file against draft-1, draft-2, available draft logs, project term files, and cumulative glossaries.
- Revises the specified draft-3 file in place.
- Adds or updates a concise `[review]...[/review]` block near the start of the same draft-3 file for the human reviewer.
- Includes draft-3 terminology decisions and unresolved terminology questions inside the `[review]` block.
- Does not create a separate final-review document.
- Does not update term files with draft-3 recommendations unless the user explicitly asks.
- Does not run final Korean-only extraction unless the user explicitly asks.

## Critical Paths

- Read-only source: `source/raw/en/BuddhaStory/src-01-gcb-revised/`
- 1st draft: `translation/en-kr/BuddhaStory/draft-1/`
  - Academic, rigorous translation for Buddhist experts.
  - Buddhist technical terms may be used when they preserve doctrinal precision.
  - Translationese should still be avoided; Korean should be natural for expert readers.
- 2nd draft: `translation/en-kr/BuddhaStory/draft-2/`
  - Readable translation for ordinary Korean readers at high-school level or above.
  - Buddhist jargon should be minimized and replaced with everyday Korean where accuracy allows.
  - Public comprehension and flow are prioritized over narrow academic literalness.
- 3rd draft: `translation/en-kr/BuddhaStory/draft-3/`
  - Human-review preparation and final integration path.
  - Codex may edit this path directly when the user gives a specific file path and asks for 3rd-stage work.
- Project term files: `term/en-kr/BuddhaStory/`
- Cumulative term files: `term/cumulative/`
- Draft logs: `log/en-kr/BuddhaStory/draft-1/` and `log/en-kr/BuddhaStory/draft-2/`
- Final Korean-only manuscript output: `outputs/manuscripts/en-kr/BuddhaStory/`
  - Created only when explicitly requested or by the approved Gemini/pipeline extraction workflow.

## File Safety

- Do not modify `source/raw/` unless the user explicitly asks to correct source storage.
- Do not overwrite `translation/en-kr/BuddhaStory/draft-1/` or `draft-2/` during Codex 3rd-stage work.
- Do not copy the target draft-3 document elsewhere for editing. Modify the user-specified draft-3 file directly.
- Do not create `log/en-kr/BuddhaStory/final-review/` review notes during the default Codex 3rd-stage workflow.
- Do not write draft-3 term recommendations into `term/en-kr/BuddhaStory/` or `term/cumulative/` unless the user explicitly asks.
- Do not treat `outputs/manuscripts/en-kr/BuddhaStory/` as source.
- Do not remove English source paragraphs or `[KO]...[/KO]` translation blocks from draft files unless the user explicitly requests Korean-only extraction or repair.
- Preserve YAML frontmatter, tags, and `tagAliases` unless correcting a clear error.
- Preserve diacritics in Pali, Sanskrit, names, and aliases.

## Document Matching

Use the file stem as the document identity. For a target such as:

```txt
translation/en-kr/BuddhaStory/draft-3/gcb-1.1.1.0-Salutation & Intention.md
```

Check related files:

- `source/raw/en/BuddhaStory/src-01-gcb-revised/{stem}.md`
- `translation/en-kr/BuddhaStory/draft-1/{stem}.md`
- `translation/en-kr/BuddhaStory/draft-2/{stem}.md`
- `translation/en-kr/BuddhaStory/draft-3/{stem}.md`
- `term/en-kr/BuddhaStory/{stem}-term.md`
- `term/en-kr/BuddhaStory/gcb-revised-term.md`
- `term/cumulative/`
- `log/en-kr/BuddhaStory/draft-1/{stem}-log.md`
- `log/en-kr/BuddhaStory/draft-2/{stem}-draft2-log.md`
- `outputs/manuscripts/en-kr/BuddhaStory/{stem}.md`

If an exact related file is missing, continue with the available evidence and mention the gap in the `[review]` block or final response.

## Required Reading

Before substantial BuddhaStory translation, terminology, or workflow edits, read the relevant current instructions:

- `GEMINI.md`
- `UBTF-GLOBAL-MANUAL.md`
- `UBTF-WORKFLOW.md`
- `translation/en-kr/BuddhaStory/PROJECT-GUIDE.md`
- `translation/translation-guides/lang-en.md` when English-to-Korean translation rules are needed

Use those files as governing project references. If older `.agents/` history conflicts with them, follow the current root and project guides.

## 3rd-Stage Workflow

When the user gives a specific document path and asks for 3rd-stage work:

1. Confirm the target file path and derive `{stem}` from the filename.
2. Prefer targets under `translation/en-kr/BuddhaStory/draft-3/`. If the provided path is not a draft-3 file, stop and ask unless the user clearly instructed otherwise.
3. Read the current workflow documents listed above.
4. Read the target draft-3 file first.
5. Read available draft-1, draft-2, source, term files, cumulative glossaries, and draft logs for the same stem.
6. Revise the target draft-3 file directly, preserving YAML, source text, `[KO]` blocks, headings, footnotes, tags, aliases, and diacritics.
7. Add or update one `[review]...[/review]` block:
   - place it immediately after YAML frontmatter when frontmatter exists
   - otherwise place it at the top of the file before the first heading
   - do not duplicate an existing review block
8. In the review block, briefly record:
   - files and reference materials checked
   - major 1st/2nd draft comparison points
   - final wording or style decisions
   - terminology decisions that would formerly have gone to a term recommendation file
   - unresolved human-review questions
9. Do not create a separate review note, update term files, or run final extraction unless separately requested.
10. Record meaningful workflow or document-edit work in `.agents/context/work-log.md`.

## Current Workflow Standards

- **1차 작업**: 불교전문연구자의 학술적이고 엄밀한 번역. 단순 직역이 아니라 불교전문가 그룹을 독자로 설정한 번역이다. 불교전문용어 사용이 가능하되, 원어의 번역어투를 피하고 자연스러운 한국어 문장으로 번역한다.
- **2차 작업**: 고등학교 이상의 평범한 대한민국 독자를 대상으로 한 쉽고 이해 가능한 번역이다. 불교전문용어를 최대한 자제하고 일상어로 대체한다. 학술적 엄밀함보다 대중적 이해 가능성과 가독성을 우선한다.
- **3차 작업**: 인간 감수자의 최종 감수를 위한 번역본을 준비한다. 1차의 교리적·학술적 정확성과 2차의 대중적 가독성을 통합하되, 본문은 고등학교 이상의 일반 한국어 독자가 자연스럽게 읽을 수 있는 현대 한국어 문체를 원칙으로 한다. 불교전문용어는 원칙적으로 일상어로 대체하고, 전문용어를 유지해야 교리적 의미가 보존되는 경우에만 제한적으로 사용한다. 쉬운 표현으로 대체할 때 의미 손실 가능성이 있거나 전문용어 유지가 필요한 경우, 그 판단 근거를 `[review]` 블록에 남긴다. Codex는 명시 요청된 draft-3 문서를 직접 수정하고, 감수자가 볼 핵심 검토 내용을 같은 문서의 `[review]` 블록에 남긴다.
- **최종 추출**: 한국어-only 최종 결과물 추출은 기본 3차 작업에 포함하지 않는다. 사용자가 명시 요청하거나 기존 Gemini/pipeline workflow가 수행한다.

## Skill Use

- Use `$buddha-draft3-workflow` when the user gives a specific BuddhaStory document path and asks for 3rd-stage work.
- Use `$buddha-draft3-revision` when directly revising a draft-3 manuscript in place.
- Use `$buddha-term-review` when comparing 1st/2nd-stage term choices; put draft-3 term decisions in the target file's `[review]` block unless term-file edits are explicitly requested.
- Use `$buddha-review-log` to compose the inline `[review]` block. Do not create separate review-log files by default.
- Use `$buddha-final-manuscript` only when the user explicitly asks to inspect, run, or repair final Korean-only extraction.

## Context

- Before substantial work, read `.agents/context/current-state.md` and `.agents/context/decisions.md`.
- Use `.agents/context/work-log.md` for recent progress and unresolved follow-ups.
- Keep context files concise. They are continuity records, not transcripts.
- Update `.agents/context/work-log.md` after workflow-rule changes, meaningful draft-3 edits, final extraction work, or repository-management work.
