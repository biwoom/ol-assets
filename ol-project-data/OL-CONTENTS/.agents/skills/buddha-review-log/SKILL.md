---
name: buddha-review-log
description: Compose the inline [review] block for a BuddhaStory draft-3 manuscript during 3rd-stage work. Use to summarize checked files, draft-1/draft-2 comparison, terminology decisions, revision rationale, and unresolved human-review questions inside the target file instead of creating a separate final-review note.
---

# Buddha Inline Review Block

## Scope

Use this skill to prepare the reviewer-facing `[review]...[/review]` block that lives inside the target draft-3 file.

Default location:

```txt
translation/en-kr/BuddhaStory/draft-3/{stem}.md
```

Do not create a separate `log/en-kr/BuddhaStory/final-review/` note by default.

## Placement

Place exactly one block:

```md
[review]
...
[/review]
```

- If YAML frontmatter exists, place the block immediately after the closing `---`.
- If there is no YAML frontmatter, place the block at the top of the file before the first heading.
- If a review block already exists, update it instead of adding another one.

## Content

Keep the block concise and useful for a human reviewer. Include:

- `검토 자료`: source, draft-1, draft-2, draft-3, term files, cumulative glossaries, and logs actually checked
- `1차/2차 비교`: major differences that affected draft-3 choices
- `수정 방향`: readability, doctrinal precision, and style decisions
- `용어 판단`: final draft-3 term choices and alternatives that need human confirmation
- `감수자 확인`: unresolved issues, source ambiguities, footnote concerns, or naming policy questions

## Style

- Write in Korean unless the term itself must remain in Pali, Sanskrit, English, or another source language.
- Avoid long critique. Prefer direct, actionable notes.
- Do not include generic statements such as "문체 개선 필요" without a concrete decision or location.
- Include term decisions here instead of writing draft-3 recommendations to term files.

## Output Expectation

Report:

- whether the review block was added or updated
- highest-priority reviewer items
- whether any separate review file was intentionally not created
