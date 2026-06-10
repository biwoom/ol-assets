# OL ATLAS v0.0.6 독서뷰(Reader View) 작업지시서

> 기준 파일: `ol-atlas_v0.0.5.html` (6,996줄, schemaVersion 10) 산출물: `dist/ol-atlas_v0.0.6.html`

---

## ▌에이전트 터미널 권한 선언

아래 권한 범위 안에서만 작업한다.

**허용**

- 읽기: `cat`, `grep`, `find`, `diff`, `wc`, `sed -n`
- 쓰기: `str_replace` (단일 파일), `write_file`, `create_file`, `cp`, `mv`, `mkdir`, `rm` (단일 파일만)
- 실행: bash 스크립트·파이프, `node`, `node --check`, `npm run build`, `npm run dev`
- git: `status`, `diff`, `log`, `add`, `commit`, `tag`

**금지 — 별도 명시적 승인 없이 절대 불가**

- `rm -rf` (디렉토리 삭제)
- `git push`, `git reset --hard`, `git clean -fd`
- `npm install` (새 패키지 추가)
- 프로젝트 폴더 외부 파일 접근
- 네트워크 요청 (`fetch`, `curl`, `wget` 등)

---

## ▌하면 안 되는 일

1. **기존 문서뷰 편집 기능 수정 금지** — `dv-edit-btn`, `Pn()`, `on()`, `jn()` 등 편집 관련 JS 및 CSS 수정 불가
2. **라우터 `O()` 내부 수정 금지** — `'reader'` 케이스 추가만 허용. 기존 케이스 수정 불가
3. **기존 CSS 클래스 정의 수정 금지** — `.dv-*`, `.home-*` 는 읽기 참조만. 독서뷰는 `.rv-*` 전용 네임스페이스 사용
4. **`Pe()`, `_e()` 함수 수정 금지** — 독서뷰 전용 `_eR()` 함수를 별도로 신규 추가
5. **`buildExportHTML()` 수정 금지** — 내보내기 로직은 이번 작업 범위 밖
6. **여러 Phase 동시 작업 금지** — 반드시 Phase 순서대로, 각 Phase 검증 통과 후 다음 진행
7. **지시되지 않은 리팩토링 금지** — 주석 일괄 삭제, 변수명 변경, 코드 재구성 불가
8. **minify/bundle 임의 최적화 금지** — 빌드는 `npm run build` 한 번만 실행

---

## ▌Phase별 검증 원칙

**각 Phase의 검증 항목을 모두 통과해야 다음 Phase를 진행한다.**

통과하지 못한 항목이 하나라도 있으면 즉시 작업을 중단하고, 해당 Phase를 수정한 뒤 검증을 다시 실행한다. 다음 Phase로 넘어가지 않는다.

---

## ▌현재 코드베이스 핵심 참조

### 제거 대상: dv-read-mode 시스템

**CSS** (약 2602~2660줄)

```
.dv-readmode-btn { ... }
.dv-readmode-btn.active { ... }
body.dv-read-mode #header { ... }
body.dv-read-mode #sidebar { ... }
body.dv-read-mode .dv-layout { ... }
body.dv-read-mode .dv-layout > .dv-wrap { ... }
body.dv-read-mode .dv-toc { ... }
```

**JS** (6827줄 일대)

```
변수: Si = 'ol_docview_readmode', Ze (boolean), Se (타이머 객체)
함수: Nr(e)  — readMode 토글 실행
      Ti()   — dv-readmode-btn 상태 업데이트
      Hr()   — dv-readmode-btn DOM 생성/삽입
      Hn(e)  — mousemove/touchstart 이벤트 등록/해제
      Li(e)  — header/sidebar peek 핸들러 (mousemove)
      Ii(e)  — header/sidebar peek 핸들러 (touchstart)
Pt 핸들러: e==='document' 분기 내 Hr(), dv-read-mode 처리 블록
```

### 재사용 대상 (독서뷰에서 호출)

```
qt(cardId)       → { prev, next, idx, total } 반환
_r(card)         → 카드 본문 HTML 반환 (이미지 포함)
at()             → 현재 카드 목록 반환
pe(id)           → 현재 카드 id 설정 (j 변수)
O(viewName)      → 뷰 전환 라우터
Bt               → 테마 토글 함수
Vi(theme), Yn()  → 테마 상태 읽기
h                → 전역 상태 (h.cards, h.columns, h.userData 등)
j                → 현재 선택된 카드 id
I(str)           → XSS escape
b(tag, cls, txt) → createElement 헬퍼
_e(id)           → 문서뷰로 카드 열기 (편집 진입)
V(name, fn)      → 뷰 렌더러 등록
Pt(fn)           → 뷰 전환 훅 등록
```

### 독서뷰 DOM 구조

```
#view-reader
  ├── .rv-topbar              ← pill 헤더, scroll-hide
  │     └── .rv-nav
  │           OL로고 | [편집] [홈] [About] | 테마토글
  └── .rv-stage               ← flex row, 3열
        ├── .rv-side-left     ← 원형 토글 아이콘 + 문서 목록 패널
        ├── .rv-body-wrap     ← 중앙 본문 (max-width: 42rem)
        │     ├── .rv-meta    ← 메타 + 글자크기 A+/A-
        │     ├── .rv-title
        │     ├── .rv-content ← md-body 본문
        │     └── .rv-foot    ← 이전/다음 이동
        └── .rv-side-right    ← 원형 토글 아이콘 + TOC 패널
```

