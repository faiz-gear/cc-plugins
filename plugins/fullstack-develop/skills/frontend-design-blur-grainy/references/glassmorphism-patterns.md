# Glassmorphism 2.0 Patterns

## Table of Contents
1. [Core Glassmorphism](#core-glassmorphism)
2. [Advanced Glass Variants](#advanced-glass-variants)
3. [Glass Cards](#glass-cards)
4. [Glass Navigation](#glass-navigation)
5. [Glass Modals](#glass-modals)
6. [Glass Input Fields](#glass-input-fields)
7. [Layered Glass Depth](#layered-glass-depth)

## Core Glassmorphism

```css
/* Foundation glass effect */
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
}

/* Variables for consistent glass theming */
:root {
  --glass-bg: rgba(255, 255, 255, 0.1);
  --glass-blur: 20px;
  --glass-saturate: 180%;
  --glass-border: rgba(255, 255, 255, 0.2);
  --glass-shadow: rgba(0, 0, 0, 0.1);
  --glass-radius: 16px;
}

.glass-base {
  background: var(--glass-bg);
  backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturate));
  -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(var(--glass-saturate));
  border: 1px solid var(--glass-border);
  border-radius: var(--glass-radius);
  box-shadow: 0 8px 32px var(--glass-shadow);
}
```

## Advanced Glass Variants

```css
/* Tinted glass - pastel hues */
.glass-pink {
  background: rgba(255, 182, 193, 0.15);
  backdrop-filter: blur(20px) saturate(150%);
  border: 1px solid rgba(255, 182, 193, 0.25);
}

.glass-blue {
  background: rgba(173, 216, 230, 0.15);
  backdrop-filter: blur(20px) saturate(150%);
  border: 1px solid rgba(173, 216, 230, 0.25);
}

.glass-purple {
  background: rgba(221, 160, 221, 0.15);
  backdrop-filter: blur(20px) saturate(150%);
  border: 1px solid rgba(221, 160, 221, 0.25);
}

.glass-mint {
  background: rgba(152, 251, 152, 0.12);
  backdrop-filter: blur(20px) saturate(150%);
  border: 1px solid rgba(152, 251, 152, 0.2);
}

/* Gradient glass */
.glass-gradient {
  background: linear-gradient(
    135deg,
    rgba(255, 182, 193, 0.15) 0%,
    rgba(173, 216, 230, 0.15) 100%
  );
  backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Iridescent glass */
.glass-iridescent {
  background: linear-gradient(
    135deg,
    rgba(255, 182, 255, 0.1) 0%,
    rgba(182, 255, 255, 0.1) 50%,
    rgba(255, 255, 182, 0.1) 100%
  );
  backdrop-filter: blur(24px) saturate(200%);
  border: 1px solid;
  border-image: linear-gradient(
    135deg,
    rgba(255, 182, 255, 0.3),
    rgba(182, 255, 255, 0.3),
    rgba(255, 255, 182, 0.3)
  ) 1;
}

/* Dark glass for dark mode */
.glass-dark {
  background: rgba(15, 15, 25, 0.7);
  backdrop-filter: blur(20px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
}

/* Frosted acrylic (Windows-style) */
.glass-acrylic {
  background: rgba(255, 255, 255, 0.5);
  backdrop-filter: blur(40px) saturate(125%);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

/* Mica-style subtle glass */
.glass-mica {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(100px) saturate(100%);
  border: 1px solid rgba(255, 255, 255, 0.05);
}
```

## Glass Cards

```css
/* Standard glass card */
.glass-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  padding: 24px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

/* Hover lift effect */
.glass-card-hover {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.glass-card-hover:hover {
  transform: translateY(-8px);
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

/* Glass card with inner glow */
.glass-card-glow {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.1),
    inset 0 0 30px rgba(255, 255, 255, 0.1);
}

/* Stacked glass cards */
.glass-stack {
  position: relative;
}

.glass-stack::before,
.glass-stack::after {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: inherit;
  z-index: -1;
}

.glass-stack::before {
  transform: translateY(8px) scale(0.95);
}

.glass-stack::after {
  transform: translateY(16px) scale(0.9);
  z-index: -2;
}

/* Feature card with gradient border */
.glass-card-gradient-border {
  position: relative;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 24px;
}

.glass-card-gradient-border::before {
  content: '';
  position: absolute;
  inset: -1px;
  background: linear-gradient(
    135deg,
    rgba(255, 182, 193, 0.5),
    rgba(173, 216, 230, 0.5),
    rgba(221, 160, 221, 0.5)
  );
  border-radius: inherit;
  z-index: -1;
  mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  mask-composite: exclude;
  padding: 1px;
}
```

## Glass Navigation

```css
/* Top navigation bar */
.glass-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.15);
  padding: 16px 24px;
  z-index: 1000;
}

/* Pill navigation */
.glass-nav-pill {
  display: inline-flex;
  gap: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 100px;
  padding: 6px;
}

.glass-nav-pill button {
  padding: 10px 20px;
  border: none;
  border-radius: 100px;
  background: transparent;
  color: inherit;
  cursor: pointer;
  transition: background 0.2s ease;
}

.glass-nav-pill button.active,
.glass-nav-pill button:hover {
  background: rgba(255, 255, 255, 0.2);
}

/* Side navigation */
.glass-sidebar {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 280px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(24px) saturate(150%);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  padding: 24px;
}

/* Floating action menu */
.glass-fab-menu {
  position: fixed;
  bottom: 24px;
  right: 24px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.glass-fab {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease, background 0.2s ease;
}

.glass-fab:hover {
  transform: scale(1.1);
  background: rgba(255, 255, 255, 0.25);
}
```

## Glass Modals

```css
/* Modal overlay */
.glass-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

/* Modal content */
.glass-modal {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(24px) saturate(180%);
  -webkit-backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 32px;
  padding: 32px;
  max-width: 500px;
  width: 90%;
  box-shadow:
    0 24px 48px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
}

/* Drawer modal */
.glass-drawer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(24px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 32px 32px 0 0;
  padding: 24px;
  transform: translateY(100%);
  transition: transform 0.3s ease;
}

.glass-drawer.open {
  transform: translateY(0);
}

/* Notification toast */
.glass-toast {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 16px 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}
```

## Glass Input Fields

```css
/* Text input */
.glass-input {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 14px 18px;
  color: inherit;
  font-size: 16px;
  outline: none;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.glass-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

.glass-input:focus {
  border-color: rgba(255, 255, 255, 0.4);
  box-shadow: 0 0 0 4px rgba(255, 255, 255, 0.1);
}

/* Search input with icon */
.glass-search {
  position: relative;
}

.glass-search input {
  width: 100%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 100px;
  padding: 14px 18px 14px 48px;
}

.glass-search .icon {
  position: absolute;
  left: 18px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0.6;
}

/* Textarea */
.glass-textarea {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 16px;
  padding: 16px;
  min-height: 120px;
  resize: vertical;
}

/* Select dropdown */
.glass-select {
  appearance: none;
  background: rgba(255, 255, 255, 0.1) url("data:image/svg+xml,...") no-repeat right 16px center;
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  padding: 14px 48px 14px 18px;
  cursor: pointer;
}

/* Toggle switch */
.glass-toggle {
  width: 56px;
  height: 32px;
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 100px;
  position: relative;
  cursor: pointer;
  transition: background 0.2s ease;
}

.glass-toggle::after {
  content: '';
  position: absolute;
  top: 4px;
  left: 4px;
  width: 22px;
  height: 22px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.glass-toggle.active {
  background: rgba(100, 200, 255, 0.4);
}

.glass-toggle.active::after {
  transform: translateX(24px);
}
```

## Layered Glass Depth

```css
/* Multi-layer glass composition */
.glass-layered {
  position: relative;
}

.glass-layer-1 {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(60px);
  border-radius: 32px;
  z-index: 1;
}

.glass-layer-2 {
  position: absolute;
  inset: 20px;
  background: rgba(255, 255, 255, 0.06);
  backdrop-filter: blur(40px);
  border-radius: 24px;
  z-index: 2;
}

.glass-layer-3 {
  position: absolute;
  inset: 40px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  z-index: 3;
}

/* Glass with depth shadow */
.glass-depth {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 24px;
  box-shadow:
    0 4px 8px rgba(0, 0, 0, 0.05),
    0 8px 16px rgba(0, 0, 0, 0.05),
    0 16px 32px rgba(0, 0, 0, 0.08),
    0 32px 64px rgba(0, 0, 0, 0.1);
}

/* Floating glass panels */
.glass-float-container {
  perspective: 1000px;
}

.glass-float-panel {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 20px;
  transform: translateZ(50px);
  transform-style: preserve-3d;
  transition: transform 0.3s ease;
}

.glass-float-panel:hover {
  transform: translateZ(80px) rotateX(5deg);
}

/* Nested glass containers */
.glass-nest-outer {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(30px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 32px;
  padding: 24px;
}

.glass-nest-inner {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  padding: 20px;
}
```

## Browser Support & Fallbacks

```css
/* Feature detection fallback */
@supports not (backdrop-filter: blur(20px)) {
  .glass {
    background: rgba(255, 255, 255, 0.85);
  }
}

/* Safari-specific fixes */
@supports (-webkit-backdrop-filter: blur(20px)) {
  .glass {
    -webkit-backdrop-filter: blur(20px) saturate(180%);
  }
}

/* Reduced transparency for accessibility */
@media (prefers-reduced-transparency: reduce) {
  .glass {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: none;
  }
}
```
