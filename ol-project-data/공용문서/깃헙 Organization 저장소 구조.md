# 깃헙 Organization 저장소 구조

## 질문

OL-PROJECT 깃헙 organization 저장소 설계를 제안해줘. OL-HOME / OL-ATLAS / OL-BOOK / OL-CONTENTS. OL-HOME 저장소는 깃헙페이지를 활용해 olbit.org 홈페이지가 될 저장소. 이 홈페이지 역할-atlas와 book 컨텐츠 다운로드 페이지 제공, atlas 기능 소개, book UX 소개, 불교인포그래픽과 디자인-삽화이미지 등의 앨범이면서 라이브러리 제공.  OL-ATLAS 저장소는 atlas 소스코드, OL-BOOK 저장소는 소스코드가 아닌 book형태의 불교컨텐츠들을 모아서 저장. OL-CONTENTS 저장소는 불교인포그래픽과 디자인-삽화이미지 등의 저장소.
이렇게 구상하고 있는데 이에 대한 당신의 의견을 제시해줘. 그런데 내가 궁금한 점은 OL-CONTENTS 저장소에 불교인포그래픽 이미지를 업로드 하면 이 이미지 웹주소를 olbit.org 홈페이지에서 사용할 수 있나? 불교인포그래픽과 디자인-삽화이미지 등의 이미지나 아티팩트 등은 어떤 저장소에 저장하는 것이 좋을까? OL-HOME 저장소? OL-CONTENTS 저장소?

---
## 의견

현재 구상은 상당히 좋은 방향입니다. 특히 중요한 점은, 단순 “코드 저장소” 구조가 아니라 **OL의 철학적 레이어(홈/도구/콘텐츠/아카이브)를 분리하려고 한다는 점**입니다. 이는 장기적으로 매우 중요합니다.  
당신의 현재 구조는 이미 다음 철학과 잘 맞습니다:

- OL-HOME = “디지털 도량의 입구”
    
- OL-ATLAS = “도구(engine)”
    
- OL-BOOK = “법(法) 콘텐츠”
    
- OL-CONTENTS = “시각 자산 라이브러리”
    

이는 현재 선언문과 브랜드 정의서의 방향성과도 상당히 일치합니다. 특히 “콘텐츠와 도구의 분리”, “fork 가능한 구조”, “자산 관리 체계 초기 설계” 원칙과 잘 연결됩니다.

다만 장기 운영 관점에서 몇 가지 구조적 조정을 추천합니다.

---

# 1. 추천 Organization 구조

추천 구조:

```text
OL-PROJECT (GitHub Organization)
│
├── ol-home
├── ol-atlas
├── ol-book
├── ol-contents
│
├── ol-design-system      (선택)
├── ol-docs               (선택)
├── ol-lab                (선택)
└── .github               (organization 공통 설정)
```

---

# 2. 각 저장소 역할 추천

## 2.1 OL-HOME

### 역할

`olbit.org` 자체.

즉:

- 랜딩 페이지
    
- 브랜드 소개
    
- 선언문
    
- atlas 다운로드
    
- book 라이브러리
    
- 콘텐츠 진입 포털
    
- 이미지 갤러리 일부
    
- 뉴스/업데이트
    
- 프로젝트 철학
    

### 기술 추천

```text
GitHub Pages + Astro or Next static export
```

또는 초기엔:

```text
정적 HTML/CSS/JS
```

로 매우 단순하게 시작해도 충분.

---

## 2.2 OL-ATLAS

이건 아주 명확합니다.

### 저장 내용

- atlas source code
    
- build system
    
- dist outputs
    
- docs
    
- release notes
    

### 중요한 점

여기는 “앱 엔진 저장소”입니다.

따라서 콘텐츠를 과도하게 넣지 않는 것이 중요합니다.

즉:

```text
atlas ≠ 콘텐츠 저장소
atlas = reader/runtime
```

이 분리가 매우 중요합니다.

현재 당신이 추구하는:

> tool / content separation

철학과 완전히 일치합니다.

---

## 2.3 OL-BOOK

이 저장소 방향도 매우 좋습니다.

다만 여기서 핵심은:

> “source manuscript repository” 인가?  
> 아니면 “deployable books repository” 인가?

를 구분하는 것입니다.

나는 다음을 추천합니다.

---

### 추천: OL-BOOK = “배포용 웹북 저장소”

즉:

```text
books/
  buddha-story/
  dhammapada/
  madhyamaka/
```

각 폴더 안:

```text
index.html
assets/
manifest.json
```

형태.

즉:

- 실제 사용자에게 전달 가능한 형태
    
- atlas 탑재 가능 형태
    
- 단일 HTML 산출물
    

중심.

---

### 반면 원고/스크립트는?

가능하면 별도:

```text
ol-manuscripts
```

또는 로컬/private repo.

왜냐하면:

- AI 생성 중간 산출물
    
- 번역 초안
    
- 검수 기록
    
- 실험 데이터
    

는 매우 빠르게 저장소를 오염시킵니다.

---

# 3. 핵심 질문: 이미지 자산은 어디에?

