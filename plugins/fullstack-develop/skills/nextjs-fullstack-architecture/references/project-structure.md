# Project Structure Reference

## T3 Stack + Supabase Directory Layout

```
project-root/
├── src/
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/             # Auth route group
│   │   │   ├── login/
│   │   │   ├── register/
│   │   │   └── callback/       # Supabase auth callback
│   │   ├── (dashboard)/        # Protected routes group
│   │   ├── api/                # API routes
│   │   │   └── trpc/[trpc]/    # tRPC handler
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page
│   │   └── globals.css         # Global styles + Tailwind
│   │
│   ├── components/
│   │   ├── ui/                 # shadcn/ui components
│   │   ├── forms/              # Form components
│   │   ├── layouts/            # Layout components
│   │   └── providers/          # Context providers
│   │
│   ├── lib/
│   │   ├── supabase/
│   │   │   ├── client.ts       # Browser client
│   │   │   ├── server.ts       # Server client
│   │   │   ├── middleware.ts   # Auth middleware helper
│   │   │   └── admin.ts        # Admin client (service role)
│   │   ├── utils.ts            # Utility functions (cn, etc.)
│   │   └── validators.ts       # Zod schemas
│   │
│   ├── server/
│   │   ├── api/
│   │   │   ├── routers/        # tRPC routers
│   │   │   │   ├── user.ts
│   │   │   │   ├── post.ts
│   │   │   │   └── index.ts    # Root router
│   │   │   └── trpc.ts         # tRPC initialization
│   │   └── db/
│   │       ├── index.ts        # Drizzle client
│   │       └── schema.ts       # Drizzle schema
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── use-user.ts
│   │   └── use-supabase.ts
│   │
│   ├── types/                  # TypeScript types
│   │   ├── database.types.ts   # Supabase generated types
│   │   └── index.ts
│   │
│   └── trpc/
│       ├── react.tsx           # React Query + tRPC provider
│       └── server.ts           # Server-side caller
│
├── supabase/
│   ├── migrations/             # Database migrations
│   ├── seed.sql                # Seed data
│   └── config.toml             # Supabase local config
│
├── public/                     # Static assets
├── drizzle/                    # Drizzle migrations output
├── .env.local                  # Environment variables
├── .env.example                # Environment template
├── drizzle.config.ts           # Drizzle configuration
├── tailwind.config.ts          # Tailwind configuration
├── components.json             # shadcn/ui configuration
├── next.config.js              # Next.js configuration
├── tsconfig.json               # TypeScript configuration
└── eslint.config.mjs           # ESLint flat config
```

## Route Groups Explained

### `(auth)` Group
- Public authentication pages
- Login, register, password reset
- OAuth callback handling

### `(dashboard)` Group
- Protected routes requiring authentication
- Middleware redirects unauthenticated users
- Shared dashboard layout

### `(marketing)` Group (optional)
- Public marketing pages
- Landing, pricing, about
- Different layout from dashboard

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `UserProfile.tsx` |
| Hooks | camelCase with `use-` | `use-user.ts` |
| Utilities | camelCase | `formatDate.ts` |
| Types | PascalCase | `User.types.ts` |
| API routes | kebab-case folders | `api/auth/callback/` |
| tRPC routers | camelCase | `userRouter.ts` |

## Import Aliases

Configure in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/server/*": ["./src/server/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/types/*": ["./src/types/*"]
    }
  }
}
```
