# OL 듀얼 런타임 설계서 v1.2

**버전**: v1.2 (v1.1 → ES modules 전면 전환 반영) **작성일**: 2026-05-22 (v1.0) / 2026-05-23 (v1.1, v1.2 갱신) **선행 문서**: `OL_ATLAS_v0_7_최종_기획서_v2.md`, Phase 0~2 작업지시서 (모두 완료), Phase 2 완료 코드(`ol-atlas.html` 약 5800줄) **상태**: 설계 확정 — 구현 사이클 진입 가능

### v1.2에서 갱신된 핵심 사항

- ✅ **ES modules 전면 전환 채택**: Phase 8.0에서 concat 방식 → ES modules로 전환. 메모리 #2의 원래 의도("소스는 ES modules") 회복.
- ✅ **빌드 도구**: esbuild가 ES modules → 단일 IIFE 번들로 변환. 산출물은 외부 의존성 0인 단일 HTML 그대로.
- ✅ **듀얼 런타임 분기 안전성 강화**: reader/author 간 함수 우연 호출이 빌드 시점에 잡힘 (런타임 ReferenceError 회피).
- ✅ **AUTHOR_BUNDLE 마커 보존 전략**: esbuild `legalComments` 설정 또는 마커 함수 호출 패턴.
- ✅ **Phase 8.0 작업량 증가 반영**: 2~3일 → 4~6일 (ES modules 전환 포함).
- ✅ **총 일정**: 20~29일 → 22~32일.

### v1.1에서 갱신된 핵심 사항 (이어받음)

- ✅ **실제 코드 구조 반영**: `src/components/`, `src/actions/`, `src/core/`, `src/ui/`, `src/data/`, `src/styles/` 구조
- ✅ **데이터 모델 보정**: `S.columns` (실제 필드명), `S.userData.status[id]`
- ✅ **Phase 1 인프라 명시**: `markDirty`, `markClean`, `_scheduleAutosave`, `installBeforeUnloadGuard` 모두 작동 중
- ✅ **신규 작업**: §7.8 커스텀 confirm 모달 + §8.4 ATLAS 정비 + Phase 7.x 신설

---

## 0. 한 줄 요약

> v0.7 Phase 0~2가 완료된 시점에서 OL은 **ATLAS(편집기) + BOOK(출판물)** 의 듀얼 런타임으로 분기한다. Phase 8.0에서 **ES modules 전면 전환**과 함께 두 런타임은 한 코드베이스에서 빌드되고, 한 dist 파일에 공존하며, **브라우저에서 `exportBook()` 한 번으로 BOOK이 생성**된다. ATLAS는 그대로 풍부한 편집 환경, BOOK은 몰입형 독서 환경.

### Phase 2 완료 시점에 이미 작동하는 것 (재확인용)

- ✅ Action Layer: `dispatch(action)`, `registerReducer(fn)`, 9개 reducer 등록 완료
- ✅ Render Queue: `queueRender(viewName)` + rAF flush
- ✅ Dirty State: `markDirty`, `markClean`, `isDirty`
- ✅ Autosave: 1초 디바운스 자동 저장
- ✅ beforeunload guard: 시스템 다이얼로그로 새로고침 경고 (이미 작동)
- ✅ Proxy strict mode: 직접 `S.xxx = ...` 시 에러
- ✅ Schema v7 마이그레이션
- ⚠ **빌드 방식**: 현재는 파일 concat. **Phase 8.0에서 ES modules로 전환 예정.**

---

## 1. 정체성 분리 — ATLAS vs BOOK

### 1.1 두 런타임의 성격

|측면|ATLAS (Author Runtime)|BOOK (Reader Runtime)|
|---|---|---|
|**정체성**|콘텐츠 제작 공방|출판물 / 책|
|**사용자**|제작자 (비움)|독자|
|**모드**|편집 가능 + 모든 뷰|읽기 전용 + 몰입형|
|**첫 화면**|카드보드 (홈랜딩 폐기)|커버페이지|
|**데이터 상태**|dirty + autosave 작동|readonly, 진행률만 저장|
|**UI 인터랙션**|햄버거 토글, 명시적|사라지는 UI, 몰입형|
|**목적**|"어떻게 편집할까"|"어떻게 읽히게 할까"|

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

## 3. 아키텍처 — ES Modules + 마커 기반 단일 번들

### 3.1 빌드 모델의 진화

**v1.0** → **v1.1** → **v1.2** 세 단계의 변화:

|측면|v1.0 (가정)|v1.1 (concat 유지)|v1.2 (★현재 채택)|
|---|---|---|---|
|소스 작성|ES modules|평면 파일 + 전역 함수|**ES modules + import/export**|
|빌드 변환|esbuild 두 번들|단순 concat|**esbuild → 단일 IIFE**|
|의존성|명시적 import|암묵적 전역|**명시적 import**|
|트리쉐이킹|가능|불가|**가능**|
|듀얼 런타임 격리|두 script 분리|마커 주석|**마커 보존 + import 그래프 검증**|
|최종 산출물|단일 HTML|단일 HTML|**단일 HTML (동일)**|

**핵심**: 사용자 입장에서는 v1.1과 v1.2가 똑같다. 단일 외부 의존성 0 HTML. 차이는 **소스 작성 방식**과 **빌드 시점에 잡히는 오류의 양**.

### 3.2 ES modules 작성 원칙

#### 3.2.1 모든 파일은 명시적 import/export

```js
// src/core/store.js
let _state = null;
const _subscribers = new Map();

export function storeInit(initialState) {
  _state = initialState;
  devLog('BOOT', 'store initialized', { cardCount: _state.cards?.length });
}

export function getState() { return _state; }
export function applyState(newState) { _state = newState; }
export function subscribe(viewName, renderFn) {
  _subscribers.set(viewName, renderFn);
}
export function getSubscriber(viewName) { return _subscribers.get(viewName); }
export function listViews() { return [..._subscribers.keys()]; }
```

```js
// src/core/action.js
import { devLog, devAssert, devTime } from './dev.js';
import { getState, applyState } from './store.js';
import { markDirty } from './dirty.js';
import { queueRender } from './render-queue.js';

const _reducers = [];

export function registerReducer(reducer) {
  _reducers.push(reducer);
}

export function dispatch(action) {
  // 기존 로직 그대로
  devLog('ACTION', action.type, action.payload || {});
  let state = getState();
  for (const reducer of _reducers) {
    state = reducer(state, action);
  }
  applyState(state);
  markDirty();
  // ...
}
```

#### 3.2.2 글로벌 `S` Proxy의 처리

현재 코드는 `S`가 글로벌 변수로 어디서나 접근 가능. ES modules 전환 후:

```js
// src/core/state.js
import { getState } from './store.js';
import { devLog } from './dev.js';

export const S = new Proxy({}, {
  get(target, prop) {
    const state = getState();
    return state ? state[prop] : undefined;
  },
  set(target, prop, value) {
    const msg = '[STRICT] Direct S.' + String(prop) + ' mutation forbidden — use dispatch()';
    console.error(msg);
    throw new Error(msg);
  },
});

// 다른 파일에서 사용
import { S } from '../core/state.js';
S.cards    // 읽기 OK
S.cards = [] // 에러 (strict mode)
```

#### 3.2.3 ICONS_X, ORIGIN 등 상수도 명시적 export

```js
// src/core/constants.js
export const ORIGIN = Object.freeze({
  author: '비움',
  site: 'olbit.org',
  copyright: 'Copyright © 2026 biwoom',
  license: 'CC BY-SA 4.0',
  tool: 'OL · ATLAS · Weaving the Wisdom',
});

export const COL_COLORS = [/* ... */];
export const OL_PROJECTS = Object.freeze([/* ... */]);
export const ICONS_X = { /* ... */ };
```

### 3.3 esbuild 빌드 — ES modules → 단일 IIFE

#### 3.3.1 빌드 명령

```js
// build/build.mjs
import { build } from 'esbuild';
import { readFileSync, writeFileSync } from 'node:fs';

async function buildOL() {
  // 1. ES modules → 단일 IIFE 번들
  const result = await build({
    entryPoints: ['src/main.js'],
    bundle: true,
    format: 'iife',
    minify: false,                    // 마커 보존 위해 처음엔 minify off
    legalComments: 'inline',          // 마커 주석 보존
    target: 'es2020',
    write: false,                     // 메모리에서 받아서 inline 처리
    define: {
      'process.env.NODE_ENV': '"production"',
    },
  });

  const jsBundle = result.outputFiles[0].text;

  // 2. CSS concat
  const cssFiles = [
    'src/styles/tokens.css',
    'src/styles/base.css',
    'src/styles/components.css',
    // ...
  ];
  const cssBundle = cssFiles.map(f => readFileSync(f, 'utf8')).join('\n');

  // 3. HTML 셸에 inline
  const htmlShell = readFileSync('src/index.html', 'utf8');
  const html = htmlShell
    .replace('<!--CSS-->', `<style>${cssBundle}</style>`)
    .replace('<!--JS-->', `<script>${jsBundle}</script>`);

  writeFileSync('dist/ol-atlas.html', html);
  console.log('Build complete:', html.length, 'bytes');
}

buildOL();
```

