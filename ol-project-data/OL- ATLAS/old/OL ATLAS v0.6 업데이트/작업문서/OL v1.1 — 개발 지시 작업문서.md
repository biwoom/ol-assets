# OL v1.1 — 개발 지시 작업문서

> **베이스 파일**: `ol-v1_0.html` (8,245줄) **출력 파일**: `/mnt/user-data/outputs/ol-v1_1.html` **스타일 기준**: `스타일_구현_정책_및_수정_로드맵.md` + [shadcn/ui](https://ui.shadcn.com/) **작업 원칙**: 단일 HTML 자기완결 / 외부 의존 0 / 기존 함수·DOM ID 최대 보존 / 작은 단위 `str_replace` 누적 편집

---

## 0. 개발 전략 총론

### 0.1 전체 작업 흐름

요청 9개를 **의존 관계와 영향 범위**에 따라 7개의 작업 단위(Task)로 묶어 순차 진행합니다. 각 Task는 다음 4단계로 처리:

```
① 사전 분석 → ② 변경 지점 명시 → ③ 코드 패치 → ④ 검증 (node --check + 수동 점검)
```

### 0.2 의존 그래프

```
T0 (사전 점검·헬퍼 도입)
 ├─ T1: 컬러셋 확장 + 파스텔 교체 [요청 5]
 ├─ T2: 사이드바 — 컬럼 클릭 필터 + 태그 필터/검색 [요청 3, 4]
 │      └ 의존: 카드뷰 필터 로직(이미 selectedTags 존재)
 ├─ T3: 마크다운 개별 내보내기 [요청 1]
 │      └ 의존: 기존 export-md-btn 로직 확장
 ├─ T4: 마크다운 가져오기 (1개/다중) [요청 2]
 │      └ 의존: openMergeModal + executeMerge 재사용
 ├─ T5: 문서뷰 레이아웃 + TOC 스크롤 오프셋 [요청 6, 7]
 │      └ 의존: dv-layout / scroll-margin-top
 ├─ T6: 문서뷰 사이드바 — 칼럼>그룹>카드 트리 네비 [요청 8]
 │      └ 의존: T2의 사이드바 분기 로직 패턴
 └─ T7: 초기 랜딩페이지 + 로고 동작 변경 [요청 9]
        └ 의존: switchView('home') 추가, init 변경
```

### 0.3 호환성·데이터 안전 원칙

- `normalizeState`/`normalizeCard` 시그니처 보존. 새 필드는 **기본값으로 흡수**만 한다.
- 기존 사용자가 저장한 OL 파일(`ol_v1` localStorage)이 v1.1에서 깨지지 않도록, **신규 컬러 값은 기존 COL_COLORS 뒤에 추가**하지 말고(기존 카드의 `col.color`는 hex 그대로 유지되므로 안전), **별도 신규 팔레트 `COL_COLORS_PASTEL`로 교체**한다 (1번 정책 참조).
- `__STATIC_HTML__` 캡처 시점(JS 첫 줄)을 변경하지 않는다. 모든 신규 DOM은 init 이후 동적으로만 만든다.
- 모든 신규 HTML은 **이스케이프(`escapeHTML`)** 를 거친다.

### 0.4 스타일 적용 원칙 (shadcn 정합성)

|항목|규칙|
|---|---|
|색|`hsl(var(--foreground))` 등 토큰만 사용. 하드코딩 hex는 컬럼 컬러(`COL_COLORS_PASTEL`)에 한정|
|간격|`rem` 기반 (0.25/0.5/0.75/1/1.5/2…)|
|radius|`calc(var(--radius) - 4px)`, `calc(var(--radius) - 2px)`, `var(--radius)`|
|폰트|신규 폰트 도입 금지. 기존 시스템 폰트 스택 사용|
|아이콘|lucide 스타일 인라인 SVG (`stroke-width:2`, `viewBox 0 0 24 24`)|
|transition|`.15s` 또는 `.12s` 기본, easing 미지정|
|컴포넌트 매핑|트리 네비 → `Collapsible` 패턴 / 입력 → `Input` / 컬렉트 → `ToggleGroup`|

---

## Task 0 — 사전 점검 및 공용 헬퍼 도입

### 0.A 변경 위치

`'use strict';` 직후, `ORIGIN` 선언 다음, `COL_COLORS` 선언 **앞**.

### 0.B 추가할 헬퍼

```js
// ──── DOM 헬퍼 보강 ─────────────────────────────
// 1) 신규 SVG 아이콘 (T2/T6에서 사용)
const ICONS_X = {
  chevronRight: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 18 6-6-6-6"/></svg>',
  chevronDown:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>',
  search:       '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
  tag:          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" x2="7.01" y1="7" y2="7"/></svg>',
  fileText:     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
  home:         '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
};

// 2) 안전한 파일명 슬러그 (T3에서 사용)
//    한글/영문/숫자/하이픈/언더스코어만 남기고 공백 → '-'
function slugFilename(s, fallback) {
  const t = String(s || '').trim()
    .replace(/[\\/:*?"<>|]/g, '')   // OS 금지 문자
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .slice(0, 80);
  return t || (fallback || 'untitled');
}

// 3) JSZip 없이 다중 .md 다운로드: 순차 트리거
//    브라우저별 동작 차이 흡수를 위해 50ms 간격
function dlBlobSequential(items, doneCb) {
  let i = 0;
  function step() {
    if (i >= items.length) { if (doneCb) doneCb(); return; }
    dlBlob(items[i].blob, items[i].filename);
    i++; setTimeout(step, 80);
  }
  step();
}
```

### 0.C 검증

- `node --check` 통과
- 페이지 로딩 후 `console.log(ICONS_X)` 정상

---

## Task 1 — 컬럼 컬러 파스텔 교체 + 15색 확장 [요청 5]

### 1.A 정책

- 기존 10색 (어두운 단청·먹·황토 톤)은 v1.0 데이터 호환을 위해 **하드코딩된 hex로 카드 상태에 남을 수 있으므로 코드에서는 완전히 제거하되 런타임 상으로는 문제없음** (카드의 `col.color`는 hex로 저장되므로 화면 표시는 그대로 됨).
- 신규 팔레트: **shadcn-friendly 파스텔 15색** — 라이트/다크 모드 모두에서 자연스럽게 보이도록 채도 35~55%, 명도 75~85% 범위.
- 컬러피커 그리드: **5열 × 3행 = 15** (기존 5×2에서 행만 +1).

### 1.B 컬러 정의

```js
// COL_COLORS 변경 (기존 10색 → 신규 파스텔 15색)
const COL_COLORS = [
  // Row 1 — 따뜻한 톤
  '#fecaca', // soft red
  '#fed7aa', // soft orange
  '#fef3c7', // soft amber
  '#fef08a', // soft yellow
  '#d9f99d', // soft lime
  // Row 2 — 시원한 톤
  '#bbf7d0', // soft green
  '#a7f3d0', // soft emerald
  '#a5f3fc', // soft cyan
  '#bae6fd', // soft sky
  '#bfdbfe', // soft blue
  // Row 3 — 보라/뉴트럴
  '#c7d2fe', // soft indigo
  '#ddd6fe', // soft violet
  '#f5d0fe', // soft fuchsia
  '#fbcfe8', // soft pink
  '#e7e5e4', // soft stone (뉴트럴)
];
```

### 1.C CSS 패치

위치: `#cpicker.open` 블록 (라인 3587 근처)

```css
/* 변경 전 */
#cpicker.open {
  display: grid;
  grid-template-columns: repeat(5, 1.375rem);
  gap: 0.375rem;
}

/* 변경 후 */
#cpicker.open {
  display: grid;
  grid-template-columns: repeat(5, 1.5rem);
  grid-template-rows: repeat(3, 1.5rem);
  gap: 0.375rem;
  padding: 0.625rem;
}

/* 스와치 크기 살짝 키움 — 파스텔이라 시인성 보강 */
.cswatch {
  width: 1.5rem; height: 1.5rem;
  /* 파스텔이라 보더가 필요 */
  border: 1px solid hsl(var(--border));
}
.cswatch.sel {
  border-color: hsl(var(--foreground));
  box-shadow: 0 0 0 2px hsl(var(--background)), 0 0 0 3.5px hsl(var(--foreground));
}
```

> **다크모드 배려**: 파스텔은 다크모드에서 너무 밝게 보이므로 `.dark .cswatch { border-color: hsl(var(--border)); opacity: 0.92; }` 정도 추가 권장.

### 1.D JS 패치

`showCPicker` 내부의 `cols = 5` (라인 7057)는 **그대로 둠** (5열 유지). 변경 사항 없음 — 자동으로 15색이 3행으로 표시됨.

### 1.E 검증

- 칸반 컬럼 헤더 색 점 클릭 → 컬러피커가 5×3 그리드로 열림
- 15색 모두 선택 가능
- 다크모드 토글 후에도 가독성 OK
- 기존에 저장된 어두운 색 컬럼은 그대로 표시됨 (하위호환)

---

## Task 2 — 사이드바: 컬럼 클릭 필터 + 태그 필터/검색 [요청 3, 4]

### 2.A 정책

- **컬럼 항목**: 현재는 표시만 됨(`sb-col-row`). 클릭 시 → `switchView('cards')` + 카드뷰에서 **해당 컬럼 카드만 필터링**.
- **카드뷰 필터 모델 확장**:
    - 현재: `cg-fg` (그룹), `cg-fs` (상태), `selectedTags`
    - 추가: `selectedColId` (전역 변수, `null = 전체`)
- **태그 필터 강화**:
    - 사이드바에 **태그 섹션** 신설 (그룹 섹션 아래, About 위)
    - 태그명·카운트 표시, 클릭 시 다중 선택(`selectedTags`와 동기), 검색창 1개 추가

### 2.B 상태 변수 추가

`let selectedTags = new Set();` (라인 7665) **위쪽**에 추가:

```js
// ──── 카드뷰 필터: 컬럼 선택 (사이드바 연동) ────
let selectedColId = null;  // null = 전체 컬럼
let sbTagQuery = '';       // 사이드바 태그 검색 키워드
```

### 2.C `renderCards` 패치

라인 6139 (`let cards = [...S.cards];`) 직후:

```js
let cards = [...S.cards];
if (selectedColId != null) cards = cards.filter(c => c.colId === selectedColId);   // ← 추가
if (fg) cards = cards.filter(c=>c.group===fg);
// ... 이하 동일
```

`hasFilter` 판정에도 포함 (라인 6157 근처):

```js
const hasFilter = !!(fg || fs || selectedTags.size > 0 || selectedColId != null);
```

### 2.D `renderSidebar` 재작성

기존 라인 5585~5653을 다음과 같이 확장. **핵심 변경**:

```js
function renderSidebar() {
  const el = document.getElementById('sb-inner');
  el.innerHTML = '';

  // 📌 카드뷰 활성 컬럼 (필터 상태) 시각화
  const activeColId = (currentView === 'cards') ? selectedColId : null;

  // ── 1) 컬럼 현황 ── (클릭 가능하게 변경)
  const sec2 = ce('div','sb-section');
  sec2.appendChild(ce('div','sb-label','컬럼'));

  // "모든 컬럼" 항목 (카드뷰에서만 의미 있지만 항상 표시)
  const totalCardCnt = S.cards.length;
  const allColRow = ce('div', 'sb-col-row' + (activeColId === null && currentView === 'cards' ? ' active' : ''));
  allColRow.innerHTML = `
    <div class="sb-col-dot sb-col-dot-all"></div>
    <span class="sb-col-name">모든 컬럼</span>
    <span class="sb-col-cnt">${totalCardCnt}</span>
  `;
  allColRow.onclick = () => {
    selectedColId = null;
    switchView('cards');
  };
  sec2.appendChild(allColRow);

  // 개별 컬럼
  S.columns.forEach(col => {
    const row = ce('div', 'sb-col-row' + (activeColId === col.id ? ' active' : ''));
    const dot = ce('div','sb-col-dot'); dot.style.background = col.color;
    const nm  = ce('span','sb-col-name', col.title);
    const cnt = ce('span','sb-col-cnt', String(S.cards.filter(c=>c.colId===col.id).length));
    row.append(dot, nm, cnt);
    row.onclick = () => {
      selectedColId = col.id;
      // 그룹/상태 필터는 유지, 태그 필터도 유지 (사용자 의도 보존)
      switchView('cards');
    };
    sec2.appendChild(row);
  });
  el.appendChild(sec2);

  el.appendChild(ce('div','sb-divider'));

  // ── 2) 그룹 (기존 유지, 코드 동일) ──
  // ... 기존 로직 그대로 ...

  el.appendChild(ce('div','sb-divider'));

  // ── 3) 태그 섹션 (신규) ──
  const sec4 = ce('div','sb-section sb-tag-section');
  const tagHead = ce('div','sb-tag-head');
  tagHead.innerHTML = `
    <span class="sb-label" style="padding:0">태그</span>
    <span class="sb-tag-count" id="sb-tag-count"></span>
  `;
  sec4.appendChild(tagHead);

  // 검색 입력
  const tagSearchWrap = ce('div','sb-tag-search');
  tagSearchWrap.innerHTML = `
    <span class="sb-tag-search-icon">${ICONS_X.search}</span>
    <input type="text" class="sb-tag-search-input" id="sb-tag-search-input"
           placeholder="태그 검색…" value="${escapeHTML(sbTagQuery)}">
    ${sbTagQuery ? `<button class="sb-tag-search-clear" id="sb-tag-search-clear" aria-label="지우기">×</button>` : ''}
  `;
  sec4.appendChild(tagSearchWrap);

  // 태그 목록
  const tagListEl = ce('div','sb-tag-list');
  const tagMap = getAllTags();
  const allTags = Object.keys(tagMap).sort();
  const q = sbTagQuery.trim().toLowerCase();
  const filteredTags = q ? allTags.filter(t => t.toLowerCase().includes(q)) : allTags;

  if (!filteredTags.length) {
    tagListEl.innerHTML = `<div class="sb-tag-empty">${q ? '검색 결과 없음' : '태그 없음'}</div>`;
  } else {
    filteredTags.forEach(tag => {
      const item = ce('div','sb-tag-item' + (selectedTags.has(tag) ? ' selected' : ''));
      // 검색어 하이라이트
      const display = q ? highlightText(tag, q) : escapeHTML(tag);
      item.innerHTML = `
        <span class="sb-tag-mark">${selectedTags.has(tag) ? '✓' : ICONS_X.tag}</span>
        <span class="sb-tag-name">${display}</span>
        <span class="sb-tag-cnt">${tagMap[tag]}</span>
      `;
      item.onclick = () => {
        if (selectedTags.has(tag)) selectedTags.delete(tag);
        else selectedTags.add(tag);
        // 카드뷰 진입 + 필터 적용
        if (currentView !== 'cards') switchView('cards');
        else { renderCards(); updateTagFilterBtn(); renderSidebar(); }
      };
      tagListEl.appendChild(item);
    });
  }
  sec4.appendChild(tagListEl);

  // 선택된 태그 카운트 표시
  if (selectedTags.size > 0) {
    sec4.querySelector('#sb-tag-count').textContent = selectedTags.size + ' 선택됨';
    // "모두 해제" 버튼
    const clearAll = ce('button','sb-tag-clear-all','선택 해제');
    clearAll.onclick = () => {
      selectedTags.clear();
      renderSidebar();
      if (currentView === 'cards') { renderCards(); updateTagFilterBtn(); }
    };
    sec4.appendChild(clearAll);
  }
  el.appendChild(sec4);

  // 검색 입력 핸들러
  const tsi = document.getElementById('sb-tag-search-input');
  if (tsi) {
    tsi.addEventListener('input', e => {
      sbTagQuery = e.target.value;
      // 검색은 가벼우니 즉시 부분 재렌더 (전체 사이드바 재렌더는 포커스 손실)
      // → 태그 섹션만 다시 그리는 부분 함수 분리 권장
      const oldList = sec4.querySelector('.sb-tag-list');
      const oldEmpty= sec4.querySelector('.sb-tag-empty');
      // 간단화: 전체 사이드바 재렌더 후 포커스 복원
      renderSidebar();
      const nt = document.getElementById('sb-tag-search-input');
      if (nt) { nt.focus(); nt.setSelectionRange(nt.value.length, nt.value.length); }
    });
  }
  const tsc = document.getElementById('sb-tag-search-clear');
  if (tsc) tsc.onclick = () => { sbTagQuery = ''; renderSidebar(); };

  // ── 4) About 링크 (기존 유지) ──
  // ... 기존 코드 ...

  // ── 5) 푸터 메타 정보 (기존 유지) ──
}
```

### 2.E CSS 추가

`sb-tag-section` 관련 스타일을 사이드바 CSS 블록 끝(라인 1006 근처) 다음에:

```css
/* ── 사이드바: 컬럼 dot 'all' 변형 ── */
.sb-col-dot-all {
  background: transparent;
  border: 1.5px solid hsl(var(--muted-foreground));
}

/* ── 사이드바: 컬럼 row 클릭 가능 ── */
.sb-col-row { cursor: pointer; }
.sb-col-row.active {
  background: hsl(var(--secondary));
  color: hsl(var(--secondary-foreground));
  font-weight: 600;
}
.sb-col-row.active .sb-col-name {
  color: hsl(var(--foreground));
  font-weight: 600;
}

/* ── 사이드바: 태그 섹션 ── */
.sb-tag-section { padding-bottom: 0.75rem; }
.sb-tag-head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 0.5rem 0.75rem 0.375rem;
}
.sb-tag-count {
  font-size: 0.6875rem;
  color: hsl(var(--muted-foreground));
  font-weight: 500;
}

.sb-tag-search {
  position: relative;
  margin: 0 0.5rem 0.375rem;
}
.sb-tag-search-icon {
  position: absolute; left: 0.5rem; top: 50%;
  transform: translateY(-50%);
  width: 0.75rem; height: 0.75rem;
  color: hsl(var(--muted-foreground));
  display: inline-flex; pointer-events: none;
}
.sb-tag-search-icon svg { width: 100%; height: 100%; }
.sb-tag-search-input {
  width: 100%;
  height: 1.75rem;
  font: inherit; font-size: 0.75rem;
  padding: 0 1.75rem 0 1.875rem;
  background: hsl(var(--background));
  border: 1px solid hsl(var(--input));
  border-radius: calc(var(--radius) - 4px);
  color: hsl(var(--foreground));
  outline: none;
  transition: border-color .15s, box-shadow .15s;
}
.sb-tag-search-input::placeholder { color: hsl(var(--muted-foreground)); }
.sb-tag-search-input:focus-visible {
  border-color: hsl(var(--ring));
  box-shadow: 0 0 0 3px hsl(var(--ring) / 0.15);
}
.sb-tag-search-clear {
  position: absolute; right: 0.375rem; top: 50%;
  transform: translateY(-50%);
  width: 1rem; height: 1rem;
  display: inline-flex; align-items: center; justify-content: center;
  background: transparent; border: 0;
  color: hsl(var(--muted-foreground));
  font-size: 0.875rem;
  cursor: pointer; border-radius: 9999px;
}
.sb-tag-search-clear:hover {
  background: hsl(var(--accent));
  color: hsl(var(--foreground));
}

.sb-tag-list {
  display: flex; flex-direction: column;
  max-height: 16rem;
  overflow-y: auto;
  padding: 0 0.25rem;
  /* shadcn 스크롤바 */
  scrollbar-width: thin;
  scrollbar-color: hsl(var(--border)) transparent;
}
.sb-tag-list::-webkit-scrollbar { width: 4px; }
.sb-tag-list::-webkit-scrollbar-thumb { background: hsl(var(--border)); border-radius: 9999px; }

.sb-tag-item {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.3125rem 0.5rem;
  margin: 0 0.25rem;
  font-size: 0.75rem;
  color: hsl(var(--foreground));
  border-radius: calc(var(--radius) - 4px);
  cursor: pointer;
  transition: background-color .12s, color .12s;
  line-height: 1.4;
}
.sb-tag-item:hover {
  background: hsl(var(--accent));
}
.sb-tag-item.selected {
  background: hsl(var(--secondary));
  font-weight: 500;
}
.sb-tag-mark {
  display: inline-flex; align-items: center; justify-content: center;
  width: 0.875rem; height: 0.875rem;
  color: hsl(var(--muted-foreground));
  flex-shrink: 0;
}
.sb-tag-item.selected .sb-tag-mark {
  color: hsl(var(--primary));
  font-weight: 700;
}
.sb-tag-mark svg { width: 100%; height: 100%; }
.sb-tag-name {
  flex: 1; min-width: 0;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.sb-tag-name mark {
  background: hsl(var(--warning) / 0.2);
  color: inherit; padding: 0 0.0625rem; border-radius: 2px;
}
.sb-tag-cnt {
  font-size: 0.6875rem;
  color: hsl(var(--muted-foreground));
  flex-shrink: 0;
}

.sb-tag-empty {
  font-size: 0.75rem;
  color: hsl(var(--muted-foreground));
  text-align: center;
  padding: 1rem 0.5rem;
}

.sb-tag-clear-all {
  display: block;
  width: calc(100% - 1rem);
  margin: 0.375rem 0.5rem 0;
  padding: 0.3125rem;
  font: inherit; font-size: 0.6875rem;
  background: transparent;
  border: 1px solid hsl(var(--border));
  border-radius: calc(var(--radius) - 4px);
  color: hsl(var(--muted-foreground));
  cursor: pointer;
  transition: background-color .12s;
}
.sb-tag-clear-all:hover {
  background: hsl(var(--accent));
  color: hsl(var(--foreground));
}
```

### 2.F 컬럼 필터 리셋 처리

뷰 전환 시 동작:

- 카드뷰 진입 시 `selectedColId` 유지 (사용자가 일부러 사이드바에서 컬럼 선택했을 가능성)
- **다른 뷰 진입 시 초기화 X**: 사용자가 칸반/문서뷰로 갔다 와도 컬럼 필터 유지가 자연스러움
- 카드뷰 안에서 "+카드 추가"는 영향 없음

또한 카드뷰 toolbar에 **현재 컬럼 필터 표시 칩** 추가 권장 (선택 사항):

```html
<!-- view-bar 안, .vb-spacer 직전에 -->
<span class="cg-active-col-chip" id="cg-active-col-chip" style="display:none">
  <span class="cg-chip-dot"></span>
  <span class="cg-chip-name"></span>
  <button class="cg-chip-clear" title="필터 해제">×</button>
</span>
```

`renderCards` 시작부에서 chip 상태 갱신:

```js
const chipEl = document.getElementById('cg-active-col-chip');
if (chipEl) {
  if (selectedColId != null) {
    const col = S.columns.find(c => c.id === selectedColId);
    if (col) {
      chipEl.style.display = 'inline-flex';
      chipEl.querySelector('.cg-chip-dot').style.background = col.color;
      chipEl.querySelector('.cg-chip-name').textContent = col.title;
      chipEl.querySelector('.cg-chip-clear').onclick = () => {
        selectedColId = null;
        renderCards(); renderSidebar();
      };
    } else {
      chipEl.style.display = 'none';
    }
  } else {
    chipEl.style.display = 'none';
  }
}
```

### 2.G 검증

- [ ] 사이드바 컬럼 클릭 → 카드뷰로 전환되며 해당 컬럼만 표시
- [ ] "모든 컬럼" 클릭 → 필터 해제
- [ ] 사이드바 태그 클릭 → 카드뷰로 가며 태그 필터 적용
- [ ] 태그 검색창에 입력 시 즉시 필터링 (포커스 유지)
- [ ] 태그 다중 선택 가능
- [ ] 기존 헤더의 태그 필터 버튼과 사이드바 태그가 **동일한 `selectedTags` 상태 공유**

---

## Task 3 — 개별 마크다운 내보내기 [요청 1]

### 3.A 정책

- **단일 카드 내보내기**: 카드 모달 안에 "마크다운으로 내보내기" 액션 추가
- **선택 카드 일괄 내보내기**: 카드뷰 bulk-actions-bar의 우측에 "MD 내보내기(N개)" 액션 추가
- **전체 카드 개별 파일 내보내기**: 헤더 "저장" 드롭다운에 새 메뉴 "각 카드를 개별 .md로 내보내기" 추가 (기존 단일파일 export-md-btn은 유지)
- **파일명 규칙**: `{slugFilename(card.title)}.md`, 중복 시 `-2`, `-3` 접미 (Map 카운터)
- **프런트매터 형식**: 기존 export-md-btn과 동일 (column/group/priority/learnStatus/tags/created)

### 3.B 공용 변환 함수 신설

`safeFname()` 함수 (라인 7124) 다음에:

```js
// 카드 한 장 → 마크다운 텍스트 (프런트매터 + 본문)
function cardToMarkdownText(card) {
  const colMap = {};
  (S.columns || []).forEach(col => { colMap[col.id] = col.title; });
  const colName     = colMap[card.colId] || '';
  const learnStatus = S.userData.status[card.id] || 'wait';
  const priority    = VALID_PRIORITIES.includes(card.priority) ? card.priority : 'mid';
  const fm = [
    '---',
    'title: '       + JSON.stringify(card.title || ''),
    'column: '      + JSON.stringify(colName),
    'group: '       + JSON.stringify(card.group || ''),
    'priority: '    + priority,
    'learnStatus: ' + learnStatus,
    'tags: ['       + (card.tags || []).map(t => JSON.stringify(t)).join(', ') + ']',
    'created: '     + (card.created || ''),
    '---',
  ].join('\n');
  return fm + '\n\n' + (card.body || '');
}

// 카드 리스트 → 개별 .md 파일들 (파일명 중복 방지 포함)
function exportCardsAsIndividualMd(cards) {
  if (!cards || !cards.length) {
    toast('내보낼 카드가 없습니다');
    return;
  }
  const used = new Map();   // baseName → count
  const items = cards.map(card => {
    const base = slugFilename(card.title, 'card-' + card.id);
    const n = (used.get(base) || 0) + 1;
    used.set(base, n);
    const filename = (n > 1 ? `${base}-${n}.md` : `${base}.md`);
    return {
      filename,
      blob: new Blob([cardToMarkdownText(card)], { type: 'text/markdown; charset=utf-8' }),
    };
  });
  dlBlobSequential(items, () => {
    toast(`${items.length}개 마크다운 파일을 내보냈습니다`, 'success');
  });
}
```

### 3.C 헤더 메뉴 항목 추가

라인 3886~3890 (export-md-btn 직후) 마크다운 항목을 다음과 같이 **2개로 분리**:

```html
<!-- 기존 (유지) -->
<button class="h-dropdown-item" id="export-md-btn" role="menuitem">
  <svg class="icon" ...></svg>
  마크다운으로 내보내기 (단일 파일)
</button>
<!-- 신규 -->
<button class="h-dropdown-item" id="export-md-each-btn" role="menuitem">
  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
    <polyline points="14 2 14 8 20 8"/>
    <line x1="9" x2="15" y1="13" y2="13"/>
    <line x1="9" x2="15" y1="17" y2="17"/>
  </svg>
  각 카드를 개별 .md로 내보내기
</button>
```

핸들러:

```js
document.getElementById('export-md-each-btn').addEventListener('click', () => {
  closeAllDropdowns();
  exportCardsAsIndividualMd(S.cards || []);
});
```

### 3.D 카드 모달에 단일 내보내기 액션 추가

`openCardModal`이 모달을 띄울 때 footer 영역에 "MD로 저장" 버튼이 있는지 확인 후, 없으면 추가. (현재 코드에서는 모달 footer에 저장/삭제 버튼만 있을 가능성)

**확인 필요 지점**: 라인 6883 근처 `openCardModal`. modal 내부의 footer DOM에 `id="card-modal-md-btn"` 버튼 추가:

```html
<!-- modal footer 안 -->
<button class="btn sm" id="card-modal-md-btn" title="이 카드만 마크다운 파일로 내보내기">
  <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
  .md
</button>
```

핸들러 (openCardModal 내부, 다른 버튼 핸들러 등록 영역):

```js
const mdBtn = document.getElementById('card-modal-md-btn');
if (mdBtn) {
  mdBtn.onclick = () => {
    // 현재 모달 입력값을 임시 카드로 만들어 내보내기 (저장하지 않은 변경도 반영)
    const tempCard = {
      ...card,
      title: document.getElementById('cm-title').value || card.title,
      body:  document.getElementById('cm-body').value  || card.body,
      group: document.getElementById('cm-group').value || card.group,
      // 태그·우선순위·colId 등은 card 그대로 사용 (간단화)
    };
    const filename = slugFilename(tempCard.title, 'card-' + (card.id||'new')) + '.md';
    dlBlob(
      new Blob([cardToMarkdownText(tempCard)], { type: 'text/markdown; charset=utf-8' }),
      filename
    );
    toast('마크다운 파일을 내보냈습니다', 'success');
  };
}
```

> **주의**: 모달 내부 input ID(`cm-title`, `cm-body`, `cm-group`)는 실제 코드 확인 후 보정. 일치하지 않으면 단순히 `card` 객체만 사용.

### 3.E 카드뷰 bulk-actions에 추가

라인 4109 (`bulk-sep` 다음, 삭제 버튼 직전):

```html
<button class="bulk-action-btn" id="cg-bulk-md">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
  MD 내보내기
</button>
```

`initBulkBar('cg')` 부분에 핸들러:

```js
const mdBulkBtn = document.getElementById('cg-bulk-md');
if (mdBulkBtn) {
  mdBulkBtn.onclick = () => {
    const ids = [...cgSelected];
    const cards = S.cards.filter(c => ids.includes(c.id));
    exportCardsAsIndividualMd(cards);
  };
}
```

리스트 뷰도 동일 패턴(`lv-bulk-md`) 적용.

### 3.F 검증

- [ ] 카드 모달 → ".md" 버튼 → 한 파일 다운로드
- [ ] 카드뷰에서 카드 선택 → bulk 액션 → 선택분만 개별 파일 다운로드
- [ ] 헤더 저장 메뉴 → "각 카드를 개별 .md로" → 전체 카드 개별 파일
- [ ] 동일 제목 카드 2개 → 두 번째 파일명에 `-2` 접미
- [ ] 한글 제목 정상 인코딩 (`encodeURIComponent` 처리 — `dlBlob` 점검 필요)

---

## Task 4 — 마크다운 파일 가져오기 (1개/다중) [요청 2]

### 4.A 정책

- **단일/다중 파일 동시 처리**: `<input type="file" multiple accept=".md,.markdown,text/markdown">` 활용
- **각 파일** = 카드 1장 (프런트매터 있으면 메타 추출, 없으면 본문만 + 파일명을 제목으로)
- 기존 **병합 모달(`openMergeModal`)** 재사용. 여러 파일을 카드 배열로 변환한 후 한꺼번에 모달로 전달
- **프런트매터 파싱**:
    - `---` 으로 둘러싸인 YAML-ish 블록 (안전한 최소 파서)
    - 지원 키: `title, column, group, priority, learnStatus, tags, created`
    - 없으면 기본값 채움

### 4.B 헤더 메뉴 항목 추가

라인 3909 (`import-json-btn` 다음, dropdown 닫기 전):

```html
<button class="h-dropdown-item" id="import-md-btn" role="menuitem">
  <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" x2="12" y1="3" y2="15"/></svg>
  마크다운 파일 가져오기 (.md)
</button>
```

hidden input 추가 (라인 3915 다음):

```html
<input type="file" id="import-md-file" accept=".md,.markdown,text/markdown" multiple style="display:none">
```

### 4.C 프런트매터 파서

`detectDuplicates` 함수 직전(라인 7314 근처)에 추가:

```js
// 안전한 미니 YAML 파서 — 한 줄 단위, 깊은 구조는 미지원
// 지원: key: "값" / key: 값 / key: [item, "item2"]
function parseFrontmatterLine(line) {
  const m = line.match(/^([A-Za-z][A-Za-z0-9_-]*)\s*:\s*(.*)$/);
  if (!m) return null;
  const key = m[1];
  let raw   = m[2].trim();
  // 배열
  if (raw.startsWith('[') && raw.endsWith(']')) {
    const inner = raw.slice(1, -1).trim();
    if (!inner) return { key, val: [] };
    // 매우 단순화: 쉼표 분리, 각각 JSON.parse 시도 (실패 시 trim 문자열)
    const parts = [];
    let buf = '', inStr = false, esc = false;
    for (const ch of inner) {
      if (esc) { buf += ch; esc = false; continue; }
      if (ch === '\\') { esc = true; buf += ch; continue; }
      if (ch === '"') { inStr = !inStr; buf += ch; continue; }
      if (ch === ',' && !inStr) {
        parts.push(buf.trim()); buf = ''; continue;
      }
      buf += ch;
    }
    if (buf.trim()) parts.push(buf.trim());
    return { key, val: parts.map(p => {
      try { return JSON.parse(p); } catch { return p.replace(/^["']|["']$/g, ''); }
    }) };
  }
  // 문자열/숫자/불리언
  try { return { key, val: JSON.parse(raw) }; }
  catch { return { key, val: raw.replace(/^["']|["']$/g, '') }; }
}

function parseMarkdownFile(text, fallbackTitle) {
  let title = fallbackTitle || '';
  let column = '', group = '', priority = 'mid', learnStatus = 'wait';
  let tags = [], created = today();
  let body = text;

  // 프런트매터 검출: 첫 줄이 '---' 이고, 그 다음 '---'까지
  const fmRe = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/;
  const m = text.match(fmRe);
  if (m) {
    const lines = m[1].split(/\r?\n/);
    lines.forEach(line => {
      const kv = parseFrontmatterLine(line);
      if (!kv) return;
      switch (kv.key) {
        case 'title':       title = String(kv.val); break;
        case 'column':      column = String(kv.val); break;
        case 'group':       group = String(kv.val); break;
        case 'priority':    if (VALID_PRIORITIES.includes(kv.val)) priority = kv.val; break;
        case 'learnStatus': if (['wait','doing','done'].includes(kv.val)) learnStatus = kv.val; break;
        case 'tags':        if (Array.isArray(kv.val)) tags = kv.val.map(String); break;
        case 'created':     created = String(kv.val); break;
      }
    });
    body = text.slice(m[0].length);
  } else {
    // 프런트매터 없음: 본문 첫 # 헤딩을 제목으로 추정
    const headingMatch = text.match(/^\s*#\s+(.+?)\s*$/m);
    if (headingMatch && !title) title = headingMatch[1].trim();
  }

  // 본문 정리 (앞쪽 빈 줄 제거)
  body = body.replace(/^\s*\n+/, '');

  return {
    title:       title || fallbackTitle || '제목 없음',
    column,
    group,
    priority,
    learnStatus,
    tags,
    created,
    body,
  };
}
```

### 4.D import 핸들러

```js
// ── 5. 마크다운 파일 가져오기 (.md, 다중) ────
document.getElementById('import-md-btn').addEventListener('click', () => {
  closeAllDropdowns();
  document.getElementById('import-md-file').click();
});

document.getElementById('import-md-file').addEventListener('change', async e => {
  const files = Array.from(e.target.files || []);
  e.target.value = '';
  if (!files.length) return;

  const cards = [];
  let errCnt = 0;

  // 파일들을 순차 읽기 (대용량 대비, Promise.all로 동시 처리도 OK)
  for (const file of files) {
    try {
      const text = await file.text();
      // 파일명에서 확장자 제거 → fallback 제목
      const fallbackTitle = file.name.replace(/\.(md|markdown)$/i, '');
      const card = parseMarkdownFile(text, fallbackTitle);
      cards.push(card);
    } catch (err) {
      errCnt++;
    }
  }

  if (!cards.length) {
    toast('읽을 수 있는 마크다운 파일이 없습니다', 'error');
    return;
  }

  if (errCnt > 0) toast(`${errCnt}개 파일을 읽지 못했습니다`, 'warning');

  // 기존 병합 모달로 위임 (중복 감지·전략 선택 UI 재사용)
  openMergeModal(cards, 'markdown');
});
```

### 4.E `executeMerge` 호환성 점검

`executeMerge`의 `makeCard`는 이미 다음을 흡수합니다:

- `card.title, card.body, card.group, card.tags, card.priority, card.created`
- `card.learnStatus` (별도 처리됨)
- `card.column` → `colId` 매핑

→ **그대로 호환됨**. 추가 변경 불필요.

### 4.F 검증

- [ ] 헤더 "파일 열기" → "마크다운 파일 가져오기" → 다중 파일 선택 가능
- [ ] 프런트매터 있는 파일: 메타 정확히 적용
- [ ] 프런트매터 없는 파일: 파일명이 제목, 본문 첫 # 있으면 그것이 제목
- [ ] 신규 컬럼명이면 자동 생성
- [ ] 중복 카드는 병합 모달에서 전략 선택 가능
- [ ] 한글 파일명 정상 처리

---

## Task 5 — 문서뷰 레이아웃 + TOC 스크롤 오프셋 [요청 6, 7]

### 5.A 정책

**현재 상태 분석**:

- `.dv-wrap`: `max-width: 58rem` (≈ 928px), `padding: 2.25rem 3.5rem 4rem`
- `.dv-toc`: `flex: 0 0 14rem` (224px 고정)
- `.dv-layout`: 그냥 flex, max-width 미설정 → 화면 폭에 따라 본문이 좌측으로 쏠림
- 브라우저 1920px 이상 시 우측 공간 과다

**개선안 (요청 6)**:

- `.dv-layout` 자체에 **max-width를 두지 않고**, 본문(`.dv-wrap`)의 max-width를 살리되 layout 자체를 **중앙 정렬**
- 본문 max-width를 살짝 키움: `58rem` → `64rem` (≈ 1024px, 가독성 한계)
- 1280px 이상에서 본문 + TOC가 **컨테이너 중앙에 묶여 정렬**되도록

**개선안 (요청 7)**:

- 헤더(56px) + view-bar(약 53px) = **약 109px** 영역이 문서를 가림
- 스크롤 시 헤딩이 상단에 닿을 때 가려지지 않도록 **`scroll-margin-top` 적용** (CSS only, 자바스크립트 변경 X)
- `IntersectionObserver`의 `rootMargin: '-80px 0px -55% 0px'` 도 헤더+뷰바를 정확히 반영하도록 `-120px`로 보정

### 5.B CSS 패치

라인 1718~1729 (`.dv-wrap`, `.dv-layout > .dv-wrap`):

```css
/* 변경 후 */
.dv-wrap {
  padding: 2.25rem 3rem 4rem;
  max-width: 64rem;             /* 58rem → 64rem */
  margin: 0 auto;
}

.dv-layout > .dv-wrap {
  margin: 0;
  padding-right: 1.5rem;
  padding-left: 3rem;           /* 컨테이너 중앙 정렬 보강 */
}
```

라인 1618~1629 (`.dv-layout`, `.dv-layout .dv-wrap`):

```css
.dv-layout {
  display: flex;
  align-items: flex-start;
  gap: 0;
  position: relative;
  /* 큰 화면 대응: 본문 + TOC 묶음을 컨테이너 중앙으로 */
  max-width: 88rem;              /* 본문(64rem) + TOC(14rem) + gap/padding 여유 */
  margin: 0 auto;
}

.dv-layout .dv-wrap {
  flex: 1;
  min-width: 0;
  max-width: 64rem;              /* layout 안에서도 본문폭 제한 */
}
```

`.dv-toc` (라인 1632~1642):

```css
.dv-toc {
  flex: 0 0 14rem;
  position: sticky;
  /* 헤더 + view-bar 높이 분만큼 아래로 */
  top: calc(var(--header-h) + 3.5rem);   /* 기존 1.5rem → 3.5rem */
  max-height: calc(100vh - var(--header-h) - 5rem);
  overflow-y: auto;
  padding: 1.25rem 0 1rem 1.5rem;
  scrollbar-width: thin;
  scrollbar-color: hsl(var(--border)) transparent;
}
```

미디어 쿼리 보정 (라인 1700~1709):

```css
@media (max-width: 1279px) and (min-width: 1024px) {
  .dv-toc { flex: 0 0 11rem; }
  .dv-toc-item { font-size: 0.75rem; }
  .dv-layout > .dv-wrap { padding-left: 2rem; }
}

@media (max-width: 1023px) {
  .dv-toc { display: none !important; }
  .dv-layout {
    max-width: 64rem;
    margin: 0 auto;
  }
  .dv-layout .dv-wrap { max-width: 64rem; margin: 0 auto; padding-left: 2rem; padding-right: 2rem; }
}
```

### 5.C TOC 스크롤 오프셋 (요청 7)

**핵심**: `scrollIntoView({ block: 'start' })`가 헤더+view-bar에 가려지는 문제.

**해결 방법 — CSS-only**: 각 헤딩에 `scroll-margin-top` 적용.

마크다운 렌더 결과 헤딩(`md-h1, md-h2, md-h3` 등)에 적용. CSS 추가:

```css
/* 문서뷰 본문의 헤딩 — 스크롤 시 상단 고정 영역만큼 여백 확보 */
.dv-body .md-h1[id],
.dv-body .md-h2[id],
.dv-body .md-h3[id],
.dv-body .md-h4[id],
.dv-body .md-h5[id],
.dv-body .md-h6[id] {
  scroll-margin-top: calc(var(--header-h) + 4rem);  /* 헤더(56) + view-bar(53) + 여유 */
}
```

추가로 `IntersectionObserver`의 `rootMargin` 보정 — `setupTocObserver` 내 라인 5029:

```js
// 변경 전
rootMargin: '-80px 0px -55% 0px',

// 변경 후 — 헤더 + view-bar 합산 + 여유
rootMargin: '-120px 0px -55% 0px',
```

### 5.D 검증

- [ ] 1920px 화면: 본문이 좌측에 쏠리지 않고 중앙 정렬됨
- [ ] 1024~1280px: TOC가 줄어들지만 본문 정상
- [ ] 1023px 이하: TOC 숨김, 본문 중앙
- [ ] 목차 H2 클릭 → 해당 헤딩이 view-bar 바로 아래에 정확히 위치 (가려지지 않음)
- [ ] 자연스러운 스크롤 (smooth)에서도 동일

---

## Task 6 — 문서뷰 사이드바: 칼럼>그룹>카드 트리 네비 [요청 8]

### 6.A 정책

- **문서뷰**일 때만 표시되는 사이드바 분기
- 다른 뷰일 때 사이드바: 기존 컬럼/그룹/태그 (T2 기준)
- 문서뷰 사이드바: **컬럼 > 그룹 > 카드(제목)** 3단 트리. shadcn `Collapsible` 패턴
- 현재 보고 있는 카드를 **active**로 표시 (스크롤 자동 정렬)
- 클릭 시 `goToDocCard(cardId)` 호출

### 6.B `renderSidebar`에 분기 추가

`renderSidebar` 함수 최상단에:

```js
function renderSidebar() {
  const el = document.getElementById('sb-inner');
  el.innerHTML = '';

  // ✦ 문서뷰 전용 트리 사이드바
  if (currentView === 'document') {
    renderSidebarForDocView(el);
    // 푸터 메타 정보는 공통으로
    el.appendChild(ce('div','sb-divider'));
    const meta = ce('div','sb-meta');
    meta.innerHTML = `
      <span class="sb-meta-line"><strong style="color:hsl(var(--foreground));font-weight:500">${escapeHTML(S.meta.title)}</strong></span>
      <span class="sb-meta-line">v${escapeHTML(S.meta.version)}</span>
    `;
    el.appendChild(meta);
    return;
  }
  // ... (이하 기존 코드)
}
```

### 6.C 신규 함수 `renderSidebarForDocView`

`renderSidebar` 함수 바로 다음에:

```js
// 문서뷰 전용 사이드바: 컬럼 > 그룹 > 카드 트리
function renderSidebarForDocView(rootEl) {
  const sec = ce('div','sb-section');
  sec.appendChild(ce('div','sb-label','문서 목록'));

  if (!S.cards.length) {
    const empty = ce('div','sb-doc-tree-empty','카드가 없습니다');
    sec.appendChild(empty);
    rootEl.appendChild(sec);
    return;
  }

  // 컬럼 정렬 순서 그대로
  S.columns.forEach(col => {
    const cardsInCol = S.cards.filter(c => c.colId === col.id);
    if (!cardsInCol.length) return;  // 빈 컬럼 스킵

    // 그룹별 분할
    const byGroup = {};
    const NO_GROUP = '__no_group__';
    cardsInCol.forEach(c => {
      const g = c.group || NO_GROUP;
      if (!byGroup[g]) byGroup[g] = [];
      byGroup[g].push(c);
    });
    const groupNames = Object.keys(byGroup);

    // 컬럼 노드
    const colNode = ce('div','sb-tree-col');
    const colHead = ce('div','sb-tree-col-head');
    // 펼침 상태 (sessionStorage 등에 저장 안 함, 매 렌더마다 기본 펼침)
    const colKey = 'col_' + col.id;
    const expanded = sbDocExpanded[colKey] !== false;  // 기본 펼침
    colHead.innerHTML = `
      <button class="sb-tree-chevron" aria-expanded="${expanded}">${expanded ? ICONS_X.chevronDown : ICONS_X.chevronRight}</button>
      <span class="sb-tree-col-dot" style="background:${col.color}"></span>
      <span class="sb-tree-col-name">${escapeHTML(col.title)}</span>
      <span class="sb-tree-col-cnt">${cardsInCol.length}</span>
    `;
    colNode.appendChild(colHead);

    const colBody = ce('div','sb-tree-col-body');
    if (!expanded) colBody.style.display = 'none';

    groupNames.forEach(gn => {
      const groupCards = byGroup[gn];
      const isNoGroup  = gn === NO_GROUP;

      if (groupNames.length === 1 && isNoGroup) {
        // 그룹이 사실상 없으면 카드를 컬럼 바로 아래에 평면 표시
        groupCards.forEach(card => colBody.appendChild(buildDocTreeCard(card)));
        return;
      }

      const gNode = ce('div','sb-tree-grp');
      const gKey  = 'grp_' + col.id + '_' + gn;
      const gExpanded = sbDocExpanded[gKey] !== false;
      const gHead = ce('div','sb-tree-grp-head');
      gHead.innerHTML = `
        <button class="sb-tree-chevron sb-tree-chevron-sm" aria-expanded="${gExpanded}">${gExpanded ? ICONS_X.chevronDown : ICONS_X.chevronRight}</button>
        <span class="sb-tree-grp-name">${isNoGroup ? '(그룹 없음)' : escapeHTML(gn)}</span>
        <span class="sb-tree-grp-cnt">${groupCards.length}</span>
      `;
      gNode.appendChild(gHead);

      const gBody = ce('div','sb-tree-grp-body');
      if (!gExpanded) gBody.style.display = 'none';
      groupCards.forEach(card => gBody.appendChild(buildDocTreeCard(card)));
      gNode.appendChild(gBody);

      gHead.onclick = () => {
        sbDocExpanded[gKey] = !gExpanded;
        renderSidebar();
      };
      colBody.appendChild(gNode);
    });

    colNode.appendChild(colBody);
    colHead.onclick = () => {
      sbDocExpanded[colKey] = !expanded;
      renderSidebar();
    };
    sec.appendChild(colNode);
  });

  rootEl.appendChild(sec);

  // 활성 카드를 뷰포트에 보이도록
  requestAnimationFrame(() => {
    const active = rootEl.querySelector('.sb-tree-card.active');
    if (active) active.scrollIntoView({ block: 'nearest' });
  });
}

function buildDocTreeCard(card) {
  const item = ce('div', 'sb-tree-card' + (card.id === currentDocCardId ? ' active' : ''));
  item.innerHTML = `
    <span class="sb-tree-card-bullet"></span>
    <span class="sb-tree-card-title">${escapeHTML(card.title || '(제목 없음)')}</span>
  `;
  item.onclick = () => {
    if (currentView !== 'document') switchView('document');
    goToDocCard(card.id);
  };
  return item;
}

// 펼침 상태 보관 (메모리 only)
const sbDocExpanded = {};
```

### 6.D CSS 추가

사이드바 CSS 블록 끝(`sb-tag-clear-all` 다음)에:

```css
/* ══════════════════════════════════════════
   사이드바: 문서뷰 트리 네비
══════════════════════════════════════════ */
.sb-doc-tree-empty {
  font-size: 0.75rem;
  color: hsl(var(--muted-foreground));
  text-align: center;
  padding: 1rem 0.5rem;
}

.sb-tree-col {
  margin: 0 0.25rem;
}
.sb-tree-col-head {
  display: flex; align-items: center; gap: 0.375rem;
  padding: 0.375rem 0.5rem 0.375rem 0.25rem;
  font-size: 0.8125rem;
  font-weight: 500;
  color: hsl(var(--foreground));
  border-radius: calc(var(--radius) - 4px);
  cursor: pointer;
  transition: background-color .12s;
  user-select: none;
}
.sb-tree-col-head:hover { background: hsl(var(--accent)); }
.sb-tree-col-dot {
  width: 0.5rem; height: 0.5rem;
  border-radius: 50%;
  flex-shrink: 0;
}
.sb-tree-col-name { flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sb-tree-col-cnt {
  font-size: 0.6875rem;
  color: hsl(var(--muted-foreground));
}

.sb-tree-chevron {
  display: inline-flex; align-items: center; justify-content: center;
  width: 1rem; height: 1rem;
  background: transparent; border: 0;
  color: hsl(var(--muted-foreground));
  cursor: pointer;
  flex-shrink: 0;
  padding: 0;
}
.sb-tree-chevron svg { width: 0.75rem; height: 0.75rem; }
.sb-tree-chevron-sm svg { width: 0.625rem; height: 0.625rem; }
.sb-tree-chevron:hover { color: hsl(var(--foreground)); }

.sb-tree-col-body {
  padding-left: 0.5rem;
  margin-top: 0.0625rem;
}

.sb-tree-grp-head {
  display: flex; align-items: center; gap: 0.375rem;
  padding: 0.25rem 0.5rem 0.25rem 0.625rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: hsl(var(--muted-foreground));
  border-radius: calc(var(--radius) - 4px);
  cursor: pointer;
  transition: background-color .12s, color .12s;
  user-select: none;
}
.sb-tree-grp-head:hover {
  background: hsl(var(--accent));
  color: hsl(var(--foreground));
}
.sb-tree-grp-name { flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sb-tree-grp-cnt {
  font-size: 0.6875rem;
}

.sb-tree-grp-body {
  padding-left: 0.625rem;
}

.sb-tree-card {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.3125rem 0.5rem 0.3125rem 1.125rem;
  margin: 0.0625rem 0;
  font-size: 0.75rem;
  color: hsl(var(--foreground));
  border-radius: calc(var(--radius) - 4px);
  cursor: pointer;
  transition: background-color .12s, color .12s;
  position: relative;
}
.sb-tree-card:hover {
  background: hsl(var(--accent));
}
.sb-tree-card.active {
  background: hsl(var(--secondary));
  color: hsl(var(--foreground));
  font-weight: 600;
}
.sb-tree-card.active::before {
  content: '';
  position: absolute;
  left: 0.5rem; top: 50%;
  width: 2px; height: 1rem;
  transform: translateY(-50%);
  background: hsl(var(--primary));
  border-radius: 1px;
}
.sb-tree-card-bullet {
  display: none;  /* 활성 표시에 ::before 사용 */
}
.sb-tree-card-title {
  flex: 1; min-width: 0;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
```

### 6.E `goToDocCard` 사이드바 갱신 연동

라인 5183 근처 `openDocCard` 또는 `goToDocCard` 함수 끝에 `renderSidebar();` 호출 추가:

```js
function goToDocCard(cardId) {
  // ... 기존 로직 ...
  currentDocCardId = cardId;
  renderDocumentView();
  renderSidebar();  // ← 추가: 활성 카드 시각화 갱신
}
```

### 6.F 검증

- [ ] 문서뷰 진입 → 사이드바가 트리로 바뀜
- [ ] 컬럼명 클릭 → 펼침/접힘 토글
- [ ] 그룹 펼침/접힘 토글
- [ ] 카드 제목 클릭 → 해당 카드로 이동
- [ ] 현재 카드 active 표시, 트리 안에서 자동 스크롤
- [ ] 다른 뷰로 가면 기존 사이드바로 돌아옴

---

## Task 7 — 초기 랜딩페이지 + 로고 동작 [요청 9]

### 7.A 정책

- **새 뷰 `home`** 추가
- `init()`에서 최초 진입 시 (저장 데이터 유무와 무관하게) **첫 화면 = home**
    - 단, **포크된 파일에 데이터가 들어 있는 경우** 사용자가 받은 파일은 이미 콘텐츠가 채워져 있는 게 일반적 → 랜딩으로 가는 게 자연스럽지 않을 수 있음
    - 절충안: **localStorage에 `ol_seen_home` 플래그**가 없으면 home, 있으면 기존대로 kanban. 또는 **항상 home부터 시작** + 사용자가 한번 다른 뷰로 가면 그 뷰가 마지막 뷰로 기억됨 (lastView)
    - **권장: localStorage에 `ol_last_view`를 저장, 있으면 그것으로 시작, 없으면 home**
- **로고 클릭 동작**: 현재는 `onclick="switchView('kanban')"`. 변경 → `switchView('home')`
- **홈 컨텐츠**:
    1. 히어로 영역: "OL · Weaving the Wisdom" 타이틀 + 한 줄 설명
    2. ol-core 기본 기능 소개 (4~6개 카드)
    3. **올확장 프로젝트** 소개 섹션 — 외부 사이트로 가는 카드들 (붓다스토리, 중관학 번역 등). 이 데이터는 `ORIGIN` 옆에 새 상수 `OL_PROJECTS`로 하드코딩

### 7.B HTML 추가

라인 4192 (`view-about` 다음, `#main` 닫기 전):

```html
<!-- ⑥ Home (Landing) -->
<div class="view" id="view-home">
  <div class="view-bar">
    <span class="view-bar-title">홈</span>
    <div class="vb-spacer"></div>
    <button class="btn pri sm" id="home-start-btn">바로 시작</button>
  </div>
  <div class="home-wrap" id="home-inner"></div>
</div>
```

### 7.C `OL_PROJECTS` 상수 추가

`ORIGIN` 선언 다음(라인 4429 근처):

```js
// ──── 올확장 프로젝트 카탈로그 ─────────────
//      홈 화면 하단 "올확장" 섹션에 표시
const OL_PROJECTS = Object.freeze([
  {
    name: '붓다스토리',
    desc: '붓다의 생애를 단행본 형식으로 엮은 OL 콘텐츠 파일',
    url: 'https://borido.org/buddhastory',
    tag: '콘텐츠',
  },
  {
    name: '중관학 번역 모음',
    desc: '나가르주나 · 짠드라끼르띠 등 중관학 핵심 논서 한글 번역',
    url: 'https://borido.org/madhyamaka',
    tag: '콘텐츠',
  },
  {
    name: '경전 모음 (OL 형식)',
    desc: '대승·초기 경전을 OL 카드로 정리한 학습 자료',
    url: 'https://borido.org/sutras',
    tag: '콘텐츠',
  },
  // 추후 확장 가능
]);
```

> **주의**: 실제 URL은 사용자 확인 필요. 임시 placeholder로 두고 비움(`#`) 가능.

### 7.D `renderHome` 함수 신설

`renderAbout` 함수(라인 5474) 다음에:

```js
function renderHome() {
  const wrap = document.getElementById('home-inner');
  wrap.innerHTML = '';

  // ─── HERO ───────────────────────────────
  const hero = ce('section','home-hero');
  hero.innerHTML = `
    <div class="home-hero-eyebrow">${escapeHTML(ORIGIN.tool)}</div>
    <h1 class="home-hero-title">단일 HTML 파일로 작동하는<br>지식 정리 도구</h1>
    <p class="home-hero-sub">
      다운로드만 하면 어디서든 사용할 수 있습니다. 카드로 정리하고, 마크다운으로 작성하고,
      파일 하나로 공유합니다.
    </p>
    <div class="home-hero-actions">
      <button class="btn pri" id="home-hero-start">칸반 보드로 시작</button>
      <button class="btn" id="home-hero-doc">문서뷰로 보기</button>
    </div>
  `;
  wrap.appendChild(hero);

  // ─── ol-core 기능 ──────────────────────
  const features = [
    {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="18" x="3" y="3" rx="1"/><rect width="7" height="18" x="14" y="3" rx="1"/></svg>',
      title: '칸반 보드',
      desc:  '컬럼 단위로 카드의 흐름을 관리합니다. 드래그앤드롭 지원.'
    },
    {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>',
      title: '카드 뷰',
      desc:  '같은 데이터를 그리드로 한눈에 보고, 태그·그룹·상태로 필터링합니다.'
    },
    {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" x2="21" y1="6" y2="6"/><line x1="8" x2="21" y1="12" y2="12"/><line x1="8" x2="21" y1="18" y2="18"/><line x1="3" x2="3.01" y1="6" y2="6"/><line x1="3" x2="3.01" y1="12" y2="12"/><line x1="3" x2="3.01" y1="18" y2="18"/></svg>',
      title: '리스트 뷰',
      desc:  '정렬·일괄 작업·인쇄에 최적화된 테이블 형식.'
    },
    {
      icon: ICONS_X.fileText,
      title: '문서뷰',
      desc:  '마크다운 본문을 책처럼 읽고, 목차를 따라 자유롭게 이동합니다.'
    },
    {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>',
      title: '내보내기 / 가져오기',
      desc:  'OL 파일(.html), 카드 JSON, 개별 마크다운으로 자유롭게 입출력합니다.'
    },
    {
      icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"/><path d="M12 6v6l4 2"/></svg>',
      title: '오프라인 우선',
      desc:  '인터넷 없이도 동작합니다. 데이터는 브라우저 로컬과 파일 안에만 머뭅니다.'
    },
  ];

  const featLabel = ce('div','home-section-label','OL Core · 기본 기능');
  wrap.appendChild(featLabel);
  const featGrid = ce('div','home-feat-grid');
  features.forEach(f => {
    const c = ce('div','home-feat-card');
    c.innerHTML = `
      <span class="home-feat-icon">${f.icon}</span>
      <div class="home-feat-title">${escapeHTML(f.title)}</div>
      <div class="home-feat-desc">${escapeHTML(f.desc)}</div>
    `;
    featGrid.appendChild(c);
  });
  wrap.appendChild(featGrid);

  // ─── 올확장 프로젝트 ─────────────────────
  if (OL_PROJECTS && OL_PROJECTS.length) {
    const ext = ce('div','home-section-label','올확장 · 콘텐츠 프로젝트');
    ext.style.marginTop = '2.5rem';
    wrap.appendChild(ext);

    const projGrid = ce('div','home-proj-grid');
    OL_PROJECTS.forEach(p => {
      const a = document.createElement('a');
      a.className = 'home-proj-card';
      a.href = p.url || '#';
      if (p.url && p.url !== '#') { a.target = '_blank'; a.rel = 'noopener'; }
      a.innerHTML = `
        <div class="home-proj-head">
          <span class="home-proj-tag">${escapeHTML(p.tag || '')}</span>
          <div class="home-proj-title">${escapeHTML(p.name)}</div>
        </div>
        <div class="home-proj-desc">${escapeHTML(p.desc)}</div>
        <span class="home-proj-arrow">${ICONS_X.chevronRight}</span>
      `;
      projGrid.appendChild(a);
    });
    wrap.appendChild(projGrid);
  }

  // ─── 푸터 (원저자 정보 간략) ────────────────
  const foot = ce('div','home-foot');
  foot.innerHTML = `
    <div>${escapeHTML(ORIGIN.tool)} · ${escapeHTML(ORIGIN.copyright)}</div>
    <div>License: ${escapeHTML(ORIGIN.license)} · <a href="https://${ORIGIN.site}" target="_blank" rel="noopener">${escapeHTML(ORIGIN.site)}</a></div>
  `;
  wrap.appendChild(foot);

  // 핸들러
  document.getElementById('home-hero-start').onclick = () => switchView('kanban');
  document.getElementById('home-hero-doc').onclick   = () => switchView('document');
  document.getElementById('home-start-btn').onclick  = () => switchView('kanban');
}
```

### 7.E `switchView`에 'home' 케이스 추가

라인 4867 근처:

```js
if (v === 'kanban')   renderKanban();
if (v === 'cards')    renderCards();
if (v === 'list')     renderList();
if (v === 'about')    renderAbout();
if (v === 'document') renderDocumentView();
if (v === 'home')     renderHome();   // ← 추가

// 마지막 뷰 저장 (home은 저장 안 함 — 다음 진입 시 자연스럽게 home으로)
if (v !== 'home') {
  try { localStorage.setItem('ol_last_view', v); } catch(_) {}
}
```

### 7.F `init()` 변경

라인 8231:

```js
(function init() {
  try {
    if (__LOADED_DATA_B64__ && __LOADED_DATA_B64__ !== '__INIT_DATA_B64__') {
      const json = decodeURIComponent(escape(atob(__LOADED_DATA_B64__)));
      S = normalizeState(JSON.parse(json));
      localStorage.setItem('ol_v1', JSON.stringify(S));
    } else {
      load();
    }
  } catch(e) { load(); }

  // 마지막 뷰 복원 or home으로 진입
  let startView = 'home';
  try {
    const last = localStorage.getItem('ol_last_view');
    if (last && ['kanban','cards','list','document','about'].includes(last)) {
      startView = last;
    }
  } catch(_) {}

  switchView(startView);
})();
```

### 7.G 로고 클릭 동작 변경

라인 3822:

```html
<!-- 변경 전 -->
<div class="h-brand" onclick="switchView('kanban')">

<!-- 변경 후 -->
<div class="h-brand" onclick="switchView('home')" style="cursor:pointer" role="button" tabindex="0" aria-label="홈으로">
```

### 7.H CSS (Home 페이지)

기존 about-wrap 스타일과 유사하되 더 임팩트 있게. CSS 블록 어딘가(`/* APP LAYOUT */` 위쪽) 또는 about CSS 다음:

```css
/* ══════════════════════════════════════════
   HOME (Landing)
══════════════════════════════════════════ */
.home-wrap {
  max-width: 64rem;
  margin: 0 auto;
  padding: 3rem 2rem 4rem;
}

.home-hero {
  padding: 1.5rem 0 2.5rem;
  border-bottom: 1px solid hsl(var(--border));
  margin-bottom: 2.5rem;
}
.home-hero-eyebrow {
  font-size: 0.75rem;
  font-weight: 500;
  color: hsl(var(--muted-foreground));
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 0.875rem;
}
.home-hero-title {
  font-size: 2.25rem;
  font-weight: 700;
  line-height: 1.18;
  letter-spacing: -0.025em;
  color: hsl(var(--foreground));
  margin: 0 0 1rem;
}
.home-hero-sub {
  font-size: 1rem;
  line-height: 1.55;
  color: hsl(var(--muted-foreground));
  max-width: 42rem;
  margin-bottom: 1.5rem;
}
.home-hero-actions {
  display: flex; gap: 0.5rem; flex-wrap: wrap;
}

.home-section-label {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Pretendard Variable", sans-serif;
  font-size: 0.75rem;
  font-weight: 600;
  color: hsl(var(--muted-foreground));
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 1rem;
}

/* ── Features 그리드 ── */
.home-feat-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}
.home-feat-card {
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  padding: 1rem 1.125rem 1.125rem;
  background: hsl(var(--card));
  transition: background-color .15s, border-color .15s;
}
.home-feat-card:hover {
  background: hsl(var(--accent) / 0.4);
  border-color: hsl(var(--border));
}
.home-feat-icon {
  display: inline-flex; align-items: center; justify-content: center;
  width: 1.75rem; height: 1.75rem;
  background: hsl(var(--secondary));
  border-radius: calc(var(--radius) - 4px);
  color: hsl(var(--foreground));
  margin-bottom: 0.625rem;
}
.home-feat-icon svg { width: 1rem; height: 1rem; }
.home-feat-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: hsl(var(--foreground));
  margin-bottom: 0.25rem;
}
.home-feat-desc {
  font-size: 0.8125rem;
  line-height: 1.5;
  color: hsl(var(--muted-foreground));
}

/* ── 올확장 프로젝트 그리드 ── */
.home-proj-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr));
  gap: 0.75rem;
  margin-bottom: 2rem;
}
.home-proj-card {
  display: block;
  position: relative;
  border: 1px solid hsl(var(--border));
  border-radius: var(--radius);
  padding: 1rem 1.125rem 1.125rem;
  background: hsl(var(--card));
  color: hsl(var(--foreground));
  text-decoration: none;
  transition: background-color .15s, border-color .15s, transform .15s;
}
.home-proj-card:hover {
  background: hsl(var(--accent) / 0.5);
  transform: translateY(-1px);
}
.home-proj-head {
  display: flex; flex-direction: column; gap: 0.375rem;
  margin-bottom: 0.5rem;
}
.home-proj-tag {
  display: inline-block;
  align-self: flex-start;
  font-size: 0.6875rem;
  font-weight: 500;
  padding: 0.125rem 0.5rem;
  background: hsl(var(--secondary));
  color: hsl(var(--secondary-foreground));
  border-radius: 9999px;
}
.home-proj-title {
  font-size: 1rem;
  font-weight: 600;
  color: hsl(var(--foreground));
}
.home-proj-desc {
  font-size: 0.8125rem;
  line-height: 1.5;
  color: hsl(var(--muted-foreground));
}
.home-proj-arrow {
  position: absolute;
  top: 1rem; right: 1rem;
  display: inline-flex; align-items: center; justify-content: center;
  width: 1.25rem; height: 1.25rem;
  color: hsl(var(--muted-foreground));
  opacity: 0;
  transition: opacity .15s, transform .15s;
}
.home-proj-arrow svg { width: 0.875rem; height: 0.875rem; }
.home-proj-card:hover .home-proj-arrow {
  opacity: 1;
  transform: translateX(2px);
}

.home-foot {
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid hsl(var(--border));
  font-size: 0.75rem;
  color: hsl(var(--muted-foreground));
  line-height: 1.7;
  text-align: center;
}
.home-foot a {
  color: hsl(var(--foreground));
  text-decoration: none;
}
.home-foot a:hover { text-decoration: underline; }

/* 모바일 */
@media (max-width: 640px) {
  .home-wrap { padding: 2rem 1rem 3rem; }
  .home-hero-title { font-size: 1.75rem; }
  .home-feat-grid, .home-proj-grid { grid-template-columns: 1fr; }
}
```

### 7.I 헤더 네비에 home 활성화 표시 처리

`switchView` 안에서 `h-nav-btn`의 active 처리는 `data-view` 기준. `data-view="home"` 버튼이 없으므로 home일 때는 **어떤 네비도 active되지 않음**. 이게 자연스러우므로 변경 불필요. 로고가 "홈 진입점" 역할.

### 7.J 검증

- [ ] 처음 진입 (`ol_last_view` 없음) → home 표시
- [ ] 칸반 뷰로 이동 후 새로고침 → 칸반으로 시작
- [ ] 로고 클릭 → 항상 home
- [ ] home의 "칸반 보드로 시작" 버튼 동작
- [ ] 올확장 카드 클릭 → 새 탭에서 외부 URL 열림
- [ ] 라이트/다크모드 모두 가독성 OK

---

## 작업 순서 권장 (실제 코드 편집 시)

1. **Task 0 (헬퍼)** → Task 1 (컬러) → 검증 (스타일만 영향) → 1차 배포 가능 지점
2. **Task 3 (MD export)** → **Task 4 (MD import)** → 검증 (export/import만 영향)
3. **Task 5 (문서뷰 레이아웃)** → 검증 (CSS only가 대부분)
4. **Task 2 (사이드바 컬럼 필터 + 태그)** → 검증
5. **Task 6 (문서뷰 트리)** → 검증 (T2 기반 분기 추가)
6. **Task 7 (Home)** → 검증 (전체 통합 후)

각 Task 사이에 다음 검증:

```bash
node --check ol-v1_1.html  # syntax 점검
```

브라우저 검증:

- 라이트/다크 모드 양쪽
- 1920 / 1440 / 1280 / 1024 / 768 / 640 / 375 폭

---

## 부록 A — 자기참조 회피 점검표

다음 항목은 `buildExportHTML` 등에서 정규식 자기참조를 일으킬 위험이 있으니, 변경 시마다 점검:

1. 새로 추가하는 함수에서 `__LOADED_DATA_B64__` 문자열을 **하드코딩하지 말 것** (필요 시 `'__LOADED' + '_DATA_B64__'`)
2. `__STATIC_HTML__` 변수에 의존하는 export 로직은 그대로 유지 — 신규 DOM은 init 이후에만 생성
3. `__INIT_DATA_B64__` 플레이스홀더 패턴은 빌드 시 치환되므로 코드에 직접 작성하지 말 것

---

## 부록 B — 출력 파일

작업 완료 후 `/mnt/user-data/outputs/ol-v1_1.html` 생성. 변경 라인 수가 많으므로 다음 방식으로 검수 권장:

```bash
diff -u ol-v1_0.html ol-v1_1.html | wc -l        # 총 변경 라인
diff -u ol-v1_0.html ol-v1_1.html | head -200    # 상단 일부
```

---

## 부록 C — 향후(v1.2+) 확장 후보 메모

이번 v1.1 작업 범위에서 **제외**한 항목이지만 자연스러운 다음 단계:

- 사이드바 태그를 **OR/AND 토글** 가능하게 (현재는 OR)
- 사이드바 트리에서 카드 드래그앤드롭으로 컬럼/그룹 이동
- 마크다운 import 시 **이미지 base64 인라인** 자동 변환 옵션
- 홈 화면에 "최근 편집한 카드" 위젯
- ZIP 압축 export (다중 .md를 하나의 zip으로) — JSZip 단일파일 ESM 임베드 가능

— 끝 —