# ESLint Configuration Reference

## ESLint Flat Config for T3 Stack + Supabase

### Complete Configuration (`eslint.config.mjs`)

```javascript
import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import reactPlugin from "eslint-plugin-react";
import reactHooksPlugin from "eslint-plugin-react-hooks";
import importPlugin from "eslint-plugin-import";
import drizzlePlugin from "eslint-plugin-drizzle";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

export default tseslint.config(
  // Ignore patterns
  {
    ignores: [
      "node_modules/**",
      ".next/**",
      "out/**",
      "dist/**",
      "build/**",
      "*.config.js",
      "*.config.mjs",
      "supabase/**",
      "drizzle/**",
    ],
  },

  // Base configs
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,

  // Next.js config (via compat)
  ...compat.extends("next/core-web-vitals"),

  // Global settings
  {
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: __dirname,
      },
    },
  },

  // React rules
  {
    plugins: {
      react: reactPlugin,
      "react-hooks": reactHooksPlugin,
    },
    rules: {
      "react/prop-types": "off",
      "react/react-in-jsx-scope": "off",
      "react-hooks/rules-of-hooks": "error",
      "react-hooks/exhaustive-deps": "warn",
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  },

  // Import rules
  {
    plugins: {
      import: importPlugin,
    },
    rules: {
      "import/order": [
        "error",
        {
          groups: [
            "builtin",
            "external",
            "internal",
            ["parent", "sibling"],
            "index",
            "type",
          ],
          pathGroups: [
            {
              pattern: "react",
              group: "external",
              position: "before",
            },
            {
              pattern: "next/**",
              group: "external",
              position: "before",
            },
            {
              pattern: "@/**",
              group: "internal",
              position: "before",
            },
          ],
          pathGroupsExcludedImportTypes: ["react"],
          "newlines-between": "always",
          alphabetize: {
            order: "asc",
            caseInsensitive: true,
          },
        },
      ],
      "import/no-duplicates": "error",
      "import/no-unresolved": "off", // TypeScript handles this
    },
  },

  // Drizzle rules
  {
    plugins: {
      drizzle: drizzlePlugin,
    },
    rules: {
      "drizzle/enforce-delete-with-where": [
        "error",
        { drizzleObjectName: ["db", "ctx.db"] },
      ],
      "drizzle/enforce-update-with-where": [
        "error",
        { drizzleObjectName: ["db", "ctx.db"] },
      ],
    },
  },

  // TypeScript-specific rules
  {
    files: ["**/*.ts", "**/*.tsx"],
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "warn",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          caughtErrorsIgnorePattern: "^_",
        },
      ],
      "@typescript-eslint/consistent-type-imports": [
        "error",
        {
          prefer: "type-imports",
          fixStyle: "inline-type-imports",
        },
      ],
      "@typescript-eslint/no-misused-promises": [
        "error",
        { checksVoidReturn: { attributes: false } },
      ],
      "@typescript-eslint/require-await": "off",
      "@typescript-eslint/no-floating-promises": "warn",
      "@typescript-eslint/no-unsafe-assignment": "warn",
      "@typescript-eslint/no-unsafe-member-access": "warn",
      "@typescript-eslint/no-unsafe-call": "warn",
      "@typescript-eslint/no-unsafe-return": "warn",
      "@typescript-eslint/no-explicit-any": "warn",
    },
  },

  // Test files
  {
    files: ["**/*.test.ts", "**/*.test.tsx", "**/*.spec.ts", "**/*.spec.tsx"],
    rules: {
      "@typescript-eslint/no-unsafe-assignment": "off",
      "@typescript-eslint/no-unsafe-member-access": "off",
      "@typescript-eslint/no-unsafe-call": "off",
    },
  }
);
```

---

## Required Dependencies

```bash
npm install -D eslint @eslint/eslintrc @eslint/js typescript-eslint \
  eslint-plugin-react eslint-plugin-react-hooks \
  eslint-plugin-import eslint-plugin-drizzle
```

---

## Key Rules Explained

### TypeScript Rules

| Rule | Purpose |
|------|---------|
| `consistent-type-imports` | Enforce `type` keyword for type-only imports |
| `no-unused-vars` | Warn on unused variables (ignore `_` prefixed) |
| `no-misused-promises` | Prevent common async/await mistakes |
| `no-floating-promises` | Catch unhandled promises |

### React Rules

| Rule | Purpose |
|------|---------|
| `rules-of-hooks` | Enforce hooks call order |
| `exhaustive-deps` | Warn on missing effect dependencies |

### Import Rules

| Rule | Purpose |
|------|---------|
| `import/order` | Enforce consistent import ordering |
| `import/no-duplicates` | Prevent duplicate imports |

### Drizzle Rules

| Rule | Purpose |
|------|---------|
| `enforce-delete-with-where` | Require WHERE clause on DELETE |
| `enforce-update-with-where` | Require WHERE clause on UPDATE |

---

## Import Order Convention

```typescript
// 1. React/Next.js
import { useState } from "react";
import { useRouter } from "next/navigation";

// 2. External packages
import { z } from "zod";
import { toast } from "sonner";

// 3. Internal aliases (@/*)
import { Button } from "@/components/ui/button";
import { api } from "@/trpc/react";

// 4. Parent/sibling imports
import { PostCard } from "./post-card";

// 5. Type imports (grouped at end)
import type { Post } from "@/types";
```

---

## Scripts

Add to `package.json`:

```json
{
  "scripts": {
    "lint": "eslint . --max-warnings 0",
    "lint:fix": "eslint . --fix"
  }
}
```

---

## VS Code Integration

### Settings (`.vscode/settings.json`)

```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": "explicit"
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "eslint.useFlatConfig": true
}
```

---

## Common Patterns

### Disabling Rules Inline

```typescript
// Disable for entire file
/* eslint-disable @typescript-eslint/no-explicit-any */

// Disable for next line
// eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
const data = JSON.parse(response);

// Disable for specific section
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
// ... code ...
/* eslint-enable @typescript-eslint/no-unsafe-member-access */
```

### Type-Only Imports

```typescript
// Correct (enforced by consistent-type-imports)
import { type User, type Post } from "@/types";
import type { ReactNode } from "react";

// Also correct (inline style)
import { useState, type Dispatch, type SetStateAction } from "react";
```
