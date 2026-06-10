# OL ATLAS 현재상태 및 OL-DESK 의미중심 전환 검토보고서

작성일: 2026-06-07  
대상 저장소: `/Users/damjin/Projects/ol-project/github/ol-atlas`  
참조 문서: `07_OL-DESK_의미중심_전환기획.md`

---

## 1. 요약

OL ATLAS는 현재 단일 HTML 파일로 동작하는 로컬 우선 콘텐츠 제작 도구다. 핵심 단위는 `card`이고, 카드는 `column`, `group`, `tags`, `status`, `priority`, `body`를 통해 보드, 카드 목록, 문서뷰, 독서뷰에서 다른 방식으로 재배열된다.

현재 버전은 `0.0.8`이며, 최신 변경사항은 WORKS zip 가져오기 기능이다. WORKS 원고의 frontmatter를 자동 판별하여 ATLAS 카드 스키마로 매핑하고, zip 내부에서 같은 폴더에 있는 이미지를 마크다운 본문에 data URL로 포함한다.

OL-DESK 의미중심 전환기획 관점에서 ATLAS는 이미 `Source Board Mode`, `Meaning Board Mode`, `Desk Mode`의 UI 원형 일부를 갖고 있다. 특히 칸반보드, 카드 중심 UI, 문서뷰, 독서뷰는 “자료를 모으고, 의미 단위로 정리하고, 최종 원고처럼 읽고 쓰는” 작업 흐름에 직접 기여할 수 있다.

다만 ATLAS는 아직 `meaning_unit`, `source_packet`, `chapter_dossier`, `grounding`, `interpretation`, `rendering` 같은 OL-DESK 전환기획의 구조화 계층을 별도 스키마로 갖고 있지 않다. 따라서 ATLAS는 현재 “의미중심 작업실의 UI/UX 프로토타입과 로컬 저작 도구”로는 적합하지만, OL-DESK 전체 시스템의 데이터 백본을 그대로 대체하기에는 부족하다.

---

## 2. 저장소 현재 상태

### 2.1 버전과 Git 상태

- 현재 패키지 버전: `0.0.8`
- 최신 커밋: `e270d95 업데이트: v0.0.8 WORKS zip 가져오기`
- 브랜치 상태: `main...origin/main`
- 원격 반영 상태: 최신 변경사항은 `origin/main`에 업로드된 상태

### 2.2 전체 디렉토리 구조

주요 구조는 다음과 같다.

```text
ol-atlas/
  README.md
  package.json
  package-lock.json
  build/
    build.mjs
    dev.mjs
    inline.mjs
    fixtures/
  dist/
    index.html
    ol-atlas_v0.0.7.html
    ol-atlas_v0.0.8.html
    bundle.css
  src/
    actions/
      card-actions.js
      column-actions.js
      export-import.js
      settings-actions.js
    components/
      author/
        bulk-select.js
        card-modal.js
        cardgrid.js
        color-picker.js
        home.js
        kanban.js
        listview.js
        md-editor.js
      shared/
        about.js
        dirty-indicator.js
        docview.js
        reader.js
        sidebar.js
        trash.js
    core/
      action.js
      body-helpers.js
      constants.js
      dirty.js
      editing-state.js
      events.js
      fingerprint.js
      markdown.js
      md-parser.js
      normalize.js
      render-queue.js
      router.js
      schema.js
      state.js
      static-html.js
      storage.js
      store.js
      tag-filter.js
      tag-parser.js
      theme.js
      utils.js
      zip.js
    data/
    i18n/
    styles/
    ui/
```

---

## 3. ATLAS의 기본 특징

### 3.1 단일 HTML 기반 로컬 우선 도구

ATLAS는 서버, 계정, 데이터베이스 없이 브라우저에서 동작하는 구조다. 상태는 `localStorage`의 `ol_state`에 저장되고, 내보내기 시 앱 코드와 콘텐츠 상태를 하나의 HTML 파일에 포함한다.

