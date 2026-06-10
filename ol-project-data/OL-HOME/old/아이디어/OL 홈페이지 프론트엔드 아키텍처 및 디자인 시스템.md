# OL 프로젝트 프론트엔드 아키텍처 및 디자인 시스템 인계 문서

*(2026.05 기준 정리)*

---

# 주요 메뉴

- OL HOME : OL 홈페이지(정적웹사이트), 웹서버로 깃헙페이지 사용

- OL ATLAS : ATLAS 툴(단일 HTML 파일 불교컨텐츠 제작툴이자 뷰어) 소개 페이지. 다운로드 페이지 제공.

- OL BOOK : OL 제작 불교컨텐츠book 소개와 라이브러리. ATLAS 툴에 불교컨텐츠 탑재해 배포하는 의미 소개. 제작된 모든 컨텐츠 보고 다운할수 있는 라이브러이 페이지 제공. OL 붓다스토리, OL 담마빠다, OL 중관학강의, OL 선림(선사들의 삶과 노래) 등등

- OL DESIGN : 불교컨텐츠 스타일 레퍼런스 아카이브. 불교컨텐츠를 위해서는 원문데이터, 각 인물, 복장, 건물, 지역환경 등에 대한 스타일 레퍼런스 필요. OL 은 이 스타일 레퍼런스를 만들어 자체 컨텐츠로 활용할 뿐만 아니라 저작권을 개방하여 불교 컨텐츠를 만들고자 하는 모든 사람들에게 오픈소스로 제공한다.

- OL AI : 장래 개발 구상. 불교컨텐츠 학습하고 불교지혜와 자비로 정렬된 로컬 구동 AI 모델

- OL BLOG : OL 컨텐츠 개발, 수정 과정 소식들 공유, 메인 헤더가 아닌 하단 메뉴로 공개.

# 1. 프로젝트 핵심 방향성

OL 프로젝트는 일반적인 SaaS/생산성 앱이 아니라:

> “불교 지식·수행·연구를 위한 디지털 도량이자
> 연결된 불교 컨텐츠 연기망”

을 지향한다.

핵심 철학:

* 조용한 탐색
* 깊은 체류
* 문사수(聞思修)
* 수행적 UX
* 연결된 지혜망
* 컨텐츠 중심 구조
* 오픈 아카이브
* lineage/origin 기반 구조
* low-noise interface
* static-first architecture

---

# 2. 전체 기술 방향

## 핵심 구조

```text
Astro = OL engine
Basecoat = OL visual foundation
OL CSS = OL identity
```

---

# 3. Astro 역할 정의

## Astro는:

* 사이트 엔진
* 라우팅
* 정적 빌드
* markdown/mdx 처리
* content collections
* 이미지 최적화
* SEO
* 검색 인덱싱
* 페이지 생성

등을 담당한다.

---

## Astro를 채택한 이유

OL은:

* 장문 읽기
* 문헌 중심
* 아카이브 구조
* static-first
* low JS
* markdown 기반 컨텐츠
* deep reading UX

를 중요시한다.

이는 Astro의 강점과 매우 잘 맞는다.

---

# 4. Basecoat 역할 정의

참고:

[Basecoat UI](https://basecoatui.com/?utm_source=chatgpt.com)
[Basecoat GitHub](https://github.com/hunvreus/basecoat?utm_source=chatgpt.com)

---

## Basecoat는:

* UI foundation
* typography baseline
* spacing system
* card system
* layout rhythm
* responsive foundation
* shadcn/ui 계열 디자인 언어

를 담당한다.

---

## Basecoat를 선택한 이유

OL은:

* 과도한 SaaS 감성
* neon/cyberpunk
* aggressive landing
* startup aesthetics

와 거리가 멀다.

Basecoat는:

* 조용함
* 절제된 미니멀리즘
* typography 중심
* editorial 감성
* shadcn/ui 계열 질서감

을 갖고 있어 OL 방향성과 잘 맞는다.

---

# 5. 디자인 철학

## OL은 “앱”보다 “디지털 도량”에 가깝다

따라서:

* dashboard 느낌 최소화
* marketing funnel 최소화
* CTA 과잉 배제
* 과도한 animation 배제

가 중요하다.

---

## 핵심 미학 키워드

```text
contemplative
editorial
archive
library
monastic minimalism
scholarly
quiet interface
deep reading
```

---

# 6. 레퍼런스 구조

---

# OL HOME

## 핵심 방향

> “디지털 수행 공동체의 입구”

---

## 주요 레퍼런스

- 샘플 홈페이지/home
* Basecoat
* shadcn/ui
* Mainline Astro

---

## 특징

* editorial landing
* 큰 여백
* 조용한 hero
* 낮은 시각 자극
* typography 중심
* 철학 중심 소개

---

# OL BOOK

## 주요 레퍼런스

- 샘플 홈페이지/book
- https://ui.shadcn.com/blocks
- https://ui.shadcn.com/docs/components

---

## 특징

* deep reading UX
* prose optimized
* chapter navigation
* reference/citation structure
* long-form reading

---

# OL DESIGN

## 최종 채택 레퍼런스

- 샘플 홈페이지/design
- [Are.na](https://www.are.na/?utm_source=chatgpt.com)
- https://ui.shadcn.com/charts/area
- https://ui.shadcn.com/create


---

## OL DESIGN 정의

OL DESIGN은 단순 이미지 갤러리가 아니다.

정의:

> “오픈 불교 시각문화 연구 아카이브”

---

## 주요 목적

* 불교 컨텐츠 스타일 레퍼런스 구축
* 복식/건축/인물/환경 연구
* AI 생성 컨텐츠 reference
* 오픈소스 시각자료 제공
* lineage 기반 시각문화 정리

---

## 핵심 특징

* 이미지 + 메타데이터
* relation links
* 출처 기반 구조
* 태그 연결
* 인물/시대/지역 필터
* reference graph

---

# OL BLOG

## 최종 채택 레퍼런스

- 샘플 홈페이지/blog

# OL AI

## 최종 채택 레퍼런스

- 샘플 홈페이지/ai

---

# 7. 디자인 시스템 전략

---

# 핵심 원칙

```text
공통 디자인 언어
    ↓
페이지별 경험 변주
```

---

## 잘못된 방향

```text
HOME = 완전 다른 디자인
BOOK = 완전 다른 디자인
DESIGN = 완전 다른 디자인
```

이 방식은 지양.

이유:

* 유지보수 붕괴
* 브랜딩 붕괴
* UX 불일치

---

## 올바른 방향

```text
Basecoat foundation
    ↓
OL theme layer
    ↓
page-specific experiential variants
```

---

# 8. CSS 아키텍처 전략

---

# 절대 원칙

## Basecoat source 직접 수정 금지

Basecoat는:

* infrastructure layer
* upstream layer

로 유지.

---

# 추천 구조

```text
1. Tailwind base
2. Basecoat
3. shadcn/ui
4. OL design tokens
5. OL components
6. page variants
```

---

# 9. OL CSS 전략

현재 샘플 CSS는 이미:

> “OL Design System 초기형”

으로 판단됨.

특징:

* monochrome
* restrained motion
* archive layout
* typography rhythm
* semantic cards
* low-noise UI

---

# 매우 중요한 권장사항

## generic class names 지양

예:

```css
.card
.btn
.badge
```

대신:

```css
.ol-card
.ol-btn
.ol-badge
```

권장.

이유:

* Basecoat 충돌 방지
* 유지보수 향상
* namespace 확보

---

# 10. Content Collections 구조

---

# BLOG 구조

```text
content/blog/
```

예:

```text
content/blog/madhyamaka.md
```

---

## frontmatter 예시

```yaml
---
title:
date:
tags:
excerpt:
cover:
author:
---
```

---

# DESIGN 구조

```text
content/design/
```

예:

```text
content/design/gandhara-face.md
```

---

## DESIGN frontmatter 예시

```yaml
---
title:
era:
region:
type:
tags:
image:
sources:
related:
license:
---
```

---

# 핵심 개념

OL DESIGN은:

```text
이미지 저장소
```

가 아니라:

```text
metadata-based visual archive
```

이다.

---

# 11. 추천 컴포넌트 구조

```text
components/
├── ui/
├── layout/
├── typography/
├── cards/
└── relations/
```

---

## 핵심 컴포넌트 예시

```text
OLHero
OLCard
OLBookCard
OLAssetCard
OLRelationPanel
OLMetadataBlock
OLCitationBlock
```

---

# 12. OL DESIGN의 핵심 UX 방향

---

## 목표

Pinterest 느낌이 아니라:

```text
visual research archive
```

구조.

---

## 핵심 기능

### 1. Relation links

예:

* 관련 인물
* 관련 시대
* 관련 건축
* 관련 복식
* 관련 문헌
* 관련 지역

---

### 2. Metadata panel

예:

* 인물
* 시대
* 지역
* 출처
* 라이선스
* AI prompt reference
* 참고 문헌

---

### 3. Filter system

예:

* 인물별
* 시대별
* 지역별
* 전통별
* 유형별

---

# 13. OL HOME 권장 구조

```text
Hero
↓
존재 이유 / 철학
↓
ATLAS / BOOK / DESIGN 진입
↓
대표 컨텐츠
↓
아카이브 소개
↓
조용한 footer
```

---

# 14. 장기적 목표

OL은 단순 웹사이트가 아니라:

```text
connected buddhist knowledge ecosystem
```

을 지향한다.

따라서:

* 컨텐츠 독립성
* markdown 기반
* open archive
* static-first
* forkable structure

가 중요하다.

---

# 15. 최종 정리

## 현재 방향성 요약

```text
Astro
= engine / content infrastructure

Basecoat
= visual foundation

OL CSS
= philosophical identity layer

OL Pages
= experiential variations
```

---

# 핵심 디자인 원칙

```text
조용함
깊은 읽기
수행적 UX
연결성
아카이브성
문헌성
현대적 절제
```

---

# 최종 목표

OL은:

> “불교 컨텐츠를 위한 디지털 공공 인프라이자
> 연결된 수행적 지식 환경”

을 구축하는 방향으로 개발한다.
