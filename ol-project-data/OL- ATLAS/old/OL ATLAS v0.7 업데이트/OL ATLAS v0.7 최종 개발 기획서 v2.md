# OL ATLAS v0.7 최종 개발 기획서 v2

**버전**: Final v2.0 **작성일**: 2026-05-21 **전임 버전**: OL ATLAS v0.6 **프로젝트 단계**: prototype → platform 전환 (구조 정합성 우선) **예상 일정**: 4~6.5주 (일정 비제약 모드)

---

## 0. 한 줄 요약

> v0.7은 **3계층 모델**(UI → Action → State → Render Queue)을 정착시키고, PDF 새 UI를 적용하며, 개발/배포 분리를 도입하는 사이클이다. Plugin API / Hook System / Event Bus는 전면 폐기. **Action Layer만으로 충분한 단순성**을 추구한다.

---

## 1. v0.7의 목표

### 1.1 세 가지 축

```
1) 구조 축    개발/배포 분리(src→dist) + 모듈화
2) 런타임 축  Action Layer + Render Queue + Dirty State
3) UI 축      PDF 아이디어 채택분 (카드보드 통합, 테이블뷰, 사이드바 숨김)
```

### 1.2 v0.7 완료의 정의(DoD)

- [ ] `src/` ES modules → `dist/ol-atlas.html` 단일 파일 빌드 정착 (esbuild)
- [ ] PDF 채택 UI 전체 작동 (헤더 슬림, 사이드바 숨김 기본, 탭 네비, 카드보드 통합, 테이블뷰)
- [ ] **모든 state 변경이 Action 경유** (dispatch 외 직접 mutation 0건)
- [ ] **모든 view 갱신이 RenderQueue 경유** (직접 render 호출 0건)
- [ ] Dirty State + beforeunload + autosave 작동
- [ ] 카드 모달: 본문 readonly + 제목/태그 인라인 편집 + "편집→문서뷰"
- [ ] shadcn/ui 디자인 토큰·컴포넌트 매핑 일관 적용
- [ ] v0.6 → v0.7 마이그레이션 작동 (schemaVersion 6→7)
- [ ] i18n 키 분리 완료 (사전은 한국어만)
- [ ] 설정뷰 작동 (테마/데이터 관리/언어 슬롯)

### 1.3 명시적 비목표 (Non-goals)

- **Plugin API / Hook System / Event Bus**: 전면 폐기 확정
- **Semantic Search / Knowledge Graph**: 미구현. 검색 추상화 계층만 마련
- **다중 언어 실제 번역**: 사전은 한국어만, EN/ZH/JA/ES는 v0.8 이후
- **IndexedDB / PWA / Electron / 런타임 CDN 라이브러리**: 채택 안 함
- **분기 기록·기여자 추적**: 폐기. ORIGIN 하드코딩만 유지
- **문서뷰 에디터 확장**(각주/원문박스/주석박스/메모): v0.7.x 별도 작업

---

## 2. 확정된 결정 사항

|#|항목|확정|
|---|---|---|
|1|**범위**|UI 전면 개편 + 모듈화 + Action Layer + Render Queue + Dirty State. (Plugin/Hook/EventBus 폐기)|
|2|**사이드바**|PDF안 그대로. 데스크탑/모바일 기본 숨김, 햄버거 토글. 칼럼/그룹/태그 영역 제거. 검색바는 탭 네비 상단.|
|3|**카드 모달**|본문 readonly + 제목/태그 인라인 편집 + "편집" 버튼 → 문서뷰.|
|4|**빌드 도구**|esbuild.|
|5|**다중 언어**|v0.7은 i18n 키 분리만, 사전 한국어만.|
|6|**일정 정책**|일정 비제약. 구조 정합성 우선.|
|7|**플러그인**|전면 폐기. Plugin API, Hook System, Event Bus 모두 없음.|

---

## 3. 새 UI 설계 — PDF 아이디어 정리

### 3.1 채택 — 그대로 반영

