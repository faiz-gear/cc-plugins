---
name: frontend-design-blur-grainy
description: Create dreamy, ethereal web interfaces with blur effects, soft gradients, subtle noise textures, and modern glassmorphism. Use when users request airy futuristic UI, soft-focus designs, pastel haze aesthetics, film grain overlays, diffuse glow effects, frosted glass interfaces, dreamy soft blur backgrounds, or any UI that should feel atmospheric and dreamlike rather than sharp and crisp.
---

This skill guides creation of blur and grainy UI effects that transform flat interfaces into atmospheric, dreamlike experiences. Implement soft gradients, subtle noise textures, glassmorphism 2.0, and diffuse glow to achieve an airy, futuristic aesthetic.

The user provides frontend requirements: a dreamy landing page, frosted glass cards, film-textured backgrounds, soft neon accents, or any interface that benefits from blur and grain aesthetics.

## Effect Selection

Choose the right approach based on the desired aesthetic:

| Use Case | Primary Effect | When to Use |
|----------|----------------|-------------|
| Frosted glass UI | Glassmorphism 2.0 | Cards, modals, navigation overlays |
| Dreamy backgrounds | Soft blur + gradients | Hero sections, full-page backgrounds |
| Film/analog feel | Grain overlay | Photography sites, vintage aesthetics |
| Ethereal glow | Diffuse glow + blur | CTAs, featured elements, neon accents |
| Pastel atmosphere | Haze overlays | Soft, airy landing pages |
| Textured depth | Combined blur + grain | Premium, layered UI compositions |

## Design Philosophy

Before coding, establish the atmospheric direction:

- **Blur Intensity**: Subtle frost (4-12px) or heavy diffusion (40-80px)?
- **Grain Character**: Fine film (0.7+ frequency) or coarse texture (0.3-0.5)?
- **Color Temperature**: Warm pastels (pink/peach) or cool pastels (blue/mint)?
- **Opacity Balance**: Barely visible (3-5%) or noticeable texture (8-15%)?

**CRITICAL**: These effects should enhance, not overwhelm. A subtle grain overlay adds organic warmth; too much becomes distracting noise.

## Core Patterns

### Soft Blur & Gradients

For dreamy backgrounds, floating orbs, pastel haze, soft-focus effects:

```css
.dreamy-bg {
  background: linear-gradient(135deg, #ffeef8 0%, #f0f8ff 100%);
  position: relative;
}

.dreamy-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 50%, rgba(255, 182, 255, 0.3) 0%, transparent 40%),
    radial-gradient(circle at 80% 30%, rgba(182, 255, 255, 0.3) 0%, transparent 40%);
  filter: blur(60px);
  z-index: -1;
}
```

See [references/blur-gradient-patterns.md](references/blur-gradient-patterns.md) for:
- Core blur properties and intensity scale
- Soft gradient techniques (pastel, aurora, mesh)
- Dreamy background blur patterns
- Frosted glass effects (warm, cool, dark variants)
- Diffuse glow effects (pulsing, rainbow, inner glow)
- Pastel haze overlays
- Soft-focus neon

### Glassmorphism 2.0

For modern frosted glass cards, modals, navigation, inputs:

```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}
```

See [references/glassmorphism-patterns.md](references/glassmorphism-patterns.md) for:
- Core glassmorphism with CSS variables
- Advanced glass variants (tinted, gradient, iridescent, dark)
- Glass cards with hover effects and depth
- Glass navigation (navbar, pills, sidebar, FAB)
- Glass modals and drawers
- Glass input fields and toggles
- Layered glass depth compositions
- Browser support and fallbacks

### Film Grain & Texture

For noise overlays, film grain effects, analog textures:

```css
.noise-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.05;
  mix-blend-mode: overlay;
  pointer-events: none;
}
```

See [references/grain-texture-patterns.md](references/grain-texture-patterns.md) for:
- CSS noise texture patterns
- SVG noise filters (fine, medium, coarse, colored)
- Film grain effects (Kodak warm, Fuji cool, vintage)
- Animated grain (flicker, drift, pulse)
- Noise overlays (full-page, hover, masked)
- Texture combinations (paper, glass+grain, metallic)
- React/JS integration patterns

## Effect Intensity Guidelines

**Blur Values:**
- Subtle: `blur(4px)` - barely perceptible softness
- Soft: `blur(12px)` - gentle dream-like quality
- Medium: `blur(20px)` - clear glassmorphism
- Heavy: `blur(40px)` - strong frosted effect
- Extreme: `blur(80px)` - maximum diffusion for backgrounds

**Grain Opacity:**
- `0.03-0.04`: Barely visible warmth
- `0.05-0.06`: Subtle texture
- `0.08-0.10`: Noticeable film grain
- `0.12-0.15`: Strong vintage effect

**Gradient Opacity:**
- `0.1-0.2`: Subtle tint
- `0.3-0.4`: Soft atmosphere
- `0.5-0.6`: Prominent haze

## Combining Effects

Layer blur, grain, and glow for rich atmospheric compositions:

```css
/* Dreamy glass with grain */
.atmospheric-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  position: relative;
}

/* Add subtle grain */
.atmospheric-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,...");
  opacity: 0.04;
  mix-blend-mode: overlay;
  pointer-events: none;
  border-radius: inherit;
}

/* Optional: ambient glow */
.atmospheric-card::before {
  content: '';
  position: absolute;
  inset: -20px;
  background: inherit;
  filter: blur(40px);
  opacity: 0.3;
  z-index: -1;
}
```

## Performance Checklist

- [ ] Use `will-change: transform, opacity` on animated elements
- [ ] Limit `backdrop-filter` usage - expensive on mobile
- [ ] Prefer SVG noise over canvas for static grain
- [ ] Use `steps()` timing for animated grain to reduce renders
- [ ] Test on Safari - webkit prefix required for backdrop-filter
- [ ] Provide fallbacks for `@supports not (backdrop-filter: blur())`
- [ ] Respect `prefers-reduced-motion` and `prefers-reduced-transparency`
- [ ] Keep grain `numOctaves` at 2-3 for performance

## Anti-Patterns to Avoid

- **Over-blurring**: Don't blur everything; use it to create visual hierarchy
- **Excessive grain**: Film texture should be felt, not seen
- **Opacity stacking**: Multiple transparent layers multiply opacity issues
- **Mobile blindness**: Test blur/filter effects on real mobile devices
- **Accessibility neglect**: Ensure sufficient contrast through blur layers
- **Animation overload**: Animated grain should be subtle, not distracting

## Implementation Flow

1. **Define atmosphere** → Choose warm/cool palette, blur intensity, grain character
2. **Layer background** → Set base gradient, add floating color orbs if needed
3. **Add blur** → Apply backdrop-filter to cards/modals, background blur to heroes
4. **Apply grain** → Subtle noise overlay on page or specific sections
5. **Enhance with glow** → Diffuse glow on featured elements
6. **Optimize** → Test performance, add fallbacks
7. **Validate accessibility** → Check contrast, reduced motion support
