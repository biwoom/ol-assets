# OL ATLAS 편집자 전환 브라우저 콘솔 테스트 가이드

**대상 버전**: v0.0.2  
**목적**: 편집자 등록, 전환, 히스토리 확인을 콘솔에서 직접 테스트

---

## 기본 원리

OL은 모든 함수가 IIFE 스코프 안에 있어 콘솔에서 직접 호출 불가능.  
접근 방법은 두 가지다:

1. **localStorage 직접 조작** → 편집자 세션 전환 (가장 빠름)
2. **`ol_state` JSON 조작** → state 전체 교체 (편집자 목록, acts 등 자유 조작)

---

## STEP 1: 현재 상태 확인

```js
// 현재 state 전체 확인
JSON.parse(localStorage.getItem('ol_state'))

// 편집자 목록만
JSON.parse(localStorage.getItem('ol_state')).meta.editors

// saveLog만
JSON.parse(localStorage.getItem('ol_state')).meta.saveLog

// 첫 번째 카드의 acts
JSON.parse(localStorage.getItem('ol_state')).cards[0]?.acts

// 현재 세션 편집자 (localStorage)
{
  id:    localStorage.getItem('ol_editor_id'),
  name:  localStorage.getItem('ol_editor_name'),
  email: localStorage.getItem('ol_editor_email'),
}
```

---

## STEP 2: 편집자 A로 세션 설정

```js
// ── 편집자 A 세션 설정 ──────────────────────────────
localStorage.setItem('ol_editor_id',    'fp_test0001');
localStorage.setItem('ol_editor_name',  '편집자A');
localStorage.setItem('ol_editor_email', 'a@test.com');

// 확인
console.log('현재 세션:', localStorage.getItem('ol_editor_name'));

// 페이지 새로고침 (세션 복원 확인)
location.reload();
```

새로고침 후 카드를 수정하면 `fp_test0001` ID로 acts가 기록된다.

---

## STEP 3: 편집자 B로 세션 전환

```js
// ── 편집자B로 완전 전환 ──────────────────────────────

// 1. localStorage 세션 키 변경
localStorage.setItem('ol_editor_id',    'fp_test0004');
localStorage.setItem('ol_editor_name',  '편집자4');
localStorage.setItem('ol_editor_email', 'b@test4.com');

// 2. ol_state의 currentEditorId도 함께 변경 ← 이게 핵심
const s = JSON.parse(localStorage.getItem('ol_state'));
s.meta.currentEditorId = 'fp_test0004';

// 3. 편집자B가 editors 목록에 없으면 추가
const exists = s.meta.editors.find(e => e.id === 'fp_test0004');
if (!exists) {
  s.meta.editors.push({
    id: 'fp_test0004',
    name: '편집자4',
    email: 'b@test4.com',
    firstSavedAt: new Date().toISOString(),
    lastSavedAt: new Date().toISOString(),
    saveCount: 0
  });
}

localStorage.setItem('ol_state', JSON.stringify(s));
location.reload();
```

이후 카드 수정 시 `fp_test0002` ID로 기록된다.

---

## STEP 4: 테스트용 편집자 데이터 일괄 주입

여러 편집자의 기록을 한번에 만들고 싶을 때 state를 직접 조작한다.

```js
// ── 현재 state에 테스트 편집자 + acts 주입 ────────────
const state = JSON.parse(localStorage.getItem('ol_state'));

// 테스트 편집자 2명 추가
const now = new Date().toISOString();
const editors = [
  {
    id: 'fp_test0001',
    name: '편집자A',
    email: 'a@test.com',
    firstSavedAt: now,
    lastSavedAt: now,
    saveCount: 2,
  },
  {
    id: 'fp_test0002',
    name: '편집자B',
    email: 'b@test.com',
    firstSavedAt: now,
    lastSavedAt: now,
    saveCount: 1,
  }
];

// saveLog에 테스트 기록 추가
const saveLog = [
  { at: '2026-05-25T10:00:00.000Z', editorId: 'fp_test0001' },
  { at: '2026-05-25T12:00:00.000Z', editorId: 'fp_test0001' },
  { at: '2026-05-25T14:00:00.000Z', editorId: 'fp_test0002' },
];

// 첫 번째 카드에 두 편집자의 acts 추가
const cards = state.cards.map((card, i) => {
  if (i !== 0) return card;
  return {
    ...card,
    acts: [
      { type: 'create', at: '2026-05-25T10:00:00.000Z', editorId: 'fp_test0001' },
      { type: 'update', at: '2026-05-25T12:00:00.000Z', editorId: 'fp_test0001' },
      { type: 'update', at: '2026-05-25T14:00:00.000Z', editorId: 'fp_test0002' },
    ]
  };
});

// state 교체
const newState = {
  ...state,
  meta: {
    ...state.meta,
    editors: [...(state.meta.editors || []), ...editors],
    saveLog,
    currentEditorId: 'fp_test0001',
  },
  cards,
};

localStorage.setItem('ol_state', JSON.stringify(newState));
location.reload();
```

