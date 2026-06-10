# OL ATLAS — v0.0.4 Dev 서버 구현 작업지시서

**버전**: v0.0.4 (dev 인프라) **작성일**: 2026-05-25 **목적**: esbuild 내장 서버로 개발 환경 구축 — 소스 변경 시 자동 재빌드 + 브라우저 자동 새로고침

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
npm run build → dist/ol-atlas_v0.0.4.html
npm run dev   → dist/ol-atlas_dev.html (dev 전용 고정명, 버전 없음)
```

---

## 현재 구조 파악

```
프로젝트/
├── build/
│   ├── build.mjs     ← prod 빌드 (현재 존재)
│   └── inline.mjs    ← HTML 인라인 조립 (현재 존재)
├── src/
│   ├── main.js       ← 번들 진입점
│   ├── index.html    ← HTML 템플릿
│   └── styles/       ← CSS 파일들
├── dist/             ← 빌드 산출물
└── package.json
```

현재 `build.mjs`가 esbuild로 번들링 + `inline.mjs`로 단일 HTML 조립하는 구조. Dev 서버는 이 파이프라인과 **별도**로 동작하며, `src/index.html`을 직접 서빙한다.

---

## 구현 방식 개요

```
npm run dev 실행 시:
  1. esbuild context 생성 (watch 모드)
  2. esbuild 내장 서버 (포트 3000) 시작
  3. 소스 변경 감지 → 자동 재빌드
  4. 재빌드 완료 → 브라우저에 SSE(EventSource)로 신호 전송
  5. 브라우저 자동 새로고침

접속: http://localhost:3000
```

**Dev vs Prod 차이점**

|항목|Dev (`npm run dev`)|Prod (`npm run build`)|
|---|---|---|
|출력 형식|`src/index.html` + `bundle.js` 분리|단일 인라인 HTML|
|번들|minify 없음, 소스맵 포함|minify, 소스맵 없음|
|서빙|localhost:3000 (esbuild 서버)|파일 직접 열기|
|파일명|`ol-atlas_dev.html` (빌드 시)|`ol-atlas_v0.0.4.html`|
|`__LOADED_DATA_B64__`|dev fixture 데이터 주입|`__INIT_DATA_B64__` 플레이스홀더|

---

## Phase 1 — `build/dev.mjs` 신규 작성

### 1.1 파일 전체 내용

```js
// build/dev.mjs
// OL ATLAS Dev Server — esbuild 내장 서버 + 자동 새로고침

import * as esbuild from 'esbuild';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
const SRC  = resolve(ROOT, 'src');
const DIST = resolve(ROOT, 'dist');

// ── 설정 ──────────────────────────────────────────────
const PORT = 3000;

// ── CSS 파일 목록 (build.mjs와 동일하게 유지) ─────────
// build.mjs의 CSS 목록을 참조하여 동일하게 맞출 것
// 예시 (실제 build.mjs의 CSS 순서를 그대로 복사):
const CSS_FILES = [
  'styles/tokens.css',
  'styles/base.css',
  'styles/components.css',
  'styles/sidebar.css',
  'styles/kanban.css',
  'styles/cardgrid.css',
  'styles/listview.css',
  'styles/docview.css',
  'styles/modal.css',
];

// ── dev용 HTML 생성 ───────────────────────────────────
// src/index.html을 기반으로 dev 전용 태그 주입
function buildDevHtml(pkg) {
  let html = readFileSync(resolve(SRC, 'index.html'), 'utf8');

  // CSS 인라인 주입 (prod와 동일하게 <style> 블록으로)
  const css = CSS_FILES
    .map(f => readFileSync(resolve(SRC, f), 'utf8'))
    .join('\n');
  html = html.replace('</head>', `<style>\n${css}\n</style>\n</head>`);

  // __OL_BUILD__ 주입
  const build = {
    version: pkg.version,
    schemaVersion: 9,
    buildAt: new Date().toISOString(),
    dev: true,
  };
  const buildScript = `<script>window.__OL_BUILD__=${JSON.stringify(build)};</script>`;

  // __LOADED_DATA_B64__ — dev fixture (비어있는 초기 상태)
  const dataScript = `<script>const __LOADED_DATA_B64__ = '__INIT_DATA_B64__';</script>`;

  // 자동 새로고침 스크립트 (esbuild SSE)
  const liveReloadScript = `
<script>
  // esbuild live reload
  new EventSource('/esbuild').addEventListener('change', () => {
    console.log('[OL Dev] 변경 감지 → 새로고침');
    location.reload();
  });
</script>`;

  // bundle.js 로드 (esbuild가 /bundle.js로 서빙)
  const bundleScript = `<script src="/bundle.js"></script>`;

  html = html.replace('</head>',
    `${buildScript}\n${dataScript}\n${liveReloadScript}\n</head>`
  );
  html = html.replace('</body>', `${bundleScript}\n</body>`);

  return html;
}

