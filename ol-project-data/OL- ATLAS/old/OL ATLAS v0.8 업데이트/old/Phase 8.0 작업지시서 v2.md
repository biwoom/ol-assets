# Phase 8.0 작업지시서 v2 — Claude CLI 작업용

**대상**: OL ATLAS v0.7 Phase 8.0 — ES modules 전환 + 빌드 구조 재편 **작업 환경**: 로컬 PC + Claude CLI **선행 문서**: `OL_듀얼_런타임_설계서_v1_2.md`, Phase 7.x 완료 **진입 조건**: `v0.7-phase7x-complete` 태그 시점 **Phase 8.0 목표 일수**: 4~6일 (5세션) **위험 등급**: 🔴 높음 — 빌드 파이프라인 전체 교체. 기능 동등성이 게이트.

---

## ⚡ 권한 선언 — AI 에이전트 전용 (세션 시작 시 1회 적용)

**이하 모든 권한을 사전 일괄 승인한다. 작업 중 개별 확인 요청 금지.**

### ✅ 전면 허용 — 작업 폴더 내 모든 터미널 명령어

작업 폴더(`ol-atlas/`) 및 모든 하위 경로에서 묻지 않고 즉시 실행:

```
파일 시스템
  cat, head, tail, grep, find, wc, diff      (읽기)
  write, create, str_replace, cp, mv, mkdir  (쓰기/생성/이동)
  echo "..." > file, touch file
  rm <단일 파일>

셸 명령
  bash/sh 스크립트, 파이프, 리다이렉트, &&, ||, ; 체인

Node / npm
  node <script.js>, node --check <file.js>
  npm run *  (build, dev, test 등)
  npx *

Python
  python3 <script.py>

Git
  git status, git diff, git log, git show
  git add, git commit, git tag
  git stash, git stash pop
  git branch (조회/생성)

빌드 도구
  esbuild 직접 실행, node build/build.mjs
```

### ❌ 별도 승인 필요 (실행 전 반드시 사용자에게 확인)

```
rm -rf <디렉토리>   폴더 전체 삭제
git push            원격 저장소 반영
git reset --hard    작업 내용 파괴
git clean -fd       추적 안 된 파일 전체 삭제
npm install <새패키지>  새 외부 패키지 추가
작업 폴더(ol-atlas/) 밖 경로 접근
네트워크 요청 (fetch, curl, wget 등)
시스템 설정 변경
```

### 작업 진행 원칙

- 묻지 말고 진행. 의심스러우면 cat/grep으로 읽기 먼저.
- 에러 발생 시 즉시 중단, 에러 전문 보고.
- **세션마다 빌드 검증 통과 후** git commit.
- 한 세션에 여러 파일을 한꺼번에 바꾸지 말 것. 파일 하나 바꾸면 빌드 확인.

---

## 0. Phase 8.0 개요

### 0.1 Phase 8.0의 임무

현재 `build.mjs`는 `JS_FILES` 배열에 명시한 순서대로 파일을 concat하고 하나의 IIFE로 감싸는 방식이다. Phase 8.0에서는 이것을:

1. **각 소스 파일에 `export` / `import` 추가** — 명시적 의존성
2. **`src/main.js` 엔트리 파일 작성** — import 그래프의 루트
3. **`build/build.mjs`를 esbuild bundle 방식으로 전환** — esbuild가 import 그래프를 따라 단일 IIFE 번들 생성
4. **`/*! AUTHOR_BUNDLE_START */` 마커 삽입** — 향후 `exportBook()`이 제거할 경계
5. **디렉토리 재편** — `components/{shared,author,reader}/` 구조로 이동

완료 후 사용자는 변화를 느끼지 못한다. 빌드 산출물(`dist/ol-atlas.html`)은 기능적으로 `v0.7-phase7x-complete`와 100% 동등해야 한다.

### 0.2 Phase 8.0이 변경하지 않는 것

- UI 동작, 데이터 모델, Action Layer, reducer — 전혀 변경 없음
- 빌드 산출물의 기능, 데이터 흐름 — 전혀 변경 없음
- CSS, HTML 셸 — 전혀 변경 없음

### 0.3 Phase 8.0 완료 시점의 상태

```
src/
├── main.js                         ★ 신규: ES modules 엔트리
├── core/                           (파일 그대로, export 추가)
├── actions/                        (파일 그대로, export 추가)
├── ui/                             (confirm-modal 이동됨 — §1.4 참조)
│   ├── custom-select.js            (기존)
│   ├── confirm-modal.js            ★ Phase 7.x에서 이동 (components/shared/ → ui/)
│   └── confirm-modal.css           ★ Phase 7.x에서 이동
├── components/
│   ├── shared/                     (Phase 7.x에서 생성됨, confirm-modal은 이동됨)
│   │   ├── dirty-indicator.js/css  (그대로 유지)
│   │   ├── docview.js
│   │   ├── sidebar.js
│   │   ├── about.js
│   │   └── toc.js
│   ├── author/                     ★ 신규: 기존 컴포넌트 이동
│   │   ├── home.js
│   │   ├── kanban.js
│   │   ├── cardgrid.js
│   │   ├── listview.js
│   │   ├── card-modal.js
│   │   ├── docview-inline.js
│   │   ├── md-editor.js
│   │   ├── bulk-select.js
│   │   └── color-picker.js
│   └── reader/                     ★ 신규: Phase 8.x에서 추가될 위치
├── data/
│   ├── init.js
│   └── search/search.js
├── styles/                         (변경 없음)
└── ui/custom-select.js             → 위 ui/ 디렉토리로 통합됨

build/build.mjs                     ★ esbuild bundle 방식으로 교체
```

---

## 1. 실제 코드 분석 결과 (Phase 8.0 작업의 기반)