이 구조의 장점은 명확하다.

- 설치 없이 실행 가능
- HTML 파일 하나로 작업실과 콘텐츠를 함께 전달 가능
- 외부 서버 의존성이 낮음
- 원고, 이미지, 카드, 설정을 한 파일에 담을 수 있음

제약도 있다.

- 대규모 이미지와 다량 문서에서는 `localStorage`와 단일 HTML 용량이 커짐
- 협업, 권한, 동시 편집, 서버 동기화 구조는 없음
- 복합 검색, 그래프 쿼리, 대규모 관계 데이터 관리에는 한계가 있음

### 3.2 카드 중심 콘텐츠 모델

ATLAS의 기본 단위는 카드다. 하나의 카드는 제목, 본문, 그룹, 태그, 컬럼, 우선순위, 학습상태를 가진다. 같은 카드 데이터가 칸반, 카드그리드, 리스트, 문서뷰, 독서뷰에서 다른 화면으로 렌더링된다.

이 구조는 원고 문헌, 작업 단위, 의미 단위, 발췌 묶음, 장별 dossier를 모두 카드로 임시 모델링할 수 있다는 점에서 OL-DESK 전환기획과 연결된다.

---

## 4. UI 특징

### 4.1 칸반보드

칸반보드는 `src/components/author/kanban.js`에서 구현된다. 컬럼은 작업 흐름을 나타내며, 카드는 drag and drop으로 컬럼 간 이동 및 순서 변경이 가능하다.

현재 구현 특징:

- 컬럼 추가, 이름 변경, 색상 변경, 삭제
- 카드 추가, 편집, 삭제
- 카드 드래그 이동
- 컬럼별 카드 수 표시
- 카드 본문 미리보기 표시
- 카드 태그와 작성일 표시
- 카드에서 바로 문서뷰로 이동

OL-DESK 관점에서는 이 칸반보드가 `Source Board Mode`와 `Meaning Board Mode`의 기본 골격으로 재사용될 수 있다. 예를 들어 컬럼을 `원천자료`, `목차`, `사건`, `주제`, `챕터 dossier`, `표현 후보`, `검토 완료` 등으로 정의하면 자료 수집과 의미 판단의 흐름을 시각적으로 관리할 수 있다.

### 4.2 카드그리드와 리스트

카드그리드는 `src/components/author/cardgrid.js`에서 구현된다. 컬럼, 그룹, 상태, 태그, prefix 태그 기준으로 필터링하고, 제목/우선순위/상태/작성일 기준으로 정렬할 수 있다.

현재 구현 특징:

- 카드형 UI 중심의 빠른 탐색
- 컬럼 필터
- 그룹 필터
- 상태 필터
- 일반 태그 필터
- prefix 태그 필터
- 제목/우선순위/상태/작성일 정렬
- 라쏘 선택과 벌크 액션
- 카드에서 문서뷰로 이동

이 화면은 OL-DESK의 “의미 단위 카드”나 “source packet 카드”를 훑어보고 분류하는 데 적합한 패턴이다.

### 4.3 문서뷰

문서뷰는 `src/components/shared/docview.js`에서 구현된다. 카드 하나를 문서처럼 읽고, 필요하면 인라인 편집으로 전환한다.

현재 구현 특징:

- 카드 본문을 마크다운 문서로 렌더링
- H1-H3 기반 목차 자동 생성
- 이전/다음 카드 이동
- 문서 메타데이터 표시: 컬럼, 그룹, 우선순위, 상태, 태그
- 인라인 편집 지원
- 제목, 그룹, 태그, 슬러그, 컬럼, 우선순위, 상태 수정
- 마크다운 툴바와 미리보기
- 이미지 패널
- 편집 중 뷰 전환 가드
- 문서 단위 `.md` 내보내기

