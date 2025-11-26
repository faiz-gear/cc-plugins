# Film Texture & Grain Overlay Patterns

## Table of Contents
1. [CSS Noise Texture](#css-noise-texture)
2. [SVG Noise Filters](#svg-noise-filters)
3. [Film Grain Effects](#film-grain-effects)
4. [Animated Grain](#animated-grain)
5. [Noise Overlays](#noise-overlays)
6. [Texture Combinations](#texture-combinations)
7. [React/JS Integration](#reactjs-integration)

## CSS Noise Texture

```css
/* Base64 noise texture - lightweight, performant */
.noise-overlay {
  position: relative;
}

.noise-overlay::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E");
  opacity: 0.05;
  pointer-events: none;
  mix-blend-mode: overlay;
}

/* Adjustable grain intensity */
.grain-subtle::after { opacity: 0.03; }
.grain-light::after { opacity: 0.05; }
.grain-medium::after { opacity: 0.08; }
.grain-heavy::after { opacity: 0.12; }
.grain-strong::after { opacity: 0.18; }

/* Grain color variations */
.grain-warm::after {
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' fill='%23ffeedd'/%3E%3C/svg%3E");
  mix-blend-mode: multiply;
}

.grain-cool::after {
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' fill='%23ddeeff'/%3E%3C/svg%3E");
  mix-blend-mode: multiply;
}
```

## SVG Noise Filters

```html
<!-- Include in HTML, reference in CSS -->
<svg style="display: none;">
  <defs>
    <!-- Fine grain -->
    <filter id="grain-fine">
      <feTurbulence
        type="fractalNoise"
        baseFrequency="0.8"
        numOctaves="4"
        stitchTiles="stitch"
      />
      <feColorMatrix type="saturate" values="0"/>
    </filter>

    <!-- Medium grain -->
    <filter id="grain-medium">
      <feTurbulence
        type="fractalNoise"
        baseFrequency="0.5"
        numOctaves="3"
        stitchTiles="stitch"
      />
      <feColorMatrix type="saturate" values="0"/>
    </filter>

    <!-- Coarse grain (film-like) -->
    <filter id="grain-coarse">
      <feTurbulence
        type="fractalNoise"
        baseFrequency="0.3"
        numOctaves="2"
        stitchTiles="stitch"
      />
      <feColorMatrix type="saturate" values="0"/>
    </filter>

    <!-- Colored noise -->
    <filter id="grain-colored">
      <feTurbulence
        type="fractalNoise"
        baseFrequency="0.6"
        numOctaves="3"
      />
    </filter>

    <!-- Soft noise with blur -->
    <filter id="grain-soft">
      <feTurbulence
        type="fractalNoise"
        baseFrequency="0.7"
        numOctaves="4"
      />
      <feGaussianBlur stdDeviation="0.5"/>
      <feColorMatrix type="saturate" values="0"/>
    </filter>
  </defs>
</svg>
```

```css
/* Apply SVG filters */
.grain-filter-fine {
  position: relative;
}

.grain-filter-fine::after {
  content: '';
  position: absolute;
  inset: 0;
  filter: url(#grain-fine);
  opacity: 0.06;
  pointer-events: none;
  mix-blend-mode: overlay;
}
```

## Film Grain Effects

```css
/* Classic film grain */
.film-grain {
  position: relative;
}

.film-grain::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n' x='0' y='0'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.08;
  mix-blend-mode: overlay;
  pointer-events: none;
}

/* Kodak-style warm grain */
.film-kodak::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"),
    linear-gradient(rgba(255, 240, 220, 0.1), rgba(255, 220, 180, 0.1));
  opacity: 0.1;
  mix-blend-mode: overlay;
  pointer-events: none;
}

/* Fuji-style cool grain */
.film-fuji::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"),
    linear-gradient(rgba(220, 235, 255, 0.1), rgba(200, 220, 255, 0.1));
  opacity: 0.1;
  mix-blend-mode: overlay;
  pointer-events: none;
}

/* Vintage film with vignette */
.film-vintage {
  position: relative;
}

.film-vintage::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.5' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.12;
  mix-blend-mode: multiply;
  pointer-events: none;
}

.film-vintage::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(
    ellipse at center,
    transparent 50%,
    rgba(0, 0, 0, 0.3) 100%
  );
  pointer-events: none;
}

/* High ISO grain */
.film-high-iso::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='5'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.15;
  mix-blend-mode: overlay;
  pointer-events: none;
}
```

## Animated Grain

```css
/* Flickering film grain */
@keyframes grain-flicker {
  0%, 100% { transform: translate(0, 0); }
  10% { transform: translate(-2%, -3%); }
  20% { transform: translate(3%, 2%); }
  30% { transform: translate(-1%, 4%); }
  40% { transform: translate(4%, -2%); }
  50% { transform: translate(-3%, 1%); }
  60% { transform: translate(2%, -4%); }
  70% { transform: translate(-4%, 3%); }
  80% { transform: translate(1%, -1%); }
  90% { transform: translate(-2%, 2%); }
}

.grain-animated {
  position: relative;
  overflow: hidden;
}

.grain-animated::after {
  content: '';
  position: absolute;
  inset: -10%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.07;
  mix-blend-mode: overlay;
  pointer-events: none;
  animation: grain-flicker 0.8s steps(10) infinite;
}

/* Subtle grain movement */
@keyframes grain-drift {
  0% { transform: translate(0, 0); }
  100% { transform: translate(5%, 5%); }
}

.grain-drift::after {
  content: '';
  position: absolute;
  inset: -5%;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 300 300' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.6' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.05;
  mix-blend-mode: overlay;
  pointer-events: none;
  animation: grain-drift 3s linear infinite alternate;
}

/* Pulsing grain opacity */
@keyframes grain-pulse {
  0%, 100% { opacity: 0.05; }
  50% { opacity: 0.08; }
}

.grain-pulse::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  mix-blend-mode: overlay;
  pointer-events: none;
  animation: grain-pulse 4s ease-in-out infinite;
}
```

## Noise Overlays

```css
/* Full-page noise overlay */
.page-noise::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.04;
  mix-blend-mode: overlay;
  pointer-events: none;
  z-index: 9999;
}

/* Noise on hover only */
.noise-hover {
  position: relative;
}

.noise-hover::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0;
  mix-blend-mode: overlay;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

.noise-hover:hover::after {
  opacity: 0.08;
}

/* Noise with gradient blend */
.noise-gradient-blend {
  position: relative;
  background: linear-gradient(135deg, #ffeef8, #f0f8ff);
}

.noise-gradient-blend::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.06;
  mix-blend-mode: soft-light;
  pointer-events: none;
}

/* Masked noise (fades at edges) */
.noise-masked {
  position: relative;
}

.noise-masked::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.08;
  mix-blend-mode: overlay;
  pointer-events: none;
  mask-image: radial-gradient(ellipse at center, black 40%, transparent 80%);
  -webkit-mask-image: radial-gradient(ellipse at center, black 40%, transparent 80%);
}
```

## Texture Combinations

```css
/* Paper texture with grain */
.texture-paper {
  position: relative;
  background: #faf8f5;
}

.texture-paper::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.04' numOctaves='5'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.08;
  mix-blend-mode: multiply;
  pointer-events: none;
}

.texture-paper::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.04;
  mix-blend-mode: overlay;
  pointer-events: none;
}

/* Glass with grain */
.texture-grainy-glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  position: relative;
}

.texture-grainy-glass::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.04;
  mix-blend-mode: overlay;
  pointer-events: none;
  border-radius: inherit;
}

/* Dreamy blur with grain */
.texture-dreamy {
  position: relative;
  background: linear-gradient(135deg, #ffeef8 0%, #f0f8ff 100%);
}

.texture-dreamy::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 30% 40%, rgba(255, 182, 193, 0.4) 0%, transparent 50%),
    radial-gradient(circle at 70% 60%, rgba(173, 216, 230, 0.4) 0%, transparent 50%);
  filter: blur(60px);
}

.texture-dreamy::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.05;
  mix-blend-mode: overlay;
  pointer-events: none;
}

/* Metallic grain */
.texture-metallic {
  background: linear-gradient(135deg, #e8e8e8, #d0d0d0, #e8e8e8);
  position: relative;
}

.texture-metallic::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.12;
  mix-blend-mode: overlay;
  pointer-events: none;
}
```

## React/JS Integration

```jsx
// React component with grain overlay
function GrainOverlay({ intensity = 0.05, animated = false }) {
  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        pointerEvents: 'none',
        zIndex: 9999,
      }}
    >
      <svg style={{ position: 'absolute', width: 0, height: 0 }}>
        <filter id="grain-filter">
          <feTurbulence
            type="fractalNoise"
            baseFrequency="0.65"
            numOctaves="3"
            stitchTiles="stitch"
          />
        </filter>
      </svg>
      <div
        style={{
          position: 'absolute',
          inset: animated ? '-10%' : 0,
          filter: 'url(#grain-filter)',
          opacity: intensity,
          mixBlendMode: 'overlay',
          animation: animated ? 'grain-flicker 0.8s steps(10) infinite' : 'none',
        }}
      />
    </div>
  );
}

// Usage
<GrainOverlay intensity={0.06} animated={true} />
```

```jsx
// Dynamic grain with canvas (high-performance)
function CanvasGrain({ opacity = 0.08 }) {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');

    const resize = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    resize();
    window.addEventListener('resize', resize);

    const imageData = ctx.createImageData(canvas.width, canvas.height);
    const data = imageData.data;

    for (let i = 0; i < data.length; i += 4) {
      const value = Math.random() * 255;
      data[i] = value;
      data[i + 1] = value;
      data[i + 2] = value;
      data[i + 3] = 255;
    }

    ctx.putImageData(imageData, 0, 0);

    return () => window.removeEventListener('resize', resize);
  }, []);

  return (
    <canvas
      ref={canvasRef}
      style={{
        position: 'fixed',
        inset: 0,
        opacity,
        mixBlendMode: 'overlay',
        pointerEvents: 'none',
        zIndex: 9999,
      }}
    />
  );
}
```

```css
/* Include in global CSS for animation */
@keyframes grain-flicker {
  0%, 100% { transform: translate(0, 0); }
  10% { transform: translate(-2%, -3%); }
  20% { transform: translate(3%, 2%); }
  30% { transform: translate(-1%, 4%); }
  40% { transform: translate(4%, -2%); }
  50% { transform: translate(-3%, 1%); }
  60% { transform: translate(2%, -4%); }
  70% { transform: translate(-4%, 3%); }
  80% { transform: translate(1%, -1%); }
  90% { transform: translate(-2%, 2%); }
}
```

## Performance Considerations

1. **SVG filters are GPU-accelerated** - prefer over canvas for static grain
2. **Limit animated grain** - use `steps()` timing to reduce render calls
3. **Reduce `numOctaves`** for better performance (2-3 is usually enough)
4. **Consider `will-change: transform`** for animated overlays
5. **Test on mobile** - noise effects can be heavy on low-end devices
6. **Provide reduced motion alternatives** - respect user preferences
