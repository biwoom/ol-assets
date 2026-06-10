# Astro 에서 ol-atlas.html 저장구조

ATLAS_v0.0.6.html 베이직 파일도 public/atlas/ 에서 저장하면 될까?

---

네.
그 용도라면:

```text
public/atlas/ATLAS_v0.0.6.html
```

또는 더 권장되는 형태로:

```text
public/atlas/v0.0.6/index.html
```

로 저장하는 것이 매우 적절합니다.

---

# 왜 `public/atlas/` 가 맞는가

현재 당신의 구조에서 ATLAS는 사실상:

* Astro 내부 페이지
* React app
* 동적 SPA

가 아니라,

> “독립 실행 가능한 self-contained HTML application”

입니다.

즉 이전에 논의했던:

```text
BOOK = 출판 artifact
ATLAS = 실행 artifact
```

구조와 동일합니다.

따라서:

```text
src/pages/
```

보다:

```text
public/
```

에 두는 것이 훨씬 철학적·기술적으로 자연스럽습니다.

---

# 추천 구조

## 권장안 1 (최소 구조)

```text
public/
  atlas/
    ATLAS_v0.0.6.html
```

접속:

```text
https://biwoom.github.io/ol-home/atlas/ATLAS_v0.0.6.html
```

---

# 하지만 장기적으로는 권장안 2가 더 좋음

## 권장안 2 (버전 디렉토리 구조)

```text
public/
  atlas/
    v0.0.6/
      index.html
      assets/
```

접속:

```text
https://biwoom.github.io/ol-home/atlas/v0.0.6/
```

이 방식이 훨씬 좋습니다.

---

# 이유

## 1. URL이 깨끗함

```text
/atlas/v0.0.6/
```

는:

* 문서
* 앱
* 릴리즈

모두에 자연스럽습니다.

---

## 2. asset 충돌 방지

ATLAS가 내부적으로:

```text
./assets/
./fonts/
./images/
```

를 참조할 경우 매우 안정적입니다.

단일 html이라도 이후 확장 시 유리합니다.

---

## 3. 버전 병렬 유지 가능

```text
/atlas/v0.0.5/
/atlas/v0.0.6/
/atlas/dev/
```

공존 가능.

이건 매우 중요합니다.

OL/ATLAS는 장기적으로:

> “연구용 툴체인”

이 되기 때문입니다.

---

# 특히 중요한 점

현재 OL 철학에서:

```text
ATLAS = tool/runtime
BOOK = publication
HOME = gateway
```

입니다.

즉:

| 영역           | 성격          |
| ------------ | ----------- |
| Astro pages  | 홈페이지/메타 정보  |
| public/books | 출판 artifact |
| public/atlas | 실행 artifact |

로 나뉘게 됩니다.

이 구조는 매우 안정적이고 장기 유지보수에 강합니다.

---

# 오히려 이것이 OL의 핵심 장점이 될 수 있음

보통 웹사이트는:

```text
site = app
```

인데,

OL은:

```text
site = archive + gateway + runtime distribution
```

구조가 됩니다.

즉 GitHub Pages 자체가:

* 앱 저장소
* 북 라이브러리
* 배포 허브

가 되는 것입니다.

이건 상당히 좋은 방향입니다.

---

# 매우 중요한 추가 권장사항

## `/public/atlas/latest/` 심볼릭 구조

장기적으로 추천:

```text
public/
  atlas/
    latest/
      index.html

    v0.0.6/
    v0.0.7/
```

이 구조.

그러면:

```text
/atlas/latest/
```

항상 최신버전 유지 가능.

---

# 또 하나 중요한 점

## ATLAS와 BOOK의 상대경로 설계

장기적으로 매우 중요합니다.

예:

```text
/atlas/v0.0.6/
/books/buddha-story/
```

일 때,

ATLAS 내부 링크가:

```text
/books/buddha-story/
```

로 이동 가능해야 합니다.

즉:

```text
absolute root-relative path
```

를 사용하는 습관이 중요합니다.

예:

```html
<a href="/ol-home/books/buddha-story/">
```

GitHub Pages에서는 repository base path 때문에 이것이 중요합니다.

---

# 따라서 추천 최종 구조

```text
public/
├─ atlas/
│  ├─ latest/
│  ├─ v0.0.6/
│  └─ v0.0.7/
│
├─ books/
│  ├─ buddha-story/
│  └─ dhammapada/
│
├─ images/
└─ icons/
```

---

# Astro 내부 역할은 오히려 이것

```text
src/pages/
```

는:

* 소개
* 탐색
* 메타 정보
* 라이브러리 index
* entity pages
* ontology navigation

을 담당.

즉:

> “OL 도서관의 안내 시스템”

역할입니다.

반면 실제 책과 도구는:

```text
public/
```

에서 독립 artifact로 존재.

이 구조는 현재 OL 철학과 매우 강하게 정렬됩니다.
