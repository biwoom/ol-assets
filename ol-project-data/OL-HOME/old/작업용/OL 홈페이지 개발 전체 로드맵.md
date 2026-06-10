아주 적절한 시점입니다.
지금까지 OL 프로젝트는 철학·브랜드·런타임·콘텐츠 구조·디자인 언어를 정립하는 단계였다면, 이제부터는 그것을 “작동하는 실제 시스템”으로 변환하는 단계로 넘어갑니다.

현재 문서들을 종합하면 OL은 단순 홈페이지가 아니라:

* 정적 아카이브
* 불교 콘텐츠 허브
* OL BOOK 배포 포털
* 디자인 레퍼런스 라이브러리
* 장래의 AI/ATLAS 생태계 진입점

을 모두 포괄하는 “디지털 도량의 입구”로 설계되어 있습니다. 

또한 현재 기술 방향은 명확합니다:

```text
Astro = 엔진
Basecoat = 시각적 기초
OL CSS = 브랜드 정체성
```



따라서 지금 필요한 것은:

> “완벽한 기능 구현”

이 아니라,

> “OL의 철학을 훼손하지 않는 실제 개발 기반 구축”

입니다.

---

# OL 홈페이지 개발 전체 로드맵 (권장 구조)

## 전체 개발 전략

OL HOME은 처음부터 거대한 시스템으로 만들지 않는 것이 중요합니다.

권장 전략:

```text
PHASE 1
정적 기반 구축

↓

PHASE 2
콘텐츠 구조화

↓

PHASE 3
OL BOOK 라이브러리 구축

↓

PHASE 4
ATLAS/BOOK 연동

↓

PHASE 5
OL DESIGN 아카이브

↓

PHASE 6
검색/지식연결/온톨로지

↓

PHASE 7
AI 및 장기 구조
```

---

# PHASE 1 — FOUNDATION 구축 단계

가장 중요합니다.

이 단계 목표는:

> “OL의 미학과 구조를 실제 코드베이스로 고정”

하는 것입니다.

아직 CMS도 필요 없고 DB도 필요 없습니다.

---

# PHASE 1 목표

## 최종 결과물

아래가 작동해야 함:

* Astro 기반 프로젝트 생성
* GitHub 저장소 구조 정리
* Basecoat 통합
* 글로벌 디자인 토큰 구축
* 라우팅 구조 생성
* 홈페이지 샘플 구현
* 다크모드
* 반응형
* typography 시스템
* MDX 콘텐츠 파이프라인
* GitHub Pages 자동 배포

즉:

> “OL 웹사이트 골격 완성”

이 목표입니다.

---

# 권장 기술 스택

## Core

