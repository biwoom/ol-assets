# OL ATLAS v0.0.2 설계서

**버전**: v0.0.2  
**작성일**: 2026-05-25  
**이전 버전**: v0.0.1 (읽기 모드 토글 + 태그 해제 버튼 완료)

---

## 0. v0.0.2 작업 목록

| Phase | 내용 | 규모 |
|-------|------|------|
| **Phase 0** | 읽기 모드 버그 수정 2건 | 소 |
| **Phase 1** | 편집자 시스템 + 저장 모달 | 중 |
| **Phase 2** | 카드 행위 기록 | 중 |
| **Phase 3** | 히스토리 뷰 (About 탭) | 중 |

---

## 0-1. 고정 규칙 (모든 설계서 공통)

### 권한 선언 — AI 에이전트 전용 (세션 시작 시 1회 적용)

이하 모든 권한을 사전 일괄 승인한다. 작업 중 개별 확인 요청 금지.

**✅ 전면 허용**
```
파일 시스템
  cat, head, tail, grep, find, wc, diff      (읽기)
  write, create, str_replace, cp, mv, mkdir  (쓰기/생성/이동)
  rm <단일 파일>

셸 명령
  bash/sh 스크립트, 파이프, 리다이렉트, &&, ||, ; 체인

Node / npm
  node <script.js>, node --check <file.js>
  npm run *  (build, dev, test 등)

Git
  git status, git diff, git log, git add, git commit, git tag

빌드
  node build/build.mjs, node build/inline.mjs
```

**❌ 별도 승인 필요**
```
rm -rf <디렉토리> / git push / git reset --hard / git clean -fd
npm install <새패키지> / 폴더 외부 접근 / 네트워크 요청
```

### 빌드 산출물 파일명 규칙

`npm run build` 실행 시 `dist/` 산출물 파일명은 반드시 버전 포함:
```
ol-atlas_v{package.json의 version}.html
예: ol-atlas_v0.0.2.html
```

---

## 1. Phase 0 — 읽기 모드 버그 수정

### 1.1 버그 A: TOC(목차) 숨김 해제

**현재 문제**:
```css
body.dv-read-mode .dv-toc { display: none !important; }
```
읽기 모드에서 목차가 강제 숨김 처리되어 있음. 요구사항은 목차를 표시해야 함.

**수정**: `src/styles/docview.css` 읽기 모드 블록에서 해당 규칙 제거.

```css
/* 제거할 줄 */
body.dv-read-mode .dv-toc { display: none !important; }
```

단, TOC는 1023px 이하에서는 기존 반응형 규칙에 의해 자동으로 숨겨지므로
추가 처리 불필요.

---

### 1.2 버그 B: 본문 중앙 정렬 깨짐

**현재 문제**: `.dv-layout`이 `display: flex`이므로 자식 `.dv-wrap`은
flex item이 되어 `max-width: 720px` + `margin: 0 auto`가 기대대로 동작하지 않음.
TOC가 `display: none`이 되면 `.dv-wrap`이 `flex: 1`로 전체 폭을 차지하여
720px 제한이 실질적으로 무효가 됨.

**HTML 구조**:
```html
<div class="dv-layout">          <!-- display:flex -->
  <div class="dv-wrap" id="dv-wrap"></div>
  <aside class="dv-toc" id="dv-toc"></aside>
</div>
```

**수정**: 읽기 모드에서 `.dv-layout`을 flex 해제하고
`.dv-wrap`에 직접 max-width + margin 적용.

```css
/* 수정 전 */
body.dv-read-mode .dv-layout {
  max-width: 720px;
  margin: 0 auto;
}
body.dv-read-mode .dv-layout > .dv-wrap {
  padding: 2rem 1.5rem;
  max-width: 100%;
}

/* 수정 후 */
body.dv-read-mode .dv-layout {
  display: block;          /* flex 해제 */
  max-width: none;         /* 컨테이너 제한 해제 */
  margin: 0;
}
body.dv-read-mode .dv-layout > .dv-wrap {
  max-width: 720px;        /* 본문에 직접 제한 */
  margin: 0 auto;          /* 본문 중앙 정렬 */
  padding: 2rem 1.5rem;
}
/* TOC는 본문 오른쪽에 sticky로 표시 */
body.dv-read-mode .dv-toc {
  position: fixed;
  right: 1.5rem;
  top: calc(var(--header-h, 56px) + 4rem);
  width: 13rem;
  max-height: calc(100vh - var(--header-h, 56px) - 6rem);
}
```

