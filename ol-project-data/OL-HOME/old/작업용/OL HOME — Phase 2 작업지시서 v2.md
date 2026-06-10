# OL HOME — Phase 2 작업지시서 v2
## WORKS 메뉴 신설 + BOOK collection 신설 + BLOG 자동반영

> **기준 상태**: Phase 1 완료 (Astro 6.3.8, GitHub Pages 정상 배포)
> **v1 대비 변경**: Astro 6 API 전면 반영, book/works 분리 정책 확정

---

## 에이전트 필독 — Astro 6 필수 규칙

이 프로젝트는 **Astro 6** 기반입니다. Phase 1에서 이미 새 API로 마이그레이션되어 있습니다.
아래 5개 규칙을 코드 작성 전 숙지하고, 구버전 패턴을 절대 사용하지 마세요.

```
규칙 1. 설정 파일 위치
  src/content.config.ts  (프로젝트 루트, 점 표기)
  ← src/content/config.ts 가 아님

규칙 2. Collection 정의 방식
  defineCollection({ loader: glob({ pattern, base }), schema })
  ← defineCollection({ type: 'content', schema }) 가 아님
  glob import: import { glob } from 'astro/loaders';

규칙 3. Entry ID 접근
  entry.id  /  post.id
  ← entry.slug / post.slug 가 아님 (Astro 6에서 제거됨)

규칙 4. 콘텐츠 렌더링
  import { render } from 'astro:content';
  const { Content } = await render(entry);
  ← await entry.render() 가 아님

규칙 5. blog 스키마 필드명
  post.data.description  (발췌/소개)
  post.data.readingTime  (읽기 시간)
  ← post.data.excerpt 없음
```

---

## 설계 정책 — book / works 분리

이번 Phase에서 확정하는 4공간 구조입니다.

```
src/content/works/          제작 중인 원고 (챕터별 md)
                            → /works/ 페이지에서 열람

src/content/book/           완결 출판물 메타데이터 (경량 md)
  (신규)                    → /book/ 페이지 카드 렌더링에 사용

public/books/               브라우저 열기용 최신 완결 HTML
                            → /books/buddha-story/ 로 직접 접근

public/downloads/books/     버전별 다운로드용 HTML
                            → download 속성으로 파일 저장
```

**기존 `src/pages/book/`**: 이번 Phase에서 손대지 않음.
향후 `public/books/`의 완결 HTML을 가리키는 목록 페이지로 재용도 변경 예정.

**기존 `src/content/book/`**: Phase 1에서 만든 샘플 파일들이 있음.
이 폴더를 `src/content/works/`로 이동 후, `book`은 새 역할(완결 메타)로 신설.

---

## TASK A. 사전 준비 — 구조 재편

### A-1. 기존 book 폴더를 works로 이동

```bash
mv src/content/book src/content/works
```

이동 후 `src/content/works/` 안에 기존 파일들(`buddha-story/01-birth.md` 등)이 있어야 합니다.

### A-2. src/content.config.ts 업데이트

`src/content.config.ts` (루트 위치) 파일을 열어 아래를 수행합니다.

**① 기존 `book` collection 정의를 `works`로 교체**

기존 book collection 정의를 찾아 전체를 아래로 교체합니다.
(기존 RelationSchema, 다른 collection 정의는 그대로 유지)

```typescript
// works — 제작 중인 원고 (챕터별 단편 문서)
const worksCollection = defineCollection({
  loader: glob({
    pattern: '**/*.{md,mdx}',
    base: './src/content/works',
  }),
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
```

**② `book` collection을 새 역할로 신설**

완결 출판물의 메타데이터를 담는 경량 collection입니다.
기존 book 정의 자리에 아래를 추가합니다.

```typescript
// book — 완결된 출판물 메타데이터 (서지 정보)
const bookCollection = defineCollection({
  loader: glob({
    pattern: '**/*.{md,mdx}',
    base: './src/content/book',
  }),
  schema: z.object({
    title: z.string(),
    subtitle: z.string().optional(),
    version: z.string().default('v1.0'),
    publishedAt: z.coerce.date(),
    // public/books/ 하위 경로 (슬래시 없이)
    // 예: 'buddha-story' → /books/buddha-story/
    htmlPath: z.string(),
    // public/downloads/books/ 파일명 (확장자 포함)
    // 예: 'buddha-story-v1.0.html'
    downloadFile: z.string().optional(),
    // 대표 entity ID 목록 (세부 entity는 works에서 관리)
    primaryEntities: z.array(z.string()).default([]),
    description: z.string().optional(),
    tags: z.array(z.string()).default([]),
    lang: z.string().default('ko'),
    // 난이도: 1(입문) ~ 5(심화)
    level: z.number().min(1).max(5).optional(),
    published: z.boolean().default(true),
  }),
});
```

