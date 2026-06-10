# OL DESIGN 인포그래픽 및 시각자료 제작 매뉴얼

> 대상: OL DESIGN에 인포그래픽, 삽화, 스타일시트, 레퍼런스 자료를 등록하는 작업자
> 목적: 불교 지식을 시각화하고 HTML/PDF/이미지 산출물로 관리하는 기준 정리
> 기준일: 2026-06-04

## 0. OL DESIGN의 목적

OL DESIGN은 불교 콘텐츠를 위한 시각자료 라이브러리다.

현재 중심은 인포그래픽이다. 삽화, 스타일시트, 캐릭터·배경·소품 레퍼런스는 인포그래픽과 BOOK/WORKS 제작을 돕는 보조 콘텐츠로 관리한다.

```text
중심: 인포그래픽
보조: 삽화, 스타일시트, 캐릭터시트, 배경 레퍼런스, 소품 레퍼런스
산출물: HTML, PDF, 이미지
분류: prefix tag
```

ENTITY와 지식그래프 연결은 장기 확장 가능성으로 둔다. 현재 제작 단계에서는 필수 요건이 아니며, prefix tag를 우선 사용한다.

## 1. 인포그래픽 제작 기준

인포그래픽은 불교 개념, 서사, 비교, 연표, 분류, 흐름을 시각적으로 정리한 배포 단위다.

좋은 인포그래픽은 다음 조건을 만족한다.

- 한 화면 또는 한 문서 안에서 핵심 구조가 보인다.
- 제목만 보고 다루는 주제를 알 수 있다.
- 시각 요소가 장식이 아니라 이해를 돕는다.
- 출전, 참고 문헌, 제작자, 라이선스가 메타데이터에 남는다.
- HTML과 PDF 중 최소 하나의 배포 산출물을 가진다.

권장 유형:

```text
timeline       연표
diagram        구조도
flowchart      흐름도
concept-map    개념 지도
comparison     비교표
map            지도
poster         포스터형 요약
```

## 2. 산출물 기준

### 2.1 HTML

HTML은 웹브라우저에서 바로 여는 열람용 산출물이다.

권장 기준:

- `public/design/{slug}/index.html`에 저장
- 외부 서버 없이 단독으로 열릴 수 있어야 함
- 모바일과 데스크톱에서 핵심 내용이 읽혀야 함
- 폰트와 이미지 경로가 깨지지 않아야 함

### 2.2 PDF

PDF는 인쇄, 보존, 파일 공유용 산출물이다.

권장 기준:

- `public/design/{slug}/{slug}.pdf`에 저장
- 가능하면 10MB 이하
- A4 세로 또는 A4 가로 기준을 우선 사용
- PDF만 봐도 제목, 주제, 출처, 라이선스를 확인할 수 있어야 함

### 2.3 이미지

이미지는 목록 썸네일과 상세 미리보기에 사용한다.

권장 기준:

```text
thumb.webp     목록 카드용, 가볍게
preview1.webp  상세 페이지 대표 미리보기용
preview2.webp  상세 페이지 추가 미리보기용
image.webp     단일 이미지 자료 원본
```

인포그래픽은 `thumbnailPath`와 `imagePath`를 둘 다 준비하는 것을 권장한다. 미리보기가 여러 장이면 `previewPaths`에 이미지 파일을 순서대로 적는다. PDF 파일은 `<img>` 미리보기로 쓰지 않고, JPG/WebP/PNG로 내보낸 뒤 등록한다.

인포그래픽의 preview 이미지는 미리보기용 보조 자산이다. 상세 페이지의 다운로드 버튼은 HTML과 PDF를 우선 제공하며, preview 이미지 다운로드 버튼은 만들지 않는다. 이미지 자체가 주 산출물인 `format: image` 자료에서만 이미지 다운로드 버튼을 표시한다.

## 3. 보조 콘텐츠 기준

### 3.1 삽화

삽화는 BOOK, WORKS, ATLAS, 인포그래픽에 들어갈 시각 장면이다.

메타데이터 기준:

```yaml
primaryKind: illustration
type: illustration
format: image
```

### 3.2 스타일시트

스타일시트는 인물, 복장, 소품, 건축물의 반복 제작을 위한 기준 자료다.

