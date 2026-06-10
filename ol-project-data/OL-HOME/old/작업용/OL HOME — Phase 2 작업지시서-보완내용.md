# OL HOME — Phase 2 작업지시서-보완내용
## 검토 결과 — 4개 충돌, 2개 보완 필요

보고서와 Phase 2 작업지시서를 대조한 결과입니다.

---

### 🔴 충돌 1 (가장 중요): `config.ts` 경로 오류

**작업지시서**: `src/content/config.ts` 수정하라고 지시  
**실제 상태**: Astro 6에서 `src/content.config.ts` (위치 다름)로 마이그레이션 완료

```
❌ 지시서: src/content/config.ts
✅ 실제:   src/content.config.ts   ← 루트에 위치, 점(.)으로 구분
```

에이전트가 지시서대로 `src/content/config.ts`를 수정하려 하면 파일을 못 찾거나 새로 만들어 충돌이 납니다.

**수정 지시**: TASK A-2의 파일 경로를 `src/content.config.ts`로 교체.

---

### 🔴 충돌 2: `defineCollection` 대신 `glob()` 로더 방식 사용 중

**작업지시서**: 기존 `defineCollection({ type: 'content', schema: ... })` 패턴으로 works collection 추가 지시  
**실제 상태**: Astro 6 Content Layer API로 마이그레이션되어 모든 컬렉션이 `glob()` 로더 방식 사용

실제 파일은 이런 패턴일 것:

```typescript
// 실제 src/content.config.ts 패턴
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const worksCollection = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/works' }),
  schema: z.object({ ... }),
});
```

작업지시서의 `defineCollection({ type: 'content', schema: ... })` 코드를 그대로 쓰면 오류 발생.

**수정 지시**: TASK A-2의 collection 정의 코드 전체를 glob 로더 방식으로 교체:

```typescript
// TASK A-2 수정안
const worksCollection = defineCollection({
  loader: glob({
    pattern: '**/*.{md,mdx}',
    base: './src/content/works'
  }),
  schema: z.object({
    title: z.string(),
    series: z.string().optional(),
    chapter: z.number().optional(),
    order: z.number().default(0),
    date: z.coerce.date().optional(),
    status: z.enum(['draft', 'revising', 'ready', 'published']).default('draft'),
    entities: z.array(z.string()).default([]),
    relations: z.array(RelationSchema).default([]),
    primary_entity: z.string().optional(),
    sources: z.array(z.object({
      text: z.string(),
      ref: z.string().optional(),
      passage: z.string().optional(),
    })).default([]),
    tags: z.array(z.string()).default([]),
    published: z.boolean().default(false),
    excerpt: z.string().optional(),
  }),
});
```

---

### 🔴 충돌 3: `entry.slug` → `entry.id` (Astro 6 API 변경)

**작업지시서**: `entry.slug` 사용 (약 7곳)  
**실제 상태**: Astro 6 새 API에서 `.slug` 제거됨, `.id` 사용

영향받는 코드 위치:
```
WorksLayout.astro    — entry.slug (사이드바 active 비교, href)
works/index.astro    — entry.slug (href)
works/[...slug].astro — entry.slug (getStaticPaths의 params, currentSlug prop)
OLLatestUpdates.astro — post.slug (href)
blog/index.astro     — post.slug (href)
```

**수정 지시**: 작업지시서 전체에서 `entry.slug` → `entry.id`, `post.slug` → `post.id` 치환. `params: { slug: entry.slug }` → `params: { slug: entry.id }`.

---

### 🔴 충돌 4: `entry.render()` → `render(entry)` (Astro 6 API 변경)

**작업지시서** `works/[...slug].astro`:
```astro
const { Content } = await entry.render();   ← 레거시 API
```

**실제 사용 방식**:
```astro
import { render } from 'astro:content';
const { Content } = await render(entry);    ← Astro 6 방식
```

보고서에서 이미 이 변경을 Phase 1에서 수행했다고 명시.

**수정 지시**: `works/[...slug].astro`의 render 호출 방식 교체:

```astro
---
import { getCollection, render } from 'astro:content';
// ...
const { Content } = await render(entry);
---
```

---

### 🟡 보완 1: blog collection 스키마 필드명 불일치

**작업지시서** blog/index.astro:
```astro
e.data.description  // excerpt라고 표시된 곳에서 혼용
```

**실제 보고서의 blog 스키마**:
```
blog: title, description, date, readingTime, category, published
```

`excerpt` 필드가 없고 `description`과 `readingTime`이 있습니다. 작업지시서 E-2의 blog/index.astro가 `post.data.excerpt`를 참조하는 부분을 `post.data.description`으로 수정해야 합니다. `readingTime`도 목록에 표시할 수 있는 유용한 필드입니다.

**수정 지시**: `post.data.excerpt` → `post.data.description`, 필요시 `post.data.readingTime` 추가 표시.

---

### 🟡 보완 2: `OLLatestUpdates.astro` 이미 하드코딩 → 동적 변환 시 스키마 확인 필요

보고서에 따르면 `OLLatestUpdates.astro`는 이미 구현된 컴포넌트입니다. TASK F에서 이 파일을 동적으로 전환할 때, 위 blog 스키마(description, readingTime)에 맞게 필드를 참조해야 합니다.

---

## 에이전트에게 전달할 수정 지침 (추가)

Phase 2 작업지시서 앞에 다음 블록을 추가하여 전달하세요:

```
[Phase 1 실제 구현과의 차이 — 반드시 준수]

1. 설정 파일 경로
   작업지시서의 src/content/config.ts
   → 실제: src/content.config.ts (프로젝트 루트에 위치)

2. Content Collection 정의 방식
   작업지시서의 defineCollection({ type: 'content', schema })
   → 실제: defineCollection({ loader: glob({ pattern, base }), schema })
   모든 collection에 glob() 로더 추가 필수.
   glob import: import { glob } from 'astro/loaders';

3. entry ID 접근
   작업지시서의 entry.slug, post.slug
   → 실제: entry.id, post.id
   Astro 6에서 .slug 제거됨.

4. 콘텐츠 렌더링
   작업지시서의 const { Content } = await entry.render()
   → 실제: import { render } from 'astro:content'
            const { Content } = await render(entry)

5. blog 스키마 필드
   작업지시서의 post.data.excerpt
   → 실제: post.data.description
   blog collection 스키마: title, description, date, readingTime, category, published
```

---

## 요약

| 구분 | 항목 | 심각도 |
|------|------|--------|
| 충돌 1 | config.ts 경로 | 🔴 빌드 오류 |
| 충돌 2 | glob 로더 방식 | 🔴 빌드 오류 |
| 충돌 3 | entry.slug → entry.id | 🔴 런타임 오류 |
| 충돌 4 | entry.render() | 🔴 런타임 오류 |
| 보완 1 | blog 필드명 | 🟡 렌더링 누락 |
| 보완 2 | OLLatestUpdates 필드 | 🟡 렌더링 누락 |

4개의 빨간 항목은 수정 없이 그대로 실행하면 빌드가 깨집니다. 