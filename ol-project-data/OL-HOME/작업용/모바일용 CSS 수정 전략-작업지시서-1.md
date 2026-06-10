# 모바일용 CSS 수정 전략-작업지시서-1

# OL HOME — 모바일 CSS 긴급 수정 작업지시서
## 1순위: WORKS min-width 제거 + 2순위: 헤더 모바일 메뉴

> **전제**: Phase 3 완료 상태, `ol-components.css` 1364줄
> **목표**: 모바일에서 가로 스크롤 제거 + 네비게이션 소실 해결
> **참조**: Phase 3 CSS 상태 보고서

---

## 에이전트 필독 — 수정 원칙

```
1. ol-components.css 만 수정. 컴포넌트 astro 파일은 최소한만.
2. OL 디자인 토큰 (var(--ol-*)) 사용. 하드코딩 색상 금지.
3. 기존 데스크탑 스타일 건드리지 않음. @media 안에서만 추가/덮어쓰기.
4. 다크모드(.dark) 대응 반드시 포함.
5. 새 클래스는 .ol- 접두어.
```

---

## TASK 1. WORKS min-width 제거 (가로 스크롤 해결)

### 문제

```css
/* 현재 — 가로 스크롤의 원인 */
.ol-works-outer   { min-width: 1200px; }
.ol-works-layout  { min-width: 900px;  }
```

모바일에서 이 두 규칙 때문에 페이지가 강제로 넓어져 가로 스크롤이 발생합니다.
900px 이하 미디어쿼리에서 `display: block`으로 덮고 있지만,
미디어쿼리 적용 전에 min-width가 먼저 계산되어 의미가 없습니다.

### 수정

`ol-components.css`에서 아래 두 속성을 찾아 **제거하거나 변경**합니다.

```css
/* ── 변경 전 ── */
.ol-works-outer {
  /* ... 다른 속성들 ... */
  min-width: 1200px;    /* ← 삭제 */
  max-width: 1200px;    /* 유지 */
}

.ol-works-layout {
  /* ... 다른 속성들 ... */
  min-width: 900px;     /* ← 삭제 */
}

/* ── 변경 후 ── */
.ol-works-outer {
  /* ... 다른 속성들 ... */
  /* min-width 삭제됨 */
  max-width: 1200px;
  width: 100%;          /* ← 추가: 화면 너비에 맞게 */
}

.ol-works-layout {
  /* ... 다른 속성들 ... */
  /* min-width 삭제됨 */
  width: 100%;          /* ← 추가 */
}
```

### 검증

수정 후 `npm run dev` → 브라우저 375px 폭에서:
- [ ] `/works` 페이지에 가로 스크롤바 없음
- [ ] `/works/{문서id}` 개별 문서에도 가로 스크롤바 없음
- [ ] 데스크탑(1280px)에서 기존 레이아웃 변화 없음

---

## TASK 2. 헤더 모바일 메뉴 — 하단 시트(Bottom Sheet) 방식

### 2-1. OLHeader.astro 수정

#### 햄버거 버튼 추가

`.ol-header-right` 안에, 기존 검색/다크모드 버튼들 **앞에** 햄버거 버튼을 추가합니다.
이 버튼은 데스크탑에서 숨겨지고 모바일에서만 나타납니다.

```astro
<!-- .ol-header-right 내부, 맨 앞에 추가 -->
<button
  class="ol-mobile-menu-trigger"
  id="ol-mobile-menu-trigger"
  aria-label="메뉴 열기"
  aria-expanded="false"
>
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
    <line x1="4" y1="6" x2="20" y2="6"/>
    <line x1="4" y1="12" x2="20" y2="12"/>
    <line x1="4" y1="18" x2="20" y2="18"/>
  </svg>
</button>
```

#### 하단 시트 HTML 추가

`</header>` 닫기 태그 바로 아래에 하단 시트 마크업을 추가합니다.