이 질문이 사실 가장 중요합니다.

당신 질문:

> 인포그래픽 이미지를 업로드하면  
> 그 웹주소를 olbit.org 에서 사용할 수 있나?

정답:

## 예. 가능하다.

GitHub 저장소의 raw URL 또는 GitHub Pages URL로 사용 가능.

예:

```text
https://raw.githubusercontent.com/OL-PROJECT/ol-contents/main/infographics/karma-map.webp
```

또는 GitHub Pages 활성화 시:

```text
https://ol-project.github.io/ol-contents/infographics/karma-map.webp
```

그리고 이것을:

- ol-home
    
- ol-book
    
- atlas
    

모두에서 사용 가능.

---

# 4. 그런데 실제로 어디 저장하는 것이 좋은가?

여기서 중요한 건:

> “사용 목적” 기준으로 나누는 것.

이게 핵심입니다.

---

# 5. 내가 추천하는 실제 구조

## 결론 먼저

### “공용 자산”은 OL-CONTENTS

### “홈페이지 전용 자산”은 OL-HOME

이 구조 추천.

---

# 6. 왜 그렇게 해야 하는가

## 6.1 OL-HOME에 다 넣으면 생기는 문제

처음엔 편합니다.

하지만 시간이 지나면:

```text
homepage assets
+
webtoon assets
+
infographics
+
atlas screenshots
+
logos
+
illustrations
+
social thumbnails
```

가 혼재합니다.

그러면:

- 빌드 느려짐
    
- 저장소 비대화
    
- 이미지 재사용 어려움
    
- 구조 혼란
    
- 브랜딩 자산 관리 어려움
    

이 생깁니다.

특히 당신 프로젝트는:

> 이미지 자산이 폭발적으로 증가할 가능성

이 매우 높습니다.  
이미 기획서에서도 자산 관리 중요성을 언급했습니다.

---

# 7. 따라서 추천 구조

## OL-CONTENTS

여기를 “Canonical Asset Repository”로 사용.

즉:

```text
ol-contents/
│
├── infographics/
├── illustrations/
├── icons/
├── logos/
├── maps/
├── characters/
├── webtoon/
├── social/
├── thumbnails/
└── textures/
```

그리고:

```text
metadata/
style-guides/
licenses/
```

같은 것도 추가 가능.

---

# 8. 그리고 OL-HOME은?

OL-HOME은:

```text
홈페이지 조립용 저장소
```

로 유지.

즉:

- layout
    
- pages
    
- minimal local assets
    

만 유지.

이미지는 가능하면:

```html
<img src="https://...ol-contents/...">
```

처럼 외부 참조.

---

# 9. 그러나 예외가 있다

다음은 OL-HOME 내부에 두는 게 좋음:

## 홈페이지 전용 경량 자산

예:

```text
favicon
hero background
small ui icons
og-image
```

왜냐하면:

- 외부 fetch 줄임
    
- 초기 렌더 안정성
    
- homepage portability
    

때문.

---

# 10. 장기적으로 매우 중요한 추천

## “원본(master)”과 “배포용(optimized)” 분리

이거 정말 중요합니다.

추천:

```text
ol-contents/
  source/
  optimized/
```

예:

```text
source/illustrations/buddha-4k.psd
optimized/illustrations/buddha.webp
```

왜냐하면:

- 웹 최적화본 필요
    
- SNS용 필요
    
- atlas embed용 필요
    
- retina 대응 필요
    

등이 생깁니다.

---

# 11. 추가로 강력 추천하는 저장소

## ol-design-system

이건 미래에 매우 중요해질 가능성 큼.

여기에:

- color tokens
    
- typography
    
- spacing
    
- icon rules
    
- illustration guides
    
- prompt guides
    
- SVG assets
    

보관.

즉:

```text
OL visual canon
```

저장소.

당신 프로젝트는 단순 앱이 아니라:

> 불교 디지털 미학 체계

를 만들 가능성이 높기 때문입니다.

---

# 12. 가장 추천하는 최종 구조

```text
OL-PROJECT
│
├── ol-home
│   └── 홈페이지/배포 포털
│
├── ol-atlas
│   └── 앱 엔진
│
├── ol-book
│   └── 배포형 웹북
│
├── ol-contents
│   └── 공용 시각 자산 라이브러리
│
├── ol-design-system
│   └── 디자인 규칙/토큰/브랜드 시스템
│
└── ol-manuscripts (private 추천)
    └── 번역 원고/초안/AI workflow
```

---

# 13. 당신 구조의 가장 좋은 점

현재 구상에서 가장 뛰어난 부분은:

> “도구와 콘텐츠를 분리하려는 태도”

입니다.

대부분 프로젝트는 초기에:

```text
app + content + assets + experiments
```

를 한 저장소에 다 밀어넣고,  
나중에 유지보수 지옥이 됩니다.

반면 지금 당신 방향은:

- atlas = runtime
    
- book = canon
    
- contents = assets
    
- home = gateway
    

로 역할 분리가 매우 선명합니다.

이건 장기적으로 상당히 건강한 구조입니다.