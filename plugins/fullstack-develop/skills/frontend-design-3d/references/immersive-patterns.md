# Immersive Experience Patterns

## Table of Contents
1. [Product Configurators](#product-configurators)
2. [Virtual Try-On](#virtual-try-on)
3. [360° Environments](#360-environments)
4. [Data Visualization](#data-visualization)
5. [Interactive Stories](#interactive-stories)
6. [Game-Like Interfaces](#game-like-interfaces)
7. [AR/VR Ready Patterns](#arvr-ready-patterns)

## Product Configurators

### Color/Material Selector

```jsx
import { useGLTF, Html } from '@react-three/drei';
import { useState, useRef } from 'react';

const materials = {
  leather: { color: '#2d2d2d', roughness: 0.6, metalness: 0 },
  chrome: { color: '#e8e8e8', roughness: 0.1, metalness: 1 },
  gold: { color: '#ffd700', roughness: 0.3, metalness: 0.9 },
  matte: { color: '#1a1a1a', roughness: 0.9, metalness: 0 }
};

const colors = ['#ef4444', '#3b82f6', '#22c55e', '#f59e0b', '#8b5cf6'];

function ProductConfigurator({ modelPath }) {
  const { scene, nodes } = useGLTF(modelPath);
  const [selectedMaterial, setSelectedMaterial] = useState('leather');
  const [selectedColor, setSelectedColor] = useState('#3b82f6');

  // Apply material to specific parts
  const materialProps = {
    ...materials[selectedMaterial],
    color: selectedColor
  };

  return (
    <>
      <primitive object={scene}>
        {/* Override specific mesh materials */}
        {nodes.MainBody && (
          <meshStandardMaterial
            attach-material
            {...materialProps}
          />
        )}
      </primitive>

      <Html position={[2, 0, 0]}>
        <div className="configurator-panel">
          <h3>Material</h3>
          <div className="material-options">
            {Object.keys(materials).map(mat => (
              <button
                key={mat}
                className={selectedMaterial === mat ? 'active' : ''}
                onClick={() => setSelectedMaterial(mat)}
              >
                {mat}
              </button>
            ))}
          </div>

          <h3>Color</h3>
          <div className="color-options">
            {colors.map(color => (
              <button
                key={color}
                style={{ backgroundColor: color }}
                className={selectedColor === color ? 'active' : ''}
                onClick={() => setSelectedColor(color)}
              />
            ))}
          </div>
        </div>
      </Html>
    </>
  );
}
```

### Part Assembly Viewer

```jsx
import { useState } from 'react';
import { useSpring, animated } from '@react-spring/three';

function ExplodedView({ parts }) {
  const [exploded, setExploded] = useState(false);

  return (
    <>
      {parts.map((part, index) => {
        const spring = useSpring({
          position: exploded
            ? part.explodedPosition
            : part.assembledPosition,
          config: { mass: 1, tension: 170, friction: 26 }
        });

        return (
          <animated.mesh
            key={part.id}
            geometry={part.geometry}
            material={part.material}
            position={spring.position}
          />
        );
      })}

      <Html>
        <button onClick={() => setExploded(!exploded)}>
          {exploded ? 'Assemble' : 'Explode'}
        </button>
      </Html>
    </>
  );
}
```

### Dimension Annotations

```jsx
import { Line, Html } from '@react-three/drei';

function DimensionLine({ start, end, label, offset = 0.5 }) {
  const midpoint = [
    (start[0] + end[0]) / 2,
    (start[1] + end[1]) / 2 + offset,
    (start[2] + end[2]) / 2
  ];

  return (
    <group>
      {/* Main dimension line */}
      <Line
        points={[start, end]}
        color="#6366f1"
        lineWidth={2}
        dashed
        dashSize={0.1}
        gapSize={0.05}
      />

      {/* End caps */}
      <Line
        points={[
          [start[0], start[1] - 0.1, start[2]],
          [start[0], start[1] + 0.1, start[2]]
        ]}
        color="#6366f1"
        lineWidth={2}
      />
      <Line
        points={[
          [end[0], end[1] - 0.1, end[2]],
          [end[0], end[1] + 0.1, end[2]]
        ]}
        color="#6366f1"
        lineWidth={2}
      />

      {/* Label */}
      <Html position={midpoint}>
        <div className="dimension-label">{label}</div>
      </Html>
    </group>
  );
}
```

## Virtual Try-On

### Face Tracking Overlay

```jsx
// Using MediaPipe Face Mesh with Three.js
import { FaceMesh } from '@mediapipe/face_mesh';

function VirtualTryOn() {
  const videoRef = useRef();
  const canvasRef = useRef();
  const [faceLandmarks, setFaceLandmarks] = useState(null);

  useEffect(() => {
    const faceMesh = new FaceMesh({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`;
      }
    });

    faceMesh.setOptions({
      maxNumFaces: 1,
      refineLandmarks: true,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5
    });

    faceMesh.onResults((results) => {
      if (results.multiFaceLandmarks?.[0]) {
        setFaceLandmarks(results.multiFaceLandmarks[0]);
      }
    });

    // Start camera and process frames
    const camera = new Camera(videoRef.current, {
      onFrame: async () => {
        await faceMesh.send({ image: videoRef.current });
      },
      width: 1280,
      height: 720
    });
    camera.start();
  }, []);

  return (
    <>
      <video ref={videoRef} style={{ display: 'none' }} />
      <Canvas>
        {faceLandmarks && (
          <GlassesOverlay landmarks={faceLandmarks} />
        )}
      </Canvas>
    </>
  );
}

function GlassesOverlay({ landmarks }) {
  const glassesRef = useRef();

  useFrame(() => {
    if (!landmarks) return;

    // Key landmarks for glasses positioning
    const leftEye = landmarks[33];   // Left eye outer corner
    const rightEye = landmarks[263]; // Right eye outer corner
    const noseBridge = landmarks[168];

    // Calculate position and rotation
    const eyeDistance = Math.sqrt(
      Math.pow(rightEye.x - leftEye.x, 2) +
      Math.pow(rightEye.y - leftEye.y, 2)
    );

    const centerX = (leftEye.x + rightEye.x) / 2;
    const centerY = (leftEye.y + rightEye.y) / 2;

    // Map to 3D space (simplified)
    glassesRef.current.position.set(
      (centerX - 0.5) * 4,
      -(centerY - 0.5) * 3,
      -noseBridge.z * 2
    );

    glassesRef.current.scale.setScalar(eyeDistance * 5);

    // Rotation based on face angle
    const angle = Math.atan2(
      rightEye.y - leftEye.y,
      rightEye.x - leftEye.x
    );
    glassesRef.current.rotation.z = angle;
  });

  return (
    <group ref={glassesRef}>
      <primitive object={glassesModel} />
    </group>
  );
}
```

### Body Measurement Overlay

```jsx
function ClothingSizeVisualizer({ measurements, garmentModel }) {
  const { scene } = useGLTF(garmentModel);
  const groupRef = useRef();

  // Scale garment based on measurements
  const scale = useMemo(() => {
    return {
      x: measurements.chest / 100,
      y: measurements.height / 170,
      z: measurements.waist / 80
    };
  }, [measurements]);

  return (
    <group ref={groupRef} scale={[scale.x, scale.y, scale.z]}>
      <primitive object={scene} />

      {/* Size indicator */}
      <Html position={[1, 1, 0]}>
        <div className="size-badge">
          Recommended: {calculateSize(measurements)}
        </div>
      </Html>
    </group>
  );
}
```

## 360° Environments

### Panoramic Viewer

```jsx
import { useTexture } from '@react-three/drei';

function PanoramicViewer({ imageUrl }) {
  const texture = useTexture(imageUrl);

  return (
    <mesh scale={[-1, 1, 1]}>
      <sphereGeometry args={[500, 60, 40]} />
      <meshBasicMaterial map={texture} side={THREE.BackSide} />
    </mesh>
  );
}

// With hotspots
function PanoramicWithHotspots({ panoramas, currentPanorama }) {
  const texture = useTexture(panoramas[currentPanorama].image);
  const [setPanorama] = useState(currentPanorama);

  return (
    <>
      <mesh scale={[-1, 1, 1]}>
        <sphereGeometry args={[500, 60, 40]} />
        <meshBasicMaterial map={texture} side={THREE.BackSide} />
      </mesh>

      {panoramas[currentPanorama].hotspots.map((hotspot, i) => (
        <group key={i} position={hotspot.position}>
          <mesh onClick={() => setPanorama(hotspot.targetPanorama)}>
            <sphereGeometry args={[2, 16, 16]} />
            <meshBasicMaterial color="#6366f1" transparent opacity={0.8} />
          </mesh>
          <Html>
            <div className="hotspot-label">{hotspot.label}</div>
          </Html>
        </group>
      ))}
    </>
  );
}
```

### Room Configurator

```jsx
function RoomConfigurator() {
  const [furniture, setFurniture] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);

  const addFurniture = (type, position) => {
    setFurniture([...furniture, {
      id: Date.now(),
      type,
      position,
      rotation: [0, 0, 0]
    }]);
  };

  return (
    <Canvas shadows>
      {/* Room shell */}
      <RoomGeometry />

      {/* Draggable furniture */}
      {furniture.map(item => (
        <DraggableFurniture
          key={item.id}
          model={item.type}
          position={item.position}
          rotation={item.rotation}
          selected={selectedItem === item.id}
          onSelect={() => setSelectedItem(item.id)}
          onMove={(newPos) => updateFurniturePosition(item.id, newPos)}
        />
      ))}

      {/* Floor plane for raycasting */}
      <mesh
        rotation={[-Math.PI / 2, 0, 0]}
        position={[0, 0, 0]}
        onPointerDown={(e) => {
          if (selectedFurnitureType) {
            addFurniture(selectedFurnitureType, [e.point.x, 0, e.point.z]);
          }
        }}
      >
        <planeGeometry args={[20, 20]} />
        <meshStandardMaterial visible={false} />
      </mesh>
    </Canvas>
  );
}
```

## Data Visualization

### 3D Bar Chart

```jsx
function BarChart3D({ data }) {
  const maxValue = Math.max(...data.map(d => d.value));

  return (
    <group>
      {data.map((item, index) => {
        const height = (item.value / maxValue) * 5;
        const x = (index - data.length / 2) * 1.5;

        return (
          <group key={item.label} position={[x, height / 2, 0]}>
            <mesh castShadow>
              <boxGeometry args={[1, height, 1]} />
              <meshStandardMaterial
                color={item.color || '#6366f1'}
                metalness={0.3}
                roughness={0.4}
              />
            </mesh>

            <Html position={[0, height / 2 + 0.5, 0]}>
              <div className="data-label">{item.value}</div>
            </Html>

            <Html position={[0, -height / 2 - 0.5, 0]}>
              <div className="axis-label">{item.label}</div>
            </Html>
          </group>
        );
      })}
    </group>
  );
}
```

### Globe Visualization

```jsx
import { useTexture } from '@react-three/drei';

