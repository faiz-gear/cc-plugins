---
name: nextjs-fullstack-architecture
description: "Build production-ready Next.js fullstack applications using T3 Stack architecture with Supabase (database + auth), tRPC for type-safe APIs, Drizzle ORM, shadcn/ui components, and ESLint flat config. Use when creating new Next.js projects, adding features to T3 stack apps, implementing authentication flows, building CRUD operations with tRPC, setting up database schemas, or configuring modern ESLint. Triggers on T3 stack, Supabase integration, tRPC routers, Drizzle schema, shadcn components, Next.js App Router patterns."
---

# Next.js Fullstack Architecture

Production-ready fullstack architecture using T3 Stack + Supabase for type-safe, scalable applications.

## Stack Overview

| Layer | Technology | Purpose |
|-------|------------|---------|
| Framework | Next.js 15 (App Router) | React fullstack framework |
| API | tRPC | End-to-end type-safe APIs |
| Database | Supabase (PostgreSQL) | Managed database + auth |
| ORM | Drizzle | Type-safe database queries |
| UI | shadcn/ui + Tailwind | Component library |
| Validation | Zod | Runtime type validation |
| Linting | ESLint (flat config) | Code quality |

## Quick Start

### 1. Create Project

```bash
npx create-t3-app@latest my-app --noGit
cd my-app
```

Select: TypeScript, tRPC, Tailwind, Drizzle, App Router

### 2. Initialize Supabase

```bash
npx supabase init
npx supabase start  # Local development
```

### 3. Configure Environment

```env
# .env.local
DATABASE_URL="postgresql://postgres:postgres@localhost:54322/postgres"
NEXT_PUBLIC_SUPABASE_URL="http://localhost:54321"
NEXT_PUBLIC_SUPABASE_ANON_KEY="your-anon-key"
SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
```

### 4. Install Supabase SSR

```bash
npm install @supabase/supabase-js @supabase/ssr
```

### 5. Initialize shadcn/ui

```bash
npx shadcn@latest init
npx shadcn@latest add button card form input
```

## Architecture Decision Tree

```
What are you building?
│
├─► New feature with UI
│   └─► See: Component Workflow
│
├─► API endpoint / data operation
│   └─► See: tRPC Router Workflow
│
├─► Authentication flow
│   └─► See: references/supabase.md (Authentication Patterns)
│
├─► Database schema change
│   └─► See: references/drizzle.md (Schema Definition)
│
└─► Project setup / configuration
    └─► See: references/project-structure.md
```

## Component Workflow

Building a feature with UI components:

### Step 1: Define Data Schema (if needed)

```typescript
// src/server/db/schema.ts
export const posts = createTable("posts", {
  id: uuid("id").defaultRandom().primaryKey(),
  title: varchar("title", { length: 255 }).notNull(),
  content: text("content").notNull(),
  authorId: uuid("author_id").notNull().references(() => users.id),
  createdAt: timestamp("created_at").default(sql`CURRENT_TIMESTAMP`).notNull(),
});
```

### Step 2: Create tRPC Router

```typescript
// src/server/api/routers/post.ts
export const postRouter = createTRPCRouter({
  getAll: publicProcedure.query(async ({ ctx }) => {
    return ctx.db.query.posts.findMany({
      with: { author: true },
      orderBy: desc(posts.createdAt),
    });
  }),

  create: protectedProcedure
    .input(z.object({
      title: z.string().min(1),
      content: z.string().min(1),
    }))
    .mutation(async ({ ctx, input }) => {
      return ctx.db.insert(posts).values({
        ...input,
        authorId: ctx.user.id,
      }).returning();
    }),
});
```

### Step 3: Build UI Components

```typescript
// src/components/posts/post-list.tsx
"use client";

import { api } from "@/trpc/react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

export function PostList() {
  const { data: posts, isLoading } = api.post.getAll.useQuery();

  if (isLoading) {
    return <PostListSkeleton />;
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {posts?.map((post) => (
        <Card key={post.id}>
          <CardHeader>
            <CardTitle>{post.title}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-muted-foreground">{post.content}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
```

### Step 4: Server Component Integration

```typescript
// src/app/posts/page.tsx
import { api } from "@/trpc/server";
import { PostList } from "@/components/posts/post-list";

export default async function PostsPage() {
  // Prefetch data on server
  const posts = await api.post.getAll();

  return (
    <main className="container py-8">
      <h1 className="text-3xl font-bold mb-8">Posts</h1>
      <PostList initialData={posts} />
    </main>
  );
}
```

