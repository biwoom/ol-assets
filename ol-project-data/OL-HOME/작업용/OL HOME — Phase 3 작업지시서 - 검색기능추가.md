# OL HOME — Phase 3 작업지시서 - 검색기능추가

```
[검색 기능 추가 — Pagefind + Command Palette]

## 1. Pagefind 설치

npm install -D pagefind

package.json scripts 수정:
  변경 전: "build": "astro build"
  변경 후: "build": "astro build && npx pagefind --site dist"

이렇게 하면 astro build 후 자동으로 dist/ 를 스캔하여
dist/pagefind/ 폴더에 인덱스 생성.

## 2. BaseLayout.astro 수정

### 인덱싱 범위 지정

OLHeader 에 data-pagefind-ignore 추가:
  <header class="ol-header" data-pagefind-ignore>

OLFooter 에도 동일:
  <footer class="ol-footer" data-pagefind-ignore>

모든 페이지의 <main> 태그에 data-pagefind-body 추가.
현재 <main> 이 각 페이지(index.astro, atlas.astro 등)에 있으므로
각 페이지의 <main> 에 data-pagefind-body 를 추가.
또는 BaseLayout 에서 slot 감싸는 div에 적용:

  <div class="ol-app">
    <OLHeader />
    <div data-pagefind-body>
      <slot />
    </div>
    <OLFooter />
  </div>

## 3. OLSearchModal.astro 생성

src/components/layout/OLSearchModal.astro

이 컴포넌트는 BaseLayout.astro 에서 OLHeader 바로 아래에 import.

```astro
---
// OLSearchModal.astro — Pagefind Command Palette
---

<!-- 오버레이 -->
<div class="ol-search-overlay" id="ol-search-overlay" aria-hidden="true">
  <div class="ol-search-modal" role="dialog" aria-label="검색">

    <!-- 검색 입력 -->
    <div class="ol-search-input-wrap">
      <svg class="ol-search-icon" width="16" height="16" viewBox="0 0 24 24"
        fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8"/>
        <line x1="21" y1="21" x2="16.65" y2="16.65"/>
      </svg>
      <input
        id="ol-search-input"
        class="ol-search-input"
        type="text"
        placeholder="검색어 입력..."
        autocomplete="off"
        autofocus
      />
      <kbd class="ol-search-kbd">ESC</kbd>
    </div>

    <!-- 결과 영역 -->
    <div class="ol-search-results" id="ol-search-results">
      <div class="ol-search-empty">
        검색어를 입력하세요
      </div>
    </div>

    <!-- 하단 힌트 -->
    <div class="ol-search-footer">
      <span><kbd>↑</kbd><kbd>↓</kbd> 이동</span>
      <span><kbd>Enter</kbd> 열기</span>
      <span><kbd>ESC</kbd> 닫기</span>
    </div>

  </div>
</div>

