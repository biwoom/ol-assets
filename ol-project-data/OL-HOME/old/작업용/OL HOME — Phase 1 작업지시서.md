# OL HOME — Phase 1 작업지시서
## Astro + Basecoat + OL CSS 통합 개발 가이드

> **대상 독자**: Astro 초보자 / Claude Code · Cursor Agent 등 로컬 AI 에이전트
> **최종 결과물**: GitHub Pages에 배포된 OL 홈페이지 골격 (6개 페이지 라우팅 + OL 디자인 시스템 적용)
> **기준 파일**: `OL_Homepage_Sample.html` + `styles.css`

---

## 0. 시작 전 — 이 지시서를 읽는 방법

이 지시서는 세 부분으로 구성됩니다.

1. **환경 준비** — Node.js 설치부터 GitHub 저장소 생성까지 (처음 한 번만)
2. **Astro + Basecoat 설치** — 단계별 설치 안내 (명령어 복사·붙여넣기)
3. **OL 구현 작업** — AI 에이전트가 실행할 구체적 작업 목록

AI 에이전트에게 전달할 때는 **섹션 3만** 전달해도 됩니다. 섹션 1·2는 사람이 직접 실행하는 환경 준비 단계입니다.

---

## 섹션 1. 환경 준비 (사람이 직접 실행)

### 1-1. Node.js 설치 확인

터미널(맥: Terminal, 윈도우: PowerShell)을 열고 아래를 입력합니다.

```bash
node -v
npm -v
```

버전 번호가 나오면 이미 설치되어 있습니다. 아무 반응이 없거나 오류가 나오면:

- **설치 링크**: https://nodejs.org → "LTS" 버튼 클릭 → 다운로드 후 설치
- 설치 후 터미널을 **새로 열고** 다시 `node -v` 확인

> Node.js 18 이상이면 됩니다. 2026년 현재 LTS는 22.x입니다.

### 1-2. VS Code 설치 (권장)

- **설치 링크**: https://code.visualstudio.com
- 설치 후 **Astro 확장** 설치: VS Code 왼쪽 확장(Extensions) 탭 → `Astro` 검색 → 설치

### 1-3. GitHub 저장소 생성

1. https://github.com 접속 → 로그인
2. 오른쪽 상단 `+` → `New repository`
3. Repository name: `OL-HOME`
4. Public 선택
5. **Add a README file** 체크
6. `Create repository` 클릭

> GitHub Pages는 Public 저장소에서 무료로 사용할 수 있습니다.

### 1-4. 로컬에 저장소 클론

터미널에서:

```bash
# 작업 폴더로 이동 (예: 바탕화면)
cd ~/Desktop

# 저장소 클론 (YOUR_USERNAME을 본인 GitHub 아이디로 교체)
git clone https://github.com/YOUR_USERNAME/OL-HOME.git

# 폴더 진입
cd OL-HOME
```

---

## 섹션 2. Astro + Basecoat 설치 (단계별 안내)

### 2-1. Astro 프로젝트 생성

`OL-HOME` 폴더 안에서:

```bash
# Astro 설치 마법사 실행
npm create astro@latest .
```

> `.` 은 "현재 폴더에 설치"를 의미합니다.

설치 마법사가 몇 가지를 묻습니다. 아래처럼 답하세요:

| 질문 | 답변 |
|------|------|
| How would you like to start your new project? | `Empty` (비어있는 템플릿) |
| Do you plan to write TypeScript? | `Yes` |
| How strict should TypeScript be? | `Strict` |
| Install dependencies? | `Yes` |
| Initialize a new git repository? | `No` (이미 git 있음) |

설치가 완료되면:

```bash
# 개발 서버 실행 테스트
npm run dev
```

브라우저에서 `http://localhost:4321` 을 열면 빈 Astro 페이지가 보입니다. `Ctrl+C`로 서버를 종료합니다.

###  2-2. Tailwind CSS 설치

Astro에 Tailwind를 추가합니다 (Basecoat가 Tailwind 기반이므로 필수):

```bash
npm install -D @tailwindcss/vite tailwindcss
```