// ── 메인 ──────────────────────────────────────────────
async function main() {
  const pkg = JSON.parse(readFileSync(resolve(ROOT, 'package.json'), 'utf8'));

  mkdirSync(DIST, { recursive: true });

  // dev HTML 미리 생성 (서버 시작 전)
  const devHtml = buildDevHtml(pkg);
  writeFileSync(resolve(DIST, 'index.html'), devHtml);

  // esbuild context — watch + serve
  const ctx = await esbuild.context({
    entryPoints: [resolve(SRC, 'main.js')],
    bundle: true,
    outfile: resolve(DIST, 'bundle.js'),
    format: 'iife',
    sourcemap: true,
    minify: false,
    // build.mjs와 동일한 define/alias 등 옵션 유지
    logLevel: 'info',
  });

  // esbuild 내장 서버 (정적 파일 서빙 + SSE /esbuild 엔드포인트)
  const server = await ctx.serve({
    servedir: DIST,
    port: PORT,
    onRequest: ({ method, path: p, status, timeInMS }) => {
      const color = status >= 400 ? '\x1b[31m' : '\x1b[32m';
      console.log(`${color}[${status}]\x1b[0m ${method} ${p} (${timeInMS}ms)`);
    },
  });

  // watch 모드 활성화 (변경 감지 → 재빌드 → SSE 트리거)
  await ctx.watch();

  console.log('\n\x1b[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m');
  console.log(`\x1b[1m  OL ATLAS Dev Server\x1b[0m`);
  console.log(`  v${pkg.version} · schemaVersion ${build.schemaVersion}`);
  console.log(`\n  \x1b[4mhttp://localhost:${PORT}\x1b[0m`);
  console.log('\n  소스 변경 → 자동 재빌드 + 새로고침');
  console.log('  종료: Ctrl+C');
  console.log('\x1b[36m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\x1b[0m\n');

  // 프로세스 종료 처리
  process.on('SIGINT', async () => {
    console.log('\n[OL Dev] 서버 종료 중...');
    await ctx.dispose();
    process.exit(0);
  });
}

main().catch(err => {
  console.error('[OL Dev] 오류:', err);
  process.exit(1);
});
```

### 1.2 주의사항

**CSS 목록 동기화**: `CSS_FILES` 배열은 실제 `build.mjs`의 CSS 처리 순서와 **정확히 동일**해야 한다. `build.mjs`를 먼저 읽어서 CSS 파일 목록과 순서를 확인한 뒤 `dev.mjs`에 복사할 것.

**esbuild 옵션 동기화**: `build.mjs`의 esbuild 옵션(define, alias, inject 등)이 있다면 `dev.mjs`에도 동일하게 적용해야 한다. `build.mjs`를 먼저 읽어서 확인할 것.

---

## Phase 2 — `package.json` scripts 추가

```json
{
  "scripts": {
    "build": "node build/build.mjs",
    "dev":   "node build/dev.mjs"
  }
}
```

기존 `build` 스크립트가 있다면 유지하고 `dev`만 추가한다.

---

## Phase 3 — `src/index.html` 확인 및 조정

dev 서버는 `src/index.html`을 HTML 템플릿으로 사용한다.

현재 `src/index.html`에 다음이 없어야 한다:

- `<style>` 블록 (dev.mjs가 CSS를 동적으로 주입)
- `<script>` 블록 (dev.mjs가 `__OL_BUILD__`, `__LOADED_DATA_B64__`, bundle.js를 주입)
- `<!--STYLES-->`, `<!--SCRIPTS-->` 같은 플레이스홀더

**현재 `src/index.html` 상태에 따라 처리**:

```
시나리오 A — src/index.html이 순수 HTML 뼈대 (CSS/JS 없음):
  → dev.mjs가 그대로 사용 가능 (추가 작업 없음)