OL-DESK 전환기획의 `Desk Mode`와 가장 직접적으로 연결되는 화면이다. 최종 원고, 해설글, 에세이, 대본을 문서 중심으로 쓰고 다듬는 경험에 이미 가까운 형태를 갖고 있다.

### 4.4 독서뷰

독서뷰는 `src/components/shared/reader.js`에서 구현된다. 일반 앱 헤더와 사이드바를 숨기고, 본문 읽기에 집중하는 화면이다.

현재 구현 특징:

- 전체 화면에 가까운 읽기 모드
- 왼쪽 문서 목록 패널
- 오른쪽 목차 패널
- 패널 hover/pin 동작
- 글자 크기 조절
- 테마 전환
- 스크롤 방향에 따른 상단바 숨김
- 이전/다음 문서 이동
- 카드 메타데이터와 태그 표시

OL-DESK 관점에서는 “완성 원고가 독자에게 어떻게 읽히는가”를 확인하는 검토 모드로 가치가 있다. 전환기획에서 말하는 장시간 읽기, 여백, 타이포그래피, UI 은닉 원칙과 잘 맞는다.

### 4.5 사이드바

사이드바는 현재 보드/카드 탐색용과 문서뷰용으로 다르게 렌더링된다.

일반 뷰에서는 다음을 제공한다.

- 컬럼 목록
- 그룹 목록
- 일반 태그 목록
- prefix 태그 드롭다운
- 태그 검색
- 필터 해제
- 휴지통/정보 섹션

문서뷰에서는 다음을 제공한다.

- 컬럼별 문서 트리
- 그룹별 문서 접기/펼치기
- 현재 문서 active 표시

이 구조는 OL-DESK의 `Source Board Mode`에서 원천자료, 주제, 사건, 목차 단위를 탐색하는 왼쪽 정보 패널로 확장할 수 있다.

---

## 5. 태그 시스템

ATLAS의 태그는 카드의 `tags` 배열에 저장된다.

현재 태그 시스템은 두 층으로 동작한다.

- 일반 태그: `수행`, `해설`, `붓다전기` 같은 자유 태그
- prefix 태그: `source:니까야`, `theme:출가`, `status:검토` 같은 `prefix:value` 형태

`src/core/tag-parser.js`는 태그 문자열을 prefix와 value로 파싱한다. `src/core/tag-filter.js`와 사이드바는 일반 태그 선택, prefix 태그 인덱스, 태그 검색, 필터링을 제공한다.

WORKS 가져오기에서는 일반 `tags`가 있으면 그것을 우선 사용하고, 일반 태그가 없을 때만 `prefixTags`를 fallback으로 가져온다. 이 전략은 홈페이지 WORKS 메타데이터와 ATLAS 태그 체계의 충돌을 줄이는 방식이다.

OL-DESK 전환기획 관점에서 prefix 태그는 빠른 프로토타이핑에 유용하다. 예를 들어 다음처럼 사용할 수 있다.

```text
source:니까야
source:불전
theme:출가
event:성도
grounding:direct
rendering:commentary
reader:general
```

다만 장기적으로 `grounding`, `rendering_type`, `source_basis`, `editor_decision` 같은 핵심 필드는 태그만으로 유지하기보다 명시적 메타데이터 스키마로 승격하는 것이 좋다.

---

## 6. 스키마와 메타데이터 상태

### 6.1 현재 스키마 버전

현재 스키마 버전은 `10`이다.

`src/core/schema.js`의 마이그레이션 흐름:

- v6 -> v7: settings, dirty, lastSavedAt 추가
- v7 -> v8: editors, saveLog, currentEditorId, card.acts 추가
- v8 -> v9: meta.actLog 추가
- v9 -> v10: meta.bookInfo 추가

### 6.2 최상위 상태 구조

기본 상태는 `src/core/state.js`의 `makeDefault()`에서 정의된다.

```text
state
  meta
  settings
  columns
  cards
  userData
  nextColId
  nextCardId
  trash
```

### 6.3 meta

`meta`는 파일과 책 단위의 정보를 담는다.