* [Astro](https://astro.build?utm_source=chatgpt.com)
* [Basecoat UI](https://basecoatui.com?utm_source=chatgpt.com)
* [Tailwind CSS](https://tailwindcss.com?utm_source=chatgpt.com)
* [MDX](https://mdxjs.com?utm_source=chatgpt.com)

---

## 배포

* [GitHub Pages](https://pages.github.com?utm_source=chatgpt.com)
* [GitHub Actions](https://github.com/features/actions?utm_source=chatgpt.com)

---

## 권장 구조

```text
OL-HOME/
├─ src/
│  ├─ components/
│  ├─ layouts/
│  ├─ pages/
│  ├─ content/
│  ├─ styles/
│  ├─ data/
│  └─ lib/
│
├─ public/
│  ├─ images/
│  ├─ icons/
│  ├─ fonts/
│  └─ books/
│
├─ content/
├─ astro.config.mjs
├─ tailwind.config.mjs
└─ package.json
```

---

# 페이지 우선순위

Phase1에서 전부 만들 필요 없습니다.

우선순위:

| 우선 | 페이지    | 목적     |
| -- | ------ | ------ |
| 1  | HOME   | 브랜드 입구 |
| 2  | ATLAS  | 도구 소개  |
| 3  | BOOK   | 라이브러리  |
| 4  | DESIGN | 아카이브   |
| 5  | BLOG   | 개발 기록  |
| 6  | AI     | 장래 구상  |

---

# 디자인 시스템 우선순위

현재 styles.css 방향은 매우 좋습니다. 

특히:

* monochrome
* editorial
* low-noise
* typography 중심
* quiet interface

방향이 OL 철학과 정확히 맞습니다.

다만 이제 이것을:

```text
임시 CSS
↓
토큰 기반 디자인 시스템
```

으로 승격해야 합니다.

---

# 추천 디자인 시스템 구조

```text
src/styles/
├─ tokens.css
├─ base.css
├─ typography.css
├─ layout.css
├─ components.css
├─ utilities.css
└─ themes/
    ├─ light.css
    └─ dark.css
```

---

# 콘텐츠 구조 방향

OL은 결국 콘텐츠 프로젝트입니다.

따라서 초기에 반드시:

```text
콘텐츠가 코드보다 우위
```

여야 합니다.

즉:

* md/mdx 우선
* content collections 사용
* JSON 하드코딩 최소화

권장.

---

# BOOK 구조 권장

```text
src/content/books/
  buddha-story/
    chapter-01.mdx
    chapter-02.mdx

  dhammapada/
    verse-001.mdx
```

---

# GitHub 저장소 구조 (권장 최종안)

```text
OL-HOME
→ 홈페이지

OL-ATLAS
→ 에디터 소스코드

OL-BOOKS
→ 완성된 BOOK html

OL-ASSETS
→ 이미지/삽화/SVG/인포그래픽

OL-DOCS
→ 설계서/철학/워크플로우
```

현재 구상과 거의 동일하지만:

```text
OL-CONTENTS
```

보다는:

```text
OL-ASSETS
```

가 더 명확합니다.

---

# 중요한 전략적 결정

## 초기에 절대 하지 말아야 할 것

아래는 늦게 해야 합니다:

* DB
* 사용자 계정
* SaaS 구조
* 서버 렌더링
* 복잡한 검색엔진
* 벡터DB
* 실시간 기능

OL 철학 자체가:

```text
static-first
low-noise
deep reading
```

이기 때문입니다. 

---

# 가장 중요한 개발 원칙

## “조용한 인터페이스”

현재 웹은:

* 과잉 CTA
* 과잉 motion
* startup aesthetic
* dopamine UX

가 지배적입니다.

OL은 정반대여야 합니다.

즉:

* 깊은 여백
* 낮은 자극
* 읽기 중심
* contemplative rhythm
* 수행적 UX

가 핵심입니다. 

---

# 로컬 에이전트용 PHASE 1 작업지시서

아래 문서는 그대로 로컬 에이전트(Codex CLI / Claude Code / Cursor Agent 등)에 전달 가능한 형태입니다.

---

# OL HOME — Phase 1 작업지시서

## 프로젝트 목표

OL 프로젝트 홈페이지의 foundational frontend architecture 구축.

철학:

* static-first
* contemplative editorial UI
* low-noise interface
* typography-centered UX
* deep reading optimized

기술 방향:

```text
Astro = engine
Basecoat = visual foundation
OL CSS = brand identity
```

---

# 기술 스택

## 필수

* Astro
* Tailwind CSS
* Basecoat UI
* TypeScript
* MDX

## 배포

* GitHub Pages
* GitHub Actions

---

# 구현 목표

다음을 완료:

## 1. Astro 프로젝트 초기화

* 최신 Astro 설치
* TypeScript strict mode
* Tailwind 통합
* MDX 통합

---

## 2. 프로젝트 구조 생성

다음 구조 생성:

```text
src/
  components/
  layouts/
  pages/
  content/
  styles/
  data/
  lib/

public/
  images/
  icons/
  books/
```

---

## 3. 글로벌 디자인 시스템 구축

현재 제공된 styles.css 기반으로:

### 분리 구조 생성

```text
tokens.css
base.css
typography.css
layout.css
components.css
utilities.css
```

### 유지해야 할 핵심 미학

* monochrome
* quiet interface
* editorial minimalism
* soft borders
* large whitespace
* typography rhythm

---

## 4. Basecoat 통합

* Basecoat 기반 UI 적용
* shadcn/ui aesthetic 유지
* 과도한 SaaS 느낌 제거

금지:

* neon
* gradient-heavy
* startup hero
* aggressive CTA
* dashboard aesthetic

---

## 5. 라우팅 생성

다음 페이지 생성:

```text
/
 /atlas
 /book
 /design
 /ai
 /blog
```

---

## 6. HOME 페이지 구현

제공된 HTML 샘플 기반 구현:

필수 섹션:

* Header
* Hero
* Project Cards
* Manifest
* Stats
* Latest Updates
* Footer

---

## 7. Layout 시스템 구축

구현:

* MainLayout
* ContentLayout
* EditorialLayout

---

## 8. Typography 시스템 구축

폰트:

* Inter
* Noto Sans KR
* JetBrains Mono

구현:

* prose typography
* Korean readability optimization
* long-form reading spacing
* responsive typography scale

---

## 9. 다크모드 구현

조건:

* class 기반 theme switching
* localStorage persistence
* light/dark only

다크모드도 “조용한 흑백” 유지.

---

## 10. 반응형 구현

기준:

* mobile-first
* tablet optimization
* desktop editorial layout

모바일에서:

* 과도한 animation 제거
* typography 우선
* spacing 유지

---

## 11. Content Collections 설정

Astro content collections 사용.

초기 구조:

```text
content/
  blog/
  books/
  updates/
```

---

## 12. GitHub Pages 배포

구현:

* GitHub Actions workflow
* 자동 배포
* main branch deploy

---

# 개발 원칙

## 반드시 유지

* static-first
* accessibility
* semantic HTML
* low JS
* performance-first

---

## 절대 금지

* SPA obsession
* unnecessary animation
* dashboard UI
* excessive interactivity
* SaaS marketing patterns

---

# 디자인 키워드

```text
contemplative
editorial
archive
library
monastic minimalism
deep reading
quiet interface
```

---

# 완료 조건

다음 상태이면 완료:

* GitHub Pages 정상 배포
* 모든 페이지 라우팅 정상
* 모바일/데스크탑 반응형 정상
* 다크모드 정상
* typography 시스템 정상
* Lighthouse 성능 우수
* 정적 export 정상

---

# 우선순위

가장 중요한 순서:

1. typography
2. spacing rhythm
3. reading experience
4. information architecture
5. responsiveness
6. animation

animation은 마지막.

---

# 구현 철학

OL은 SaaS가 아니다.

OL은:

> “불교 지식과 수행을 위한 디지털 도량”

이어야 한다.

따라서 UI는 사용자를 흥분시키기보다:

* 머무르게 하고
* 읽게 하고
* 사유하게 하고
* 다시 삶으로 돌아가게 해야 한다.

---

추가로 원하시면 다음 단계도 이어서 설계 가능합니다:

* Phase2 콘텐츠 아키텍처
* Astro 컴포넌트 구조 설계
* 실제 GitHub Organization 구조
* ATLAS ↔ BOOK 연동 전략
* OL 홈페이지 IA(site map)
* Tailwind/Basecoat 토큰 구조
* Astro content collections schema 설계
* 로컬 AI 협업 워크플로우
* Codex CLI 전용 작업 분할 시스템
* Cursor/Claude Code용 agent prompt 체계
