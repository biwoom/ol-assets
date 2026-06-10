# OL 듀얼 런타임 설계서 v1.0

**버전**: v1.0 **작성일**: 2026-05-22 **선행 문서**: `OL_ATLAS_v0_7_최종_기획서_v2.md`, Phase 0~2 작업지시서 (모두 완료) **상태**: 설계 확정 — 구현 사이클 진입 가능

---

## 0. 한 줄 요약

> v0.7 Phase 0~2가 완료된 시점에서 OL은 **ATLAS(편집기) + BOOK(출판물)** 의 듀얼 런타임으로 분기한다. 두 런타임은 한 코드베이스에서 빌드되고, 한 dist 파일에 공존하며, **브라우저에서 `exportBook()` 한 번으로 BOOK이 생성**된다. ATLAS는 그대로 풍부한 편집 환경, BOOK은 몰입형 독서 환경.

---

## 1. 정체성 분리 — ATLAS vs BOOK

### 1.1 두 런타임의 성격

| 측면          | ATLAS (Author Runtime) | BOOK (Reader Runtime) |
| ----------- | ---------------------- | --------------------- |
| **정체성**     | 콘텐츠 제작 공방              | 출판물 / 책               |
| **사용자**     | 제작자 (비움)               | 독자                    |
| **모드**      | 편집 가능 + 모든 뷰           | 읽기 전용 + 몰입형           |
| **첫 화면**    | 카드보드 (홈랜딩 폐기)          | 커버페이지                 |
| **데이터 상태**  | dirty + autosave 작동    | readonly, 진행률만 저장     |
| **UI 인터랙션** | 햄버거 토글, 명시적            | 사라지는 UI, 몰입형          |
| **목적**      | "어떻게 편집할까"             | "어떻게 읽히게 할까"          |

### 1.2 메타포

```
ATLAS = 공방          (제작 도구가 풍부함)
BOOK  = 출판된 경전   (콘텐츠만 깨끗하게 전달)
```

ATLAS에서 만든 콘텐츠를 BOOK으로 export하면, 그 BOOK은 독립된 작품이 된다. 독자가 BOOK을 받아 ATLAS에서 열어볼 수도 있지만(편집 가능 상태가 됨), 일반 독자는 BOOK 그대로 사용한다.

---

## 2. 기능 분리표 — 무엇을 어디에

### 2.1 ATLAS / BOOK / SHARED 분류

|기능|ATLAS|BOOK|비고|
|---|---|---|---|
|카드보드|✅ 풀 기능|✅ readonly + 단순화|shared 모듈 + 분기|
|문서뷰|✅ 편집 가능|✅ readonly|shared 모듈 + 분기|
|사이드바|✅ 햄버거 토글|✅ 사라지는 UI|다른 인터랙션|
|About 페이지|✅|✅ 콘텐츠 통계 추가|분기|
|검색 (⌘K)|✅|✅|shared|
|다크모드|✅ light/dark|✅ light/dark/sepia|sepia는 BOOK 전용|
|리스트뷰|✅|❌|BOOK 제거|
|카드뷰 (그리드)|✅|❌|BOOK 제거|
|휴지통|✅|❌|BOOK 제거|
|카드 모달|✅|❌|BOOK은 즉시 문서뷰|
|카드/칼럼 추가 버튼|✅|❌|BOOK 제거|
|인라인 편집|✅|❌|BOOK 제거|
|저장/열기 버튼|✅|❌|BOOK은 readonly|
|설정뷰|✅|❌|BOOK은 최소 설정|
|커버페이지|❌|✅|BOOK 진입점|
|커버페이지 편집기|✅|❌|ATLAS에서 작성|
|진행률 추적|❌|✅|localStorage|
|책갈피|❌|✅|localStorage|
|본문 내부 링크 [[id]]|✅ 표시|✅ 표시|shared (마크다운 파서)|
|내부 링크 작성 보조|✅|❌|ATLAS의 에디터 기능|
|콘텐츠 통계|✅ 옵션|✅ About에 표시|shared|
|떠있는 mini-TOC|(보류)|(보류)|v1.x로 미룸|

### 2.2 ATLAS의 정체성

비움 결정대로 **ATLAS는 v0.7 기획서 v2 그대로 유지**한다. 듀얼 런타임 분기로 인해 ATLAS에 추가되는 것:

1. **커버페이지 편집기**: 사이드바에 "표지" 항목 추가 → 클릭 시 전용 편집 뷰
2. **본문 내부 링크 자동완성**: 마크다운 에디터에서 `[[` 입력 시 카드 자동완성 제안
3. **콘텐츠 통계 옵션**: ABOUT에서 통계 보기 (BOOK과 공유 가능한 계산 로직)
4. **BOOK 배포 버튼**: 사이드바 또는 설정뷰에 "BOOK으로 배포" 버튼

ATLAS에서 제거되는 것: **없음**. 비움이 명시한 결정 — "ATLAS에는 모든 기능 유지".

---

## 3. 아키텍처 — Dual Bundle 구조

### 3.1 빌드 산출물 구조

```
dist/ol-atlas.html
├── <head>
│   ├── meta, favicon
│   └── <style>  /* shared + author + reader CSS 통합 */
├── <body>
│   ├── <div id="app"></div>
│   ├── <script id="ol-shared-bundle">
│   │     /* 공통 코드: core, data, components, shared UI */
│   │   </script>
│   ├── <script id="ol-reader-bundle">
│   │     /* reader 전용 코드: cover, progress, bookmark, ... */
│   │   </script>
│   ├── <script id="ol-author-bundle">
│   │     /* author 전용 코드: tableview, trash, editors, ... */
│   │   </script>
│   └── <script id="ol-boot">
│         /* 부팅: shared + reader + author 모두 평가, author 활성 */
│       </script>
└── (옵션) <script>  /* __LOADED_DATA_B64__ 데이터 마커 */
```

