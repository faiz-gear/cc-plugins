# CC Plugins

A Claude Code plugin marketplace for full-stack development.

## Installation

### Step 1: Add the Marketplace

Run the following command in Claude Code:

```
/plugin marketplace add faiz-gear/cc-plugins
```

### Step 2: Browse and Install Plugins

Open the plugin menu to browse available plugins:

```
/plugin
```

Then install the plugins you need:

```
/plugin install fullstack-develop
```

## Available Plugins

### fullstack-develop

A collection of full-stack development skills for frontend design and architecture.

**Skills included:**

| Skill | Description |
|-------|-------------|
| `frontend-design-3d` | Create immersive 3D web experiences with Three.js, CSS 3D transforms, and interactive animations |
| `frontend-design-blur-grainy` | Create dreamy UI with glassmorphism, blur effects, soft gradients, and film grain textures |
| `nextjs-fullstack-architecture` | Build production-ready Next.js apps with T3 Stack (Supabase, tRPC, Drizzle, shadcn/ui) |
| `git-annual-work-summary` | Generate yearly summaries of git activity across repositories: collect commits, analyze themes, and render reports (CLI with GitHub/GitLab/local collectors) |

## Usage

Once installed, skills activate automatically when you describe relevant tasks:

```
# 3D Frontend
"Build a product viewer with orbit controls"
"Create a parallax landing page"

# Blur & Grain UI
"Design a glassmorphism dashboard"
"Add film grain texture to the hero"

# Fullstack Architecture
"Set up a T3 stack project with Supabase"
"Create a tRPC router for users"

# Git Annual Summary
"Generate an annual work summary for 2025"
"Collect commits across repos and render a report"
```

## Author

**Lyle** - [faiz-gear](https://github.com/faiz-gear)

## License

MIT
