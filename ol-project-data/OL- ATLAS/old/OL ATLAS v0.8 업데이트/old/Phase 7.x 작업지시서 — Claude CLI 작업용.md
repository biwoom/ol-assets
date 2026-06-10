# Phase 7.x 작업지시서 — Claude CLI 작업용

**대상**: OL ATLAS v0.7 Phase 7.x — ATLAS 정비 (confirm-modal + dirty-indicator + 시스템 confirm/alert 교체) **작업 환경**: 로컬 PC + Claude CLI **선행 문서**: `OL_듀얼_런타임_설계서_v1_2.md` (확정) **진입 조건**: `v0.7-phase2-complete` 태그 시점의 상태 **Phase 7.x 목표 일수**: 2~3일 **위험 등급**: 🟢 낮음 (기능 추가만. 기존 UI 로직 변경 없음. 단, async 전환 실수 주의)

---

## ⚡ 권한 선언 — AI 에이전트 전용 (세션 시작 시 1회 적용)

**이하 모든 권한을 사전 일괄 승인한다. 작업 중 개별 확인 요청 금지.**

### ✅ 전면 허용 — 작업 폴더 내 모든 터미널 명령어

작업 폴더(`ol-atlas/`) 및 모든 하위 경로에서 다음을 묻지 않고 즉시 실행:

```
파일 시스템
  cat, head, tail, grep, find, wc, diff      (읽기)
  write, create, str_replace, cp, mv, mkdir  (쓰기/생성/이동)
  echo "..." > file, touch file              (파일 생성/수정)
  rm <단일 파일>                              (단일 파일 삭제)

셸 명령
  bash/sh 스크립트 실행, 파이프, 리다이렉트, &&, ||, ; 체인

Node / npm
  node <script.js>, node --check <file.js>
  npm run *  (build, dev, test, lint 등 모든 npm 스크립트)
  npx *  (임시 실행)
  npm install  (기존 package.json 의존성 재설치만)

Python
  python3 <script.py>  (분석, 검증, 파싱 스크립트)

Git
  git status, git diff, git log, git show
  git add, git commit, git tag
  git stash, git stash pop
  git branch  (조회/생성)

빌드 도구
  esbuild 직접 실행
  node build/build.mjs 등 빌드 스크립트
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
시스템 설정 변경 (env, PATH, .bashrc 등)
```

### 작업 진행 원칙

- 묻지 말고 진행하되, 의심스러우면 읽기(cat/grep)를 먼저 한 후 수정
- 에러 발생 시 즉시 중단, 에러 전문을 사용자에게 보고
- 각 세션 종료 전 검증 게이트 통과 후 git commit 실행

---

## 0. Phase 7.x 개요

### 0.1 목적

Phase 8.0(ES modules 전환 + 듀얼 런타임 분기) 진입 전 ATLAS 자체를 정비한다.

1. **`customConfirm` / `customAlert`** — 시스템 `confirm()` / `alert()` 10개를 div 기반 커스텀 모달로 교체
2. **`dirty-indicator`** — dirty 상태를 헤더에 시각적으로 표시

### 0.2 작업 범위

|구분|내용|
|---|---|
|**신규 파일 4개**|`src/components/shared/confirm-modal.js`, `confirm-modal.css`, `dirty-indicator.js`, `dirty-indicator.css`|
|**수정 파일**|`src/core/dirty.js` (2줄 추가), `src/core/storage.js` (1곳), `src/core/router.js` (1곳), `src/components/docview-inline.js` (2곳), `src/components/about.js` (3곳), `src/components/kanban.js` (1곳), `src/components/card-modal.js` (1곳), `src/components/bulk-select.js` (1곳)|
|**빌드 수정**|`build/build.mjs` — JS_FILES, CSS_FILES 배열에 신규 파일 추가|

### 0.3 Phase 7.x 완료 후 상태

- 사용자 경험: ATLAS 동작 100% 동일. 모든 경고/확인 다이얼로그가 shadcn 스타일 커스텀 모달로 변경됨
- 헤더에 dirty 상태 "● 변경됨" / "✓ 저장됨" 표시
- `grep -E "(?<![a-zA-Z_])(confirm|alert)\s*\(" src/` 결과 0건

### 0.4 변경하지 않는 것

- 기존 UI 로직, Action Layer, reducer, store — 전혀 변경 없음
- 빌드 방식 — concat 방식 그대로 (ES modules 전환은 Phase 8.0)
- beforeunload 시스템 다이얼로그 — 브라우저 보안 정책상 변경 불가, 그대로 유지

---

