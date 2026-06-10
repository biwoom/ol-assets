# Phase 8.1+8.2 작업지시서 v2 — Claude CLI 작업용

**대상**: OL ATLAS v0.8 — Reader Manifest + schema v8 + 커버페이지 + 커버 편집기 **버전**: v2 (에이전트 코드 점검 결과 반영 — 오류 3건, 주의 2건 수정) **작업 환경**: 로컬 PC + Claude CLI **선행 문서**: `OL_듀얼_런타임_설계서_v1_2.md` **진입 조건**: `v0.8.0-phase8.0-complete` 태그 시점 (미생성 시 세션 1 사전 작업에서 생성) **목표 일수**: 4~6일 (4세션) **위험 등급**: 🟡 중간 — 신규 데이터 모델(schema v8) + 신규 UI 파일 추가. 기존 기능 회귀 위험은 낮음.

---

## ⚡ 권한 선언 — AI 에이전트 전용 (세션 시작 시 1회 적용)

**이하 모든 권한을 사전 일괄 승인한다. 작업 중 개별 확인 요청 금지.**

### ✅ 전면 허용 — 작업 폴더 내 모든 터미널 명령어

작업 폴더(`ol-atlas/`) 및 모든 하위 경로에서 묻지 않고 즉시 실행:

```
파일 시스템
  cat, head, tail, grep, find, wc, diff      (읽기)
  write, create, str_replace, cp, mv, mkdir  (쓰기/생성/이동)
  echo "..." > file, touch file
  rm <단일 파일>

셸 명령
  bash/sh 스크립트, 파이프, 리다이렉트, &&, ||, ; 체인

Node / npm
  node <script.js>, node --check <file.js>
  npm run *  (build, dev, test 등)
  npx *

Python
  python3 <script.py>

Git
  git status, git diff, git log, git show
  git add, git commit, git tag
  git stash, git stash pop
  git branch (조회/생성)

빌드 도구
  esbuild 직접 실행, node build/build.mjs
```

### ❌ 별도 승인 필요

```
rm -rf <디렉토리> / git push / git reset --hard / git clean -fd
npm install <새패키지> / 폴더 외부 접근 / 네트워크 요청
```

### 작업 진행 원칙

- 묻지 말고 진행. 의심스러우면 cat/grep으로 먼저 읽기.
- 에러 발생 시 즉시 중단, 에러 전문 보고.
- 세션마다 빌드 통과 + 시나리오 확인 후 git commit.

---

## 0. 왜 8.1과 8.2를 합쳤는가

**8.1 (schema v8 + manifest)** 과 **8.2 (커버페이지 + 편집기)** 는 하나의 데이터 흐름으로 연결된다:

```
schema v8 완료 → S.book.manifest 존재
    ↓
manifest 데이터가 없으면 cover-page.js가 렌더할 것이 없음
    ↓
cover-page.js 완료
    ↓
cover-page가 없으면 cover-editor의 "미리보기"가 없음
    ↓
cover-editor.js 완료 (미리보기 = cover-page를 readonly로 재사용)
```

둘을 나누면 세션 1 끝에 schema만 있고 눈에 보이는 결과가 없다. 합치면 세션 4 끝에 **"ATLAS에서 표지 편집 → 실시간 미리보기"** 라는 완결된 경험이 생긴다.

---

## 1. Phase 8.1+8.2 개요

### 1.1 이번 Phase가 만드는 것

|산출물|파일|성격|
|---|---|---|
|schema v8 마이그레이터|`src/core/schema.js` 수정|데이터|
|manifest 액션|`src/actions/settings-actions.js` 수정|데이터|
|커버페이지 렌더|`src/components/reader/cover-page.js`|BOOK 전용|
|커버페이지 CSS|`src/styles/cover-page.css`|BOOK 전용|
|커버 편집기|`src/components/author/cover-editor.js`|ATLAS 전용|
|커버 편집기 CSS|`src/styles/cover-editor.css`|ATLAS 전용|
|사이드바 "표지 편집" 항목|`src/components/shared/sidebar.js` 수정|ATLAS|
|main.js 신규 import|`src/main.js` 수정|빌드|
|CSS_FILES 갱신|`build/build.mjs` 수정|빌드|

### 1.2 이번 Phase가 변경하지 않는 것

- 기존 카드/칼럼/뷰 UI — 전혀 변경 없음
- exportBook() — Phase 8.3에서 작성
- BOOK 모드 부팅 — Phase 8.4에서 작성
- cover-page는 이번에 "렌더 함수"만 작성. 실제로 BOOK 부팅 시 첫 화면으로 뜨는 것은 Phase 8.4에서 연결됨

### 1.3 Phase 8.1+8.2 완료 시점의 상태

- ATLAS에서 사이드바 "표지 편집" 클릭 → 좌우 분할 편집 뷰
- 제목/부제/이미지 입력 → 우측 미리보기 실시간 갱신
- localStorage에 manifest 데이터가 schema v8 형식으로 저장됨
- 기존 v0.7 사용자 데이터 → schema v8로 자동 마이그레이션 (무손실)
- BOOK 부팅은 아직 안 됨 (Phase 8.4에서 연결)

---

## 2. 사전 작업 — 현재 코드 확인

### 2.1 반드시 먼저 확인할 것들

```bash
# 0. Phase 8.0 완료 태그 생성 (미생성 시 지금 생성)
git tag | grep phase8.0
# 없으면:
git tag v0.8.0-phase8.0-complete
git log --oneline -3

# 1. schema.js 현재 구조 확인 (최신 schemaVersion 파악)
cat src/core/schema.js

# 2. settings-actions.js 현재 액션 목록 확인
cat src/actions/settings-actions.js

# 3. sidebar.js 현재 구조 확인 (표지 편집 항목 삽입 위치 파악)
cat src/components/shared/sidebar.js

# 4. main.js 현재 import 순서 확인
cat src/main.js

# 5. ★ 빌드 구조 확인 — CSS 처리가 build.mjs인지 inline.mjs인지 확인
ls build/
cat build/inline.mjs   # CSS_FILES 배열이 여기 있을 것
cat build/build.mjs    # JS 번들링만 담당

# 6. ORIGIN 상수 현재 값 확인
grep -A 8 "ORIGIN" src/core/constants.js
```

