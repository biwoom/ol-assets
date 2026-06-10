# Phase 1 작업지시서 — Claude CLI 작업용

**대상**: OL ATLAS v0.7 Phase 1 **작업 환경**: 로컬 PC + Claude CLI **선행 문서**: `OL_ATLAS_v0_7_최종_기획서_v2.md`, `OL_ATLAS_v0_7_Phase0_작업지시서.md` (완료) **Phase 1 목표 일수**: 4~6일 **위험 등급**: 🔴 **최고** (v0.7 전체에서 가장 위험한 구간)

---

## ⚡ 권한 선언 (작업 시작 시 1회 적용, 이후 묻지 말 것)

다음 모든 권한을 **사전 일괄 승인**한다. 작업 중 매번 확인 요청 금지.

### ✅ 허용

- **현재 작업 폴더(`ol-atlas/`) 및 모든 하위 폴더** 내에서:
    - 파일 읽기 (read, view, cat 등)
    - 파일 쓰기·생성·수정·삭제 (write, create, edit, rm 등)
    - 디렉토리 생성·삭제·이동
    - bash 명령어 실행 (모든 shell 명령)
    - Node.js 스크립트 실행 (`node`, `npm run *`, `npx *`)
    - Python 스크립트 실행 (`python`, `python3`)
    - esbuild, jsdom 등 이미 설치된 패키지 사용
    - git 명령 (`git add`, `git commit`, `git diff`, `git log` 등)
    - grep, find, sed, awk 등 표준 unix 도구 사용
    - `npm install` (개발 의존성 추가가 필요한 경우만, 본문 §에서 명시한 경우)

### ❌ 별도 승인 필요 (실행 전 사용자 확인)

- 작업 폴더 외부(`ol-atlas/`를 벗어나는 경로) 접근
- 네트워크 요청 (외부 URL fetch, 새 패키지 다운로드 외)
- 시스템 설정 변경 (env, PATH, shell 설정)
- `git push`, `git reset --hard`, `git clean` 같은 파괴적 git 작업
- `rm -rf`로 폴더 전체 삭제

### 작업 진행 원칙

- **묻지 말고 진행**하되, 의심스러우면 **읽기 우선**(view, cat) 후 행동
- 매 Step 종료 시 **git commit** 실행 (검증 게이트 통과 후)
- 에러 발생 시 즉시 중단하고 사용자에게 보고

---

## 0. Phase 1 작업 개요

### 0.1 Phase 1의 핵심 임무

Phase 0에서 v0.6 코드를 모듈로 분해만 했다면, **Phase 1은 v0.6의 "직접 mutation + 직접 render 호출" 패턴을 Action Layer + Render Queue로 갈아끼우는 작업**이다.

**이 단계 완료 시점의 상태**:

- 사용자 입장: v0.6과 100% 동일 작동
- 개발자 입장: 모든 state 변경이 `dispatch(action)`을 거치고, 모든 view 갱신이 `queueRender(viewName)`을 거침
- Phase 2(Action 도메인 정의) 진입 가능

### 0.2 작업 범위

|구분|내용|
|---|---|
|**신규 작성**|`src/core/store.js`, `action.js`, `render-queue.js`, `dirty.js`, `schema.js`|
|**개조 대상**|`src/core/state.js` (S를 store 내부로 이동), `src/ui/*` 모든 view (직접 호출 제거)|
|**외부 영향**|없음. v0.6 기능 100% 보존|
|**금지**|UI 디자인 변경, 새 기능 추가, 리팩토링을 빙자한 로직 변경|

### 0.3 Phase 1의 핵심 원칙

> **"기능은 v0.6과 동일하다. 단, 흐름이 바뀐다."**

모든 PR/커밋 검증의 첫 질문: "이게 v0.6과 다르게 작동하는가?" — Yes면 잘못된 것.

---

## 1. 아키텍처 재확인 — 3계층 모델

Phase 1 완료 시점의 상태:

```
┌──────────────────────────────────────────────────────┐
│  UI Layer (src/ui/*)                                 │
│  - DOM 렌더링만 담당                                 │
│  - dispatch(action) 또는 queueRender('view')만 호출  │
│  - S 직접 mutation 금지                              │
│  - render*() 직접 호출 금지                          │
└────────────────────────┬─────────────────────────────┘
                         │ dispatch
                         ▼
┌──────────────────────────────────────────────────────┐
│  Action Layer (src/core/action.js)                   │
│  - dispatch(action) → reducer 실행                   │
│  - state 변경 후 markDirty() 자동 호출               │
│  - 영향받는 view들을 자동으로 queueRender            │
└────────────────────────┬─────────────────────────────┘
                         │ mutate
                         ▼
┌──────────────────────────────────────────────────────┐
│  State + Render Queue                                │
│  - store.getState() / store.subscribe(view, fn)      │
│  - queueRender → rAF flush                           │
│  - dirty + autosave debounce                         │
└──────────────────────────────────────────────────────┘
```

