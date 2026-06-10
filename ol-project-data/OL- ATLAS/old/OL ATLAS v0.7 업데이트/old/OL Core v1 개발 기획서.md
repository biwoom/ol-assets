# OL Core v1 개발 기획서

## 불교 지식 탐색형 경험 플랫폼 아키텍처 재구성 제안서

버전: Draft v1.0
작성 목적: OL 프로젝트 핵심 방향성 검토 및 전문가 협업 토론용
기반 문서: v0.5~v0.6 개발 논의 및 구조 개선 제안 종합 

---

# 1. 프로젝트 개요

## 1.1 프로젝트명

**OL (OL ATLAS / OL Core)**

---

## 1.2 프로젝트 비전

OL은 단순한 메모앱·위키·노트앱이 아니다.

OL의 핵심 목표는:

> “불교 지식을 탐색 가능한 살아있는 구조로 조직하고 경험하게 하는 것”

이다.

즉 단순한 정보 저장이 아니라:

* 탐독
* 연결
* 사유
* 관조
* 수행적 탐색

을 가능하게 하는 **지식 경험 환경(Knowledge Experience Environment)** 을 지향한다. 

---

# 2. 핵심 철학(Core Philosophy)

## 2.1 Local First

사용자의 데이터는 서버보다 사용자 로컬 환경을 우선한다.

* 브라우저 기반 동작
* 오프라인 사용 가능
* 사용자가 데이터 완전 소유
* 장기 보존 가능성 확보

---

## 2.2 Single-file Distribution

배포는 가능한 한 self-contained single HTML 구조를 유지한다.

이는 다음 가치를 가진다:

* portability
* archiveability
* lineage preservation
* 개인 보존성
* 장기 접근 가능성

이는 TiddlyWiki 의 장점을 계승하면서도, OL만의 탐색형 구조로 발전시키는 전략이다. 

---

## 2.3 Modular Development / Unified Deployment

개발 단계:

```text
/src
/core
/ui
/storage
/search
/plugins
/views
/styles
```

배포 단계:

```text
Single self-contained HTML
```

즉:

> “개발은 모듈화, 배포는 단일화”

를 원칙으로 한다.

---

## ~~2.4 Knowledge as Living Nodes~~

OL의 데이터는 단순 카드가 아니라 “지식 노드(node)”로 취급한다.

예:

* 인물
* 장소
* 경전
* 개념
* 수행법
* 사건
* 교단
* 시대

등은 서로 연결 가능한 탐색 단위이다. 

---

## 2.5 Buddhist Ontology-aware Structure

OL은 범용 위키가 아니라:

> “불교 지식 구조를 이해하는 탐색 시스템”

을 지향한다.

예시 ontology:

```text
인물:
장소:
경전:
개념:
수행:
교단:
시대:
의례:
```

현재 prefix tag 시스템은 이 ontology의 초기 형태로 볼 수 있다. 

---

# 3. 현재 v0.x 구조 평가

## 3.1 현재 구조의 장점

현재 v0.6 방향성은 상당히 우수한 기반을 형성하고 있다.

### 이미 확보한 핵심 자산

* 개발/배포 분리
* build.js 기반 구조
* sidebar 탐색 UX
* prefix ontology
* 모바일 최적화 경험
* single-file 배포 전략
* local-first 철학
* lineage 개념



---

## 3.2 현재 구조의 한계

현재 구조는 아직 prototype 단계의 특성이 남아 있다.

### 주요 문제

```text
global state
+
direct DOM mutation
+
render side-effect
+
UI-event coupling
```

이 구조는 프로젝트 규모 확대 시:

* race condition
* 유지보수 난이도 증가
* 렌더 충돌
* 모바일 이벤트 버그
* plugin chaos

를 유발할 가능성이 높다. 

---

# 4. 재개발 전략 방향

## 4.1 “완전 재개발”은 지양

전체 폐기 후 신규 개발은 권장하지 않는다.

그 이유:

* 기존 UX 자산 손실
* 데이터 구조 실험 결과 손실
* 실제 사용 흐름 검증 손실
* endless redesign 위험



---

## 4.2 권장 전략

# “OL Core v1 재아키텍처 + 점진적 이전”

```text
OL v0.x
  → 실제 사용 및 검증

OL Core v1
  → 새 구조 구축

기능 단위 점진 이전
```



---

# 5. OL Core v1 핵심 아키텍처

# 5.1 상태 관리(State Architecture)

## 목표

직접 render 호출 구조를 제거하고:

```text
UI
 → Action
   → State Mutation
     → Render Queue
       → Renderer
```

구조로 전환한다.



---

## 권장 구조

```js
dispatch('CARD_UPDATED', payload)
dispatch('NODE_LINKED', payload)
dispatch('VIEW_CHANGED', payload)
```

---

## 핵심 원칙

* UI는 state 직접 수정 금지
* render 함수는 state 수정 금지
* mutation은 action layer에서만 수행

---

# 5.2 Render Scheduler

현재 구조는 동일 이벤트에서 다중 render 가능성이 존재한다.

예:

```js
renderCards()
renderSidebar()
renderList()
```

연속 호출.

이는 모바일 성능 저하와 race condition을 유발한다. 

---

## 권장 구조

```js
queueRender('cards')
queueRender('sidebar')

requestAnimationFrame(flushQueue)
```

---

# 5.3 Event Bus

컴포넌트 직접 참조를 줄이기 위해 event bus 도입.

```js
OL.emit('card:updated', card)
OL.on('card:updated', handler)
```