---

---

# Phase 1 — dv-read-mode 제거 및 readmode-btn 재연결

## 목표

기존 읽기 모드 시스템을 완전히 제거하고, `#dv-readmode-btn`이 독서뷰로 진입하도록 변경한다.

---

## Task 1-A: CSS 제거

**파일**: `src/styles/docview.css`

아래 블록을 완전히 삭제한다.

```
.dv-readmode-btn 정의 블록
.dv-readmode-btn.active 정의 블록
body.dv-read-mode 로 시작하는 모든 규칙 블록 전체
```

---

## Task 1-B: JS 변수·함수 6개 삭제

**파일**: `src/components/shared/docview.js`

아래 항목을 완전히 삭제한다.

```javascript
// 삭제: 변수 선언
var Si = 'ol_docview_readmode', Ze = localStorage.getItem(Si) === '1', Se = {};

// 삭제: 함수 6개
function Nr(e) { ... }
function Ti() { ... }
function Hr() { ... }
function Hn(e) { ... }
function Li(e) { ... }
function Ii(e) { ... }
```

---

## Task 1-C: Pt 핸들러 수정

`Pt` 핸들러 내 `e === 'document'` 분기에서 `Hr()`, `dv-read-mode` 관련 코드를 제거한다.

**수정 전**:

```javascript
Pt(e => {
  e === 'document'
    ? (Hr(), Ze && (document.body.classList.add('dv-read-mode'), Hn(true)))
    : (document.body.classList.remove('dv-read-mode'), Hn(false));
});
```

**수정 후**:

```javascript
Pt(e => {
  // dv-read-mode 제거됨. 독서뷰 전환은 _eR() 에서 처리.
});
```

---

## Task 1-D: dv-readmode-btn 클릭 이벤트 재연결

`Rr()` (renderDocview) 함수 내 view-bar 구성 시, 기존 `Hr()` 호출 대신 아래 버튼 삽입 코드를 추가한다. `dv-edit-btn` 삽입 직전에 위치시킨다.

```javascript
const readerBtn = document.createElement('button');
readerBtn.id = 'dv-readmode-btn';
readerBtn.className = 'btn sm';
readerBtn.title = '독서뷰로 보기';
readerBtn.innerHTML = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
  stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
  style="width:1rem;height:1rem;flex-shrink:0">
  <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
  <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
</svg>`;
readerBtn.onclick = () => { if (j != null) _eR(j); };
viewBarEl.insertBefore(readerBtn, dvEditBtn);
```

`_eR()` 함수는 Phase 3에서 구현한다. Phase 1에서는 클릭 시 아무 일도 없어도 된다.

---

## Phase 1 검증

```bash
# 구문 검사
node --check src/components/shared/docview.js

# 빌드
npm run build

# dv-read-mode 완전 제거 확인 (결과가 0이어야 통과)
grep -c "dv-read-mode" dist/ol-atlas_v0.0.6.html
grep -c "ol_docview_readmode" dist/ol-atlas_v0.0.6.html
```

**통과 기준 — 아래 항목을 모두 충족해야 Phase 2를 진행한다.**

- [ ] `grep -c "dv-read-mode"` 결과: 0
- [ ] `grep -c "ol_docview_readmode"` 결과: 0
- [ ] `Nr`, `Ti`, `Hr`, `Hn`, `Li`, `Ii` 함수 정의가 빌드 산출물에 없음
- [ ] 빌드 성공 (에러 없음)
- [ ] 브라우저에서 문서뷰 편집 버튼(편집, 저장, 취소)이 정상 동작
- [ ] 브라우저에서 문서뷰 view-bar에 책 아이콘 버튼이 표시됨
- [ ] 브라우저 콘솔에 JS 에러 없음

---

---

# Phase 2 — `#view-reader` HTML DOM 추가 + 기본 CSS

## 목표

독서뷰 전용 뷰 컨테이너를 HTML에 추가하고 기본 레이아웃 CSS를 작성한다.

---

## Task 2-A: HTML DOM 추가

**파일**: `src/index.html`

기존 `<!-- ⑤ About -->` 블록 바로 앞에 삽입한다.