`astro.config.mjs` 파일을 열어 아래처럼 수정합니다:

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://YOUR_USERNAME.github.io',  // GitHub Pages URL
  base: '/OL-HOME',                          // 저장소 이름
  vite: {
    plugins: [tailwindcss()],
  },
});
```

> `YOUR_USERNAME`을 본인 GitHub 아이디로 교체하세요.

### 2-3. MDX 설치

```bash
npx astro add mdx
```

질문이 나오면 `y`를 누릅니다.

### 2-4. Basecoat 설치

Basecoat는 두 가지 방법으로 설치할 수 있습니다. **OL 프로젝트에는 npm 설치 방식**을 권장합니다.

```bash
npm install basecoat-css
```

`src/styles/global.css` 파일을 생성하고 아래 내용을 입력합니다:

```css
/* ① Tailwind */
@import "tailwindcss";

/* ② Basecoat — shadcn/ui 계열 컴포넌트 기반 */
@import "basecoat-css";

/* ③ OL 디자인 토큰 (다음 단계에서 추가) */
@import "./tokens.css";

/* ④ OL 컴포넌트 스타일 (다음 단계에서 추가) */
@import "./ol-components.css";
```

> **Basecoat를 직접 수정하지 마세요.** OL 커스터마이징은 반드시 별도 파일(`tokens.css`, `ol-components.css`)에서만 합니다.
> 이유: Basecoat가 업데이트될 때 `npm update` 한 번으로 최신 버전을 받을 수 있어야 하기 때문입니다.

Basecoat의 JavaScript(탭, 드롭다운 등 인터랙티브 컴포넌트용)는 나중에 필요할 때 추가합니다. Phase 1에서는 CSS만으로 충분합니다.

### 2-5. 글로벌 CSS를 레이아웃에 연결

`src/layouts/BaseLayout.astro` 파일을 생성합니다 (다음 섹션에서 상세 내용 작성):

```astro
---
// src/layouts/BaseLayout.astro
import '../styles/global.css';
---
```

### 2-6. 개발 서버 재실행 및 확인

```bash
npm run dev
```

오류 없이 실행되면 기반 설치가 완료된 것입니다.

### 2-7. GitHub Actions 배포 설정

`.github/workflows/deploy.yml` 파일을 생성합니다:

```yaml
name: Deploy OL HOME to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

GitHub 저장소 → Settings → Pages → Source를 `GitHub Actions`로 변경합니다.

---

## 섹션 3. OL 구현 작업 (AI 에이전트 작업지시)

> 이 섹션부터는 Claude Code / Cursor Agent 등 AI 에이전트에게 전달하거나, 직접 파일을 작성합니다.

---

### 사전 맥락 (에이전트에게 전달)

이 프로젝트는 **OL(올)** — 불교 콘텐츠 프로젝트의 홈페이지입니다.

**기술 스택**:
- Astro (정적 사이트 빌더)
- Tailwind CSS + Basecoat (UI foundation)
- OL CSS (커스텀 디자인 레이어)

**디자인 철학**: `contemplative · editorial · archive · low-noise`
- 과도한 애니메이션, SaaS 마케팅 패턴, 화려한 CTA 금지
- 무채색(monochrome) 베이스, 큰 여백, 타이포그래피 중심

**기준 파일**:
- `OL_Homepage_Sample.html` — 페이지 구조와 콘텐츠 기준
- `styles.css` — OL 디자인 시스템 기준

**클래스 네이밍 규칙**: Basecoat 충돌 방지를 위해 OL 전용 클래스는 `.ol-` 접두어 사용
(단, `styles.css`에서 이미 정의된 `.hero`, `.card`, `.btn` 등은 `.ol-hero`, `.ol-card`, `.ol-btn`으로 마이그레이션)

---

### TASK 1. 디렉토리 구조 생성

아래 구조를 만듭니다. 파일 내용은 이후 태스크에서 채웁니다.

