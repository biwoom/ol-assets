# OL 듀얼 런타임 설계를 위한 추가 검토 자료
## ol-atlas-v0.7 하위 트리 구조

```
.
├── build
│   ├── build.mjs
│   └── inline.mjs
├── dist
│   ├── bundle.js
│   └── ol-atlas.html
├── lib
├── node_modules
│   ├── @esbuild
│   │   └── darwin-x64
│   │       ├── bin
│   │       │   └── esbuild
│   │       ├── package.json
│   │       └── README.md
│   └── esbuild
│       ├── bin
│       │   └── esbuild
│       ├── install.js
│       ├── lib
│       │   ├── main.d.ts
│       │   └── main.js
│       ├── LICENSE.md
│       ├── package.json
│       └── README.md
├── package-lock.json
├── package.json
└── src
    ├── actions
    │   ├── card-actions.js
    │   ├── column-actions.js
    │   ├── export-import.js
    │   ├── settings-actions.js
    │   └── view-actions.js
    ├── components
    │   ├── about.js
    │   ├── bulk-select.js
    │   ├── card-modal.js
    │   ├── cardgrid.js
    │   ├── color-picker.js
    │   ├── docview-inline.js
    │   ├── docview.js
    │   ├── home.js
    │   ├── kanban.js
    │   ├── listview.js
    │   ├── md-editor.js
    │   ├── sidebar.js
    │   └── toc.js
    ├── core
    │   ├── action.js
    │   ├── body-helpers.js
    │   ├── constants.js
    │   ├── dev.js
    │   ├── dirty.js
    │   ├── events.js
    │   ├── history.js
    │   ├── markdown.js
    │   ├── normalize.js
    │   ├── render-queue.js
    │   ├── router.js
    │   ├── schema.js
    │   ├── state.js
    │   ├── static-html.js
    │   ├── storage.js
    │   ├── store.js
    │   ├── tag-filter.js
    │   ├── tag-parser.js
    │   ├── theme.js
    │   └── utils.js
    ├── data
    │   ├── init.js
    │   └── search
    │       └── search.js
    ├── i18n
    ├── index.html
    ├── styles
    │   ├── base.css
    │   ├── cardgrid.css
    │   ├── components.css
    │   ├── docview.css
    │   ├── kanban.css
    │   ├── listview.css
    │   ├── modal.css
    │   ├── sidebar.css
    │   └── tokens.css
    └── ui
        └── custom-select.js

20 directories, 67 files
```

---

## 추가할 기능

- 브라우저 새로고침시 업데이트한 내용 유실 경고창 만들기, 카드 삭제 시에도 경고창 만들기. 시스템 경고창이 아닌 div 태그 통한 경고창 만들기.
- Dirty State + beforeunload + autosave 작동 기능.

---

# 클로드 CLI 에이전트가 작업수행 후 만든 문서

# Phase 2 사전 확인 노트 (§7 항목)

## 1. updatedAt 갱신 정책
- v0.6 카드에 `updatedAt` 필드 없음. 오직 `created`만 사용.
- reducer에서 updatedAt 자동 추가 **금지**.

## 2. 카드 삭제 정책
- `S.trash` 배열에 `{ ...card, _trashedAt: ISO }` 형태로 `unshift` (맨 앞 추가).
- `S.userData.status[id]` 삭제.

## 3. 카드 순서 관리
- `S.cards` 배열 순서로 표현 (col.cardOrder 없음).
- 드래그드롭: 카드 제거 후 targetIdx 위치에 재삽입.

## 4. 칼럼 삭제 시 카드
- 해당 컬럼의 카드가 모두 **삭제** (휴지통 이동 없음, 즉시 제거).
- `S.cards = S.cards.filter(c => c.colId !== colId)`.

## 5. 뷰 상태 영구 저장
- `currentView`: 모듈 전역 변수, `localStorage.ol_last_view`에 저장됨 (S 외부).
- `prefixFilter`, `selectedTags`: 모듈 전역 변수 (S 외부).
- Phase 2에서 S.ui로 이동 **보류** — Phase 3+ 대상.
- Phase 2는 S.cards, S.columns, S.trash, S.userData, S.meta mutation만 dispatch로 전환.

## 6. 실제 state 필드명
- `S.columns` (not S.cols) — column-actions.js reducer에서 state.columns 사용
- `S.userData.status` — S.userData 직접 접근 (S.userData.status[id] 패턴)
- `S.nextColId`, `S.nextCardId` — reducer에서 관리

## 7. 빌드 방식
- ES modules 없음. 파일 concat 후 단일 스크립트.
- 모든 함수가 전역 scope 공유.
- action 파일은 load-time에 registerReducer() 호출.

