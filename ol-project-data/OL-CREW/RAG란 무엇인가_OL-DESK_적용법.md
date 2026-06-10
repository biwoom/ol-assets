## 1. RAG란 무엇인가

**RAG**는 특정 제품 이름이 아니라 AI 개발 방식입니다.

정식 명칭은 **Retrieval-Augmented Generation**, 보통 한국어로는 **검색 증강 생성**이라고 번역합니다. 말 그대로 AI가 자기 머릿속 지식만으로 답하는 것이 아니라, 먼저 외부 자료를 **검색**하고, 그 자료를 읽은 뒤, 그 근거에 기대어 답을 **생성**하게 하는 방식입니다. IBM은 RAG를 “AI 모델을 외부 지식베이스와 연결하여 성능을 높이는 아키텍처”라고 설명합니다. ([IBM][1])

아주 쉽게 말하면 이렇습니다.

```text
일반 AI:
질문 → AI가 기억과 추론으로 답변

RAG AI:
질문 → 관련 문서 검색 → 관련 부분 읽기 → 근거를 바탕으로 답변
```

비유하면, 일반 AI는 “많이 배운 사람”이고, RAG AI는 “많이 배운 사람이 도서관 검색까지 하면서 대답하는 방식”입니다.

---

## 2. RAG는 특정 오픈소스인가?

아닙니다.

**RAG는 특정 오픈소스 프로그램이 아니라 AI 시스템을 설계하는 개념·방법론입니다.**

다만 RAG를 구현할 때 여러 오픈소스 도구를 사용할 수 있습니다.

대표적으로는 다음 계열이 있습니다.

```text
LLM 실행 도구
- Ollama
- LM Studio
- llama.cpp

RAG 개발 프레임워크
- LlamaIndex
- LangChain
- Haystack

벡터 데이터베이스
- Chroma
- Qdrant
- Milvus
- FAISS

문서 처리 도구
- PyMuPDF
- unstructured
- LlamaParse
```

LlamaIndex 문서는 RAG의 색인 단계에서 데이터를 넣고, 임베딩을 만들고, 이를 vector store에 저장해 검색 가능하게 만든다고 설명합니다. ([Developer Documentation][2]) Ollama는 로컬에서 오픈 모델을 실행하기 위한 도구이며, 공식 사이트에서도 터미널 설치 명령과 오픈 모델 실행을 안내합니다. ([Ollama][3])

따라서 정리하면 다음과 같습니다.

```text
RAG = 개념 / 설계 방식
LlamaIndex = RAG를 쉽게 만들게 해주는 개발 프레임워크
Chroma, Qdrant = 문서 조각을 검색 가능하게 저장하는 벡터DB
Ollama = 로컬 AI 모델을 실행하는 도구
```

---

## 3. RAG는 왜 필요한가

AI는 기본적으로 자신이 학습된 범위 안에서 답합니다. 그런데 불교 문헌 작업에서는 다음 문제가 자주 생깁니다.

```text
- 특정 문헌의 어느 구절에 근거하는가?
- 같은 사건이 다른 문헌에서는 어떻게 나타나는가?
- 같은 용어가 니까야, 아함, 논서, 대승경전에서 다르게 쓰이는가?
- 현대 해설서의 설명은 원문 근거와 얼마나 가까운가?
- 이 문장은 번역인가, 해석인가, 창작적 확장인가?
```

일반 AI에게 그냥 물으면 그럴듯한 답을 만들 수는 있지만, 원문 근거가 불분명할 수 있습니다. RAG는 이 문제를 줄이기 위한 방식입니다.

RAG의 핵심 기능은 네 가지입니다.

```text
1. 내 자료를 읽게 한다.
2. 질문과 관련된 부분만 찾아온다.
3. 찾아온 근거를 바탕으로 답하게 한다.
4. 답변이 어떤 자료에 근거했는지 추적하게 한다.
```