### 3.2 부팅 시퀀스

```js
// ol-boot
window.__STATIC_HTML__ = document.documentElement.outerHTML;  // 캡처
OL.Shared.init();      // store, action, render-queue, schema migrate
OL.Reader.register();  // reader 모듈을 store에 subscribe
OL.Author.register();  // author 모듈을 store에 subscribe (ATLAS 모드일 때만)
OL.boot({ mode: detectMode() });  // 'atlas' or 'book'
```

### 3.3 모드 감지

부팅 시 자기 자신이 ATLAS인지 BOOK인지 판단해야 한다.

```js
function detectMode() {
  // BOOK은 export 시점에 다음 마커가 박힘
  if (window.__OL_MODE__ === 'book') return 'book';
  // author 번들이 살아있으면 ATLAS
  if (typeof window.OL.Author === 'object') return 'atlas';
  return 'book';  // 안전 폴백
}
```

`__OL_MODE__`는 `exportBook()`이 BOOK 산출물 생성 시 박는 마커. 단순한 방법이고 깔끔하다.

### 3.4 디렉토리 구조

```
src/
├── core/                       # 공통: 모든 런타임의 핵심
│   ├── store.js
│   ├── action.js
│   ├── render-queue.js
│   ├── dirty.js                # ATLAS에서만 활성
│   ├── schema.js
│   ├── storage.js
│   ├── origin.js
│   ├── id.js
│   └── dev.js
│
├── data/                       # 공통: 데이터 모델·변환
│   ├── card.js
│   ├── tag.js
│   ├── markdown.js             # [[id]] 파서 포함
│   └── search/
│
├── actions/                    # 공통: Action Layer (Phase 2 산출물)
│   ├── card-actions.js
│   ├── column-actions.js
│   ├── view-actions.js
│   └── settings-actions.js
│
├── ui/
│   ├── shared/                 # 양쪽에 유지되는 UI
│   │   ├── docview/            # 본문 렌더 (편집은 분기)
│   │   ├── cardboard/          # 카드보드 (편집 버튼은 분기)
│   │   ├── sidebar/            # 사이드바 셸 (콘텐츠는 분기)
│   │   ├── search/             # ⌘K command palette
│   │   ├── about/              # ABOUT 셸 (통계는 분기 가능)
│   │   └── theme/              # 라이트/다크 토글
│   │
│   ├── reader/                 # BOOK 전용
│   │   ├── cover-page/         # 커버페이지 표시
│   │   ├── progress/           # 진행률 추적
│   │   ├── bookmark/           # 책갈피
│   │   ├── reader-sidebar-items.js  # 사이드바 BOOK 항목
│   │   ├── reader-docview-extras.js # 진행률 표시, 다음/이전 네비
│   │   ├── reader-cardboard.js      # readonly 카드보드 + 인덱스 정렬
│   │   └── sepia-theme/        # sepia 모드 토큰
│   │
│   └── author/                 # ATLAS 전용
│       ├── tableview/
│       ├── cardview-grid/
│       ├── trash/
│       ├── card-modal-edit/
│       ├── inline-editors/
│       ├── settings-view/
│       ├── cover-editor/       # 커버페이지 편집기 (BOOK 위해 작성)
│       ├── internal-link-completer.js  # [[ 자동완성
│       └── export/
│           └── export-book.js  # exportBook() 함수
│
├── components/                 # 공통 UI 컴포넌트
│   ├── dialog.js
│   ├── popover.js
│   ├── badge.js
│   ├── toast.js
│   ├── icons.js
│   └── ...
│
├── i18n/
│   ├── t.js
│   └── ko.js
│
├── styles/
│   ├── tokens.css              # 공통 토큰
│   ├── base.css
│   ├── components.css
│   ├── shared.css              # 양쪽 공통 view 스타일
│   ├── atlas.css               # ATLAS 전용
│   ├── reader.css              # BOOK 전용
│   ├── reader-typography.css   # BOOK 독서 typography
│   └── sepia.css               # sepia 토큰
│
└── boot.js
```

### 3.5 빌드 설정 변경

```js
// build/build.mjs (변경 부분)
const sharedBundle = await esbuild.build({
  entryPoints: [join(SRC, 'shared-entry.js')],
  bundle: true,
  format: 'iife',
  globalName: 'OL.Shared',
  define: { __DEV__: 'false' },
  write: false,
});

const readerBundle = await esbuild.build({
  entryPoints: [join(SRC, 'reader-entry.js')],
  bundle: true,
  format: 'iife',
  globalName: 'OL.Reader',
  external: ['./core/*', './data/*', './actions/*'],  // shared로 빠짐
  define: { __DEV__: 'false' },
  write: false,
});

const authorBundle = await esbuild.build({
  entryPoints: [join(SRC, 'author-entry.js')],
  bundle: true,
  format: 'iife',
  globalName: 'OL.Author',
  external: ['./core/*', './data/*', './actions/*'],
  define: { __DEV__: 'false' },
  write: false,
});

// 세 번들을 한 HTML에 인라이닝
```

각 entry 파일은 단순히 해당 모듈들을 모아 export:

```js
// src/reader-entry.js
export * from './ui/reader/cover-page/index.js';
export * from './ui/reader/progress/index.js';
export * from './ui/reader/bookmark/index.js';
// ...
```

---

## 4. Reader Manifest 스펙

BOOK 콘텐츠의 메타 정보 + 독서 경험을 제어한다. ATLAS에서 제작자가 채우고, BOOK이 사용한다.

### 4.1 스키마