```
OL-HOME/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── OLHeader.astro
│   │   │   └── OLFooter.astro
│   │   ├── ui/
│   │   │   ├── OLBadge.astro
│   │   │   └── OLButton.astro
│   │   └── home/
│   │       ├── OLHero.astro
│   │       ├── OLProductCards.astro
│   │       ├── OLManifest.astro
│   │       ├── OLStats.astro
│   │       └── OLLatestUpdates.astro
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   └── PageLayout.astro
│   ├── pages/
│   │   ├── index.astro
│   │   ├── atlas.astro
│   │   ├── book.astro
│   │   ├── design.astro
│   │   ├── ai.astro
│   │   └── blog/
│   │       └── index.astro
│   ├── content/
│   │   ├── blog/
│   │   │   └── _placeholder.md
│   │   └── updates/
│   │       └── _placeholder.md
│   ├── styles/
│   │   ├── global.css
│   │   ├── tokens.css
│   │   └── ol-components.css
│   └── data/
│       └── nav.ts
├── public/
│   ├── images/
│   └── icons/
├── .github/
│   └── workflows/
│       └── deploy.yml
├── astro.config.mjs
└── package.json
```

---

### TASK 2. 디자인 토큰 파일 작성

`src/styles/tokens.css` — `styles.css`의 `:root` 변수를 OL 네임스페이스로 정리합니다.

```css
/* ============================================================
   OL Design Tokens — Phase 1
   Source: styles.css (OL Design System v2)
   ============================================================ */

:root {
  /* ── Color ── */
  --ol-bg:              #ffffff;
  --ol-surface:         #ffffff;
  --ol-surface-2:       #f5f5f5;
  --ol-surface-3:       #fafafa;
  --ol-border:          #e9e9e9;
  --ol-border-strong:   #d4d4d4;
  --ol-ink:             #0a0a0a;
  --ol-ink-2:           #2a2a2a;
  --ol-muted:           #737373;
  --ol-subtle:          #a3a3a3;

  /* ── Typography ── */
  --ol-font-sans:    "Inter", "Pretendard", "Noto Sans KR",
                     -apple-system, BlinkMacSystemFont, sans-serif;
  --ol-font-mono:    "JetBrains Mono", "IBM Plex Mono",
                     ui-monospace, monospace;

  /* ── Radius ── */
  --ol-r-sm:  6px;
  --ol-r:     8px;
  --ol-r-lg: 14px;

  /* ── Shadow ── */
  --ol-shadow-sm: 0 1px 0 rgba(0,0,0,0.03);
  --ol-shadow:    0 1px 2px rgba(0,0,0,0.04);

  /* ── Spacing scale ── */
  --ol-sp-1:  0.25rem;   /*  4px */
  --ol-sp-2:  0.5rem;    /*  8px */
  --ol-sp-3:  0.75rem;   /* 12px */
  --ol-sp-4:  1rem;      /* 16px */
  --ol-sp-6:  1.5rem;    /* 24px */
  --ol-sp-8:  2rem;      /* 32px */
  --ol-sp-12: 3rem;      /* 48px */
}

/* ── Dark mode ── */
.dark {
  --ol-bg:            #0a0a0a;
  --ol-surface:       #111111;
  --ol-surface-2:     #1a1a1a;
  --ol-surface-3:     #141414;
  --ol-border:        #272727;
  --ol-border-strong: #3a3a3a;
  --ol-ink:           #fafafa;
  --ol-ink-2:         #d4d4d4;
  --ol-muted:         #737373;
  --ol-subtle:        #525252;
}
```

---

### TASK 3. OL 컴포넌트 스타일 작성

`src/styles/ol-components.css` — `styles.css` 전체를 `.ol-` 네임스페이스로 포팅합니다.

> **중요**: `styles.css`의 내용을 그대로 복사하되, 모든 클래스에 `.ol-` 접두어를 붙입니다.
> CSS 변수 참조는 `var(--bg)` → `var(--ol-bg)` 로 치환합니다.

핵심 규칙:

```css
/* styles.css 원본 → ol-components.css 변환 규칙 */

/* .card → .ol-card */
.ol-card {
  background: var(--ol-surface);
  border: 1px solid var(--ol-border);
  border-radius: var(--ol-r-lg);
  padding: 24px;
  box-shadow: var(--ol-shadow-sm);
}

/* .btn → .ol-btn */
.ol-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 38px;
  padding: 0 16px;
  border-radius: var(--ol-r);
  font-size: 14px;
  font-weight: 500;
  border: 1px solid transparent;
  cursor: pointer;
  text-decoration: none;
  transition: background 120ms ease, border 120ms ease, color 120ms ease;
  background: transparent;
  color: var(--ol-ink);
  font-family: inherit;
}
/* ... styles.css의 나머지 모든 규칙을 같은 방식으로 변환 */
```

변환 대상 클래스 목록 (`styles.css` 기준):

| 원본 | 변환 |
|------|------|
| `.btn`, `.btn-primary` 등 | `.ol-btn`, `.ol-btn-primary` 등 |
| `.card`, `.card-tight` 등 | `.ol-card`, `.ol-card-tight` 등 |
| `.badge`, `.badge-accent` 등 | `.ol-badge`, `.ol-badge-accent` 등 |
| `.hero` | `.ol-hero` |
| `.product-card` | `.ol-product-card` |
| `.book-card` | `.ol-book-card` |
| `.manifest` | `.ol-manifest` |
| `.stats`, `.stat` | `.ol-stats`, `.ol-stat` |
| `.section`, `.section-tight` | `.ol-section`, `.ol-section-tight` |
| `.container` | `.ol-container` |
| `.footer`, `.footer-grid` 등 | `.ol-footer`, `.ol-footer-grid` 등 |
| `.nav` | `.ol-nav` |
| `.header`, `.header-inner` | `.ol-header`, `.ol-header-inner` |
| `.kicker`, `.mono-label` | `.ol-kicker`, `.ol-mono-label` |
| `.grid-2`, `.grid-3`, `.grid-4` | `.ol-grid-2`, `.ol-grid-3`, `.ol-grid-4` |
| `.feature` | `.ol-feature` |
| `.chip`, `.chips` | `.ol-chip`, `.ol-chips` |
| `.tabs` | `.ol-tabs` |
| `.timeline`, `.timeline-item` | `.ol-timeline`, `.ol-timeline-item` |
| `.post` | `.ol-post` |
| `.asset` | `.ol-asset` |
| `.cat-nav` | `.ol-cat-nav` |
| `.principle` | `.ol-principle` |

기타 유틸리티:

```css
/* Korean text optimization */
:lang(ko), .ol-kr { word-break: keep-all; }

/* Grid background */
.ol-grid-bg {
  background-image:
    linear-gradient(to right, var(--ol-border) 1px, transparent 1px),
    linear-gradient(to bottom, var(--ol-border) 1px, transparent 1px);
  background-size: 32px 32px;
}
```

---

### TASK 4. BaseLayout 작성

`src/layouts/BaseLayout.astro`

```astro
---
import '../styles/global.css';
import OLHeader from '../components/layout/OLHeader.astro';
import OLFooter from '../components/layout/OLFooter.astro';

interface Props {
  title?: string;
  description?: string;
  lang?: string;
}

const {
  title = 'OL — Weaving the Wisdom',
  description = 'OL(올)은 한 올, 한 올 지혜를 엮어가는 불교 콘텐츠 프로젝트입니다.',
  lang = 'ko',
} = Astro.props;
---

<!DOCTYPE html>
<html lang={lang} class="ol-light">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content={description} />
  <title>{title}</title>

  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+KR:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap"
    rel="stylesheet"
  />

  <!-- Dark mode init (prevents flash) -->
  <script is:inline>
    (function() {
      const saved = localStorage.getItem('ol-theme');
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      const theme = saved || (prefersDark ? 'dark' : 'light');
      document.documentElement.classList.toggle('dark', theme === 'dark');
    })();
  </script>
</head>
<body class="ol-kr">
  <div class="ol-app">
    <OLHeader />
    <slot />
    <OLFooter />
  </div>
</body>
</html>
```

---

### TASK 5. OLHeader 컴포넌트

`src/components/layout/OLHeader.astro`

