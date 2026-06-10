# OL 홈페이지 콘텐츠 관리 매뉴얼 v1

> **대상**: OL 프로젝트에 처음 참여하는 사람, Astro 기반 정적 사이트를 처음 접하는 사람
> **기준일**: 2026-05-31
> **기술 스택**: Astro 6 + GitHub Pages

---

## 0. 시작하기 전에 — 핵심 개념

### OL HOME의 구조

OL HOME은 **정적 사이트 생성기(SSG)** Astro로 만들어져 있습니다. 코드를 수정하고 `npm run build`를 실행하면 HTML 파일이 생성되고, 이것이 GitHub Pages에 배포됩니다.

콘텐츠는 **Markdown(.md) 파일**로 작성합니다. 각 md 파일 상단에 `---`로 감싼 **프론트매터(frontmatter)** 영역에 메타데이터를 적고, 그 아래에 본문을 적습니다.

```markdown
---
title: "제목"
date: 2026-06-01
published: true
---

여기에 본문을 적습니다.
```

### 두 곳에 나누어 저장하는 이유

OL의 콘텐츠는 크게 두 곳에 저장됩니다.

```
src/content/     ← 메타데이터 + 본문 (Markdown)
public/          ← 실제 파일 (HTML, 이미지 등)
```

이렇게 분리하는 이유는 **메타데이터와 실제 파일의 성격이 다르기 때문**입니다. 메타데이터(제목, 설명, 태그 등)는 목록 페이지에서 카드를 렌더링하는 데 쓰이고, 실제 파일(완성 HTML, 이미지)은 사용자가 직접 열거나 다운로드합니다.

### 프로젝트 폴더 전체 구조

```
ol-home/
├── public/                    ← 정적 파일 (빌드 시 그대로 복사됨)
│   ├── atlas/latest/          ← ATLAS 최신 파일
│   ├── books/                 ← BOOK 완성 HTML
│   └── design/                ← DESIGN 이미지
│
├── src/
│   ├── content/               ← 콘텐츠 (Markdown)
│   │   ├── blog/              ← 블로그 포스트
│   │   ├── book/              ← BOOK 메타데이터
│   │   ├── works/             ← WORKS 원고
│   │   ├── design/            ← DESIGN 메타데이터
│   │   ├── pages/             ← 상설 문서
│   │   ├── entities/          ← 엔티티 (인물, 장소, 개념 등)
│   │   └── ontology/          ← 온톨로지 정의
│   │
│   ├── lib/site.ts            ← 사이트 공통 설정 (이메일, GitHub 등)
│   └── content.config.ts      ← 콘텐츠 스키마 정의
│
└── astro.config.mjs           ← Astro 설정 (site URL, base 경로)
```

### 빌드와 배포

```bash
# 로컬에서 개발 서버 실행 (미리보기)
npm run dev

# 빌드 (dist/ 폴더에 HTML 생성)
npm run build

# 빌드 결과 미리보기
npm run preview
```

GitHub에 push하면 GitHub Actions가 자동으로 빌드하고 GitHub Pages에 배포합니다.

---

## 1. ATLAS 페이지

ATLAS는 단일 HTML 파일로 동작하는 콘텐츠 뷰어입니다. 홈페이지는 `public/atlas/latest/` 폴더에 있는 파일을 자동으로 감지합니다.

### 1.1 새 버전 배포하기

**1단계**: 파일명을 `ol-atlas_v{버전}.html` 형식으로 저장합니다.

```
예: ol-atlas_v0.0.7.html
```

**2단계**: `public/atlas/latest/` 폴더에 넣습니다. 기존 파일을 교체합니다.

```
public/atlas/latest/ol-atlas_v0.0.7.html
```

**3단계**: 빌드합니다. 끝입니다.

```bash
npm run build
```

### 1.2 자동 감지 원리

빌드 시 `atlas.astro`가 `public/atlas/latest/` 폴더를 스캔해서 `ol-atlas_v{버전}.html` 패턴에 맞는 파일을 찾습니다. 파일명에서 **버전**, **파일 크기**를 자동 추출하여 페이지 전체에 반영합니다.

- Hero 다운로드/열기 버튼
- iframe 미리보기
- 사이드바 다운로드 카드

모두 자동으로 갱신됩니다. **하드코딩 수정이 필요 없습니다.**

### 1.3 파일명 규칙

