# Phase 8.4 작업지시서 v2

# Phase 8.4 작업지시서 v2
**목표**: BOOK HTML을 열었을 때 독자용 UI로 동작하게 만들기  
**전제**: Phase 8.3 완료 — `window.__OL_MODE__='book'` 삽입, AUTHOR 번들 제거 확인됨

---

## 0. 현재 상태 (Phase 8.3 완료 시점)

| 항목 | 상태 |
|------|------|
| AUTHOR 번들 제거 | ✅ (kanban, cardgrid, listview, cover-editor 등 제거됨) |
| `window.__OL_MODE__='book'` | ✅ 삽입됨 |
| 데이터 삽입 | ✅ |
| 헤더 UI | ❌ 칸반/카드/리스트/문서뷰 버튼, 저장, 파일열기 그대로 노출 |
| 사이드바 | ❌ 컬럼 필터, 그룹 필터, 태그 검색, 표지 편집 그대로 노출 |
| 커버 페이지 | ❌ "읽기 시작"/목차 버튼이 둘 다 kanban으로 이동 |
| 카드 노출 | ❌ boot이 BOOK 모드를 감지하지 않아 빈 화면 |
| 문서뷰 편집 | ❌ 편집 버튼(카드 편집, + 카드 추가 등)이 그대로 노출 |

---

## 1. 설계 원칙

### 1.1 BOOK 모드 감지 방법
```js
const IS_BOOK = (typeof window.__OL_MODE__ !== 'undefined' && window.__OL_MODE__ === 'book');
```
이 플래그 하나로 전체 UI 분기. ATLAS에서는 `window.__OL_MODE__`가 undefined.

### 1.2 UI 숨김 전략 — CSS 클래스 방식
부트 시 `document.body.classList.add('book-mode')` 추가.  
신규 CSS 파일 `src/styles/book-mode.css`에서 `.book-mode` 셀렉터로 저자 UI를 숨김.  
JS 로직 변경을 최소화하고 CSS로 처리 가능한 것은 CSS로 처리.

### 1.3 디자인 레퍼런스 반영 — 레이아웃 패턴 중심
참조: Mainline Astro template (shadcn/ui + Tailwind 스타일, Linear-like 이슈 트래커)

레퍼런스에서 가져올 것: **"클린한 좌측 계층 네비게이션 + 우측 단일 콘텐츠 패널"이라는 레이아웃 패턴**  
레퍼런스를 그대로 따르지 않을 것: 이슈 트래커의 밀도감과 UI 언어 — BOOK은 독서 도구임

OL BOOK은 지식 정리 결과물을 조용히 읽는 경험이어야 함. 이 Phase에서 최소한의 형태로 잡아야 할 요소:
- 읽기에 적합한 본문 너비 (`max-width: 680px`)
- 편안한 줄간격과 폰트 크기
- 선택적 세피아/크림 배경 (manifest.display 토큰 대응, 단 Phase 8.4에서는 기본값 유지)

### 1.4 Phase 8.4 범위 명확화

| 항목 | Phase 8.4 | 이연 |
|------|-----------|------|
| 저자 UI 숨김 | ✅ | |
| 커버 페이지 → 읽기 라우팅 | ✅ | |
| 사이드바 챕터 네비게이션 | ✅ | |
| 문서뷰 읽기전용 | ✅ | |
| 독서 타이포그래피 (max-width, line-height) | ✅ | |
| 진행률 저장 (localStorage) | | Phase 8.5 |
| 책갈피 | | Phase 8.5 |
| 세피아 배경 토글 | | Phase 8.5 |

**진행률 localStorage에 대한 명시적 결정 (v1 검토의견 반영)**:  
`_bootBook()`에서 임베디드 데이터를 localStorage에 **저장하지 않는다**. 이유: 독자의 ATLAS 데이터를 덮어쓰는 위험 방지. 진행률 등 사용자 상태는 향후 bookId 기반 별도 localStorage 키(`ol_book_progress_{bookId}`)로 격리 저장 — Phase 8.5에서 구현.

---

## 2. 사전 확인 (작업 시작 전 필수)

### 2.1 핵심 함수 존재 확인

