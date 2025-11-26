# Blur & Soft Gradient Patterns

## Table of Contents
1. [Core Blur Properties](#core-blur-properties)
2. [Soft Gradient Techniques](#soft-gradient-techniques)
3. [Dreamy Background Blur](#dreamy-background-blur)
4. [Frosted Glass Effect](#frosted-glass-effect)
5. [Diffuse Glow Effects](#diffuse-glow-effects)
6. [Pastel Haze Overlays](#pastel-haze-overlays)
7. [Soft-Focus Neon](#soft-focus-neon)

## Core Blur Properties

```css
/* Backdrop blur - blurs content behind element */
.backdrop-blur {
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* Filter blur - blurs the element itself */
.element-blur {
  filter: blur(8px);
}

/* Blur intensity scale */
.blur-subtle { backdrop-filter: blur(4px); }   /* Barely perceptible */
.blur-soft { backdrop-filter: blur(12px); }    /* Soft dream-like */
.blur-medium { backdrop-filter: blur(20px); }  /* Clear glassmorphism */
.blur-heavy { backdrop-filter: blur(40px); }   /* Strong frosted effect */
.blur-extreme { backdrop-filter: blur(80px); } /* Maximum diffusion */
```

## Soft Gradient Techniques

```css
/* Pastel gradient - soft, airy feel */
.gradient-pastel {
  background: linear-gradient(
    135deg,
    rgba(255, 182, 193, 0.6) 0%,    /* Soft pink */
    rgba(176, 224, 230, 0.6) 50%,   /* Powder blue */
    rgba(221, 160, 221, 0.6) 100%   /* Plum */
  );
}

/* Aurora gradient - ethereal northern lights */
.gradient-aurora {
  background: linear-gradient(
    to bottom right,
    rgba(120, 200, 255, 0.4),
    rgba(160, 120, 255, 0.3),
    rgba(255, 120, 200, 0.4)
  );
}

/* Mesh gradient with multiple points */
.gradient-mesh {
  background:
    radial-gradient(at 20% 30%, rgba(255, 182, 193, 0.8) 0%, transparent 50%),
    radial-gradient(at 80% 20%, rgba(173, 216, 230, 0.8) 0%, transparent 50%),
    radial-gradient(at 60% 80%, rgba(221, 160, 221, 0.8) 0%, transparent 50%),
    radial-gradient(at 30% 70%, rgba(255, 218, 185, 0.8) 0%, transparent 50%);
  background-color: #f8f9ff;
}

/* Soft radial fade */
.gradient-radial-soft {
  background: radial-gradient(
    ellipse at center,
    rgba(255, 255, 255, 0.9) 0%,
    rgba(240, 240, 255, 0.6) 40%,
    rgba(220, 220, 240, 0.3) 70%,
    transparent 100%
  );
}

/* Multi-stop soft transition */
.gradient-soft-transition {
  background: linear-gradient(
    180deg,
    rgba(255, 245, 250, 1) 0%,
    rgba(250, 240, 255, 0.9) 25%,
    rgba(240, 248, 255, 0.8) 50%,
    rgba(245, 240, 255, 0.7) 75%,
    rgba(255, 250, 245, 0.6) 100%
  );
}
```

## Dreamy Background Blur

```css
/* Full-page dreamy background */
.dreamy-bg {
  position: relative;
  background: linear-gradient(135deg, #ffeef8 0%, #f0f8ff 100%);
}

.dreamy-bg::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 50%, rgba(255, 182, 255, 0.3) 0%, transparent 40%),
    radial-gradient(circle at 80% 30%, rgba(182, 255, 255, 0.3) 0%, transparent 40%),
    radial-gradient(circle at 50% 80%, rgba(255, 255, 182, 0.3) 0%, transparent 40%);
  filter: blur(60px);
  z-index: -1;
}

/* Animated gradient orbs */
.floating-orbs {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: float-orb 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: rgba(255, 105, 180, 0.4);
  top: -100px;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 500px;
  height: 500px;
  background: rgba(64, 224, 208, 0.4);
  top: 50%;
  right: -100px;
  animation-delay: -7s;
}

.orb-3 {
  width: 350px;
  height: 350px;
  background: rgba(147, 112, 219, 0.4);
  bottom: -50px;
  left: 30%;
  animation-delay: -14s;
}

@keyframes float-orb {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.05);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.95);
  }
}

/* Blurred hero section */
.hero-blurred {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-blurred::before {
  content: '';
  position: absolute;
  inset: -100px;
  background: url('hero-image.jpg') center/cover;
  filter: blur(30px) saturate(1.2);
  z-index: -1;
  transform: scale(1.1);
}
```

## Frosted Glass Effect

```css
/* Standard frosted glass */
.frosted-glass {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}

/* Warm frosted glass */
.frosted-warm {
  background: rgba(255, 245, 238, 0.25);
  backdrop-filter: blur(16px) saturate(150%);
  -webkit-backdrop-filter: blur(16px) saturate(150%);
  border: 1px solid rgba(255, 200, 150, 0.2);
}

/* Cool frosted glass */
.frosted-cool {
  background: rgba(240, 248, 255, 0.25);
  backdrop-filter: blur(16px) saturate(150%);
  -webkit-backdrop-filter: blur(16px) saturate(150%);
  border: 1px solid rgba(150, 200, 255, 0.2);
}

/* Dark frosted glass */
.frosted-dark {
  background: rgba(20, 20, 30, 0.6);
  backdrop-filter: blur(24px) saturate(120%);
  -webkit-backdrop-filter: blur(24px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.08);
}

/* Layered frosted depth */
.frosted-layered {
  position: relative;
}

.frosted-layered::before {
  content: '';
  position: absolute;
  inset: -2px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(30px);
  border-radius: inherit;
  z-index: -1;
}

.frosted-layered::after {
  content: '';
  position: absolute;
  inset: -4px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(50px);
  border-radius: inherit;
  z-index: -2;
}
```

## Diffuse Glow Effects

```css
/* Soft glow behind element */
.soft-glow {
  position: relative;
}

.soft-glow::before {
  content: '';
  position: absolute;
  inset: -20px;
  background: inherit;
  filter: blur(40px);
  opacity: 0.5;
  z-index: -1;
}

/* Pulsing ambient glow */
.ambient-glow {
  box-shadow:
    0 0 20px rgba(255, 182, 193, 0.3),
    0 0 40px rgba(255, 182, 193, 0.2),
    0 0 60px rgba(255, 182, 193, 0.1);
  animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% {
    box-shadow:
      0 0 20px rgba(255, 182, 193, 0.3),
      0 0 40px rgba(255, 182, 193, 0.2),
      0 0 60px rgba(255, 182, 193, 0.1);
  }
  50% {
    box-shadow:
      0 0 30px rgba(255, 182, 193, 0.4),
      0 0 60px rgba(255, 182, 193, 0.3),
      0 0 90px rgba(255, 182, 193, 0.15);
  }
}

/* Multi-color diffuse glow */
.rainbow-glow {
  position: relative;
}

.rainbow-glow::before {
  content: '';
  position: absolute;
  inset: -30px;
  background: conic-gradient(
    from 0deg,
    rgba(255, 182, 193, 0.4),
    rgba(173, 216, 230, 0.4),
    rgba(221, 160, 221, 0.4),
    rgba(255, 218, 185, 0.4),
    rgba(255, 182, 193, 0.4)
  );
  filter: blur(60px);
  opacity: 0.7;
  z-index: -1;
  animation: rotate-glow 10s linear infinite;
}

@keyframes rotate-glow {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Inner glow effect */
.inner-glow {
  box-shadow:
    inset 0 0 20px rgba(255, 255, 255, 0.3),
    inset 0 0 40px rgba(255, 182, 193, 0.1);
}
```

## Pastel Haze Overlays

```css
/* Haze overlay on images */
.haze-overlay {
  position: relative;
}

.haze-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(255, 240, 245, 0.3) 0%,
    rgba(240, 248, 255, 0.2) 50%,
    rgba(255, 250, 240, 0.3) 100%
  );
  pointer-events: none;
}

/* Dreamy vignette */
.vignette-soft {
  position: relative;
}

.vignette-soft::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at center,
    transparent 40%,
    rgba(255, 240, 245, 0.5) 100%
  );
  pointer-events: none;
}

/* Color-shifting haze */
.haze-animated {
  position: relative;
}

.haze-animated::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    45deg,
    rgba(255, 182, 193, 0.2),
    rgba(173, 216, 230, 0.2),
    rgba(221, 160, 221, 0.2)
  );
  background-size: 200% 200%;
  animation: shift-haze 8s ease-in-out infinite;
  pointer-events: none;
}

@keyframes shift-haze {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}
```

## Soft-Focus Neon

```css
/* Soft neon glow - not harsh */
.neon-soft {
  color: #fff;
  text-shadow:
    0 0 10px currentColor,
    0 0 20px currentColor,
    0 0 40px currentColor;
  filter: blur(0.5px);
}

.neon-soft-pink {
  color: #ff9eb5;
  text-shadow:
    0 0 10px rgba(255, 158, 181, 0.8),
    0 0 30px rgba(255, 158, 181, 0.5),
    0 0 60px rgba(255, 158, 181, 0.3);
}

.neon-soft-blue {
  color: #7ec8ff;
  text-shadow:
    0 0 10px rgba(126, 200, 255, 0.8),
    0 0 30px rgba(126, 200, 255, 0.5),
    0 0 60px rgba(126, 200, 255, 0.3);
}

/* Neon border - soft glow */
.neon-border-soft {
  border: 2px solid rgba(255, 158, 181, 0.6);
  box-shadow:
    0 0 10px rgba(255, 158, 181, 0.4),
    0 0 20px rgba(255, 158, 181, 0.2),
    inset 0 0 10px rgba(255, 158, 181, 0.1);
}

/* Glowing line divider */
.glow-divider {
  height: 2px;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 182, 193, 0.8),
    rgba(173, 216, 230, 0.8),
    transparent
  );
  box-shadow:
    0 0 10px rgba(255, 182, 193, 0.5),
    0 0 20px rgba(173, 216, 230, 0.3);
}

/* Blurred neon shape */
.neon-shape-blur {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #ff6b9d, #c44fff);
  border-radius: 30% 70% 70% 30% / 30% 30% 70% 70%;
  filter: blur(40px);
  opacity: 0.6;
}
```

## Performance Tips

1. **Use `will-change: transform, opacity`** on animated blur elements
2. **Limit backdrop-filter** - expensive on mobile, use sparingly
3. **Prefer opacity over filter** for simple fade effects
4. **Test on Safari** - webkit prefix required for backdrop-filter
5. **Consider reduced motion** - provide alternatives for prefers-reduced-motion
6. **Layer strategically** - don't stack multiple blur effects
