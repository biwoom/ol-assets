# OL HOME — Phase 2 작업지시서
## WORKS 메뉴 신설 + BLOG 자동반영

> **전제 조건**: Phase 1 완료, GitHub Pages 정상 배포 상태
> **참조 문서**: 주의지침(BOOK/WORKS 분기), v2 작업지시서
> **핵심 원칙**: OL 디자인 시스템(`ol-` 클래스, `url()` 헬퍼) 일관 적용

---

## Phase 1 실제 구현과의 차이 — 반드시 준수

```
[Phase 1 실제 구현과의 차이 — 반드시 준수]

1. 설정 파일 경로
   작업지시서의 src/content/config.ts
   → 실제: src/content.config.ts (프로젝트 루트에 위치)

2. Content Collection 정의 방식
   작업지시서의 defineCollection({ type: 'content', schema })
   → 실제: defineCollection({ loader: glob({ pattern, base }), schema })
   모든 collection에 glob() 로더 추가 필수.
   glob import: import { glob } from 'astro/loaders';

3. entry ID 접근
   작업지시서의 entry.slug, post.slug
   → 실제: entry.id, post.id
   Astro 6에서 .slug 제거됨.

4. 콘텐츠 렌더링
   작업지시서의 const { Content } = await entry.render()
   → 실제: import { render } from 'astro:content'
            const { Content } = await render(entry)

5. blog 스키마 필드
   작업지시서의 post.data.excerpt
   → 실제: post.data.description
   blog collection 스키마: title, description, date, readingTime, category, published
```
## 사전 맥락 (에이전트에게 전달)

이 프로젝트는 OL — 불교 콘텐츠 프로젝트 홈페이지입니다.
Phase 1에서 구축된 Astro + Basecoat + OL CSS 기반 위에 작업합니다.

**디자인 원칙**:
- OL 고유 CSS 토큰(`--ol-bg`, `--ol-ink` 등) 우선 사용
- Basecoat 클래스는 구조·인터랙션용, OL 클래스로 스타일 오버라이드
- 무채색(monochrome), 큰 여백, 타이포그래피 중심
- `url()` 헬퍼(`src/lib/url.ts`) 반드시 사용, 수동 경로 작성 금지

**핵심 규칙**:
- `src/content/book/` → `src/content/works/` 리네이밍 (이번 작업에서 수행)
- `public/books/` = 완결 HTML 저장소 (빌드 결과물 아님, 직접 배치)
- 모든 CSS 클래스는 `.ol-` 접두어 유지

---

## TASK A. 사전 준비 — Collection 리네이밍

**이유**: `book`이라는 이름이 출판 완결물(public/books/)과 혼동됨.
원고(제작중)는 `works`, 완결물은 `book`으로 의미를 명확히 분리.

### A-1. 폴더 이동

```bash
mv src/content/book src/content/works
```

### A-2. config.ts 업데이트

`src/content/config.ts`에서 collection 이름 변경:

```typescript
// 변경 전
const bookCollection = defineCollection({ ... });
export const collections = {
  book: bookCollection,
  ...
};

// 변경 후
const worksCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    series: z.string().optional(),
    chapter: z.number().optional(),
    order: z.number().default(0),
    date: z.coerce.date().optional(),
    status: z.enum(['draft', 'revising', 'ready', 'published']).default('draft'),
    entities: z.array(z.string()).default([]),
    relations: z.array(RelationSchema).default([]),
    primary_entity: z.string().optional(),
    sources: z.array(z.object({
      text: z.string(),
      ref: z.string().optional(),
      passage: z.string().optional(),
    })).default([]),
    tags: z.array(z.string()).default([]),
    published: z.boolean().default(false),
    excerpt: z.string().optional(),
  }),
});

export const collections = {
  works: worksCollection,   // book → works
  blog: blogCollection,
  design: designCollection,
  ai: aiCollection,
  entities: entitiesCollection,
  ontology: ontologyCollection,
};
```

### A-3. 기존 참조 업데이트

`getCollection('book')` → `getCollection('works')` 전체 치환:

```bash
grep -rn "getCollection('book')" src/
# 찾은 파일들에서 일괄 치환
```