이 섹션은 Phase 2 완료 코드를 직접 분석해서 얻은 정보다. 작업 전 반드시 숙지할 것.

### 1.1 번들 구조와 파일 경계

빌드 산출물을 분석한 결과, 현재 파일들의 **대략적인 위치와 크기**:

|구간|원본 파일|핵심 함수|
|---|---|---|
|0~598|`src/core/dev.js`|`devLog`, `devAssert`, `devTime`, `devGroup`|
|598~2404|`src/core/store.js`|`storeInit`, `getState`, `applyState`, `subscribe`, `getSubscriber`, `listViews`|
|2404~3056|`src/core/schema.js`|`migrate`, `getSchemaVersion`|
|3056~4088|`src/core/storage.js`|`storageSave`, `storageLoad`, `STORAGE_KEY`|
|4088~5067|`src/core/dirty.js`|`markDirty`, `markClean`, `isDirty`, `_scheduleAutosave`, `installBeforeUnloadGuard`|
|5067~5772|`src/core/action.js`|`registerReducer`, `dispatch`|
|5772~18421|`src/core/tag-parser.js` + `tag-filter.js` + `constants.js` + `utils.js`|`parseTag`, `buildPrefixIndex`, `ORIGIN`, `escapeHTML`, `toast`, `slugFilename`|
|18421~19772|`src/core/body-helpers.js`|body image/token helpers|
|19772~22564|`src/core/markdown.js`|`parseMarkdown`, `parseInline`, `stripMarkdown`|
|22564~27592|`src/core/normalize.js` + `state.js`|`normalizeCard`, `normalizeState`, `S` Proxy|
|27592~35852|`src/actions/*.js`|`cardReducer`, `columnReducer`, `viewReducer`, `settingsReducer`|
|35852~41351|`src/core/theme.js` + `router.js` + `events.js`|`setTheme`, `switchView`, `routeFromHash`|
|41351~63253|`src/components/docview.js` + `docview-inline.js` + `toc.js`|`renderDocumentView`|
|63253~70112|`src/components/about.js`|`renderAbout`, `renderTrash`|
|70112~75608|`src/components/home.js`|`renderHome`|
|75608~86738|`src/components/sidebar.js`|`renderSidebar`|
|86738~157439|`src/components/kanban.js` + `cardgrid.js` + `listview.js` + `card-modal.js` + `bulk-select.js` + `color-picker.js` + `md-editor.js`|`renderKanban`, `renderCardGrid`, `renderListView`|
|157439~177593|`src/data/search/search.js`|`runSearch`, `closeSearch`|
|177593~끝|`src/data/init.js` (boot IIFE)|boot 진입점|

### 1.2 subscribe 등록 뷰 목록

Phase 7.x 완료 기준 **9개** 뷰가 subscribe 등록됨:

```
'docview', 'about', 'trash', 'home', 'sidebar', 'kanban', 'cards', 'list',
'dirty-indicator'   ← Phase 7.x에서 dirty-indicator.js가 추가
```

### 1.3 파일별 필요 import (분석 결과)

실제 코드 분석으로 도출한 각 파일의 import 필요 목록:

```
src/core/store.js          ← devLog, devAssert  (from dev.js)
src/core/schema.js         ← devLog, devAssert, getState, applyState  (from dev+store)
src/core/storage.js        ← devLog, getState, customAlert  ← Phase 7.x 추가
src/core/dirty.js          ← devLog, getState, storageSave, queueRender
src/core/action.js         ← devLog, devAssert, getState, applyState, markDirty, queueRender
src/core/tag-parser.js     ← devLog, getState (직접 S 접근 가능성 있음 — 검토 필요)
src/core/tag-filter.js     ← getState, dispatch, queueRender
src/core/constants.js      ← (없음 — 순수 상수)
src/core/utils.js          ← (없음 또는 devLog만)
src/core/markdown.js       ← escapeHTML  (from utils.js)
src/core/normalize.js      ← devLog, getState (S Proxy 정의 위치)
src/core/state.js          ← getState, devLog (S Proxy if separate)
src/core/router.js         ← devLog, switchView, queueRender, getState, dispatch, customConfirm  ← Phase 7.x 추가
src/core/theme.js          ← devLog, queueRender
src/actions/card-actions.js   ← devLog, normalizeCard, registerReducer, getState
src/actions/column-actions.js ← devLog, registerReducer, getState
src/actions/view-actions.js   ← devLog, registerReducer, getState
src/actions/settings-actions.js ← devLog, registerReducer, getState
src/actions/export-import.js  ← devLog, dispatch, getState, normalizeCard, normalizeState, migrate, S
src/components/docview.js     ← subscribe, dispatch, escapeHTML, parseMarkdown, queueRender, slugFilename, toast
src/components/about.js       ← subscribe, dispatch, toast, S, customConfirm, customAlert
src/components/home.js        ← subscribe, escapeHTML, S
src/components/sidebar.js     ← subscribe, buildPrefixIndex, escapeHTML, queueRender, S, dispatch
src/components/kanban.js      ← subscribe, dispatch, escapeHTML, parseMarkdown, queueRender, S, customConfirm
src/components/cardgrid.js    ← subscribe, dispatch, escapeHTML, S
src/components/listview.js    ← subscribe, dispatch, escapeHTML, S
src/components/card-modal.js  ← dispatch, escapeHTML, parseMarkdown, S, customConfirm
src/components/bulk-select.js ← dispatch, S, customConfirm
src/data/search/search.js     ← escapeHTML, queueRender, S
src/data/init.js              ← devLog, storageLoad, migrate, normalizeState, bootState, queueRender, flushNow, routeFromHash, switchView
```

> **주의**: 이 목록은 번들 분석 기반 추정이다. 실제 작업 시 각 파일을 열어 확인하고 보정해야 한다.

