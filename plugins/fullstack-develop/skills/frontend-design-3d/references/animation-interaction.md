# Animation & Interaction Reference

## Table of Contents
1. [GSAP Integration](#gsap-integration)
2. [Framer Motion 3D](#framer-motion-3d)
3. [Scroll Animations](#scroll-animations)
4. [Mouse/Touch Interactions](#mousetouch-interactions)
5. [Gesture Recognition](#gesture-recognition)
6. [State Transitions](#state-transitions)
7. [Loading Animations](#loading-animations)

## GSAP Integration

### Basic 3D Animations

```javascript
import gsap from 'gsap';

// Rotate and move
gsap.to('.cube', {
  rotateX: 360,
  rotateY: 180,
  z: 100,
  duration: 2,
  ease: 'power2.inOut'
});

// Staggered 3D entrance
gsap.from('.card-3d', {
  rotateY: -90,
  opacity: 0,
  z: -200,
  duration: 0.8,
  stagger: 0.1,
  ease: 'back.out(1.7)'
});
```

### GSAP with Three.js

```javascript
import gsap from 'gsap';

// Animate mesh properties
gsap.to(mesh.rotation, {
  x: Math.PI * 2,
  y: Math.PI,
  duration: 2,
  ease: 'elastic.out(1, 0.3)'
});

gsap.to(mesh.position, {
  x: 5,
  y: 2,
  z: -3,
  duration: 1.5,
  ease: 'power3.inOut'
});

gsap.to(mesh.scale, {
  x: 2,
  y: 2,
  z: 2,
  duration: 1,
  ease: 'bounce.out'
});

// Animate material
gsap.to(mesh.material, {
  opacity: 0.5,
  duration: 0.5
});

gsap.to(mesh.material.color, {
  r: 1,
  g: 0,
  b: 0.5,
  duration: 1
});
```

### GSAP ScrollTrigger with 3D

```javascript
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// CSS 3D scroll animation
gsap.to('.hero-3d', {
  scrollTrigger: {
    trigger: '.hero-section',
    start: 'top top',
    end: 'bottom top',
    scrub: 1
  },
  rotateX: 45,
  rotateY: -30,
  z: -500,
  opacity: 0
});

// Three.js with ScrollTrigger
gsap.to(camera.position, {
  scrollTrigger: {
    trigger: 'body',
    start: 'top top',
    end: 'bottom bottom',
    scrub: 1
  },
  x: 10,
  y: 5,
  z: 15,
  onUpdate: () => camera.lookAt(scene.position)
});
```

### Timeline Orchestration

```javascript
const tl = gsap.timeline({
  defaults: { duration: 0.8, ease: 'power3.out' }
});

tl.from('.scene-3d', { opacity: 0, scale: 0.8 })
  .from('.object-1', { rotateY: -180, z: -300 }, '-=0.4')
  .from('.object-2', { rotateX: 90, y: 200 }, '-=0.6')
  .from('.object-3', { scale: 0, z: -100 }, '-=0.4')
  .to('.scene-3d', { rotateY: 15, duration: 1.5 });
```

## Framer Motion 3D

### Basic 3D Transforms

```jsx
import { motion } from 'framer-motion';

function Card3D() {
  return (
    <motion.div
      style={{ transformStyle: 'preserve-3d', perspective: 1000 }}
      initial={{ rotateY: -90, opacity: 0 }}
      animate={{ rotateY: 0, opacity: 1 }}
      transition={{ type: 'spring', stiffness: 100, damping: 15 }}
      whileHover={{
        rotateY: 15,
        rotateX: -10,
        z: 50,
        transition: { duration: 0.3 }
      }}
    >
      <CardContent />
    </motion.div>
  );
}
```

### Gesture-Based 3D

```jsx
import { motion, useMotionValue, useTransform } from 'framer-motion';

function TiltCard() {
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const rotateX = useTransform(y, [-100, 100], [30, -30]);
  const rotateY = useTransform(x, [-100, 100], [-30, 30]);

  function handleMouse(event) {
    const rect = event.currentTarget.getBoundingClientRect();
    x.set(event.clientX - rect.left - rect.width / 2);
    y.set(event.clientY - rect.top - rect.height / 2);
  }

  return (
    <motion.div
      style={{
        perspective: 1000,
        transformStyle: 'preserve-3d',
        rotateX,
        rotateY
      }}
      onMouseMove={handleMouse}
      onMouseLeave={() => {
        x.set(0);
        y.set(0);
      }}
    >
      <CardContent />
    </motion.div>
  );
}
```

### 3D Flip Animation

```jsx
import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';

function FlipCard() {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div
      style={{ perspective: 1000 }}
      onClick={() => setIsFlipped(!isFlipped)}
    >
      <motion.div
        style={{ transformStyle: 'preserve-3d' }}
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.6, type: 'spring', stiffness: 100 }}
      >
        <motion.div
          style={{
            position: 'absolute',
            backfaceVisibility: 'hidden',
            width: '100%',
            height: '100%'
          }}
        >
          <FrontFace />
        </motion.div>

        <motion.div
          style={{
            position: 'absolute',
            backfaceVisibility: 'hidden',
            rotateY: 180,
            width: '100%',
            height: '100%'
          }}
        >
          <BackFace />
        </motion.div>
      </motion.div>
    </div>
  );
}
```

### Framer Motion 3D with React Three Fiber

```jsx
import { motion } from 'framer-motion-3d';
import { Canvas } from '@react-three/fiber';

function AnimatedScene() {
  return (
    <Canvas>
      <motion.mesh
        initial={{ scale: 0, rotateY: -Math.PI }}
        animate={{ scale: 1, rotateY: 0 }}
        transition={{ type: 'spring', duration: 1.5 }}
        whileHover={{ scale: 1.2 }}
        whileTap={{ scale: 0.9 }}
      >
        <boxGeometry />
        <meshStandardMaterial color="#6366f1" />
      </motion.mesh>
    </Canvas>
  );
}
```

## Scroll Animations

### Intersection Observer + 3D

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('animate-in-3d');
    }
  });
}, {
  threshold: 0.2,
  rootMargin: '-50px'
});

document.querySelectorAll('.scroll-3d').forEach(el => {
  observer.observe(el);
});
```

```css
.scroll-3d {
  opacity: 0;
  transform: perspective(1000px) rotateX(45deg) translateY(100px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.scroll-3d.animate-in-3d {
  opacity: 1;
  transform: perspective(1000px) rotateX(0deg) translateY(0);
}
```

### Scroll-Linked Camera Movement

```jsx
import { useScroll } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

function ScrollCamera() {
  const scroll = useScroll();
  const cameraPositions = [
    { x: 0, y: 5, z: 10 },   // Start
    { x: 5, y: 3, z: 8 },    // 25%
    { x: 0, y: 1, z: 5 },    // 50%
    { x: -5, y: 2, z: 8 },   // 75%
    { x: 0, y: 0, z: 3 }     // End
  ];

  useFrame(({ camera }) => {
    const offset = scroll.offset;
    const segment = offset * (cameraPositions.length - 1);
    const index = Math.floor(segment);
    const t = segment - index;

    const from = cameraPositions[Math.min(index, cameraPositions.length - 1)];
    const to = cameraPositions[Math.min(index + 1, cameraPositions.length - 1)];

    camera.position.x = from.x + (to.x - from.x) * t;
    camera.position.y = from.y + (to.y - from.y) * t;
    camera.position.z = from.z + (to.z - from.z) * t;
    camera.lookAt(0, 0, 0);
  });

  return null;
}
```

## Mouse/Touch Interactions

### Mouse Tracking 3D Tilt

```javascript
class TiltEffect {
  constructor(element, options = {}) {
    this.element = element;
    this.maxTilt = options.maxTilt || 15;
    this.perspective = options.perspective || 1000;
    this.speed = options.speed || 300;

    this.element.style.transformStyle = 'preserve-3d';
    this.element.style.transition = `transform ${this.speed}ms ease-out`;

    this.bindEvents();
  }

  bindEvents() {
    this.element.addEventListener('mousemove', this.onMouseMove.bind(this));
    this.element.addEventListener('mouseleave', this.onMouseLeave.bind(this));
  }

  onMouseMove(e) {
    const rect = this.element.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const centerX = rect.width / 2;
    const centerY = rect.height / 2;

    const tiltX = ((y - centerY) / centerY) * -this.maxTilt;
    const tiltY = ((x - centerX) / centerX) * this.maxTilt;

    this.element.style.transform = `
      perspective(${this.perspective}px)
      rotateX(${tiltX}deg)
      rotateY(${tiltY}deg)
      scale3d(1.05, 1.05, 1.05)
    `;
  }

  onMouseLeave() {
    this.element.style.transform = `
      perspective(${this.perspective}px)
      rotateX(0deg)
      rotateY(0deg)
      scale3d(1, 1, 1)
    `;
  }
}

// Usage
new TiltEffect(document.querySelector('.tilt-card'), {
  maxTilt: 20,
  perspective: 1000,
  speed: 400
});
```

### Three.js Raycasting Interactions

```jsx
import { useThree } from '@react-three/fiber';
import { useState } from 'react';

function InteractiveMesh() {
  const [hovered, setHovered] = useState(false);
  const [clicked, setClicked] = useState(false);

  return (
    <mesh
      onPointerOver={(e) => {
        e.stopPropagation();
        setHovered(true);
        document.body.style.cursor = 'pointer';
      }}
      onPointerOut={() => {
        setHovered(false);
        document.body.style.cursor = 'auto';
      }}
      onClick={(e) => {
        e.stopPropagation();
        setClicked(!clicked);
      }}
      scale={hovered ? 1.2 : 1}
    >
      <boxGeometry />
      <meshStandardMaterial color={clicked ? '#f43f5e' : '#6366f1'} />
    </mesh>
  );
}
```

### Drag Rotation

```jsx
import { useDrag } from '@use-gesture/react';
import { useSpring, animated } from '@react-spring/three';

function DraggableMesh() {
  const [spring, api] = useSpring(() => ({
    rotation: [0, 0, 0],
    config: { mass: 1, tension: 170, friction: 26 }
  }));

  const bind = useDrag(({ movement: [mx, my], down }) => {
    api.start({
      rotation: down
        ? [my / 100, mx / 100, 0]
        : [0, 0, 0]
    });
  });

  return (
    <animated.mesh {...bind()} rotation={spring.rotation}>
      <boxGeometry />
      <meshStandardMaterial color="#6366f1" />
    </animated.mesh>
  );
}
```

## Gesture Recognition

### Pinch to Zoom (Touch)

```jsx
import { useGesture } from '@use-gesture/react';
import { useSpring, animated } from '@react-spring/three';

function PinchableModel() {
  const [spring, api] = useSpring(() => ({
    scale: [1, 1, 1],
    config: { mass: 1, tension: 200, friction: 30 }
  }));

  const bind = useGesture({
    onPinch: ({ offset: [scale] }) => {
      api.start({ scale: [scale, scale, scale] });
    }
  });

  return (
    <animated.mesh {...bind()} scale={spring.scale}>
      <boxGeometry />
      <meshStandardMaterial color="#6366f1" />
    </animated.mesh>
  );
}
```

### Swipe Navigation

```javascript
let startX = 0;
let currentSlide = 0;
const threshold = 50;

element.addEventListener('touchstart', (e) => {
  startX = e.touches[0].clientX;
});

element.addEventListener('touchend', (e) => {
  const endX = e.changedTouches[0].clientX;
  const diff = startX - endX;

  if (Math.abs(diff) > threshold) {
    if (diff > 0) {
      // Swipe left - next
      currentSlide = Math.min(currentSlide + 1, maxSlides);
    } else {
      // Swipe right - previous
      currentSlide = Math.max(currentSlide - 1, 0);
    }
    updateCarousel(currentSlide);
  }
});

function updateCarousel(index) {
  const rotation = index * (360 / totalSlides);
  carousel.style.transform = `rotateY(-${rotation}deg)`;
}
```

## State Transitions

### Scene Transitions

```jsx
import { motion, AnimatePresence } from 'framer-motion';

const sceneVariants = {
  initial: { opacity: 0, rotateY: -90, scale: 0.8 },
  enter: {
    opacity: 1,
    rotateY: 0,
    scale: 1,
    transition: { duration: 0.6, ease: [0.4, 0, 0.2, 1] }
  },
  exit: {
    opacity: 0,
    rotateY: 90,
    scale: 0.8,
    transition: { duration: 0.4 }
  }
};

function SceneTransition({ currentScene }) {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={currentScene}
        variants={sceneVariants}
        initial="initial"
        animate="enter"
        exit="exit"
        style={{ perspective: 1000 }}
      >
        {scenes[currentScene]}
      </motion.div>
    </AnimatePresence>
  );
}
```

### Material State Changes

```jsx
import { useSpring, animated } from '@react-spring/three';
import { useState } from 'react';

function StatefulMaterial() {
  const [active, setActive] = useState(false);

  const { color, metalness, roughness } = useSpring({
    color: active ? '#f43f5e' : '#6366f1',
    metalness: active ? 0.9 : 0.1,
    roughness: active ? 0.1 : 0.8,
    config: { tension: 200, friction: 20 }
  });

  return (
    <mesh onClick={() => setActive(!active)}>
      <sphereGeometry args={[1, 64, 64]} />
      <animated.meshStandardMaterial
        color={color}
        metalness={metalness}
        roughness={roughness}
      />
    </mesh>
  );
}
```

## Loading Animations

### 3D Loading Spinner

```css
.loader-3d {
  width: 60px;
  height: 60px;
  perspective: 200px;
}

.loader-cube {
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  animation: spin3d 1.5s ease-in-out infinite;
}

.loader-face {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  opacity: 0.9;
}

.loader-face:nth-child(1) { transform: translateZ(30px); }
.loader-face:nth-child(2) { transform: rotateY(180deg) translateZ(30px); }
.loader-face:nth-child(3) { transform: rotateY(90deg) translateZ(30px); }
.loader-face:nth-child(4) { transform: rotateY(-90deg) translateZ(30px); }
.loader-face:nth-child(5) { transform: rotateX(90deg) translateZ(30px); }
.loader-face:nth-child(6) { transform: rotateX(-90deg) translateZ(30px); }

@keyframes spin3d {
  0% { transform: rotateX(0deg) rotateY(0deg); }
  50% { transform: rotateX(180deg) rotateY(180deg); }
  100% { transform: rotateX(360deg) rotateY(360deg); }
}
```

### Model Loading Progress

```jsx
import { useProgress, Html } from '@react-three/drei';

function Loader() {
  const { progress, active } = useProgress();

  if (!active) return null;

  return (
    <Html center>
      <div className="loader-container">
        <div
          className="loader-bar"
          style={{ width: `${progress}%` }}
        />
        <span>{Math.round(progress)}%</span>
      </div>
    </Html>
  );
}

// Usage
<Suspense fallback={<Loader />}>
  <Model />
</Suspense>
```

### Skeleton 3D Placeholder

```jsx
function SkeletonMesh() {
  const meshRef = useRef();

  useFrame(({ clock }) => {
    meshRef.current.material.opacity = 0.3 + Math.sin(clock.elapsedTime * 2) * 0.2;
  });

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[1, 1, 1]} />
      <meshBasicMaterial
        color="#374151"
        transparent
        opacity={0.5}
        wireframe
      />
    </mesh>
  );
}
```