## 1. 교체 대상 전체 목록 (실제 코드 기반)

Phase 2 완료 코드(`ol-atlas.html`)에서 확인된 10개 호출:

|#|함수|실제 메시지|소스 파일|교체 타입|
|---|---|---|---|---|
|1|`alert`|`"저장 실패: " + n.message`|`src/core/storage.js`|`customAlert` ⚠ danger|
|2|`confirm`|`"변경 사항이 저장되지 않았습니다. 다른 뷰로 이동하시겠습니까?"`|`src/core/router.js`|`customConfirm`|
|3|`confirm`|`"변경 사항이 저장되지 않았습니다. 다른 카드로 이동하시겠습니까?"`|`src/components/docview-inline.js`|`customConfirm`|
|4|`confirm`|`"변경 사항을 버리시겠습니까?"`|`src/components/docview-inline.js`|`customConfirm`|
|5|`confirm`|`"영구 삭제하시겠습니까? 되돌릴 수 없습니다."`|`src/components/about.js` (단건)|`customConfirm` ⚠ danger|
|6|`confirm`|`e.length + "개 카드를 영구 삭제하시겠습니까? 되돌릴 수 없습니다."`|`src/components/about.js` (일괄)|`customConfirm` ⚠ danger|
|7|`confirm`|`"휴지통을 완전히 비우시겠습니까? 되돌릴 수 없습니다."`|`src/components/about.js` (비우기)|`customConfirm` ⚠ danger|
|8|`confirm`|`n` (컬럼 삭제 경고 변수, 카드 수 포함)|`src/components/kanban.js`|`customConfirm` ⚠ danger|
|9|`confirm`|`"선택한 " + t.size + "개 카드를 휴지통으로 이동하시겠습니까?"`|`src/components/bulk-select.js`|`customConfirm`|
|10|`confirm`|`"이 카드를 휴지통으로 이동하시겠습니까?"`|`src/components/card-modal.js`|`customConfirm`|

> ⚠ danger: 파괴적/되돌릴 수 없는 동작. 확인 버튼이 빨간색, 기본 포커스가 취소 버튼.

---

## 2. 신규 모듈 코드

### 2.1 `src/components/shared/confirm-modal.js`

