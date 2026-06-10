# OL ATLAS v0.7 최종 개발 기획서

**버전**: Final v1.0
**작성일**: 2026-05-21
**전임 버전**: OL ATLAS v0.6
**프로젝트 단계**: prototype → platform 전환 (압축 사이클)
**예상 일정**: 5~9주 (일정 비제약 모드)

-----

## 0. 한 줄 요약

> v0.7은 OL Core v1 기획서의 **Phase A + B + C를 한 번에 압축**하는 대형 사이클이다.
> v0.6의 검증된 자산을 계승하면서, src→dist 빌드 분리·새 UI(PDF 아이디어)·상태/렌더/플러그인 인프라까지 동시에 정착시킨다. 일정보다 구조 정합성을 우선한다.

-----

## 1. v0.7의 목표

### 1.1 네 가지 축

```
1) 구조 축    개발/배포 분리 + 모듈화 + 패키지화
2) 런타임 축  Action Layer + Event Bus + Hook System + Render Scheduler
3) UI 축      PDF 아이디어 채택분 (카드보드 통합, 테이블뷰, 사이드바 숨김)
4) 확장 축    Plugin API + 사용자 붙여넣기 로딩 시스템
```

### 1.2 v0.7 완료의 정의(DoD)

- [ ] `src/` ES modules → `dist/ol-atlas.html` 단일 파일 빌드 정착 (esbuild)
- [ ] PDF 채택 UI 전체 작동 (헤더 슬림, 사이드바 숨김 기본, 탭 네비, 카드보드 통합, 테이블뷰)
- [ ] **모든 state 변경이 Action 경유**, **모든 view 갱신이 RenderQueue 경유**, **모든 컴포넌트 간 통신이 Event Bus 경유**
- [ ] **Hook System 작동**: 핵심 기능 일부가 내장 플러그인으로 구현되어 Hook 시스템 실증
- [ ] **Plugin API + 붙여넣기 로딩 UI 작동**: 사용자가 플러그인 JS 텍스트를 설정에서 등록 → localStorage 저장 → 부팅 시 평가·실행
- [ ] Dirty State + beforeunload + autosave 작동
- [ ] 카드 모달: 본문 readonly + 제목/태그 인라인 편집 + “편집→문서뷰”
- [ ] shadcn/ui 디자인 토큰·컴포넌트 매핑 일관 적용
- [ ] v0.6 → v0.7 마이그레이션 작동 (schemaVersion 6→7)
- [ ] i18n 키 분리 완료 (사전은 한국어만)

### 1.3 명시적 비목표 (Non-goals)

- **Semantic Search / Knowledge Graph**: 미구현 확정. 검색 인덱스 추상화 계층까지만 마련.
- **다중 언어 실제 번역**: 사전은 한국어만. EN/ZH/JA/ES는 v0.8 이후.
- **IndexedDB / PWA / Electron**: 채택 안 함. localStorage + 단일 HTML 유지.
- **런타임 CDN 라이브러리**: 채택 안 함.
- **분기 기록·기여자 추적**: 폐기. ORIGIN 하드코딩만 유지.
- **외부 파일 import 모델**: 채택 안 함. 플러그인은 “붙여넣기 + localStorage” 모델만.
- **플러그인 마켓플레이스**: 없음. 공유는 텍스트 복사·붙여넣기로.

-----

## 2. 확정된 결정 사항

|#|항목            |확정                                                             |
|-|--------------|---------------------------------------------------------------|
|1|**범위**        |C안 전면 + Plugin API 외부 로딩 완성. OL Core v1 Phase A+B+C 압축.        |
|2|**사이드바**      |PDF안 그대로. 데스크탑/모바일 기본 숨김, 햄버거 토글. 칼럼/그룹/태그 영역 제거. 검색바는 탭 네비 상단.|
|3|**카드 모달**     |본문 readonly + 제목/태그 인라인 편집 + “편집” 버튼 → 문서뷰.                    |
|4|**빌드 도구**     |esbuild.                                                       |
|5|**다중 언어**     |v0.7은 i18n 키 분리만, 사전 한국어만.                                     |
|6|**플러그인 로딩 모델**|사용자 붙여넣기 모델 (설정 UI → localStorage → 부팅 시 평가). 단일 HTML 철학 유지.   |
|7|**일정 정책**     |일정 비제약. 구조 정합성 우선.                                             |

-----