#### 3.3.2 src/main.js — 통합 엔트리

```js
// src/main.js
// 모든 모듈을 명시적으로 import하여 esbuild가 의존성 그래프 구성

// === 1. CORE (양쪽 공통) ===
import './core/dev.js';
import './core/store.js';
import './core/render-queue.js';
import './core/schema.js';
import './core/storage.js';
import './core/dirty.js';
import './core/action.js';
import './core/static-html.js';
import './core/state.js';
import './core/constants.js';
import './core/utils.js';
import './core/markdown.js';
import './core/tag-parser.js';
import './core/tag-filter.js';
import './core/theme.js';
import './core/router.js';

// === 2. ACTIONS ===
import './actions/card-actions.js';
import './actions/column-actions.js';
import './actions/view-actions.js';
import './actions/settings-actions.js';

// === 3. SHARED COMPONENTS ===
import './components/shared/confirm-modal.js';
import './components/shared/dirty-indicator.js';
import './components/shared/docview.js';
import './components/shared/sidebar.js';
import './components/shared/about.js';
import './components/shared/toc.js';
import './ui/custom-select.js';

// === 4. AUTHOR BUNDLE START (마커는 import 사이에 주석으로) ===
// AUTHOR_BUNDLE_START
import './components/author/home.js';
import './components/author/kanban.js';
import './components/author/cardgrid.js';
import './components/author/listview.js';
import './components/author/card-modal.js';
import './components/author/docview-inline.js';
import './components/author/md-editor.js';
import './components/author/bulk-select.js';
import './components/author/color-picker.js';
import './components/author/cover-editor.js';
import './components/author/internal-link-completer.js';
import './actions/export-import.js';
import './components/author/export-book.js';
// AUTHOR_BUNDLE_END

// === 5. READER COMPONENTS ===
import './components/reader/cover-page.js';
import './components/reader/cover-actions.js';
import './components/reader/progress.js';
import './components/reader/bookmark.js';
import './components/reader/reader-sidebar.js';
import './components/reader/floating-ui.js';
import './components/reader/reader-cardboard.js';
import './components/reader/sepia-theme.js';
import './components/reader/stats.js';
import './components/reader/internal-link.js';

// === 6. BOOT ===
import { boot } from './data/init.js';
boot();
```

### 3.4 AUTHOR_BUNDLE 마커 보존 전략

ES modules + esbuild 환경에서 마커를 빌드 산출물까지 살려두는 두 가지 방법:

#### 방법 A: `/*! */` 형식 주석 + `legalComments: 'inline'` (권장)

esbuild는 `/*! */` 형식 주석을 "legal comment"로 간주하여 보존한다.

```js
// src/main.js
/*! AUTHOR_BUNDLE_START */
import './components/author/home.js';
import './components/author/kanban.js';
// ...
import './components/author/export-book.js';
/*! AUTHOR_BUNDLE_END */
```

빌드 후:

```js
(()=>{
  // ... shared ...
  /*! AUTHOR_BUNDLE_START */
  // 모든 author 코드 (esbuild가 import를 따라가서 인라인)
  /*! AUTHOR_BUNDLE_END */
  // ... reader ...
})();
```

`exportBook()`은 두 마커 사이를 정규식으로 제거.

#### 방법 B: 마커 함수 호출 패턴

```js
// src/core/markers.js
export function __authorBundleStart() {}
export function __authorBundleEnd() {}

// src/main.js
import { __authorBundleStart, __authorBundleEnd } from './core/markers.js';

__authorBundleStart();
import './components/author/home.js';
// ...
__authorBundleEnd();
```

빌드 후 함수 호출이 살아남아 마커 역할.

#### 방법 결정: A 채택

- 간단함, 추가 코드 0
- esbuild 표준 기능
- minify 시에도 `legalComments: 'inline'`이 보존

### 3.5 빌드 산출물 구조

```
dist/ol-atlas.html
├── <head>
│   ├── meta, favicon, <title>
│   └── <style>  /* CSS 인라인 (모든 .css concat) */
├── <body>
│   ├── <div id="app"></div>
│   ├── <script>
│   │     const __LOADED_DATA_B64__ = '__INIT_DATA_B64__';
│   │   </script>
│   └── <script>
│         (()=>{
│           /* esbuild가 만든 단일 IIFE */
│           
│           // CORE imports (의존성 순서대로 인라인됨)
│           // dev, store, render-queue, schema, storage, dirty, action, ...
│           
│           // ACTIONS
│           // card-actions, column-actions, view-actions, settings-actions
│           
│           // SHARED COMPONENTS
│           // confirm-modal, dirty-indicator, docview, sidebar(shared), ...
│           
│           /*! AUTHOR_BUNDLE_START */
│           // home, kanban, cardgrid, listview, card-modal,
│           // docview-inline, md-editor, bulk-select, color-picker,
│           // cover-editor, internal-link-completer, export-import, export-book
│           /*! AUTHOR_BUNDLE_END */
│           
│           // READER COMPONENTS
│           // cover-page, progress, bookmark, floating-ui, sepia, stats, ...
│           
│           // BOOT
│           // boot()  // detectMode → bootAtlas | bootBook
│         })();
│       </script>
└── </body>
```

### 3.6 모드 감지 + 부팅 분기

ES modules 환경에서도 모드 감지는 동일하다. 단, author 함수가 export 안 되었으니 `typeof openCardModal` 같은 글로벌 체크는 불가. 대신 **author 모듈이 등록한 view subscriber**의 존재 여부로 감지.

```js
// src/data/init.js
import { devLog } from '../core/dev.js';
import { listViews } from '../core/store.js';
import { storageLoad } from '../core/storage.js';
import { migrate } from '../core/schema.js';
import { storeInit } from '../core/store.js';
import { normalizeState } from '../core/normalize.js';
import { installBeforeUnloadGuard } from '../core/dirty.js';
import { routeFromHash } from '../core/router.js';

function detectMode() {
  // BOOK은 export 시점에 마커가 박힘
  if (typeof window !== 'undefined' && window.__OL_MODE__ === 'book') {
    return 'book';
  }
  // author 모듈이 'kanban' subscriber를 등록했으면 ATLAS
  // (author 번들이 제거되었다면 'kanban'은 등록 안 됨)
  if (listViews().includes('kanban')) {
    return 'atlas';
  }
  return 'book';  // 안전 폴백
}

export function boot() {
  devLog('BOOT', 'boot start');
  
  // 1. 데이터 로드 + 마이그레이션
  let raw = storageLoad();
  raw = migrate(raw);
  raw = normalizeState(raw);
  storeInit(raw);
  
  // 2. beforeunload guard 설치
  installBeforeUnloadGuard();
  
  // 3. 모드 감지 후 분기
  const mode = detectMode();
  devLog('BOOT', 'detected mode:', mode);
  
  if (mode === 'atlas') {
    bootAtlas();
  } else {
    bootBook();
  }
}

function bootAtlas() {
  // 기존 v0.7 부팅 흐름
  routeFromHash();
}

function bootBook() {
  // BOOK 부팅 흐름
  document.body.classList.add('ol-book-mode');
  // cover-page가 첫 화면
  routeBookFromHash();
}
```

**중요**: 각 컴포넌트 파일은 **부수효과(side effect)로 subscribe를 호출**한다. import만 해도 subscribe가 실행된다.

```js
// src/components/author/kanban.js
import { S } from '../../core/state.js';
import { subscribe } from '../../core/store.js';
import { dispatch } from '../../core/action.js';
import { moveCard, createColumn, deleteColumn } from '../../actions/card-actions.js';
// ... 기타 import

export function renderKanban() {
  // 기존 로직 그대로
}

// 부수효과: 이 파일이 import되면 subscribe 실행
subscribe('kanban', renderKanban);
```

BOOK 산출물에서는 author 폴더 import가 통째로 제거되므로 이 파일이 평가되지 않고, `subscribe('kanban', ...)`도 실행되지 않는다. 따라서 `listViews().includes('kanban')`가 false가 되어 BOOK 모드로 감지된다.

### 3.7 디렉토리 구조 (현재 Phase 2 완료 상태)

**Phase 8.0 전 현재**: 파일 concat 방식이지만, Phase 8.0에서 ES modules로 전환된다. 디렉토리는 그대로 유지하면서 각 파일에 import/export만 추가하면 된다.