```js
// src/components/shared/confirm-modal.js
// Promise 기반 div 커스텀 모달. concat 방식이므로 전역 함수로 정의.

let _modalStack = [];
let _modalPrevFocus = null;

/**
 * @param {Object} opts
 * @param {string}  opts.title
 * @param {string}  opts.message          줄바꿈 \n 지원
 * @param {string}  [opts.confirmText]    기본 '확인'
 * @param {string}  [opts.cancelText]     기본 '취소'
 * @param {boolean} [opts.danger]         true이면 확인 버튼 빨간색
 * @param {boolean} [opts.defaultCancel]  기본 true. true이면 취소 버튼에 포커스
 * @returns {Promise<boolean>}
 */
function customConfirm(opts) {
  opts = opts || {};
  return new Promise(function(resolve) {
    _showModal({
      title:         opts.title        || '확인',
      message:       opts.message      || '',
      confirmText:   opts.confirmText  || '확인',
      cancelText:    opts.cancelText   || '취소',
      danger:        !!opts.danger,
      defaultCancel: opts.defaultCancel !== false,
      onConfirm: function() { resolve(true);  },
      onCancel:  function() { resolve(false); },
    });
  });
}

/**
 * @param {Object} opts
 * @param {string}  opts.title
 * @param {string}  opts.message
 * @param {string}  [opts.confirmText]    기본 '확인'
 * @param {boolean} [opts.danger]
 * @returns {Promise<void>}
 */
function customAlert(opts) {
  opts = opts || {};
  return new Promise(function(resolve) {
    _showModal({
      title:         opts.title       || '알림',
      message:       opts.message     || '',
      confirmText:   opts.confirmText || '확인',
      cancelText:    null,
      danger:        !!opts.danger,
      defaultCancel: false,
      onConfirm: function() { resolve(); },
    });
  });
}

function _ensureModalRoot() {
  let root = document.getElementById('ol-modal-root');
  if (!root) {
    root = document.createElement('div');
    root.id = 'ol-modal-root';
    document.body.appendChild(root);
  }
  return root;
}

function _showModal(o) {
  const root = _ensureModalRoot();
  _modalPrevFocus = document.activeElement;

  const overlay = document.createElement('div');
  overlay.className = 'ol-modal-overlay';

  const uid = 'olm-' + Date.now();
  const dialog = document.createElement('div');
  dialog.className = 'ol-modal-dialog' + (o.danger ? ' ol-modal-danger' : '');
  dialog.setAttribute('role', 'alertdialog');
  dialog.setAttribute('aria-modal', 'true');
  dialog.setAttribute('aria-labelledby', uid);

  const titleEl = document.createElement('div');
  titleEl.className = 'ol-modal-title';
  titleEl.id = uid;
  titleEl.textContent = o.title;

  const msgEl = document.createElement('div');
  msgEl.className = 'ol-modal-message';
  String(o.message || '').split('\n').forEach(function(line, i) {
    if (i > 0) msgEl.appendChild(document.createElement('br'));
    msgEl.appendChild(document.createTextNode(line));
  });

  const actions = document.createElement('div');
  actions.className = 'ol-modal-actions';

  let cancelBtn = null;
  if (o.cancelText) {
    cancelBtn = document.createElement('button');
    cancelBtn.type = 'button';
    cancelBtn.className = 'ol-modal-btn ol-modal-cancel';
    cancelBtn.textContent = o.cancelText;
    cancelBtn.addEventListener('click', function() {
      _closeModal(overlay);
      if (o.onCancel) o.onCancel();
    });
    actions.appendChild(cancelBtn);
  }

  const confirmBtn = document.createElement('button');
  confirmBtn.type = 'button';
  confirmBtn.className = 'ol-modal-btn ol-modal-confirm' +
    (o.danger ? ' ol-modal-confirm-danger' : '');
  confirmBtn.textContent = o.confirmText;
  confirmBtn.addEventListener('click', function() {
    _closeModal(overlay);
    if (o.onConfirm) o.onConfirm();
  });
  actions.appendChild(confirmBtn);

  dialog.appendChild(titleEl);
  dialog.appendChild(msgEl);
  dialog.appendChild(actions);
  overlay.appendChild(dialog);
  root.appendChild(overlay);

  // Esc → 취소, Enter → 현재 포커스 버튼의 기본 동작
  const onKey = function(e) {
    if (!root.contains(overlay)) return;
    if (e.key === 'Escape') {
      e.preventDefault();
      e.stopPropagation();
      if (cancelBtn) cancelBtn.click();
      else confirmBtn.click();
    }
  };
  document.addEventListener('keydown', onKey, true);
  overlay._cleanup = function() {
    document.removeEventListener('keydown', onKey, true);
  };

  // backdrop 클릭 → 취소
  overlay.addEventListener('mousedown', function(e) {
    if (e.target === overlay && cancelBtn) cancelBtn.click();
  });

  _modalStack.push(overlay);
  document.body.style.overflow = 'hidden';

  requestAnimationFrame(function() {
    if (o.defaultCancel && cancelBtn) cancelBtn.focus();
    else confirmBtn.focus();
  });
}

function _closeModal(overlay) {
  if (!overlay) return;
  if (overlay._cleanup) overlay._cleanup();
  const idx = _modalStack.indexOf(overlay);
  if (idx >= 0) _modalStack.splice(idx, 1);
  if (overlay.parentNode) overlay.parentNode.removeChild(overlay);
  if (_modalStack.length === 0) {
    // 카드 모달이 열려있으면 overflow 복구 안 함
    const cardModal = document.getElementById('card-modal');
    if (!cardModal || !cardModal.classList.contains('open')) {
      document.body.style.overflow = '';
    }
    if (_modalPrevFocus) {
      try { _modalPrevFocus.focus(); } catch(e) {}
      _modalPrevFocus = null;
    }
  }
}
```

### 2.2 `src/components/shared/confirm-modal.css`

