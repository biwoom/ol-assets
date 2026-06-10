# OL ATLAS v0.6 작업기획서 및 상세 작업지시서

작성: 2026-05-17  
대상: v0.5.1 → v0.6.0  
상태: 비움 확정

---
## 1. 확정된 원칙

### 유지하는 것

- 단일 HTML 파일 배포 (fork 가능성의 핵심)
- 외부 런타임 의존성 0
- localStorage 기반 데이터 저장
- ORIGIN 하드코딩 (author/copyright/license) — fork 이후는 받는 사람 몫
- shadcn/ui 디자인 시스템 (Phase 1~6 완료 상태 유지)

### 도입하는 것

- dev/dist 분리 (소스는 모듈로, 산출물은 단일 HTML)
- prefix 태그 파싱 (`인물:사리뿟다`, `학파:중관` 등 자유 어휘)
- prefix 기반 사이드바 자동 구조화
- prefix 기반 검색

### 도입하지 않는 것 (v0.6 비범위)

- 마이그레이션 시스템 — 현재 실사용 데이터 없음. 불필요
- 고정 6축 meta 필드 (`meta.person`, `meta.place` 등) — 콘텐츠 다양성 커버 불가
- links 필드 + wikilink — 6축 meta 쿼리로 대부분 대체 가능. 필요성 미검증
- IndexedDB / PWA / Electron
- 런타임 외부 라이브러리 (Cytoscape, Leaflet 등)
- 빌드 시스템 (webpack/vite)

---

## 2. v0.6의 핵심 가치 한 문장

> "태그 입력창 하나에서 `인물:사리뿟다`, `학파:중관` 처럼 자유 어휘의 prefix 태그를 입력하면,  
> 코드가 이를 자동 파싱해서 사이드바를 구조화하고 검색을 강화한다.  
> 그리고 이 모든 것을 가능하게 하는 빌드 시스템을 도입한다."

---

## 3. prefix 태그 방식 상세 결정

### 3.1 방식

태그 입력창은 현재와 동일하다. 사용자가 콜론(:)을 포함한 태그를 입력하면 코드가 자동으로 prefix와 값을 분리한다.

```
입력:  인물:사리뿟다
파싱:  prefix = "인물",  value = "사리뿟다"

입력:  학파:중관
파싱:  prefix = "학파",  value = "중관"

입력:  안내
파싱:  prefix = null,    value = "안내"  (자유 태그)
```

### 3.2 어휘 자유도

코드가 강제하는 prefix 목록은 없다. 비움이 콘텐츠 시리즈마다 자기 어휘를 자유롭게 발명한다.

```
붓다스토리:   인물:붓다  장소:기원정사  시기:성도후1년  주제:연기  유형:설법  경전:DN1
법구경:       품:쌍서품  게송:1  주제:마음  유형:게송
중관학:       학파:중관  논사:용수  논서:중론  주제:공  유형:논증
선림:         법맥:임제종  공안:무문관28칙  인물:마조
```

같은 `인물:` prefix가 시리즈를 넘어 공유되면 자연스러운 횡단 연결이 생긴다.  
어휘 통일은 코드가 강제하지 않고 사용자 컨벤션으로 관리한다.

### 3.3 콜론 충돌 정책

자유 태그에 콜론이 들어갈 경우 의도치 않게 prefix로 파싱된다.  
**결정: 별도 처리하지 않는다.** 태그에 콜론을 쓰는 것은 prefix 의도로 약속한다.  
자유 태그에는 콜론을 쓰지 않는 컨벤션으로 운영한다. 코드는 단순하게 유지한다.

### 3.4 파싱 함수 (핵심 로직)

```js
// 태그 하나 파싱
function parseTag(tag) {
  const colonIdx = tag.indexOf(':');
  if (colonIdx > 0) {
    return {
      prefix: tag.slice(0, colonIdx).trim(),
      value:  tag.slice(colonIdx + 1).trim(),
      raw:    tag
    };
  }
  return { prefix: null, value: tag, raw: tag };
}

// 전체 카드에서 사용 중인 prefix → 값 목록 추출
function buildPrefixIndex(cards) {
  const index = {};  // { "인물": ["붓다", "사리뿟다"], "학파": ["중관"] }
  cards.forEach(card => {
    (card.tags || []).forEach(tag => {
      const { prefix, value } = parseTag(tag);
      if (prefix && value) {
        if (!index[prefix]) index[prefix] = new Set();
        index[prefix].add(value);
      }
    });
  });
  // Set → 정렬된 배열로 변환
  Object.keys(index).forEach(k => {
    index[k] = [...index[k]].sort();
  });
  return index;
}
```

