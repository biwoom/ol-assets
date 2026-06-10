# ASTRO 에서 파일다운과 브라우저 열기 링크 적용법과 저장구조 분리

GitHub Pages + Astro 구조에서는 다음처럼 작성하는 것이 가장 안정적입니다.

가정:

```text id="l9jlwm"
public/
  books/
    ol-book/
      index.html
```

웹 주소:

```text id="zjlwm4"
https://biwoom.github.io/ol-home/books/ol-book/
```

---

# 1. 웹페이지로 열기 버튼

## 권장 HTML

```html id="71ycj2"
<a
  href="/ol-home/books/ol-book/"
  class="ol-button"
>
  웹에서 읽기
</a>
```

---

# 왜 `/ol-home/` 가 필요한가

GitHub Pages repository 배포는:

```text id="jcck29"
https://username.github.io/repository-name/
```

구조이므로:

```text id="vbgfzw"
/books/ol-book/
```

만 쓰면 루트 기준으로 잘못 연결될 수 있습니다.

즉 반드시:

```text id="kvf34m"
/ol-home/books/ol-book/
```

처럼 repository base path 포함 권장.

---

# 더 좋은 방법 (Astro 권장)

Astro config:

```js id="b4j65y"
// astro.config.mjs

export default defineConfig({
  site: 'https://biwoom.github.io',
  base: '/ol-home',
})
```

설정 후:

```astro id="1r9hmk"
---
const BASE = import.meta.env.BASE_URL;
---

<a href={`${BASE}books/ol-book/`}>
  웹에서 읽기
</a>
```

이 방식이 가장 안전합니다.

---

# 2. 파일 다운로드 버튼

## 가장 단순한 방식

```html id="c9s8jf"
<a
  href="/ol-home/books/ol-book/index.html"
  download="ol-book.html"
  class="ol-button"
>
  HTML 다운로드
</a>
```

---

# 하지만 여기 매우 중요한 문제 있음

브라우저는:

```text id="ch8e80"
download
```

속성을 GitHub Pages에서 항상 강제 적용하지 않을 수 있습니다.

특히:

* Safari
* 모바일 브라우저

에서 그냥 열릴 수도 있음.

---

# 따라서 더 좋은 구조

추천:

```text id="6jlwmh"
public/books/ol-book/
  index.html

public/downloads/
  ol-book-v1.0.html
```

---

# 그리고 다운로드 버튼은 별도 파일 링크

```html id="fjlwmj"
<a
  href="/ol-home/downloads/ol-book-v1.0.html"
  download
  class="ol-button"
>
  HTML 다운로드
</a>
```

---

# 이것이 훨씬 좋은 이유

## 1. 역할 분리

| 용도      | 경로                             |
| ------- | ------------------------------ |
| 웹 읽기    | `/books/ol-book/`              |
| 파일 다운로드 | `/downloads/ol-book-v1.0.html` |

---

## 2. 버전 관리 쉬움

```text id="mjlwm1"
downloads/
  ol-book-v1.0.html
  ol-book-v1.1.html
```

가능.

---

## 3. analytics/log 분리 가능

장래 확장 유리.

---

# 추천 최종 구조

```text id="ujlwmr"
public/
├─ books/
│  └─ ol-book/
│      └─ index.html
│
├─ downloads/
│  └─ ol-book-v1.0.html
│
└─ atlas/
```

---

# 실제 최종 버튼 예시

```html id="fq7lxt"
<div class="ol-book-actions">
  <a
    href="/ol-home/books/ol-book/"
    class="ol-button"
  >
    웹에서 읽기
  </a>

  <a
    href="/ol-home/downloads/ol-book-v1.0.html"
    download
    class="ol-button ol-button-secondary"
  >
    HTML 다운로드
  </a>
</div>
```

---

# 그리고 장기적으로 매우 중요한 점

OL BOOK 철학상:

```text id="o3p4ku"
웹페이지 보기
≠
다운로드
```

입니다.

왜냐하면 OL BOOK은:

* 독립 artifact
* offline-readable
* forkable
* preservable

철학을 가지기 때문입니다.

즉 다운로드 자체가:

> “디지털 경전 유통”

행위가 됩니다.

이건 일반 웹사이트와 매우 다른 지점입니다.

---

# 추가 권장

장래에는 다운로드 포맷을 이렇게 확장 추천:

```text id="rujlwm"
다운로드:
- HTML
- EPUB
- PDF
- Markdown
- OL Package (.olbook)
```

즉 OL BOOK은 단순 웹페이지가 아니라:

> “portable knowledge object”

로 가는 방향이 매우 자연스럽습니다.
