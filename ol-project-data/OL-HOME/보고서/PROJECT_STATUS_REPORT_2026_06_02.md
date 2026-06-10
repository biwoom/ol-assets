# OL HOME — Project Status Report

작성일: 2026-06-02  
대상 저장소: `/Users/damjin/Projects/ol-project/github/ol-home`  
현재 브랜치: `main`  
최근 커밋: `d3a9f66 Fix:works Page sectionEntries`  
문서 성격: 외부 전문가/후속 개발자 핸드오버용 현황 보고서

---

## 1. 한 줄 요약

OL HOME은 Astro 기반 정적 사이트이며, OL 프로젝트의 포털이다. 단순 홈페이지가 아니라 `ATLAS`라는 단일 HTML 제작 도구, `WORKS`라는 제작 중 원고 공간, `BOOK`이라는 완결 HTML 출판물, `DESIGN`이라는 시각 레퍼런스 아카이브, `ENTITY`라는 불교 지식 그래프, `BLOG`라는 작업 일지를 하나의 정보 구조로 묶는다.

현재 상태는 production build가 통과하는 초기 운영 가능 단계다. 다만 다음 개발의 핵심은 새 기능 추가보다 데이터 모델 정리, 콘텐츠 파이프라인 완주, 그리고 몇 가지 논리 버그 수정이다.

---

## 2. 프로젝트 철학과 개발 기준

이 프로젝트는 일반적인 SaaS, 커뮤니티, 학습 관리 서비스가 아니다. `.ol-ref/브랜드/OL_프로젝트_존재_선언문_V1.md`와 `brand.md` 기준으로 OL의 핵심 질문은 다음이다.

> 사람들이 이 경험을 통해 정말 더 자유로워지는가?

따라서 앞으로의 기술/기능 판단은 아래 기준을 따른다.

- 깊은 독서, 사유, 관조를 돕는가
- 사용자가 OL에 오래 붙잡히게 하는가, 자기 삶으로 잘 돌아가게 하는가
- 단일 HTML, 오프라인, 로컬 우선, 계정 없음 원칙을 보존하는가
- 콘텐츠의 출처와 원전 맥락을 보존하는가
- 불교 콘텐츠 제작자가 실제로 다시 사용할 수 있는가

의도적으로 피해야 할 기능:

- 계정/소셜 로그인
- 댓글, 좋아요, 별점, 진도율 경쟁, 배지
- 추천 알고리즘
- 푸시 알림과 학습 리마인더
- 사용자 행동 분석, 텔레메트리, 대시보드
- AI의 능동적 개입
- 광고, 후원 콘텐츠, 상업적 결합

---

## 3. 지금까지의 개발 흐름

### Phase 1 — Astro 기반 구축

목표는 OL HOME을 단순 랜딩 페이지가 아닌 Ontology-aware Buddhist Knowledge System의 입구로 만드는 것이었다.

완료된 핵심 작업:

- Astro 6.3.8 기반 정적 사이트 구조 구축
- Astro 6 Content Layer API 대응
  - `src/content.config.ts`
  - `defineCollection({ loader: glob(...) })`
  - `entry.id`, `render(entry)` 패턴 사용
- `blog`, `works/book`, `design`, `ai`, `entities`, `ontology` 컬렉션 설계
- Entity 7종 구조 설계
  - `person`, `place`, `concept`, `text`, `event`, `practice`, `school`
- Triple 관계 스키마 도입
  - `{ subject, predicate, object, source?, note? }`
- GitHub Pages base path 대응용 `src/lib/url.ts` 도입
- `BaseLayout`, 헤더/푸터, 다크모드, 디자인 토큰, 공통 `.ol-*` 컴포넌트 구축

### Phase 2 — WORKS / BOOK 분리

중요한 정책 결정은 `WORKS`와 `BOOK`을 분리한 것이다.

현재 정책:

```text
src/content/works/     제작 중 원고. 챕터별 Markdown.
src/content/book/      완결 출판물 메타데이터.
public/books/          완결 BOOK 단일 HTML 파일.
```

이 결정은 `.ol-ref/작업용/OL HOME — Phase 2 작업지시서 v2.md`와 `.ol-ref/사용법/Book 메뉴 파일 저장 구조와 관리법 최종.md`에 정리되어 있다.

### Phase 3 — 검색 및 운영 기능

초기에는 MiniSearch + JSON 인덱스도 검토했으나, 최종 구현 방향은 Pagefind + Command Palette로 확정되었다.

완료된 작업:

- `package.json` build script에 Pagefind 인덱싱 연결
- `OLSearchModal.astro` 생성
- 헤더 검색 버튼과 Cmd/Ctrl+K 검색 모달 연결
- `BaseLayout`에서 `data-pagefind-body` 적용
- sitemap, RSS, OG 메타, robots, 404 등 운영 기능 보강

### 이후 보정 — WORKS/모바일 레이아웃

최근 주요 작업은 WORKS 페이지의 사이드바, 본문 중앙 정렬, 모바일 가로 스크롤, 모바일 메뉴 문제 보정이었다.

관련 문서:

- `.ol-ref/작업용/WORKS페이지 추가수정.md`
- `.ol-ref/작업용/모바일용 CSS 수정 전략.md`
- `.ol-ref/작업용/모바일용 CSS 수정 전략-작업지시서-1.md`
- `.ol-ref/에러보고용/*.png`

핵심 문제:

- WORKS 영역의 `min-width`가 모바일 가로 스크롤을 만들었음
- 모바일에서 사이드바 드로어와 본문이 겹침
- WORKS 상세 본문이 중앙 정렬되지 않거나, 사이드바 접힘 상태와 레이아웃이 어긋남
- 모바일 헤더 네비게이션이 사라지는 문제

현재 코드는 이 문제를 상당 부분 반영한 상태지만, 모바일/반응형은 실제 화면 검증을 계속해야 한다.

---

## 4. OL HOME과 OL ATLAS의 관계

OL ATLAS는 별도 프로젝트지만, OL HOME의 제품 구조에서 핵심이다.

ATLAS의 역할:

- 단일 HTML 파일로 동작하는 콘텐츠 에디터 겸 뷰어
- 서버/계정 없이 브라우저에서 실행
- 파일 자체에 데이터와 편집 환경을 포함
- 최종적으로 OL BOOK을 만드는 런타임이자 독서 환경

ATLAS 진행 흐름:

- v0.0.1: 듀얼 런타임 폐기, 단일 런타임 정리, 문서뷰 읽기 모드
- v0.0.2: 편집자 시스템, 저장 로그, 카드 행위 기록
- v0.0.3: 영구삭제 시 기록 보존, 원본 편집자 자동 등록, 히스토리 UI
- v0.0.4: esbuild dev 서버
- v0.0.5: 홈 랜딩, 책 메타데이터, 세피아 독서 테마
- v0.0.6: 기존 문서뷰 읽기 모드 제거, 독서뷰 별도 생성
- v0.0.7: 구조 리팩토링 및 유지보수성 개선

OL HOME의 `src/pages/atlas.astro`는 `public/atlas/latest/ol-atlas_v*.html`을 자동 감지해 최신 버전, 파일 크기, 다운로드 링크, iframe 미리보기를 구성한다. 현재 latest는 `ol-atlas_v0.0.7.html`이다.

---

## 5. 기술 스택

| 영역 | 현재 값 |
| --- | --- |
| Framework | Astro `^6.3.8` |
| Runtime | Node `>=22.12.0` |
| Markdown/MDX | `@astrojs/mdx`, `remark-gfm` |
| Search | Pagefind `^1.5.2` |
| Sitemap | `@astrojs/sitemap` |
| RSS | `@astrojs/rss` |
| CSS | Tailwind CSS v4 Vite plugin, Basecoat CSS, 자체 tokens |
| 배포 기준 | GitHub Pages |
| site | `https://biwoom.github.io` |
| base | `/ol-home` |