<script>
  // Pagefind 로드 + 검색 로직
  let pagefind: any = null;
  let selectedIndex = -1;

  async function loadPagefind() {
    if (pagefind) return pagefind;
    // Pagefind는 빌드 시 dist/pagefind/ 에 생성됨
    // base 경로 포함하여 로드
    const base = import.meta.env.BASE_URL || '/';
    pagefind = await import(/* @vite-ignore */ `${base}pagefind/pagefind.js`);
    await pagefind.init();
    return pagefind;
  }

  const overlay = document.getElementById('ol-search-overlay')!;
  const input = document.getElementById('ol-search-input') as HTMLInputElement;
  const resultsContainer = document.getElementById('ol-search-results')!;

  // 모달 열기
  function openSearch() {
    overlay.setAttribute('aria-hidden', 'false');
    input.value = '';
    resultsContainer.innerHTML = '<div class="ol-search-empty">검색어를 입력하세요</div>';
    selectedIndex = -1;
    // 약간의 딜레이 후 포커스 (트랜지션 후)
    requestAnimationFrame(() => input.focus());
  }

  // 모달 닫기
  function closeSearch() {
    overlay.setAttribute('aria-hidden', 'true');
    input.blur();
  }

  // 검색 실행 (디바운스)
  let debounceTimer: ReturnType<typeof setTimeout>;
  input.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      const query = input.value.trim();
      if (!query) {
        resultsContainer.innerHTML = '<div class="ol-search-empty">검색어를 입력하세요</div>';
        selectedIndex = -1;
        return;
      }

      const pf = await loadPagefind();
      const search = await pf.search(query);

      if (search.results.length === 0) {
        resultsContainer.innerHTML = '<div class="ol-search-empty">검색 결과가 없습니다</div>';
        selectedIndex = -1;
        return;
      }

      // 상위 8개 결과만 표시
      const results = await Promise.all(
        search.results.slice(0, 8).map((r: any) => r.data())
      );

      resultsContainer.innerHTML = results.map((r: any, i: number) => `
        
          href="${r.url}"
          class="ol-search-result ${i === 0 ? 'active' : ''}"
          data-index="${i}"
        >
          <span class="ol-search-result-title">${r.meta?.title ?? '제목 없음'}</span>
          <span class="ol-search-result-excerpt">${r.excerpt ?? ''}</span>
        </a>
      `).join('');

      selectedIndex = 0;
    }, 200);
  });

  // 키보드 네비게이션
  input.addEventListener('keydown', (e) => {
    const items = resultsContainer.querySelectorAll('.ol-search-result');
    if (!items.length) return;

    if (e.key === 'ArrowDown') {
      e.preventDefault();
      selectedIndex = Math.min(selectedIndex + 1, items.length - 1);
      updateSelection(items);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      selectedIndex = Math.max(selectedIndex - 1, 0);
      updateSelection(items);
    } else if (e.key === 'Enter' && selectedIndex >= 0) {
      e.preventDefault();
      (items[selectedIndex] as HTMLAnchorElement).click();
    }
  });

  function updateSelection(items: NodeListOf<Element>) {
    items.forEach((el, i) => {
      el.classList.toggle('active', i === selectedIndex);
    });
    items[selectedIndex]?.scrollIntoView({ block: 'nearest' });
  }

  // 전역 키보드 단축키: Cmd+K / Ctrl+K
  document.addEventListener('keydown', (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
      e.preventDefault();
      openSearch();
    }
    if (e.key === 'Escape') {
      closeSearch();
    }
  });

  // 오버레이 클릭으로 닫기
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeSearch();
  });

  // 헤더 검색 버튼 연결
  document.getElementById('ol-search-trigger')?.addEventListener('click', openSearch);
</script>
```

## 4. OLHeader.astro — 검색 버튼 추가

다크모드 토글 버튼 왼쪽에 검색 버튼 추가:

```astro
<!-- 검색 트리거 -->
<button
  id="ol-search-trigger"
  class="ol-btn ol-btn-ghost ol-btn-sm ol-btn-icon"
  title="검색 (⌘K)"
  aria-label="검색"
>
  <svg width="15" height="15" viewBox="0 0 24 24"
    fill="none" stroke="currentColor" stroke-width="2">
    <circle cx="11" cy="11" r="8"/>
    <line x1="21" y1="21" x2="16.65" y2="16.65"/>
  </svg>
</button>
```

순서: [검색] [다크모드] [BLOG] [GitHub]

## 5. BaseLayout.astro — OLSearchModal import

OLHeader 아래에 추가:

```astro
import OLSearchModal from '../components/layout/OLSearchModal.astro';
---

<div class="ol-app">
  <OLHeader />
  <OLSearchModal />
  <div data-pagefind-body>
    <slot />
  </div>
  <OLFooter />
</div>
```

## 6. ol-components.css — 검색 모달 스타일

```css
/* ============================================================
   OL Search — Command Palette
   ============================================================ */

/* 오버레이 */
.ol-search-overlay {
  position: fixed;
  inset: 0;
  z-index: 300;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: min(20vh, 160px);
  background: rgba(0, 0, 0, 0.4);
  opacity: 1;
  transition: opacity 150ms ease;
}
.ol-search-overlay[aria-hidden="true"] {
  opacity: 0;
  pointer-events: none;
}