```css
/* src/components/shared/confirm-modal.css */

.ol-modal-overlay {
  position: fixed;
  inset: 0;
  background: hsl(0 0% 0% / 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 300;
  padding: 1rem;
  animation: olModalFadeIn 120ms ease;
}

@keyframes olModalFadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

.ol-modal-dialog {
  background: hsl(var(--background));
  color: hsl(var(--foreground));
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  box-shadow: 0 20px 60px hsl(0 0% 0% / 0.20), 0 4px 16px hsl(0 0% 0% / 0.10);
  max-width: 28rem;
  width: 100%;
  padding: 1.5rem;
  animation: olModalSlideIn 180ms cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes olModalSlideIn {
  from { transform: translateY(8px) scale(0.97); opacity: 0; }
  to   { transform: translateY(0) scale(1);      opacity: 1; }
}

.ol-modal-danger .ol-modal-title {
  color: hsl(var(--destructive));
}

.ol-modal-title {
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.625rem;
  line-height: 1.4;
}

.ol-modal-message {
  font-size: 0.875rem;
  line-height: 1.65;
  color: hsl(var(--muted-foreground));
  margin-bottom: 1.5rem;
  white-space: pre-wrap;
  word-break: break-word;
}

.ol-modal-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.ol-modal-btn {
  padding: 0.45rem 1rem;
  font-size: 0.875rem;
  font-weight: 500;
  border-radius: calc(var(--radius) - 2px);
  border: 1px solid hsl(var(--border));
  background: hsl(var(--background));
  color: hsl(var(--foreground));
  cursor: pointer;
  transition: background 100ms, border-color 100ms;
  line-height: 1.5;
}

.ol-modal-btn:hover       { background: hsl(var(--muted)); }
.ol-modal-btn:focus-visible {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 2px;
}

.ol-modal-confirm {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  border-color: hsl(var(--primary));
}
.ol-modal-confirm:hover { background: hsl(var(--primary) / 0.88); }

.ol-modal-confirm-danger {
  background: hsl(var(--destructive));
  color: hsl(var(--destructive-foreground));
  border-color: hsl(var(--destructive));
}
.ol-modal-confirm-danger:hover { background: hsl(var(--destructive) / 0.88); }

@media (max-width: 480px) {
  .ol-modal-actions     { flex-direction: column-reverse; }
  .ol-modal-btn         { width: 100%; padding: 0.625rem 1rem; text-align: center; }
}
```

### 2.3 `src/components/shared/dirty-indicator.js`

```js
// src/components/shared/dirty-indicator.js

let _dirtyEl = null;
let _fadeTimer = null;
const DIRTY_FADE_DELAY = 5000;

function _ensureDirtyEl() {
  if (_dirtyEl && _dirtyEl.isConnected) return _dirtyEl;
  // 헤더에 삽입 시도
  const header = document.querySelector(
    '.h-header, #h-header, .app-header, header'
  );
  _dirtyEl = document.createElement('div');
  _dirtyEl.id = 'ol-dirty-indicator';
  _dirtyEl.className = 'dirty-ind';
  _dirtyEl.setAttribute('aria-live', 'polite');
  _dirtyEl.setAttribute('aria-atomic', 'true');
  if (header) {
    header.appendChild(_dirtyEl);
  } else {
    _dirtyEl.classList.add('dirty-ind-floating');
    document.body.appendChild(_dirtyEl);
  }
  return _dirtyEl;
}

function renderDirtyIndicator() {
  const el = _ensureDirtyEl();
  const dirty = isDirty();
  clearTimeout(_fadeTimer);
  el.classList.remove('dirty-ind-dirty', 'dirty-ind-clean', 'dirty-ind-hidden');
  if (dirty) {
    el.classList.add('dirty-ind-dirty');
    el.textContent = '● 변경됨';
  } else {
    el.classList.add('dirty-ind-clean');
    el.textContent = '✓ 저장됨';
    _fadeTimer = setTimeout(function() {
      if (_dirtyEl) {
        _dirtyEl.classList.remove('dirty-ind-clean');
        _dirtyEl.classList.add('dirty-ind-hidden');
      }
    }, DIRTY_FADE_DELAY);
  }
}

subscribe('dirty-indicator', renderDirtyIndicator);
```

### 2.4 `src/components/shared/dirty-indicator.css`

```css
/* src/components/shared/dirty-indicator.css */

.dirty-ind {
  display: inline-flex;
  align-items: center;
  font-size: 0.72rem;
  font-weight: 500;
  padding: 0.2rem 0.55rem;
  border-radius: 9999px;
  line-height: 1;
  transition: opacity 400ms ease;
  user-select: none;
  pointer-events: none;
  white-space: nowrap;
  margin-left: auto;
}

.dirty-ind-dirty {
  background: hsl(38 90% 90%);
  color: hsl(38 60% 28%);
  opacity: 1;
}
.dirty-ind-clean {
  background: hsl(142 60% 90%);
  color: hsl(142 40% 26%);
  opacity: 0.85;
}
.dirty-ind-hidden { opacity: 0; }

:root.dark .dirty-ind-dirty { background: hsl(38 40% 20%); color: hsl(38 80% 68%); }
:root.dark .dirty-ind-clean { background: hsl(142 25% 18%); color: hsl(142 50% 65%); }

.dirty-ind-floating {
  position: fixed;
  bottom: 4.5rem;
  right: 1rem;
  z-index: 150;
  box-shadow: 0 2px 8px hsl(0 0% 0% / 0.15);
  pointer-events: none;
}
```

---

## 3. `src/core/dirty.js` 수정 — 2줄 추가