```
반드시: ol-atlas_v{버전}.html
예시:   ol-atlas_v0.0.6.html
        ol-atlas_v1.0.0.html
        ol-atlas_v2.1.0-beta.html

잘못된 예: atlas.html, ol-atlas.html, v0.0.6.html
```

`latest/` 폴더에는 **파일 하나만** 두세요. 여러 개 있으면 첫 번째 매칭 파일이 사용됩니다.

### 1.4 이전 버전 보관 (선택)

이전 버전을 보관하고 싶으면 별도 폴더에 저장합니다.

```
public/atlas/v0.0.6/ol-atlas_v0.0.6.html    ← 보관용
public/atlas/latest/ol-atlas_v0.0.7.html     ← 최신 (자동 감지 대상)
```

---

## 2. WORKS 페이지

WORKS는 완결 이전의 초고, 번역 초안, 주석 연구를 공개하는 작업장입니다.

### 2.1 새 원고 추가하기

**1단계**: `src/content/works/` 아래에 시리즈 폴더를 만듭니다.

```
src/content/works/buddha-story/       ← "붓다 스토리" 시리즈
src/content/works/diamond-sutra/      ← "금강경공부" 시리즈
src/content/works/lamrim/             ← "람림공부" 시리즈
```

**2단계**: 시리즈 폴더 안에 Markdown 파일을 만듭니다.

```
src/content/works/buddha-story/01-birth.md
src/content/works/buddha-story/02-renunciation.md
```

**3단계**: 프론트매터를 작성합니다.

```yaml
---
title: "1장 — 탄생: 도솔천에서 룸비니까지"
series: "붓다 스토리"
category: "인물 · 행적"
status: revising
order: 1
tags: ["불전", "탄생"]
published: true
---
```

**4단계**: `---` 아래에 본문을 작성합니다.

### 2.2 메타데이터 필드 설명

| 필드          | 필수     | 설명                          | 예시                                        |
| ----------- | ------ | --------------------------- | ----------------------------------------- |
| `title`     | **필수** | 원고 제목                       | `"1장 — 탄생"`                               |
| `series`    | 권장     | 소속 시리즈명 (같은 값이면 같은 그룹으로 묶임) | `"붓다 스토리"`                                |
| `category`  | 선택     | 카테고리 (필터 칩에 표시됨)            | `"인물 · 행적"`, `"경전"`, `"수행"`               |
| `status`    | 선택     | 작업 상태                       | `draft`, `revising`, `ready`, `published` |
| `order`     | 선택     | 시리즈 내 정렬 순서 (기본값 0)         | `1`, `2`, `3`                             |
| `chapter`   | 선택     | 챕터 번호 (목록에 표시)              | `1`                                       |
| `tags`      | 선택     | 태그 (드롭다운 필터에 사용)            | `["불전", "탄생"]`                            |
| `published` | 선택     | 발행 여부 (기본값 false)           | `true`                                    |
| `excerpt`   | 선택     | 짧은 발췌문 (목록에 표시)             | `"도솔천에서의 결심..."`                          |
| `date`      | 선택     | 작성/수정일                      | `2026-06-01`                              |
| `entities`  | 선택     | 관련 엔티티 ID                   | `["siddhartha-gautama"]`                  |

### 2.3 이미지 추가하기

Works 본문에 이미지를 넣으려면 **같은 폴더에 이미지를 저장**하고 상대 경로로 참조합니다.

```
src/content/works/buddha-story/
  01-birth.md
  lumbini-garden.jpg      ← 이미지 파일
```

본문에서:

```markdown
![룸비니 동산](./lumbini-garden.jpg)
```

Astro가 빌드 시 이미지를 자동으로 최적화합니다.

### 2.4 시리즈 없는 독립 문서

시리즈에 속하지 않는 독립 문서는 `series`를 생략하면 "독립 문서" 그룹으로 자동 분류됩니다.

```
src/content/works/standalone-essay.md
```

---

## 3. BOOK 페이지

BOOK은 완결된 출판물입니다. **완성 HTML**과 **메타데이터 md**를 각각 다른 위치에 저장합니다.

### 3.1 새 BOOK 등록하기

**1단계**: 완성 HTML을 `public/books/` 아래 폴더에 저장합니다.

```
public/books/buddha-story/index.html
```

**2단계**: 메타데이터 md를 `src/content/book/`에 만듭니다.

```
src/content/book/buddha-story.md
```

**3단계**: 프론트매터를 작성합니다.