```
src/
├── core/                       # 공통: 모든 런타임의 핵심 (Phase 0~1 산출물)
│   ├── dev.js                  # devLog, devAssert, devTime
│   ├── store.js                # storeInit, getState, applyState, subscribe (★완료)
│   ├── action.js               # dispatch, registerReducer (★완료)
│   ├── render-queue.js         # queueRender + rAF flush (★완료)
│   ├── dirty.js                # markDirty, markClean, autosave, beforeunload (★완료)
│   ├── schema.js               # v7 migrate (★완료)
│   ├── storage.js              # localStorage save/load (★완료)
│   ├── static-html.js          # __STATIC_HTML__ 캡처 (★완료)
│   ├── state.js                # S Proxy + normalizeCard, normalizeState (★완료)
│   ├── normalize.js            # 정규화 보조
│   ├── constants.js            # ORIGIN, COL_COLORS, OL_PROJECTS
│   ├── markdown.js             # parseInline, parseMarkdown, stripMarkdown
│   ├── tag-parser.js           # parseTag, buildPrefixIndex
│   ├── tag-filter.js           # selectedTags, sbFilter, 필터 헬퍼
│   ├── body-helpers.js         # bodyImagesToTokens, bodyTokensToStandardMd
│   ├── theme.js                # 다크모드 토글
│   ├── router.js               # currentView, switchView, routeFromHash
│   ├── events.js               # 전역 이벤트
│   ├── history.js              # (v0.6 잔존 - Phase 8.0에서 제거)
│   └── utils.js                # ce, today, escapeHTML, sanitizeURL, dlBlob 등
│
├── data/                       # 데이터 / 초기화
│   ├── init.js                 # boot 진입점
│   └── search/
│       └── search.js           # 검색 로직
│
├── actions/                    # Action Layer (Phase 2 산출물, ★완료)
│   ├── card-actions.js         # CARD_CREATE, CARD_UPDATE, CARD_DELETE, ... + cardReducer
│   ├── column-actions.js       # COLUMN_* + columnReducer
│   ├── view-actions.js         # VIEW_*, BOARD_WIDTH_SET, ... + viewReducer
│   ├── settings-actions.js     # SETTINGS_*, THEME_SET + settingsReducer
│   └── export-import.js        # importMerge 액션 + CSV/OL 가져오기
│
├── components/                 # ATLAS UI 컴포넌트 (현재 모든 뷰)
│   ├── home.js                 # 홈 랜딩 (BOOK에서는 cover-page로 대체)
│   ├── about.js                # ABOUT 페이지
│   ├── sidebar.js              # 사이드바
│   ├── kanban.js               # 칸반 뷰
│   ├── cardgrid.js             # 카드 그리드 뷰
│   ├── listview.js             # 리스트 뷰
│   ├── docview.js              # 문서 뷰 (BOOK에서도 readonly로 재사용)
│   ├── docview-inline.js       # 문서뷰 인라인 편집
│   ├── card-modal.js           # 카드 모달
│   ├── bulk-select.js          # 일괄 선택
│   ├── color-picker.js         # 색상 선택
│   ├── md-editor.js            # 마크다운 에디터
│   └── toc.js                  # 자동 목차
│
├── ui/                         # 공용 UI 패턴
│   └── custom-select.js        # 커스텀 select 컴포넌트
│
├── styles/                     # CSS
│   ├── tokens.css              # HSL 토큰 (양쪽 공통)
│   ├── base.css                # reset + 시스템 폰트
│   ├── components.css          # btn, input, dialog 등
│   ├── sidebar.css
│   ├── kanban.css
│   ├── cardgrid.css
│   ├── listview.css
│   ├── docview.css
│   └── modal.css
│
└── index.html                  # HTML 셸
```

### 3.8 듀얼 런타임 분기를 위한 디렉토리 재편 (Phase 8.0에서 수행)

위 구조 위에 듀얼 런타임 분기를 적용하면:

```
src/
├── main.js                     # ★신규: ES modules 통합 엔트리 (§3.3.2 참조)
├── core/                       # 그대로 (양쪽 공통, 각 파일에 export 추가)
├── data/                       # 그대로
├── actions/                    # 그대로 (단, BOOK에서는 변형 액션 dispatch 안 됨)
├── components/                 # → 아래로 재분류
│   ├── shared/                 # 양쪽 유지
│   │   ├── docview.js          # 본문 readonly 부분은 공통
│   │   ├── sidebar.js          # 사이드바 셸 (항목은 분기)
│   │   ├── about.js            # ABOUT 셸 (통계는 분기)
│   │   ├── toc.js              # 자동 목차
│   │   ├── custom-select.js
│   │   ├── confirm-modal.js    # ★신규 (§7.8): div 기반 confirm
│   │   └── dirty-indicator.js  # ★신규 (§8.4.2): dirty 시각 표시
│   │
│   ├── reader/                 # ★신규: BOOK 전용
│   │   ├── cover-page.js       # 커버페이지 렌더
│   │   ├── cover-actions.js    # 목차/시작 액션
│   │   ├── progress.js         # 진행률 추적
│   │   ├── bookmark.js         # 책갈피
│   │   ├── reader-sidebar.js   # BOOK 사이드바 항목
│   │   ├── floating-ui.js      # 사라지는 UI (가장자리 호버 + 모바일 탭)
│   │   ├── reader-cardboard.js # readonly 카드보드
│   │   ├── sepia-theme.js      # sepia 토글
│   │   ├── stats.js            # 콘텐츠 통계 계산
│   │   └── internal-link.js    # [[id]] 클릭 핸들러 (파서는 shared markdown.js에)
│   │
│   └── author/                 # ★신규: ATLAS 전용 (기존 컴포넌트 이동)
│       ├── home.js             # 홈 랜딩 (기존)
│       ├── kanban.js
│       ├── cardgrid.js
│       ├── listview.js
│       ├── card-modal.js
│       ├── docview-inline.js   # 문서뷰 편집 부분
│       ├── md-editor.js
│       ├── bulk-select.js
│       ├── color-picker.js
│       ├── cover-editor.js     # ★신규: 표지 편집 뷰
│       ├── export-book.js      # ★신규: exportBook() 함수
│       └── internal-link-completer.js  # ★신규: [[ 자동완성
│
├── ui/                         # 그대로
├── styles/                     # 분기 추가
│   ├── tokens.css              # 양쪽 공통
│   ├── base.css
│   ├── components.css
│   ├── shared.css              # 양쪽 공통 view 스타일
│   ├── atlas.css               # ATLAS 전용 (기존 sidebar, kanban, ... 통합)
│   ├── reader.css              # ★신규: BOOK 전용
│   ├── reader-typography.css   # ★신규: BOOK 독서 typography
│   ├── sepia.css               # ★신규
│   ├── cover-page.css          # ★신규
│   ├── floating-ui.css         # ★신규
│   ├── confirm-modal.css       # ★신규
│   └── dirty-indicator.css     # ★신규
│
└── index.html
```

**Phase 8.0에서의 작업 흐름**:

1. 기존 평면 파일들을 위 구조로 이동
2. 각 파일에 `export` 키워드 추가 + 다른 파일을 사용하는 곳에 `import` 추가
3. `src/main.js` 생성 (§3.3.2)
4. `build/build.mjs`를 esbuild 호출 방식으로 전환 (§3.3.1)
5. 검증: 빌드 산출물이 v0.7-phase7x-complete와 기능 동등

### 3.9 빌드 도구 비교 — concat 방식(v1.1) vs ES modules(v1.2)

v1.1에서는 `build.mjs`의 `JS_FILES` 배열에 명시한 순서대로 파일을 concat하는 방식이었다. v1.2의 ES modules에서는 **JS_FILES 배열이 사라지고, `src/main.js`의 import 그래프가 그 역할을 대신한다**.

비교:

|측면|v1.1 (concat)|v1.2 (ES modules)|
|---|---|---|
|순서 결정|JS_FILES 배열 수동 작성|import 그래프 자동 분석|
|빠진 파일 검출|런타임에 ReferenceError|빌드 시점 에러|
|중복 import|무관 (이미 평가됨)|esbuild가 자동 중복 제거|
|트리쉐이킹|불가|가능 (export 안 된 것 제거)|
|마커 보존|가짜 문자열 `'// === AUTHOR_BUNDLE_START ==='`|`/*! AUTHOR_BUNDLE_START */` 주석 + `legalComments: 'inline'`|
|빌드 도구|단순 fs.readFileSync + concat|esbuild bundle|

#### 참고용 — v1.1 시점의 JS_FILES 배열 (Phase 8.0 전 그대로 사용)

Phase 7.x 작업 중에는 아직 concat 방식이므로, JS_FILES 배열은 다음과 같이 유지된다. Phase 8.0에서 이 배열은 `src/main.js`의 import문으로 변환된다.

