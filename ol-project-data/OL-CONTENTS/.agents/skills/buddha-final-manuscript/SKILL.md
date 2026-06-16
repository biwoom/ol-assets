---
name: buddha-final-manuscript
description: Inspect, run, or troubleshoot BuddhaStory final Korean-only manuscript extraction only when explicitly requested. Use for outputs/manuscripts/en-kr/BuddhaStory extraction readiness or repair; it is not part of the default 3rd-stage draft editing workflow.
---

# Buddha Final Manuscript Extraction

## Scope

Final Korean-only manuscripts are produced from finalized draft-3 files by the approved Gemini/pipeline workflow or by Codex only when the user explicitly requests extraction, inspection, or repair.

Current draft-3 path:

```txt
translation/en-kr/BuddhaStory/draft-3/{stem}.md
```

Current output path:

```txt
outputs/manuscripts/en-kr/BuddhaStory/{stem}.md
```

## Default Position

Do not run extraction as part of a normal `3차번역작업 시작` request. That request prepares the draft-3 file for human final review and records notes in the inline `[review]` block.

Use this skill only when the user explicitly asks to:

- inspect final extraction readiness
- run the approved final extraction
- repair a final Korean-only output
- troubleshoot extraction script behavior

## Readiness Checks

1. Read current workflow and project guidance:

```txt
GEMINI.md
UBTF-GLOBAL-MANUAL.md
UBTF-WORKFLOW.md
translation/en-kr/BuddhaStory/PROJECT-GUIDE.md
```

2. Inspect the target draft-3 file:
   - Korean body blocks are wrapped correctly in `[KO]...[/KO]`
   - Korean headings are present where expected
   - Korean footnotes are extractable and identifiers match
   - source paragraphs remain available in draft-3
   - YAML frontmatter is preserved
   - inline `[review]` block will not be mistaken for final manuscript content, or extraction behavior is known
3. Report issues before extraction when possible.

## Explicit Extraction

Only when the user explicitly asks Codex to run extraction, use the approved project command from the current manuals, such as:

```txt
python3 scripts/run_pipeline.py --extract-final translation/en-kr/BuddhaStory/draft-3/{stem}.md
```

After extraction, verify that draft-1, draft-2, draft-3, term files, and logs were not unintentionally modified.

## Output Expectation

Report:

- target draft-3 path
- expected final output path
- readiness or extraction status
- issues fixed or still pending
- whether extraction was run