## 3. 새 UI 설계 — PDF 아이디어 정리

### 3.1 채택 — 그대로 반영

|PDF 아이디어               |설명                                                       |
|-----------------------|---------------------------------------------------------|
|**사이드바 기본 숨김 + 햄버거 토글**|데스크탑/모바일 동일                                              |
|**사이드바 단순화**           |칼럼·그룹·태그 영역 제거 → ABOUT, 휴지통, (문서뷰)카드 목록·목차, 저장/열기/다크모드/설정|
|**칸반 → 카드보드 통합**       |카드뷰 별도 전환 제거. 너비 토글(MAX/WIDE/NORMAL)                     |
|**리스트 → 테이블뷰**         |인라인 편집 + 칼럼별 검색 필터                                       |
|**탭 네비게이션**            |카드보드 칼럼 ↔ 테이블뷰 매칭. 각 탭은 해당 칼럼의 테이블                       |
|**로고 클릭 → 카드보드**       |홈 랜딩 폐기                                                  |
|**카드 모달**              |본문 readonly + 제목/태그 인라인 편집 + 편집→문서뷰                      |
|**메타 토글**              |“전체 / 제목 / 내용 / 태그” 토글로 카드 상단 메타 표시 제어                   |
|**새로고침 유실 경고**         |beforeunload + Dirty State                               |
|**카드보드 칼럼 순서 이동**      |칼럼 헤더 드래그                                                |
|**모달 팝업 시 배경 어둡게**     |overlay 적용                                               |
|**설정뷰 추가**             |신규. 테마, 플러그인 관리, i18n 미래 슬롯                              |
|**검색바 탭 상단으로**         |헤더에서 분리                                                  |

### 3.2 보류 — v0.7.x 또는 이후

|PDF 아이디어                    |v0.7 결정             |사유                    |
|----------------------------|--------------------|----------------------|
|**다중 언어 실제 번역(EN/ZH/JA/ES)**|i18n 키 분리만          |사전은 한국어만, 번역 품질 통제 필요 |
|**문서뷰 각주/원문박스/주석박스/메모**     |별도 작업(v0.7.x)       |에디터 확장은 콘텐츠 작업 본격화 시점에|
|**카드 본문 폭 좁게 + 이미지 확장**     |shadcn prose 폭으로 통일만|이미지 확장 토큰은 후속         |
|**문서뷰 태그 클릭 → 검색**          |v0.7.x              |검색 결과 모달 정리 선행        |
|**모듈 다운로드(외부)**             |채택 안 함              |붙여넣기 모델로 대체           |

### 3.3 와이어 정리

```
┌─────────────────────────────────────────────────────────────────┐
│ ☰  OL · ATLAS                              ⚙  🌗  💾  📂        │  헤더(56px)
├─────────────────────────────────────────────────────────────────┤
│ [너비: ●MAX ○WIDE ○NORMAL]   [검색 ⌘K]   토글: 전체/제목/내용/태그│  서브헤더
├─────────────────────────────────────────────────────────────────┤
│ [BOARD] [서원] [바라밀] [탄생] [출가] [성도] [전법] [열반]      │  탭 네비
├─────────────────────────────────────────────────────────────────┤
│ BOARD 탭: 모든 칼럼이 칸반 형태로                                │
│ 칼럼 탭: 해당 칼럼의 카드를 테이블 형태로                        │
└─────────────────────────────────────────────────────────────────┘
```

### 3.4 디자인 시스템

스타일 문서(`스타일 구현 정책 및 수정 로드맵.md`) + v0.6 메모리 자산 계승.

- HSL 토큰(neutral), 라이트/다크
- 시스템 폰트 + Pretendard
- shadcn 컴포넌트 매핑: Dialog, Badge, ToggleGroup, Tabs, Table, Command, Sonner, Popover, Select
- lucide 스타일 인라인 SVG

-----

## 4. 아키텍처 — 4계층 모델

v0.7의 핵심 변화. 한 번에 정착시킨다.

### 4.1 계층 구조

