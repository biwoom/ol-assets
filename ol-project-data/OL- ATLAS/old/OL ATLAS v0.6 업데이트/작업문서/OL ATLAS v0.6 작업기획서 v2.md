# OL ATLAS v0.6 작업기획서 v2

작성: 2026-05-17 대상: v0.5.1 → v0.6.0 상태: 비움 확정 (점검 1~3 + 사이드바 UI + 모듈 분리 분석 반영)

---

## 0. 이 문서의 위치

이 기획서는 다음 검증 과정을 거쳤다.

1. 타전문가 분석 보고서 검토
2. Claude 1차 검증 보고서
3. 비움-Claude 의견 교환 (마이그레이션, wikilink, links.type, 6축 태그, 콘텐츠 다양성)
4. v1 작업기획서 작성
5. v1 재점검 (3가지 핵심 질문)
6. 사이드바 UI 결정 + 모듈 분리 분석
7. v2 확정 (본 문서)

작업 중 의문이 생기면 이 문서의 결정 사항이 기준이다. 이 문서에 명시되지 않은 변경은 별도 합의 없이 도입하지 않는다.

---

## 1. 확정된 원칙

### 유지

- 단일 HTML 파일 배포 (fork 가능성의 핵심)
- 외부 런타임 의존성 0
- localStorage 기반 데이터 저장
- ORIGIN 하드코딩 (author/copyright/license)
- shadcn/ui 디자인 시스템 (Phase 1~6 완료 상태 유지)

### 도입

- dev/dist 분리 (소스는 모듈로, 산출물은 단일 HTML)
- prefix 태그 파싱 (`인물:사리뿟다`, `학파:중관` 등 자유 어휘)
- 사이드바 드롭다운 UI (분류 축마다 select 박스 하나)
- prefix 기반 검색
- 데이터 안정성 장치: `schemaVersion` 필드 + 미래 필드 보존 정책
- 빌드 메타데이터 (`__OL_BUILD__` 객체)

### 도입하지 않음 (v0.6 비범위)

- 마이그레이션 로직 (필드만 박아두고 로직은 v0.7에서)
- 고정 6축 meta 필드 (`meta.person` 등)
- links 필드 + wikilink
- 다중 선택 필터 (v0.6은 단일 선택만)
- IndexedDB / PWA / Electron
- 런타임 외부 라이브러리

---

## 2. v0.6 핵심 가치 한 문장

> "태그 입력창에서 자유 어휘 prefix 태그(`인물:사리뿟다`)를 쓰면, 코드가 자동 파싱해서 사이드바에 분류 축별 드롭다운 필터를 자동 생성한다. 모든 변경은 dev/dist 분리된 빌드 시스템 안에서 이루어진다."

---

## 3. prefix 태그 방식

### 3.1 입력 방식

태그 입력창은 현재와 동일. 콜론(:) 포함 시 자동 파싱.

```
인물:사리뿟다  → prefix="인물", value="사리뿟다"
학파:중관      → prefix="학파", value="중관"
안내           → prefix=null, value="안내" (자유 태그)
```

### 3.2 어휘 자유도

코드가 강제하는 prefix 목록 없음. 콘텐츠 시리즈마다 자기 어휘:

```
붓다스토리:  인물:붓다  장소:기원정사  시기:성도후1년  주제:연기  유형:설법  경전:DN1
법구경:      품:쌍서품  게송:1  주제:마음  유형:게송
중관학:      학파:중관  논사:용수  논서:중론  주제:공  유형:논증
선림:        법맥:임제종  공안:무문관28칙  인물:마조
```

### 3.3 콜론 충돌 정책

태그 안의 콜론은 prefix 의도로 약속한다. 자유 태그에는 콜론을 쓰지 않는다. `인물::붓다` 같은 이중 콜론 입력은 `prefix="인물", value=":붓다"`로 파싱되며, 사용자의 의도된 입력으로 간주하여 그대로 둔다. 코드는 단순하게 유지한다.

---

## 4. 데이터 모델

### 4.1 카드 스키마 — v0.5.1 그대로

```js
{
  id:       number,
  colId:    number,
  title:    string,
  body:     string,
  slug:     string,
  group:    string,
  tags:     string[],   // prefix + 자유 태그 혼용
  priority: 'high' | 'mid' | 'low',
  images:   { [tokenId]: dataURI },
  created:  'YYYY-MM-DD'
}
```

### 4.2 상태 메타 — schemaVersion 도입

```js
state.meta = {
  ...기존,
  schemaVersion: 6   // ← v0.6 신규
}
```

마이그레이션 로직은 작성하지 않는다. 필드만 박아둔다. v0.7에서 첫 마이그레이션이 도입될 때 이 필드가 분기 기준이 된다.

### 4.3 미래 필드 보존 정책 (중요)

`normalizeCard`는 알려진 필드를 정규화하되, **모르는 필드를 삭제하지 않는다**.

이유: fork 모델에서 v0.7로 만든 데이터(`meta`, `links` 필드 포함)를 누군가 v0.6 파일로 열어도 데이터가 손실되어선 안 된다.

현재 코드의 `delete card.bodyMd`, `delete card.history` 같은 패턴은 _명시적 레거시 마이그레이션_이므로 유지한다. 그러나 **그 외 알려지지 않은 필드를 적극 삭제하는 코드를 추가하지 않는다**는 원칙을 코드 주석으로 명문화한다.