```js
// state.book.manifest (ATLAS에서 작성, BOOK에 inline됨)
{
  // === 정체성 ===
  id: 'buddha-story-v1',           // 고유 BOOK ID (진행률 키 네임스페이스)
  title: '붓다 스토리',
  subtitle: '팔리 경전으로 읽는 석가모니의 생애',
  author: '비움',                   // ORIGIN.author 자동 복제
  series: 'OL BOOK · 붓다 시리즈 1',
  version: '1.0',
  publishedAt: '2026-05-22',

  // === 표지 ===
  cover: {
    image: 'data:image/jpeg;base64,...',  // 표지 이미지 (base64 inline)
    backgroundColor: 'auto',               // 'auto' 또는 'hsl(...)'
  },

  // === 진입 정책 ===
  entry: {
    view: 'cover',                  // 'cover'만 (v1 고정)
    actions: ['start', 'toc'],      // 커버에 보일 액션 버튼
    startTarget: 'first-card',      // 'first-card' | 'cardboard'
  },

  // === 정렬 정책 ===
  ordering: {
    cards: 'array-index',           // v1 고정 (재고 2-2에 따라)
  },

  // === 표시 정책 ===
  display: {
    showColumns: true,              // 카드보드에 칼럼 표시 여부
    showTags: true,                 // 카드에 태그 표시 여부
    showProgress: true,             // 진행률 UI 표시
    showBookmarks: true,            // 책갈피 기능
  },

  // === 라이선스 ===
  license: 'CC BY-SA 4.0',          // ORIGIN.license 복제
  copyright: 'Copyright © 2026 biwoom',  // ORIGIN.copyright 복제
}
```

### 4.2 데이터 모델에 추가

기존 v0.7 schema v7에 추가:

```js
S.book = {                          // 신규 (schema v8로 마이그레이트)
  manifest: { /* 위 스키마 */ },
}
```

schema v7 → v8 마이그레이션:

```js
// src/core/schema.js
7: (s) => {
  s.meta.schemaVersion = 8;
  s.book = {
    manifest: {
      id: generateBookId(s),
      title: s.meta?.title || 'Untitled',
      subtitle: '',
      author: ORIGIN.author,
      series: '',
      version: '1.0',
      publishedAt: new Date().toISOString().slice(0, 10),
      cover: { image: null, backgroundColor: 'auto' },
      entry: { view: 'cover', actions: ['start', 'toc'], startTarget: 'first-card' },
      ordering: { cards: 'array-index' },
      display: { showColumns: true, showTags: true, showProgress: true, showBookmarks: true },
      license: ORIGIN.license,
      copyright: ORIGIN.copyright,
    },
  };
  return s;
},
```

---

## 5. Export Manifest 스펙

`exportBook()`이 BOOK 생성 시 어떤 데이터를 포함하고 어떤 것을 잘라낼지 정책.

### 5.1 export 포함 데이터

```js
const bookData = {
  meta: {
    schemaVersion: 8,
    olVersion: '0.8.0-book',         // BOOK은 v0.8부터 (분기 표시)
    exportedAt: ISO,
    sourceFingerprint: hash(S),      // 원본 ATLAS의 지문
  },
  cards: S.cards,                    // 활성 카드만 (trash 제외)
  cols: S.cols,
  book: {
    manifest: S.book.manifest,
  },
  settings: {                        // BOOK용 최소 설정
    theme: 'system',                 // 독자가 직접 선택
    locale: S.settings.locale,
  },
};
```

### 5.2 export 제외 데이터

명시적으로 BOOK에 들어가지 않는 것:

- `S.trash` — 삭제된 카드 (개인정보·미공개 콘텐츠 노출 방지)
- `S.meta.dirty`, `S.meta.lastSavedAt` — 편집 상태
- `S.settings.sidebarOpen`, `S.settings.boardWidth`, `S.settings.metaToggles`, `S.settings.activeTabId` — ATLAS UI 상태
- `S.ui` (Phase 2에서 통합된 view state) — 독자가 새로 시작
- localStorage의 `ol_backup_v6` 등 백업 데이터

### 5.3 BOOK 독자의 로컬 데이터

BOOK에서 독자가 만드는 로컬 데이터는 **독자의 localStorage**에만 저장. BOOK HTML 자체에는 박히지 않음.

```js
// BOOK 독자의 localStorage 키: ol_reader_<bookId>
{
  progress: {
    lastReadCardId: 'card-042',
    lastReadAt: ISO,
    readCards: ['card-001', ...],
    totalCards: 87,
  },
  bookmarks: [
    { cardId: 'card-042', addedAt: ISO },
  ],
  preferences: {
    theme: 'sepia',                  // 독자가 선택한 테마
  },
}
```

같은 BOOK을 다시 받아도 `bookId`가 같으면 진행률 보존.

---

## 6. exportBook() 함수 설계

### 6.1 흐름

```
[ATLAS 사이드바 또는 설정뷰의 "BOOK으로 배포" 버튼]
    ↓
[exportBook() 호출]
    ↓
1. Reader Manifest 유효성 검사
   - 필수 필드 (title, id 등) 확인
   - 경고가 있으면 confirm 다이얼로그
    ↓
2. 현재 HTML 가져오기
   - window.__STATIC_HTML__ 사용 (v0.6 패턴 계승)
    ↓
3. author 번들 제거
   - <script id="ol-author-bundle"> 통째로 제거
   - <script id="ol-author-styles"> 제거 (있다면)
    ↓
4. mode 마커 박기
   - <script>window.__OL_MODE__='book';</script> 추가
    ↓
5. 데이터 inline
   - bookData를 JSON → base64 → __LOADED_DATA_B64__ 마커에 박기
    ↓
6. BOOK 메타 정보 head에 박기
   - <title>, og:title, og:image 등 (manifest에서 추출)
    ↓
7. Blob 생성 + 다운로드
   - 파일명: <bookId>.html 또는 <title>.html
```