---

## 2. 신규 코어 모듈 — 상세 설계

### 2.1 src/core/store.js

```js
// src/core/store.js
// 중앙 상태 저장소. S는 store 내부 변수로 옮긴다.

import { devLog, devAssert } from './dev.js';

let _state = null;
const _subscribers = new Map();  // viewName → renderFn

export function init(initialState) {
  devAssert(initialState && typeof initialState === 'object', 'store.init: invalid state');
  _state = initialState;
  devLog('BOOT', 'store initialized', { cardCount: _state.cards?.length });
}

export function getState() {
  return _state;
}

// reducer 결과를 적용 (Action Layer에서만 호출)
export function applyState(newState) {
  devAssert(newState && typeof newState === 'object', 'store.applyState: invalid state');
  _state = newState;
}

// view 등록
export function subscribe(viewName, renderFn) {
  devAssert(typeof viewName === 'string', 'store.subscribe: viewName must be string');
  devAssert(typeof renderFn === 'function', 'store.subscribe: renderFn must be function');
  _subscribers.set(viewName, renderFn);
  devLog('BOOT', `subscribed view: ${viewName}`);
}

export function getSubscriber(viewName) {
  return _subscribers.get(viewName);
}

export function listViews() {
  return [..._subscribers.keys()];
}
```

### 2.2 src/core/action.js

```js
// src/core/action.js
// 모든 state 변경의 단일 진입점.

import { devLog, devAssert, devTime } from './dev.js';
import { getState, applyState } from './store.js';
import { markDirty } from './dirty.js';
import { queueRender } from './render-queue.js';

const _reducers = [];

// reducer 등록 (Phase 2에서 각 도메인 reducer가 등록됨)
export function registerReducer(reducer) {
  devAssert(typeof reducer === 'function', 'registerReducer: must be function');
  _reducers.push(reducer);
  devLog('BOOT', `reducer registered (total: ${_reducers.length})`);
}

// action에 영향받는 view 목록을 reducer가 직접 반환할 수도 있고,
// action.meta.affects 로 명시할 수도 있다. Phase 1은 후자 사용.
export function dispatch(action) {
  devAssert(action && typeof action === 'object', 'dispatch: action must be object');
  devAssert(typeof action.type === 'string', 'dispatch: action.type required');

  devLog('ACTION', action.type, action.payload || {});

  const t = devTime(`reduce ${action.type}`);
  let state = getState();
  for (const reducer of _reducers) {
    state = reducer(state, action);
  }
  applyState(state);
  t.end();

  markDirty();

  // 영향받는 view 자동 queue
  const affects = (action.meta && action.meta.affects) || ['all'];
  if (affects.includes('all')) {
    queueRender('__all__');
  } else {
    affects.forEach(v => queueRender(v));
  }
}
```

### 2.3 src/core/render-queue.js

```js
// src/core/render-queue.js
// rAF 기반 렌더 큐. 한 tick 안의 다중 queueRender는 1회로 합쳐짐.

import { devLog, devGroup } from './dev.js';
import { getSubscriber, listViews } from './store.js';

const _queue = new Set();
let _scheduled = false;

export function queueRender(viewName) {
  _queue.add(viewName);
  devLog('QUEUE', viewName, `(queue size: ${_queue.size})`);
  if (!_scheduled) {
    _scheduled = true;
    requestAnimationFrame(flush);
  }
}

function flush() {
  _scheduled = false;
  if (_queue.size === 0) return;

  const targets = _queue.has('__all__') ? listViews() : [..._queue];
  _queue.clear();

  devGroup('FLUSH', `flush ${targets.length} view(s)`, () => {
    for (const v of targets) {
      const fn = getSubscriber(v);
      if (!fn) {
        devLog('FLUSH', `no subscriber for view: ${v}`);
        continue;
      }
      devLog('RENDER', v);
      try {
        fn();
      } catch (err) {
        console.error(`[RENDER FAIL] ${v}:`, err);
      }
    }
  });
}

// 즉시 flush (테스트/디버깅용)
export function flushNow() {
  flush();
}
```

### 2.4 src/core/dirty.js

