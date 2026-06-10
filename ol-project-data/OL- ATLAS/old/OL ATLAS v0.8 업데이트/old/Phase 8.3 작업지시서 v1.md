# Phase 8.3 작업지시서 — exportBook() 구현

  

**대상**: OL ATLAS v0.8 — ATLAS → BOOK HTML 단일 파일 배포

**버전**: v1.0

**작성일**: 2026-05-24

**작업 환경**: 로컬 PC + Claude CLI

**선행 문서**: `OL 듀얼 런타임 설계서 v1.2.md` §5, §6

**진입 조건**: Phase 8.1+8.2 완료 (schema v8, `S.book.manifest`, `cover-page.js`, `cover-editor.js` 모두 완료)

**목표 일수**: 2일 (2세션)

**위험 등급**: 🟡 중간 — AUTHOR_BUNDLE 마커 재배치 필요. 기존 save/load 회귀 주의.

  

---

  

## ⚡ 권한 선언 — AI 에이전트 전용 (세션 시작 시 1회 적용)

  

**이하 모든 권한을 사전 일괄 승인한다. 작업 중 개별 확인 요청 금지.**

  

### ✅ 전면 허용 — 작업 폴더 내 모든 터미널 명령어

  

```

파일 시스템

cat, head, tail, grep, find, wc, diff (읽기)

write, create, str_replace, cp, mv, mkdir (쓰기/생성/이동)

rm <단일 파일>

  

셸 명령

bash/sh 스크립트, 파이프, 리다이렉트, &&, ||, ; 체인

  

Node / npm

node <script.js>, node --check <file.js>

npm run * (build, dev, test 등)

  

Git

git status, git diff, git log, git add, git commit, git tag

  

빌드

node build/build.mjs, node build/inline.mjs

```

  

### ❌ 별도 승인 필요

  

```

rm -rf <디렉토리> / git push / git reset --hard / git clean -fd

npm install <새패키지> / 폴더 외부 접근 / 네트워크 요청

```

  

---

  

## 0. Phase 8.3 개요

  

### 0.1 목표

  

ATLAS 사이드바의 "BOOK으로 배포" 버튼 클릭 → `exportBook()` 실행 → BOOK HTML 다운로드.

  

BOOK HTML은:

- AUTHOR 전용 코드(kanban, 편집기 등)가 제거된 자기완결형 단일 파일

- `S.cards`, `S.columns`, `S.book.manifest` 데이터가 base64로 내장

- `window.__OL_MODE__ = 'book'` 마커가 삽입되어 부팅 시 BOOK 모드 감지 가능

  

### 0.2 이번 Phase가 만드는 것

  

| 산출물 | 파일 | 성격 |

|---|---|---|

| AUTHOR_BUNDLE 마커 재배치 | `build/inline.mjs` 수정 | 빌드 |

| AUTHOR_BUNDLE 마커 추가 | `src/main.js` 수정 | 빌드 |

| `exportBook()` 함수 | `src/components/author/export-book.js` **신규** | ATLAS 전용 |

| "BOOK으로 배포" 버튼 | `src/components/shared/sidebar.js` 수정 | ATLAS UI |

  

### 0.3 이번 Phase가 건드리지 않는 것

  

- 기존 `export-import.js`의 save/load 기능 — 전혀 변경 없음

- `cover-page.js`, `cover-editor.js` — 전혀 변경 없음

- `bootBook()`, `detectMode()` — Phase 8.4에서 작성 (지금은 BOOK HTML을 열어도 ATLAS처럼 부팅됨. Phase 8.4에서 reader 모드 부팅을 연결)

  

---

  

## 1. 핵심 개념 — AUTHOR_BUNDLE 마커 전략

  

### 1.1 현재 상태 (Phase 8.0 완료 시점)와 문제점

  

`build/inline.mjs`는 현재 번들 **전체**를 AUTHOR_BUNDLE 마커로 감싼다:

  

```js

// build/inline.mjs, line 116 (현재 — 잘못된 위치)

.replace('<!--SCRIPTS-->', r(`<script>

/*! AUTHOR_BUNDLE_START */

${bundleJs}

/*! AUTHOR_BUNDLE_END */