NVIDIA도 RAG를 “특정하고 관련 있는 데이터 소스에서 정보를 가져와 생성형 AI 모델의 정확성과 신뢰성을 높이는 기술”로 설명합니다. ([NVIDIA Blog][4])

---

## 4. RAG의 기본 작동 구조

RAG는 보통 두 단계로 나뉩니다.

### A. 사전 준비 단계

문서를 미리 정리해 검색 가능한 상태로 만듭니다.

```text
문서 수집
→ 문서 정리
→ 작은 조각으로 나누기
→ 각 조각을 숫자 벡터로 변환
→ 벡터DB에 저장
```

여기서 중요한 개념이 **임베딩 embedding**입니다.

임베딩은 문장의 의미를 숫자 좌표로 바꾸는 작업입니다. 예를 들어 “부처님의 탄생”, “마야부인의 꿈”, “룸비니 동산”은 서로 의미적으로 가까우므로 벡터 공간에서도 가깝게 배치됩니다.

### B. 질문 응답 단계

사용자가 질문하면 다음 흐름이 일어납니다.

```text
질문 입력
→ 질문도 임베딩으로 변환
→ 벡터DB에서 의미적으로 가까운 문서 조각 검색
→ 관련 문서 조각을 AI에게 함께 전달
→ AI가 근거를 읽고 답변 생성
→ 가능하면 출처 표시
```

즉, RAG의 핵심은 **AI가 모든 문서를 한 번에 기억하는 것이 아니라, 질문할 때마다 관련 부분을 찾아서 읽는 것**입니다.

---

## 5. RAG와 “AI 학습”은 다르다

이 부분이 매우 중요합니다.

RAG는 보통 AI 모델을 새로 학습시키는 것이 아닙니다.

```text
Fine-tuning / 학습:
AI 모델의 내부 가중치를 바꿈.
AI 자체의 습관과 지식을 바꾸는 방식.

RAG:
AI 모델은 그대로 둠.
대신 외부 문서를 검색해서 답변에 참고하게 함.
```

비유하면 이렇습니다.

```text
Fine-tuning = 사람의 머릿속 지식과 말버릇을 훈련시키는 것
RAG = 사람 옆에 잘 정리된 도서관과 검색 시스템을 붙여주는 것
```

OL 프로젝트의 초기 단계에서는 불교 AI를 직접 학습시키는 것보다 RAG가 훨씬 현실적입니다. 왜냐하면 문헌을 계속 추가·수정해도 모델을 다시 학습시킬 필요가 없기 때문입니다.

---

## 6. 오픈소스 로컬 AI가 꼭 필요한가?

꼭 필요하지는 않습니다. 선택지는 세 가지입니다.

### 1) 클라우드 AI + 로컬 문서 검색

예를 들어 ChatGPT API, Claude API, Gemini API 등을 사용하고, 문서 색인과 검색은 내 컴퓨터에서 처리하는 방식입니다.

장점은 답변 품질이 높고 개발이 상대적으로 쉽다는 것입니다. 단점은 민감한 자료나 미공개 원고가 외부 API로 전송될 수 있다는 점입니다.

### 2) 완전 로컬 AI + 로컬 RAG

Ollama, LM Studio, llama.cpp 같은 도구로 모델을 내 컴퓨터에서 실행하고, Chroma나 Qdrant 같은 벡터DB도 로컬에서 실행합니다.

장점은 자료 통제권이 높고, 인터넷 없이도 작동할 수 있다는 것입니다. 단점은 컴퓨터 성능이 필요하고, 대형 모델 수준의 답변 품질을 얻기 어렵거나 속도가 느릴 수 있습니다.

### 3) 혼합형

검색·색인·자료 저장은 로컬에서 하고, 어려운 해석·문체 생성은 클라우드 AI에게 맡기는 방식입니다.

OL 프로젝트에는 이 혼합형이 가장 현실적입니다.

```text
로컬:
- 원문 저장
- 자료 색인
- 검색
- source packet 생성
- 근거 위치 보존

클라우드 또는 고성능 모델:
- 해석 후보 생성
- 문체 변환
- 대본화
- 해설문 작성
```