|PDF 아이디어|설명|
|---|---|
|**사이드바 기본 숨김 + 햄버거 토글**|데스크탑/모바일 동일|
|**사이드바 단순화**|칼럼·그룹·태그 영역 제거 → ABOUT, 휴지통, (문서뷰)카드 목록·목차, 저장/열기/다크모드/설정|
|**칸반 → 카드보드 통합**|카드뷰 별도 전환 제거. 너비 토글(MAX/WIDE/NORMAL)|
|**리스트 → 테이블뷰**|인라인 편집 + 칼럼별 검색 필터|
|**탭 네비게이션**|카드보드 칼럼 ↔ 테이블뷰 매칭. 각 탭은 해당 칼럼의 테이블|
|**로고 클릭 → 카드보드**|홈 랜딩 폐기|
|**카드 모달**|본문 readonly + 제목/태그 인라인 편집 + 편집→문서뷰|
|**메타 토글**|"전체 / 제목 / 내용 / 태그" 토글로 카드 상단 메타 표시 제어|
|**새로고침 유실 경고**|beforeunload + Dirty State|
|**카드보드 칼럼 순서 이동**|칼럼 헤더 드래그|
|**모달 팝업 시 배경 어둡게**|overlay 적용|
|**설정뷰 추가**|신규. 테마, 데이터 관리, i18n 미래 슬롯 (플러그인 섹션 없음)|
|**검색바 탭 상단으로**|헤더에서 분리|

### 3.2 보류 — v0.7.x 또는 이후

|PDF 아이디어|v0.7 결정|사유|
|---|---|---|
|**다중 언어 실제 번역(EN/ZH/JA/ES)**|i18n 키 분리만|사전은 한국어만, 번역 품질 통제 필요|
|**문서뷰 각주/원문박스/주석박스/메모**|별도 작업(v0.7.x)|에디터 확장은 콘텐츠 작업 본격화 시점에|
|**카드 본문 폭 좁게 + 이미지 확장**|shadcn prose 폭으로 통일만|이미지 확장 토큰은 후속|
|**문서뷰 태그 클릭 → 검색**|v0.7.x|검색 결과 모달 정리 선행|
|**모듈 다운로드(외부)**|채택 안 함|플러그인 전면 폐기|

### 3.3  새 UI 와이어 정리

```
┌─────────────────────────────────────────────────────────────────┐
│ ☰  OL · ATLAS                                                   │  헤더(56px)
├─────────────────────────────────────────────────────────────────┤
│ [너비: ●MAX ○WIDE ○NORMAL]   [검색 ⌘K]   토글: 전체/제목/내용/태그│  서브헤더
├─────────────────────────────────────────────────────────────────┤
│ [BOARD] [서원] [바라밀] [탄생] [출가] [성도] [전법] [열반]      │  탭 네비
├─────────────────────────────────────────────────────────────────┤
│  ┌서원────┐ ┌바라밀──┐ ┌탄생────┐ ┌출가────┐ ┌성도────┐         │
│  │● 카드  │ │● 카드  │ │● 카드  │ │● 카드  │ │● 카드  │  ← BOARD 탭
│  │  제목  │ │  제목  │ │  제목  │ │  제목  │ │  제목  │
│  │  메타  │ │  메타  │ │  메타  │ │  메타  │ │  메타  │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘
└─────────────────────────────────────────────────────────────────┘

  탭이 [서원]이면 → 그 칼럼의 카드만 테이블로
  ┌─제목────────Q ─내용──────Q ─태그────Q ─수정일────문서뷰─┐
  │ Group A                                                  │
  │   카드 제목       short info     [#수메다] 2026-05-19  ↗ │
  │   카드 제목       short info     [#바라밀] 2026-05-18  ↗ │
  │ Group B                                                  │
  │   ...                                                    │
  └──────────────────────────────────────────────────────────┘
```

탭이 곧 "보드의 한 칼럼"이므로, 칸반의 칼럼과 테이블의 탭이 1:1 매칭된다.

### 3.4 디자인 시스템

스타일 문서(`스타일 구현 정책 및 수정 로드맵.md`) + v0.6 메모리 자산 계승.

