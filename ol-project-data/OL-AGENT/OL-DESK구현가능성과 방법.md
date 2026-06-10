# OL-DESK구현가능성과 방법

# 질문 - 실제 구현 방법은?

이제 'OL DESK 개발기획안 v0.1 수정본'을 중심에 놓고 실제적으로 이것이 구현 가능한지 astro 빌더가 적합한 대안인지? 구체적으로 어떻게 구현할지 등에 대한 당신의 의견 제안해줘. 우선 요약하여 핵심만 설명해줘.

### 응답
### 결론부터 말하면: 구현 가능하고, Astro는 적합합니다.

다만 조건이 있습니다.

**OL DESK를 “정적 홈페이지”로 만들면 부적합**하고, **Astro + Node 로컬 서버 기반 편집 앱**으로 만들면 적합합니다.

Astro는 원래 콘텐츠 중심 웹 프레임워크이고, 파일 시스템·외부 API·CMS 등 다양한 위치의 데이터를 불러오는 구조에 강점이 있습니다. ([Astro][1]) 또 Node 어댑터를 사용하면 서버 기능, actions, sessions 같은 on-demand 기능을 Node 환경에서 실행할 수 있습니다. ([Astro Docs][2])
따라서 OL DESK처럼 **로컬 JSON을 읽고, 수정하고, 다시 파일로 저장하는 검수 대시보드**는 Astro 단독 정적 빌드가 아니라 **Astro SSR + Node API 레이어**로 가야 합니다.

---

## 1. 내 판단

### Astro를 쓰는 것은 맞다

OL DESK는 일반적인 SaaS 관리도구가 아니라, 다음 성격을 가집니다.

```text
문헌 중심
파일 중심
로컬 중심
Git 관리 가능
OL HOME 디자인 계승
Markdown/JSON 기반
브라우저 UI 필요
```

이 조건에서는 Astro가 꽤 잘 맞습니다.

특히 OL HOME이 이미 Astro 기반이므로, OL DESK도 Astro로 가면 다음 장점이 있습니다.

```text
1. OL HOME과 디자인 철학·CSS·컴포넌트 공유 가능
2. 문헌 중심 UI에 적합
3. 정적 페이지와 동적 편집 화면을 혼합 가능
4. 로컬 개발 서버에서 가볍게 운영 가능
5. 나중에 OL BOOK / ATLAS / HOME과 연결하기 쉬움
```

---

## 2. 단, Astro만으로는 부족하다

OL DESK는 단순히 보여주는 앱이 아닙니다.

반드시 해야 하는 일이 있습니다.

```text
JSON 파일 읽기
JSON 파일 수정
새 용어·각주·태그 생성
3차 가번역 저장
draft3-instructions.json 생성
폴더 감지
Paperclip 산출물 반영
```

이것은 정적 Astro 사이트만으로는 어렵습니다.

따라서 구조는 이렇게 가야 합니다.

```text
Astro
= 화면, 라우팅, 문헌 표시, 탭 UI

Node API
= 파일 읽기/쓰기, JSON 저장, handoff 생성

로컬 파일 시스템
= ol-translation-lab 데이터 저장

Paperclip
= 에이전트 실행과 산출물 생성
```

즉, OL DESK는 **Astro 앱이지만 내부적으로는 작은 로컬 Node 서버 앱**입니다.

---

## 3. 추천 구현 방식

### 가장 현실적인 v0.1 구조

```text
ol-desk-project/
├─ ol-desk/                 Astro 앱
├─ ol-translation-lab/      번역 데이터
└─ paperclip/               에이전트 지침문서
```

`ol-desk`는 `../ol-translation-lab` 폴더를 읽고 씁니다.

예상 실행 방식은 다음입니다.

```bash
cd ol-desk
npm run dev
```

브라우저에서:

```text
http://localhost:4321
```

Paperclip은 별도 서버로:

```bash
npx paperclipai onboard --yes
```

---

## 4. 구현 핵심은 “파일 API”입니다

OL DESK의 핵심은 화려한 UI보다 이 API입니다.

```text
GET  /api/documents
GET  /api/documents/:doc_id
POST /api/reviews/:doc_id/save
POST /api/handoff/:doc_id/draft3
POST /api/final/:doc_id/save
```

각 API 역할은 다음과 같습니다.

```text
/api/documents
= documents.json 읽어서 문서 리스트 반환

/api/documents/:doc_id
= 원문, 1차, 2차, 3차 가번역, 후보 용어·각주·태그를 합쳐서 반환

/api/reviews/:doc_id/save
= 인간 감수자가 수정한 3차 가번역, 신규 용어, 신규 각주, 신규 태그 저장

/api/handoff/:doc_id/draft3
= draft3-instructions.json 생성

/api/final/:doc_id/save
= 4차 최종원고 저장
```

이 API만 안정적으로 만들면 OL DESK는 구현 가능합니다.

---

## 5. UI는 처음부터 복잡하게 만들 필요 없습니다

v0.1은 다음 화면 2개면 충분합니다.

### 1번 화면: 문서 리스트

