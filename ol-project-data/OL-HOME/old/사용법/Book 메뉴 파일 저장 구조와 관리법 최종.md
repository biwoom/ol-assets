# Book 메뉴 파일 저장 구조와 관리법 최종
## 질문

BOOK 출판 (완결 후)

```markdown
<!-- src/content/book/buddha-story.md -->
---
title: "붓다 이야기"
version: "v1.0"
publishedAt: 2026-06-01
htmlPath: "buddha-story"
downloadFile: "buddha-story-v1.0.html"
primaryEntities: [siddhartha-gautama, shakyamuni-buddha]
description: "싯다르타 고타마의 생애를 원전 기반으로 재구성했습니다."
tags: [붓다전기, 초기불교]
level: 1
published: true
---

```

그리고 `public/books/buddha-story/index.html`, `public/downloads/books/buddha-story-v1.0.html` 배치.

직접 테스트 해보니 하나의 파일을 이렇게 두 곳에 저장하는 것은 불필요한 것 같아. htmlPath 하나로 통일하고 book 페이지에서 a 태그 속성으로 download 추가해서 웹에서 읽기와 내려받기를 분리하면 좋겠어. 어떻게 생각하니?

---

## 응답
좋은 판단입니다. 다만 한 가지 기술적 제약을 먼저 짚고 결론을 드리겠습니다.

---

## 핵심 제약 — `download` 속성의 한계

```html
<!-- 같은 파일, 용도만 다른 두 링크 -->
<a href="/books/buddha-story/">웹에서 읽기</a>
<a href="/books/buddha-story/index.html" download="buddha-story-v1.0.html">내려받기</a>
```

이 방식은 **동일 출처(same-origin)에서만 `download`가 동작**합니다. GitHub Pages는 같은 출처이므로 원칙적으로 됩니다.

단, 실제 테스트에서 브라우저마다 다르게 동작합니다.

| 브라우저 | 결과 |
|----------|------|
| Chrome (데스크탑) | ✅ 파일 저장 |
| Firefox | ✅ 파일 저장 |
| Safari (macOS) | ⚠️ 브라우저에서 열릴 수 있음 |
| iOS Safari | ❌ download 무시, 그냥 열림 |
| Android Chrome | ✅ 대체로 동작 |

Safari/iOS가 문제인데, OL BOOK 사용자 중 모바일 비중이 있다면 무시하기 어렵습니다.

---

## 제안 — 단일 파일 + `download` 속성, 단 파일명에 버전 포함

두 곳에 저장하는 대신 이렇게 구조를 가져가는 것이 좋습니다.

```
public/books/
  buddha-story/
    index.html          ← 웹 읽기용 (URL: /books/buddha-story/)
    buddha-story-v1.0.html  ← 다운로드용 (index.html과 동일 내용)
```

같은 폴더 안에 두 파일. 내용은 동일하지만 역할이 다릅니다.

```astro
<!-- 웹에서 읽기 -->
<a href={url(`/books/${book.data.htmlPath}/`)}>
  웹에서 읽기
</a>

<!-- 내려받기 -->

  href={url(`/books/${book.data.htmlPath}/${book.data.downloadFile}`)}
  download={book.data.downloadFile}
>
  HTML 내려받기
</a>
```

`book` collection 스키마도 단순해집니다:

```typescript
htmlPath: z.string(),        // 폴더명: 'buddha-story'
downloadFile: z.string().optional(),  // 파일명: 'buddha-story-v1.0.html'
```

`downloadFile`이 없으면 내려받기 버튼을 표시하지 않음.

---

## 하지만 제안한 방식도 충분히 유효합니다

단일 `index.html`에 `download` 속성:

```astro
<a href={url(`/books/${book.data.htmlPath}/`)}>웹에서 읽기</a>
<a href={url(`/books/${book.data.htmlPath}/index.html`)} download="buddha-story.html">내려받기</a>
```

스키마에서 `downloadFile` 필드 제거, `htmlPath` 하나만 유지. 구조가 가장 단순합니다.

**이 방식을 채택한다면 한 가지만 추가 권장합니다**: `download` 속성에 파일명을 명시적으로 지정. `download` 속성만 있고 파일명이 없으면 `index.html`로 저장되어 사용자가 헷갈립니다.

```astro
download={`${book.data.title}-${book.data.version}.html`}
// → "붓다 이야기-v1.0.html" 로 저장됨
```

---

## 결론 — 세 가지 선택지 정리

| 방식 | 구조 | 장점 | 단점 |
|------|------|------|------|
| **A. 현재 제안** | 파일 1개, `download` 속성 | 가장 단순 | iOS Safari 미지원 |
| **B. 같은 폴더 2파일** | `index.html` + `버전명.html` | Safari 포함 안정 | 파일 2개 관리 |
| **C. 별도 폴더** | `public/books/` + `public/downloads/` | 역할 명확 | 파일 2곳 관리 |

OL BOOK의 "디지털 경전 유통" 철학을 생각하면 **모든 브라우저에서 안정적으로 파일을 전달하는 것**이 중요합니다. 그 관점에서는 B가 가장 현실적입니다.

하지만 지금 단계에서 콘텐츠가 없는 상태라면 A로 시작해서 실제 사용자 피드백을 보고 B로 전환하는 것도 합리적입니다. 구조 변경이 크지 않으니까요.

어느 방식으로 결정하시든 `book` collection 스키마와 `book/index.astro`의 버튼 코드만 수정하면 됩니다. 결정해주시면 해당 부분 코드를 바로 작성해드리겠습니다.

--

## 최종안

### `src/content/book/` 에 저장할 book메타데이터 MD

```
<!-- src/content/book/buddha-story.md -->
---

title: "buddha story"

version: "v0.0.4"

publishedAt: 2026-05-29

htmlPath: "buddha-story"

primaryEntities: []

description: "붓다스토리 - 부처님의 일대기를 담은 책입니다."

tags: []

published: true

---

  
내용

```


### `public/books/`에 저장할 HTML

```
public/books/buddha-story/index.html
```

### BOOK 완성 파일 홈페이지 등록 과정

1.`public/books/`에 `buddha-story`라는 완성책 이름으로 폴더를 만들고 완성파일을 `index.html` 로 저장한다.

2.`src/content/book/` `buddha-story`라는 완성책 이름으로 폴더를 만들고 그 폴더 에 `buddha-story.md`라는 완성책 이름으로 메타데이터 MD 파일을 만든다.

3.`buddha-story.md` 파일에 메타데이터를 등록한다.
```
<!-- src/content/book/buddha-story.md -->
---

title: "buddha story"

version: "v0.0.4"

publishedAt: 2026-05-29

htmlPath: "buddha-story"

primaryEntities: []

description: "붓다스토리 - 부처님의 일대기를 담은 책입니다."

tags: []

published: true

---

```

- `htmlPath: "buddha-story"` 를 완성책 이름으로 등록. 파일 경로입력 불필요.
- `version: "v0.0.4"` 버전이름은 책 다운로드시 `buddha story-v0.0.4.html`
과같이 책이름에 뒤에 추가되어 표시됨.

---

