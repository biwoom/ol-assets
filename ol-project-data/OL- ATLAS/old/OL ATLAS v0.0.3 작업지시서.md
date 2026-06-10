# OL ATLAS v0.0.3 작업지시서

**버전**: v0.0.3  
**작성일**: 2026-05-25  
**이전 버전**: v0.0.2 (편집자 시스템 + 카드 행위 기록 완료)  
**작업 목적**: 편집 기록 시스템 완성 — 영구삭제 시 기록 소실 수정 + 비움 자동 등록 + 히스토리 UI 개선

---

## ⚡ 권한 선언 — AI 에이전트 전용 (세션 시작 시 1회 적용)

이하 모든 권한을 사전 일괄 승인한다. 작업 중 개별 확인 요청 금지.

**✅ 전면 허용**
```
파일 시스템
  cat, head, tail, grep, find, wc, diff      (읽기)
  write, create, str_replace, cp, mv, mkdir  (쓰기/생성/이동)
  rm <단일 파일>

셸 명령
  bash/sh 스크립트, 파이프, 리다이렉트, &&, ||, ; 체인

Node / npm
  node <script.js>, node --check <file.js>
  npm run *  (build, dev, test 등)

Git
  git status, git diff, git log, git add, git commit, git tag

빌드
  node build/build.mjs, node build/inline.mjs
```

**❌ 별도 승인 필요**
```
rm -rf <디렉토리> / git push / git reset --hard / git clean -fd
npm install <새패키지> / 폴더 외부 접근 / 네트워크 요청
```

---

## 빌드 산출물 파일명 규칙

```
dist/ol-atlas_v0.0.3.html
```
`build/inline.mjs`에서 `package.json` version을 읽어 자동 반영.  
`package.json` version을 `0.0.3`으로 업데이트 후 빌드.

---

## 작업 목록

| Phase | 내용 | 수정 파일 |
|-------|------|----------|
| **0** | package.json 버전 업데이트 | `package.json` |
| **1** | 영구삭제 시 acts 보존 — `meta.actLog` 아카이브 | `src/core/schema.js`, `src/core/normalize.js`, `src/actions/card-actions.js`, `src/components/shared/about.js` |
| **2** | 비움 첫 편집자 자동 등록 | `src/data/init.js` |
| **3** | saveLog editorName 제거 | `src/actions/export-import.js`, `src/components/shared/about.js` |
| **4** | 히스토리 UI — 2컬럼 레이아웃 | `src/components/shared/about.js`, `src/styles/components.css` |

---

## Phase 0 — 버전 업데이트

```json
// package.json
{
  "version": "0.0.3"
}
```

---

## Phase 1 — 영구삭제 시 acts 보존

### 1.1 문제 요약

현재 `_collectActsForEditor()`가 `S.cards`와 `S.trash`를 순회하여 acts를 수집한다.  
`CARD_PURGE` reducer가 `trash.filter(c => c.id !== id)`로 카드를 완전히 제거하면  
그 카드의 acts도 함께 사라져 편집 기록이 소실된다.

### 1.2 해결 구조: `meta.actLog` 아카이브

카드가 영구삭제되기 전 해당 카드의 acts를 `meta.actLog`에 이관한 후 삭제한다.  
`_collectActsForEditor()`는 카드의 acts + `meta.actLog`를 합산하여 반환한다.

```
카드 영구삭제 흐름:
CARD_PURGE dispatch
  → reducer: 삭제 전 card.acts → meta.actLog에 append (cardTitle 스냅샷 포함)
  → reducer: trash에서 카드 제거
  → _collectActsForEditor: S.cards + S.trash + S.meta.actLog 통합 반환
```

### 1.3 스키마 변경 (v8 → v9)

`meta.actLog` 필드 추가. 배열, 최대 1000개 유지.