```js
// build/build.mjs의 JS_FILES (Phase 7.x까지 유효)
const JS_FILES = [
  // === 1. SHARED CORE ===
  'src/core/dev.js',
  'src/core/store.js',
  'src/core/render-queue.js',
  'src/core/schema.js',
  'src/core/storage.js',
  'src/core/dirty.js',
  'src/core/action.js',
  'src/core/static-html.js',
  'src/core/tag-parser.js',
  'src/ui/custom-select.js',
  'src/core/tag-filter.js',
  'src/core/constants.js',
  'src/core/utils.js',
  'src/core/body-helpers.js',
  'src/core/markdown.js',
  'src/core/normalize.js',
  'src/core/state.js',
  
  // === 2. ACTIONS ===
  'src/actions/card-actions.js',
  'src/actions/column-actions.js',
  'src/actions/view-actions.js',
  'src/actions/settings-actions.js',
  
  // === 3. SHARED COMPONENTS (Phase 7.x에서 추가) ===
  'src/components/shared/confirm-modal.js',
  'src/components/shared/dirty-indicator.js',
  
  // === 4. AUTHOR COMPONENTS (Phase 7.x까지는 분기 전) ===
  'src/components/about.js',
  'src/components/sidebar.js',
  'src/components/kanban.js',
  'src/components/cardgrid.js',
  'src/components/listview.js',
  'src/components/docview.js',
  'src/components/docview-inline.js',
  'src/components/card-modal.js',
  'src/components/bulk-select.js',
  'src/components/color-picker.js',
  'src/components/md-editor.js',
  'src/components/toc.js',
  'src/components/home.js',
  'src/actions/export-import.js',
  
  // === 5. ROUTER + BOOT ===
  'src/core/theme.js',
  'src/core/router.js',
  'src/core/events.js',
  'src/data/init.js',
];
```

**Phase 8.0의 전환 작업**:

- 위 JS_FILES 배열의 각 파일을 ES modules로 변환 (export 추가 + 의존성 import 추가)
- `src/main.js`에서 §3.3.2와 같이 명시적 import (단, AUTHOR_BUNDLE_START/END 사이는 author 모듈만)
- `build.mjs`를 esbuild 호출로 전환
- 빌드 산출물의 AUTHOR_BUNDLE 마커가 살아남는지 검증

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
[ATLAS 사이드바 또는 ABOUT 페이지의 "BOOK으로 배포" 버튼]
    ↓
[exportBook() 호출]
    ↓
1. Reader Manifest 유효성 검사
   - 필수 필드 (title, id 등) 확인
   - 경고가 있으면 custom-confirm 다이얼로그 (§7.8)
    ↓
2. 현재 HTML 가져오기
   - window.__STATIC_HTML__ 사용 (v0.6 패턴 계승, 이미 작동 중)
    ↓
3. AUTHOR_BUNDLE 영역 제거
   - // === AUTHOR_BUNDLE_START === 부터
   -   // === AUTHOR_BUNDLE_END === 까지 통째로 삭제
   - 정규식: /\/\/ === AUTHOR_BUNDLE_START ===[\s\S]*?\/\/ === AUTHOR_BUNDLE_END ===/
    ↓
4. mode 마커 박기
   - <script>window.__OL_MODE__='book';</script>를 boot 직전에 추가
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
// src/components/author/export-book.js
// 이 파일은 AUTHOR_BUNDLE_START/END 마커 안에 위치 (BOOK에는 안 포함됨)

async function exportBook(opts) {
  opts = opts || {};
  devLog('BOOT', 'exportBook start');

  // 1. 유효성
  const s = getState();
  const manifest = (s.book && s.book.manifest) || buildDefaultManifest(s);
  const validation = validateManifest(manifest);
  if (!validation.ok) {
    const proceed = await customConfirm({
      title: 'BOOK 배포 전 확인',
      message: '다음 항목을 확인해주세요:\n\n' + validation.warnings.join('\n') + '\n\n그래도 진행하시겠습니까?',
      confirmText: '진행',
      cancelText: '취소',
    });
    if (!proceed) return;
  }

  // 2. HTML 베이스 가져오기 (이미 boot 시점에 캡처됨)
  let html = window.__STATIC_HTML__;
  if (!html) {
    customAlert({ title: '오류', message: '__STATIC_HTML__이 캡처되지 않았습니다.' });
    return;
  }

  // 3. AUTHOR_BUNDLE 영역 제거
  // 메모리의 자기참조 정규식 트랩 회피: 분리 패턴
  // v1.2 ES modules: 마커가 /*! AUTHOR_BUNDLE_START */ ... /*! AUTHOR_BUNDLE_END */ 형태
  const MARKER_START = '/*! ' + 'AUTHOR_BUNDLE_START' + ' */';
  const MARKER_END = '/*! ' + 'AUTHOR_BUNDLE_END' + ' */';
  const escapeRe = function(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); };
  const bundleRe = new RegExp(escapeRe(MARKER_START) + '[\\s\\S]*?' + escapeRe(MARKER_END), 'g');
  html = html.replace(bundleRe, '/*! [author bundle removed] */');

  // 4. mode 마커
  html = injectBeforeBoot(html, '<script>window.__OL_MODE__="book";</script>');

  // 5. 데이터 inline
  const bookData = buildBookData(s);
  const json = JSON.stringify(bookData);
  const b64 = btoa(unescape(encodeURIComponent(json)));
  
  // __LOADED_DATA_B64__의 자기참조 회피 패턴
  const DATA_MARKER = '__LOADED' + '_DATA_B64__';
  const initRe = new RegExp("'__INIT_DATA_B64__'");
  html = html.replace(initRe, "'" + b64 + "'");

  // 6. 메타 정보 head 갱신
  html = updateHead(html, manifest);

  // 7. 다운로드
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = slugFilename(manifest.title || 'ol-book', 'ol-book') + '.html';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);

  devLog('BOOT', 'exportBook done');
  toast('BOOK으로 배포되었습니다');
}

function buildBookData(s) {
  return {
    meta: {
      schemaVersion: 8,  // v8: book 필드 추가
      olVersion: '0.8.0-book',
      exportedAt: new Date().toISOString(),
    },
    cards: s.cards,
    columns: s.columns,  // 실제 필드명: cols 아님
    userData: { status: {} },  // BOOK에서는 status는 독자 localStorage에
    nextColId: s.nextColId,
    nextCardId: s.nextCardId,
    book: { manifest: (s.book && s.book.manifest) || buildDefaultManifest(s) },
    settings: { theme: 'system', locale: s.settings.locale },
    // trash는 명시적으로 제외
  };
}

function validateManifest(m) {
  const warnings = [];
  if (!m || !m.title) warnings.push('· 책 제목이 비어있습니다');
  if (!m || !m.id) warnings.push('· BOOK ID가 비어있습니다');
  if (!m || !m.cover || !m.cover.image) warnings.push('· 표지 이미지가 없습니다');
  return { ok: warnings.length === 0, warnings: warnings };
}