시나리오 B — src/index.html에 플레이스홀더(<!--SCRIPTS--> 등)가 있음:
  → dev.mjs의 replace 패턴을 index.html의 플레이스홀더에 맞게 수정

시나리오 C — src/index.html에 이미 CSS/JS가 하드코딩되어 있음:
  → dev.mjs에서 직접 파일을 읽어서 서빙하는 방식으로 전환
  → 또는 dev 전용 index.dev.html 생성
```

**작업 전 반드시 `cat src/index.html`로 현재 상태를 확인하고 시나리오를 판단할 것.**

---

## Phase 4 — `.gitignore` 업데이트

dev 빌드 산출물은 git에서 제외:

```
# .gitignore에 추가
dist/index.html
dist/bundle.js
dist/bundle.js.map
```

prod 빌드(`dist/ol-atlas_v*.html`)는 git 추적 유지.

---

## Phase 5 — dev fixture 데이터 (선택)

편집자 전환 테스트를 빠르게 하려면 dev 빌드에 테스트 데이터를 자동 주입한다.

### 5.1 `build/fixtures/dev-state.js` 신규 작성

```js
// build/fixtures/dev-state.js
// npm run dev 시 자동 주입되는 테스트 state

export const DEV_STATE = {
  meta: {
    fileId: 'dev-fixture-001',
    title: 'OL ATLAS Dev',
    created: '2026-05-25T00:00:00.000Z',
    version: '0.0.4',
    schemaVersion: 9,
    dirty: false,
    lastSavedAt: null,
    editors: [
      {
        id: 'origin_biwoom',
        name: '비움',
        email: '',
        firstSavedAt: '2026-05-25T00:00:00.000Z',
        lastSavedAt: '2026-05-25T00:00:00.000Z',
        saveCount: 0,
        isOrigin: true,
      },
      {
        id: 'fp_test0001',
        name: '편집자A',
        email: 'a@test.com',
        firstSavedAt: '2026-05-25T10:00:00.000Z',
        lastSavedAt: '2026-05-25T14:00:00.000Z',
        saveCount: 2,
      },
      {
        id: 'fp_test0002',
        name: '편집자B',
        email: 'b@test.com',
        firstSavedAt: '2026-05-25T12:00:00.000Z',
        lastSavedAt: '2026-05-25T12:00:00.000Z',
        saveCount: 1,
      },
    ],
    saveLog: [
      { at: '2026-05-25T00:00:00.000Z', editorId: 'origin_biwoom', note: '원본 생성' },
      { at: '2026-05-25T10:00:00.000Z', editorId: 'fp_test0001' },
      { at: '2026-05-25T14:00:00.000Z', editorId: 'fp_test0001' },
      { at: '2026-05-25T12:00:00.000Z', editorId: 'fp_test0002' },
    ],
    actLog: [],
    currentEditorId: null,
  },
  settings: {
    theme: 'system',
    locale: 'ko',
    sidebarOpen: false,
    boardWidth: '',
  },
  columns: [
    { id: 1, title: '기획', color: '#6366f1', order: 0 },
    { id: 2, title: '작성중', color: '#f59e0b', order: 1 },
    { id: 3, title: '완료', color: '#22c55e', order: 2 },
  ],
  cards: [
    {
      id: 1, colId: 1,
      title: '붓다 출가 에피소드',
      body: '# 붓다 출가\n\n왕궁을 떠나는 장면에 대한 경전 기록 비교.',
      bodyMode: 'markdown',
      tags: ['#인물:붓다', '#주제:출가', '#경전:DN1'],
      priority: 'mid',
      acts: [
        { type: 'create', at: '2026-05-25T10:00:00.000Z', editorId: 'fp_test0001' },
        { type: 'update', at: '2026-05-25T14:00:00.000Z', editorId: 'fp_test0001' },
      ],
    },
    {
      id: 2, colId: 1,
      title: '사성제 개요',
      body: '고·집·멸·도의 기본 구조 정리.',
      bodyMode: 'plain',
      tags: ['#주제:사성제'],
      priority: 'high',
      acts: [
        { type: 'create', at: '2026-05-25T12:00:00.000Z', editorId: 'fp_test0002' },
      ],
    },
    {
      id: 3, colId: 2,
      title: '12연기 도표',
      body: '무명 → 행 → 식 → 명색 → 육처 → 촉 → 수 → 애 → 취 → 유 → 생 → 노사',
      bodyMode: 'plain',
      tags: ['#주제:연기'],
      priority: 'low',
      acts: [
        { type: 'create', at: '2026-05-25T10:00:00.000Z', editorId: 'fp_test0001' },
      ],
    },
  ],
  trash: [],
  userData: { status: {} },
  nextCardId: 4,
  nextColId: 4,
};
```

### 5.2 `build/dev.mjs`에 fixture 주입 추가

```js
// dev.mjs의 buildDevHtml 함수에서 __LOADED_DATA_B64__ 처리 수정