```astro
<!-- 모바일 하단 시트 메뉴 -->
<div class="ol-mobile-overlay" id="ol-mobile-overlay" aria-hidden="true">
  <nav class="ol-mobile-sheet" id="ol-mobile-sheet" role="navigation" aria-label="모바일 메뉴">

    <!-- 드래그 핸들 (시각적 힌트) -->
    <div class="ol-mobile-sheet-handle"></div>

    <!-- 메뉴 링크 -->
    <div class="ol-mobile-sheet-links">
      {navItems.map(item => (
        <a
          href={item.href}
          class:list={['ol-mobile-sheet-link', { active: currentPath === item.href || (item.href !== url('/') && currentPath.startsWith(item.href)) }]}
        >
          {item.label}
        </a>
      ))}

      <!-- 구분선 -->
      <div class="ol-mobile-sheet-divider"></div>

      <!-- 하단 보조 링크 -->
      <a href={url('/blog')} class="ol-mobile-sheet-link ol-mobile-sheet-link--sub">BLOG</a>
      <a
        href="https://github.com/biwoom"
        class="ol-mobile-sheet-link ol-mobile-sheet-link--sub"
        target="_blank"
        rel="noopener noreferrer"
      >
        GitHub
        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-left: 4px;">
          <path d="M7 17 17 7"/><path d="M7 7h10v10"/>
        </svg>
      </a>
    </div>

    <!-- 닫기 버튼 -->
    <button class="ol-mobile-sheet-close" id="ol-mobile-sheet-close" aria-label="메뉴 닫기">
      닫기
    </button>

  </nav>
</div>
```

#### 하단 시트 스크립트 추가

`</header>` 아래 또는 기존 `<script>` 블록 안에 추가합니다.

```html
<script>
  // 모바일 메뉴 하단 시트
  const trigger = document.getElementById('ol-mobile-menu-trigger');
  const overlay = document.getElementById('ol-mobile-overlay');
  const sheet = document.getElementById('ol-mobile-sheet');
  const closeBtn = document.getElementById('ol-mobile-sheet-close');

  function openMobileMenu() {
    overlay?.setAttribute('aria-hidden', 'false');
    trigger?.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileMenu() {
    overlay?.setAttribute('aria-hidden', 'true');
    trigger?.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  trigger?.addEventListener('click', openMobileMenu);
  closeBtn?.addEventListener('click', closeMobileMenu);

  // 오버레이(배경) 클릭으로 닫기
  overlay?.addEventListener('click', (e) => {
    if (e.target === overlay) closeMobileMenu();
  });

  // ESC 키로 닫기
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && overlay?.getAttribute('aria-hidden') === 'false') {
      closeMobileMenu();
    }
  });

  // 링크 클릭 시 자동 닫기
  sheet?.querySelectorAll('.ol-mobile-sheet-link').forEach(link => {
    link.addEventListener('click', () => {
      closeMobileMenu();
    });
  });
</script>
```

### 2-2. ol-components.css — 모바일 메뉴 스타일 추가

아래 전체를 `ol-components.css` 하단(기존 `@media` 규칙 근처)에 추가합니다.