샘플 HTML의 `<header class="header">` 섹션을 기반으로 작성합니다.
`styles.css` 클래스를 `.ol-` 클래스로 교체합니다.

```astro
---
const navItems = [
  { href: '/', label: 'HOME' },
  { href: '/atlas', label: 'ATLAS' },
  { href: '/book', label: 'BOOK' },
  { href: '/design', label: 'DESIGN' },
  { href: '/ai', label: 'AI' },
];

const currentPath = Astro.url.pathname;
---

<header class="ol-header">
  <div class="ol-container ol-header-inner">
    <!-- Brand -->
    <a href="/" class="ol-brand">
      <span class="ol-brand-name">OL</span>
      <span class="ol-brand-meta">Weaving the Wisdom</span>
    </a>

    <!-- Nav -->
    <nav class="ol-nav" aria-label="주요 메뉴">
      {navItems.map(item => (
        <a
          href={item.href}
          class:list={['ol-nav-link', { 'active': currentPath === item.href || (item.href !== '/' && currentPath.startsWith(item.href)) }]}
        >
          {item.label}
        </a>
      ))}
    </nav>

    <!-- Right -->
    <div class="ol-header-right">
      <!-- Dark mode toggle -->
      <button
        id="ol-theme-toggle"
        class="ol-btn ol-btn-ghost ol-btn-sm ol-btn-icon"
        title="테마 전환"
        aria-label="다크모드 전환"
      >
        <!-- Sun icon (light mode) -->
        <svg class="ol-icon-sun" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/>
          <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
          <line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/>
          <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
        </svg>
        <!-- Moon icon (dark mode) -->
        <svg class="ol-icon-moon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
        </svg>
      </button>

      <!-- Blog link -->
      <a href="/blog" class="ol-btn ol-btn-outline ol-btn-sm">BLOG</a>

      <!-- GitHub -->
      <a
        href="https://github.com/biwoom"
        class="ol-btn ol-btn-primary ol-btn-sm"
        target="_blank"
        rel="noopener noreferrer"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
          <path d="M12 .5C5.65.5.5 5.65.5 12c0 5.08 3.29 9.39 7.86 10.91.58.11.79-.25.79-.56v-2.21c-3.2.7-3.87-1.36-3.87-1.36-.52-1.33-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.76 2.7 1.25 3.36.96.1-.75.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.69 0-1.26.45-2.29 1.19-3.1-.12-.29-.51-1.47.11-3.06 0 0 .97-.31 3.18 1.18.92-.26 1.91-.39 2.9-.39.99 0 1.98.13 2.9.39 2.21-1.5 3.18-1.18 3.18-1.18.63 1.59.23 2.77.11 3.06.74.81 1.19 1.84 1.19 3.1 0 4.43-2.69 5.4-5.26 5.68.41.36.78 1.06.78 2.13v3.16c0 .31.21.67.79.56C20.21 21.39 23.5 17.08 23.5 12 23.5 5.65 18.35.5 12 .5z"/>
        </svg>
        GitHub
      </a>
    </div>
  </div>
</header>

<script>
  // Dark mode toggle
  const btn = document.getElementById('ol-theme-toggle');
  btn?.addEventListener('click', () => {
    const isDark = document.documentElement.classList.toggle('dark');
    localStorage.setItem('ol-theme', isDark ? 'dark' : 'light');
  });
</script>
```

---

### TASK 6. OLFooter 컴포넌트

`src/components/layout/OLFooter.astro`

샘플 HTML의 footer 섹션을 기반으로 작성합니다.