```js
// meta.actLog 항목 구조
{
  at: "2026-05-25T10:00:00.000Z",
  type: "create" | "update" | "delete",
  editorId: "fp_a3f9b2c1",
  cardId: 5,
  cardTitle: "연기법",          // 삭제 시점 스냅샷
  archivedAt: "2026-05-25T15:00:00.000Z"  // 아카이브 시각
}
```

### 1.4 수정: `src/core/schema.js`

마이그레이터에 v9 추가:

```js
9: function(state) {
  devLog('MIGRATE', 'v8 → v9');
  state.meta.schemaVersion = 9;
  if (!Array.isArray(state.meta.actLog)) {
    state.meta.actLog = [];
  }
  return state;
}
```

`SCHEMA_VERSION` 상수를 `9`로 변경.

### 1.5 수정: `src/core/normalize.js`

`normalizeState`에 actLog 필드 보장 추가:

```js
// 기존 editors/saveLog 보장 코드 다음에 추가
if (!Array.isArray(s.meta.actLog)) s.meta.actLog = [];
```

### 1.6 수정: `src/actions/card-actions.js`

`CARD_PURGE` / `CARD_PURGE_ALL` reducer에 acts 이관 로직 추가:

```js
case CARD_PURGE: {
  const { id } = action.payload;
  const target = (state.trash || []).find(c => c.id === id);
  
  // acts 아카이브 이관
  const archivedAt = new Date().toISOString();
  const newActLogEntries = (target?.acts || []).map(act => ({
    ...act,
    cardId: target.id,
    cardTitle: target.title || '(제목 없음)',
    archivedAt
  }));
  const actLog = [
    ...(state.meta.actLog || []),
    ...newActLogEntries
  ].slice(-1000);  // 최대 1000개 유지
  
  return {
    ...state,
    meta: { ...state.meta, actLog },
    trash: (state.trash || []).filter(c => c.id !== id)
  };
}

case CARD_PURGE_ALL: {
  const archivedAt = new Date().toISOString();
  const newActLogEntries = (state.trash || []).flatMap(card =>
    (card.acts || []).map(act => ({
      ...act,
      cardId: card.id,
      cardTitle: card.title || '(제목 없음)',
      archivedAt
    }))
  );
  const actLog = [
    ...(state.meta.actLog || []),
    ...newActLogEntries
  ].slice(-1000);
  
  return {
    ...state,
    meta: { ...state.meta, actLog },
    trash: []
  };
}
```

### 1.7 수정: `src/components/shared/about.js`

`_collectActsForEditor()`에 actLog 통합:

```js
function _collectActsForEditor(editorId) {
  const acts = [];

  // 1. 현재 cards + trash의 acts (기존 방식 유지)
  [...S.cards || [], ...S.trash || []].forEach(card => {
    (card.acts || []).forEach(act => {
      if (act.editorId === editorId) {
        acts.push({
          at: act.at,
          type: act.type,
          editorId: act.editorId,
          cardId: card.id,
          cardTitle: card.title || '(제목 없음)'
        });
      }
    });
  });

  // 2. 영구삭제된 카드의 아카이브된 acts 추가
  (S.meta.actLog || []).forEach(act => {
    if (act.editorId === editorId) {
      acts.push({
        at: act.at,
        type: act.type,
        editorId: act.editorId,
        cardId: act.cardId,
        cardTitle: act.cardTitle || '(삭제된 카드)'
      });
    }
  });

  return acts;
}
```

### 1.8 Phase 1 검증

```
시나리오:
1. 카드 생성 (편집자 A)
2. 카드 수정 (편집자 A)
3. About 편집 기록 → 편집자 A에 생성/수정 기록 2건 표시 확인
4. 카드를 휴지통으로 이동
5. 휴지통에서 영구삭제
6. About 편집 기록 → 편집자 A에 기록 2건 여전히 표시 확인  ← 핵심
7. 전체 비우기 후에도 기록 유지 확인
```

---

## Phase 2 — 비움 첫 편집자 자동 등록

### 2.1 문제 요약

