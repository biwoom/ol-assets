# OL HOME — 현재 상태 보고서
> 검색 기능 추가 전 핸드오버 문서  
> 기준일: 2026-05-30

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| 프레임워크 | Astro 6.3.8 (Static Site Generation) |
| 배포 대상 | GitHub Pages — `https://biwoom.github.io/ol-home` |
| base 경로 | `/ol-home` (astro.config.mjs `base` 설정) |
| 스타일 | 커스텀 디자인 시스템 + Tailwind v4 + basecoat-css |
| 콘텐츠 도메인 | 불교 콘텐츠 (한국어 주 / 팔리어·산스크리트 병기) |

**빌드 상태**: `npm run build` 무오류, 17페이지 생성.

---

## 2. 파일 구조

```
src/
├── components/
│   ├── book/          OLBookCard, OLBookReader
│   ├── entity/        OLEntityCard, OLEntityPanel, OLRelationLinks
│   ├── graph/         OLGraphView (미구현, 스텁)
│   ├── home/          OLHero, OLLatestUpdates, OLManifest, OLProductCards, OLStats
│   ├── layout/        OLHeader, OLFooter
│   └── ui/            OLBadge, OLButton
│
├── content/
│   ├── works/         단일 컬렉션, 챕터 단위 md — 현재 1편 (published: true)
│   │   └── buddha-story/01-birth.md
│   ├── entities/      인물·장소·개념 5편 (published: true)
│   │   ├── persons/   siddhartha-gautama, nagarjuna
│   │   ├── places/    lumbini
│   │   └── concepts/  dependent-origination, sunyata
│   ├── book/          출판물 메타 2편 (buddha-story 1편 published)
│   ├── blog/          2편 (atlas-v042 published, test 미공개)
│   ├── design/        비어 있음 (.gitkeep)
│   ├── ai/            비어 있음 (.gitkeep)
│   └── ontology/      entity-types, relation-types (내부 참조용)
│
├── layouts/
│   ├── BaseLayout.astro      HTML 셸, 헤더/푸터, 다크모드/사이드바 FOUC 방지 스크립트
│   ├── WorksLayout.astro     WORKS 전용 레이아웃 (사이드바 + TOC)
│   ├── BookLayout.astro
│   ├── EntityLayout.astro
│   └── PageLayout.astro
│
├── lib/
│   ├── url.ts         base 경로 처리 헬퍼 — 모든 내부 링크는 url() 통과 필수
│   ├── search.ts      검색 인덱스 빌더 (스캐폴드 완성, 미연결)
│   └── relations.ts   Entity 관계 처리
│
├── pages/
│   ├── index.astro
│   ├── atlas.astro
│   ├── works/[...slug].astro
│   ├── works/index.astro
│   ├── book/[...slug].astro
│   ├── book/index.astro
│   ├── entity/[type]/[id].astro
│   ├── entity/index.astro
│   ├── blog/[slug].astro
│   ├── blog/index.astro
│   ├── design/[slug].astro   (빈 컬렉션, 빌드는 통과)
│   ├── design/index.astro
│   └── ai.astro
│
├── styles/
│   ├── tokens.css     디자인 토큰 (색상·타이포·간격·radius·shadow)
│   ├── ol-components.css  컴포넌트 스타일 (1,215줄)
│   └── global.css     @import 순서: tailwind → basecoat → tokens → ol-components
│
├── data/
│   └── nav.ts         (현재 OLHeader.astro 내부 배열 직접 사용 — 이 파일은 미사용)
│
└── content.config.ts  Zod 스키마 정의 + collections export
```

---

## 3. 디자인 시스템

### 3.1 레이아웃 기준

- **헤더**: `position: sticky; top: 0; z-index: 50; height: 64px`
- **컨테이너**: `max-width: 1200px; margin: 0 auto; padding: 0 32px` (`.ol-container`)
- **모든 섹션 레이아웃**은 이 1200px 기준에 맞춰 설계

### 3.2 토큰 (tokens.css)

| 그룹 | 주요 변수 |
|------|----------|
| 색상 | `--ol-bg`, `--ol-surface`, `--ol-surface-2`, `--ol-ink`, `--ol-muted`, `--ol-border` |
| 폰트 | `--ol-font-sans` (Inter/Noto Sans KR), `--ol-font-mono` (JetBrains Mono) |
| 반경 | `--ol-r-sm (6px)`, `--ol-r (8px)`, `--ol-r-lg (14px)` |

다크모드: `.dark` 클래스 + CSS 변수 오버라이드. 토글은 localStorage 연동.

### 3.3 스크롤 동작

```css
html { scroll-padding-top: 80px; }  /* 헤더 64px + 여백 16px */
```
모든 `#` 앵커 스크롤 시 헤더 하단에 정확히 위치.