```astro
---
const currentYear = new Date().getFullYear();
---

<footer class="ol-footer">
  <div class="ol-container">
    <div class="ol-footer-grid">
      <!-- Brand column -->
      <div>
        <div class="ol-brand" style="margin-bottom: 12px;">
          <span class="ol-brand-name">OL</span>
        </div>
        <p style="color: var(--ol-muted); font-size: 13.5px; line-height: 1.7; max-width: 28ch;" class="ol-kr">
          한 올, 한 올 지혜를 엮어가는<br>1인 불교 콘텐츠 프로젝트.
        </p>
      </div>

      <!-- Projects -->
      <div>
        <h4>PROJECTS</h4>
        <a href="/atlas">OL ATLAS</a>
        <a href="/book">OL BOOK</a>
        <a href="/design">OL DESIGN</a>
        <a href="/ai">OL AI</a>
      </div>

      <!-- Resources -->
      <div>
        <h4>RESOURCES</h4>
        <a href="/blog">BLOG</a>
        <a href="https://github.com/biwoom" target="_blank" rel="noopener">GitHub</a>
        <a href="https://borido.org" target="_blank" rel="noopener">borido.org</a>
      </div>

      <!-- License -->
      <div>
        <h4>OPEN SOURCE</h4>
        <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" rel="noopener">CC BY-SA 4.0</a>
        <a href="https://github.com/biwoom/ol-atlas/blob/main/LICENSE" target="_blank" rel="noopener">MIT License</a>
      </div>
    </div>

    <div class="ol-footer-bottom">
      <span>© {currentYear} biwoom · OL Project</span>
      <span>olbit.org · CC BY-SA 4.0</span>
    </div>
  </div>
</footer>
```

---

### TASK 7. HOME 페이지 컴포넌트 분리

샘플 HTML의 `<main data-page-id="home">` 섹션을 다음 5개 컴포넌트로 분리합니다.

#### 7-1. OLHero.astro

`src/components/home/OLHero.astro`

샘플 HTML의 `<section class="hero">` 섹션을 기반으로 작성.
모든 클래스는 `.ol-` 접두어 사용.

```astro
---
// OLHero.astro — HOME 페이지 히어로 섹션
---
<section class="ol-hero ol-grid-bg">
  <div class="ol-container">
    <span class="ol-kicker">OL · Weaving the Wisdom · 불교 콘텐츠 프로젝트</span>
    <h1 class="ol-kr">
      <em>열린 불교 콘텐츠</em><br>
      모든 소스를 공개합니다.
    </h1>
    <p class="ol-lead ol-kr">
      OL(올)은 한 올, 한 올 지혜를 엮어가는 1인 제작 불교 콘텐츠 프로젝트입니다.
      단일 프로젝트를 넘어 스튜디오, 허브, 개방형 아카이브를 지향합니다.
    </p>
    <div class="ol-hero-actions">
      <a href="/atlas" class="ol-btn ol-btn-accent">
        ATLAS 도구 내려받기
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M7 17 17 7"/><path d="M7 7h10v10"/>
        </svg>
      </a>
      <a href="/book" class="ol-btn ol-btn-outline">콘텐츠 라이브러리 보기</a>
    </div>
  </div>
</section>
```

#### 7-2. OLProductCards.astro

`src/components/home/OLProductCards.astro`

샘플 HTML의 "6 product cards" 섹션을 기반으로 작성.

```astro
---
// 샘플 HTML의 product-card 섹션 기반
// 6개 카드 (ATLAS, BOOK, DESIGN, AI, BLOG, OPEN)
---
<section class="ol-section">
  <div class="ol-container">
    <div class="ol-section-head">
      <span class="ol-kicker">PROJECTS · 다섯 갈래</span>
      <h2 class="ol-kr">OL이 만드는 다섯 가지</h2>
      <p class="ol-kr">각 프로젝트는 독립적으로 다운로드·열람·사용할 수 있으며, 모두 단일 HTML 파일이거나 오픈소스 자료로 배포됩니다.</p>
    </div>

    <div class="ol-grid-3">
      <!-- 샘플 HTML의 6개 product-card를 ol-product-card로 변환하여 여기에 배치 -->
      <!-- ...카드 내용은 OL_Homepage_Sample.html 참고... -->
    </div>
  </div>
</section>
```

#### 7-3. OLManifest.astro, OLStats.astro, OLLatestUpdates.astro

같은 방식으로 샘플 HTML의 해당 섹션을 각각 컴포넌트로 분리합니다.

---

### TASK 8. HOME 페이지 조립