```js
function normalizeCard(card) {
  // ── 레거시 마이그레이션 (알려진 구필드만 삭제) ──
  if (card.bodyMd) { ... }
  delete card.bodyMode;
  if ('history' in card) delete card.history;

  // ── 정책: 모르는 필드는 보존한다 (fork 호환성) ──
  // v0.6이 모르는 필드(meta, links 등)가 들어와도 삭제하지 않는다.
  // 알려진 필드만 정규화하고 나머지는 그대로 통과시킨다.

  // ... 알려진 필드 정규화 ...
}
```

---

## 5. 작업 Phase 구성

```
Phase A: 빌드 골격 + legacy.js 통째 이동       (기능 변경 0)
Phase B: 핵심 모듈 추출 (3개)
  B1: src/core/tag-parser.js  (신규)
  B2: src/ui/sidebar.js       (legacy → 추출, prefix 드롭다운 구현)
  B3: src/core/search.js      (legacy → 추출, prefix 검색 통합)
Phase C: schemaVersion + 빌드 메타데이터 + 검증 강화
Phase D: 회귀 테스트 및 릴리스
```

각 Phase 완료 시 `dist/snapshots/`에 산출물 보존.

---

## 6. 모듈 분리 방침

### 6.1 분리 결정 룰

다음 4가지 룰로 모듈 추출 여부 결정:

1. **v0.6에서 직접 수정되는가?** → YES면 분리
2. **신규 추가되는가?** → YES면 신규 파일
3. **향후 자주 변경될 영역인가?** → YES면 분리 권장
4. **위 3개 모두 NO?** → legacy.js에 그대로

### 6.2 v0.6 디렉토리 구조

```
ol-atlas/
├── src/
│   ├── index.html              ← HTML 골격 (슬롯 마커)
│   ├── styles/
│   │   ├── tokens.css          ← HSL 변수, radius, 다크모드 토큰
│   │   └── main.css            ← 나머지 CSS 전체
│   ├── core/
│   │   ├── tag-parser.js       ← [신규] parseTag, buildPrefixIndex
│   │   ├── search.js           ← [추출] runSearch, cardMatchesQuery
│   │   └── legacy.js           ← 위에 추출 안 된 JS 전체
│   ├── ui/
│   │   └── sidebar.js          ← [추출] renderSidebar 관련 전체
│   └── assets/
│       └── favicon.b64         ← base64 favicon
├── build.js                    ← Node 빌드 스크립트
├── package.json                ← scripts만
├── test/
│   ├── syntax-check.sh
│   └── build-check.sh
└── dist/
    ├── OL_ATLAS_v0.6.html      ← 빌드 산출물
    └── snapshots/              ← Phase별 스냅샷
```

**v0.6에서 분리하지 않는 것 (legacy.js 잔존)**:

- 칸반, 그리드, 리스트, 문서, 트래시, About 뷰 렌더 함수들
- 마크다운 파서 (안정적이지만 큼. v0.7에서 분리 검토)
- 모달, 토스트, 헤더 등 기타 UI 컴포넌트
- 드래그앤드롭, 인라인 편집 등 인터랙션 로직

이유: v0.6에서 직접 수정되지 않는다. 옮기는 비용 대비 효용 없음.

### 6.3 CSS 분리 방침

CSS는 JS보다 분리 효과가 낮다 (cascade 추적 어려움). v0.6에서는 최소 분리:

- `tokens.css`: HSL 변수, radius, 다크모드 토큰만. 디자인 시스템 변경 시 여기만 수정.
- `main.css`: 나머지 전부.

이 정도가 v0.6 sweet spot. 컴포넌트별 분리는 v0.7 이후 검증된 필요가 생기면 도입.

---

## 7. Phase A — 빌드 골격 구축

### A.1 목표

v0.5.1을 기능 변경 없이 dev/dist 구조로 옮긴다. 빌드 산출물이 v0.5.1과 기능적으로 동일해야 한다.

### A.2 src/index.html 구조

```html
<html lang="ko"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/jpeg" href="<!-- BUILD:FAVICON -->">
<title>OL · ATLAS</title>
<script>/* 다크모드 FOUC 방지 — 원본 그대로 */</script>
<!-- BUILD:CSS -->
<!-- BUILD:INFO -->
</head>
<body>
<!-- v0.5.1 body 마크업 전체 -->
<!-- BUILD:JS -->
</body></html>
```

슬롯 4개: `BUILD:FAVICON`, `BUILD:CSS`, `BUILD:INFO`, `BUILD:JS`.

### A.3 build.js