---

## 4. WORKS 레이아웃 (최근 수정 완료)

WORKS 페이지는 전체 프로젝트에서 가장 복잡한 레이아웃입니다. 최근 수정으로 완성된 상태입니다.

### 4.1 HTML 구조

```
<BaseLayout>
  <button class="ol-sidebar-toggle">   <!-- 모바일 전용 (900px 이하) -->
  <div class="ol-works-outer">          <!-- 1200px 중앙정렬 래퍼 -->
    <aside class="ol-works-sidebar">   <!-- position: sticky, flex child -->
    <div class="ol-works-layout">      <!-- flex: 1, grid 내부 -->
      <main class="ol-works-main">
      <aside><!-- TOC slot --></aside>  <!-- slug 페이지에만 존재 -->
    </div>
  </div>
</BaseLayout>
```

### 4.2 사이드바 동작

| 상태 | CSS |
|------|-----|
| 열림 (기본) | `width: 240px` |
| 닫힘 | `[data-works-sidebar="closed"]` → `width: 40px` |
| 전환 | `transition: width 200ms ease` |
| 상태 저장 | `localStorage('ol-works-sidebar')` |
| FOUC 방지 | `BaseLayout.astro` `<head>` 내 `is:inline` 스크립트 |

**반응형**:
- 900px 이하: `position: fixed; transform: translateX(-100%)` 오버레이 방식
- 토글 버튼 `aria-hidden` 속성으로 제어

### 4.3 TOC (오른쪽 목차)

- `[...slug].astro`에서만 `slot="toc"` 사용
- JS로 `.ol-prose h2, h3` 수집 → `#heading-N` ID 자동 부여
- `IntersectionObserver`로 현재 위치 하이라이트
- 헤딩 < 2개면 TOC 숨김
- 1100px 이하 반응형에서 TOC 숨김

---

## 5. 콘텐츠 컬렉션 스키마 요약

### 5.1 works

```typescript
{
  title: string
  series?: string         // 시리즈명 (예: "OL 붓다 스토리")
  chapter?: number
  order: number           // 정렬 기준
  date?: Date
  status: 'draft' | 'revising' | 'ready' | 'published'
  entities: string[]      // entity ID 참조
  relations: Relation[]
  primary_entity?: string
  sources: { text, ref?, passage? }[]
  tags: string[]
  published: boolean      // 기본값: false
  excerpt?: string
}
```

### 5.2 entities (discriminatedUnion)

type별 스키마 분기: `person | place | concept | text | event | practice | school`

공통 필드:
```typescript
{
  id: string              // URL 식별자 (예: "siddhartha-gautama")
  type: EntityType
  name: { ko, en?, pali?, sanskrit?, chinese? }
  aliases: string[]
  description?: string
  relations: Relation[]   // subject–predicate–object 트리플
  tags: string[]
  sources: string[]
  external_ids?: { wikidata?, cbeta?, suttacentral?, wikipedia_ko? }
  published: boolean
}
```

### 5.3 Relation 스키마

```typescript
{ subject: string, predicate: string, object: string, source?, note? }
```
predicate 예시: `born_in`, `is_related_to`, `founded`, `taught_at`

---

## 6. 검색 인덱스 스캐폴드 (`src/lib/search.ts`)

이미 작성된 `buildSearchIndex()` 함수가 있습니다. **현재 어떤 페이지에도 연결되어 있지 않습니다.**

```typescript
// 반환 타입 (추론)
type SearchRecord = {
  type: 'works' | 'entity' | 'design' | 'blog'
  id: string
  title: string
  excerpt: string
  entities: string[]   // 연결된 entity ID
  tags: string[]
  url: string          // base 경로 없음 — url() 처리 필요
}
```

**현재 문제점**:
1. `published` 필터가 `e.data.published` (boolean)를 직접 getCollection 두 번째 인자로 넘기고 있음 → `getCollection('works', e => e.data.published !== false)` 패턴과 다름
2. `url` 필드에 `url()` 헬퍼를 거치지 않아 GitHub Pages base 경로 누락
3. `book` 컬렉션은 인덱스에 포함되지 않음
4. entity의 `aliases` (예: "석가모니", "붓다") 가 인덱스에 없어 별칭 검색 불가

---

## 7. 검색 기능 추가 시 고려사항

### 7.1 아키텍처 선택

정적 사이트이므로 세 가지 옵션이 현실적입니다:

| 방식 | 라이브러리 | 특징 |
|------|-----------|------|
| **빌드 타임 인덱스 + 클라이언트 검색** | [Pagefind](https://pagefind.app/) | Astro 공식 권장, 한국어 부분 지원, 추가 설정 거의 없음 |
| **런타임 JSON 인덱스** | [Fuse.js](https://www.fusejs.io/) | 작은 번들, 퍼지 검색, 한국어 토크나이징 약함 |
| **런타임 JSON 인덱스** | [MiniSearch](https://lucaong.github.io/minisearch/) | 필드 가중치 지원, 한국어 커스텀 토크나이저 연동 가능 |

**추천**: 콘텐츠 양이 적고(현재 ~10개 문서) 한국어 중심이므로 **MiniSearch + 빌드 타임 JSON 엔드포인트** 조합이 가장 적합합니다. 한국어는 공백 기준 토크나이저가 충분히 작동합니다.

### 7.2 JSON 인덱스 엔드포인트 구현

`src/pages/search.json.ts` 파일로 빌드 타임에 JSON 생성:

```typescript
// src/pages/search.json.ts
import type { APIRoute } from 'astro';
import { buildSearchIndex } from '../lib/search';
import { url } from '../lib/url';

export const GET: APIRoute = async () => {
  const index = await buildSearchIndex();
  // url() 처리를 여기서 적용
  const withBase = index.map(r => ({ ...r, url: url(r.url) }));
  return new Response(JSON.stringify(withBase), {
    headers: { 'Content-Type': 'application/json' },
  });
};
```

접근 경로: `/ol-home/search.json`

### 7.3 search.ts 수정 필요 항목

```typescript
// 현재 (버그)
getCollection('works', e => e.data.published)
// 수정
getCollection('works', e => e.data.published !== false)

// 추가 필요: aliases 포함
aliases: doc.data.aliases ?? [],   // entity 검색 강화

// 추가 필요: book 컬렉션
...books.map(doc => ({
  type: 'book' as const,
  id: doc.id,
  title: doc.data.title,
  excerpt: doc.data.description ?? '',
  tags: doc.data.tags ?? [],
  url: `/book/${doc.id}`,
})),
```

### 7.4 UI 배치 옵션

| 위치 | 방식 | 장단점 |
|------|------|--------|
| **헤더 검색 버튼** | 버튼 클릭 → 전체화면 모달 | 어느 페이지에서나 접근 가능, UX 명확 |
| **WORKS 사이드바 상단** | 인라인 입력창 | WORKS 전용, 구현 단순 |
| **전용 `/search` 페이지** | URL 파라미터 기반 | 딥링크 가능, 공유 가능 |

**추천**: 헤더에 검색 아이콘 버튼 → **Cmd+K 스타일 팔레트 모달** (전역 접근, 현재 헤더 오른쪽 `ol-header-right` 영역에 자연스럽게 추가 가능)

### 7.5 한국어 특이사항

- 단어가 띄어쓰기로 구분되므로 공백 토크나이저 사용 가능
- 단, 붙여쓴 용어 (`연기법`, `공성`, `도솔천`) 는 형태소 분석 없이도 그대로 매칭됨
- 팔리어·산스크리트 용어 (`Nidānakathā`, `sunyata`) 는 ASCII로 저장되어 검색 용이
- entity `aliases` 필드에 한자·이표기 수록 → 이를 검색 인덱스에 포함하는 것이 핵심

### 7.6 헤더 수정 시 주의

`OLHeader.astro`는 모든 레이아웃에서 공유됩니다. WORKS 페이지의 경우 헤더가 `z-index: 50`이고 WORKS 사이드바가 `z-index: 10`이므로, 검색 모달은 `z-index: 100` 이상으로 설정해야 합니다.

---

## 8. 현재 미완성/빈 영역

| 섹션 | 상태 | 비고 |
|------|------|------|
| DESIGN | 컬렉션 비어 있음 | 빌드는 통과, 인덱스 페이지만 존재 |
| AI | 컬렉션 비어 있음 | 헤더 네비에서 주석 처리됨 |
| Graph View | 스텁만 있음 | `OLGraphView.astro` 내용 없음 |
| `src/data/nav.ts` | 미사용 | `OLHeader.astro`가 내부 배열 직접 사용 |
| 검색 | `search.ts` 스캐폴드만 | 페이지·UI 미연결 |

---

## 9. 빌드 환경

```bash
node >= 22.12.0
npm run dev      # astro dev
npm run build    # astro build (dist/ 생성)
npm run preview  # astro preview
```

`npm run build` 결과물은 `dist/` 폴더에 정적 HTML/CSS/JS로 출력되며, GitHub Actions로 `gh-pages` 브랜치에 자동 배포됩니다 (설정 여부 미확인, 로컬 빌드만 확인됨).

---

*이 문서는 코드 실제 상태를 기준으로 작성되었습니다. 추가 수정 후 업데이트 필요.*
