# Astro에서 콘텐츠 원고 md와 완결버전 ol-book.html 저장위치 분리

 Astro의 **`src/content`**, **`src/pages`**, **`public`** 의 역할 차이를 명확히 이해하는 것이 매우 중요합니다.

현재 질문의 핵심은 사실상:

> “OL BOOK 완결 HTML 파일과 개별 md/mdx 문서 기반 콘텐츠 시스템을 어떻게 공존시킬 것인가?”

입니다.

결론부터 말하면:

```text id="3af1e8"
완결된 ATLAS/BOOK html 파일
↔
Astro md/mdx 콘텐츠 시스템
```

은 충돌 없이 공존 가능합니다.

하지만 저장 위치를 잘못 선택하면 Astro 빌드 구조와 충돌하거나 예상과 다르게 동작할 수 있습니다.

---

# 핵심 결론

## ❌ 권장하지 않는 방식

```text id="1m7m2h"
src/content/book/buddha-story.html
```

여기에 HTML 완결본 저장.

이 방식은 Astro content collections 목적과 맞지 않습니다.

---

# 이유

Astro에서:

```text id="9k7gjm"
src/content/
```

는 단순 정적 파일 저장소가 아니라:

> “콘텐츠 데이터 레이어”

입니다.

즉:

* md
* mdx
* yaml
* json

등을 Astro가 파싱하여 컬렉션 시스템으로 처리하는 공간입니다.

HTML 완결본 저장 위치로는 부적절합니다.

---

# 권장 구조

## ✅ 가장 좋은 구조

```text id="58zcfa"
public/books/
  buddha-story.html
  dhammapada.html
```

또는:

```text id="o2b03p"
public/books/
  buddha-story/
    index.html
```

이 구조입니다.

---

# 이유

Astro에서:

```text id="qffu13"
public/
```

는:

> “빌드 없이 그대로 배포되는 정적 자산”

입니다.

즉:

```text id="m63qlg"
public/books/buddha-story.html
```

↓

웹에서는:

```text id="jlwmc6"
https://biwoom.github.io/ol-home/books/buddha-story.html
```

로 바로 열립니다.

---

# 그리고 이것이 OL 구조와 매우 잘 맞음

왜냐하면 OL BOOK은 원래:

> “독립된 출판물”

이기 때문입니다. 

즉 OL HOME 안의 일반 페이지가 아니라:

* export된 단일 HTML 책
* 독립 배포 가능한 artifact
* self-contained publication

입니다.

따라서 Astro 페이지 시스템 내부보다:

```text id="wzhc7w"
public/books/
```

가 철학적으로도 더 맞습니다.

---

# 충돌 문제

질문:

```text id="m6t93m"
src/content/book/buddha-story/01-birth.md
```

와 충돌하는가?

## 결론

```text id="xjogtt"
충돌하지 않음
```

입니다.

왜냐하면 역할이 완전히 다르기 때문입니다.

---

# 역할 차이

## 1. md/mdx 콘텐츠

```text id="jlwm8u"
src/content/books/buddha-story/01-birth.md
```

역할:

* 원고
* 구조화된 콘텐츠
* 챕터 단위 데이터
* Astro 렌더링용 소스

즉:

> “제작용 원천 데이터”

입니다.

---

## 2. export된 html

```text id="muo96x"
public/books/buddha-story.html
```

역할:

* 완결본
* 배포 artifact
* 독립 실행 책

즉:

> “출판된 결과물”

입니다.

---

# 이것은 오히려 OL 철학과 매우 잘 맞음

현재 OL 설계에서:

```text id="b5pp34"
ATLAS = 제작 공방
BOOK = 출판물
```

로 분리되어 있었습니다. 

따라서:

```text id="2kp97z"
src/content/books/
```

는:

> 제작 원고 저장소

이고,

```text id="4kfx3y"
public/books/
```

는:

> 출판 완료된 artifact 저장소

가 됩니다.

이 구분은 장기적으로 매우 중요합니다.

---

# 추천 최종 구조

OL에 가장 적합한 형태는 아마 이것입니다:

```text id="k6k1mb"
src/content/books/
  buddha-story/
    01-birth.mdx
    02-renunciation.mdx

public/books/
  buddha-story/
    index.html
    cover.jpg
    meta.json
```

---

# 이 구조의 장점

## 1. 제작과 배포 분리

명확함.

---

## 2. 향후 자동 export 가능

장래:

```text id="6x5s5j"
ATLAS export
→ public/books/ 자동 저장
```

가능.

---

## 3. Astro와 충돌 없음

매우 안정적.

---

## 4. GitHub Pages 친화적

GitHub Pages는 정적 파일 배포에 매우 적합.

---

## 5. 독립 배포 가능

나중에:

```text id="9n4lwl"
books.olbit.org
```

같은 서브도메인으로 분리 가능.

---

# 추가로 중요한 점

## `.html` 직접 링크보다 더 좋은 방식

권장:

```text id="5v76ic"
public/books/buddha-story/index.html
```

웹 접근:

```text id="97gk0q"
/books/buddha-story/
```

이 방식.

---

# 이유

이 구조가:

* prettier URL
* SEO 유리
* GitHub Pages 친화적
* later expansion 가능

합니다.

---

# 따라서 권장 최종안

## 콘텐츠 원고

```text id="yjlwmr"
src/content/books/
```

---

## 완결 BOOK export

```text id="xz02q3"
public/books/
```

---

# 콘텐츠 원고 md와 완결 BOOK.html 저장위치 분리
## 실제 URL

```text id="0w8k61"
https://biwoom.github.io/ol-home/books/buddha-story/
```

---

# 매우 중요한 장기 전략

사실 현재 구조는 장기적으로 아래 구조로 발전하기 좋습니다:

```text id="0y0j89"
원천 콘텐츠(MDX)
↓
ATLAS 구조화
↓
BOOK export
↓
public/books/
↓
GitHub Pages 배포
```

즉:

> “OL HOME 자체가 출판 플랫폼”

이 됩니다.

이 방향은 현재 OL 철학과 거의 완벽하게 정렬됩니다.