function GlobeVisualization({ points }) {
  const earthTexture = useTexture('/textures/earth.jpg');
  const globeRef = useRef();

  useFrame(() => {
    globeRef.current.rotation.y += 0.001;
  });

  // Convert lat/lng to 3D coordinates
  const latLngToVector3 = (lat, lng, radius = 1) => {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lng + 180) * (Math.PI / 180);

    return new THREE.Vector3(
      -radius * Math.sin(phi) * Math.cos(theta),
      radius * Math.cos(phi),
      radius * Math.sin(phi) * Math.sin(theta)
    );
  };

  return (
    <group ref={globeRef}>
      {/* Earth sphere */}
      <mesh>
        <sphereGeometry args={[1, 64, 64]} />
        <meshStandardMaterial map={earthTexture} />
      </mesh>

      {/* Data points */}
      {points.map((point, i) => {
        const position = latLngToVector3(point.lat, point.lng, 1.01);
        const height = point.value / 100;

        return (
          <group key={i} position={position}>
            <mesh lookAt={new THREE.Vector3(0, 0, 0)}>
              <cylinderGeometry args={[0.02, 0.02, height, 8]} />
              <meshStandardMaterial color="#f43f5e" />
            </mesh>
          </group>
        );
      })}

      {/* Atmosphere glow */}
      <mesh scale={1.1}>
        <sphereGeometry args={[1, 64, 64]} />
        <shaderMaterial
          transparent
          side={THREE.BackSide}
          uniforms={{
            glowColor: { value: new THREE.Color('#6366f1') }
          }}
          vertexShader={atmosphereVertexShader}
          fragmentShader={atmosphereFragmentShader}
        />
      </mesh>
    </group>
  );
}
```

### Network Graph

```jsx
function NetworkGraph3D({ nodes, edges }) {
  const nodePositions = useMemo(() => {
    // Force-directed layout in 3D
    return calculateForceLayout(nodes, edges);
  }, [nodes, edges]);

  return (
    <group>
      {/* Edges */}
      {edges.map((edge, i) => (
        <Line
          key={i}
          points={[
            nodePositions[edge.source],
            nodePositions[edge.target]
          ]}
          color="#374151"
          lineWidth={1}
          transparent
          opacity={0.5}
        />
      ))}

      {/* Nodes */}
      {nodes.map((node, i) => (
        <mesh key={node.id} position={nodePositions[i]}>
          <sphereGeometry args={[node.size * 0.1, 16, 16]} />
          <meshStandardMaterial
            color={node.color}
            emissive={node.color}
            emissiveIntensity={0.2}
          />
        </mesh>
      ))}
    </group>
  );
}
```

## Interactive Stories

### Scroll-Based Narrative

```jsx
import { ScrollControls, Scroll, useScroll } from '@react-three/drei';