- HSL 토큰(neutral), 라이트/다크
- 시스템 폰트 + Pretendard
- shadcn 컴포넌트 매핑: Dialog, Badge, ToggleGroup, Tabs, Table, Command, Sonner, Popover, Select
- lucide 스타일 인라인 SVG

---

## 4. 아키텍처 — 3계층 모델

v0.7의 핵심 변화. 단순하지만 엄격하게 정착시킨다.

### 4.1 계층 구조

```
┌──────────────────────────────────────────────────────┐
│  UI Layer (views, components)                        │
│  - DOM 렌더링만 담당                                 │
│  - state 직접 수정 절대 금지                         │
│  - 변경은 반드시 dispatch(action)                    │
│  - 다른 UI 갱신은 queueRender('viewName')            │
└────────────────────────┬─────────────────────────────┘
                         │ dispatch
                         ▼
┌──────────────────────────────────────────────────────┐
│  Action Layer                                        │
│  - 모든 state 변경의 단일 진입점                     │
│  - reducer 패턴: (state, action) → newState          │
│  - 변경 후 자동으로 dirty 마킹 + 영향받는 view queue │
└────────────────────────┬─────────────────────────────┘
                         │ mutate
                         ▼
┌──────────────────────────────────────────────────────┐
│  State Layer (S) + Render Queue                      │
│  - cards, cols, settings, meta                       │
│  - localStorage persist (debounced autosave)         │
│  - dirty flag                                        │
│  - queueRender + rAF flush                           │
│  - store.subscribe(viewName, renderFn)               │
└──────────────────────────────────────────────────────┘
```

### 4.2 핵심 원칙

**금지 사항**:

- ❌ UI 코드에서 `S.cards.push(...)` 같은 직접 mutation
- ❌ UI 코드에서 `renderCards()` 같은 직접 render 호출
- ❌ 컴포넌트 간 직접 참조 (`document.getElementById('sidebar').foo()`)

**권장 패턴**:

- ✅ `dispatch({ type: 'CARD_CREATE', payload: {...} })`
- ✅ `queueRender('cardboard')` — 명시적으로 갱신 필요한 view만
- ✅ Action의 reducer가 자동으로 영향받는 view를 queue에 등록 (가능한 경우)

### 4.3 디렉토리 구조