`markDirty`와 `markClean` 각각 마지막에 `queueRender('dirty-indicator')` 추가.

```
// markDirty 끝에 추가:
queueRender('dirty-indicator');

// markClean 끝에 추가:
queueRender('dirty-indicator');
```

---

## 4. 파일별 교체 명세

### 핵심 변환 규칙

`confirm()`은 동기, `customConfirm()`은 Promise 비동기 → **호출 함수가 `async`이어야 한다**.

```js
// Before (동기)
function doDelete() {
  if (!confirm("삭제하시겠습니까?")) return;
  dispatch(...);
}

// After (비동기)
async function doDelete() {
  const ok = await customConfirm({ title: '삭제', message: '삭제하시겠습니까?' });
  if (!ok) return;
  dispatch(...);
}
```

---

### 4.1 `src/core/storage.js` — alert 1개

catch 블록의 `alert("저장 실패: " + n.message)` 교체:

```js
// After
customAlert({
  title: '저장 실패',
  message: '저장 중 오류가 발생했습니다:\n' + (n.message || String(n)),
  danger: true,
});
// await 불필요 — 오류 알림 후 흐름 계속
```

---

### 4.2 `src/core/router.js` — confirm 1개

`switchView` 함수 안의 confirm 처리. **wrapper 패턴** 사용 (switchView 호출처가 많아서 전부 async로 바꾸는 것보다 안전).

```js
// After: switchView 상단 조건을 async wrapper로 분리
function switchView(e) {
  // confirm이 필요한 상황이면 async 경로로 위임
  if (currentView === "document" && e !== "document"
      && typeof dvEditing !== 'undefined' && dvEditing
      && typeof isDvEditDirty === 'function' && isDvEditDirty()) {
    _switchViewAsync(e);
    return;
  }
  _switchViewCore(e);
}

async function _switchViewAsync(e) {
  const ok = await customConfirm({
    title: '뷰 전환',
    message: '저장되지 않은 변경사항이 있습니다.\n다른 뷰로 이동하시겠습니까?',
    confirmText: '이동',
    cancelText: '취소',
  });
  if (!ok) return;
  _switchViewCore(e);
}

function _switchViewCore(e) {
  // 기존 switchView 본체 전체
  // (첫 번째 confirm 조건 제거, 나머지 그대로)
  if (e !== "document") {
    if (typeof dvEditing !== 'undefined') {
      dvEditing = false;
      dvEditOriginal = "";
    }
  }
  // ... 이하 기존 로직 그대로 ...
}
```

---

### 4.3 `src/components/docview-inline.js` — confirm 2개

**goToDocCard 함수**:

```js
// After
async function goToDocCard(e) {
  if (dvEditing && isDvEditDirty()) {
    const ok = await customConfirm({
      title: '카드 이동',
      message: '저장되지 않은 변경사항이 있습니다.\n다른 카드로 이동하시겠습니까?',
      confirmText: '이동',
      cancelText: '취소',
    });
    if (!ok) return;
  }
  dvEditing = false; dvEditOriginal = "";
  // 기존 나머지 로직 그대로
}
```

**cancelInlineEdit 함수**:

```js
// After
async function cancelInlineEdit() {
  if (!dvEditing) return;
  if (isDvEditDirty()) {
    const ok = await customConfirm({
      title: '편집 취소',
      message: '변경사항을 버리시겠습니까?',
      confirmText: '버리기',
      cancelText: '계속 편집',
    });
    if (!ok) return;
  }
  dvEditing = false; dvEditOriginal = "";
  // 기존 나머지 로직 그대로
}
```

---

### 4.4 `src/components/about.js` — confirm 3개

**trash 단건 영구삭제** (`_trashDelCard` 또는 클릭 핸들러):

```js
// After
async function _trashDelCard(id) {
  id = Number(id);
  const ok = await customConfirm({
    title: '⚠ 영구 삭제',
    message: '이 카드를 영구적으로 삭제합니다.\n\n되돌릴 수 없습니다.',
    confirmText: '영구 삭제', cancelText: '취소',
    danger: true, defaultCancel: true,
  });
  if (!ok) return;
  dispatch(purgeCard(id));
  toast("영구 삭제되었습니다");
}
```

**trash 일괄 영구삭제** (trash-del-sel-btn 핸들러):