</script>`));

```

  

Phase 8.0의 게이트 체크는 "마커가 HTML에 존재하는가"를 확인했고 통과. 하지만 이 상태에서 `exportBook()`이 마커 사이 내용을 제거하면 **JS 전체**가 사라져 빈 화면이 된다.

  

### 1.2 목표 상태

  

마커는 **esbuild 번들 내부**에 위치해야 한다. 설계서 §3.4 "방법 A" 채택.

  

```

dist/bundle.js 구조 (목표):

(()=>{

// CORE: dev, store, render-queue, schema, storage, dirty, action ...

// ACTIONS: card-actions, column-actions, view-actions, settings-actions

// SHARED: confirm-modal, dirty-indicator, sidebar, docview, about, ...

// READER: cover-page

  

/*! AUTHOR_BUNDLE_START */

// kanban, cardgrid, listview, home, cover-editor, export-book

/*! AUTHOR_BUNDLE_END */

  

// boot()

})();

```

  

`exportBook()`은 `/*! AUTHOR_BUNDLE_START */` ~ `/*! AUTHOR_BUNDLE_END */` 사이만 교체한다.

  

### 1.3 구현 방법 요약

  

| 단계 | 파일 | 변경 내용 |

|---|---|---|

| 1 | `build/inline.mjs` | SCRIPTS 플레이스홀더에서 외부 마커 제거 |

| 2 | `src/main.js` | author import 그룹에 `/*! AUTHOR_BUNDLE_START/END */` 주석 추가 |

| 검증 | `build.mjs` | `legalComments: 'inline'` (이미 설정됨 ✅) — esbuild가 `/*! */` 주석 보존 |

  

**esbuild legal comment 원리**: `/*!`로 시작하는 블록 주석은 minify 시에도 번들 내 위치를 유지한다. import 사이에 삽입하면 해당 위치 근처에 출력된다.

  

### 1.4 export-import.js 경로 확인

  

`export-import.js`는 현재 `src/main.js`에 직접 import 되어 있지 않다. `src/core/events.js`가 `closeAllDropdowns`를 import하면서 간접 로드된다:

  

```js

// src/core/events.js (현재)

import { closeAllDropdowns } from '../actions/export-import.js';

```

  

따라서 `export-import.js`는 마커 **밖**에서 로드되는 것이 맞다 — save/load는 BOOK에서도 불필요하지만, events.js가 BOOK에 포함되므로 bundle에는 남는다. 이 구조는 Phase 8.4에서 정리할 예정. Phase 8.3에서는 그대로 유지.

  

---

  

## 2. 세션 구성

  

| 세션 | 내용 | 완료 조건 |

|---|---|---|

| Session 1 | AUTHOR_BUNDLE 마커 재배치 + 빌드 검증 | `dist/bundle.js` 내부에 마커 확인 |

| Session 2 | `export-book.js` 작성 + 사이드바 버튼 + 테스트 | BOOK HTML 다운로드 + `__OL_MODE__==='book'` 확인 |

  

---

  

## 3. Session 1 — AUTHOR_BUNDLE 마커 재배치

  

### 3.1 Step 1: build/inline.mjs 수정

  

파일 `build/inline.mjs`, line 116 근처.

  

**수정 전**:

```js

.replace('<!--SCRIPTS-->', r(`<script>\n/*! AUTHOR_BUNDLE_START */\n${bundleJs}\n/*! AUTHOR_BUNDLE_END */\n</script>`));

```

  

**수정 후**:

```js

.replace('<!--SCRIPTS-->', r(`<script>\n${bundleJs}\n</script>`));

```

  

마커는 이제 main.js → esbuild → bundle.js 내부에 자리한다. inline.mjs는 마커를 직접 삽입하지 않는다.

  

### 3.2 Step 2: src/main.js 수정

  

Author 전용 import 그룹 앞뒤에 legal comment 마커를 추가하고, export-book.js는 아직 미생성이므로 주석 처리한다.

  

**수정 전**:

```js

// src/main.js

import './components/author/kanban.js';

import './components/author/cardgrid.js';

import './components/author/listview.js';

import './components/shared/sidebar.js';

import './components/shared/docview.js';

import './components/author/home.js';

import './components/reader/cover-page.js';

import './components/author/cover-editor.js';

import './components/shared/about.js';

import './components/shared/dirty-indicator.js';

import './data/search/search.js';

import './core/events.js';

import { boot } from './data/init.js';

boot();

```

  

**수정 후**:

```js

// src/main.js

// ── OL Atlas 진입점 ─────────────────────────────────────

  

// ── SHARED 컴포넌트 (BOOK에도 포함) ─────────────────────

import './components/shared/sidebar.js';

import './components/shared/docview.js';

import './components/shared/about.js';

import './components/shared/dirty-indicator.js';

  

// ── READER 컴포넌트 (BOOK에 포함) ───────────────────────

import './components/reader/cover-page.js';

  

/*! AUTHOR_BUNDLE_START */

// ── AUTHOR 전용 컴포넌트 (BOOK 배포 시 제거됨) ──────────

import './components/author/kanban.js';

import './components/author/cardgrid.js';

import './components/author/listview.js';

import './components/author/home.js';

import './components/author/cover-editor.js';

// import './components/author/export-book.js'; // Session 2에서 추가

/*! AUTHOR_BUNDLE_END */

  

// ── 검색 ────────────────────────────────────────────────

import './data/search/search.js';

  

// ── 이벤트 와이어링 ─────────────────────────────────────

import './core/events.js';

  

// ── 부팅 ─────────────────────────────────────────────────

import { boot } from './data/init.js';

boot();

```

  

**주의**:

- SHARED(sidebar, docview, about, dirty-indicator)와 READER(cover-page)는 마커 **밖**에 위치 — BOOK에도 포함됨

- search.js, events.js, boot()는 마커 **밖** — BOOK에도 포함됨

- `export-book.js`는 아직 미생성이므로 주석 처리. Session 1 빌드는 이 상태로 진행.

  

### 3.3 Step 3: 빌드 실행

  

```bash

node build/build.mjs

```

  

### 3.4 Step 4: 마커 위치 검증

  

```bash

# bundle.js에 마커가 존재하는지 확인

grep -c 'AUTHOR_BUNDLE_START' dist/bundle.js # → 1 이어야 함

grep -c 'AUTHOR_BUNDLE_END' dist/bundle.js # → 1 이어야 함

  

# 마커 줄 번호와 마커 사이에 author 코드가 있는지 확인

node -e "

const fs = require('fs');

const b = fs.readFileSync('dist/bundle.js', 'utf8');

const MSTART = '/*! ' + 'AUTHOR_BUNDLE_START' + ' */';

const MEND = '/*! ' + 'AUTHOR_BUNDLE_END' + ' */';

const si = b.indexOf(MSTART);

const ei = b.indexOf(MEND);

console.log('AUTHOR_BUNDLE_START at byte:', si);

console.log('AUTHOR_BUNDLE_END at byte:', ei);

console.log('Range OK:', si > 0 && ei > si);

const inner = b.slice(si, ei);

console.log('Inner size:', inner.length, 'chars');

console.log('Has kanban code:', inner.includes('kanban'));

console.log('Has cover-editor:', inner.includes('cover-editor') || inner.includes('openCoverEditor'));

"

```

  

**예상 출력**:

```

AUTHOR_BUNDLE_START at byte: (양수)

AUTHOR_BUNDLE_END at byte: (START보다 큰 양수)

Range OK: true

Inner size: (수천 이상)

Has kanban code: true

Has cover-editor: true

```

  

`Range OK: false`이거나 kanban이 없으면 §5.1 대응 절 참고.

  

### 3.5 Session 1 게이트 체크리스트

  

- [ ] `build/inline.mjs`: SCRIPTS 플레이스홀더에 외부 AUTHOR_BUNDLE 마커 **없음**

- [ ] `src/main.js`: `/*! AUTHOR_BUNDLE_START */` / `/*! AUTHOR_BUNDLE_END */` 추가 완료

- [ ] `src/main.js`: `export-book.js` import 주석 처리 상태

- [ ] `node build/build.mjs` 에러 없이 완료

