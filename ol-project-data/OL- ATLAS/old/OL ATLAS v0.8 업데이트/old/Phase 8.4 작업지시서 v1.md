# Phase 8.4 작업지시서 v1
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
새 CSS 파일 `src/styles/book-mode.css`에서 `.book-mode` 셀렉터로 저자 UI를 숨김.  
JS 로직 변경을 최소화하고 CSS로 처리 가능한 것은 CSS로 처리.

### 1.3 디자인 레퍼런스 반영
참조: Mainline Astro template (shadcn/ui + Tailwind 스타일의 Linear-like 이슈 트래커)
- 사이드바: 챕터(컬럼) → 아티클(카드) 계층 목록 네비게이션
- 헤더: 브랜드명을 책 제목으로 교체, 독자용 최소 툴바
- 메인: 깨끗한 문서 읽기 뷰, 편집 UI 제거
- 진행률 표시: 전체 카드 중 읽은 카드 수 (선택적, manifest.display.showProgress 준수)

---

## 2. 사전 확인 (작업 시작 전 필수)

```bash
# BOOK HTML에서 __OL_MODE__ 확인
grep -c "window.__OL_MODE__='book'" 경로/OL-파일명.html
# → 1 이어야 함

# init.js에 IS_BOOK 분기가 없는지 확인 (중복 작업 방지)
grep -n "IS_BOOK\|__OL_MODE__\|book-mode" src/data/init.js src/styles/base.css
```

---

## 3. Session 1 — 부트 & 헤더 (init.js + book-mode.css)

### 3.1 `src/data/init.js` 수정

**수정 위치**: `boot()` 함수 최상단 (devLog 직후)  
**추가 내용**:

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

**추가 함수** (같은 파일 하단):

```js
function _bootBook() {
  devLog('BOOT', 'BOOK mode boot');

  // 1. 임베디드 데이터 로드 (localStorage 저장 없이)
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

  // 2. 헤더 브랜드명을 책 제목으로 교체
  const bookTitle = (raw.book && raw.book.manifest && raw.book.manifest.title) || 'OL BOOK';
  const brandMark = document.querySelector('.h-brand-mark-info');
  if (brandMark) brandMark.textContent = 'BOOK';
  const brandEl = document.querySelector('.h-brand');
  if (brandEl) brandEl.setAttribute('aria-label', bookTitle);

  // 3. state 초기화 (beforeunload 가드 없이)
  bootState(raw);

  // 4. 첫 렌더
  queueRender('__all__');
  flushNow();

  // 5. 커버 페이지로 시작 (manifest.entry.view 참조)
  const entryView = (raw.book && raw.book.manifest && raw.book.manifest.entry && raw.book.manifest.entry.view) || 'cover';
  if (entryView === 'cover') {
    switchView('cover-page');
  } else {
    switchView('document');
  }

  devLog('BOOT', 'BOOK boot complete');
}
```

**import 추가** (파일 상단):
```js
import { switchView } from '../core/router.js';
```
(이미 있으면 생략)

### 3.2 `src/styles/book-mode.css` 신규 생성

```css
/* src/styles/book-mode.css */
/* BOOK 모드에서 저자 전용 UI 숨김 */

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

/* 사이드바 저자 섹션 (컬럼 필터, 그룹 필터, 태그 검색, 표지 편집 버튼, BOOK 배포 버튼) */
/* sidebar.js에서 BOOK 모드용 별도 renderSidebar 분기로 처리 — CSS 숨김 불필요 */

/* 칸반/카드/리스트 뷰 자체를 BOOK에서 접근 불가 처리 (라우터에서 차단) */
/* view 요소는 display:none 기본값이므로 추가 숨김 불필요 */

/* 문서뷰 편집 버튼 숨김 */
.book-mode #dv-edit-btn,
.book-mode #dv-new-card-btn,
.book-mode .dv-edit-actions,
.book-mode .dv-card-actions-row { display: none !important; }

/* 문서뷰 이미지 패널 (편집 전용) */
.book-mode #dv-img-panel { display: none !important; }

/* 칸반 내 "+ 카드 추가" 버튼 영역 */
.book-mode #new-card-btn,
.book-mode #add-col-btn { display: none; }

/* 뷰 전환 토글 (view-bar 내 칸반/카드 버튼) */
.book-mode .view-toggle { display: none; }
```

### 3.3 `build/inline.mjs`에 book-mode.css 추가

