# tRPC Integration Reference

## Table of Contents
1. [Core Setup](#core-setup)
2. [Router Patterns](#router-patterns)
3. [Context & Middleware](#context--middleware)
4. [Client Usage](#client-usage)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)

---

## Core Setup

### tRPC Initialization (`src/server/api/trpc.ts`)

```typescript
import { initTRPC, TRPCError } from "@trpc/server";
import superjson from "superjson";
import { ZodError } from "zod";
import { createClient } from "@/lib/supabase/server";

export const createTRPCContext = async (opts: { headers: Headers }) => {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();

  return {
    supabase,
    user,
    ...opts,
  };
};

const t = initTRPC.context<typeof createTRPCContext>().create({
  transformer: superjson,
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError ? error.cause.flatten() : null,
      },
    };
  },
});

export const createCallerFactory = t.createCallerFactory;
export const createTRPCRouter = t.router;

// Public procedure - no auth required
export const publicProcedure = t.procedure;

// Protected procedure - requires authenticated user
export const protectedProcedure = t.procedure.use(({ ctx, next }) => {
  if (!ctx.user) {
    throw new TRPCError({ code: "UNAUTHORIZED" });
  }
  return next({
    ctx: {
      ...ctx,
      user: ctx.user,
    },
  });
});
```

### Root Router (`src/server/api/routers/index.ts`)

```typescript
import { createTRPCRouter } from "@/server/api/trpc";
import { userRouter } from "./user";
import { postRouter } from "./post";

export const appRouter = createTRPCRouter({
  user: userRouter,
  post: postRouter,
});

export type AppRouter = typeof appRouter;
```

### API Route Handler (`src/app/api/trpc/[trpc]/route.ts`)

```typescript
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { appRouter } from "@/server/api/routers";
import { createTRPCContext } from "@/server/api/trpc";

const handler = (req: Request) =>
  fetchRequestHandler({
    endpoint: "/api/trpc",
    req,
    router: appRouter,
    createContext: () => createTRPCContext({ headers: req.headers }),
    onError:
      process.env.NODE_ENV === "development"
        ? ({ path, error }) => {
            console.error(
              `❌ tRPC failed on ${path ?? "<no-path>"}: ${error.message}`
            );
          }
        : undefined,
  });

export { handler as GET, handler as POST };
```

---

## Router Patterns

### Basic Router (`src/server/api/routers/post.ts`)

```typescript
import { z } from "zod";
import { createTRPCRouter, publicProcedure, protectedProcedure } from "@/server/api/trpc";
import { TRPCError } from "@trpc/server";

export const postRouter = createTRPCRouter({
  // Public query
  getAll: publicProcedure
    .input(z.object({
      limit: z.number().min(1).max(100).default(10),
      cursor: z.string().nullish(),
    }))
    .query(async ({ ctx, input }) => {
      const { data, error } = await ctx.supabase
        .from("posts")
        .select("*, author:users(name)")
        .eq("published", true)
        .order("created_at", { ascending: false })
        .limit(input.limit);

      if (error) throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: error.message });

      return data;
    }),

  // Public query - single item
  getById: publicProcedure
    .input(z.object({ id: z.string().uuid() }))
    .query(async ({ ctx, input }) => {
      const { data, error } = await ctx.supabase
        .from("posts")
        .select("*, author:users(name, avatar)")
        .eq("id", input.id)
        .single();

      if (error || !data) {
        throw new TRPCError({ code: "NOT_FOUND", message: "Post not found" });
      }

      return data;
    }),

  // Protected mutation - create
  create: protectedProcedure
    .input(z.object({
      title: z.string().min(1).max(255),
      content: z.string().min(1),
      published: z.boolean().default(false),
    }))
    .mutation(async ({ ctx, input }) => {
      const { data, error } = await ctx.supabase
        .from("posts")
        .insert({
          ...input,
          user_id: ctx.user.id,
        })
        .select()
        .single();

      if (error) throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: error.message });

      return data;
    }),

  // Protected mutation - update
  update: protectedProcedure
    .input(z.object({
      id: z.string().uuid(),
      title: z.string().min(1).max(255).optional(),
      content: z.string().min(1).optional(),
      published: z.boolean().optional(),
    }))
    .mutation(async ({ ctx, input }) => {
      const { id, ...updates } = input;

      const { data, error } = await ctx.supabase
        .from("posts")
        .update(updates)
        .eq("id", id)
        .eq("user_id", ctx.user.id)
        .select()
        .single();

      if (error) throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: error.message });
      if (!data) throw new TRPCError({ code: "NOT_FOUND", message: "Post not found or unauthorized" });

      return data;
    }),

  // Protected mutation - delete
  delete: protectedProcedure
    .input(z.object({ id: z.string().uuid() }))
    .mutation(async ({ ctx, input }) => {
      const { error } = await ctx.supabase
        .from("posts")
        .delete()
        .eq("id", input.id)
        .eq("user_id", ctx.user.id);

      if (error) throw new TRPCError({ code: "INTERNAL_SERVER_ERROR", message: error.message });

      return { success: true };
    }),
});
```

---

## Context & Middleware

### Custom Middleware

```typescript
const loggerMiddleware = t.middleware(async ({ path, type, next }) => {
  const start = Date.now();
  const result = await next();
  const duration = Date.now() - start;
  console.log(`${type} ${path} - ${duration}ms`);
  return result;
});

const rateLimitMiddleware = t.middleware(async ({ ctx, next }) => {
  // Implement rate limiting logic
  return next();
});

export const loggedProcedure = publicProcedure.use(loggerMiddleware);
export const rateLimitedProcedure = publicProcedure.use(rateLimitMiddleware);
```

### Role-Based Middleware

```typescript
const adminProcedure = protectedProcedure.use(async ({ ctx, next }) => {
  const { data: profile } = await ctx.supabase
    .from("profiles")
    .select("role")
    .eq("id", ctx.user.id)
    .single();

  if (profile?.role !== "admin") {
    throw new TRPCError({ code: "FORBIDDEN" });
  }

  return next({ ctx: { ...ctx, role: "admin" as const } });
});
```

---

## Client Usage

### React Provider (`src/trpc/react.tsx`)

```typescript
"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { httpBatchLink, loggerLink } from "@trpc/client";
import { createTRPCReact } from "@trpc/react-query";
import { useState } from "react";
import superjson from "superjson";
import type { AppRouter } from "@/server/api/routers";

export const api = createTRPCReact<AppRouter>();

function getBaseUrl() {
  if (typeof window !== "undefined") return "";
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return `http://localhost:${process.env.PORT ?? 3000}`;
}

export function TRPCReactProvider(props: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() =>
    api.createClient({
      links: [
        loggerLink({
          enabled: (op) =>
            process.env.NODE_ENV === "development" ||
            (op.direction === "down" && op.result instanceof Error),
        }),
        httpBatchLink({
          url: getBaseUrl() + "/api/trpc",
          transformer: superjson,
        }),
      ],
    })
  );

  return (
    <QueryClientProvider client={queryClient}>
      <api.Provider client={trpcClient} queryClient={queryClient}>
        {props.children}
      </api.Provider>
    </QueryClientProvider>
  );
}
```

### Server-Side Caller (`src/trpc/server.ts`)

```typescript
import "server-only";
import { createTRPCContext, createCallerFactory } from "@/server/api/trpc";
import { appRouter } from "@/server/api/routers";
import { headers } from "next/headers";
import { cache } from "react";

const createContext = cache(async () => {
  const heads = new Headers(await headers());
  return createTRPCContext({ headers: heads });
});

const createCaller = createCallerFactory(appRouter);

export const api = createCaller(createContext);
```

### Client Component Usage

```typescript
"use client";

import { api } from "@/trpc/react";

export function PostList() {
  const { data: posts, isLoading } = api.post.getAll.useQuery({ limit: 10 });
  const utils = api.useUtils();

  const createPost = api.post.create.useMutation({
    onSuccess: () => {
      utils.post.getAll.invalidate();
    },
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <div>
      {posts?.map((post) => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  );
}
```

### Server Component Usage

```typescript
import { api } from "@/trpc/server";

export default async function PostsPage() {
  const posts = await api.post.getAll({ limit: 10 });

  return (
    <div>
      {posts.map((post) => (
        <div key={post.id}>{post.title}</div>
      ))}
    </div>
  );
}
```

---

## Error Handling

### Error Codes

| Code | HTTP | Description |
|------|------|-------------|
| `PARSE_ERROR` | 400 | Invalid JSON |
| `BAD_REQUEST` | 400 | Invalid input |
| `UNAUTHORIZED` | 401 | Not authenticated |
| `FORBIDDEN` | 403 | Not authorized |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource conflict |
| `INTERNAL_SERVER_ERROR` | 500 | Server error |

### Client Error Handling

```typescript
const createPost = api.post.create.useMutation({
  onError: (error) => {
    if (error.data?.zodError) {
      // Handle validation errors
      const fieldErrors = error.data.zodError.fieldErrors;
    } else {
      // Handle other errors
      toast.error(error.message);
    }
  },
});
```

---

## Best Practices

1. **Input Validation**: Always use Zod schemas for input validation
2. **Error Messages**: Provide meaningful error messages
3. **Optimistic Updates**: Use for better UX on mutations
4. **Cache Invalidation**: Invalidate relevant queries after mutations
5. **Type Safety**: Export router types for end-to-end type safety
6. **Batching**: tRPC batches requests automatically - leverage this
7. **Prefetching**: Use `prefetch` for anticipated data needs
