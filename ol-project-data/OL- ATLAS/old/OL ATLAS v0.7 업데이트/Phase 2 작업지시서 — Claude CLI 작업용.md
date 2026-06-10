# Phase 2 작업지시서 — Claude CLI 작업용

**대상**: OL ATLAS v0.7 Phase 2 — Action 도메인 정의 **작업 환경**: 로컬 PC + Claude CLI **선행 문서**: `OL_ATLAS_v0_7_최종_기획서_v2.md`, `OL_ATLAS_v0_7_Phase0_작업지시서.md`(완료), `OL_ATLAS_v0_7_Phase1_작업지시서.md`(완료) **필수 입력**: `PHASE_2_TODO.md` (Phase 1 세션 5에서 작성된 잔존 mutation 위치 목록) **Phase 2 목표 일수**: 2~3일 **위험 등급**: 🟡 중간 (Phase 1보다 낮지만, 잘못 교체하면 v0.6 기능 회귀 가능)

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
    - `npm install` (개발 의존성 추가가 필요한 경우만, 본문에서 명시한 경우)

### ❌ 별도 승인 필요 (실행 전 사용자 확인)

- 작업 폴더 외부(`ol-atlas/`를 벗어나는 경로) 접근
- 네트워크 요청 (외부 URL fetch 등)
- 시스템 설정 변경 (env, PATH, shell 설정)
- `git push`, `git reset --hard`, `git clean` 같은 파괴적 git 작업
- `rm -rf`로 폴더 전체 삭제

### 작업 진행 원칙

- **묻지 말고 진행**하되, 의심스러우면 **읽기 우선**(view, cat) 후 행동
- 매 세션 종료 시 **git commit** 실행 (검증 게이트 통과 후)
- 에러 발생 시 즉시 중단하고 사용자에게 보고

---

## 0. Phase 2 작업 개요

### 0.1 Phase 2의 핵심 임무

Phase 1에서 Action Layer 인프라(dispatch, reducer 등록, queueRender)는 마련됐지만, **실제 사용되는 액션은 거의 없는 상태**다. UI 코드의 대부분은 여전히 `S.cards.push(...)` 같은 직접 mutation을 사용하고 있고, Phase 1의 Proxy 어댑터가 이를 경고로 잡아 `PHASE_2_TODO.md`에 기록해뒀다.

**Phase 2의 임무**: 그 잔존 mutation을 모두 도메인별 액션으로 교체한다.

### 0.2 작업 범위

|구분|내용|
|---|---|
|**신규 작성**|`src/actions/card-actions.js`, `column-actions.js`, `view-actions.js`, `settings-actions.js` (4개 파일)|
|**개조 대상**|`src/ui/*` 전체, `PHASE_2_TODO.md`에 기록된 모든 위치|
|**부수 작업**|Phase 1 Proxy 어댑터 제거 또는 strict 모드 전환|
|**외부 영향**|없음. v0.6 기능 100% 보존|
|**금지**|UI 디자인 변경, 새 기능 추가, 액션 의미 변경|

### 0.3 Phase 2의 핵심 원칙

> **"v0.6과 똑같이 작동하지만, 모든 변경이 명시적 액션으로 표현된다."**

각 액션은 **v0.6 코드의 의도를 1:1로 옮긴 것**이지, 새로운 의미를 부여하는 것이 아니다.

### 0.4 Phase 2 완료 시점의 상태

- 사용자 입장: v0.6과 100% 동일 작동 (변화 없음)
- 개발자 입장:
    - 모든 state 변경이 명시적 액션 타입을 가짐
    - 콘솔에서 `[ACTION] CARD_UPDATE { id, patch }` 형태로 모든 변경 흐름이 추적 가능
    - Phase 1의 Proxy 경고 0건
    - Phase 3(사이드바 단순화)부터 새 UI 작업 시작 가능

---

## 1. Action 설계 원칙

### 1.1 액션 형태

```js
{
  type: 'DOMAIN_VERB',                    // 필수, 도메인_동사 형식
  payload: { /* 데이터 */ },              // 변경에 필요한 데이터
  meta: {                                 // (선택) 메타 정보
    affects: ['kanban', 'sidebar'],       // 영향받는 view 목록
    silent: false,                        // true면 dirty 마킹 안 함
  }
}
```

**`meta.affects`가 없으면 `['all']`로 간주** (Phase 1 action.js 설계).

### 1.2 액션 타입 명명 규칙

- 도메인(대문자) + 언더스코어 + 동사(대문자): `CARD_CREATE`, `COLUMN_REORDER`, `VIEW_CHANGE`
- 약어 금지 (`CRD_UPD` 같은 단축 금지)
- 도메인은 4개로 한정: `CARD_*`, `COLUMN_*`, `VIEW_*`, `SETTINGS_*`

### 1.3 Action Creator 패턴

```js
// 직접 객체 리터럴 작성하지 않고, 함수로 생성한다.
// 이유: 타입 일관성, 호출처 추적 용이.

// ❌ 금지
dispatch({ type: 'CARD_UPDATE', payload: { id, patch } });

// ✅ 권장
import { updateCard } from '@/actions/card-actions';
dispatch(updateCard(id, patch));
```

### 1.4 Reducer 작성 원칙

```js
// reducer는 (state, action) => newState 형태의 순수 함수
// 절대 state를 직접 수정하지 않고, 새 객체 반환

// ❌ 금지
function cardReducer(state, action) {
  state.cards.push(action.payload);    // 직접 mutation
  return state;
}

// ✅ 권장
function cardReducer(state, action) {
  switch (action.type) {
    case CARD_CREATE: {
      return {
        ...state,
        cards: [...state.cards, action.payload],
      };
    }
    default:
      return state;
  }
}
```

