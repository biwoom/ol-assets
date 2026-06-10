## Phase 3 이후 현 CSS 상태 보고서 — OL HOME

### 1. CSS 파일 구조

|파일|역할|
|---|---|
|`styles/tokens.css`|디자인 토큰 (색상, 폰트, 간격, 반경, 그림자)|
|`styles/global.css`|임포트 진입점 (Tailwind → Basecoat → tokens → ol-components)|
|`styles/ol-components.css`|전체 컴포넌트 스타일 (1364줄)|

컴포넌트 파일(`*.astro`)에는 `<style>` 블록 없음 — **모든 스타일이 `ol-components.css` 단일 파일에 집중**.

---

### 2. 디자인 토큰 (tokens.css)

- **색상**: `--ol-bg`, `--ol-surface`, `--ol-surface-2/3`, `--ol-border/border-strong`, `--ol-ink`, `--ol-ink-2`, `--ol-muted`, `--ol-subtle`
- **폰트**: `--ol-font-sans` (Inter/Pretendard/Noto Sans KR), `--ol-font-mono` (JetBrains Mono)
- **간격**: `--ol-sp-1~12` (4px~48px)
- **반경**: `--ol-r-sm`(6px), `--ol-r`(8px), `--ol-r-lg`(14px)
- **다크모드**: `.dark` 클래스로 토큰 재정의 (body/html 미디어 쿼리 방식 아님)

---

### 3. 데스크탑 레이아웃 현황

#### 3-1. 공통 컨테이너

```css
.ol-container  → max-width: 1200px, padding: 0 32px
.ol-hero       → padding: 96px 0 64px, 내부 max-width: 920px
.ol-section    → padding: 80px 0
```

#### 3-2. 헤더

```css
.ol-header-inner → height: 64px, sticky top:0
.ol-nav          → flex, gap 4px (데스크탑에서만 표시)
.ol-header-right → flex, gap 6px (검색 버튼 + 다크모드 토글 등)
```

#### 3-3. 그리드 시스템

|클래스|데스크탑|
|---|---|
|`.ol-grid-2`|2컬럼|
|`.ol-grid-3`|3컬럼|
|`.ol-grid-4`|4컬럼|
|`.ol-stats`|4컬럼|
|`.ol-footer-grid`|`1.4fr 1fr 1fr 1fr`|
|`.ol-post`|`220px 1fr`|
|`.ol-entity-list`|3컬럼|
|`.ol-principle`|`80px 1fr`|

#### 3-4. Hero

```css
h1 → font-size: 64px, letter-spacing: -0.035em
.ol-lead → font-size: 18px, max-width: 62ch
```

#### 3-5. Works 레이아웃 (사이드바+본문)

```css
.ol-works-outer   → display: flex, max-width: 1200px, min-width: 1200px  ⚠️
.ol-works-sidebar → position: sticky, width: 240px, top: 64px
.ol-works-layout  → flex: 1, min-width: 900px  ⚠️
.ol-works-main    → padding: 48px 56px
.ol-works-layout--toc → grid: 1fr 200px (TOC 포함 시)
```

#### 3-6. Search Modal (데스크탑)

```css
.ol-search-modal → width: min(560px, calc(100vw-32px)), max-height: min(480px, 70vh)
overlay → padding-top: min(20vh, 160px), align-items: flex-start
```

---

### 4. 반응형 브레이크포인트 현황

#### `@media (max-width: 1100px)` — Works TOC 숨김

```css
.ol-works-layout--toc → grid-template-columns: 1fr
.ol-works-toc         → display: none
```

#### `@media (max-width: 900px)` — 태블릿/모바일 공통

|대상|변경|
|---|---|
|`.ol-grid-3`, `.ol-grid-4`|2컬럼|
|`.ol-grid-2`|1컬럼|
|`.ol-hero h1`|40px|
|`.ol-footer-grid`|1fr 1fr|
|`.ol-nav`|`display: none` (햄버거 없음)|
|`.ol-post`|1컬럼|
|`.ol-stats`|2컬럼|
|`.ol-container`|padding: 0 20px|
|`.ol-entity-list`|2컬럼|
|`.ol-works-outer`|`display: block`|
|`.ol-works-sidebar`|`position: fixed`, width: 280px, `translateX(-100%)` 오버레이 방식|
|`.ol-sidebar-toggle`|`display: flex` (모바일 사이드바 열기 버튼)|
|`.ol-works-main`|padding: 32px 24px|

#### `@media (max-width: 600px)` — 모바일 소형

|대상|변경|
|---|---|
|`.ol-grid-3`, `.ol-grid-4`|1컬럼|
|`.ol-hero`|padding: 64px 0 40px|
|`.ol-hero h1`|32px|
|`.ol-stats`|2컬럼 유지|
|`.ol-entity-list`|1컬럼|
|`.ol-works-main`|padding: 24px 16px|
|`.ol-search-overlay`|padding-top: 0, align-items: stretch|
|`.ol-search-modal`|width: 100%, border-radius: 0 (풀스크린)|

---

### 5. 현재 문제점 / 조정이 필요한 부분

|항목|상태|내용|
|---|---|---|
|`min-width: 1200px` on `.ol-works-outer`|⚠️ 위험|900px 이하 미디어쿼리에서 `display:block`으로 덮지만, 가로 스크롤 발생 가능|
|`min-width: 900px` on `.ol-works-layout`|⚠️ 위험|모바일에서 레이아웃이 강제로 900px 이상으로 확장됨|
|`.ol-nav display:none`|⚠️ 불완전|모바일 햄버거 메뉴 없음, 네비게이션 완전 소실|
|`.ol-stats` 600px에서 2컬럼|중립|4개 항목이 2x2로 배치 — 더 좁게 가려면 1컬럼 필요|
|`.ol-manifest` padding: 48px|중립|모바일 반응형 미지정|
|`.ol-post` (blog)|⚠️ 불완전|900px에서 1컬럼 전환되나 h3 font-size 미조정|
|`.ol-product-card` min-height: 240px|중립|모바일에서 과도하게 길어질 수 있음|
|`.ol-hero .ol-lead` 18px|중립|600px 이하 font-size 미조정|

---

### 6. 인라인 스타일이 있는 페이지 (클래스 없이 직접 지정)

- `OLFooter.astro` — `max-width: 32ch` (소개 문구)
- `atlas.astro` — `max-width: 48ch`, `50ch`
- `ai.astro` — 채팅 버블 `max-width: 80%/90%`
- `design/[slug].astro` — `max-width: 800px`
- `blog/[slug].astro` — `max-width: 720px`
- `works/index.astro` — `max-width: 52ch`

---

어떤 영역부터 조정할지 알려주시면 바로 작업하겠습니다.