- [ ] `dist/bundle.js`에 `/*! AUTHOR_BUNDLE_START */` 존재

- [ ] `dist/bundle.js`에 `/*! AUTHOR_BUNDLE_END */` 존재, START보다 뒤

- [ ] 마커 사이에 kanban 코드 포함 확인

- [ ] `dist/ol-atlas.html`을 브라우저에서 열어 기본 기능 정상 (ATLAS 회귀 없음)

  

---

  

## 4. Session 2 — export-book.js 작성 + 버튼 연결

  

### 4.1 Step 1: src/components/author/export-book.js 신규 작성

  

```js

// src/components/author/export-book.js

// ── BOOK HTML 내보내기 ───────────────────────────────────

// AUTHOR_BUNDLE 마커 내에 위치.

// exportBook()이 자기 자신(이 파일)을 BOOK에서 제거하는 원리:

// __STATIC_HTML__은 JS 실행 전 캡처 → 이 코드는 이미 번들에 포함

// 하지만 BOOK HTML에서는 마커 사이 코드(이 파일 포함)가 제거됨.

  

import { S } from '../../core/state.js';

import { __STATIC_HTML__ } from '../../core/static-html.js';

import { dlBlob, toast, escapeHTML } from '../../core/utils.js';

import { slugFilename } from '../../core/constants.js';

import { customConfirm, customAlert } from '../../ui/confirm-modal.js';

import { devLog } from '../../core/dev.js';

  

// ── 진입점 ─────────────────────────────────────────────

export async function exportBook() {

devLog('EXPORT', 'exportBook start');

  

// 1. 유효성 검사

const manifest = S.book && S.book.manifest;

const validation = validateManifest(manifest);

if (!validation.ok) {

const proceed = await customConfirm({

title: 'BOOK 배포 전 확인',

message: '다음 항목이 비어있습니다:\n\n' + validation.warnings.join('\n') +

'\n\n그래도 배포하시겠습니까?',

confirmText: '배포',

cancelText: '취소',

});

if (!proceed) return;

}

  

// 2. 기반 HTML — 페이지 로드 시점에 캡처된 정적 HTML

let html = __STATIC_HTML__;

if (!html) {

customAlert({ title: '오류', message: '__STATIC_HTML__이 캡처되지 않았습니다.' });

return;

}

  

// 3. AUTHOR_BUNDLE 영역 제거

// 정규식이 자기 자신을 매치하지 않도록 문자열 concat으로 마커를 분리 구성

const MSTART = '/*! ' + 'AUTHOR_BUNDLE_START' + ' */';

const MEND = '/*! ' + 'AUTHOR_BUNDLE_END' + ' */';

const escRe = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

const bundleRe = new RegExp(escRe(MSTART) + '[\\s\\S]*?' + escRe(MEND), 'g');

html = html.replace(bundleRe, '/* [author bundle removed for BOOK] */');

  

// 4. BOOK 모드 마커 주입 + 5. 데이터 inline — 한 번에 처리

// DATA_VAR 스크립트 패턴: const __LOADED_DATA_B64__ = '...';

// window.__OL_MODE__='book' 을 선행 삽입하여 IIFE 실행 전 설정

const bookData = buildBookData();

const b64 = btoa(unescape(encodeURIComponent(JSON.stringify(bookData))));

const VAR = '__LOADED' + '_DATA_B64__';

const KEY = 'const ' + VAR + " = '";

const RE = new RegExp('const ' + VAR + " = '[^']*';");

html = html.replace(RE, `window.__OL_MODE__='book';\n${KEY}${b64}';`);

  

// 6. <title> 갱신

if (manifest && manifest.title) {

html = html.replace(

/<title>[^<]*<\/title>/,

`<title>${escapeHTML(manifest.title)}</title>`

);

}

  

// 7. 다운로드

const fname = slugFilename(

(manifest && manifest.title) || 'ol-book',

'ol-book'

) + '.html';

dlBlob(new Blob([html], { type: 'text/html;charset=utf-8' }), fname);

  

toast('BOOK으로 배포되었습니다 — ' + fname, 'success');

devLog('EXPORT', 'exportBook done:', fname);

}

  