function StoryExperience() {
  return (
    <Canvas>
      <ScrollControls pages={5} damping={0.25}>
        {/* 3D Scene */}
        <StoryScene />

        {/* HTML Overlay */}
        <Scroll html>
          <section className="story-section" style={{ height: '100vh' }}>
            <h1>Chapter 1</h1>
            <p>The journey begins...</p>
          </section>
          <section className="story-section" style={{ height: '100vh' }}>
            <h1>Chapter 2</h1>
            <p>Discovery awaits...</p>
          </section>
          {/* More sections... */}
        </Scroll>
      </ScrollControls>
    </Canvas>
  );
}

function StoryScene() {
  const scroll = useScroll();
  const modelRef = useRef();
  const cameraRef = useRef();

  // Story waypoints
  const waypoints = [
    { position: [0, 0, 5], rotation: [0, 0, 0] },
    { position: [5, 2, 3], rotation: [0, Math.PI / 4, 0] },
    { position: [0, 5, 0], rotation: [Math.PI / 4, 0, 0] },
    { position: [-5, 2, 3], rotation: [0, -Math.PI / 4, 0] },
    { position: [0, 0, 5], rotation: [0, Math.PI * 2, 0] }
  ];

  useFrame(({ camera }) => {
    const offset = scroll.offset;
    const index = Math.floor(offset * (waypoints.length - 1));
    const t = (offset * (waypoints.length - 1)) % 1;

    const from = waypoints[index];
    const to = waypoints[Math.min(index + 1, waypoints.length - 1)];

    // Interpolate camera position
    camera.position.lerpVectors(
      new THREE.Vector3(...from.position),
      new THREE.Vector3(...to.position),
      t
    );

    // Interpolate model rotation
    modelRef.current.rotation.y = THREE.MathUtils.lerp(
      from.rotation[1],
      to.rotation[1],
      t
    );
  });

  return (
    <group ref={modelRef}>
      <StoryModel />
    </group>
  );
}
```

### Choice-Based Branching

```jsx
function InteractiveChoice({ choices, onChoice }) {
  return (
    <group>
      {choices.map((choice, i) => {
        const angle = (i / choices.length) * Math.PI * 2;
        const radius = 3;

        return (
          <group
            key={choice.id}
            position={[
              Math.cos(angle) * radius,
              0,
              Math.sin(angle) * radius
            ]}
          >
            <mesh onClick={() => onChoice(choice.id)}>
              <boxGeometry args={[1, 1, 0.2]} />
              <meshStandardMaterial color="#6366f1" />
            </mesh>
            <Html center>
              <div className="choice-label">{choice.text}</div>
            </Html>
          </group>
        );
      })}
    </group>
  );
}
```

## Game-Like Interfaces

### First-Person Controls

```jsx
import { PointerLockControls } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';

