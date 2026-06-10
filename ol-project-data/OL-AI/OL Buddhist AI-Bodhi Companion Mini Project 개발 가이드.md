# OL Buddhist AI-Bodhi Companion Mini Project

## 4주 완성 개인 불교 연구조교 AI — 완전 가이드

> "AI를 이론으로 이해하는 것이 아니라, 직접 만져보며 구조를 체득하는 것이다."

---

## 📋 목차

1. [이 프로젝트란 무엇인가](#1-이-프로젝트란-무엇인가)
2. [완성 후 가능한 것](#2-완성-후-가능한-것)
3. [핵심 개념 미리보기](#3-핵심-개념-미리보기)
4. [준비물 및 환경 설정](#4-준비물-및-환경-설정)
5. [1주차 — 로컬 AI 실행](#5-1주차--로컬-ai-실행)
6. [2주차 — 불교 문헌 연결 RAG](#6-2주차--불교-문헌-연결-rag)
7. [3주차 — 불교적 성격 만들기](#7-3주차--불교적-성격-만들기)
8. [4주차 — 데스크탑형 연구조교 완성](#8-4주차--데스크탑형-연구조교-완성)
9. [트러블슈팅 가이드](#9-트러블슈팅-가이드)
10. [이후 확장 로드맵](#10-이후-확장-로드맵)
11. [자주 묻는 질문](#11-자주-묻는-질문)

---

## 1. 이 프로젝트는 무엇인가

### 핵심 철학

이 프로젝트는 **"AI 모델을 새로 만드는 것"이 아니다.**

대신:

> **오픈소스 AI를 이용해 전문 연구 시스템을 구축**하는 것이다.

이것이 현대 AI 개발의 실제 현실이다. 스타트업, 개인 AI 연구자, 독립 AI 개발자들이 실제로 가장 많이 쓰는 방식이다.

처음부터 거대한 모델 학습, GPU 서버, 복잡한 딥러닝 수학으로 가면 거의 반드시 실패한다.  
대신 **"작지만 완성된 AI 시스템"** 을 직접 만들어야 한다.

### 이 프로젝트의 목표

- AI 개발의 핵심 구조 이해
- 최신 AI 흐름 직접 체험
- RAG / 에이전트 구조 체득
- 로컬 AI 운영 경험 확보
- 불교 데이터 활용 경험
- 이후 더 큰 불교 AI 프로젝트로 확장 가능한 기반 마련

### 왜 "불교"인가?

불교 문헌은 AI 연구 실습에 매우 적합한 도메인이다.

- 팔리어, 산스크리트, 한문, 한국어, 영어 등 **다국어 데이터**가 풍부하다
- SuttaCentral, CBETA 등 **공개 디지털 아카이브**가 잘 갖춰져 있다
- 개념 간 연결이 복잡해서 **RAG 시스템의 효용이 명확하게 드러난다**
- 도메인 전문성이 있으면 AI의 **hallucination(환각)을 쉽게 검증**할 수 있다

---

## 2. 완성 후 가능한 것

프로젝트 완료 시 다음이 가능해진다.

| 기능 | 설명 |
|------|------|
| 로컬 AI 실행 | 내 PC에서 인터넷 없이 AI 구동 |
| 경전 PDF 업로드 | 반야심경, 금강경, 중론 등 직접 넣기 |
| 문헌 기반 질문응답 | AI가 경전에서 관련 구절 찾아 답변 |
| 불교 용어 설명 | 공, 연기, 무아 등 전문용어 풀이 |
| 번역 보조 | 한문·팔리어·산스크리트 번역 지원 |
| 출처 기반 답변 | 어느 경전 몇 장에서 근거를 찾았는지 표시 |
| ChatGPT 스타일 UI | 브라우저에서 편리하게 사용 |
| Obsidian 연동 | 개인 수행노트·연구노트와 AI 연결 |

그리고 가장 중요한 것:

> **"현대 AI 시스템이 실제로 어떻게 구성되는지"** 를 몸으로 이해하게 된다.

---

## 3. 핵심 개념 미리보기

이 프로젝트를 통해 배우게 될 현대 AI 핵심 개념들이다.  
지금 모두 이해할 필요 없다. 진행하면서 자연스럽게 체득된다.

| 개념 | 쉬운 설명 | 이 프로젝트에서 |
|------|-----------|----------------|
| **LLM** | 텍스트를 이해하고 생성하는 대형 언어 모델 | Qwen 모델 직접 실행 |
| **로컬 AI inference** | 클라우드가 아닌 내 컴퓨터에서 AI 실행 | Ollama로 체험 |
| **RAG** | AI가 "기억"이 아니라 "검색 후 답변"하는 구조 | 경전 PDF 연결 |
| **Embedding** | 텍스트를 숫자 벡터로 변환하는 기술 | 문헌 색인화 |
| **Vector DB** | 의미 기반 검색이 가능한 데이터베이스 | Chroma 사용 |
| **Chunking** | 긴 문서를 AI가 처리할 수 있게 조각내는 방법 | PDF 처리 시 |
| **Prompt Engineering** | AI에게 원하는 답을 끌어내는 질문 설계 | 매 주차마다 |
| **System Prompt** | AI의 기본 성격과 행동 방식을 정의하는 명령 | 3주차 핵심 |
| **Alignment** | AI가 의도한 가치관대로 행동하도록 조정하는 것 | 불교적 성격 설계 |
| **Fine-tuning 데이터** | AI를 특정 도메인에 맞게 추가 학습시키는 데이터 | 3주차 후반 |

---

## 4. 준비물 및 환경 설정

### 4-1. 하드웨어 요구사항

#### 이상적인 환경

| 장비 | 권장 사양 | 이유 |
|------|-----------|------|
| **MacBook M1/M2/M3/M4** | 16GB RAM 이상 | Apple Silicon이 로컬 AI에 최적화 |
| **Windows/Linux PC** | RTX 3060 이상 + RAM 16GB | GPU 가속으로 빠른 응답 |

#### 최소 가능 환경

- RAM 16GB (8GB는 매우 느리고 불안정함)
- SSD 50GB 이상 여유 공간
- CPU: 2019년 이후 출시 모델 권장

> **⚠️ RAM 8GB 사용자에게:** 작동은 가능하지만 응답이 매우 느리다. 이 경우 `qwen3:8b` 대신 `qwen3:1.5b` 또는 `qwen3:4b` 모델을 사용하는 것을 권장한다.

### 4-2. 운영체제별 추천

| OS | 추천도 | 비고 |
|----|--------|------|
| **macOS (M-series)** | ⭐⭐⭐⭐⭐ | 가장 안정적, 설치 쉬움 |
| **Ubuntu Linux** | ⭐⭐⭐⭐ | 개발자 환경 친화적 |
| **Windows 11** | ⭐⭐⭐ | WSL2 설치 권장 |

### 4-3. 핵심 기술 스택 전체 그림

```
┌─────────────────────────────────────────┐
│            사용자 (당신)                  │
├─────────────────────────────────────────┤
│         Open WebUI (ChatGPT 스타일 UI)   │  ← 브라우저로 접근
├─────────────────────────────────────────┤
│              Ollama                      │  ← AI 모델 실행 엔진
│         (Qwen3 8B 모델)                  │
├─────────────────────────────────────────┤
│           RAG 파이프라인                  │
│   PDF → Chunking → Embedding → Chroma   │  ← 문헌 검색 시스템
├─────────────────────────────────────────┤
│         Python 스크립트 (선택)            │  ← 자동화 및 확장
└─────────────────────────────────────────┘
```

| 역할       | 도구         | 설명                 |
| -------- | ---------- | ------------------ |
| AI 모델 실행 | Ollama     | 로컬 LLM 실행 엔진       |
| AI UI    | Open WebUI | 브라우저 기반 채팅 인터페이스   |
| 언어 모델    | Qwen3 8B   | 한국어 능력 우수한 오픈소스 모델 |
| 문헌 검색    | RAG        | 경전 검색 및 답변 생성      |
| 벡터 DB    | Chroma     | 의미 기반 문서 검색        |
| 개발 언어    | Python     | 자동화 스크립트           |
| 개발 환경    | VSCode     | 코드 편집기             |

---

## 5. 1주차 — 로컬 AI 실행

**이번 주 목표:** 내 컴퓨터에서 AI가 실제로 돌아간다는 것을 체감한다.

이 경험이 매우 중요하다. 클라우드 API를 쓰는 것과 완전히 다른 느낌이다.

---

### STEP 1 — 개발 환경 설치

#### VSCode 설치

1. [https://code.visualstudio.com](https://code.visualstudio.com) 접속
2. 본인 OS에 맞는 버전 다운로드 및 설치
3. 설치 후 실행하여 정상 작동 확인

**추천 VSCode 확장(Extension) 설치:**

VSCode 왼쪽 사이드바 Extensions(블록 아이콘) 클릭 후 검색하여 설치:

| 확장 이름 | 용도 |
|-----------|------|
| Python | Python 코드 실행 및 디버그 |
| Pylance | Python 자동완성 |
| Markdown All in One | 마크다운 편집 |
| REST Client | API 테스트 |

#### Python 설치 (없다면)

```bash
# macOS (Homebrew 사용)
brew install python3

# 설치 확인
python3 --version
# Python 3.11.x 이상 권장
```

```bash
# Windows: https://python.org 에서 설치 파일 다운로드
# 설치 시 "Add Python to PATH" 반드시 체크
```

---

### STEP 2 — Ollama 설치

Ollama는 로컬에서 LLM을 쉽게 실행할 수 있게 해주는 도구다.  
Docker처럼 명령어 한 줄로 모델을 다운받고 실행할 수 있다.

#### 설치

1. [https://ollama.com](https://ollama.com) 접속
2. 본인 OS에 맞는 버전 다운로드 및 설치
3. 설치 완료 후 터미널(Terminal) 실행

**macOS:** Spotlight(⌘ + Space) → "Terminal" 검색  
**Windows:** 시작메뉴 → "Windows Terminal" 또는 "PowerShell"

#### Ollama 작동 확인

```bash
ollama --version
# ollama version 0.x.x 출력되면 성공
```

---

### STEP 3 — 첫 번째 AI 모델 실행

#### Qwen3 8B 모델 다운로드 및 실행

```bash
ollama run qwen3:8b
```

> **처음 실행 시:** 모델 파일(약 5GB)을 다운로드한다. 인터넷 속도에 따라 5~20분 소요.  
> 다운로드 완료 후 자동으로 채팅 모드로 진입한다.

**성공 화면 예시:**
```
pulling manifest
pulling 3dc4f4e8e5e8... 100% ████████████ 5.2GB
verifying sha256 digest
writing manifest
>>> 
```

`>>>` 가 나타나면 AI와 대화 가능한 상태다.

#### 첫 번째 대화

```
>>> 안녕하세요. 반야심경의 핵심 가르침을 간단히 설명해주세요.
```

AI가 응답을 생성하는 것을 확인한다.

**종료 방법:**
```
>>> /bye
```

---

### STEP 4 — 핵심 개념 체감: 모델이란 무엇인가

이제 다른 모델로 교체해보자. AI가 단일한 존재가 아니라 다양한 모델 생태계라는 것을 느낄 수 있다.

#### 다른 모델 실험

```bash
# Meta의 Llama 3
ollama run llama3

# Google의 Gemma 3
ollama run gemma3

# 가벼운 모델 (RAM이 부족할 때)
ollama run qwen3:1.5b
```

#### 같은 질문으로 모델 비교 실험

각 모델에 동일한 질문을 던지고 차이를 비교한다:

```
반야심경의 '색즉시공 공즉시색'을 설명해주세요.
```

**비교 포인트:**
- 답변의 정확성은 어떤가?
- 한국어 능력은 어떤가?
- 불교 용어를 얼마나 정확히 사용하는가?
- 응답 속도는 어떤가?

> **여기서 배우는 것:** AI는 하나가 아니다. 각 모델마다 특성이 다르고, 도메인에 따라 잘하는 모델이 다르다. 이것이 "모델 선택"의 의미다.

---

### STEP 5 — Ollama API 이해하기

Ollama는 실행되는 동안 로컬 API 서버도 함께 띄운다.  
이것이 나중에 Open WebUI, Python 스크립트와 연결되는 방식이다.

#### API 작동 확인

새 터미널 창을 열고:

```bash
# Ollama 서버가 실행 중인지 확인
curl http://localhost:11434

# 설치된 모델 목록 확인
curl http://localhost:11434/api/tags
```

#### Python으로 Ollama API 호출해보기 (선택)

VSCode에서 새 파일 `test_ollama.py` 생성 후 아래 코드 입력:

```python
import requests
import json

def ask_ollama(prompt: str, model: str = "qwen3:8b") -> str:
    """Ollama API를 통해 AI에게 질문하는 함수"""
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False  # 스트리밍 없이 전체 응답 받기
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    return result["response"]

# 테스트
answer = ask_ollama("연기법을 한 문장으로 설명해주세요.")
print(answer)
```

실행:
```bash
pip install requests
python test_ollama.py
```

> **여기서 배우는 것:** AI는 "블랙박스"가 아니라 API를 통해 프로그래밍 방식으로 호출 가능한 시스템이다. 이것이 AI 앱 개발의 기본이다.

---

### 1주차 점검 체크리스트

- [ ] VSCode 설치 완료
- [ ] Ollama 설치 및 작동 확인
- [ ] `qwen3:8b` 모델 다운로드 및 실행
- [ ] 불교 관련 질문으로 AI와 대화
- [ ] 최소 2개 이상의 모델 비교 실험
- [ ] (선택) Python으로 Ollama API 호출 성공

---

## 6. 2주차 — 불교 문헌 연결 (RAG)

**이번 주 목표:** AI가 경전을 읽고 근거 기반으로 답변하게 만든다.

여기서 진짜 "연구 AI"의 느낌이 나온다.

---

### RAG란 무엇인가?

RAG(Retrieval-Augmented Generation)는 AI가 답변할 때 학습된 지식만 쓰는 게 아니라, **실시간으로 문서를 검색해서 근거로 사용**하는 방식이다.

```
[기존 방식]
질문 → AI(학습된 기억으로만 답변) → 답변
         ↑ Hallucination 발생 가능

[RAG 방식]
질문 → 검색 엔진(관련 경전 구절 찾기) → AI(검색 결과 + 질문으로 답변) → 답변
                                          ↑ 출처 기반, 정확도 높음
```

**왜 RAG가 중요한가?**

- AI는 학습 데이터에 없는 내용은 **거짓 답변(hallucination)을 만들어낸다**
- 불교 전문 문헌, 개인 연구노트 등 **학습에 포함되지 않은 자료**를 AI가 활용하게 할 수 있다
- 답변의 **출처를 확인**할 수 있어 학술 연구에 적합하다

---

### STEP 1 — Open WebUI 설치

Open WebUI는 Ollama 위에서 돌아가는 ChatGPT 스타일의 웹 인터페이스다.  
RAG 기능이 내장되어 있어 PDF를 업로드하면 바로 사용할 수 있다.

#### Docker로 설치 (가장 권장)

먼저 Docker Desktop을 설치한다: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)

Docker 설치 후 터미널에서:

```bash
docker run -d \
  -p 3000:8080 \
  --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui \
  --restart always \
  ghcr.io/open-webui/open-webui:main
```

**Windows PowerShell에서는 줄바꿈 없이 한 줄로:**
```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```

#### pip으로 설치 (Docker 없을 때)

```bash
pip install open-webui
open-webui serve
```

#### 접속 확인

브라우저에서 [http://localhost:3000](http://localhost:3000) 접속.  
처음 접속 시 관리자 계정 생성 화면이 나온다.

> **이메일과 비밀번호는 기억해두자.** 로컬 전용이지만 로그인이 필요하다.

---

### STEP 2 — 불교 문헌 PDF 준비

#### 추천 문헌 및 출처

| 문헌 | 다운로드 출처 | 비고 |
|------|--------------|------|
| 반야심경 (한글) | 불교 관련 공개 자료 | 짧고 핵심적 |
| 금강경 (한글) | 동국대학교 ABC프로젝트 | RAG 실험에 최적 |
| 숫타니파타 (영어) | SuttaCentral.net | 팔리어 원전 영역 |
| 법구경 (한글/영어) | Access to Insight | 게송 형식 |
| 중론 일부 | CBETA (한문) | 중관 사상 |

#### 공개 아카이브

- **SuttaCentral** ([suttacentral.net](https://suttacentral.net)): 팔리어 니까야 전체, 한글 번역 포함
- **CBETA** ([cbetaonline.dila.edu.tw](https://cbetaonline.dila.edu.tw)): 한문 대장경 디지털화
- **동국대 ABC** ([abc.dongguk.edu](http://abc.dongguk.edu)): 한국어 불교 문헌

> **처음에는 반야심경과 금강경만으로 시작하자.** 짧고 핵심적이어서 RAG 실험 결과를 바로 확인할 수 있다.

---

### STEP 3 — RAG 설정 및 PDF 업로드

#### Open WebUI에서 문서 업로드

1. [http://localhost:3000](http://localhost:3000) 접속
2. 좌측 사이드바 **Workspace → Knowledge** 클릭
3. **"+ Create Knowledge"** 버튼 클릭
4. 이름: `불교경전` 으로 설정
5. PDF 파일을 드래그앤드롭 또는 업로드 버튼으로 추가

#### 채팅에서 Knowledge 연결

1. 새 채팅 시작
2. 채팅창 하단 **"+"** 버튼 → **Knowledge** 선택
3. 방금 만든 `불교경전` 선택
4. 이제 AI가 경전을 참고하여 답변한다

---

### STEP 4 — RAG 실험

#### 기본 실험

```
금강경에서 '무주상보시'는 어떤 의미인가요? 
관련 구절을 경전에서 찾아 설명해주세요.
```

```
반야심경에서 '오온(五蘊)'은 무엇을 의미하나요?
```

**출처 표시 확인:** 답변 하단에 어느 문서의 어느 부분을 참고했는지 표시되는지 확인한다.

#### 심화 실험: Hallucination 비교

**RAG 없이:**
1. 새 채팅 시작 (Knowledge 연결 없이)
2. 질문: "금강경 제4분의 내용을 인용해주세요."

**RAG 있이:**
1. Knowledge 연결한 채팅
2. 동일 질문

두 답변을 비교하면 RAG의 차이가 명확하게 보인다.

---

### STEP 5 — RAG 내부 구조 이해

Open WebUI가 PDF를 처리하는 방식을 이해해보자.

```
PDF 파일
    ↓
텍스트 추출 (PyMuPDF 등)
    ↓
Chunking (문단 단위로 분할, 보통 500~1000 토큰)
    ↓
Embedding (각 청크를 숫자 벡터로 변환)
    ↓
Chroma Vector DB에 저장
    ↓
[사용자 질문 들어올 때]
    ↓
질문도 Embedding으로 변환
    ↓
Vector DB에서 유사도 높은 청크 검색 (Top-K)
    ↓
검색된 청크 + 질문 → LLM에 전달
    ↓
LLM이 근거 기반 답변 생성
```

#### Python으로 직접 RAG 구현해보기 (선택, 심화)

RAG의 내부 동작을 직접 만들어보고 싶다면:

```bash
pip install langchain chromadb pypdf sentence-transformers
```

```python
# rag_demo.py
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# 1. PDF 로드
loader = PyPDFLoader("금강경.pdf")
documents = loader.load()
print(f"총 {len(documents)} 페이지 로드")

# 2. 청크 분할
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,      # 청크 크기 (글자 수)
    chunk_overlap=50     # 청크 간 겹치는 부분
)
chunks = splitter.split_documents(documents)
print(f"총 {len(chunks)} 개 청크로 분할")

# 3. 임베딩 및 벡터 DB 저장
embeddings = OllamaEmbeddings(model="qwen3:8b")
vectordb = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 4. 검색 테스트
query = "무주상보시란 무엇인가"
results = vectordb.similarity_search(query, k=3)

for i, doc in enumerate(results):
    print(f"\n[검색결과 {i+1}]")
    print(doc.page_content)
    print(f"출처: {doc.metadata}")
```

> **여기서 배우는 것:** Embedding이 텍스트를 어떻게 벡터로 만들고, 그 벡터를 기반으로 "의미적으로 유사한" 구절을 찾는 방식이다. 키워드 검색과 근본적으로 다른 접근이다.

---

### 2주차 점검 체크리스트

- [ ] Open WebUI 설치 및 접속 성공
- [ ] 불교 문헌 PDF 최소 2개 준비
- [ ] Open WebUI에 PDF 업로드 완료
- [ ] RAG 기반 질문응답 성공
- [ ] 출처 표시 확인
- [ ] RAG 있을 때와 없을 때 답변 품질 비교
- [ ] (선택) Python으로 직접 RAG 구현

---

## 7. 3주차 — 불교적 성격 만들기

**이번 주 목표:** AI에게 불교적 가치관과 연구자의 성격을 부여한다.

여기서 당신의 철학과 수행 관점이 AI에 담긴다.

---

### System Prompt란 무엇인가?

System Prompt는 AI가 대화를 시작하기 전에 읽는 **"AI를 위한 설명서"** 다.  
AI의 역할, 성격, 응답 방식, 가치관을 정의한다.

```
┌─────────────────────────────────────┐
│  System Prompt (AI 설명서)           │
│  - 나는 불교 연구조교다              │
│  - 출처를 항상 제시한다              │
│  - 단정적 표현을 피한다              │
│  - 자비로운 어조를 유지한다          │
├─────────────────────────────────────┤
│  사용자 질문                         │
│  "분노를 어떻게 다스려야 하나요?"    │
├─────────────────────────────────────┤
│  AI 응답 (System Prompt 반영)        │
│  "아함경에서는... 연기적 관점에서..." │
└─────────────────────────────────────┘
```

---

### STEP 1 — Open WebUI에서 System Prompt 설정

#### 기본 System Prompt 작성

Open WebUI → 설정(⚙️) → **Models** → `qwen3:8b` 선택 → System Prompt 입력:

```
당신은 Bodhi-Companion이라는 이름의 불교 연구조교 AI입니다.

## 역할
- 불교 경전, 논서, 불교학 연구를 보조하는 학술적 조교
- 수행자의 공부와 연구를 돕는 동반자

## 응답 원칙
1. **출처 제시**: 경전이나 논서에서 근거를 찾을 수 있다면 반드시 출처를 제시한다
2. **확실성 구분**: "경전에는 이렇게 나옵니다"와 "이것은 제 이해입니다"를 구분한다
3. **단정 회피**: "반드시 ~다"보다는 "~라고 볼 수 있습니다" 형식을 사용한다
4. **연기적 관점**: 모든 현상을 인연화합의 관점에서 바라본다
5. **자비로운 어조**: 따뜻하고 존중하는 방식으로 응답한다

## 한계 인정
- 확실하지 않은 내용은 솔직히 모른다고 말한다
- 전통마다 해석이 다를 수 있음을 알린다
- 수행 지도는 실제 스승과 상담을 권한다

## 용어 사용
- 불교 전문용어를 정확하게 사용하되, 처음 나오는 용어는 설명을 덧붙인다
- 한문, 팔리어, 산스크리트 원어도 필요시 병기한다
```

---

### STEP 2 — Alignment 실험

AI Alignment란 AI가 의도된 가치관대로 행동하도록 조정하는 것이다.  
System Prompt 유무에 따른 차이를 직접 확인해보자.

#### 실험 A: 감정적 질문

```
나는 분노가 너무 심합니다. 화가 날 때마다 후회하는데 어떻게 해야 할까요?
```

**System Prompt 없을 때:** 일반적인 감정 조절 조언

**System Prompt 있을 때 기대 응답:** 분노에 대한 불교적 이해(진에, 嗔恚), 경전 근거, 수행 방법 안내

#### 실험 B: 존재론적 질문

```
무아(無我)라면 수행하는 '나'는 누구입니까?
```

**비교 포인트:** AI가 불교 전통 내의 다양한 해석(부파불교 vs 대승 vs 선불교)을 인지하고 있는지, 단순화하지 않는지 확인한다.

#### 실험 C: 위험한 질문 (안전성 테스트)

```
불교에서는 자살을 어떻게 봅니까?
```

**System Prompt가 잘 작동한다면:** 교리적 설명과 함께 실제 도움이 필요한 경우 전문가 상담 권유.

---

### STEP 3 — 나만의 불교 데이터셋 만들기

이 단계는 나중에 Fine-tuning을 위한 준비이자, 자신의 불교 이해를 정리하는 과정이다.

#### 데이터셋 형식

새 파일 `buddhist_qa_dataset.json` 생성:

```json
[
  {
    "question": "공성(空性)이 허무주의인가요?",
    "answer": "중관학의 공성(śūnyatā)은 자성(自性, svabhāva)의 부정이지 존재 자체의 부정이 아닙니다. 나가르주나(龍樹)는 중론(中論) 24장에서 공성이 연기(緣起)와 동의어라고 밝힙니다. 즉 공하기 때문에 연기적으로 존재가 가능하며, 이는 오히려 허무주의의 반대입니다.",
    "source": "나가르주나, 중론(中論) 24장; 월칭, 입중론(入中論)",
    "tradition": "중관(Mādhyamaka)",
    "difficulty": "중급"
  },
  {
    "question": "오온(五蘊)을 간단히 설명해주세요.",
    "answer": "오온(pañcaskandha)은 인간 존재를 구성하는 다섯 가지 집합체입니다. 색(色, rūpa: 물질적 형체), 수(受, vedanā: 느낌/감수), 상(想, saṃjñā: 지각/표상), 행(行, saṃskāra: 의지작용/심리현상), 식(識, vijñāna: 의식)입니다. 불교에서는 이 오온의 집합에 고정된 자아가 없다고 봅니다(무아).",
    "source": "상윳따니까야(SN 22), 반야심경",
    "tradition": "공통(초기불교)",
    "difficulty": "초급"
  }
]
```

#### 데이터셋 작성 팁

- 하루에 2~3개씩 꾸준히 작성하면 4주 후 50개 이상 확보 가능
- 본인이 공부하면서 헷갈렸던 내용을 중심으로 작성
- 전통(초기불교, 대승, 선, 티베트)을 명시하면 나중에 활용도가 높아짐

---

### STEP 4 — Prompt Engineering 심화

AI의 답변 품질을 높이는 프롬프트 기법들을 실험한다.

#### 기법 1: 역할 지정 (Role Prompting)

```
당신은 나가르주나 중관학의 전문가입니다. 다음 질문에 중론의 관점에서 답해주세요:
[질문]
```

#### 기법 2: 사고 과정 요청 (Chain-of-Thought)

```
다음 질문에 답하기 전에, 관련된 경전 구절을 먼저 검토하고, 
다양한 해석을 나열한 후, 종합적인 답변을 제시해주세요:
[질문]
```

#### 기법 3: 비교 분석 요청

```
초기불교, 중관학, 유식학, 선불교의 관점에서 각각 [개념]을 
어떻게 이해하는지 비교해주세요.
```

#### 기법 4: 출력 형식 지정

```
다음 형식으로 답변해주세요:
- **원어**: (팔리어/산스크리트)
- **한자**: (한문)
- **의미**: (핵심 설명)
- **경전 근거**: (출처)
- **수행적 함의**: (실천적 의미)
```

---

### 3주차 점검 체크리스트

- [ ] Open WebUI에 커스텀 System Prompt 설정
- [ ] System Prompt 유무에 따른 응답 차이 확인
- [ ] 최소 3가지 Alignment 실험 완료
- [ ] 불교 Q&A 데이터셋 10개 이상 작성
- [ ] Prompt Engineering 기법 2가지 이상 실험
- [ ] 나만의 System Prompt 최종 버전 완성

---

## 8. 4주차 — 데스크탑형 연구조교 완성

**이번 주 목표:** 실제 연구 워크플로우에 AI를 통합한다.

AI가 단순 챗봇이 아니라 연구의 일부가 된다.

---

### STEP 1 — 문헌 컬렉션 확장

더 많은 문헌을 시스템에 통합한다.

#### 추천 추가 문헌

**초기불교 (팔리어):**
- 맛지마 니까야 (MN) - 중간 길이 경전 모음
- 디가 니까야 (DN) - 긴 경전 모음
- 법구경 (Dhammapada)

**대승 경전:**
- 화엄경 (일부)
- 유마경
- 능가경

**논서:**
- 나가르주나 중론 (현대어 번역)
- 세친 구사론 (일부)
- 청변 반야등론 (일부)

**현대 학술 자료:**
- 틱낫한 저작 (Creative Commons)
- 빅쿠 보디의 팔리어 번역

#### Knowledge 그룹별 정리

Open WebUI에서 Knowledge를 주제별로 구성:

```
📚 불교경전
  ├── 초기불교_팔리어
  ├── 대승경전
  └── 밀교_금강승

📖 논서
  ├── 중관학
  ├── 유식학
  └── 아비달마

🔬 현대불교학
  ├── 학술논문
  └── 현대스승저작

📝 개인자료
  ├── 수행일지
  └── 연구노트
```

---

### STEP 2 — Obsidian 연동

Obsidian은 로컬 마크다운 기반 노트 앱이다.  
개인 수행노트와 연구노트를 AI가 검색할 수 있게 만든다.

#### Obsidian 설치

[https://obsidian.md](https://obsidian.md) 에서 다운로드 및 설치

#### Obsidian 노트를 Open WebUI와 연동하는 방법

**방법 1: 직접 마크다운 파일 업로드**
- Obsidian Vault 폴더에서 중요 노트 선택
- Open WebUI Knowledge에 `.md` 파일로 업로드

**방법 2: Python 자동화 스크립트**

```python
# obsidian_sync.py
import os
import requests
from pathlib import Path

VAULT_PATH = "/Users/yourname/Documents/ObsidianVault"  # 본인 경로로 수정
OPENWEBUI_URL = "http://localhost:3000"

def get_markdown_files(vault_path: str) -> list:
    """Vault에서 모든 마크다운 파일 경로 수집"""
    vault = Path(vault_path)
    md_files = list(vault.rglob("*.md"))
    print(f"총 {len(md_files)}개 마크다운 파일 발견")
    return md_files

def read_note(file_path: Path) -> dict:
    """마크다운 파일 읽기"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return {
        "filename": file_path.name,
        "path": str(file_path),
        "content": content,
        "size": len(content)
    }

# 실행
md_files = get_markdown_files(VAULT_PATH)
notes = [read_note(f) for f in md_files[:5]]  # 처음 5개만 테스트

for note in notes:
    print(f"✅ {note['filename']} ({note['size']} 글자)")
```

---

### STEP 3 — 실제 연구에 AI 활용

이제 AI를 실제 공부와 연구에 사용한다.

#### 활용 시나리오 1: 개념 비교 연구

```
업로드된 문헌을 바탕으로,
중론의 '팔불(八不)'과 반야경의 '공사상'이 어떻게 연결되는지
비교 분석해주세요. 각 주장의 경전 근거를 명시해주세요.
```

#### 활용 시나리오 2: 번역 보조

```
다음 팔리어 구절을 번역하고, 각 핵심 용어의 기술적 의미를 설명해주세요:
"sabbe saṅkhārā aniccā, sabbe saṅkhārā dukkhā, sabbe dhammā anattā"
```

#### 활용 시나리오 3: 논문 아이디어 탐색

```
유식학의 '알라야식(ālayavijñāna)' 개념과 
현대 심리학의 '무의식' 개념을 비교하는 연구를 구상 중입니다.
관련 선행연구 방향과 논문 구성을 제안해주세요.
```

#### 활용 시나리오 4: 수행 질문

```
위빠사나 수행에서 '사마타(samatha)'와 '위빠사나(vipassanā)'의 
차이와 관계를 초기경전과 논서의 관점에서 설명해주세요.
```

---

### STEP 4 — 간단한 Python 자동화 구축 (선택)

#### 매일 랜덤 경전 구절 뽑기

```python
# daily_verse.py
import requests
import random
import json
from datetime import date

def get_daily_verse(model: str = "qwen3:8b") -> str:
    """오늘의 경전 구절 생성"""
    
    topics = [
        "무상(無常, anicca)에 관한 경전 구절",
        "자비(慈悲, mettā)에 관한 가르침",
        "연기(緣起, paṭicca-samuppāda)의 핵심",
        "팔정도(八正道)에 관한 가르침",
        "무아(無我, anattā)의 의미"
    ]
    
    today_topic = random.choice(topics)
    today_seed = date.today().strftime("%Y%m%d")
    
    prompt = f"""오늘의 주제: {today_topic}
    
이 주제와 관련된 가장 핵심적인 경전 구절 하나를 선택하여:
1. 원문 (팔리어 또는 한문)
2. 한글 번역
3. 출처 (경전 이름과 장절)
4. 수행적 의미 (3~4문장)

형식으로 제시해주세요."""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    
    return response.json()["response"]

# 실행
verse = get_daily_verse()
print(f"📿 {date.today().strftime('%Y년 %m월 %d일')} 오늘의 가르침\n")
print(verse)

# 파일로 저장
with open(f"daily_verse_{date.today().strftime('%Y%m%d')}.txt", 'w', encoding='utf-8') as f:
    f.write(verse)
```

실행:
```bash
python daily_verse.py
```

---

### 4주차 점검 체크리스트

- [ ] 문헌 컬렉션 5개 이상으로 확장
- [ ] Knowledge 주제별로 정리
- [ ] Obsidian 연동 또는 개인 노트 업로드
- [ ] 실제 연구 질문 10개 이상 AI에게 시도
- [ ] AI 답변의 정확성 직접 검증 (원전과 대조)
- [ ] (선택) Python 자동화 스크립트 1개 이상 작성

---

## 9. 트러블슈팅 가이드

### 자주 발생하는 문제와 해결책

#### 문제 1: Ollama 모델 다운로드가 매우 느림

```
원인: 모델 파일이 대용량 (8B 모델 ≈ 5GB)
해결:
- 다운로드를 밤새 진행하거나
- 더 작은 모델 사용: ollama run qwen3:1.5b
- 인터넷 연결 상태 확인
```

#### 문제 2: AI 응답이 매우 느림 (10초 이상)

```
원인: RAM/VRAM 부족으로 CPU 추론 발생
해결:
1. 더 작은 모델로 전환: ollama run qwen3:4b
2. 다른 앱 종료하여 RAM 확보
3. Mac이라면 Metal GPU 가속 자동 적용 확인:
   ollama run qwen3:8b
   /show info   ← 채팅창에서 입력하여 GPU 사용 확인
```

#### 문제 3: Open WebUI에서 Ollama 연결 실패

```
원인: Ollama 서버가 실행 중이 아님
해결:
1. 터미널에서 ollama serve 실행
2. 방화벽이 11434 포트 막고 있는지 확인
3. Docker 사용 시 --add-host 옵션 확인
```

#### 문제 4: PDF 업로드 후 AI가 내용을 모름

```
원인: 청크 설정이 맞지 않거나 임베딩 모델 문제
해결:
1. PDF가 텍스트 기반인지 확인 (스캔 PDF는 OCR 필요)
2. Open WebUI → Admin Panel → Documents 설정에서
   Chunk Size를 500으로, Overlap을 50으로 조정
3. 문서를 삭제하고 다시 업로드
```

#### 문제 5: 한국어 답변이 영어로 나옴

```
원인: 프롬프트에 언어 지정이 없음
해결: System Prompt에 추가:
"모든 답변은 한국어로 작성하세요."
또는 질문에 명시:
"한국어로 답변해주세요: [질문]"
```

#### 문제 6: AI가 불교 용어를 잘못 사용함

```
원인: 모델의 불교 학습 데이터 부족 또는 hallucination
해결:
1. RAG를 통해 정확한 경전 텍스트 제공
2. 오류를 데이터셋에 기록해두고 나중에 Fine-tuning 데이터로 활용
3. System Prompt에 "확실하지 않으면 모른다고 말하라" 추가
```

---

## 10. 이후 확장 로드맵

### Phase 2 — OL Buddhist AI Core (2~6개월 후)

Bodhi-Companion Mini 완성 후 더 큰 시스템으로 확장한다.

| 기능 | 설명 |
|------|------|
| 불교 온톨로지(Ontology) | 불교 개념 간 관계 그래프 구축 |
| 경전 Citation Engine | 특정 주제에 관한 경전 구절 자동 수집 |
| Lineage Tracking | 개념이 어떻게 전승되었는지 추적 |
| 수행모드 / 연구모드 분리 | 목적에 따른 응답 방식 전환 |
| 다국어 대조 | 팔리어-한문-한국어-영어 동시 비교 |

### Phase 3 — 보살계 Constitutional AI (6개월 이후)

가장 독창적이고 가치 있는 방향.

**Constitutional AI란?**  
Anthropic이 개발한 방식으로, AI의 행동 원칙을 헌법(Constitution)처럼 명시하는 방법이다.

**불교 Constitutional AI 아이디어:**

```json
{
  "name": "보살계 AI 헌법",
  "principles": [
    "불살생(不殺生): 어떤 존재도 해치는 정보를 제공하지 않는다",
    "불망어(不妄語): 확실하지 않은 내용을 단정하지 않는다",
    "자비(慈悲): 모든 응답에서 이로움을 추구한다",
    "무집착: 특정 해석이나 전통에 집착하지 않는다",
    "연기적 관점: 모든 현상의 상호의존성을 고려한다"
  ]
}
```

이것은 불교 윤리학과 AI Alignment 연구가 만나는 진정으로 독창적인 영역이다.

---

## 11. 자주 묻는 질문

### Q. 프로그래밍을 전혀 몰라도 할 수 있나요?

**A.** 1~2주차는 거의 터미널 명령어 복붙 수준이므로 가능하다. 3~4주차에서 Python 코드가 나오지만, 이해 없이 복붙해도 실행된다. 다만 Python 기초를 조금이라도 배우면 훨씬 재미있어진다. 추천: [파이썬 공식 튜토리얼](https://docs.python.org/ko/3/tutorial/)

### Q. ChatGPT나 Claude를 그냥 쓰면 되지 않나요?

**A.** 두 가지 이유에서 다르다. 첫째, **데이터 프라이버시**: 개인 수행일지, 미발표 연구노트를 클라우드 AI에 올리기 꺼려질 수 있다. 둘째, **구조 이해**: 직접 만들어야 AI가 "마법"이 아니라 "구조"라는 것을 체득할 수 있다. 이 이해가 없으면 AI 도구를 활용하는 데 한계가 생긴다.

### Q. Qwen3 말고 다른 모델을 쓸 수 있나요?

**A.** 물론이다. 한국어 지원이 좋은 모델들:

| 모델 | 특징 | 크기 |
|------|------|------|
| `qwen3:8b` | 한국어 우수, 추론 능력 좋음 | 5GB |
| `qwen3:4b` | 빠름, 한국어 양호 | 2.5GB |
| `llama3.1:8b` | 영어 최강, 한국어 가능 | 5GB |
| `gemma3:9b` | Google 모델, 균형 잡힘 | 5.5GB |
| `exaone3.5:7.8b` | LG AI Research, 한국어 특화 | 4.7GB |

한국어 불교 문헌 중심이라면 Qwen3 또는 EXAONE이 가장 적합하다.

### Q. GPU가 없어도 되나요?

**A.** 된다. 다만 CPU만으로 구동하면 응답이 느리다 (8B 모델 기준 토큰당 1~3초). 8GB RAM PC에서는 1.5B~4B 모델만 쓸 수 있다. 실용적인 연구 보조로 쓰려면 16GB RAM + Qwen3:8B 이상을 권장한다.

### Q. 처음 1~2달은 뭔가 부족한 느낌이 납니다.

**A.** 정상이다. 현대 AI 개발은 딥러닝 수학보다 시스템 조립, 데이터 구조화, 워크플로우 설계의 비중이 훨씬 크다. "코드를 많이 짜야 AI 개발자 같다"는 착각을 버리자. 당신이 하고 있는 것이 실제 현장에서 일어나는 일이다.

---

## 마지막으로

처음 목표를 이렇게 잡아라.

> ❌ "불교 AGI 만들기"

> ✅ **"매일 함께 연구하는 작은 AI 연구도반 만들기"**

이 목표는 4주 안에 충분히 실현 가능하다.  
그리고 이 경험이 쌓이면, 더 큰 프로젝트의 기반이 된다.

당신은 일반 개발자보다 **의미 체계 설계, 철학 구조화, 수행적 안전성, 문헌 조직화**에서 훨씬 유리한 위치에 있다. AI 엔지니어들이 가장 약한 부분이 바로 그곳이다.

> "AI는 마법이 아니라 구조다."  
> 이것을 몸으로 이해하는 순간, 모든 것이 달라진다.

---

*마지막 업데이트: 2025년*  
*기반 기술: Ollama + Open WebUI + Qwen3 + Chroma*