import { DEV_STATE } from './fixtures/dev-state.js';

// fixture를 base64로 인코딩
const fixtureJson = JSON.stringify(DEV_STATE);
const fixtureB64 = Buffer.from(fixtureJson, 'utf8').toString('base64');

// dataScript 수정: __INIT_DATA_B64__ 대신 실제 fixture 데이터 주입
const dataScript = `<script>const __LOADED_DATA_B64__ = '${fixtureB64}';</script>`;
```

이렇게 하면 `npm run dev`로 서버를 시작할 때마다 편집자A/B가 이미 등록된 상태로 열린다.

**주의**: fixture 데이터는 localStorage를 덮어쓴다. dev 중에 직접 입력한 데이터가 서버 재시작 시 초기화된다. 이는 의도된 동작이다.

---

## 전체 수정/생성 파일 요약

|파일|작업|비고|
|---|---|---|
|`build/dev.mjs`|신규 생성|dev 서버 메인|
|`build/fixtures/dev-state.js`|신규 생성|test fixture (선택)|
|`package.json`|`"dev"` script 추가||
|`.gitignore`|dist 임시 파일 추가||
|`src/index.html`|확인 후 필요 시 조정|Phase 3 참고|

신규 파일: 2개 (fixtures는 선택) 수정 파일: 2~3개

---

## 작업 순서

```
1. cat build/build.mjs              ← esbuild 옵션 + CSS 목록 확인
2. cat src/index.html               ← HTML 템플릿 구조 확인 (Phase 3 시나리오 판단)
3. build/dev.mjs 작성               ← Phase 1 (build.mjs 옵션 동기화)
4. package.json 수정                ← Phase 2
5. .gitignore 업데이트              ← Phase 4
6. npm run dev                      ← 실행 테스트
7. 브라우저에서 http://localhost:3000 접속 확인
8. src/main.js 저장 → 자동 새로고침 확인
9. build/fixtures/dev-state.js 작성 ← Phase 5 (선택)
10. dev.mjs에 fixture 주입 추가     ← Phase 5 (선택)
```

---

## 검증 체크리스트

- [ ] `npm run dev` 실행 시 오류 없음
- [ ] `http://localhost:3000` 접속 시 OL ATLAS 정상 표시
- [ ] `src/main.js` 저장 후 3초 내 브라우저 자동 새로고침
- [ ] `src/styles/tokens.css` 저장 후 자동 새로고침
- [ ] 브라우저 DevTools에서 소스맵으로 실제 파일명/줄번호 표시
- [ ] `npm run build`는 여전히 정상 동작 (dev 작업으로 영향 없음)
- [ ] `dist/index.html`, `dist/bundle.js`가 `.gitignore`에 포함됨
- [ ] fixture 주입 시 About → 편집 기록에서 편집자A/B 즉시 표시

---

## 트러블슈팅

### `EventSource is not defined` 오류

esbuild 서버가 `/esbuild` SSE 엔드포인트를 제공하지 않는 경우. esbuild 버전 확인: `node_modules/.bin/esbuild --version` 0.17 이상이어야 `serve()` + `watch()` 조합이 정상 동작.

### 포트 3000 충돌

```js
// dev.mjs에서 PORT를 변경
const PORT = 3001;
```

### CSS가 적용되지 않음

`CSS_FILES` 배열 순서가 `build.mjs`와 다를 가능성. 두 파일의 CSS 목록을 비교할 것.

### fixture 데이터가 무시됨

boot 시 localStorage에 이미 `ol_state`가 있으면 `__LOADED_DATA_B64__`보다 localStorage를 우선한다. `localStorage.removeItem('ol_state')`로 초기화 후 새로고침.

---

_OL ATLAS Dev 서버 구현 작업지시서 — 2026-05-25_