### 1.5 reducer가 자기 도메인이 아닌 액션을 받으면

`default: return state;`로 그대로 반환한다. action.js의 dispatch는 모든 reducer에 모든 액션을 순회 전달하므로, 각 reducer는 자기가 처리할 액션만 골라서 처리해야 한다.

---

## 2. 도메인별 액션 정의

### 2.1 src/actions/card-actions.js

```js
// src/actions/card-actions.js
import { normalizeCard } from '../core/state.js';

// === Action Types ===
export const CARD_CREATE = 'CARD_CREATE';
export const CARD_UPDATE = 'CARD_UPDATE';
export const CARD_DELETE = 'CARD_DELETE';
export const CARD_RESTORE = 'CARD_RESTORE';   // 휴지통에서 복원
export const CARD_MOVE = 'CARD_MOVE';         // 칼럼 간 이동
export const CARD_REORDER = 'CARD_REORDER';   // 같은 칼럼 내 순서 변경
export const CARD_TAGS_UPDATE = 'CARD_TAGS_UPDATE';
export const CARD_PURGE = 'CARD_PURGE';       // 휴지통에서 완전 삭제

// === Action Creators ===

export function createCard(card, opts = {}) {
  return {
    type: CARD_CREATE,
    payload: { card, ...opts },
    meta: { affects: ['kanban', 'cards', 'list', 'sidebar'] },
  };
}

export function updateCard(id, patch) {
  return {
    type: CARD_UPDATE,
    payload: { id, patch },
    meta: { affects: ['kanban', 'cards', 'list', 'docview', 'sidebar'] },
  };
}

export function deleteCard(id) {
  return {
    type: CARD_DELETE,
    payload: { id },
    meta: { affects: ['kanban', 'cards', 'list', 'sidebar'] },
  };
}

export function restoreCard(id) {
  return {
    type: CARD_RESTORE,
    payload: { id },
    meta: { affects: ['kanban', 'cards', 'list', 'sidebar'] },
  };
}

export function moveCard(id, fromColId, toColId, toIndex) {
  return {
    type: CARD_MOVE,
    payload: { id, fromColId, toColId, toIndex },
    meta: { affects: ['kanban', 'cards', 'list'] },
  };
}

export function reorderCard(id, colId, toIndex) {
  return {
    type: CARD_REORDER,
    payload: { id, colId, toIndex },
    meta: { affects: ['kanban', 'cards', 'list'] },
  };
}

export function updateCardTags(id, tags) {
  return {
    type: CARD_TAGS_UPDATE,
    payload: { id, tags },
    meta: { affects: ['kanban', 'cards', 'list', 'sidebar'] },
  };
}

export function purgeCard(id) {
  return {
    type: CARD_PURGE,
    payload: { id },
    meta: { affects: ['sidebar'] },
  };
}

// === Reducer ===

export function cardReducer(state, action) {
  switch (action.type) {
    case CARD_CREATE: {
      const { card } = action.payload;
      const normalized = normalizeCard(card);
      return {
        ...state,
        cards: [...state.cards, normalized],
      };
    }

    case CARD_UPDATE: {
      const { id, patch } = action.payload;
      return {
        ...state,
        cards: state.cards.map(c =>
          c.id === id ? normalizeCard({ ...c, ...patch, updatedAt: new Date().toISOString() }) : c
        ),
      };
    }

    case CARD_DELETE: {
      const { id } = action.payload;
      const card = state.cards.find(c => c.id === id);
      if (!card) return state;
      return {
        ...state,
        cards: state.cards.filter(c => c.id !== id),
        trash: [...(state.trash || []), { ...card, deletedAt: new Date().toISOString() }],
      };
    }

    case CARD_RESTORE: {
      const { id } = action.payload;
      const card = (state.trash || []).find(c => c.id === id);
      if (!card) return state;
      const { deletedAt, ...restored } = card;
      return {
        ...state,
        cards: [...state.cards, restored],
        trash: (state.trash || []).filter(c => c.id !== id),
      };
    }

    case CARD_MOVE: {
      const { id, fromColId, toColId, toIndex } = action.payload;
      return {
        ...state,
        cards: state.cards.map(c =>
          c.id === id ? { ...c, colId: toColId, updatedAt: new Date().toISOString() } : c
        ),
        // 순서는 별도 메커니즘 (cards 배열 순서 또는 col.cardOrder)
      };
    }

    case CARD_REORDER: {
      // v0.6의 실제 순서 관리 방식에 맞춰 구현
      // (cards 배열 순서로 표현되는지, col.cardOrder로 표현되는지 확인 필요)
      return state;  // TODO: v0.6 구현 확인 후 채움
    }

    case CARD_TAGS_UPDATE: {
      const { id, tags } = action.payload;
      return {
        ...state,
        cards: state.cards.map(c =>
          c.id === id ? { ...c, tags, updatedAt: new Date().toISOString() } : c
        ),
      };
    }

    case CARD_PURGE: {
      const { id } = action.payload;
      return {
        ...state,
        trash: (state.trash || []).filter(c => c.id !== id),
      };
    }

    default:
      return state;
  }
}
```

**중요**: 위 reducer는 v0.6 코드의 실제 동작에 맞춰 보정해야 한다. 예를 들어 v0.6이 `card.updatedAt`을 자동으로 갱신하지 않는다면, 그 부분은 제거. **새 의미를 추가하지 말 것**.