**③ collections export 업데이트**

```typescript
export const collections = {
  works: worksCollection,    // 기존 book → works
  book: bookCollection,      // 신규: 완결 출판물 메타
  blog: blogCollection,
  design: designCollection,
  ai: aiCollection,
  entities: entitiesCollection,
  ontology: ontologyCollection,
};
```

### A-3. 기존 참조 일괄 치환

`getCollection('book')` → `getCollection('works')`로 치환합니다.
아래 파일들을 열어 확인하고 수정합니다.

```bash
grep -rn "getCollection('book')" src/
```

**반드시 확인할 파일:**
- `src/lib/relations.ts`
- `src/lib/search.ts`
- `src/pages/book/index.astro`
- `src/pages/book/[...slug].astro`

각 파일에서 `getCollection('book')` → `getCollection('works')` 치환.
`entry.slug` → `entry.id` 도 함께 확인하여 수정.

### A-4. src/content/book/ 폴더 및 샘플 파일 생성

```bash
mkdir -p src/content/book
mkdir -p public/books/placeholder
mkdir -p public/downloads/books
```

**샘플 메타 파일** `src/content/book/placeholder.md`:

```markdown
---
title: "OL BOOK — 준비 중"
version: "v0.1"
publishedAt: 2026-05-29
htmlPath: "placeholder"
downloadFile: "placeholder-v0.1.html"
primaryEntities: []
description: "첫 번째 완결 BOOK이 곧 출판됩니다."
tags: []
published: false
---

첫 번째 완결 BOOK 준비 중입니다.
```

