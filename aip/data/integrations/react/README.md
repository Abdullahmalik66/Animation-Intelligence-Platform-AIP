# React Integration Guide

Animation integration patterns for React projects.

---

## Setup

### Recommended Libraries for React

| Use Case | Library |
|---|---|
| UI state transitions | Motion for React |
| Scroll animations | GSAP + ScrollTrigger |
| 3D scenes | Three.js or @react-three/fiber |
| Designer assets | Rive or Lottie |
| Lightweight | Anime.js or Motion |

---

## GSAP + React

```bash
npm install gsap
```

### Pattern

```tsx
import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function GSAPComponent() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const ctx = gsap.context(() => {
      const mm = gsap.matchMedia();
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.from(".item", { opacity: 0, y: 30, stagger: 0.1 });
      });
    }, ref);

    return () => ctx.revert();
  }, []);

  return <div ref={ref}><div className="item">Hello</div></div>;
}
```

---

## Motion for React

```bash
npm install motion
```

### Pattern

```tsx
import { motion, AnimatePresence, useReducedMotion } from "motion/react";

const VARIANTS = {
  hidden: { opacity: 0, y: 16 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 0 },
};

export function MotionComponent({ show }: { show: boolean }) {
  const reduced = useReducedMotion();
  return (
    <AnimatePresence>
      {show && (
        <motion.div
          key="content"
          variants={reduced ? { hidden: { opacity: 0 }, visible: { opacity: 1 }, exit: { opacity: 0 } } : VARIANTS}
          initial="hidden"
          animate="visible"
          exit="exit"
        />
      )}
    </AnimatePresence>
  );
}
```

---

## Three.js + React

For React, prefer `@react-three/fiber`:

```bash
npm install three @react-three/fiber @react-three/drei
```

```tsx
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";

export function Scene() {
  return (
    <Canvas>
      <ambientLight />
      <mesh>
        <boxGeometry />
        <meshStandardMaterial color="indigo" />
      </mesh>
      <OrbitControls />
    </Canvas>
  );
}
```

---

## SSR Considerations (Next.js)

```tsx
// For libraries that need DOM (Three.js, Lottie, Rive)
import dynamic from "next/dynamic";

const ThreeScene = dynamic(() => import("./ThreeScene"), { ssr: false });
const LottieAnimation = dynamic(() => import("./LottieAnimation"), { ssr: false });
```