### 2.2 src/actions/column-actions.js

```js
// src/actions/column-actions.js

export const COLUMN_CREATE = 'COLUMN_CREATE';
export const COLUMN_RENAME = 'COLUMN_RENAME';
export const COLUMN_DELETE = 'COLUMN_DELETE';
export const COLUMN_REORDER = 'COLUMN_REORDER';
export const COLUMN_COLOR_UPDATE = 'COLUMN_COLOR_UPDATE';

export function createColumn(col) {
  return {
    type: COLUMN_CREATE,
    payload: { col },
    meta: { affects: ['kanban', 'cards', 'list', 'sidebar'] },
  };
}

export function renameColumn(id, name) {
  return {
    type: COLUMN_RENAME,
    payload: { id, name },
    meta: { affects: ['kanban', 'cards', 'list', 'sidebar'] },
  };
}

export function deleteColumn(id) {
  return {
    type: COLUMN_DELETE,
    payload: { id },
    meta: { affects: ['kanban', 'cards', 'list', 'sidebar'] },
  };
}

export function reorderColumns(orderArray) {
  return {
    type: COLUMN_REORDER,
    payload: { order: orderArray },
    meta: { affects: ['kanban', 'sidebar'] },
  };
}

export function updateColumnColor(id, color) {
  return {
    type: COLUMN_COLOR_UPDATE,
    payload: { id, color },
    meta: { affects: ['kanban', 'sidebar'] },
  };
}

export function columnReducer(state, action) {
  switch (action.type) {
    case COLUMN_CREATE: {
      const { col } = action.payload;
      return { ...state, cols: [...state.cols, col] };
    }

    case COLUMN_RENAME: {
      const { id, name } = action.payload;
      return {
        ...state,
        cols: state.cols.map(c => c.id === id ? { ...c, name } : c),
      };
    }

    case COLUMN_DELETE: {
      const { id } = action.payload;
      // v0.6의 삭제 정책 확인 필요: 카드도 함께 휴지통 이동? 카드는 무소속?
      return {
        ...state,
        cols: state.cols.filter(c => c.id !== id),
      };
    }

    case COLUMN_REORDER: {
      const { order } = action.payload;
      const byId = new Map(state.cols.map(c => [c.id, c]));
      return {
        ...state,
        cols: order.map(id => byId.get(id)).filter(Boolean),
      };
    }

    case COLUMN_COLOR_UPDATE: {
      const { id, color } = action.payload;
      return {
        ...state,
        cols: state.cols.map(c => c.id === id ? { ...c, color } : c),
      };
    }

    default:
      return state;
  }
}
```

### 2.3 src/actions/view-actions.js

```js
// src/actions/view-actions.js

export const VIEW_CHANGE = 'VIEW_CHANGE';                 // 카드보드/리스트/문서뷰/about 전환
export const TAB_SELECT = 'TAB_SELECT';                   // v0.7 신규 (Phase 3 이후)
export const BOARD_WIDTH_SET = 'BOARD_WIDTH_SET';         // v0.7 신규
export const META_TOGGLE_SET = 'META_TOGGLE_SET';         // v0.7 신규
export const PREFIX_FILTER_SET = 'PREFIX_FILTER_SET';     // 사이드바 prefix 필터
export const PREFIX_FILTER_CLEAR = 'PREFIX_FILTER_CLEAR';
export const TAG_FILTER_SET = 'TAG_FILTER_SET';           // 검색바 태그 필터
export const SEARCH_QUERY_SET = 'SEARCH_QUERY_SET';

export function changeView(viewName, opts = {}) {
  return {
    type: VIEW_CHANGE,
    payload: { view: viewName, ...opts },
    meta: { affects: ['__all__'] },  // view 전환은 모두 갱신
  };
}

export function setPrefixFilter(prefix, value) {
  return {
    type: PREFIX_FILTER_SET,
    payload: { prefix, value },
    meta: { affects: ['kanban', 'cards', 'list', 'sidebar'] },
  };
}

export function clearPrefixFilter() {
  return {
    type: PREFIX_FILTER_CLEAR,
    payload: {},
    meta: { affects: ['kanban', 'cards', 'list', 'sidebar'] },
  };
}

export function setTagFilter(tags) {
  return {
    type: TAG_FILTER_SET,
    payload: { tags },
    meta: { affects: ['kanban', 'cards', 'list', 'sidebar'] },
  };
}

export function setSearchQuery(query) {
  return {
    type: SEARCH_QUERY_SET,
    payload: { query },
    meta: { affects: ['kanban', 'cards', 'list'] },
  };
}

export function viewReducer(state, action) {
  // view 관련 state가 어디 저장되는지 v0.6 코드 확인 필요
  // - currentView, prefixFilter, tagFilter, searchQuery 등
  // - 일부는 S 안에, 일부는 별도 모듈 전역에 있을 수 있음
  // Phase 2에서는 S.ui 또는 S.viewState 같은 네임스페이스로 통일

  switch (action.type) {
    case VIEW_CHANGE: {
      const { view } = action.payload;
      return {
        ...state,
        ui: { ...(state.ui || {}), currentView: view },
      };
    }

    case PREFIX_FILTER_SET: {
      const { prefix, value } = action.payload;
      return {
        ...state,
        ui: { ...(state.ui || {}), prefixFilter: { prefix, value } },
      };
    }

    case PREFIX_FILTER_CLEAR: {
      return {
        ...state,
        ui: { ...(state.ui || {}), prefixFilter: null },
      };
    }

    case TAG_FILTER_SET: {
      const { tags } = action.payload;
      return {
        ...state,
        ui: { ...(state.ui || {}), tagFilter: tags },
      };
    }

    case SEARCH_QUERY_SET: {
      const { query } = action.payload;
      return {
        ...state,
        ui: { ...(state.ui || {}), searchQuery: query },
      };
    }

    default:
      return state;
  }
}
```