---

# 5.4 Sidebar Architecture

현재 sidebar는:

* filtering
* dropdown
* overlay
* mobile interaction
* portal rendering

등이 복합적으로 결합되어 있다.

따라서 다음 구조로 분리 필요:

```text
SidebarController
SidebarState
SidebarRenderer
```



---

# 5.5 Storage Layer

## 단기 목표

localStorage 직접 접근 제거.

```js
storage.save()
storage.load()
```

추상화 계층 도입.

---

## 중기 목표

IndexedDB 기반 저장 계층 도입.

---

## 장기 목표

Snapshot / lineage 기반 저장 구조.

```text
Workspace Snapshot
Revision
Lineage Export
```

---

# 5.6 Dirty State / Auto Save

현재 가장 시급한 과제 중 하나.



---

## 핵심 기능

### Dirty flag

```js
S.meta.dirty = true
```

---

### beforeunload 보호

```js
window.addEventListener('beforeunload', ...)
```

---

### Auto Save Queue

```text
수정 후 debounce 자동 저장
```

이는 장기 UX 안정성 핵심 요소이다.

---

# 6. Plugin Architecture

# 6.1 Plugin-first 전략

OL은 장기적으로:

```text
Core + Plugin Ecosystem
```

구조를 지향한다.



---

# 6.2 핵심 원칙

## 플러그인의 DOM 직접 접근 금지

금지 예시:

```js
document.querySelector(...)
```

---

## 공식 Plugin API 제공

```js
OL.registerPlugin({
  id,
  routes,
  panels,
  commands,
  hooks
})
```

---

# 6.3 Hook System

예시:

```js
hooks: {
  onNodeOpen(node) {},
  onNodeSave(node) {},
  onSidebarRender(ctx) {},
  onSearch(query) {},
}
```

---

# 6.4 예상 Plugin 방향

## 불교 전문 패키지 예시

* 붓다스토리 패키지
* 초기불교 경전 패키지
* 정토 패키지
* 중관학 패키지
* 인물 관계 탐색 패키지
* 연표 패키지
* 법맥 지도 패키지

---

# ~~7. Search & Semantic Layer~~

OL의 핵심 차별점 중 하나.

---

# ~~7.1 단순 검색을 넘는 구조~~

예:

```text
붓다
 → 제자
 → 사건
 → 설법
 → 개념
 → 관련 경전
```

즉 semantic navigation 지원.



---

# 7.2 권장 구조

```text
/search
  basic-search.js
  tag-index.js
  fulltext-index.js
  semantic-index.js
```

---

# 8. View System 확장

현재:

* card
* list
* doc

중심 구조.

장기적으로:

```text
timeline
graph
character-map
sutra-flow
meditation-view
lineage-view
```

등으로 확장 가능.

---

# 9. 디자인 시스템 방향

# 9.1 핵심 미학

OL의 UX 방향은:

> “조용한 탐색성”

이다. 

---

## 지향점

* 낮은 시각 피로
* 높은 정보 밀도
* 읽기 흐름 중심
* 과도한 애니메이션 최소화
* 수행적 분위기 유지

---

# 9.2 스타일 시스템

## Design Token 도입 권장

```css
--space-xs
--space-sm
--radius-md
--font-ui
--color-accent
```

---

# 9.3 아이콘 시스템

통일 필요.

권장:

* [Lucide Icons](https://lucide.dev?utm_source=chatgpt.com) 스타일

중 하나 선택 후 일관 적용.

---

# 10. 권장 기술 방향

## 10.1 React/Vue 대규모 도입은 보류

현재 프로젝트 규모와 철학상:

```text
Web Components
+
lightweight runtime
```

구조가 더 적합할 가능성이 높다.



---

# 10.2 권장 디렉토리 구조

```text
/core
/ui
/views
/plugins
/search
/storage
/schema
/runtime
/styles
/assets
```

---

# 11. 단계별 개발 로드맵

# Phase A — 안정화

우선순위 최고.

1. Dirty State
2. Auto Save
3. Render Scheduler
4. Sidebar Lifecycle 정리
5. Event Bus

---

# Phase B — 구조화

1. Action Layer
2. Storage Abstraction
3. Schema Migration
4. Settings System
5. Design Token 도입

---

# Phase C — 플랫폼화

1. Plugin API
2. Hook System
3. Semantic Search Layer
4. Extension Manifest
5. View Expansion

---

# Phase D — 지식 경험 고도화

1. Buddhist Ontology 강화
2. Semantic Navigation
3. Knowledge Graph
4. 경전 관계 구조
5. 인물·사건 연결망
6. 수행 탐색 흐름

---

# 12. 최종 결론

OL 프로젝트의 핵심 가치는 단순한 기술 구현이 아니다.

진정한 핵심은:

> “불교 지식을 탐색 가능한 살아있는 구조로 경험하게 하는 것”

이다. 

따라서 앞으로 가장 중요한 것은:

* 기능 추가 속도
* 화려한 UI
* 프레임워크 유행

보다,

# “지식 경험 구조의 일관성과 지속성”

을 유지하는 것이다.

OL은 단순 노트앱보다:

```text
지식 수행 환경
+
탐색형 불교 ontology 플랫폼
+
장기 보존 가능한 개인 지식 우주
```

에 가까운 방향성을 가진다.

이 점을 유지하면서 아키텍처를 안정화한다면,
OL은 매우 독자적인 지식 플랫폼으로 성장할 가능성이 있다.
