# OL HOME 구축과 데이터 설계 - Phase 1 작업지시서 v2
## Astro + Basecoat + Ontology-aware Content Architecture

> **문서 버전**: v2.0 (온톨로지 기반 지식그래프 설계 통합)
> **이전 버전 대비 추가**: 섹션 A (설계 철학), 섹션 B (Content 구조 설계), 섹션 C (Ontology 스키마)
> **대상**: Astro 초보자 + Claude Code · Cursor Agent 등 로컬 AI 에이전트

---

## 이 문서를 읽기 전에 — 설계 결정의 이유

v1 지시서는 "어떻게 만드는가"를 다뤘다면,  
v2는 그 전에 **"왜 이렇게 설계하는가"** 를 먼저 정립합니다.

OL은 단순 홈페이지가 아닙니다.

```
겉모습: 조용한 불교 콘텐츠 웹사이트
내부 구조: Ontology-aware Buddhist Knowledge System
장기 목표: 불교 콘텐츠 연기망 (Dependent Origination Network)
```

이 목표를 처음부터 구조에 반영하지 않으면,  
콘텐츠가 쌓일수록 나중에 고치기가 매우 어려워집니다.  
**스키마 설계는 콘텐츠보다 먼저여야 합니다.**

---

# 섹션 A. 설계 철학 — 왜 지식그래프인가

## A-1. 태그 시스템의 한계

대부분의 콘텐츠 시스템은 태그로 관계를 표현합니다.

```yaml
# 일반적인 태그 방식
tags: [용수, 중관학, 공성]
```

이 방식의 문제는 **관계의 의미가 없다**는 것입니다.  
용수가 중관학을 *창시했는지*, *비판했는지*, *단순 언급인지* 알 수 없습니다.

OL이 지향하는 방식:

```yaml
# OL Ontology 방식
relations:
  - subject: nagarjuna
    predicate: founded
    object: madhyamaka-school
  - subject: nagarjuna
    predicate: authored
    object: mulamadhyamakakarika
```

주어-관계-목적어 **(Triple 구조)**가 의미를 보존합니다.  
이것이 지식그래프의 핵심 단위입니다.

## A-2. OL의 세 층위

```
┌─────────────────────────────────────────┐
│  EXPERIENCE LAYER  (독자가 경험하는 것)    │
│  조용한 독서 · 탐색 · 깊은 체류             │
├─────────────────────────────────────────┤
│  CONTENT LAYER     (문서들)              │
│  book · blog · design · ai              │
├─────────────────────────────────────────┤
│  SEMANTIC LAYER    (의미망)              │
│  entities · relations · ontology        │
└─────────────────────────────────────────┘
```

독자는 Semantic Layer를 보지 않습니다.  
하지만 이 층이 없으면 "연기망"은 불가능합니다.  
경험은 단순해야 하고, 구조는 깊어야 합니다.

## A-3. 불교 철학과의 연결

연기법(緣起法): 모든 것은 조건에 의해 발생하고 상호 연결되어 있다.

```
붓다 ←──── 가르쳤다 ───→ 사성제
사성제 ←── 포함한다 ───→ 팔정도
팔정도 ←── 포함한다 ───→ 정견
정견 ←──── 근거한다 ───→ 연기법
연기법 ←── 설명한다 ───→ 공성
공성 ←──── 발전시켰다 ── 용수
용수 ←──── 저술했다 ───→ 중론
```

이것이 OL이 만들려는 **불교 콘텐츠 연기망**의 모습입니다.

## A-4. 중요한 경고 — 과잉 설계 금지

이 문서가 제안하는 온톨로지 구조는 **점진적으로** 채워가는 것입니다.

```
Phase 1: 구조만 설계, 데이터는 비어있어도 됨
Phase 2-3: 핵심 entity 파일 작성 시작
Phase 4+: relation 연결 확장
장기: semantic search, graph visualization 추가
```

처음부터 수백 개의 entity를 만들려 하지 마세요.  
**구조가 올바르면 데이터는 천천히 채울 수 있습니다.**

---

# 섹션 B. Content 구조 설계 — 전체 아키텍처

## B-1. 권장 디렉토리 구조 (전체)