**중요**: v0.6에서 view 관련 state(currentView, prefixFilter 등)가 어디 저장되는지 정확히 확인해야 한다. `S` 안에 있을 수도 있고, `let currentView = 'kanban'` 같은 별도 모듈 전역에 있을 수도 있다. Phase 2에서는 모두 `S.ui.*` 같은 네임스페이스로 통일.

### 2.4 src/actions/settings-actions.js

```js
// src/actions/settings-actions.js

export const SETTINGS_UPDATE = 'SETTINGS_UPDATE';
export const THEME_SET = 'THEME_SET';
export const SIDEBAR_TOGGLE = 'SIDEBAR_TOGGLE';

export function updateSettings(patch) {
  return {
    type: SETTINGS_UPDATE,
    payload: { patch },
    meta: { affects: ['__all__'] },  // 설정 변경은 전체에 영향 가능
  };
}

export function setTheme(theme) {
  return {
    type: THEME_SET,
    payload: { theme },
    meta: { affects: ['__all__'] },
  };
}

export function toggleSidebar(open) {
  return {
    type: SIDEBAR_TOGGLE,
    payload: { open },
    meta: { affects: ['sidebar', 'header'] },
  };
}

export function settingsReducer(state, action) {
  switch (action.type) {
    case SETTINGS_UPDATE: {
      const { patch } = action.payload;
      return {
        ...state,
        settings: { ...(state.settings || {}), ...patch },
      };
    }

    case THEME_SET: {
      const { theme } = action.payload;
      return {
        ...state,
        settings: { ...(state.settings || {}), theme },
      };
    }

    case SIDEBAR_TOGGLE: {
      const { open } = action.payload;
      return {
        ...state,
        settings: { ...(state.settings || {}), sidebarOpen: !!open },
      };
    }

    default:
      return state;
  }
}
```

---

## 3. boot.js에 reducer 등록

Phase 1의 boot.js에서 reducer 등록 부분이 비어있었다. Phase 2에서 채운다.

```js
// src/boot.js (Phase 2)
// ... 기존 import 다음에 추가

import { registerReducer } from './core/action.js';
import { cardReducer } from './actions/card-actions.js';
import { columnReducer } from './actions/column-actions.js';
import { viewReducer } from './actions/view-actions.js';
import { settingsReducer } from './actions/settings-actions.js';

// boot() 함수 안, store init 직후, UI 모듈 import 전에 추가:
registerReducer(cardReducer);
registerReducer(columnReducer);
registerReducer(viewReducer);
registerReducer(settingsReducer);
devLog('BOOT', '4 reducers registered');
```

---

## 4. PHASE_2_TODO.md 처리 — 핵심 작업

Phase 1 세션 5에서 작성된 `PHASE_2_TODO.md`에는 다음 형식의 목록이 있다:

```
- src/ui/kanban.js:123 — S.cards.push(...)  → CARD_CREATE
- src/ui/cards.js:456 — S.cards[i].title = ... → CARD_UPDATE
- src/ui/sidebar.js:789 — setPrefixFilter(prefix, value) → PREFIX_FILTER_SET
- ...
```

**Phase 2의 가장 큰 작업은 이 목록을 하나씩 dispatch 호출로 교체하는 것**.

### 4.1 교체 패턴

#### 패턴 A: 단순 mutation 교체

**Before**:

```js
// src/ui/kanban.js
function addCardToCol(colId, title) {
  const newCard = { id: newId(), title, colId, tags: [] };
  S.cards.push(newCard);
  renderKanban();
}
```

**After**:

```js
import { dispatch } from '../core/action.js';
import { createCard } from '../actions/card-actions.js';

function addCardToCol(colId, title) {
  const newCard = { id: newId(), title, colId, tags: [] };
  dispatch(createCard(newCard));
  // renderKanban() 호출 불필요 - action.meta.affects가 자동 처리
}
```

#### 패턴 B: 객체 속성 직접 변경

**Before**:

```js
function updateTitle(cardId, newTitle) {
  const card = S.cards.find(c => c.id === cardId);
  card.title = newTitle;
  card.updatedAt = new Date().toISOString();
  save();
  renderCards();
}
```

**After**:

```js
import { dispatch } from '../core/action.js';
import { updateCard } from '../actions/card-actions.js';

function updateTitle(cardId, newTitle) {
  dispatch(updateCard(cardId, { title: newTitle }));
  // updatedAt은 reducer가 처리
  // save()는 markDirty()의 autosave가 처리
  // render는 affects가 처리
}
```

#### 패턴 C: 복잡한 다단계 변경

**Before**:

```js
function moveCardToColumn(cardId, toCol) {
  const card = S.cards.find(c => c.id === cardId);
  const fromCol = card.colId;
  card.colId = toCol;
  // 순서 조정 로직
  reorderArrInPlace(...);
  save();
  renderKanban();
  renderSidebar();
}
```

**After**:

```js
import { dispatch } from '../core/action.js';
import { moveCard, reorderCard } from '../actions/card-actions.js';

function moveCardToColumn(cardId, toCol, toIndex) {
  const card = S.cards.find(c => c.id === cardId);  // 읽기는 OK
  const fromCol = card.colId;
  dispatch(moveCard(cardId, fromCol, toCol, toIndex));
}
```