---

## 4. 데이터 모델

### 4.1 카드 스키마 — 변경 없음

```js
// v0.6 카드 스키마 = v0.5.1 그대로
{
  id:       number,
  colId:    number,
  title:    string,
  body:     string,
  slug:     string,
  group:    string,
  tags:     string[],   // prefix 태그 + 자유 태그 혼용
  priority: 'high' | 'mid' | 'low',
  images:   { [tokenId]: dataURI },
  created:  'YYYY-MM-DD'
}
```

`meta`, `links` 필드는 추가하지 않는다.  
prefix 태그가 `tags` 안에서 구조 역할을 담당한다.

### 4.2 마이그레이션 — 없음

현재 실사용 데이터가 없으므로 마이그레이션 로직을 작성하지 않는다.  
schemaVersion 필드도 v0.6에서는 도입하지 않는다. v0.7에서 실제 사용자 데이터가 누적된 뒤 첫 마이그레이션 시점에 도입한다.

---

## 5. 작업 Phase 구성

```
Phase A: 빌드 골격 구축        ← dev/dist 분리. 기능 변경 0
Phase B: prefix 파싱 + 검색    ← 핵심 기능. 태그 로직 + 검색 강화
Phase C: 사이드바 자동 구조화  ← prefix 인덱스 기반 사이드바
Phase D: 검증 및 릴리스        ← 회귀 테스트 + 산출물 확정
```

각 Phase는 완료 조건을 충족해야 다음으로 진행한다.  
Phase마다 dist 스냅샷을 보존한다.

---

## 6. Phase A — 빌드 골격 구축

### A.1 목표

v0.5.1을 기능 변경 없이 dev/dist 구조로 옮긴다.  
빌드 스크립트 하나로 `dist/OL_ATLAS_v0.6.html`을 생성한다.  
빌드 결과물이 v0.5.1과 기능적으로 동일해야 한다.

### A.2 디렉토리 구조

```
ol-atlas/
├── src/
│   ├── index.html          ← HTML 골격 (슬롯 마커 포함)
│   ├── styles/
│   │   └── main.css        ← v0.5.1 CSS 전체
│   ├── core/
│   │   └── legacy.js       ← v0.5.1 JS 전체 (Phase A에서는 단일 덩어리)
│   └── assets/
│       └── favicon.b64     ← base64 favicon
├── build.js                ← 빌드 스크립트 (Node 기본 fs만 사용)
├── package.json            ← scripts만. devDependencies 없음
└── dist/
    ├── OL_ATLAS_v0.6.html  ← 빌드 산출물
    └── snapshots/          ← Phase별 스냅샷 보관
```

Phase A에서는 분할하지 않는다. JS 전체를 `legacy.js` 한 파일로 두고,  
Phase B부터 필요한 부분만 별도 모듈로 추출한다.

### A.3 src/index.html 구조

```html
<html lang="ko"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/jpeg" href="<!-- BUILD:FAVICON -->">
<title>OL · ATLAS</title>
<script>(function(){/* 다크모드 FOUC 방지 — 원본 그대로 */})()</script>
<!-- BUILD:CSS -->
</head>
<body>
<!-- v0.5.1 body 마크업 전체 -->
<!-- BUILD:JS -->
</body></html>
```

슬롯 마커 3개: `<!-- BUILD:FAVICON -->`, `<!-- BUILD:CSS -->`, `<!-- BUILD:JS -->`

### A.4 build.js