```text
meta
  fileId
  title
  created
  version
  schemaVersion
  dirty
  lastSavedAt
  editors
  saveLog
  actLog
  currentEditorId
  bookInfo
```

`bookInfo`는 책 수준의 서지 정보를 위한 확장이다.

```text
bookInfo
  bookTitle
  subtitle
  author
  translator
  publisher
  publishedAt
  revisedAt
  bookVersion
  description
  coverColor
  language
  isbn
```

### 6.4 card

카드는 실제 콘텐츠와 작업 단위를 담는다.

```text
card
  id
  colId
  title
  body
  group
  tags
  priority
  created
  slug
  images
  acts
```

상태값은 카드 내부가 아니라 `userData.status[card.id]`에 저장된다. 가능한 값은 현재 UI 기준으로 다음과 같다.

```text
wait  = 학습대기
doing = 학습중
done  = 학습완료
```

### 6.5 schema 설계 평가

현재 스키마는 단순하고 이식성이 좋다. 카드, 컬럼, 그룹, 태그만으로도 상당히 다양한 작업 구조를 만들 수 있다.

그러나 OL-DESK 의미중심 전환기획에서 요구하는 다음 계층은 아직 명시적 구조로 없다.

```text
source_collection
source_profile
source_toc
event
theme
alignment
excerpt
source_packet
chapter_dossier
outline_draft
composition_plan
meaning_unit
interpretation
claim
rendering
grounding
review_decision
export_version
```

따라서 ATLAS를 OL-DESK로 직접 확장하려면 `card.type`, `card.meta`, `relations`, `sourceRefs`, `renderings`, `reviewLog` 같은 구조가 필요하다.

---

## 7. 핵심 설계

### 7.1 중앙 상태와 액션 디스패치

상태 변경은 `src/core/action.js`의 `dispatch(action)`을 통해 수행된다. `S` 프록시는 직접 변경을 금지하고, reducer를 통해 상태를 갱신한다.

현재 설계 특징:

- 중앙 store: `src/core/store.js`
- reducer 등록: `registerReducer`
- 단일 dispatch 진입점
- 카드 생성/수정/삭제/복구 시 `acts` 기록
- 변경 발생 시 dirty 처리
- 변경 영향 범위에 따라 render queue 등록

이 구조는 작은 단일 페이지 앱으로서는 명확하다. OL-DESK처럼 상태와 작업 로그가 중요한 시스템에서는 이 액션 기반 변경 기록 구조를 더 확장할 수 있다.

### 7.2 렌더 큐와 뷰별 구독

각 화면은 `subscribe(viewName, renderFn)`으로 렌더러를 등록한다. 상태 변경 후 `queueRender()`가 호출되고, 필요한 뷰만 다시 렌더링한다.

이 방식은 DOM 기반 앱의 복잡도를 낮추면서도 화면별 관심사를 분리한다.

### 7.3 저장과 내보내기

현재 지원하는 저장/내보내기/가져오기:

- OL HTML 파일 저장
- OL HTML 파일 열기
- 카드 JSON 내보내기/가져오기
- 전체 카드 Markdown 내보내기
- 카드별 Markdown zip 내보내기
- Markdown 파일 다중 가져오기
- WORKS zip 가져오기

WORKS zip 가져오기는 현재 v0.0.8의 핵심 기능이다.

동작 방식:

- zip에서 `.md`, `.markdown` 파일을 찾음
- 같은 폴더의 이미지 파일을 찾음
- 본문에 상대경로 이미지가 있으면 data URL로 치환
- 본문에 참조되지 않은 같은 폴더 이미지는 `## 첨부 이미지` 아래 추가
- WORKS frontmatter이면 ATLAS 카드 메타데이터로 자동 매핑
- 기존 가져오기 병합 모달로 연결

---

## 8. 라우터 작동 방식

라우터는 `src/core/router.js`에 있다.

현재 뷰:

```text
home
kanban
cards
list
document
reader
about
trash
```

`switchView(v)`는 다음을 수행한다.

- 현재 뷰 변경
- `body.is-home` 토글
- `.view.active` 변경
- 헤더 nav active 변경
- 사이드바와 대상 뷰 렌더 큐 등록
- 마지막 뷰를 `localStorage.ol_last_view`에 저장
- hash 갱신
- post switch hook 실행

hash 규칙:

```text
home          -> hash 제거
kanban        -> #kanban
cards         -> #cards
list          -> #list
about         -> #about
trash         -> #trash
document card -> #document/{slugOrId}
reader        -> #reader
```

단, `routeFromHash()`는 현재 `reader` hash를 명시적으로 처리하지 않는다. `switchView('reader')`로 진입하면 동작하지만, 새로고침이나 직접 URL 접근에서 `#reader`는 home으로 떨어질 가능성이 있다. 독서뷰를 공유 가능한 라우트로 삼으려면 `routeFromHash()`에 `reader`와 `reader/{slug}` 처리가 필요하다.

문서뷰는 편집 중 변경사항이 있으면 뷰 전환 전에 확인 모달을 띄운다. 이 점은 OL-DESK의 감수/편집 작업에서 중요한 안전장치다.

---

## 9. WORKS 가져오기와 메타데이터 매핑 상태

현재 `src/core/md-parser.js`는 ATLAS Markdown과 WORKS Markdown을 구분한다.

WORKS로 판별하는 조건:

- `series`
- `part`
- `category`
- `published`
- `prefixTags`

단, `column` 또는 `learnStatus`가 있으면 ATLAS Markdown으로 본다.

WORKS 매핑:

```text
title       -> card.title
part        -> card.column
category    -> card.column fallback
group       -> card.group
status      -> learnStatus
tags        -> card.tags 우선
prefixTags  -> tags가 없을 때만 fallback
date        -> created
slug        -> slug
body        -> body
```

status 매핑:

```text
draft     -> wait
revising  -> doing
ready     -> done
published -> done
```

이 전략은 “홈페이지 WORKS에 올린 원고문헌을 시리즈 zip으로 묶어 ATLAS에서 한 번에 가져오고, 자동으로 칼럼과 그룹 구조로 정리한다”는 현재 구상과 맞는다.

현재 구현에서 이미지 처리도 가능하다. 원고 안에 이미지 링크가 하드코딩되어 있지 않더라도, zip 안에서 같은 폴더에 있는 이미지를 해당 원고의 첨부 이미지로 추가한다.

---

## 10. OL-DESK 의미중심 전환기획과 ATLAS의 기여

전환기획 문서는 OL-DESK를 단순 번역 도구가 아니라 “의미중심 창작 책상”으로 재정의한다. 핵심은 원천자료를 모으고, 목차/사건/주제를 비교하고, 의미 단위를 추출하며, 인간 최고편집장이 최종 해석과 표현을 결정하는 구조다.

### 10.1 ATLAS가 이미 기여할 수 있는 부분

ATLAS는 다음 측면에서 전환기획에 바로 기여할 수 있다.

첫째, 보드 기반 작업 흐름이다. 칸반보드는 원천자료 수집, 분류, 검토, 완료 흐름을 시각화할 수 있다. 이는 `Source Board Mode`의 초기 UI와 잘 맞는다.

둘째, 카드 중심 구조다. 전환기획의 의미 단위 카드는 다음 정보를 담는다.

```text
원문
직역
핵심 뜻
대안 해석
표현 후보
최종 표현
근거 강도
불확실성
관련 용어/각주/태그
```

ATLAS의 카드는 아직 이 필드를 구조화하지는 않지만, 마크다운 본문과 태그를 이용해 임시로 이 내용을 담을 수 있다.