복잡한 단계가 여러 액션의 조합이면, 액션을 순차 dispatch하거나, 한 액션의 reducer가 모든 변경을 처리하도록 설계.

### 4.2 교체 작업 워크플로

```bash
# 1. PHASE_2_TODO.md 열기
cat PHASE_2_TODO.md

# 2. 각 항목마다:
#    - 해당 파일/줄 열기
#    - mutation 패턴 분석
#    - 적절한 액션 찾기 (또는 §2의 정의에 추가)
#    - dispatch 호출로 교체
#    - 처리 완료 표시

# 3. 작업 진행률 추적
# PHASE_2_TODO.md에 체크박스 추가
```

### 4.3 PHASE_2_TODO.md 수정 예시

작업하면서 다음 형식으로 진행 상황 표시:

```markdown
# Phase 2 잔존 직접 mutation 처리 목록

## 카드 도메인
- [x] src/ui/kanban.js:123 — S.cards.push(...) → dispatch(createCard(...))
- [x] src/ui/cards.js:456 — S.cards[i].title = ... → dispatch(updateCard(id, {title}))
- [ ] src/ui/docview.js:234 — S.cards[i].body = ... → dispatch(updateCard(id, {body}))

## 칼럼 도메인
- [x] src/ui/sidebar.js:567 — S.cols.push(...) → dispatch(createColumn(...))

## 뷰 상태 도메인
- [ ] src/ui/router.js:78 — currentView = 'kanban' → dispatch(changeView('kanban'))
...
```

---

## 5. Proxy 어댑터 처리

Phase 1의 `state.js` Proxy 어댑터는 잔존 mutation을 검출하는 디버깅 도구였다. Phase 2 완료 시점에 처리 방향을 결정해야 한다.

### 5.1 옵션 A — Strict 모드 전환 (권장)

Phase 2 완료 후 더 이상 직접 mutation이 있으면 안 된다. Proxy를 strict 모드로 전환해서 직접 mutation 시 **에러를 던지게** 한다.

```js
// src/core/state.js (Phase 2 완료 후)
import { getState, applyState, init as storeInit } from './store.js';
import { devLog, DEV } from './dev.js';

const STRICT_MODE = true;  // Phase 2 완료 후 true

export const S = new Proxy({}, {
  get(target, prop) {
    const state = getState();
    return state ? state[prop] : undefined;
  },
  set(target, prop, value) {
    if (STRICT_MODE && DEV) {
      console.error(`[STRICT] direct S.${String(prop)} mutation forbidden — use dispatch`);
      throw new Error(`Direct state mutation not allowed: S.${String(prop)}`);
    }
    devLog('DIRTY', `WARN: direct S.${String(prop)} mutation`);
    const state = getState();
    if (state) state[prop] = value;
    return true;
  },
});
```

**장점**: 이후 작업에서 실수로 직접 mutation을 도입하면 즉시 에러로 잡힘.

**단점**: 읽기는 여전히 Proxy를 통하므로 약간의 성능 오버헤드.

### 5.2 옵션 B — Proxy 완전 제거 (Phase 3 이후로 미룸)

`S`를 단순 getter로 전환:

```js
// src/core/state.js
export function getCards() { return getState().cards; }
export function getCols() { return getState().cols; }
// ...
```

UI 코드에서 `S.cards` → `getCards()`로 모두 교체.

**장점**: Proxy 오버헤드 0.

**단점**: 모든 `S.xxx` 호출을 다 교체해야 함. Phase 2 작업량이 2배로 늘어남.

### 5.3 Phase 2 권장: 옵션 A

옵션 A로 진행하고, 옵션 B는 v0.8 이후 정리.

---

## 6. 작업 순서 (5세션 분할)

### 세션 1 — 액션 도메인 4개 파일 작성 (1일)

**목표**: src/actions/card-actions.js, column-actions.js, view-actions.js, settings-actions.js 4개 파일 신규 작성.

**작업**:

1. `mkdir -p src/actions`
2. §2의 4개 파일 작성
3. 각 파일에서 v0.6 코드의 실제 동작을 확인하며 reducer 로직 보정
4. 각 파일 작성 후 `node --check src/actions/<file>.js`로 문법 검증

**v0.6 동작 확인 명령**:

```bash
# 카드 생성 시 v0.6이 무엇을 하는지 확인
grep -rn "S\.cards\.push\|cards\.push" src/ --include="*.js" -B 2 -A 5

# 카드 업데이트 시
grep -rn "\.title\s*=\|\.body\s*=\|\.tags\s*=" src/ui/ --include="*.js"

# updatedAt 갱신 여부
grep -rn "updatedAt" src/ --include="*.js"
```

**검증**:

- [ ] 4개 파일 모두 생성됨
- [ ] `node --check` 모두 통과
- [ ] 각 reducer가 v0.6의 동작과 1:1 매칭됨 (새 의미 추가 없음)
- [ ] action creator가 모두 `meta.affects` 명시

**git commit**: `[Phase 2.1] add action domains (card/column/view/settings)`

### 세션 2 — boot.js에 reducer 등록 + 기본 동작 검증 (0.5일)

**목표**: 4개 reducer를 boot에서 등록하고, dispatch가 작동하는지 확인.

**작업**:

1. §3에 따라 `src/boot.js`에 reducer 등록 코드 추가
2. `npm run dev`로 개발 서버 실행
3. 브라우저 콘솔에서 수동 dispatch 테스트:
    
    ```js
    // 콘솔에서import('./core/action.js').then(m => {  m.dispatch({ type: 'TEST', payload: {} });});
    ```
    
    에러 없이 처리되어야 함 (TEST 액션은 모든 reducer에서 default로 빠짐)

**검증**:

- [ ] 부팅 시 콘솔에 `4 reducers registered` 로그
- [ ] 부팅 시 콘솔에 `[BOOT]` 로그 정상
- [ ] v0.6 시나리오 7종 작동 (아직 mutation이 직접 mutation이라 정상 작동해야 함)
- [ ] Proxy 경고가 여전히 보임 (Phase 2에서 처리할 잔존 mutation)

**git commit**: `[Phase 2.2] register all reducers in boot`

### 세션 3 — 카드/칼럼 도메인 mutation 교체 (1일, 가장 큰 작업)

**목표**: PHASE_2_TODO.md의 카드/칼럼 관련 항목을 모두 dispatch로 교체.

**작업**:

1. PHASE_2_TODO.md를 읽고 카드/칼럼 관련 항목 추출
2. 각 항목에 대해 §4.1의 교체 패턴 적용
3. 한 위치 교체 후 즉시 `npm run dev`에서 해당 시나리오 작동 확인
4. PHASE_2_TODO.md에 체크박스 표시

**교체 우선순위**:

1. 카드 생성 (CARD_CREATE) — 가장 빈번
2. 카드 업데이트 (CARD_UPDATE) — 가장 많은 위치
3. 카드 삭제/복원 (CARD_DELETE / CARD_RESTORE)
4. 카드 이동/순서 (CARD_MOVE / CARD_REORDER)
5. 카드 태그 (CARD_TAGS_UPDATE)
6. 칼럼 작업 전체 (COLUMN_*)

**검증** (각 교체 후):

- [ ] 해당 위치의 v0.6 시나리오가 동일하게 작동
- [ ] 콘솔에 `[ACTION] CARD_xxx` 로그가 보임
- [ ] 해당 위치에서 Proxy 경고가 사라짐

**검증** (세션 끝):

- [ ] PHASE_2_TODO.md의 카드/칼럼 항목 모두 체크
- [ ] `grep -rEn "S\.cards\s*[\.\[]\s*[a-z]+\s*=" src/ui/` 결과 0건 (직접 mutation 0건)
- [ ] `grep -rEn "S\.cols\s*[\.\[]\s*[a-z]+\s*=" src/ui/` 결과 0건
- [ ] v0.6 시나리오 7종 완전 작동

**git commit**: `[Phase 2.3] migrate card/column mutations to dispatch`

### 세션 4 — 뷰/설정 도메인 mutation 교체 (0.5~1일)

**목표**: PHASE_2_TODO.md의 뷰 상태/설정 관련 항목을 모두 dispatch로 교체.

**작업**:

1. **사전 작업**: v0.6에서 뷰 관련 state가 어디 저장되는지 확인
    
    ```bash
    grep -rn "currentView\|prefixFilter\|tagFilter\|searchQuery" src/ --include="*.js"
    ```
    
2. 모듈 전역 변수로 있다면 → S.ui로 이동하는 추가 작업 필요
3. 뷰 상태 교체 (PREFIX_FILTER_SET, TAG_FILTER_SET, SEARCH_QUERY_SET, VIEW_CHANGE)
4. 설정 교체 (THEME_SET, SETTINGS_UPDATE 등)

**모듈 전역 → S.ui 마이그레이션** (필요시):

- Phase 1의 schema migrator를 v7 → v7.1로 분기하거나, normalizeState에서 보정
- `let currentView = 'kanban'` 같은 모듈 전역 변수를 모두 제거하고 `state.ui.currentView`로 통일

**검증**:

- [ ] PHASE_2_TODO.md의 뷰/설정 항목 모두 체크
- [ ] 모듈 전역 변수(currentView 등) 0건 (있다면 S.ui로 이동됨)
- [ ] v0.6 시나리오 7종 완전 작동
- [ ] 뷰 전환 시 콘솔에 `[ACTION] VIEW_CHANGE` 로그
- [ ] 필터/검색 시 콘솔에 해당 ACTION 로그

**git commit**: `[Phase 2.4] migrate view/settings mutations to dispatch`

### 세션 5 — Proxy strict 전환 + 최종 검증 (0.5~1일)

**목표**: Proxy를 strict 모드로 전환하고, Phase 2 게이트 모두 통과.

**작업**:

1. §5.1에 따라 state.js의 Proxy를 strict 모드로 전환
2. 부팅 시 에러가 나면, 잔존 mutation이 있다는 뜻 → 검출하여 처리
3. 모든 시나리오 재실행 + Proxy 에러 0건 확인
4. 빌드 검증 (`npm run build && npm run build:verify`)
5. 빌드 산출물에서 v0.6 시나리오 재확인

**검증** (Phase 2 게이트):

- [ ] **v0.6 시나리오 7종 100% 작동**
- [ ] **`grep -rEn "S\.(cards|cols|trash|settings|ui)\s*[\.\[]\s*[a-z]+\s*=" src/ui/ src/data/` 결과 0건** (직접 mutation 0건)
- [ ] **모든 변경이 dispatch 경유** (콘솔 ACTION 로그가 시나리오마다 보임)
- [ ] **Proxy strict 모드 작동** (실수 mutation 시 에러)
- [ ] **PHASE_2_TODO.md 100% 체크 완료**
- [ ] **`npm run build` 성공 + dist 기능 동등**
- [ ] **`npm run build:verify` PASS**
- [ ] **dev 로그가 dist에서 제거됨**