```html
<!-- ⑥ 독서뷰 (Reader View) -->
<div class="view" id="view-reader">
  <header class="rv-topbar" id="rv-topbar">
    <nav class="rv-nav" aria-label="독서뷰 메뉴">
      <span class="rv-brand" id="rv-brand" tabindex="0" role="button" aria-label="홈으로">OL</span>
      <div class="rv-nav-divider"></div>
      <button class="rv-nav-btn" id="rv-edit-btn">편집</button>
      <button class="rv-nav-btn" id="rv-home-btn">홈</button>
      <button class="rv-nav-btn" id="rv-about-btn">About</button>
      <div class="rv-nav-divider"></div>
      <button class="rv-theme-btn" id="rv-theme-btn" aria-label="테마 전환">
        <span class="icon-sun"></span>
        <span class="icon-moon" style="display:none"></span>
        <span class="icon-book" style="display:none"></span>
      </button>
    </nav>
  </header>
  <div class="rv-stage" id="rv-stage">
    <!-- 좌측: 문서 목록 -->
    <div class="rv-side-left" id="rv-side-left">
      <button class="rv-toggle-icon" id="rv-toggle-list"
              title="문서 목록" aria-expanded="false">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
             width="18" height="18">
          <circle cx="12" cy="12" r="10"/>
          <line x1="8" y1="9"  x2="16" y2="9"/>
          <line x1="8" y1="12" x2="16" y2="12"/>
          <line x1="8" y1="15" x2="13" y2="15"/>
        </svg>
      </button>
      <div class="rv-panel rv-panel-left" id="rv-panel-left" aria-hidden="true">
        <div class="rv-doc-list" id="rv-doc-list"></div>
      </div>
    </div>
    <!-- 중앙: 본문 -->
    <div class="rv-body-wrap" id="rv-body-wrap">
      <div class="rv-meta"    id="rv-meta"></div>
      <h1  class="rv-title"   id="rv-title"></h1>
      <div class="rv-content md-body" id="rv-content"></div>
      <div class="rv-foot"    id="rv-foot"></div>
    </div>
    <!-- 우측: TOC -->
    <div class="rv-side-right" id="rv-side-right">
      <button class="rv-toggle-icon" id="rv-toggle-toc"
              title="목차" aria-expanded="false">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
             stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"
             width="18" height="18">
          <circle cx="12" cy="12" r="10"/>
          <line x1="9"  y1="9"  x2="15" y2="9"/>
          <line x1="9"  y1="12" x2="15" y2="12"/>
          <line x1="9"  y1="15" x2="13" y2="15"/>
        </svg>
      </button>
      <div class="rv-panel rv-panel-right" id="rv-panel-right" aria-hidden="true">
        <div class="rv-toc-inner" id="rv-toc-inner"></div>
      </div>
    </div>
  </div>
</div>
```

---

## Task 2-B: CSS 추가

**파일**: `src/styles/reader.css` 신규 생성 후 `src/main.js`에 `import './styles/reader.css'` 추가.