셋째, 문서뷰와 독서뷰다. 전환기획의 `Desk Mode`는 “원고 하나만 올라가 있는 빈 책상”을 지향한다. ATLAS의 문서뷰는 쓰기/편집 중심이고, 독서뷰는 읽기 중심이다. 이 둘은 Desk Mode의 쓰기와 검토 경험을 이미 나누어 구현한 셈이다.

넷째, 태그와 prefix 태그다. source, theme, event, grounding, rendering, reader 같은 분류를 prefix 태그로 빠르게 적용할 수 있다. 초기 실험 단계에서는 별도 DB 없이도 의미중심 분류 체계를 시험할 수 있다.

다섯째, WORKS zip import다. 홈페이지 WORKS 원고를 시리즈 단위로 모아 ATLAS에 가져오는 흐름은 OL-DESK의 source collection ingestion에 가까운 초기 기능이다.

### 10.2 ATLAS가 아직 부족한 부분

ATLAS는 현재 카드형 저작 도구이지, 의미중심 지식 구조를 갖춘 OL-DESK 전체 시스템은 아니다.

부족한 부분:

- 원천자료 간 alignment 모델 없음
- source packet, chapter dossier, meaning_unit의 명시적 타입 없음
- 해석 후보와 인간 판단 기록을 분리하는 구조 없음
- grounding level과 creative distance를 별도 필드로 관리하지 않음
- source_basis와 rendering 결과를 관계형으로 연결하지 않음
- OL-Runner 작업 로그를 구조화해 수신하는 인터페이스 없음
- 대규모 자료 검색, 비교, 그래프 탐색 구조 없음
- 협업/권한/동기화/검토 승인 흐름 없음

즉 ATLAS는 OL-DESK 전환기획의 UI 감각과 로컬 작업실 모델에는 강하지만, 전환기획의 전체 데이터 계층을 수용하려면 스키마 확장이 필요하다.

---

## 11. Astro와 ATLAS의 중립적 적합성 검토

전환기획에서 상정한 OL-DESK 대시보드는 현재 Astro 기반 정적 웹사이트 빌더로 초기 구현되었다. Astro와 ATLAS는 목적이 다르므로 어느 하나가 절대적으로 우월하다고 보기 어렵다.

### 11.1 Astro가 적합한 경우

Astro는 다음 목적에 적합하다.

- 공개 웹사이트
- 문서/콘텐츠 포털
- 정적 대시보드
- SEO가 필요한 페이지
- Git 기반 콘텐츠 배포
- 빠른 로딩의 읽기 중심 페이지
- OL-DESK 결과물을 보여주는 read-only UI
- OL-TOON, OL-STUDIO, OL-HOME과 연결되는 공개 산출물 페이지

Astro의 강점은 “출판”과 “정적 배포”다. OL-DESK가 만든 결과를 외부에 보여주거나, 프로젝트 현황/문서/산출물을 정리하는 웹 포털에는 적합하다.

### 11.2 Astro가 약한 경우

전환기획의 OL-DESK는 정적 표시만으로 끝나지 않는다. 자료를 수집하고, 비교하고, 의미 단위를 수정하고, 표현 후보를 선택하고, 인간 판단 로그를 남겨야 한다.

이런 작업에는 Astro 단독이 약하다.

- 복잡한 로컬 편집 상태
- 드래그 앤 드롭 보드
- 문단/의미 단위별 즉시 편집
- 오프라인 저작 환경
- 대량 인터랙션
- 브라우저 내부 작업실 경험
- OL-Runner와의 실시간 또는 반자동 작업 연동

Astro에서도 React/Svelte/Vue 같은 클라이언트 앱을 붙이면 가능하지만, 그 경우 Astro는 주 앱이라기보다 shell 또는 publishing layer에 가까워진다.

### 11.3 ATLAS가 적합한 경우

ATLAS는 다음 목적에 적합하다.

- 로컬 우선 저작 도구
- 카드 중심 원고 정리
- 보드 기반 분류와 진행 관리
- 마크다운 문서 편집
- 독서/검토 모드
- 단일 HTML 파일 공유
- WORKS 원고 묶음 가져오기
- 의미중심 UI/UX 프로토타입