현재 `makeDefault()`에서 `editors: []`로 초기화된다.  
요구사항: 새 파일 생성 시 첫 편집자를 항상 `ORIGIN.author(비움)`으로 자동 등록.  
About 편집 기록에서 비움 탭이 항상 첫 번째로 표시되어야 함.

### 2.2 수정: `src/data/init.js`

`makeDefault()`에서 ORIGIN 기반 초기 편집자 등록:

```js
function makeDefault() {
  const now = today();         // 기존 today() 함수 사용
  const originEditorId = 'origin_biwoom';  // 고정 ID — 핑거프린트 없음

  return {
    meta: {
      // ... 기존 필드들 ...
      editors: [
        {
          id: originEditorId,
          name: ORIGIN.author,          // '비움'
          email: '',
          firstSavedAt: now,
          lastSavedAt: now,
          saveCount: 0,
          isOrigin: true                // 원본 편집자 마커
        }
      ],
      saveLog: [
        {
          at: now,
          editorId: originEditorId,
          note: '원본 생성'             // About 저장기록에 표시될 텍스트
        }
      ],
      actLog: [],
      currentEditorId: null
    },
    // ... 나머지 기존 구조 유지 ...
  };
}
```

**주의**: `origin_biwoom`은 핑거프린트 기반 ID가 아닌 고정 문자열.  
마이그레이션된 기존 파일(editors: [])에는 이 초기값이 없으므로  
About 히스토리 렌더에서 editors가 빈 배열일 때 "편집 이력 없음"으로 처리하면 됨.  
소급 적용(기존 파일에 비움 자동 추가) 하지 않음 — 데이터 무결성 원칙.

### 2.3 About 히스토리에서 origin 편집자 표시

`_renderAboutHistory`에서 `isOrigin: true`인 편집자는 탭/목록에서  
항상 첫 번째로 정렬되고 "(원본)" 레이블 표시:

```js
// editors 정렬: origin 먼저
const sortedEditors = [
  ...editors.filter(e => e.isOrigin),
  ...editors.filter(e => !e.isOrigin)
];
```

### 2.4 Phase 2 검증

```
1. 새 탭에서 빌드 파일 열기 (localStorage 없는 상태)
2. About → 편집 기록 탭 이동
3. 편집자 목록에 "비움 (원본)" 자동 표시 확인
4. 저장 기록에 "원본 생성" 표시 확인
```

---

## Phase 3 — saveLog editorName 제거

### 3.1 문제 요약

현재 saveLog 항목: `{ at, editorId, editorName }`.  
`editorName`은 `editors` 배열에 이미 있으므로 중복. 저장 누적 시 불필요한 데이터.

### 3.2 수정: `src/actions/export-import.js`

saveLog 항목 생성 시 editorName 제거:

```js
// 수정 전
{ at: now, editorId: editor.id, editorName: editor.name }

// 수정 후
{ at: now, editorId: editor.id }
```

### 3.3 수정: `src/components/shared/about.js`

저장 기록 렌더에서 editorName 참조 제거.  
editorId로 editors에서 이름을 조회하도록 변경:

```js
// 수정 전
entry.editorName || selectedEditor.name || '비움'

// 수정 후
editorById.get(entry.editorId)?.name || selectedEditor?.name || '비움'
```

**하위 호환**: 기존 저장된 파일에 editorName이 있을 수 있음.  
normalizeState에서 제거하지 않고 렌더에서만 무시하면 됨.

---

## Phase 4 — 히스토리 UI 2컬럼 레이아웃

### 4.1 현재 문제

가로 탭 방식은 편집자가 많아지면 줄바꿈 발생 및 공간 낭비.  
탭 전환 시 화면 전체가 리렌더되어 스크롤 위치 초기화.

### 4.2 새 레이아웃 구조