읽기 모드에서 TOC는 fixed로 우측에 띄워 본문 중앙 정렬과 공존.
1023px 이하에서는 기존 반응형 규칙으로 TOC 자동 숨김.

**검증**:
- 읽기 모드에서 본문이 화면 중앙에 위치하는지
- TOC가 우측에 fixed로 표시되는지
- 1023px 이하에서 TOC 자동 숨김 여부

---

## 2. Phase 1 — 편집자 시스템

### 2.1 데이터 스키마 설계 (schemaVersion 7 → 8)

#### 2.1.1 새 필드: `meta.editors`

파일 최상위 `meta` 객체에 `editors` 배열 추가.

```js
meta: {
  // 기존 필드 유지
  fileId, title, created, version, schemaVersion, dirty, lastSavedAt,
  
  // 신규
  editors: [
    {
      id: "fp_a3f9b2c1",          // 디바이스 핑거프린트 해시 (8자)
      name: "비움",                // 사용자 입력
      email: "bingeoul@gmail.com", // 사용자 입력
      firstSavedAt: "2026-05-25T10:00:00.000Z",  // 첫 저장 시각
      lastSavedAt:  "2026-05-25T14:30:00.000Z",  // 최근 저장 시각
      saveCount: 3,                // 누적 저장 횟수
    }
  ],
  currentEditorId: "fp_a3f9b2c1", // 현재 세션 편집자 ID (localStorage와 동기)
}
```

#### 2.1.2 새 필드: `meta.saveLog`

파일 저장 단위 이력. 저장할 때마다 한 줄씩 추가.

```js
meta: {
  // ...
  saveLog: [
    {
      at: "2026-05-25T10:00:00.000Z",  // 저장 시각
      editorId: "fp_a3f9b2c1",          // 편집자 ID
      note: "초기 저장",                 // 저장 메모 (선택, 빈 문자열 허용)
    }
    // 최신이 마지막 (push)
  ]
}
```

saveLog는 최대 200개까지 유지. 초과 시 오래된 항목부터 삭제.

#### 2.1.3 새 필드: `card.acts`

카드 단위 행위 기록. 생성/수정/삭제만 기록.

```js
// 각 card 객체에 추가
{
  id: 1,
  title: "연기법",
  body: "...",
  // 기존 필드들...
  
  // 신규
  acts: [
    {
      type: "create",                    // "create" | "update" | "delete"
      at: "2026-05-25T10:00:00.000Z",
      editorId: "fp_a3f9b2c1",
    }
    // 최신이 마지막 (push)
  ]
}
```

`type: "delete"`는 카드가 휴지통으로 이동될 때 기록.
acts는 카드당 최대 50개. 초과 시 오래된 항목부터 삭제.

---

### 2.2 디바이스 핑거프린트 생성

민감 정보 없이 브라우저 환경 조합으로 8자리 해시 생성.

```js
// src/core/fingerprint.js (신규)
function generateFingerprint() {
  const raw = [
    navigator.userAgent,
    navigator.language,
    screen.width + 'x' + screen.height,
    screen.colorDepth,
    Intl.DateTimeFormat().resolvedOptions().timeZone,
    navigator.hardwareConcurrency || 0,
  ].join('|');
  
  // 단순 해시 (CRC32 대신 가벼운 구현)
  let hash = 0;
  for (let i = 0; i < raw.length; i++) {
    hash = ((hash << 5) - hash + raw.charCodeAt(i)) | 0;
  }
  return 'fp_' + Math.abs(hash).toString(36).padStart(8, '0').slice(0, 8);
}

export { generateFingerprint };
```

**특성**:
- 같은 기기+브라우저: 동일한 값
- 다른 기기: 다른 값 (충돌 가능성 낮음)
- 개인 식별 불가 수준의 정보만 사용
- 외부 전송 없음, localStorage에만 저장

---

### 2.3 편집자 식별 흐름

```
앱 부팅 시
  └── localStorage에 ol_editor_id, ol_editor_name, ol_editor_email 있는가?
        Yes → 세션 편집자 자동 복원
        No  → 편집자 미설정 상태 (저장 시 모달 표시)

저장 버튼(export-btn) 클릭 시
  └── 세션 편집자 설정되어 있는가?
        Yes → 바로 저장 실행
        No  → 편집자 입력 모달 표시
                └── 이름 + 이메일 입력 후 확인
                      └── 핑거프린트와 함께 편집자 등록 → 저장 실행
```

---

### 2.4 편집자 입력 모달 UI

저장 버튼 클릭 시 편집자 미설정이면 표시. 기존 `confirm-modal` 패턴 활용.