v1 검토의견에서 "함수명이 minify로 바뀔 수 있다"는 우려가 있었으나, 우리는 소스 ES모듈을 직접 작업하므로 해당 없음. 단, 아래 스텝으로 현재 상태를 명시적으로 확인 후 진행:

```bash
# init.js의 import 목록 확인
grep "^import" src/data/init.js
```

**예상 결과** (이미 확인됨):
- `bootState` ← `state.js` ✅
- `queueRender`, `flushNow` ← `render-queue.js` ✅  
- `switchView` ← `router.js` ✅
- `makeDefault`, `normalizeState`, `migrate` ✅

```bash
# getOrderedCardList 존재 확인
grep -n "getOrderedCardList" src/core/router.js
```
**예상 결과**: `router.js:95`에 `export function getOrderedCardList()` 존재 — **이미 구현되어 있음**. 신규 작성 불필요.

### 2.2 BOOK HTML 상태 확인

```bash
# BOOK HTML에서 __OL_MODE__ 확인
grep -c "window.__OL_MODE__='book'" 경로/BOOK파일명.html
# → 1 이어야 함

# init.js에 IS_BOOK 분기가 없는지 확인 (중복 작업 방지)
grep -n "IS_BOOK\|__OL_MODE__\|book-mode" src/data/init.js src/styles/base.css
```

---

## 3. Session 1 — 부트 & 헤더 & 독서 타이포그래피 (init.js + book-mode.css)

### 3.1 `src/data/init.js` 수정

**수정 위치**: `boot()` 함수 최상단 (devLog 직후)

```js
export function boot() {
  devLog('BOOT', 'boot start');

  // BOOK 모드 감지
  const IS_BOOK = (typeof window.__OL_MODE__ !== 'undefined' && window.__OL_MODE__ === 'book');
  if (IS_BOOK) {
    document.body.classList.add('book-mode');
    _bootBook();
    return;
  }

  // 기존 ATLAS 부트 로직 그대로...
```

**추가 함수** (같은 파일 하단, 기존 `boot()` 다음):

```js
function _bootBook() {
  devLog('BOOT', 'BOOK mode boot');

  // 1. 임베디드 데이터 로드 (localStorage에 저장하지 않음 — 독자 데이터 보호)
  let raw = makeDefault();
  try {
    if (typeof __LOADED_DATA_B64__ !== 'undefined' &&
        __LOADED_DATA_B64__ &&
        __LOADED_DATA_B64__ !== '__INIT_DATA_B64__') {
      const json = decodeURIComponent(escape(atob(__LOADED_DATA_B64__)));
      raw = normalizeState(migrate(JSON.parse(json)));
      devLog('BOOT', 'BOOK: loaded embedded data, cards=' + (raw.cards || []).length);
    }
  } catch(e) {
    devLog('BOOT', 'BOOK: embedded data load failed: ' + e.message);
  }

  // 2. 헤더 브랜드 영역에 BOOK 표시
  const brandMark = document.querySelector('.h-brand-mark-info');
  if (brandMark) brandMark.textContent = 'BOOK';

  // 3. state 초기화 (beforeunload 가드 없이 — BOOK은 읽기 전용)
  bootState(raw);

  // 4. 첫 렌더
  queueRender('__all__');
  flushNow();

  // 5. 커버 페이지로 시작
  const entryView = (raw.book && raw.book.manifest && raw.book.manifest.entry && raw.book.manifest.entry.view) || 'cover';
  switchView(entryView === 'cover' ? 'cover-page' : 'document');

  devLog('BOOT', 'BOOK boot complete');
}
```

**추가 import 없음** — `bootState`, `queueRender`, `flushNow`, `switchView`, `makeDefault`, `normalizeState`, `migrate` 모두 이미 import됨.

### 3.2 `src/styles/book-mode.css` 신규 생성

저자 UI 숨김 + **독서 타이포그래피** 포함:

```css
/* src/styles/book-mode.css */
/* BOOK 모드: 저자 UI 숨김 + 독서 경험 CSS */

/* ── 저자 UI 숨김 ──────────────────────────────── */

/* 헤더 네비게이션 (칸반/카드/리스트/문서뷰 버튼) */
.book-mode .h-nav { display: none; }

/* 저장/파일열기 드롭다운 */
.book-mode #save-dropdown,
.book-mode #open-dropdown { display: none; }

/* 모바일: 저장/열기 드롭다운 */
.book-mode #sb-save-dropdown,
.book-mode #sb-open-dropdown { display: none; }

/* dirty indicator */
.book-mode #dirty-indicator { display: none; }

/* 문서뷰 편집 버튼 (동적 생성 포함) */
.book-mode #dv-edit-btn,
.book-mode #dv-new-card-btn,
.book-mode .dv-edit-actions,
.book-mode .dv-card-actions-row { display: none !important; }

/* 문서뷰 이미지 패널 (편집 전용) */
.book-mode #dv-img-panel { display: none !important; }

/* 칸반 내 액션 버튼 */
.book-mode #new-card-btn,
.book-mode #add-col-btn { display: none; }

/* 뷰 전환 토글 */
.book-mode .view-toggle { display: none; }

/* ── 독서 타이포그래피 ──────────────────────────── */
/* 레퍼런스: Mainline의 단일 콘텐츠 패널 + 충분한 여백 패턴 */

/* 문서뷰 본문 읽기 너비 제한 */
.book-mode #view-document .dv-card-body,
.book-mode #view-document .dv-card-content {
  max-width: 680px;
  margin-left: auto;
  margin-right: auto;
}

/* 본문 줄간격 & 폰트 크기 */
.book-mode #view-document .dv-card-body {
  font-size: 1.05rem;
  line-height: 1.8;
}

/* 제목 여백 */
.book-mode #view-document .dv-card-title {
  max-width: 680px;
  margin-left: auto;
  margin-right: auto;
}

/* 이전/다음 카드 네비게이션 여백 조정 */
.book-mode #view-document .dv-nav {
  max-width: 680px;
  margin-left: auto;
  margin-right: auto;
}
```

**주의**: 위 CSS의 `.dv-card-body`, `.dv-card-content`, `.dv-card-title`, `.dv-nav` 등 실제 클래스명은 Session 1 시작 전 `src/components/shared/docview.js`를 Read하여 확인한 후 맞춰 수정할 것.

### 3.3 `build/inline.mjs`에 book-mode.css 추가

`CSS_FILES` 배열에 추가:
```js
const CSS_FILES = [
  // ... 기존 파일들 ...
  'src/styles/book-mode.css',   // ← 추가
];
```

### Session 1 완료 게이트
- `npm run build` 빌드 성공
- BOOK HTML을 브라우저로 열었을 때:
  - [ ] 커버 페이지가 기본으로 표시됨 (빈 화면 아님)
  - [ ] 헤더에 칸반/카드/리스트/문서뷰 탭 없음
  - [ ] 저장/파일열기 드롭다운 없음
  - [ ] 콘솔 에러 없음

---

## 4. Session 2 — BOOK 사이드바 & 커버 페이지 (sidebar.js + cover-page.js)

### 4.1 `src/components/shared/sidebar.js` 수정

`renderSidebar()` 함수 최상단에 BOOK 모드 분기 추가:

```js
function renderSidebar() {
  const el = document.getElementById('sb-inner');
  el.innerHTML = '';

  // BOOK 모드: 챕터 네비게이션으로 대체
  if (document.body.classList.contains('book-mode')) {
    renderSidebarForBook(el);
    return;
  }

  // 기존 ATLAS 사이드바 코드 그대로...
```

**신규 함수 추가** (파일 하단):