```
┌──────────────────────────────────────────────────────┐
│ 편집 기록                                             │
├──────────────┬───────────────────────────────────────┤
│ 비움    ●   │  비움  <bingeoul@gmail.com>            │
│              │  카드기록 12건 · 저장 3회              │
│ 편집자A      │  첫 기록 05-25 10:00 · 마지막 14:30   │
│ 편집자B      ├───────────────────────────────────────┤
│ 편집자C      │  ── 카드 기록 ──────────────────────  │
│              │  [수정] 연기법        05-25 14:30      │
│              │  [생성] 사성제        05-25 12:00      │
│              │  [삭제] 임시카드      05-25 10:00      │  ← 삭제된 카드도 표시
│              ├───────────────────────────────────────┤
│              │  ── 저장 기록 ──────────────────────  │
│              │  원본 생성            05-25 10:00      │
│              │  파일 저장            05-25 14:30      │
└──────────────┴───────────────────────────────────────┘
```

### 4.3 CSS 추가: `src/styles/components.css`

```css
/* ── About 히스토리 2컬럼 레이아웃 ─────────────────── */
.about-history-layout {
  display: grid;
  grid-template-columns: 11rem 1fr;
  gap: 0;
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  overflow: hidden;
  min-height: 20rem;
}

/* 좌측 편집자 목록 */
.about-editor-list {
  border-right: 1px solid hsl(var(--border));
  background: hsl(var(--muted) / 0.3);
  overflow-y: auto;
}

.about-editor-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 0.875rem;
  font-size: 0.8125rem;
  font-weight: 500;
  color: hsl(var(--muted-foreground));
  cursor: pointer;
  border-bottom: 1px solid hsl(var(--border));
  transition: background 0.12s, color 0.12s;
  user-select: none;
}

.about-editor-item:last-child { border-bottom: none; }

.about-editor-item:hover {
  background: hsl(var(--accent));
  color: hsl(var(--foreground));
}

.about-editor-item.active {
  background: hsl(var(--background));
  color: hsl(var(--foreground));
  font-weight: 600;
}

.about-editor-item-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: hsl(var(--primary));
  flex-shrink: 0;
  opacity: 0;
}
.about-editor-item.active .about-editor-item-dot { opacity: 1; }

.about-editor-item-origin-badge {
  font-size: 0.6rem;
  color: hsl(var(--muted-foreground));
  font-weight: 400;
}

/* 우측 기록 패널 */
.about-editor-detail {
  overflow-y: auto;
  background: hsl(var(--background));
}

.about-detail-header {
  padding: 0.875rem 1rem;
  border-bottom: 1px solid hsl(var(--border));
}

.about-detail-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: hsl(var(--foreground));
  margin-bottom: 0.15rem;
}

.about-detail-meta {
  font-size: 0.75rem;
  color: hsl(var(--muted-foreground));
}

.about-detail-section {
  padding: 0.5rem 1rem 0;
}

.about-detail-section-label {
  font-size: 0.625rem;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: hsl(var(--muted-foreground));
  padding: 0.5rem 0 0.25rem;
  border-bottom: 1px solid hsl(var(--border) / 0.5);
  margin-bottom: 0.25rem;
}

.about-detail-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.35rem 0;
  font-size: 0.8rem;
  border-bottom: 1px solid hsl(var(--border) / 0.4);
}
.about-detail-row:last-child { border-bottom: none; }

.about-detail-time {
  color: hsl(var(--muted-foreground));
  font-size: 0.72rem;
  flex-shrink: 0;
  min-width: 7.5rem;
}

.about-detail-content {
  color: hsl(var(--foreground));
  font-weight: 500;
}

/* acts type 뱃지 */
.about-act-badge {
  display: inline-block;
  padding: 0.1rem 0.35rem;
  border-radius: 3px;
  font-size: 0.68rem;
  font-weight: 600;
  flex-shrink: 0;
}
.about-act-badge.create { background: hsl(142 71% 92%); color: hsl(142 50% 28%); }
.about-act-badge.update { background: hsl(217 91% 92%); color: hsl(217 60% 35%); }
.about-act-badge.delete { background: hsl(0 84% 93%);   color: hsl(0 65% 38%); }
.dark .about-act-badge.create { background: hsl(142 40% 18%); color: hsl(142 60% 72%); }
.dark .about-act-badge.update { background: hsl(217 50% 20%); color: hsl(217 80% 75%); }
.dark .about-act-badge.delete { background: hsl(0 45% 20%);   color: hsl(0 75% 75%); }

/* 모바일: 상하 스택 */
@media (max-width: 600px) {
  .about-history-layout {
    grid-template-columns: 1fr;
  }
  .about-editor-list {
    border-right: none;
    border-bottom: 1px solid hsl(var(--border));
    max-height: 8rem;
    overflow-x: auto;
    overflow-y: hidden;
    display: flex;
    flex-direction: row;
  }
  .about-editor-item {
    flex-shrink: 0;
    border-bottom: none;
    border-right: 1px solid hsl(var(--border));
  }
}
```