```js
// src/core/dirty.js
// Dirty State + autosave + beforeunload 경고.

import { devLog } from './dev.js';
import { getState } from './store.js';
import { save } from './storage.js';

let _autosaveTimer = null;
const AUTOSAVE_DEBOUNCE_MS = 1000;

export function markDirty() {
  const s = getState();
  if (!s.meta) s.meta = {};
  if (!s.meta.dirty) {
    s.meta.dirty = true;
    devLog('DIRTY', 'state marked dirty');
  }
  scheduleAutosave();
}

export function markClean() {
  const s = getState();
  if (!s.meta) s.meta = {};
  s.meta.dirty = false;
  s.meta.lastSavedAt = new Date().toISOString();
  devLog('DIRTY', 'state marked clean', s.meta.lastSavedAt);
}

function scheduleAutosave() {
  if (_autosaveTimer) clearTimeout(_autosaveTimer);
  _autosaveTimer = setTimeout(() => {
    devLog('DIRTY', 'autosave triggered');
    save();
    markClean();
  }, AUTOSAVE_DEBOUNCE_MS);
}

export function isDirty() {
  return !!getState()?.meta?.dirty;
}

// beforeunload 경고 (dirty일 때만)
export function installBeforeUnloadGuard() {
  window.addEventListener('beforeunload', (e) => {
    if (isDirty()) {
      const msg = '저장하지 않은 변경사항이 있습니다. 정말 나가시겠습니까?';
      e.preventDefault();
      e.returnValue = msg;
      return msg;
    }
  });
  devLog('BOOT', 'beforeunload guard installed');
}
```

### 2.5 src/core/schema.js

```js
// src/core/schema.js
// schemaVersion 마이그레이션. Phase 1은 v6→v7 추가.

import { devLog, devAssert } from './dev.js';

const CURRENT_VERSION = 7;

const migrators = {
  // v6 → v7: meta.dirty, meta.lastSavedAt, settings 추가
  6: (s) => {
    devLog('MIGRATE', 'v6 → v7');
    if (!s.meta) s.meta = {};
    s.meta.schemaVersion = 7;
    s.meta.dirty = false;
    s.meta.lastSavedAt = null;

    s.settings = s.settings || {
      theme: localStorage.getItem('ol_theme') || 'system',
      locale: 'ko',
      sidebarOpen: false,
      boardWidth: 'NORMAL',
      metaToggles: { title: true, body: true, tags: true },
      activeTabId: 'board',
    };
    return s;
  },
};

export function migrate(state) {
  if (!state) return state;
  if (!state.meta) state.meta = { schemaVersion: 6 };  // v6 추정

  let v = state.meta.schemaVersion || 6;
  devLog('MIGRATE', `current version: ${v}, target: ${CURRENT_VERSION}`);

  if (v === CURRENT_VERSION) {
    devLog('MIGRATE', 'no migration needed');
    return state;
  }

  // v6 백업을 localStorage에 저장 (안전망)
  if (v === 6) {
    try {
      localStorage.setItem('ol_backup_v6', JSON.stringify(state));
      devLog('MIGRATE', 'v6 backup saved to localStorage');
    } catch (e) {
      devLog('MIGRATE', 'v6 backup FAILED:', e.message);
    }
  }

  while (v < CURRENT_VERSION) {
    const fn = migrators[v];
    devAssert(fn, `no migrator for v${v}`);
    state = fn(state);
    v++;
  }

  devLog('MIGRATE', `migration complete: v${v}`);
  return state;
}

export function getCurrentVersion() {
  return CURRENT_VERSION;
}
```

---

## 3. state.js 개조

Phase 0에서 export하던 `S`를 store 내부로 옮긴다. **하지만 v0.6 호환성을 위해 임시 어댑터 유지**.

### 3.1 변경 전 (Phase 0 상태)

```js
// src/core/state.js (Phase 0)
export let S;
export function setState(newS) { S = newS; }
export function getS() { return S; }
```

### 3.2 변경 후 (Phase 1 상태)

```js
// src/core/state.js (Phase 1)
import { getState, applyState, init as storeInit } from './store.js';
import { devLog } from './dev.js';

// v0.6 호환 어댑터: 기존 코드의 `import { S } from './state.js'`가 깨지지 않게
// Proxy로 store의 getState()를 가리키게 한다.
export const S = new Proxy({}, {
  get(target, prop) {
    const state = getState();
    return state ? state[prop] : undefined;
  },
  set(target, prop, value) {
    devLog('DIRTY', `WARN: direct S.${String(prop)} mutation detected — should use dispatch`);
    const state = getState();
    if (state) state[prop] = value;
    return true;
  },
});

export function makeDefault() { /* v0.6 그대로 */ }
export function normalizeState(s) { /* v0.6 그대로 */ }
export function normalizeCard(c) { /* v0.6 그대로 */ }

// 초기화 시 store에 inject
export function bootState(initial) {
  storeInit(initial);
  devLog('BOOT', 'state injected into store');
}
```