```css
/* ══════════════════════════════════════
   독서뷰 (rv-* 네임스페이스)
   ══════════════════════════════════════ */

#view-reader {
  display: none;
  flex-direction: column;
  min-height: 100vh;
  background: hsl(var(--background));
}
#view-reader.active { display: flex; }

/* 헤더 */
.rv-topbar {
  position: sticky;
  top: 1rem;
  z-index: 50;
  display: flex;
  justify-content: center;
  padding: 0 1rem;
  pointer-events: none;
  transition: transform 0.25s ease, opacity 0.25s ease;
}
.rv-topbar.rv-topbar-hidden {
  transform: translateY(-120%);
  opacity: 0;
  pointer-events: none;
}
.rv-nav {
  display: flex;
  align-items: center;
  gap: 0.125rem;
  padding: 0.375rem 0.75rem;
  background: hsl(var(--background) / 0.92);
  backdrop-filter: blur(12px);
  border: 1px solid hsl(var(--border));
  border-radius: 9999px;
  box-shadow: 0 1px 6px hsl(0 0% 0% / 0.06);
  pointer-events: all;
}
.rv-brand {
  font-size: 0.875rem;
  font-weight: 600;
  color: hsl(var(--foreground));
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  user-select: none;
}
.rv-brand:hover { background: hsl(var(--accent)); }
.rv-nav-divider {
  width: 1px;
  height: 1rem;
  background: hsl(var(--border));
  margin: 0 0.25rem;
}
.rv-nav-btn {
  font-size: 0.8125rem;
  color: hsl(var(--muted-foreground));
  background: transparent;
  border: none;
  border-radius: 9999px;
  padding: 0.25rem 0.625rem;
  cursor: pointer;
  transition: color 0.15s, background 0.15s;
}
.rv-nav-btn:hover {
  color: hsl(var(--foreground));
  background: hsl(var(--accent));
}
.rv-theme-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.75rem;
  background: transparent;
  border: none;
  border-radius: 9999px;
  cursor: pointer;
  color: hsl(var(--muted-foreground));
  transition: color 0.15s, background 0.15s;
}
.rv-theme-btn:hover {
  background: hsl(var(--accent));
  color: hsl(var(--foreground));
}
.rv-theme-btn svg { width: 0.875rem; height: 0.875rem; }

/* 스테이지 */
.rv-stage {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: flex-start;
  width: 100%;
  padding: 2.5rem 1rem 4rem;
}

/* 중앙 본문 */
.rv-body-wrap {
  flex: 0 0 auto;
  width: min(42rem, 100%);
  min-width: 0;
}

/* 좌우 사이드 컨테이너 */
.rv-side-left,
.rv-side-right {
  position: sticky;
  top: 5rem;
  display: flex;
  align-items: flex-start;
  height: 0;
  width: 0;
  overflow: visible;
}
.rv-side-left  { flex-direction: row-reverse; }
.rv-side-right { flex-direction: row; }

/* 원형 토글 아이콘 */
.rv-toggle-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  border: 1px solid hsl(var(--border));
  background: hsl(var(--background) / 0.85);
  backdrop-filter: blur(8px);
  color: hsl(var(--muted-foreground));
  cursor: pointer;
  transition: color 0.15s, background 0.15s, border-color 0.15s;
  position: relative;
  z-index: 10;
  flex-shrink: 0;
}
.rv-toggle-icon:hover,
.rv-toggle-icon.pinned {
  color: hsl(var(--foreground));
  border-color: hsl(var(--foreground) / 0.3);
  background: hsl(var(--background));
}

/* 사이드 패널 */
.rv-panel {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
  min-width: 11rem;
  max-width: 14rem;
  padding: 0.5rem 0;
  background: transparent;
}
.rv-panel.rv-panel-visible {
  opacity: 1;
  pointer-events: all;
}
.rv-panel-left  { margin-right: 0.75rem; }
.rv-panel-right { margin-left: 0.75rem; }

/* 문서 목록 */
.rv-doc-list { display: flex; flex-direction: column; }
.rv-doc-section-label {
  font-size: 0.6875rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: hsl(var(--muted-foreground) / 0.7);
  padding: 0.75rem 0.5rem 0.25rem;
}
.rv-doc-item {
  font-size: 0.8125rem;
  color: hsl(var(--muted-foreground));
  padding: 0.3125rem 0.5rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color 0.12s, background 0.12s;
  background: transparent;
  border: none;
  text-align: left;
  width: 100%;
}
.rv-doc-item:hover { color: hsl(var(--foreground)); background: hsl(var(--accent) / 0.4); }
.rv-doc-item.active { color: hsl(var(--foreground)); font-weight: 500; }

/* TOC */
.rv-toc-inner { display: flex; flex-direction: column; }
.rv-toc-item {
  font-size: 0.8rem;
  color: hsl(var(--muted-foreground));
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  cursor: pointer;
  text-decoration: none;
  display: block;
  transition: color 0.12s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.rv-toc-item:hover { color: hsl(var(--foreground)); }
.rv-toc-item.active { color: hsl(var(--foreground)); font-weight: 500; }
.rv-toc-h1 { padding-left: 0.5rem; }
.rv-toc-h2 { padding-left: 1rem; }
.rv-toc-h3 { padding-left: 1.625rem; font-size: 0.75rem; }

/* 메타 */
.rv-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.375rem;
  margin-bottom: 1rem;
  font-size: 0.8125rem;
  color: hsl(var(--muted-foreground));
}
.rv-meta-right { margin-left: auto; display: flex; align-items: center; gap: 0.25rem; }
.rv-font-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.75rem;
  border-radius: var(--radius-sm);
  border: 1px solid hsl(var(--border));
  background: transparent;
  color: hsl(var(--muted-foreground));
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.12s, background 0.12s;
}
.rv-font-btn:hover {
  color: hsl(var(--foreground));
  background: hsl(var(--accent));
}

/* 제목 */
.rv-title {
  font-size: 1.75rem;
  font-weight: 700;
  line-height: 1.25;
  color: hsl(var(--foreground));
  margin: 0 0 1.5rem;
  letter-spacing: -0.02em;
}

/* 본문 */
.rv-content {
  font-size: var(--rv-font-size, 1rem);
  line-height: 1.75;
  color: hsl(var(--foreground));
}

/* 하단 이동 */
.rv-foot {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin-top: 3rem;
  padding-top: 1.5rem;
  border-top: 1px solid hsl(var(--border));
}
.rv-nav-btn-page {
  display: flex;
  flex-direction: column;
  gap: 0.125rem;
  padding: 0.75rem 1rem;
  border-radius: var(--radius);
  border: 1px solid hsl(var(--border));
  background: transparent;
  cursor: pointer;
  transition: background 0.15s;
  max-width: 48%;
  text-align: left;
}
.rv-nav-btn-page.next-page { text-align: right; margin-left: auto; }
.rv-nav-btn-page:hover:not(:disabled) { background: hsl(var(--accent)); }
.rv-nav-btn-page:disabled { opacity: 0.35; cursor: default; }
.rv-nav-label { font-size: 0.75rem; color: hsl(var(--muted-foreground)); }
.rv-nav-title {
  font-size: 0.875rem;
  font-weight: 500;
  color: hsl(var(--foreground));
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 반응형 */
@media (max-width: 900px) {
  .rv-side-left, .rv-side-right { display: none; }
  .rv-body-wrap { width: 100%; }
}
@media (max-width: 640px) {
  .rv-stage { padding: 1.5rem 1rem 3rem; }
  .rv-title { font-size: 1.375rem; }
  .rv-topbar { top: 0.5rem; }
}
```

---

## Phase 2 검증

```bash
npm run build

# DOM 존재 확인 (결과가 1 이상이어야 통과)
grep -c "view-reader"  dist/ol-atlas_v0.0.6.html
grep -c "rv-body-wrap" dist/ol-atlas_v0.0.6.html
grep -c "rv-panel"     dist/ol-atlas_v0.0.6.html
```

**통과 기준 — 아래 항목을 모두 충족해야 Phase 3을 진행한다.**