```
OL-HOME/
│
├── src/
│   │
│   ├── content/                    ← Astro Content Collections
│   │   ├── config.ts               ← 스키마 정의 (핵심!)
│   │   │
│   │   ├── blog/                   ← 개발 기록, 소식
│   │   │   └── *.md
│   │   │
│   │   ├── book/                   ← 불교 콘텐츠 본문
│   │   │   ├── buddha-story/
│   │   │   │   └── *.md
│   │   │   └── dhammapada/
│   │   │       └── *.md
│   │   │
│   │   ├── design/                 ← 시각 레퍼런스 아카이브
│   │   │   └── *.md
│   │   │
│   │   ├── ai/                     ← AI 실험 기록 (장래)
│   │   │   └── *.md
│   │   │
│   │   ├── entities/               ← ★ 온톨로지 핵심 노드
│   │   │   ├── persons/            ← 인물 (붓다, 용수, 아난 등)
│   │   │   │   └── *.md
│   │   │   ├── places/             ← 장소 (룸비니, 기원정사 등)
│   │   │   │   └── *.md
│   │   │   ├── concepts/           ← 개념 (공성, 연기, 팔정도 등)
│   │   │   │   └── *.md
│   │   │   ├── texts/              ← 문헌 (중론, 담마빠다 등)
│   │   │   │   └── *.md
│   │   │   ├── events/             ← 사건 (성도, 초전법륜 등)
│   │   │   │   └── *.md
│   │   │   ├── practices/          ← 수행 (선정, 위빠사나 등)
│   │   │   │   └── *.md
│   │   │   └── schools/            ← 학파 (중관, 유식, 선종 등)
│   │   │       └── *.md
│   │   │
│   │   └── ontology/               ← ★ 온톨로지 스키마 정의
│   │       ├── entity-types.md     ← entity 유형 목록
│   │       ├── relation-types.md   ← 관계 유형 목록
│   │       └── namespaces.md       ← ID 네이밍 규칙
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── OLHeader.astro
│   │   │   └── OLFooter.astro
│   │   ├── ui/
│   │   │   ├── OLBadge.astro
│   │   │   └── OLButton.astro
│   │   ├── home/
│   │   │   ├── OLHero.astro
│   │   │   ├── OLProductCards.astro
│   │   │   ├── OLManifest.astro
│   │   │   ├── OLStats.astro
│   │   │   └── OLLatestUpdates.astro
│   │   ├── book/
│   │   │   ├── OLBookCard.astro
│   │   │   └── OLBookReader.astro
│   │   ├── entity/                 ← ★ 엔티티 렌더링 컴포넌트
│   │   │   ├── OLEntityCard.astro
│   │   │   ├── OLEntityPanel.astro ← 사이드바 관련 정보
│   │   │   └── OLRelationLinks.astro ← 관계 링크 목록
│   │   └── graph/                  ← ★ 지식그래프 (장래)
│   │       └── OLGraphView.astro   ← Phase 4+ 에서 구현
│   │
│   ├── layouts/
│   │   ├── BaseLayout.astro
│   │   ├── PageLayout.astro
│   │   ├── BookLayout.astro        ← 장문 읽기 최적화
│   │   └── EntityLayout.astro      ← entity 페이지 전용
│   │
│   ├── pages/
│   │   ├── index.astro
│   │   ├── atlas.astro
│   │   ├── book/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   ├── design/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   ├── blog/
│   │   │   ├── index.astro
│   │   │   └── [slug].astro
│   │   ├── ai.astro
│   │   └── entity/                 ← ★ 자동 생성 entity 페이지
│   │       ├── [type]/
│   │       │   └── [id].astro      ← /entity/persons/nagarjuna
│   │       └── index.astro         ← 전체 entity 목록
│   │
│   ├── lib/
│   │   ├── graph.ts                ← ★ 지식그래프 빌드 유틸
│   │   ├── search.ts               ← 검색 인덱스 생성
│   │   └── relations.ts            ← 관계 데이터 처리
│   │
│   ├── styles/
│   │   ├── global.css
│   │   ├── tokens.css
│   │   └── ol-components.css
│   │
│   └── data/
│       └── nav.ts
│
├── public/
│   ├── images/
│   ├── icons/
│   └── books/                      ← ATLAS HTML 파일 저장
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── astro.config.mjs
├── package.json
└── tsconfig.json
```

## B-2. 두 가지 핵심 원칙

### 원칙 1: Document ≠ Entity 분리

이것이 v1과 v2의 가장 큰 차이입니다.

```
❌ 잘못된 방식 (태그 기반)
book/buddha-birth.md
  tags: [붓다, 룸비니, 마야부인]
  → 관계 없음, 검색만 가능

✅ OL 방식 (entity 분리)
book/buddha-birth.md          ← 문서 (이야기, 설명)
  entities: [siddhartha, maya, lumbini]
  relations:
    - maya gave_birth_to siddhartha
    - siddhartha born_in lumbini

entities/persons/siddhartha.md  ← entity 노드
entities/persons/maya.md
entities/places/lumbini.md
```

문서는 이야기를 담고, entity는 개념을 담습니다.  
같은 entity가 수백 개의 문서에 등장해도 하나의 파일로 관리됩니다.

### 원칙 2: 점진적 정밀화 (Progressive Enrichment)

```
Phase 1: entity 파일 존재만 해도 됨 (내용 비어도 OK)
Phase 2: 기본 속성 채우기
Phase 3: relations 연결
Phase 4: 역방향 링크(backlinks) 자동 생성
Phase 5: 시각화, 의미 검색
```

처음부터 완벽할 필요 없습니다.  
구조가 올바르면 내용은 나중에 채울 수 있습니다.

---

# 섹션 C. Ontology 스키마 설계

## C-1. Entity Type 정의

OL 불교 온톨로지의 7가지 기본 entity 유형입니다.