```css
/* ============================================================
   OL Mobile Menu — Bottom Sheet
   ============================================================ */

/* 햄버거 버튼 (데스크탑에서 숨김) */
.ol-mobile-menu-trigger {
  display: none;       /* 데스크탑: 숨김 */
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  color: var(--ol-ink, #0a0a0a);
  cursor: pointer;
  border-radius: var(--ol-r, 8px);
  transition: background 100ms ease;
  padding: 0;
  -webkit-tap-highlight-color: transparent;
}
.ol-mobile-menu-trigger:hover { background: var(--ol-surface-2, #f5f5f5); }

/* 오버레이 (배경 dim) */
.ol-mobile-overlay {
  position: fixed;
  inset: 0;
  z-index: 400;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: flex-end;   /* 하단 정렬 */
  justify-content: center;
  opacity: 1;
  transition: opacity 200ms ease;
}
.ol-mobile-overlay[aria-hidden="true"] {
  opacity: 0;
  pointer-events: none;
}

/* 하단 시트 본체 */
.ol-mobile-sheet {
  width: 100%;
  max-width: 480px;
  max-height: 80vh;
  background: var(--ol-surface, #fff);
  border-top-left-radius: 16px;
  border-top-right-radius: 16px;
  padding: 8px 0 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transform: translateY(0);
  transition: transform 250ms ease;
}
.ol-mobile-overlay[aria-hidden="true"] .ol-mobile-sheet {
  transform: translateY(100%);
}

/* 드래그 핸들 (시각적 힌트) */
.ol-mobile-sheet-handle {
  width: 36px;
  height: 4px;
  background: var(--ol-border-strong, #d4d4d4);
  border-radius: 2px;
  margin: 0 auto 12px;
}

/* 링크 영역 */
.ol-mobile-sheet-links {
  display: flex;
  flex-direction: column;
  padding: 0 8px;
  overflow-y: auto;
}

/* 개별 메뉴 링크 */
.ol-mobile-sheet-link {
  display: flex;
  align-items: center;
  padding: 14px 16px;
  font-size: 16px;
  font-weight: 600;
  color: var(--ol-ink, #0a0a0a);
  text-decoration: none;
  border-radius: var(--ol-r, 8px);
  transition: background 80ms ease;
  letter-spacing: 0.02em;
  -webkit-tap-highlight-color: transparent;
}
.ol-mobile-sheet-link:hover,
.ol-mobile-sheet-link:active {
  background: var(--ol-surface-2, #f5f5f5);
}
.ol-mobile-sheet-link.active {
  color: var(--ol-ink, #0a0a0a);
  background: var(--ol-surface-2, #f5f5f5);
}

/* 보조 링크 (BLOG, GitHub — 작게) */
.ol-mobile-sheet-link--sub {
  font-size: 14px;
  font-weight: 500;
  color: var(--ol-muted, #737373);
}
.ol-mobile-sheet-link--sub:hover { color: var(--ol-ink, #0a0a0a); }

/* 구분선 */
.ol-mobile-sheet-divider {
  height: 1px;
  background: var(--ol-border, #e9e9e9);
  margin: 4px 16px 4px;
}

/* 닫기 버튼 */
.ol-mobile-sheet-close {
  display: flex;
  align-items: center;
  justify-content: center;
  width: calc(100% - 16px);
  margin: 8px 8px 12px;
  padding: 14px;
  font-size: 15px;
  font-weight: 600;
  color: var(--ol-muted, #737373);
  background: var(--ol-surface-2, #f5f5f5);
  border: none;
  border-radius: var(--ol-r, 8px);
  cursor: pointer;
  font-family: inherit;
  -webkit-tap-highlight-color: transparent;
  transition: background 80ms ease, color 80ms ease;
}
.ol-mobile-sheet-close:hover {
  background: var(--ol-surface-3, #fafafa);
  color: var(--ol-ink, #0a0a0a);
}

/* iOS safe area 대응 */
@supports (padding-bottom: env(safe-area-inset-bottom)) {
  .ol-mobile-sheet-close {
    margin-bottom: calc(12px + env(safe-area-inset-bottom));
  }
}

/* ── 다크모드 ── */
.dark .ol-mobile-overlay { background: rgba(0, 0, 0, 0.6); }
.dark .ol-mobile-sheet { background: var(--ol-surface, #111); }
.dark .ol-mobile-sheet-handle { background: var(--ol-border, #272727); }
.dark .ol-mobile-sheet-link:hover,
.dark .ol-mobile-sheet-link:active,
.dark .ol-mobile-sheet-link.active {
  background: var(--ol-surface-2, #1a1a1a);
}
.dark .ol-mobile-sheet-close {
  background: var(--ol-surface-2, #1a1a1a);
  color: var(--ol-muted, #737373);
}
.dark .ol-mobile-sheet-close:hover {
  background: var(--ol-surface-3, #141414);
}

/* 데스크탑에서 모바일 메뉴 전체 숨김 */
@media (min-width: 901px) {
  .ol-mobile-overlay {
    display: none !important;
  }
}
```

### 2-3. 기존 @media (max-width: 900px) 수정

`ol-components.css`의 기존 `@media (max-width: 900px)` 블록을 찾아 아래를 **추가**합니다.
(기존 규칙은 삭제하지 않음, 아래만 추가)

