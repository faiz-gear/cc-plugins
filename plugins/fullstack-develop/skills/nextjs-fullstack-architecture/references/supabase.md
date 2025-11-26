# Supabase Integration Reference

## Table of Contents
1. [Client Setup](#client-setup)
2. [Authentication Patterns](#authentication-patterns)
3. [Middleware Configuration](#middleware-configuration)
4. [Database Access Patterns](#database-access-patterns)
5. [Row Level Security](#row-level-security)
6. [Type Generation](#type-generation)

---

## Client Setup

### Browser Client (`src/lib/supabase/client.ts`)

```typescript
import { createBrowserClient } from "@supabase/ssr";
import type { Database } from "@/types/database.types";

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

### Server Client (`src/lib/supabase/server.ts`)

```typescript
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import type { Database } from "@/types/database.types";

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          } catch {
            // Server Component - ignore
          }
        },
      },
    }
  );
}
```

### Admin Client (`src/lib/supabase/admin.ts`)

```typescript
import { createClient } from "@supabase/supabase-js";
import type { Database } from "@/types/database.types";

// Use only in server-side code, never expose to client
export const supabaseAdmin = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false,
    },
  }
);
```

---

## Authentication Patterns

### Sign Up with Email

```typescript
const { data, error } = await supabase.auth.signUp({
  email: "user@example.com",
  password: "secure-password",
  options: {
    emailRedirectTo: `${origin}/auth/callback`,
    data: {
      full_name: "John Doe", // Custom user metadata
    },
  },
});
```

### Sign In with Email

```typescript
const { data, error } = await supabase.auth.signInWithPassword({
  email: "user@example.com",
  password: "secure-password",
});
```

### OAuth Sign In

```typescript
const { data, error } = await supabase.auth.signInWithOAuth({
  provider: "github", // or 'google', 'discord', etc.
  options: {
    redirectTo: `${origin}/auth/callback`,
  },
});
```

### Sign Out

```typescript
const { error } = await supabase.auth.signOut();
```

### Auth Callback Route (`src/app/auth/callback/route.ts`)

```typescript
import { NextResponse } from "next/server";
import { createClient } from "@/lib/supabase/server";

export async function GET(request: Request) {
  const { searchParams, origin } = new URL(request.url);
  const code = searchParams.get("code");
  const next = searchParams.get("next") ?? "/dashboard";

  if (code) {
    const supabase = await createClient();
    const { error } = await supabase.auth.exchangeCodeForSession(code);
    if (!error) {
      return NextResponse.redirect(`${origin}${next}`);
    }
  }

  return NextResponse.redirect(`${origin}/auth/error`);
}
```

### Get Current User (Server)

```typescript
const supabase = await createClient();
const { data: { user }, error } = await supabase.auth.getUser();
```

### Get Current Session (Server)

```typescript
const supabase = await createClient();
const { data: { session }, error } = await supabase.auth.getSession();
```

---

## Middleware Configuration

### Full Middleware (`src/middleware.ts`)

```typescript
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({
    request,
  });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          );
          supabaseResponse = NextResponse.next({
            request,
          });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // Refresh session if expired
  const { data: { user } } = await supabase.auth.getUser();

  // Protect dashboard routes
  if (request.nextUrl.pathname.startsWith("/dashboard") && !user) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    return NextResponse.redirect(url);
  }

  // Redirect authenticated users away from auth pages
  if (user && (
    request.nextUrl.pathname.startsWith("/login") ||
    request.nextUrl.pathname.startsWith("/register")
  )) {
    const url = request.nextUrl.clone();
    url.pathname = "/dashboard";
    return NextResponse.redirect(url);
  }

  return supabaseResponse;
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
```

---

## Database Access Patterns

### Query Data

```typescript
const { data, error } = await supabase
  .from("posts")
  .select("*, author:users(name, avatar)")
  .eq("published", true)
  .order("created_at", { ascending: false })
  .limit(10);
```

### Insert Data

```typescript
const { data, error } = await supabase
  .from("posts")
  .insert({
    title: "New Post",
    content: "Content here",
    user_id: user.id,
  })
  .select()
  .single();
```

### Update Data

```typescript
const { data, error } = await supabase
  .from("posts")
  .update({ title: "Updated Title" })
  .eq("id", postId)
  .select()
  .single();
```

### Delete Data

```typescript
const { error } = await supabase
  .from("posts")
  .delete()
  .eq("id", postId);
```

### Upsert Data

```typescript
const { data, error } = await supabase
  .from("profiles")
  .upsert({
    id: user.id,
    username: "newusername",
    updated_at: new Date().toISOString(),
  })
  .select()
  .single();
```

---

## Row Level Security

### Enable RLS on Table

```sql
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
```

### Common RLS Policies

```sql
-- Users can read all published posts
CREATE POLICY "Public posts are viewable by everyone"
  ON posts FOR SELECT
  USING (published = true);

-- Users can read their own unpublished posts
CREATE POLICY "Users can view own posts"
  ON posts FOR SELECT
  USING (auth.uid() = user_id);

-- Users can insert their own posts
CREATE POLICY "Users can create posts"
  ON posts FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own posts
CREATE POLICY "Users can update own posts"
  ON posts FOR UPDATE
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Users can delete their own posts
CREATE POLICY "Users can delete own posts"
  ON posts FOR DELETE
  USING (auth.uid() = user_id);
```

### Service Role Bypass

The admin client with service role key bypasses RLS - use carefully.

---

## Type Generation

### Generate Types from Supabase

```bash
npx supabase gen types typescript --project-id <project-id> > src/types/database.types.ts
```

### Or from local Supabase

```bash
npx supabase gen types typescript --local > src/types/database.types.ts
```

### Using Types

```typescript
import type { Database } from "@/types/database.types";

type Post = Database["public"]["Tables"]["posts"]["Row"];
type InsertPost = Database["public"]["Tables"]["posts"]["Insert"];
type UpdatePost = Database["public"]["Tables"]["posts"]["Update"];
```