이 출력 결과를 바탕으로 아래 작업을 진행한다. **추정 없이 실제 파일 내용을 확인한 후 작업할 것.**

---

## 3. Phase 8.1 — schema v8 + manifest 데이터 모델

### 3.1 schema.js 수정 — v7 → v8 마이그레이터 추가

현재 최신 schemaVersion을 확인한 후, 그 다음 번호로 v8 마이그레이터를 추가한다.

```js
// src/core/schema.js 에 추가할 마이그레이터
// 기존 마이그레이터 객체(migrate map) 안에 추가

// 현재 최신이 7이면: 키 7을 추가
// 현재 최신이 다른 번호면: 실제 번호 확인 후 그 다음 번호로

7: function(s) {
  // 기존 데이터 백업 (패턴 유지)
  try {
    localStorage.setItem('ol_backup_v7', JSON.stringify(s));
  } catch(e) {
    devLog('SCHEMA', 'backup v7 failed:', e.message);
  }

  s.meta = s.meta || {};
  s.meta.schemaVersion = 8;

  // manifest 초기값 생성 (ORIGIN에서 자동 복제)
  s.book = {
    manifest: {
      id:          _generateBookId(s),
      title:       (s.meta && s.meta.title) || '',
      subtitle:    '',
      author:      ORIGIN.author,
      series:      '',
      version:     '1.0',
      publishedAt: new Date().toISOString().slice(0, 10),
      cover: {
        image:           null,
        backgroundColor: 'auto',
      },
      entry: {
        view:        'cover',
        actions:     ['start', 'toc'],
        startTarget: 'first-card',
      },
      ordering: {
        cards: 'array-index',
      },
      display: {
        showColumns:   true,
        showTags:      true,
        showProgress:  true,
        showBookmarks: true,
      },
      license:   ORIGIN.license,
      copyright: ORIGIN.copyright,
    },
  };

  devLog('SCHEMA', 'migrated v7 → v8, book.manifest created');
  return s;
},
```

### 3.2 `_generateBookId` 헬퍼 추가

```js
// src/core/schema.js 안에 내부 헬퍼로 추가
function _generateBookId(s) {
  // site + title slug + 생성일 조합으로 고유 ID 생성
  // 진행률 localStorage 키에 사용됨 — 변경 불가이므로 안정적인 값으로 생성
  const site  = ORIGIN.site  || 'olbit.org';
  const title = (s.meta && s.meta.title)
    ? s.meta.title.toLowerCase().replace(/[^a-z0-9가-힣]+/g, '-').replace(/^-|-$/g, '').slice(0, 40)
    : 'untitled';
  const date  = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  return site + '/' + title + '/' + date;
}
```

### 3.3 normalizeState 수정 — S.book 누락 방어

schema 마이그레이션을 거쳐도 `S.book`이 없는 엣지케이스를 방어한다.

```js
// src/core/normalize.js 또는 schema.js의 normalizeState 함수 안에 추가
// S.book이 없으면 기본값 생성 (마이그레이션 실패 안전망)
if (!s.book || !s.book.manifest) {
  s.book = {
    manifest: {
      id:          'olbit.org/untitled/' + new Date().toISOString().slice(0,10).replace(/-/g,''),
      title:       '',
      subtitle:    '',
      author:      ORIGIN.author,
      series:      '',
      version:     '1.0',
      publishedAt: new Date().toISOString().slice(0, 10),
      cover:    { image: null, backgroundColor: 'auto' },
      entry:    { view: 'cover', actions: ['start', 'toc'], startTarget: 'first-card' },
      ordering: { cards: 'array-index' },
      display:  { showColumns: true, showTags: true, showProgress: true, showBookmarks: true },
      license:   ORIGIN.license,
      copyright: ORIGIN.copyright,
    },
  };
}
```

### 3.4 MANIFEST_UPDATE 액션 추가

```js
// src/actions/settings-actions.js 에 추가

export const MANIFEST_UPDATE = 'MANIFEST_UPDATE';

export function updateManifest(patch) {
  return {
    type: MANIFEST_UPDATE,
    payload: { patch },
    meta: { affects: ['cover-editor', 'cover-page'] },
  };
}
```

기존 settingsReducer에 케이스 추가:

```js
case MANIFEST_UPDATE: {
  const { patch } = action.payload;
  const currentManifest = state.book && state.book.manifest
    ? state.book.manifest
    : {};
  return {
    ...state,
    book: {
      ...(state.book || {}),
      manifest: { ...currentManifest, ...patch },
    },
  };
}
```

---

## 4. Phase 8.2a — 커버페이지 렌더러 (BOOK 전용)

### 4.1 `src/components/reader/cover-page.js`