```css
@media (max-width: 900px) {
  /* ── 기존 규칙 유지 ── */

  /* ── 추가: 햄버거 표시 ── */
  .ol-mobile-menu-trigger {
    display: flex;
  }

  /* ── 추가: 헤더 우측 정리 ── */
  /* BLOG 버튼과 GitHub 버튼은 하단 시트로 이동했으므로 숨김 */
  .ol-header-right .ol-btn-outline,
  .ol-header-right .ol-btn-primary {
    display: none;
  }

  /* 헤더 우측에 남는 것: 햄버거 + 검색 + 다크모드 */
  .ol-header-right {
    gap: 4px;
  }
}
```

**주의**: `.ol-nav { display: none }` 규칙은 이미 존재합니다. 그대로 유지.
이것이 데스크탑 수평 메뉴를 숨기고, 대신 하단 시트가 그 역할을 대체합니다.

### 2-4. 헤더 아이콘 순서 (모바일 시각적 정리)

모바일에서 `.ol-header-right` 안에 남는 요소 순서:

```
[햄버거 ☰]  [검색 🔍]  [다크모드 🌙]
```

3개 아이콘이 일렬로 배치됩니다. `gap: 4px`으로 간격을 좁혀 공간을 절약합니다.

---

## TASK 3. 검증 체크리스트

### WORKS 가로 스크롤 (TASK 1)

- [ ] `min-width: 1200px` 제거 확인 (grep으로 잔존 여부 검색)
- [ ] `min-width: 900px` 제거 확인
- [ ] 375px 폭에서 `/works` 가로 스크롤 없음
- [ ] 375px 폭에서 `/works/{문서}` 가로 스크롤 없음
- [ ] 1280px 데스크탑에서 WORKS 레이아웃 변화 없음
- [ ] 사이드바 토글 정상 동작 (데스크탑)
- [ ] 사이드바 오버레이 정상 동작 (모바일)

### 헤더 모바일 메뉴 (TASK 2)

- [ ] 900px 이상: 햄버거 버튼 숨겨짐
- [ ] 900px 이상: 데스크탑 `.ol-nav` 정상 표시
- [ ] 900px 이상: BLOG·GitHub 버튼 정상 표시
- [ ] 900px 이하: 햄버거 버튼 표시됨
- [ ] 900px 이하: `.ol-nav` 숨겨짐
- [ ] 900px 이하: BLOG·GitHub 버튼 숨겨짐
- [ ] 햄버거 클릭 → 하단 시트 올라옴 (슬라이드 애니메이션)
- [ ] 하단 시트: 6개 메뉴 링크 + 구분선 + BLOG + GitHub 표시
- [ ] 현재 페이지 링크에 active 표시
- [ ] 메뉴 링크 클릭 → 해당 페이지 이동 + 시트 닫힘
- [ ] 닫기 버튼 클릭 → 시트 닫힘
- [ ] 배경(오버레이) 클릭 → 시트 닫힘
- [ ] ESC 키 → 시트 닫힘
- [ ] 시트 열림 중 body 스크롤 잠김
- [ ] 시트 닫힘 후 body 스크롤 복원
- [ ] 다크모드 전환 후 시트 스타일 정상
- [ ] 검색 모달(Cmd+K)과 충돌 없음 (z-index: 검색 300, 메뉴 400)

### 공통

- [ ] npm run build 무오류
- [ ] npm run preview 에서 전체 확인
- [ ] GitHub Pages 배포 성공

---

## 참고 — z-index 체계

```
사이드바 (WORKS):   30
헤더:               50
모달 (카드 편집):   100
토스트:             200
검색 모달:          300
모바일 메뉴:        400   ← 최상위 (모든 것 위에)
```

모바일 메뉴는 검색 모달보다 위에 있어야 합니다.
검색 모달이 열린 상태에서 메뉴를 열 가능성은 낮지만,
z-index 충돌을 원천 방지하기 위해 400으로 설정합니다.

---

*OL HOME 모바일 CSS 긴급 수정 — 2026.05*