**왜 Proxy?**: Phase 1에서는 아직 모든 UI 코드를 dispatch로 갈아끼우지 않았다. v0.6에서 `S.cards = ...` 같은 직접 mutation이 남아있을 수 있다. Proxy로 가로채서:

1. 코드는 그대로 작동
2. 콘솔에 경고 로그가 뜸 ("이 부분은 dispatch로 바꿔야 함" 표시)
3. Phase 1 후반에 grep + dev log로 남은 mutation을 모두 찾아 dispatch로 교체

이 어댑터는 **Phase 2 완료 시점에 제거**한다.

---

## 4. boot.js 재구성

부팅 순서가 가장 중요하다. **`__STATIC_HTML__` 캡처 → store 초기화 → reducer 등록 → UI 마운트 → 첫 렌더** 순서.

```js
// src/boot.js
import { devLog } from './core/dev.js';

devLog('BOOT', 'boot start');

// 1. __STATIC_HTML__ 캡처 (모든 DOM 조작 이전)
const __STATIC_HTML__ = document.documentElement.outerHTML;
window.__STATIC_HTML__ = __STATIC_HTML__;
devLog('BOOT', `__STATIC_HTML__ captured: ${(__STATIC_HTML__.length / 1024).toFixed(1)} KB`);

// 2. 코어 import
import { load } from './core/storage.js';
import { migrate } from './core/schema.js';
import { bootState, normalizeState } from './core/state.js';
import { installBeforeUnloadGuard } from './core/dirty.js';
import { registerReducer } from './core/action.js';
import { subscribe } from './core/store.js';
import { queueRender, flushNow } from './core/render-queue.js';

// 3. UI 모듈 import (subscribe 호출됨)
import './ui/sidebar.js';
import './ui/kanban.js';
import './ui/cards.js';
import './ui/list.js';
import './ui/docview.js';
import './ui/about.js';
import './ui/header.js';
import './ui/router.js';

// 4. (Phase 2에서) actions/* import + reducer 등록
// Phase 1에서는 reducer가 거의 비어있다. UI가 아직 dispatch를 직접 호출하지 않음.

// 5. 부팅 실행
async function boot() {
  devLog('BOOT', 'loading state from localStorage');
  let raw = load();  // Phase 1: load는 raw state만 반환하고 normalize/migrate는 boot에서

  raw = migrate(raw);                // v6 → v7
  raw = normalizeState(raw);
  bootState(raw);                    // store에 inject

  installBeforeUnloadGuard();

  devLog('BOOT', 'first render');
  queueRender('__all__');
  flushNow();  // 첫 렌더는 즉시 (rAF 대기 안 함)

  devLog('BOOT', 'boot complete');
}

boot().catch(err => {
  console.error('[BOOT FAIL]', err);
  alert('초기화 실패: ' + err.message);
});
```

---

## 5. UI 모듈 개조 — 패턴

각 view 모듈은 다음 패턴을 따른다.

### 5.1 변경 전 (v0.6 / Phase 0)

```js
// src/ui/kanban.js (Phase 0)
import { S } from '../core/state.js';

export function renderKanban() {
  // ... v0.6 그대로
}

// 다른 파일에서 직접 호출됨
// e.g. addCard() 함수가 S.cards.push() 후 renderKanban() 직접 호출
```

### 5.2 변경 후 (Phase 1)

```js
// src/ui/kanban.js (Phase 1)
import { S } from '../core/state.js';
import { subscribe } from '../core/store.js';
import { devLog } from '../core/dev.js';

function renderKanban() {
  devLog('RENDER', 'kanban');
  // ... v0.6 로직 그대로
}

// 모듈 로드 시 자동으로 store에 등록
subscribe('kanban', renderKanban);

// 더 이상 export하지 않음 (외부에서 직접 호출 금지)
```

다른 곳에서 칸반을 다시 그리고 싶으면:

```js
import { queueRender } from '../core/render-queue.js';
queueRender('kanban');
```

### 5.3 직접 호출 제거 작업

Phase 0 코드에서 `renderKanban()`, `renderCards()`, `renderList()`, `renderSidebar()` 등을 직접 호출하는 모든 지점을 찾아 `queueRender(viewName)`으로 교체.

**검색 명령**:

```bash
grep -rEn "render(Kanban|Cards|List|Sidebar|DocumentView|About)\s*\(" src/ui/ src/core/ src/data/
```

결과 0건이 될 때까지 작업.

**예외**: `boot.js`의 최초 렌더 호출은 `flushNow()`로 즉시 실행 OK.

---

## 6. storage.js 개조

Phase 0의 storage는 `localStorage` 직접 접근이지만, Phase 1에서는:

- `save()`: store.getState() → JSON → localStorage
- `load()`: localStorage → JSON parse → raw state 반환 (normalize/migrate는 boot에서)

```js
// src/core/storage.js
import { devLog } from './dev.js';
import { getState } from './store.js';

const KEY = 'ol_state';

export function save() {
  const t0 = performance.now();
  const state = getState();
  if (!state) {
    devLog('STORAGE', 'save skipped: no state');
    return;
  }
  try {
    const json = JSON.stringify(state);
    localStorage.setItem(KEY, json);
    devLog('STORAGE', `save: ${(json.length / 1024).toFixed(1)} KB in ${(performance.now() - t0).toFixed(1)}ms`);
  } catch (err) {
    console.error('[STORAGE] save failed:', err);
    alert('저장 실패: ' + err.message);
  }
}

export function load() {
  const t0 = performance.now();
  try {
    const json = localStorage.getItem(KEY);
    if (!json) {
      devLog('STORAGE', 'load: no existing state, returning empty');
      return null;
    }
    const raw = JSON.parse(json);
    devLog('STORAGE', `load: ${(json.length / 1024).toFixed(1)} KB in ${(performance.now() - t0).toFixed(1)}ms`);
    return raw;
  } catch (err) {
    console.error('[STORAGE] load failed:', err);
    return null;
  }
}
```

---

## 7. 작업 순서 (5세션 분할)

### 세션 1 — 신규 코어 모듈 작성 (1일)

**목표**: src/core/store.js, action.js, render-queue.js, dirty.js, schema.js 5개 파일 신규 작성.

**작업**:

1. §2의 5개 파일 그대로 작성
2. 각 파일 작성 후 `node --check src/core/<file>.js`로 문법 검증
3. 단위 테스트 작성 (옵션, 본문 §8 참조)

**검증**:

- [ ] 5개 파일 모두 생성됨
- [ ] `node --check` 모두 통과
- [ ] dev 로그 카테고리(ACTION, REDUCER, QUEUE, FLUSH, DIRTY, MIGRATE, BOOT, STORAGE, RENDER) 모두 사용됨

**git commit**: `[Phase 1.1] add core runtime modules (store, action, render-queue, dirty, schema)`

### 세션 2 — state.js 개조 + boot.js 재구성 (1일)

**목표**: state.js에 Proxy 어댑터, boot.js에 부팅 시퀀스 반영.

**작업**:

1. `src/core/state.js`를 §3.2의 형태로 변경
2. `src/boot.js`를 §4의 형태로 재작성
3. `src/core/storage.js`를 §6의 형태로 변경

**검증**:

- [ ] `npm run dev` 실행 → 브라우저 열기 → 콘솔에 `[BOOT]` 로그가 보임
- [ ] `[MIGRATE]` 로그가 보임 (v6 → v7 변환)
- [ ] 콘솔에 에러 없음
- [ ] v0.6 시나리오 7종 작동 확인 (Phase 0 작업지시서 §7 Step 0.3 참조)

**git commit**: `[Phase 1.2] inject store, migrate v6→v7, install beforeunload guard`

### 세션 3 — UI 모듈에 subscribe 등록 (1~2일)

**목표**: 각 view 모듈이 `subscribe('viewName', renderFn)`을 자체적으로 호출하도록 개조.

**작업**:

1. `src/ui/sidebar.js` → `subscribe('sidebar', renderSidebar)`
2. `src/ui/kanban.js` → `subscribe('kanban', renderKanban)`
3. `src/ui/cards.js` → `subscribe('cards', renderCards)`
4. `src/ui/list.js` → `subscribe('list', renderList)`
5. `src/ui/docview.js` → `subscribe('docview', renderDocumentView)`
6. `src/ui/about.js` → `subscribe('about', renderAbout)`
7. `src/ui/header.js` → `subscribe('header', renderHeader)` (있다면)

각 파일에서 render 함수는 더 이상 export하지 않음.

**검증**:

- [ ] `grep -rE "export function render" src/ui/` 결과 0건
- [ ] 부팅 시 콘솔에 `subscribed view: <name>` 로그가 7회(또는 해당 개수만큼) 보임
- [ ] v0.6 시나리오 7종 작동 확인