### 6.2 코드 구조

```js
// src/ui/author/export/export-book.js

import { getState } from '../../../core/store.js';
import { devLog } from '../../../core/dev.js';

export async function exportBook(opts = {}) {
  devLog('BOOT', 'exportBook start');

  // 1. 유효성
  const s = getState();
  const validation = validateManifest(s.book.manifest);
  if (!validation.ok) {
    const proceed = confirm(`BOOK으로 배포 가능하지만 다음 항목을 확인하세요:\n\n${validation.warnings.join('\n')}\n\n그래도 진행하시겠습니까?`);
    if (!proceed) return;
  }

  // 2. HTML 베이스 가져오기
  let html = window.__STATIC_HTML__;

  // 3. author 번들 제거
  html = removeBlock(html, /<script id="ol-author-bundle"[^>]*>[\s\S]*?<\/script>/);
  html = removeBlock(html, /<style id="ol-author-styles"[^>]*>[\s\S]*?<\/style>/);

  // 4. mode 마커
  html = injectBeforeBoot(html, `<script>window.__OL_MODE__='book';</script>`);

  // 5. 데이터 inline
  const bookData = buildBookData(s);
  const b64 = btoa(unescape(encodeURIComponent(JSON.stringify(bookData))));
  html = injectLoadedData(html, b64);

  // 6. 메타 정보 head 갱신
  html = updateHead(html, s.book.manifest);

  // 7. 다운로드
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${slugify(s.book.manifest.title)}.html`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  devLog('BOOT', 'exportBook done');
}

function buildBookData(s) {
  return {
    meta: {
      schemaVersion: 8,
      olVersion: '0.8.0-book',
      exportedAt: new Date().toISOString(),
    },
    cards: s.cards,
    cols: s.cols,
    book: { manifest: s.book.manifest },
    settings: { theme: 'system', locale: s.settings.locale },
  };
}

function validateManifest(m) {
  const warnings = [];
  if (!m.title) warnings.push('· 제목이 비어있습니다');
  if (!m.id) warnings.push('· BOOK ID가 비어있습니다');
  if (!m.cover.image) warnings.push('· 표지 이미지가 없습니다');
  return { ok: warnings.length === 0, warnings };
}

// removeBlock, injectBeforeBoot, injectLoadedData, updateHead, slugify
// 모두 단순 문자열 조작
```

### 6.3 메모리의 자기참조 정규식 트랩 회피

`__LOADED_DATA_B64__` 마커 처리는 메모리 기록된 패턴을 따른다:

```js
// 정규식이 자기 자신을 매치하지 않게 분리
const MARKER = '__LOADED' + '_DATA_B64__';
const pattern = new RegExp(MARKER, 'g');
html = html.replace(pattern, b64);
```

---

## 7. BOOK 신규 모듈 상세

### 7.1 커버페이지 (`ui/reader/cover-page/`)

```
ui/reader/cover-page/
├── cover-page.js          # 렌더 + 상태 구독
├── cover-page.css         # 위계 디자인 (디자인 3-3)
└── start-resume-button.js # 진행률 기반 버튼 상태 결정
```

#### 렌더 로직

```js
// cover-page.js
export function renderCoverPage() {
  const s = getState();
  const m = s.book.manifest;
  const progress = loadProgress(m.id);

  return `
    <div class="cover-page">
      ${m.cover.image ? `<img class="cover-image" src="${m.cover.image}" alt="${m.title}">` : ''}
      <h1 class="cover-title">${escapeHTML(m.title)}</h1>
      ${m.subtitle ? `<p class="cover-subtitle">${escapeHTML(m.subtitle)}</p>` : ''}
      <p class="cover-author">${escapeHTML(m.author)}</p>
      <div class="cover-actions">
        <button class="btn-secondary" data-action="toc">목차</button>
        <button class="btn-primary" data-action="start">
          ${progress.lastReadCardId ? `이어 읽기 (${progress.readCards.length}/${m.totalCards || s.cards.length})` : '읽기 시작'}
        </button>
      </div>
    </div>
  `;
}
```

#### CSS (디자인 3-3 위계)

```css
/* styles/reader.css */
.cover-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.cover-image {
  width: clamp(240px, 60vw, 320px);
  aspect-ratio: 5 / 7;      /* 책 표지 비율 */
  object-fit: cover;
  border-radius: var(--radius);
  box-shadow: 0 12px 48px hsl(0 0% 0% / 0.12);
  margin-bottom: 3rem;
}

.cover-title {
  font-family: 'Pretendard', serif;
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 700;
  margin: 0 0 0.75rem;
  letter-spacing: -0.02em;
}

.cover-subtitle {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: hsl(var(--muted-foreground));
  margin: 0 0 2rem;
  max-width: 28rem;
}

.cover-author {
  font-size: 0.9rem;
  color: hsl(var(--muted-foreground));
  letter-spacing: 0.05em;
  margin-bottom: 3rem;
}

