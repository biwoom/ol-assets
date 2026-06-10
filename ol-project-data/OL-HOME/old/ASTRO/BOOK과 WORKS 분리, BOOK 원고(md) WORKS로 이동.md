# BOOK과 WORKS 분리, BOOK 원고(md) WORKS로 이동

네. 현재 OL의 철학과 장기 구조를 고려하면, 그 방향이 매우 합리적입니다.
다만 실제로는 한 단계 더 구조를 분리하는 것이 좋습니다.

결론부터 말하면:

```text id="4f3h5g"
BOOK = 출판 완료된 라이브러리
WORKS(or SCRIPTURE LAB) = 제작중 원고/연구 노트
```

로 분리하는 방향을 강하게 권장합니다.

그리고 현재 제안한:

```text id="7h2a1m"
콘텐츠 원고(md)
+
완결 HTML 브라우저 보기
+
다운로드 HTML
```

구조는 매우 좋습니다.

다만 “어디에 무엇을 노출할 것인가”를 명확히 나누는 것이 중요합니다.

---

# 1. 현재 제안 구조 평가

당신이 제안한 구조:

```text id="3pwjlwm"
BOOK 메뉴
├─ 원고(md)
├─ 브라우저 보기(html)
└─ 다운로드(html)
```

기술적으로는 문제없습니다.

하지만 UX/철학 관점에서는 약간 혼합되어 있습니다.

왜냐하면:

```text id="djlwm2"
원고(md)
≠
출판물(html)
```

이기 때문입니다.

---

# 이 둘은 본질적으로 다름

## md 원고

성격:

* 제작중
* 편집 가능
* 구조화 데이터
* source manuscript
* evolving text

즉:

> “공방(workshop)”

입니다.

---

## export html

성격:

* 완결 artifact
* 배포본
* 독서 최적화
* self-contained
* preservation 대상

즉:

> “출판물(publication)”

입니다.

---

# 따라서 BOOK은 무엇이 되어야 하는가

현재 OL 철학상 BOOK은:

```text id="jlwm93"
디지털 불교 도서관
```

에 가깝습니다.

즉 사용자는 BOOK에서:

* 완결된 책
* 안정된 읽기 경험
* 다운로드 가능한 artifact

를 기대합니다.

따라서:

```text id="6jlwmc"
BOOK = 완결본 라이브러리
```

로 유지하는 것이 훨씬 강력합니다.

---

# 매우 중요한 점

당신이 지금 만드는 것은 단순 CMS가 아닙니다.

사실상:

```text id="2jlwm9"
출판 시스템
```

입니다.

출판 시스템에서:

| 단계  | 역할 |
| --- | -- |
| 원고  | 제작 |
| 교정본 | 편집 |
| 출판본 | 배포 |

은 분리됩니다.

OL도 이 구조를 가지는 것이 장기적으로 매우 유리합니다.

---

# 내가 권장하는 구조

## 최종 권장 IA

```text id="jlwmda"
HOME
├─ BOOK
├─ WORKS
├─ DESIGN
├─ ATLAS
├─ BLOG
└─ AI
```

---

# 각 메뉴의 역할

## BOOK

출판 완료 라이브러리.

포함:

* 웹에서 읽기
* 다운로드
* 메타데이터
* 버전
* 언어
* 저자
* 난이도

즉:

> “디지털 경전 도서관”

---

## WORKS (강력 추천)

제작중 콘텐츠 공간.

예:

* buddha-story draft
* 번역 초안
* 주석 연구
* 미완성 시리즈
* 실험적 텍스트

즉:

> “불교 콘텐츠 작업실”

---

# 이 구조가 중요한 이유

## 1. 사용자가 혼란스럽지 않음

BOOK에 들어갔는데:

* draft
* unfinished
* markdown source

가 섞이면 UX가 흔들립니다.

---

## 2. OL 철학과 맞음

OL은:

```text id="jlwmfj"
조용한 독서 경험
```

을 중요시합니다.

완결본과 작업중 원고는 리듬이 다릅니다.

---

## 3. 장기적으로 매우 강력함

미래에:

```text id="9jlwmf"
WORKS
↓
ATLAS 편집
↓
BOOK 출판
```

파이프라인이 명확해집니다.

---

# 추천 실제 폴더 구조

## source manuscripts

```text id="gjlwm0"
src/content/book/
  buddha-story/
    01-birth.md
```

---

## published books

```text id="jlwmr5"
public/books/
  buddha-story/
    index.html
```

---

## downloadable artifacts

```text id="jlwmw1"
public/downloads/books/
  buddha-story-v1.0.html
```

---

# 그리고 BOOK 페이지 UI는 이렇게 추천

## BOOK 카드

```text id="jlwmg2"
붓다 이야기
━━━━━━━━━━
완결판 v1.0

[웹에서 읽기]
[HTML 다운로드]

출판일: 2026-05
형식: OL BOOK
```

---

# 반면 WORKS는

```text id="jlwmz7"
붓다 이야기 (집필중)
━━━━━━━━━━
진행률: 42%

[원고 보기]
[최근 수정]
[ATLAS에서 열기]
```

---

# 아주 중요한 철학적 차이

이 구조는 사실상:

```text id="jlwm13"
BOOK = 결과물
WORKS = 수행 과정
```

을 분리합니다.

이건 OL 철학과 매우 잘 맞습니다.

불교에서도:

* 수행
* 편집
* 퇴고
* 전승

과

* 결집된 경전

은 다르기 때문입니다.

---

# 메뉴 이름 추천

## 가장 추천

```text id="jlwm85"
WORKS
```

짧고 강력함.

---

# 불교적 느낌 강화 버전

| 이름          | 느낌        |
| ----------- | --------- |
| SCRIPTORIUM | 필사실 느낌    |
| STUDIO      | 현대적       |
| WORKS       | 가장 안정적    |
| LAB         | 실험실 느낌 강함 |
| MANUSCRIPTS | 문헌학 느낌    |
| DRAFTS      | 너무 임시적    |
| ARCHIVE     | BOOK과 겹침  |

---

# 개인적으로 가장 추천

```text id="jlwm67"
BOOK = 출판된 지혜
WORKS = 생성중인 지혜
```

구조.

즉:

```text id="jlwm89"
BOOK
↔
WORKS
```

이 이중구조가 OL의 핵심이 될 가능성이 큽니다.

---

# 따라서 현재 시점 추천 결론

## 추천 구조

```text id="jlwm21"
BOOK
→ 완결 라이브러리만

WORKS
→ md 원고/제작중 콘텐츠
```

---

# 그리고 내부 파이프라인은

```text id="jlwm44"
WORKS(md)
↓
ATLAS
↓
BOOK(html)
↓
DOWNLOAD(html/epub/pdf)
```

---

이 구조는:

* 기술적으로 안정적
* GitHub Pages 친화적
* Astro와 충돌 없음
* 온톨로지 구조와 정렬됨
* 장기 AI/지식그래프 구조와도 자연스럽게 연결됨

이라는 장점이 있습니다.