중요 규칙:

- Astro 6 기준이므로 `src/content/config.ts`가 아니라 `src/content.config.ts`를 사용한다.
- `entry.slug`가 아니라 `entry.id`를 사용한다.
- `entry.render()`가 아니라 `render(entry)`를 사용한다.
- 내부 링크는 가능하면 `url('/path')` 헬퍼를 통과시킨다.
- GitHub Pages 하위 경로 배포 때문에 `/foo` 하드코딩은 배포에서 깨질 수 있다.

---

## 6. 현재 디렉토리 트리

불필요한 `node_modules`, `dist` 내부 상세 파일은 생략했다.

```text
ol-home/
├── astro.config.mjs
├── package.json
├── package-lock.json
├── README.md                         # 아직 Astro 기본 템플릿 상태
├── public/
│   ├── atlas/
│   │   ├── latest/
│   │   │   └── ol-atlas_v0.0.7.html
│   │   └── v0.0.6/
│   │       └── ol-atlas_v0.0.6.html
│   ├── books/
│   │   ├── buddha-story/
│   │   │   └── index.html
│   │   └── placeholder/
│   │       └── index.html
│   ├── design/
│   │   ├── wall-e-3d-render.jpg
│   │   ├── wall-e-blueprint.jpg
│   │   └── wall-e-concept.webp
│   ├── favicon*.png / favicon.ico
│   ├── og-image.png
│   └── robots.txt
├── src/
│   ├── content.config.ts
│   ├── content/
│   │   ├── ai/
│   │   ├── blog/
│   │   │   ├── atlas-dev-journey/
│   │   │   ├── atlas-footnotes/
│   │   │   ├── blog-atlas-code-restructuring/
│   │   │   ├── book-design-guide/
│   │   │   ├── ol-brand-design/
│   │   │   ├── ol-home-build/
│   │   │   ├── ol-home-phase4/
│   │   │   └── ol-why/
│   │   ├── book/
│   │   │   ├── buddha-story.md
│   │   │   └── placeholder.md
│   │   ├── design/
│   │   │   ├── wall-e-3d-render.md
│   │   │   ├── wall-e-blueprint.md
│   │   │   └── wall-e-concept.md
│   │   ├── entities/
│   │   │   ├── concepts/
│   │   │   │   ├── dependent-origination.md
│   │   │   │   └── sunyata.md
│   │   │   ├── persons/
│   │   │   │   ├── nagarjuna.md
│   │   │   │   └── siddhartha-gautama.md
│   │   │   └── places/
│   │   │       └── lumbini.md
│   │   ├── ontology/
│   │   │   ├── entity-types.md
│   │   │   └── relation-types.md
│   │   ├── pages/
│   │   │   ├── brand.md
│   │   │   ├── manifesto.md
│   │   │   ├── rfc.md
│   │   │   └── style-guide.md
│   │   └── works/
│   │       ├── buddha-story/
│   │       │   ├── 01-birth.md
│   │       │   ├── 02-renunciation.md
│   │       │   └── 03-enlightenment.md
│   │       ├── diamond-sutra/
│   │       │   └── 01-intro.md
│   │       └── lamrim/
│   │           └── 01-foundation.md
│   ├── components/
│   │   ├── book/
│   │   ├── entity/
│   │   ├── graph/
│   │   ├── home/
│   │   ├── layout/
│   │   └── ui/
│   ├── data/
│   │   └── nav.ts
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   ├── BookLayout.astro
│   │   ├── EntityLayout.astro
│   │   ├── PageLayout.astro
│   │   └── WorksLayout.astro
│   ├── lib/
│   │   ├── design.ts
│   │   ├── relations.ts
│   │   ├── search.ts
│   │   ├── site.ts
│   │   └── url.ts
│   ├── pages/
│   │   ├── 404.astro
│   │   ├── ai.astro
│   │   ├── atlas.astro
│   │   ├── index.astro
│   │   ├── partners.astro
│   │   ├── rss.xml.ts
│   │   ├── blog/
│   │   ├── book/
│   │   ├── design/
│   │   ├── entity/
│   │   ├── pages/
│   │   └── works/
│   └── styles/
│       ├── global.css
│       ├── ol-components.css
│       └── tokens.css
└── .ol-ref/
    ├── atlas/                         # ATLAS 설계/현황/리팩토링 기록
    ├── 브랜드/                        # 브랜드 정의, 선언문, 로드맵
    ├── 사용법/                        # 콘텐츠 운영 매뉴얼
    ├── 작업용/                        # Phase 작업지시서
    ├── 에러보고용/                    # 모바일/레이아웃 이슈 캡처
    └── 보고서/
```

