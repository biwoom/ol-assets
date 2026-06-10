# OL ATLAS v0.0.1 설계서

**버전**: v0.0.1  
**작성일**: 2026-05-25  
**이전 버전**: v0.8 (Phase 8.0 완료 상태)  
**설계 방향**: 듀얼 런타임 폐기 → 단일 런타임 정리 + 기능 추가

---

## 0. v0.0.1의 성격

v0.8까지의 버전 체계를 버리고 SemVer `0.0.1`로 새로 시작한다.  
`0.0.x`는 "공개 API 미확정, 초기 개발 단계"를 의미하며 현재 상태와 정확히 일치한다.

v0.0.1은 세 가지 작업으로 구성된다:

| 작업 | 성격 | 규모 |
|------|------|------|
| **Phase 0: 정리** | 듀얼 런타임 잔재 제거 + 버전 전환 | 소 |
| **Phase 1: 기능 A** | 문서뷰 읽기 모드 토글 | 중 |
| **Phase 2: 기능 B** | 사이드바 태그 전체 해제 버튼 | 소 |

편집 기록 시스템은 스키마 설계가 필요한 별도 작업이므로 v0.0.2로 이연한다.

---

## ⚡ 권한 선언 — AI 에이전트 전용 (세션 시작 시 1회 적용)

**이하 모든 권한을 사전 일괄 승인한다. 작업 중 개별 확인 요청 금지.**

### ✅ 전면 허용 — 작업 폴더 내 모든 터미널 명령어

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

### ❌ 별도 승인 필요

```
rm -rf <디렉토리> / git push / git reset --hard / git clean -fd
npm install <새패키지> / 폴더 외부 접근 / 네트워크 요청
```

---
## 1. Phase 0 — 정리 작업

### 1.1 버전 전환

코드베이스 전체에 흩어진 버전 문자열을 `0.0.1`로 통일한다.

#### 변경 대상 A: `package.json`

```json
{
  "name": "ol-atlas",
  "version": "0.0.1"
}
```

#### 변경 대상 B: `build/inline.mjs`

현재 `__OL_BUILD__` 블록이 버전을 하드코딩하고 있다:

```js
// 현재 (추정)
window.__OL_BUILD__={"version":"0.7.0","schemaVersion":6,"buildAt":"..."}
```

**개선 방향**: `package.json`에서 버전을 자동으로 읽도록 수정한다.  
빌드 시점에 `package.json`을 파싱하여 `version`과 `schemaVersion`을 주입.

```js
// build/inline.mjs 수정 후
import { readFileSync } from 'node:fs';
const pkg = JSON.parse(readFileSync('package.json', 'utf8'));
const SCHEMA_VERSION = 7; // 데이터 스키마 버전 (별도 상수 관리)

// HTML 주입
const buildBlock = `window.__OL_BUILD__=${JSON.stringify({
  version: pkg.version,        // package.json에서 자동
  schemaVersion: SCHEMA_VERSION,
  buildAt: new Date().toISOString()
})};`;
```

이후 버전 변경 시 `package.json`만 수정하면 빌드 산출물에 자동 반영된다.

**현재 불일치 수정**: `__OL_BUILD__.schemaVersion`이 `6`으로 되어있으나 실제 운영 스키마는 `7`이다. 이번에 `7`로 맞춘다.

#### 변경 대상 C: `src/data/init.js` — `makeDefault()` 함수

```js
// 수정 전
meta: {
  ...
  version: "1.0.0",
  schemaVersion: 7,
  ...
}

// 수정 후
meta: {
  ...
  version: "0.0.1",
  schemaVersion: 7,
  ...
}
```

`makeDefault()`는 새 파일을 처음 만들 때의 초기값이다.  
기존 저장 파일을 불러올 때는 저장된 버전이 그대로 유지되므로 마이그레이션 불필요.

---

### 1.2 듀얼 런타임 잔재 제거

Phase 8.0 완료 후 남은 흔적들을 제거한다.

#### 제거 대상 A: `AUTHOR_BUNDLE` 마커 — `build/inline.mjs`

현재 `inline.mjs`가 JS 번들 전체를 마커로 감싸고 있다:

```js
// 현재 (제거 대상)
.replace('<!--SCRIPTS-->', `<script>
/*! AUTHOR_BUNDLE_START */
${bundleJs}
/*! AUTHOR_BUNDLE_END */
</script>`)
```