장기적으로는 완전 로컬화할 수 있지만, 초기에는 혼합형이 효율적입니다.

---

## 7. 구글 NotebookLM과 RAG는 어떻게 다른가

NotebookLM은 사용자가 올린 자료를 바탕으로 요약, 질의응답, 학습자료, 오디오 개요 등을 만들어주는 Google의 AI 연구·학습 도구입니다. Google은 NotebookLM을 “사용자의 sources를 분석하고 복잡한 내용을 명확하게 바꾸는 AI research tool”이라고 소개합니다. ([Google NotebookLM][5]) 공식 FAQ에 따르면 NotebookLM은 노트북과 source 수, source당 단어 수, 업로드 용량 등에 제한이 있습니다. ([구글 도움말][6])

NotebookLM은 넓은 의미에서 RAG적 성격을 가진 서비스라고 볼 수 있습니다. 사용자가 넣은 자료를 근거로 답하기 때문입니다.

하지만 OL 프로젝트에서 말하는 RAG Layer와는 성격이 다릅니다.

```text
NotebookLM:
완성된 서비스

OL용 RAG:
직접 설계하는 내부 시스템
```

차이를 표로 정리하면 다음과 같습니다.

| 항목         | NotebookLM           | OL용 로컬 RAG                                           |
| ---------- | -------------------- | ---------------------------------------------------- |
| 성격         | Google이 제공하는 완성형 서비스 | 직접 만드는 시스템 구조                                        |
| 자료 저장      | Google 서비스 내부        | 내 로컬 폴더·DB                                           |
| 커스터마이징     | 제한적                  | 자유롭게 설계 가능                                           |
| 데이터 구조     | 사용자가 내부 구조를 통제하기 어려움 | source_profile, event_index, chapter_dossier 등 직접 설계 |
| OL-DESK 연동 | 직접 연동 어려움            | OL-DESK/OL-Runner와 직접 연결 가능                          |
| 장기 보존성     | 서비스 정책에 의존           | 내 프로젝트 구조에 의존                                        |
| 적합 용도      | 빠른 문서 이해, 요약, 학습     | 장기 문헌 작업, 근거 추적, 콘텐츠 제작 파이프라인                        |

따라서 NotebookLM은 **연구 보조 도구**로는 매우 좋습니다. 하지만 OL-DESK의 Source Collection Layer를 담당하는 내부 엔진으로 쓰기에는 한계가 있습니다.

쉽게 말하면,

```text
NotebookLM = 똑똑한 외부 독서실
OL RAG = OL 프로젝트 안에 직접 짓는 자료 도서관과 검색 사서
```

입니다.

---

## 8. RAG 설치법은 어떻게 되는가

RAG는 하나의 프로그램이 아니므로 “RAG 설치”라는 것은 정확히 말하면 없습니다. 대신 다음 구성요소들을 설치합니다.

가장 쉬운 로컬 실험 구성은 다음입니다.

```text
1. Python
2. Ollama
3. LlamaIndex
4. Chroma 또는 Qdrant
5. 임베딩 모델
6. 생성 모델
```

예시 구성은 다음과 같습니다.

```text
AI 실행:
Ollama

생성 모델:
llama3.1, qwen, gemma 계열 등

임베딩 모델:
nomic-embed-text 또는 bge 계열

RAG 프레임워크:
LlamaIndex

벡터DB:
Chroma
```

Ollama는 공식적으로 macOS, Linux, Windows에서 오픈 모델을 실행할 수 있게 해주는 도구이며, 공식 설치 명령도 제공합니다. ([Ollama][3]) LlamaIndex는 RAG 파이프라인과 에이전트형 앱을 만들기 위한 프레임워크를 제공합니다. ([Developer Documentation][7])

개념적 설치 흐름은 이렇습니다.

