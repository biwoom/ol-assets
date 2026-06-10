# Phase 1 구현이 완료 및 검증과 수정

**`npm run build` 성공 — 14페이지 생성:**

|경로|설명|
|---|---|
|`/`|HOME|
|`/atlas`|ATLAS 툴 소개|
|`/ai`|AI R&D 구상|
|`/book`|BOOK 라이브러리|
|`/book/buddha-story/01-birth`|붓다 스토리 1장|
|`/blog`|블로그 목록|
|`/blog/atlas-v042`|블로그 포스트|
|`/design`|DESIGN 아카이브|
|`/entity`|지식 그래프 전체|
|`/entity/persons/nagarjuna`|나가르주나 ✓|
|`/entity/persons/siddhartha-gautama`|석가모니|
|`/entity/concepts/sunyata`|공(空)|
|`/entity/concepts/dependent-origination`|연기(緣起)|
|`/entity/places/lumbini`|룸비니|

**마이그레이션 과정에서 해결한 주요 이슈:**

- Astro 6는 레거시 `src/content/config.ts` 미지원 → `src/content.config.ts` + `glob()` 로더로 마이그레이션
- Book 챕터 파일이 서브디렉토리 구조라 `[slug]` 라우트 불가 → `[...slug]` rest route로 변경
- `entry.render()` → `render(entry)` (새 Content Layer API)
- `OLEntityPanel` 컴포넌트의 prop 인터페이스 수정 (`entity.data.xxx` → `entity.xxx`)

---

# 1차 검증

phase1. 완료후 검증: dev 서버에서 확인해보니 헤더 메뉴 클릭해보니 연결 안됨. 그래서 http://localhost:4321/ol-home/atlas 이 주소로 연결하니 연결됨. 깃헙페이지 주소도 베이스가 biwoom.github.io/ol-home 이 될 예정. 그렇다면 로컬 개발시 주소 정책을 어떻게 가져가야 하지?

## 1차 검증 해결책

이건 Astro의 `base` 설정 때문에 발생하는 매우 흔한 이슈입니다. 원인부터 짚고 해결책을 드리겠습니다.

---

## 원인 진단

`astro.config.mjs`에 이렇게 설정되어 있을 겁니다:

```javascript
export default defineConfig({
  site: 'https://biwoom.github.io',
  base: '/ol-home',
  // ...
});
```

이 `base: '/ol-home'` 때문에 Astro의 모든 정적 자산과 페이지가 `/ol-home/...` 접두어 아래에 배치됩니다. 로컬 서버에서도 마찬가지입니다.

문제는 **링크 작성 방식**입니다.

```astro
<!-- 잘못된 방식 -->
<a href="/atlas">ATLAS</a>
<!-- → 브라우저는 localhost:4321/atlas 로 가려고 함 → 404 -->

<!-- 올바른 방식 (수동) -->
<a href="/ol-home/atlas">ATLAS</a>
<!-- → 동작은 하지만 base가 바뀌면 전부 수정해야 함 -->
```

`href="/atlas"`는 절대 경로라서 `base`를 무시합니다. Astro는 이 경우 자동으로 base를 붙여주지 **않습니다**.

---

## 해결책 — 세 가지 방법

### 방법 1: `import.meta.env.BASE_URL` 사용 (권장)

Astro가 자동으로 제공하는 환경 변수입니다. 로컬과 배포 환경 모두에서 올바르게 동작합니다.
`
### 방법 2: 헬퍼 함수로 추상화 (더 권장)

링크가 많아지면 매번 `${base}...` 쓰는 게 번거롭고 실수하기 쉽습니다. 헬퍼 함수를 만드세요.

`src/lib/url.ts` 생성:

```typescript
/**
 * Astro base path를 자동으로 붙여주는 URL 헬퍼.
 * 로컬 (base=/ol-home) 과 배포 환경 모두에서 안전.
 *
 * 사용:
 *   url('/atlas')      → '/ol-home/atlas'
 *   url('atlas')       → '/ol-home/atlas'
 *   url('/')           → '/ol-home/'
 */
export function url(path: string): string {
  const base = import.meta.env.BASE_URL;        // "/ol-home/"
  const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;  // "/ol-home"
  const cleanPath = path.startsWith('/') ? path : `/${path}`;       // "/atlas"
  return `${cleanBase}${cleanPath}`;
}
```

사용 예시:

```astro
---
import { url } from '../../lib/url';