- [ ] 빌드 성공 (에러 없음)
- [ ] `grep -c "view-reader"` 결과: 1 이상
- [ ] `grep -c "rv-body-wrap"` 결과: 1 이상
- [ ] 브라우저에서 기존 뷰(홈, 칸반, 문서뷰 등) 모두 정상 표시
- [ ] `.rv-*` 클래스가 기존 CSS와 충돌 없음 (브라우저 콘솔 에러 없음)

---

---

# Phase 3 — renderReader() JS 구현

## 목표

독서뷰 렌더링 함수 및 관련 유틸 함수를 구현하고 라우터에 등록한다.

---

## Task 3-A: `_eR()` 독서뷰 전환 함수

`_e()` 함수 정의 바로 아래에 추가한다.

```javascript
function _eR(id) {
  X = false;
  qe = '';
  pe(id);
  O('reader');
}
```

---

## Task 3-B: 독서뷰 상태 변수 선언

`V('docview', Rr)` 등록 코드 아래에 추가한다.

```javascript
var rvFontSize = (function() {
  try { return parseFloat(localStorage.getItem('ol_rv_fontsize')) || 1; } catch(e) { return 1; }
})();
var rvPanelLeftPinned  = false;
var rvPanelRightPinned = false;
var rvPanelLeftHover   = false;
var rvPanelRightHover  = false;
var rvTocObserver      = null;
```

---

## Task 3-C: 글자크기 함수

```javascript
function rvSetFont(delta) {
  rvFontSize = Math.min(1.25, Math.max(0.75, rvFontSize + delta));
  try { localStorage.setItem('ol_rv_fontsize', rvFontSize); } catch(e) {}
  var wrap = document.getElementById('rv-body-wrap');
  if (wrap) wrap.style.setProperty('--rv-font-size', rvFontSize + 'rem');
}
```

---

## Task 3-D: 패널 상태 관리 함수

```javascript
function rvUpdatePanel(side) {
  var panelId  = side === 'left' ? 'rv-panel-left'  : 'rv-panel-right';
  var toggleId = side === 'left' ? 'rv-toggle-list' : 'rv-toggle-toc';
  var panel    = document.getElementById(panelId);
  var toggle   = document.getElementById(toggleId);
  if (!panel) return;
  var pinned = side === 'left' ? rvPanelLeftPinned  : rvPanelRightPinned;
  var hover  = side === 'left' ? rvPanelLeftHover   : rvPanelRightHover;
  var show   = pinned || hover;
  panel.classList.toggle('rv-panel-visible', show);
  panel.setAttribute('aria-hidden', String(!show));
  if (toggle) toggle.classList.toggle('pinned', pinned);
}

function rvBindToggle(btnId, side) {
  var btn = document.getElementById(btnId);
  if (!btn || btn._rvBound) return;
  btn._rvBound = true;
  btn.addEventListener('mouseenter', function() {
    if (side === 'left') rvPanelLeftHover = true;
    else rvPanelRightHover = true;
    rvUpdatePanel(side);
  });
  btn.addEventListener('mouseleave', function() {
    if (side === 'left') rvPanelLeftHover = false;
    else rvPanelRightHover = false;
    rvUpdatePanel(side);
  });
  btn.addEventListener('click', function(e) {
    e.stopPropagation();
    if (side === 'left') rvPanelLeftPinned = !rvPanelLeftPinned;
    else rvPanelRightPinned = !rvPanelRightPinned;
    rvUpdatePanel(side);
    btn.setAttribute('aria-expanded',
      String(side === 'left' ? rvPanelLeftPinned : rvPanelRightPinned));
  });
}

function rvBindPanelHover(panelId, side) {
  var panel = document.getElementById(panelId);
  if (!panel || panel._rvPanelBound) return;
  panel._rvPanelBound = true;
  panel.addEventListener('mouseenter', function() {
    if (side === 'left') rvPanelLeftHover = true;
    else rvPanelRightHover = true;
    rvUpdatePanel(side);
  });
  panel.addEventListener('mouseleave', function() {
    if (side === 'left') rvPanelLeftHover = false;
    else rvPanelRightHover = false;
    rvUpdatePanel(side);
  });
}
```

---

## Task 3-E: 문서 목록 렌더링 함수

```javascript
function rvRenderDocList(currentId) {
  var list = document.getElementById('rv-doc-list');
  if (!list) return;
  list.innerHTML = '';
  h.columns.forEach(function(col) {
    var cards = h.cards.filter(function(c) { return c.colId === col.id; });
    if (!cards.length) return;
    var label = document.createElement('div');
    label.className = 'rv-doc-section-label';
    label.textContent = col.title;
    list.appendChild(label);
    cards.forEach(function(card) {
      var btn = document.createElement('button');
      btn.className = 'rv-doc-item' + (card.id === currentId ? ' active' : '');
      btn.textContent = card.title || '(제목 없음)';
      btn.title = card.title || '';
      btn.addEventListener('click', function() {
        _eR(card.id);
        rvPanelLeftPinned = false;
        rvUpdatePanel('left');
      });
      list.appendChild(btn);
    });
  });
}
```

---

## Task 3-F: TOC 렌더링 및 스크롤 하이라이트 함수