### 4.4 JS 수정: `src/components/shared/about.js`

`_renderAboutHistory` 함수를 2컬럼 구조로 재작성:

```js
function _renderAboutHistory(wrap, esc) {
  const editors = S.meta.editors || [];
  const saveLog = S.meta.saveLog || [];
  const createdAt = S.meta.created
    ? new Date(S.meta.created).toLocaleString('ko-KR', { dateStyle: 'short', timeStyle: 'short' })
    : '';

  // editors 정렬: origin 먼저
  const sortedEditors = [
    ...editors.filter(e => e.isOrigin),
    ...editors.filter(e => !e.isOrigin)
  ];

  const editorById = new Map(editors.map(e => [e.id, e]));

  // 선택된 편집자 ID 결정
  const validId = sortedEditors.some(e => e.id === _historyEditorId)
    ? _historyEditorId
    : sortedEditors[0]?.id ?? null;
  _historyEditorId = validId;

  // ── 원본 섹션 ──
  wrap.insertAdjacentHTML('beforeend', `
    <div class="about-section-label">원본</div>
    <div class="about-history-card" style="margin-bottom:1.5rem">
      <div class="about-editor-row">
        <div class="about-editor-name">비움</div>
        <div class="about-editor-meta">원본 생성${createdAt ? ' · ' + esc(createdAt) : ''}</div>
      </div>
    </div>
    <div class="about-section-label">편집자 기록</div>
  `);

  if (!sortedEditors.length) {
    wrap.insertAdjacentHTML('beforeend',
      '<div class="about-history-card"><div class="about-history-empty">편집 이력이 없습니다.</div></div>'
    );
    return;
  }

  // ── 2컬럼 레이아웃 ──
  const layout = ce('div', 'about-history-layout');

  // 좌측: 편집자 목록
  const editorList = ce('div', 'about-editor-list');
  sortedEditors.forEach(editor => {
    const acts = _collectActsForEditor(editor.id);
    const item = ce('div', 'about-editor-item' + (editor.id === validId ? ' active' : ''));
    item.innerHTML = `
      <span class="about-editor-item-dot"></span>
      <span>${esc(editor.name || '비움')}${editor.isOrigin ? ' <span class="about-editor-item-origin-badge">(원본)</span>' : ''}</span>
      <span style="margin-left:auto;font-size:0.72rem;color:hsl(var(--muted-foreground))">${acts.length}</span>
    `;
    item.addEventListener('click', () => {
      _historyEditorId = editor.id;
      queueRender('about');
    });
    editorList.appendChild(item);
  });
  layout.appendChild(editorList);

  // 우측: 선택된 편집자 기록 패널
  const detail = ce('div', 'about-editor-detail');
  const selectedEditor = editorById.get(validId) ?? sortedEditors[0] ?? null;

  if (selectedEditor) {
    _renderEditorDetail(detail, selectedEditor, saveLog, esc);
  }

  layout.appendChild(detail);
  wrap.appendChild(layout);
}

function _renderEditorDetail(detail, editor, saveLog, esc) {
  const acts = _collectActsForEditor(editor.id);
  const editorSaveLog = saveLog.filter(e => e.editorId === editor.id);
  const typeLabel = { create: '생성', update: '수정', delete: '삭제' };

  // 시간 포맷 헬퍼
  const fmt = at => at
    ? new Date(at).toLocaleString('ko-KR', { dateStyle: 'short', timeStyle: 'short' })
    : '';

  // 헤더
  const firstAt = editorSaveLog[0]?.at || acts[0]?.at || editor.firstSavedAt || null;
  const lastAt = editorSaveLog.length
    ? editorSaveLog[editorSaveLog.length - 1].at
    : acts[0]?.at || editor.lastSavedAt || null;

  const header = ce('div', 'about-detail-header');
  header.innerHTML = `
    <div class="about-detail-name">
      ${esc(editor.name || '비움')}
      ${editor.email ? `<span style="font-weight:400;font-size:0.8rem;color:hsl(var(--muted-foreground))"> &lt;${esc(editor.email)}&gt;</span>` : ''}
      ${editor.isOrigin ? `<span class="about-editor-item-origin-badge" style="margin-left:0.4rem">(원본)</span>` : ''}
    </div>
    <div class="about-detail-meta">
      카드기록 ${acts.length}건 · 저장 ${editorSaveLog.length}회
      ${firstAt ? ' · 첫 기록 ' + fmt(firstAt) : ''}
      ${lastAt && lastAt !== firstAt ? ' · 마지막 ' + fmt(lastAt) : ''}
    </div>
  `;
  detail.appendChild(header);

  // 카드 기록 섹션
  const actSection = ce('div', 'about-detail-section');
  actSection.innerHTML = '<div class="about-detail-section-label">카드 기록</div>';
  if (!acts.length) {
    actSection.insertAdjacentHTML('beforeend',
      '<div style="padding:0.75rem 0;font-size:0.8125rem;color:hsl(var(--muted-foreground))">카드 기록이 없습니다.</div>'
    );
  } else {
    const sorted = [...acts]
      .sort((a, b) => (b.at ?? '').localeCompare(a.at ?? ''))
      .slice(0, 50);
    sorted.forEach(act => {
      const row = ce('div', 'about-detail-row');
      row.innerHTML = `
        <span class="about-detail-time">${fmt(act.at)}</span>
        <span class="about-act-badge ${act.type}">${typeLabel[act.type] || act.type}</span>
        <span class="about-detail-content">${esc(act.cardTitle)}</span>
      `;
      actSection.appendChild(row);
    });
    if (acts.length > 50) {
      actSection.insertAdjacentHTML('beforeend',
        `<div class="about-history-more">… 외 ${acts.length - 50}건</div>`
      );
    }
  }
  detail.appendChild(actSection);

  // 저장 기록 섹션
  const saveSection = ce('div', 'about-detail-section');
  saveSection.innerHTML = '<div class="about-detail-section-label">저장 기록</div>';
  if (!editorSaveLog.length) {
    saveSection.insertAdjacentHTML('beforeend',
      '<div style="padding:0.75rem 0;font-size:0.8125rem;color:hsl(var(--muted-foreground))">저장 기록이 없습니다.</div>'
    );
  } else {
    const recent = [...editorSaveLog].reverse().slice(0, 30);
    recent.forEach(entry => {
      const row = ce('div', 'about-detail-row');
      row.innerHTML = `
        <span class="about-detail-time">${fmt(entry.at)}</span>
        <span class="about-detail-content">${esc(entry.note || '파일 저장')}</span>
      `;
      saveSection.appendChild(row);
    });
    if (editorSaveLog.length > 30) {
      saveSection.insertAdjacentHTML('beforeend',
        `<div class="about-history-more">… 외 ${editorSaveLog.length - 30}건</div>`
      );
    }
  }
  detail.appendChild(saveSection);
}
```

