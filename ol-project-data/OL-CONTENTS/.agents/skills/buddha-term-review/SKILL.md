---
name: buddha-term-review
description: Analyze BuddhaStory draft-1, draft-2, project glossary, and cumulative glossary term choices for draft-3 work. Use during 3rd-stage editing to decide terminology for the target draft-3 file and record those decisions in the inline [review] block, not in term files unless explicitly requested.
---

# Buddha Term Review

## Scope

Use this skill for terminology analysis during BuddhaStory 3rd-stage work.

Primary references:

```txt
term/en-kr/BuddhaStory/{stem}-term.md
term/en-kr/BuddhaStory/gcb-revised-term.md
term/cumulative/
translation/en-kr/BuddhaStory/draft-1/{stem}.md
translation/en-kr/BuddhaStory/draft-2/{stem}.md
translation/en-kr/BuddhaStory/draft-3/{stem}.md
log/en-kr/BuddhaStory/draft-1/{stem}-log.md
log/en-kr/BuddhaStory/draft-2/{stem}-draft2-log.md
```

Do not rewrite term files or cumulative glossaries by default. During normal draft-3 work, put final term decisions and unresolved term questions inside the target file's `[review]` block.

## Workflow

1. Read current project guidance:

```txt
GEMINI.md
UBTF-GLOBAL-MANUAL.md
UBTF-WORKFLOW.md
translation/en-kr/BuddhaStory/PROJECT-GUIDE.md
translation/translation-guides/lang-en.md
```

2. Identify the target document stem.
3. Read available term files, cumulative glossaries, draft-1, draft-2, draft-3, and draft logs.
4. Compare term choices for:
   - draft-1 scholarly precision
   - draft-2 everyday readability
   - source-language traceability
   - project glossary consistency
   - doctrinal risk
5. Apply final term choices in the draft-3 manuscript when needed.
6. Prefer everyday Korean over Buddhist technical terms as the draft-3 default.
7. Keep a Buddhist technical term only when an everyday expression would distort doctrinal meaning, erase a necessary distinction, or break an established name/formula.
8. Record decisions in the target file's `[review]` block.

## Review Block Format

Use concise entries inside `[review]`, for example:

```md
- 용어 판단: Dhamma는 삼보 정형 표현에서는 "법", 설명 문맥에서는 "가르침"을 우선 적용. 인간 감수자는 문서 전체의 정형성 유지 여부를 확인할 것.
```

## Standards

- Preserve Pali/Sanskrit diacritics.
- Keep established names stable unless a strong reason exists.
- Distinguish expert-facing precision from public-facing readability.
- Keep original terms traceable in the review block when everyday Korean may hide a doctrinal distinction.
- Mark unresolved ambiguity for human review instead of silently resolving it.

## Explicit Term-File Edit Exception

Only if the user explicitly asks to update a term file:

- preserve useful 1st/2nd-stage term history
- add new notes without erasing prior rationale
- do not update cumulative files unless explicitly requested

## Output Expectation

Report:

- term references inspected
- final term decisions applied or recommended
- review-block entries added
- unresolved terms for human review