```javascript
function rvRenderToc(bodyHtml) {
  var inner = document.getElementById('rv-toc-inner');
  if (!inner) return;
  inner.innerHTML = '';
  var tmp = document.createElement('div');
  tmp.innerHTML = bodyHtml;
  var headings = tmp.querySelectorAll('h1[id], h2[id], h3[id]');
  headings.forEach(function(hEl) {
    var a = document.createElement('a');
    a.className = 'rv-toc-item rv-toc-' + hEl.tagName.toLowerCase();
    a.textContent = hEl.textContent;
    a.href = '#' + hEl.id;
    a.addEventListener('click', function(e) {
      e.preventDefault();
      var target = document.getElementById(hEl.id);
      if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    inner.appendChild(a);
  });
}

function rvInitTocObserver() {
  if (rvTocObserver) { rvTocObserver.disconnect(); rvTocObserver = null; }
  var content = document.getElementById('rv-content');
  if (!content) return;
  var headings = content.querySelectorAll('h1[id], h2[id], h3[id]');
  if (!headings.length) return;
  rvTocObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (!entry.isIntersecting) return;
      document.querySelectorAll('.rv-toc-item').forEach(function(item) {
        item.classList.toggle('active',
          item.getAttribute('href') === '#' + entry.target.id);
      });
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
  headings.forEach(function(hEl) { rvTocObserver.observe(hEl); });
}
```

---

## Task 3-G: 헤더 버튼 초기화 함수

```javascript
function rvInitNav() {
  var editBtn  = document.getElementById('rv-edit-btn');
  var homeBtn  = document.getElementById('rv-home-btn');
  var aboutBtn = document.getElementById('rv-about-btn');
  var themeBtn = document.getElementById('rv-theme-btn');
  var brand    = document.getElementById('rv-brand');
  if (editBtn  && !editBtn._rvInit)  { editBtn._rvInit  = true; editBtn.onclick  = function() { if (j != null) _e(j); else O('document'); }; }
  if (homeBtn  && !homeBtn._rvInit)  { homeBtn._rvInit  = true; homeBtn.onclick  = function() { O('home'); }; }
  if (aboutBtn && !aboutBtn._rvInit) { aboutBtn._rvInit = true; aboutBtn.onclick = function() { O('about'); }; }
  if (themeBtn && !themeBtn._rvInit) { themeBtn._rvInit = true; themeBtn.onclick = Bt; }
  if (brand    && !brand._rvInit)    { brand._rvInit    = true; brand.onclick    = function() { O('home'); }; }
}

function rvSyncThemeIcon() {
  var btn = document.getElementById('rv-theme-btn');
  if (!btn) return;
  var cur  = Vi(Yn());
  var sun  = btn.querySelector('.icon-sun');
  var moon = btn.querySelector('.icon-moon');
  var book = btn.querySelector('.icon-book');
  if (sun)  sun.style.display  = cur === 'light'   ? '' : 'none';
  if (moon) moon.style.display = cur === 'dark'    ? '' : 'none';
  if (book) book.style.display = cur === 'reading' ? '' : 'none';
}
```

---

## Task 3-H: `renderReader()` 메인 함수

```javascript
function renderReader() {
  var contentEl = document.getElementById('rv-content');
  var titleEl   = document.getElementById('rv-title');
  var metaEl    = document.getElementById('rv-meta');
  var footEl    = document.getElementById('rv-foot');
  var wrapEl    = document.getElementById('rv-body-wrap');
  if (!contentEl) return;

  if (!h.cards.length) {
    titleEl.textContent = '문서 없음';
    contentEl.innerHTML = '<p style="color:hsl(var(--muted-foreground))">카드를 추가하면 이곳에서 읽을 수 있습니다.</p>';
    metaEl.innerHTML = '';
    footEl.innerHTML = '';
    return;
  }

  var card = j != null ? h.cards.find(function(c) { return c.id === j; }) : null;
  if (!card) { card = at()[0] || h.cards[0]; if (card) pe(card.id); }
  if (!card) return;

  if (wrapEl) wrapEl.style.setProperty('--rv-font-size', rvFontSize + 'rem');

  titleEl.textContent = card.title || '(제목 없음)';

  var col    = h.columns.find(function(c) { return c.id === card.colId; });
  var status = h.userData.status[card.id] || 'wait';
  var pLabel = { high: '높음', mid: '보통', low: '낮음' }[card.priority] || '보통';
  var sLabel = { wait: '학습대기', doing: '학습중', done: '학습완료' }[status];
  var mHtml  = '';
  if (col) mHtml += '<span class="dv-meta-col"><span class="dv-meta-col-dot" style="background:' + (col.color || '#888') + '"></span>' + I(col.title) + '</span>';
  mHtml += '<span class="dv-meta-prio ' + (card.priority || 'mid') + '">' + pLabel + '</span>';
  mHtml += '<span class="dv-meta-status ' + status + '">' + sLabel + '</span>';
  if (card.tags && card.tags.length) {
    mHtml += '<span class="dv-meta-tags">' + card.tags.map(function(t) {
      return '<span class="dv-meta-tag">' + I(t) + '</span>';
    }).join('') + '</span>';
  }
  mHtml += '<span class="rv-meta-right">'
    + '<button class="rv-font-btn" id="rv-font-minus" title="글자 작게">A-</button>'
    + '<button class="rv-font-btn" id="rv-font-plus"  title="글자 크게">A+</button>'
    + '</span>';
  metaEl.innerHTML = mHtml;
  var fm = document.getElementById('rv-font-minus');
  var fp = document.getElementById('rv-font-plus');
  if (fm) fm.onclick = function() { rvSetFont(-0.0625); };
  if (fp) fp.onclick = function() { rvSetFont(+0.0625); };

  var bodyHtml = _r(card);
  contentEl.innerHTML = bodyHtml;

  rvRenderToc(bodyHtml);
  requestAnimationFrame(rvInitTocObserver);

  var nav  = qt(card.id);
  var prev = nav.prev, next = nav.next;
  footEl.innerHTML =
    '<button class="rv-nav-btn-page prev-page" id="rv-prev"' + (prev ? '' : ' disabled') + '>'
    + '<span class="rv-nav-label">← 이전</span>'
    + '<span class="rv-nav-title">' + (prev ? I(prev.title || '(제목 없음)') : '—') + '</span>'
    + '</button>'
    + '<button class="rv-nav-btn-page next-page" id="rv-next"' + (next ? '' : ' disabled') + '>'
    + '<span class="rv-nav-label">다음 →</span>'
    + '<span class="rv-nav-title">' + (next ? I(next.title || '(제목 없음)') : '—') + '</span>'
    + '</button>';
  if (prev) document.getElementById('rv-prev').onclick = function() { _eR(prev.id); };
  if (next) document.getElementById('rv-next').onclick = function() { _eR(next.id); };

  rvRenderDocList(card.id);

  rvBindToggle('rv-toggle-list', 'left');
  rvBindToggle('rv-toggle-toc',  'right');
  rvBindPanelHover('rv-panel-left',  'left');
  rvBindPanelHover('rv-panel-right', 'right');

  rvInitNav();
  rvSyncThemeIcon();
  rvInitScrollHide();

  var main = document.getElementById('main');
  if (main) main.scrollTop = 0;
}

V('reader', renderReader);
```