```
┌──────────────────────────────────────────────────────┐
│  UI Layer (views, components)                        │
│  - DOM 렌더링만 담당                                 │
│  - state 직접 수정 금지                              │
│  - 변경은 dispatch(action), 통신은 emit(event)       │
└────────────────────────┬─────────────────────────────┘
                         │ dispatch
                         ▼
┌──────────────────────────────────────────────────────┐
│  Action Layer                                        │
│  - 모든 state 변경의 단일 진입점                     │
│  - reducer 패턴 (state, action) → newState           │
│  - Hook 실행 지점 (beforeAction / afterAction)       │
└────────────────────────┬─────────────────────────────┘
                         │ mutate
                         ▼
┌──────────────────────────────────────────────────────┐
│  State Layer (S)                                     │
│  - cards, cols, settings, meta                       │
│  - localStorage persist (debounced)                  │
│  - dirty flag                                        │
└────────────────────────┬─────────────────────────────┘
                         │ subscribe
                         ▼
┌──────────────────────────────────────────────────────┐
│  Render Queue + Event Bus                            │
│  - queueRender(viewName) → rAF flush                 │
│  - OL.emit(event, payload) / OL.on(event, handler)   │
│  - 컴포넌트 간 직접 참조 제거                        │
└──────────────────────────────────────────────────────┘
```

### 4.2 디렉토리 구조

```
ol-atlas/
├── src/
│   ├── core/
│   │   ├── state.js              # S 객체, makeDefault, normalizeState
│   │   ├── action.js             # dispatch, reducer registry, action types
│   │   ├── store.js              # subscribe, getState, applyPatch
│   │   ├── event-bus.js          # OL.emit / OL.on / OL.off
│   │   ├── render-queue.js       # queueRender + rAF flush
│   │   ├── storage.js            # localStorage 추상화 (save/load/backup)
│   │   ├── schema.js             # schemaVersion + migrators (6→7)
│   │   ├── dirty.js              # markDirty / markClean / autosave debounce
│   │   ├── hook.js               # Hook 등록·실행 시스템
│   │   ├── origin.js             # ORIGIN 하드코딩
│   │   └── id.js                 # slug, uniqueSlug, imgId
│   │
│   ├── data/
│   │   ├── card.js               # normalizeCard, validators
│   │   ├── tag.js                # parseTag, prefix index, free tags
│   │   ├── markdown.js           # parseInline, parseMarkdown, stripMarkdown
│   │   └── search/
│   │       ├── index.js          # search 진입점 (계층 추상화)
│   │       ├── basic.js          # 단순 텍스트 검색 (v0.7 활성)
│   │       ├── tag-index.js      # 태그 색인
│   │       └── semantic.js       # 시멘틱 검색 (v0.7 미구현, 슬롯만)
│   │
│   ├── actions/                  # 각 도메인별 액션 정의
│   │   ├── card-actions.js       # CARD_CREATE, CARD_UPDATE, CARD_DELETE...
│   │   ├── column-actions.js     # COLUMN_CREATE, COLUMN_REORDER...
│   │   ├── view-actions.js       # VIEW_CHANGE, TAB_SELECT, BOARD_WIDTH...
│   │   ├── settings-actions.js   # SETTINGS_UPDATE, THEME_TOGGLE...
│   │   └── plugin-actions.js     # PLUGIN_INSTALL, PLUGIN_TOGGLE...
│   │
│   ├── ui/
│   │   ├── header.js
│   │   ├── sidebar.js            # 단순화된 사이드바
│   │   ├── tabs.js               # 탭 네비게이션
│   │   ├── cardboard.js          # 카드보드 (통합된 칸반)
│   │   ├── tableview.js          # 테이블뷰 (인라인편집 + 필터)
│   │   ├── docview.js            # 문서뷰
│   │   ├── about.js
│   │   ├── settings.js           # 신규: 설정뷰
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
│   ├── plugins/
│   │   ├── api.js                # OL.registerPlugin 공개 API
│   │   ├── loader.js             # 붙여넣기 코드 평가·로딩
│   │   ├── sandbox.js            # 플러그인 실행 컨텍스트 (제한된 API surface)
│   │   ├── registry.js           # 설치된 플러그인 메타 (localStorage)
│   │   └── builtin/              # 핵심 기능을 내장 플러그인으로 리팩토링
│   │       ├── search-plugin.js  # 검색 (실증용)
│   │       └── export-plugin.js  # 단일 HTML export
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

### 4.3 부팅 시퀀스

```js
// src/boot.js (의사 코드)
async function boot() {
  // 1. localStorage에서 state 로드 + schema 마이그레이션
  let raw = storage.load();
  raw = schema.migrate(raw);                 // v6 → v7 자동
  store.init(normalizeState(raw));

  // 2. Action Layer 활성화
  action.registerReducers(coreReducers);

  // 3. Event Bus + Render Queue 활성화
  bus.init();
  renderQueue.init();

  // 4. 내장 플러그인 등록
  builtinPlugins.forEach(p => pluginApi.register(p));

  // 5. 사용자 플러그인 로딩 (localStorage → 평가 → 등록)
  await pluginLoader.loadUserPlugins();

  // 6. UI 마운트 (모든 view 등록)
  ui.mount();

  // 7. Hook: onBoot
  hooks.run('onBoot', { state: store.getState() });

  // 8. 첫 렌더
  renderQueue.flush();
}
```

-----

## 5. Plugin API — 사용자 붙여넣기 모델

### 5.1 사용자 흐름

```
1. 사용자가 어디선가 플러그인 JS 코드를 복사
   (텍스트 형태로 공유됨, 파일 아님)