| 유형 | 영문 ID | 예시 | 설명 |
|------|---------|------|------|
| 인물 | `person` | 붓다, 용수, 아난 | 역사적 인물, 신화적 존재 포함 |
| 장소 | `place` | 룸비니, 기원정사, 보드가야 | 지리적 위치, 가상 장소 포함 |
| 개념 | `concept` | 공성, 연기, 무아 | 교리적 개념, 철학 용어 |
| 문헌 | `text` | 중론, 담마빠다, 반야경 | 경전, 논서, 주석서 |
| 사건 | `event` | 성도, 초전법륜, 열반 | 역사적/서사적 사건 |
| 수행 | `practice` | 선정, 위빠사나, 사념처 | 수행 방법, 의례 |
| 학파 | `school` | 중관학, 유식학, 선종 | 불교 전통, 철학 학파 |

## C-2. Relation Type 정의

OL 온톨로지의 핵심 관계 유형입니다. 단방향(→)으로 정의합니다.

### 인물 관련 관계
```
person → text       : authored (저술했다)
person → concept    : developed (발전시켰다), taught (가르쳤다)
person → person     : student_of (제자이다), teacher_of (스승이다)
person → place      : born_in (태어났다), lived_in (머물렀다), died_in (입적했다)
person → school     : founded (창시했다), belonged_to (속했다)
person → event      : participated_in (참여했다), experienced (경험했다)
```

### 문헌 관련 관계
```
text → concept      : explains (설명한다), discusses (논한다)
text → text         : commentary_on (주석이다), quotes (인용한다), responds_to (반론한다)
text → person       : mentions (언급한다)
text → school       : represents (대표한다)
```

### 개념 관련 관계
```
concept → concept   : related_to (관련된다), includes (포함한다),
                      contrasts_with (대비된다), derived_from (유래한다)
concept → practice  : realized_through (실현된다)
concept → school    : central_to (핵심이다)
```

### 학파/전통 관련 관계
```
school → school     : emerged_from (파생됐다), influenced (영향줬다)
school → text       : canonical_text (소의경전이다)
school → place      : originated_in (발원했다)
```

## C-3. ID 네이밍 규칙

일관된 ID 체계가 없으면 나중에 링크가 깨집니다.

```
규칙:
- 소문자 영문 + 하이픈
- 팔리어/산스크리트어 우선, 한국어 병기
- 약어나 별칭 사용 금지 (정식 명칭 사용)

예시:
✅ siddhartha-gautama     (붓다의 개인 이름)
✅ shakyamuni-buddha      (석가모니불)
✅ nagarjuna              (용수)
✅ mulamadhyamakakarika   (중론)
✅ sunyata                (공성)
✅ lumbini                (룸비니)
✅ jetavana-monastery     (기원정사)

❌ buddha (너무 일반적)
❌ 나가르주나 (한국어 ID)
❌ mmk (약어)
```

## C-4. Content Collections 스키마 (`src/content/config.ts`)

