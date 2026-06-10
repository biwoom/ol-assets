# Phase 2 TODO — Action Layer 마이그레이션

**상태: ✅ COMPLETE** (2026-05-22)

Phase 1 완료 후 남은 직접 S 변이(mutation) 목록.
Phase 2에서 각 항목을 `dispatch(action)` 패턴으로 전환한다.

## 직접 변이 위치 목록

### S.cards 재할당 (filter로 교체)
| 파일 | 라인 | 코드 | 상태 |
|------|------|------|------|
| src/components/bulk-select.js | 58 | `S.cards = S.cards.filter(c => c.id !== id)` | ✅ `dispatch(bulkDeleteCards(ids))` |
| src/components/kanban.js | 139 | `S.cards = S.cards.filter(c => c.id !== dragCardId)` | ✅ `dispatch(moveCard(...))` |
| src/components/kanban.js | 174–175 | `S.columns/cards = ...filter(...)` (컬럼 삭제) | ✅ `dispatch(deleteColumn(colId))` |
| src/components/card-modal.js | 186 | `S.cards = S.cards.filter(c=>c.id!==deletedId)` | ✅ `dispatch(deleteCard(id))` |

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