// ── BOOK에 내장할 데이터 구성 ────────────────────────────

// 설계서 §5.1 포함 / §5.2 제외 정책 적용

function buildBookData() {

return {

meta: {

schemaVersion: 8,

olVersion: '0.8.0-book',

exportedAt: new Date().toISOString(),

},

cards: S.cards,

columns: S.columns,

userData: { status: {} }, // 독자 진행률은 BOOK의 localStorage에 별도 관리

nextColId: S.nextColId,

nextCardId: S.nextCardId,

book: { manifest: S.book && S.book.manifest },

settings: { theme: 'system', locale: S.settings && S.settings.locale },

// trash: 명시적 제외 — 미공개 콘텐츠 보호 (설계서 §5.2)

};

}

  

// ── 유효성 검사 ─────────────────────────────────────────

function validateManifest(m) {

const warnings = [];

if (!m || !m.title) warnings.push('· 책 제목이 비어있습니다');

if (!m || !m.id) warnings.push('· BOOK ID가 비어있습니다');

if (!m || !m.cover || !m.cover.image) warnings.push('· 표지 이미지가 없습니다');

return { ok: warnings.length === 0, warnings };

}

```

  

### 4.2 Step 2: src/main.js 수정 — export-book.js 주석 해제

  

`export-book.js` 라인 주석을 해제:

  

```js

/*! AUTHOR_BUNDLE_START */

import './components/author/kanban.js';

import './components/author/cardgrid.js';

import './components/author/listview.js';

import './components/author/home.js';

import './components/author/cover-editor.js';

import './components/author/export-book.js'; // ← 주석 해제

/*! AUTHOR_BUNDLE_END */

```

  

### 4.3 Step 3: src/components/shared/sidebar.js 수정

  

#### import 추가 (파일 상단 import 그룹에 추가)

  

```js

import { exportBook } from '../author/export-book.js';

```

  

#### buildCoverEditorSection 함수 수정

  

현재 코드 (line 440~458):

  

```js

function buildCoverEditorSection(rootEl) {

const sec = ce('div', 'sb-section');

const item = ce('div', 'sb-item' + (currentView === 'cover-editor' ? ' active' : ''));

item.innerHTML = `

<span class="sb-item-icon">

<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">

<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>

<path d="M14 2v6h6"></path>

<path d="M16 13H8"></path>

<path d="M16 17H8"></path>

</svg>

</span>

<span>표지 편집</span>`;

item.onclick = () => {

openCoverEditor();

};

sec.appendChild(item);

rootEl.appendChild(sec);

}

```

  

수정 후 — "BOOK으로 배포" 버튼 추가:

  

```js

function buildCoverEditorSection(rootEl) {

const sec = ce('div', 'sb-section');

  

// 표지 편집 버튼 (기존)

const coverItem = ce('div', 'sb-item' + (currentView === 'cover-editor' ? ' active' : ''));

coverItem.innerHTML = `

<span class="sb-item-icon">

<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">

<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>

<path d="M14 2v6h6"></path>

<path d="M16 13H8"></path>

<path d="M16 17H8"></path>

</svg>

</span>

<span>표지 편집</span>`;

coverItem.onclick = () => { openCoverEditor(); };

sec.appendChild(coverItem);

  

// BOOK으로 배포 버튼 (신규)

const bookItem = ce('div', 'sb-item');

bookItem.innerHTML = `

<span class="sb-item-icon">

<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">

<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>

<polyline points="7 10 12 15 17 10"></polyline>

<line x1="12" y1="15" x2="12" y2="3"></line>

</svg>

</span>

<span>BOOK으로 배포</span>`;

bookItem.onclick = () => { exportBook(); };

sec.appendChild(bookItem);

  

rootEl.appendChild(sec);

}

```

  

**주의**: `buildCoverEditorSection`은 sidebar.js 내에서 **두 곳**에서 호출된다 (데스크톱 뷰와 문서뷰 사이드바). 함수를 하나만 수정하면 두 곳 모두 반영된다.

  

### 4.4 Step 4: 빌드 실행

  

```bash

node build/build.mjs