### 1.4 아키텍처 결정 — confirm-modal.js 위치 (세션 1 시작 전 필수)

Phase 7.x에서 `confirm-modal.js`를 `src/components/shared/`에 작성했으나, ES modules 전환 시 다음 계층 역전이 발생한다:

```
core/storage.js  ──import──▶  components/shared/confirm-modal.js  ← 상향 의존성
core/router.js   ──import──▶  components/shared/confirm-modal.js  ← 상향 의존성
```

순환 의존성은 아니므로 빌드는 통과하지만, 계층 규칙을 어긴다.

**채택 결정: `src/ui/`로 이동 (A안)**

근거:

- `confirm-modal.js`는 `getState`, `dispatch`, `S` 등 아무것도 사용하지 않는 순수 DOM 유틸
- `custom-select.js`가 이미 `src/ui/`에 있어 성격이 동일
- `src/ui/`는 `core/`에서 import 가능한 계층 (역방향 아님)
- Phase 8.3의 `exportBook()` 때 BOOK 산출물 포함/제외 결정이 더 명확해짐

이동 결과 import 경로:

```js
// src/core/storage.js
import { customAlert } from '../ui/confirm-modal.js';   ✅ 정방향

// src/core/router.js
import { customConfirm } from '../ui/confirm-modal.js'; ✅ 정방향

// src/components/author/kanban.js 등
import { customConfirm } from '../../ui/confirm-modal.js';
```

**세션 1 사전 작업에 이동 작업이 추가됨** (§2.1 참조)

### 1.5 현재 `render-queue.js`가 없는 이유

분석 결과 `queueRender`와 `_renderFlush`는 번들에서 `storeInit` 직후에 정의된다. 이는 현재 소스에서 `src/core/render-queue.js`의 내용이 `src/core/store.js` 또는 별도 파일에 있을 수 있다. **세션 1에서 실제 파일을 열어 확인해야 한다.**

---

## 2. 작업 세션 분할 (5세션)

### 세션 1 — 소스 파일 구조 파악 + core/ ES modules 전환 (1~2일)

**목표**: src/ 실제 파일 구조 완전히 파악 → core/ 파일들에 export/import 추가 → 빌드 검증

#### 2.1.1 사전 작업 — confirm-modal 이동 + 실제 파일 구조 완전 파악

**Step 0: confirm-modal.js/css를 src/ui/로 이동 (§1.4 결정 실행)**

```bash
# Phase 7.x에서 components/shared/에 작성된 파일을 ui/로 이동
mv src/components/shared/confirm-modal.js src/ui/confirm-modal.js
mv src/components/shared/confirm-modal.css src/ui/confirm-modal.css

# 이동 후 import 경로가 달라진 파일들 업데이트 (Phase 7.x에서 수정된 파일들)
# 수정 대상: storage.js, router.js, about.js, kanban.js, bulk-select.js, card-modal.js, docview-inline.js

# 각 파일에서 '../shared/confirm-modal' 또는 '../../shared/confirm-modal' 경로를 수정
grep -rn "confirm-modal" src/ --include="*.js"
# → 위 결과를 보고 각 파일의 import 경로를 올바르게 수정

# 경로 수정 후 빌드 (현재는 concat 방식이므로 경로가 코드에 직접 없을 수 있음)
# concat 방식에서는 경로가 없으므로, 이 이동은 ES modules 전환 후에야 의미가 있음
# → 파일을 이동만 해두고, import 경로는 각 파일을 ES modules로 전환할 때 올바르게 작성

echo "confirm-modal 이동 완료:"
ls src/ui/
```

**Step 1: 실제 파일 구조 완전 파악**

```bash
# 1. 현재 src/ 전체 파일 목록과 라인 수
find src -name "*.js" -not -path "*/node_modules/*" | sort | xargs wc -l

# 2. 각 core 파일의 첫 10줄 확인 (현재 concat 방식인지, 이미 export가 있는지)
for f in src/core/*.js; do
  echo "=== $f ==="
  head -5 "$f"
  echo
done

# 3. build.mjs 현재 내용 전체 확인
cat build/build.mjs

# 4. package.json scripts 확인
cat package.json | python3 -c "import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get('scripts',{}), indent=2, ensure_ascii=False))"
```

이 출력 결과를 바탕으로 아래 작업을 진행한다.

#### 2.1.2 core/ 파일 ES modules 전환

**전환 원칙**:

1. 파일 안에서 **다른 파일의 함수를 사용하는 모든 곳**에 import 추가
2. 파일 안에서 **다른 파일이 사용할 모든 함수/변수**에 export 추가
3. IIFE 래퍼 `(function(){ ... })()` 있으면 제거 (최상위 레벨 코드로)
4. 파일 자체 실행 부수효과(addEventListener, subscribe 등)는 그대로

**`src/core/dev.js` 변환 예시**:

```js
// Before (concat 방식 — 전역 함수)
const _devMode = (function(){ ... })();
function devLog(tag, ...args) { ... }
function devAssert(cond, msg) { ... }
function devTime(label, fn) { ... }
function devGroup(label, fn) { ... }

// After (ES modules)
const _devMode = (function(){ ... })();

export function devLog(tag, ...args) { ... }
export function devAssert(cond, msg) { ... }
export function devTime(label, fn) { ... }
export function devGroup(label, fn) { ... }
```

**`src/core/store.js` 변환 예시**:

```js
// After
import { devLog, devAssert } from './dev.js';

let _state = null;
const _subscribers = new Map();

export function storeInit(initialState) { ... }
export function getState() { return _state; }
export function applyState(s) { _state = s; }
export function subscribe(viewName, fn) { _subscribers.set(viewName, fn); }
export function getSubscriber(viewName) { return _subscribers.get(viewName); }
export function listViews() { return [..._subscribers.keys()]; }
export function bootState(s) { _state = s; }  // init.js에서 사용
```