```js
// src/components/reader/cover-page.js
import { S }           from '../../core/state.js';
import { subscribe }   from '../../core/store.js';
import { dispatch }    from '../../core/action.js';
import { escapeHTML }  from '../../core/utils.js';
import { changeView }  from '../../actions/view-actions.js';

export function renderCoverPage() {
  const el = document.getElementById('app');
  if (!el) return;

  const m = S.book && S.book.manifest ? S.book.manifest : {};
  const title     = m.title     || '(제목 없음)';
  const subtitle  = m.subtitle  || '';
  const author    = m.author    || '';
  const coverImg  = m.cover && m.cover.image ? m.cover.image : null;
  const totalCards = (S.cards || []).length;

  el.innerHTML = `
    <div class="cover-page" id="cover-page-root">
      ${coverImg
        ? `<img class="cover-image" src="${coverImg}" alt="${escapeHTML(title)}">`
        : '<div class="cover-image-placeholder"></div>'
      }
      <h1 class="cover-title">${escapeHTML(title)}</h1>
      ${subtitle
        ? `<p class="cover-subtitle">${escapeHTML(subtitle)}</p>`
        : ''
      }
      ${author
        ? `<p class="cover-author">${escapeHTML(author)}</p>`
        : ''
      }
      <div class="cover-actions">
        <button class="btn btn-secondary cover-btn-toc"  data-action="toc">목차</button>
        <button class="btn btn-primary   cover-btn-start" data-action="start">읽기 시작</button>
      </div>
    </div>
  `;

  // 이벤트 바인딩
  const root = document.getElementById('cover-page-root');
  if (!root) return;

  root.addEventListener('click', function(e) {
    const btn = e.target.closest('[data-action]');
    if (!btn) return;
    const action = btn.dataset.action;
    if (action === 'toc') {
      dispatch(changeView('cardboard'));
    } else if (action === 'start') {
      _startReading();
    }
  });
}

function _startReading() {
  // Phase 8.5에서 진행률 연동 예정
  // 지금은 단순히 첫 카드의 문서뷰로 이동
  const cards = S.cards || [];
  if (!cards.length) {
    dispatch(changeView('cardboard'));
    return;
  }
  // Phase 8.4에서 openCard dispatch 연동 예정
  // 현재는 카드보드로 이동
  dispatch(changeView('cardboard'));
}

// 부수효과: import되면 subscribe 자동 등록
subscribe('cover-page', renderCoverPage);
```

**주의**: `renderCoverPage`가 Phase 8.4 전까지는 실제로 BOOK 부팅 시 호출되지 않는다. subscribe 등록만 해두고, Phase 8.4에서 `bootBook()`이 `changeView('cover')`를 호출하면 그때 렌더된다.

### 4.2 `src/styles/cover-page.css`

```css
/* src/styles/cover-page.css */

.cover-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background: hsl(var(--background));
}

.cover-image {
  width: clamp(200px, 50vw, 280px);
  aspect-ratio: 5 / 7;
  object-fit: cover;
  border-radius: var(--radius);
  box-shadow: 0 12px 48px hsl(0 0% 0% / 0.12);
  margin-bottom: 2.5rem;
}

.cover-image-placeholder {
  width: clamp(200px, 50vw, 280px);
  aspect-ratio: 5 / 7;
  border-radius: var(--radius);
  background: hsl(var(--muted));
  margin-bottom: 2.5rem;
  border: 1px dashed hsl(var(--border));
}

.cover-title {
  font-size: clamp(1.75rem, 5vw, 3rem);
  font-weight: 700;
  margin: 0 0 0.75rem;
  letter-spacing: -0.02em;
  line-height: 1.2;
  max-width: 32rem;
  color: hsl(var(--foreground));
}

.cover-subtitle {
  font-size: clamp(0.9rem, 2vw, 1.1rem);
  color: hsl(var(--muted-foreground));
  margin: 0 0 1.5rem;
  max-width: 28rem;
  line-height: 1.5;
}

.cover-author {
  font-size: 0.85rem;
  color: hsl(var(--muted-foreground));
  letter-spacing: 0.08em;
  text-transform: uppercase;
  margin-bottom: 2.5rem;
}

.cover-actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
}

/* 모바일 */
@media (max-width: 480px) {
  .cover-page   { padding: 3rem 1.5rem; }
  .cover-actions { flex-direction: column; align-items: stretch; width: 100%; max-width: 240px; }
}
```

---

## 5. Phase 8.2b — 커버 편집기 (ATLAS 전용)

### 5.1 `src/components/author/cover-editor.js`

커버 편집기는 ATLAS에서만 사용. AUTHOR_BUNDLE 마커 안에 위치.