const navItems = [
  { href: url('/'),       label: 'HOME' },
  { href: url('/atlas'),  label: 'ATLAS' },
  { href: url('/book'),   label: 'BOOK' },
  { href: url('/design'), label: 'DESIGN' },
  { href: url('/ai'),     label: 'AI' },
];
---

<a href={url('/blog')}>BLOG</a>
<img src={url('/images/logo.png')} />
```

장점: `base` 설정이 바뀌어도 코드를 고칠 필요 없음. 실수 방지.

## 권장 결론

**방법 2 (헬퍼 함수)를 채택**하세요. 이유:

1. 코드가 깔끔: `url('/atlas')` 가 `${base}atlas` 보다 읽기 쉬움
2. 한 곳에서 관리: 나중에 도메인 정책이 바뀌어도 `url.ts` 한 파일만 수정
3. 실수 방지: 슬래시 위치를 매번 신경 쓸 필요 없음
4. 환경 일관성: 로컬 = 배포 동일하게 동작

---

## 적용해야 할 위치 (체크리스트)

- [ ] `src/lib/url.ts` 생성
- [ ] `OLHeader.astro` — 모든 nav 링크
- [ ] `OLFooter.astro` — 모든 footer 링크
- [ ] `OLProductCards.astro` — 6개 카드 링크
- [ ] `OLHero.astro` — 버튼 링크
- [ ] `OLLatestUpdates.astro` — 카드 링크
- [ ] 모든 페이지(`index.astro`, `atlas.astro` 등) 내부 링크
- [ ] `<img src=...>` 의 정적 이미지 경로 (`public/images/` 참조하는 경우)

> **참고**: `import` 문에서 가져오는 이미지(`import logo from '../assets/logo.png'`)는 Astro가 자동 처리하므로 `url()` 불필요. `<img src="/images/..." />` 같은 직접 경로만 `url()` 필요.

---

## 검증 방법

수정 후:

```bash
# 1. 로컬 dev
npm run dev
# → localhost:4321/ol-home/ 에서 모든 링크 클릭 동작 확인

# 2. 로컬 build + preview (배포 환경 시뮬레이션)
npm run build
npm run preview
# → 마찬가지로 모든 링크 확인