/* 모달 */
.ol-search-modal {
  width: min(560px, calc(100vw - 32px));
  max-height: min(480px, 70vh);
  background: var(--ol-surface, #fff);
  border: 1px solid var(--ol-border, #e9e9e9);
  border-radius: var(--ol-r-lg, 14px);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.12);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* 입력 영역 */
.ol-search-input-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--ol-border, #e9e9e9);
}

.ol-search-icon { color: var(--ol-muted, #737373); flex-shrink: 0; }

.ol-search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 15px;
  font-family: inherit;
  color: var(--ol-ink, #0a0a0a);
}
.ol-search-input::placeholder { color: var(--ol-subtle, #a3a3a3); }

.ol-search-kbd {
  font-family: var(--ol-font-mono);
  font-size: 10px;
  color: var(--ol-muted);
  background: var(--ol-surface-2, #f5f5f5);
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid var(--ol-border);
}

/* 결과 영역 */
.ol-search-results {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.ol-search-empty {
  padding: 32px 16px;
  text-align: center;
  color: var(--ol-muted);
  font-size: 13.5px;
}

/* 개별 결과 */
.ol-search-result {
  display: block;
  padding: 10px 12px;
  border-radius: var(--ol-r, 8px);
  text-decoration: none;
  color: inherit;
  transition: background 80ms ease;
}
.ol-search-result:hover,
.ol-search-result.active {
  background: var(--ol-surface-2, #f5f5f5);
}

.ol-search-result-title {
  display: block;
  font-size: 14px;
  font-weight: 600;
  color: var(--ol-ink);
  margin-bottom: 3px;
}

.ol-search-result-excerpt {
  display: block;
  font-size: 12.5px;
  color: var(--ol-muted);
  line-height: 1.5;
  /* 검색어 하이라이트: Pagefind가 <mark>로 감싸줌 */
}
.ol-search-result-excerpt mark {
  background: transparent;
  color: var(--ol-ink);
  font-weight: 600;
}

/* 하단 힌트 */
.ol-search-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 16px;
  border-top: 1px solid var(--ol-border);
  font-size: 11px;
  color: var(--ol-subtle);
}
.ol-search-footer kbd {
  font-family: var(--ol-font-mono);
  font-size: 10px;
  background: var(--ol-surface-2);
  padding: 1px 4px;
  border-radius: 3px;
  border: 1px solid var(--ol-border);
  margin: 0 2px;
}

/* 다크모드 */
.dark .ol-search-overlay { background: rgba(0, 0, 0, 0.6); }
.dark .ol-search-modal {
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
}

/* 모바일: 전체 화면 */
@media (max-width: 600px) {
  .ol-search-overlay { padding-top: 0; align-items: stretch; }
  .ol-search-modal {
    width: 100%;
    max-height: 100%;
    border-radius: 0;
    border: none;
  }
}
```

## 7. deploy.yml 수정 불필요

Pagefind는 로컬 빌드 시 dist/pagefind/ 에 인덱스 생성.
package.json 의 build 스크립트가 astro build && npx pagefind --site dist
이므로 GitHub Actions 에서도 동일하게 동작.

## 8. .gitignore 확인

dist/ 는 이미 .gitignore 에 있으므로 pagefind 인덱스 파일이
git에 포함되지 않음. 정상.

## 완료 조건

- [ ] npm install -D pagefind 완료
- [ ] package.json build 스크립트에 pagefind 추가
- [ ] BaseLayout.astro 에 data-pagefind-body 적용
- [ ] OLHeader, OLFooter 에 data-pagefind-ignore 적용
- [ ] OLSearchModal.astro 생성
- [ ] OLHeader 에 검색 버튼 추가
- [ ] BaseLayout 에 OLSearchModal import
- [ ] ol-components.css 에 검색 모달 스타일 추가
- [ ] npm run build 무오류
- [ ] 로컬에서 Cmd+K → 모달 열기 확인
- [ ] 검색어 입력 → 결과 표시 확인
- [ ] ↑↓ Enter Esc 키보드 동작 확인
- [ ] 결과 클릭 → 해당 페이지 이동 확인
- [ ] 모바일 전체화면 모달 확인
- [ ] 다크모드 정상
- [ ] GitHub Pages 배포 후 검색 동작 확인
```