```js
// src/components/author/cover-editor.js
import { S }              from '../../core/state.js';
import { subscribe }      from '../../core/store.js';
import { dispatch }       from '../../core/action.js';
import { escapeHTML }     from '../../core/utils.js';
import { updateManifest } from '../../actions/settings-actions.js';
import { switchView }     from '../../core/router.js';        // ★ 추가 (돌아가기 버튼)
import { customAlert }    from '../../ui/confirm-modal.js';   // ★ 추가 (이미지 용량 경고)
import { ORIGIN }         from '../../core/constants.js';     // ★ 추가 (저자/라이선스 기본값)

let _editorActive = false;

export function renderCoverEditor() {
  const el = document.getElementById('app');
  if (!el) return;
  if (!_editorActive) {
    // cover-editor 뷰가 아니면 렌더하지 않음
    return;
  }

  const m = (S.book && S.book.manifest) || {};

  el.innerHTML = `
    <div class="cover-editor-wrap">

      <!-- 좌측: 입력 폼 -->
      <div class="cover-editor-form">
        <div class="cover-editor-header">
          <button class="btn btn-ghost cover-editor-back" id="ce-back">← 돌아가기</button>
          <h2 class="cover-editor-title">표지 편집</h2>
        </div>

        <div class="ce-field">
          <label class="ce-label" for="ce-title">제목 <span class="ce-required">*</span></label>
          <input class="ce-input" id="ce-title" type="text"
            value="${escapeHTML(m.title || '')}" placeholder="책 제목을 입력하세요">
        </div>

        <div class="ce-field">
          <label class="ce-label" for="ce-subtitle">부제</label>
          <input class="ce-input" id="ce-subtitle" type="text"
            value="${escapeHTML(m.subtitle || '')}" placeholder="부제 (선택)">
        </div>

        <div class="ce-field">
          <label class="ce-label" for="ce-series">시리즈</label>
          <input class="ce-input" id="ce-series" type="text"
            value="${escapeHTML(m.series || '')}" placeholder="OL BOOK · 붓다 시리즈 1">
        </div>

        <div class="ce-field">
          <label class="ce-label">표지 이미지</label>
          <div class="ce-img-wrap">
            ${m.cover && m.cover.image
              ? `<img class="ce-img-preview" src="${m.cover.image}" alt="현재 표지">`
              : '<div class="ce-img-empty">이미지 없음</div>'
            }
            <div class="ce-img-actions">
              <label class="btn btn-secondary ce-img-upload-label" for="ce-img-input">
                이미지 선택
              </label>
              <input id="ce-img-input" type="file" accept="image/*" style="display:none">
              ${m.cover && m.cover.image
                ? '<button class="btn btn-ghost ce-img-remove" id="ce-img-remove">제거</button>'
                : ''
              }
            </div>
            <p class="ce-img-hint">권장: 5:7 비율 (예: 500×700px). BOOK HTML에 base64로 포함됩니다.</p>
          </div>
        </div>

        <div class="ce-field-row">
          <div class="ce-field">
            <label class="ce-label" for="ce-version">버전</label>
            <input class="ce-input" id="ce-version" type="text"
              value="${escapeHTML(m.version || '1.0')}" placeholder="1.0">
          </div>
          <div class="ce-field">
            <label class="ce-label" for="ce-date">발행일</label>
            <input class="ce-input" id="ce-date" type="date"
              value="${escapeHTML(m.publishedAt || new Date().toISOString().slice(0,10))}">
          </div>
        </div>

        <div class="ce-field ce-readonly">
          <label class="ce-label">저자 <span class="ce-badge">자동</span></label>
          <div class="ce-static">${escapeHTML(m.author || ORIGIN.author)}</div>
        </div>

        <div class="ce-field ce-readonly">
          <label class="ce-label">라이선스 <span class="ce-badge">자동</span></label>
          <div class="ce-static">${escapeHTML(m.license || ORIGIN.license)}</div>
        </div>

      </div>

      <!-- 우측: 실시간 미리보기 -->
      <div class="cover-editor-preview">
        <div class="ce-preview-label">미리보기</div>
        <div class="ce-preview-frame" id="ce-preview-frame">
          ${_renderPreviewHTML(m)}
        </div>
      </div>

    </div>
  `;

  _bindCoverEditorEvents();
}

function _renderPreviewHTML(m) {
  const title    = escapeHTML(m.title    || '(제목 없음)');
  const subtitle = escapeHTML(m.subtitle || '');
  const author   = escapeHTML(m.author   || ORIGIN.author);
  const img      = m.cover && m.cover.image ? m.cover.image : null;

  return `
    <div class="cover-page cover-preview-inner">
      ${img
        ? `<img class="cover-image" src="${img}" alt="${title}" style="max-height:180px;margin-bottom:1rem">`
        : '<div class="cover-image-placeholder" style="height:120px;margin-bottom:1rem"></div>'
      }
      <h1 class="cover-title" style="font-size:1.4rem;margin-bottom:0.4rem">${title}</h1>
      ${subtitle ? `<p class="cover-subtitle" style="font-size:0.85rem;margin-bottom:0.75rem">${subtitle}</p>` : ''}
      <p class="cover-author" style="font-size:0.75rem;margin-bottom:1rem">${author}</p>
      <div class="cover-actions" style="gap:0.5rem">
        <button class="btn btn-secondary" style="font-size:0.8rem;padding:0.3rem 0.75rem" disabled>목차</button>
        <button class="btn btn-primary"   style="font-size:0.8rem;padding:0.3rem 0.75rem" disabled>읽기 시작</button>
      </div>
    </div>
  `;
}

function _bindCoverEditorEvents() {
  // 돌아가기
  const backBtn = document.getElementById('ce-back');
  if (backBtn) {
    backBtn.addEventListener('click', function() {
      _editorActive = false;
      switchView('kanban');  // import된 함수 직접 호출
    });
  }

  // 텍스트 입력 → 실시간 미리보기 + dispatch
  const textFields = {
    'ce-title':    'title',
    'ce-subtitle': 'subtitle',
    'ce-series':   'series',
    'ce-version':  'version',
    'ce-date':     'publishedAt',
  };

  Object.entries(textFields).forEach(function([id, key]) {
    const input = document.getElementById(id);
    if (!input) return;
    input.addEventListener('input', function() {
      dispatch(updateManifest({ [key]: input.value }));
      _updatePreview();
    });
  });

  // 이미지 업로드
  const imgInput = document.getElementById('ce-img-input');
  if (imgInput) {
    imgInput.addEventListener('change', function(e) {
      const file = e.target.files && e.target.files[0];
      if (!file) return;

      // 5MB 용량 경고
      if (file.size > 5 * 1024 * 1024) {
        customAlert({
          title: '이미지 용량 초과',
          message: '이미지가 5MB를 초과합니다.\n\n큰 이미지는 BOOK 파일 크기를 크게 늘립니다.\n500×700px 내외의 이미지를 권장합니다.',
          danger: true,
        });
      }

      const reader = new FileReader();
      reader.onload = function(ev) {
        dispatch(updateManifest({ cover: { ...((S.book && S.book.manifest && S.book.manifest.cover) || {}), image: ev.target.result } }));
        _updatePreview();
        // 편집기 전체 재렌더 (이미지 미리보기 갱신)
        renderCoverEditor();
      };
      reader.readAsDataURL(file);
    });
  }

  // 이미지 제거
  const removeBtn = document.getElementById('ce-img-remove');
  if (removeBtn) {
    removeBtn.addEventListener('click', function() {
      dispatch(updateManifest({ cover: { ...((S.book && S.book.manifest && S.book.manifest.cover) || {}), image: null } }));
      renderCoverEditor();
    });
  }
}

function _updatePreview() {
  const frame = document.getElementById('ce-preview-frame');
  if (!frame) return;
  const m = (S.book && S.book.manifest) || {};
  frame.innerHTML = _renderPreviewHTML(m);
}

// cover-editor 뷰 진입 함수 (sidebar에서 호출)
export function openCoverEditor() {
  _editorActive = true;
  renderCoverEditor();
}

subscribe('cover-editor', renderCoverEditor);
```