2. OL 설정뷰 → "플러그인 추가" → 텍스트 영역에 붙여넣기
3. 이름·설명·신뢰 확인 후 "설치" 클릭
4. localStorage에 코드 + 메타 저장
5. 다음 부팅부터 자동 평가 + 등록
6. 설정뷰에서 켜기/끄기/제거 가능
```

### 5.2 Plugin API 표면

```js
OL.registerPlugin({
  id: 'buddha-story',           // 고유 ID
  name: '붓다스토리 패키지',
  version: '0.1.0',
  
  // 라이프사이클
  onInstall(ctx) {},
  onEnable(ctx) {},
  onDisable(ctx) {},
  
  // Hook 등록
  hooks: {
    onCardOpen(card, ctx) {},
    onCardSave(card, ctx) {},
    onSidebarRender(sidebarCtx) {},
    onSearch(query, ctx) {},
    onBoot(ctx) {},
    onViewChange(viewName, ctx) {},
  },
  
  // 커맨드 등록 (⌘K 팔레트)
  commands: [
    { id: 'bs:open-buddha', label: '붓다 노드 열기', run(ctx) {} }
  ],
  
  // 추가 View 등록 (장기, v0.8 본격화)
  views: [],
});
```

### 5.3 Sandbox 정책

플러그인이 `document.querySelector` 직접 호출 같은 짓을 못 하게 차단하기는 어렵지만(JS 동적 평가의 본질적 한계), **권장 표면은 제한**한다.

```js
// 플러그인에 노출되는 ctx 객체
ctx = {
  // 읽기 전용 state 접근
  getState() {},
  getCard(id) {},
  
  // 변경은 반드시 dispatch
  dispatch(action) {},
  
  // 이벤트
  emit(event, payload) {},
  on(event, handler) {},
  
  // UI
  toast(msg) {},
  openDialog(opts) {},
  
  // 저장 (플러그인별 namespace)
  storage: {
    get(key) {},
    set(key, val) {},
  },
};
```

**중요**: `document`, `window`, `S` 같은 글로벌 직접 접근은 “비권장”이지 “차단 불가”. 사용자는 자신이 설치한 플러그인의 코드를 신뢰한다는 전제. **설치 UI에서 “이 플러그인은 임의 코드를 실행합니다” 경고 명시**.

### 5.4 내장 플러그인 (실증용)

Hook System이 실제로 작동하는지 검증하기 위해 핵심 기능 중 일부를 내장 플러그인으로 리팩토링.

- **search-plugin**: ⌘K 커맨드 + onSearch hook 등록. 검색 결과 모달 제공.
- **export-plugin**: 단일 HTML export 기능을 플러그인으로. 커맨드 + onBoot에서 export 버튼 등록.

이 둘이 작동하면 Hook 시스템이 실증된 것. 외부 플러그인이 같은 인터페이스로 동작 가능.

-----

## 6. 데이터 모델 — schema v7

### 6.1 변경점

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

S.plugins = {                        // 신규
  installed: [
    {
      id: 'buddha-story',
      name: '...',
      version: '0.1.0',
      enabled: true,
      code: '...',                   // 사용자가 붙여넣은 원본 JS
      installedAt: ISO,
    }
  ],
  storage: {                         // 플러그인별 namespace 저장소
    'buddha-story': { ... }
  }
}
```

### 6.2 마이그레이션

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
    s.plugins = { installed: [], storage: {} };
    return s;
  },
};

