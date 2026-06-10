# Phase 0 작업지시서 — Claude CLI 작업용

**대상**: OL ATLAS v0.7 Phase 0 **작업 환경**: 로컬 PC + Claude CLI **선행 문서**: `OL_ATLAS_v0_7_최종_기획서_v2.md` **Phase 0 목표 일수**: 2~4일

---

## 0. 작업 개요

Phase 0은 v0.7의 모든 후속 작업의 기반이다. **이 단계의 산출물(`dist/ol-atlas.html`)이 v0.6과 기능적으로 동등해야** Phase 1으로 진입할 수 있다.

### 0.1 Phase 0의 핵심 임무

1. v0.6의 단일 HTML 파일(`OL_ATLAS_v0_6.html`)을 `src/` 모듈 구조로 **수작업 분해**
2. esbuild 기반 빌드 파이프라인 구축 (`build/build.mjs`)
3. CSS·JS·아이콘을 단일 HTML로 인라이닝하는 후처리 (`build/inline.mjs`)
4. `__STATIC_HTML__` 캡처와 `__LOADED_DATA_B64__` 자기참조 보호 패턴 보존
5. `npm run dev` (개발 서버), `npm run build` (배포 산출물) 명령 정착
6. v0.6 기능 동등성 회귀 테스트 통과

### 0.2 Phase 0이 다루지 않는 것 (Phase 1 이후로 미룸)

- ❌ Action Layer, Store, Render Queue 도입 (Phase 1)
- ❌ Dirty State, autosave, beforeunload (Phase 1)
- ❌ 새 UI 작업 (Phase 3 이후)
- ❌ schema v6→v7 마이그레이션 (Phase 1)

**Phase 0의 핵심 원칙**: v0.6 코드를 **그대로 모듈로 쪼개기만** 한다. 로직 변경 금지. 리팩토링 금지. **순수 분해 작업**.

---

## 1. 작업 환경 셋업

### 1.1 디렉토리 초기화

```bash
mkdir -p ol-atlas
cd ol-atlas
mkdir -p src/{core,data,ui,components,styles}
mkdir -p src/data/search
mkdir -p build dist
```

### 1.2 package.json 생성

```json
{
  "name": "ol-atlas",
  "version": "0.7.0-dev",
  "type": "module",
  "private": true,
  "scripts": {
    "dev": "node build/dev-server.mjs",
    "build": "node build/build.mjs",
    "build:verify": "node build/verify.mjs",
    "check": "node --check dist/check-syntax.js 2>&1"
  },
  "devDependencies": {
    "esbuild": "^0.21.0",
    "jsdom": "^24.0.0"
  }
}
```

```bash
npm install
```

### 1.3 .gitignore

```
node_modules/
dist/
.DS_Store
*.log
```

---

## 2. v0.6 HTML 분해 — 매핑표

v0.6 HTML(`OL_ATLAS_v0_6.html`, 약 11,700줄)을 다음과 같이 분해한다. **각 모듈은 v0.6의 해당 영역을 그대로 옮기고, ES module export만 추가**한다.

### 2.1 core/ — 핵심 인프라

|대상 파일|v0.6 추출 범위|비고|
|---|---|---|
|`src/core/origin.js`|`ORIGIN = Object.freeze({...})`|하드코딩 그대로|
|`src/core/state.js`|`let S`, `makeDefault()`, `normalizeState()`, `normalizeCard()`|기존 로직 변경 금지|
|`src/core/storage.js`|`save()`, `load()` (localStorage 접근부)|추상화는 Phase 1에서|
|`src/core/id.js`|`slugFilename()`, `titleToSlug()`, `ensureUniqueSlug()`, `newImgId()`, `safeImgAlt()`||
|`src/core/dev.js`|(신규 작성)|본 지시서 §4 참조|

### 2.2 data/ — 데이터 변환