```
┌─────────────────────────────────┐
│  편집자 정보 입력                │
│                                  │
│  이름  [ 비움           ]        │
│  이메일 [ bingeoul@...  ]        │
│                                  │
│  ☑ 이 기기에서 기억하기          │
│                                  │
│         [취소]  [저장하기]       │
└─────────────────────────────────┘
```

- "이 기기에서 기억하기" 체크 시 localStorage에 저장 (기본 체크됨)
- 이름만 필수, 이메일은 선택
- 이미 editors에 같은 핑거프린트가 있으면 → 기존 편집자로 처리 (이름/이메일 표시)
- 같은 이름+이메일이지만 다른 핑거프린트면 → 새 편집자로 등록 + 소프트 알림
  ("같은 이름의 편집자가 있습니다. 다른 기기에서 접근 중이면 계속하세요.")

---

### 2.5 저장 실행 시 처리 (export-btn 핸들러 수정)

```js
// 기존 export-btn 핸들러 수정
document.getElementById('export-btn').addEventListener('click', () => {
  closeDropdowns();
  
  const editor = getCurrentEditor(); // localStorage에서 복원
  if (!editor) {
    showEditorModal(onEditorConfirmed);
    return;
  }
  
  executeSave(editor);
});

function executeSave(editor) {
  // 1. saveLog에 이번 저장 기록 추가
  const saveEntry = {
    at: new Date().toISOString(),
    editorId: editor.id,
    note: '',  // 향후 메모 입력 확장 가능
  };
  
  // 2. editors 목록에서 해당 편집자 업데이트
  //    (없으면 추가, 있으면 lastSavedAt + saveCount 갱신)
  
  // 3. dispatch(META_UPDATE, { editors, saveLog, currentEditorId })
  
  // 4. localStorage storageSave
  
  // 5. buildExportHTML → Blob 다운로드
  
  toast('저장되었습니다.');
}
```

---

### 2.6 스키마 마이그레이션 (v7 → v8)

```js
// src/core/schema.js 마이그레이터 추가
8: function(state) {
  devLog('MIGRATE', 'v7 → v8');
  state.meta.schemaVersion = 8;
  
  // editors, saveLog 초기화
  if (!Array.isArray(state.meta.editors)) {
    state.meta.editors = [];
  }
  if (!Array.isArray(state.meta.saveLog)) {
    state.meta.saveLog = [];
  }
  state.meta.currentEditorId = null;
  
  // 기존 카드에 acts 초기화
  (state.cards || []).forEach(card => {
    if (!Array.isArray(card.acts)) {
      card.acts = [];
    }
  });
  
  return state;
}
```

`src/data/init.js` — `makeDefault()`의 schemaVersion을 8로 변경.
`build/inline.mjs` — `SCHEMA_VERSION` 상수를 8로 변경 + 빌드 산출물 파일명 버전 자동 반영.

---

### 2.7 빌드 산출물 파일명 버전 자동 반영

`build/inline.mjs`에서 `package.json`의 `version`을 읽어
`dist/` 폴더 산출물 파일명에 자동 반영한다.

```js
// build/inline.mjs 수정
import { readFileSync } from 'node:fs';
import { writeFileSync } from 'node:fs';

const pkg = JSON.parse(readFileSync('package.json', 'utf8'));
const version = pkg.version; // "0.0.2"

// 기존: writeFileSync('dist/ol-atlas.html', html);
// 수정:
const outFilename = `ol-atlas_v${version}.html`;
writeFileSync(`dist/${outFilename}`, html);
console.log(`빌드 완료: dist/${outFilename}`);
```

**결과**: `npm run build` 실행 시 `dist/ol-atlas_v0.0.2.html` 생성.  
`package.json` version만 올리면 다음 빌드부터 파일명이 자동 변경됨.  
런타임 저장(export-btn) 파일명은 기존 방식(`제목_v버전.html`) 그대로 유지.

---

### 2.8 새 액션 타입

```js
// src/actions/settings-actions.js 에 추가
META_UPDATE_EDITORS   // editors + saveLog + currentEditorId 갱신
```

---

### 2.9 수정 파일 목록 (Phase 1)

| 파일 | 작업 |
|------|------|
| `src/core/fingerprint.js` | 신규 — 핑거프린트 생성 함수 |
| `src/core/schema.js` | v7→v8 마이그레이터 추가, SCHEMA_VERSION=8 |
| `src/data/init.js` | makeDefault schemaVersion=8, editors/saveLog/currentEditorId 초기화 |
| `src/core/normalize.js` | normalizeState에 editors/saveLog 필드 보장, normalizeCard에 acts 보장 |
| `src/actions/settings-actions.js` | META_UPDATE_EDITORS 액션 추가 |
| `src/actions/export-import.js` | export-btn 핸들러 수정 — 편집자 체크 + executeSave() |
| `src/ui/editor-modal.js` | 신규 — 편집자 입력 모달 |
| `src/ui/editor-modal.css` | 신규 — 모달 스타일 |
| `build/inline.mjs` | SCHEMA_VERSION=8 |
| `package.json` | version=0.0.2 |