function FirstPersonExperience() {
  const controlsRef = useRef();
  const [moveForward, setMoveForward] = useState(false);
  const [moveBackward, setMoveBackward] = useState(false);
  const [moveLeft, setMoveLeft] = useState(false);
  const [moveRight, setMoveRight] = useState(false);

  useEffect(() => {
    const onKeyDown = (e) => {
      switch (e.code) {
        case 'KeyW': setMoveForward(true); break;
        case 'KeyS': setMoveBackward(true); break;
        case 'KeyA': setMoveLeft(true); break;
        case 'KeyD': setMoveRight(true); break;
      }
    };

    const onKeyUp = (e) => {
      switch (e.code) {
        case 'KeyW': setMoveForward(false); break;
        case 'KeyS': setMoveBackward(false); break;
        case 'KeyA': setMoveLeft(false); break;
        case 'KeyD': setMoveRight(false); break;
      }
    };

    document.addEventListener('keydown', onKeyDown);
    document.addEventListener('keyup', onKeyUp);

    return () => {
      document.removeEventListener('keydown', onKeyDown);
      document.removeEventListener('keyup', onKeyUp);
    };
  }, []);

  useFrame(({ camera }) => {
    const speed = 0.1;
    const direction = new THREE.Vector3();

    camera.getWorldDirection(direction);
    direction.y = 0;
    direction.normalize();

    const right = new THREE.Vector3();
    right.crossVectors(camera.up, direction).normalize();

    if (moveForward) camera.position.add(direction.multiplyScalar(speed));
    if (moveBackward) camera.position.add(direction.multiplyScalar(-speed));
    if (moveLeft) camera.position.add(right.multiplyScalar(speed));
    if (moveRight) camera.position.add(right.multiplyScalar(-speed));
  });

  return (
    <>
      <PointerLockControls ref={controlsRef} />
      <Environment />
    </>
  );
}
```

### Collectibles and Scoring

```jsx
function CollectibleSystem() {
  const [score, setScore] = useState(0);
  const [collectibles, setCollectibles] = useState(
    generateCollectibles(20)
  );

  const collect = (id) => {
    setCollectibles(prev => prev.filter(c => c.id !== id));
    setScore(prev => prev + 10);
  };

  return (
    <>
      {collectibles.map(item => (
        <Collectible
          key={item.id}
          position={item.position}
          onCollect={() => collect(item.id)}
        />
      ))}

      <Html fullscreen>
        <div className="hud">
          <div className="score">Score: {score}</div>
        </div>
      </Html>
    </>
  );
}