---

## Task 3-I: 라우터 `O()`에 헤더/사이드바 처리 추가

기존 `O()` 함수 내부, 뷰 전환 처리 블록에 아래 조건을 추가한다. 기존 케이스는 수정하지 않는다.

```javascript
var appHeader  = document.getElementById('header');
var appSidebar = document.getElementById('sidebar');
if (viewName === 'reader') {
  if (appHeader)  appHeader.style.display  = 'none';
  if (appSidebar) appSidebar.style.display = 'none';
} else {
  if (appHeader)  appHeader.style.display  = '';
  if (appSidebar) appSidebar.style.display = '';
}
```

---

## Phase 3 검증

```bash
node --check src/components/shared/docview.js
npm run build

grep -c "renderReader" dist/ol-atlas_v0.0.6.html
grep -c "rvFontSize"   dist/ol-atlas_v0.0.6.html
```

**통과 기준 — 아래 항목을 모두 충족해야 Phase 4를 진행한다.**

- [ ] `node --check` 에러 없음
- [ ] 빌드 성공
- [ ] 브라우저: 문서뷰 책 아이콘 클릭 → `#view-reader`로 전환됨
- [ ] 브라우저: 독서뷰에서 카드 본문이 마크다운 렌더링되어 표시됨
- [ ] 브라우저: 이전/다음 버튼 클릭 시 카드 이동됨
- [ ] 브라우저: 독서뷰 진입 시 기존 헤더(`#header`)와 사이드바(`#sidebar`) 숨겨짐
- [ ] 브라우저: 독서뷰에서 홈/편집/About 버튼 클릭 시 정상 전환, 헤더 복원됨
- [ ] 브라우저: 좌측 아이콘 hover → 문서 목록 fade-in
- [ ] 브라우저: hover 벗어나면 fade-out (pinned 아닌 경우)
- [ ] 브라우저: 아이콘 클릭 → 고정, 재클릭 → 숨김
- [ ] 브라우저 콘솔에 JS 에러 없음

---

---

# Phase 4 — scroll-hide 헤더 + 글자크기 최종 검증

## 목표

헤더 scroll-hide 동작을 완성하고 테마 아이콘 동기화를 마무리한다.

---

## Task 4-A: scroll-hide 헤더 함수

```javascript
var rvLastScrollY = 0;

function rvInitScrollHide() {
  var main = document.getElementById('main');
  if (!main || main._rvScrollBound) return;
  main._rvScrollBound = true;
  main.addEventListener('scroll', function() {
    var topbar   = document.getElementById('rv-topbar');
    if (!topbar) return;
    var currentY = main.scrollTop;
    if (currentY < 60) {
      topbar.classList.remove('rv-topbar-hidden');
    } else if (currentY > rvLastScrollY) {
      topbar.classList.add('rv-topbar-hidden');
    } else {
      topbar.classList.remove('rv-topbar-hidden');
    }
    rvLastScrollY = currentY;
  }, { passive: true });
}
```

`renderReader()` 내에 이미 `rvInitScrollHide()` 호출이 포함되어 있으므로 별도 호출 불필요.

**주의**: `#main`이 실제 스크롤 컨테이너가 아닐 경우 실제 id로 교체한다.

---

## Task 4-B: 테마 변경 시 독서뷰 아이콘 동기화