새로고침 후 About → 편집 기록 탭에서 편집자A, 편집자B 탭이 모두 표시되어야 한다.

---

## STEP 5: 영구삭제 acts 소실 테스트

```js
// ── 영구삭제 전후 acts 비교 ───────────────────────────

// 1. 현재 trash 확인
const s = JSON.parse(localStorage.getItem('ol_state'));
console.log('trash:', s.trash);
console.log('actLog:', s.meta.actLog);  // v0.0.3 이후

// 2. UI에서 카드를 휴지통으로 이동 후
const s2 = JSON.parse(localStorage.getItem('ol_state'));
console.log('trash 이동 후:', s2.trash.map(c => ({id: c.id, title: c.title, acts: c.acts})));

// 3. UI에서 영구삭제 후
const s3 = JSON.parse(localStorage.getItem('ol_state'));
console.log('영구삭제 후 trash:', s3.trash);
console.log('actLog (v0.0.3 이후 보존되어야 함):', s3.meta.actLog);
```

---

## STEP 6: 세션 초기화 (원상복구)

```js
// ── 테스트 데이터 전체 초기화 ────────────────────────

// 편집자 세션만 초기화
localStorage.removeItem('ol_editor_id');
localStorage.removeItem('ol_editor_name');
localStorage.removeItem('ol_editor_email');

// state 전체 초기화 (앱 처음 상태로)
localStorage.removeItem('ol_state');

location.reload();
```

---

## STEP 7: 개발 로그 활성화

콘솔에서 ACTION, BOOT, MIGRATE 등 내부 로그를 보려면:

```js
// 개발 로그 켜기
localStorage.setItem('ol_dev', '1');
location.reload();

// 개발 로그 끄기
localStorage.removeItem('ol_dev');
location.reload();
```

활성화 후 카드 수정 시 콘솔에:

```
[ACTION] CARD_UPDATE {id: 1}
[ACTION] META_UPDATE_EDITORS {editors: [...], ...}
[STORAGE] save: 12.3 KB in 0.8ms
```

형태로 출력된다.

---

## 편집자 전환 전체 시나리오 (빠른 버전)

```js
// ① 상태 확인
const s = JSON.parse(localStorage.getItem('ol_state'));
console.table(s.meta.editors);

// ② 편집자 A로 전환
localStorage.setItem('ol_editor_id', 'fp_test0001');
localStorage.setItem('ol_editor_name', '편집자A');
location.reload();
// → 카드 수정 → About 편집기록 확인

// ③ 편집자 B로 전환
localStorage.setItem('ol_editor_id', 'fp_test0002');
localStorage.setItem('ol_editor_name', '편집자B');
location.reload();
// → 다른 카드 수정 → About 편집기록 확인

// ④ 두 편집자의 기록이 각각의 탭에 분리되어 있는지 확인
const s2 = JSON.parse(localStorage.getItem('ol_state'));
s2.cards.forEach(c => {
  if (c.acts?.length) console.log(c.title, c.acts);
});
```

---

## 빠른 참조 — localStorage 키 목록

|키|내용|
|---|---|
|`ol_state`|앱 전체 state JSON|
|`ol_editor_id`|현재 세션 편집자 ID|
|`ol_editor_name`|현재 세션 편집자 이름|
|`ol_editor_email`|현재 세션 편집자 이메일|
|`ol_dev`|개발 로그 (`"1"` = 활성)|
|`ol_theme`|테마 (`light`/`dark`/`system`)|
|`ol_last_view`|마지막 뷰|

---

_OL ATLAS 콘솔 테스트 가이드 — 2026-05-25_