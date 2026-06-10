
# OL HOME — Phase 3 검색기능추가 구현전략


---

## 권장: Pagefind + Command Palette UI

### 왜 Pagefind인가

```
Pagefind 장점:
- Astro 빌드 후 자동 인덱싱 (플러그인 한 줄)
- 클라이언트 JS 6KB 이내
- 한국어 지원
- GitHub Pages 완전 호환 (서버 불필요)
- search.ts에서 별도 인덱스 안 만들어도 됨

비교:
- Fuse.js: JSON 인덱스 직접 생성해야 함, 콘텐츠 많아지면 번들 무거움
- FlexSearch: 같은 문제
- Algolia: 외부 서비스 의존, OL 철학(self-contained)과 어긋남
```

Pagefind는 `npm run build` 후 `dist/` 폴더를 스캔해서 자동으로 인덱스를 생성합니다. 별도 설정이 거의 없습니다.

---

## 검색 아이콘 위치

헤더 우측, 다크모드 토글 옆에 돋보기 아이콘 배치. 클릭하면 Command Palette(모달) 열림. `Cmd+K` (Mac) / `Ctrl+K` (Windows) 단축키도 지원.

```
┌────────────────────────────────────────────────────┐
│ OL    HOME  ATLAS  BOOK  WORKS  DESIGN  AI   [🔍] [🌙] [BLOG] [GitHub] │
└────────────────────────────────────────────────────┘
                                                ↑ 여기
```

이 위치를 권장하는 이유: shadcn/ui, Basecoat, Astro Starlight 등 모든 문서 사이트가 이 패턴을 씁니다. 사용자가 직관적으로 찾습니다.

---

## 검색 범위

Pagefind는 기본적으로 빌드된 모든 HTML 페이지를 인덱싱합니다. 현재 14개 페이지 전체가 대상:

```
✅ HOME, ATLAS, AI          — 소개 페이지
✅ BOOK, WORKS              — 콘텐츠 본문
✅ BLOG                     — 포스트
✅ Entity 페이지             — 인물, 장소, 개념, 문헌
❌ public/books/ HTML        — Pagefind 기본 범위 밖 (별도 설정 가능)
```

`public/books/`의 완결 HTML은 Astro 빌드 결과물이 아니라 직접 배치한 파일이므로, Pagefind가 기본적으로 스캔하지 않습니다. 지금은 콘텐츠가 없으니 무시하고, 나중에 필요하면 Pagefind 설정에 추가할 수 있습니다.

### 검색에서 제외할 영역

헤더, 푸터, 네비게이션 텍스트가 검색 결과에 잡히면 노이즈가 됩니다.

```html
<!-- BaseLayout.astro 에서 -->
<header data-pagefind-ignore>...</header>
<footer data-pagefind-ignore>...</footer>

<!-- 본문 영역만 인덱싱 -->
<main data-pagefind-body>
  ...
</main>
```

`data-pagefind-body`를 `<main>`에 붙이면 그 안쪽만 인덱싱됩니다. `data-pagefind-ignore`는 명시적 제외.

---

## 검색 결과 UI — Command Palette

shadcn/ui의 Command 컴포넌트와 동일한 느낌의 모달입니다. OL 디자인 시스템으로 오버라이드.

```
[Cmd+K 또는 돋보기 클릭]

┌─────────────────────────────────────────┐
│  🔍 검색어 입력...                       │
├─────────────────────────────────────────┤
│                                         │
│  ENTITY                                 │
│  ┌─ 용수 (龍樹, Nāgārjuna)             │
│  │  대승불교 중관학파의 창시자            │
│  └─────────────────────────────────────│
│                                         │
│  WORKS                                  │
│  ┌─ 룸비니의 탄생                       │
│  │  마야부인이 룸비니 동산에서...         │
│  └─────────────────────────────────────│
│                                         │
│  BLOG                                   │
│  ┌─ v0.4.2 — 단일 파일 내보내기 개선     │
│  │  에디터에서 작성한 콘텐츠를...         │
│  └─────────────────────────────────────│
│                                         │
│  ESC 닫기 · ↑↓ 이동 · Enter 열기        │
└─────────────────────────────────────────┘
```

특징:
- 배경 dim 오버레이 (z-index: 300)
- 입력과 동시에 실시간 결과 표시
- 키보드 네비게이션 (↑↓ Enter Esc)
- 결과 없으면 "검색 결과가 없습니다" 표시
- 결과 클릭 시 해당 페이지로 이동 + 모달 닫힘
- 모바일에서는 전체 화면 모달로 전환

---

## 구현 전략 요약

```
설치:     npm install pagefind (devDependency)
빌드:     package.json scripts에 postbuild 추가
인덱싱:   data-pagefind-body 를 <main>에 적용
제외:     data-pagefind-ignore 를 header/footer에 적용
UI:       OLSearchModal.astro 컴포넌트 + 인라인 JS
단축키:   Cmd+K / Ctrl+K → 모달 열기
스타일:   ol-search-* 클래스, OL 디자인 토큰 사용
```

---