---

## 3. Phase 2 — 카드 행위 기록

### 3.1 기록 대상 액션

| 액션 타입 | 기록 type | 대상 |
|-----------|-----------|------|
| `CARD_CREATE` | `"create"` | 생성된 카드 |
| `CARD_UPDATE` | `"update"` | 수정된 카드 |
| `CARD_DELETE` | `"delete"` | 삭제된 카드 (휴지통 이동) |
| `CARD_BULK_DELETE` | `"delete"` | 일괄 삭제된 모든 카드 |

`CARD_MOVE`, `CARD_RESTORE`, `CARD_PURGE` 등은 기록하지 않음.

### 3.2 구현 위치

카드 행위 기록은 **dispatch 레이어에서 side effect로 처리**.
reducer를 수정하지 않고, dispatch 함수 실행 후 `currentEditorId`가 있을 때만 기록.

```js
// src/core/action.js — dispatch() 함수 수정
function dispatch(action) {
  // 기존 로직 ...
  
  // 카드 행위 기록 side effect
  if (currentEditorId) {
    recordCardAct(action, currentEditorId);
  }
}

function recordCardAct(action, editorId) {
  const at = new Date().toISOString();
  const state = getState();
  
  const targets = {
    'CARD_CREATE':      [action.payload.card?.id ?? state.nextCardId - 1],
    'CARD_UPDATE':      [action.payload.id],
    'CARD_DELETE':      [action.payload.id],
    'CARD_BULK_DELETE': action.payload.ids,
  }[action.type];
  
  if (!targets) return;
  
  // applyState로 acts 업데이트
  const newCards = state.cards.map(card => {
    if (!targets.includes(card.id)) return card;
    const acts = [...(card.acts || []), { type: actType, at, editorId }];
    // 최대 50개 유지
    return { ...card, acts: acts.length > 50 ? acts.slice(-50) : acts };
  });
  
  applyState({ ...state, cards: newCards });
}
```

**주의**: CARD_CREATE는 reducer 실행 후 카드 ID가 확정되므로
reducer 실행 후 state에서 마지막 카드를 찾아 기록.

---

### 3.3 편집자 미설정 시 기록 건너뜀

`currentEditorId`가 null이면 카드 행위 기록 자체를 건너뜀.
부팅 직후, 또는 편집자 모달을 취소한 상태에서는 기록 없음.

---

### 3.4 수정 파일 목록 (Phase 2)

| 파일 | 작업 |
|------|------|
| `src/core/action.js` | dispatch() 에 카드 행위 기록 side effect 추가 |

---

## 4. Phase 3 — 히스토리 뷰

### 4.1 위치: About 페이지 탭 추가

About 페이지에 탭 구조 추가.

```
[ 파일 정보 ]  [ 편집 기록 ]
```

"파일 정보" 탭: 기존 About 페이지 내용 그대로.
"편집 기록" 탭: 편집자별 탭 + 히스토리.

---

### 4.2 편집 기록 탭 UI 구조

```
[ 편집 기록 ]

편집자 탭: [ 비움 (3) ]  [ 편집자A (1) ]

─────────────────────────────────────────
비움  ·  bingeoul@gmail.com
첫 편집: 2026-05-25  ·  총 3회 저장
─────────────────────────────────────────

▼ 저장 기록
  2026-05-25 14:30  저장  ──────────────
  2026-05-25 12:00  저장  ──────────────
  2026-05-25 10:00  저장  ──────────────

▼ 카드 기록
  [생성] 연기법          2026-05-25 14:30
  [수정] 사성제          2026-05-25 12:00
  [생성] 팔정도          2026-05-25 10:00
  [삭제] 임시 카드       2026-05-25 10:00
```

---

### 4.3 편집자 탭 렌더 로직

```js
// 편집자 탭 클릭 시
function renderEditorHistory(editorId) {
  const editor = state.meta.editors.find(e => e.id === editorId);
  
  // 저장 기록: saveLog에서 해당 editorId 필터
  const saveLogs = state.meta.saveLog
    .filter(s => s.editorId === editorId)
    .reverse(); // 최신 먼저
  
  // 카드 기록: 모든 카드의 acts에서 해당 editorId 필터
  const cardActs = [];
  state.cards.forEach(card => {
    (card.acts || []).forEach(act => {
      if (act.editorId === editorId) {
        cardActs.push({ ...act, cardId: card.id, cardTitle: card.title });
      }
    });
  });
  // 시간 역순 정렬
  cardActs.sort((a, b) => b.at.localeCompare(a.at));
  
  // 렌더...
}
```