.cover-actions {
  display: flex;
  gap: 1rem;
}
```

#### 액션

```js
// 커버페이지 액션 핸들러
function handleCoverAction(action) {
  if (action === 'toc') {
    dispatch(changeView('cardboard'));
  } else if (action === 'start') {
    const progress = loadProgress();
    const targetId = progress.lastReadCardId 
                  || getFirstCard().id;
    dispatch(changeView('docview'));
    dispatch(openCard(targetId));
  }
}
```

### 7.2 진행률 (`ui/reader/progress/`)

```
ui/reader/progress/
├── progress-store.js      # localStorage 입출력
├── progress-tracker.js    # 문서뷰 열림 감지 → readCards에 추가
└── progress-bar.js        # 문서뷰 하단 진행 바
```

#### Storage 키

```js
// localStorage 키
const PROGRESS_KEY = (bookId) => `ol_reader_progress_${bookId}`;
```

#### 추적 로직

```js
// progress-tracker.js
export function trackCardRead(cardId) {
  const bookId = getState().book.manifest.id;
  const p = loadProgress(bookId);
  if (!p.readCards.includes(cardId)) {
    p.readCards.push(cardId);
  }
  p.lastReadCardId = cardId;
  p.lastReadAt = new Date().toISOString();
  saveProgress(bookId, p);
  devLog('STORAGE', 'progress updated', cardId);
  queueRender('progress-bar');
  queueRender('cover-page');  // 이어읽기 버튼 갱신
}

export function loadProgress(bookId) {
  bookId = bookId || getState().book.manifest.id;
  try {
    const raw = localStorage.getItem(PROGRESS_KEY(bookId));
    if (!raw) return defaultProgress();
    return JSON.parse(raw);
  } catch {
    return defaultProgress();
  }
}

function defaultProgress() {
  return { lastReadCardId: null, lastReadAt: null, readCards: [] };
}
```

#### UI 표시

- **커버페이지**: 이어읽기 버튼에 진행률 표시
- **카드보드**: 읽은 카드에 옅은 표시 (체크 또는 색 변화)
- **문서뷰 하단**: `이 책의 35% (30/87)` 진행 바

### 7.3 책갈피 (`ui/reader/bookmark/`)

```
ui/reader/bookmark/
├── bookmark-store.js
├── bookmark-button.js     # 문서뷰 우측의 책갈피 토글
└── bookmark-list.js       # 사이드바의 책갈피 섹션
```

#### Storage 키

```js
const BOOKMARK_KEY = (bookId) => `ol_reader_bookmarks_${bookId}`;
```

진행률과 같은 네임스페이스 패턴.

#### UI

- 문서뷰 우측 가장자리에 작은 책갈피 아이콘 (lucide `bookmark`)
- 클릭 시 토글 (저장됨/안 저장됨)
- 사이드바에 "책갈피" 섹션, 책갈피 카드 목록 표시

### 7.4 본문 내부 링크 `[[id]]` (shared)

마크다운 파서 확장 — 양쪽 런타임 공통.

#### 문법

```markdown
이 개념은 [[연기]]와 깊이 연결된다.
또한 [[card-buddha-001|붓다의 깨달음]] 장면을 참고하라.
```

- `[[id]]` 또는 `[[id|표시명]]` 형태
- `id`는 카드 ID 또는 slug

#### 파서 구현

```js
// src/data/markdown.js (parseInline 안에 추가)
function parseInternalLink(text) {
  return text.replace(/\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g, (match, id, label) => {
    const card = findCardByIdOrSlug(id);
    if (!card) {
      return `<span class="internal-link broken" title="찾을 수 없음: ${id}">${label || id}</span>`;
    }
    const display = label || card.title;
    return `<a class="internal-link" href="#card/${card.id}" data-card-id="${card.id}">${escapeHTML(display)}</a>`;
  });
}
```

#### 클릭 핸들러

```js
// 본문 내 a.internal-link 클릭 시
document.addEventListener('click', (e) => {
  const link = e.target.closest('a.internal-link');
  if (!link) return;
  e.preventDefault();
  const cardId = link.dataset.cardId;
  dispatch(changeView('docview'));
  dispatch(openCard(cardId));
});
```

#### ATLAS 자동완성 (author 전용)

```js
// src/ui/author/internal-link-completer.js
// 마크다운 에디터에서 [[ 입력 시 카드 목록 팝오버
```

### 7.5 콘텐츠 통계 (shared, BOOK ABOUT에)

```js
// src/data/stats.js (신규)
export function computeBookStats(state) {
  const cards = state.cards;
  return {
    cardCount: cards.length,
    columnCount: state.cols.length,
    estimatedReadingMinutes: estimateReading(cards),
    topTags: countTopTags(cards, 10),
    topPersons: countByPrefix(cards, '인물', 5),
    topPlaces: countByPrefix(cards, '장소', 5),
    topThemes: countByPrefix(cards, '주제', 10),
    lastUpdated: maxUpdatedAt(cards),
  };
}

function estimateReading(cards) {
  const totalChars = cards.reduce((sum, c) => sum + (c.body?.length || 0), 0);
  return Math.ceil(totalChars / 600);  // 한국어 분당 약 600자
}
```

BOOK의 ABOUT 페이지에서 이 통계를 표시. ATLAS는 옵션.

### 7.6 Sepia 모드 (`ui/reader/sepia-theme/`)

```css
/* src/styles/sepia.css */
:root.theme-sepia {
  --background: 38 27% 92%;    /* 따뜻한 미색 */
  --foreground: 30 25% 22%;
  --card: 38 27% 95%;
  --card-foreground: 30 25% 22%;
  --muted: 38 20% 86%;
  --muted-foreground: 30 15% 40%;
  --border: 38 15% 82%;
  --primary: 30 30% 25%;
  --primary-foreground: 38 27% 95%;
}
```

테마 토글에서 light/dark/sepia 3단계 순환.

### 7.7 BOOK Typography (`styles/reader-typography.css`)

```css
/* src/styles/reader-typography.css */
.book-docview {
  font-family: 'Pretendard Variable', 'Apple SD Gothic Neo', sans-serif;
  font-size: 18px;
  line-height: 1.75;
  letter-spacing: -0.01em;
  max-width: 36rem;
  margin: 0 auto;
  padding: 3rem 1.5rem 6rem;
  color: hsl(var(--foreground));
}