### 4.5 About 페이지 max-width 조정

히스토리 탭에서는 2컬럼이 필요하므로 `about-wrap` max-width 확장:

```css
/* 기존 */
.about-wrap { max-width: 44rem; }

/* 히스토리 탭 진입 시 body 클래스 또는 탭 상태로 분기 */
/* 방법: _aboutTab === 'history'일 때 about-wrap에 클래스 추가 */
.about-wrap.wide { max-width: 56rem; }
```

`renderAbout()`에서 탭 전환 시 about-wrap에 `wide` 클래스 토글:

```js
// renderAbout() 내부
const aboutWrap = document.querySelector('.about-wrap');
if (aboutWrap) {
  aboutWrap.classList.toggle('wide', _aboutTab === 'history');
}
```

### 4.6 Phase 4 검증

- [ ] 편집자 2명 이상 등록 후 좌측 목록에 모두 표시
- [ ] 편집자 클릭 시 우측 패널 내용 전환
- [ ] 카드 기록 — 생성/수정/삭제 뱃지 색상 구분
- [ ] 저장 기록 — "원본 생성", "파일 저장" 텍스트 표시
- [ ] 영구삭제된 카드도 카드 기록에 표시 (삭제된 카드 타이틀 포함)
- [ ] 모바일(600px 이하) — 상하 스택으로 전환
- [ ] 다크모드 — 뱃지 색상 정상 표시