```yaml
---
title: "붓다 스토리"
subtitle: "부처님의 일대기"
series: "OL 붓다 스토리"
category: "인물 · 행적"
version: "v1.0"
publishedAt: 2026-06-01
htmlPath: "buddha-story"
description: "싯다르타 고타마의 생애를 원전 기반으로 재구성했습니다."
tags: ["불전", "초기불교"]
level: 1
published: true
---
```

### 3.2 메타데이터 필드 설명

| 필드 | 필수 | 설명 | 예시 |
|------|------|------|------|
| `title` | **필수** | 책 제목 | `"붓다 스토리"` |
| `publishedAt` | **필수** | 출판일 | `2026-06-01` |
| `htmlPath` | **필수** | `public/books/` 아래 폴더명 | `"buddha-story"` |
| `version` | 선택 | 버전 (다운로드 파일명에 포함) | `"v1.0"` |
| `subtitle` | 선택 | 부제 | `"부처님의 일대기"` |
| `series` | 선택 | 시리즈명 | `"OL 붓다 스토리"` |
| `category` | 선택 | 카테고리 | `"인물 · 행적"` |
| `description` | 선택 | 설명 (카드에 표시) | `"원전 기반 재구성..."` |
| `tags` | 선택 | 태그 (필터에 사용) | `["불전", "초기불교"]` |
| `level` | 선택 | 난이도 (1~5) | `1` |
| `published` | 선택 | 발행 여부 (기본값 true) | `true` |

### 3.3 핵심 규칙: htmlPath와 폴더명 일치

`htmlPath`의 값과 `public/books/` 아래의 **폴더명이 정확히 일치**해야 합니다.

```
htmlPath: "buddha-story"
→ public/books/buddha-story/index.html  (이 경로에 파일이 있어야 함)
```

### 3.4 다운로드 파일명

사용자가 "내려받기" 버튼을 클릭하면 `{title}-{version}.html` 형식으로 저장됩니다.

```
예: "붓다 스토리-v1.0.html"
```

### 3.5 웹에서 읽기 vs 내려받기

두 버튼 모두 같은 파일(`index.html`)을 가리킵니다.
- "웹에서 읽기" → 새 탭에서 열기
- "내려받기" → `download` 속성으로 파일 저장

---

## 4. DESIGN 페이지

DESIGN은 불교 콘텐츠 제작을 위한 스타일 레퍼런스 아카이브입니다.

### 4.1 새 이미지 등록하기

**1단계**: 이미지 파일을 `public/design/`에 저장합니다.

```
public/design/gandhara-buddha-face.jpg
```

**2단계**: 메타데이터 md를 `src/content/design/`에 만듭니다.

```
src/content/design/gandhara-buddha-face.md
```

**3단계**: 프론트매터를 작성합니다.

```yaml
---
title: "간다라 양식 불상 얼굴"
type: portrait
era: "1~3세기"
region: "간다라 (현 파키스탄)"
tradition: "초기 대승"
imagePath: "gandhara-buddha-face.jpg"
imageAlt: "간다라 양식 불상의 정면 얼굴 클로즈업"
source: "OL Project 자체 제작"
sourceUrl: ""
license: "CC0"
tags: [간다라, 불상, 초기대승]
published: true
---

간다라 지역의 헬레니즘 영향을 받은 불상 양식입니다.
```

### 4.2 메타데이터 필드 설명

| 필드 | 필수 | 설명 | 예시 |
|------|------|------|------|
| `title` | **필수** | 이미지 제목 | `"간다라 양식 불상 얼굴"` |
| `imagePath` | 권장 | `public/design/` 기준 파일명 | `"gandhara-buddha-face.jpg"` |
| `type` | 선택 | 분류 (사이드바 필터에 사용) | 아래 표 참조 |
| `era` | 선택 | 시대 | `"1~3세기"` |
| `region` | 선택 | 지역 | `"간다라"` |
| `tradition` | 선택 | 전통 | `"초기 대승"` |
| `imageAlt` | 선택 | 대체 텍스트 (접근성) | `"불상 정면 클로즈업"` |
| `source` | 선택 | 출처 | `"OL Project 자체 제작"` |
| `sourceUrl` | 선택 | 출처 URL | `"https://..."` |
| `license` | 선택 | 라이선스 (기본값 CC0) | `"CC0"` |
| `tags` | 선택 | 태그 | `["간다라", "불상"]` |
| `published` | 선택 | 발행 여부 (기본값 false) | `true` |

### 4.3 type 분류표