**git commit**: `[Phase 2.5] complete Phase 2 — all mutations via dispatch` + git tag `v0.7-phase2-complete`

---

## 7. v0.6 동작 확인이 필요한 지점

Phase 2의 가장 큰 함정은 "v0.6과 다르게 작동하는 액션을 만드는 것". 다음 지점들은 v0.6 코드를 직접 확인하며 reducer를 작성해야 한다.

### 7.1 updatedAt 갱신 정책

- v0.6이 카드 수정 시 `updatedAt`을 갱신하는가? 어떤 변경 때?
- 칼럼 변경 시에도 갱신?
- 태그만 바꿀 때도 갱신?

```bash
grep -rn "updatedAt" src/ui/ --include="*.js" -B 2 -A 2
```

### 7.2 카드 삭제 시 휴지통 이동 vs 즉시 삭제

- v0.6이 삭제 시 `state.trash`로 이동하는가?
- 휴지통이 별도 배열인가, 카드의 `deleted: true` 플래그인가?

```bash
grep -rn "trash\|deleted" src/ --include="*.js"
```

### 7.3 카드 순서 관리 방식

- 카드 순서가 `state.cards` 배열의 순서로 표현되는가?
- 아니면 `col.cardOrder` 같은 배열로?
- 칼럼별 정렬 규칙이 있는가?

```bash
grep -rn "cardOrder\|sortBy" src/ --include="*.js"
```

### 7.4 칼럼 삭제 시 카드 처리

- 칼럼 삭제 시 그 칼럼의 카드들은? 휴지통? 다른 칼럼으로 이동? 무소속?

```bash
grep -rn "deleteCol\|removeCol" src/ --include="*.js" -A 10
```

### 7.5 뷰 상태가 영구 저장되는가

- `currentView`가 localStorage에 저장되는가? 아니면 매번 기본값?
- prefixFilter는?

```bash
grep -rn "localStorage\|ol_state" src/ --include="*.js"
```

이 5가지 확인을 세션 1 시작 전에 수행하고, 결과를 `PHASE_2_NOTES.md`에 정리한다.

---

## 8. 자주 발생할 수 있는 문제 + 대응

### 8.1 Reducer가 v0.6과 다르게 동작

**증상**: 카드 추가 후 화면에 보이지 않거나, 다른 위치에 추가됨.

**원인**: reducer가 v0.6 코드의 의도를 부정확하게 옮김. 예를 들어 v0.6은 `unshift`로 맨 앞에 추가하는데, reducer는 `push`로 끝에 추가하는 경우.

**대응**:

- v0.6 원본 함수와 reducer를 나란히 비교
- v0.6의 의도를 그대로 옮길 것 — "개선"하지 말 것
- 의도가 불명확하면 §7의 검색 명령으로 확인

### 8.2 dispatch 후 화면이 안 갱신됨

**증상**: 액션은 dispatch되고 state는 바뀌었는데 화면 그대로.

**원인**:

1. `action.meta.affects`가 누락되어 `['all']`로 처리되지만, subscribe된 view가 없음
2. reducer가 새 객체를 반환하지 않고 기존 state를 수정

**대응**:

- 콘솔에서 `[QUEUE]`, `[FLUSH]` 로그 확인
- store.listViews()로 등록된 view 확인
- reducer가 `return { ...state, ... }` 패턴인지 확인

### 8.3 autosave 무한 루프

**증상**: dispatch마다 autosave 트리거 → save() → markClean → 또 dispatch?

**원인**: save() 안에서 다시 dispatch를 호출하는 경우.

**대응**:

- save()는 순수 localStorage 쓰기여야 함, dispatch 호출 금지
- markClean은 dispatch가 아니라 state.meta.dirty를 직접 수정 (이 부분만 예외적으로 허용)

### 8.4 모듈 전역 변수가 S.ui로 옮겨지면서 마이그레이션 실패

**증상**: 부팅 후 currentView가 undefined, 화면이 빈 상태.

**원인**: v0.6 localStorage에는 `currentView`가 없고, Phase 2의 migrator가 기본값을 주지 않음.

**대응**:

- normalizeState에서 `state.ui = state.ui || { currentView: 'kanban', ... }` 추가
- 또는 schema.js의 v7 migrator에서 S.ui 초기값 주입

### 8.5 Proxy strict 전환 후 부팅 실패

**증상**: 세션 5에서 strict 전환 후 부팅 시 즉시 에러.

**원인**: 어딘가 잔존 mutation. PHASE_2_TODO.md 누락.

**대응**:

- 에러 메시지의 `S.xxx` 부분 확인
- grep으로 해당 패턴 검색
- 발견된 위치를 dispatch로 교체
- strict 모드는 _Phase 2 게이트 통과 후_에 활성화. 너무 일찍 켜지 말 것.

---

## 9. Phase 2 → Phase 3 진입 조건

**모든 항목 체크 시 Phase 3 진입 가능**:

- [ ] 4개 액션 도메인 파일 작성 완료
- [ ] boot.js에서 4개 reducer 등록
- [ ] PHASE_2_TODO.md 100% 체크 완료
- [ ] grep 검증: 직접 mutation 0건
- [ ] 모든 변경이 dispatch 경유 (콘솔 ACTION 로그 확인)
- [ ] Proxy strict 모드 작동
- [ ] v0.6 시나리오 7종 100% 작동
- [ ] `npm run build` 성공 + dist 기능 동등
- [ ] `npm run build:verify` PASS
- [ ] dev 로그가 dist에서 제거됨
- [ ] git tag `v0.7-phase2-complete` 부여됨