```typescript
import { defineCollection, z } from 'astro:content';

// ─── 공통 relation 스키마 ───────────────────────────────
const RelationSchema = z.object({
  subject: z.string(),    // entity ID
  predicate: z.string(),  // relation type
  object: z.string(),     // entity ID 또는 자유 텍스트
  source: z.string().optional(),  // 출처 문헌 ID
  note: z.string().optional(),    // 부연 설명
});

// ─── Entity 공통 스키마 ────────────────────────────────
const EntityBaseSchema = z.object({
  id: z.string(),                           // 고유 ID (파일명과 일치)
  type: z.enum([
    'person', 'place', 'concept',
    'text', 'event', 'practice', 'school'
  ]),
  name: z.object({
    ko: z.string(),                         // 한국어 이름 (필수)
    en: z.string().optional(),              // 영문
    pali: z.string().optional(),            // 팔리어
    sanskrit: z.string().optional(),        // 산스크리트어
    chinese: z.string().optional(),         // 한자
  }),
  aliases: z.array(z.string()).default([]), // 별칭, 다른 표기
  description: z.string().optional(),       // 한 줄 설명
  relations: z.array(RelationSchema).default([]),
  tags: z.array(z.string()).default([]),
  sources: z.array(z.string()).default([]), // 참고 문헌 ID
  published: z.boolean().default(true),
});

// ─── Entity 유형별 확장 스키마 ─────────────────────────

const PersonSchema = EntityBaseSchema.extend({
  type: z.literal('person'),
  era: z.object({
    born: z.string().optional(),   // "BC 563" 형식
    died: z.string().optional(),   // "BC 483" 형식
    active: z.string().optional(), // "BC 5세기" 형식 (불확실할 때)
  }).optional(),
  tradition: z.string().optional(), // 소속 전통
  nationality: z.string().optional(),
});

const PlaceSchema = EntityBaseSchema.extend({
  type: z.literal('place'),
  location: z.object({
    country: z.string().optional(),   // 현재 국가
    region: z.string().optional(),    // 지역
    lat: z.number().optional(),       // 위도 (지도 연동 장래)
    lng: z.number().optional(),       // 경도
  }).optional(),
  era: z.string().optional(),         // "붓다 시대", "현존" 등
});

const ConceptSchema = EntityBaseSchema.extend({
  type: z.literal('concept'),
  tradition: z.string().optional(),   // "초기불교", "대승" 등
  complexity: z.enum(['introductory', 'intermediate', 'advanced']).optional(),
});

const TextSchema = EntityBaseSchema.extend({
  type: z.literal('text'),
  author: z.string().optional(),      // entity ID
  tradition: z.string().optional(),
  language: z.object({
    original: z.string().optional(),  // "pali", "sanskrit", "chinese"
    translations: z.array(z.string()).default([]),
  }).optional(),
  era: z.string().optional(),
});

const EventSchema = EntityBaseSchema.extend({
  type: z.literal('event'),
  date: z.string().optional(),        // "BC 528" 또는 "BC 5세기"
  location: z.string().optional(),    // place entity ID
  participants: z.array(z.string()).default([]), // person entity IDs
});

const PracticeSchema = EntityBaseSchema.extend({
  type: z.literal('practice'),
  tradition: z.string().optional(),
  level: z.string().optional(),       // 수행 단계
});

const SchoolSchema = EntityBaseSchema.extend({
  type: z.literal('school'),
  tradition: z.string().optional(),   // "초기불교", "대승", "밀교" 등
  founded: z.string().optional(),     // person entity ID
  era: z.string().optional(),
  region: z.string().optional(),
});

// ─── Content Collections ───────────────────────────────

// 블로그
const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    excerpt: z.string().optional(),
    category: z.enum(['ATLAS', 'BOOK', 'DESIGN', 'AI', 'META']).optional(),
    // 온톨로지 연결 (블로그도 entity 참조 가능)
    entities: z.array(z.string()).default([]),
    published: z.boolean().default(false),
  }),
});

// 불교 콘텐츠 BOOK
const bookCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    series: z.string().optional(),         // "buddha-story", "dhammapada"
    chapter: z.number().optional(),
    order: z.number().default(0),          // 시리즈 내 순서
    date: z.coerce.date().optional(),

    // ★ 온톨로지 연결 (핵심)
    entities: z.array(z.string()).default([]),    // 등장 entity ID 목록
    relations: z.array(RelationSchema).default([]), // 이 문서의 triple
    primary_entity: z.string().optional(),          // 주인공 entity

    // 출처
    sources: z.array(z.object({
      text: z.string(),         // 경전/문헌명
      ref: z.string().optional(), // entity ID
      passage: z.string().optional(),
    })).default([]),

    tags: z.array(z.string()).default([]),
    published: z.boolean().default(false),
    excerpt: z.string().optional(),
  }),
});

// 디자인 레퍼런스
const designCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    type: z.enum([
      'costume', 'architecture', 'portrait',
      'artifact', 'landscape', 'manuscript', 'other'
    ]),
    era: z.string().optional(),         // "통일신라", "고려 후기"
    region: z.string().optional(),      // "한국", "인도", "중국"
    tradition: z.string().optional(),   // "선종", "밀교"

    // ★ 온톨로지 연결
    entities: z.array(z.string()).default([]),   // 관련 entity ID

    // 자산 정보
    image: z.string().optional(),       // 이미지 경로
    source: z.string().optional(),      // 원본 출처
    license: z.string().default('CC0'),

    tags: z.array(z.string()).default([]),
    published: z.boolean().default(false),
  }),
});

// AI 실험 기록
const aiCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    type: z.enum(['experiment', 'workflow', 'prompt', 'result', 'reflection']),
    tags: z.array(z.string()).default([]),
    published: z.boolean().default(false),
  }),
});

// ★ Entity Collection — 7가지 유형 통합
// 실제로는 유형별로 별도 파일을 두거나 union 스키마 사용
const entitiesCollection = defineCollection({
  type: 'content',
  schema: z.discriminatedUnion('type', [
    PersonSchema,
    PlaceSchema,
    ConceptSchema,
    TextSchema,
    EventSchema,
    PracticeSchema,
    SchoolSchema,
  ]),
});

// ★ Ontology — 스키마 정의 문서 (메타)
const ontologyCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    version: z.string().default('0.1'),
    date: z.coerce.date().optional(),
  }),
});

export const collections = {
  blog: blogCollection,
  book: bookCollection,
  design: designCollection,
  ai: aiCollection,
  entities: entitiesCollection,
  ontology: ontologyCollection,
};
```

---

# 섹션 D. Entity 파일 예시 — 실제 작성법

## D-1. 인물 entity 예시

`src/content/entities/persons/nagarjuna.md`