---

## 7. 콘텐츠 현황

현재 Markdown/MDX 콘텐츠 수:

| 컬렉션 | 수량 | 현재 의미 |
| --- | ---: | --- |
| `blog` | 8 | ATLAS/OL HOME 작업 기록 중심 |
| `works` | 5 | 제작 중 원고. 붓다스토리 3편, 금강경 1편, 람림 1편 |
| `book` | 2 | buddha-story published, placeholder 비공개 |
| `design` | 3 | WALL-E 샘플 레퍼런스 |
| `entities` | 5 | 붓다, 용수, 룸비니, 연기, 공 |
| `ontology` | 2 | entity type, relation type 정의 |
| `pages` | 4 | brand, manifesto, rfc, style-guide |
| `ai` | 0 | 컬렉션만 있음 |

현재 콘텐츠는 실제 OL 운영 콘텐츠와 프로토타입/샘플 콘텐츠가 섞여 있다. 특히 DESIGN은 페이지 목적이 “불교 콘텐츠 스타일 레퍼런스”인데 현재 공개 항목은 WALL-E 샘플 3개다. 이 항목은 디자인 시스템 테스트용 또는 임시 샘플로 해석해야 한다.

---

## 8. 라우트와 기능 현황

### HOME

파일:

- `src/pages/index.astro`
- `src/components/home/*`

현황:

- 랜딩 구조는 완성
- Hero, Product Cards, Manifest, Stats, Latest Updates 조립
- 브랜드 문구와 제품 체계가 반영됨

### ATLAS

파일:

- `src/pages/atlas.astro`
- `public/atlas/latest/ol-atlas_v0.0.7.html`

현황:

- latest 폴더에서 ATLAS 파일명 자동 감지
- 버전, 파일 크기, 다운로드, 브라우저 열기, iframe 미리보기 구성
- ATLAS는 OL BOOK 제작/유통의 핵심 도구로 소개됨

주의:

- `latest/` 폴더에는 원칙적으로 매칭 파일을 하나만 두는 것이 안전하다.

### WORKS

파일:

- `src/pages/works/index.astro`
- `src/pages/works/[...slug].astro`
- `src/layouts/WorksLayout.astro`

현황:

- 원고 목록, 시리즈 그룹, 카테고리 필터, 태그 필터 구현
- 상세 페이지에는 좌측 원고 목록 사이드바와 우측 TOC가 있음
- TOC는 본문 `h2`, `h3`을 JS로 수집하여 생성
- 최근 모바일/사이드바 레이아웃 이슈를 중심으로 보정된 영역

앞으로 확인할 점:

- 375px, 768px, 1280px에서 가로 스크롤 없음
- 모바일 드로어가 본문과 충돌하지 않음
- 사이드바 닫힘 상태에서 본문 중앙 정렬이 유지됨

### BOOK

파일:

- `src/pages/book/index.astro`
- `src/pages/book/[...slug].astro`
- `src/content/book/*.md`
- `public/books/*/index.html`

현재 정책:

- BOOK 목록은 `src/content/book` 메타데이터로 렌더링한다.
- “웹에서 읽기”와 “HTML 내려받기”는 같은 `public/books/{htmlPath}/index.html`을 가리킨다.
- 다운로드 파일명은 `{title}-{version}.html` 방식으로 지정한다.

중요 혼선:

- `book/[...slug].astro`는 현재 `book` 컬렉션이 아니라 `works` 컬렉션 중 `published`인 원고를 렌더링한다.
- 이 때문에 `/book/buddha-story/01-birth` 같은 경로가 생성된다.
- 반면 `book/index.astro`의 카드 버튼은 `/books/buddha-story/`라는 public HTML을 연다.

판정:

- 운영 전 반드시 BOOK의 세부 라우트 정책을 정리해야 한다.
- 현재 `.ol-ref/사용법` 기준으로는 BOOK은 public 단일 HTML 중심이므로, `/book/[...slug]` 원고 렌더링은 제거하거나 WORKS에서만 유지하는 쪽이 더 일관적이다.

### DESIGN

파일:

- `src/pages/design/index.astro`
- `src/pages/design/[slug].astro`
- `src/lib/design.ts`

현황:

- 타입 필터, 태그 필터, 그리드, 상세 이미지, 메타데이터, 다운로드 버튼 구현
- 저장 정책은 `src/content/design/*.md` + `public/design/*` 분리 구조

앞으로의 방향:

- WALL-E 샘플을 불교 실제 레퍼런스로 교체
- 붓다스토리 캐릭터/배경 레퍼런스를 우선 제작
- type/series/entities/scriptureRef를 적극 사용

### ENTITY

파일:

- `src/pages/entity/index.astro`
- `src/pages/entity/[type]/[id].astro`
- `src/components/entity/*`
- `src/lib/relations.ts`

현황:

- 타입별 목록과 상세 페이지 구현
- 관계와 역참조 표시 컴포넌트 존재
- 지식 그래프의 장기 기반

문제:

- `getEntityRelations()`가 async 함수인데 호출부에서 await 없이 사용됨
- outgoing 관계 표시가 실제로 누락될 가능성이 높음

### BLOG

파일:

- `src/pages/blog/index.astro`
- `src/pages/blog/[slug].astro`
- `src/pages/rss.xml.ts`

현황:

- 작업 일지 중심의 블로그 목록/상세 구현
- 카테고리 필터, 연도 아카이브, 더 보기 구현
- RSS 생성

### AI

파일:

- `src/pages/ai.astro`
- `src/content/ai`

현황:

- 정적 컨셉 페이지
- 컬렉션 파일은 없음
- 빌드 경고 발생

방향:

- 지금은 “구상” 상태로 두는 것이 맞다.
- OL 철학상 AI는 중심 인터페이스가 아니라 요청 기반의 조용한 보조자다.

---

## 9. 빌드 검증

검증 명령:

```sh
npm run build
```

최근 확인 결과:

- Astro build 성공
- 정적 페이지 40개 생성
- sitemap 생성 성공
- Pagefind 인덱스 생성 성공
- Pagefind 기준 40페이지, 4,216 words 인덱싱
- `dist` 파일 수: 117
- `dist` 크기: 약 4.3 MB
- `public` 크기: 약 2.2 MB
- `src` 크기: 약 1.1 MB

빌드 경고:

- `src/content/ai`에 Markdown/MDX 파일이 없다는 경고
- 현재 기능 실패는 아니며, 빈 컬렉션을 유지하는 설계상 경고다.

---

## 10. 확인된 이슈

### P0-1. ENTITY 관계 렌더링 논리 버그

파일:

- `src/lib/relations.ts`
- `src/pages/entity/[type]/[id].astro`

문제:

```ts
export async function getEntityRelations(...)
```

