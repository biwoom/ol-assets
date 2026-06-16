# 🌐 통합 불교 문헌 번역 프레임워크 (UBTF) 아키텍처 명세서
(Unified Buddhist Translation Framework - Architecture Specification)

본 문서는 UBTF(통합 불교 문헌 번역 프레임워크)의 디렉토리 구조 및 계층적 자산 관리 설계를 기술합니다. 이 아키텍처는 원본 문헌의 보호와 다국어 서브 프로젝트의 유연한 확장을 핵심 목표로 합니다.

---

## 1. 디렉토리 구조 트리 (Directory Structure Tree)

```txt
OL-CONTENTS/
├── source/
│   └── raw/                   [최상단 원본 소스 보관소 - Read Only]
│       ├── en/                (영어 문헌 원본)
│       │   ├── BuddhaStory/   - 마하붓다왐사 영어 원본
│       │   └── Visuddhimagga/ - 청정도론 영역본 원본
│       ├── lzh/               (한역 문헌 원본)
│       │   ├── LotusSutra/    - 묘법연화경 한문 원본
│       │   └── AmitabhaSutra/ - 아미타경 한문 원본
│       ├── pli/               (빨리어 문헌 원본)
│       └── san/               (범어 문헌 원본)
│
├── translation/               [번역 작업 공간]
│   ├── en-kr/                 (영한 번역 영역)
│   │   ├── BuddhaStory/       - 마하붓다왐사 번역 프로젝트
│   │   │   ├── draft-1/       1차 학술적 초안
│   │   │   ├── draft-2/       2차 대중적 윤문
│   │   │   └── draft-3/       3차 감수 통합 및 이중언어 검토본
│   │   └── Visuddhimagga/     - 청정도론 번역 프로젝트 (동일하게 draft-1/2/3 수용)
│   │
│   ├── lzh-kr/                (한역-한글 번역 영역)
│   │   ├── LotusSutra/        - 법화경 한역 번역 프로젝트
│   │   └── AmitabhaSutra/     - 아미타경 한역 번역 프로젝트
│   │
│   ├── pli-kr/                (빨리어-한글 번역 영역)
│   └── san-kr/                (범어-한글 번역 영역)
│
├── term/                      [프로젝트별 용어 제어]
│   ├── cumulative/            - 범불교적 누적 대조 용어집 (pli-san-lzh-en-kr)
│   ├── en-kr/
│   │   ├── BuddhaStory/       - 마하붓다왐사 전용 Term 파일들
│   │   └── Visuddhimagga/
│   └── lzh-kr/
│       ├── LotusSutra/
│       └── AmitabhaSutra/
│
├── log/                       [번역 자가검증 및 감수 로그 공간]
│   ├── en-kr/
│   │   ├── BuddhaStory/       (draft-1/, draft-2/, final-review/ 로그 분할)
│   │   └── Visuddhimagga/
│   └── lzh-kr/
│       ├── LotusSutra/
│       └── AmitabhaSutra/
│
└── outputs/
    └── manuscripts/           [최종 한국어 전용 경전 원고 추출처]
        ├── en-kr/
        │   ├── BuddhaStory/   - 마하붓다왐사 최종 한국어 경전 파일
        │   └── Visuddhimagga/
        └── lzh-kr/
            ├── LotusSutra/
            └── AmitabhaSutra/
```

---

## 2. 핵심 설계 지향점 (Core Architectural Guidelines)

### 2.1 최상단 원본 소스 보호막 (`source/raw/`)
*   **원칙**: 번역의 시발점이 되는 모든 원문 자료는 `source/raw/` 하위의 언어군 및 프로젝트 단위로 원형 보존합니다.
*   **보안 규칙**: 어떠한 자동화 스크립트나 AI 에이전트도 이 디렉토리 내의 파일들을 생성, 수정, 삭제할 수 없도록 물리적/논리적으로 제한합니다. (오직 사람이 수동으로 소스를 보관할 때만 쓰기 권한 허용)

### 2.2 동일 언어군 내 다중 프로젝트 독립성 (`translation/` & `outputs/`)
*   영어 번역(`en-kr`)이나 한역 번역(`lzh-kr`) 내에서도 텍스트의 성격, 스타일 지침, TOC 매핑이 상이한 개별 프로젝트들이 존재할 수 있습니다.
*   모든 번역 작업과 최종 마크다운 결과물은 `{language-code}-kr/{project-id}/` 라는 서브 폴더 명세를 통해 완벽하게 네임스페이스가 분리되어 충돌을 방지합니다.

### 2.3 다중 레이어 용어 제어 모델 (`term/`)
*   **Local Terminology (프로젝트별 용어집)**: 개별 경전 프로젝트의 고유 대조 용어는 `term/{lang-kr}/{project-id}/` 아래에 별도로 적재되어 관리됩니다.
*   **Global Terminology (통합 누적 용어집)**: 역사적으로 가치가 인정되거나 여러 프로젝트에서 교차 검증된 불교 개념어는 `term/cumulative/` 경로로 상향 통합되어 프레임워크 전반의 번역 일관성을 향상시킵니다.

---

## 3. 향후 스크립트 확장 및 이관 가이드라인
*   파이프라인 검증 스크립트(`run_pipeline.py`) 구동 시 `--lang`과 `--project` 인자를 필수적으로 매개변수화하여, 실행 경로가 상단의 UBTF 디렉토리 레이아웃에 맞춰 자동으로 바인딩되도록 업그레이드할 예정입니다.