```js
// build.js — Node 기본 fs만 사용. 외부 의존성 0
const fs   = require('fs');
const path = require('path');
const pkg  = require('./package.json');

const SRC  = path.join(__dirname, 'src');
const DIST = path.join(__dirname, 'dist');

// 1. 소스 읽기
let html = fs.readFileSync(path.join(SRC, 'index.html'), 'utf8');
const favicon = fs.readFileSync(path.join(SRC, 'assets/favicon.b64'), 'utf8').trim();

// 2. CSS 모듈 순서
const CSS_MODULES = [
  'styles/tokens.css',   // 변수 먼저
  'styles/main.css'
];
const css = CSS_MODULES
  .map(p => fs.readFileSync(path.join(SRC, p), 'utf8'))
  .join('\n\n');

// 3. JS 모듈 순서 (의존성: 위→아래)
const JS_MODULES = [
  'core/tag-parser.js',   // 의존성 없음
  'core/search.js',       // tag-parser 의존
  'ui/sidebar.js',        // tag-parser, search 의존
  'core/legacy.js'        // 위 모두에 의존
];
const js = JS_MODULES
  .map(p => fs.readFileSync(path.join(SRC, p), 'utf8'))
  .join('\n\n');

// 4. 빌드 메타데이터
const buildInfo = {
  version: pkg.version,
  schemaVersion: 6,
  buildAt: new Date().toISOString()
};
const infoScript = `<script>window.__OL_BUILD__=${JSON.stringify(buildInfo)};</script>`;

// 5. 슬롯 치환
html = html
  .replace('<!-- BUILD:FAVICON -->', `data:image/jpeg;base64,${favicon}`)
  .replace('<!-- BUILD:CSS -->',     `<style>\n${css}\n</style>`)
  .replace('<!-- BUILD:INFO -->',    infoScript)
  .replace('<!-- BUILD:JS -->',      `<script>\n${js}\n</script>`);

// 6. 슬롯 미치환 검증
const remaining = html.match(/<!-- BUILD:[A-Z_]+ -->/g);
if (remaining) {
  console.error('✗ 미치환 슬롯:', remaining);
  process.exit(1);
}

// 7. 태그 개수 검증 (다크모드 script 1개 + 본체 script 2개 = 총 3개)
const scriptCount = (html.match(/<script[\s>]/g) || []).length;
if (scriptCount !== 3) {
  console.warn(`⚠ <script> 태그 ${scriptCount}개 (예상: 3)`);
}

// 8. 저장
if (!fs.existsSync(DIST)) fs.mkdirSync(DIST, { recursive: true });
const outPath = path.join(DIST, 'OL_ATLAS_v0.6.html');
fs.writeFileSync(outPath, html);

const kb = (fs.statSync(outPath).size / 1024).toFixed(1);
console.log(`✓ built → ${outPath}  (${kb} KB)`);
console.log(`  build: ${buildInfo.version} @ ${buildInfo.buildAt}`);
```

**Phase A 시점에서는 JS_MODULES와 CSS_MODULES가 각각 다음과 같이 시작**:

```js
// Phase A 시작 시
const CSS_MODULES = ['styles/main.css'];
const JS_MODULES  = ['core/legacy.js'];
```

`tokens.css`, `tag-parser.js`, `search.js`, `sidebar.js`는 Phase B에서 추가된다.

### A.4 package.json

```json
{
  "name": "ol-atlas",
  "version": "0.6.0",
  "scripts": {
    "build": "node build.js",
    "check": "bash test/syntax-check.sh",
    "test":  "bash test/syntax-check.sh && bash test/build-check.sh",
    "dev":   "node build.js && echo '→ open dist/OL_ATLAS_v0.6.html'"
  }
}
```

### A.5 작업 지시

1. `/home/claude/ol-v6/ol-atlas/` 디렉토리 생성
2. v0.5.1 HTML 파싱 및 분할:
    - favicon base64 → `src/assets/favicon.b64`
    - `<style>` 내용 전체 → `src/styles/main.css`
    - `<script>` 본체 전체 → `src/core/legacy.js`
    - HTML 골격 (4개 슬롯 마커 삽입) → `src/index.html`
3. `build.js`, `package.json` 작성
4. `node --check src/core/legacy.js` — 오류 없어야 함
5. `node build.js` — dist 생성

**주의사항**:

- CSS 분리 시 `/* */` 주석 깨짐 방지
- favicon base64는 줄바꿈 없는 단일 문자열
- legacy.js 첫 줄의 `'use strict'` 또는 IIFE 그대로 유지

### A.6 검증 체크리스트

- [ ] `node --check src/core/legacy.js` 통과
- [ ] `node build.js` 오류 없이 실행, 슬롯 미치환 0개
- [ ] dist 파일 크기 692 KB ±5%
- [ ] 브라우저에서 모든 기능 정상:
    - 칸반/그리드/리스트/문서 뷰
    - 검색 (Cmd+K)
    - About / 휴지통
    - 다크모드 토글
    - 카드 추가/편집/삭제/드래그
- [ ] `window.__OL_BUILD__` 콘솔에서 확인 가능
- [ ] `dist/snapshots/OL_ATLAS_v0.6-phaseA.html` 보존

### A.7 완료 조건

dist가 v0.5.1과 기능 동일. 소스가 빌드 가능한 구조로 분리됨. 빌드 메타데이터 주입 작동.

---

## 8. Phase B — 핵심 모듈 추출 (3개)

### B.0 추출 순서와 원칙

Phase B는 3개 하위 단계로 진행한다. 각 하위 단계마다 빌드+검증.

```
B1: tag-parser.js 신규 생성        (의존성 없는 신규)
B2: sidebar.js 추출 + 드롭다운 UI  (renderSidebar 이동)
B3: search.js 추출 + prefix 검색   (runSearch 이동, prefix 통합)
```

**추출의 의미**: legacy.js에서 _코드를 잘라내어_ 새 파일로 _이동_하는 것. 복사가 아니다. 코드가 두 곳에 있으면 안 된다.

