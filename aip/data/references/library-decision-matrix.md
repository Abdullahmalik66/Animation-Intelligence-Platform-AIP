# Library Decision Matrix

Use this matrix to select the correct animation library for a given requirement.

---

## Quick Selection Guide

| Requirement | Recommended | Why |
|---|---|---|
| Simple hover/focus transition | **CSS** | Zero cost, native, most performant |
| Fade/slide entrance on load | **CSS** | `@keyframes` + `animation-fill-mode: both` |
| Looping decorative animation | **CSS** | `animation: infinite` |
| Scroll reveal (simple) | **CSS + IntersectionObserver** | No library needed |
| Scroll-driven (scrub) | **GSAP ScrollTrigger** or CSS `animation-timeline` | |
| Pinned scroll section | **GSAP ScrollTrigger** | Only library with robust pin support |
| Multi-step choreographed timeline | **GSAP** | Most powerful timeline API |
| Text character animation | **GSAP SplitText** | Built for this purpose |
| SVG draw/morph | **GSAP DrawSVG/MorphSVG** | Best SVG animation tools |
| React state-driven animation | **Motion for React** | Designed for this |
| React exit/unmount animation | **Motion for React** | `AnimatePresence` |
| Shared layout transition (React) | **Motion for React** | `layoutId` |
| Drag/gesture animation | **Motion for React** | Built-in physics drag |
| 3D scene / WebGL | **Three.js** | Only option |
| After Effects animation (JSON) | **Lottie** | Reads AE export format |
| Interactive animation with states | **Rive** | State machine runtime |
| Lightweight vanilla animation | **Anime.js** or **Motion** | Small bundle |
| Scroll-linked (vanilla, no pin) | **Motion (scroll())** | Clean API |
| IntersectionObserver entrance | **Motion (inView())** | Simple, clean |

---

## Detailed Matrix

### Feature Support

| Feature | CSS | GSAP | Motion React | Three.js | Rive | Lottie | Anime.js | Motion |
|---|---|---|---|---|---|---|---|---|
| Simple transitions | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Keyframe animations | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Timeline sequencing | ⚠️ | ✅ | ⚠️ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Scroll-triggered | ⚠️ | ✅ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Scroll-pinned | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Scroll-linked (scrub) | ✅* | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Exit animations | ⚠️ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Layout animations | ❌ | ⚠️ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Drag/gesture physics | ❌ | ⚠️ | ✅ | ❌ | ❌ | ❌ | ❌ | ⚠️ |
| Spring physics | ❌ | ⚠️ | ✅ | ❌ | ❌ | ❌ | ⚠️ | ✅ |
| SVG drawing | ⚠️ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| SVG morphing | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Text splitting | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 3D / WebGL | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| After Effects files | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| State machines | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Stagger | ⚠️ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| prefers-reduced-motion | ✅ | ✅ | ✅ | Manual | Manual | Manual | Manual | Manual |

*CSS scroll-timeline: Chrome 115+, limited Safari support

✅ = Native support
⚠️ = Possible but limited or manual
❌ = Not supported

---

### Framework Compatibility

| Library | React | Next.js | Vue | Nuxt | Svelte | Angular | Vanilla |
|---|---|---|---|---|---|---|---|
| CSS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| GSAP | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Motion for React | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Three.js | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Rive | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Lottie | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Anime.js | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Motion | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

### Bundle Size (Gzipped Approximate)

| Library | Min Size | Typical Size | Notes |
|---|---|---|---|
| CSS | 0kb | 0kb | Native |
| Motion (vanilla) | ~3kb | ~5kb | Modular |
| Anime.js | ~7kb | ~7kb | Monolithic |
| Motion for React | ~18kb | ~20kb | + React overhead |
| GSAP core | ~27kb | ~35kb | + plugins |
| Rive runtime | ~40kb | ~40kb | + .riv file |
| Lottie-web | ~25kb | ~40kb | + JSON file |
| Three.js | ~150kb | ~250kb | With tree-shaking |
| Three.js (no treeshake) | ~600kb+ | ~600kb+ | Full import |

---

### Licence Summary

| Library | Licence | Commercial Use |
|---|---|---|
| CSS | N/A | Free |
| GSAP (core) | GSAP Standard | Free for most; check terms |
| GSAP (Club plugins) | Club GSAP | Paid |
| Motion for React | MIT | Free |
| Three.js | MIT | Free |
| Rive runtime | MIT | Free |
| Rive editor | Commercial | Free tier available |
| Lottie-web | MIT | Free |
| Anime.js | MIT | Free |
| Motion (vanilla) | MIT | Free |

---

### SSR Compatibility (Next.js, Nuxt, etc.)

| Library | SSR Compatible | Notes |
|---|---|---|
| CSS | ✅ | Always |
| GSAP | ⚠️ | Use `useEffect`, avoid `typeof window` guard |
| Motion for React | ✅ | SSR-safe by default |
| Three.js | ⚠️ | DOM/WebGL not available in SSR — use dynamic import with `ssr: false` |
| Rive | ⚠️ | Canvas not available in SSR — use dynamic import |
| Lottie | ⚠️ | DOM not available in SSR — use dynamic import |
| Anime.js | ⚠️ | DOM not available in SSR — use `useEffect` |
| Motion | ⚠️ | Use `useEffect` for DOM access |

---

## Decision Flowchart

```
Start: What do you need to animate?
│
├─ CSS sufficient? (hover, fade, slide, loop) → CSS ✅
│
├─ 3D / WebGL scene → Three.js
│
├─ Designer file?
│   ├─ .riv (interactive states) → Rive
│   └─ .json (After Effects / static) → Lottie
│
├─ Scroll-driven with pinning or complex timeline → GSAP
│
├─ React + state/gesture/exit/layout → Motion for React
│
├─ Lightweight vanilla or non-React → Anime.js or Motion
│
└─ Complex, no match above → GSAP (safe default)
```