```js
// build.js — Node 기본 fs만 사용. 외부 의존성 0
const fs   = require('fs');
const path = require('path');

const SRC  = path.join(__dirname, 'src');
const DIST = path.join(__dirname, 'dist');

// 1. index.html 읽기
let html = fs.readFileSync(path.join(SRC, 'index.html'), 'utf8');

// 2. 소스 읽기
const favicon = fs.readFileSync(path.join(SRC, 'assets/favicon.b64'), 'utf8').trim();
const css     = fs.readFileSync(path.join(SRC, 'styles/main.css'),    'utf8');

// JS 모듈 순서 — Phase A에서는 legacy 하나뿐
// Phase B부터 앞에 추가됨: ['core/tag-parser.js', 'core/legacy.js']
const JS_MODULES = [
  'core/legacy.js'
];
const js = JS_MODULES
  .map(p => fs.readFileSync(path.join(SRC, p), 'utf8'))
  .join('\n\n');

// 3. 슬롯 치환
html = html
  .replace('<!-- BUILD:FAVICON -->', `data:image/jpeg;base64,${favicon}`)
  .replace('<!-- BUILD:CSS -->',     `<style>\n${css}\n</style>`)
  .replace('<!-- BUILD:JS -->',      `<script>\n${js}\n</script>`);

// 4. dist 저장
if (!fs.existsSync(DIST)) fs.mkdirSync(DIST, { recursive: true });
const outPath = path.join(DIST, 'OL_ATLAS_v0.6.html');
fs.writeFileSync(outPath, html);

const kb = (fs.statSync(outPath).size / 1024).toFixed(1);
console.log(`✓ built → ${outPath}  (${kb} KB)`);
```

### A.5 package.json

```json
{
  "name": "ol-atlas",
  "version": "0.6.0",
  "scripts": {
    "build": "node build.js",
    "check": "node --check src/core/legacy.js",
    "dev":   "node build.js && echo '→ open dist/OL_ATLAS_v0.6.html'"
  }
}
```

### A.6 작업 지시

다음 순서로 실행한다.

1. `/home/claude/ol-v6/ol-atlas/` 디렉토리 구조 생성
2. v0.5.1 HTML 파싱 및 분할:
    - `<link rel="icon" ... href="data:...">` 의 base64 값 → `src/assets/favicon.b64`
    - `<style>...</style>` 내용 → `src/styles/main.css`
    - `<script>...</script>` 내용 → `src/core/legacy.js`
    - HTML 골격 (슬롯 마커 삽입) → `src/index.html`
3. `build.js` 작성
4. `package.json` 작성
5. `node --check src/core/legacy.js` 실행 — 오류 없어야 함
6. `node build.js` 실행 — `dist/OL_ATLAS_v0.6.html` 생성
7. 검증 체크리스트 확인

**주의사항**:

- CSS 파일 분리 시 `/* ... */` 주석이 잘리지 않도록 확인 (과거 사고 재발 방지)
- favicon base64는 줄바꿈 없는 단일 문자열이어야 함
- `legacy.js` 첫 줄에 `'use strict';` 또는 즉시실행함수가 있으면 그대로 유지

### A.7 검증 체크리스트

- [ ] `node --check src/core/legacy.js` 통과
- [ ] `node build.js` 오류 없이 실행
- [ ] dist 파일 크기가 v0.5.1 (692 KB)과 ±5% 이내
- [ ] dist 파일을 브라우저에서 열어 다음 모두 정상 작동:
    - 칸반 뷰 (드래그앤드롭, 컬럼 추가/삭제)
    - 카드 그리드 / 리스트 뷰
    - 문서 뷰 (TOC, 이전/다음)
    - 검색 (Cmd+K)
    - About 페이지
    - 다크모드 토글
- [ ] `dist/snapshots/OL_ATLAS_v0.6-phaseA.html` 보존

### A.8 완료 조건

`dist/OL_ATLAS_v0.6.html`이 v0.5.1과 기능적으로 동일하고,  
소스가 빌드 가능한 구조로 분리되어 있다.

---

## 7. Phase B — prefix 태그 파싱 + 검색 강화

### B.1 목표

태그에서 prefix를 파싱하는 핵심 로직을 추가한다.  
검색이 `인물:붓다` 형태의 prefix 검색을 지원한다.  
기존 태그 기능은 영향받지 않는다.

### B.2 추출할 모듈: `src/core/tag-parser.js`

legacy.js에서 태그 관련 로직을 추출하지 않고, **신규 파일로 추가**한다.  
legacy.js는 이 파일의 함수를 사용한다.