추출 후 함수는 여전히 글로벌 스코프에 있다 (IIFE로 감싸지 않는다). build.js가 모든 파일을 단순 concat하므로 함수가 같은 스코프에 살아있다.

### B.1 tag-parser.js 신규 생성

`src/core/tag-parser.js` 생성:

```js
// src/core/tag-parser.js
// ── prefix 태그 파싱 유틸 ──────────────────────────────

/**
 * 태그 문자열 하나를 파싱.
 * "인물:사리뿟다" → { prefix: "인물", value: "사리뿟다", raw: "인물:사리뿟다" }
 * "안내"          → { prefix: null,   value: "안내",     raw: "안내" }
 */
function parseTag(tag) {
  if (typeof tag !== 'string') {
    return { prefix: null, value: String(tag), raw: tag };
  }
  const colonIdx = tag.indexOf(':');
  if (colonIdx > 0) {
    const prefix = tag.slice(0, colonIdx).trim();
    const value  = tag.slice(colonIdx + 1).trim();
    if (prefix && value) {
      return { prefix, value, raw: tag };
    }
  }
  return { prefix: null, value: tag.trim(), raw: tag };
}

/**
 * 카드 배열에서 prefix 인덱스 빌드.
 * 반환: { "인물": ["붓다", "사리뿟다"], "학파": ["중관", "유식"] }
 * 키와 값 모두 가나다/알파벳 순 정렬.
 */
function buildPrefixIndex(cards) {
  const index = {};
  (cards || []).forEach(card => {
    (card.tags || []).forEach(tag => {
      const { prefix, value } = parseTag(tag);
      if (prefix && value) {
        if (!index[prefix]) index[prefix] = new Set();
        index[prefix].add(value);
      }
    });
  });
  const result = {};
  Object.keys(index).sort().forEach(k => {
    result[k] = [...index[k]].sort();
  });
  return result;
}

/**
 * 카드 배열에서 prefix 없는 자유 태그 목록 추출.
 * 반환: ["안내", "시작", "중요"]  (정렬됨)
 */
function getFreeTags(cards) {
  const free = new Set();
  (cards || []).forEach(card => {
    (card.tags || []).forEach(tag => {
      const { prefix, value } = parseTag(tag);
      if (!prefix && value) free.add(value);
    });
  });
  return [...free].sort();
}

/**
 * 특정 prefix:value 태그를 가진 카드 수 카운트.
 */
function countCardsWithPrefixValue(cards, prefix, value) {
  let count = 0;
  (cards || []).forEach(card => {
    if ((card.tags || []).some(tag => {
      const p = parseTag(tag);
      return p.prefix === prefix && p.value === value;
    })) count++;
  });
  return count;
}

/**
 * 특정 자유 태그를 가진 카드 수 카운트.
 */
function countCardsWithFreeTag(cards, tagValue) {
  let count = 0;
  (cards || []).forEach(card => {
    if ((card.tags || []).some(tag => {
      const p = parseTag(tag);
      return !p.prefix && p.value === tagValue;
    })) count++;
  });
  return count;
}
```

build.js의 `JS_MODULES`를 업데이트:

```js
const JS_MODULES = [
  'core/tag-parser.js',   // ← 추가
  'core/legacy.js'
];
```

#### B.1 검증

- [ ] `node --check src/core/tag-parser.js` 통과
- [ ] 빌드 후 콘솔에서 `parseTag('인물:붓다')` 동작 확인
- [ ] 기존 기능 영향 없음 (legacy.js의 모든 기능)

### B.2 sidebar.js 추출 + 드롭다운 UI 구현

#### B.2.1 추출 대상

legacy.js에서 다음을 **잘라내어** `src/ui/sidebar.js`로 이동:

- `renderSidebar` 함수 (약 7018~7183 라인)
- `refreshSbTagList` 함수
- `refreshSbTagClearBtn` 함수
- `renderSidebarForDocView` 함수
- `buildDocTreeCard` 함수
- 관련 글로벌 변수: `selectedTags`, `selectedColId`

#### B.2.2 사이드바 필터 상태 통합

기존 분산된 필터 상태를 단일 객체로 통합:

```js
// sidebar.js 상단
// ── 사이드바 필터 상태 (v0.6 통합) ──
const sbFilter = {
  group:     '',      // 그룹 필터 (기존 fg)
  status:    '',      // 학습 상태 필터 (기존 fs)
  colId:     null,    // 칸반 컬럼 필터 (기존 selectedColId)
  freeTag:   '',      // 자유 태그 단일 선택 (v0.6)
  prefix:    null,    // { prefix: "인물", value: "붓다" } | null (v0.6 신규)
};

// 레거시 호환: 기존 코드가 selectedColId, selectedTags 참조하던 곳은
// sbFilter.colId, sbFilter.freeTag로 점진 교체.
// Phase B.2 시점에는 호환 변수를 유지하면서 sbFilter도 함께 갱신.
let selectedColId = null;       // 레거시 호환 (deprecated)
let selectedTags  = new Set();  // 레거시 호환 (deprecated)
```

**중요**: 기존 코드의 `selectedColId`, `selectedTags` 참조처가 많으므로 B.2 시점에는 _변수를 제거하지 않는다_. sbFilter와 병행한다. 선택 변경 시 양쪽 모두 갱신:

```js
function setColFilter(colId) {
  sbFilter.colId = colId;
  selectedColId  = colId;     // 레거시 호환
}
```