|대상 파일|v0.6 추출 범위|
|---|---|
|`src/data/card.js`|`bodyImagesToTokens()`, `bodyTokensToStandardMd()`, `cardPreviewText()`, `cardSearchText()`, `VALID_PRIORITIES`|
|`src/data/tag.js`|`parseTag()`, `buildPrefixIndex()`, `getFreeTags()`, `countCardsWithPrefixValue()`, `countCardsWithFreeTag()`|
|`src/data/markdown.js`|`escapeHTML()`, `sanitizeURL()`, `parseInline()`, `parseMarkdown()`, `stripMarkdown()`|

### 2.3 ui/ — 뷰

|대상 파일|v0.6 추출 범위|
|---|---|
|`src/ui/sidebar.js`|`renderSidebar()`, `renderSidebarForDocView()`, `buildDocTreeCard()`, `setPrefixFilter()`, `clearPrefixFilter()`, `buildSbDropdown()`, `refreshSbTagList()`, `refreshSbTagClearBtn()`, sb 관련 전역|
|`src/ui/kanban.js`|`renderKanban()` 및 종속 함수들|
|`src/ui/cards.js`|`renderCards()` 및 종속 함수들|
|`src/ui/list.js`|`renderList()` 및 종속 함수들|
|`src/ui/docview.js`|`renderDocumentView()`, `renderDocBody()`, `renderDocToc()`|
|`src/ui/about.js`|`renderAbout()`|
|`src/ui/header.js`|헤더 관련 렌더 + 이벤트 핸들러|
|`src/ui/router.js`|`currentView` 전역 + view 전환 로직(`if v === 'kanban' renderKanban()...`)|

### 2.4 components/ — 공용 컴포넌트

|대상 파일|v0.6 추출 범위|
|---|---|
|`src/components/dropdown.js`|`closeOpenDrop()`, `_openDrop`, custom select 로직|
|`src/components/icons.js`|`ICONS_X` 사전 (인라인 SVG)|
|`src/components/empty.js`|`EMPTY_ICONS`, `buildEmptyState()`|
|`src/components/utils.js`|`ce()`, `today()`, `dlBlobSequential()`|

### 2.5 styles/ — CSS

v0.6의 `<style>` 블록 전체를 다음 4개 파일로 분리:

|대상 파일|내용|
|---|---|
|`src/styles/tokens.css`|`:root` HSL 토큰 + `html.dark, :root.dark`|
|`src/styles/base.css`|reset, body, 시스템 폰트|
|`src/styles/components.css`|`.btn`, `.input`, `.card`, `.dialog`, badge, popover 등 공용|
|`src/styles/views.css`|sidebar, kanban, cards, list, docview, about, header|

**중요**: CSS 주석(`/* */`)을 절대 잃지 말 것. 메모리 기록된 `.overlay` 사고 재발 방지.

### 2.6 메인 파일

|대상 파일|내용|
|---|---|
|`src/index.html`|빈 셸: `<head>` 메타 + favicon + `<body><div id="app"></div><script type="module" src="boot.js"></script></body>`|
|`src/boot.js`|모든 모듈 import + `__STATIC_HTML__` 캡처 + `load()` + 첫 렌더 호출 (현재 v0.6의 부팅 순서 그대로)|

---

## 3. ES Module 변환 규칙

### 3.1 변환 원칙

각 함수/상수를 모듈로 옮길 때:

1. **로직은 한 글자도 바꾸지 않는다.**
2. 모듈 상단에 필요한 import 추가.
3. 모듈 하단(또는 선언부에서) `export` 추가.
4. v0.6의 전역 의존성은 **명시적 import로 변환**.

### 3.2 변환 예시

**v0.6 (단일 HTML)**:

```js
function parseTag(tag) {
  const colonIdx = tag.indexOf(':');
  // ...
}

function buildPrefixIndex(cards) {
  const result = {};
  for (const card of cards) {
    for (const tag of (card.tags || [])) {
      const parsed = parseTag(tag);
      // ...
    }
  }
  return result;
}
```

**Phase 0 분해 후 (`src/data/tag.js`)**:

```js
// src/data/tag.js

export function parseTag(tag) {
  const colonIdx = tag.indexOf(':');
  // ...
}

export function buildPrefixIndex(cards) {
  const result = {};
  for (const card of cards) {
    for (const tag of (card.tags || [])) {
      const parsed = parseTag(tag);
      // ...
    }
  }
  return result;
}
```

`parseTag`는 같은 파일이므로 import 불필요. 다른 파일에서 사용하는 곳:

```js
// src/ui/sidebar.js
import { parseTag, buildPrefixIndex, getFreeTags } from '../data/tag.js';
import { devLog } from '../core/dev.js';

export function renderSidebar() {
  devLog('BOOT', 'renderSidebar called');
  const index = buildPrefixIndex(S.cards);
  // ... 기존 로직 그대로
}
```

### 3.3 전역 `S` 객체 처리 — Phase 0의 가장 까다로운 점

v0.6은 전역 `let S` 하나로 모든 모듈이 공유한다. Phase 1에서 Store로 대체하지만, **Phase 0에서는 그대로 전역 공유를 유지**해야 한다 (로직 변경 금지 원칙).

해결책: `src/core/state.js`에서 `S`를 export하고, 모든 모듈이 import.

```js
// src/core/state.js
export let S;

export function setState(newS) {
  S = newS;
}

export function getS() {
  return S;
}

export function makeDefault() { /* v0.6 그대로 */ }
export function normalizeState(s) { /* v0.6 그대로 */ }
export function normalizeCard(c) { /* v0.6 그대로 */ }
```

```js
// 다른 모듈에서
import { S, setState } from '../core/state.js';

// 읽기는 S 그대로
const cards = S.cards;

// 수정도 일단 Phase 0에서는 직접 mutation 유지 (v0.6 그대로)
S.cards.push(newCard);
// Phase 1에서 dispatch로 전환
```

**주의**: ES module은 export된 `let` 바인딩이 import 측에서 readonly로 보이지만, 객체 내부 mutation은 가능하다. Phase 0 분해 작업 동안 이 패턴을 임시 유지하고, Phase 1에서 일괄 제거한다.

---

## 4. dev.js 신규 작성 (개발 전용 로그/디버그)

### 4.1 src/core/dev.js

```js
// src/core/dev.js
// 개발 전용 로그/디버그 유틸. 빌드 시 esbuild --define으로 __DEV__=false 박혀 제거됨.

export const DEV = typeof __DEV__ !== 'undefined' ? __DEV__ : true;

const COLORS = {
  ACTION:   'color: #3b82f6; font-weight: bold',
  REDUCER:  'color: #8b5cf6',
  QUEUE:    'color: #f59e0b',
  FLUSH:    'color: #10b981; font-weight: bold',
  DIRTY:    'color: #ef4444',
  MIGRATE:  'color: #ec4899; font-weight: bold',
  BOOT:     'color: #6366f1; font-weight: bold',
  STORAGE:  'color: #14b8a6',
  PERF:     'color: #71717a; font-style: italic',
  RENDER:   'color: #0ea5e9',
};

export function devLog(category, ...args) {
  if (!DEV) return;
  console.log(`%c[${category}]`, COLORS[category] || '', ...args);
}

export function devWarn(category, ...args) {
  if (!DEV) return;
  console.warn(`%c[${category}]`, COLORS[category] || '', ...args);
}

export function devError(category, ...args) {
  if (!DEV) return;
  console.error(`%c[${category}]`, COLORS[category] || '', ...args);
}

export function devAssert(cond, msg) {
  if (!DEV) return;
  if (!cond) {
    console.error(`[ASSERT FAIL] ${msg}`);
    debugger;
  }
}

export function devTime(label) {
  if (!DEV) return { end: () => {} };
  const start = performance.now();
  return {
    end: () => devLog('PERF', `${label}: ${(performance.now() - start).toFixed(2)}ms`),
  };
}

export function devGroup(category, label, fn) {
  if (!DEV) { fn(); return; }
  console.groupCollapsed(`%c[${category}]`, COLORS[category] || '', label);
  try { fn(); } finally { console.groupEnd(); }
}
```