```js
// src/core/tag-parser.js
// ── prefix 태그 파싱 유틸 ──────────────────────────────

/**
 * 태그 문자열 하나를 파싱한다.
 * "인물:사리뿟다" → { prefix: "인물", value: "사리뿟다", raw: "인물:사리뿟다" }
 * "안내"          → { prefix: null,   value: "안내",     raw: "안내" }
 */
function parseTag(tag) {
  if (typeof tag !== 'string') return { prefix: null, value: String(tag), raw: tag };
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
 * 카드 배열에서 prefix 인덱스를 빌드한다.
 * 반환: { "인물": ["붓다", "사리뿟다"], "학파": ["중관", "유식"] }
 * prefix 키는 가나다 순, 값 배열도 가나다 순 정렬.
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
 * 검색어가 prefix 검색인지 판별하고 파싱한다.
 * "인물:붓다" → { isPrefix: true,  prefix: "인물", value: "붓다" }
 * "붓다"      → { isPrefix: false, prefix: null,   value: "붓다" }
 */
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

/**
 * 카드가 검색어와 매칭되는지 판별한다.
 * prefix 검색: 해당 prefix의 값이 포함되면 매칭
 * 일반 검색:   기존 cardSearchText 로직 유지
 */
function cardMatchesQuery(card, parsedQuery) {
  const { isPrefix, prefix, value } = parsedQuery;
  if (!value) return true;

  if (isPrefix) {
    // prefix 검색: tags 중 prefix:value 를 가진 태그가 있으면 매칭
    return (card.tags || []).some(tag => {
      const parsed = parseTag(tag);
      return parsed.prefix === prefix &&
             parsed.value.toLowerCase().includes(value.toLowerCase());
    });
  }

  // 일반 검색: 기존 cardSearchText 함수 활용
  // (legacy.js의 cardSearchText를 그대로 사용)
  return cardSearchText(card).toLowerCase().includes(value.toLowerCase());
}
```

### B.3 build.js 모듈 순서 업데이트

```js
const JS_MODULES = [
  'core/tag-parser.js',   // ← 신규. legacy.js보다 먼저 로드되어야 함
  'core/legacy.js'
];
```

### B.4 legacy.js 검색 로직 수정

기존 `renderSearchDropdown` 함수에서 카드 필터링 부분을 교체한다.

```js
// 기존 (추정 패턴)
const results = S.cards.filter(c =>
  cardSearchText(c).toLowerCase().includes(q.toLowerCase())
);

// 변경 후
const parsedQuery = parseSearchQuery(q);
const results = S.cards.filter(c => cardMatchesQuery(c, parsedQuery));
```

**주의**: legacy.js에서 수정할 정확한 위치는 작업 시점에 코드를 확인 후 결정한다.  
`str_replace`로 최소 범위만 수정한다.

### B.5 검증 체크리스트

- [ ] `node --check src/core/tag-parser.js` 통과
- [ ] `node build.js` 오류 없이 실행
- [ ] 검색창에 `인물:붓다` 입력 → `인물:붓다` 태그를 가진 카드만 표시
- [ ] 검색창에 `학파:중관` 입력 → 해당 태그 카드만 표시
- [ ] 검색창에 `붓다` 입력 → 기존 전체 텍스트 검색 정상 작동
- [ ] prefix 없는 기존 태그 검색 영향 없음
- [ ] 빈 검색어에서 모든 카드 표시
- [ ] `dist/snapshots/OL_ATLAS_v0.6-phaseB.html` 보존

### B.6 완료 조건

prefix 태그 파싱 로직이 작동하고, 검색이 prefix 방식을 지원한다.  
기존 검색 기능은 영향받지 않는다.

---

## 8. Phase C — 사이드바 자동 구조화

### C.1 목표

사이드바가 prefix 인덱스를 자동 탐지해서 섹션을 구성한다.  
비움이 새 prefix를 사용하기 시작하면 사이드바에 자동으로 섹션이 생긴다.  
기존 그룹/태그 사이드바는 그대로 유지한다.

### C.2 사이드바 구성 변경

현재 사이드바 구조:

```
[그룹]
  시작하기
  붓다스토리

[태그]
  안내
  시작
```

v0.6 사이드바 구조:

```
[그룹]
  시작하기
  붓다스토리

── prefix 태그 (자동 생성) ──

[인물]            ← "인물:" prefix 카드가 있을 때 자동 등장
  붓다 (12)
  사리뿟다 (5)

[학파]            ← "학파:" prefix 카드가 있을 때 자동 등장
  중관 (8)
  유식 (3)

[주제]
  공 (6)
  연기 (4)

── 자유 태그 ──

[태그]
  안내 (1)
  중요 (3)
```

- prefix 섹션은 실제 데이터에 등장하는 것만 표시 (빈 섹션 없음)
- prefix 키는 가나다/알파벳 순 정렬
- 각 값 옆에 해당 카드 수 표시
- 클릭 시 해당 prefix:value 태그를 가진 카드만 필터링