## tRPC Router Workflow

Creating type-safe API endpoints:

### Pattern: CRUD Router

```typescript
export const entityRouter = createTRPCRouter({
  // List with pagination
  list: publicProcedure
    .input(z.object({
      limit: z.number().min(1).max(100).default(10),
      cursor: z.string().nullish(),
    }))
    .query(async ({ ctx, input }) => { /* ... */ }),

  // Get by ID
  byId: publicProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(async ({ ctx, input }) => { /* ... */ }),

  // Create (protected)
  create: protectedProcedure
    .input(createSchema)
    .mutation(async ({ ctx, input }) => { /* ... */ }),

  // Update (protected)
  update: protectedProcedure
    .input(updateSchema)
    .mutation(async ({ ctx, input }) => { /* ... */ }),

  // Delete (protected)
  delete: protectedProcedure
    .input(z.object({ id: z.string().uuid() }))
    .mutation(async ({ ctx, input }) => { /* ... */ }),
});
```

### Client Usage Patterns

```typescript
// Queries
const { data, isLoading, error } = api.entity.list.useQuery({ limit: 10 });

// Mutations with cache invalidation
const utils = api.useUtils();
const createMutation = api.entity.create.useMutation({
  onSuccess: () => {
    utils.entity.list.invalidate();
    toast.success("Created successfully");
  },
  onError: (error) => {
    toast.error(error.message);
  },
});
```

## Authentication Setup

### 1. Create Supabase Clients

See: [references/supabase.md](references/supabase.md) - Client Setup section

### 2. Configure Middleware

See: [references/supabase.md](references/supabase.md) - Middleware Configuration section

### 3. Integrate with tRPC Context

```typescript
// src/server/api/trpc.ts
export const createTRPCContext = async (opts: { headers: Headers }) => {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();

  return {
    supabase,
    user,
    db, // Drizzle client
    ...opts,
  };
};
```

## ESLint Configuration

Use flat config format for modern ESLint setup.

See: [references/eslint.md](references/eslint.md) for complete configuration.

Key features:
- TypeScript strict type checking
- React hooks rules
- Import ordering
- Drizzle safety rules (enforce WHERE clauses)
- Type-only import enforcement

## References

Detailed documentation for each technology:

| Reference | Contents |
|-----------|----------|
| [project-structure.md](references/project-structure.md) | Directory layout, naming conventions, import aliases |
| [supabase.md](references/supabase.md) | Auth patterns, client setup, RLS policies, middleware |
| [trpc.md](references/trpc.md) | Router patterns, middleware, client usage, error handling |
| [shadcn-ui.md](references/shadcn-ui.md) | Component patterns, forms, theming, compositions |
| [drizzle.md](references/drizzle.md) | Schema definition, queries, migrations, relations |
| [eslint.md](references/eslint.md) | Flat config, rules, import ordering |

## Common Patterns

### Form with Server Action Alternative

For simple forms, consider server actions over tRPC:

```typescript
// src/app/posts/actions.ts
"use server";

import { createClient } from "@/lib/supabase/server";
import { revalidatePath } from "next/cache";

export async function createPost(formData: FormData) {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) throw new Error("Unauthorized");

  await db.insert(posts).values({
    title: formData.get("title") as string,
    content: formData.get("content") as string,
    authorId: user.id,
  });

  revalidatePath("/posts");
}
```

### Protected Layout

```typescript
// src/app/(dashboard)/layout.tsx
import { redirect } from "next/navigation";
import { createClient } from "@/lib/supabase/server";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login");
  }

  return (
    <div className="flex min-h-screen">
      <Sidebar user={user} />
      <main className="flex-1 p-8">{children}</main>
    </div>
  );
}
```

### Loading States

```typescript
// src/app/posts/loading.tsx
import { Skeleton } from "@/components/ui/skeleton";

export default function Loading() {
  return (
    <div className="container py-8">
      <Skeleton className="h-10 w-48 mb-8" />
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {[...Array(6)].map((_, i) => (
          <Skeleton key={i} className="h-48 rounded-lg" />
        ))}
      </div>
    </div>
  );
}
```

### Error Boundary

```typescript
// src/app/posts/error.tsx
"use client";

import { Button } from "@/components/ui/button";

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div className="flex min-h-[400px] flex-col items-center justify-center">
      <h2 className="text-2xl font-bold mb-4">Something went wrong</h2>
      <p className="text-muted-foreground mb-4">{error.message}</p>
      <Button onClick={reset}>Try again</Button>
    </div>
  );
}
```