전환기획의 `Desk Mode`, `Source Board Mode`, `Meaning Board Mode`를 빠르게 실험하려면 ATLAS 방식이 Astro보다 직접적이다. 이미 보드, 카드, 문서, 독서라는 핵심 화면이 구현되어 있기 때문이다.

### 11.4 ATLAS가 약한 경우

ATLAS도 OL-DESK 전체 구현체로 보기에는 한계가 있다.

- 현재 데이터 저장은 localStorage 중심
- 관계형/그래프형 데이터 모델 없음
- 대규모 원천자료 관리에는 취약
- runner stage 결과를 구조화해 누적하는 백엔드 없음
- 다중 사용자 협업 구조 없음
- 정적 공개 사이트나 SEO에는 Astro보다 불리
- 데이터 검증과 마이그레이션이 커질수록 단일 파일 구조가 부담이 될 수 있음

### 11.5 결론: Astro vs ATLAS가 아니라 역할 분리

중립적으로 보면 OL-DESK 전환기획에는 Astro와 ATLAS의 역할이 다르다.

```text
Astro
= 공개/정적/출판/포털/문서화/산출물 표시 계층

ATLAS
= 로컬/상호작용/저작/분류/검토/의미 보드 계층
```

따라서 OL-DESK가 단순 대시보드라면 Astro가 적합하다. 그러나 전환기획 문서가 말하는 “의미중심 창작 책상”을 실제 작업 도구로 구현하려면 ATLAS형 인터랙티브 앱 구조가 더 적합하다.

권장 방향은 하이브리드다.

- Astro: OL-DESK의 공개 문서, 산출물, 진행 대시보드, 읽기 전용 포털
- ATLAS 또는 ATLAS형 SPA: 원천자료 수집, 의미 단위 편집, 원고 작성, 검토 작업실
- OL-Runner: 구조화 데이터 생성, alignment, meaning extraction, grounding check
- 중간 데이터 계층: Contents-Asset 또는 별도 JSON/SQLite 기반 구조화 저장소

---

## 12. OL-DESK 구현을 위한 ATLAS 확장 제안

### 12.1 card.type 추가

현재 카드는 모두 같은 타입이다. OL-DESK로 확장하려면 다음 타입을 구분하는 것이 좋다.

```text
source_profile
source_toc
event
theme
excerpt
source_packet
chapter_dossier
meaning_unit
interpretation
rendering
review_decision
export_version
```

초기에는 `card.meta.type`으로 시작해도 된다.

### 12.2 card.meta 확장

태그에 넣기에는 중요한 필드는 `card.meta`로 분리하는 것이 좋다.

```text
card.meta
  type
  sourceIds
  sourceBasis
  meaningUnitId
  renderingType
  targetReader
  groundingLevel
  creativeDistance
  editorDecision
  uncertainty
```

### 12.3 관계 모델 추가

OL-DESK는 단순 목록보다 관계가 중요하다.

필요한 관계:

```text
source -> segment
segment -> meaning_unit
meaning_unit -> interpretation
interpretation -> rendering
rendering -> review_decision
chapter_dossier -> source_packet
outline_draft -> chapter_dossier
```

ATLAS에서 이를 가볍게 시작하려면 `relations` 배열을 둘 수 있다.

```text
relations
  from
  to
  type
  note
```

### 12.4 Desk/Board 모드 분리

현재 ATLAS의 화면을 OL-DESK 모드로 해석하면 다음과 같다.

```text
Kanban/Card Grid/List = Board Mode
Document View         = Desk Mode
Reader View           = Reading Review Mode
Sidebar               = Source/Meaning Navigator
```

OL-DESK로 발전시키려면 현재 뷰명을 유지하더라도 상위 작업 모드를 다음처럼 재정의할 수 있다.

```text
Source Board
Meaning Board
Desk
Reader
Export
```