function Collectible({ position, onCollect }) {
  const meshRef = useRef();
  const [collected, setCollected] = useState(false);

  useFrame(({ clock }) => {
    if (!collected) {
      meshRef.current.rotation.y = clock.elapsedTime * 2;
      meshRef.current.position.y = position[1] + Math.sin(clock.elapsedTime * 3) * 0.2;
    }
  });

  const handleClick = () => {
    if (!collected) {
      setCollected(true);
      onCollect();
    }
  };

  if (collected) return null;

  return (
    <mesh ref={meshRef} position={position} onClick={handleClick}>
      <octahedronGeometry args={[0.3]} />
      <meshStandardMaterial
        color="#fbbf24"
        emissive="#fbbf24"
        emissiveIntensity={0.5}
      />
    </mesh>
  );
}
```

## AR/VR Ready Patterns

### XR Session Setup

```jsx
import { VRButton, ARButton, XR, Controllers, Hands } from '@react-three/xr';

function XRExperience() {
  return (
    <>
      <VRButton />
      <Canvas>
        <XR>
          <Controllers />
          <Hands />

          {/* Your 3D content - automatically works in VR/AR */}
          <Scene />
        </XR>
      </Canvas>
    </>
  );
}
```

### Teleportation Movement

```jsx
import { useXR, useController } from '@react-three/xr';

function TeleportSystem() {
  const { player } = useXR();
  const rightController = useController('right');
  const [teleportTarget, setTeleportTarget] = useState(null);

  useFrame(() => {
    if (!rightController) return;

    // Cast ray from controller
    const raycaster = new THREE.Raycaster();
    raycaster.setFromXRController(rightController);

    const intersects = raycaster.intersectObjects(teleportSurfaces);

    if (intersects.length > 0) {
      setTeleportTarget(intersects[0].point);
    }
  });

  const teleport = () => {
    if (teleportTarget) {
      player.position.copy(teleportTarget);
    }
  };

  return (
    <>
      {teleportTarget && (
        <mesh position={teleportTarget}>
          <ringGeometry args={[0.3, 0.5, 32]} />
          <meshBasicMaterial color="#6366f1" transparent opacity={0.5} />
        </mesh>
      )}
    </>
  );
}
```

### Hand Tracking Interactions

```jsx
import { useHand } from '@react-three/xr';

function HandInteraction() {
  const hand = useHand('right');
  const [grabbing, setGrabbing] = useState(null);

  useFrame(() => {
    if (!hand) return;

    const indexTip = hand.joints['index-finger-tip'];
    const thumbTip = hand.joints['thumb-tip'];

    if (indexTip && thumbTip) {
      const distance = indexTip.position.distanceTo(thumbTip.position);
      const isPinching = distance < 0.02;

      if (isPinching && !grabbing) {
        // Check for grabbable objects near pinch point
        const grabPoint = indexTip.position.clone().lerp(thumbTip.position, 0.5);
        const nearbyObject = findNearestGrabbable(grabPoint);

        if (nearbyObject) {
          setGrabbing(nearbyObject);
        }
      } else if (!isPinching && grabbing) {
        setGrabbing(null);
      }
    }
  });

  return null;
}
```