```js
// 수정 후
.replace('<!--SCRIPTS-->', `<script>\n${bundleJs}\n</script>`)
```

v0.0.1에서는 단일 런타임이므로 마커가 불필요하다.  
빌드 산출물에서 `/*! AUTHOR_BUNDLE_START/END */` 주석이 사라지는 것 외에 기능 변화 없음.

**검증**:
```bash
grep 'AUTHOR_BUNDLE' dist/ol-atlas.html
# → 결과 없어야 함
```

#### 제거 대상 B: `src/components/reader/` 빈 디렉토리

```bash
rmdir src/components/reader
```

Phase 8.x를 위해 만들어진 빈 디렉토리. 내용이 없으므로 삭제.

---

### 1.3 Phase 0 검증

```bash
# 빌드
node build/build.mjs

# 버전 확인
grep '__OL_BUILD__' dist/ol-atlas.html
# → {"version":"0.0.1","schemaVersion":7,"buildAt":"..."}

# 마커 제거 확인
grep 'AUTHOR_BUNDLE' dist/ol-atlas.html
# → 결과 없음

# 기능 회귀 없음 확인 (브라우저에서)
# - 카드 생성/편집/삭제
# - HTML 저장 후 불러오기
# - 다크모드 전환
```

---

## 2. Phase 1 — 문서뷰 읽기 모드 토글

### 2.1 기능 정의

문서뷰(`docview`) 한정 읽기 모드 전환 기능.  
토글 시 문서뷰 레이아웃과 스타일만 변경하며, 다른 뷰(칸반, 카드, 리스트)에 영향 없음.

**읽기 모드 진입 조건**: 문서뷰가 활성화된 상태에서 토글 버튼 클릭

**읽기 모드 동작**:

| 대상 | 기본 모드 | 읽기 모드 |
|------|----------|----------|
| 헤더 | 표시 | 숨김 → 커서 상단 이동 시 표시 |
| 사이드바 | 표시 | 숨김 → 커서 좌측 이동 시 표시 |
| 문서뷰 편집 버튼 | 표시 | 숨김 |
| 본문 레이아웃 | 현재 유지 | 중앙 정렬, 여백 확대 |
| 폰트/줄간격 | 현재 유지 | 현재 유지 (변경 안 함) |
| sepia 배경 | 미적용 | 미적용 (차후 검토) |

**모바일 대응**:  
hover가 없는 모바일에서는 화면 상단/좌측 엣지 탭으로 헤더/사이드바를 표시한다.  
v0.0.1 범위에 포함.

**상태 저장**: 읽기 모드 on/off 상태를 `localStorage`에 저장. 다음 열기 시 유지.

---

### 2.2 UI 설계

#### 토글 버튼 위치

문서뷰 우상단에 아이콘 버튼 배치. 칸반/카드/리스트 뷰에서는 표시 안 됨.

```
읽기 모드 OFF: 📖 아이콘 (또는 집중 모드 아이콘)
읽기 모드 ON:  ✕ 또는 편집 아이콘
```

인라인 SVG 아이콘 사용 (외부 의존성 없음).

#### 헤더/사이드바 자동 표시 트리거

```
헤더: mousemove y < 60px → 헤더 표시 (fadeIn)
      마우스가 헤더 영역 벗어나면 → 헤더 숨김 (fadeOut, 1.5초 딜레이)

사이드바: mousemove x < 40px → 사이드바 표시
          마우스가 사이드바 영역 벗어나면 → 사이드바 숨김 (1.5초 딜레이)

모바일: touchstart y < 60px → 헤더 표시 (2초 후 자동 숨김)
        touchstart x < 40px → 사이드바 표시 (2초 후 자동 숨김)
```

---

### 2.3 구현 설계

#### 상태 관리

읽기 모드는 전역 앱 상태(`S`)에 넣지 않는다.  
문서뷰 한정 UI 상태이므로 `localStorage` + 모듈 변수로 관리.

```js
// src/components/shared/docview.js 내부
const LS_KEY = 'ol_docview_readmode';
let _readMode = localStorage.getItem(LS_KEY) === '1';

function setReadMode(on) {
  _readMode = on;
  localStorage.setItem(LS_KEY, on ? '1' : '0');
  document.body.classList.toggle('dv-read-mode', on);
  _updateReadModeHoverListeners(on);
}
```

