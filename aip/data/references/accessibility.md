# Animation Accessibility Reference

WCAG 2.2 rules and best practices for accessible animation.

---

## Core Rule

Every animation must:
1. Respect `prefers-reduced-motion`
2. Have a static/visible fallback
3. Not convey essential information through motion alone
4. Not flash more than 3 times per second

---

## `prefers-reduced-motion`

### CSS
```css
/* Accessible-first: start with no animation */
@media (prefers-reduced-motion: no-preference) {
  .element { animation: slideIn 0.6s ease-out both; }
}
```

### JavaScript
```typescript
const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
```

### GSAP
```typescript
gsap.matchMedia().add("(prefers-reduced-motion: no-preference)", () => {
  // animation here
});
```

### Motion for React
```typescript
const prefersReducedMotion = useReducedMotion();
```

---

## WCAG Success Criteria

| SC | Level | Requirement |
|---|---|---|
| 1.4.3 | AA | Maintain colour contrast during animation |
| 2.1.1 | A | All functionality keyboard accessible |
| 2.2.2 | A | Auto-play >5s: must have pause/stop/hide |
| 2.3.1 | A | No flash >3 times/second |
| 2.3.3 | AAA | Allow users to disable motion triggered by interaction |

---

## Auto-Play Pause Control (WCAG 2.2.2)

```tsx
function AutoPlayAnimation() {
  const [paused, setPaused] = useState(false);
  return (
    <div>
      <div className={`animation ${paused ? "paused" : ""}`} />
      <button onClick={() => setPaused(p => !p)} aria-label={paused ? "Resume" : "Pause"}>
        {paused ? "▶" : "⏸"}
      </button>
    </div>
  );
}
```

---

## ARIA Patterns

```html
<!-- Decorative animation -->
<div class="decorative-bg-animation" aria-hidden="true"></div>

<!-- Loading animation -->
<div role="status" aria-label="Loading">
  <!-- spinner -->
</div>

<!-- Live update -->
<div aria-live="polite" aria-atomic="true">
  <!-- Dynamic content -->
</div>
```

---

## Vestibular Disorder Triggers (Avoid)

- Large-scale parallax
- Background animations that cover the full viewport
- Spinning or rotating animations >360°
- Zoom animations (rapid scale)
- Scrolljacking (overriding natural scroll)

Under `prefers-reduced-motion: reduce`, disable all of the above entirely.

---

## Accessibility Audit Checklist

```
□ prefers-reduced-motion handled in all animations
□ Elements visible without animation
□ No flashing >3/second
□ Auto-play >5s has pause control
□ Decorative animations are aria-hidden
□ Focus managed during transitions
□ Colour contrast maintained during animation
□ No info conveyed by motion alone
□ Scroll-driven parallax disabled under reduced motion
```