### C.3 구현 방식

`renderSidebar` 함수 내부에 prefix 섹션 렌더 로직을 추가한다.  
`buildPrefixIndex(S.cards)`로 인덱스를 빌드하고, 결과를 순회하며 섹션을 생성한다.

```js
// renderSidebar 내부 추가 (pseudocode)
const prefixIndex = buildPrefixIndex(S.cards);

Object.keys(prefixIndex).forEach(prefix => {
  const values = prefixIndex[prefix];
  // 섹션 헤더: prefix명
  // 항목: value (count) — 클릭 시 필터 적용
  // 필터 적용: S.activeFilter = { type: 'prefix', prefix, value }
});
```

필터 상태는 기존 사이드바 필터 구조에 `prefix` 타입을 추가한다.

### C.4 필터 연동

기존 뷰 렌더 함수(renderKanban, renderGrid, renderList)에서  
`prefix` 타입 필터를 처리하는 조건을 추가한다:

```js
// 카드 필터링 시
if (activeFilter.type === 'prefix') {
  return cards.filter(card =>
    (card.tags || []).some(tag => {
      const { prefix, value } = parseTag(tag);
      return prefix === activeFilter.prefix && value === activeFilter.value;
    })
  );
}
```

### C.5 검증 체크리스트

- [ ] 테스트 카드에 `인물:붓다`, `인물:사리뿟다` 태그 추가 후 사이드바에 [인물] 섹션 자동 생성
- [ ] `학파:중관` 태그 추가 시 [학파] 섹션 자동 생성
- [ ] 모든 `인물:` 태그 삭제 시 [인물] 섹션 자동 사라짐
- [ ] 사이드바 [인물] > 붓다 클릭 → `인물:붓다` 카드만 칸반/그리드/리스트에 표시
- [ ] prefix 필터 + 검색이 동시에 작동
- [ ] 기존 그룹/자유태그 필터 영향 없음
- [ ] `dist/snapshots/OL_ATLAS_v0.6-phaseC.html` 보존

### C.6 완료 조건

데이터에 등장하는 prefix가 사이드바에 자동으로 구조화되고,  
클릭 필터링이 모든 뷰에서 동작한다.

---

## 9. Phase D — 검증 및 릴리스

### D.1 자동 검증 스크립트

```
ol-atlas/
└── test/
    ├── syntax-check.sh     ← JS 파일 전체 문법 검사
    └── build-check.sh      ← 빌드 + 크기 검증
```

`test/syntax-check.sh`:

```bash
#!/bin/bash
set -e
echo "── syntax check ──"
for f in src/core/*.js; do
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
# 500 KB ~ 900 KB 범위 검사
if [ "$SIZE" -lt 512000 ] || [ "$SIZE" -gt 921600 ]; then
  echo "✗ unexpected file size"
  exit 1
fi
echo "✓ build OK"
```

### D.2 수동 회귀 테스트 목록

빈 상태에서 시작:

- [ ] 칸반 뷰: 카드 추가, 드래그앤드롭, 컬럼 추가/삭제
- [ ] 카드 그리드 뷰: 정렬, 그룹 필터
- [ ] 리스트 뷰: 정렬, bulk 선택/삭제
- [ ] 문서 뷰: TOC 클릭, 이전/다음 이동, 인라인 편집, 저장
- [ ] 검색 (Cmd+K): 일반 검색, prefix 검색
- [ ] About 페이지: 제목/버전 편집, 저장
- [ ] 휴지통: 삭제 → 복원, 영구삭제
- [ ] 다크모드 토글 (라이트/다크/시스템)
- [ ] 마크다운 렌더: 헤딩, 리스트, 코드블록, 인용
- [ ] export HTML/JSON/Markdown

prefix 태그 시나리오:

- [ ] `인물:붓다` 태그 추가 → 사이드바 [인물] 섹션 생성
- [ ] `학파:중관`, `학파:유식` 추가 → [학파] 섹션에 두 항목
- [ ] 사이드바 클릭 필터 → 해당 카드만 표시
- [ ] 검색 `인물:붓다` → 해당 카드만 표시
- [ ] 일반 검색 `붓다` → 제목/본문/태그 전체 검색 유지

### D.3 최종 빌드 결과물 명세

```
dist/OL_ATLAS_v0.6.html

크기:     v0.5.1 (692 KB) + tag-parser.js 분량 (< 5 KB) = 약 700 KB 예상
외부의존: 0
첫 줄:    <html lang="ko">
ORIGIN:   하드코딩, Object.freeze 유지
```