### 5.2 `src/styles/cover-editor.css`

```css
/* src/styles/cover-editor.css */

.cover-editor-wrap {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0;
  min-height: 100vh;
  background: hsl(var(--background));
}

/* 좌측 폼 */
.cover-editor-form {
  padding: 1.5rem;
  border-right: 1px solid hsl(var(--border));
  overflow-y: auto;
  max-height: 100vh;
}

.cover-editor-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid hsl(var(--border));
}

.cover-editor-title {
  font-size: 1rem;
  font-weight: 600;
  margin: 0;
}

.cover-editor-back {
  font-size: 0.85rem;
  color: hsl(var(--muted-foreground));
  padding: 0.25rem 0.5rem;
}

/* 폼 필드 */
.ce-field {
  margin-bottom: 1.25rem;
}

.ce-field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.ce-label {
  display: block;
  font-size: 0.8rem;
  font-weight: 500;
  color: hsl(var(--foreground));
  margin-bottom: 0.375rem;
}

.ce-required { color: hsl(var(--destructive)); margin-left: 2px; }

.ce-badge {
  font-size: 0.7rem;
  font-weight: 400;
  background: hsl(var(--muted));
  color: hsl(var(--muted-foreground));
  padding: 0.1rem 0.4rem;
  border-radius: 9999px;
  margin-left: 0.375rem;
}

.ce-input {
  width: 100%;
  padding: 0.4rem 0.625rem;
  font-size: 0.875rem;
  border: 1px solid hsl(var(--border));
  border-radius: calc(var(--radius) - 2px);
  background: hsl(var(--background));
  color: hsl(var(--foreground));
  box-sizing: border-box;
  transition: border-color 100ms;
}
.ce-input:focus {
  outline: 2px solid hsl(var(--ring));
  outline-offset: 1px;
}

.ce-readonly .ce-static {
  padding: 0.4rem 0.625rem;
  font-size: 0.875rem;
  color: hsl(var(--muted-foreground));
  background: hsl(var(--muted));
  border: 1px solid hsl(var(--border));
  border-radius: calc(var(--radius) - 2px);
}

/* 이미지 */
.ce-img-wrap { display: flex; flex-direction: column; gap: 0.625rem; }
.ce-img-preview {
  width: 100%;
  max-width: 140px;
  aspect-ratio: 5/7;
  object-fit: cover;
  border-radius: calc(var(--radius) - 2px);
  border: 1px solid hsl(var(--border));
}
.ce-img-empty {
  width: 140px;
  aspect-ratio: 5/7;
  border: 1px dashed hsl(var(--border));
  border-radius: calc(var(--radius) - 2px);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  color: hsl(var(--muted-foreground));
  background: hsl(var(--muted));
}
.ce-img-actions { display: flex; gap: 0.5rem; align-items: center; }
.ce-img-upload-label {
  cursor: pointer;
  font-size: 0.8rem;
  padding: 0.3rem 0.75rem;
}
.ce-img-hint {
  font-size: 0.72rem;
  color: hsl(var(--muted-foreground));
  line-height: 1.4;
  margin: 0;
}

/* 우측 미리보기 */
.cover-editor-preview {
  background: hsl(var(--muted));
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
}

.ce-preview-label {
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  color: hsl(var(--muted-foreground));
  margin-bottom: 1rem;
}

.ce-preview-frame {
  background: hsl(var(--background));
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  box-shadow: 0 8px 32px hsl(0 0% 0% / 0.10);
  width: 100%;
  max-width: 280px;
  min-height: 400px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-preview-inner {
  padding: 1.5rem 1rem;
  min-height: auto;
}

/* 모바일: 세로 스택 */
@media (max-width: 768px) {
  .cover-editor-wrap {
    grid-template-columns: 1fr;
  }
  .cover-editor-preview {
    position: static;
    height: auto;
    padding: 1.5rem;
    border-top: 1px solid hsl(var(--border));
  }
}
```

---

## 6. 사이드바에 "표지 편집" 항목 추가

### 6.1 sidebar.js 수정

```bash
# 현재 사이드바 항목 구조 확인
grep -n "about\|kanban\|cover\|표지\|sb-menu\|sb-item\|sb-nav" src/components/shared/sidebar.js | head -30
```

**ES modules 방식 — import로 명확히 연결**:

```js
// src/components/shared/sidebar.js 상단 import 블록에 추가
import { openCoverEditor } from '../author/cover-editor.js';
```

> **주의**: sidebar.js는 shared/에 있고 cover-editor.js는 author/에 있다. 이 방향의 import(`shared → author`)는 Phase 8.3의 exportBook()이 author 번들을 제거할 때 sidebar.js 안의 `openCoverEditor` 참조가 끊길 수 있다. **해결**: BOOK 산출물에서는 sidebar가 cover-editor를 호출할 일이 없으므로, `openCoverEditor`를 조건부로 호출하거나, BOOK 빌드에서 sidebar.js의 해당 항목을 렌더하지 않도록 Phase 8.3 또는 8.4에서 처리한다. **지금은 import 추가 + 항목 렌더만 구현.**

**항목 추가 패턴** (실제 sidebar.js 구조에 맞춰 조정):

```js
// sidebar.js의 ATLAS 전용 항목 렌더 위치에 추가
// 실제 sidebar.js를 읽어서 기존 패턴(about, settings 등)과 동일한 방식으로 작성

// 예: 기존 패턴이 버튼 생성 방식이면
const ceBtn = document.createElement('button');
ceBtn.className = 'sb-nav-item';   // 실제 클래스명 확인 후 맞출 것
ceBtn.textContent = '표지 편집';
ceBtn.addEventListener('click', function() {
  openCoverEditor();
});
// 적절한 위치에 appendChild
```