```bash
# 1. Ollama 설치 후 모델 받기
ollama pull llama3.1
ollama pull nomic-embed-text

# 2. Python 가상환경 만들기
python -m venv .venv
source .venv/bin/activate

# 3. RAG 관련 패키지 설치
pip install llama-index chromadb
pip install llama-index-llms-ollama
pip install llama-index-embeddings-ollama
```

실제 코드는 프로젝트 구조에 맞게 따로 작성해야 합니다.

---

## 9. 실제 운영법은 어떻게 되는가

OL 프로젝트 기준으로 실제 운영은 다음 흐름이 좋습니다.

### 1단계: 자료 폴더 만들기

```text
ol-source-library/
  buddha-life/
    mahābuddhavaṃsa/
    buddhacarita/
    lalitavistara/
    nikaya-agama/
    modern-studies/
```

### 2단계: 자료 메타데이터 작성

각 자료마다 이런 정보를 붙입니다.

```yaml
id: source-mahabuddhavamsa-001
title: Mahābuddhavaṃsa
language: English / Burmese / Pāli
tradition: Theravāda
source_type: canonical_commentarial_narrative
reliability_note: 전승적 서사 자료. 사건 구성에는 유용하나 역사비평적 검토 필요.
use_for:
  - buddha_life_event_index
  - narrative_source
  - comparison
```

### 3단계: 문서를 chunk로 나누기

한 문서를 너무 크게 넣으면 검색이 부정확해집니다. 너무 작게 나누면 맥락이 끊깁니다.

불교 문헌 작업에서는 다음 단위가 좋습니다.

```text
- 장
- 절
- 문단
- 게송
- 사건 단위
- 의미 단위
```

### 4단계: 색인 만들기

문서 조각을 임베딩으로 바꾸고 벡터DB에 저장합니다.

```text
문서 조각
→ 임베딩
→ 벡터DB 저장
→ 검색 가능 상태
```

### 5단계: 질문 또는 작업 명령

예를 들어 이렇게 묻습니다.

```text
“싯다르타 태자의 출가 사건과 관련된 원천자료를 찾아줘.
각 자료별로 사건 순서, 주요 인물, 정서적 강조점, 차이를 정리해줘.”
```

### 6단계: source packet 생성

검색 결과를 그냥 답변으로 끝내지 않고, OL-DESK가 읽을 수 있는 구조로 저장합니다.

```yaml
source_packet_id: packet-great-renunciation-001
topic: great_renunciation
related_sources:
  - source_id: buddhacarita
    location: canto_5
    summary_ko: 태자의 출가가 시적·영웅적 장면으로 묘사됨.
  - source_id: mahabuddhavamsa
    location: chapter_x
    summary_ko: 전생 발원과 보살행의 맥락에서 출가가 해석됨.
conflicts:
  - 출가 시점과 주변 인물 묘사 차이
human_check_required: true
```

### 7단계: chapter dossier로 묶기

```text
source packet 여러 개
→ chapter dossier
→ 새 목차 한 장의 자료 묶음
→ 인간 편집장이 최종 원고 작성
```

이 흐름이 OL-DESK의 Source Collection Layer와 가장 잘 맞습니다.

---

## 10. OL 프로젝트에서 RAG는 어디에 놓이는가

제가 권하는 위치는 다음입니다.

```text
[자료 폴더]
원문, 번역본, 연구서, 메모

↓ 색인

[OL-Source RAG]
검색, 유사 구절 탐색, source packet 생성

↓ 실행

[OL-Runner]
toc-extract, event-index, theme-index, source-align,
chapter-dossier-build, grounding-check

↓ 표시

[OL-DESK]
Source Board, Meaning Board, Desk Mode

↓ 산출

[OL-BOOK / OL-TOON / OL-STUDIO]
```

즉, RAG는 OL-Runner를 대체하는 것이 아니라 **OL-Runner 앞에서 자료를 찾아주는 기반 계층**입니다.

---

## 11. RAG가 잘하는 일과 못하는 일

RAG가 잘하는 일은 다음입니다.