**`src/core/action.js` 변환 예시**:

```js
// After
import { devLog, devAssert } from './dev.js';
import { getState, applyState } from './store.js';
import { markDirty } from './dirty.js';
import { queueRender } from './render-queue.js';  // 또는 store.js에 있으면 그쪽에서

const _reducers = [];

export function registerReducer(fn) { _reducers.push(fn); }

export function dispatch(action) {
  devLog('ACTION', action.type, action.payload || {});
  let state = getState();
  for (const r of _reducers) state = r(state, action);
  applyState(state);
  markDirty();
  const affects = action.meta?.affects || ['__all__'];
  if (affects.includes('__all__') || affects.includes('all')) {
    queueRender('__all__');
  } else {
    affects.forEach(v => queueRender(v));
  }
}
```

#### 2.1.3 세션 1 변환 대상 파일

다음 파일들을 ES modules로 전환:

```
src/core/dev.js
src/core/store.js
src/core/render-queue.js  (또는 queueRender가 있는 파일)
src/core/schema.js
src/core/storage.js
src/core/dirty.js
src/core/action.js
```

#### 2.1.4 빌드 방식 임시 병용

세션 1에서는 **concat 빌드를 유지**하면서 ES modules 전환만 한다. esbuild 전환은 세션 3에서 한다.

concat 방식의 현재 `build.mjs`에서는 `export`/`import` 키워드를 esbuild가 번들링 전에 strip해줄 것을 기대하지만, 현재는 그냥 concat이라 **빌드가 실패**할 수 있다.

이를 해결하는 두 가지 접근:

**접근 A (권장)**: 세션 1부터 esbuild 전환을 시작. core 파일만 변환되면 esbuild로 전환해도 나머지 파일은 전역 함수로 남아있어 잠깐 혼용 상태가 되지만, esbuild가 `sideEffects: false`로 처리하면 됨.

**접근 B**: 세션 3 전까지 `export`만 추가하고 `import`는 나중에 추가. concat 방식에서 `export` 키워드는 문법 에러가 되므로 이 방법은 불가.

→ **접근 A 채택**: 세션 1 말미에 build.mjs를 esbuild 방식으로 전환. 단, main.js 없이 src/data/init.js를 임시 엔트리로 사용.

---

### 세션 2 — constants, utils, markdown, normalize, actions/ ES modules 전환 (1~2일)

**목표**: core/ 나머지 + actions/ ES modules 전환 + 빌드 검증

#### 2.2.1 전환 대상 파일

```
src/core/constants.js
src/core/utils.js
src/core/body-helpers.js
src/core/tag-parser.js
src/core/tag-filter.js
src/core/markdown.js
src/core/normalize.js
src/core/state.js
src/core/theme.js
src/core/router.js
src/core/events.js
src/core/static-html.js
src/actions/card-actions.js
src/actions/column-actions.js
src/actions/view-actions.js
src/actions/settings-actions.js
src/actions/export-import.js
src/ui/confirm-modal.js          (Phase 7.x에서 생성됨, 세션 1에서 ui/로 이동됨)
src/components/shared/dirty-indicator.js (Phase 7.x에서 생성됨)
```

#### 2.2.2 상수 파일 처리

`src/core/constants.js`는 `ORIGIN`, `COL_COLORS`, `STORAGE_KEY` 등 순수 상수.

```js
// After
export const ORIGIN = Object.freeze({
  author: '비움',
  site: 'olbit.org',
  copyright: 'Copyright © 2026 biwoom',
  license: 'CC BY-SA 4.0',
  tool: 'OL · ATLAS · Weaving the Wisdom',
});

export const STORAGE_KEY = 'ol_state_v7';  // 실제 값 확인 필요
export const COL_COLORS = [ ... ];
// ...
```

#### 2.2.3 actions/ 파일 처리

```js
// src/actions/card-actions.js After
import { devLog } from '../core/dev.js';
import { getState, applyState } from '../core/store.js';
import { registerReducer, dispatch } from '../core/action.js';
import { normalizeCard } from '../core/normalize.js';

// 액션 타입 상수
export const CARD_CREATE = 'CARD_CREATE';
export const CARD_UPDATE = 'CARD_UPDATE';
// ... 나머지 타입들

// Action Creators
export function createCard(card) { ... }
export function updateCard(id, patch) { ... }
// ... 나머지 creators

// Reducer
function cardReducer(state, action) { ... }

// 부수효과: 이 파일이 import되면 reducer 자동 등록
registerReducer(cardReducer);
```

**중요**: `registerReducer(cardReducer)`는 파일 레벨 부수효과. 이 파일이 import되면 자동으로 reducer가 등록된다. esbuild는 부수효과가 있는 파일의 import를 제거하지 않는다.

#### 2.2.4 `src/core/state.js` (S Proxy) 처리

`S` Proxy는 모든 컴포넌트에서 사용하는 전역 객체. Phase 2에서 Proxy strict mode가 이미 적용되어 있다.

```js
// After
import { getState } from './store.js';
import { devLog } from './dev.js';

export const S = new Proxy({}, {
  get(target, prop) {
    const state = getState();
    return state ? state[prop] : undefined;
  },
  set(target, prop, value) {
    const msg = `[STRICT] Direct S.${String(prop)} mutation — use dispatch()`;
    console.error(msg);
    throw new Error(msg);
  },
});
```

---

### 세션 3 — build.mjs esbuild 전환 + main.js 작성 (1일)

**목표**: build.mjs를 esbuild bundle 방식으로 완전 전환. main.js 엔트리 작성.

#### 2.3.1 `src/main.js` 작성

