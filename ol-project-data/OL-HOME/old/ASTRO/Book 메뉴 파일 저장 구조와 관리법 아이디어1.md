# Book 메뉴 파일 저장 구조와 관리법 아이디어1

 `book` collection 자체 처리' 관련 : 분리 유지: `book` collection은 그대로 두되 의미만 "완결된 출판물 메타"로 재정의. `works`는 새 collection으로 추가. 두 collection 공존. 이 방식으로 진행해줘. 내 의도는 `book`은 완결 출판물, `works`는 제작해가는 단편 문서들. 또 올홈페이지는 특성상 html 파일 자체를 브라우저로 열어서 연결하거나 html을 다운로드 해야 하는 버튼들이 많기 때문에 이를 열기용 html은 `public/books/` 에 두고 다운용 html은 `public/downloads/books/` 에 두자는 아이디어임. 우선 이를 분석해 보고 내 의견이 코드 유지 관리 효율성 측면에서 어떠한지 판단해서 의견줘.


---

## 요약
1.`src/content/book/` 에는 book 메타서지정보만 저장.

2.`public/books/` 은 웹상에서 바로보기 용. 주의: `index.html` 파일명 사용. 이 링크를 참조하는 다른 페이지들의 주소변경없이 항상 최신본 링크 유지가능.
예시) `public/books/buddha-story/index.html` 

3.`public/downloads/books/` 는 웹상에서 다운로드 용. 파일명에 제목 추가해 사용.
`public/downloads/books/buddha-story-v1.0.html`


좋습니다. 코드 구조 관점에서 분석하겠습니다.

---

## 분석: (B) 분리 유지 방식 — `book` + `works` 공존

### 데이터 흐름 전체 그림

```
제작 과정                          출판 결과
──────────────────────────────────────────────────────
src/content/works/          →    public/books/
  buddha-story/                    buddha-story/
    01-birth.md  (원고)              index.html  (완결본, 브라우저 열기용)
    02-renounce.md                 
                                 public/downloads/books/
src/content/book/                  buddha-story-v1.0.html  (다운로드용)
  buddha-story.md  ←──────────────────────┘
  (완결본 메타데이터)
    title, version,
    publishedAt,
    entities[],
    htmlPath: 'buddha-story'
```

이 구조에서 `book` collection은 완결된 출판물의 **메타데이터 허브** 역할을 합니다. 실제 HTML은 `public/`에 있고, `book` collection은 그 HTML로 가는 링크와 서지 정보를 담습니다.

---

## 장점

**1. 의미가 가장 명확합니다**

```
book   = "이미 출판된 것의 목록" (도서관 카탈로그)
works  = "만들어가는 중인 것" (작업실 서랍)
```

코드를 처음 보는 사람도, 1년 후 본인도 역할을 즉시 이해합니다.

**2. `public/` 분리가 자연스럽게 정렬됩니다**

```
src/content/book/buddha-story.md
  ├── htmlPath: 'buddha-story'           → public/books/buddha-story/index.html
  ├── downloadVersion: 'v1.0'            → public/downloads/books/buddha-story-v1.0.html
  └── entities: [siddhartha, lumbini]    → /entity/persons/siddhartha-gautama 연결
```

`book` collection 파일 하나가 "이 책의 모든 링크와 메타"를 담는 단일 진실 소스(single source of truth)가 됩니다. BOOK 목록 페이지를 만들 때 이 collection만 읽으면 됩니다.

**3. `works` → `book` 출판 파이프라인이 명시적입니다**

```
works의 status가 'published'가 되면
→ 수동으로 book/buddha-story.md 생성
→ public/books/에 HTML 배치
→ public/downloads/에 다운로드 파일 배치
```

"출판"이라는 행위가 실제로 파일을 만드는 의식(ritual)이 됩니다. OL 철학과도 정렬됩니다.

**4. 온톨로지 연결이 완결본에도 유지됩니다**

`works`의 원고 md에는 entity 참조가 있습니다. `book` collection에도 같은 entity 참조를 두면, 완결된 책도 지식그래프에 노드로 연결됩니다. 나중에 "이 entity가 등장하는 완결된 책"을 조회할 수 있게 됩니다.

---

## 단점 및 주의점

**1. 중복 관리 가능성**

`works/buddha-story/01-birth.md`에도 entity가 있고, `book/buddha-story.md`에도 entity가 있습니다. 원고를 수정했을 때 book 메타도 같이 업데이트해야 한다는 것을 잊기 쉽습니다.

**완화책**: `book` collection의 스키마를 최소화. 원고 수준의 세부 entity는 `works`에만, `book`에는 대표 entity만:

```yaml
# book/buddha-story.md — 가볍게 유지
---
title: "붓다 이야기"
version: "v1.0"
publishedAt: 2026-05-29
htmlPath: "buddha-story"        # public/books/ 하위 경로
downloadFile: "buddha-story-v1.0.html"
primaryEntities: [siddhartha-gautama, shakyamuni-buddha]
tags: [붓다전기, 초기불교]
status: published
---
```

세부 내용은 works에서 관리, book은 서지 정보만.

**2. `public/books/`와 `public/downloads/books/` 분리의 실용성**

이 구조는 분명한 이점이 있습니다.

```
브라우저 열기용:  public/books/buddha-story/index.html
                  → /books/buddha-story/ (깔끔한 URL)

다운로드용:       public/downloads/books/buddha-story-v1.0.html
                  → /downloads/books/buddha-story-v1.0.html
                  → download 속성으로 강제 다운로드
```

한 가지 현실적 주의점이 있습니다. 브라우저 열기용과 다운로드용 HTML이 **내용이 동일하다면**, 같은 파일을 두 곳에 두는 셈입니다. 관리 부담이 생길 수 있습니다.

**권장 운영 방식**:

```
public/books/buddha-story/index.html      ← 항상 최신본 (웹 읽기)
public/downloads/books/
  buddha-story-v1.0.html                  ← 버전 고정 (다운로드, 영구 URL)
  buddha-story-v1.1.html
  buddha-story-latest.html                ← v1.1의 복사본 (항상 최신 다운로드)
```

`index.html`과 `buddha-story-latest.html`은 내용이 같아도 역할이 다릅니다. 전자는 "웹에서 읽는 것", 후자는 "가져가서 오프라인에서 읽는 것". OL BOOK 철학상 이 구분은 의미가 있습니다.

---

## 결론 및 권장

**이 방식(B)을 강하게 권장합니다.** 이유:

```
유지관리 효율성:  ★★★★☆
의미 명확성:      ★★★★★
확장성:           ★★★★★
OL 철학 정렬:     ★★★★★
```

유일한 약점은 "중복 관리 가능성"인데, `book` collection을 최소한의 서지 정보만 담도록 설계하면 충분히 통제됩니다.

최종 구조를 정리하면:

```
src/content/works/          → 제작 중인 원고, 챕터별 md
src/content/book/           → 완결된 출판물 메타데이터 (경량)
public/books/               → 브라우저 열기용 최신 HTML
public/downloads/books/     → 버전별 다운로드용 HTML
```

이 네 공간의 역할이 각각 독립적이어서, 나중에 어느 한 쪽만 바꿔도 다른 쪽에 영향이 없습니다. 이것이 장기 유지관리에서 가장 중요한 특성입니다.

---

이 방향으로 확인되면 Phase 2 작업지시서 v2를 바로 재작성하겠습니다.