```text
- 많은 문서 중 관련 부분 찾기
- 비슷한 사건·주제·용어 찾기
- 특정 원고에 필요한 근거 모으기
- 문헌 간 비교 후보 만들기
- 출처 기반 요약 만들기
- 초안용 자료 묶음 만들기
```

RAG가 못하거나 조심해야 할 일은 다음입니다.

```text
- 최종 교리 해석 확정
- 원전 간 우열 판단
- 역사적 사실 최종 판정
- 전승 차이의 정통성 판단
- 창작적 각색의 허용 범위 결정
- 인간 편집자의 책임 판단 대체
```

따라서 OL 프로젝트에서 RAG는 **사서**이지 **최고편집장**이 아닙니다.

---

## 12. 초보자용 최소 실험 로드맵

처음부터 큰 시스템을 만들 필요는 없습니다.

가장 작은 실험은 다음 정도면 됩니다.

```text
실험 1:
PDF 또는 Markdown 문서 3개를 폴더에 넣는다.

실험 2:
LlamaIndex로 문서를 색인한다.

실험 3:
“출가 장면 관련 자료를 찾아줘”라고 질문한다.

실험 4:
검색된 문단과 요약을 함께 출력한다.

실험 5:
출력 결과를 YAML source_packet으로 저장한다.

실험 6:
OL-DESK Source Board에서 이 YAML을 읽어 보여준다.
```

이 정도만 성공해도 OL-RAG의 핵심은 이미 체험한 것입니다.

---

## 13. 가장 중요한 구분

마지막으로 핵심만 정리하면 다음입니다.

```text
RAG는 특정 프로그램이 아니다.
RAG는 AI가 외부 자료를 검색해서 근거 기반으로 답하게 하는 설계 방식이다.

RAG는 AI 학습과 다르다.
모델을 다시 훈련시키는 것이 아니라, 자료 검색 능력을 붙이는 것이다.

오픈소스 로컬 AI는 선택 사항이다.
완전 로컬, 클라우드 혼합, 클라우드 중심 모두 가능하다.

NotebookLM은 RAG적 성격의 완성형 서비스다.
하지만 OL 프로젝트의 데이터 구조와 창작 파이프라인을 직접 통제하려면 자체 RAG가 필요하다.

OL에서 RAG의 역할은 최고편집장이 아니라 사서다.
자료를 찾아오고, 근거를 묶고, 차이를 표시하고, 인간 판단을 돕는 계층이다.
```

따라서 OL 프로젝트에 맞는 최종 정의는 이렇게 잡으면 좋습니다.

> **OL-Source RAG는 불교 원전·번역·연구서·메모를 로컬에서 색인하고, 특정 사건·주제·교리·문장에 관련된 근거 자료를 찾아 `source packet`과 `chapter dossier`로 묶어 OL-Runner와 OL-DESK에 전달하는 자료 검색·근거 보조 계층이다.**

[1]: https://www.ibm.com/think/topics/retrieval-augmented-generation?utm_source=chatgpt.com "What is RAG (Retrieval Augmented Generation)?"
[2]: https://developers.llamaindex.ai/python/framework/understanding/rag/?utm_source=chatgpt.com "Introduction to RAG | Developer Documentation - LlamaParse"
[3]: https://ollama.com/?utm_source=chatgpt.com "Ollama"
[4]: https://blogs.nvidia.com/blog/what-is-retrieval-augmented-generation/?utm_source=chatgpt.com "What Is Retrieval-Augmented Generation aka RAG"
[5]: https://notebooklm.google/?utm_source=chatgpt.com "Google NotebookLM | AI Research Tool & Thinking Partner"
[6]: https://support.google.com/notebooklm/answer/16269187?hl=en&utm_source=chatgpt.com "Frequently asked questions - NotebookLM Help"
[7]: https://developers.llamaindex.ai/python/framework/?utm_source=chatgpt.com "Welcome to LlamaIndex ! | Developer Documentation"