메타데이터 기준:

```yaml
primaryKind: style-sheet
type: turnaround
format: image
```

대표 예:

- 캐릭터 턴어라운드
- 표정 시트
- 의상·소품 시트
- 컬러 모델 시트
- 건축/배경 구조 시트

### 3.3 레퍼런스

레퍼런스는 직접 출판물이라기보다 제작을 돕는 참고 자료다.

메타데이터 기준:

```yaml
primaryKind: reference
type: architecture
format: image
```

외부 저작물이 포함될 경우 라이선스를 반드시 자료별로 명시한다. `CC0`를 일괄 선언하지 않는다.

## 4. prefix tag 작성법

DESIGN은 현재 prefix tag로 운영한다.

권장 prefix:

```text
kind:infographic
kind:illustration
kind:style-sheet
kind:reference

topic:연기
topic:공
topic:사성제

format:html
format:pdf
format:image

level:introductory
level:intermediate
level:advanced

use:education
use:book
use:illustration-reference

tradition:초기불교
tradition:대승불교
```

운영 규칙:

- `prefixTags`에는 필터링에 직접 쓰는 핵심 태그를 넣는다.
- `tags`에는 검색용 일반 태그를 함께 넣을 수 있다.
- 같은 뜻의 태그를 여러 방식으로 쓰지 않는다.
- ENTITY 연결은 필수가 아니다.

## 5. 메타데이터 템플릿

### 5.1 인포그래픽

```yaml
---
title: ""
description: ""
summary: ""
primaryKind: infographic
type: diagram
format: mixed
series: ""
version: "0.1.0"
status: published
date: 2026-06-04

thumbnailPath: "{slug}/thumb.webp"
imagePath: "{slug}/preview1.webp"
previewPaths:
  - "{slug}/preview1.webp"
htmlPath: "{slug}/index.html"
pdfPath: "{slug}/{slug}.pdf"
imageAlt: ""

scriptureRef: ""
dimensions: ""
pageSize: "A4"
orientation: portrait
medium: "HTML/CSS, PDF"
source: "OL Project"
sourceUrl: ""
credits: []
license: "CC0"

prefixTags:
  - kind:infographic
  - format:html
  - format:pdf
tags: []
published: true
---
```

### 5.2 보조 이미지

```yaml
---
title: ""
description: ""
primaryKind: style-sheet
type: turnaround
format: image
series: ""
version: "0.1.0"
status: published

thumbnailPath: ""
imagePath: ""
imageAlt: ""

medium: "digital illustration"
dimensions: ""
source: "OL Project"
sourceUrl: ""
license: "CC0"

prefixTags:
  - kind:style-sheet
tags: []
published: true
---
```

## 6. 등록 절차

1. `src/content/design/{slug}.md`를 만든다.
2. 인포그래픽이면 `public/design/{slug}/` 폴더를 만든다.
3. HTML, PDF, 썸네일, 미리보기 이미지를 배치한다.
4. `thumbnailPath`, `imagePath`, `htmlPath`, `pdfPath`를 메타데이터에 기록한다.
5. `prefixTags`를 최소 2개 이상 작성한다.
6. `npm run build`로 컬렉션 스키마와 경로 오류를 확인한다.

## 7. 라이선스 기준

OL 자체 제작 자료는 가능한 한 `CC0`를 기본으로 한다.

외부 저작물, 샘플, 참고 이미지가 포함되면 다음 원칙을 따른다.

- 라이선스를 자료별로 적는다.
- 출처가 불분명한 이미지는 공개 자료로 등록하지 않는다.
- 저작권이 제한된 자료는 `published: false` 또는 내부 참고용으로만 둔다.
- 페이지 전체에 `CC0`라고 일괄 표시하지 않는다.

## 8. 향후 확장

현재는 prefix tag 중심으로 운영한다.

향후 ENTITY와 지식그래프가 실제 기능으로 구현되면 다음 방식으로 확장할 수 있다.

```text
topic:연기  -> concept/dependent-origination
person:아난다 -> person/ananda
place:룸비니 -> place/lumbini
```

이 확장은 가능성으로 남겨두되, 현재 DESIGN 콘텐츠 제작의 필수 조건으로 삼지 않는다.
