# WORKS-ATLAS 메타데이터 매핑 해결제안서

작성일: 2026-06-05  
대상: OL HOME WORKS 원고를 OL ATLAS로 가져와 OL BOOK 제작에 사용하는 흐름  
참고 문서:

- `/Users/damjin/Projects/ol-project/OL-Project-매뉴얼/공용문서/OL BOOK 워크플로우 v2.md`
- `/Users/damjin/Projects/ol-project/OL-Project-매뉴얼/OL- ATLAS/OL ATLAS 현재상태보고서 2026-06-05.md`
- `/Users/damjin/Projects/ol-project/OL-Project-매뉴얼/OL-HOME/사용법/OL 홈페이지 콘텐츠 관리 매뉴얼 v1.md`

---

## 1. 문제 요약

현재 OL HOME의 WORKS 원고를 OL BOOK으로 발전시키려면, WORKS Markdown 문서를 OL ATLAS로 가져와 카드 단위로 편집하고 재구성해야 한다.

하지만 WORKS와 ATLAS는 문서의 목적과 메타데이터 경계가 다르다.

- WORKS는 홈페이지의 공개 문서 라이브러리다.
- ATLAS는 OL BOOK 제작을 위한 로컬 우선 카드 제작 도구다.
- WORKS frontmatter는 공개, 저작권, 분류, 정렬, 관리용 태그까지 포함한다.
- ATLAS Markdown import는 카드 제작에 필요한 일부 frontmatter만 읽는다.

따라서 WORKS Markdown을 그대로 ATLAS에 import하면 다음 문제가 생긴다.

- ATLAS가 모르는 WORKS 메타데이터는 버려진다.
- 기존 WORKS의 `group`은 ATLAS의 `column`에 가까웠고, ATLAS의 `group`과 의미 층위가 달라 충돌했다.
- 이 문제를 줄이기 위해 WORKS 구조를 `series > part > group > document`로 정리한다.
- WORKS의 `prefixTags`는 관리용인데, ATLAS는 prefix 형식 태그를 카드 태그로 직접 사용하는 경향이 있어 충돌한다.
- WORKS 원고의 전체 메타데이터를 ATLAS에 모두 등록하는 것은 ATLAS 카드 스키마를 과도하게 복잡하게 만든다.

결론적으로 raw WORKS Markdown을 직접 import하는 방식은 권장하지 않는다. 대신 WORKS 원본을 ATLAS import 전용 Markdown 또는 JSON으로 변환하는 매핑 계층이 필요하다.

---

## 2. 현재 스키마 경계

### 2.1 WORKS 구조

현재 WORKS는 다음 위계를 따른다.

```text
series
  part
    group
      document
```

주요 frontmatter:

```yaml
title: "문서 제목"
series: "큰 문서 묶음"
seriesOrder: 10
part: "시리즈 안의 대분류"
partOrder: 10
group: "part 안의 소분류"
groupOrder: 10
category: "전체 WORKS 필터용 분류"
chapter: 1
order: 1
date: 2026-06-04
status: revising
tags: ["표시용", "일반 태그"]
prefixTags:
  - "kind:works"
  - "type:paper"
  - "topic:수행체계"
authors: ["비움"]
license: "CC0"
published: true
excerpt: "목록용 요약"
```

WORKS에서 `category`는 문서 위계가 아니라 전체 문서 목록의 필터다. `series`, `part`, `group`이 화면 위계를 만든다.

### 2.2 ATLAS 구조

현재 ATLAS state는 다음 구조를 갖는다.

```text
meta.bookInfo
columns
cards
```

ATLAS 카드 구조:

```js
{
  id,
  colId,
  title,
  body,
  group,
  tags,
  priority,
  created,
  slug,
  images,
  acts
}
```

ATLAS Markdown import가 실제로 읽는 frontmatter는 제한적이다.

```yaml
---
title: "..."
column: "..."
group: "..."
priority: high | mid | low
learnStatus: wait | doing | done
tags: ["..."]
slug: "..."
created: "YYYY-MM-DD"
---
```

이 목록 밖의 frontmatter는 현재 ATLAS import 과정에서 버려진다.

---

## 3. 핵심 판단

WORKS 메타데이터 전체를 ATLAS 카드 스키마로 옮기지 않는다.

ATLAS가 현재 실제로 사용하는 필드만 WORKS에서 추출한다. 나머지 WORKS 메타데이터는 WORKS 원본에 남긴다.

즉, 정답은 “스키마 통합”이 아니라 “변환 매핑”이다.

```text
WORKS 원본 md
  ↓
WORKS → ATLAS 변환 규칙
  ↓
ATLAS import용 md 또는 JSON
  ↓
ATLAS 카드
  ↓
OL BOOK 제작
```