**git commit**: `[Phase 1.3] convert UI modules to store subscribers`

### 세션 4 — 직접 render 호출 제거 (1~2일, 가장 위험)

**목표**: 모든 `render*()` 직접 호출을 `queueRender('viewName')`으로 교체.

**검색 명령**:

```bash
grep -rEn "render(Kanban|Cards|List|Sidebar|DocumentView|About|Header)\s*\(" src/ --include="*.js"
```

**교체 작업**:

- 검색 결과의 각 위치를 열어, `renderXxx()` → `queueRender('xxx')`로 교체
- 해당 파일 상단에 `import { queueRender } from '../core/render-queue.js';` 추가
- 단, **boot.js의 첫 렌더는 `queueRender('__all__'); flushNow();` 패턴 유지**

**검증**:

- [ ] `grep -rEn "render(Kanban|Cards|List|Sidebar|DocumentView|About|Header)\s*\(" src/` 결과 0건
- [ ] `npm run dev` 실행 → 모든 시나리오 작동
- [ ] 콘솔에 `[QUEUE]` 로그가 액션마다 보임
- [ ] 콘솔에 `[FLUSH]` 그룹이 rAF 마다 보임
- [ ] 한 액션이 여러 view 갱신을 트리거할 때, FLUSH가 1회로 합쳐지는지 확인

**git commit**: `[Phase 1.4] replace direct render calls with queueRender`

### 세션 5 — Dirty State + autosave + 검증 (1일)

**목표**: dirty/autosave가 실제로 작동하는지 확인 + 전체 회귀 테스트.

**작업**:

1. `markDirty()` 호출 지점 확인 — Phase 1에서는 dispatch 안에서만 호출되어야 함. 다른 곳에서 호출하지 말 것.
2. 단, Proxy 어댑터(state.js §3.2)에서 `S.cards.push()` 같은 직접 mutation도 감지되도록 했으니, 그 경고가 보이면 해당 위치를 dispatch로 바꿔야 함 (Phase 2에서 본격 진행, Phase 1에서는 기록만)
3. 수동 테스트:
    - 카드 추가 → 1초 후 자동 저장 → 콘솔 `[DIRTY] autosave triggered` 보임
    - 카드 편집 중 새로고침 시도 → beforeunload 경고 뜸
    - 저장 후 새로고침 → 경고 안 뜸

**검증** (Phase 1 게이트):

- [ ] **v0.6 시나리오 7종 작동** (카드 추가/편집, 사이드바 필터, 뷰 전환, 다크모드, 검색, 저장)
- [ ] **dispatch 외 직접 state 수정 없음** (Proxy 경고 로그 확인하며 잔존 검출)
    - `[DIRTY] WARN: direct S.xxx mutation detected` 로그가 콘솔에 보이는 위치 기록 → §9 후속 작업으로 정리
- [ ] **직접 render 호출 0건** (grep 검증)
- [ ] **dirty/autosave 작동** (1초 디바운스, beforeunload 경고)
- [ ] **schema v6 → v7 마이그레이션 작동** (기존 localStorage 데이터 호환)
- [ ] **`ol_backup_v6` 자동 백업 생성됨**
- [ ] **`npm run build`로 dist 빌드 성공** + dist HTML이 v0.6과 기능 동등
- [ ] **`npm run build:verify` PASS**
- [ ] **빌드 산출물에 dev 로그 잔존 없음** (`grep -E '\[ACTION\]|\[FLUSH\]|\[QUEUE\]' dist/ol-atlas.html` 결과 0건)

**git commit**: `[Phase 1.5] complete Phase 1 — runtime infrastructure ready` + git tag `v0.7-phase1-complete`

---

## 8. (선택) 단위 테스트

코어 모듈은 jsdom 기반 단위 테스트가 가능하다. 시간 여유 있으면 작성.

### 8.1 build/test-core.mjs