// 부팅 시 v6 백업을 localStorage에 자동 저장 (ol_backup_v6)
```

-----

## 7. 작업 목록 (WBS)

각 Phase는 자기완결적 단위. 일정 비제약이지만 의존성 순서는 엄격히 지킴.

### Phase 0 — 빌드 셋업 + 모듈 분해 (2~4일)

|#  |작업                                                            |산출물                  |
|---|--------------------------------------------------------------|---------------------|
|0.1|v0.6 HTML을 `src/` 모듈로 수작업 분해                                  |`src/**` 초기 구조       |
|0.2|esbuild 기반 `build/build.mjs` 작성                               |번들 JS 생성             |
|0.3|CSS concat + 인라이닝 (`build/inline.mjs`)                        |단일 HTML 생성           |
|0.4|`__STATIC_HTML__` 캡처 + `__LOADED_DATA_B64__` 자기참조 보호 패턴 빌드에 통합|export 작동            |
|0.5|`npm run dev` (vite 또는 esbuild –servedir) / `npm run build` 명령|README + package.json|
|0.6|v0.6 기능 동등성 회귀 테스트 (manual QA 체크리스트)                          |Phase 1 진입 게이트       |

### Phase 1 — 런타임 인프라 (4~6일)

**핵심**. 이 단계가 끝나야 이후 모든 작업이 새 패턴으로 진행 가능.

|#  |작업                                                                   |산출물               |
|---|---------------------------------------------------------------------|------------------|
|1.1|`core/store.js` — getState, applyPatch, subscribe                    |store 작동          |
|1.2|`core/action.js` — dispatch, reducer registry, action types          |dispatch 작동       |
|1.3|`core/event-bus.js` — emit/on/off                                    |bus 작동            |
|1.4|`core/render-queue.js` — queueRender + rAF flush                     |다중 render 1회 합치기  |
|1.5|`core/hook.js` — Hook 등록/실행 (beforeAction, afterAction, custom hooks)|hook 호출 작동        |
|1.6|`core/dirty.js` — markDirty + markClean + autosave debounce 1000ms   |dirty flag + 자동 저장|
|1.7|beforeunload 핸들러                                                     |새로고침 경고           |
|1.8|`core/schema.js` — v6→v7 migrator + v6 백업                            |마이그레이션 작동         |
|1.9|v0.6 기능을 새 런타임 위로 어댑팅 (직접 render 호출 모두 제거)                           |grep으로 검증         |

**검증 게이트**:

- `grep -r "renderCards\|renderKanban\|renderList(" src/ui/` 결과 0건 (모두 queueRender 경유)
- `grep -r "S\.cards\.push\|S\.cards\[" src/ui/` 결과 0건 (모두 dispatch 경유)

### Phase 2 — Action 도메인 정의 (2~3일)

|#  |작업                                                                         |산출물    |
|---|---------------------------------------------------------------------------|-------|
|2.1|`actions/card-actions.js` (CREATE/UPDATE/DELETE/MOVE)                      |카드 액션  |
|2.2|`actions/column-actions.js` (CREATE/RENAME/REORDER/DELETE)                 |칼럼 액션  |
|2.3|`actions/view-actions.js` (VIEW_CHANGE/TAB_SELECT/BOARD_WIDTH/META_TOGGLE) |뷰 액션   |
|2.4|`actions/settings-actions.js` (SETTINGS_UPDATE/THEME_TOGGLE/SIDEBAR_TOGGLE)|설정 액션  |
|2.5|`actions/plugin-actions.js` (PLUGIN_INSTALL/TOGGLE/REMOVE/UPDATE_STORAGE)  |플러그인 액션|

### Phase 3 — Plugin API + Loader (4~6일)

|#  |작업                                                 |산출물          |
|---|---------------------------------------------------|-------------|
|3.1|`plugins/api.js` — OL.registerPlugin 표면 정의         |API 표면       |
|3.2|`plugins/sandbox.js` — ctx 객체 (제한된 surface)        |sandbox 객체   |
|3.3|`plugins/registry.js` — installed 플러그인 메타 관리       |registry 작동  |
|3.4|`plugins/loader.js` — 코드 평가(`new Function`) + 에러 격리|사용자 코드 실행    |
|3.5|설정뷰에 “플러그인 추가” UI (붙여넣기 + 미리보기 + 경고)               |설치 UI        |
|3.6|설정뷰에 “설치된 플러그인 목록” (켜기/끄기/제거/코드 보기)                |관리 UI        |
|3.7|`plugins/builtin/search-plugin.js` — 검색을 플러그인으로    |hook 시스템 실증 1|
|3.8|`plugins/builtin/export-plugin.js` — export를 플러그인으로|hook 시스템 실증 2|
|3.9|플러그인 평가 실패 시 격리 (다른 플러그인·코어 영향 없음)                 |에러 격리 검증     |

### Phase 4 — 사이드바 단순화 (2일)

|#  |작업                                          |산출물        |
|---|--------------------------------------------|-----------|
|4.1|사이드바에서 칼럼·그룹·태그 영역 코드 제거                    |sidebar 단순화|
|4.2|햄버거 토글 (헤더 좌상단) + `settings.sidebarOpen` 바인딩|토글 동작      |
|4.3|사이드바 콘텐츠: ABOUT / 휴지통 / (문서뷰)카드 목록 + 목차     |항목 정렬      |
|4.4|저장 / 열기 / 다크모드 / 설정 버튼을 사이드바로 이동            |버튼 이동      |
|4.5|모바일 오버레이, 데스크탑 슬라이드, 햄버거 오버레이 z-index(25)   |반응형        |

### Phase 5 — 탭 + 카드보드 통합 (4~6일)

|#  |작업                                       |산출물    |
|---|-----------------------------------------|-------|
|5.1|`components/tabs.js` — shadcn Tabs       |탭 컴포넌트 |
|5.2|탭 정의: BOARD + 각 칼럼 (자동 생성)               |탭 목록   |
|5.3|`ui/cardboard.js` — 칸반 + 카드그리드 통합        |카드뷰 폐기 |
|5.4|너비 토글 (MAX/WIDE/NORMAL) → `--board-col-w`|너비 변경  |
|5.5|메타 토글 (전체/제목/내용/태그)                      |토글 동작  |
|5.6|카드 상단 메타 + 하단 연결문서                       |카드 레이아웃|
|5.7|카드보드 칼럼 순서 이동 (drag handle)              |칼럼 재정렬 |

### Phase 6 — 테이블뷰 (4~6일)

|#  |작업                                    |산출물       |
|---|--------------------------------------|----------|
|6.1|`components/table.js` — shadcn Table  |테이블 컴포넌트  |
|6.2|`ui/tableview.js` — 탭이 칼럼일 때 해당 카드만 표시|탭 ↔ 테이블 매칭|
|6.3|인라인 편집 (제목, 내용 요약, 태그)                |셀 편집      |
|6.4|칼럼별 검색 필터 (제목/내용/태그 셀의 🔍 팝오버)         |필터 동작     |
|6.5|그룹 행 (Group A / Group B)              |그룹별 정렬    |
|6.6|“문서뷰” 칼럼 → 행 클릭 시 문서뷰 진입              |진입 동작     |

### Phase 7 — 카드 모달 + 검색 + 헤더 (2~3일)

|#  |작업                                         |산출물             |
|---|-------------------------------------------|----------------|
|7.1|모달 본문을 readonly 렌더로 변경                     |본문 미리보기         |
|7.2|제목 인라인 편집 (contenteditable 또는 inline Input)|제목 즉시 편집        |
|7.3|태그 인라인 편집 (배지 + 추가/삭제)                     |태그 즉시 편집        |
|7.4|“편집” 버튼 → 문서뷰 라우팅                          |본문 편집은 문서뷰      |
|7.5|모달 overlay 어둡게                             |shadcn Dialog 표준|
|7.6|제목/태그 변경 → dispatch + markDirty + autosave |자동 저장 연동        |
|7.7|검색바를 탭 네비 상단으로 이동                          |위치 변경           |
|7.8|`components/command.js` — ⌘K 트리거           |키보드 단축키         |
|7.9|헤더 슬림화 (좌: 햄버거+로고, 우: 설정/테마)               |헤더 정리           |

### Phase 8 — 설정뷰 (2~3일)

|#  |작업                               |산출물    |
|---|---------------------------------|-------|
|8.1|`ui/settings.js` — 설정뷰 레이아웃      |설정 페이지 |
|8.2|테마 설정 섹션 (system/light/dark)     |테마 토글  |
|8.3|플러그인 관리 섹션 (Phase 3.5, 3.6 통합 지점)|플러그인 UI|
|8.4|언어 설정 슬롯 (v0.7은 한국어만, UI는 미래 대비) |슬롯 마련  |
|8.5|데이터 관리 (백업·복원·초기화)               |데이터 도구 |

### Phase 9 — i18n 키 분리 (2~3일)

|#  |작업                                  |산출물    |
|---|------------------------------------|-------|
|9.1|`i18n/t.js` — `t(key, params?)` 함수  |t 함수   |
|9.2|`i18n/ko.js` — 한국어 사전               |사전     |
|9.3|UI 코드의 모든 하드코딩 한국어 → `t(...)` 치환    |키 추출 완료|
|9.4|`i18n/KEYS.md` — 등록된 키 목록 자동 생성 스크립트|문서     |

### Phase 10 — 마무리 (3~4일)

|#   |작업                                           |산출물          |
|----|---------------------------------------------|-------------|
|10.1|v0.6 데이터 import 회귀 테스트 (실제 파일 3종 이상)         |마이그레이션 검증    |
|10.2|grep 검증 (직접 render·state 수정 0건)              |패턴 일관성       |
|10.3|shadcn 토큰 일관성 lint (하드코딩 색상 0건)              |디자인 일관성      |
|10.4|모바일 QA (iOS Safari, Android Chrome)          |반응형 검증       |
|10.5|플러그인 실증: 가상의 외부 플러그인 작성 → 설치 → 작동            |Plugin API 검증|
|10.6|`dist/ol-atlas.html` 콘텐츠 시연 (OL 붓다스토리 1차 PoC)|OL BOOK 준비   |

-----

## 8. 위험 요소 및 대응

|위험                                                    |등급       |대응                                                                       |
|------------------------------------------------------|---------|-------------------------------------------------------------------------|
|빌드 분리 중 export 로직 자기참조 정규식 깨짐                         |중        |메모리 패턴(`'__LOADED' + '_DATA_B64__'` 분리 + `new RegExp(...)`)을 빌드 출력 검사에 포함|
|CSS concat 시 주석 누락 → 규칙 무효화                           |중        |빌드 후 CSS 파싱 검증 (postcss-parser 등)                                        |
|Phase 1 런타임 인프라 도입 중 v0.6 기능 회귀                       |**높음**   |Phase 0 완료 후 v0.6 동등성 회귀 테스트를 게이트로. Phase 1을 작은 단위 PR로 쪼개기               |
|사용자 플러그인 코드 평가의 보안 위험                                 |**높음**   |설치 UI에 명시적 경고. 코드 일부 미리보기 강제. 플러그인 실행 실패는 격리. Sandbox는 권장이지 강제 아님 명시     |
|플러그인 평가 실패가 부팅 자체를 막음                                 |중        |`loader.js`에서 try/catch + 실패한 플러그인 자동 비활성화 + 사용자 통보                      |
|Hook 호출 무한 루프 (플러그인이 dispatch → afterAction → 같은 플러그인)|중        |Hook 호출 깊이 제한 (예: 8) + 순환 감지                                             |
|마이그레이션 실패로 사용자 데이터 손실                                 |낮음 (영향 큼)|v6→v7 시 `ol_backup_v6` 자동 백업 + 복원 UI                                     |
|Action Layer 도입으로 코드량 폭증                              |중        |액션은 도메인별 파일로 분리. action type을 enum으로 통일                                  |
|iOS Safari 다크모드 + 햄버거 + 모달 z-index 충돌                 |중        |위계: hamburger overlay 25, sidebar 30, header 50, modal 100, toast 200    |
|OL Core v1 Phase A+B+C 압축으로 회귀 사이클 폭증                 |**높음**   |일정 비제약이지만, Phase 1·3을 통과 못 하면 후속 Phase 진입 금지. 게이트 엄격 적용                  |

-----

## 9. 검증 게이트

Phase 진입 전 충족 조건. 게이트 미달 시 다음 Phase 금지.

|Gate           |조건                                        |
|---------------|------------------------------------------|
|**Phase 1 진입** |Phase 0 완료 + dist가 v0.6과 기능 동등 (manual QA)|
|**Phase 2 진입** |Phase 1 완료 + 런타임 자체 단위 테스트 통과             |
|**Phase 4 진입** |Phase 2 완료 + Phase 3 진행 가능 (병렬 가능)        |
|**Phase 7 진입** |Phase 5, 6 모두 완료                          |
|**Phase 10 진입**|Phase 3 내장 플러그인 2개가 실제로 hook 시스템 통해 작동    |
|**v0.7 릴리스**   |DoD 9개 항목 전부 체크 + 위험 대응책 전부 적용            |

-----

## 10. OL BOOK 세대 준비

v0.7 완료 시점에 OL BOOK 콘텐츠 탑재 관점에서 준비되는 것:

1. **읽기 흐름 우선 UI**: 사이드바 기본 숨김 + 너비 토글로 읽기 화면 확보
2. **문서뷰 중심 편집**: 카드 모달 절충안으로 “쓰기 = 문서뷰” 정책 정착
3. **빌드 분리**: `dist/ol-book-buddha-story.html` 같은 변형 산출물 생성 가능
4. **schemaVersion 시스템**: 향후 카드 관계 필드 추가가 안전
5. **shadcn 일관성**: 콘텐츠 패키지에서 UI 재발명 불필요
6. **Plugin API**: OL BOOK별 특수 기능을 플러그인으로 분리 가능 (예: 붓다스토리 인물 네트워크 패널)
7. **i18n 인프라**: 한국어→다국어 확장이 코드 변경 없이 사전 추가만으로 가능

-----

## 11. 일정 추정

총 **5~9주** (단독 작업, 일정 비제약 모드).

|Phase          |일수        |
|---------------|----------|
|0. 빌드 셋업       |2~4       |
|1. 런타임 인프라     |4~6       |
|2. Action 도메인  |2~3       |
|3. Plugin API  |4~6       |
|4. 사이드바 단순화    |2         |
|5. 탭 + 카드보드    |4~6       |
|6. 테이블뷰        |4~6       |
|7. 모달 + 검색 + 헤더|2~3       |
|8. 설정뷰         |2~3       |
|9. i18n 키 분리   |2~3       |
|10. 마무리        |3~4       |
|**합계**         |**31~46일**|

일정 비제약이므로 게이트 통과 시점을 기준으로 진행. 압축하지 않음.

-----

## 12. 즉시 다음 행동

1. **본 최종 기획서 승인.**
2. Phase 0 착수: v0.6 HTML을 `src/` 구조로 분해하면서 `build/build.mjs` 동시 작성.
3. Phase 0 완료 시점에 `dist/ol-atlas.html`이 v0.6과 기능 동등함을 확인. 이게 Phase 1 게이트.
4. Phase 1 런타임 인프라 도입 — 가장 위험한 구간. 작은 PR로 쪼개고 게이트 엄격 적용.
5. 이후 Phase 2~10 순차 진행. Phase 3과 Phase 4는 의존성 없으므로 병렬 가능.

-----

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

- 분기 기록 / 기여자 추적
- IndexedDB / PWA / Electron / 런타임 CDN 라이브러리
- 온보딩 플로우 / 프로필 페이지 / 변경 이력
- React / Vue / Solid 도입
- 외부 플러그인 파일 import 모델
- 플러그인 마켓플레이스
- Semantic Search / Knowledge Graph (v0.7 미구현, 슬롯만)
- 다중 언어 실제 번역 (v0.7은 i18n 키만)

## 부록 C — Plugin API 사용 예시 (참고)

```js
// 사용자가 설정뷰에 붙여넣는 예시 코드
OL.registerPlugin({
  id: 'buddha-timeline',
  name: '붓다 연표 패널',
  version: '0.1.0',
  
  hooks: {
    onSidebarRender(ctx) {
      // ctx.addPanel(...) 같은 sandbox API 사용
      ctx.addPanel({
        id: 'buddha-timeline',
        title: '붓다 연표',
        render: () => {
          const cards = ctx.getState().cards
            .filter(c => c.tags.some(t => t.startsWith('시기:')))
            .sort(/* ... */);
          return /* HTML */;
        }
      });
    },
    
    onCardOpen(card, ctx) {
      if (card.tags.includes('인물:붓다')) {
        ctx.toast('붓다 관련 카드입니다');
      }
    },
  },
  
  commands: [
    {
      id: 'bt:show-timeline',
      label: '붓다 연표 보기',
      run(ctx) { ctx.dispatch({ type: 'VIEW_CHANGE', view: 'sidebar:buddha-timeline' }); }
    }
  ],
});
```

-----

**작성**: Claude (with biwoom)
**상태**: 최종 확정. 결정 사항 7건 모두 반영 완료.
**다음 문서**: Phase 0 작업 체크리스트 (착수 시 작성)