```
ol-atlas/
├── src/
│   ├── core/
│   │   ├── state.js              # S 객체, makeDefault, normalizeState
│   │   ├── action.js             # dispatch, reducer registry, action types
│   │   ├── store.js              # subscribe, getState
│   │   ├── render-queue.js       # queueRender + rAF flush
│   │   ├── storage.js            # localStorage 추상화 (save/load/backup)
│   │   ├── schema.js             # schemaVersion + migrators (6→7)
│   │   ├── dirty.js              # markDirty / markClean / autosave debounce
│   │   ├── origin.js             # ORIGIN 하드코딩
│   │   └── id.js                 # slug, uniqueSlug, imgId
│   │
│   ├── data/
│   │   ├── card.js               # normalizeCard, validators
│   │   ├── tag.js                # parseTag, prefix index, free tags
│   │   ├── markdown.js           # parseInline, parseMarkdown, stripMarkdown
│   │   └── search/
│   │       ├── index.js          # search 진입점 (추상화)
│   │       ├── basic.js          # 단순 텍스트 검색 (v0.7 활성)
│   │       ├── tag-index.js      # 태그 색인
│   │       └── semantic.js       # 시멘틱 검색 (v0.7 미구현, 슬롯만)
│   │
│   ├── actions/                  # 도메인별 액션 정의
│   │   ├── card-actions.js       # CARD_CREATE, CARD_UPDATE, CARD_DELETE...
│   │   ├── column-actions.js     # COLUMN_CREATE, COLUMN_REORDER...
│   │   ├── view-actions.js       # VIEW_CHANGE, TAB_SELECT, BOARD_WIDTH...
│   │   └── settings-actions.js   # SETTINGS_UPDATE, THEME_TOGGLE...
│   │
│   ├── ui/
│   │   ├── header.js
│   │   ├── sidebar.js            # 단순화된 사이드바
│   │   ├── tabs.js               # 탭 네비게이션
│   │   ├── cardboard.js          # 카드보드 (통합된 칸반)
│   │   ├── tableview.js          # 테이블뷰 (인라인편집 + 필터)
│   │   ├── docview.js            # 문서뷰
│   │   ├── about.js
│   │   ├── settings.js           # 신규: 설정뷰 (플러그인 섹션 없음)
│   │   └── modal-card.js         # 카드 미리보기 모달 (절충안)
│   │
│   ├── components/
│   │   ├── toggle-group.js
│   │   ├── select.js
│   │   ├── command.js            # ⌘K 검색 팔레트
│   │   ├── popover.js
│   │   ├── dialog.js
│   │   ├── toast.js              # Sonner 스타일
│   │   ├── badge.js
│   │   ├── table.js              # shadcn Table 베이스
│   │   ├── tabs.js               # shadcn Tabs 베이스
│   │   └── icons.js              # 인라인 SVG 사전 (lucide 스타일)
│   │
│   ├── i18n/
│   │   ├── t.js                  # t(key) 함수
│   │   ├── ko.js                 # 한국어 사전 (v0.7 유일 사전)
│   │   └── KEYS.md               # 등록된 키 목록 문서
│   │
│   ├── styles/
│   │   ├── tokens.css
│   │   ├── base.css
│   │   ├── components.css
│   │   ├── tabs.css
│   │   ├── cardboard.css
│   │   ├── tableview.css
│   │   ├── docview.css
│   │   └── settings.css
│   │
│   ├── boot.js                   # 부팅 시퀀스
│   └── index.html                # 빈 셸 + <script type="module" src="boot.js">
│
├── build/
│   ├── build.mjs                 # esbuild 빌드 + 인라이닝
│   └── inline.mjs                # CSS·JS·아이콘 → 단일 HTML
│
├── dist/
│   └── ol-atlas.html             # 배포 산출물 (자기완결)
│
└── package.json
```

### 4.4 부팅 시퀀스

```js
// src/boot.js (의사 코드)
async function boot() {
  // 1. localStorage에서 state 로드 + schema 마이그레이션
  let raw = storage.load();
  raw = schema.migrate(raw);                 // v6 → v7 자동
  store.init(normalizeState(raw));

  // 2. Action Layer 활성화 (모든 reducer 등록)
  action.registerReducers([
    cardReducer, columnReducer, viewReducer, settingsReducer
  ]);

  // 3. Render Queue 활성화
  renderQueue.init();

  // 4. UI 마운트 (모든 view를 store에 subscribe)
  ui.mount();

  // 5. 첫 렌더
  renderQueue.flush();
}
```

### 4.5 Action 예시

```js
// src/actions/card-actions.js
export const CARD_UPDATE = 'CARD_UPDATE';

export function updateCard(id, patch) {
  return { type: CARD_UPDATE, payload: { id, patch } };
}

export function cardReducer(state, action) {
  switch (action.type) {
    case CARD_UPDATE: {
      const { id, patch } = action.payload;
      const cards = state.cards.map(c => 
        c.id === id ? normalizeCard({ ...c, ...patch }) : c
      );
      return { ...state, cards };
    }
    // ...
  }
}

// UI에서 사용
import { updateCard } from '@/actions/card-actions';
dispatch(updateCard(cardId, { title: newTitle }));
// → reducer 실행 → state 변경 → dirty 마킹 → autosave queue → 
//   render queue('cardboard', 'tableview', 'sidebar') → rAF flush
```

---

## 5. 데이터 모델 — schema v7

### 5.1 변경점

```js
S.meta.schemaVersion = 7
S.meta.dirty         = false        // 신규
S.meta.lastSavedAt   = ISO          // 신규

S.settings = {                       // 신규
  theme: 'system' | 'light' | 'dark',
  locale: 'ko',                      // v0.7 고정값
  sidebarOpen: false,                // 기본 false (PDF안)
  boardWidth: 'NORMAL' | 'WIDE' | 'MAX',
  metaToggles: { title: true, body: true, tags: true },
  activeTabId: 'board',
}

// S.plugins 없음 (플러그인 폐기)
```