**브라우저 열기용 더미** `public/books/placeholder/index.html`:

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>OL BOOK — 준비 중</title>
  <style>
    body {
      font-family: -apple-system, sans-serif;
      max-width: 600px;
      margin: 80px auto;
      padding: 0 24px;
      color: #0a0a0a;
      line-height: 1.7;
    }
    h1 { font-size: 28px; font-weight: 700; margin-bottom: 16px; }
    p { color: #737373; }
    a { color: #0a0a0a; }
  </style>
</head>
<body>
  <h1>OL BOOK</h1>
  <p>이 페이지는 완결된 OL BOOK이 배치될 자리입니다.</p>
  <p><a href="javascript:history.back()">← 돌아가기</a></p>
</body>
</html>
```

**다운로드용 더미** `public/downloads/books/placeholder-v0.1.html`:
(위 index.html과 동일한 내용으로 생성)

---

## TASK B. WORKS 레이아웃 구축

### B-1. WorksLayout.astro 생성

`src/layouts/WorksLayout.astro`

Basecoat sidebar 구조를 OL 스타일로 오버라이드하는 2단 레이아웃.
왼쪽 사이드바(문서 트리) + 오른쪽 메인 콘텐츠.

```astro
---
import BaseLayout from './BaseLayout.astro';
import { url } from '../lib/url';
import { getCollection } from 'astro:content';

interface Props {
  title?: string;
  description?: string;
  currentId?: string;   // entry.id (Astro 6)
}

const {
  title = 'OL WORKS',
  description = '진행 중인 불교 콘텐츠 원고',
  currentId,
} = Astro.props;

// Astro 6: entry.id 사용
const allWorks = await getCollection('works', e => e.data.published !== false);

// 시리즈별 그룹화
const groups = allWorks.reduce((acc, entry) => {
  const series = entry.data.series ?? '_standalone';
  if (!acc[series]) acc[series] = [];
  acc[series].push(entry);
  return acc;
}, {} as Record<string, typeof allWorks>);

// 그룹 내 order 정렬
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

<BaseLayout title={title} description={description}>

  <!-- 모바일 사이드바 토글 -->
  <button
    class="ol-sidebar-toggle"
    aria-label="목차 열기/닫기"
    onclick="document.dispatchEvent(new CustomEvent('basecoat:sidebar', { detail: { id: 'works-sidebar' } }))"
  >
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="3" y1="6" x2="21" y2="6"/>
      <line x1="3" y1="12" x2="21" y2="12"/>
      <line x1="3" y1="18" x2="21" y2="18"/>
    </svg>
    <span>목차</span>
  </button>

  <div class="ol-works-layout">

    <!-- 왼쪽 사이드바 (Basecoat sidebar 구조 기반, OL 오버라이드) -->
    <aside
      class="sidebar ol-works-sidebar"
      id="works-sidebar"
      data-side="left"
      aria-hidden="false"
    >
      <nav aria-label="WORKS 문서 목차">

        <div class="ol-works-sidebar-header">
          <a href={url('/works')} class="ol-works-sidebar-title">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
            WORKS
          </a>
          <span class="ol-works-sidebar-count">{allWorks.length}</span>
        </div>

        <section class="scrollbar ol-works-sidebar-scroll">
          {Object.entries(groups).map(([series, entries]) => (
            <div role="group" aria-labelledby={`wg-${series}`}>

              <h3 id={`wg-${series}`} class="ol-works-group-label">
                <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                </svg>
                {formatSeries(series)}
              </h3>

              <ul>
                {entries.map(entry => {
                  // Astro 6: entry.id 사용
                  const isActive = currentId === entry.id;
                  const statusKey = entry.data.status ?? 'draft';
                  return (
                    <li>
                      <a
                        href={url(`/works/${entry.id}`)}
                        class:list={['ol-works-nav-link', { active: isActive }]}
                        aria-current={isActive ? 'page' : undefined}
                      >
                        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                          <polyline points="14 2 14 8 20 8"/>
                        </svg>
                        <span class="ol-works-nav-title">{entry.data.title}</span>
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

    <!-- 메인 콘텐츠 -->
    <main class="ol-works-main">
      <slot />
    </main>

  </div>

  <!-- Basecoat sidebar JS -->
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
   OL WORKS Layout
   Basecoat .sidebar 구조 기반 + OL 스타일 전면 오버라이드
   ============================================================ */

.ol-works-layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  min-height: calc(100vh - 64px);
}

/* ── 사이드바 (Basecoat .sidebar 오버라이드) ── */

.ol-works-sidebar.sidebar {
  position: sticky;
  top: 64px;
  height: calc(100vh - 64px);
  width: 240px;
  background: var(--ol-surface-3, #fafafa);
  border-right: 1px solid var(--ol-border, #e9e9e9);
  overflow: hidden;
  flex-shrink: 0;
  transform: none !important;  /* Basecoat 기본 transform 제거 */
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
  gap: 7px;
  font-family: var(--ol-font-mono);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--ol-ink, #0a0a0a);
  text-decoration: none;
}
.ol-works-sidebar-title:hover { opacity: 0.7; }

.ol-works-sidebar-count {
  font-family: var(--ol-font-mono);
  font-size: 10px;
  color: var(--ol-muted, #737373);
  background: var(--ol-surface-2, #f5f5f5);
  padding: 2px 6px;
  border-radius: 10px;
}

.ol-works-sidebar-scroll {
  padding: 6px 0 32px;
  overflow-y: auto;
  height: calc(100% - 53px);
}

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
  padding: 14px 16px 5px;
  margin: 0;
}

.ol-works-sidebar-scroll ul {
  list-style: none;
  margin: 0;
  padding: 0 0 4px;
}

.ol-works-nav-link {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 16px;
  font-size: 13px;
  color: var(--ol-ink-2, #2a2a2a);
  text-decoration: none;
  transition: background 100ms ease, color 100ms ease;
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
  box-shadow: inset 2px 0 0 var(--ol-ink, #0a0a0a);
}
.ol-works-nav-link svg { flex-shrink: 0; color: var(--ol-subtle, #a3a3a3); }
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
  letter-spacing: 0.05em;
  text-transform: uppercase;
  padding: 2px 5px;
  border-radius: 3px;
}
.ol-works-status--draft    { background: var(--ol-surface-2, #f5f5f5); color: var(--ol-subtle, #a3a3a3); }
.ol-works-status--revising { background: transparent; color: var(--ol-muted, #737373); border: 1px solid var(--ol-border, #e9e9e9); }
.ol-works-status--ready    { background: var(--ol-ink, #0a0a0a); color: #fff; }

/* ── 메인 콘텐츠 ── */
.ol-works-main {
  min-height: 100%;
  padding: 48px 56px;
  background: var(--ol-bg, #ffffff);
}

.ol-works-index-header {
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--ol-border, #e9e9e9);
}

.ol-works-article { max-width: 68ch; }

.ol-works-article-header {
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--ol-border, #e9e9e9);
}

.ol-works-article-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 12px;
  flex-wrap: wrap;
}

/* ── 모바일 토글 버튼 ── */
.ol-sidebar-toggle {
  display: none;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--ol-surface-2, #f5f5f5);
  border: none;
  border-bottom: 1px solid var(--ol-border, #e9e9e9);
  width: 100%;
  font-size: 13px;
  font-weight: 500;
  color: var(--ol-ink, #0a0a0a);
  cursor: pointer;
  font-family: inherit;
  text-align: left;
}

/* ── 다크모드 ── */
.dark .ol-works-sidebar.sidebar {
  background: var(--ol-surface-3, #141414);
  border-color: var(--ol-border, #272727);
}
.dark .ol-works-nav-link:hover  { background: var(--ol-surface-2, #1a1a1a); }
.dark .ol-works-nav-link.active { background: var(--ol-surface-2, #1a1a1a); }
.dark .ol-works-status--draft   { background: #1a1a1a; color: #525252; }
.dark .ol-works-status--ready   { background: #f5f5f5; color: #0a0a0a; }

/* ── 반응형 ── */
@media (max-width: 900px) {
  .ol-works-layout { grid-template-columns: 1fr; }
  .ol-sidebar-toggle { display: flex; }

  /* 모바일: Basecoat 슬라이드 동작 복원 */
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
  .ol-works-main { padding: 32px 24px; }
}

@media (max-width: 600px) {
  .ol-works-main { padding: 24px 16px; }
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

// Astro 6: entry.id
const allWorks = await getCollection('works', e => e.data.published !== false);

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

<WorksLayout title="OL WORKS — 제작 중인 원고들">
  <div class="ol-works-index-header">
    <span class="ol-kicker">WORKS · 생성 중인 지혜</span>
    <h1 style="font-size: 32px; margin-top: 10px;" class="ol-kr">
      작업 중인 원고들
    </h1>
    <p style="color: var(--ol-muted); margin-top: 12px; max-width: 52ch; line-height: 1.7;" class="ol-kr">
      완결 이전의 초고, 번역 초안, 주석 연구를 공개합니다.
      완결된 원고는 OL BOOK으로 출판됩니다.
    </p>
  </div>

  {Object.entries(groups).map(([series, entries]) => (
    <section style="margin-bottom: 48px;">
      <h2 class="ol-kicker" style="margin-bottom: 14px;">
        {formatSeries(series)} · {entries.length}편
      </h2>

      <div style="display: flex; flex-direction: column; border: 1px solid var(--ol-border); border-radius: var(--ol-r-lg); overflow: hidden;">
        {entries.map((entry, i) => (
          <a
            href={url(`/works/${entry.id}`)}
            style={[
              'display:flex;align-items:center;justify-content:space-between;',
              'padding:16px 20px;background:var(--ol-surface);text-decoration:none;',
              'color:inherit;transition:background 100ms ease;',
              i > 0 ? 'border-top:1px solid var(--ol-border);' : '',
            ].join('')}
            onmouseover="this.style.background='var(--ol-surface-2)'"
            onmouseout="this.style.background='var(--ol-surface)'"
          >
            <div style="display:flex;align-items:center;gap:14px;">
              <span class="ol-mono-label" style="min-width:24px;text-align:right;">
                {String(entry.data.chapter ?? (i + 1)).padStart(2, '0')}
              </span>
              <div>
                <div style="font-size:15px;font-weight:600;color:var(--ol-ink);" class="ol-kr">
                  {entry.data.title}
                </div>
                {entry.data.excerpt && (
                  <div style="font-size:13px;color:var(--ol-muted);margin-top:3px;line-height:1.5;" class="ol-kr">
                    {entry.data.excerpt}
                  </div>
                )}
              </div>
            </div>
            <div style="display:flex;align-items:center;gap:10px;flex-shrink:0;">
              <span class={`ol-works-status ol-works-status--${entry.data.status ?? 'draft'}`}>
                {statusLabel[entry.data.status ?? 'draft']}
              </span>
              <span style="color:var(--ol-subtle);">→</span>
            </div>
          </a>
        ))}
      </div>
    </section>
  ))}

  {allWorks.length === 0 && (
    <div style="text-align:center;padding:80px 0;color:var(--ol-muted);">
      <p class="ol-kr">아직 공개된 원고가 없습니다.</p>
    </div>
  )}
</WorksLayout>
```

### C-2. WORKS 개별 문서 페이지

`src/pages/works/[...slug].astro`

```astro
---
import { getCollection, render } from 'astro:content';  // Astro 6: render import
import WorksLayout from '../../layouts/WorksLayout.astro';
import { url } from '../../lib/url';

export async function getStaticPaths() {
  const works = await getCollection('works', e => e.data.published !== false);
  return works.map(entry => ({
    params: { slug: entry.id },   // Astro 6: entry.id
    props: { entry },
  }));
}

const { entry } = Astro.props;
const { Content } = await render(entry);  // Astro 6: render(entry)

const statusLabel: Record<string, string> = {
  draft: '초고', revising: '수정중', ready: '완료', published: '출판됨',
};
const statusKey = entry.data.status ?? 'draft';
---

<WorksLayout
  title={`${entry.data.title} — OL WORKS`}
  currentId={entry.id}
>
  <article class="ol-works-article">

    <header class="ol-works-article-header">
      {entry.data.series && (
        <span class="ol-kicker">
          {entry.data.series.replace(/-/g, ' ').toUpperCase()}
        </span>
      )}
      <h1 style="font-size: 30px; margin-top: 10px; line-height: 1.3;" class="ol-kr">
        {entry.data.title}
      </h1>

      <div class="ol-works-article-meta">
        <span class={`ol-works-status ol-works-status--${statusKey}`}>
          {statusLabel[statusKey]}
        </span>
        {entry.data.date && (
          <span class="ol-mono-label">
            {new Date(entry.data.date).toLocaleDateString('ko-KR', {
              year: 'numeric', month: 'long', day: 'numeric',
            })}
          </span>
        )}
        {entry.data.tags.map(tag => (
          <span class="ol-badge">{tag}</span>
        ))}
      </div>

      {entry.data.excerpt && (
        <p style="color:var(--ol-muted);margin-top:16px;line-height:1.7;" class="ol-kr">
          {entry.data.excerpt}
        </p>
      )}
    </header>

    <div class="ol-prose ol-kr">
      <Content />
    </div>

    {entry.data.sources.length > 0 && (
      <footer style="margin-top:48px;padding-top:24px;border-top:1px solid var(--ol-border);">
        <h3 class="ol-kicker" style="margin-bottom:12px;">참고 문헌</h3>
        <ul style="list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px;">
          {entry.data.sources.map(src => (
            <li style="font-size:13.5px;color:var(--ol-muted);">
              <span class="ol-kr">{src.text}</span>
              {src.passage && (
                <span style="margin-left:8px;font-family:var(--ol-font-mono);font-size:11px;">
                  {src.passage}
                </span>
              )}
            </li>
          ))}
        </ul>
      </footer>
    )}

  </article>
</WorksLayout>
```

---

## TASK D. BOOK 페이지 업데이트 (완결 출판물 목록)

기존 `src/pages/book/index.astro`를 `book` collection 기반으로 교체합니다.
"웹에서 읽기" + "다운로드" 버튼이 있는 카드 목록 페이지입니다.

`src/pages/book/index.astro` 전체 교체:

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import { url } from '../../lib/url';

// Astro 6: entry.id
const books = (
  await getCollection('book', e => e.data.published === true)
).sort((a, b) => b.data.publishedAt.valueOf() - a.data.publishedAt.valueOf());
---

<BaseLayout
  title="OL BOOK — 불교 콘텐츠 라이브러리"
  description="완결된 OL 불교 콘텐츠를 브라우저에서 읽거나 내려받을 수 있습니다."
>
  <main>
    <section class="ol-section">
      <div class="ol-container">

        <div style="margin-bottom: 48px;">
          <span class="ol-kicker">BOOK · 출판된 지혜</span>
          <h1 style="font-size: 32px; margin-top: 10px;" class="ol-kr">
            OL BOOK 라이브러리
          </h1>
          <p style="color:var(--ol-muted);margin-top:12px;max-width:52ch;line-height:1.7;" class="ol-kr">
            완결된 불교 콘텐츠를 브라우저에서 읽거나 단일 HTML 파일로 내려받을 수 있습니다.
            모든 파일은 설치 없이 브라우저 하나로 열립니다.
          </p>
        </div>

        {books.length > 0 ? (
          <div class="ol-grid-2">
            {books.map(book => (
              <div class="ol-card" style="display:flex;flex-direction:column;gap:20px;">

                <!-- 서지 정보 -->
                <div>
                  <span class="ol-mono-label" style="margin-bottom:8px;display:block;">
                    {new Date(book.data.publishedAt).getFullYear()} · {book.data.version}
                    {book.data.level && ` · 난이도 ${book.data.level}/5`}
                  </span>
                  <h2 style="font-size:22px;margin:0 0 8px;" class="ol-kr">
                    {book.data.title}
                  </h2>
                  {book.data.subtitle && (
                    <p style="font-size:14px;color:var(--ol-muted);margin:0 0 8px;" class="ol-kr">
                      {book.data.subtitle}
                    </p>
                  )}
                  {book.data.description && (
                    <p style="font-size:14px;color:var(--ol-muted);line-height:1.6;" class="ol-kr">
                      {book.data.description}
                    </p>
                  )}
                </div>

                <!-- 태그 -->
                {book.data.tags.length > 0 && (
                  <div style="display:flex;gap:6px;flex-wrap:wrap;">
                    {book.data.tags.map(tag => (
                      <span class="ol-badge">{tag}</span>
                    ))}
                  </div>
                )}

                <!-- 액션 버튼 -->
                <div style="display:flex;gap:10px;margin-top:auto;">
                  <!-- 웹에서 읽기: public/books/{htmlPath}/ -->
                  <a
                    href={url(`/books/${book.data.htmlPath}/`)}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="ol-btn ol-btn-primary ol-btn-sm"
                    style="flex:1;justify-content:center;"
                  >
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <line x1="2" y1="12" x2="22" y2="12"/>
                      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                    </svg>
                    웹에서 읽기
                  </a>

                  <!-- 다운로드: public/downloads/books/{downloadFile} -->
                  {book.data.downloadFile && (
                    <a
                      href={url(`/downloads/books/${book.data.downloadFile}`)}
                      download={book.data.downloadFile}
                      class="ol-btn ol-btn-outline ol-btn-sm"
                      style="flex:1;justify-content:center;"
                    >
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M12 3v13m0 0 4-4m-4 4-4-4M4 21h16"/>
                      </svg>
                      HTML 내려받기
                    </a>
                  )}
                </div>

              </div>
            ))}
          </div>
        ) : (
          <div style="text-align:center;padding:80px 0;color:var(--ol-muted);">
            <p class="ol-kr" style="font-size:15px;">준비 중입니다.</p>
            <p class="ol-kr" style="font-size:13px;margin-top:8px;">
              <a href={url('/works')} style="color:inherit;">WORKS</a>에서 제작 중인 원고를 먼저 만나보세요.
            </p>
          </div>
        )}

      </div>
    </section>
  </main>
</BaseLayout>
```

> **주의**: "웹에서 읽기" 버튼은 `public/books/{htmlPath}/index.html`을 새 탭으로 엽니다.
> "HTML 내려받기" 버튼은 `public/downloads/books/{downloadFile}`을 다운로드합니다.
> Safari에서 `download` 속성이 무시될 수 있으므로 실제 배포 후 반드시 테스트.

---

## TASK E. 네비게이션에 WORKS 추가

`src/components/layout/OLHeader.astro`의 `navItems`에 WORKS 추가:

```astro
const navItems = [
  { href: url('/'),       label: 'HOME'   },
  { href: url('/atlas'),  label: 'ATLAS'  },
  { href: url('/book'),   label: 'BOOK'   },
  { href: url('/works'),  label: 'WORKS'  },
  { href: url('/design'), label: 'DESIGN' },
  { href: url('/ai'),     label: 'AI'     },
];
```

메뉴가 6개로 늘어납니다. 모바일(375px)에서 줄바꿈 발생 여부 확인 후,
필요시 `ol-components.css`의 `.ol-nav a` 폰트 크기를 `12.5px`로 줄이거나
`gap`을 `2px`로 축소합니다.

---

## TASK F. BLOG 자동반영 구현

### F-1. 현재 상태 확인

`src/pages/blog/index.astro`를 열어 `getCollection('blog')` 호출이 있는지 확인합니다.
있으면 이미 자동반영 중이고, blog 스키마 필드명만 점검합니다.

```bash
grep -n "getCollection\|post\.data\." src/pages/blog/index.astro
```

**blog 스키마 실제 필드명 (Phase 1 보고서 기준):**
```
title, description, date, readingTime, category, published
```
`excerpt` 없음. `post.data.description` 사용.

### F-2. blog/index.astro 전면 업데이트

`src/pages/blog/index.astro` 전체를 아래로 교체:

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../layouts/BaseLayout.astro';
import { url } from '../../lib/url';

// Astro 6: post.id, post.data.description
const posts = (
  await getCollection('blog', e => e.data.published === true)
).sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());

const categoryLabel: Record<string, string> = {
  ATLAS: 'ATLAS', BOOK: 'BOOK', DESIGN: 'DESIGN', AI: 'AI', META: 'META',
};
---

<BaseLayout
  title="OL BLOG — 개발 기록"
  description="OL 콘텐츠를 만들고 고쳐가는 과정의 기록"
>
  <main>
    <section class="ol-section">
      <div class="ol-container">

        <div style="margin-bottom: 48px;">
          <span class="ol-kicker">BLOG · 개발 기록</span>
          <h1 style="font-size: 32px; margin-top: 10px;" class="ol-kr">
            결정과 회고, 작은 발견들
          </h1>
          <p style="color:var(--ol-muted);margin-top:8px;">{posts.length}개의 기록</p>
        </div>

        {posts.length > 0 ? (
          <div style="display:flex;flex-direction:column;border:1px solid var(--ol-border);border-radius:var(--ol-r-lg);overflow:hidden;">
            {posts.map((post, i) => (
              <a
                href={url(`/blog/${post.id}`)}
                style={[
                  'display:flex;align-items:flex-start;justify-content:space-between;gap:24px;',
                  'padding:20px 24px;background:var(--ol-surface);text-decoration:none;',
                  'color:inherit;transition:background 100ms ease;',
                  i > 0 ? 'border-top:1px solid var(--ol-border);' : '',
                ].join('')}
                onmouseover="this.style.background='var(--ol-surface-2)'"
                onmouseout="this.style.background='var(--ol-surface)'"
              >
                <div style="flex:1;min-width:0;">
                  <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
                    {post.data.category && (
                      <span class="ol-mono-label">
                        {categoryLabel[post.data.category] ?? post.data.category}
                      </span>
                    )}
                    <span class="ol-mono-label">
                      {new Date(post.data.date).toLocaleDateString('ko-KR', {
                        year: 'numeric', month: '2-digit', day: '2-digit',
                      })}
                    </span>
                    {post.data.readingTime && (
                      <span class="ol-mono-label">{post.data.readingTime}</span>
                    )}
                  </div>

                  <h2 style="font-size:17px;font-weight:600;letter-spacing:-0.015em;line-height:1.4;margin:0;" class="ol-kr">
                    {post.data.title}
                  </h2>

                  <!-- Astro 6 blog 스키마: description (excerpt 아님) -->
                  {post.data.description && (
                    <p style="font-size:13.5px;color:var(--ol-muted);margin-top:6px;line-height:1.6;" class="ol-kr">
                      {post.data.description}
                    </p>
                  )}
                </div>

                <span style="color:var(--ol-subtle);flex-shrink:0;margin-top:2px;">→</span>
              </a>
            ))}
          </div>
        ) : (
          <div style="text-align:center;padding:80px 0;color:var(--ol-muted);">
            <p class="ol-kr">아직 공개된 포스트가 없습니다.</p>
          </div>
        )}

      </div>
    </section>
  </main>
</BaseLayout>
```

### F-3. blog/[slug].astro의 slug → id 확인

`src/pages/blog/[slug].astro` (또는 `[...slug].astro`)를 열어
`entry.slug` → `entry.id`, `entry.render()` → `render(entry)` 수정 여부 확인.

---

## TASK G. HOME 최신 업데이트 자동반영

`src/components/home/OLLatestUpdates.astro`를 blog collection 기반으로 업데이트:

```astro
---
import { getCollection } from 'astro:content';
import { url } from '../../lib/url';

// Astro 6: post.id, post.data.description
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
        <a
          href={url(`/blog/${post.id}`)}
          class="ol-card ol-card-tight"
          style="text-decoration:none;color:inherit;display:block;"
        >
          <span class="ol-mono-label">
            {new Date(post.data.date).toLocaleDateString('ko-KR', {
              year: 'numeric', month: '2-digit', day: '2-digit',
            })}
            {post.data.category && ` · ${categoryLabel[post.data.category] ?? post.data.category}`}
          </span>
          <h4 style="font-size:17px;margin-top:8px;letter-spacing:-0.015em;" class="ol-kr">
            {post.data.title}
          </h4>
          {/* blog 스키마: description */}
          {post.data.description && (
            <p style="color:var(--ol-muted);font-size:13.5px;margin-top:8px;line-height:1.6;" class="ol-kr">
              {post.data.description}
            </p>
          )}
        </a>
      ))}

      {latestPosts.length === 0 && (
        <p class="ol-kr" style="color:var(--ol-muted);grid-column:1/-1;">
          아직 공개된 포스트가 없습니다.
        </p>
      )}
    </div>
  </div>
</section>
```

---

## TASK H. 완료 조건 체크리스트

### 구조
- [ ] `src/content/book/` → `src/content/works/` 이동 완료
- [ ] `src/content/book/` 폴더 신설, `placeholder.md` 작성
- [ ] `src/content.config.ts`에 `works` (glob 로더) + `book` (glob 로더) 정의
- [ ] `getCollection('book')` → `getCollection('works')` 전체 치환 완료
  - `src/lib/relations.ts`
  - `src/lib/search.ts`
  - `src/pages/book/[...slug].astro`
- [ ] `public/books/placeholder/index.html` 생성
- [ ] `public/downloads/books/placeholder-v0.1.html` 생성

### WORKS
- [ ] `src/layouts/WorksLayout.astro` 생성
- [ ] `src/pages/works/index.astro` 생성
- [ ] `src/pages/works/[...slug].astro` 생성
- [ ] 헤더 navItems에 WORKS 추가
- [ ] `/works` 라우팅 정상
- [ ] 사이드바 시리즈 그룹 표시 확인
- [ ] 현재 문서 active 상태(좌측 2px 선) 확인
- [ ] 상태 뱃지 표시 확인
- [ ] 모바일 토글 동작 확인 (900px 이하)
- [ ] 다크모드 정상

### BOOK
- [ ] `src/pages/book/index.astro` 교체 완료
- [ ] "웹에서 읽기" 버튼 → `public/books/placeholder/` 새 탭 열기 확인
- [ ] "HTML 내려받기" 버튼 → `public/downloads/books/` 파일 다운로드 확인
- [ ] Safari 다운로드 동작 별도 테스트

### BLOG
- [ ] `blog/index.astro` 업데이트 완료 (post.id, post.data.description)
- [ ] `OLLatestUpdates.astro` 동적 연결 완료
- [ ] 새 md 파일(published: true) 추가 → BLOG 목록 자동 반영 확인
- [ ] HOME 최신 업데이트 섹션 자동 표시 확인

### 공통
- [ ] `npm run build` 무오류
- [ ] `npm run preview`에서 전 페이지 링크 확인
- [ ] GitHub Pages 배포 성공
- [ ] 모든 링크에 `url()` 헬퍼 사용 (수동 `/ol-home/...` 없음)

---

## 운영 가이드 — 새 콘텐츠 추가 방법

### WORKS 원고 추가 (제작 중)
```markdown
<!-- src/content/works/buddha-story/02-four-sights.md -->
---
title: "사문유관"
series: buddha-story
chapter: 2
order: 2
status: draft
published: true
date: 2026-05-30
excerpt: "싯다르타 태자가 성 밖에서 늙음, 병, 죽음, 수행자를 만나다."
tags: [붓다전기, 출가]
entities: [siddhartha-gautama, kapilavastu]
---
본문...
```

### BOOK 출판 (완결 후)
```markdown
<!-- src/content/book/buddha-story.md -->
---
title: "붓다 이야기"
version: "v1.0"
publishedAt: 2026-06-01
htmlPath: "buddha-story"
downloadFile: "buddha-story-v1.0.html"
primaryEntities: [siddhartha-gautama, shakyamuni-buddha]
description: "싯다르타 고타마의 생애를 원전 기반으로 재구성했습니다."
tags: [붓다전기, 초기불교]
level: 1
published: true
---
```

그리고 `public/books/buddha-story/index.html`, `public/downloads/books/buddha-story-v1.0.html` 배치.

---

*OL HOME Phase 2 작업지시서 v2 — 2026.05*
*WORKS 신설 + BOOK collection 재편 + BLOG 자동반영*
*Astro 6 API 전면 반영*