#### CSS — `src/styles/docview.css` 하단에 추가

```css
/* ── 읽기 모드 ────────────────────────────────── */
body.dv-read-mode #header {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease;
}
body.dv-read-mode #header.peek {
  opacity: 1;
  pointer-events: auto;
}

body.dv-read-mode #sidebar {
  transform: translateX(-100%);
  transition: transform 0.2s ease;
}
body.dv-read-mode #sidebar.peek {
  transform: translateX(0);
}

/* 편집 버튼 숨김 */
body.dv-read-mode #dv-edit-btn,
body.dv-read-mode #dv-new-card-btn,
body.dv-read-mode .dv-edit-actions,
body.dv-read-mode .dv-card-actions-row { display: none !important; }

/* 본문 레이아웃 — 읽기 최적화 */
body.dv-read-mode #docview-main {
  max-width: 720px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}
```

#### hover 리스너 — `src/components/shared/docview.js`

```js
let _hoverTimers = {};

function _updateReadModeHoverListeners(on) {
  if (on) {
    document.addEventListener('mousemove', _handleReadModeMouseMove);
    document.addEventListener('touchstart', _handleReadModeTouchStart, { passive: true });
  } else {
    document.removeEventListener('mousemove', _handleReadModeMouseMove);
    document.removeEventListener('touchstart', _handleReadModeTouchStart);
    // peek 클래스 모두 제거
    document.getElementById('header')?.classList.remove('peek');
    document.getElementById('sidebar')?.classList.remove('peek');
  }
}

function _handleReadModeMouseMove(e) {
  const header = document.getElementById('header');
  const sidebar = document.getElementById('sidebar');

  if (e.clientY < 60) {
    header?.classList.add('peek');
    clearTimeout(_hoverTimers.header);
  } else {
    clearTimeout(_hoverTimers.header);
    _hoverTimers.header = setTimeout(() => {
      if (!header?.matches(':hover'))
        header?.classList.remove('peek');
    }, 1500);
  }

  if (e.clientX < 40) {
    sidebar?.classList.add('peek');
    clearTimeout(_hoverTimers.sidebar);
  } else {
    clearTimeout(_hoverTimers.sidebar);
    _hoverTimers.sidebar = setTimeout(() => {
      if (!sidebar?.matches(':hover'))
        sidebar?.classList.remove('peek');
    }, 1500);
  }
}

function _handleReadModeTouchStart(e) {
  const touch = e.touches[0];
  if (touch.clientY < 60) {
    const header = document.getElementById('header');
    header?.classList.add('peek');
    setTimeout(() => header?.classList.remove('peek'), 2000);
  }
  if (touch.clientX < 40) {
    const sidebar = document.getElementById('sidebar');
    sidebar?.classList.add('peek');
    setTimeout(() => sidebar?.classList.remove('peek'), 2000);
  }
}
```

---

### 2.4 수정 파일 목록

| 파일 | 작업 |
|------|------|
| `src/components/shared/docview.js` | 읽기 모드 토글 버튼 + 상태 관리 + hover 리스너 |
| `src/styles/docview.css` | 읽기 모드 CSS 추가 |

새 파일 생성 없음. CSS 파일 추가 없음.

---

### 2.5 Phase 1 검증

- [x] 문서뷰 우상단에 읽기 모드 토글 버튼 표시
- [x] 토글 클릭 시 헤더/사이드바 숨김
- [x] 마우스 상단 이동 시 헤더 표시
- [x] 마우스 좌측 이동 시 사이드바 표시
- [x] 편집 버튼 숨김 확인
- [ ] 본문 중앙 정렬 확인 ??
- [x] localStorage에 상태 저장 → 새로고침 후 유지
- [x] 다른 뷰(칸반 등)에서는 토글 버튼 없음
- [x] 모바일: 상단 엣지 탭으로 헤더 표시
- [x] 콘솔 에러 없음

---

## 3. Phase 2 — 사이드바 태그 전체 해제 버튼

### 3.1 기능 정의

사이드바 태그 필터 영역에서 prefix 태그를 다중 선택한 상태에서  
"모든 태그 선택 해제" 버튼 한 번으로 전체 해제.

**표시 조건**: 태그가 1개 이상 선택된 경우에만 버튼 표시  
**위치**: 태그 필터 영역 상단 또는 하단 (기존 `tfd-clear-btn` 패턴 참조)