---

## 10. 검증 체크리스트 한 페이지 요약

```
[세션 0] 사전 확인 (§7) ................... [ ]
  ├ updatedAt 갱신 정책 ............... [ ]
  ├ 카드 삭제 정책 .................... [ ]
  ├ 카드 순서 관리 .................... [ ]
  ├ 칼럼 삭제 시 카드 ................. [ ]
  └ 뷰 상태 영구 저장 여부 ............ [ ]

[세션 1] 액션 도메인 4개 파일 ............. [ ]
  ├ card-actions.js ................... [ ]
  ├ column-actions.js ................. [ ]
  ├ view-actions.js ................... [ ]
  └ settings-actions.js ............... [ ]

[세션 2] boot.js reducer 등록 ............. [ ]
  ├ 4 reducers registered 로그 ........ [ ]
  └ v0.6 시나리오 7종 (이전 작동) ..... [ ]

[세션 3] 카드/칼럼 mutation 교체 .......... [ ]
  ├ CARD_CREATE 위치 모두 교체 ........ [ ]
  ├ CARD_UPDATE 위치 모두 교체 ........ [ ]
  ├ CARD_DELETE/RESTORE 교체 .......... [ ]
  ├ CARD_MOVE/REORDER 교체 ............ [ ]
  ├ CARD_TAGS_UPDATE 교체 ............. [ ]
  └ COLUMN_* 전체 교체 ................ [ ]

[세션 4] 뷰/설정 mutation 교체 ............ [ ]
  ├ 모듈 전역 변수 → S.ui 이동 ........ [ ]
  ├ VIEW_CHANGE 교체 .................. [ ]
  ├ PREFIX/TAG/SEARCH 필터 교체 ....... [ ]
  └ SETTINGS_*/THEME_SET 교체 ......... [ ]

[세션 5] Strict 전환 + 최종 검증 .......... [ ]
  ├ Proxy strict 모드 ................. [ ]
  ├ 직접 mutation grep 0건 ............ [ ]
  ├ PHASE_2_TODO.md 100% ............. [ ]
  ├ dist 빌드 성공 .................... [ ]
  ├ dev 로그 제거 확인 ................ [ ]
  └ v0.6 시나리오 7종 ................. [ ]

[Phase 3 진입 게이트] ..................... [ ]
```

---

## 부록 A — Claude CLI 지시 프롬프트 템플릿 (Phase 2용)

각 세션 시작 시:

```
[작업 컨텍스트]
- 프로젝트: OL ATLAS v0.7 Phase 2 — Action 도메인 정의
- 작업 디렉토리: <ol-atlas/의 절대경로>
- 참조 문서: OL_ATLAS_v0_7_Phase2_작업지시서.md
- 필수 입력: PHASE_2_TODO.md (Phase 1 산출물)
- 현재 세션: 세션 N — <설명>

[권한]
작업지시서 최상단 권한 선언에 따라, 현재 폴더 내 모든 작업 일괄 승인.
파일 읽기/쓰기/실행/git 등 매번 묻지 말 것.

[이번 세션 목표]
- <구체적 산출물 1>
- <구체적 산출물 2>

[제약]
- v0.6 기능 변경 금지. 흐름만 바꾼다.
- 각 reducer는 v0.6의 동작을 1:1로 옮긴다. 새 의미 추가 금지.
- 각 파일 작성 후 `node --check`로 문법 검증
- 세션 끝에 git add + git commit (메시지는 본문에 명시된 형식)
- 검증 체크리스트 통과 후 다음 세션 진입
```

## 부록 B — 진척 추적 방법

Phase 2는 PHASE_2_TODO.md의 항목 수가 진척 지표다.

```bash
# 처리율 확인
total=$(grep -c '^- \[' PHASE_2_TODO.md)
done=$(grep -c '^- \[x\]' PHASE_2_TODO.md)
echo "진척: $done / $total ($((done * 100 / total))%)"
```

세션 3, 4 종료 시 이 명령으로 확인.

---

## 부록 C — Phase 2 후 마음의 짐

Phase 2 완료 시점에서 **여전히 남아있는 부채**:

1. **Proxy 어댑터의 읽기 경로 오버헤드**: v0.8에서 `S` 전체 제거 + getter 패턴으로 정리
2. **action.meta.affects의 수동 명시**: 누락 시 자동으로 `['all']` 처리되지만, 정밀도가 낮음. v0.8 이후 reducer가 영향 view를 자동 산출하는 방식 고려
3. **action creator의 boilerplate**: 모든 액션이 비슷한 패턴. Redux Toolkit 같은 도구 도입 검토 (단, 의존성 0 원칙과 충돌)

이것들은 Phase 2의 비목표다. **지금은 v0.6과 동일 작동 + dispatch 일관성**까지만 달성.

---

**작성**: Claude (with biwoom) **상태**: Phase 1 완료 후 즉시 사용 가능 **다음 문서**: Phase 3 작업지시서 (Phase 2 완료 후)

**기억할 것**: Phase 2까지 완료하면 v0.6과 겉보기에 동일하지만 내부 구조만 탄탄한 v0.7이 완성된다. 이 시점에서 콘텐츠 작업을 v0.6에서 v0.7로 옮길지, Phase 3 새 UI를 먼저 적용할지는 비움이 결정한다. 메모리의 원칙대로 **본질은 불교 콘텐츠**임을 잊지 말 것.