현재 `CSS_FILES` 배열에 `book-mode.css` 추가:
```js
const CSS_FILES = [
  // ... 기존 파일들 ...
  'src/styles/book-mode.css',   // ← 추가
];
```

### Session 1 완료 게이트
- `npm run build` 빌드 성공
- BOOK HTML을 브라우저로 열었을 때:
  - [ ] 커버 페이지가 기본으로 표시됨
  - [ ] 헤더에 칸반/카드/리스트/문서뷰 버튼 없음
  - [ ] 저장/파일열기 드롭다운 없음
  - [ ] 콘솔 에러 없음

---

## 4. Session 2 — BOOK 사이드바 (sidebar.js + cover-page.js)

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

  // 책 제목 섹션
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
      const item = ce('div', 'sb-book-card-item');
      item.textContent = card.title || '(제목 없음)';
      item.onclick = () => {
        import('../../core/router.js').then(({ switchView, setCurrentDocCardId }) => {
          setCurrentDocCardId(card.id);
          switchView('document');
        });
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

**import 확인**: `switchView`가 이미 import되어 있으므로 별도 추가 불필요.  
단, `setCurrentDocCardId`는 현재 미import. 파일 상단 import 라인에 추가:
```js
import { currentView, currentDocCardId, setCurrentDocCardId } from '../../core/router.js';
```

### 4.2 `src/styles/sidebar.css`에 BOOK 사이드바 스타일 추가

파일 하단에 추가:

```css
/* ── BOOK 모드 사이드바 ── */
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
  font-weight: 500;
}
```

### 4.3 `src/components/reader/cover-page.js` 수정

현재 "목차"와 "읽기 시작" 버튼이 둘 다 `switchView('kanban')`으로 연결되어 있음.  
올바른 동작으로 수정:

```js
root.addEventListener('click', function(e) {
  const btn = e.target.closest('[data-action]');
  if (!btn) return;
  if (btn.dataset.action === 'toc') {
    // 목차: 사이드바를 펼쳐서 목차 보여주기 (사이드바가 BOOK nav로 렌더됨)
    // 데스크탑: 사이드바 토글; 모바일: 모바일 사이드바 오픈
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.add('open');
    const overlay = document.getElementById('sb-overlay');
    if (overlay) overlay.classList.add('show');
  } else if (btn.dataset.action === 'start') {
    // 읽기 시작: manifest.entry.startTarget에 따라 첫 카드로 이동
    const ordered = getOrderedCardList();
    if (ordered.length > 0) {
      setCurrentDocCardId(ordered[0].id);
      switchView('document');
    }
  }
});
```

**import 추가** (파일 상단):
```js
import { switchView, setCurrentDocCardId, getOrderedCardList } from '../../core/router.js';
```
(현재는 `switchView`만 import됨)

### Session 2 완료 게이트
- [ ] BOOK 사이드바에 챕터/카드 목록이 표시됨
- [ ] 카드 클릭 시 해당 카드의 문서뷰로 이동
- [ ] "읽기 시작" → 첫 카드 문서뷰로 이동
- [ ] "목차" → 사이드바 오픈
- [ ] "표지로 돌아가기" → cover-page로 이동
- [ ] 콘솔 에러 없음

---

## 5. Session 3 — 문서뷰 읽기 전용 + 진행률 (선택)

### 5.1 `src/components/shared/docview.js` 읽기 전용 처리

`renderDocView()` 또는 렌더 엔트리 함수 최상단에 추가:

```js
function renderDocView() {
  // BOOK 모드: 편집 UI 강제 숨김 (book-mode.css가 처리하지 못하는 동적 요소)
  const isBook = document.body.classList.contains('book-mode');
  // ... 이후 카드 렌더 시 편집 버튼 조건부 생성
```

docview에서 동적으로 생성되는 편집 버튼(카드 편집, 카드 삭제, + 카드 추가 등)에 대해:
```js
// 편집 버튼 생성 조건
if (!isBook) {
  // 편집 버튼, 이미지 패널 등 생성
}
```

**주의**: docview.js는 크기가 큼. 실제 수정 전 파일 전체를 Read하여 편집 버튼 생성 위치를 확인한 후 작업.

### 5.2 문서뷰 이전/다음 카드 네비게이션 확인

BOOK 모드에서 이전/다음 카드 이동이 이미 `getPrevNextCard()`로 구현되어 있는지 확인.  
구현되어 있으면 추가 작업 불필요.

### 5.3 진행률 표시 (manifest.display.showProgress === true인 경우)

`userData.status` 활용. BOOK 모드에서는 localStorage에 저장하지 않으므로,  
세션 내 임시 상태로만 관리 (페이지 새로고침 시 초기화 — 이 동작은 Phase 8.4 범위에서 허용).

구현 복잡도가 높으면 Phase 8.5로 이연.

### Session 3 완료 게이트
- [ ] 문서뷰에서 편집 버튼, 이미지 패널 등이 보이지 않음
- [ ] 이전/다음 카드 네비게이션 작동
- [ ] 콘솔 에러 없음

---

## 6. 전체 검증 체크리스트

BOOK HTML 내보내기 후 브라우저에서 확인:

### 기능 체크
- [ ] 커버 페이지가 첫 화면으로 표시됨
- [ ] 표지 이미지/제목/부제/저자 표시됨
- [ ] "읽기 시작" 클릭 → 첫 카드 문서뷰
- [ ] "목차" 클릭 → 사이드바 오픈 + 챕터 목록 표시
- [ ] 사이드바에서 카드 클릭 → 해당 카드 문서뷰 이동
- [ ] "표지로 돌아가기" → 커버 페이지 복귀
- [ ] 문서뷰 이전/다음 카드 이동

### UI 체크 (저자 UI 부재 확인)
- [ ] 헤더에 칸반/카드/리스트/문서뷰 탭 없음
- [ ] 저장 드롭다운 없음
- [ ] 파일 열기 드롭다운 없음
- [ ] 문서뷰에 편집 버튼 없음
- [ ] 사이드바에 컬럼 필터/태그 필터/표지 편집 없음

### 예외 체크
- [ ] 카드 0개 BOOK: 커버 페이지에서 "읽기 시작" 클릭해도 에러 없음 (토스트 등으로 안내)
- [ ] 콘솔 에러 없음
- [ ] ATLAS에서 열었을 때 기존 기능 정상 (book-mode.css가 ATLAS에는 적용 안 됨 확인)

---

## 7. 수정 파일 목록 요약

| 파일 | 작업 | Session |
|------|------|---------|
| `src/data/init.js` | `_bootBook()` 추가, IS_BOOK 분기 | 1 |
| `src/styles/book-mode.css` | 신규 생성 — 저자 UI 숨김 CSS | 1 |
| `build/inline.mjs` | CSS_FILES에 book-mode.css 추가 | 1 |
| `src/components/shared/sidebar.js` | `renderSidebarForBook()` 추가 | 2 |
| `src/styles/sidebar.css` | BOOK 사이드바 스타일 추가 | 2 |
| `src/components/reader/cover-page.js` | 버튼 동작 수정 | 2 |
| `src/components/shared/docview.js` | 읽기 전용 처리 | 3 |

---

## 8. 디자인 레퍼런스 적용 포인트

참조 디자인: Mainline Astro template (shadcn/ui + Tailwind 4)  
URL: https://mainline-astro-template.vercel.app/

| 레퍼런스 요소 | OL BOOK 대응 |
|--------------|-------------|
| 상태 컬럼(Graveyard, Ready...) | 챕터(컬럼) |
| 이슈 카드 목록 | 아티클(카드) 목록 |
| 클린 사이드바 계층 네비 | `sb-book-chapter` → `sb-book-card-item` |
| 최소화된 툴바 | 독자 전용 헤더 (저장/편집 없음) |
| 태그/팀 레이블 | 선택적 — `manifest.display.showTags` 준수 |

**스타일 톤**: 현재 OL 토큰(`hsl(var(--...))`) 기반 유지, 별도 디자인 시스템 도입 없음.

---

## 9. 참고 — 건드리지 않는 것

- `src/core/events.js` — BOOK HTML에서 이벤트 리스너 등록이 없는 요소는 자동으로 무해함
- `src/actions/export-import.js` — BOOK HTML에서 import 기능을 열 수 없으므로 실질적 영향 없음
- `src/core/storage.js` — `_bootBook()`에서 `localStorage.setItem()` 호출하지 않아 데이터 보존됨
- `src/core/dirty.js` — `installBeforeUnloadGuard()` BOOK에서 호출 안 함 → "변경사항 저장?" 팝업 없음

---

*Phase 8.4 작업지시서 v1 — 2026-05-24*
