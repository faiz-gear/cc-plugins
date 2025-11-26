---
name: frontend-design-3d
description: Create immersive 3D web experiences with realistic textures, depth, and fluid interactions. Use this skill when the user asks to build 3D interfaces, product showcases, 360° viewers, virtual try-ons, parallax effects, floating UI elements, interactive environments, data visualizations with depth, or any web page that should feel spatial and immersive rather than flat.
---

This skill guides creation of immersive 3D web experiences that transform static interfaces into memorable, spatial interactions. Implement real working code with exceptional attention to depth, lighting, motion, and interactivity.

The user provides 3D frontend requirements: a product viewer, immersive landing page, interactive environment, data visualization, or any interface that benefits from depth and spatial design.

## Technology Selection

Choose the right approach based on complexity:

| Use Case | Technology | When to Use |
|----------|------------|-------------|
| Card flips, carousels, parallax | CSS 3D Transforms | Simple depth effects, no complex geometries |
| Floating elements, tilting cards | CSS + light JS | Mouse-tracking, hover effects |
| Product viewers, 3D models | Three.js / R3F | Need actual 3D objects, lighting, materials |
| Complex scenes, particles | Three.js + shaders | Immersive environments, effects |
| Hybrid experiences | CSS + Three.js + GSAP | Landing pages mixing 2D and 3D |

**React Three Fiber (R3F)** is preferred for React projects. Use vanilla Three.js for non-React or performance-critical applications.

## Design Thinking for 3D

Before coding, commit to an immersive direction:

- **Depth Strategy**: How will layers create depth? Parallax? Z-spacing? Atmospheric perspective?
- **Lighting Mood**: Dramatic single source? Soft studio? Neon accents? Natural environment?
- **Motion Philosophy**: Continuous ambient movement? Reactive to user? Scroll-driven narrative?
- **Interaction Model**: Orbit controls? First-person? Gesture-based? Passive viewing?

**CRITICAL**: 3D should serve the experience, not overwhelm it. A subtle parallax hero can be more impactful than a cluttered WebGL scene.

## Core Patterns

### CSS 3D (Simple Depth)

For card flips, carousels, parallax layers, floating elements, perspective text:

```css
.scene { perspective: 1000px; }
.object {
  transform-style: preserve-3d;
  transform: rotateX(15deg) rotateY(-20deg) translateZ(50px);
}
```

See [references/css-3d-transforms.md](references/css-3d-transforms.md) for patterns:
- 3D card flip with front/back faces
- Rotating carousels with `translateZ`
- Parallax depth layers
- Floating animations with rotation
- Perspective text effects
- 3D buttons with depth shadows
- Isometric grid layouts

### Three.js / R3F (Full 3D)

For 3D models, product viewers, particle systems, complex lighting:

```jsx
<Canvas shadows>
  <PerspectiveCamera makeDefault position={[0, 2, 5]} />
  <OrbitControls enableDamping />
  <Environment preset="studio" />
  <Model />
</Canvas>
```

See [references/threejs-patterns.md](references/threejs-patterns.md) for:
- Scene setup (vanilla + R3F)
- Three-point and dramatic lighting
- PBR materials and textures
- Product showcase with auto-rotation
- Particle systems (floating, galaxy)
- Scroll-driven camera animations
- Post-processing (bloom, DOF, vignette)
- Performance optimization (instances, LOD)

### Animation & Interaction

For GSAP, Framer Motion, scroll effects, mouse tracking:

```jsx
// Framer Motion 3D tilt
const rotateX = useTransform(mouseY, [-100, 100], [30, -30]);
const rotateY = useTransform(mouseX, [-100, 100], [-30, 30]);
```

See [references/animation-interaction.md](references/animation-interaction.md) for:
- GSAP with Three.js integration
- Framer Motion 3D transforms
- Scroll-linked animations (ScrollTrigger, useScroll)
- Mouse-tracking tilt effects
- Drag rotation controls
- State transitions between scenes
- Loading animations (3D spinners)

### Immersive Experiences

For product configurators, virtual try-on, environments, data viz:

See [references/immersive-patterns.md](references/immersive-patterns.md) for:
- Product configurators (color/material/assembly)
- Virtual try-on with face tracking
- 360° panoramic viewers with hotspots
- Room configurators with draggable furniture
- 3D data visualization (bar charts, globes, networks)
- Scroll-based interactive narratives
- Game-like controls and collectibles
- AR/VR ready patterns (XR, teleportation, hand tracking)

## Lighting Guidelines

Lighting makes or breaks 3D realism:

**Product Photography (Studio)**
- Key light (main): 45° above, to the side
- Fill light: Opposite side, 50% intensity
- Back light: Behind subject, edge definition
- Use `Environment` preset="studio" in R3F

**Dramatic/Moody**
- Single spotlight from above
- Colored rim lights for accent
- Dark environment, high contrast

**Natural/Outdoor**
- Hemisphere light (sky + ground)
- Directional light as sun
- Use HDRI environment maps

## Material Quality

For realistic surfaces:

```jsx
<meshPhysicalMaterial
  color="#ffffff"
  metalness={0.9}
  roughness={0.1}
  clearcoat={1.0}        // Glossy top layer
  transmission={0.95}    // Glass transparency
  ior={1.5}              // Glass refraction
/>
```

Load texture maps for realism: color, normal, roughness, ambient occlusion.

## Performance Checklist

- [ ] Use `instances` for repeated objects
- [ ] Implement LOD (Level of Detail) for complex models
- [ ] Compress textures, use appropriate resolutions
- [ ] Limit shadow-casting lights
- [ ] Use `AdaptiveDpr` for automatic quality scaling
- [ ] Dispose geometries/materials on unmount
- [ ] Test on mobile - reduce particle counts, simplify shaders

## Anti-Patterns to Avoid

- **Gratuitous 3D**: Don't add depth just because you can
- **Motion sickness**: Avoid constant rotation or disorienting camera movement
- **Performance blindness**: Test on real devices, not just dev machines
- **Missing fallbacks**: Provide 2D alternatives for unsupported browsers
- **Overlit scenes**: Flat lighting kills 3D realism
- **Ignoring shadows**: Shadows ground objects in space

## Implementation Flow

1. **Assess complexity** → Choose CSS 3D vs Three.js
2. **Set up scene** → Camera, controls, lighting, environment
3. **Add content** → Models, geometries, materials
4. **Layer effects** → Post-processing, particles, atmosphere
5. **Wire interactions** → Mouse, touch, scroll, gestures
6. **Optimize** → Test performance, add fallbacks
7. **Polish** → Transitions, loading states, edge cases