---

### 3.2 현재 코드 분석

헤더의 태그 필터 드롭다운에는 이미 `tfd-clear-btn`이 존재하며  
클릭 시 `H.clear()` → `De()` → `vn()` → `w('cards')` 흐름으로 동작한다.

사이드바의 태그 영역에는 동일한 clear 버튼이 없다.  
`src/components/shared/sidebar.js`의 태그 렌더 함수에 버튼 추가.

---

### 3.3 구현 설계

#### `src/components/shared/sidebar.js` 수정

태그 섹션 렌더 함수 내에서 선택된 태그가 있을 때만 버튼을 렌더:

```js
// 태그 섹션 렌더 부분에 추가
if (activeTagCount > 0) {
  const clearBtn = ce('button', 'sb-tag-clear-btn');
  clearBtn.textContent = '선택 해제';
  clearBtn.onclick = () => {
    // 기존 H(태그 필터 Set) clear 로직과 동일하게
    clearAllTagFilters();   // 기존 함수 재사용 또는 dispatch
    queueRender('sidebar');
    queueRender('cards');
  };
  tagSection.appendChild(clearBtn);
}
```

#### 스타일 — `src/styles/sidebar.css` 하단에 추가

```css
.sb-tag-clear-btn {
  display: inline-flex;
  align-items: center;
  font-size: 0.72rem;
  color: hsl(var(--muted-foreground));
  background: none;
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius-sm, 4px);
  padding: 0.15rem 0.5rem;
  cursor: pointer;
  margin-top: 0.25rem;
  transition: color 0.15s, border-color 0.15s;
}
.sb-tag-clear-btn:hover {
  color: hsl(var(--foreground));
  border-color: hsl(var(--foreground));
}
```

---

### 3.4 수정 파일 목록

| 파일 | 작업 |
|------|------|
| `src/components/shared/sidebar.js` | 태그 clear 버튼 추가 |
| `src/styles/sidebar.css` | 버튼 스타일 추가 |

---

### 3.5 Phase 2 검증

- [x] 태그 미선택 상태: 버튼 없음
- [x] 태그 1개 이상 선택: "선택 해제" 버튼 표시
- [x] 버튼 클릭: 모든 태그 선택 해제
- [x] 카드 목록 즉시 업데이트
- [x] 콘솔 에러 없음

---

## 4. 전체 수정 파일 요약

| 파일 | Phase | 작업 내용 |
|------|-------|----------|
| `package.json` | 0 | version → `0.0.1` |
| `build/inline.mjs` | 0 | AUTHOR_BUNDLE 마커 제거, `__OL_BUILD__` version을 package.json에서 자동 주입, schemaVersion `6`→`7` 수정 |
| `src/data/init.js` | 0 | `makeDefault().meta.version` → `"0.0.1"` |
| `src/components/shared/docview.js` | 1 | 읽기 모드 토글 버튼 + 상태 관리 + hover/touch 리스너 |
| `src/styles/docview.css` | 1 | 읽기 모드 CSS 추가 |
| `src/components/shared/sidebar.js` | 2 | 태그 전체 해제 버튼 추가 |
| `src/styles/sidebar.css` | 2 | 버튼 스타일 추가 |
| `src/components/reader/` (디렉토리) | 0 | 삭제 |

총 **7개 파일 수정 + 1개 디렉토리 삭제**.  
새로 생성하는 파일 없음.

---

## 5. 작업 순서 권장

```
Phase 0 (정리) → 빌드 검증 → git commit
Phase 2 (태그 해제 버튼) → 검증 → git commit   ← 작고 독립적
Phase 1 (읽기 모드) → 검증 → git commit         ← 크고 복잡
git tag v0.0.1
```

Phase 2를 Phase 1보다 먼저 하는 이유: 작고 독립적이라 빠르게 완료 가능하고,  
Phase 1에서 문제가 생겨도 Phase 2 성과는 보존된다.

---

## 6. 이후 로드맵 (참고)

| 버전 | 주요 내용 |
|------|----------|
| v0.0.2 | 편집 기록 시스템 (스키마 v8, 편집자 탭 UI) |
| v0.1.0 | 실제 불교 컨텐츠 탑재 (붓다스토리 초안) |
| v1.0.0 | 첫 공개 배포 버전 |

---

*OL ATLAS v0.0.1 설계서 — 2026-05-25*