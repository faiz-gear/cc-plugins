# Drizzle ORM + Supabase Reference

## Table of Contents
1. [Setup](#setup)
2. [Schema Definition](#schema-definition)
3. [Common Patterns](#common-patterns)
4. [Migrations](#migrations)
5. [Type Safety](#type-safety)

---

## Setup

### Drizzle Configuration (`drizzle.config.ts`)

```typescript
import { type Config } from "drizzle-kit";

export default {
  schema: "./src/server/db/schema.ts",
  out: "./drizzle",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  tablesFilter: ["project_*"], // Optional: filter tables by prefix
} satisfies Config;
```

### Database Client (`src/server/db/index.ts`)

```typescript
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "./schema";

const connectionString = process.env.DATABASE_URL!;

// For query purposes
const queryClient = postgres(connectionString);
export const db = drizzle(queryClient, { schema });

// For migrations (connection pooling disabled)
const migrationClient = postgres(connectionString, { max: 1 });
export const migrationDb = drizzle(migrationClient);
```

---

## Schema Definition

### Complete Schema Example (`src/server/db/schema.ts`)

```typescript
import { relations, sql } from "drizzle-orm";
import {
  boolean,
  index,
  integer,
  pgTableCreator,
  primaryKey,
  text,
  timestamp,
  uuid,
  varchar,
} from "drizzle-orm/pg-core";

// Create table with prefix (optional, useful for multi-tenant)
const createTable = pgTableCreator((name) => `app_${name}`);

// Users table (extends Supabase auth.users)
export const users = createTable(
  "users",
  {
    id: uuid("id").primaryKey(), // References auth.users.id
    email: varchar("email", { length: 255 }).notNull().unique(),
    name: varchar("name", { length: 255 }),
    avatarUrl: text("avatar_url"),
    role: varchar("role", { length: 50 }).default("user").notNull(),
    createdAt: timestamp("created_at", { withTimezone: true })
      .default(sql`CURRENT_TIMESTAMP`)
      .notNull(),
    updatedAt: timestamp("updated_at", { withTimezone: true })
      .default(sql`CURRENT_TIMESTAMP`)
      .notNull(),
  },
  (table) => ({
    emailIdx: index("users_email_idx").on(table.email),
  })
);

// Posts table
export const posts = createTable(
  "posts",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    title: varchar("title", { length: 255 }).notNull(),
    content: text("content").notNull(),
    slug: varchar("slug", { length: 255 }).notNull().unique(),
    published: boolean("published").default(false).notNull(),
    authorId: uuid("author_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    createdAt: timestamp("created_at", { withTimezone: true })
      .default(sql`CURRENT_TIMESTAMP`)
      .notNull(),
    updatedAt: timestamp("updated_at", { withTimezone: true })
      .default(sql`CURRENT_TIMESTAMP`)
      .notNull(),
  },
  (table) => ({
    authorIdx: index("posts_author_idx").on(table.authorId),
    slugIdx: index("posts_slug_idx").on(table.slug),
    publishedIdx: index("posts_published_idx").on(table.published),
  })
);

// Categories table
export const categories = createTable("categories", {
  id: uuid("id").defaultRandom().primaryKey(),
  name: varchar("name", { length: 100 }).notNull().unique(),
  slug: varchar("slug", { length: 100 }).notNull().unique(),
});

// Posts to categories (many-to-many)
export const postsToCategories = createTable(
  "posts_to_categories",
  {
    postId: uuid("post_id")
      .notNull()
      .references(() => posts.id, { onDelete: "cascade" }),
    categoryId: uuid("category_id")
      .notNull()
      .references(() => categories.id, { onDelete: "cascade" }),
  },
  (table) => ({
    pk: primaryKey({ columns: [table.postId, table.categoryId] }),
  })
);

// Comments table
export const comments = createTable(
  "comments",
  {
    id: uuid("id").defaultRandom().primaryKey(),
    content: text("content").notNull(),
    postId: uuid("post_id")
      .notNull()
      .references(() => posts.id, { onDelete: "cascade" }),
    authorId: uuid("author_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    createdAt: timestamp("created_at", { withTimezone: true })
      .default(sql`CURRENT_TIMESTAMP`)
      .notNull(),
  },
  (table) => ({
    postIdx: index("comments_post_idx").on(table.postId),
  })
);

// Relations
export const usersRelations = relations(users, ({ many }) => ({
  posts: many(posts),
  comments: many(comments),
}));

export const postsRelations = relations(posts, ({ one, many }) => ({
  author: one(users, {
    fields: [posts.authorId],
    references: [users.id],
  }),
  comments: many(comments),
  categories: many(postsToCategories),
}));

export const categoriesRelations = relations(categories, ({ many }) => ({
  posts: many(postsToCategories),
}));

export const postsToCategoriesRelations = relations(
  postsToCategories,
  ({ one }) => ({
    post: one(posts, {
      fields: [postsToCategories.postId],
      references: [posts.id],
    }),
    category: one(categories, {
      fields: [postsToCategories.categoryId],
      references: [categories.id],
    }),
  })
);

export const commentsRelations = relations(comments, ({ one }) => ({
  post: one(posts, {
    fields: [comments.postId],
    references: [posts.id],
  }),
  author: one(users, {
    fields: [comments.authorId],
    references: [users.id],
  }),
}));
```

---

## Common Patterns

### Select with Relations

```typescript
// Select with nested relations
const postsWithAuthor = await db.query.posts.findMany({
  where: eq(posts.published, true),
  with: {
    author: true,
    comments: {
      with: {
        author: true,
      },
      limit: 5,
    },
  },
  orderBy: desc(posts.createdAt),
  limit: 10,
});
```

### Insert

```typescript
const [newPost] = await db
  .insert(posts)
  .values({
    title: "New Post",
    content: "Content here",
    slug: "new-post",
    authorId: userId,
  })
  .returning();
```

### Update

```typescript
const [updatedPost] = await db
  .update(posts)
  .set({
    title: "Updated Title",
    updatedAt: new Date(),
  })
  .where(eq(posts.id, postId))
  .returning();
```

### Delete

```typescript
await db.delete(posts).where(eq(posts.id, postId));
```

### Transactions

```typescript
await db.transaction(async (tx) => {
  const [post] = await tx
    .insert(posts)
    .values({ title, content, slug, authorId })
    .returning();

  await tx.insert(postsToCategories).values(
    categoryIds.map((categoryId) => ({
      postId: post.id,
      categoryId,
    }))
  );

  return post;
});
```

### Pagination

```typescript
const page = 1;
const pageSize = 10;

const results = await db.query.posts.findMany({
  where: eq(posts.published, true),
  limit: pageSize,
  offset: (page - 1) * pageSize,
  orderBy: desc(posts.createdAt),
});
```

---

## Migrations

### Generate Migration

```bash
npx drizzle-kit generate
```

### Apply Migrations

```bash
npx drizzle-kit migrate
```

### Push (Dev Only)

```bash
npx drizzle-kit push
```

### Introspect Existing DB

```bash
npx drizzle-kit introspect
```

---

## Type Safety

### Infer Types from Schema

```typescript
import type { InferSelectModel, InferInsertModel } from "drizzle-orm";
import { posts, users } from "@/server/db/schema";

// Row types
export type Post = InferSelectModel<typeof posts>;
export type User = InferSelectModel<typeof users>;

// Insert types
export type NewPost = InferInsertModel<typeof posts>;
export type NewUser = InferInsertModel<typeof users>;

// With relations (manual)
export type PostWithAuthor = Post & {
  author: User;
};
```

### Package.json Scripts

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  }
}
```