```markdown
---
id: nagarjuna
type: person
name:
  ko: 용수
  en: Nagarjuna
  sanskrit: Nāgārjuna
  chinese: 龍樹
aliases:
  - 나가르주나
  - 용수보살
description: 대승불교 중관학파의 창시자. 공성(空性) 철학을 체계화했다.
era:
  active: "AD 2~3세기"
tradition: 대승불교
relations:
  - subject: nagarjuna
    predicate: authored
    object: mulamadhyamakakarika
  - subject: nagarjuna
    predicate: authored
    object: vigrahavyavartani
  - subject: nagarjuna
    predicate: founded
    object: madhyamaka-school
  - subject: nagarjuna
    predicate: developed
    object: sunyata
tags: [대승, 중관, 공성, 논사]
sources: [mulamadhyamakakarika]
published: true
---

용수(龍樹, Nāgārjuna)는 인도 대승불교의 위대한 논사로,
2~3세기경 활동한 것으로 추정됩니다.

중관학(中觀學, Madhyamaka)을 창시하여 공성(空性, Śūnyatā)을
체계적으로 철학화했으며, 이후 동아시아 불교와 티베트 불교 전반에
깊은 영향을 미쳤습니다.
```

## D-2. 개념 entity 예시

`src/content/entities/concepts/sunyata.md`

```markdown
---
id: sunyata
type: concept
name:
  ko: 공성
  en: Emptiness
  sanskrit: Śūnyatā
  pali: Suññatā
  chinese: 空性
aliases:
  - 공(空)
  - 공(空性)
description: 모든 현상은 고정된 자성(自性)이 없다는 대승불교의 핵심 교리.
tradition: 대승불교
complexity: advanced
relations:
  - subject: sunyata
    predicate: derived_from
    object: dependent-origination
  - subject: sunyata
    predicate: central_to
    object: madhyamaka-school
  - subject: sunyata
    predicate: related_to
    object: anatman
tags: [공, 무아, 중관, 대승]
sources: [mulamadhyamakakarika, heart-sutra]
published: true
---

공성(空性, Śūnyatā)은 모든 존재와 현상에 고정된 자성(自性, svabhāva)이
없다는 대승불교의 핵심 철학입니다.
```

## D-3. Book 문서 예시 (entity 연결 포함)

`src/content/book/buddha-story/01-birth.md`

```markdown
---
title: 룸비니의 탄생
series: buddha-story
chapter: 1
order: 1

# ★ 온톨로지 연결
entities:
  - siddhartha-gautama
  - maya-devi
  - lumbini
  - kapilavastu

relations:
  - subject: maya-devi
    predicate: gave_birth_to
    object: siddhartha-gautama
    source: lalitavistara
  - subject: siddhartha-gautama
    predicate: born_in
    object: lumbini

primary_entity: siddhartha-gautama

sources:
  - text: 방광대장엄경
    ref: lalitavistara
    passage: "제3장 탁태품"
  - text: 팔리 율장 大品
    ref: pali-vinaya-mahavagga

tags: [붓다전기, 탄생, 룸비니]
published: true
excerpt: "마야부인이 룸비니 동산에서 아기 싯다르타를 낳다."
---

기원전 약 563년, 샤카족의 왕비 마야(Māyā)부인은
친정인 데바다하로 가던 도중 룸비니 동산에서 멈췄습니다.
```

---

# 섹션 E. lib/ — 지식그래프 빌드 유틸리티

## E-1. `src/lib/relations.ts` — 관계 데이터 처리

```typescript
import { getCollection } from 'astro:content';

export type Triple = {
  subject: string;
  predicate: string;
  object: string;
  source?: string;
  note?: string;
};

/**
 * 모든 collection에서 triple을 수집하여 지식그래프 데이터 반환
 * build 시에만 실행됨 (Astro SSG)
 */
export async function buildKnowledgeGraph() {
  const [books, entities, designs, blogs] = await Promise.all([
    getCollection('book'),
    getCollection('entities'),
    getCollection('design'),
    getCollection('blog'),
  ]);

  const triples: Triple[] = [];
  const entityMap = new Map<string, any>();

  // Entity 노드 수집
  for (const entity of entities) {
    entityMap.set(entity.data.id, entity);
    // entity 자체의 relations 수집
    for (const rel of entity.data.relations ?? []) {
      triples.push(rel);
    }
  }

  // Book 문서의 relations 수집
  for (const book of books) {
    for (const rel of book.data.relations ?? []) {
      triples.push({ ...rel, source: book.slug });
    }
  }

  return { triples, entityMap };
}

/**
 * 특정 entity의 모든 관계 반환 (양방향)
 */
export async function getEntityRelations(entityId: string) {
  const { triples } = await buildKnowledgeGraph();

  const asSubject = triples.filter(t => t.subject === entityId);
  const asObject  = triples.filter(t => t.object  === entityId);

  return { outgoing: asSubject, incoming: asObject };
}

/**
 * 특정 entity를 언급하는 모든 문서 반환 (backlinks)
 */
export async function getBacklinks(entityId: string) {
  const books   = await getCollection('book');
  const designs = await getCollection('design');
  const blogs   = await getCollection('blog');

  const allDocs = [...books, ...designs, ...blogs];

  return allDocs.filter(doc =>
    (doc.data.entities ?? []).includes(entityId)
  );
}
```

## E-2. `src/lib/search.ts` — 검색 인덱스