# 3. GitHub Pages 배포 후
# → biwoom.github.io/ol-home/ 에서 동일하게 동작해야 함
```

세 환경에서 동일하게 동작하면 성공입니다.

---

# Phase 1 이후 현재 상태 보고

# OL HOME — 프로젝트 현황 문서

> 최종 업데이트: 2026-05-29  
> 현재 단계: **Phase 1 완료**

---

## 기술 스택

| 항목 | 버전 / 값 |
|------|-----------|
| Astro | 6.3.8 (Content Layer API) |
| Tailwind CSS | v4.3.0 |
| Basecoat CSS | 0.3.11 (shadcn/ui 기반 컴포넌트 기반) |
| MDX | @astrojs/mdx 5.0.6 |
| Node.js | ≥ 22.12.0 |
| 배포 | GitHub Pages (`biwoom.github.io/ol-home`) |
| base 경로 | `/ol-home` |

---

## 현재 파일 구조

```
ol-home/
├── astro.config.mjs              # site + base 설정
├── tsconfig.json
├── package.json
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Pages 자동 배포
│
├── public/
│   ├── images/                   # (비어 있음 — Phase 2에서 채움)
│   ├── icons/
│   └── books/
│
└── src/
    ├── content.config.ts         # Content Collections 스키마 (glob 로더)
    │
    ├── content/
    │   ├── blog/
    │   │   └── atlas-v042.md     # 샘플 블로그 포스트 1편
    │   ├── book/
    │   │   └── buddha-story/
    │   │       └── 01-birth.md   # 붓다 스토리 1장 샘플
    │   ├── design/               # (비어 있음 — .gitkeep)
    │   ├── ai/                   # (비어 있음 — .gitkeep)
    │   ├── entities/
    │   │   ├── persons/
    │   │   │   ├── nagarjuna.md
    │   │   │   └── siddhartha-gautama.md
    │   │   ├── concepts/
    │   │   │   ├── sunyata.md
    │   │   │   └── dependent-origination.md
    │   │   └── places/
    │   │       └── lumbini.md
    │   └── ontology/
    │       ├── entity-types.md   # 7가지 엔티티 유형 정의
    │       └── relation-types.md # 관계(predicate) 유형 정의
    │
    ├── styles/
    │   ├── global.css            # @import 체인: tailwind → basecoat → tokens → ol-components
    │   ├── tokens.css            # OL 디자인 토큰 (CSS 변수, 다크모드)
    │   └── ol-components.css     # .ol-* 클래스 전체 (헤더·카드·버튼·배지 등)
    │
    ├── layouts/
    │   ├── BaseLayout.astro      # 모든 페이지의 기반 (폰트, FOUC 방지, Header/Footer 포함)
    │   ├── PageLayout.astro      # BaseLayout 래퍼
    │   ├── BookLayout.astro      # 장문 독서용 레이아웃
    │   └── EntityLayout.astro    # Entity 상세 페이지용 레이아웃
    │
    ├── components/
    │   ├── layout/
    │   │   ├── OLHeader.astro    # 스티키 헤더, 네비, 다크모드 토글
    │   │   └── OLFooter.astro    # 4컬럼 푸터
    │   ├── home/
    │   │   ├── OLHero.astro      # 홈 히어로 섹션
    │   │   ├── OLProductCards.astro  # 6개 프로덕트 카드
    │   │   ├── OLManifest.astro  # 선언문 다크 섹션
    │   │   ├── OLStats.astro     # 숫자 통계 4개
    │   │   └── OLLatestUpdates.astro # 최신 업데이트 카드 3개
    │   ├── entity/
    │   │   ├── OLEntityCard.astro    # Entity 미리보기 카드
    │   │   ├── OLEntityPanel.astro   # Entity 사이드바 패널
    │   │   └── OLRelationLinks.astro # 관계 링크 목록
    │   ├── book/
    │   │   ├── OLBookCard.astro      # 책 표지 카드
    │   │   └── OLBookReader.astro    # (Phase 3 스텁)
    │   ├── graph/
    │   │   └── OLGraphView.astro     # (Phase 5 스텁)
    │   └── ui/
    │       ├── OLBadge.astro
    │       └── OLButton.astro
    │
    ├── lib/
    │   ├── url.ts                # url() 헬퍼: base 경로 자동 처리
    │   ├── relations.ts          # 지식 그래프: Triple 타입, buildKnowledgeGraph 등
    │   └── search.ts             # 검색 인덱스 빌더
    │
    ├── data/
    │   └── nav.ts                # NavItem 타입 + navItems 배열
    │
    └── pages/
        ├── index.astro           # HOME (컴포넌트 5개 조립)
        ├── atlas.astro           # ATLAS 툴 소개
        ├── ai.astro              # AI R&D 구상
        ├── blog/
        │   ├── index.astro       # 블로그 목록 (Content Collections)
        │   └── [slug].astro      # 블로그 개별 포스트
        ├── book/
        │   ├── index.astro       # BOOK 라이브러리
        │   └── [...slug].astro   # 책 개별 챕터 (rest route — 서브디렉토리 지원)
        ├── design/
        │   ├── index.astro       # DESIGN 아카이브
        │   └── [slug].astro      # DESIGN 개별 항목
        └── entity/
            ├── index.astro       # 전체 Entity 목록 (유형별 그룹)
            └── [type]/
                └── [id].astro    # Entity 상세 페이지