### 4.2 Phase 0에서의 dev.js 활용

Phase 0 분해 작업 중에는 다음 지점에만 로그를 박는다 (과도한 로그 금지):

```js
// src/boot.js
import { devLog } from './core/dev.js';

devLog('BOOT', 'boot start');
// ... 기존 v0.6 부팅 코드 ...
devLog('BOOT', 'boot complete, state loaded:', S.cards.length, 'cards');
```

```js
// src/core/storage.js
import { devLog } from './dev.js';

export function save() {
  devLog('STORAGE', 'save called');
  // ... v0.6 그대로
}

export function load() {
  devLog('STORAGE', 'load called');
  // ... v0.6 그대로
}
```

Phase 1 이후로 Action·Reducer·Queue·Flush 지점에 추가한다.

---

## 5. 빌드 시스템

### 5.1 build/build.mjs

```js
// build/build.mjs
import * as esbuild from 'esbuild';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { inlineToSingleHtml } from './inline.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const SRC = join(ROOT, 'src');
const DIST = join(ROOT, 'dist');

async function build() {
  console.log('[build] start');
  await mkdir(DIST, { recursive: true });

  // 1. JS 번들 (IIFE, 자기참조 정규식 보호를 위해 단일 출력)
  const jsResult = await esbuild.build({
    entryPoints: [join(SRC, 'boot.js')],
    bundle: true,
    format: 'iife',
    target: 'es2020',
    define: {
      __DEV__: 'false',  // 프로덕션: 모든 devLog 등 제거됨
    },
    minify: false,  // Phase 0에서는 minify 끄기 (디버깅 용이)
    write: false,
    sourcemap: false,
  });
  const jsCode = jsResult.outputFiles[0].text;
  console.log(`[build] JS bundle: ${(jsCode.length / 1024).toFixed(1)} KB`);

  // 2. CSS concat (순서 중요: tokens → base → components → views)
  const cssFiles = [
    'styles/tokens.css',
    'styles/base.css',
    'styles/components.css',
    'styles/views.css',
  ];
  let cssCode = '';
  for (const f of cssFiles) {
    cssCode += `\n/* ===== ${f} ===== */\n`;
    cssCode += await readFile(join(SRC, f), 'utf8');
  }
  console.log(`[build] CSS concat: ${(cssCode.length / 1024).toFixed(1)} KB`);

  // 3. HTML 셸 읽기 + 인라이닝
  const htmlShell = await readFile(join(SRC, 'index.html'), 'utf8');
  const finalHtml = await inlineToSingleHtml(htmlShell, jsCode, cssCode);
  console.log(`[build] Final HTML: ${(finalHtml.length / 1024).toFixed(1)} KB`);

  // 4. 출력
  const outPath = join(DIST, 'ol-atlas.html');
  await writeFile(outPath, finalHtml, 'utf8');
  console.log(`[build] written to ${outPath}`);
}

build().catch(err => {
  console.error('[build] FAILED:', err);
  process.exit(1);
});
```

### 5.2 build/inline.mjs

```js
// build/inline.mjs

export async function inlineToSingleHtml(htmlShell, jsCode, cssCode) {
  // 1. <link rel="stylesheet"> 또는 placeholder를 인라인 <style>로 치환
  let out = htmlShell.replace(
    /<!--\s*INJECT_CSS\s*-->/,
    `<style>\n${cssCode}\n</style>`
  );

  // 2. <script type="module" src="boot.js"> 또는 placeholder를 인라인 <script>로 치환
  out = out.replace(
    /<script[^>]*src="[^"]*boot\.js"[^>]*><\/script>/,
    `<script>\n${jsCode}\n</script>`
  );
  out = out.replace(
    /<!--\s*INJECT_JS\s*-->/,
    `<script>\n${jsCode}\n</script>`
  );

  return out;
}
```

### 5.3 build/dev-server.mjs (단순 정적 서버)