이 함수는 Promise를 반환하지만 상세 페이지에서는 다음처럼 사용한다.

```ts
const outgoing = getEntityRelations(entry.data.id, allRelations);
...
{outgoing.length > 0 && (...)}
```

해결 방향:

- 함수 내부에 비동기 작업이 없으므로 `async` 제거
- 또는 호출부에서 `await` 후 반환 구조를 `{ outgoing, incoming }`에 맞게 조정

권장:

- `getEntityRelations`는 순수 동기 함수로 바꾼다.
- 현재 반환 형태가 `{ outgoing, incoming }`이므로 상세 페이지 변수명도 맞춘다.

### P0-2. BOOK 상세 라우트 정책 혼선

파일:

- `src/pages/book/[...slug].astro`
- `src/pages/book/index.astro`

문제:

- BOOK 목록은 완결 HTML 메타데이터 중심
- BOOK 상세 라우트는 WORKS 원고 렌더링 중심

권장:

- BOOK은 `public/books/{htmlPath}/index.html` 중심으로 통일한다.
- `/book/[...slug]`는 삭제하거나, 정말 필요하면 “웹 내장 리더” 역할로 별도 정책을 문서화한다.
- WORKS 원고는 `/works/*`에만 둔다.

### P1-1. README가 Astro 기본 템플릿

문제:

- 실제 프로젝트 구조, 콘텐츠 작성법, 빌드/배포, `.ol-ref` 문서 활용법을 설명하지 못한다.

권장:

- README를 OL HOME 운영 문서로 교체
- 최소 포함 항목:
  - 프로젝트 철학
  - 개발 명령
  - 콘텐츠 추가법
  - ATLAS/BOOK/DESIGN 저장 구조
  - 배포 흐름
  - 금지/주의 기능

### P1-2. DESIGN 콘텐츠 정합성

문제:

- 현재 DESIGN 공개 항목은 WALL-E 샘플
- 페이지 설명은 불교 콘텐츠 스타일 레퍼런스

권장:

- 샘플임을 명시하거나 비공개 처리
- 1차 실제 콘텐츠로 “붓다스토리 캐릭터/배경 레퍼런스” 제작

### P1-3. AI 빈 컬렉션 경고

문제:

- 매 빌드마다 경고 발생

선택지:

- 현 상태 유지: 구상 페이지이므로 경고 허용
- placeholder MD 추가: 경고 제거
- ai 컬렉션 제거: 향후 확장성 감소

권장:

- 당장은 유지 가능. 운영 문서에서 “AI 컬렉션은 아직 비어 있음”을 명시한다.

### P1-4. 검색 유틸 중복

파일:

- `src/lib/search.ts`

문제:

- 자체 `buildSearchIndex()`가 있지만 실제 검색은 Pagefind 중심
- 현재 라우트에서 직접 사용되는 흔적 없음

권장:

- Pagefind만 쓸지, Entity-aware 검색용 보조 인덱스로 살릴지 결정
- 살린다면 `book`, aliases, base URL 처리까지 보강

### P2-1. 접근성/모바일 검증 미완

점검 필요:

- href 없는 `<a>` 정리
- 검색 모달 키보드 탐색
- 모바일 하단 시트 focus/scroll lock
- WORKS 사이드바 닫힘/열림 aria 상태
- 디자인 카드/필터 키보드 조작

---

## 11. 콘텐츠 파이프라인 목표

`.ol-ref/브랜드/OL 홈페이지 전략 분석 및 향후 개발 로드맵.md` 기준으로 다음 단계의 핵심은 “완결된 하나”다.

권장 1차 목표:

```text
붓다스토리 1장 파이프라인 완주

WORKS
  1장 원고 완성
  원전/각주/Entity 연결 보강
    ↓
DESIGN
  붓다, 마야, 아난다 등 캐릭터 레퍼런스
  룸비니/카필라바스투 배경 레퍼런스
    ↓
BOOK
  ATLAS 기반 완성 HTML 생성
  public/books/buddha-story/index.html 등록
    ↓
BLOG
  제작 과정과 결정 기록 작성
```

