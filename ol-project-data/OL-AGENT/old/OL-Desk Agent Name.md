# OL Buddhist Translation Desk Agent Name 

```text
CEO / Translation Director Agent
= CEO-총괄디렉터-법장
```

## A 라인 — Draft Production Mode

| 기존 영어 명칭                   | 한국어 명칭       |
| -------------------------- | ------------ |
| A-Draft Production Manager | A-관리매니저-선행   |
| Basic Setup Agent          | A1-기초정리-정안   |
| Reference Split Agent      | A2-참고번역분리-분명 |
| Glossary Agent             | A3-용어후보-명해   |
| Draft 1 Translator Agent   | A4-1차번역-초역   |
| Source Review Agent        | A5-대조감수-조견   |
| Annotation Candidate Agent | A6-각주-해의     |
| Draft 2 Translator Agent   | A7-2차번역-윤문   |

## B 라인 — Editorial Confirmation Mode

| 기존 영어 명칭                         | 한국어 명칭      |
| -------------------------------- | ----------- |
| B-Editorial Confirmation Manager | B-확정매니저-결정 |
| Human Review Preparation         | B1-인간검수-청문  |
| Draft 3 Integration              | B2-3차반영-정반  |
| Final Scan                       | B3-최종스캔-무루  |
| Final Handoff                    | B4-최종인계-회향  |

## 전체 매칭 목록

```text
CEO / Translation Director Agent
→ CEO-총괄디렉터-법장

A-Draft Production Manager
→ A-관리매니저-선행

Basic Setup Agent
→ A1-기초정리-정안

Reference Split Agent
→ A2-참고번역분리-분명

Glossary Agent
→ A3-용어후보-명해

Draft 1 Translator Agent
→ A4-1차번역-초역

Source Review Agent
→ A5-대조감수-조견

Annotation Candidate Agent
→ A6-각주-해의

Draft 2 Translator Agent
→ A7-2차번역-윤문

B-Editorial Confirmation Manager
→ B-확정매니저-결정

Human Review Preparation
→ B1-인간검수-청문

Draft 3 Integration
→ B2-3차반영-정반

Final Scan
→ B3-최종스캔-무루

Final Handoff
→ B4-최종인계-회향
```

## 전체 조직 트리

```text
CEO-총괄디렉터-법장

├─ A-관리 매니저-선행
│  ├─ A1-기초정리-정안
│  ├─ A2-참고번역분리-분명
│  ├─ A3-용어후보-명해
│  ├─ A4-1차번역-초역
│  ├─ A5-대조감수-조견
│  ├─ A6-각주-해의
│  └─ A7-2차번역-윤문
│
└─ B-3차 확정 관리 매니저-결정
   ├─ B1-인간검수-청문
   ├─ B2-3차반영-정반
   ├─ B3-최종스캔-무루
   └─ B4-최종인계-회향
```

## 법명 의미

```text
법장 法藏
- 전체 번역 프로젝트의 법문 저장고, 총괄 디렉터에 적합

선행 善行
- 여러 문서를 2차 번역까지 밀어 올리는 생산 실천 관리자

정안 正眼
- 원문을 바르게 보는 기초 정리 담당

분명 分明
- 원문과 참고번역을 분명히 나누는 역할

명해 明解
- 용어의 뜻을 밝히고 후보를 제시하는 역할

초역 初譯
- 1차 번역 담당

조견 照見
- 원문과 번역을 비추어 보고 누락·오역을 점검하는 역할

해의 解義
- 각주와 해석 후보를 풀어내는 역할

윤문 潤文
- 2차 번역에서 문장을 자연스럽게 다듬는 역할

결정 決定
- 인간이 확정한 판단만 3차 이후에 반영하도록 관리하는 역할

청문 聽聞
- 인간 편집자가 검수할 내용을 잘 듣고 정리하는 역할

정반 正反
- 확정된 내용을 바르게 반영하는 역할

무루 無漏
- 최종스캔에서 누락과 오류가 새지 않도록 점검하는 역할

회향 回向
- 최종탈고 전 사람에게 원고를 넘기는 인계 역할
```


## 다른 에이전트에 통합 검토

- A2-참고번역분리-분명
- B1-인간검수-청문
- B4-최종인계-회향