### 5.2 마이그레이션

```js
// src/core/schema.js
const migrators = {
  6: (s) => {
    s.meta.schemaVersion = 7;
    s.meta.dirty = false;
    s.meta.lastSavedAt = null;
    s.settings = {
      theme: localStorage.getItem('ol_theme') || 'system',
      locale: 'ko',
      sidebarOpen: false,
      boardWidth: 'NORMAL',
      metaToggles: { title: true, body: true, tags: true },
      activeTabId: 'board',
    };
    return s;
  },
};

// 부팅 시 v6 백업을 localStorage에 자동 저장 (ol_backup_v6)
```

---

## 6. 작업 목록 (WBS)

각 Phase는 자기완결적 단위. 일정 비제약이지만 의존성 순서는 엄격히 지킴.

### Phase 0 — 빌드 셋업 + 모듈 분해 (2~4일)

|#|작업|산출물|
|---|---|---|
|0.1|v0.6 HTML을 `src/` 모듈로 수작업 분해|`src/**` 초기 구조|
|0.2|esbuild 기반 `build/build.mjs` 작성|번들 JS 생성|
|0.3|CSS concat + 인라이닝 (`build/inline.mjs`)|단일 HTML 생성|
|0.4|`__STATIC_HTML__` 캡처 + `__LOADED_DATA_B64__` 자기참조 보호 패턴 빌드에 통합|export 작동|
|0.5|`npm run dev` / `npm run build` 명령|README + package.json|
|0.6|v0.6 기능 동등성 회귀 테스트 (manual QA 체크리스트)|Phase 1 진입 게이트|

### Phase 1 — 런타임 인프라 (4~6일)

**핵심 위험 구간**. 이 단계가 끝나야 이후 모든 작업이 새 패턴으로 진행 가능.

|#|작업|산출물|
|---|---|---|
|1.1|`core/store.js` — getState, subscribe, applyPatch|store 작동|
|1.2|`core/action.js` — dispatch, reducer registry, action types|dispatch 작동|
|1.3|`core/render-queue.js` — queueRender + rAF flush|다중 render 1회 합치기|
|1.4|`core/dirty.js` — markDirty + markClean + autosave debounce 1000ms|dirty flag + 자동 저장|
|1.5|beforeunload 핸들러|새로고침 경고|
|1.6|`core/schema.js` — v6→v7 migrator + v6 백업|마이그레이션 작동|
|1.7|v0.6 기능을 새 런타임 위로 어댑팅 (직접 render 호출 모두 제거)|grep으로 검증|

**검증 게이트**:

- `grep -rE "renderCards\(|renderKanban\(|renderList\(" src/ui/` 결과 0건 (모두 queueRender 경유)
- `grep -rE "S\.cards\.push|S\.cards\[.*\]\s*=" src/ui/` 결과 0건 (모두 dispatch 경유)

### Phase 2 — Action 도메인 정의 (2~3일)

|#|작업|산출물|
|---|---|---|
|2.1|`actions/card-actions.js` (CREATE/UPDATE/DELETE/MOVE) + cardReducer|카드 액션|
|2.2|`actions/column-actions.js` (CREATE/RENAME/REORDER/DELETE) + columnReducer|칼럼 액션|
|2.3|`actions/view-actions.js` (VIEW_CHANGE/TAB_SELECT/BOARD_WIDTH/META_TOGGLE) + viewReducer|뷰 액션|
|2.4|`actions/settings-actions.js` (SETTINGS_UPDATE/THEME_TOGGLE/SIDEBAR_TOGGLE) + settingsReducer|설정 액션|

### Phase 3 — 사이드바 단순화 (2일)

|#|작업|산출물|
|---|---|---|
|3.1|사이드바에서 칼럼·그룹·태그 영역 코드 제거|sidebar 단순화|
|3.2|햄버거 토글 (헤더 좌상단) + `settings.sidebarOpen` 바인딩|토글 동작|
|3.3|사이드바 콘텐츠: ABOUT / 휴지통 / (문서뷰)카드 목록 + 목차|항목 정렬|
|3.4|저장 / 열기 / 다크모드 / 설정 버튼을 사이드바로 이동|버튼 이동|
|3.5|모바일 오버레이, 데스크탑 슬라이드, 햄버거 오버레이 z-index(25)|반응형|