```js
// src/main.js
// OL ATLAS v0.8 — ES modules 통합 엔트리
// esbuild가 이 파일의 import 그래프를 따라 단일 IIFE 번들을 생성한다.

// === 1. CORE ===
import './core/dev.js';
import './core/store.js';
import './core/render-queue.js';
import './core/schema.js';
import './core/storage.js';
import './core/dirty.js';
import './core/action.js';
import './core/static-html.js';
import './core/constants.js';
import './core/utils.js';
import './core/body-helpers.js';
import './core/tag-parser.js';
import './core/tag-filter.js';
import './core/markdown.js';
import './core/normalize.js';
import './core/state.js';
import './core/theme.js';
import './core/events.js';

// === 2. ACTIONS ===
// 각 파일이 import될 때 registerReducer() 부수효과 실행됨
import './actions/card-actions.js';
import './actions/column-actions.js';
import './actions/view-actions.js';
import './actions/settings-actions.js';

// === 3. UI UTILITIES ===
import './ui/custom-select.js';
import './ui/confirm-modal.js';          // core/storage, core/router가 의존 → core 앞에 위치

// === 4. SHARED COMPONENTS ===
import './components/shared/dirty-indicator.js';
import './components/shared/toc.js';

/*! AUTHOR_BUNDLE_START */
// === 4. AUTHOR COMPONENTS ===
// 이 영역은 exportBook() 시 제거됨
import './components/author/home.js';
import './components/author/kanban.js';
import './components/author/cardgrid.js';
import './components/author/listview.js';
import './components/author/card-modal.js';
import './components/author/docview-inline.js';
import './components/author/md-editor.js';
import './components/author/bulk-select.js';
import './components/author/color-picker.js';
import './actions/export-import.js';
/*! AUTHOR_BUNDLE_END */

// === 5. SHARED VIEW COMPONENTS ===
// (author 마커 밖에 있으므로 BOOK에도 유지됨)
import './components/shared/docview.js';
import './components/shared/sidebar.js';
import './components/shared/about.js';
import './ui/custom-select.js';

// === 6. SEARCH ===
import './data/search/search.js';

// === 7. ROUTER + BOOT ===
import './core/router.js';
import { boot } from './data/init.js';
boot();
```

#### 2.3.2 `build/build.mjs` 전환

```js
// build/build.mjs (Phase 8.0 이후)
import { build } from 'esbuild';
import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const SRC  = 'src';
const DIST = 'dist';

async function buildOL() {
  const startTime = Date.now();

  // 1. JS 번들 — esbuild가 ES modules를 단일 IIFE로 변환
  const result = await build({
    entryPoints: [join(SRC, 'main.js')],
    bundle:       true,
    format:       'iife',
    globalName:   'OL',
    minify:       false,          // 마커 보존을 위해 minify OFF
    legalComments: 'inline',      // /*! */ 주석 보존 (AUTHOR_BUNDLE 마커)
    target:       ['es2020'],
    define: {
      '__DEV__': 'false',
    },
    logLevel: 'info',
    write:    false,              // 파일 쓰지 않고 메모리에서 받기
  });

  const jsBundle = result.outputFiles[0].text;

  // 2. 마커 잔존 검증
  if (!jsBundle.includes('AUTHOR_BUNDLE_START') || !jsBundle.includes('AUTHOR_BUNDLE_END')) {
    console.error('[BUILD] ❌ AUTHOR_BUNDLE 마커가 번들에서 사라짐!');
    console.error('  legalComments: "inline" 설정을 확인하세요.');
    process.exit(1);
  }

  // 3. CSS 번들
  const CSS_FILES = [
    'src/styles/tokens.css',
    'src/styles/base.css',
    'src/styles/components.css',
    'src/styles/sidebar.css',
    'src/styles/kanban.css',
    'src/styles/cardgrid.css',
    'src/styles/listview.css',
    'src/styles/docview.css',
    'src/styles/modal.css',
    'src/ui/confirm-modal.css',                    // ui/로 이동됨
    'src/components/shared/dirty-indicator.css',
  ];
  const cssBundle = CSS_FILES.map(f => readFileSync(f, 'utf8')).join('\n');

  // 4. HTML 셸에 인라인
  let html = readFileSync(join(SRC, 'index.html'), 'utf8');
  html = html.replace('<!--CSS-->', `<style>\n${cssBundle}\n</style>`);
  html = html.replace('<!--JS-->',  `<script>\n${jsBundle}\n</script>`);

  writeFileSync(join(DIST, 'ol-atlas.html'), html, 'utf8');
  console.log(`[BUILD] ✅ 완료 (${Date.now() - startTime}ms)`);
  console.log(`[BUILD] 산출물: ${join(DIST, 'ol-atlas.html')} (${(html.length / 1024).toFixed(1)} KB)`);
}

buildOL().catch(e => { console.error(e); process.exit(1); });
```

> **주의**: 현재 `build.mjs`가 CSS를 처리하는 방식(CSS_FILES 배열 또는 다른 방식)을 반드시 먼저 확인하고 그대로 계승해야 한다.

#### 2.3.3 세션 3 검증

```bash
# 1. main.js와 새 build.mjs 작성 후 빌드
npm run build

# 2. 마커 잔존 확인
grep -c "AUTHOR_BUNDLE_START\|AUTHOR_BUNDLE_END" dist/ol-atlas.html
# 기대값: 2

# 3. 빌드 산출물 크기 (v0.7 빌드와 비슷해야 함)
ls -lah dist/ol-atlas.html

# 4. 필수 함수 존재
grep -c "function customConfirm\|renderDirtyIndicator\|function dispatch\|function storeInit" dist/ol-atlas.html

# 5. 브라우저에서 열기 → 부팅 정상
```