---

## 전체 수정 파일 요약

| 파일 | Phase | 작업 |
|------|-------|------|
| `package.json` | 0 | version → `0.0.3` |
| `build/inline.mjs` | 0 | SCHEMA_VERSION → 9 |
| `src/core/schema.js` | 1 | v9 마이그레이터 추가 (actLog 필드) |
| `src/core/normalize.js` | 1 | actLog 필드 보장 추가 |
| `src/actions/card-actions.js` | 1 | CARD_PURGE/PURGE_ALL에 actLog 이관 로직 |
| `src/data/init.js` | 2 | makeDefault에 비움 초기 편집자 + 원본 생성 saveLog |
| `src/actions/export-import.js` | 3 | saveLog 항목에서 editorName 제거 |
| `src/components/shared/about.js` | 1+3+4 | _collectActsForEditor actLog 통합, editorName 참조 제거, 2컬럼 레이아웃 |
| `src/styles/components.css` | 4 | 2컬럼 히스토리 레이아웃 CSS 추가 |

신규 파일 없음. 수정 파일 9개.

---

## 작업 순서

```
Phase 0 (버전) → Phase 1 (actLog) → 검증 → git commit
Phase 2 (비움 자동 등록) → 검증 → git commit
Phase 3 (saveLog 정리) → git commit
Phase 4 (UI 개선) → 검증 → git commit
node build/build.mjs → dist/ol-atlas_v0.0.3.html 확인
git tag v0.0.3
```

---

## 주의사항

### A. makeDefault 기존 카드에 acts 필드 없음

현재 `makeDefault()`의 초기 카드(`id: 1`, "OL에 오신 것을 환영합니다")에  
`acts` 필드가 없다. `normalizeCard`가 `if (!Array.isArray(card.acts)) card.acts = []`로  
처리하므로 런타임에서는 문제 없으나, 명시적으로 `acts: []`를 초기 카드에도 추가하면 일관성이 좋다.

### B. origin_biwoom ID 충돌 가능성

핑거프린트 기반 ID(`fp_xxxxxxxx`)와 `origin_biwoom` 고정 ID가  
다른 편집자 ID와 충돌할 가능성은 없다.  
단, 비움이 직접 파일을 편집하면 `fp_xxxxxxxx` 형태의 두 번째 "비움" 편집자가  
생성될 수 있다. 이것은 의도된 동작이다.  
(원본 비움 = 파일 생성자, fp 비움 = 실제 편집 세션)

### C. actLog 최대 1000개 초과 시

가장 오래된 항목부터 제거(`slice(-1000)`).  
영구삭제 빈도가 높은 사용 패턴에서는 초기 기록이 소실될 수 있으나  
일반적인 불교 컨텐츠 편집 패턴에서는 문제 없다.

---

*OL ATLAS v0.0.3 작업지시서 — 2026-05-25*