대상 파일:
- `src/lib/relations.ts`
- `src/lib/search.ts`
- `src/pages/book/index.astro` (있으면)
- `src/pages/book/[slug].astro` (있으면)

### A-4. public/books/ 구조 생성

완결 BOOK HTML을 저장하는 정적 자산 폴더:

```bash
mkdir -p public/books/placeholder
mkdir -p public/downloads/books
```

`public/books/placeholder/index.html` — 테스트용 더미 파일:

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>OL BOOK — 준비 중</title>
  <style>
    body { font-family: sans-serif; max-width: 600px; margin: 80px auto; padding: 0 24px; color: #0a0a0a; }
    h1 { font-size: 28px; margin-bottom: 16px; }
    p { color: #737373; line-height: 1.7; }
  </style>
</head>
<body>
  <h1>OL BOOK</h1>
  <p>이 페이지는 완결된 OL BOOK이 배치될 자리입니다.</p>
  <p><a href="../">← 목록으로</a></p>
</body>
</html>
```

---

## TASK B. WORKS 레이아웃 구축

### B-1. WorksLayout.astro 생성

`src/layouts/WorksLayout.astro`

Basecoat sidebar 구조를 OL 스타일로 오버라이드하는 3단 레이아웃.
왼쪽 사이드바(문서 트리) + 메인 콘텐츠 + (선택) 오른쪽 아웃라인.

```astro
---
import BaseLayout from './BaseLayout.astro';
import { url } from '../lib/url';
import { getCollection } from 'astro:content';

interface Props {
  title?: string;
  description?: string;
  currentSlug?: string;
}

const {
  title = 'OL WORKS',
  description = '진행 중인 불교 콘텐츠 원고',
  currentSlug,
} = Astro.props;

// works collection에서 published된 것 + 시리즈별 그룹화
const allWorks = await getCollection('works', e => e.data.published !== false);

// 시리즈별 그룹화
const groups = allWorks.reduce((acc, entry) => {
  const series = entry.data.series ?? '_standalone';
  if (!acc[series]) acc[series] = [];
  acc[series].push(entry);
  return acc;
}, {} as Record<string, typeof allWorks>);

// 각 그룹 내 order 정렬
for (const key of Object.keys(groups)) {
  groups[key].sort((a, b) => (a.data.order ?? 0) - (b.data.order ?? 0));
}

// 시리즈 이름 포맷 헬퍼 (buddha-story → Buddha Story)
function formatSeries(key: string): string {
  if (key === '_standalone') return '독립 문서';
  return key.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

// 상태 레이블
const statusLabel: Record<string, string> = {
  draft:     '초고',
  revising:  '수정중',
  ready:     '완료',
  published: '출판됨',
};
---

<BaseLayout title={title} description={description}>
  <!--
    Basecoat sidebar 구조 기반.
    OL 스타일로 전면 오버라이드.
    ref: https://basecoatui.com/components/sidebar/
  -->

  <!-- Sidebar toggle (모바일용) -->
  <button
    class="ol-sidebar-toggle"
    aria-label="사이드바 열기/닫기"
    onclick="document.dispatchEvent(new CustomEvent('basecoat:sidebar', { detail: { id: 'works-sidebar' } }))"
  >
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="3" y1="6" x2="21" y2="6"/>
      <line x1="3" y1="12" x2="21" y2="12"/>
      <line x1="3" y1="18" x2="21" y2="18"/>
    </svg>
    <span>목차</span>
  </button>

  <div class="ol-works-layout">

    <!-- 왼쪽 사이드바: 문서 트리 -->
    <aside
      class="sidebar ol-works-sidebar"
      id="works-sidebar"
      data-side="left"
      aria-hidden="false"
    >
      <nav aria-label="WORKS 문서 목차">

        <!-- 헤더 -->
        <div class="ol-works-sidebar-header">
          <a href={url('/works')} class="ol-works-sidebar-title">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
            WORKS
          </a>
          <span class="ol-works-sidebar-count">{allWorks.length} 문서</span>
        </div>

        <section class="scrollbar ol-works-sidebar-scroll">
          {Object.entries(groups).map(([series, entries]) => (
            <div role="group" aria-labelledby={`group-${series}`}>

              <!-- 시리즈 그룹 헤더 -->
              <h3 id={`group-${series}`} class="ol-works-group-label">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                </svg>
                {formatSeries(series)}
              </h3>

              <ul>
                {entries.map(entry => {
                  const isActive = currentSlug === entry.slug;
                  const statusKey = entry.data.status ?? 'draft';
                  return (
                    <li>
                      <a
                        href={url(`/works/${entry.slug}`)}
                        class:list={['ol-works-nav-link', { 'active': isActive }]}
                        aria-current={isActive ? 'page' : undefined}
                      >
                        <!-- 문서 아이콘 -->
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                          <polyline points="14 2 14 8 20 8"/>
                        </svg>
                        <span class="ol-works-nav-title">{entry.data.title}</span>
                        <!-- 상태 뱃지 (draft/revising만 표시) -->
                        {statusKey !== 'published' && (
                          <span class={`ol-works-status ol-works-status--${statusKey}`}>
                            {statusLabel[statusKey]}
                          </span>
                        )}
                      </a>
                    </li>
                  );
                })}
              </ul>

            </div>
          ))}
        </section>
      </nav>
    </aside>

    <!-- 메인 콘텐츠 영역 -->
    <main class="ol-works-main">
      <slot />
    </main>

  </div>

  <!-- Basecoat sidebar JS (CDN, 로컬 대체 가능) -->
  <script
    src="https://cdn.jsdelivr.net/npm/basecoat-css@0.3.11/dist/js/sidebar.min.js"
    defer
    is:inline
  ></script>
</BaseLayout>
```

### B-2. WorksLayout 전용 CSS

`src/styles/ol-components.css` 하단에 추가:

```css
/* ============================================================
   OL WORKS Layout — 3단 문서 레이아웃
   Basecoat sidebar 구조 기반, OL 스타일 오버라이드
   ============================================================ */

/* 레이아웃 컨테이너 */
.ol-works-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: calc(100vh - 64px); /* 헤더 높이 제외 */
  max-width: 1200px;
  margin: 0 auto;
}

/* ── 사이드바 ── */

/* Basecoat .sidebar 오버라이드 */
.ol-works-sidebar.sidebar {
  position: sticky;
  top: 64px;         /* 헤더 높이 */
  height: calc(100vh - 64px);
  width: 240px;
  background: var(--ol-surface-3, #fafafa);
  border-right: 1px solid var(--ol-border, #e9e9e9);
  overflow: hidden;
  flex-shrink: 0;
  /* Basecoat sidebar의 기본 transform/animation 재설정 */
  transform: none !important;
}

.ol-works-sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 16px 12px;
  border-bottom: 1px solid var(--ol-border, #e9e9e9);
}

.ol-works-sidebar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--ol-font-mono);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--ol-ink, #0a0a0a);
  text-decoration: none;
}
.ol-works-sidebar-title:hover { color: var(--ol-ink, #0a0a0a); }

.ol-works-sidebar-count {
  font-family: var(--ol-font-mono);
  font-size: 10px;
  color: var(--ol-muted, #737373);
}

.ol-works-sidebar-scroll {
  padding: 8px 0 24px;
  overflow-y: auto;
  height: calc(100% - 57px); /* 헤더 제외 */
}

/* 그룹 레이블 */
.ol-works-group-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--ol-font-mono);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--ol-muted, #737373);
  padding: 12px 16px 6px;
  margin: 0;
}

/* 문서 링크 */
.ol-works-sidebar-scroll ul {
  list-style: none;
  margin: 0;
  padding: 0;
}

.ol-works-nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  font-size: 13px;
  color: var(--ol-ink-2, #2a2a2a);
  text-decoration: none;
  border-radius: 0;
  transition: background 120ms ease, color 120ms ease;
  line-height: 1.4;
}
.ol-works-nav-link:hover {
  background: var(--ol-surface-2, #f5f5f5);
  color: var(--ol-ink, #0a0a0a);
}
.ol-works-nav-link.active {
  background: var(--ol-surface-2, #f5f5f5);
  color: var(--ol-ink, #0a0a0a);
  font-weight: 600;
  /* 왼쪽 강조 선 */
  box-shadow: inset 2px 0 0 var(--ol-ink, #0a0a0a);
}

.ol-works-nav-link svg {
  flex-shrink: 0;
  color: var(--ol-subtle, #a3a3a3);
}
.ol-works-nav-link.active svg { color: var(--ol-ink, #0a0a0a); }

.ol-works-nav-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 상태 뱃지 */
.ol-works-status {
  flex-shrink: 0;
  font-family: var(--ol-font-mono);
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  padding: 2px 5px;
  border-radius: 4px;
}
.ol-works-status--draft    { background: #f5f5f5; color: #a3a3a3; }
.ol-works-status--revising { background: #fafafa; color: #737373; border: 1px solid #e9e9e9; }
.ol-works-status--ready    { background: #0a0a0a; color: #ffffff; }

/* ── 메인 콘텐츠 ── */
.ol-works-main {
  min-height: 100%;
  padding: 48px 56px;
  background: var(--ol-bg, #ffffff);
}

/* WORKS 인덱스 페이지 */
.ol-works-index-header {
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--ol-border, #e9e9e9);
}

/* WORKS 문서 본문 */
.ol-works-article {
  max-width: 68ch; /* 읽기 최적 너비 */
}

.ol-works-article-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--ol-border, #e9e9e9);
}

.ol-works-article-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 12px;
  flex-wrap: wrap;
}

/* ── 모바일 사이드바 토글 ── */
.ol-sidebar-toggle {
  display: none;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  background: var(--ol-surface-2, #f5f5f5);
  border: none;
  border-bottom: 1px solid var(--ol-border, #e9e9e9);
  width: 100%;
  font-size: 13px;
  font-weight: 500;
  color: var(--ol-ink, #0a0a0a);
  cursor: pointer;
  font-family: inherit;
}

/* ── 다크모드 ── */
.dark .ol-works-sidebar.sidebar {
  background: var(--ol-surface-3, #141414);
  border-color: var(--ol-border, #272727);
}
.dark .ol-works-nav-link:hover { background: var(--ol-surface-2, #1a1a1a); }
.dark .ol-works-nav-link.active { background: var(--ol-surface-2, #1a1a1a); }
.dark .ol-works-status--draft { background: #1a1a1a; color: #525252; }
.dark .ol-works-status--ready { background: #fafafa; color: #0a0a0a; }

/* ── 반응형 ── */
@media (max-width: 900px) {
  .ol-works-layout {
    grid-template-columns: 1fr;
  }
  .ol-sidebar-toggle {
    display: flex;
  }
  /* 모바일: Basecoat sidebar의 기본 슬라이드 동작 허용 */
  .ol-works-sidebar.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    z-index: 200;
    width: 280px;
    transform: translateX(-100%) !important;
    transition: transform 200ms ease;
  }
  .ol-works-sidebar.sidebar[aria-hidden="false"] {
    transform: translateX(0) !important;
  }
  .ol-works-main {
    padding: 32px 24px;
  }
}

@media (max-width: 600px) {
  .ol-works-main {
    padding: 24px 16px;
  }
}
```

---

## TASK C. WORKS 페이지 구현

### C-1. WORKS 인덱스 페이지

`src/pages/works/index.astro`

```astro
---
import { getCollection } from 'astro:content';
import WorksLayout from '../../layouts/WorksLayout.astro';
import { url } from '../../lib/url';

const allWorks = await getCollection('works', e => e.data.published !== false);

// 시리즈별 그룹화 + 정렬
const groups = allWorks.reduce((acc, entry) => {
  const series = entry.data.series ?? '_standalone';
  if (!acc[series]) acc[series] = [];
  acc[series].push(entry);
  return acc;
}, {} as Record<string, typeof allWorks>);

for (const key of Object.keys(groups)) {
  groups[key].sort((a, b) => (a.data.order ?? 0) - (b.data.order ?? 0));
}

function formatSeries(key: string): string {
  if (key === '_standalone') return '독립 문서';
  return key.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

const statusLabel: Record<string, string> = {
  draft:     '초고',
  revising:  '수정중',
  ready:     '완료',
  published: '출판됨',
};
---

<WorksLayout title="OL WORKS — 제작 중인 콘텐츠">
  <div class="ol-works-index-header">
    <span class="ol-kicker">WORKS · 제작 중인 지혜</span>
    <h1 style="font-size: 32px; margin-top: 10px;" class="ol-kr">
      작업 중인 원고들
    </h1>
    <p style="color: var(--ol-muted); margin-top: 12px; max-width: 52ch; line-height: 1.7;" class="ol-kr">
      완결 이전의 초고, 번역 초안, 주석 연구를 공개합니다.
      모든 원고는 수정 중일 수 있으며, 완결 시 OL BOOK으로 이동됩니다.
    </p>
  </div>

  <!-- 시리즈별 목록 -->
  {Object.entries(groups).map(([series, entries]) => (
    <section style="margin-bottom: 48px;">
      <h2 class="ol-kicker" style="margin-bottom: 16px;">
        {formatSeries(series)} · {entries.length}편
      </h2>

      <div style="display: flex; flex-direction: column; gap: 1px; border: 1px solid var(--ol-border); border-radius: var(--ol-r-lg); overflow: hidden;">
        {entries.map((entry, i) => (
          <a
            href={url(`/works/${entry.slug}`)}
            style={`
              display: flex;
              align-items: center;
              justify-content: space-between;
              padding: 16px 20px;
              background: var(--ol-surface);
              text-decoration: none;
              color: inherit;
              transition: background 120ms ease;
              ${i > 0 ? 'border-top: 1px solid var(--ol-border);' : ''}
            `}
            onmouseover="this.style.background='var(--ol-surface-2)'"
            onmouseout="this.style.background='var(--ol-surface)'"
          >
            <div style="display: flex; align-items: center; gap: 14px;">
              <span class="ol-mono-label" style="min-width: 28px; text-align: right;">
                {String(entry.data.chapter ?? (i + 1)).padStart(2, '0')}
              </span>
              <div>
                <div style="font-size: 15px; font-weight: 600; color: var(--ol-ink);" class="ol-kr">
                  {entry.data.title}
                </div>
                {entry.data.excerpt && (
                  <div style="font-size: 13px; color: var(--ol-muted); margin-top: 3px;" class="ol-kr">
                    {entry.data.excerpt}
                  </div>
                )}
              </div>
            </div>

            <div style="display: flex; align-items: center; gap: 10px; flex-shrink: 0;">
              <span class={`ol-works-status ol-works-status--${entry.data.status ?? 'draft'}`}>
                {statusLabel[entry.data.status ?? 'draft']}
              </span>
              <span style="color: var(--ol-subtle);">→</span>
            </div>
          </a>
        ))}
      </div>
    </section>
  ))}

  <!-- 비어있을 때 -->
  {allWorks.length === 0 && (
    <div style="text-align: center; padding: 80px 0; color: var(--ol-muted);">
      <p class="ol-kr">아직 공개된 원고가 없습니다.</p>
    </div>
  )}
</WorksLayout>
```

### C-2. WORKS 개별 문서 페이지

`src/pages/works/[...slug].astro`

```astro
---
import { getCollection, getEntry } from 'astro:content';
import WorksLayout from '../../layouts/WorksLayout.astro';
import { url } from '../../lib/url';

export async function getStaticPaths() {
  const works = await getCollection('works', e => e.data.published !== false);
  return works.map(entry => ({
    params: { slug: entry.slug },
    props: { entry },
  }));
}

const { entry } = Astro.props;
const { Content } = await entry.render();

const statusLabel: Record<string, string> = {
  draft:     '초고',
  revising:  '수정중',
  ready:     '완료',
  published: '출판됨',
};

const statusKey = entry.data.status ?? 'draft';
---

<WorksLayout
  title={`${entry.data.title} — OL WORKS`}
  currentSlug={entry.slug}
>
  <article class="ol-works-article">

    <!-- 문서 헤더 -->
    <header class="ol-works-article-header">
      {entry.data.series && (
        <span class="ol-kicker">{entry.data.series.replace(/-/g, ' ').toUpperCase()}</span>
      )}
      <h1
        style="font-size: 30px; margin-top: 10px; line-height: 1.3;"
        class="ol-kr"
      >
        {entry.data.title}
      </h1>

      <div class="ol-works-article-meta">
        <span class={`ol-works-status ol-works-status--${statusKey}`}>
          {statusLabel[statusKey]}
        </span>
        {entry.data.date && (
          <span class="ol-mono-label">
            {new Date(entry.data.date).toLocaleDateString('ko-KR', {
              year: 'numeric', month: 'long', day: 'numeric'
            })}
          </span>
        )}
        {entry.data.tags.map(tag => (
          <span class="ol-badge">{tag}</span>
        ))}
      </div>

      {entry.data.excerpt && (
        <p style="color: var(--ol-muted); margin-top: 16px; line-height: 1.7;" class="ol-kr">
          {entry.data.excerpt}
        </p>
      )}
    </header>

    <!-- 본문 -->
    <div class="ol-prose ol-kr">
      <Content />
    </div>

    <!-- 출처 -->
    {entry.data.sources.length > 0 && (
      <footer style="margin-top: 48px; padding-top: 24px; border-top: 1px solid var(--ol-border);">
        <h3 class="ol-kicker" style="margin-bottom: 12px;">참고 문헌</h3>
        <ul style="list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 6px;">
          {entry.data.sources.map(src => (
            <li style="font-size: 13.5px; color: var(--ol-muted);">
              <span class="ol-kr">{src.text}</span>
              {src.passage && <span style="margin-left: 8px; font-family: var(--ol-font-mono); font-size: 11px;">{src.passage}</span>}
            </li>
          ))}
        </ul>
      </footer>
    )}

  </article>
</WorksLayout>
```

---

## TASK D. 네비게이션에 WORKS 추가

### D-1. OLHeader.astro 수정

`src/components/layout/OLHeader.astro`의 `navItems` 배열에 WORKS 추가:

```astro
---
const navItems = [
  { href: url('/'),       label: 'HOME'   },
  { href: url('/atlas'),  label: 'ATLAS'  },
  { href: url('/book'),   label: 'BOOK'   },
  { href: url('/works'),  label: 'WORKS'  },  // ← 추가
  { href: url('/design'), label: 'DESIGN' },
  { href: url('/ai'),     label: 'AI'     },
];
---
```

**모바일 고려**: 메뉴가 6개로 늘어나므로 좁은 화면에서 줄바꿈 또는 글자 크기 축소 확인 필요.

---

## TASK E. BLOG 자동반영 구현

### E-1. 현재 상태 확인

`src/pages/blog/index.astro` 파일을 열어 아래 패턴이 있는지 확인:

```astro
const posts = await getCollection('blog', e => e.data.published === true);
```

이 코드가 **있으면** 이미 자동반영 중. `published: true`인 `.md` 파일을 추가하면 자동으로 반영됩니다.

**없으면** 아래 E-2를 적용합니다.

### E-2. blog/index.astro 전면 업데이트

`src/pages/blog/index.astro` 전체를 아래로 교체:

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import { url } from '../../lib/url';

// published: true 인 것만, 날짜 최신순 정렬
const posts = (
  await getCollection('blog', e => e.data.published === true)
).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

const categoryLabel: Record<string, string> = {
  ATLAS:  'ATLAS',
  BOOK:   'BOOK',
  DESIGN: 'DESIGN',
  AI:     'AI',
  META:   'META',
};
---

<BaseLayout
  title="OL BLOG — 개발 기록"
  description="OL 콘텐츠를 만들고 고쳐가는 과정의 기록"
>
  <main>
    <section class="ol-section">
      <div class="ol-container">

        <!-- 헤더 -->
        <div style="margin-bottom: 48px;">
          <span class="ol-kicker">BLOG · 개발 기록</span>
          <h1 style="font-size: 32px; margin-top: 10px;" class="ol-kr">
            결정과 회고, 작은 발견들
          </h1>
          <p style="color: var(--ol-muted); margin-top: 12px;" class="ol-kr">
            {posts.length}개의 기록
          </p>
        </div>

        <!-- 포스트 목록 -->
        {posts.length > 0 ? (
          <div style="display: flex; flex-direction: column; border: 1px solid var(--ol-border); border-radius: var(--ol-r-lg); overflow: hidden;">
            {posts.map((post, i) => (
              <a
                href={url(`/blog/${post.slug}`)}
                style={`
                  display: flex;
                  align-items: flex-start;
                  justify-content: space-between;
                  gap: 24px;
                  padding: 20px 24px;
                  background: var(--ol-surface);
                  text-decoration: none;
                  color: inherit;
                  transition: background 120ms ease;
                  ${i > 0 ? 'border-top: 1px solid var(--ol-border);' : ''}
                `}
                onmouseover="this.style.background='var(--ol-surface-2)'"
                onmouseout="this.style.background='var(--ol-surface)'"
              >
                <div style="flex: 1; min-width: 0;">
                  <!-- 카테고리 + 날짜 -->
                  <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                    {post.data.category && (
                      <span class="ol-mono-label">
                        {categoryLabel[post.data.category] ?? post.data.category}
                      </span>
                    )}
                    <span class="ol-mono-label">
                      {new Date(post.data.date).toLocaleDateString('ko-KR', {
                        year: 'numeric', month: '2-digit', day: '2-digit'
                      })}
                    </span>
                  </div>

                  <!-- 제목 -->
                  <h2
                    style="font-size: 17px; font-weight: 600; letter-spacing: -0.015em; line-height: 1.4; margin: 0;"
                    class="ol-kr"
                  >
                    {post.data.title}
                  </h2>

                  <!-- 발췌 -->
                  {post.data.excerpt && (
                    <p
                      style="font-size: 13.5px; color: var(--ol-muted); margin-top: 6px; line-height: 1.6;"
                      class="ol-kr"
                    >
                      {post.data.excerpt}
                    </p>
                  )}

                  <!-- 태그 -->
                  {post.data.tags.length > 0 && (
                    <div style="display: flex; gap: 6px; margin-top: 10px; flex-wrap: wrap;">
                      {post.data.tags.map(tag => (
                        <span class="ol-badge">{tag}</span>
                      ))}
                    </div>
                  )}
                </div>

                <!-- 화살표 -->
                <span style="color: var(--ol-subtle); flex-shrink: 0; margin-top: 2px;">→</span>
              </a>
            ))}
          </div>
        ) : (
          <!-- 비어있을 때 -->
          <div style="text-align: center; padding: 80px 0; color: var(--ol-muted);">
            <p class="ol-kr">아직 공개된 포스트가 없습니다.</p>
          </div>
        )}

      </div>
    </section>
  </main>
</BaseLayout>
```

### E-3. 자동반영 원리 확인

새 md 파일을 추가하고 `npm run dev`에서 바로 반영되는지 검증:

```
src/content/blog/test-post.md
```

```markdown
---
title: "테스트 포스트"
date: 2026-05-29
category: META
excerpt: "자동반영 테스트"
tags: ["테스트"]
published: true
---

내용.
```

저장 후 `http://localhost:4321/ol-home/blog` 에서 포스트가 나타나면 성공.

---

## TASK F. HOME 최신 업데이트 섹션 자동반영

`src/components/home/OLLatestUpdates.astro` — 하드코딩된 3개 카드를 blog collection에서 자동으로 가져오도록 수정:

```astro
---
import { getCollection } from 'astro:content';
import { url } from '../../lib/url';

// 최신 3개 포스트
const latestPosts = (
  await getCollection('blog', e => e.data.published === true)
)
  .sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf())
  .slice(0, 3);

const categoryLabel: Record<string, string> = {
  ATLAS: 'ATLAS', BOOK: 'BOOK', DESIGN: 'DESIGN', AI: 'AI', META: 'META',
};
---

<section class="ol-section">
  <div class="ol-container">
    <div class="ol-row" style="margin-bottom: 24px;">
      <div>
        <span class="ol-kicker">LATEST · 최근 소식</span>
        <h2 style="font-size: 28px; margin-top: 8px;">진행 중인 작업</h2>
      </div>
      <div class="ol-spacer"></div>
      <a href={url('/blog')} class="ol-btn ol-btn-ghost ol-btn-sm">전체 보기 →</a>
    </div>

    <div class="ol-grid-3">
      {latestPosts.map(post => (
        <a href={url(`/blog/${post.slug}`)} class="ol-card ol-card-tight" style="text-decoration: none; color: inherit; display: block;">
          <span class="ol-mono-label">
            {new Date(post.data.date).toLocaleDateString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit' })}
            {post.data.category && ` · ${categoryLabel[post.data.category] ?? post.data.category}`}
          </span>
          <h4 style="font-size: 17px; margin-top: 8px; letter-spacing: -0.015em;" class="ol-kr">
            {post.data.title}
          </h4>
          {post.data.excerpt && (
            <p style="color: var(--ol-muted); font-size: 13.5px; margin-top: 8px; line-height: 1.6;" class="ol-kr">
              {post.data.excerpt}
            </p>
          )}
        </a>
      ))}

      {latestPosts.length === 0 && (
        <p class="ol-kr" style="color: var(--ol-muted); grid-column: 1/-1;">
          아직 공개된 포스트가 없습니다.
        </p>
      )}
    </div>
  </div>
</section>
```

---

## TASK G. 완료 조건 체크리스트

### 구조 체크
- [ ] `src/content/book/` → `src/content/works/` 이동 완료
- [ ] `config.ts`에서 `works` collection 정의 완료
- [ ] `getCollection('book')` → `getCollection('works')` 전체 치환 완료
- [ ] `public/books/placeholder/` 구조 생성 완료

### WORKS 체크
- [ ] `src/layouts/WorksLayout.astro` 생성
- [ ] `src/pages/works/index.astro` 생성
- [ ] `src/pages/works/[...slug].astro` 생성
- [ ] 헤더 navItems에 WORKS 추가
- [ ] `npm run dev`에서 `/works` 라우팅 정상
- [ ] 3단 레이아웃 (사이드바 + 메인) 렌더링 확인
- [ ] 사이드바의 폴더 그룹(시리즈) 구조 표시 확인
- [ ] 현재 문서 active 상태(왼쪽 선) 확인
- [ ] 상태 뱃지(초고/수정중/완료) 표시 확인
- [ ] 모바일 토글 동작 확인 (900px 이하)
- [ ] 다크모드 정상

### BLOG 체크
- [ ] `blog/index.astro` 업데이트 완료
- [ ] `OLLatestUpdates.astro` 동적 데이터 연결 완료
- [ ] 새 md 파일 추가 → 즉시 BLOG 목록 반영 확인
- [ ] HOME의 최신 업데이트 섹션에 자동 표시 확인
- [ ] `published: false` 인 파일은 표시 안 됨 확인

### 공통 체크
- [ ] `npm run build` 무오류
- [ ] GitHub Pages 배포 성공
- [ ] `url()` 헬퍼 사용 (수동 경로 없음)
- [ ] OL 디자인 시스템 일관성 유지

---

## 참고 — 새 WORKS 원고 작성 방법 (운영 가이드)

Phase 2 완료 후 원고를 추가할 때:

```markdown
<!-- src/content/works/buddha-story/01-birth.md -->
---
title: "룸비니의 탄생"
series: buddha-story
chapter: 1
order: 1
status: draft       ← draft | revising | ready | published
published: true     ← false면 사이트에 안 나옴
date: 2026-05-29
excerpt: "마야부인이 룸비니 동산에서 아기 싯다르타를 낳다."
tags: [붓다전기, 탄생]
entities:
  - siddhartha-gautama
  - maya-devi
  - lumbini
---

본문 내용...
```

파일 저장 → `npm run dev`에서 즉시 사이드바와 목록에 반영됩니다.

---

*OL HOME Phase 2 작업지시서 — 2026.05*
*WORKS 메뉴 신설 + BLOG 자동반영*