| 값 | 의미 | 사이드바 표시 |
|----|------|-------------|
| `portrait` | 인물·도상 | 인물 · 도상 |
| `costume` | 복장·가사 | 복장 · 가사 |
| `architecture` | 건축·사찰 | 건축 · 사찰 |
| `landscape` | 지역·자연 | 지역 · 자연 |
| `manuscript` | 원문·필사 | 원문 · 필사 |
| `artifact` | 유물·공예 | 유물 · 공예 |
| `other` | 기타 | 기타 |

### 4.4 이미지 파일 규칙

- **권장 포맷**: WebP, JPG, PNG
- **권장 크기**: 웹용 최적화 (가로 2000px 이하, 파일 2MB 이하)
- **파일명**: 영문 소문자 + 하이픈, 공백 사용 금지

```
좋은 예: gandhara-buddha-face.jpg
나쁜 예: 간다라 불상.jpg, Gandhara Buddha.PNG
```

### 4.5 이미지 다운로드

상세 페이지에서 "이미지 다운로드" 버튼이 자동 표시됩니다. `imagePath`가 있는 항목에만 표시됩니다.

---

## 5. BLOG 페이지

BLOG는 OL의 작업 일지입니다.

### 5.1 새 포스트 작성하기

**1단계**: `src/content/blog/` 아래에 **폴더**를 만듭니다. 폴더명이 URL slug가 됩니다.

```
src/content/blog/my-first-post/
```

**2단계**: 폴더 안에 `index.md`를 만듭니다.

```
src/content/blog/my-first-post/index.md
```

**3단계**: 프론트매터를 작성합니다.

```yaml
---
title: "첫 번째 포스트"
description: "이 포스트에서는..."
date: 2026-06-01
category: OL
readingTime: 5
tags: ["개발", "Astro"]
published: true
---

여기에 본문을 작성합니다.
```

### 5.2 메타데이터 필드 설명

| 필드 | 필수 | 설명 | 예시 |
|------|------|------|------|
| `title` | **필수** | 포스트 제목 | `"첫 번째 포스트"` |
| `date` | **필수** | 발행일 (목록 정렬에 사용) | `2026-06-01` |
| `description` | 권장 | 설명 (목록 카드에 표시) | `"이 포스트에서는..."` |
| `category` | 선택 | 카테고리 (필터 칩에 표시) | `"OL"`, `"ATLAS"`, `"BOOK"` |
| `readingTime` | 선택 | 읽기 시간 (분) | `5` |
| `tags` | 선택 | 태그 | `["개발", "Astro"]` |
| `published` | 선택 | 발행 여부 (**기본값 false**) | `true` |

> **주의**: `published`의 기본값이 `false`입니다. `published: true`를 반드시 적어야 목록에 표시됩니다.

### 5.3 포스트에 이미지 추가하기

포스트 폴더 안에 이미지를 넣고 상대 경로로 참조합니다.

```
src/content/blog/my-first-post/
  index.md
  screenshot.png      ← 이미지
```

본문에서:

```markdown
![스크린샷](./screenshot.png)
```

목록 페이지에서 본문의 **첫 번째 이미지**가 자동으로 썸네일로 사용됩니다.

### 5.4 카테고리와 연도 필터

목록 페이지에서 카테고리 칩과 사이드바 연도 필터가 자동 생성됩니다. 포스트의 `category`와 `date`에서 추출하므로 별도 설정이 필요 없습니다.

---

## 6. PAGES — 상설 문서

시간순으로 흐르지 않는 고정 문서(선언문, 스타일 가이드 등)를 위한 컬렉션입니다.

### 6.1 새 상설 문서 추가하기

**1단계**: `src/content/pages/`에 md 파일을 만듭니다.

```
src/content/pages/rfc.md
```

**2단계**: 프론트매터를 작성합니다.

```yaml
---
title: "RFC · 설계 노트"
description: "OL 프로젝트의 설계 결정과 그 배경"
published: true
---
```

URL은 `/pages/{파일명}`이 됩니다.

```
src/content/pages/rfc.md          → /pages/rfc
src/content/pages/manifesto.md    → /pages/manifesto
src/content/pages/style-guide.md  → /pages/style-guide
```

### 6.2 푸터 링크 연결

새 상설 문서를 푸터에 추가하려면 `src/components/layout/OLFooter.astro`를 수정합니다.

---

## 7. 사이트 공통 설정

### 7.1 사이트 정보 변경