```

  

### 4.5 Step 5: 동작 검증

  

**브라우저 검증** (`dist/ol-atlas.html` 열기):

  

1. 사이드바 하단에 "BOOK으로 배포" 버튼 표시 확인

2. 클릭 → 유효성 경고 다이얼로그 (표지 이미지 미설정 시) 또는 즉시 다운로드

3. 다운로드된 `[제목].html` 파일을 별도 탭에서 열기

  

**다운로드된 BOOK HTML DevTools 콘솔에서 검증**:

  

```js

// BOOK 파일에서 아래 명령 실행

console.log('mode:', window.__OL_MODE__); // 'book' 이어야 함

console.log('BUILD:', window.__OL_BUILD__); // 존재해야 함

console.log('ATLAS code removed:', typeof renderKanban); // 'undefined' 이어야 함

// 데이터 로드 확인 (IIFE 실행 후 전역 접근 불가 → 콘솔에서 확인 어려움)

// 대신 DOM에서 카드 관련 엘리먼트가 렌더됐는지 확인

```

  

**Node.js에서 BOOK 파일 구조 검증** (브라우저 없이):

  

```bash

node -e "

const fs = require('fs');

// BOOK HTML 파일명은 manifest.title 기반으로 생성됨 — 실제 파일명으로 수정

const html = fs.readFileSync('dist/[BOOK파일명].html', 'utf8');

  

const MSTART = '/*! ' + 'AUTHOR_BUNDLE_START' + ' */';

const MEND = '/*! ' + 'AUTHOR_BUNDLE_END' + ' */';

console.log('Author bundle removed:', !html.includes(MSTART) && !html.includes(MEND));

  