뷰 렌더 함수들은 v0.6에서 수정하지 않는다. 기존 변수 참조 그대로 둔다.

#### B.2.3 사이드바 UI 구조 (드롭다운 방식)

비움이 결정한 UI:

```
[그룹]        [전체 ▼]    ← 기존 group select 유지
[학습상태]    [전체 ▼]    ← 기존 status select 유지
[칸반 컬럼]   [전체 ▼]    ← 기존 컬럼 필터 유지

── 자동 분류 ──

[태그]        [전체 ▼]    ← v0.6: 자유 태그 드롭다운
[경전]        [전체 ▼]    ← v0.6: prefix 드롭다운 (데이터 있을 때만)
[인물]        [전체 ▼]
[주제]        [전체 ▼]
[시기]        [전체 ▼]
[유형]        [전체 ▼]
```

- 각 prefix는 데이터에 등장할 때만 드롭다운 생성 (빈 섹션 없음)
- 드롭다운 옵션: "전체" + 가나다 정렬된 값 목록 + 각 값 옆 `(count)`
- 단일 선택 (v0.6은 multi-select 미지원)
- 한 prefix 선택 시 다른 prefix 선택은 유지 (AND 결합)

#### B.2.4 드롭다운 렌더 함수

```js
// sidebar.js
function renderPrefixDropdowns(container, cards) {
  // 자유 태그 드롭다운
  const freeTags = getFreeTags(cards);
  if (freeTags.length > 0) {
    container.appendChild(buildSidebarDropdown({
      label: '태그',
      key:   '__free',
      options: freeTags.map(t => ({
        value: t,
        label: `${t} (${countCardsWithFreeTag(cards, t)})`
      })),
      selected: sbFilter.freeTag,
      onChange: (val) => {
        sbFilter.freeTag = val;
        // 레거시 호환
        selectedTags = val ? new Set([val]) : new Set();
        rerenderViews();
      }
    }));
  }

  // prefix 드롭다운들
  const prefixIndex = buildPrefixIndex(cards);
  Object.keys(prefixIndex).forEach(prefix => {
    const values = prefixIndex[prefix];
    const selectedValue = (sbFilter.prefix && sbFilter.prefix.prefix === prefix)
      ? sbFilter.prefix.value : '';

    container.appendChild(buildSidebarDropdown({
      label: prefix,
      key:   prefix,
      options: values.map(v => ({
        value: v,
        label: `${v} (${countCardsWithPrefixValue(cards, prefix, v)})`
      })),
      selected: selectedValue,
      onChange: (val) => {
        sbFilter.prefix = val ? { prefix, value: val } : null;
        rerenderViews();
      }
    }));
  });
}

function buildSidebarDropdown({ label, key, options, selected, onChange }) {
  const wrap = document.createElement('div');
  wrap.className = 'sb-section';
  wrap.innerHTML = `
    <div class="sb-section-title">${escapeHTML(label)}</div>
    <select class="sb-select" data-key="${escapeHTML(key)}">
      <option value="">전체</option>
      ${options.map(o =>
        `<option value="${escapeHTML(o.value)}" ${o.value === selected ? 'selected' : ''}>
           ${escapeHTML(o.label)}
         </option>`
      ).join('')}
    </select>
  `;
  wrap.querySelector('select').addEventListener('change', e => onChange(e.target.value));
  return wrap;
}

function rerenderViews() {
  // 현재 뷰에 따라 적절한 렌더 함수 호출
  // legacy.js의 renderCards / renderKanban / renderList 등 호출
  if (typeof renderCards   === 'function') renderCards();
  if (typeof renderKanban  === 'function') renderKanban();
  if (typeof renderListView === 'function') renderListView();
  renderSidebar();
}
```

#### B.2.5 뷰 필터링에 prefix 조건 추가

legacy.js의 뷰 필터링 부분(예: 7849~7855 라인)에 prefix 필터를 _추가_한다. 기존 필터는 건드리지 않는다.

```js
// legacy.js의 카드 필터링 부분 — str_replace로 추가
let cards = [...S.cards];
if (selectedColId != null) cards = cards.filter(c => c.colId === selectedColId);
if (fg) cards = cards.filter(c => c.group === fg);
if (fs) cards = cards.filter(c => (S.userData.status[c.id]||'wait') === fs);
if (selectedTags.size > 0) {
  cards = cards.filter(c => (c.tags||[]).some(t => selectedTags.has(t.trim())));
}

// ↓ v0.6 추가
if (sbFilter && sbFilter.prefix) {
  const { prefix: p, value: v } = sbFilter.prefix;
  cards = cards.filter(c => (c.tags||[]).some(tag => {
    const parsed = parseTag(tag);
    return parsed.prefix === p && parsed.value === v;
  }));
}
```

같은 패턴을 `renderKanban`, `renderListView`에도 적용한다. _수정 위치_는 작업 시점에 grep으로 찾아 최소 범위만 `str_replace`.

#### B.2.6 자유 태그 중복 표시 방지

기존 자유태그 사이드바(refreshSbTagList)는 모든 태그를 표시한다. v0.6에서는 자유 태그만 표시되도록 필터링 추가:

```js
// refreshSbTagList 내부 — 태그 목록 빌드 시
const allTagsSet = new Set();
S.cards.forEach(c => (c.tags||[]).forEach(t => {
  const { prefix } = parseTag(t);
  if (!prefix) allTagsSet.add(t.trim());   // ← prefix 태그 제외
}));
```