---

## 7. main.js와 build.mjs 갱신

### 7.1 main.js — 신규 파일 import 추가

```bash
# main.js 현재 구조 확인
cat src/main.js
```

두 import를 추가한다. 위치는 **기존 reader/author 컴포넌트 import 근처**에 삽입:

```js
// reader 컴포넌트 섹션에 추가
import './components/reader/cover-page.js';

// author 컴포넌트 섹션에 추가 (기존 author 컴포넌트들과 함께)
import './components/author/cover-editor.js';
```

> **AUTHOR_BUNDLE 마커에 대하여**: 마커(`/*! AUTHOR_BUNDLE_START */`, `/*! AUTHOR_BUNDLE_END */`)는 esbuild가 번들링한 **dist/ol-atlas.html 출력물 안에** legal comment로 존재한다. `src/main.js`에는 마커가 없다. main.js의 import 순서와 마커는 무관하다. **cover-editor.js를 main.js 어디에 추가해도 빌드 결과에서 마커 안에 포함된다.** (esbuild가 author 컴포넌트 코드를 번들링할 때 자동으로 마커 사이에 위치시킴)

빌드 후 마커 확인:

```bash
npm run build
grep -c "AUTHOR_BUNDLE" dist/ol-atlas.html
# 기대: 2 (START, END 각 1개)

# cover-editor 코드가 번들에 포함됐는지
grep -c "renderCoverEditor\|openCoverEditor" dist/ol-atlas.html
# 기대: 1 이상
```

### 7.2 CSS 파일 추가 — `build/inline.mjs`

> **Phase 8.0 빌드 재편 결과**: CSS 처리는 `build/build.mjs`가 아니라 **`build/inline.mjs`**가 담당한다. `inline.mjs`에 `CSS_FILES` 배열이 있다.

```bash
# 현재 CSS_FILES 배열 확인
grep -A 20 "CSS_FILES" build/inline.mjs
```

`inline.mjs`의 `CSS_FILES` 배열에 두 CSS를 추가:

```js
// build/inline.mjs — CSS_FILES 배열 안에 추가
'src/styles/cover-page.css',    // ★ 추가
'src/styles/cover-editor.css',  // ★ 추가
```

---

## 8. 작업 세션 분할 (4세션)

### 세션 1 — schema v8 + MANIFEST_UPDATE 액션 (1일)

**목표**: 데이터 모델 완성. S.book.manifest가 부팅 시 자동 생성됨.

```bash
# 1. schema.js 현재 구조 확인
cat src/core/schema.js

# 2. 현재 최신 schemaVersion 확인
grep -n "schemaVersion\|meta.schemaVersion\|migrate\[" src/core/schema.js

# 3. §3.1 마이그레이터 추가 (실제 번호 확인 후)

# 4. §3.2 _generateBookId 헬퍼 추가

# 5. §3.3 normalizeState 방어 코드 추가

# 6. §3.4 settings-actions.js에 MANIFEST_UPDATE 추가

# 7. 빌드
npm run build

# 8. 브라우저에서 ATLAS 열기
# → 콘솔에서 S.book.manifest 확인
# F12 → 콘솔 → S.book
# 기대값: { manifest: { id: 'olbit.org/...', title: '', author: '비움', ... } }

# 9. 기존 localStorage 데이터로 마이그레이션 테스트
# → 이미 데이터가 있는 상태에서 새 빌드 열기 → S.book.manifest 자동 생성 확인

# 10. 문법 검증
node --check src/core/schema.js
node --check src/actions/settings-actions.js
```

**검증 게이트 (세션 1)**:

- [ ] `npm run build` 성공
- [ ] 브라우저 콘솔에서 `S.book.manifest.author === '비움'` 확인
- [ ] 기존 localStorage 데이터 열기 → 콘솔 에러 없음 + manifest 자동 생성
- [ ] `updateManifest({ title: '테스트' })` dispatch → `S.book.manifest.title === '테스트'` 확인
- [ ] 기존 ATLAS 기능(칸반, 카드 편집 등) 정상 작동

```bash
git add -A
git commit -m "[Phase 8.1] schema v8 migration + S.book.manifest + MANIFEST_UPDATE action"
```

### 세션 2 — cover-page.js + cover-page.css (0.5~1일)

**목표**: BOOK 커버페이지 렌더 함수 완성. subscribe 등록.

```bash
# 1. §4.1 cover-page.js 작성
# 2. §4.2 cover-page.css 작성
# 3. main.js에 reader 섹션 import 추가
# 4. build/inline.mjs CSS_FILES에 cover-page.css 추가
```

**IIFE 번들 환경 — 콘솔 테스트를 위한 임시 전역 노출**:

esbuild `format: 'iife'`로 번들되면 모든 함수가 IIFE 스코프 안에 갇혀 브라우저 콘솔에서 직접 호출할 수 없다. 세션 2 테스트를 위해 `cover-page.js` 끝에 **임시 전역 노출 코드**를 추가한다.

```js
// src/components/reader/cover-page.js 끝에 임시 추가 (세션 4 완료 후 제거)
// TODO: Phase 8.2 테스트용 임시 노출 — Phase 8.4 이후 제거
if (typeof window !== 'undefined') {
  window.__dev_renderCoverPage = renderCoverPage;
}
```

```bash
# 빌드
npm run build

# 브라우저에서 ATLAS 열기 → F12 → 콘솔
# 임시 노출된 함수로 수동 테스트
document.getElementById('app').innerHTML = '';
window.__dev_renderCoverPage();
# → 커버페이지 렌더 확인

# S.book.manifest 데이터 없을 때 placeholder 표시 확인
# S.book.manifest.title이 있으면 해당 제목 표시 확인
```

**검증 게이트 (세션 2)**:

