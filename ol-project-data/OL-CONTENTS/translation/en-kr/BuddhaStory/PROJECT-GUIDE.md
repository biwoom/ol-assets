# 📖 마하붓다왐사 번역 프로젝트 전용 스타일 가이드 (PROJECT-GUIDE)
(Mahā Buddhavaṃsa Translation - Project-Specific Guidelines)

본 문서는 UBTF(통합 불교 문헌 번역 프레임워크) 상에서 **마하붓다왐사(Mahā Buddhavaṃsa, 위대한 부처님들의 연대기) 번역 프로젝트**를 수행하는 에이전트와 감수자를 위한 전용 스타일 가이드라인입니다.

---

## 1. 차수별 대상 독자층 및 서식 기준

마하붓다왐사 번역 프로젝트는 각 번역 차수마다 독자 지향점을 명확히 분리하여 수행합니다.

### 1.1 [1차 번역] 학술적 초안 (`draft-1`)
* **독자층**: **불교전문연구자 및 교학 전문가 그룹**
* **지향점**: 번역어투를 지양하고 자연스러운 한국어 표현을 사용하되, 불교전문용어(Pali/Sanskrit 전사 표기 및 한역 교학 용어)를 적극 활용하여 교리적 구분을 명확히 하는 **엄밀하고 학술적인 번역**입니다.
* **헤더 번역 규칙**: 본문의 모든 제목 헤더(h1~h5)를 번역하며, 타이틀 헤더는 프로젝트 목차 대조 파일인 `gcb-kr-TOC.md`를 엄격히 준수하여 번역합니다.

### 1.2 [2단계] 대중적 윤문 (`draft-2`)
* **독자층**: **고등학교 수준 이상의 평범한 대한민국 일반 대중**
* **지향점**: 1차 번역의 어려운 불교전문용어를 최대한 배제하고, 쉬운 일상어로 대체하거나 풀어서 설명하는 **가독성 극대화 윤문**입니다.
* **어조 조율**: 영어식 피동 표현이나 무겁고 딱딱한 교학적 문체를 제거하고, 소설이나 문학 작품처럼 자연스럽고 유려한 현대 구어/문어체 흐름으로 리라이팅합니다.

---

## 2. 프로젝트 전용 태그 및 앨리어스 예시

마하붓다왐사 문헌의 색인 및 검색 최적화를 위해 YAML Frontmatter 작성 시 다음 접두사 태그 규격을 정독하여 적용합니다.

* **인물**: `"인물/수메다-고행자"`, `"인물/디빵까라-부처님"`, `"인물/아나타삔디까"`
* **장소**: `"장소/아마라와띠-도시"`, `"장소/라자가하-왕사성"`, `"장소/제따와나-사원"`
* **주제**: `"주제/수기"`, `"주제/에히빅쿠"`, `"주제/보살"`
* **경전**: `"경전/붓다왐사"`
* **유형**: `"유형/연대기"`
* **시기**: `"시기/헤아릴-수-없는-과거겁"`

### 2.1 tagAliases 매핑 리스트 구성 예시
* 고유명사의 이칭과 빨리어 원형(diacritics 유지)을 매핑합니다.
```yaml
tagAliases:
  "인물/디빵까라-부처님": ["Dīpaṅkara", "Dīpaṅkara Buddha", "연등불", "燃燈佛"]
  "인물/아나타삔디까": ["Anāthapiṇḍika", "Sudatta", "급고독장자", "수다따"]
  "장소/라자가하-왕사성": ["Rājagaha", "왕사성"]
  "주제/보살": ["Bodhisatta", "미래의 부처님"]
```

---

## 3. 실제 파일 번역 작성 예시 (Chapter 1)

에이전트는 원고 파일을 가공할 때 본문 구조를 다음과 같이 1:1 영어-한국어 대칭 구조로 빌드해야 합니다.

```markdown
---
tags:
  - "인물/수메다-고행자"
  - "인물/디빵까라-부처님"
  - "장소/아마라와띠-도시"
---

# Chapter 1 - Salutation & Intention

[KO]
# 1장: 부처님께 올리는 예경과 이 책을 쓰는 뜻
[/KO]

## 본문

The author, Bhaddanta Vicittasārābhivaṃsa, Mingun Tipiṭakadhara Sayadaw, as he is popularly known, was born in the village of Thaibyuwa on November 11, 1911. At the age of eight he was sent to Sayadaw U Sobhita of Min-gyaung Monastery, Myingyan, to start learning the rudiments of Buddhism.

[KO]
저자인 바단따 비찟따사라비왐사(Bhaddanta Vicittasārābhivaṃsa), 곧 대중에게 밍군 티피타카다라 사야도(Mingun Tipiṭakadhara Sayadaw)로 널리 알려진 그는 1911년 11월 11일 타이뷰와(Thaibyuwa) 마을에서 태어났다. 그는 여덟 살 때 불교의 기초를 배우기 위해 밍얀(Myingyan)의 민짜웅(Min-gyaung) 사원에 있던 우 소비따 사야도(Sayadaw U Sobhita)에게 보내졌다.
[/KO]

When he was ten he was ordained a sāmaṇera by the same Sayadaw. Ten years later he went to Dhammanāda Monastery, a secluded place of holy personages, in Mingun, Sagaing Township, for further learning. In 1930, he received higher ordination.

[KO]
그는 열 살이 되었을 때 같은 사야도를 은사로 하여 사미(sāmaṇera)가 되었다. 10년 뒤에는 더 깊이 배우기 위해 사가잉(Sagaing) 지역 밍군(Mingun)에 있는, 성스러운 이들이 머무는 은둔처인 담마나다(Dhammanāda) 사원으로 갔다. 1930년에는 구족계를 받았다.
[/KO]
```