기존 `Xn()` 함수(테마 적용 함수) 마지막 줄에 추가한다.

```javascript
rvSyncThemeIcon();
```

---

## Phase 4 검증

```bash
npm run build
```

**통과 기준 — 아래 항목을 모두 충족해야 Phase 5를 진행한다.**

- [ ] 빌드 성공
- [ ] 독서뷰 스크롤 다운 시 헤더 숨겨짐 (transform 애니메이션)
- [ ] 스크롤 업 시 헤더 다시 나타남
- [ ] 최상단(scrollTop < 60)에서는 항상 헤더 표시
- [ ] `A+` 클릭 시 본문 글자 커짐 (최대 1.25rem)
- [ ] `A-` 클릭 시 본문 글자 작아짐 (최소 0.75rem)
- [ ] 새로고침 후 글자 크기 유지됨 (localStorage 확인)
- [ ] 테마 전환 시 독서뷰 헤더 아이콘이 올바르게 바뀜
- [ ] 브라우저 콘솔에 JS 에러 없음

---

---

# Phase 5 — 최종 빌드 및 통합 검증

## Task 5-A: package.json 버전 업데이트

```json
"version": "0.0.6"
```

## Task 5-B: 빌드

```bash
npm run build
ls dist/ol-atlas_v0.0.6.html
wc -l dist/ol-atlas_v0.0.6.html
```

## Task 5-C: 자동 검증 스크립트

```bash
echo "=== dv-read-mode 제거 확인 ==="
count=$(grep -c "dv-read-mode" dist/ol-atlas_v0.0.6.html 2>/dev/null || echo 0)
[ "$count" -eq 0 ] && echo "PASS" || echo "FAIL: dv-read-mode ${count}건 잔재"

count=$(grep -c "ol_docview_readmode" dist/ol-atlas_v0.0.6.html 2>/dev/null || echo 0)
[ "$count" -eq 0 ] && echo "PASS" || echo "FAIL: ol_docview_readmode ${count}건 잔재"

echo ""
echo "=== 독서뷰 DOM 확인 ==="
count=$(grep -c "view-reader" dist/ol-atlas_v0.0.6.html 2>/dev/null || echo 0)
[ "$count" -ge 1 ] && echo "PASS" || echo "FAIL: view-reader 없음"

count=$(grep -c "rv-body-wrap" dist/ol-atlas_v0.0.6.html 2>/dev/null || echo 0)
[ "$count" -ge 1 ] && echo "PASS" || echo "FAIL: rv-body-wrap 없음"

echo ""
echo "=== JS 함수 확인 ==="
count=$(grep -c "renderReader" dist/ol-atlas_v0.0.6.html 2>/dev/null || echo 0)
[ "$count" -ge 1 ] && echo "PASS" || echo "FAIL: renderReader 없음"

count=$(grep -c "rvFontSize" dist/ol-atlas_v0.0.6.html 2>/dev/null || echo 0)
[ "$count" -ge 1 ] && echo "PASS" || echo "FAIL: rvFontSize 없음"

echo ""
echo "=== 스키마 버전 (변경 없어야 함) ==="
grep -q "schemaVersion.*10" dist/ol-atlas_v0.0.6.html && echo "PASS: schemaVersion 10 유지" || echo "FAIL"

echo ""
echo "=== 빌드 버전 ==="
grep -q "version.*0.0.6" dist/ol-atlas_v0.0.6.html && echo "PASS: v0.0.6 확인" || echo "FAIL"
```

모든 항목이 `PASS`이어야 한다.

## Task 5-D: 브라우저 최종 체크리스트

`dist/ol-atlas_v0.0.6.html`을 브라우저에서 직접 열어 확인한다.

|시나리오|확인 항목|결과|
|---|---|---|
|앱 로드|홈 화면 정상 표시|□|
|칸반 보드|카드 추가/이동/삭제 정상|□|
|문서뷰 진입|카드 열리고 편집버튼 표시|□|
|문서뷰 → 독서뷰|책 아이콘 클릭 → 독서뷰 전환|□|
|독서뷰 본문|마크다운 렌더링 정상|□|
|독서뷰 이전/다음|하단 버튼으로 카드 이동|□|
|목록 패널 hover|좌측 아이콘 hover → 표시, 벗어나면 숨김|□|
|목록 패널 고정|클릭 → 고정, 스크롤 유지, 재클릭 → 숨김|□|
|TOC 패널|우측 아이콘 동작, 클릭 시 스크롤 이동|□|
|TOC 하이라이트|스크롤 중 현재 섹션 active 표시|□|
|글자크기|A+/A- 동작, 새로고침 후 유지|□|
|헤더 scroll-hide|다운 → 숨김, 업 → 표시|□|
|독서뷰 → 편집|편집 버튼 → 문서뷰 전환, 헤더 복원|□|
|독서뷰 → 홈/About|헤더 메뉴 → 정상 전환, 헤더 복원|□|
|테마 전환|독서뷰에서 테마 전환 정상|□|
|저장/내보내기|독서뷰 방문 후 저장 기능 정상|□|
|콘솔|JS 에러 없음|□|

**모든 항목이 통과되면 커밋한다.**

```bash
git add -A
git commit -m "feat: reader view (v0.0.6)"
git tag v0.0.6
```