`src/pages/index.astro`

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import OLHero from '../components/home/OLHero.astro';
import OLProductCards from '../components/home/OLProductCards.astro';
import OLManifest from '../components/home/OLManifest.astro';
import OLStats from '../components/home/OLStats.astro';
import OLLatestUpdates from '../components/home/OLLatestUpdates.astro';
---

<BaseLayout
  title="OL — Weaving the Wisdom"
  description="OL(올)은 한 올, 한 올 지혜를 엮어가는 불교 콘텐츠 프로젝트입니다."
>
  <main>
    <OLHero />
    <OLProductCards />
    <OLManifest />
    <OLStats />
    <OLLatestUpdates />
  </main>
</BaseLayout>
```

---

### TASK 9. 나머지 페이지 — 쉘 페이지 생성

Phase 1에서는 ATLAS, BOOK, DESIGN, AI, BLOG 페이지는 **샘플 HTML의 해당 섹션을 그대로 마이그레이션**합니다. 각 페이지 파일 형식:

```astro
---
// src/pages/atlas.astro
import BaseLayout from '../layouts/BaseLayout.astro';
---

<BaseLayout
  title="OL ATLAS — 단일 HTML 불교 콘텐츠 제작 도구"
  description="ATLAS는 단일 HTML 파일로 동작하는 불교 콘텐츠 에디터이자 뷰어입니다."
>
  <main>
    <!-- OL_Homepage_Sample.html의 atlas 섹션 내용 마이그레이션 -->
    <!-- 모든 클래스명에 ol- 접두어 추가 -->
  </main>
</BaseLayout>
```

마이그레이션 대상:
- `data-page-id="atlas"` → `/atlas`
- `data-page-id="book"` → `/book`
- `data-page-id="design"` → `/design`
- `data-page-id="ai"` → `/ai`
- `data-page-id="blog"` → `/blog/index`

---

### TASK 10. Content Collections 설정

`src/content/config.ts`

```typescript
import { defineCollection, z } from 'astro:content';

// 블로그 포스트 스키마
const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    excerpt: z.string().optional(),
    category: z.enum(['ATLAS', 'BOOK', 'DESIGN', 'AI', 'META']).optional(),
    published: z.boolean().default(false),
  }),
});

// 업데이트 공지 스키마
const updatesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    category: z.enum(['ATLAS', 'BOOK', 'DESIGN', 'AI', 'BLOG']),
    published: z.boolean().default(true),
  }),
});

export const collections = {
  blog: blogCollection,
  updates: updatesCollection,
};
```

샘플 블로그 포스트 `src/content/blog/atlas-v042.md`:

```markdown
---
title: "v0.4.2 — 단일 파일 내보내기 개선"
date: 2026-05-21
tags: ["atlas", "release"]
excerpt: "에디터에서 작성한 콘텐츠를 5MB 이하 단일 HTML 파일로 압축하는 흐름을 정비했습니다."
category: ATLAS
published: true
---

에디터에서 작성한 콘텐츠를 5MB 이하 단일 HTML 파일로 압축하는 흐름을 정비했습니다.
```

---

### TASK 11. 다크모드 완성

`tokens.css`의 `.dark` 블록이 이미 정의되어 있으므로, `OLHeader.astro`의 토글 스크립트를 확인합니다. 추가로 `ol-components.css`에:

```css
/* Dark mode — icon visibility */
html.dark .ol-icon-sun { display: none; }
html:not(.dark) .ol-icon-moon { display: none; }

/* Smooth theme transition */
body {
  transition: background-color 200ms ease, color 200ms ease;
}
```

---

### TASK 12. 반응형 최종 점검

`ol-components.css` 하단에 반응형 규칙을 추가합니다:

```css
/* Responsive — styles.css 기반, ol- 클래스 적용 */
@media (max-width: 900px) {
  .ol-grid-3, .ol-grid-4 { grid-template-columns: repeat(2, 1fr); }
  .ol-grid-2 { grid-template-columns: 1fr; }
  .ol-hero h1 { font-size: 40px; }
  .ol-footer-grid { grid-template-columns: 1fr 1fr; }
  .ol-nav { display: none; }
  .ol-container { padding: 0 20px; }
}