function injectBeforeBoot(html, snippet) {
  // boot 진입 직전(<script id="ol-init">) 또는 첫 <script> 직전에 삽입
  const re = /<script>(?=\(function\(\)\{)/;
  return html.replace(re, snippet + '<script>');
}

function updateHead(html, manifest) {
  // <title>, og:title, description 갱신
  let out = html;
  if (manifest.title) {
    out = out.replace(/<title>[^<]*<\/title>/, '<title>' + escapeHTML(manifest.title) + '</title>');
  }
  return out;
}
```

### 6.3 v0.6 자기참조 정규식 트랩 회피 — 메모리 패턴 적용

위 코드는 메모리에 기록된 사고 패턴을 회피:

```js
// ❌ 위험: 정규식 자체가 빌드 산출물 안에서 자기 자신과 매치
const re = /__LOADED_DATA_B64__/g;

// ✅ 안전: 문자열 concat으로 마커 분리
const DATA_MARKER = '__LOADED' + '_DATA_B64__';
const re = new RegExp(escapeRe(DATA_MARKER), 'g');
```

`AUTHOR_BUNDLE_START`/`END` 마커도 같은 방식으로 처리.

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

### 7.8 커스텀 confirm/alert 모달 (★신규, shared) — `confirm-modal.js`

비움의 요청: **시스템 confirm/alert을 div 기반 커스텀 모달로 교체**.

#### 배경

현재 Phase 2 완료 코드에는 9개의 시스템 confirm/alert가 남아있다:

|위치|메시지|대응|
|---|---|---|
|`core/storage.js` save 실패|`alert("저장 실패: ...")`|customAlert|
|`core/router.js` switchView|"변경 사항이 저장되지 않았습니다..."|customConfirm|
|`components/docview-inline.js` goToDocCard|동일|customConfirm|
|`components/docview-inline.js` cancelInlineEdit|"변경 사항을 버리시겠습니까?"|customConfirm|
|`components/about.js` trash 영구삭제|"영구 삭제하시겠습니까?..."|customConfirm|
|`components/about.js` 휴지통 비우기|"휴지통을 완전히..."|customConfirm|
|`components/kanban.js` 컬럼 삭제|"N개의 카드가 있습니다..."|customConfirm (위험 강조)|
|`components/card-modal.js` 카드 삭제|"이 카드를 휴지통으로..."|customConfirm|
|`components/bulk-select.js` 일괄 삭제|"선택한 N개..."|customConfirm|

#### 모듈 설계 (`src/components/shared/confirm-modal.js`)

```js
// src/components/shared/confirm-modal.js
// div 기반 confirm/alert 모달. Promise 기반 API.

let _modalStack = [];
let _modalPrevFocus = null;

function _ensureModalRoot() {
  let root = document.getElementById('ol-modal-root');
  if (!root) {
    root = document.createElement('div');
    root.id = 'ol-modal-root';
    document.body.appendChild(root);
  }
  return root;
}

function customConfirm(opts) {
  opts = opts || {};
  return new Promise(function(resolve) {
    _showModal({
      title: opts.title || '확인',
      message: opts.message || '',
      confirmText: opts.confirmText || '확인',
      cancelText: opts.cancelText || '취소',
      danger: !!opts.danger,
      defaultCancel: opts.defaultCancel !== false,  // 기본: 취소가 default focus
      onConfirm: function() { resolve(true); },
      onCancel: function() { resolve(false); },
    });
  });
}

function customAlert(opts) {
  opts = opts || {};
  return new Promise(function(resolve) {
    _showModal({
      title: opts.title || '알림',
      message: opts.message || '',
      confirmText: opts.confirmText || '확인',
      cancelText: null,  // alert는 취소 없음
      danger: !!opts.danger,
      onConfirm: function() { resolve(); },
    });
  });
}

function _showModal(o) {
  const root = _ensureModalRoot();
  _modalPrevFocus = document.activeElement;

  const overlay = document.createElement('div');
  overlay.className = 'ol-modal-overlay';

  const dialog = document.createElement('div');
  dialog.className = 'ol-modal-dialog' + (o.danger ? ' ol-modal-danger' : '');
  dialog.setAttribute('role', 'alertdialog');
  dialog.setAttribute('aria-modal', 'true');
  dialog.setAttribute('aria-labelledby', 'ol-modal-title');

  const titleEl = document.createElement('div');
  titleEl.className = 'ol-modal-title';
  titleEl.id = 'ol-modal-title';
  titleEl.textContent = o.title;

  const msgEl = document.createElement('div');
  msgEl.className = 'ol-modal-message';
  // 줄바꿈 보존
  String(o.message).split('\n').forEach(function(line, i) {
    if (i > 0) msgEl.appendChild(document.createElement('br'));
    msgEl.appendChild(document.createTextNode(line));
  });

  const actions = document.createElement('div');
  actions.className = 'ol-modal-actions';

  // 취소 버튼 (있을 때만)
  let cancelBtn = null;
  if (o.cancelText) {
    cancelBtn = document.createElement('button');
    cancelBtn.className = 'ol-modal-btn ol-modal-cancel';
    cancelBtn.textContent = o.cancelText;
    cancelBtn.addEventListener('click', function() {
      _closeModal(overlay);
      if (o.onCancel) o.onCancel();
    });
    actions.appendChild(cancelBtn);
  }

  // 확인 버튼
  const confirmBtn = document.createElement('button');
  confirmBtn.className = 'ol-modal-btn ol-modal-confirm' + (o.danger ? ' ol-modal-confirm-danger' : '');
  confirmBtn.textContent = o.confirmText;
  confirmBtn.addEventListener('click', function() {
    _closeModal(overlay);
    if (o.onConfirm) o.onConfirm();
  });
  actions.appendChild(confirmBtn);

  dialog.appendChild(titleEl);
  dialog.appendChild(msgEl);
  dialog.appendChild(actions);
  overlay.appendChild(dialog);
  root.appendChild(overlay);

  // 키보드: Esc = 취소, Enter = 확인
  const onKey = function(e) {
    if (e.key === 'Escape') {
      e.preventDefault();
      if (cancelBtn) cancelBtn.click();
      else confirmBtn.click();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      confirmBtn.click();
    }
  };
  document.addEventListener('keydown', onKey);
  overlay._cleanup = function() { document.removeEventListener('keydown', onKey); };

  // overlay 클릭 시 닫기 (취소 동작)
  overlay.addEventListener('click', function(e) {
    if (e.target === overlay && cancelBtn) {
      cancelBtn.click();
    }
  });

  _modalStack.push(overlay);

  // focus: 기본은 취소 (위험 동작은 사용자가 명시적으로 클릭해야)
  requestAnimationFrame(function() {
    if (o.defaultCancel && cancelBtn) cancelBtn.focus();
    else confirmBtn.focus();
  });
}

function _closeModal(overlay) {
  if (!overlay) return;
  if (overlay._cleanup) overlay._cleanup();
  const idx = _modalStack.indexOf(overlay);
  if (idx >= 0) _modalStack.splice(idx, 1);
  overlay.remove();
  if (_modalStack.length === 0 && _modalPrevFocus) {
    try { _modalPrevFocus.focus(); } catch(e) {}
    _modalPrevFocus = null;
  }
}
```

#### CSS (`src/styles/confirm-modal.css`)

```css
.ol-modal-overlay {
  position: fixed;
  inset: 0;
  background: hsl(0 0% 0% / 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;  /* toast(150)보다 위, 시스템 다이얼로그 대체 */
  padding: 1rem;
  animation: olModalFadeIn 150ms ease;
}

@keyframes olModalFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.ol-modal-dialog {
  background: hsl(var(--background));
  color: hsl(var(--foreground));
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  box-shadow: 0 20px 60px hsl(0 0% 0% / 0.25);
  max-width: 28rem;
  width: 100%;
  padding: 1.5rem;
  animation: olModalSlideIn 200ms cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes olModalSlideIn {
  from { transform: translateY(8px) scale(0.98); opacity: 0; }
  to { transform: translateY(0) scale(1); opacity: 1; }
}

.ol-modal-title {
  font-size: 1.05rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
  color: hsl(var(--foreground));
}

.ol-modal-danger .ol-modal-title {
  color: hsl(var(--destructive));
}

.ol-modal-message {
  font-size: 0.9rem;
  line-height: 1.6;
  color: hsl(var(--muted-foreground));
  margin-bottom: 1.5rem;
  white-space: pre-wrap;
}

.ol-modal-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.ol-modal-btn {
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
  border-radius: calc(var(--radius) - 2px);
  border: 1px solid hsl(var(--border));
  background: hsl(var(--background));
  color: hsl(var(--foreground));
  cursor: pointer;
  font-weight: 500;
  transition: background 120ms, border-color 120ms;
}

.ol-modal-btn:hover {
  background: hsl(var(--muted));
}

.ol-modal-btn:focus-visible {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}

.ol-modal-cancel {
  /* 기본 스타일 */
}

.ol-modal-confirm {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  border-color: hsl(var(--primary));
}

.ol-modal-confirm:hover {
  opacity: 0.9;
}

.ol-modal-confirm-danger {
  background: hsl(var(--destructive));
  color: hsl(var(--destructive-foreground));
  border-color: hsl(var(--destructive));
}

/* 모바일 */
@media (max-width: 640px) {
  .ol-modal-dialog {
    padding: 1.25rem;
  }
  .ol-modal-actions {
    flex-direction: column-reverse;  /* 위험 버튼이 아래로 */
  }
  .ol-modal-btn {
    width: 100%;
    padding: 0.625rem 1rem;
  }
}
```

#### 사용 예시 — 카드 삭제 흐름 (비움 요청 사항)

기존 코드:

```js
// components/card-modal.js
function _cmDeleteCard() {
  if (!editCard || !confirm("이 카드를 휴지통으로 이동하시겠습니까?")) return;
  // ...
}
```

신규 코드:

```js
async function _cmDeleteCard() {
  if (!editCard) return;
  const ok = await customConfirm({
    title: '카드를 휴지통으로 이동',
    message: '이 카드를 휴지통으로 이동하시겠습니까?\n\n휴지통에서 다시 복원할 수 있습니다.',
    confirmText: '휴지통으로 이동',
    cancelText: '취소',
    danger: true,
  });
  if (!ok) return;
  // 기존 로직 그대로
  const id = editCard.id;
  dispatch(deleteCard(id));
  // ...
}
```

휴지통 영구삭제(되돌릴 수 없음)는 더 강한 경고:

```js
async function _trashPurge(id) {
  const ok = await customConfirm({
    title: '⚠ 영구 삭제',
    message: '이 카드를 영구적으로 삭제합니다.\n\n이 작업은 되돌릴 수 없습니다.',
    confirmText: '영구 삭제',
    cancelText: '취소',
    danger: true,
    defaultCancel: true,  // 기본 focus는 취소 (안전)
  });
  if (!ok) return;
  dispatch(purgeCard(id));
}
```

#### beforeunload는 그대로 시스템 다이얼로그

**중요**: `installBeforeUnloadGuard()`의 새로고침 경고는 브라우저 시스템 다이얼로그입니다. 이는 보안 정책상 div 기반으로 대체할 수 없습니다 (악성 페이지가 이탈 막는 것을 방지). 비움 요청 사항 중 "브라우저 새로고침시 유실 경고"는 **이미 v0.7 Phase 1에서 시스템 다이얼로그로 구현 완료**되어 있습니다. 이 부분은 그대로 둡니다.

대신 가능한 보강은:

- **Dirty 상태 시각 표시** — 상단 헤더에 "● 변경됨" 같은 작은 표시. 사용자가 dirty 상태임을 명시적으로 인지하게.
- **저장 직후 토스트** — autosave 작동 시 "저장됨" 한 줄. 이미 작동 중인 autosave를 사용자에게 알리는 표시.

이건 **§8.4 ATLAS 정비 작업**에 포함합니다.

---

### 7.9 사라지는 UI (`components/reader/floating-ui.js`)

비움 결정 사항: BOOK은 몰입형 독서. 사이드바와 상단 메뉴가 평소 숨겨져 있다가 가장자리 호버(데스크탑) / 본문 탭(모바일)으로 호출됨.

#### 데스크탑 — 가장자리 호버 (재고 2-1 결정)

```js
// src/components/reader/floating-ui.js
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

### 8.4 ATLAS 정비 작업 — 시스템 confirm/alert 교체 + Dirty 시각 표시

**v1.1 신설**. Phase 8.0~ 진입 전 ATLAS 자체에 적용할 정비 작업. 비움이 요청한 두 가지 기능:

- "브라우저 새로고침시 업데이트한 내용 유실 경고창" → 이미 Phase 1에서 작동 중. 추가 시각 표시 신설.
- "카드 삭제 시에도 경고창" → 이미 작동 중. div 기반 커스텀 모달로 격상.
- "시스템 경고창이 아닌 div 태그 통한 경고창" → §7.8 confirm-modal 적용.

#### 8.4.1 9개 시스템 confirm/alert → customConfirm/customAlert 교체

§7.8 표에 명시된 9개 위치를 customConfirm/customAlert으로 교체. 작업 위치 요약:

```
core/storage.js     : alert("저장 실패: ...")              → customAlert
core/router.js      : confirm("변경 사항이 저장되지...")   → customConfirm
components/docview-inline.js (2개)                          → customConfirm
components/about.js (2개)                                    → customConfirm (영구삭제는 danger)
components/kanban.js : 컬럼 삭제                            → customConfirm (danger)
components/card-modal.js : 카드 삭제                        → customConfirm (danger)
components/bulk-select.js : 일괄 삭제                       → customConfirm (danger)
```

**중요**: customConfirm/customAlert은 Promise를 반환하므로, 호출처가 `async` 함수가 되거나 `.then()` 패턴을 사용해야 한다. 동기 confirm을 사용하던 코드는 흐름이 약간 달라진다:

```js
// ❌ 기존 (동기)
if (!confirm('정말 삭제?')) return;
doDelete();

// ✅ 신규 (비동기)
const ok = await customConfirm({ title: '삭제 확인', message: '정말 삭제?' });
if (!ok) return;
doDelete();
```

#### 8.4.2 Dirty 상태 시각 표시

현재 `isDirty()`는 작동하지만, UI에 표시되지 않음. 사용자가 변경 사항이 저장되지 않았음을 알 방법이 없음.

**추가 UI**:

- 헤더 우측에 작은 인디케이터: dirty일 때 `● 변경됨` 표시, clean일 때 `✓ 저장됨` (5초 후 fade out)
- `markDirty`/`markClean` 호출 시 자동 갱신

```js
// src/components/shared/dirty-indicator.js (★신규 shared 모듈)
// dirty 상태를 헤더에 시각 표시

let _indicatorEl = null;
let _fadeTimer = null;

function ensureDirtyIndicator() {
  if (_indicatorEl) return _indicatorEl;
  const header = document.querySelector('.app-header, header') || document.body;
  const el = document.createElement('div');
  el.className = 'dirty-indicator';
  el.setAttribute('aria-live', 'polite');
  header.appendChild(el);
  _indicatorEl = el;
  return el;
}

function renderDirtyIndicator() {
  const el = ensureDirtyIndicator();
  const dirty = isDirty();
  if (dirty) {
    el.className = 'dirty-indicator dirty';
    el.textContent = '● 변경됨';
    if (_fadeTimer) clearTimeout(_fadeTimer);
  } else {
    el.className = 'dirty-indicator clean';
    el.textContent = '✓ 저장됨';
    if (_fadeTimer) clearTimeout(_fadeTimer);
    _fadeTimer = setTimeout(() => {
      el.className = 'dirty-indicator hidden';
    }, 5000);
  }
}

subscribe('dirty-indicator', renderDirtyIndicator);

// markDirty / markClean 호출 시 자동 queueRender
// dirty.js 안에서 queueRender('dirty-indicator') 호출 추가
```

dirty.js의 markDirty/markClean에 1줄 추가:

```js
function markDirty() {
  // 기존 로직
  queueRender('dirty-indicator');  // ★추가
}

function markClean() {
  // 기존 로직
  queueRender('dirty-indicator');  // ★추가
}
```

#### CSS (`styles/dirty-indicator.css`)

```css
.dirty-indicator {
  font-size: 0.75rem;
  padding: 0.25rem 0.625rem;
  border-radius: 9999px;
  transition: opacity 200ms, background 200ms;
  user-select: none;
}

.dirty-indicator.dirty {
  background: hsl(38 90% 92%);
  color: hsl(38 60% 30%);
}

.dirty-indicator.clean {
  background: hsl(140 60% 92%);
  color: hsl(140 40% 30%);
  opacity: 0.7;
}

.dirty-indicator.hidden {
  opacity: 0;
  pointer-events: none;
}

:root.dark .dirty-indicator.dirty {
  background: hsl(38 30% 20%);
  color: hsl(38 80% 70%);
}
:root.dark .dirty-indicator.clean {
  background: hsl(140 20% 18%);
  color: hsl(140 50% 70%);
}
```

#### 8.4.3 beforeunload는 그대로

비움 요청 사항 중 "브라우저 새로고침시 유실 경고"는 이미 Phase 1에서 시스템 다이얼로그로 작동 중. 보안 정책상 div 기반으로 대체 불가. 그대로 둔다.

대신 dirty 인디케이터가 시각적으로 알려주므로, 사용자가 새로고침 전에 인지할 수 있다.

#### 8.4.4 정비 작업 산출물

Phase 8.0 시작 전 또는 Phase 8.0 첫 세션에 다음을 완료:

|작업|산출물|
|---|---|
|confirm-modal.js + CSS|`components/shared/confirm-modal.js`, `styles/confirm-modal.css`|
|dirty-indicator.js + CSS|`components/shared/dirty-indicator.js`, `styles/dirty-indicator.css`|
|9개 confirm/alert 교체|위 표의 9개 파일 수정|
|dirty.js 갱신|markDirty/markClean에 queueRender 추가|
|build.mjs 갱신|JS_FILES에 신규 파일 추가|

이 정비가 끝나면 ATLAS UI는 일관된 시각 언어 + 명확한 dirty 표시를 가진다. 그 후에 듀얼 런타임 분기 작업에 들어간다.

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

### Phase 7.x — ATLAS 정비 (★v1.1 신설, 2~3일)

듀얼 런타임 분기 진입 전 ATLAS 자체 정비. §8.4 작업 내용 그대로:

|#|작업|산출물|
|---|---|---|
|7.x.1|`confirm-modal.js` + CSS 작성|shared 모듈|
|7.x.2|`dirty-indicator.js` + CSS 작성|shared 모듈|
|7.x.3|`dirty.js`의 markDirty/markClean에 queueRender 추가|1줄 패치|
|7.x.4|9개 시스템 confirm/alert → customConfirm/customAlert 교체|7개 파일 수정|
|7.x.5|`build.mjs` JS_FILES에 신규 파일 추가|빌드 갱신|
|7.x.6|회귀 테스트: 모든 confirm 흐름이 div 기반으로 작동|manual QA|

**진입 조건**: Phase 2 완료, 즉 `v0.7-phase2-complete` 태그 시점. **완료 조건**: `grep -E "(confirm|alert)\(" src/` 결과 0건 (customConfirm/customAlert만 남음).

### Phase 8.0 — ES modules 전환 + 빌드 구조 재편 (★v1.2 확장, 4~6일)

**핵심 작업**: concat 방식 → ES modules 전환. 동시에 듀얼 런타임 분기를 위한 디렉토리 재편.

#### 작업 흐름 (세션 분할)

**세션 1: core/ + actions/ ES modules 변환** (1~2일)

- `src/core/*.js` 각 파일에 export 키워드 추가
- 다른 파일을 사용하는 곳에 import 추가
- `src/actions/*.js` 동일 적용
- 기존 글로벌 함수 호출(`dispatch`, `getState` 등)을 import로 변환
- 검증: ATLAS 부팅 + v0.6 시나리오 7종 작동

**세션 2: components/ 재구성** (1~2일)

- `src/components/`를 `shared/`, `reader/`, `author/` 하위 디렉토리로 이동 (§3.8)
- 각 컴포넌트 파일에 export 추가 + 의존성 import 추가
- 부수효과 호출(`subscribe('kanban', renderKanban)` 등)은 파일 끝에 유지
- 검증: 모든 view 정상 렌더링

**세션 3: main.js + esbuild 도입** (1일)

- `src/main.js` 생성 (§3.3.2)
- `/*! AUTHOR_BUNDLE_START */` 마커 삽입
- `build/build.mjs`를 esbuild bundle 호출 방식으로 전환 (§3.3.1)
- esbuild `legalComments: 'inline'` 확인
- 빌드 후 산출물의 마커 잔존 grep 확인

**세션 4: 모드 감지 + 부팅 분기** (0.5~1일)

- `detectMode()` (§3.6)
- `bootAtlas()` / `bootBook()` (§3.6)
- 부수효과 subscribe로 author/reader view 자동 등록
- 검증: ATLAS 모드로 v0.7-phase7x-complete와 기능 동등성

**세션 5: 검증 + 정리** (0.5~1일)

- ES modules 전환 빠진 파일 grep으로 검출
- `core/history.js` 등 사용 안 하는 파일 정리
- import 그래프 시각화 (옵션, 디버깅용)
- git tag `v0.8.0-phase8.0-complete`

#### 진입 조건

- Phase 7.x 완료 (`v0.7-phase7x-complete` 태그)
- 모든 시스템 confirm/alert이 customConfirm/customAlert으로 교체됨

#### 완료 조건

- ATLAS 모드 부팅 + v0.7-phase7x와 100% 기능 동등
- 빌드 산출물에 `/*! AUTHOR_BUNDLE_START */` `/*! AUTHOR_BUNDLE_END */` 마커 존재
- 모든 파일이 ES modules (export/import 명시)
- `grep -L "import\\|export" src/**/*.js` 결과 0건 (모든 .js가 ES module)
- esbuild 빌드 시간 1초 이내

### Phase 8.1 — Reader Manifest + schema v8 (1~2일)

- schema v7 → v8 마이그레이션
- S.book.manifest 데이터 모델
- ATLAS 부팅 시 manifest 자동 생성 (기존 데이터에서)

### Phase 8.2 — 커버페이지 (reader) + 편집기 (author) (3~4일)

- `components/reader/cover-page.js`
- `components/author/cover-editor.js`
- ATLAS 사이드바에 "표지 편집" 추가
- 미리보기 실시간 갱신

### Phase 8.3 — exportBook() (2~3일)

- `components/author/export-book.js`
- 메모리 자기참조 정규식 패턴 적용 (§6.3)
- ATLAS 사이드바/ABOUT에 "BOOK으로 배포" 버튼
- 검증: 작은 데이터로 BOOK 생성 → 더블클릭 → 커버 표시

### Phase 8.4 — BOOK 기본 작동 (3~4일)

- BOOK 모드 부팅 시퀀스
- BOOK 사라지는 UI (`floating-ui.js`, 모바일 토글)
- BOOK typography (`reader-typography.css`)
- 카드보드 readonly + 인덱스 정렬
- 카드 클릭 즉시 문서뷰
- 검증: BOOK에서 모든 콘텐츠 읽기 가능

### Phase 8.5 — 진행률 + 책갈피 (2~3일)

- `components/reader/progress.js`
- `components/reader/bookmark.js`
- 커버페이지 이어읽기 버튼
- 문서뷰 하단 진행 바
- 사이드바 책갈피 섹션

### Phase 8.6 — 본문 내부 링크 [[id]] (2일)

- `core/markdown.js` 파서 확장 (`[[id|label]]` 패턴)
- `components/reader/internal-link.js` 클릭 핸들러 (BOOK)
- `components/author/internal-link-completer.js` 자동완성 (ATLAS)

### Phase 8.7 — 콘텐츠 통계 + sepia 모드 (1~2일)

- `components/reader/stats.js`
- BOOK ABOUT 페이지에 통계 표시
- `styles/sepia.css` + 테마 토글 3단계 (light → dark → sepia)

### Phase 8.8 — 마무리 (2일)

- 모든 분기 게이트 통과 확인
- ATLAS에서 BOOK export → 독립 사용 시나리오
- 첫 BOOK 콘텐츠 시연 (OL 붓다스토리 일부)

**총 예상**: 약 22~32일 (4~6.5주) — Phase 7.x ATLAS 정비(2~3일) + Phase 8.0 ES modules 전환(4~6일) 포함.

---

## 11. 검증 게이트

각 Phase 종료 시 충족해야 할 조건.

|Gate|조건|
|---|---|
|**Phase 7.x** (★v1.1)|시스템 confirm/alert 0건 (`grep` 결과). dirty 인디케이터가 변경 시 1초 안에 갱신됨.|
|**Phase 8.0**|ATLAS 모드로 v0.7-phase7x와 100% 기능 동등. **모든 .js 파일이 ES modules**. AUTHOR_BUNDLE 마커가 빌드 산출물에 존재. esbuild 빌드 1초 이내.|
|**Phase 8.1**|schema v7 → v8 마이그레이션 무손실. 기존 사용자가 ATLAS를 다시 열어도 콘텐츠 그대로 + manifest 자동 생성됨.|
|**Phase 8.2**|커버 편집 → 미리보기 실시간 갱신 (입력 후 100ms 안에 반영).|
|**Phase 8.3**|exportBook() 결과 더블클릭 → BOOK 부팅. AUTHOR_BUNDLE 영역이 산출물에서 사라짐. 데이터 inline 작동.|
|**Phase 8.4**|BOOK에서 모든 콘텐츠 읽기 가능. 사라지는 UI 작동 (데스크탑 가장자리 호버 + 모바일 본문 탭).|
|**Phase 8.5**|진행률 보존: BOOK 새로고침 후에도 이어읽기 작동. 책갈피 토글 작동.|
|**Phase 8.6**|`[[card-id]]` 클릭 시 해당 카드 문서뷰로 이동. ATLAS의 `[[` 자동완성 작동. 깨진 ID는 회색 표시.|
|**Phase 8.7**|sepia 모드 토글 작동 (light → dark → sepia 순환). 통계 정확 (수동 카운트와 일치).|
|**Phase 8.8**|OL 붓다스토리 일부를 실제 BOOK으로 만들어 시연. 외부 사용자 1명 이상 받아 사용.|

---

## 12. 위험 요소 및 대응

|위험|등급|대응|
|---|---|---|
|ES modules 전환 중 import 누락으로 ReferenceError|🔴 (Phase 8.0)|세션별로 작은 단위 변환 + 매번 빌드 검증. 한 번에 모든 파일 변환하지 말 것|
|ES modules 전환 시 부수효과 순서 깨짐|🔴 (Phase 8.0)|`subscribe`, `registerReducer` 같은 부수효과는 파일 끝에 두고, main.js의 import 순서가 평가 순서를 결정함을 명시|
|esbuild가 `/*! */` 주석을 제거|🔴 (Phase 8.0)|`legalComments: 'inline'` 옵션 명시. 빌드 후 grep으로 마커 잔존 확인|
|AUTHOR_BUNDLE 마커가 minify로 소실|🔴|`minify: false` 또는 `legalComments` 옵션. 빌드 후 grep으로 마커 잔존 확인|
|`__STATIC_HTML__` 캡처 시점 깨짐|🔴|메모리 패턴 그대로 적용. **이미 작동 중**이므로 그대로 유지|
|`__LOADED_DATA_B64__` 자기참조 정규식|🔴|`'__LOADED' + '_DATA_B64__'` 분리 패턴 강제 (§6.3)|
|BOOK 모드에서 author 함수 호출 시도|🟡|ES modules 환경에서는 author 모듈이 import 안 되면 함수 자체가 존재 안 함. `listViews().includes('kanban')` 가드로 확인|
|진행률 localStorage 키 충돌|🟡|bookId에 ORIGIN.site + title + version 조합|
|sepia 모드와 마크다운 코드블록 색상 충돌|🟡|sepia.css에 코드블록 색상도 명시|
|BOOK의 `[[broken-id]]` 처리|🟡|카드 없으면 회색 + 점선 표시, 클릭 무반응|
|모바일 본문 탭 vs 링크 클릭 충돌|🟡|`event.target.closest('a, button, ...)`로 가드|
|커버 이미지 base64로 인해 HTML 크기 급증|🟡|권장 해상도 명시(480x672 등), 사용자에게 경고|
|customConfirm 비동기화로 인한 흐름 변경|🟡 (Phase 7.x)|호출처를 async로 변경. 흐름이 단순하면 .then()|
|dirty 인디케이터의 무한 재렌더|🟡 (Phase 7.x)|markDirty→queueRender→render→state 변경 없음. 안전. 단 markDirty 안에서 state 변경 금지|
|import 그래프에서 빠진 파일이 빌드에 안 들어감|🟡 (Phase 8.0)|Phase 8.0 검증 게이트에 grep으로 모든 .js 파일이 import 그래프에 포함됐는지 확인|
|트리쉐이킹으로 부수효과 파일이 제거됨|🟡 (Phase 8.0)|부수효과 있는 파일은 `import './subscribe-only.js'` 형태로 명시. esbuild는 이런 import를 보존|

---

## 12.5 v1.0 / v1.1 / v1.2 핵심 차이 요약

|항목|v1.0|v1.1|v1.2 (★현재)|
|---|---|---|---|
|**소스 작성**|ES modules|concat (전역 함수)|**ES modules**|
|**빌드 변환**|esbuild 두 번들 분리|단순 concat|**esbuild → 단일 IIFE**|
|**모드 감지**|`window.OL.Author` 존재|`typeof openCardModal === 'function'`|**`listViews().includes('kanban')`**|
|**AUTHOR 마커**|(없음, 번들 분리)|가짜 문자열 마커|**`/*! AUTHOR_BUNDLE_START */`**|
|**데이터 필드명**|`S.cols`|`S.columns`|`S.columns` (그대로)|
|**userData 위치**|별도|`S.userData.status[id]`|그대로|
|**import/export**|ES modules|전역 scope 공유 (concat)|**ES modules**|
|**시스템 confirm/alert**|(다루지 않음)|§7.8 customConfirm + §8.4 9곳 교체|그대로|
|**dirty 시각 표시**|(다루지 않음)|§8.4 dirty-indicator 신설|그대로|
|**Phase 7.x**|없음|ATLAS 정비 단계 신설|그대로|
|**Phase 8.0 작업량**|(없음)|2~3일 (디렉토리 재편)|**4~6일 (ES modules + 재편)**|
|**총 일수**|18~26일|20~29일|**22~32일**|
|**빌드 시 의존성 누락 검출**|가능|불가 (런타임에 발견)|**가능 (빌드 에러)**|
|**트리쉐이킹**|가능|불가|**가능**|

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

1. **본 설계서(v1.2) 검토 후 확정 선언.**
2. **Phase 7.x 작업지시서 작성 요청** (ATLAS 정비). `v0.7-phase2-complete` 태그에서 출발.
3. Phase 7.x 착수 — 비교적 안전. concat 방식 그대로, confirm-modal + dirty-indicator + 9개 confirm 교체.
4. Phase 7.x 완료 후 `v0.7-phase7x-complete` 태그. ATLAS UI 일관성 검증.
5. **Phase 8.0 작업지시서 작성** — ★v1.2의 핵심 변환점. ES modules 전면 전환 + 듀얼 런타임 분기 디렉토리 재편 동시 진행. 5세션 분할(§Phase 8.0 본문).
6. Phase 8.0 완료 시점에 `v0.7-phase7x-complete`와 ATLAS 기능 동등 확인 + 빌드 산출물에 AUTHOR_BUNDLE 마커 잔존 확인 — 이게 후속 진행의 게이트.
7. 이후 Phase 8.1~8.8 순차 진행.

**Phase 7.x를 먼저 하는 이유** (Phase 8.0 ES modules 전환에 그대로 흡수하지 않는 이유):

- Phase 7.x는 concat 방식 그대로에서 가능한 작은 단위 작업
- Phase 8.0의 ES modules 전환은 위험도가 높음 — 한 번에 너무 많이 바꾸지 말 것
- Phase 7.x 완료 시점에 ATLAS UI 일관성이 한 번 검증되고, 그 상태에서 ES modules 전환만 별도 작업으로 진행하면 회귀 검출이 용이

각 Phase는 Phase 0~2의 작업지시서 형식을 그대로 따른다:

- 권한 선언 블록 최상단 (메모리 정책)
- 세션 분할
- 검증 게이트
- 세션마다 git commit + Phase 끝에 tag

---

## 부록 B — 메모리 원칙 점검

작성 시점에 본 설계서가 메모리 원칙과 정합한지 점검:

|원칙|본 설계와의 정합성|
|---|---|
|OL은 불교콘텐츠 연기망의 그물코|✅ 강화. 본문 내부 링크 [[id]]가 연기망 직접 구현|
|본질은 불교콘텐츠|✅ BOOK 분리로 콘텐츠 전달이 중심|
|받은 사람이 자유롭게 수정·배포|✅ ATLAS는 그대로. BOOK은 출판물이라는 다른 형식|
|ORIGIN 하드코딩|✅ Reader Manifest가 ORIGIN을 자동 복제|
|ES modules dev, 단일 HTML dist|✅ **v1.2에서 정확히 회복**. Phase 8.0에서 ES modules 전면 전환 → esbuild가 단일 IIFE로 번들|
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

## 부록 D — v1.2 갱신 정합성 노트

### D.1 Phase 2 완료 코드와 일치하는 점

Phase 2 완료 코드(`ol-atlas.html` 약 5800줄)를 분석한 결과, 본 v1.1 설계는 다음과 일치한다:

- ✅ `ORIGIN`: `{author:'비움', site:'olbit.org', copyright:'Copyright © 2026 biwoom', license:'CC BY-SA 4.0', tool:'OL · ATLAS · Weaving the Wisdom'}`
- ✅ S 데이터 모델: `S.cards`, `S.columns`, `S.userData.status`, `S.trash`, `S.nextColId`, `S.nextCardId`, `S.meta`, `S.settings`
- ✅ Schema v7 마이그레이션 작동 (v6 → v7, `ol_backup_v6` 자동 저장)
- ✅ Proxy strict mode: 직접 mutation 시 에러
- ✅ Action Layer 액션: CARD_CREATE/UPDATE/DELETE/RESTORE/MOVE/PURGE/PURGE_ALL/BULK__, STATUS_SET/CLEAR/BULK, COLUMN__, VIEW_CHANGE, BOARD_WIDTH_SET, META_TOGGLE_SET, SIDEBAR_OPEN_SET, SETTINGS_UPDATE, THEME_SET, META_UPDATE, IMPORT_MERGE
- ✅ dirty/autosave/beforeunload 작동
- ✅ `__STATIC_HTML__` 캡처 + `__LOADED_DATA_B64__` 마커 작동

### D.2 v0.6/v0.7 자산 중 v1.2에서 사용 안 하는 것

- ❌ `core/history.js` — v0.6 잔존, 사용 안 됨. Phase 8.0에서 JS_FILES에서 제외.
- ❌ `ol_v1` legacy storage key — 폴백으로 남아있지만 호출되지 않음.
- ❌ `cardModalPrevFocus` 등 일부 UI 상태 변수 — 그대로 둠.

### D.3 v1.2에서 처음 명시한 데이터 모델 추가

```js
S.book = {                       // schema v8
  manifest: {
    id, title, subtitle, author, series, version, publishedAt,
    cover: { image, backgroundColor },
    entry: { view, actions, startTarget },
    ordering: { cards },
    display: { showColumns, showTags, showProgress, showBookmarks },
    license, copyright,
  }
}
```

`S.book`이 없는 기존 사용자의 ATLAS는 schema v7 → v8 마이그레이션에서 자동 생성된다. 마이그레이션은 메모리 패턴(`ol_backup_v7` 자동 저장 → migrate) 그대로 따른다.

### D.4 v1.2 적용 후 보존되어야 하는 메모리 원칙

|원칙|v1.2 적용 후 상태|
|---|---|
|단일 HTML 산출물|✅ esbuild가 ES modules → 단일 IIFE 번들로 변환 (외부 의존성 0)|
|받은 사람 자유 수정·배포|✅ ATLAS는 그대로. BOOK은 출판 형식이라는 다른 자산.|
|ORIGIN 하드코딩|✅ Reader Manifest가 ORIGIN 복제. ORIGIN은 코드에 그대로|
|ES modules dev / 단일 HTML dist|✅ **Phase 8.0에서 전환 완료 예정**. 메모리 #2 원래 의도 회복|
|IndexedDB/PWA/Electron 미채택|✅ 그대로|
|카드 스키마 관계 필드|✅ Phase 8.6 `[[id]]` 파서가 관계의 첫 구현|

✅ v1.2 핵심 — 메모리 #2의 "소스는 ES modules로 분할 가능한 dev 형식, 빌드 산출물은 단일 HTML(dist)" 원칙이 Phase 8.0 완료 시점에 정확히 달성된다. v1.1까지의 concat 방식 우회는 폐기.

### D.5 v1.0 → v1.1 → v1.2 진화 요약

```
v1.0 (2026-05-22)
  ├─ 동료 A의 권장안 채택 (Dual Bundle, 두 script 분리)
  └─ 가정: ES modules

v1.1 (2026-05-23 아침)
  ├─ 실제 Phase 2 완료 코드 확인 → concat 방식이었음
  ├─ 빌드 모델을 단일 IIFE + 마커 보존으로 수정
  ├─ Phase 7.x 신설 (confirm-modal, dirty-indicator)
  └─ 메모리 #2 정합성 ⚠ 표시

v1.2 (2026-05-23 결정)
  ├─ 비움 결정: ES modules 전면 전환 (A안)
  ├─ Phase 8.0에 ES modules 전환 작업 통합
  ├─ /*! AUTHOR_BUNDLE_START */ 마커 보존 패턴
  ├─ 메모리 #2 원래 의도 회복
  └─ 총 일정 22~32일
```

---

**작성**: Claude (with biwoom) **버전**: v1.2 (ES modules 전면 전환 반영) **상태**: 설계 확정. **Phase 7.x 작업지시서** 작성 단계로 진입 가능. **다음 문서**: Phase 7.x 작업지시서 (ATLAS 정비 — confirm-modal + dirty-indicator + 9개 confirm 교체). Phase 7.x 완료 후 Phase 8.0 작업지시서(ES modules 전환 + 빌드 구조 재편).