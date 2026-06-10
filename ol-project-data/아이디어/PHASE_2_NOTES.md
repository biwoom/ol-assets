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
