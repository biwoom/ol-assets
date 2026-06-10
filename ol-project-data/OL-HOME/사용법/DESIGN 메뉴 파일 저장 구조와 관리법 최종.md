# DESIGN 메뉴 파일 저장 구조와 관리법 최종

> 기준일: 2026-06-04
> 적용 대상: OL HOME의 `DESIGN` 메뉴

## 1. DESIGN의 현재 방향

OL DESIGN은 더 이상 단순한 스타일 레퍼런스 아카이브가 아니다.

현재 운영 기준은 다음과 같다.

```text
1차 콘텐츠: 인포그래픽
보조 콘텐츠: 삽화, 스타일시트, 캐릭터/배경/소품 레퍼런스
기본 산출물: HTML + PDF
목록 탐색: 썸네일 이미지
분류 운영: prefix tag 중심
```

인포그래픽은 불교 개념, 서사, 비교, 연표, 구조를 시각적으로 정리한 배포 단위다. HTML은 웹브라우저 열람용, PDF는 인쇄·보존·공유용으로 관리한다.

ENTITY와 지식그래프 연결은 장기 확장 가능성으로 남기되, 현재 운영에서는 필수 연결 규칙으로 강조하지 않는다.

## 2. 저장 구조

### 2.1 인포그래픽

인포그래픽은 여러 산출물을 함께 관리하므로 폴더 구조를 기본으로 한다.

```text
src/content/design/
  dependent-origination.md

public/design/
  dependent-origination/
    index.html
    dependent-origination.pdf
    preview.webp
    preview2.webp
    thumb.webp
```

각 파일의 역할은 다음과 같다.

```text
index.html                  웹브라우저 열람용 인포그래픽
dependent-origination.pdf   PDF 다운로드용 파일
preview.webp                상세 페이지 대표 미리보기 이미지
preview2.webp               상세 페이지 추가 미리보기 이미지
thumb.webp                  목록 카드 썸네일
```

미리보기 이미지가 여러 장이면 `imagePath`에는 대표 이미지를, `previewPaths`에는 상세 페이지에서 보여줄 전체 미리보기 이미지를 순서대로 적는다.

```yaml
thumbnailPath: "dependent-origination/thumb.webp"
imagePath: "dependent-origination/preview1.webp"
previewPaths:
  - "dependent-origination/preview1.webp"
  - "dependent-origination/preview2.webp"
```

`previewPaths`는 브라우저에서 `<img>`로 표시할 수 있는 이미지 파일만 넣는다. PDF 페이지를 프리뷰로 보여주고 싶으면 PDF를 JPG/WebP/PNG로 별도 내보내 `preview2.webp`처럼 등록한다.

인포그래픽에서 preview 이미지는 미리보기용 보조 자산이다. 다운로드 버튼의 기본 대상은 HTML과 PDF이며, preview 이미지는 별도 다운로드 버튼을 만들지 않는다. 이미지 자체가 주 산출물인 `format: image` 자료에서만 이미지 다운로드 버튼을 표시한다.

### 2.2 삽화·스타일시트·레퍼런스

단일 이미지 자료는 간단한 파일 구조를 허용한다.

```text
src/content/design/
  ananda-turnaround.md

public/design/
  ananda-turnaround.webp
```

다만 다음 중 하나에 해당하면 폴더 구조를 권장한다.

- 원본, 썸네일, PDF 등 산출물이 2개 이상이다.
- 향후 HTML/PDF 인포그래픽으로 확장될 가능성이 높다.
- 같은 주제의 이미지가 여러 장 묶인다.

```text
public/design/
  ananda-style-sheet/
    image.webp
    thumb.webp
    source.png
```

## 3. 메타데이터 작성 기준

DESIGN 메타데이터는 `src/content/design/*.md`에 둔다.

### 3.1 인포그래픽 예시

```yaml
---
title: "연기법 한눈에 보기"
description: "십이연기 흐름을 입문자용 도식으로 정리한 인포그래픽."
summary: "십이연기 흐름도"
primaryKind: infographic
type: flowchart
format: mixed
series: "불교 핵심 개념"
version: "0.1.0"
status: published
date: 2026-06-04

thumbnailPath: "dependent-origination/thumb.webp"
imagePath: "dependent-origination/preview.webp"
previewPaths:
  - "dependent-origination/preview.webp"
htmlPath: "dependent-origination/index.html"
pdfPath: "dependent-origination/dependent-origination.pdf"
imageAlt: "십이연기 흐름을 원형 구조로 정리한 인포그래픽"

scriptureRef: "상윳따 니까야 12장"
dimensions: "1600×2200"
pageSize: "A4"
orientation: portrait
medium: "HTML/CSS, PDF"
source: "OL Project"
license: "CC0"

tags:
  - kind:infographic
  - topic:연기
  - format:html
  - format:pdf
  - level:introductory
prefixTags:
  - kind:infographic
  - topic:연기
  - format:html
  - format:pdf
published: true
---

십이연기를 처음 접하는 독자가 전체 흐름을 한 화면에서 파악하도록 만든 인포그래픽이다.
```

### 3.2 보조 이미지 예시

```yaml
---
title: "아난다 존자 — 전후좌우 턴어라운드"
description: "아난다 존자의 기본 외형과 의상을 정리한 캐릭터 스타일시트."
primaryKind: style-sheet
type: turnaround
format: image
series: "붓다스토리 캐릭터"
version: "0.1.0"
status: published

imagePath: "ananda-turnaround.webp"
imageAlt: "아난다 존자 전신 턴어라운드"
medium: "digital illustration"
dimensions: "4000×2400"
source: "OL Project"
license: "CC0"

tags:
  - kind:style-sheet
  - character:아난다
  - use:illustration-reference
prefixTags:
  - kind:style-sheet
  - character:아난다
published: true
---

아난다 존자의 전신 턴어라운드 시트.
```

## 4. prefix tag 운영

현재 DESIGN은 prefix tag 중심으로 탐색·분류한다.

권장 prefix는 다음과 같다.

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

`entities` 필드는 스키마에 남겨두지만, 현재 단계에서는 필수로 작성하지 않는다. 나중에 지식그래프가 실제 기능으로 구현되면 prefix tag와 entities를 매핑할 수 있다.

## 5. GitHub 저장 용량 기준

GitHub 저장소는 이미지와 PDF를 무제한으로 저장하는 공간이 아니다.

```text
개별 파일: 100MB 이하
50MB 이상 파일: push 경고 가능
저장소 전체: 1GB 미만 권장, 5GB 미만 강력 권장
```

운영 기준:

- 웹용 이미지는 WebP/JPG로 최적화한다.
- PDF는 가능하면 10MB 이하로 관리한다.
- 원본 대용량 작업 파일은 Git에 넣지 않는다.
- 자료가 수백 개 이상 쌓이면 별도 assets 저장소나 외부 스토리지를 검토한다.

## 6. 요약

```text
인포그래픽: src/content/design/*.md + public/design/{slug}/
보조 이미지: 단일 파일 허용, 확장 가능하면 폴더 권장
목록 카드: thumbnailPath 우선
상세 미리보기: imagePath 우선
웹 보기: htmlPath
PDF 다운로드: pdfPath
이미지 다운로드: format:image 자료의 imagePath
분류: prefixTags 중심
ENTITY: 장기 확장 필드로만 유지
```