---

### 세션 4 — components/ 디렉토리 재편 (1~2일)

**목표**: 기존 `src/components/` 평면 파일들을 `shared/`, `author/`, `reader/`로 이동 + ES modules 전환

#### 2.4.1 이동 계획

```bash
# shared/ — 이미 Phase 7.x에서 생성됨
# 아래 파일들을 추가로 이동

# docview.js → shared/ (읽기 전용 부분)
cp src/components/docview.js src/components/shared/docview.js

# sidebar.js → shared/
cp src/components/sidebar.js src/components/shared/sidebar.js

# about.js → shared/
cp src/components/about.js src/components/shared/about.js

# toc.js → shared/
cp src/components/toc.js src/components/shared/toc.js

# author/ 디렉토리 생성 + 이동
mkdir -p src/components/author
cp src/components/home.js src/components/author/home.js
cp src/components/kanban.js src/components/author/kanban.js
cp src/components/cardgrid.js src/components/author/cardgrid.js
cp src/components/listview.js src/components/author/listview.js
cp src/components/card-modal.js src/components/author/card-modal.js
cp src/components/docview-inline.js src/components/author/docview-inline.js
cp src/components/md-editor.js src/components/author/md-editor.js
cp src/components/bulk-select.js src/components/author/bulk-select.js
cp src/components/color-picker.js src/components/author/color-picker.js

# reader/ 디렉토리 생성 (Phase 8.x에서 채워질 예정)
mkdir -p src/components/reader
```

> **중요**: 원본 파일을 바로 `mv`하지 말고, `cp`로 복사한 후 새 위치에서 ES modules 변환을 완료한 다음 빌드 확인 후 구 파일 삭제.

#### 2.4.2 각 파일의 ES modules 전환

`src/components/` 하위 파일들은 `../core/`, `../actions/`로의 상대 경로 import가 필요하다.

**변환 예시 — `src/components/author/kanban.js`**:

```js
// Before (전역 함수 사용)
function renderKanban() {
  const state = S;  // 또는 getState()
  // ...
  dispatch(moveCard(...));
  // ...
}
subscribe('kanban', renderKanban);

// After (ES modules)
import { S } from '../../core/state.js';
import { dispatch } from '../../core/action.js';
import { subscribe } from '../../core/store.js';
import { queueRender } from '../../core/render-queue.js';
import { parseMarkdown } from '../../core/markdown.js';
import { escapeHTML, slugFilename } from '../../core/utils.js';
import { moveCard, deleteCard, createColumn, deleteColumn } from '../../actions/card-actions.js';
import { customConfirm } from '../../ui/confirm-modal.js';

export function renderKanban() {
  // 기존 로직 그대로
}

// 부수효과: 이 파일이 import되면 subscribe 자동 실행
subscribe('kanban', renderKanban);
```

**변환 시 주의**: 기존 코드에서 사용하는 모든 전역 참조를 import로 변경. 전역 참조 탐색 방법:

```bash
# kanban.js에서 사용하는 전역 함수 목록 확인
grep -oE "[a-zA-Z_$][a-zA-Z0-9_$]+" src/components/kanban.js | sort -u | grep -v "^[A-Z_]*$" | head -50
```

#### 2.4.3 세션 4 검증 — 세션 3과 동일한 명령어

```bash
npm run build

# 부팅 정상
# 시나리오 7종 통과
# 디렉토리 구조 확인
find src/components -name "*.js" | sort
```

---

### 세션 5 — 전환 완료 검증 + 정리 + 태그 (0.5~1일)

**목표**: 모든 .js 파일이 ES modules인지 검증. 미변환 파일 처리. 최종 빌드 검증. 태그.

#### 2.5.1 미변환 파일 검출

```bash
# export/import가 없는 .js 파일 찾기
python3 << 'EOF'
import os, re

missing = []
for root, dirs, files in os.walk('src'):
    dirs[:] = [d for d in dirs if d not in ('node_modules',)]
    for fname in files:
        if not fname.endswith('.js'): continue
        path = os.path.join(root, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        has_export = bool(re.search(r'\bexport\b', content))
        has_import = bool(re.search(r'\bimport\b', content))
        if not has_export and not has_import:
            missing.append(path)

if missing:
    print("⚠ export/import 없는 파일:")
    for p in missing:
        print(f"  {p}")
else:
    print("✅ 모든 .js 파일이 ES modules")
EOF
```

#### 2.5.2 사용 안 하는 파일 정리

```bash
# history.js — v0.6 잔존, main.js에 import 없으면 트리쉐이킹으로 자동 제거
# 확인
grep -r "history" src/main.js
# 없으면 삭제해도 됨 (또는 남겨둬도 무방 — import 안 되면 번들에 안 들어감)
```

#### 2.5.3 구버전 파일 정리

세션 4에서 `cp`로 복사했던 구 파일들을 삭제:

```bash
# components/ 루트의 이전 파일들 삭제 (shared/author/reader로 이동 완료 후)
# 단, main.js 빌드가 통과된 것을 확인한 후에만 삭제
for f in home kanban cardgrid listview card-modal docview-inline md-editor bulk-select color-picker docview sidebar about toc; do
  if [ -f "src/components/${f}.js" ]; then
    echo "삭제: src/components/${f}.js"
    rm "src/components/${f}.js"
  fi
done
```

#### 2.5.4 Phase 8.0 최종 검증