console.log('OL_MODE set:', html.includes(\"window.__OL_MODE__='book'\"));

  

const VAR = '__LOADED' + '_DATA_B64__';

const m = html.match(new RegExp('const ' + VAR + \" = '([^']+)';\"));

if (m) {

const json = decodeURIComponent(escape(atob(m[1])));

const data = JSON.parse(json);

console.log('cards count:', data.cards && data.cards.length);

console.log('book.manifest.title:', data.book && data.book.manifest && data.book.manifest.title);

console.log('trash excluded:', data.trash === undefined);

}

"

```

  

**예상 출력**:

```

Author bundle removed: true

OL_MODE set: true

cards count: [카드 수]

book.manifest.title: [책 제목]

trash excluded: true

```

  

### 4.6 Session 2 게이트 체크리스트

  

- [ ] `src/components/author/export-book.js` 파일 생성 완료

- [ ] `src/main.js`: `export-book.js` import 주석 해제

- [ ] `src/components/shared/sidebar.js`: `exportBook` import + 버튼 HTML 추가

- [ ] `node build/build.mjs` 에러 없이 완료

- [ ] ATLAS 사이드바에 "BOOK으로 배포" 버튼 표시

- [ ] 버튼 클릭 → 파일 다운로드 발생

- [ ] BOOK HTML 내 AUTHOR_BUNDLE 마커가 제거됨 (Node.js 검증)

- [ ] BOOK HTML 내 `window.__OL_MODE__='book'` 존재

- [ ] BOOK HTML 내 카드 데이터 내장 확인

- [ ] BOOK HTML 내 `trash` 필드 **없음** 확인

- [ ] ATLAS 기존 save/load 기능 회귀 없음 확인

  

---

  

## 5. 알려진 위험과 대응

  

### 5.1 esbuild legal comment 위치 보장 실패

  

**위험**: esbuild가 `/*! AUTHOR_BUNDLE_START */` 주석을 번들 내에서 예상 위치 밖에 배치할 수 있다 (예: shared 코드가 마커 안에 끼거나, 마커가 너무 좁은 범위를 감싸는 경우).

  

**확인**: Session 1 Gate에서 `node -e "..."` 검증으로 inner 범위에 kanban 코드 있는지 확인.

  

**대응 A**: 마커 사이에 불필요한 shared 코드가 포함된 경우 — BOOK 파일이 약간 커지지만 기능에는 문제없음. Phase 8.4에서 정밀 조정 가능.

  

**대응 B**: 마커가 번들에 전혀 없는 경우 (`Range OK: false`) — `build.mjs`에서 `legalComments` 옵션 확인. `legalComments: 'inline'`이 맞는지 재확인. 없으면 추가.

  

**대응 C**: 마커가 있으나 kanban이 마커 밖에 있는 경우 — `src/main.js`의 import 순서 재검토. shared 컴포넌트를 마커 앞으로, author 컴포넌트를 마커 안으로 명확히 분리.

  

### 5.2 minify 모드에서 마커 생략

  

`build.mjs`의 `legalComments: 'inline'` 설정이 minify 시에도 `/*! */` 주석을 보존한다. 이미 설정되어 있으므로 정상 작동 예상.

  

만약 문제 발생 시: `node build/build.mjs --dev`로 개발 모드 빌드하여 마커 존재 확인 후, 프로덕션 빌드와 비교.

  

### 5.3 DATA_VAR 스크립트 매칭 실패

  

`buildExportHTML(json)`과 동일한 정규식 패턴 `'[^']*'`을 사용하므로 기존에 검증된 패턴. ATLAS 파일을 OL로 저장 후 재열기한 경우에도 (DATA_VAR가 실제 base64) 정상 교체됨.

  

### 5.4 BOOK 파일에서 kanban 코드가 완전히 제거되지 않음

  

`export-import.js`는 마커 밖(`events.js` 경유)에 있으므로 BOOK에 포함된다. 이는 설계서 §5.2의 "제외 데이터"가 아니라 코드 제거 범위 문제. Phase 8.4에서 events.js의 ATLAS 전용 임포트를 마커 내부로 이동할 예정. Phase 8.3에서는 허용.

  

---

  

## 6. 커밋 가이드

  

Session 1 완료 후:

```bash

git add build/inline.mjs src/main.js

git commit -m "Phase 8.3 (1/2): AUTHOR_BUNDLE 마커를 bundle.js 내부로 이동

  

- build/inline.mjs: SCRIPTS 플레이스홀더에서 외부 마커 제거

- src/main.js: author import 그룹에 /*! AUTHOR_BUNDLE_START/END */ 추가

- esbuild legalComments: 'inline' 이 마커를 bundle.js에 보존"

```

  

Session 2 완료 후:

```bash

git add src/components/author/export-book.js src/components/shared/sidebar.js src/main.js

git commit -m "Phase 8.3 (2/2): exportBook() 구현 + BOOK 배포 버튼

  

- src/components/author/export-book.js: AUTHOR_BUNDLE 제거, 데이터 inline,

window.__OL_MODE__='book' 주입, Blob 다운로드

- src/components/shared/sidebar.js: BOOK으로 배포 버튼 추가

- src/main.js: export-book.js import 활성화"

  

git tag v0.8.0-phase8.3-complete

```

  

---

  

## 7. Phase 8.3 완료 후 상태

  

### 산출물

  

```

src/

├── main.js ← AUTHOR_BUNDLE 마커 추가

├── components/

│ ├── author/

│ │ └── export-book.js ← 신규: exportBook() 함수

│ └── shared/

│ └── sidebar.js ← BOOK 배포 버튼 추가

build/

└── inline.mjs ← 외부 AUTHOR_BUNDLE 마커 제거

```

  

### BOOK 파일 구조

  

```

[제목].html (다운로드)

├── <head>

│ ├── <title>[manifest.title]</title>

│ └── <style>...</style>

├── <body>

│ └── <script>

│ window.__OL_MODE__='book';

│ const __LOADED_DATA_B64__ = '[base64 encoded bookData]';

│ </script>

│ └── <script>

│ (()=>{

│ // CORE, ACTIONS, SHARED, READER ...

│ /* [author bundle removed for BOOK] */

│ // boot()

│ })();

│ </script>

└── </body>

```

  

### 다음 Phase (Phase 8.4)

  

- `bootBook()` / `detectMode()` 구현 → BOOK 파일을 열면 cover-page가 첫 화면으로 표시

- reader 전용 sidebar 항목 구성

- BOOK 파일에서 ATLAS 편집 UI 숨기기

- events.js의 ATLAS 전용 import 정리 (export-import.js의 마커 내부 이동 검토)