- [ ] `npm run build` 성공
- [ ] `window.__dev_renderCoverPage()` → 화면에 커버페이지 표시
- [ ] 표지 이미지 없을 때 placeholder 표시 (에러 없음)
- [ ] 제목/부제 있을 때 해당 내용 표시
- [ ] 기존 ATLAS 기능 정상 작동

```bash
git add -A
git commit -m "[Phase 8.2a] cover-page.js + css (reader component)"
```

### 세션 3 — cover-editor.js + cover-editor.css (1~2일)

**목표**: ATLAS 커버 편집기 완성. 입력 → 실시간 미리보기 갱신.

```bash
# 1. §5.1 cover-editor.js 작성 (import 8개 포함)
# 2. §5.2 cover-editor.css 작성
# 3. main.js author 컴포넌트 섹션에 cover-editor.js import 추가
# 4. build/inline.mjs CSS_FILES에 cover-editor.css 추가
```

**임시 전역 노출 — cover-editor.js 끝에 추가**:

```js
// src/components/author/cover-editor.js 끝에 임시 추가 (세션 4 완료 후 제거)
// TODO: Phase 8.2 테스트용 임시 노출 — 사이드바 연결 후 제거
if (typeof window !== 'undefined') {
  window.__dev_openCoverEditor = openCoverEditor;
}
```

```bash
npm run build

# 브라우저 콘솔
window.__dev_openCoverEditor();
# → 편집기 화면 렌더 확인

# 각 필드 입력 테스트
# → 미리보기 실시간 갱신 확인 (입력 즉시 우측 미리보기 변경)

# 이미지 업로드 테스트
# → 5MB 이상: customAlert 표시 확인
# → 정상 크기: 미리보기에 이미지 표시

# dispatch 동작 확인 — 콘솔에서 입력 후
JSON.stringify(S.book.manifest.title)
# → 입력한 값으로 변경됐는지 확인
```

**검증 게이트 (세션 3)**:

- [ ] `npm run build` 성공
- [ ] `window.__dev_openCoverEditor()` → 편집기 렌더
- [ ] 제목 입력 → 우측 미리보기 즉시 갱신
- [ ] 이미지 업로드 → 미리보기에 이미지 표시
- [ ] `S.book.manifest.title`이 입력값으로 업데이트 (콘솔 확인)
- [ ] 돌아가기 버튼 → `switchView('kanban')` 호출 (칸반 뷰로 복귀)
- [ ] AUTHOR_BUNDLE 마커 잔존 확인 (`grep -c "AUTHOR_BUNDLE" dist/ol-atlas.html` → 2)

```bash
git add -A
git commit -m "[Phase 8.2b] cover-editor.js + css (author component, realtime preview)"
```

### 세션 4 — 사이드바 연결 + 임시 노출 제거 + 최종 검증 + 태그 (0.5~1일)

**목표**: 사이드바에서 "표지 편집" 진입. 임시 노출 코드 제거. Phase 게이트 모두 통과.

```bash
# 1. sidebar.js 현재 구조 정확히 파악
cat src/components/shared/sidebar.js

# 2. §6 사이드바 "표지 편집" 항목 추가
#    sidebar.js 상단에 import { openCoverEditor } from '../author/cover-editor.js'; 추가
#    기존 패턴에 맞춰 버튼/항목 생성 코드 추가

# 3. 임시 전역 노출 코드 제거
#    cover-page.js 끝의 window.__dev_renderCoverPage 블록 제거
#    cover-editor.js 끝의 window.__dev_openCoverEditor 블록 제거

# 4. 빌드
npm run build

# 5. 사이드바에서 "표지 편집" 클릭 → 편집기 진입 확인
# 6. 편집기에서 "돌아가기" → 칸반 뷰 복귀 확인
# 7. 편집 후 새로고침 → 값 유지 확인 (localStorage)
```

**Phase 8.1+8.2 최종 게이트**:

- [ ] `npm run build` 성공
- [ ] **schema v7 → v8 마이그레이션 무손실** — 기존 데이터 열어도 카드/칼럼 그대로
- [ ] `S.book.manifest` 부팅 시 자동 생성 (콘솔 확인)
- [ ] 사이드바 "표지 편집" 클릭 → 편집기 진입
- [ ] 제목/부제/이미지 입력 → 미리보기 실시간 갱신 (100ms 이내)
- [ ] 편집 값이 localStorage에 저장 (새로고침 후 유지)
- [ ] **임시 전역 노출 코드 제거** (`grep "window.__dev_" src/components/reader/cover-page.js src/components/author/cover-editor.js` → 결과 없음)
- [ ] AUTHOR_BUNDLE 마커 잔존 확인 (`grep -c "AUTHOR_BUNDLE" dist/ol-atlas.html` → 2)
- [ ] `build/inline.mjs`에 cover-page.css, cover-editor.css 추가됨
- [ ] 기존 ATLAS 기능 7종 시나리오 정상 작동

```bash
git add -A
git commit -m "[Phase 8.1+8.2] complete: cover-page + cover-editor + sidebar integration"
git tag v0.8.0-phase8.1-2-complete
```

---

## 9. 자주 발생하는 문제 + 대응

### 9.1 schema 마이그레이션 후 기존 카드 사라짐

**원인**: 마이그레이터가 `return s`를 빠뜨리거나 state를 새 객체로 덮어씀.

**대응**: 마이그레이터 함수가 반드시 `return s`로 끝나는지 확인. `s.book = {...}`는 state에 필드를 추가하는 것이지 state를 교체하는 것이 아님.

```js
// ✅ 올바른 패턴
7: function(s) {
  s.meta.schemaVersion = 8;
  s.book = { manifest: { ... } };
  return s;  // 반드시 return
},
```

### 9.2 `S.book is undefined` 런타임 에러

**원인**: normalizeState가 실행되기 전 S.book에 접근.

**대응**: cover-page.js, cover-editor.js 모두 `S.book && S.book.manifest` 방어 코드 사용. §3.3의 normalizeState 방어 코드가 올바르게 추가되었는지 확인.

