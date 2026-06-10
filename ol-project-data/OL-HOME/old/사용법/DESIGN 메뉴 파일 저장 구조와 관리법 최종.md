# DESIGN 메뉴 파일 저장 구조와 관리법 최종

## 질문
현재 BOOK완성책 등록시 아래와 같이 완성책html과 메타데이터를 분리 저장하는데 DESIGN 페이지에 내가 만든 개별 이미지들, 인포그래픽들을 등록하는 경우에도 이와같은 방식을 차용하는 것이 좋을지 아니면 더 나은 대안이 있을지 검토해줘. 그리고 깃헙에서 이미지를 무제한 등록할 수 있는 저장용량을 제공하는지도 조사해줘.

---
## 응답
두 질문에 대해 답변합니다.

---

## 1. GitHub 저장 용량 한계

저장소 권장 크기는 1GB 미만이고, 5GB 미만이 강력 권장됩니다. 개별 파일은 100MB가 최대이며, 이를 초과하면 push가 차단됩니다. 50MB 이상 파일은 경고가 발생하고, 브라우저 업로드는 25MB가 한도입니다.

정리하면:

```
개별 파일:     100MB 이하 (50MB 이상 경고)
저장소 전체:   1GB 권장, 5GB 강력 권장, 100GB 하드 리밋
이미지 개수:   제한 없음 (총 용량만 제한)
```

**OL DESIGN에 미치는 영향**: 웹용 이미지(JPG/PNG/WebP)는 보통 100KB~2MB이므로 개별 파일 제한에는 문제없습니다. 하지만 이미지가 수백 장 쌓이면 저장소 전체가 무거워집니다. 예를 들어 평균 500KB 이미지 1000장이면 500MB로, 권장 1GB의 절반을 이미지만으로 차지합니다.

---

## 2. DESIGN 페이지 — BOOK 패턴 적용 여부

### BOOK과 DESIGN의 차이

```
BOOK:    파일 1개 = 완결된 책 (5~50MB HTML)
         → 메타데이터 분리가 당연함

DESIGN:  파일 1개 = 이미지 (100KB~2MB)
         → 이미지 자체가 가벼움, 메타가 더 중요
```

BOOK은 "거대한 HTML + 가벼운 메타"이지만, DESIGN은 "가벼운 이미지 + 풍부한 메타"입니다. 성격이 반대입니다.

### 권장: BOOK 패턴 변형 채택, 단 구조를 단순화

BOOK처럼 두 곳에 나누되, DESIGN의 특성에 맞게 조정합니다.

```
src/content/design/              ← 메타데이터 (md)
  gandhara-buddha-face.md
  goryeo-monk-robe.md

public/design/                   ← 실제 이미지 파일
  gandhara-buddha-face.jpg
  goryeo-monk-robe.png
```

BOOK과의 차이: BOOK은 `public/books/{이름}/index.html` 폴더 구조이지만, DESIGN은 **이미지 파일을 바로 저장**합니다. 폴더로 감쌀 필요 없음.

### DESIGN 메타데이터 md 예시

```markdown
<!-- src/content/design/gandhara-buddha-face.md -->
---
title: "간다라 양식 불상 얼굴"
type: portrait          # costume | architecture | portrait | artifact | landscape | manuscript
era: "1~3세기"
region: "간다라 (현 파키스탄)"
tradition: "초기 대승"

# 이미지 경로 (public/ 기준)
imagePath: "gandhara-buddha-face.jpg"    # → public/design/gandhara-buddha-face.jpg
imageAlt: "간다라 양식 불상의 정면 얼굴 클로즈업"

# 온톨로지 연결
entities:
  - shakyamuni-buddha
  - gandhara

# 출처·라이선스
source: "OL Project 자체 제작"
sourceUrl: ""
license: "CC BY-SA 4.0"

tags: [간다라, 불상, 초기대승, 조각]
published: true
---

간다라 지역의 헬레니즘 영향을 받은 불상 양식입니다.
그리스 조각의 사실적 표현과 인도 불교 도상학이 결합된 초기 불상 형식.
```

### BOOK과의 비교

```
BOOK:
  src/content/book/buddha-story/buddha-story.md  
  -   htmlPath: "buddha-story"   

  public/books/buddha-story/index.html


DESIGN:
  src/content/design/gandhara-face.md  
  -   imagePath: "gandhara-face.jpg"

  public/design/gandhara-face.jpg

```

구조가 동일합니다. md에 경로를 적고, 실제 파일은 `public/`에 둡니다.

### DESIGN 페이지에서 렌더링

```astro
<!-- design/index.astro 에서 -->
<img
  src={url(`/design/${item.data.imagePath}`)}
  alt={item.data.imageAlt}
  loading="lazy"
/>
```

---

## 장기적 이미지 관리 전략

이미지가 많아지면 GitHub 저장소가 무거워지는 문제에 대한 단계별 대응:

```
Phase 현재 (이미지 ~50장):
  → public/design/ 에 직접 저장. 문제없음.

Phase 중기 (이미지 ~200장):
  → 이미지 WebP 변환 + 리사이징으로 용량 관리
  → Astro의 astro:assets 이미지 최적화 활용

Phase 장기 (이미지 500장+):
  → 이미지를 별도 저장소(OL-ASSETS)로 분리
  → 또는 Cloudflare R2 / Cloudinary 같은 이미지 CDN 도입
  → md의 imagePath를 외부 URL로 변경
```

지금은 첫 번째 단계이므로 `public/design/`에 직접 저장하는 것이 가장 단순하고 적합합니다. 나중에 이미지가 많아지면 `imagePath` 필드를 외부 URL로 바꾸기만 하면 됩니다. md 구조를 바꿀 필요 없이 경로만 변경하면 되는 것이 이 설계의 장점입니다.

---

## 요약

| 항목          | 결론                                                |
| ----------- | ------------------------------------------------- |
| BOOK 패턴 차용? | 예, 변형 채택 (md 메타 + public 파일 분리)                   |
| 폴더 구조       | `src/content/design/*.md` + `public/design/*.jpg` |
| GitHub 용량   | 이미지 수백 장까지 문제없음, 1GB 넘으면 분리 고려                    |
| 이미지 최적화     | 현재는 불필요, 200장 넘으면 WebP 변환 권장                      |

---

## 구현

  1. src/content.config.ts — 스키마 업데이트
  - image → imagePath (문서 권장 명칭으로 통일)
  - imageAlt 필드 추가 (접근성 및 설명용) 
  - sourceUrl 필드 추가 (출처 링크)

  2. public/design/ 폴더 생성
  - 이미지 파일 실제 저장 위치. md 파일의 imagePath에 파일명만 적으면 이 폴더에서 읽어옴

  3. design/index.astro — 컬렉션 연결
  - getCollection('design')으로 실제 데이터 렌더링
  - imagePath 있으면 <img> 표시, 없으면 .ol-ph 플레이스홀더
  - 등록 자료 없을 때 빈 상태 메시지

  4. design/[slug].astro — 상세 페이지 이미지 표시
  - imagePath가 있으면 <figure> + <img> 렌더링
  - source + sourceUrl + license 조합으로 캡션 자동 생성

  앞으로 이미지를 등록할 때는:
  1. 이미지 파일 → public/design/파일명.jpg
  2. 메타데이터 → src/content/design/slug.md 작성 (imagePath, imageAlt 등 포함)
