---
name: buddha-draft3-revision
description: Revise a specified BuddhaStory draft-3 manuscript in place for human final review. Use when Codex is working on translation/en-kr/BuddhaStory/draft-3 files, balancing draft-1 scholarly precision with draft-2 public readability, preserving source/[KO] structure, and adding or updating the inline [review] block.
---

# Buddha Draft 3 Revision

## Scope

Use this skill to revise:

```txt
translation/en-kr/BuddhaStory/draft-3/{stem}.md
```

Only revise another path when the user explicitly provides it and the project rules allow it.

## Required Reading

Read current workflow and project guidance before editorial judgment:

```txt
GEMINI.md
UBTF-GLOBAL-MANUAL.md
UBTF-WORKFLOW.md
translation/en-kr/BuddhaStory/PROJECT-GUIDE.md
translation/translation-guides/lang-en.md
```

## Revision Priorities

- Integrate the strengths of draft-1 and draft-2.
- Preserve doctrinal accuracy while writing natural Korean for human final review.
- Write for ordinary Korean readers at high-school level or above.
- Prefer ordinary Korean as the default style.
- Replace Buddhist technical terms with everyday Korean wherever doctrinal accuracy allows.
- Keep Buddhist technical terms only when an everyday replacement would distort the meaning or erase an important doctrinal distinction.
- Preserve technical distinctions when simplification would distort the meaning.
- Avoid English sentence order and translationese.
- Keep headings, footnotes, source traceability, and term usage consistent.
- Mark retained technical terms, meaning-risky everyday replacements, and unresolved doctrinal or terminology ambiguity in the inline `[review]` block.

## Editing Rules

- Edit the specified draft-3 file directly.
- Do not copy the file to another location.
- Preserve YAML frontmatter, tags, `tagAliases`, and diacritics.
- Preserve source paragraphs and `[KO]...[/KO]` blocks unless the user explicitly asks for Korean-only extraction.
- Preserve footnote identifiers and Korean footnote blocks.
- Do not update term files or create separate review notes by default.

## Review Block

Ensure the revised file contains exactly one block:

```md
[review]
...
[/review]
```

Place it immediately after YAML frontmatter when present; otherwise place it before the first heading.

Use the block for:

- checked references and drafts
- major revision decisions
- terminology decisions
- remaining human-review questions

## Output Expectation

Report:

- target file path
- key revisions made
- terminology decisions recorded in `[review]`
- unresolved questions
- verification performed