이 방식은 세 가지 장점이 있다.

- WORKS 공개 문서 구조를 망가뜨리지 않는다.
- ATLAS 카드 스키마를 불필요하게 키우지 않는다.
- WORKS의 `series`, `part`, `group`, `document`를 ATLAS의 `book`, `column`, `group`, `card`로 자연스럽게 옮길 수 있다.

---

## 4. 권장 매핑 원칙

### 4.1 WORKS의 series는 ATLAS의 book 단위로 본다

WORKS의 `series`는 홈페이지 문서 라이브러리에서 큰 묶음이다.

ATLAS에서는 하나의 작업 파일이 한 권의 BOOK 또는 한 권의 BOOK 후보에 해당한다. 따라서 WORKS의 특정 `series`를 ATLAS로 가져올 때는 그 `series`를 ATLAS의 `meta.bookInfo.bookTitle` 또는 작업 파일 제목으로 매핑한다.

예:

```yaml
WORKS:
  series: "붓다 스토리"

ATLAS:
  meta.bookInfo.bookTitle: "붓다 스토리"
  meta.title: "붓다 스토리"
```

주의: ATLAS 카드 Markdown import만으로는 `meta.bookInfo`를 설정할 수 없다. 따라서 `bookInfo`는 별도 수동 입력 또는 향후 JSON/HTML state 생성 도구에서 처리해야 한다.

### 4.2 WORKS part는 ATLAS column에 대응한다

ATLAS의 `column`은 칸반 컬럼이자 카드의 큰 분류다. 사용자의 설명에 따르면 ATLAS 문서 구조에서 column은 BOOK 안의 대분류에 해당한다.

WORKS의 `part`는 series 안의 대분류다. 따라서 ATLAS로 가져갈 때 `part`를 `column`에 매핑한다.

`column`은 `category`에 연결하지 않는다. `category`는 WORKS 전체 필터용 분류이기 때문이다.

권장 기본값:

```text
ATLAS column = WORKS part
```

예:

```yaml
WORKS:
  part: "탄생과 출가"

ATLAS:
  column: "탄생과 출가"
```

BOOK 제작 과정에서 part 이름보다 출판용 column 이름을 더 다듬고 싶다면 변환 프로파일에서만 바꾼다.

```yaml
columnMap:
  "탄생과 출가": "제1부 탄생과 출가"
```

### 4.3 WORKS group은 ATLAS group에 대응한다

WORKS의 `group`은 `part` 내부의 소분류다.

ATLAS의 `group`은 column 내부에서 카드를 다시 묶는 세부 단위다.

`part` 도입 이후 두 필드는 같은 층위에 놓인다.

```text
WORKS: series > part > group > document
ATLAS: book > column > group > card
```

권장 기본값:

```yaml
ATLAS group = WORKS group
```

재지정이 필요한 경우:

```yaml
groupMap:
  "발원": "수메다의 발원"
```

### 4.4 WORKS prefixTags는 그대로 ATLAS tags에 넣지 않는다

WORKS의 `prefixTags`는 관리용이다. UI에 그대로 노출하지 않는 것을 원칙으로 한다.

ATLAS의 `tags`는 카드 편집과 탐색에 직접 쓰이는 태그다. 또한 ATLAS에서는 prefix 형식 태그를 기본 사용하려는 방향이 있다.

따라서 WORKS `prefixTags` 전체를 ATLAS `tags`에 무조건 병합하면 안 된다.

권장 방식:

- 변환 프로파일에 카드별 `tags` override가 있으면 그것을 우선 사용한다.
- override가 없으면 WORKS `prefixTags` 중 BOOK 제작에 필요한 키만 선별한다.
- WORKS 일반 `tags`를 쓸 경우에는 ATLAS prefix 태그로 변환한다.

선별 권장 key:

```text
type
topic
text
author
tradition
use
```

제외 권장 key:

```text
kind
project
format
tool
source
status
```

예:

```yaml
WORKS prefixTags:
  - "kind:works"
  - "type:paper"
  - "text:보리도차제론"
  - "topic:수행체계"
  - "author:도남-김성철"

ATLAS tags:
  - "type:paper"
  - "text:보리도차제론"
  - "topic:수행체계"
  - "author:도남-김성철"
```

WORKS 일반 태그를 ATLAS로 가져올 때:

```yaml
WORKS tags: ["람림", "삼사도"]

ATLAS tags:
  - "topic:람림"
  - "topic:삼사도"
```

---

## 5. 1:1 매핑표

### 5.1 ATLAS 카드 Markdown import 기준