#### B.2.7 build.js 업데이트

```js
const JS_MODULES = [
  'core/tag-parser.js',
  'ui/sidebar.js',         // ← 추가
  'core/legacy.js'
];
```

#### B.2 검증

- [ ] `node --check src/ui/sidebar.js` 통과
- [ ] 빌드 후 사이드바에 기존 [그룹], [학습상태] 그대로 표시
- [ ] 테스트 카드에 `인물:붓다` 추가 → [인물] 드롭다운 자동 생성
- [ ] `인물:붓다`, `인물:사리뿟다`, `학파:중관` 추가 → [인물], [학파] 드롭다운
- [ ] 드롭다운에서 값 선택 → 해당 카드만 표시 (3개 뷰 모두)
- [ ] 자유 태그 드롭다운에 prefix 태그(`인물:붓다`)가 나타나지 않음
- [ ] 모든 `인물:` 태그 삭제 → [인물] 드롭다운 자동 사라짐
- [ ] 그룹 + prefix 필터 동시 선택 → AND 결합으로 필터링
- [ ] `dist/snapshots/OL_ATLAS_v0.6-phaseB2.html` 보존

### B.3 search.js 추출 + prefix 검색

#### B.3.1 추출 대상

legacy.js에서 다음을 `src/core/search.js`로 이동:

- `runSearch` 함수
- `renderSearchDropdown` 함수
- `closeSearch` 함수
- `searchResults` 변수
- 검색 단축키 핸들러 (Cmd+K 등)

#### B.3.2 prefix 검색 통합

`runSearch`를 다음과 같이 수정. **기존 4필드 검색을 보존**한다 (이전 점검에서 발견된 회귀 위험 방지):

```js
// src/core/search.js
let searchResults = [];

function parseSearchQuery(query) {
  const trimmed = (query || '').trim();
  const colonIdx = trimmed.indexOf(':');
  if (colonIdx > 0) {
    const prefix = trimmed.slice(0, colonIdx).trim();
    const value  = trimmed.slice(colonIdx + 1).trim();
    if (prefix && value) {
      return { isPrefix: true, prefix, value };
    }
  }
  return { isPrefix: false, prefix: null, value: trimmed };
}

function cardMatchesQuery(card, parsedQuery) {
  const { isPrefix, prefix, value } = parsedQuery;
  if (!value) return false;
  const lower = value.toLowerCase();

  if (isPrefix) {
    // prefix 검색: tags에서 prefix:value 매칭
    return (card.tags || []).some(tag => {
      const p = parseTag(tag);
      return p.prefix === prefix &&
             p.value.toLowerCase().includes(lower);
    });
  }

  // 일반 검색: 기존 4필드 모두 검사 (회귀 방지)
  if (card.title && card.title.toLowerCase().includes(lower)) return true;
  if (card.group && card.group.toLowerCase().includes(lower)) return true;
  if (card.tags  && card.tags.some(t => t.toLowerCase().includes(lower))) return true;
  return cardSearchText(card).toLowerCase().includes(lower);
}

function runSearch(q) {
  if (!q || q.length < 1) { closeSearch(); return; }
  const parsed = parseSearchQuery(q);
  searchResults = S.cards.filter(c => cardMatchesQuery(c, parsed));
  renderSearchDropdown(q);
}

// renderSearchDropdown, closeSearch는 legacy.js에서 그대로 이동
```

#### B.3.3 build.js 업데이트

```js
const JS_MODULES = [
  'core/tag-parser.js',
  'core/search.js',        // ← 추가
  'ui/sidebar.js',
  'core/legacy.js'
];
```

#### B.3 검증

- [ ] `node --check src/core/search.js` 통과
- [ ] 일반 검색 `붓다` → 제목/그룹/태그/본문에서 모두 검색 (회귀 없음)
- [ ] `인물:붓다` 입력 → `인물:붓다` 태그 카드만 표시
- [ ] `학파:중관` 입력 → 해당 카드만 표시
- [ ] 빈 검색어 → 드롭다운 닫힘
- [ ] 사이드바 prefix 필터 + 검색 동시 동작
- [ ] `dist/snapshots/OL_ATLAS_v0.6-phaseB3.html` 보존

### B.4 Phase B 완료 조건

3개 모듈이 추출되고 prefix 사이드바/검색이 작동. 기존 기능 회귀 없음.

---

## 9. Phase C — schemaVersion + tokens.css + 검증 강화

### C.1 schemaVersion 도입

legacy.js의 `makeDefault()`와 `normalizeState()`를 수정:

```js
// makeDefault() 반환 객체의 meta에 추가
meta: {
  fileId:        'ol-' + ...,
  title:         'OL Weaving the Wisdom',
  created:       today(),
  version:       '1.0.0',
  schemaVersion: 6        // ← 추가
}

// normalizeState() 내부
if (!s.meta.schemaVersion) s.meta.schemaVersion = 6;
```

마이그레이션 로직은 작성하지 않는다.

### C.2 normalizeCard 정책 주석

기존 `normalizeCard` 함수 상단에 정책 주석 추가:

```js
function normalizeCard(card) {
  // ══════════════════════════════════════════════════
  // 정책 (v0.6): 모르는 필드는 보존한다.
  // fork 모델에서 v0.7+로 만든 데이터(meta, links 등)가
  // v0.6 파일로 열려도 손실되지 않도록 한다.
  // 알려진 필드만 정규화하고, 새 필드를 적극 삭제하지 않는다.
  // (단, bodyMd, bodyMode, history 등 알려진 레거시는 삭제 유지)
  // ══════════════════════════════════════════════════

  // ── 알려진 레거시 마이그레이션 ──
  if (card.bodyMd) { ... }
  ...
}
```

### C.3 tokens.css 분리

`src/styles/main.css` 상단에서 HSL 변수 블록을 잘라내어 `src/styles/tokens.css`로 이동:

```css
/* src/styles/tokens.css */
:root {
  --background: 0 0% 100%;
  /* ... 모든 HSL 토큰 ... */
  --header-h:  56px;
  --sidebar-w: 256px;
}

html.dark, :root.dark {
  --background: 0 0% 3.9%;
  /* ... 다크 모드 토큰 ... */
}
```

build.js의 CSS_MODULES 업데이트:

```js
const CSS_MODULES = [
  'styles/tokens.css',    // ← 추가, 먼저 로드
  'styles/main.css'
];
```

### C.4 자동 검증 스크립트

`test/syntax-check.sh`:

```bash
#!/bin/bash
set -e
echo "── syntax check ──"
for f in src/core/*.js src/ui/*.js; do
  [ -f "$f" ] || continue
  echo "  checking $f"
  node --check "$f"
done
echo "✓ all syntax OK"
```

`test/build-check.sh`:

```bash
#!/bin/bash
set -e
echo "── build check ──"
node build.js

SIZE=$(wc -c < dist/OL_ATLAS_v0.6.html)
echo "  dist size: ${SIZE} bytes"
if [ "$SIZE" -lt 512000 ] || [ "$SIZE" -gt 921600 ]; then
  echo "✗ unexpected file size"
  exit 1
fi

# 슬롯 미치환 검사
if grep -q "<!-- BUILD:" dist/OL_ATLAS_v0.6.html; then
  echo "✗ 미치환 슬롯 발견"
  exit 1
fi

# __OL_BUILD__ 주입 검사
if ! grep -q "__OL_BUILD__" dist/OL_ATLAS_v0.6.html; then
  echo "✗ 빌드 메타데이터 누락"
  exit 1
fi

echo "✓ build OK"
```

### C.5 검증 체크리스트

- [ ] schemaVersion이 새 데이터에 기록됨
- [ ] 기존 v0.5 데이터 로드 시 자동으로 schemaVersion=6 부여
- [ ] tokens.css 분리 후에도 라이트/다크 모드 정상
- [ ] `bash test/syntax-check.sh` 통과
- [ ] `bash test/build-check.sh` 통과
- [ ] `dist/snapshots/OL_ATLAS_v0.6-phaseC.html` 보존

---

## 10. Phase D — 회귀 테스트 및 릴리스

### D.1 회귀 테스트 (전체)

빈 상태에서 시작 + v0.5 데이터 임포트 양쪽 모두:

**기본 기능 (v0.5.1 회귀 방지)**:

- [ ] 칸반: 카드 추가/편집/삭제, 드래그앤드롭, 컬럼 추가/삭제
- [ ] 그리드: 정렬, 그룹/상태 필터
- [ ] 리스트: 정렬, bulk 선택/삭제
- [ ] 문서 뷰: TOC, 이전/다음, 인라인 편집/저장
- [ ] 검색 (Cmd+K): 4필드 일반 검색
- [ ] About: 제목/버전 편집, 저장
- [ ] 휴지통: 삭제 → 복원, 영구삭제
- [ ] 다크모드 토글 (라이트/다크/시스템)
- [ ] 마크다운: 헤딩, 리스트, 코드, 인용, 이미지
- [ ] export HTML/JSON/Markdown
- [ ] 자유 태그 사이드바 작동

**v0.6 신규**:

- [ ] `인물:붓다`, `학파:중관` 추가 → 사이드바 드롭다운 자동 생성
- [ ] 드롭다운 선택 → 3개 뷰 모두 필터링
- [ ] 자유 태그 드롭다운에 prefix 태그 미포함
- [ ] prefix 검색 (`인물:붓다`) 작동
- [ ] schemaVersion === 6 기록
- [ ] `window.__OL_BUILD__` 주입 확인
- [ ] 미래 필드(`meta: {...}`) 추가한 카드 → 저장/로드 후 보존

**필터 조합**:

- [ ] 그룹 + prefix 동시 선택 → AND 결합
- [ ] 검색 + prefix 동시 적용
- [ ] prefix 선택 해제 ("전체") → 필터 해제

### D.2 최종 빌드 명세

```
dist/OL_ATLAS_v0.6.html

크기:         약 700~720 KB (v0.5.1 692 KB + 신규 모듈 분량)
외부 의존성:  0
schemaVersion: 6
빌드메타:     window.__OL_BUILD__ 주입
ORIGIN:       하드코딩, Object.freeze
모듈 구성:    tag-parser + search + sidebar + legacy
```

### D.3 CHANGELOG

