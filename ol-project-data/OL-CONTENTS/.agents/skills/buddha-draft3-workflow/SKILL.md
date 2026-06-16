---
name: buddha-draft3-workflow
description: Run the requested BuddhaStory 3rd-stage draft workflow when the user gives a specific BuddhaStory draft-3 filename or path and asks for 3차번역작업 시작, 3차 작업, 3차 감수, draft-3 work, or final polishing. Use this skill to compare draft-1/draft-2/source/terms/logs, revise the specified draft-3 file in place, and add an inline [review] block for the human reviewer.
---

# Buddha Draft 3 Workflow

## Role

Use this skill when the user gives a specific BuddhaStory document path and asks for 3rd-stage work. In this workflow, Codex edits the specified draft-3 file directly and prepares it for human final review.

Do not copy the target file to another location. Do not create a separate review document. Do not update term files with draft-3 recommendations unless the user explicitly asks. Do not run final Korean-only extraction unless the user explicitly asks.

## Required Reading

Before making translation, terminology, or workflow judgments, read the relevant current instructions:

```txt
GEMINI.md
UBTF-GLOBAL-MANUAL.md
UBTF-WORKFLOW.md
translation/en-kr/BuddhaStory/PROJECT-GUIDE.md
translation/translation-guides/lang-en.md
```

Also read `.agents/context/current-state.md` and `.agents/context/decisions.md` before substantial work.

## Target Handling

1. Identify the exact user-specified target path.
2. Prefer a target under:

```txt
translation/en-kr/BuddhaStory/draft-3/{stem}.md
```

3. If the user-specified path is not a draft-3 file, stop and ask unless the user clearly instructed work on that nonstandard target.
4. Derive `{stem}` from the filename and use it to locate related files.

## Related Files

Read available related files. Continue if some are missing, but note gaps in the review block.

```txt
source/raw/en/BuddhaStory/src-01-gcb-revised/{stem}.md
translation/en-kr/BuddhaStory/draft-1/{stem}.md
translation/en-kr/BuddhaStory/draft-2/{stem}.md
translation/en-kr/BuddhaStory/draft-3/{stem}.md
term/en-kr/BuddhaStory/{stem}-term.md
term/en-kr/BuddhaStory/gcb-revised-term.md
term/cumulative/
log/en-kr/BuddhaStory/draft-1/{stem}-log.md
log/en-kr/BuddhaStory/draft-2/{stem}-draft2-log.md
```

## Workflow

1. Read the target draft-3 file first.
2. Compare draft-1 and draft-2 choices:
   - draft-1 scholarly precision for Buddhist expert readers
   - draft-2 public readability for ordinary Korean readers
   - source fidelity and doctrinal nuance
   - terminology consistency and cumulative glossary alignment
3. Revise the target draft-3 file in place:
   - write for ordinary Korean readers at high-school level or above
   - use natural modern Korean prose
   - replace Buddhist technical terms with everyday Korean as the default
   - keep Buddhist technical terms only when an everyday replacement would distort doctrinal meaning
   - record any retained technical term or meaning-risky everyday replacement in the `[review]` block
   - preserve YAML frontmatter
   - preserve English/source paragraphs unless explicitly asked otherwise
   - preserve `[KO]...[/KO]` block structure
   - preserve footnote identifiers and definitions
   - preserve tags, `tagAliases`, Pali/Sanskrit diacritics, and established names
4. Add or update exactly one inline review block:

```md
[review]
...
[/review]
```

Place it immediately after YAML frontmatter if frontmatter exists; otherwise place it at the top of the file before the first heading. If a review block already exists, update it instead of adding another one.

5. Include in the review block:
   - checked files and reference materials
   - key draft-1 / draft-2 comparison points
   - final wording or style decisions
   - draft-3 terminology decisions, especially technical terms replaced with everyday Korean or retained for doctrinal precision
   - unresolved human-review questions
6. Update `.agents/context/work-log.md` after meaningful draft-3 work.

## Output Expectation

Report briefly:

- target file edited
- files inspected
- highest-priority changes made
- unresolved human-review items
- verification performed

Do not produce a separate long review memo unless the user asks for one.