.book-docview h1,
.book-docview h2,
.book-docview h3 {
  font-weight: 600;
  letter-spacing: -0.02em;
}

.book-docview h1 { font-size: 2rem; margin: 2.5em 0 0.75em; }
.book-docview h2 { font-size: 1.5rem; margin: 2em 0 0.5em; }
.book-docview h3 { font-size: 1.25rem; margin: 1.5em 0 0.5em; }

.book-docview p {
  margin-bottom: 1.25em;
}

.book-docview a.internal-link {
  color: hsl(var(--primary));
  text-decoration: none;
  border-bottom: 1px dotted hsl(var(--primary) / 0.4);
}
.book-docview a.internal-link:hover {
  border-bottom-style: solid;
}
.book-docview .internal-link.broken {
  color: hsl(var(--muted-foreground));
  border-bottom: 1px dotted hsl(var(--destructive));
}

/* 모바일 */
@media (max-width: 640px) {
  .book-docview {
    font-size: 17px;
    line-height: 1.7;
    padding: 2rem 1.25rem 5rem;
  }
}
```

### 7.8 사라지는 UI (`ui/reader/`)

#### 데스크탑 — 가장자리 호버 (재고 2-1 결정)

```js
// src/ui/reader/floating-sidebar.js
const EDGE_THRESHOLD = 10;  // px

document.addEventListener('mousemove', (e) => {
  if (mode !== 'book') return;
  
  // 사이드바: 왼쪽 가장자리
  if (e.clientX <= EDGE_THRESHOLD) {
    showFloatingSidebar();
  }
  
  // 상단 메뉴 (문서뷰에서): 상단 가장자리
  if (e.clientY <= EDGE_THRESHOLD && currentView === 'docview') {
    showFloatingHeader();
  }
});

// 사이드바를 벗어나면 자동 닫힘
sidebar.addEventListener('mouseleave', hideFloatingSidebar);
```

#### 모바일 — 본문 탭 시 UI 토글 (재고 2-1 c안)

```js
// src/ui/reader/mobile-ui-toggle.js
let uiVisible = false;
let hideTimer = null;

document.addEventListener('click', (e) => {
  if (mode !== 'book') return;
  if (!isMobile()) return;

  // 링크/버튼/기타 인터랙티브 요소는 통과
  if (e.target.closest('a, button, input, textarea, [role="button"]')) return;
  
  // 본문 영역 탭 → UI 토글
  if (e.target.closest('.book-docview')) {
    toggleMobileUI();
  }
});

function toggleMobileUI() {
  uiVisible = !uiVisible;
  document.body.classList.toggle('book-ui-visible', uiVisible);
  
  if (uiVisible) {
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {
      uiVisible = false;
      document.body.classList.remove('book-ui-visible');
    }, 3000);  // 3초 무동작 시 사라짐
  }
}
```

#### 스타일 (디자인 3-1 + 권장 d안)

```css
/* src/styles/reader.css */
.book-floating-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 280px;
  background: hsl(var(--background) / 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 8px 32px hsl(0 0% 0% / 0.12);
  border-radius: 0 var(--radius) var(--radius) 0;
  transform: translateX(-100%);
  opacity: 0;
  transition: transform 200ms ease, opacity 200ms ease;
  z-index: 30;
}
.book-floating-sidebar.is-visible {
  transform: translateX(0);
  opacity: 1;
}