```js
// build/test-core.mjs
import { JSDOM } from 'jsdom';
import assert from 'node:assert/strict';

const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>', {
  runScripts: 'outside-only',
});
global.window = dom.window;
global.document = dom.window.document;
global.requestAnimationFrame = (cb) => setTimeout(cb, 16);

// dynamic import (ES module)
const { dispatch, registerReducer } = await import('../src/core/action.js');
const { getState, init } = await import('../src/core/store.js');
const { queueRender, flushNow } = await import('../src/core/render-queue.js');

// 1. store 초기화
init({ cards: [], cols: [], meta: { schemaVersion: 7 } });
assert.equal(getState().cards.length, 0, 'initial cards empty');

// 2. reducer 등록 + dispatch
registerReducer((state, action) => {
  if (action.type === 'TEST_ADD') {
    return { ...state, cards: [...state.cards, action.payload] };
  }
  return state;
});

dispatch({ type: 'TEST_ADD', payload: { id: 1, title: 'test' } });
assert.equal(getState().cards.length, 1, 'card added via dispatch');

// 3. render queue 합치기
let renderCount = 0;
const { subscribe } = await import('../src/core/store.js');
subscribe('test-view', () => { renderCount++; });

queueRender('test-view');
queueRender('test-view');
queueRender('test-view');
await new Promise(r => setTimeout(r, 50));
assert.equal(renderCount, 1, 'multiple queueRender merged into one flush');

console.log('[test] all passed');
```

실행: `node build/test-core.mjs`

**Phase 1에서는 선택사항**. 시간 여유 있을 때만 작성.

---

## 9. Phase 1 종료 후 잔존 작업 기록

세션 5의 Proxy 경고 로그에서 발견된 "직접 state 수정" 위치들을 다음 파일에 기록:

```bash
# Phase 1 종료 시 작성
cat > PHASE_2_TODO.md << 'EOF'
# Phase 2 시작 시 처리할 잔존 직접 mutation 위치

다음은 Phase 1 세션 5에서 Proxy 경고로 검출된 위치들이다.
Phase 2에서 도메인 액션 정의 후, 각각을 적절한 dispatch로 교체한다.

(목록은 실제 검출 결과로 채움)

- src/ui/kanban.js:123 — S.cards.push(...)  → CARD_CREATE
- src/ui/cards.js:456 — S.cards[i].title = ... → CARD_UPDATE
- ...
EOF
```

이 파일이 Phase 2 작업지시서의 입력이 된다.

---

## 10. 자주 발생할 수 있는 문제 + 대응

### 10.1 Proxy가 너무 많은 경고를 뱉음

**증상**: 부팅 시 `[DIRTY] WARN: direct S.xxx mutation detected` 로그가 수십 번 떠서 콘솔이 가득 참.

**원인**: v0.6 코드의 거의 모든 곳이 직접 mutation이라 자연스러움.

**대응**:

- Phase 1에서는 **경고를 무시하지 않고 기록**한다
- 모든 경고 위치를 `PHASE_2_TODO.md`에 기록
- Phase 2에서 각 위치를 dispatch로 교체
- 경고 로그 자체를 끄지 말 것 (Phase 2에서 진척도 확인용)

### 10.2 첫 렌더가 빈 화면

**증상**: 부팅 후 화면이 비어있음. 콘솔에 에러는 없음.

**원인**: subscribe가 import 순서로 인해 boot의 첫 `queueRender('__all__')` 시점에 등록되지 않음.

**대응**:

- boot.js에서 UI 모듈 import가 첫 렌더 호출보다 먼저 실행되는지 확인
- ES module import는 호이스팅되지만 평가 순서는 명시 순서대로
- `listViews()` 호출해서 등록된 view 수 확인

### 10.3 autosave가 dispatch 후마다 즉시 실행됨

**증상**: 카드 추가 → 즉시 localStorage 저장. 디바운스 작동 안 함.

**원인**: dirty.js의 `scheduleAutosave` 타이머 초기화 누락 또는 매번 새 인스턴스.

**대응**:

- `_autosaveTimer`가 모듈 스코프 변수인지 확인 (let, 아니면 매번 초기화됨)
- `clearTimeout` 후 `setTimeout` 패턴 확인

### 10.4 beforeunload 경고가 매번 뜸

**증상**: 변경사항 없는데도 새로고침 시 경고.

**원인**: `markClean()`이 autosave 후 호출되지 않음.

**대응**:

- dirty.js의 `scheduleAutosave` 안에서 `save()` 호출 후 `markClean()` 호출 확인
- 부팅 직후 `meta.dirty = false`인지 확인

### 10.5 Phase 0에서 작동하던 export 기능이 깨짐

**증상**: 저장(다운로드) 버튼 클릭 시 빈 HTML이 다운로드됨.

**원인**: `__STATIC_HTML__` 캡처 시점이 변경됨. boot.js 재구성 중 캡처 라인이 뒤로 밀림.

**대응**:

- boot.js의 첫 import 직후(또는 그 전)에 캡처가 실행되는지 확인
- 빌드 후 dist HTML 열어서 `<script>` 안의 첫 30줄에 `documentElement.outerHTML` 호출 보이는지 확인
- 안 보이면 `index.html`에 별도 `<script>` 블록으로 캡처를 분리 (boot.js import 이전 실행)