### 9.3 이미지 업로드 후 미리보기가 갱신되지 않음

**원인**: `FileReader.onload` 비동기 흐름에서 dispatch 후 `_updatePreview()`가 너무 빨리 실행되어 state 갱신 전에 미리보기를 렌더.

**대응**: `_updatePreview()` 대신 `renderCoverEditor()` 전체 재렌더 호출. (§5.1 코드에 이미 `renderCoverEditor()` 재호출로 처리됨)

### 9.4 AUTHOR_BUNDLE 마커 확인 방법

**AUTHOR_BUNDLE 마커는 `src/main.js`에 없다. `dist/ol-atlas.html`에 있다.**

마커는 esbuild가 번들링 후 legal comment(`/*! */`)로 출력물에 삽입한다. cover-editor.js를 main.js에 import 추가하는 위치 자체는 마커와 무관하다.

```bash
# 올바른 확인 방법 — dist/ol-atlas.html 기준
grep -c "AUTHOR_BUNDLE" dist/ol-atlas.html
# 기대: 2 (START 1개, END 1개)

# cover-editor 코드가 번들에 포함됐는지
grep -c "renderCoverEditor\|openCoverEditor" dist/ol-atlas.html
# 기대: 1 이상
```

### 9.5 `openCoverEditor is not a function` (사이드바 연결 후)

**원인**: sidebar.js에 `import { openCoverEditor } from '../author/cover-editor.js'`가 없음.

**대응**: ES modules 환경에서 전역 함수 참조(`typeof openCoverEditor === 'function'`)는 안티패턴이다. 반드시 import로 연결할 것.

```js
// sidebar.js 상단에 반드시 추가
import { openCoverEditor } from '../author/cover-editor.js';
```

확인:

```bash
grep "openCoverEditor" src/components/shared/sidebar.js
# import 라인과 호출 라인 둘 다 있어야 함
```

---

## 10. 검증 명령어 모음

```bash
# 빌드
npm run build

# AUTHOR_BUNDLE 마커 확인
grep -c "AUTHOR_BUNDLE" dist/ol-atlas.html
# 기대: 2

# cover-page, cover-editor 함수 존재
grep -c "renderCoverPage\|renderCoverEditor\|openCoverEditor" dist/ol-atlas.html
# 기대: 3 이상

# schema 마이그레이터 번호 확인
grep -n "schemaVersion" dist/ol-atlas.html | head -5

# S.book.manifest 구조 브라우저 콘솔 확인 명령
# → 개발자 도구 콘솔에서:
# JSON.stringify(S.book.manifest, null, 2)

# cover-page CSS 존재
grep -c "cover-page\|cover-image\|cover-title" dist/ol-atlas.html
# 기대: 여러 개

# cover-editor CSS 존재
grep -c "cover-editor\|ce-input\|ce-label\|ce-preview" dist/ol-atlas.html
# 기대: 여러 개
```

---

## 부록 A — Claude CLI 지시 프롬프트 템플릿

각 세션 시작 시:

```
[작업 컨텍스트]
- 프로젝트: OL ATLAS v0.8 Phase 8.1+8.2
- 작업 디렉토리: <ol-atlas/ 절대 경로>
- 참조 문서: OL_ATLAS_Phase8_1_2_작업지시서.md
- 현재 세션: 세션 N — <세션 설명>

[권한 선언]
작업지시서 최상단 권한 선언에 따라:
- ol-atlas/ 폴더 내 모든 파일 읽기·쓰기·생성·삭제 승인
- bash, node, python3, npm run * 실행 승인
- git add/commit/tag 승인
매번 묻지 말고 즉시 실행할 것.
단, git push / rm -rf <폴더> / 폴더 외부 접근은 실행 전 확인.

[이번 세션 목표]
- <산출물 1>
- <산출물 2>

[핵심 제약]
- 작업 전 반드시 실제 파일을 cat으로 확인한 후 작업. 추정 금지.
- schema 마이그레이터는 반드시 return s로 끝날 것.
- cover-editor import는 AUTHOR_BUNDLE 마커 안에 위치할 것.
- 세션 끝에 검증 게이트 통과 확인 후 git commit.
```

---

## 부록 B — Phase 8.3 진입 조건

**모든 항목 체크 시 Phase 8.3(exportBook) 작업지시서 요청 가능**:

- [ ] schema v8 마이그레이션 무손실 (기존 카드 유지)
- [ ] S.book.manifest 부팅 시 자동 생성
- [ ] MANIFEST_UPDATE dispatch → 값 변경 + 저장
- [ ] cover-page.js subscribe 등록 (콘솔 listViews() 확인)
- [ ] cover-editor 편집 → 미리보기 실시간 갱신
- [ ] 이미지 업로드 → 표시
- [ ] 사이드바 "표지 편집" 진입/복귀
- [ ] AUTHOR_BUNDLE 마커 2개 잔존
- [ ] `npm run build` 성공
- [ ] ATLAS 기존 기능 7종 시나리오 정상
- [ ] `git tag v0.8.0-phase8.1-2-complete`

---

**작성**: Claude (with biwoom) **상태**: Phase 8.0 완료 후 즉시 착수 가능 **선행 태그**: v0.8.0-phase8.0-complete **완료 태그**: v0.8.0-phase8.1-2-complete **다음 문서**: Phase 8.3 작업지시서 (exportBook — BOOK 산출물 생성)

> **메모리 원칙 상기**: 이 프로젝트의 본질은 불교 콘텐츠입니다. Phase 8.2의 커버 편집기는 "첫 번째 불교 콘텐츠를 독자에게 전달하기 위한 표지"를 만드는 도구입니다. 비움이 "구체적인 디자인 아이디어는 Phase 8.4에서 제안한다"고 하셨으므로, 이번 Phase의 CSS는 설계서 기준의 기본 구조로만 구현하고 Phase 8.4에서 정제합니다.