### Phase 4 — 탭 + 카드보드 통합 (4~6일)

|#|작업|산출물|
|---|---|---|
|4.1|`components/tabs.js` — shadcn Tabs|탭 컴포넌트|
|4.2|탭 정의: BOARD + 각 칼럼 (자동 생성)|탭 목록|
|4.3|`ui/cardboard.js` — 칸반 + 카드그리드 통합|카드뷰 폐기|
|4.4|너비 토글 (MAX/WIDE/NORMAL) → `--board-col-w`|너비 변경|
|4.5|메타 토글 (전체/제목/내용/태그)|토글 동작|
|4.6|카드 상단 메타 + 하단 연결문서|카드 레이아웃|
|4.7|카드보드 칼럼 순서 이동 (drag handle)|칼럼 재정렬|

### Phase 5 — 테이블뷰 (4~6일)

|#|작업|산출물|
|---|---|---|
|5.1|`components/table.js` — shadcn Table|테이블 컴포넌트|
|5.2|`ui/tableview.js` — 탭이 칼럼일 때 해당 카드만 표시|탭 ↔ 테이블 매칭|
|5.3|인라인 편집 (제목, 내용 요약, 태그)|셀 편집|
|5.4|칼럼별 검색 필터 (제목/내용/태그 셀의 🔍 팝오버)|필터 동작|
|5.5|그룹 행 (Group A / Group B)|그룹별 정렬|
|5.6|"문서뷰" 칼럼 → 행 클릭 시 문서뷰 진입|진입 동작|

### Phase 6 — 카드 모달 + 검색 + 헤더 (2~3일)

|#|작업|산출물|
|---|---|---|
|6.1|모달 본문을 readonly 렌더로 변경|본문 미리보기|
|6.2|제목 인라인 편집 (contenteditable 또는 inline Input)|제목 즉시 편집|
|6.3|태그 인라인 편집 (배지 + 추가/삭제)|태그 즉시 편집|
|6.4|"편집" 버튼 → 문서뷰 라우팅|본문 편집은 문서뷰|
|6.5|모달 overlay 어둡게|shadcn Dialog 표준|
|6.6|제목/태그 변경 → dispatch + markDirty + autosave|자동 저장 연동|
|6.7|검색바를 탭 네비 상단으로 이동|위치 변경|
|6.8|`components/command.js` — ⌘K 트리거|키보드 단축키|
|6.9|헤더 슬림화 (좌: 햄버거+로고, 우: 설정/테마)|헤더 정리|

### Phase 7 — 설정뷰 (1~2일)

|#|작업|산출물|
|---|---|---|
|7.1|`ui/settings.js` — 설정뷰 레이아웃|설정 페이지|
|7.2|테마 설정 섹션 (system/light/dark)|테마 토글|
|7.3|언어 설정 슬롯 (v0.7은 한국어만, UI는 미래 대비)|슬롯 마련|
|7.4|데이터 관리 (백업·복원·초기화)|데이터 도구|

**참고**: 플러그인 폐기로 인해 v0.7 설정뷰는 단순합니다. 플러그인 섹션 없음.

### Phase 8 — i18n 키 분리 (2~3일)

|#|작업|산출물|
|---|---|---|
|8.1|`i18n/t.js` — `t(key, params?)` 함수|t 함수|
|8.2|`i18n/ko.js` — 한국어 사전|사전|
|8.3|UI 코드의 모든 하드코딩 한국어 → `t(...)` 치환|키 추출 완료|
|8.4|`i18n/KEYS.md` — 등록된 키 목록 자동 생성 스크립트|문서|

### Phase 9 — 마무리 (3일)

