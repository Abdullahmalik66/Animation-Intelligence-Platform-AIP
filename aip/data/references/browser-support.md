# Browser Support Reference

Current browser compatibility for animation features and libraries.

---

## CSS Animation Features

| Feature | Chrome | Firefox | Safari | Edge | iOS Safari |
|---|---|---|---|---|---|
| `@keyframes` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `transition` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `animation` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `prefers-reduced-motion` | ✅ 74+ | ✅ 63+ | ✅ 10.1+ | ✅ 79+ | ✅ 10.3+ |
| CSS `animation-timeline: scroll()` | ✅ 115+ | ✅ 110+ | ❌ | ✅ 115+ | ❌ |
| CSS `animation-timeline: view()` | ✅ 115+ | ✅ 114+ | ❌ | ✅ 115+ | ❌ |
| `@starting-style` | ✅ 117+ | ✅ 129+ | ✅ 17.5+ | ✅ 117+ | ⚠️ |

---

## Library Support

| Library | Chrome | Firefox | Safari | Edge | IE |
|---|---|---|---|---|---|
| GSAP | ✅ | ✅ | ✅ | ✅ | ✅ 11 |
| Motion for React | ✅ | ✅ | ✅ | ✅ | ❌ |
| Three.js | ✅ | ✅ | ✅ | ✅ | ❌ |
| Rive | ✅ | ✅ | ✅ | ✅ | ❌ |
| Lottie | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| Anime.js | ✅ | ✅ | ✅ | ✅ | ✅ 11 |
| Motion | ✅ | ✅ | ✅ | ✅ | ❌ |

---

## WebGL (Three.js)

| Feature | Chrome | Firefox | Safari | Edge | iOS |
|---|---|---|---|---|---|
| WebGL 1 | ✅ | ✅ | ✅ | ✅ | ✅ |
| WebGL 2 | ✅ | ✅ | ✅ 15+ | ✅ | ✅ 15+ |

---

## Safari-Specific Notes

- CSS `animation-timeline` (scroll-driven) not supported — use GSAP ScrollTrigger as fallback
- Some CSS `filter` animations perform poorly — test on real device
- `backdrop-filter` animations can be janky — use sparingly
- Always test Three.js scenes on iOS Safari — WebGL support has historically been inconsistent

---

## Recommended Baseline

Target this minimum baseline for most projects:

- Chrome 90+
- Firefox 90+
- Safari 14+
- Edge 90+
- iOS Safari 14+

This covers >95% of global browser usage as of 2025.
