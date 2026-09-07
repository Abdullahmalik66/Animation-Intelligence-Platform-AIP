# Animation Performance Reference

Key performance rules, budgets, and techniques for frontend animations.

---

## The Rendering Pipeline

```
JavaScript → Style → Layout → Paint → Composite
```

**Only animate properties that skip to Composite:**
- ✅ `transform` (translate, scale, rotate, skew)
- ✅ `opacity`

**Never animate:**
- ❌ `width`, `height` → triggers Layout
- ❌ `top`, `left`, `right`, `bottom` → triggers Layout
- ❌ `margin`, `padding` → triggers Layout
- ❌ `font-size`, `border-width` → triggers Layout

---

## Transform Replacements

| Instead of | Use |
|---|---|
| `left: Xpx` | `translateX(Xpx)` |
| `top: Ypx` | `translateY(Ypx)` |
| `width: Xpx` | `scaleX(factor)` |
| `height: Ypx` | `scaleY(factor)` |

---

## Frame Budget

- 60fps = 16.67ms per frame
- Target JS < 4ms per frame
- Target Paint < 2ms per frame
- Critical threshold: >16ms = dropped frame

---

## `will-change` Rules

```css
/* Only on elements that are ABOUT to animate */
.will-animate { will-change: transform, opacity; }

/* Remove after animation completes */
```

Never apply to all elements. Never use `will-change: all`.

---

## Cleanup Rules

| Library | Cleanup call |
|---|---|
| GSAP | `ctx.revert()` |
| Three.js | `.dispose()` on all objects + `cancelAnimationFrame` |
| Rive | `rive.cleanup()` |
| Lottie | `animation.destroy()` |
| Anime.js | `anime.remove(targets)` |
| Motion | `animation.cancel()` |

---

## Bundle Budgets

| Project Type | Max Animation Bundle (gzipped) |
|---|---|
| Marketing site | 30kb |
| SaaS dashboard | 20kb |
| E-commerce | 15kb |
| Mobile-first | 10kb |

---

## DevTools Checklist

```
□ No red frames in Performance tab (>16.67ms)
□ No purple Layout blocks in animation frames
□ Paint Flashing shows minimal repaint area
□ No unnecessary compositor layers (Layers panel)
□ Memory heap stable (no upward trend)
□ FPS meter stays at 60fps during animation
```