|#|작업|산출물|
|---|---|---|
|9.1|v0.6 데이터 import 회귀 테스트 (실제 파일 3종 이상)|마이그레이션 검증|
|9.2|grep 검증 (직접 render·state 수정 0건)|패턴 일관성|
|9.3|shadcn 토큰 일관성 lint (하드코딩 색상 0건)|디자인 일관성|
|9.4|모바일 QA (iOS Safari, Android Chrome)|반응형 검증|
|9.5|`dist/ol-atlas.html` 콘텐츠 시연 (OL 붓다스토리 1차 PoC)|OL BOOK 준비|

---

## 7. 위험 요소 및 대응

|위험|등급|대응|
|---|---|---|
|Phase 1 런타임 인프라 도입 중 v0.6 기능 회귀|**높음**|Phase 0 완료 후 v0.6 동등성 회귀 테스트를 게이트로. Phase 1을 작은 PR로 쪼개기|
|빌드 분리 중 export 로직 자기참조 정규식 깨짐|중|메모리 패턴(`'__LOADED' + '_DATA_B64__'` 분리 + `new RegExp(...)`)을 빌드 출력 검사에 포함|
|CSS concat 시 주석 누락 → 규칙 무효화|중|빌드 후 CSS 파싱 검증|
|마이그레이션 실패로 사용자 데이터 손실|낮음 (영향 큼)|v6→v7 시 `ol_backup_v6` 자동 백업 + 복원 UI|
|Action Layer 도입으로 코드량 폭증|중|액션은 도메인별 파일로 분리. action type을 상수로 통일|
|iOS Safari 다크모드 + 햄버거 + 모달 z-index 충돌|중|위계: hamburger overlay 25, sidebar 30, header 50, modal 100, toast 200|
|직접 render 호출 누락이 grep으로 안 잡힘|중|코드 리뷰 시 PR마다 `core/render-queue.js` import 확인|
|칸반/카드뷰 통합 중 드래그앤드롭 회귀|중|Phase 4 시작 시 v0.6 DnD 동작 스펙을 별도 문서로 캡처|

---

## 8. 검증 게이트

Phase 진입 전 충족 조건. 게이트 미달 시 다음 Phase 금지.

|Gate|조건|
|---|---|
|**Phase 1 진입**|Phase 0 완료 + dist가 v0.6과 기능 동등 (manual QA)|
|**Phase 2 진입**|Phase 1 완료 + 런타임 자체 단위 테스트 통과|
|**Phase 3 진입**|Phase 2 완료 + 4개 reducer가 모두 dispatch로 작동 검증|
|**Phase 6 진입**|Phase 4, 5 모두 완료|
|**Phase 9 진입**|모든 UI Phase 완료|
|**v0.7 릴리스**|DoD 10개 항목 전부 체크 + 위험 대응책 전부 적용|

---

## 9. OL BOOK 세대 준비

v0.7 완료 시점에 OL BOOK 콘텐츠 탑재 관점에서 준비되는 것:

1. **읽기 흐름 우선 UI**: 사이드바 기본 숨김 + 너비 토글로 읽기 화면 확보
2. **문서뷰 중심 편집**: 카드 모달 절충안으로 "쓰기 = 문서뷰" 정책 정착
3. **빌드 분리**: `dist/ol-book-buddha-story.html` 같은 변형 산출물 생성 가능
4. **schemaVersion 시스템**: 향후 카드 관계 필드 추가가 안전
5. **shadcn 일관성**: 콘텐츠 패키지에서 UI 재발명 불필요
6. **i18n 인프라**: 한국어→다국어 확장이 사전 추가만으로 가능
7. **단순한 코어**: 플러그인·Hook 없이 깔끔한 3계층. 콘텐츠 작업에 집중 가능

---

## 10. 일정 추정

총 **4~6.5주** (단독 작업, 일정 비제약 모드).

|Phase|일수|
|---|---|
|0. 빌드 셋업|2~4|
|1. 런타임 인프라|4~6|
|2. Action 도메인|2~3|
|3. 사이드바 단순화|2|
|4. 탭 + 카드보드|4~6|
|5. 테이블뷰|4~6|
|6. 모달 + 검색 + 헤더|2~3|
|7. 설정뷰|1~2|
|8. i18n 키 분리|2~3|
|9. 마무리|3|
|**합계**|**26~38일**|