```typescript
import { getCollection } from 'astro:content';

/**
 * 전체 검색 인덱스 생성
 * pagefind 또는 fuse.js와 연동 가능
 */
export async function buildSearchIndex() {
  const [books, entities, designs, blogs] = await Promise.all([
    getCollection('book', e => e.data.published),
    getCollection('entities', e => e.data.published),
    getCollection('design', e => e.data.published),
    getCollection('blog', e => e.data.published),
  ]);

  return [
    ...books.map(doc => ({
      type: 'book' as const,
      id: doc.slug,
      title: doc.data.title,
      excerpt: doc.data.excerpt ?? '',
      entities: doc.data.entities ?? [],
      tags: doc.data.tags ?? [],
      url: `/book/${doc.slug}`,
    })),
    ...entities.map(doc => ({
      type: 'entity' as const,
      id: doc.data.id,
      title: doc.data.name.ko,
      excerpt: doc.data.description ?? '',
      entities: [doc.data.id],
      tags: doc.data.tags ?? [],
      url: `/entity/${doc.data.type}s/${doc.data.id}`,
    })),
    ...designs.map(doc => ({
      type: 'design' as const,
      id: doc.slug,
      title: doc.data.title,
      excerpt: '',
      entities: doc.data.entities ?? [],
      tags: doc.data.tags ?? [],
      url: `/design/${doc.slug}`,
    })),
    ...blogs.map(doc => ({
      type: 'blog' as const,
      id: doc.slug,
      title: doc.data.title,
      excerpt: doc.data.excerpt ?? '',
      entities: doc.data.entities ?? [],
      tags: doc.data.tags ?? [],
      url: `/blog/${doc.slug}`,
    })),
  ];
}
```

---

# 섹션 F. Entity 페이지 자동 생성

## F-1. `src/pages/entity/[type]/[id].astro`

```astro
---
import { getCollection } from 'astro:content';
import { getEntityRelations, getBacklinks } from '../../../lib/relations';
import EntityLayout from '../../../layouts/EntityLayout.astro';
import OLRelationLinks from '../../../components/entity/OLRelationLinks.astro';
import OLEntityPanel from '../../../components/entity/OLEntityPanel.astro';

export async function getStaticPaths() {
  const entities = await getCollection('entities', e => e.data.published);

  return entities.map(entity => ({
    params: {
      type: entity.data.type + 's',   // persons, places, concepts ...
      id: entity.data.id,
    },
    props: { entity },
  }));
}

const { entity } = Astro.props;
const { Content } = await entity.render();

// 관계 데이터와 역방향 링크 수집
const { outgoing, incoming } = await getEntityRelations(entity.data.id);
const backlinks = await getBacklinks(entity.data.id);
---

<EntityLayout
  title={`${entity.data.name.ko} — OL`}
  description={entity.data.description}
>
  <article>
    <!-- 이름과 기본 정보 -->
    <header class="ol-entity-header">
      <span class="ol-mono-label">{entity.data.type}</span>
      <h1>{entity.data.name.ko}</h1>
      {entity.data.name.sanskrit && (
        <p class="ol-entity-names">
          {entity.data.name.sanskrit}
          {entity.data.name.pali && ` · ${entity.data.name.pali}`}
          {entity.data.name.chinese && ` · ${entity.data.name.chinese}`}
        </p>
      )}
    </header>

    <!-- 본문 -->
    <div class="ol-prose">
      <Content />
    </div>

    <!-- 관계 링크 -->
    {outgoing.length > 0 && (
      <OLRelationLinks
        title="이 항목에서 연결된 것들"
        relations={outgoing}
        direction="outgoing"
      />
    )}

    {incoming.length > 0 && (
      <OLRelationLinks
        title="이 항목으로 연결된 것들"
        relations={incoming}
        direction="incoming"
      />
    )}

    <!-- 역방향 링크 (등장 문서) -->
    {backlinks.length > 0 && (
      <section class="ol-backlinks">
        <h2 class="ol-mono-label">등장하는 문서 ({backlinks.length})</h2>
        <ul>
          {backlinks.map(doc => (
            <li>
              <a href={`/${doc.collection}/${doc.slug}`}>
                {doc.data.title}
              </a>
            </li>
          ))}
        </ul>
      </section>
    )}
  </article>
</EntityLayout>
```

이렇게 하면 `nagarjuna.md` 파일 하나로  
`/entity/persons/nagarjuna` 페이지가 **자동 생성**됩니다.

---

# 섹션 G. 온톨로지 정의 파일 예시

## G-1. `src/content/ontology/entity-types.md`

```markdown
---
title: OL 온톨로지 — Entity 유형 정의
version: "0.1"
date: 2026-05-27
---

# OL Buddhist Ontology — Entity Types v0.1

이 문서는 OL 프로젝트에서 사용하는 entity 유형을 정의합니다.
새 entity 파일을 만들기 전에 반드시 이 문서를 참고하세요.

## 유형 목록

| type | 한국어 | 설명 | 예시 |
|------|--------|------|------|
| person | 인물 | 역사적·신화적 인물 | 붓다, 용수, 아난 |
| place | 장소 | 지리적·상징적 장소 | 룸비니, 기원정사 |
| concept | 개념 | 교리적 개념, 철학 용어 | 공성, 연기, 팔정도 |
| text | 문헌 | 경전, 논서, 주석서 | 중론, 담마빠다 |
| event | 사건 | 역사적·서사적 사건 | 성도, 초전법륜 |
| practice | 수행 | 수행 방법, 의례 | 선정, 위빠사나 |
| school | 학파 | 불교 전통, 철학 학파 | 중관학, 선종 |
```