```js
// After — 핸들러를 async로
document.getElementById("trash-del-sel-btn").addEventListener("click", async function() {
  const ids = [...document.querySelectorAll(".trash-cb:checked")].map(t => Number(t.dataset.id));
  if (!ids.length) return;
  const ok = await customConfirm({
    title: '⚠ 영구 삭제',
    message: ids.length + "개 카드를 영구적으로 삭제합니다.\n\n되돌릴 수 없습니다.",
    confirmText: '영구 삭제', cancelText: '취소',
    danger: true, defaultCancel: true,
  });
  if (!ok) return;
  ids.forEach(id => dispatch(purgeCard(Number(id))));
  toast("영구 삭제되었습니다");
});
```

**휴지통 비우기** (trash-empty-btn 핸들러):

```js
// After
document.getElementById("trash-empty-btn").addEventListener("click", async function() {
  if (!(S.trash || []).length) { toast("이미 비어 있습니다"); return; }
  const ok = await customConfirm({
    title: '⚠ 휴지통 비우기',
    message: '휴지통의 모든 카드를 영구적으로 삭제합니다.\n\n되돌릴 수 없습니다.',
    confirmText: '모두 삭제', cancelText: '취소',
    danger: true, defaultCancel: true,
  });
  if (!ok) return;
  dispatch(purgeAllCards());
  toast("휴지통을 비웠습니다");
});
```

---

### 4.5 `src/components/kanban.js` — confirm 1개

**`_kbDeleteColumn` 함수**:

```js
// After
async function _kbDeleteColumn(e) {
  const t = S.cards.filter(s => s.colId === e).length;
  const message = t
    ? `이 컬럼에는 ${t}개의 카드가 있습니다.\n컬럼과 카드 모두 삭제됩니다. 계속하시겠습니까?`
    : '이 컬럼을 삭제하시겠습니까?';
  const ok = await customConfirm({
    title: '컬럼 삭제', message,
    confirmText: '삭제', cancelText: '취소',
    danger: t > 0, defaultCancel: t > 0,
  });
  if (!ok) return;
  dispatch(deleteColumn(e));
  toast("컬럼이 삭제되었습니다");
}
```

---

### 4.6 `src/components/bulk-select.js` — confirm 1개

**`_bsDeleteCards` 함수**:

```js
// After
async function _bsDeleteCards(e) {
  const t = getBulkSet(e);
  if (!t.size) return;
  const ok = await customConfirm({
    title: '선택 카드 삭제',
    message: `선택한 ${t.size}개 카드를 휴지통으로 이동하시겠습니까?\n\n휴지통에서 복원할 수 있습니다.`,
    confirmText: '휴지통으로', cancelText: '취소',
  });
  if (!ok) return;
  // 기존 나머지 로직 그대로
}
```

---

### 4.7 `src/components/card-modal.js` — confirm 1개

**`_cmDeleteCard` 함수**:

```js
// After
async function _cmDeleteCard() {
  if (!editCard) return;
  const ok = await customConfirm({
    title: '카드 삭제',
    message: '이 카드를 휴지통으로 이동하시겠습니까?\n\n휴지통에서 복원할 수 있습니다.',
    confirmText: '휴지통으로', cancelText: '취소',
  });
  if (!ok) return;
  // 기존 나머지 로직 그대로
}
```

---

## 5. `build/build.mjs` 수정

실제 build.mjs 파일을 먼저 읽어서 JS_FILES와 CSS_FILES 배열 위치를 확인한 후 추가.

### JS_FILES — confirm-modal.js, dirty-indicator.js 추가

삽입 위치: **`src/core/dirty.js` 다음, 기존 컴포넌트들 앞**.

```js
// JS_FILES 배열 안에 추가 (dirty.js 줄 바로 뒤)
'src/core/dirty.js',
'src/components/shared/confirm-modal.js',   // ★ 추가
'src/components/shared/dirty-indicator.js', // ★ 추가
// 기존 컴포넌트들...
```

**삽입 순서 이유**:

- `confirm-modal.js`: 다른 컴포넌트들이 `customConfirm`을 쓰므로 먼저 로드
- `dirty-indicator.js`: `isDirty()`, `subscribe()` 필요 → dirty.js, store.js 뒤에 위치

### CSS_FILES — confirm-modal.css, dirty-indicator.css 추가

```js
// CSS_FILES 배열 끝에 추가
'src/components/shared/confirm-modal.css',   // ★ 추가
'src/components/shared/dirty-indicator.css', // ★ 추가
```

---

## 6. 작업 세션 분할 (2~3일)

### 세션 1 — 신규 파일 + dirty.js 패치 + 빌드 (1일)