.book-floating-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  background: hsl(var(--background) / 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  box-shadow: 0 4px 20px hsl(0 0% 0% / 0.08);
  transform: translateY(-100%);
  opacity: 0;
  transition: transform 200ms ease, opacity 200ms ease;
  z-index: 50;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  /* 토론 5-E: 좌측 로고 + 우측 검색/다크모드 */
}
.book-floating-header.is-visible,
body.book-ui-visible .book-floating-header {
  transform: translateY(0);
  opacity: 1;
}
```

---

## 8. ATLAS 신규 모듈

### 8.1 커버페이지 편집기 (`ui/author/cover-editor/`)

토론 2-D 결정: 전용 뷰 + 실시간 미리보기.

```
ui/author/cover-editor/
├── cover-editor.js        # 편집 뷰
├── cover-editor.css
└── cover-preview.js       # 우측 실시간 미리보기 (cover-page를 readonly로 렌더)
```

#### 레이아웃

```
┌─────────────────────────────────────────┐
│ ← 표지 편집                              │
├──────────────────┬──────────────────────┤
│ 제목             │                      │
│ [붓다 스토리]    │                      │
│                  │     [표지 이미지]    │
│ 부제             │                      │
│ [팔리 경전으...] │       붓다 스토리    │
│                  │   팔리 경전으로...   │
│ 표지 이미지      │       비움           │
│ [파일 선택]      │   [목차] [시작]      │
│                  │                      │
│ 시리즈           │                      │
│ [OL BOOK · ...] │                      │
│                  │                      │
│ 발행일·버전      │                      │
│ [2026-05-22]    │                      │
│ [1.0]           │                      │
└──────────────────┴──────────────────────┘
```

각 입력 → dispatch(updateManifest({ ... })) → 우측 미리보기 자동 갱신.

### 8.2 BOOK 배포 버튼 (`ui/author/export/`)

```
ui/author/export/
├── export-book.js         # exportBook() 함수
└── export-button.js       # 사이드바/설정뷰에 버튼 등록
```

배치:

- 사이드바 하단 (ATLAS 사이드바, 햄버거로 열림)
- 설정뷰의 "데이터 관리" 섹션
- 두 곳 모두에서 호출 가능

### 8.3 [[ 자동완성 (`ui/author/internal-link-completer.js`)

마크다운 에디터에 `[[` 입력 시 카드 목록 팝오버 표시. 화살표로 선택, Enter로 삽입.

---

## 9. ATLAS / BOOK 사이드바 분기

`ui/shared/sidebar/`는 셸만 제공. 항목은 reader/author로 분기.

### 9.1 사이드바 항목 정의

```js
// src/ui/shared/sidebar/sidebar.js
export function renderSidebar() {
  const items = [];
  // shared 항목
  items.push({ id: 'about', label: 'ABOUT', icon: 'info' });
  
  // reader/author 항목 주입
  if (OL.Reader.isActive()) {
    items.push(...OL.Reader.getSidebarItems());
  }
  if (OL.Author.isActive()) {
    items.push(...OL.Author.getSidebarItems());
  }
  
  return renderItems(items);
}
```

### 9.2 reader 항목 (BOOK)

```js
// src/ui/reader/reader-sidebar-items.js
export function getReaderSidebarItems() {
  return [
    { id: 'cover', label: '표지', icon: 'book', onClick: () => dispatch(changeView('cover')) },
    { id: 'cardboard', label: '목차', icon: 'list', onClick: () => dispatch(changeView('cardboard')) },
    // 칼럼별 카드 그룹
    ...getState().cols.map(col => ({
      id: `col-${col.id}`,
      label: col.name,
      icon: 'folder',
      children: getCardsInColumn(col.id).map(c => ({
        id: c.id,
        label: c.title,
        onClick: () => { dispatch(changeView('docview')); dispatch(openCard(c.id)); },
      })),
    })),
    { id: 'bookmarks', label: '책갈피', icon: 'bookmark' },
    { id: 'about', label: 'ABOUT', icon: 'info' },
  ];
}
```

### 9.3 author 항목 (ATLAS)

```js
// src/ui/author/author-sidebar-items.js
export function getAuthorSidebarItems() {
  return [
    // 기존 v0.7 항목들
    { id: 'cover-editor', label: '표지 편집', icon: 'image-edit' },
    { id: 'export-book', label: 'BOOK으로 배포', icon: 'download', onClick: exportBook },
    { id: 'trash', label: '휴지통', icon: 'trash' },
  ];
}
```

---

## 10. 작업 단계 — Phase 분할

OL v0.8 사이클(듀얼 런타임)의 작업 단계. v0.7 Phase 0~2 완료 상태에서 시작.

### Phase 8.0 — 빌드 구조 재편 (2~3일)

- src/ 디렉토리 재구성 (`ui/shared/`, `ui/reader/`, `ui/author/`)
- build.mjs를 dual bundle 빌드로 변경
- shared/reader/author entry 파일 작성
- mode 감지 로직 (`detectMode()`)
- 빌드 후 ATLAS 모드로 v0.7과 기능 동등성 확인

### Phase 8.1 — Reader Manifest + schema v8 (1~2일)

- schema v7 → v8 마이그레이션
- S.book.manifest 데이터 모델
- ATLAS 부팅 시 manifest 자동 생성 (기존 데이터에서)

### Phase 8.2 — 커버페이지 (reader) + 편집기 (author) (3~4일)

- `ui/reader/cover-page/`
- `ui/author/cover-editor/`
- ATLAS 사이드바에 "표지 편집" 추가
- 미리보기 실시간 갱신

### Phase 8.3 — exportBook() (2~3일)

- `ui/author/export/export-book.js`
- 메모리 자기참조 정규식 패턴 적용
- ATLAS 사이드바/설정뷰에 "BOOK으로 배포" 버튼
- 검증: 작은 데이터로 BOOK 생성 → 더블클릭 → 커버 표시

### Phase 8.4 — BOOK 기본 작동 (3~4일)

- BOOK 모드 부팅 시퀀스
- BOOK 사라지는 UI (`floating-sidebar`, `floating-header`, 모바일 토글)
- BOOK typography (`reader-typography.css`)
- 카드보드 readonly + 인덱스 정렬
- 카드 클릭 즉시 문서뷰
- 검증: BOOK에서 모든 콘텐츠 읽기 가능

### Phase 8.5 — 진행률 + 책갈피 (2~3일)

- `ui/reader/progress/`
- `ui/reader/bookmark/`
- 커버페이지 이어읽기 버튼
- 문서뷰 하단 진행 바
- 사이드바 책갈피 섹션

### Phase 8.6 — 본문 내부 링크 [[id]] (2일)

- `src/data/markdown.js` 파서 확장
- 클릭 핸들러
- ATLAS 자동완성 (`internal-link-completer.js`)

### Phase 8.7 — 콘텐츠 통계 + sepia 모드 (1~2일)

- `src/data/stats.js`
- BOOK ABOUT 페이지에 통계 표시
- `styles/sepia.css` + 테마 토글 3단계

### Phase 8.8 — 마무리 (2일)

- 모든 분기 게이트 통과 확인
- ATLAS에서 BOOK export → 독립 사용 시나리오
- 첫 BOOK 콘텐츠 시연 (OL 붓다스토리 일부)

**총 예상**: 약 18~26일 (3~5주).

---

## 11. 검증 게이트

각 Phase 종료 시 충족해야 할 조건.

|Gate|조건|
|---|---|
|**Phase 8.0**|ATLAS 모드로 v0.7과 100% 기능 동등|
|**Phase 8.1**|schema v7 → v8 마이그레이션 무손실|
|**Phase 8.2**|커버 편집 → 미리보기 실시간 갱신|
|**Phase 8.3**|exportBook() → 생성된 HTML 더블클릭 → BOOK 부팅|
|**Phase 8.4**|BOOK에서 모든 콘텐츠 읽기 가능. 사라지는 UI 작동|
|**Phase 8.5**|진행률 보존: BOOK 새로고침 후에도 이어읽기|
|**Phase 8.6**|`[[id]]` 클릭 시 해당 카드 문서뷰로 이동|
|**Phase 8.7**|sepia 모드 토글 작동, 통계 정확|
|**Phase 8.8**|OL 붓다스토리 일부를 실제 BOOK으로 만들어 시연|

---

## 12. 위험 요소 및 대응

|위험|등급|대응|
|---|---|---|
|author 번들 분리 중 shared 의존성 누락|🔴|esbuild external 설정 신중. 각 entry의 import 그래프 검증|
|`__STATIC_HTML__` 캡처 시점 깨짐|🔴|메모리 패턴 그대로 적용. boot 첫 줄에 캡처|
|`__LOADED_DATA_B64__` 자기참조 정규식|🔴|`'__LOADED' + '_DATA_B64__'` 분리 패턴 강제|
|BOOK 모드에서 author 액션 dispatch 시도|🟡|reducer는 자기 도메인 외 액션을 default 처리하므로 안전. 단, UI에서 author 버튼이 살아남으면 안 됨|
|진행률 localStorage 키 충돌|🟡|bookId에 ORIGIN.site + title + version 조합|
|sepia 모드와 마크다운 코드블록 색상 충돌|🟡|sepia.css에 코드블록 색상도 명시|
|BOOK의 `[[broken-id]]` 처리|🟡|카드 없으면 회색 + 점선 표시, 클릭 무반응|
|모바일 본문 탭 vs 링크 클릭 충돌|🟡|`event.target.closest('a, button, ...)`로 가드|
|커버 이미지 base64로 인해 HTML 크기 급증|🟡|권장 해상도 명시(480x672 등), 사용자에게 경고|

---

## 13. 다음 사이클 (v0.9 이후) 후보

v0.8 듀얼 런타임 완료 후 검토 가능한 항목들. **지금 결정하지 않는다.**

- 떠있는 mini-TOC (디자인 3-2 보류분)
- BOOK warm gray 팔레트 (디자인 3-2 보류분)
- BOOK 간 링크 (`[[book-id::card-id]]`)
- BOOK 검색 결과 시각화 개선
- 첫 콘텐츠(붓다스토리) 작업 경험을 반영한 BOOK UX 개선

원칙: **콘텐츠가 설계를 끌게 한다.** 첫 BOOK을 만들고 독자 반응을 본 후 결정.

---

## 14. 부록 A — 권장 작업 순서

1. **본 설계서 검토 후 확정 선언.**
2. Phase 8.0 작업지시서 작성 요청.
3. Phase 8.0 착수 — 빌드 구조 재편이 가장 위험. 한 번에 모든 디렉토리 옮기지 말고, Phase 0~2 패턴처럼 세션 분할.
4. Phase 8.0 완료 시점에 v0.7 ATLAS와 기능 동등 확인 — 이게 후속 진행의 게이트.
5. 이후 Phase 8.1~8.8 순차 진행.

각 Phase는 Phase 0~2의 작업지시서 형식을 그대로 따른다:

- 권한 선언 블록 최상단
- 세션 분할
- 검증 게이트
- 5세션마다 git commit + tag

---

## 부록 B — 메모리 원칙 점검

작성 시점에 본 설계서가 메모리 원칙과 정합한지 점검:

|원칙|본 설계와의 정합성|
|---|---|
|OL은 불교콘텐츠 연기망의 그물코|✅ 강화. 본문 내부 링크 [[id]]가 연기망 직접 구현|
|본질은 불교콘텐츠|✅ BOOK 분리로 콘텐츠 전달이 중심|
|받은 사람이 자유롭게 수정·배포|✅ ATLAS는 그대로. BOOK은 출판물이라는 다른 형식|
|ORIGIN 하드코딩|✅ Reader Manifest가 ORIGIN을 자동 복제|
|ES modules dev, 단일 HTML dist|✅ Dual Bundle도 단일 HTML 유지|
|카드 스키마에 관계 필드 추가 예정|✅ [[id]] 파서가 관계 표현의 첫 구현|
|IndexedDB/PWA/Electron/런타임 CDN 미채택|✅ 그대로|

---

## 부록 C — 외형 개선 함정 점검

본 설계서가 외형/기능에 과도하게 몰입한 것이 아닌지 마지막 점검:

|항목|본질 직결도|
|---|---|
|듀얼 런타임 분기|⭐⭐⭐ 콘텐츠 전달 방식의 본질|
|커버페이지|⭐⭐ 콘텐츠의 첫 인상|
|본문 내부 링크|⭐⭐⭐ 연기망의 직접 구현|
|진행률 추적|⭐⭐ 책의 본질 기능|
|책갈피|⭐⭐ 책의 본질 기능|
|콘텐츠 통계|⭐ 콘텐츠에 보조적|
|sepia 모드|⭐ 가독성 보조|
|BOOK typography|⭐⭐ 콘텐츠 전달의 본질|
|사라지는 UI|⭐⭐ 몰입 독서의 본질|

⭐ 단일 항목들(통계, sepia)은 외형 개선 성격이 일부 있다. 단, 구현 비용이 낮고 BOOK의 정체성에 기여하므로 v1에 포함. **그러나 Phase 8.7은 가장 마지막에 배치**하여, 시간 부족 시 v1.1로 미룰 수 있도록 함.

---

**작성**: Claude (with biwoom) **상태**: 설계 확정. Phase 8.0 작업지시서 작성 단계로 진입 가능. **다음 문서**: Phase 8.0 작업지시서 (빌드 구조 재편)