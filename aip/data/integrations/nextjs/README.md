# Next.js Integration Guide

Animation integration for Next.js (App Router and Pages Router).

---

## Key Considerations

1. **SSR**: Next.js renders on the server — DOM and WebGL APIs are not available
2. **Dynamic imports**: Use `next/dynamic` with `ssr: false` for browser-only animation libraries
3. **App Router**: Use `"use client"` directive for all component-level animations
4. **Hydration**: Avoid animation state mismatches between server and client renders

---

## App Router Setup

### Client Component Required

```tsx
// app/components/AnimatedHero.tsx
"use client";

import { motion, useReducedMotion } from "motion/react";

const VARIANTS = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0 },
};

export function AnimatedHero() {
  const reduced = useReducedMotion();
  return (
    <motion.h1
      variants={reduced ? undefined : VARIANTS}
      initial="hidden"
      animate="visible"
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      Hello World
    </motion.h1>
  );
}
```

---

## Dynamic Imports (SSR-Incompatible Libraries)

### Three.js / Lottie / Rive

```tsx
// app/components/ThreeSceneWrapper.tsx
"use client";

import dynamic from "next/dynamic";

// Prevent SSR for WebGL/Canvas components
const ThreeScene = dynamic(
  () => import("./ThreeScene"),
  {
    ssr: false,
    loading: () => <div style={{ height: 400 }} aria-label="Loading 3D scene" />,
  }
);

export function ThreeSceneWrapper() {
  return <ThreeScene />;
}
```

---

## GSAP in Next.js App Router

```tsx
"use client";

import { useEffect, useRef } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function GSAPSection() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // GSAP is browser-only — safe inside useEffect
    const ctx = gsap.context(() => {
      const mm = gsap.matchMedia();
      mm.add("(prefers-reduced-motion: no-preference)", () => {
        gsap.from(".card", {
          opacity: 0, y: 40, stagger: 0.1,
          scrollTrigger: { trigger: ref.current, start: "top 80%" },
        });
      });
    }, ref);

    return () => ctx.revert();
  }, []);

  return <section ref={ref}><div className="card">Card</div></section>;
}
```

---

## Route Transitions (App Router)

```tsx
// Use Motion for React's AnimatePresence with layout
"use client";

import { AnimatePresence, motion } from "motion/react";
import { usePathname } from "next/navigation";

export function PageTransition({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={pathname}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.25 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
}
```

---

## Performance: Lazy Loading Lottie JSON

```tsx
"use client";

import { useEffect, useRef, useState } from "react";
import type { AnimationItem } from "lottie-web";

export function LazyLottie({ src }: { src: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let animation: AnimationItem;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // Lazy-load lottie-web only in browser
    import("lottie-web").then(({ default: lottie }) => {
      animation = lottie.loadAnimation({
        container: ref.current!,
        renderer: "svg",
        loop: !reduced,
        autoplay: !reduced,
        path: src,
      });

      if (reduced) animation.goToAndStop(0, true);
    });

    return () => animation?.destroy();
  }, [src]);

  return <div ref={ref} aria-hidden="true" />;
}
```