```bash
# 1. 디렉토리 생성
mkdir -p src/components/shared

# 2. 신규 파일 4개 작성 (§2.1~2.4 코드 그대로)

# 3. dirty.js 패치 (§3)

# 4. build.mjs 갱신 (§5)

# 5. 빌드
npm run build

# 6. 문법 검증
node --check src/components/shared/confirm-modal.js
node --check src/components/shared/dirty-indicator.js
node --check src/core/dirty.js

# 7. 핵심 함수 존재 확인
grep -c "function customConfirm\|function customAlert" dist/ol-atlas.html
# 기대값: 2

grep -c "renderDirtyIndicator\|dirty-ind" dist/ol-atlas.html
# 기대값: 1 이상
```

**검증 게이트 (세션 1)**:

- [x] `node --check` 신규 파일 3개 통과
- [x] `npm run build` 성공
- [x] `customConfirm`, `customAlert` 빌드 산출물에 존재
- [x] 브라우저에서 열기 → 부팅 정상 (콘솔 에러 없음)
- [x] 카드 추가 후 헤더 "● 변경됨" 표시
- [x] autosave 1초 후 "✓ 저장됨" → 5초 후 사라짐

```bash
git add -A
git commit -m "[Phase 7.x.1] add confirm-modal + dirty-indicator modules"
```

### 세션 2 — storage, router, docview-inline 교체 (0.5~1일)

```bash
# 1. src/core/storage.js 교체 (§4.1)
# 2. src/core/router.js 교체 (§4.2)
# 3. src/components/docview-inline.js 교체 (§4.3)

npm run build

# 교체된 3개 파일 잔존 확인
node -e "
const fs = require('fs');
['src/core/storage.js','src/core/router.js','src/components/docview-inline.js'].forEach(f => {
  const c = fs.readFileSync(f,'utf8');
  const m = c.match(/(?<![a-zA-Z_])(confirm|alert)\s*\(/g);
  console.log(f + ':', m ? '❌ 잔존 ' + m.length + '개' : '✓ 0개');
});
"
```

**시나리오 테스트**:

- [x] 문서뷰 편집 중 → 다른 뷰 클릭 → 커스텀 모달 표시
- [x] 문서뷰 편집 중 → 취소 버튼 → 커스텀 모달 표시

```bash
git add -A
git commit -m "[Phase 7.x.2] replace confirm/alert in storage, router, docview-inline"
```

### 세션 3 — about, kanban, bulk-select, card-modal 교체 (0.5~1일)

```bash
# 1. src/components/about.js 교체 (§4.4)
# 2. src/components/kanban.js 교체 (§4.5)
# 3. src/components/bulk-select.js 교체 (§4.6)
# 4. src/components/card-modal.js 교체 (§4.7)

npm run build
```

**시나리오 테스트**:

- [x] 휴지통 단건 영구삭제 → danger 모달 (빨간 버튼, 취소에 포커스)
- [x] 일괄 영구삭제 → danger 모달
- [x] 휴지통 비우기 → danger 모달
- [x] 카드 있는 컬럼 삭제 → danger 모달 (N개 카드 언급)
- [x] 카드 선택 일괄 삭제 → 일반 모달 (danger 아님)
- [x] 카드 모달에서 삭제 → 일반 모달

```bash
git add -A
git commit -m "[Phase 7.x.3] replace remaining confirm/alert — about, kanban, bulk-select, card-modal"
```

### 세션 4 — 최종 검증 + 태그 (0.5일)

```bash
# 시스템 confirm/alert 완전 제거 검증
python3 << 'EOF'
import re, os

total = 0
for root, dirs, files in os.walk('src'):
    dirs[:] = [d for d in dirs if d not in ('node_modules',)]
    for fname in files:
        if not fname.endswith('.js'): continue
        path = os.path.join(root, fname)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        found = re.findall(r'(?<![a-zA-Z_])(confirm|alert)\s*\(', content)
        if found:
            print(f"  ❌ {path}: {found}")
            total += len(found)

if total == 0:
    print("✅ 시스템 confirm/alert 완전 제거 확인")
else:
    print(f"⚠ 잔존 {total}개")
EOF

# 빌드 최종
npm run build

# 시나리오 7종 테스트 후 태그
git add -A
git tag v0.7-phase7x-complete
git log --oneline -4
```

**브라우저 시나리오 7종**:

- [x] 카드 생성 → 칸반에 표시, 헤더 "● 변경됨"
- [x] 카드 편집 저장 → "✓ 저장됨"
- [x] 카드 삭제 → 커스텀 모달 (일반)
- [x] 영구 삭제 → danger 모달 (빨간 버튼, 취소 포커스)
- [x] 문서뷰 편집 중 뷰 이동 → 커스텀 모달
- [x] 카드 있는 컬럼 삭제 → danger 모달 (카드 수 표시)
- [x] 다크 모드 → 모달 다크 스타일 정상

