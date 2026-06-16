# Decisions

Last updated: 2026-06-13

## 2026-06-13

### Codex Role Re-Expanded for Explicit Draft-3 Requests

Codex CLI is still not the primary 1st or 2nd draft producer. However, when the user gives a specific BuddhaStory document path and asks for `3차번역작업 시작`, `3차 작업 시작`, `3차 감수 시작`, `draft-3 작업`, or equivalent wording, Codex should perform the requested 3rd-stage work directly on that file.

- Codex edits the specified draft-3 file in place.
- Codex does not copy the target document to another path for revision.
- Codex compares draft-3 against draft-1, draft-2, source, term files, cumulative glossaries, and draft logs when available.
- Codex records reviewer-facing notes inside the same draft-3 file using `[review]...[/review]`.
- Codex does not create a separate final-review document by default.
- Codex does not add draft-3 recommendations to term files by default.
- Codex does not run final Korean-only extraction by default.

### Current UBTF Paths

Use the UBTF layout as the active path system:

- Source: `source/raw/en/BuddhaStory/src-01-gcb-revised/`
- Drafts: `translation/en-kr/BuddhaStory/draft-1/`, `draft-2/`, `draft-3/`
- Project terms: `term/en-kr/BuddhaStory/`
- Cumulative terms: `term/cumulative/`
- Logs: `log/en-kr/BuddhaStory/draft-1/`, `log/en-kr/BuddhaStory/draft-2/`
- Final outputs: `outputs/manuscripts/en-kr/BuddhaStory/`

Older `BuddhaStory/edit/gcb-kr/...` paths are historical and should not be used as active defaults.

### Required Review Block

For explicit 3rd-stage work, add or update exactly one review block in the target draft-3 file:

```md
[review]
...
[/review]
```

Place it immediately after YAML frontmatter when frontmatter exists; otherwise place it at the top of the file before the first heading.

The block should include:

- checked files and reference materials
- major draft-1 / draft-2 comparison points
- final wording or style decisions
- draft-3 terminology decisions
- unresolved human-review questions

### Stage Meaning

- `draft-1`: scholarly and doctrinally rigorous translation for Buddhist experts. It may use Buddhist technical terminology, but should avoid translationese and remain natural Korean.
- `draft-2`: public-readable translation for ordinary Korean readers at high-school level or above. It should minimize Buddhist jargon and prefer everyday Korean where doctrinal accuracy allows.
- `draft-3`: human-review preparation and final integration draft. Codex may directly revise a specified draft-3 file when explicitly requested. The draft-3 body should target ordinary Korean readers at high-school level or above, use natural modern Korean, and replace Buddhist technical terms with everyday Korean by default. Retain technical terms only when necessary for doctrinal precision, and record the reason in the inline `[review]` block.
- `outputs/manuscripts/en-kr/BuddhaStory/`: final Korean-only extraction output from finalized draft-3, created only by explicit request or by the approved pipeline.

### Context Maintenance

`.agents/context/` files are project memory for Codex CLI continuity. They should be updated after:

- workflow-role changes
- meaningful draft-3 edits
- explicit final extraction work
- repository-management work

Historical work-log entries may mention older paths or old workflows. New active guidance should use the current UBTF layout and explicit draft-3 request rule.
