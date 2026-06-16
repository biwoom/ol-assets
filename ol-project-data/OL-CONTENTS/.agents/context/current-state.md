# Current State

Last updated: 2026-06-13

## Workspace

- Content root: `/Users/damjin/Projects/ol-project/github/ol-assets/ol-project-data/OL-CONTENTS`
- Git root: `/Users/damjin/Projects/ol-project/github/ol-assets`
- Main active content project: `BuddhaStory`
- Active language pair: `en-kr`
- Active text family: `gcb-revised`
- Codex role: requested draft-3 editor and human-review preparation assistant

## Current Workflow Ownership

- Gemini / existing production pipeline owns primary 1st draft production, 2nd draft production, validation, and final Korean-only extraction unless the user explicitly asks Codex to inspect or run an output step.
- Human reviewers own final judgment on wording, doctrinal nuance, and publication approval.
- Codex CLI directly supports 3rd-stage work when the user gives a specific document path and asks for `3차번역작업 시작`, `3차 작업 시작`, `3차 감수 시작`, `draft-3 작업`, or equivalent wording.
- In that explicit workflow, Codex edits the specified draft-3 file in place and records reviewer-facing notes in the same file's `[review]...[/review]` block.

## BuddhaStory Structure

- Source path: `source/raw/en/BuddhaStory/src-01-gcb-revised/`
- 1st draft path: `translation/en-kr/BuddhaStory/draft-1/`
- 2nd draft path: `translation/en-kr/BuddhaStory/draft-2/`
- 3rd draft path: `translation/en-kr/BuddhaStory/draft-3/`
- Project term path: `term/en-kr/BuddhaStory/`
- Cumulative term path: `term/cumulative/`
- Production logs: `log/en-kr/BuddhaStory/draft-1/`, `log/en-kr/BuddhaStory/draft-2/`
- Final Korean-only output path: `outputs/manuscripts/en-kr/BuddhaStory/`

## Stage Standards

- `draft-1`: academic, rigorous translation for Buddhist experts; technical terms are allowed; Korean must still be natural.
- `draft-2`: readable public-facing translation for ordinary Korean readers at high-school level or above; Buddhist jargon is minimized.
- `draft-3`: final human-review preparation draft. Codex may edit a specific draft-3 file directly when explicitly requested. The body should use natural modern Korean for ordinary Korean readers at high-school level or above, replacing Buddhist technical terms with everyday Korean by default unless doctrinal precision requires retention.
- `outputs/manuscripts/en-kr/BuddhaStory/`: Korean-only final extraction output created by the approved pipeline or by Codex only when explicitly requested.

## Current Draft-3 Rule

- Do not copy the target draft-3 file elsewhere for editing.
- Do not create separate review notes under `log/en-kr/BuddhaStory/final-review/` by default.
- Do not update term files with draft-3 recommendations by default.
- Put review notes, terminology decisions, and unresolved human-review questions inside one `[review]...[/review]` block near the start of the target draft-3 file.
- Record any retained Buddhist technical term, or any everyday replacement that may lose doctrinal nuance, in the `[review]` block.
- Preserve YAML frontmatter, source text, `[KO]` blocks, footnotes, tags, aliases, and diacritics.

## Current Git Note

At setup time, `ol-assets` already had an unrelated modified file:

- `ol-project-data/.obsidian/workspace.json`

Do not revert or include that file in Codex changes unless the user explicitly asks.