## G-2. `src/content/ontology/relation-types.md`

```markdown
---
title: OL 온톨로지 — Relation 유형 정의
version: "0.1"
date: 2026-05-27
---

# OL Buddhist Ontology — Relation Types v0.1

## 관계 유형 목록

| predicate | 한국어 | 주어 유형 | 목적어 유형 |
|-----------|--------|-----------|-------------|
| authored | 저술했다 | person | text |
| taught | 가르쳤다 | person | concept, practice |
| developed | 발전시켰다 | person | concept, school |
| founded | 창시했다 | person | school |
| student_of | 제자이다 | person | person |
| teacher_of | 스승이다 | person | person |
| born_in | 태어났다 | person | place |
| lived_in | 머물렀다 | person | place |
| died_in | 입적했다 | person | place |
| explains | 설명한다 | text | concept |
| commentary_on | 주석이다 | text | text |
| mentions | 언급한다 | text | person, place, concept |
| related_to | 관련된다 | concept | concept |
| includes | 포함한다 | concept | concept |
| derived_from | 유래한다 | concept | concept |
| central_to | 핵심이다 | concept | school |
| realized_through | 실현된다 | concept | practice |
| emerged_from | 파생됐다 | school | school |
| influenced | 영향줬다 | school, person | school, person |
| canonical_text | 소의경전이다 | school | text |
| participated_in | 참여했다 | person | event |
| gave_birth_to | 낳았다 | person | person |
```

---

# 섹션 H. Phase 로드맵 — 지식그래프 관점

```
Phase 1 (현재)
├── 폴더 구조 생성 ✓
├── config.ts 스키마 정의 ✓
├── 홈페이지 6개 페이지 라우팅 ✓
├── entity 폴더 생성 (빈 파일 몇 개로 시작) ✓
├── ontology 정의 파일 작성 ✓
└── lib/relations.ts, lib/search.ts 작성 ✓

Phase 2 (콘텐츠 구조화)
├── 핵심 entity 10~20개 작성 (붓다, 용수, 공성, 연기 등)
├── 첫 번째 BOOK 시리즈 (buddha-story) entity 연결
├── BLOG 포스트 작성 시작
├── entity 페이지 자동 생성 동작 확인
└── 기본 backlinks 표시

Phase 3 (OL BOOK 라이브러리)
├── BOOK 개별 페이지 (deep reading layout)
├── Entity 사이드 패널 (읽는 중 관련 정보 표시)
├── 챕터 네비게이션
└── 출처/주석 표시 시스템

Phase 4 (검색 + 탐색)
├── Pagefind 전문 검색 통합
├── Entity 기반 필터 검색
├── 태그 클라우드 / 인물 색인
└── "관련 문서" 추천 (entity 교집합 기반)

Phase 5 (지식그래프 시각화)
├── OLGraphView — D3.js 기반 경량 그래프
├── 인물 계보도
├── 사상 발전 흐름도
└── 조용한 인터페이스 유지 (과시적 시각화 금지)

Phase 6 (의미 검색)
├── "용수와 관련된 모든 개념" 쿼리
├── "초기불교 수행 문헌" 탐색
└── GraphRAG 연동 (OL AI 전 단계)
```

---

# 섹션 I. 전문가 검토 — 개선 제안

기존 대화에서 제안된 구조를 분석한 후 추가 개선점입니다.

## I-1. 잠재적 문제: discriminatedUnion의 복잡성

`z.discriminatedUnion`은 스키마가 많아질수록 TypeScript 타입 추론이 느려집니다.  
**대안**: entity 유형별로 별도 collection 분리

```typescript
// 권장 대안 — 유형별 collection 분리
export const collections = {
  // ... 기존 collections
  'entities-persons':   defineCollection({ schema: PersonSchema }),
  'entities-places':    defineCollection({ schema: PlaceSchema }),
  'entities-concepts':  defineCollection({ schema: ConceptSchema }),
  'entities-texts':     defineCollection({ schema: TextSchema }),
  'entities-events':    defineCollection({ schema: EventSchema }),
  'entities-practices': defineCollection({ schema: PracticeSchema }),
  'entities-schools':   defineCollection({ schema: SchoolSchema }),
};
```

장점: TypeScript 타입이 명확, 각 유형 독립 확장 용이  
단점: collection 수가 많아짐 → 유틸 함수에서 `Promise.all`로 병렬 수집 필요

Phase 1에서는 단일 `entities` collection으로 시작해도 됩니다.  
콘텐츠가 50개 이상 쌓이면 분리를 고려하세요.

## I-2. ID 충돌 방지 — namespace 접두어

