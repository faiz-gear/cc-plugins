# CSS 3D Transforms Reference

## Table of Contents
1. [Core Properties](#core-properties)
2. [3D Card Flip](#3d-card-flip)
3. [3D Carousel](#3d-carousel)
4. [Parallax Depth Layers](#parallax-depth-layers)
5. [Floating Elements](#floating-elements)
6. [Perspective Text](#perspective-text)
7. [3D Button Effects](#3d-button-effects)
8. [Isometric Grids](#isometric-grids)

## Core Properties

```css
/* Parent container - establishes 3D space */
.scene {
  perspective: 1000px;           /* Distance from viewer - smaller = more dramatic */
  perspective-origin: 50% 50%;   /* Vanishing point */
}

/* Child element - exists in 3D space */
.object {
  transform-style: preserve-3d;  /* Children maintain 3D position */
  transform: rotateX(15deg) rotateY(-20deg) translateZ(50px);
  backface-visibility: hidden;   /* Hide when rotated away */
}
```

**Key transforms:**
- `rotateX(deg)` - Tilt forward/backward
- `rotateY(deg)` - Spin left/right
- `rotateZ(deg)` - Rotate in place
- `translateZ(px)` - Move closer/farther
- `scale3d(x, y, z)` - Scale in 3D

## 3D Card Flip

```html
<div class="card-container">
  <div class="card">
    <div class="card-face card-front">Front Content</div>
    <div class="card-face card-back">Back Content</div>
  </div>
</div>
```

```css
.card-container {
  perspective: 1000px;
  width: 300px;
  height: 400px;
}

.card {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-container:hover .card {
  transform: rotateY(180deg);
}

.card-face {
  position: absolute;
  inset: 0;
  backface-visibility: hidden;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-front {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card-back {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  transform: rotateY(180deg);
}
```

## 3D Carousel

```html
<div class="carousel-scene">
  <div class="carousel">
    <div class="carousel-item" style="--i: 0">Item 1</div>
    <div class="carousel-item" style="--i: 1">Item 2</div>
    <div class="carousel-item" style="--i: 2">Item 3</div>
    <div class="carousel-item" style="--i: 3">Item 4</div>
    <div class="carousel-item" style="--i: 4">Item 5</div>
    <div class="carousel-item" style="--i: 5">Item 6</div>
  </div>
</div>
```

```css
.carousel-scene {
  perspective: 1000px;
  width: 100%;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel {
  --items: 6;
  --radius: 300px;
  position: relative;
  width: 200px;
  height: 300px;
  transform-style: preserve-3d;
  animation: rotate 20s linear infinite;
}

.carousel-item {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 12px;
  transform: rotateY(calc(var(--i) * (360deg / var(--items)))) translateZ(var(--radius));
}

@keyframes rotate {
  from { transform: rotateY(0deg); }
  to { transform: rotateY(360deg); }
}
```

## Parallax Depth Layers

```html
<div class="parallax-container">
  <div class="parallax-layer" data-depth="0.1">Background</div>
  <div class="parallax-layer" data-depth="0.3">Midground</div>
  <div class="parallax-layer" data-depth="0.6">Foreground</div>
</div>
```

```css
.parallax-container {
  perspective: 1000px;
  height: 100vh;
  overflow-x: hidden;
  overflow-y: auto;
  perspective-origin: center center;
}

.parallax-layer {
  position: absolute;
  inset: 0;
  transform-style: preserve-3d;
}

/* Depth levels via translateZ - farther = smaller parallax effect */
.parallax-layer[data-depth="0.1"] {
  transform: translateZ(-900px) scale(10);
}

.parallax-layer[data-depth="0.3"] {
  transform: translateZ(-700px) scale(8);
}

.parallax-layer[data-depth="0.6"] {
  transform: translateZ(-400px) scale(5);
}
```

**Mouse-tracking parallax (JS enhanced):**
```javascript
document.addEventListener('mousemove', (e) => {
  const x = (e.clientX / window.innerWidth - 0.5) * 20;
  const y = (e.clientY / window.innerHeight - 0.5) * 20;

  document.querySelectorAll('.parallax-layer').forEach(layer => {
    const depth = layer.dataset.depth;
    layer.style.transform = `
      translateX(${x * depth}px)
      translateY(${y * depth}px)
      translateZ(${-1000 * (1 - depth)}px)
      scale(${1 + (1 - depth) * 9})
    `;
  });
});
```

## Floating Elements

```css
.floating-element {
  animation: float 6s ease-in-out infinite;
  transform-style: preserve-3d;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotateX(5deg) rotateY(-5deg);
  }
  50% {
    transform: translateY(-20px) rotateX(-5deg) rotateY(5deg);
  }
}

/* Staggered floating */
.floating-element:nth-child(1) { animation-delay: 0s; }
.floating-element:nth-child(2) { animation-delay: -1s; }
.floating-element:nth-child(3) { animation-delay: -2s; }

/* Magnetic hover effect */
.magnetic-3d {
  transition: transform 0.3s ease-out;
}

.magnetic-3d:hover {
  transform: translateZ(30px) scale(1.05);
}
```

## Perspective Text

```css
/* 3D Extruded Text */
.text-3d {
  font-size: 6rem;
  font-weight: 900;
  color: #fff;
  text-shadow:
    1px 1px 0 #ccc,
    2px 2px 0 #c9c9c9,
    3px 3px 0 #bbb,
    4px 4px 0 #b9b9b9,
    5px 5px 0 #aaa,
    6px 6px 1px rgba(0,0,0,.1),
    0 0 5px rgba(0,0,0,.1),
    0 1px 3px rgba(0,0,0,.3),
    0 3px 5px rgba(0,0,0,.2),
    0 5px 10px rgba(0,0,0,.25),
    0 10px 10px rgba(0,0,0,.2),
    0 20px 20px rgba(0,0,0,.15);
}

/* Perspective heading */
.perspective-text {
  transform: perspective(500px) rotateX(15deg);
  transform-origin: center bottom;
}

/* Tilted text wall */
.text-wall {
  transform: perspective(800px) rotateY(-15deg);
  transform-origin: left center;
}
```

## 3D Button Effects

```css
.button-3d {
  position: relative;
  padding: 16px 32px;
  background: linear-gradient(180deg, #6366f1 0%, #4f46e5 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  transform-style: preserve-3d;
  transform: perspective(500px) rotateX(0deg);
  transition: transform 0.3s ease;
}

.button-3d::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, #4338ca 0%, #3730a3 100%);
  border-radius: inherit;
  transform: translateZ(-8px);
  transition: transform 0.3s ease;
}

.button-3d:hover {
  transform: perspective(500px) rotateX(-10deg) translateY(-4px);
}

.button-3d:active {
  transform: perspective(500px) rotateX(-5deg) translateY(-2px);
}

/* Depth shadow button */
.button-depth {
  box-shadow:
    0 4px 0 #3730a3,
    0 6px 10px rgba(0,0,0,0.3);
  transition: all 0.1s ease;
}

.button-depth:active {
  transform: translateY(4px);
  box-shadow:
    0 0 0 #3730a3,
    0 2px 5px rgba(0,0,0,0.3);
}
```

## Isometric Grids

```css
.isometric-container {
  transform: rotateX(60deg) rotateZ(-45deg);
  transform-style: preserve-3d;
}

.isometric-tile {
  width: 100px;
  height: 100px;
  background: #6366f1;
  position: relative;
  transform-style: preserve-3d;
}

/* Side faces */
.isometric-tile::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 40px;
  background: #4338ca;
  transform: rotateX(-90deg);
  transform-origin: bottom;
  top: 100%;
}

.isometric-tile::after {
  content: '';
  position: absolute;
  width: 40px;
  height: 100%;
  background: #3730a3;
  transform: rotateY(90deg);
  transform-origin: left;
  left: 100%;
}

/* Animated height */
.isometric-tile:hover {
  transform: translateZ(20px);
  transition: transform 0.3s ease;
}
```

## Performance Tips

1. **Use `will-change` sparingly** - Only on elements about to animate
2. **Prefer `transform` over position changes** - GPU accelerated
3. **Avoid animating `perspective`** - Expensive to recalculate
4. **Use `contain: paint`** - Isolate repaint areas
5. **Test on mobile** - 3D transforms can be heavy