```bash
# 1. ES modules 전환 완료 확인
python3 -c "
import os, re
missing = []
for root, dirs, files in os.walk('src'):
    dirs[:] = [d for d in dirs if 'node_modules' not in d]
    for f in files:
        if not f.endswith('.js'): continue
        p = os.path.join(root, f)
        c = open(p).read()
        if not re.search(r'\b(export|import)\b', c):
            missing.append(p)
print('미변환:', missing if missing else '없음 ✅')
"

# 2. AUTHOR_BUNDLE 마커 잔존
grep -c "AUTHOR_BUNDLE_START\|AUTHOR_BUNDLE_END" dist/ol-atlas.html
# 기대값: 2

# 3. 필수 subscribe 뷰 존재
python3 -c "
import re
with open('dist/ol-atlas.html') as f: c = f.read()
views = re.findall(r\"subscribe\(['\\\"]([^'\\\"]+)['\\\"\]\", c)
print('subscribe 뷰:', sorted(set(views)))
# 기대: about, cards, dirty-indicator, docview, home, kanban, list, sidebar, trash
"

# 4. 최종 빌드
npm run build

# 5. 브라우저 시나리오 7종 + Phase 7.x 시나리오

# 6. 태그
git add -A
git commit -m "[Phase 8.0] complete ES modules conversion + dual-runtime directory structure"
git tag v0.8.0-phase8.0-complete
```

---

## 3. 중요 변환 패턴 레퍼런스

### 3.1 전역 변수 S 처리

```js
// 모든 컴포넌트에서 S를 사용할 경우
import { S } from '../../core/state.js';   // components/ 에서
import { S } from '../core/state.js';      // data/ 에서
import { S } from './state.js';            // core/ 안에서
```

### 3.1b confirm-modal import 경로 (위치별)

```js
import { customConfirm, customAlert } from '../ui/confirm-modal.js';     // core/ 에서
import { customConfirm, customAlert } from '../../ui/confirm-modal.js';  // components/author/ 에서
import { customConfirm, customAlert } from '../../ui/confirm-modal.js';  // components/shared/ 에서
import { customConfirm, customAlert } from '../ui/confirm-modal.js';     // data/ 에서
```

### 3.2 registerReducer 부수효과

```js
// actions/ 파일 끝에 항상
registerReducer(myReducer);
// import될 때 자동 실행됨 — esbuild가 보존
```

### 3.3 subscribe 부수효과

```js
// components/ 파일 끝에 항상
subscribe('kanban', renderKanban);
// import될 때 자동 실행됨 — esbuild가 보존
```

### 3.4 toast 함수 위치 확인

`toast()` 함수가 실제로 어느 파일에 정의되어 있는지 확인:

```bash
grep -rn "^function toast\|^const toast\|^export function toast" src/
```

### 3.5 IIFE 래퍼 제거

현재 일부 파일이 IIFE로 감싸져 있을 수 있다:

```js
// Before
(function() {
  let _local = 0;
  function renderKanban() { ... }
  subscribe('kanban', renderKanban);
})();

// After — IIFE 제거, 상단에 import 추가
import { ... } from '...';

let _local = 0;  // 모듈 스코프로 유지됨 (안전)
export function renderKanban() { ... }
subscribe('kanban', renderKanban);
```

### 3.6 상대 경로 규칙

```
src/core/A.js → src/core/B.js       : './B.js'
src/actions/A.js → src/core/B.js    : '../core/B.js'
src/components/author/A.js → src/core/B.js  : '../../core/B.js'
src/components/author/A.js → src/actions/B.js : '../../actions/B.js'
src/components/author/A.js → src/components/shared/B.js : '../shared/B.js'
src/data/init.js → src/core/B.js    : '../core/B.js'
```

---

## 4. 자주 발생하는 문제 + 대응

### 4.1 esbuild 빌드 중 `Cannot find module` 에러

**원인**: import 경로가 잘못됨 (파일 확장자 `.js` 누락, 상대 경로 오류).

```bash
# 경로 문제 파악
node build/build.mjs 2>&1 | head -20
# 에러 메시지에 정확한 파일과 줄 번호 나옴
```

**대응**: 해당 파일 열어서 import 경로 수정.

### 4.2 `Circular dependency` 경고

**원인**: A가 B를 import하고 B가 A를 import하는 순환 의존성.

**대응**: 보통 `action.js ↔ dirty.js ↔ store.js` 사이에서 발생. 해결: `dispatch` 내에서 `markDirty()`를 직접 호출하지 않고, dirty 상태는 action 이후 별도 middleware 패턴으로 분리. 또는 `store.js`에서 `queueRender`를 받지 말고, action.js에서 직접.

### 4.3 `subscribe is not a function` 런타임 에러

**원인**: `store.js`가 컴포넌트 파일보다 나중에 평가됨 (import 순서 문제). esbuild는 import 그래프를 따라 의존성 먼저 평가하므로 일반적으로 이 문제가 없음. 단, main.js의 import 순서가 의존성보다 먼저 오면 발생.

**대응**: main.js에서 core/ import가 components/ import보다 먼저 있는지 확인.

### 4.4 AUTHOR_BUNDLE 마커가 번들에서 사라짐

**원인**: esbuild `legalComments: 'inline'` 옵션 미설정 또는 minify 활성화.

**대응**:

```js
// build.mjs 확인
legalComments: 'inline',
minify: false,
```

### 4.5 `S is not defined` 런타임 에러

**원인**: 컴포넌트가 `S`를 import 하지 않고 전역 변수로 사용하려 함.

**대응**: 해당 파일에 `import { S } from '../../core/state.js';` 추가.

### 4.6 부수효과 파일이 트리쉐이킹으로 제거됨

**원인**: esbuild가 부수효과만 있는 파일(export 없음)을 dead code로 간주.

**대응**: `package.json`에 `"sideEffects": ["src/**/*.js"]` 추가. 또는 esbuild 옵션에 `treeShaking: false` 임시 설정.

### 4.7 기존 concat build.mjs와 새 esbuild build.mjs 병용

세션 3 전까지 빌드가 실패할 수 있다. 이때:

```bash
# 원본 build.mjs 백업
cp build/build.mjs build/build.mjs.concat-backup

# 새 build.mjs 작성 (§2.3.2)
# 세션 3 이후부터 npm run build 사용
```

---

## 5. 세션별 git commit 메시지

|세션|커밋 메시지|
|---|---|
|1|`[Phase 8.0.1] convert core/ to ES modules (dev, store, schema, storage, dirty, action)`|
|2|`[Phase 8.0.2] convert constants, utils, markdown, normalize, actions/ to ES modules`|
|3|`[Phase 8.0.3] switch build.mjs to esbuild bundle + add src/main.js entry`|
|4|`[Phase 8.0.4] reorganize components/ into shared/, author/, reader/`|
|5|`[Phase 8.0.5] finalize ES modules conversion, cleanup, tag v0.8.0-phase8.0-complete`|

---

## 6. Phase 8.0 최종 게이트

**모든 항목 체크 시 Phase 8.1 진입 가능**:

- [ ] 모든 `.js` 파일이 ES modules (export/import 명시)
- [ ] `src/main.js` 작성 완료 (엔트리 포인트)
- [ ] `build.mjs` esbuild bundle 방식으로 전환 완료
- [ ] `dist/ol-atlas.html`에 `/*! AUTHOR_BUNDLE_START */` / `/*! AUTHOR_BUNDLE_END */` 마커 존재 (grep 확인)
- [ ] `npm run build` 성공, 1초 이내 완료
- [ ] subscribe 뷰 9개 모두 등록됨 (`docview, about, trash, home, sidebar, kanban, cards, list, dirty-indicator`)
- [ ] `src/components/author/`, `src/components/shared/`, `src/components/reader/` 구조 완성
- [ ] 구 파일 (`src/components/*.js` 루트) 정리 완료
- [ ] 브라우저 시나리오 7종 100% 통과
- [ ] Phase 7.x 커스텀 모달 정상 작동 확인
- [ ] dirty 인디케이터 정상 작동 확인
- [ ] 다크 모드 정상 작동 확인
- [ ] `git tag v0.8.0-phase8.0-complete` 부여됨

---

## 7. Phase 8.0 이후 → Phase 8.1 진입

Phase 8.0 완료 후 다음 단계:

```
Phase 8.1  Reader Manifest + schema v8     (1~2일)
Phase 8.2  커버페이지 + 편집기             (3~4일)
Phase 8.3  exportBook()                    (2~3일)
Phase 8.4  BOOK 기본 작동 + 사라지는 UI   (3~4일)
Phase 8.5  진행률 + 책갈피                 (2~3일)
Phase 8.6  본문 내부 링크 [[id]]           (2일)
Phase 8.7  통계 + sepia 모드               (1~2일)
Phase 8.8  마무리 + OL BOOK 첫 시연       (2일)
```

---

## 부록 A — Claude CLI 지시 프롬프트 템플릿

각 세션 시작 시 붙여넣기:

```
[작업 컨텍스트]
- 프로젝트: OL ATLAS v0.7 Phase 8.0
- 작업 디렉토리: <ol-atlas/ 절대 경로>
- 참조 문서: OL_ATLAS_v0_7_Phase8_0_작업지시서.md
- 현재 세션: 세션 N — <세션 설명>

[권한 선언]
작업지시서 최상단 권한 선언에 따라:
- ol-atlas/ 폴더 내 모든 파일 읽기·쓰기·생성·삭제 승인
- bash, node, python3, npm run * 실행 승인
- git add/commit/tag 승인
매번 묻지 말고 즉시 실행할 것.
단, git push / rm -rf <폴더> / 폴더 외부 접근은 실행 전 확인.

[이번 세션 목표]
- <산출물 1>
- <산출물 2>

[핵심 제약]
- 기능 변경 금지. ES modules 전환 + 디렉토리 재편만.
- 파일 하나 전환 후 즉시 빌드 검증. 한 번에 여러 파일 변환 금지.
- 반드시 실제 파일을 먼저 cat으로 확인 후 변환. 추정 금지.
- 세션 끝에 검증 게이트 통과 확인 후 git commit.
- 구 파일 삭제는 새 위치에서 빌드 통과 후에만.
```

---

## 부록 B — 핵심 검증 명령어 모음

```bash
# ES modules 전환 완료 확인
python3 -c "
import os, re
m=[p for r,d,f in os.walk('src') for fn in f
   if fn.endswith('.js')
   for p in [os.path.join(r,fn)]
   if 'node_modules' not in p
   and not re.search(r'\b(export|import)\b', open(p).read())]
print('미변환:',m if m else '없음 ✅')
"

# AUTHOR_BUNDLE 마커 확인
grep -c "AUTHOR_BUNDLE" dist/ol-atlas.html

# subscribe 뷰 목록 확인
python3 -c "
import re
c=open('dist/ol-atlas.html').read()
print(sorted(set(re.findall(r\"subscribe\(['\\\"]([^'\\\"]+)\", c))))
# 기대: ['about', 'cards', 'dirty-indicator', 'docview', 'home', 'kanban', 'list', 'sidebar', 'trash']
"

# 빌드 크기
ls -lah dist/ol-atlas.html

# 전체 빌드
npm run build

# 문법 검증 (빌드 전)
find src -name '*.js' -not -path '*/node_modules/*' | xargs -I{} node --check {}
```

---

**작성**: Claude (with biwoom) **기반**: Phase 2 완료 코드 직접 분석 + 설계서 v1.2 **상태**: Phase 7.x 완료 후 즉시 착수 가능 **선행 태그**: v0.7-phase7x-complete **완료 태그**: v0.8.0-phase8.0-complete **다음 문서**: Phase 8.1 작업지시서 (Reader Manifest + schema v8)