## 8. 액션 파일 위치 (build.mjs JS_FILES)
- normalize.js (15) 다음, history.js 앞에 삽입.
- card-actions.js, column-actions.js, view-actions.js, settings-actions.js

---

# Phase 2 TODO — Action Layer 마이그레이션

**상태: ✅ COMPLETE** (2026-05-22)

Phase 1 완료 후 남은 직접 S 변이(mutation) 목록.
Phase 2에서 각 항목을 `dispatch(action)` 패턴으로 전환한다.

## 직접 변이 위치 목록

### S.cards 재할당 (filter로 교체)
| 파일                            | 라인      | 코드                                                   | 상태                                 |
| ----------------------------- | ------- | ---------------------------------------------------- | ---------------------------------- |
| src/components/bulk-select.js | 58      | `S.cards = S.cards.filter(c => c.id !== id)`         | ✅ `dispatch(bulkDeleteCards(ids))` |
| src/components/kanban.js      | 139     | `S.cards = S.cards.filter(c => c.id !== dragCardId)` | ✅ `dispatch(moveCard(...))`        |
| src/components/kanban.js      | 174–175 | `S.columns/cards = ...filter(...)` (컬럼 삭제)           | ✅ `dispatch(deleteColumn(colId))`  |
| src/components/card-modal.js  | 186     | `S.cards = S.cards.filter(c=>c.id!==deletedId)`      | ✅ `dispatch(deleteCard(id))`       |

### S.cards.push / splice (카드 추가)
| 파일 | 라인 | 코드 | 상태 |
|------|------|------|------|
| src/components/about.js | 65 | `S.cards.push(card)` (trash → restore) | ✅ `dispatch(restoreCard(id))` |
| src/components/kanban.js | 144, 147 | `S.cards.push/splice` (드래그 드롭 후 재삽입) | ✅ `dispatch(moveCard(...))` |
| src/components/kanban.js | 166 | `S.columns.push(...)` (컬럼 추가) | ✅ `dispatch(createColumn({...}))` |
| src/components/card-modal.js | 163 | `S.cards.push(card)` (신규 카드 저장) | ✅ `dispatch(createCard(...))` |
| src/actions/export-import.js | 522, 556, 583 | `S.columns/cards.push(...)` (CSV/OL 가져오기) | ✅ `dispatch(importMerge(...))` |

### S.nextColId / S.nextCardId 증가
| 파일 | 라인 | 코드 | 상태 |
|------|------|------|------|
| src/components/kanban.js | 166 | `S.nextColId++` | ✅ reducer에서 처리 |
| src/components/card-modal.js | 158 | `S.nextCardId++` | ✅ reducer에서 처리 |
| src/components/about.js | 61 | `S.nextCardId++` | ✅ reducer에서 처리 |
| src/actions/export-import.js | 521, 553, 555, 582 | `S.nextColId++`, `S.nextCardId++` | ✅ reducer에서 처리 |

### S.userData.status 직접 변이
| 파일 | 라인 | 코드 | 상태 |
|------|------|------|------|
| src/components/bulk-select.js | 59, 92 | `delete/assign S.userData.status[id]` | ✅ `dispatch(setBulkStatus(...))` |
| src/components/docview-inline.js | 351 | `S.userData.status[card.id] = dvEditStatus` | ✅ `dispatch(updateCard(..., {status}))` |
| src/components/card-modal.js | 150, 164, 188 | `S.userData.status[...] = ...` / `delete` | ✅ `dispatch(updateCard/createCard/deleteCard)` |
| src/components/listview.js | 77, 127 | `S.userData.status[card.id] = v` | ✅ `dispatch(setStatus(...))` |

## 구현된 Action 파일

- `src/actions/card-actions.js` — CARD_CREATE, CARD_UPDATE, CARD_DELETE, CARD_RESTORE, CARD_MOVE, CARD_PURGE, CARD_PURGE_ALL, STATUS_SET, STATUS_CLEAR, STATUS_BULK, CARD_BULK_DELETE, CARD_BULK_GROUP, CARD_BULK_COLUMN, IMPORT_MERGE
- `src/actions/column-actions.js` — COLUMN_CREATE, COLUMN_RENAME, COLUMN_DELETE, COLUMN_COLOR_UPDATE
- `src/actions/view-actions.js` — VIEW_CHANGE, BOARD_WIDTH_SET, META_TOGGLE_SET, SIDEBAR_OPEN_SET
- `src/actions/settings-actions.js` — SETTINGS_UPDATE, THEME_SET, META_UPDATE

## Phase 2.5 — Proxy Strict Mode

- [x] `src/core/state.js` S proxy `set` 트랩: 직접 mutation 시 에러를 던지도록 전환 (2026-05-22 완료)