같은 이름의 인물이 다른 전통에 존재할 수 있습니다.

```
예: "아난다"
- 팔리 전통의 아난다 (붓다의 시자)
- 후대 논사 아난다

권장: 맥락이 명확하면 단순 ID 유지
      충돌 발생 시 접두어 추가
      ananda-disciple (제자 아난다)
      ananda-scholar  (논사 아난다)
```

## I-3. relation 순환 참조 주의

```
nagarjuna → developed → sunyata
sunyata → central_to → madhyamaka-school
madhyamaka-school → founded → nagarjuna  ← 순환!
```

순환 자체는 불교 연기론에서 자연스럽습니다.  
단, 렌더링 시 무한 루프를 방지하는 깊이 제한이 필요합니다.

```typescript
// lib/relations.ts에 추가
export function traverseRelations(
  entityId: string,
  triples: Triple[],
  maxDepth: number = 2,  // 깊이 제한
  visited = new Set<string>()
): Triple[] {
  if (visited.has(entityId) || maxDepth === 0) return [];
  visited.add(entityId);

  const direct = triples.filter(t => t.subject === entityId);
  const nested = direct.flatMap(t =>
    traverseRelations(t.object, triples, maxDepth - 1, visited)
  );

  return [...direct, ...nested];
}
```

## I-4. 온톨로지 버전 관리

entity 스키마는 시간이 지나면서 바뀝니다.  
`ontology/` 폴더의 파일에 버전을 명시하고,  
`config.ts` 상단에도 버전 상수를 기록하세요.

```typescript
// src/content/config.ts 상단
export const OL_ONTOLOGY_VERSION = '0.1.0';
// 스키마 변경 시 이 버전을 올리고 CHANGELOG 작성
```

## I-5. Wikidata 연동 준비 (장래)

entity에 `wikidata` 필드를 미리 준비해두면  
나중에 외부 데이터와 연동할 때 큰 도움이 됩니다.

```typescript
// EntityBaseSchema에 추가
external_ids: z.object({
  wikidata: z.string().optional(),  // "Q7486"
  cbeta: z.string().optional(),     // 중화전자불전 ID
  suttacentral: z.string().optional(), // SuttaCentral ID
}).optional(),
```

---

# 섹션 J. 완료 조건 체크리스트 (v2)

### 구조 체크
- [ ] `src/content/` 하위 6개 폴더 생성 완료
- [ ] `entities/` 7개 하위 폴더 생성 완료
- [ ] `ontology/` 2개 정의 파일 작성 완료
- [ ] `config.ts` 스키마 전체 정의 완료
- [ ] `lib/relations.ts` 작성 완료
- [ ] `lib/search.ts` 작성 완료

### 기능 체크
- [ ] `npm run build` 오류 없이 완료
- [ ] entity 페이지 자동 생성 동작 확인 (`/entity/persons/siddhartha-gautama`)
- [ ] backlinks 표시 확인
- [ ] 6개 페이지 라우팅 정상 동작

### 온톨로지 체크
- [ ] 샘플 entity 파일 최소 5개 작성
  - [ ] `persons/siddhartha-gautama.md`
  - [ ] `persons/nagarjuna.md`
  - [ ] `places/lumbini.md`
  - [ ] `concepts/sunyata.md`
  - [ ] `concepts/dependent-origination.md`
- [ ] 샘플 book 문서 1개 이상 (entity 연결 포함)
- [ ] `relation-types.md` 정의 파일 작성
- [ ] `entity-types.md` 정의 파일 작성

### 디자인 체크 (v1과 동일)
- [ ] 무채색 팔레트 유지
- [ ] 모바일/데스크탑 반응형 정상
- [ ] 다크모드 정상
- [ ] `.ol-` 클래스 네임스페이스 일관성

---

# 섹션 K. 핵심 요약 — 한 장으로 보기

```
OL HOME 구조의 핵심

src/content/
├── blog/        → 이야기 문서 (시간순)
├── book/        → 불교 콘텐츠 문서 (구조화)
├── design/      → 시각 레퍼런스 (메타데이터 중심)
├── ai/          → 실험 기록 (장래)
│
├── entities/    ★ 핵심 — 개념 노드 저장소
│   ├── persons/     인물
│   ├── places/      장소
│   ├── concepts/    개념
│   ├── texts/       문헌
│   ├── events/      사건
│   ├── practices/   수행
│   └── schools/     학파
│
└── ontology/    ★ 핵심 — 스키마 정의
    ├── entity-types.md
    └── relation-types.md

모든 문서는 entity를 참조 → build 시 지식그래프 생성
→ entity 페이지 자동 생성 → backlinks 표시 → 검색 인덱스
```

**기억할 것:**  
OL 프로젝트의 본질은 불교 콘텐츠입니다.  
구조는 콘텐츠를 담는 그릇입니다.  
그릇이 올바르면, 콘텐츠는 천천히 채울 수 있습니다.

---

*OL HOME Phase 1 작업지시서 v2 — 2026.05*  
*온톨로지 기반 불교 지식그래프 설계 통합*