---

## 11. Phase 1 게이트 → Phase 2 진입 조건

**모든 항목 체크 시 Phase 2 진입 가능**:

- [ ] 5개 신규 코어 모듈 작성 완료
- [ ] state.js Proxy 어댑터 작동
- [ ] boot.js 부팅 시퀀스 정상 (store init → migrate → mount → first render)
- [ ] 모든 UI 모듈이 subscribe로 등록됨
- [ ] 직접 render 호출 0건 (grep 검증)
- [ ] Dirty State + autosave + beforeunload 작동
- [ ] schema v6 → v7 마이그레이션 작동 + 백업 생성
- [ ] v0.6 시나리오 7종 100% 작동
- [ ] `npm run build` 성공 + dist 기능 동등
- [ ] dev 로그가 dist에서 제거됨
- [ ] `PHASE_2_TODO.md` 작성 완료 (잔존 직접 mutation 위치 목록)

---

## 12. 검증 체크리스트 한 페이지 요약

```
[세션 1] 신규 코어 모듈 작성 ............. [ ]
  ├ store.js .......................... [ ]
  ├ action.js ......................... [ ]
  ├ render-queue.js ................... [ ]
  ├ dirty.js .......................... [ ]
  └ schema.js ......................... [ ]

[세션 2] state.js + boot.js + storage.js .. [ ]
  ├ Proxy 어댑터 작동 ................. [ ]
  ├ boot.js 부팅 시퀀스 ............... [ ]
  └ v0.6 시나리오 7종 통과 ............ [ ]

[세션 3] UI 모듈 subscribe 전환 ........... [ ]
  ├ 7개 view subscribe ................ [ ]
  ├ render 함수 export 제거 ........... [ ]
  └ 부팅 로그 확인 .................... [ ]

[세션 4] 직접 render 호출 제거 ............ [ ]
  ├ grep 결과 0건 ..................... [ ]
  ├ queueRender 교체 .................. [ ]
  └ FLUSH 합치기 확인 ................. [ ]

[세션 5] Dirty + autosave + 검증 .......... [ ]
  ├ 자동 저장 1초 디바운스 ............ [ ]
  ├ beforeunload 경고 ................. [ ]
  ├ v6→v7 마이그레이션 ................ [ ]
  ├ ol_backup_v6 백업 ................. [ ]
  ├ dist 빌드 성공 .................... [ ]
  ├ dev 로그 제거 확인 ................ [ ]
  └ PHASE_2_TODO.md 작성 .............. [ ]

[Phase 2 진입 게이트] ..................... [ ]
```

---

## 부록 A — Claude CLI 지시 프롬프트 템플릿 (Phase 1용)

각 세션 시작 시:

```
[작업 컨텍스트]
- 프로젝트: OL ATLAS v0.7 Phase 1
- 작업 디렉토리: <ol-atlas/>의 절대경로>
- 참조 문서: OL_ATLAS_v0_7_Phase1_작업지시서.md
- 현재 세션: 세션 N — <설명>

[권한]
작업지시서 최상단 권한 선언에 따라, 현재 폴더 내 모든 작업 일괄 승인.
파일 읽기/쓰기/실행/git 등 매번 묻지 말 것.

[이번 세션 목표]
- <구체적 산출물 1>
- <구체적 산출물 2>

[제약]
- v0.6 기능 변경 금지. 흐름만 바꾼다.
- 각 파일 작성 후 `node --check`로 문법 검증
- 세션 끝에 git add + git commit (메시지는 본문에 명시된 형식)
- 검증 체크리스트 통과 후 다음 세션 진입
```

## 부록 B — 위험 등급별 git 운영

Phase 1은 위험도가 높으므로:

- **각 세션마다 git commit 필수**
- 세션 중간이라도 큰 변경 전에 `git stash` 또는 `git add` + `git commit -m "WIP"`
- 세션 종료 시 게이트 통과 후 `git commit -m "[Phase 1.N] ..."`
- Phase 1 전체 완료 시 `git tag v0.7-phase1-complete`

문제 발생 시 `git reset --hard <previous-tag>`로 안전하게 롤백 가능.

**중요**: `git reset --hard`는 §권한 선언의 "별도 승인 필요" 항목. Claude CLI가 실행하기 전 사용자 확인 받을 것.

---

**작성**: Claude (with biwoom) **상태**: Phase 0 완료 후 즉시 사용 가능 **다음 문서**: Phase 2 작업지시서 (Phase 1 완료 + PHASE_2_TODO.md 작성 후)