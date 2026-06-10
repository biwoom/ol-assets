# WORKS 페이지 추가수정

현재 문제의 원인과 해결 전략입니다.

---

## 원인

현재 방식은 사이드바가 **그리드 셀 안에 있어서** 닫힐 때 그리드 컬럼이 `240px → 40px`으로 줄어들면서 본문이 왼쪽으로 밀려오고, 사이드바도 같이 압축됩니다. 그래서 "본문 쪽으로 들어가는" 느낌이 납니다.

```
현재 (닫힘):
[40px][──────────── 본문이 왼쪽으로 밀림 ──────────][toc]
 ↑ 사이드바가 찌그러짐
```

원하는 동작:

```
원하는 (닫힘):
│40px│─────────── 본문이 제자리 ───────────│toc│
 ↑ 사이드바가 왼쪽 벽에 붙은 채 접힘, 본문은 안 밀림
```

---

## 전략: 사이드바를 그리드에서 분리 → `position: fixed`

사이드바를 그리드 셀이 아닌 **화면 왼쪽에 고정**하고, 본문 영역은 `margin-left`로 사이드바 공간을 확보합니다. 토글 시 `margin-left`만 전환합니다.

```
열림:
┌─────────────────────────────────────────────┐
│ [사이드바 240px]  [본문 margin-left:240px] [toc] │
│  position:fixed   그리드: 1fr 200px             │
└─────────────────────────────────────────────┘

닫힘:
┌─────────────────────────────────────────────┐
│ [40]  [본문 margin-left:40px]          [toc] │
│  ▶    그리드: 1fr 200px                      │
└─────────────────────────────────────────────┘
```

사이드바는 항상 왼쪽 벽에 고정. 본문은 margin만 변하므로 부드럽게 전환됩니다.

---

## 에이전트 전달 지침

```
[WORKS 사이드바 — fixed 방식으로 변경]

## 전략
사이드바를 그리드에서 분리.
position: fixed 로 화면 왼쪽에 고정.
본문 영역은 margin-left 로 사이드바 공간 확보.
토글 시 사이드바 width + 본문 margin-left 만 전환.

## CSS 수정 (ol-components.css)

### .ol-works-layout — 그리드에서 사이드바 제거

변경 전:
  grid-template-columns: 240px 1fr 200px;

변경 후:
  /* 사이드바는 fixed, 그리드는 본문+목차만 */
  display: grid;
  grid-template-columns: 1fr 200px;
  margin-left: 240px;   /* 사이드바 공간 확보 */
  transition: margin-left 200ms ease;
  min-height: calc(100vh - 64px);
  max-width: calc(1280px - 240px);

닫힘 상태:
  [data-works-sidebar="closed"] .ol-works-layout {
    margin-left: 40px;
    max-width: calc(1280px - 40px);
  }

### .ol-works-sidebar — fixed 배치

변경 전:
  position: sticky;
  top: 64px;

변경 후:
  position: fixed;
  left: 0;
  top: 64px;       /* 헤더 높이 */
  bottom: 0;
  width: 240px;
  z-index: 30;
  background: var(--ol-surface-3);
  border-right: 1px solid var(--ol-border);
  overflow: hidden;
  transition: width 200ms ease;

닫힘 상태:
  [data-works-sidebar="closed"] .ol-works-sidebar {
    width: 40px;
  }

### 사이드바 내부 컨텐츠 숨김 (닫힘)

  [data-works-sidebar="closed"] .ol-works-sidebar-scroll,
  [data-works-sidebar="closed"] .ol-works-sidebar-header > *:not(.ol-works-sidebar-toggle) {
    opacity: 0;
    pointer-events: none;
    transition: opacity 150ms ease;
  }

### 토글 버튼 위치

토글 버튼은 사이드바가 닫혔을 때에도 항상 보여야 함.
사이드바 header 우측에 위치.
닫힘 상태에서는 40px 폭 중앙 정렬:

  [data-works-sidebar="closed"] .ol-works-sidebar-header {
    justify-content: center;
    padding: 16px 8px 12px;
  }

### 반응형 수정

1100px 이하:
  목차 숨김
  .ol-works-layout {
    grid-template-columns: 1fr;
    margin-left: 240px;
  }
  [data-works-sidebar="closed"] .ol-works-layout {
    margin-left: 40px;
  }

900px 이하:
  사이드바를 fixed 유지하되 기본 닫힘, 오버레이 방식.
  .ol-works-layout { margin-left: 0; }
  .ol-works-sidebar {
    transform: translateX(-100%);
    width: 280px;
    z-index: 200;
    top: 0;         /* 모바일은 헤더 위로 덮음 */
    box-shadow: 4px 0 12px rgba(0,0,0,0.1);
  }
  .ol-works-sidebar[aria-hidden="false"] {
    transform: translateX(0);
  }

## HTML 구조 변경 (WorksLayout.astro)

사이드바를 .ol-works-layout 바깥으로 이동:

변경 전:
  <div class="ol-works-layout">
    <aside class="ol-works-sidebar">...</aside>
    <main>...</main>
  </div>

변경 후:
  <!-- 사이드바: fixed, 레이아웃 바깥 -->
  <aside class="ol-works-sidebar" id="works-sidebar">
    ...
  </aside>

  <!-- 본문: margin-left로 사이드바 공간 확보 -->
  <div class="ol-works-layout">
    <main class="ol-works-main">
      <slot />
    </main>
    <nav slot="toc" class="ol-works-toc">
      ...
    </nav>
  </div>

## 완료 조건

- [ ] 사이드바가 항상 화면 왼쪽 벽에 고정
- [ ] 닫힘 시 40px 폭으로 줄어들며 왼쪽 벽에 유지
- [ ] 닫힘 시 본문이 왼쪽으로 부드럽게 확장 (200ms)
- [ ] 열림 시 본문이 오른쪽으로 부드럽게 밀림
- [ ] 토글 버튼이 닫힘 상태에서도 보임
- [ ] 스크롤해도 사이드바 위치 유지 (fixed)
- [ ] 900px 이하: 오버레이 방식 동작 유지
- [ ] 다크모드 정상
- [ ] npm run build 무오류
```