---

### 4.4 뱃지 스타일

```css
.hist-act-badge {
  display: inline-block;
  padding: 0.1rem 0.4rem;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 600;
}
.hist-act-badge.create { background: hsl(142 71% 92%); color: hsl(142 71% 28%); }
.hist-act-badge.update { background: hsl(217 91% 92%); color: hsl(217 91% 35%); }
.hist-act-badge.delete { background: hsl(0 84% 92%);   color: hsl(0 84% 35%);   }
.dark .hist-act-badge.create { background: hsl(142 40% 20%); color: hsl(142 60% 80%); }
.dark .hist-act-badge.update { background: hsl(217 60% 20%); color: hsl(217 91% 80%); }
.dark .hist-act-badge.delete { background: hsl(0 50% 20%);   color: hsl(0 80% 80%);   }
```

---

### 4.5 수정 파일 목록 (Phase 3)

| 파일 | 작업 |
|------|------|
| `src/components/shared/about.js` | About 탭 구조 추가, 편집 기록 탭 렌더 |
| `src/styles/components.css` (또는 about.css 신규) | 히스토리 뷰 스타일 |

---

## 5. 전체 수정 파일 요약

| 파일 | Phase | 작업 |
|------|-------|------|
| `src/styles/docview.css` | 0 | TOC 숨김 규칙 제거 + 중앙정렬 CSS 수정 |
| `src/core/fingerprint.js` | 1 | 신규 |
| `src/core/schema.js` | 1 | v8 마이그레이터 추가 |
| `src/core/normalize.js` | 1 | editors/saveLog/acts 필드 보장 |
| `src/data/init.js` | 1 | schemaVersion=8, 초기값 추가 |
| `src/actions/settings-actions.js` | 1 | META_UPDATE_EDITORS 액션 |
| `src/actions/export-import.js` | 1 | export-btn 핸들러 수정 |
| `src/ui/editor-modal.js` | 1 | 신규 — 편집자 입력 모달 |
| `src/ui/editor-modal.css` | 1 | 신규 |
| `build/inline.mjs` | 1 | SCHEMA_VERSION=8, 빌드 산출물 파일명 `ol-atlas_v{version}.html` 자동 반영 |
| `package.json` | 1 | version=0.0.2 |
| `src/core/action.js` | 2 | dispatch에 카드 행위 기록 side effect |
| `src/components/shared/about.js` | 3 | 편집 기록 탭 추가 |
| `src/styles/components.css` | 3 | 히스토리 뷰 스타일 |

신규 파일: `fingerprint.js`, `editor-modal.js`, `editor-modal.css` (3개)  
수정 파일: 11개

---

## 6. 작업 순서

```
Phase 0 (버그 수정) → 빌드 검증 → git commit
Phase 1 (편집자 시스템) → 저장 모달 동작 확인 → git commit
Phase 2 (카드 행위 기록) → 카드 생성/수정/삭제 후 acts 확인 → git commit
Phase 3 (히스토리 뷰) → About 탭 전체 확인 → git commit
git tag v0.0.2
```

---

## 7. 주의사항

### 7.1 normalizeCard의 기존 history 삭제 코드

현재 `normalizeCard`에 `"history" in e && delete e.history` 코드가 있음.
이것은 과거 버전 호환을 위한 코드이고 `acts`는 다른 필드명이므로 충돌 없음.
삭제하지 말고 그대로 유지.

### 7.2 CARD_CREATE 시 ID 확정 타이밍

`CARD_CREATE` reducer 실행 후 `nextCardId - 1`이 새 카드의 ID.
`recordCardAct()`는 reducer 실행 후 `getState()`를 호출하므로
이미 카드가 추가된 state에서 마지막 카드를 안전하게 찾을 수 있음.

### 7.3 saveLog 최대 200개, acts 최대 50개

초과 시 `slice(-200)` / `slice(-50)`으로 오래된 항목 제거.
파일 크기 증가 억제 목적.

### 7.4 편집자 미설정 상태

편집자 모달을 취소하면 저장 자체가 실행되지 않음.
"편집자 없이 저장"은 지원하지 않음. 최소한 이름 입력 필수.

---

*OL ATLAS v0.0.2 설계서 — 2026-05-25*