```markdown
# v0.6.0

## Added
- prefix 태그 파싱 (`인물:붓다`, `학파:중관` 등 자유 어휘)
- 사이드바 자동 분류 드롭다운 (데이터에 등장하는 prefix별)
- prefix 검색 (`인물:붓다` → 해당 태그 카드만)
- dev/dist 빌드 시스템 (소스 모듈화, 단일 HTML 산출물)
- schemaVersion 필드 (마이그레이션 기반)
- window.__OL_BUILD__ 빌드 메타데이터

## Changed
- 사이드바 필터 상태 통합 (sbFilter 객체)
- 자유 태그 사이드바: prefix 태그 자동 제외

## Removed
- 없음

## Notes
- 카드 스키마 자체는 v0.5.1 그대로 유지
- 기존 데이터 호환 (마이그레이션 로직 없음, 필드만 부여)
- 모르는 필드 보존 정책으로 v0.7+ 데이터와 호환
```

---

## 11. 위험 관리

|위험|확률|영향|완화책|
|---|---|---|---|
|빌드 산출물이 v0.5.1과 동작 차이|중|높음|Phase A 회귀 테스트|
|CSS 주석 깨짐 (과거 사고 재발)|중|높음|CSS 별도 파일, 자동 편집 최소화|
|JS 모듈 로드 순서 문제|중|높음|의존성 순서 명시, build.js 검증|
|함수명 충돌|낮음|중|작업 전 grep 확인 (이미 함)|
|사이드바 추출 중 기존 필터 깨짐|중|중|str_replace 최소 범위, 레거시 변수 호환 유지|
|검색 4필드 회귀|중|높음|search.js의 cardMatchesQuery에 명시|
|sbFilter와 selectedColId/Tags 양립 버그|중|중|B.2에서 양쪽 동시 갱신|
|prefix 태그 중복 노출|낮음|낮음|B.2.6 처리|

### 롤백 계획

```
dist/snapshots/
├── OL_ATLAS_v0.6-phaseA.html    ← v0.5.1과 동일 (안전망)
├── OL_ATLAS_v0.6-phaseB1.html   ← tag-parser 추가
├── OL_ATLAS_v0.6-phaseB2.html   ← sidebar 드롭다운
├── OL_ATLAS_v0.6-phaseB3.html   ← prefix 검색
└── OL_ATLAS_v0.6-phaseC.html    ← schemaVersion + tokens.css
```

문제 발생 시 직전 스냅샷을 dist에 복사 → 즉시 롤백.

---

## 12. 작업 진행 절차

1. **착수 전**: 직전 단계 검증 체크리스트 모두 ✓
2. **작업**: 본 문서의 해당 절 기준
3. **편집**: `str_replace`로 최소 범위만. 전체 파일 재작성 금지
4. **매 수정 후**: `node --check`
5. **빌드**: `node build.js`
6. **검증**: 해당 단계 체크리스트
7. **스냅샷**: `dist/snapshots/`에 복사
8. **보고**: 비움에게 변경사항과 체크리스트 결과 보고
9. **허락**: 다음 단계 착수 허락 받기

검증 실패 시 무조건 멈춤. 추정 금지. 불명확하면 비움에게 먼저 확인.

---

## 13. 비범위 (v0.6 명시적 보류)

v0.7 이후로 미룬다:

- 마이그레이션 로직 (필드만 있음, 로직 없음)
- 다중 선택 필터 (멀티 체크박스 드롭다운)
- links 필드 + wikilink
- 고정 meta 필드 (person/place/time 등)
- 칸반/그리드/리스트/문서 뷰의 모듈 분리
- 마크다운 파서 모듈 분리
- 컴포넌트 단위 CSS 분리
- 그래프/타임라인/지도 뷰
- AI 보조 (자동 태깅 등)
- IndexedDB / PWA / Electron
- 외부 런타임 라이브러리

---

## 14. 첫 작업 세션 진입점

```
1. /mnt/user-data/uploads/OL_ATLAS_v0_5_1.html 확인
2. /home/claude/ol-v6/ol-atlas/ 디렉토리 구조 생성
3. Phase A.5 작업 지시 순서대로 실행
4. Phase A.6 체크리스트 통과 확인
5. dist 산출 및 비움 보고
6. Phase B1 착수 허락 받기
```

---

## 부록 A. v1 → v2 변경 요약

|영역|v1|v2|
|---|---|---|
|Phase 구성|A, B, C, D (4단계)|A, B(B1/B2/B3), C, D (6단계)|
|모듈 추출|tag-parser만 (1개)|tag-parser + sidebar + search (3개)|
|CSS 분리|main.css 하나|tokens.css + main.css (2개)|
|사이드바 UI|펼친 리스트 (값 모두 나열)|드롭다운 (분류 축당 select 하나)|
|schemaVersion|v0.7로 미룸|v0.6에서 필드만 도입|
|빌드 메타데이터|없음|window.**OL_BUILD**|
|미래 필드 보존|명시 없음|normalizeCard 주석으로 명문화|
|검색 호환|cardSearchText 한 줄|4필드 모두 검사 (회귀 방지)|
|필터 상태|분산 변수 그대로|sbFilter 객체 통합 + 레거시 호환|
|자유 태그 사이드바|변경 없음|prefix 태그 자동 제외|
|빌드 검증|단순 빌드|슬롯/태그/크기 자동 검증|

---

_이 문서는 비움과 Claude의 7단계 검증을 거친 실행 계약이다._ _v2 추가 결정: 3개 모듈 분리, 드롭다운 UI, schemaVersion 도입, 미래 필드 보존, 검증 강화_