```js
function renderSidebarForBook(rootEl) {
  const manifest = (S.book && S.book.manifest) || {};

  // 책 제목/저자 섹션
  const titleSec = ce('div', 'sb-section sb-book-title-sec');
  titleSec.innerHTML = `
    <div class="sb-book-title">${escapeHTML(manifest.title || '(제목 없음)')}</div>
    ${manifest.author ? `<div class="sb-book-author">${escapeHTML(manifest.author)}</div>` : ''}
  `;
  rootEl.appendChild(titleSec);
  rootEl.appendChild(ce('div', 'sb-divider'));

  // 챕터(컬럼) → 카드 목록
  const navSec = ce('div', 'sb-section');
  navSec.appendChild(ce('div', 'sb-label', '목차'));

  S.columns.forEach(col => {
    const cardsInCol = (S.cards || []).filter(c => c.colId === col.id);
    if (!cardsInCol.length) return;

    const chapterWrap = ce('div', 'sb-book-chapter');

    const chapterHead = ce('div', 'sb-book-chapter-head');
    const dot = ce('span', 'sb-col-dot');
    dot.style.background = col.color;
    const chapterName = ce('span', 'sb-book-chapter-name', col.title);
    chapterHead.append(dot, chapterName);
    chapterWrap.appendChild(chapterHead);

    cardsInCol.forEach(card => {
      // ─── active 상태: 현재 문서뷰에 열린 카드 표시 ───
      const isActive = card.id === currentDocCardId;
      const item = ce('div', 'sb-book-card-item' + (isActive ? ' active' : ''));
      item.textContent = card.title || '(제목 없음)';
      item.onclick = () => {
        setCurrentDocCardId(card.id);
        switchView('document');
      };
      chapterWrap.appendChild(item);
    });

    navSec.appendChild(chapterWrap);
  });

  rootEl.appendChild(navSec);

  // 커버로 돌아가기
  rootEl.appendChild(ce('div', 'sb-divider'));
  const backSec = ce('div', 'sb-section');
  const backBtn = ce('div', 'sb-item');
  backBtn.innerHTML = `
    <span class="sb-item-icon">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
        <polyline points="9 22 9 12 15 12 15 22"></polyline>
      </svg>
    </span>
    <span>표지로 돌아가기</span>`;
  backBtn.onclick = () => switchView('cover-page');
  backSec.appendChild(backBtn);
  rootEl.appendChild(backSec);
}
```

**import 수정**: 파일 상단 router import에 `setCurrentDocCardId` 추가:
```js
import { currentView, currentDocCardId, setCurrentDocCardId } from '../../core/router.js';
```
(현재 `currentDocCardId`가 import되어 있는지 확인 후 추가)

### 4.2 `src/styles/sidebar.css`에 BOOK 사이드바 스타일 추가

파일 하단에 추가:

```css
/* ── BOOK 모드 사이드바 ────────────────────────── */
.sb-book-title-sec { padding: 0.75rem 0; }
.sb-book-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: hsl(var(--foreground));
  line-height: 1.4;
}
.sb-book-author {
  font-size: 0.75rem;
  color: hsl(var(--muted-foreground));
  margin-top: 0.25rem;
}
.sb-book-chapter { margin-bottom: 0.75rem; }
.sb-book-chapter-head {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0;
  font-size: 0.72rem;
  font-weight: 600;
  color: hsl(var(--muted-foreground));
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.sb-book-chapter-name { flex: 1; }
.sb-book-card-item {
  padding: 0.3rem 0 0.3rem 1.25rem;
  font-size: 0.8rem;
  color: hsl(var(--foreground));
  cursor: pointer;
  border-radius: var(--radius-sm, 4px);
  line-height: 1.4;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sb-book-card-item:hover {
  background: hsl(var(--accent));
  color: hsl(var(--accent-foreground));
}
.sb-book-card-item.active {
  background: hsl(var(--accent));
  color: hsl(var(--accent-foreground));
  font-weight: 500;
}
```

### 4.3 `src/components/reader/cover-page.js` 수정

현재 버그: "목차"와 "읽기 시작" 버튼이 둘 다 `switchView('kanban')`으로 연결됨.

```js
root.addEventListener('click', function(e) {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  if (btn.dataset.action === 'toc') {
    // 목차: 사이드바 오픈 (BOOK nav가 렌더되어 있음)
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.add('open');
    const overlay = document.getElementById('sb-overlay');
    if (overlay) overlay.classList.add('show');
  } else if (btn.dataset.action === 'start') {
    // 읽기 시작: 첫 카드 문서뷰로 이동
    const ordered = getOrderedCardList();
    if (ordered.length > 0) {
      setCurrentDocCardId(ordered[0].id);
      switchView('document');
    } else {
      // 카드 0개 예외 처리
      import('../../core/utils.js').then(({ toast }) => toast('읽을 카드가 없습니다', 'warning'));
    }
  }
});
```

