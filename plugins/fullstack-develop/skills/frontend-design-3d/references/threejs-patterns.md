# Three.js / WebGL Patterns Reference

## Table of Contents
1. [Basic Scene Setup](#basic-scene-setup)
2. [React Three Fiber Setup](#react-three-fiber-setup)
3. [Lighting Techniques](#lighting-techniques)
4. [Materials & Textures](#materials--textures)
5. [Product Showcase 360°](#product-showcase-360)
6. [Particle Systems](#particle-systems)
7. [Scroll-Driven Animations](#scroll-driven-animations)
8. [Post-Processing Effects](#post-processing-effects)
9. [Performance Optimization](#performance-optimization)

## Basic Scene Setup

```javascript
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Scene
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a0a0a);

// Camera
const camera = new THREE.PerspectiveCamera(
  75, // FOV
  window.innerWidth / window.innerHeight, // Aspect
  0.1, // Near
  1000 // Far
);
camera.position.set(0, 2, 5);

// Renderer
const renderer = new THREE.WebGLRenderer({
  antialias: true,
  alpha: true, // Transparent background
  powerPreference: 'high-performance'
});
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
document.body.appendChild(renderer.domElement);

// Controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.maxPolarAngle = Math.PI / 2;

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();

// Resize handler
window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

## React Three Fiber Setup

```jsx
import { Canvas, useFrame, useThree } from '@react-three/fiber';
import { OrbitControls, Environment, PerspectiveCamera } from '@react-three/drei';
import { useRef } from 'react';

function Scene() {
  return (
    <Canvas
      shadows
      dpr={[1, 2]}
      gl={{
        antialias: true,
        toneMapping: THREE.ACESFilmicToneMapping,
        toneMappingExposure: 1.0
      }}
    >
      <PerspectiveCamera makeDefault position={[0, 2, 5]} fov={75} />
      <OrbitControls enableDamping dampingFactor={0.05} />

      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 5]} intensity={1} castShadow />

      {/* Environment map for reflections */}
      <Environment preset="city" />

      {/* Your 3D content */}
      <AnimatedBox />
    </Canvas>
  );
}

function AnimatedBox() {
  const meshRef = useRef();

  useFrame((state, delta) => {
    meshRef.current.rotation.y += delta * 0.5;
  });

  return (
    <mesh ref={meshRef} castShadow>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#6366f1" metalness={0.5} roughness={0.2} />
    </mesh>
  );
}
```

## Lighting Techniques

### Three-Point Lighting (Product Photography)

```javascript
// Key Light - Main illumination
const keyLight = new THREE.DirectionalLight(0xffffff, 1);
keyLight.position.set(5, 5, 5);
keyLight.castShadow = true;
keyLight.shadow.mapSize.set(2048, 2048);
scene.add(keyLight);

// Fill Light - Soften shadows
const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
fillLight.position.set(-5, 3, 5);
scene.add(fillLight);

// Back Light - Edge definition
const backLight = new THREE.DirectionalLight(0xffffff, 0.3);
backLight.position.set(0, 5, -5);
scene.add(backLight);
```

### Dramatic Lighting

```javascript
// Single spotlight for drama
const spotlight = new THREE.SpotLight(0xffffff, 2);
spotlight.position.set(0, 10, 0);
spotlight.angle = Math.PI / 6;
spotlight.penumbra = 0.5;
spotlight.castShadow = true;
scene.add(spotlight);

// Colored rim lights
const rimLight1 = new THREE.PointLight(0x6366f1, 1, 10);
rimLight1.position.set(-3, 2, -3);
scene.add(rimLight1);

const rimLight2 = new THREE.PointLight(0xf43f5e, 1, 10);
rimLight2.position.set(3, 2, -3);
scene.add(rimLight2);
```

### React Three Fiber Lighting

```jsx
import { Environment, Lightformer, ContactShadows } from '@react-three/drei';

<>
  {/* HDRI Environment */}
  <Environment preset="studio" background blur={0.5}>
    {/* Custom light formers */}
    <Lightformer
      position={[0, 5, -5]}
      scale={[10, 5, 1]}
      intensity={2}
      color="#6366f1"
    />
  </Environment>

  {/* Soft contact shadows */}
  <ContactShadows
    position={[0, -0.5, 0]}
    opacity={0.5}
    scale={10}
    blur={2}
    far={4}
  />
</>
```

## Materials & Textures

### Physical Materials

```javascript
// Realistic PBR Material
const material = new THREE.MeshPhysicalMaterial({
  color: 0xffffff,
  metalness: 0.9,
  roughness: 0.1,
  clearcoat: 1.0,
  clearcoatRoughness: 0.1,
  reflectivity: 1,
  envMapIntensity: 1,
  transmission: 0, // For glass
  thickness: 0.5,  // For glass
  ior: 1.5         // For glass
});

// Glass material
const glassMaterial = new THREE.MeshPhysicalMaterial({
  color: 0xffffff,
  metalness: 0,
  roughness: 0,
  transmission: 0.95,
  thickness: 0.5,
  ior: 1.5,
  envMapIntensity: 1
});
```

### Texture Loading

```javascript
const textureLoader = new THREE.TextureLoader();

// Load all maps
const colorMap = textureLoader.load('/textures/color.jpg');
const normalMap = textureLoader.load('/textures/normal.jpg');
const roughnessMap = textureLoader.load('/textures/roughness.jpg');
const aoMap = textureLoader.load('/textures/ao.jpg');

// Apply to material
const material = new THREE.MeshStandardMaterial({
  map: colorMap,
  normalMap: normalMap,
  roughnessMap: roughnessMap,
  aoMap: aoMap,
  aoMapIntensity: 1
});

// Texture settings
colorMap.colorSpace = THREE.SRGBColorSpace;
[colorMap, normalMap, roughnessMap, aoMap].forEach(tex => {
  tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
  tex.repeat.set(2, 2);
});
```

### React Three Fiber Textures

```jsx
import { useTexture } from '@react-three/drei';

function TexturedMesh() {
  const [colorMap, normalMap, roughnessMap] = useTexture([
    '/textures/color.jpg',
    '/textures/normal.jpg',
    '/textures/roughness.jpg'
  ]);

  return (
    <mesh>
      <sphereGeometry args={[1, 64, 64]} />
      <meshStandardMaterial
        map={colorMap}
        normalMap={normalMap}
        roughnessMap={roughnessMap}
      />
    </mesh>
  );
}
```

## Product Showcase 360°

### Auto-Rotating Model

```jsx
import { useGLTF, OrbitControls, Stage } from '@react-three/drei';
import { useRef } from 'react';

function ProductViewer({ modelPath }) {
  const { scene } = useGLTF(modelPath);
  const groupRef = useRef();

  useFrame((state, delta) => {
    groupRef.current.rotation.y += delta * 0.3;
  });

  return (
    <group ref={groupRef}>
      <primitive object={scene} />
    </group>
  );
}

// Usage with Stage for automatic lighting
function App() {
  return (
    <Canvas>
      <Stage environment="city" intensity={0.5}>
        <ProductViewer modelPath="/models/product.glb" />
      </Stage>
      <OrbitControls
        autoRotate
        autoRotateSpeed={1}
        enableZoom={true}
        minDistance={2}
        maxDistance={10}
      />
    </Canvas>
  );
}
```

### Interactive Hotspots

```jsx
import { Html } from '@react-three/drei';

function Hotspot({ position, label, description }) {
  const [hovered, setHovered] = useState(false);

  return (
    <group position={position}>
      <mesh
        onPointerOver={() => setHovered(true)}
        onPointerOut={() => setHovered(false)}
      >
        <sphereGeometry args={[0.05, 16, 16]} />
        <meshBasicMaterial color={hovered ? '#f43f5e' : '#6366f1'} />
      </mesh>

      {hovered && (
        <Html distanceFactor={10}>
          <div className="hotspot-tooltip">
            <h4>{label}</h4>
            <p>{description}</p>
          </div>
        </Html>
      )}
    </group>
  );
}
```

## Particle Systems

### Floating Particles

```jsx
import { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function FloatingParticles({ count = 500 }) {
  const meshRef = useRef();

  const particles = useMemo(() => {
    const positions = new Float32Array(count * 3);
    const scales = new Float32Array(count);

    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 20;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
      scales[i] = Math.random();
    }

    return { positions, scales };
  }, [count]);

  useFrame((state) => {
    const time = state.clock.elapsedTime;
    const positions = meshRef.current.geometry.attributes.position.array;

    for (let i = 0; i < count; i++) {
      const i3 = i * 3;
      positions[i3 + 1] += Math.sin(time + i * 0.1) * 0.002;
    }

    meshRef.current.geometry.attributes.position.needsUpdate = true;
  });

  return (
    <points ref={meshRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={particles.positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.05}
        color="#6366f1"
        transparent
        opacity={0.8}
        sizeAttenuation
      />
    </points>
  );
}
```

### Galaxy Effect

```javascript
function createGalaxy() {
  const parameters = {
    count: 100000,
    size: 0.01,
    radius: 5,
    branches: 3,
    spin: 1,
    randomness: 0.2,
    randomnessPower: 3,
    insideColor: '#ff6030',
    outsideColor: '#1b3984'
  };

  const positions = new Float32Array(parameters.count * 3);
  const colors = new Float32Array(parameters.count * 3);

  const colorInside = new THREE.Color(parameters.insideColor);
  const colorOutside = new THREE.Color(parameters.outsideColor);

  for (let i = 0; i < parameters.count; i++) {
    const i3 = i * 3;
    const radius = Math.random() * parameters.radius;
    const spinAngle = radius * parameters.spin;
    const branchAngle = (i % parameters.branches) / parameters.branches * Math.PI * 2;

    const randomX = Math.pow(Math.random(), parameters.randomnessPower) * (Math.random() < 0.5 ? 1 : -1) * parameters.randomness * radius;
    const randomY = Math.pow(Math.random(), parameters.randomnessPower) * (Math.random() < 0.5 ? 1 : -1) * parameters.randomness * radius;
    const randomZ = Math.pow(Math.random(), parameters.randomnessPower) * (Math.random() < 0.5 ? 1 : -1) * parameters.randomness * radius;

    positions[i3] = Math.cos(branchAngle + spinAngle) * radius + randomX;
    positions[i3 + 1] = randomY;
    positions[i3 + 2] = Math.sin(branchAngle + spinAngle) * radius + randomZ;

    const mixedColor = colorInside.clone();
    mixedColor.lerp(colorOutside, radius / parameters.radius);

    colors[i3] = mixedColor.r;
    colors[i3 + 1] = mixedColor.g;
    colors[i3 + 2] = mixedColor.b;
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

  const material = new THREE.PointsMaterial({
    size: parameters.size,
    sizeAttenuation: true,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    vertexColors: true
  });

  return new THREE.Points(geometry, material);
}
```

## Scroll-Driven Animations

```jsx
import { useScroll, ScrollControls, useGLTF } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

function ScrollScene() {
  return (
    <Canvas>
      <ScrollControls pages={5} damping={0.25}>
        <ScrollAnimatedModel />
      </ScrollControls>
    </Canvas>
  );
}

function ScrollAnimatedModel() {
  const scroll = useScroll();
  const { scene } = useGLTF('/model.glb');
  const groupRef = useRef();

  useFrame(() => {
    const offset = scroll.offset; // 0 to 1

    // Rotate based on scroll
    groupRef.current.rotation.y = offset * Math.PI * 2;

    // Move along path
    groupRef.current.position.y = Math.sin(offset * Math.PI) * 2;
    groupRef.current.position.z = -offset * 10;

    // Scale at midpoint
    const scale = 1 + Math.sin(offset * Math.PI) * 0.5;
    groupRef.current.scale.setScalar(scale);
  });

  return (
    <group ref={groupRef}>
      <primitive object={scene} />
    </group>
  );
}
```

## Post-Processing Effects

```jsx
import { EffectComposer, Bloom, ChromaticAberration, Vignette, DepthOfField } from '@react-three/postprocessing';
import { BlendFunction } from 'postprocessing';

function PostProcessing() {
  return (
    <EffectComposer>
      {/* Glow effect */}
      <Bloom
        luminanceThreshold={0.2}
        luminanceSmoothing={0.9}
        intensity={1.5}
      />

      {/* RGB split at edges */}
      <ChromaticAberration
        offset={[0.002, 0.002]}
        blendFunction={BlendFunction.NORMAL}
      />

      {/* Depth blur */}
      <DepthOfField
        focusDistance={0}
        focalLength={0.02}
        bokehScale={2}
      />

      {/* Dark corners */}
      <Vignette
        offset={0.3}
        darkness={0.9}
        blendFunction={BlendFunction.NORMAL}
      />
    </EffectComposer>
  );
}
```

## Performance Optimization

```jsx
// 1. Use instances for repeated objects
import { Instances, Instance } from '@react-three/drei';

function OptimizedCubes({ count = 1000 }) {
  return (
    <Instances limit={count}>
      <boxGeometry />
      <meshStandardMaterial />
      {Array.from({ length: count }, (_, i) => (
        <Instance
          key={i}
          position={[Math.random() * 10, Math.random() * 10, Math.random() * 10]}
          rotation={[Math.random(), Math.random(), 0]}
        />
      ))}
    </Instances>
  );
}

// 2. Level of Detail
import { Detailed } from '@react-three/drei';

<Detailed distances={[0, 50, 100]}>
  <HighDetailModel />  {/* Close */}
  <MediumDetailModel /> {/* Medium */}
  <LowDetailModel />    {/* Far */}
</Detailed>

// 3. Lazy loading
import { Suspense } from 'react';
import { useGLTF } from '@react-three/drei';

useGLTF.preload('/model.glb');

<Suspense fallback={<LoadingPlaceholder />}>
  <Model />
</Suspense>

// 4. Adaptive performance
import { PerformanceMonitor, AdaptiveDpr } from '@react-three/drei';

<Canvas>
  <PerformanceMonitor
    onDecline={() => setDpr(1)}
    onIncline={() => setDpr(2)}
  />
  <AdaptiveDpr pixelated />
</Canvas>
```

### Memory Management

```javascript
// Dispose of geometries and materials when removing objects
function disposeObject(object) {
  object.traverse((child) => {
    if (child.geometry) {
      child.geometry.dispose();
    }
    if (child.material) {
      if (Array.isArray(child.material)) {
        child.material.forEach(mat => mat.dispose());
      } else {
        child.material.dispose();
      }
    }
  });
}

// In React
useEffect(() => {
  return () => {
    // Cleanup on unmount
    disposeObject(meshRef.current);
  };
}, []);
```