```

---

## 생성되는 페이지 (14개)

| URL | 설명 |
|-----|------|
| `/ol-home/` | HOME |
| `/ol-home/atlas` | ATLAS 툴 소개 |
| `/ol-home/ai` | AI R&D |
| `/ol-home/book` | BOOK 라이브러리 |
| `/ol-home/book/buddha-story/01-birth` | 붓다 스토리 1장 |
| `/ol-home/blog` | 블로그 목록 |
| `/ol-home/blog/atlas-v042` | 블로그 포스트 |
| `/ol-home/design` | DESIGN 아카이브 |
| `/ol-home/entity` | 지식 그래프 전체 목록 |
| `/ol-home/entity/persons/nagarjuna` | 나가르주나 |
| `/ol-home/entity/persons/siddhartha-gautama` | 싯다르타 가우타마 |
| `/ol-home/entity/concepts/sunyata` | 공(空) |
| `/ol-home/entity/concepts/dependent-origination` | 연기(緣起) |
| `/ol-home/entity/places/lumbini` | 룸비니 |

---

## Phase 1 작업 이력 (주요 결정·변경)

### 초기 설치 (Phase 0 — 이전 세션)
- Astro 6.3.8 + Tailwind CSS v4 + Basecoat CSS + MDX 설치
- `astro.config.mjs`: `site`, `base: '/ol-home'` 설정

### 스타일 시스템 구축
- `tokens.css` 생성: `--ol-bg`, `--ol-ink`, `--ol-border` 등 CSS 변수 + `.dark` 오버라이드
- `ol-components.css` 생성: 샘플 HTML 스타일을 `.ol-` 접두어로 전환
  - 원본: `.btn`, `.card`, `.hero` → 변환: `.ol-btn`, `.ol-card`, `.ol-hero`
  - 다크모드 아이콘 가시성, 반응형 `@media` 포함

### Content Collections 마이그레이션
- **문제**: Astro 6에서 `src/content/config.ts` (레거시 API) 지원 중단
- **해결**: `src/content.config.ts`로 이동 + `glob()` 로더 방식으로 전환
  - 모든 컬렉션에 `loader: glob({ pattern: '**/*.{md,mdx}', base: '...' })` 추가
  - `entry.render()` → `import { render } from 'astro:content'` + `render(entry)` 변경
  - `entry.slug` → `entry.id` 변경 (새 API에서 `.slug` 제거됨)

### Book 라우트 변경
- **문제**: `book/[slug].astro` + `entry.id = 'buddha-story/01-birth'` (슬래시 포함) → 단일 세그먼트 라우트 매칭 실패
- **해결**: `book/[...slug].astro` (rest route)로 변경
- **이유**: 책 챕터는 서브디렉토리(`buddha-story/01-birth.md`) 구조이므로 다중 세그먼트 필요

### Entity 데이터 스키마 수정
- **문제**: entity 파일의 `description` 필드가 YAML 오브젝트(`ko: "..."`)인데, 스키마는 `z.string()` 기대 → Zod 검증 실패
- **해결**: 모든 entity 파일에서 `description`을 단순 문자열로 변경

### OLEntityPanel 인터페이스 수정
- **문제**: 컴포넌트가 `entity.data.name.ko` 접근을 시도하지만, 페이지에서 `entry.data`(데이터 자체)를 전달
- **해결**: Props 인터페이스를 `{ entity: { data: ... } }` → `{ entity: { id, type, name, ... } }` 로 수정

### base URL 처리 (`url()` 헬퍼 도입)
- **문제**: `href="/atlas"` 같은 절대 경로가 `base: '/ol-home'`을 무시 → 로컬·배포 모두 404
- **해결**: `src/lib/url.ts`에 `url()` 헬퍼 함수 생성
  - `url('/atlas')` → `/ol-home/atlas`
  - `BASE_URL` 환경 변수 기반이므로 배포 설정 변경 시 자동 반영
- **수정 파일**: OLHeader, OLFooter, OLHero, OLProductCards, OLLatestUpdates, OLEntityCard, OLRelationLinks, blog/index, blog/[slug]

---

## Content Collections 스키마 요약

### entities 컬렉션 (단일 컬렉션, 7개 유형)
```
Zod discriminatedUnion('type', [
  PersonSchema   — era, tradition, nationality
  PlaceSchema    — location(lat/lng), era
  ConceptSchema  — tradition, complexity
  TextSchema     — author, language, era
  EventSchema    — date, location, participants
  PracticeSchema — tradition, level
  SchoolSchema   — founded, era, region
])
```
공통 필드: `id`, `type`, `name(ko/en/pali/sanskrit/chinese)`, `aliases`, `description`, `relations[]`, `tags[]`, `sources[]`, `external_ids`, `published`

### 관계(Triple) 구조
```typescript
{ subject: string, predicate: string, object: string, source?, note? }
```

### 기타 컬렉션
- `blog`: title, description, date, readingTime, category, published
- `book`: title, series, order, entities[], relations[], published
- `design`: title, category, type, era, license(CC0), published
- `ai`: title, date, type, published
- `ontology`: title, version

---

## 알려진 한계 / Phase 2 이후 과제

| 항목 | 내용 |
|------|------|
| `design` / `ai` 컨텐츠 없음 | 빈 디렉토리. 빌드 시 경고 발생하나 오류 아님 |
| OLBookReader | Phase 3 스텁. 실제 ATLAS 뷰어 연동 필요 |
| OLGraphView | Phase 5 스텁. D3.js 또는 Cytoscape 연동 예정 |
| 관계 링크 표시 | OLRelationLinks가 `rel.object` ID 그대로 표시. 실제 entity 이름 조회 필요 |
| 검색 | `search.ts` 인덱스 빌더 구현됨. 프론트엔드 UI 미구현 |
| RSS | `/rss.xml` 링크만 존재. Astro RSS 피드 생성 미구현 |
| 이미지 경로 | `public/images/` 비어 있음. `url('/images/...')` 사용 예정 |