**import 수정** (파일 상단):
```js
import { switchView, setCurrentDocCardId, getOrderedCardList } from '../../core/router.js';
```
`getOrderedCardList`는 `router.js:95`에 이미 export됨 — 신규 구현 불필요.

### Session 2 완료 게이트
- [ ] BOOK 사이드바에 챕터/카드 목록이 표시됨
- [ ] 카드 클릭 시 해당 카드의 문서뷰로 이동
- [ ] 사이드바에서 현재 읽는 카드에 active 하이라이트 표시됨
- [ ] "읽기 시작" → 첫 카드 문서뷰로 이동
- [ ] "목차" → 사이드바 오픈
- [ ] "표지로 돌아가기" → cover-page로 이동
- [ ] 카드 0개 BOOK에서 "읽기 시작" 클릭 시 에러 없음 (토스트 또는 무동작)
- [ ] 콘솔 에러 없음

---

## 5. Session 3 — 문서뷰 읽기 전용 처리 (docview.js)

### 5.1 작업 전 확인

```bash
# docview에서 동적으로 생성하는 편집 버튼 위치 확인
grep -n "edit-btn\|new-card\|dv-edit\|img-panel" src/components/shared/docview.js | head -30
```

편집 버튼이 정적 HTML에 있으면 `book-mode.css`로 이미 처리됨.  
동적 생성(JS로 createElement)하는 경우에만 `isBook` 조건 분기 추가 필요.

### 5.2 `src/components/shared/docview.js` 수정 (동적 생성 버튼 조건 추가)

렌더 함수 상단에 `isBook` 플래그 선언:
```js
function renderDocView() {   // 실제 함수명을 Read 후 확인
  const isBook = document.body.classList.contains('book-mode');
  // ...
}
```

동적으로 편집 버튼 생성하는 블록:
```js
// 기존 코드 패턴 (Read 후 실제 코드 확인)
if (!isBook) {
  // 편집 버튼, 이미지 패널 등 생성 코드
}
```

**중요**: docview.js 전체를 Read하지 않고 grep 결과만 보고 수정하지 말 것. 파일 전체를 Read한 후 정확한 위치를 확인하고 수정.

### 5.3 진행률 처리 — Phase 8.5로 이연

Phase 8.4에서는 진행률 저장하지 않음. 독자가 BOOK을 닫으면 상태 초기화.  
Phase 8.5에서 `ol_book_progress_{bookId}` 키로 localStorage에 격리 저장 예정.  
이 결정은 의도적 범위 축소이며, `_bootBook()`이 `localStorage.setItem()` 호출하지 않는 설계와 일관성 유지.

### Session 3 완료 게이트
- [ ] 문서뷰에서 편집 버튼, 이미지 패널 등이 보이지 않음
- [ ] 이전/다음 카드 네비게이션 작동 (기존 구현 확인)
- [ ] 콘솔 에러 없음

---

## 6. 전체 검증 체크리스트

새 BOOK 내보내기 후 브라우저에서 확인:

### 기능 체크
- [ ] 커버 페이지가 첫 화면으로 표시됨
- [ ] 표지 이미지/제목/부제/저자 표시됨
- [ ] "읽기 시작" 클릭 → 첫 카드 문서뷰
- [ ] "목차" 클릭 → 사이드바 오픈 + 챕터 목록 표시
- [ ] 사이드바에서 카드 클릭 → 해당 카드 문서뷰 이동
- [ ] 사이드바에 현재 카드 active 하이라이트 표시
- [ ] "표지로 돌아가기" → 커버 페이지 복귀
- [ ] 문서뷰 이전/다음 카드 이동

### UI 체크 (저자 UI 부재 확인)
- [ ] 헤더에 칸반/카드/리스트/문서뷰 탭 없음
- [ ] 저장 드롭다운 없음
- [ ] 파일 열기 드롭다운 없음
- [ ] 문서뷰에 편집 버튼 없음
- [ ] 사이드바에 컬럼 필터/태그 필터/표지 편집 없음

### 독서 타이포그래피 체크
- [ ] 문서뷰 본문이 좌우 중앙 정렬 + 최대 680px 너비로 제한됨
- [ ] 본문 폰트가 읽기 편한 크기/줄간격으로 표시됨