```js
// build/dev-server.mjs
// Phase 0 개발 시: src/index.html을 ES modules 그대로 서빙

import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { join, extname, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const SRC = join(ROOT, 'src');
const PORT = 5757;

const MIME = {
  '.html': 'text/html',
  '.js':   'application/javascript',
  '.css':  'text/css',
  '.svg':  'image/svg+xml',
  '.json': 'application/json',
};

createServer(async (req, res) => {
  let path = req.url.split('?')[0];
  if (path === '/') path = '/index.html';
  const filePath = join(SRC, path);
  try {
    const data = await readFile(filePath);
    res.writeHead(200, { 'Content-Type': MIME[extname(path)] || 'application/octet-stream' });
    res.end(data);
  } catch (err) {
    res.writeHead(404);
    res.end('Not found');
  }
}).listen(PORT, () => {
  console.log(`[dev] http://localhost:${PORT}`);
});
```

### 5.4 build/verify.mjs (빌드 산출물 검증)

```js
// build/verify.mjs
import { readFile } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DIST_HTML = join(__dirname, '..', 'dist', 'ol-atlas.html');

async function verify() {
  console.log('[verify] start');
  const html = await readFile(DIST_HTML, 'utf8');
  const checks = [];

  // 1. 외부 자원 참조 없음
  if (/<link[^>]+href="https?:/.test(html)) {
    checks.push('FAIL: external stylesheet link found');
  }
  if (/<script[^>]+src="https?:/.test(html)) {
    checks.push('FAIL: external script src found');
  }

  // 2. ORIGIN 보존
  if (!/biwoom/i.test(html) || !/CC BY-SA 4\.0/.test(html)) {
    checks.push('FAIL: ORIGIN constants not found');
  }

  // 3. 자기참조 정규식 패턴 보존 (export 기능)
  // (실제 패턴은 분해 후 보존 여부 확인)
  if (!/__LOADED.*_DATA_B64__/.test(html)) {
    checks.push('FAIL: LOADED_DATA_B64 marker missing');
  }

  // 4. DEV 로그가 프로덕션에 안 남아있어야 (esbuild가 제대로 제거했는지)
  if (/\[ACTION\]|\[REDUCER\]|\[FLUSH\]/.test(html)) {
    checks.push('WARN: dev log markers found in production build');
  }

  // 5. CSS 주석 무결성 (시작/끝 짝)
  const cssOpen = (html.match(/\/\*/g) || []).length;
  const cssClose = (html.match(/\*\//g) || []).length;
  if (cssOpen !== cssClose) {
    checks.push(`FAIL: CSS comment mismatch /*: ${cssOpen}, */: ${cssClose}`);
  }

  if (checks.length === 0) {
    console.log('[verify] PASS — all checks ok');
    return 0;
  }
  console.error('[verify] FAIL:');
  checks.forEach(c => console.error('  -', c));
  return 1;
}

verify().then(code => process.exit(code));
```

---

## 6. v0.6 부팅 순서 보존 — boot.js

v0.6의 `__STATIC_HTML__` 캡처 타이밍이 깨지면 export 기능이 작동하지 않는다.

```js
// src/boot.js
import { devLog } from './core/dev.js';

devLog('BOOT', 'boot.js start');

// 1. __STATIC_HTML__ 캡처 — JS 실행 직전의 HTML 스냅샷
// v0.6에서는 inline <script>에 있었음. 빌드 후에도 같은 타이밍에 캡처되어야 함.
const __STATIC_HTML__ = document.documentElement.outerHTML;

// 2. 코어 import (state, storage, schema)
import './core/state.js';
import { load, save } from './core/storage.js';
// ... (정확한 import 목록은 분해 결과에 따라)

// 3. 데이터/UI 모듈 import
import './data/card.js';
import './data/tag.js';
import './data/markdown.js';
import './ui/sidebar.js';
import './ui/kanban.js';
// ...

// 4. 부팅 실행
function boot() {
  devLog('BOOT', 'load state');
  load();
  
  devLog('BOOT', 'initial render');
  // v0.6의 부팅 순서 그대로
  // ...
}

boot();
devLog('BOOT', 'boot complete');

// __STATIC_HTML__를 전역에 노출 (export 기능에서 필요)
window.__STATIC_HTML__ = __STATIC_HTML__;
```

**주의**: ES module의 import는 호이스팅된다. `__STATIC_HTML__` 캡처가 import 이전에 실행되도록 하려면, **단일 IIFE로 번들된 결과물에서도** 캡처 라인이 가장 먼저 실행되어야 한다. esbuild는 import를 평탄화하므로, `boot.js`의 위치가 그대로 유지된다 — 단, 다른 모듈의 top-level 코드가 먼저 실행될 수 있으므로 검증 필수.

**검증 방법**: 빌드 후 dist HTML을 열어서 `<script>` 블록 안의 첫 100줄을 확인. `document.documentElement.outerHTML` 캡처가 다른 어떤 DOM 조작보다 먼저 와야 함.

---

## 7. Phase 0 단계별 검증 리스트

각 단계를 끝낼 때마다 체크. 미달이면 다음 단계로 진행 금지.

### Step 0.1 — 디렉토리·패키지 셋업

- [ ] `ol-atlas/` 디렉토리 생성됨
- [ ] `src/`, `build/`, `dist/` 하위 폴더 모두 생성됨
- [ ] `package.json` 작성, `npm install` 성공
- [ ] `esbuild`, `jsdom` 설치 확인 (`node_modules/esbuild`, `node_modules/jsdom` 존재)

### Step 0.2 — v0.6 HTML 분해 (가장 큰 단계)

- [ ] §2 매핑표의 모든 파일이 생성됨
- [ ] 각 파일이 v0.6의 해당 영역을 **그대로 옮긴 것**이지, **다시 쓴 것이 아님**을 확인
- [ ] 각 모듈에 `export` 키워드 추가됨
- [ ] 다른 모듈을 참조하는 경우 `import` 추가됨
- [ ] 전역 `S` 객체가 `src/core/state.js`에서 export되고 모든 사용처가 import함
- [ ] CSS 4개 파일이 v0.6 `<style>` 블록을 누락 없이 분리함
    - [ ] CSS 주석(`/* */`)의 시작/끝 개수가 일치
    - [ ] `.overlay`, `.dialog`, `.modal` 등 핵심 클래스 보존

**검증 명령**:

```bash
# 분해된 JS 파일 모두 문법 체크
find src -name '*.js' -exec node --check {} \;

# CSS 주석 짝 확인
grep -o '/\*' src/styles/*.css | wc -l
grep -o '\*/' src/styles/*.css | wc -l
# 두 숫자가 일치해야 함
```

### Step 0.3 — 개발 서버 작동

- [ ] `npm run dev` 실행 → `http://localhost:5757` 응답
- [ ] 브라우저에서 열면 OL ATLAS v0.6과 동일한 화면이 보임
- [ ] 콘솔에 `[BOOT]` 로그가 보임 (dev.js 작동 확인)
- [ ] 콘솔에 에러 없음 (404, import 실패 등)

**검증 시나리오**:

1. 카드 추가 → 작동
2. 카드 편집 → 작동
3. 사이드바 필터 → 작동
4. 칸반/카드/리스트 뷰 전환 → 작동
5. 다크모드 토글 → 작동
6. 검색 → 작동
7. 저장 → localStorage에 반영

### Step 0.4 — 빌드 산출물 생성

- [ ] `npm run build` 실행 → `dist/ol-atlas.html` 생성됨
- [ ] 빌드 로그에 에러 없음
- [ ] `dist/ol-atlas.html` 파일 크기 합리적 (v0.6 대비 ±30% 이내, esbuild 번들 효율 고려)

### Step 0.5 — 빌드 산출물 검증

- [ ] `npm run build:verify` 실행 → 모든 체크 PASS
- [ ] dist HTML을 더블클릭(또는 `file://` 열기)로 열어서 v0.6과 동등 작동 확인
    - [ ] Step 0.3의 7가지 시나리오 모두 작동
    - [ ] export(저장) 기능 작동 → `__STATIC_HTML__` 캡처 정상
    - [ ] 저장된 파일을 다시 열면 데이터 복원됨
- [ ] 브라우저 콘솔에 `[BOOT]`, `[ACTION]` 등 dev 로그가 **없음** (esbuild가 제거했음)
- [ ] `grep -E '\[ACTION\]|\[FLUSH\]|console\.log' dist/ol-atlas.html` 결과 0건 (또는 v0.6의 의도된 로그만)

### Step 0.6 — v0.6 데이터 호환성

기존 v0.6 사용자가 저장해둔 HTML 파일을 v0.7 Phase 0 dist로 열어도 데이터가 보여야 한다.

- [ ] v0.6에서 export한 HTML 파일 준비 (실제 사용 파일 또는 샘플)
- [ ] v0.7 Phase 0 dist에서 "열기" → v0.6 파일 선택 → 데이터 로드됨
- [ ] 카드 개수·태그·컬럼 모두 보존됨
- [ ] localStorage 키(`ol_state`, `ol_theme` 등)도 v0.6과 동일하게 작동

### Step 0.7 — Phase 1 진입 게이트 (최종)

위 모든 항목을 통과하면 Phase 0 완료.

- [ ] **v0.6 기능 동등성 100% 확인** (모든 기능이 v0.6과 동일하게 작동)
- [ ] **외부 의존성 0** (dist HTML이 self-contained)
- [ ] **dev 로그 빌드 시 제거 확인**
- [ ] **CSS 무결성 확인**
- [ ] **`__STATIC_HTML__` + export 보존 확인**

Phase 1으로 진입 가능.

---

## 8. 작업 순서 권장안

Claude CLI에게 한 번에 모든 걸 시키지 말 것. 다음 순서로 쪼개서 지시:

### 첫 세션

1. Step 0.1 (디렉토리 + package.json)
2. 빌드 스크립트 셸만 작성 (`build.mjs`, `inline.mjs`, `dev-server.mjs`, `verify.mjs`)
3. `src/core/dev.js` 작성
4. `src/index.html` 빈 셸 작성

### 두 번째 세션

5. core/ 모듈 분해 (origin, state, storage, id)
6. data/ 모듈 분해 (card, tag, markdown)
7. 분해 후 `node --check`로 문법 검증

### 세 번째 세션

8. ui/ 모듈 분해 (sidebar, kanban, cards, list, docview, about, header, router)
9. components/ 모듈 분해

### 네 번째 세션

10. styles/ CSS 분리
11. boot.js 작성 + `__STATIC_HTML__` 캡처 타이밍 확인
12. `npm run dev`로 첫 실행 → Step 0.3 검증

### 다섯 번째 세션

13. `npm run build` → Step 0.4, 0.5 검증
14. v0.6 호환성 테스트 → Step 0.6
15. Phase 0 게이트 통과 확인 → Step 0.7

각 세션 끝에 git commit. 문제 생기면 이전 세션으로 롤백.

---

## 9. 자주 발생할 수 있는 문제 + 대응

### 9.1 `__STATIC_HTML__` 캡처가 깨짐

**증상**: export 후 다시 열면 빈 HTML이 됨.

**원인**: esbuild 번들에서 `document.documentElement.outerHTML` 호출 시점이 다른 DOM 조작보다 늦어짐.

**대응**:

- `boot.js`의 최상단(import 라인 직후)에 캡처 라인 위치
- 빌드 후 dist HTML 열어서 `<script>` 안의 코드 흐름 확인
- 필요시 캡처를 `index.html`의 별도 `<script>` 블록(번들 전)으로 분리하고 `window.__STATIC_HTML__`로 노출

### 9.2 CSS 주석으로 인한 규칙 무효화 (메모리 기록 사고)

**증상**: 모달이 일반 블록처럼 렌더링됨, overlay 작동 안 함.

**원인**: CSS 분리 중 주석 짝이 깨짐.

**대응**:

- `npm run build:verify`의 CSS 주석 검증이 잡음
- 수동 확인: `grep -c '/\*' src/styles/*.css` vs `grep -c '\*/' src/styles/*.css`

### 9.3 esbuild가 `__DEV__` 못 알아봄

**증상**: 빌드된 HTML에 `[ACTION]`, `[BOOT]` 등 로그가 그대로 남음.

**원인**: `define` 설정 누락 또는 `typeof __DEV__` 패턴이 esbuild의 분석 범위 밖.

**대응**:

- `build.mjs`의 `define: { __DEV__: 'false' }` 확인
- `src/core/dev.js`에서 `typeof __DEV__ !== 'undefined' ? __DEV__ : true` 패턴이 esbuild에 의해 평가되는지 확인
- 안 되면 `import.meta.env.DEV` 같은 대체 패턴 사용

### 9.4 자기참조 정규식 패턴 (`__LOADED_DATA_B64__`)이 깨짐

**증상**: export 시 데이터가 박히지 않거나, 재실행 시 데이터 로드 실패.

**원인**: 빌드 과정에서 마커 문자열이 변형됨.

**대응**:

- 메모리 기록된 패턴 보존: `const VAR = '__LOADED' + '_DATA_B64__'` + `new RegExp(VAR + ...)`
- 빌드 산출물에서 마커가 정확한 문자열로 남았는지 grep으로 확인
- esbuild가 문자열 concat을 상수 폴딩할 수 있으므로, **분리 형태가 유지되는지** 빌드 후 검증

---

## 10. Phase 0 완료 후 다음 행동

Phase 0 게이트를 모두 통과하면:

1. git 태그 `v0.7-phase0-complete` 부여
2. `OL_ATLAS_v0_7_최종_기획서_v2.md` 갱신: Phase 0 완료 표시
3. Phase 1 작업지시서 작성 요청
4. Phase 1은 가장 위험한 구간이므로, Phase 0 완료 시점에서 다시 한번 v0.6 동등성을 점검한 뒤 진입

---

## 부록 A — Claude CLI 지시 프롬프트 템플릿

각 세션 시작 시 다음 형식으로 지시:

```
[작업 컨텍스트]
- 프로젝트: OL ATLAS v0.7 Phase 0
- 작업 디렉토리: <경로>
- 참조 문서: OL_ATLAS_v0_7_Phase0_작업지시서.md
- 현재 단계: Step 0.X — <설명>

[이번 세션 목표]
- <구체적 산출물 1>
- <구체적 산출물 2>

[제약]
- v0.6 로직 변경 금지. 순수 분해만.
- 각 파일 작성 후 `node --check`로 문법 검증
- 모듈 import 경로 정확히 (상대경로)
- 작업 끝에 git diff 요약 출력
```

## 부록 B — 검증 체크리스트 한 페이지 요약

```
[Step 0.1] 디렉토리 + package.json ........ [ ]
[Step 0.2] v0.6 HTML 분해 ................. [ ]
  ├ core/ 모듈 ......................... [ ]
  ├ data/ 모듈 ......................... [ ]
  ├ ui/ 모듈 ........................... [ ]
  ├ components/ 모듈 ................... [ ]
  ├ styles/ CSS 4분할 .................. [ ]
  └ CSS 주석 짝 일치 ................... [ ]
[Step 0.3] npm run dev 작동 ............... [ ]
  └ v0.6 시나리오 7종 통과 ............. [ ]
[Step 0.4] npm run build 성공 ............. [ ]
[Step 0.5] npm run build:verify PASS ...... [ ]
  ├ 외부 의존성 0 ...................... [ ]
  ├ ORIGIN 보존 ........................ [ ]
  ├ LOADED_DATA_B64 마커 보존 .......... [ ]
  ├ dev 로그 제거 확인 ................. [ ]
  └ CSS 주석 짝 일치 ................... [ ]
[Step 0.6] v0.6 데이터 호환성 ............. [ ]
[Step 0.7] Phase 1 진입 게이트 ............ [ ]
```

---

**작성**: Claude (with biwoom) **다음 문서**: Phase 1 작업지시서 (Phase 0 완료 후 작성)