### 12.5 OL-Runner 결과 수신 포맷

전환기획은 OL-Runner가 source profile, TOC, event index, theme index, meaning candidates, rendering candidates, grounding logs를 생성한다고 본다.

ATLAS가 이를 받으려면 zip/JSON import에 다음 포맷을 추가하는 것이 좋다.

```text
ol-desk-runner-v1.json
  sourceCollections
  sourceProfiles
  sourceTocs
  eventIndex
  themeIndex
  sourcePackets
  chapterDossiers
  meaningUnits
  interpretations
  renderings
  logs
```

이 포맷을 ATLAS 카드와 관계로 변환하면, ATLAS는 OL-Runner 결과를 사람이 검토하는 시각적 작업실이 될 수 있다.

---

## 13. 실무적 판단

현재 ATLAS는 OL-DESK 전환기획의 전체 구현체라기보다는, 전환기획이 요구하는 UI/UX 방향을 이미 상당 부분 구현한 로컬 작업실이다.

특히 다음 기능은 OL-DESK에 직접 참고할 가치가 높다.

- 칸반 기반 작업 흐름
- 카드 중심 원고/자료 단위
- 컬럼/그룹/태그 3단 분류
- prefix 태그 기반 임시 의미분류
- 문서뷰의 집중 편집
- 독서뷰의 UI 은닉과 긴 글 검토
- 사이드바의 문서 트리와 태그 탐색
- WORKS zip import를 통한 원고 묶음 수집
- 단일 HTML 내보내기와 로컬 우선 철학

하지만 다음 영역은 ATLAS를 그대로 쓰기보다 OL-DESK 전용 설계가 필요하다.

- 의미 단위 스키마
- 원천자료 alignment
- 근거 보존과 창작 거리 기록
- 인간 판단 로그
- runner stage 결과 수신
- 다중 원천자료 간 비교 화면
- 장기 보관 가능한 구조화 저장소
- Astro/홈페이지/Contents-Asset과의 export pipeline

---

## 14. 권장 다음 단계

1. ATLAS에서 `card.meta.type`을 실험적으로 추가한다.

2. `meaning_unit`, `source_packet`, `chapter_dossier`, `rendering` 네 타입만 먼저 정의한다.

3. 현재 WORKS zip import 뒤에 “OL-DESK 카드 타입 자동 추정” 옵션을 붙인다.

4. prefix 태그는 계속 보조 분류로 사용하되, `groundingLevel`, `renderingType`, `sourceBasis`는 명시 필드로 승격한다.

5. ATLAS에서 만든 카드/문서를 Astro 또는 Contents-Asset으로 export하는 경로를 만든다.

6. OL-DESK 초기 구현은 Astro 단독이 아니라 “Astro 공개/정적 계층 + ATLAS형 작업실 계층 + OL-Runner 구조화 생성 계층”으로 나누는 것이 바람직하다.

---

## 15. 결론

ATLAS는 현재 OL 프로젝트 안에서 “문헌 원고를 카드로 수집하고, 보드로 분류하고, 문서로 편집하고, 독서뷰로 검토하는 로컬 작업실”의 성격이 분명하다.

OL-DESK 의미중심 전환기획은 ATLAS보다 더 큰 데이터 구조와 runner 연동을 요구하지만, UI/UX 방향에서는 ATLAS가 이미 중요한 답을 갖고 있다. 특히 카드 중심 보드, 문서뷰, 독서뷰는 전환기획의 Source Board Mode, Meaning Board Mode, Desk Mode를 구현하는 데 바로 참고할 수 있다.

따라서 현 단계의 전략은 ATLAS를 OL-DESK로 무리하게 전면 대체하는 것이 아니라, ATLAS의 상호작용 모델과 로컬 저작 경험을 OL-DESK의 작업실 계층으로 흡수하고, Astro는 공개/정적/산출물 표시 계층으로 유지하는 하이브리드 구조가 가장 현실적이다.