### 예외 체크
- [ ] 카드 0개 BOOK에서 에러 없음
- [ ] 콘솔 에러 없음
- [ ] ATLAS에서 열었을 때 기존 기능 정상 (book-mode.css가 ATLAS에 미적용 확인)

---

## 7. 수정 파일 목록 요약

| 파일 | 작업 | Session |
|------|------|---------|
| `src/data/init.js` | `_bootBook()` 추가, IS_BOOK 분기 | 1 |
| `src/styles/book-mode.css` | 신규 생성 — 저자 UI 숨김 + 독서 타이포그래피 | 1 |
| `build/inline.mjs` | CSS_FILES에 book-mode.css 추가 | 1 |
| `src/components/shared/sidebar.js` | `renderSidebarForBook()` 추가 (active 로직 포함) | 2 |
| `src/styles/sidebar.css` | BOOK 사이드바 스타일 추가 | 2 |
| `src/components/reader/cover-page.js` | 버튼 동작 수정 + 0카드 예외 처리 | 2 |
| `src/components/shared/docview.js` | 편집 버튼 조건부 생성 (읽기전용) | 3 |

---

## 8. 디자인 레퍼런스 → OL BOOK 매핑

참조: Mainline Astro template | URL: https://mainline-astro-template.vercel.app/

| 레퍼런스 요소 | OL BOOK 대응 | 구현 위치 |
|--------------|-------------|----------|
| 좌측 계층 네비 (상태 컬럼 → 이슈) | 챕터(컬럼) → 아티클(카드) | `renderSidebarForBook()` |
| 단일 우측 콘텐츠 패널 | 문서뷰 단독 | 기존 docview |
| 콘텐츠 최대 너비 제한 | `max-width: 680px` | `book-mode.css` |
| 클린한 구분선/여백 | `sb-divider` 활용 | 기존 CSS |
| 현재 위치 하이라이트 | `.sb-book-card-item.active` | `renderSidebarForBook()` |
| 최소화된 툴바 | 저자 UI 전부 숨김 | `book-mode.css` |

**레퍼런스를 따르지 않는 것**: 이슈 트래커의 밀도감 있는 카드 목록, 상태 배지 색상, 사용자 아바타 등 — BOOK은 조용한 독서 경험.

---

## 9. v1 → v2 변경 내역 (검토 의견 대응)

| 검토 의견 | 판정 | v2 반영 |
|----------|------|---------|
| 🔴 함수명 minify 우려 | **반박** — 소스 모듈 작업으로 해당 없음 | §2.1에 "이미 확인됨" 명시 |
| 🔴 `getOrderedCardList()` 존재 여부 | **반박** — `router.js:95`에 이미 있음 | §2.1 및 §4.3에 명시 |
| 🟡 active 상태 로직 누락 | **수용** | `renderSidebarForBook()`에 `currentDocCardId` 비교 추가 |
| 🟡 독서 타이포그래피 CSS 미포함 | **수용** | `book-mode.css`에 max-width/line-height 섹션 추가 |
| 🟡 localStorage 진행률 불일치 | **수용** | §1.4에 Phase 결정 명시, §5.3에 이연 근거 서술 |
| 총평: 독서 경험 미흡 | **수용** | §1.3 레퍼런스 해석 구분, §8 매핑 표 구체화 |

---

## 10. 참고 — 건드리지 않는 것

- `src/core/events.js` — BOOK HTML에서 이벤트 리스너 등록이 없는 요소는 자동으로 무해함
- `src/actions/export-import.js` — BOOK HTML에서 import 기능을 열 수 없으므로 실질적 영향 없음
- `src/core/dirty.js` — `installBeforeUnloadGuard()` BOOK에서 호출 안 함 → "변경사항 저장?" 팝업 없음
- `src/core/storage.js` — `_bootBook()`에서 `localStorage.setItem()` 호출하지 않아 독자 데이터 보존됨

---

*Phase 8.4 작업지시서 v2 — 2026-05-24*  
*v1 대비: 검토의견 6개 처리 (반박 2, 수용 4), active 로직 추가, 타이포그래피 CSS 추가, Phase 범위 명확화*