일정 비제약이므로 게이트 통과 시점 기준으로 진행. 압축하지 않음.

---

## 11. 즉시 다음 행동

1. **본 최종 기획서 v2 승인.**
2. Phase 0 착수: v0.6 HTML을 `src/` 구조로 분해하면서 `build/build.mjs` 동시 작성.
3. Phase 0 완료 시점에 `dist/ol-atlas.html`이 v0.6과 기능 동등함을 확인. 이게 Phase 1 게이트.
4. Phase 1 런타임 인프라 도입 — 가장 위험한 구간. 작은 PR로 쪼개고 게이트 엄격 적용.
5. 이후 Phase 2~9 순차 진행. Phase 3은 Phase 2 완료 후 즉시, Phase 4·5는 의존성 없으면 병렬 가능.

---

## 부록 A — v0.6 자산 보존 목록

v0.7에서 **그대로 계승**할 v0.6 자산.

- ORIGIN 하드코딩 (`author`, `site`, `copyright`, `license`)
- `__STATIC_HTML__` 캡처 + base64 export 패턴
- `btoa(unescape(encodeURIComponent(json)))` 인코딩
- HSL 토큰 시스템 (Phase 1~6 완료분)
- iOS Safari 다크모드 특이성 fix (`html.dark, :root.dark`)
- `normalizeCard`의 `bodyMode`/`bodyMd` 처리
- prefix tag ontology (인물/장소/경전/주제/유형/시기)
- `parseMarkdown` 인라인/블록 파서
- z-index 위계 (hamburger:25, sidebar:30, header:50, modal:100, toast:200)
- 검색 결과 Enter 키 핸들링 (ArrowUp floor: -1, fallback Enter)

## 부록 B — 폐기 확정 목록

- ❌ 분기 기록 / 기여자 추적
- ❌ IndexedDB / PWA / Electron / 런타임 CDN 라이브러리
- ❌ 온보딩 플로우 / 프로필 페이지 / 변경 이력
- ❌ React / Vue / Solid 도입
- ❌ **Plugin API / 외부 플러그인 로딩 / 내장 플러그인** (전면 폐기)
- ❌ **Hook System** (onCardOpen 등) (전면 폐기)
- ❌ **Event Bus** (OL.emit/on) (전면 폐기)
- ❌ Semantic Search / Knowledge Graph (v0.7 미구현, 슬롯만)
- ❌ 다중 언어 실제 번역 (v0.7은 i18n 키만)

## 부록 C — 왜 Action Layer만 남겼는가

OL Core v1 기획서는 Action / Event Bus / Hook 세 가지를 모두 권장했지만, v0.7은 Action Layer만 도입한다.

**이유**:

- **Event Bus는 Action Layer로 흡수 가능**: 모든 변경이 dispatch를 거치면, 컴포넌트는 store.subscribe만 하면 되고 서로 직접 호출할 일이 없다. "어떤 통신은 action으로, 어떤 통신은 event로?"라는 분기가 생기면 오히려 복잡해진다.
- **Hook System은 외부 확장점을 위한 장치**: 플러그인이 없으면 Hook을 호출당할 이유가 없다. 깔아두기만 하면 작동 검증이 안 된 채 v0.8로 넘어가서 죽은 코드가 된다.
- **단순성이 더 큰 가치**: OL은 작은 팀(1인) 프로젝트이고, 콘텐츠가 본질이다. 코어가 단순할수록 콘텐츠 작업에 집중할 수 있다.

향후 v0.8 이후 외부 확장 요구가 실제로 발생하면 그때 Event Bus·Hook를 추가하는 것이 적절하다. **추상화는 사용 사례가 두 번 이상 나타난 뒤에 추가한다.**

---

**작성**: Claude (with biwoom) **상태**: 최종 확정 v2. 결정 사항 7건 모두 반영, 플러그인 전면 폐기. **다음 문서**: Phase 0 작업 체크리스트 (착수 시 작성)