---

## 7. 자주 발생하는 문제 + 대응

### `customConfirm is not defined`

→ build.mjs JS_FILES에서 `confirm-modal.js`가 해당 컴포넌트보다 뒤에 위치. → `confirm-modal.js`를 dirty.js 바로 다음으로 이동.

### `isDirty is not defined` (dirty-indicator 로드 시)

→ `dirty-indicator.js`가 `dirty.js` 보다 먼저 평가됨. → JS_FILES에서 `dirty.js` 이후에 위치하는지 확인.

### async 함수 반환 후 상위 함수가 계속 실행됨

→ 정상. `async function`의 `return`은 해당 함수만 종료. → `if (!ok) return;` 패턴이 올바르게 작동함.

### ESC 키가 기존 사이드바 핸들러와 중복

→ confirm-modal의 keydown 리스너가 `capture: true`로 등록됨 (§2.1 코드). → capture 단계에서 먼저 처리 + `stopPropagation()`.

### body.overflow 충돌 (카드 모달과 confirm 모달 동시 열릴 때)

→ `_closeModal`에서 카드 모달이 열려있으면 overflow 복구 안 함 (§2.1 코드에 이미 포함).

---

## 8. 검증 명령어 한 페이지 요약

```bash
# confirm/alert 잔존 확인
python3 -c "
import re,os; total=0
for r,d,f in os.walk('src'):
    d[:]=[x for x in d if x!='node_modules']
    for n in f:
        if not n.endswith('.js'): continue
        p=os.path.join(r,n); c=open(p).read()
        m=re.findall(r'(?<![a-zA-Z_])(confirm|alert)\s*\(',c)
        if m: print(p,m); total+=len(m)
print('잔존:',total,'개')
"

# 빌드
npm run build

# 문법 검증
find src -name "*.js" -not -path "*/node_modules/*" | xargs -I{} node --check {}

# 핵심 함수 존재
grep -c "function customConfirm\|function customAlert\|renderDirtyIndicator" dist/ol-atlas.html

# 태그
git tag v0.7-phase7x-complete
```

---

## 9. Phase 7.x → Phase 8.0 진입 조건

**모든 항목 체크 시 Phase 8.0 작업지시서 요청 가능**:

- [ ] 신규 파일 4개 작성 완료
- [ ] `dirty.js` 패치 완료
- [ ] `build.mjs` JS_FILES + CSS_FILES 갱신 완료
- [ ] 10개 시스템 confirm/alert 전환 완료
- [ ] python3 잔존 검증 결과 0개
- [ ] `npm run build` 성공
- [ ] 브라우저 시나리오 7종 통과
- [ ] 다크 모드 모달 스타일 확인
- [ ] `git tag v0.7-phase7x-complete` 부여됨

---

## 부록 A — Claude CLI 지시 프롬프트 템플릿

각 세션 시작 시 아래를 그대로 붙여넣기:

```
[작업 컨텍스트]
- 프로젝트: OL ATLAS v0.7 Phase 7.x
- 작업 디렉토리: <ol-atlas/ 절대 경로>
- 참조 문서: OL_ATLAS_v0_7_Phase7x_작업지시서.md
- 현재 세션: 세션 N — <세션 설명>

[권한 선언]
작업지시서 최상단 권한 선언에 따라:
- ol-atlas/ 폴더 내 모든 파일 읽기·쓰기·생성·삭제 승인
- bash 명령어, node, python3, npm run * 실행 승인
- git add/commit/tag 승인
매번 묻지 말고 즉시 실행할 것.
단, git push / rm -rf <폴더> / 폴더 외부 접근은 실행 전 확인.

[이번 세션 목표]
- <산출물 1>
- <산출물 2>

[핵심 제약]
- 기존 UI 로직 변경 금지. confirm/alert 교체와 신규 모듈 추가만.
- async 전환 시 호출처 누락 주의. 함수 시그니처 확인 후 작업.
- 각 파일 수정 후 node --check 문법 검증.
- 세션 끝에 검증 게이트 통과 확인 후 git commit.
```

---

**작성**: Claude (with biwoom) **버전**: v2 (실제 코드 기반 10개 위치 확인, v1.2 설계서 반영) **상태**: 즉시 착수 가능 **선행 태그**: v0.7-phase2-complete **완료 태그**: v0.7-phase7x-complete **다음 문서**: Phase 8.0 작업지시서 (ES modules 전환 + 빌드 구조 재편)