```text
문서명
상태
1차 완료 여부
2차 완료 여부
3차 가번역 상태
3차 생산물 상태
4차 최종원고 상태
미확정 용어 수
미확정 각주 수
미확정 태그 수
```

### 2번 화면: 문서 상세

```text
왼쪽: 세그먼트 목록
중앙: 번역 탭
오른쪽: 용어·각주·태그 패널
```

중앙 탭:

```text
[1차 번역] [2차 번역] [3차 가번역] [4차 최종원고]
```

기본값:

```text
3차 가번역 탭
1단 표시
수정 가능
```

추가 비교:

```text
[원문 보기] [1차 보기] [2차 보기]
```

선택하면 2단 또는 3단 병렬로 보여줍니다.

---

## 6. 가장 중요한 데이터 설계

핵심은 `draft3_preliminary_text`입니다.

```json
{
  "segment_id": "004-001",
  "source_text": "...",
  "draft1_agent_text": "...",
  "draft2_agent_text": "...",
  "draft3_preliminary_text": "...",
  "draft3_generated_text": "",
  "draft4_final_working_text": "",
  "final_text": "",
  "draft3_preliminary_status": "editing"
}
```

여기서:

```text
draft1_agent_text
= 보기 전용

draft2_agent_text
= 보기 전용

draft3_preliminary_text
= 인간 감수자 수정 영역

draft3_generated_text
= B2 에이전트 생산물

draft4_final_working_text
= 인간 최종 탈고 영역
```

이 모델만 확정되면 구현 난이도는 크게 낮아집니다.

---

## 7. Paperclip 연동은 처음부터 자동화하지 않는 것이 좋습니다

v0.1에서는 자동 감지·자동 실행까지 욕심내지 않는 것이 좋습니다.

처음에는 이렇게 충분합니다.

```text
1. Paperclip이 ol-translation-lab에 산출물 생성
2. OL DESK에서 새로고침 또는 “데이터 다시 읽기”
3. 인간 감수자가 3차 가번역 수정
4. “3차 반영 지시 생성” 버튼 클릭
5. draft3-instructions.json 생성
6. 사용자가 Paperclip B2 에이전트에게 이 파일을 기준으로 작업 지시
```

그 다음 v0.2에서:

```text
파일 감지
자동 상태 업데이트
Paperclip Issue 생성
B2 에이전트 자동 호출
```

으로 확장하면 됩니다.

---

## 8. 구현 난이도 평가

```text
문서 리스트 표시: 쉬움
JSON 읽기: 쉬움
탭 UI: 쉬움
2~3단 병렬 보기: 보통
3차 가번역 편집 저장: 보통
신규 용어·각주·태그 생성: 보통
draft3-instructions.json 생성: 쉬움~보통
파일 감지 자동 반영: 보통
Paperclip 자동 연동: 어려움
멀티 사용자 협업: 어려움
복잡한 diff 병합: 어려움
```

따라서 v0.1은 충분히 구현 가능합니다.

위험한 부분은 Astro 자체가 아니라, **처음부터 Paperclip 자동 연동·실시간 감지·복잡한 diff·멀티 사용자 기능까지 넣으려는 것**입니다.

---

## 9. 내 제안: OL DESK v0.1은 “로컬 편집기”로 시작

처음 목표를 이렇게 제한하는 것이 좋습니다.

```text
OL DESK v0.1
= ol-translation-lab의 JSON을 읽고
= 인간 감수자가 3차 가번역을 수정하고
= 신규 용어·각주·태그를 만들고
= draft3-instructions.json을 저장하는
= Astro + Node 기반 로컬 편집기
```

이 정도면 실제 개발 가능성이 높습니다.

---

## 10. 최종 의견

Astro는 적합합니다.
다만 “Astro 정적 사이트”가 아니라 **Astro 기반 로컬 서버 앱**으로 설계해야 합니다.

가장 좋은 첫 구현 방향은 다음입니다.

```text
1. Astro + Node adapter
2. JSON 파일 기반 데이터 저장
3. ol-translation-lab을 단일 데이터 소스로 사용
4. 1·2차는 보기 전용
5. 3차 가번역은 인간 수정 영역
6. 4차는 최종 탈고 영역
7. Paperclip 연동은 v0.1에서는 파일 handoff 중심
8. 자동화는 v0.2 이후
```

즉, 지금 구상은 충분히 현실적입니다.
다만 첫 버전의 핵심은 **대시보드 전체 완성**이 아니라 **문서 1개를 실제로 열고, 3차 가번역을 수정하고, B2용 지시 JSON을 생성하는 것**이어야 합니다.

[1]: https://astro.build/?utm_source=chatgpt.com "Astro Build"
[2]: https://docs.astro.build/en/guides/integrations-guide/node/?utm_source=chatgpt.com "astrojs/node - Astro Docs"

---

# 질문 - Paperclip/ 이하는 오직 페이퍼클립 에이전트 초기설정만 담는다