| ATLAS import 필드 | WORKS 원본 필드 | 매핑 규칙 | 비고 |
|---|---|---|---|
| `title` | `title` | 그대로 사용 | 필수 |
| `column` | `part` | 기본값은 WORKS `part` 사용 | WORKS `category`에 자동 연결하지 않음 |
| `group` | `group` | 기본값은 WORKS `group` 사용 | WORKS와 ATLAS의 group 층위가 일치 |
| `priority` | 변환 프로파일 override 또는 기본값 | 없으면 `mid` | ATLAS 허용값: `high`, `mid`, `low` |
| `learnStatus` | 변환 프로파일 override 또는 `status` | `draft/revising → wait`, `ready/published → done` | 제작 진행 상태로만 사용 |
| `tags` | 변환 프로파일 override 또는 선별된 `prefixTags` | ATLAS에서는 prefix 형식 사용 | WORKS 일반 `tags`는 필요시 `topic:`으로 변환 |
| `slug` | 파일 slug 또는 `id` | WORKS entry id의 마지막 slug 사용 권장 | 중복 시 ATLAS가 보정 |
| `created` | `date` | 날짜가 있으면 사용, 없으면 변환일 | ATLAS 생성일 |
| 본문 | Markdown body | frontmatter 제거 후 본문만 사용 | 이미지 경로 주의 |

### 5.2 ATLAS bookInfo 기준

카드 Markdown import만으로는 `bookInfo`를 설정할 수 없다. 그러나 BOOK 제작상 다음 매핑을 권장한다.

| ATLAS `meta.bookInfo` 필드 | WORKS/BOOK 제작 출처 | 권장 규칙 |
|---|---|---|
| `bookTitle` | WORKS `series` 또는 BOOK 제작 프로파일 `title` | 한 ATLAS 파일이 한 권이면 BOOK 제목 |
| `subtitle` | BOOK 제작 프로파일 | WORKS 개별 문서에서 자동 추출하지 않음 |
| `author` | WORKS `authors` 또는 프로파일 `author` | 여러 저자가 섞이면 프로파일에서 확정 |
| `translator` | 프로파일 | 번역서일 때만 |
| `publisher` | 프로파일 | 예: `OL Project` |
| `publishedAt` | 프로파일 | 출판 예정일 또는 발행일 |
| `revisedAt` | 변환일 또는 프로파일 | 재작업 시 갱신 |
| `bookVersion` | 프로파일 | 예: `v0.1.0` |
| `description` | WORKS `excerpt` 조합 또는 프로파일 | 책 전체 설명 |
| `language` | 기본값 `ko` | 필요시 변경 |
| `isbn` | 프로파일 | 없으면 빈 값 |

---

## 6. 권장 변환 frontmatter

WORKS 원본 Markdown을 그대로 ATLAS에 넣지 말고, 다음 형태의 ATLAS import용 Markdown을 생성한다.

```yaml
---
title: "Systematic Buddhology와 <보리도차제론>"
column: "체계불학"
group: "보리도차제론"
priority: mid
learnStatus: wait
tags: ["type:paper", "text:보리도차제론", "topic:수행체계", "author:도남-김성철"]
slug: "systematic_buddhology"
created: "2026-06-04"
---

본문...
```

이 파일은 ATLAS import 전용 산출물이다. WORKS 원본 파일을 대체하지 않는다.

---

## 7. 변환 프로파일에서만 둘 선택 필드

WORKS의 `part`와 `group`이 ATLAS의 `column`과 `group`에 대응하므로, 원칙적으로 WORKS frontmatter에 ATLAS 전용 필드를 추가하지 않는다.

다만 BOOK 제작 과정에서 표시명을 바꾸거나 진행 상태를 다르게 주고 싶다면, WORKS 원본이 아니라 변환 프로파일에 다음 선택 필드를 둘 수 있다.

```yaml
overrides:
  "donam-kim-sung-chul/paper/systematic_buddhology/systematic_buddhology":
    column: "제1부 체계불학"
    group: "보리도차제론"
    priority: mid
    learnStatus: wait
    tags:
      - "type:paper"
      - "text:보리도차제론"
      - "topic:수행체계"
```

이 방식은 WORKS 원고가 ATLAS 제작 도구에 종속되는 것을 막는다.

---

## 8. 변환 프로파일 방식

권장 1단계는 WORKS의 기본 매핑을 사용하되, BOOK 제작 단위마다 변환 프로파일을 두어 제목, column 표시명, tag 선별 정책만 조정하는 것이다.

예:

```yaml
bookTitle: "보리도차제론과 체계불학"
source:
  collection: works
  series: "도남(圖南) 김성철"
bookInfo:
  author: "도남(圖南) 김성철"
  publisher: "OL Project"
  language: "ko"
  bookVersion: "v0.1.0"
columns:
  "체계불학": "제1부 체계불학"
groups:
  "현대 불교학": "현대 불교학"
  "보리도차제론": "보리도차제론"
works:
  - "donam-kim-sung-chul/paper/modern-buddhist-studies-problem/modern-buddhist-studies-problem"
  - "donam-kim-sung-chul/paper/systematic_buddhology/systematic_buddhology"
tagPolicy:
  usePrefixTags:
    - type
    - topic
    - text
    - author
  convertDisplayTagsToTopic: true
```

이 방식의 장점:

- WORKS 원본의 `series > part > group > document` 위계를 그대로 활용할 수 있다.
- 같은 WORKS 원고를 다른 BOOK 프로젝트에 재사용할 수 있다.
- ATLAS의 column/group 표시명만 BOOK마다 조정할 수 있다.

---

## 9. 단계별 해결안

### 1단계: 문서 운영 규칙 확정

즉시 적용한다.

- WORKS 원본 md를 ATLAS에 직접 import하지 않는다.
- ATLAS import용 md 또는 JSON으로 변환해서 가져온다.
- 변환 시 ATLAS가 읽는 필드만 생성한다.
- WORKS의 나머지 메타데이터는 원본에 보존한다.

### 2단계: 변환 스크립트 작성

OL HOME 또는 별도 도구에 `works → atlas-import-md` 변환 스크립트를 둔다.

입력:

- WORKS md 파일들
- BOOK 제작용 변환 프로파일

출력:

- ATLAS import용 Markdown 파일 묶음
- 또는 `ol-cards-v1` JSON

현재 ATLAS는 Markdown 여러 파일 가져오기와 JSON 카드 병합을 모두 지원하므로 둘 다 가능하다.

권장 출력은 JSON이다.

이유:

- JSON은 카드 배열 구조가 명확하다.
- Markdown line parser의 한계를 피할 수 있다.
- `column`, `group`, `tags` 배열을 더 안전하게 보낼 수 있다.

단, 이미지 포함 문서는 Markdown import가 이미지 토큰 변환을 처리할 수 있으므로, 이미지 중심 문서는 Markdown 출력이 유리할 수 있다.

### 3단계: ATLAS 스키마 확장 검토

장기적으로는 ATLAS 카드에 다음 필드 추가를 검토한다.

```js
sourceMeta: {
  source: "ol-home/works",
  worksId: "...",
  originalFrontmatter: {...}
}
```

이렇게 하면 ATLAS 안에서도 원본 WORKS 출처를 보존할 수 있다.

하지만 현재 단계에서 필수는 아니다. 지금은 매핑 변환으로 충분하다.

---

## 10. 최종 권장안

현재 가장 현실적인 해결책은 다음이다.

1. WORKS와 ATLAS 스키마를 통합하지 않는다.
2. WORKS 원본 md를 직접 ATLAS에 import하지 않는다.
3. BOOK 제작 단위마다 변환 프로파일을 만든다.
4. 기본 매핑은 `part → column`, `group → group`으로 둔다.
5. 변환 프로파일은 표시명, 포함 문서, tag 선별 정책만 조정한다.
6. ATLAS import에는 현재 ATLAS가 읽는 필드만 넣는다.
7. WORKS `prefixTags`는 선별 변환하고, 전체 병합하지 않는다.
8. 장기적으로 ATLAS에 `sourceMeta`를 추가해 원본 출처 보존을 강화한다.

이 구조가 OL HOME, OL ATLAS, OL BOOK의 역할을 가장 덜 섞으면서도 실제 제작 흐름을 막지 않는다.

---

## 11. 간단한 운영 예시

WORKS 원본:

```yaml
title: "몸과 마음의 정화를 위한 여섯 단계 불교명상 기초수행"
series: "수행연구"
part: "기초수행"
partOrder: 10
group: "몸과 마음의 정화"
groupOrder: 10
category: "수행"
chapter: 1
order: 1
tags: ["불교명상", "수행", "정화", "몸과 마음"]
prefixTags:
  - "kind:works"
  - "type:practice-guide"
  - "topic:불교명상"
  - "topic:정화"
  - "use:education"
```

ATLAS import용 변환 결과:

```yaml
---
title: "몸과 마음의 정화를 위한 여섯 단계 불교명상 기초수행"
column: "기초수행"
group: "몸과 마음의 정화"
priority: mid
learnStatus: wait
tags: ["type:practice-guide", "topic:불교명상", "topic:정화", "use:education"]
slug: "01-six-steps"
created: "2026-06-04"
---

본문...
```

이렇게 변환하면 WORKS의 공개 문서 구조와 ATLAS의 BOOK 제작 카드 구조가 충돌하지 않는다.