@media (max-width: 600px) {
  .ol-grid-3, .ol-grid-4 { grid-template-columns: 1fr; }
  .ol-hero { padding: 64px 0 40px; }
  .ol-hero h1 { font-size: 32px; }
  .ol-stats { grid-template-columns: 1fr 1fr; }
}
```

---

## 섹션 4. 완료 조건 체크리스트

개발 완료 후 아래 항목을 모두 확인합니다.

### 기능 체크

- [ ] `npm run dev` 오류 없이 실행
- [ ] `npm run build` 오류 없이 빌드
- [ ] `http://localhost:4321` 에서 HOME 페이지 정상 표시
- [ ] `/atlas`, `/book`, `/design`, `/ai`, `/blog` 라우팅 정상
- [ ] 헤더 네비게이션 링크 정상 동작
- [ ] 다크모드 토글 정상 동작
- [ ] 새로고침 후 테마 유지 (localStorage)
- [ ] GitHub Actions 배포 성공
- [ ] GitHub Pages URL에서 정상 접속

### 디자인 체크

- [ ] 폰트 (Inter, Noto Sans KR, JetBrains Mono) 정상 로드
- [ ] 무채색 팔레트 유지 (불필요한 색상 없음)
- [ ] 모바일 (375px) 레이아웃 정상
- [ ] 태블릿 (768px) 레이아웃 정상
- [ ] 데스크탑 (1280px) 레이아웃 정상
- [ ] 다크모드에서 모든 요소 가독성 유지
- [ ] `.ol-` 클래스 네임스페이스 일관성

### 성능 체크

- [ ] Lighthouse Performance 90점 이상
- [ ] Lighthouse Accessibility 90점 이상
- [ ] 불필요한 JavaScript 없음

---

## 섹션 5. 자주 묻는 질문

**Q. Basecoat와 OL 스타일이 충돌하면 어떻게 하나요?**

A. CSS specificity를 활용합니다. OL 스타일은 항상 Basecoat import 이후에 위치하므로 동일 specificity에서는 OL 스타일이 이깁니다. 필요하면 `:root` 에서 Basecoat의 CSS 변수를 덮어씁니다.

**Q. `npm run build` 시 "page not found" 오류가 나요.**

A. `astro.config.mjs`의 `base` 경로가 GitHub 저장소 이름과 일치하는지 확인합니다. 저장소명이 `OL-HOME`이면 `base: '/OL-HOME'`이어야 합니다.

**Q. 한국어가 깨져 보여요.**

A. `<html>` 태그에 `lang="ko"`, `<meta charset="UTF-8">`이 있는지 확인합니다. 폰트 로드 전에 system font fallback이 한국어를 지원하는지 확인합니다.

**Q. 다크모드에서 흰 배경이 잠깐 보여요 (FOUC).**

A. `BaseLayout.astro`의 `<head>` 안 인라인 스크립트(`is:inline`)가 올바르게 설정되어 있는지 확인합니다. 이 스크립트가 CSS보다 먼저 실행되어야 합니다.

**Q. GitHub Pages에 배포했는데 CSS가 안 보여요.**

A. `astro.config.mjs`에 `site`와 `base` 모두 설정했는지 확인합니다. Astro가 정적 asset 경로를 base 기준으로 생성합니다.

---

## 섹션 6. Phase 2 예고

Phase 1 완료 후 다음 단계:

```
Phase 2 — 콘텐츠 구조화
├── OL BOOK 라이브러리 페이지 (실제 책 목록)
├── BLOG 목록 + 개별 포스트 페이지
├── 태그 필터링
└── 검색 기능 (pagefind 통합)

Phase 3 — OL BOOK 뷰어 연동
├── ATLAS HTML 파일 다운로드 링크
├── 온라인 프리뷰
└── OL BOOK 개별 페이지
```

> **기억하세요**: OL 프로젝트의 본질은 불교 콘텐츠입니다. 외형 개선보다 콘텐츠 탑재를 우선합니다.

---

*OL HOME Phase 1 작업지시서 — 2026.05*
*문서 버전: v1.0*