### D.4 CHANGELOG

```markdown
# v0.6.0

## Added
- prefix 태그 파싱 (`인물:붓다`, `학파:중관` 등 자유 어휘)
- prefix 기반 사이드바 자동 구조화 (데이터에 등장하는 prefix 자동 탐지)
- prefix 검색 (`인물:붓다` → 해당 태그 카드만 표시)
- dev/dist 빌드 시스템 (소스 모듈화, 단일 HTML 산출물)

## Changed
- 없음

## Removed
- 없음

## Notes
- 기존 tags 필드 그대로 유지. 스키마 변경 없음
- 기존 데이터 호환. 마이그레이션 없음
- prefix 어휘는 코드가 강제하지 않음. 사용자 자유 정의
```

---

## 10. 위험 관리

|위험|확률|영향|완화책|
|---|---|---|---|
|빌드 산출물이 v0.5.1과 동작 차이|중|높음|Phase A 회귀 테스트 철저히|
|CSS 주석 깨짐 (과거 사고 재발)|중|높음|CSS 파일 분리로 자동 편집 대상 제외|
|JS 모듈 로드 순서 문제|중|높음|tag-parser.js를 legacy.js보다 먼저 배치|
|parseTag 함수가 legacy.js 기존 함수명과 충돌|낮음|중|작업 전 legacy.js에서 parseTag 존재 여부 grep 확인|
|사이드바 렌더 수정 중 기존 필터 깨짐|중|중|str_replace 최소 범위 수정. Phase C 후 전체 필터 테스트|

### 롤백 계획

```
dist/snapshots/
├── OL_ATLAS_v0.6-phaseA.html   ← v0.5.1과 동일. 최종 안전망
├── OL_ATLAS_v0.6-phaseB.html   ← prefix 검색까지
└── OL_ATLAS_v0.6-phaseC.html   ← 사이드바까지
```

문제 발생 시 해당 스냅샷을 dist에 복사해서 즉시 롤백.

---

## 11. 작업 진행 절차 (Claude 세션 진행 규칙)

1. **착수 전**: 직전 Phase의 검증 체크리스트가 모두 ✓인지 확인
2. **작업**: 이 문서의 해당 Phase 기준으로 진행
3. **편집 방식**: `str_replace`로 최소 범위만 수정. 전체 파일 재작성 금지
4. **매 수정 후**: `node --check` 실행
5. **빌드**: `node build.js`
6. **스냅샷**: Phase 완료 시 `dist/snapshots/`에 복사
7. **보고**: 비움에게 변경 사항과 체크리스트 결과 보고 후 다음 Phase 허락 받기

검증 실패 시 무조건 멈추고 원인 분석 후 재시도.  
불명확한 것은 추정하지 않고 비움에게 먼저 확인한다.

---

## 12. 비범위 (v0.6에서 다루지 않는 것)

v0.7 이후로 명시적 보류:

- links 필드 + wikilink — 6축 prefix 쿼리로 대부분 대체 가능. 필요성 미검증
- 고정 meta 필드 (person/place/time 등) — 콘텐츠 다양성 커버 불가
- 마이그레이션 시스템 — 실사용 데이터 없음. v0.7 첫 배포 후 도입
- schemaVersion — 마이그레이션과 함께 도입
- 그래프/타임라인/지도 뷰
- 카드 간 관계 시각화
- 자동 태깅 (AI 보조)
- IndexedDB / PWA / Electron
- 외부 런타임 라이브러리

---

## 13. 첫 작업 세션 진입점

```
1. /mnt/user-data/uploads/OL_ATLAS_v0_5_1.html 확인
2. /home/claude/ol-v6/ol-atlas/ 디렉토리 구조 생성
3. Phase A.6 작업 지시 순서대로 실행
4. Phase A.7 체크리스트 전체 통과 확인
5. /mnt/user-data/outputs/dist/OL_ATLAS_v0.6.html 산출
6. 비움에게 Phase A 완료 보고 → Phase B 착수 허락
```

---

_이 문서는 비움과 Claude의 의견 교환을 통해 확정된 실행 계약이다._  
_수용된 결정: dev/dist 분리, prefix 태그 파싱, 사이드바 자동 구조화_  
_거부된 결정: 고정 6축 meta, links/wikilink, 마이그레이션, 외부 의존성 일체_