이 파이프라인을 한 번 끝까지 돌리는 것이 새 기능 10개보다 중요하다. 그래야 실제 병목이 보인다.

---

## 12. 향후 개발 우선순위

### P0 — 즉시 처리

1. Entity 관계 렌더링 버그 수정
2. BOOK 상세 라우트 정책 정리
3. 모바일 WORKS/ATLAS 주요 화면 스모크 테스트

### P1 — 운영 전 정리

1. README 교체
2. DESIGN 샘플 콘텐츠 처리
3. AI 빈 컬렉션 경고 처리 방침 결정
4. 검색 유틸 사용 여부 결정
5. 콘텐츠 작성 규칙을 README 또는 `.ol-ref/사용법`에서 최신 코드 기준으로 동기화

### P2 — 콘텐츠 확장

1. 붓다스토리 1장 원고 완성
2. 붓다스토리 캐릭터/배경 DESIGN 자료 제작
3. 주요 Entity 확장
   - 인물: 붓다 10대 제자, 주요 재가 신자
   - 장소: 팔대성지, 주요 정사
   - 개념: 사성제, 팔정도, 무아, 열반 등
4. Entity relation predicate 검증

### P3 — 장기 기능

1. 절제된 Entity 관계 그래프
2. DESIGN series 묶음 뷰
3. WORKS ↔ BOOK 상호 링크
4. i18n 최소 영문 랜딩
5. PWA/오프라인 캐싱
6. OL TOON 초기 라우트

---

## 13. 개발자가 주의해야 할 규칙

### Astro 6 규칙

- `src/content.config.ts` 사용
- `glob` loader 사용
- `entry.id` 사용
- `render(entry)` 사용

### URL 규칙

- 내부 링크는 `url('/path')`를 우선 사용
- public asset도 base path를 고려해야 함

### 콘텐츠 저장 규칙

BOOK:

```text
src/content/book/buddha-story.md
public/books/buddha-story/index.html
htmlPath: "buddha-story"
```

DESIGN:

```text
src/content/design/ananda-turnaround.md
public/design/ananda-turnaround.png
imagePath: "ananda-turnaround.png"
```

WORKS:

```text
src/content/works/{series}/{chapter}.md
```

본문 이미지는 같은 폴더에 두고 상대 경로를 쓴다.

```md
![대체 텍스트](./image.jpg)
```

### 마크다운 주의

- 본문에서 `# h1`은 사용하지 않는다. 페이지 제목은 레이아웃이 만든다.
- CJK + 괄호 + `**` 볼드가 깨질 수 있다.
- `**도솔천(兜率天)**` 같은 패턴은 `<strong>도솔천(兜率天)</strong>` 사용.

---

## 14. 현재 판정

OL HOME은 구조적으로 올바른 방향에 있다. 특히 Content Collections, WORKS/BOOK 분리, Entity/Ontology 기반, Pagefind 검색, ATLAS 단일 HTML 연동은 프로젝트 철학과 잘 맞는다.

그러나 지금은 “기능을 더 붙일 때”가 아니라 “경계와 파이프라인을 단단히 할 때”다. 다음 전문가가 이 프로젝트를 이어받는다면 우선 다음 세 가지를 해야 한다.

1. BOOK/WORKS/ENTITY의 데이터 모델 경계를 정리한다.
2. 붓다스토리 1장을 실제 완성물로 끝까지 출판해 본다.
3. 모바일/접근성/빌드 검증을 반복 가능한 기준으로 만든다.

이 세 가지가 정리되면 OL HOME은 단순 소개 사이트가 아니라, OL 콘텐츠 생태계의 실제 운영 포털로 안정화될 수 있다.