`src/lib/site.ts`에서 사이트 공통 정보를 관리합니다.

```typescript
export const site = {
  name: 'OL',
  tagline: '지혜의 올을 짜다',
  email: 'biwoom.ol@gmail.com',
  github: 'https://github.com/biwoom',
  license: 'https://creativecommons.org/publicdomain/zero/1.0/',
} as const;
```

이 값을 변경하면 푸터 등 사이트 전체에 반영됩니다.

### 7.2 배포 설정

`astro.config.mjs`에서 site URL과 base 경로를 설정합니다.

```javascript
export default defineConfig({
  site: 'https://biwoom.github.io',
  base: '/ol-home',
});
```

---

## 8. 자주 하는 실수와 해결법

### 8.1 콘텐츠가 목록에 안 보여요

→ `published: true`를 확인하세요. 대부분의 컬렉션은 기본값이 `false`입니다.

### 8.2 빌드 오류: 스키마 불일치

→ 프론트매터 필드명이 스키마와 정확히 일치하는지 확인하세요. 오타가 있으면 빌드가 실패합니다.

```yaml
# 잘못된 예
Title: "..."       # title이어야 함 (소문자)
publish: true      # published이어야 함
```

### 8.3 이미지가 안 보여요

→ **DESIGN**: `imagePath`의 파일명과 `public/design/`의 실제 파일명이 일치하는지 확인하세요. 대소문자도 구분합니다.

→ **BLOG/WORKS 본문 이미지**: 상대 경로 `./`로 시작하는지 확인하세요.

### 8.4 BOOK 링크가 깨져요

→ `htmlPath`와 `public/books/` 아래 폴더명이 정확히 일치하는지 확인하세요.

```
htmlPath: "buddha-story"  →  public/books/buddha-story/index.html
```

### 8.5 ATLAS 버전이 0.0.0으로 표시돼요

→ 파일명이 `ol-atlas_v{버전}.html` 패턴을 따르는지 확인하세요. 언더스코어(`_`)와 소문자 `v`가 정확해야 합니다.

---

## 9. 콘텐츠 등록 체크리스트

새 콘텐츠를 등록할 때마다 확인하세요.

### ATLAS

- [ ] 파일명: `ol-atlas_v{버전}.html`
- [ ] 위치: `public/atlas/latest/`
- [ ] 기존 파일 교체 완료

### WORKS

- [ ] 시리즈 폴더 생성 (필요시)
- [ ] md 파일 생성: `src/content/works/{시리즈}/{파일명}.md`
- [ ] `title`, `series`, `order` 작성
- [ ] `published: true` 설정
- [ ] 이미지는 같은 폴더에 저장, 상대 경로 참조

### BOOK

- [ ] 완성 HTML: `public/books/{이름}/index.html`
- [ ] 메타데이터: `src/content/book/{이름}.md`
- [ ] `htmlPath`와 폴더명 일치 확인
- [ ] `published: true` 설정

### DESIGN

- [ ] 이미지 파일: `public/design/{파일명}.{확장자}`
- [ ] 메타데이터: `src/content/design/{파일명}.md`
- [ ] `imagePath`와 실제 파일명 일치 확인
- [ ] `published: true` 설정

### BLOG

- [ ] 폴더 생성: `src/content/blog/{slug}/`
- [ ] `index.md` 생성
- [ ] `title`, `date` 작성
- [ ] `published: true` 설정 (**기본값이 false**)
- [ ] 이미지는 같은 폴더에 저장

### 공통

- [ ] `npm run build` 무오류 확인
- [ ] `npm run dev`로 로컬에서 미리보기

---

## 10. 스키마 참조표

모든 컬렉션의 스키마는 `src/content.config.ts`에 정의되어 있습니다. 새 필드를 추가하려면 이 파일의 해당 컬렉션 스키마를 수정해야 합니다.

### published 기본값 주의

| 컬렉션 | `published` 기본값 | 설명 |
|--------|-------------------|------|
| blog | `false` | 반드시 `true`로 명시해야 발행 |
| works | `false` | 반드시 `true`로 명시해야 발행 |
| design | `false` | 반드시 `true`로 명시해야 발행 |
| book | `true` | 기본 발행, 숨기려면 `false` 명시 |
| pages | `true` | 기본 발행, 숨기려면 `false` 명시 |

---

**매뉴얼 버전**: v1.0
**기준일**: 2026-05-31
**대상 프로젝트**: OL HOME (Astro 6 + GitHub Pages)