Paperclip/ 이하는 오직 페이퍼클립 에이전트 초기설정을 위한 지침문서를 담는 곳이며 에이전트 생산물은 ol-translation-lab/ 이어야 한다고 생각함. 당신이 의견은?

---

## 응답

네, 그 구분이 맞습니다. 오히려 그렇게 분리해야 장기적으로 안정적입니다.

제가 보기에 최종 원칙은 이렇게 잡는 것이 좋습니다.

```text
paperclip/
= 에이전트 초기 설정과 운영 지침문서만 보관

ol-translation-lab/
= 실제 번역 프로젝트 데이터와 에이전트 생산물 보관

ol-desk/
= Astro 기반 OL DESK 앱 코드
```

## 1. 왜 `paperclip/`에 생산물을 두면 안 되는가

`paperclip/`은 성격상 **에이전트 조직의 헌장·규칙·업무지침 저장소**입니다.

여기에 번역 산출물이 섞이면 다음 문제가 생깁니다.

```text
1. 에이전트 지침과 실제 작업 결과물이 뒤섞임
2. 어떤 파일이 규칙이고 어떤 파일이 산출물인지 불명확해짐
3. Paperclip 초기 세팅을 재사용하기 어려워짐
4. 다른 번역 프로젝트에 같은 에이전트 조직을 복제하기 어려워짐
5. OL DESK가 읽어야 할 데이터 경로가 혼란스러워짐
```

따라서 `paperclip/`은 최대한 깨끗하게 유지하는 것이 좋습니다.

---

## 2. `paperclip/`의 역할

`paperclip/`은 다음만 담당합니다.

```text
paperclip/
├─ company/
│  ├─ initial-task.md
│  ├─ company-policy.md
│  └─ workflow-overview.md
│
└─ agents/
   ├─ CEO-총괄디렉터-법장/
   │  ├─ AGENTS.md
   │  ├─ HEARTBEAT.md
   │  ├─ SOUL.md
   │  └─ TOOLS.md
   │
   ├─ A-관리매니저-선행/
   │  ├─ AGENTS.md
   │  ├─ HEARTBEAT.md
   │  ├─ SOUL.md
   │  └─ TOOLS.md
   │
   └─ ...
```

즉, 이 폴더는 “에이전트 팀을 어떻게 세팅하고 운영할 것인가”만 담습니다.

비유하면:

```text
paperclip/
= 번역도량의 청규, 직책표, 수행 지침, 작업 규칙
```

---

## 3. `ol-translation-lab/`의 역할

에이전트가 실제로 생산하는 모든 결과물은 `ol-translation-lab/`로 가야 합니다.

```text
ol-translation-lab/
├─ sources/
│  ├─ raw/
│  └─ normalized/
│
├─ data/
│  ├─ documents.json
│  ├─ segments/
│  ├─ drafts/
│  ├─ glossary/
│  ├─ annotations/
│  ├─ tags/
│  └─ events/
│
├─ translations/
│  ├─ draft1/
│  ├─ draft2/
│  ├─ draft3/
│  └─ final/
│
├─ reviews/
│  └─ desk/
│
├─ handoff/
│  ├─ draft3/
│  └─ final/
│
├─ queues/
├─ batch-plans/
├─ batch-reports/
└─ manager-logs/
```

비유하면:

```text
ol-translation-lab/
= 실제 번역 작업실, 원고 보관소, 검수대장, 산출물 창고
```

---

## 4. OL DESK 입장에서도 이 구조가 좋음

OL DESK는 `paperclip/`을 거의 읽을 필요가 없습니다.

OL DESK가 읽고 써야 할 곳은 대부분 `ol-translation-lab/`입니다.

```text
OL DESK가 읽는 것:
- documents.json
- segments.json
- drafts.json
- glossary.json
- annotations.json
- tags.json

OL DESK가 쓰는 것:
- review.json
- draft3-instructions.json
- final-instructions.json
- final.md
```

반대로 `paperclip/`은 Paperclip 초기 세팅과 에이전트 지침 수정 때만 사용합니다.

---

## 5. 최종 권장 구조

따라서 개발기획안에는 이렇게 명시하는 것이 좋겠습니다.

```text
ol-desk-project/
├─ ol-desk/
│  └─ Astro 기반 OL DESK 앱 코드
│
├─ ol-translation-lab/
│  └─ 모든 번역 데이터, 에이전트 산출물, 인간 검수 데이터, handoff 파일
│
└─ paperclip/
   └─ Paperclip 에이전트 초기 설정용 지침문서만 보관
```

그리고 원칙 문장으로는 이렇게 쓰면 됩니다.

> **`paperclip/`은 에이전트 조직의 규칙과 초기 지침을 담는 설정층이며, 실제 번역 산출물과 인간 검수 데이터는 모두 `ol-translation-lab/`에 저장한다. OL DESK는 `ol-translation-lab/`을 단일 데이터 소스로 읽고 쓴다.**

이 방향이 가장 깔끔합니다.
특히 나중에 다른 번역 프로젝트를 시작할 때도 `paperclip/` 지침 세트는 재사용하고, `ol-translation-lab/`만 새로 만들 수 있습니다.
