# Animation Code Review Skill

## Goal

Review animation code for correctness, accessibility, performance, security, and maintainability. Produce an evidence-based, structured report with specific, actionable feedback, a weighted quality score, and a production readiness status.

---

## Return Format

Every review must follow the **Standard Review Output** defined in this file:

- Executive Summary
- Production Status (`PASS` / `PASS WITH CONDITIONS` / `NEEDS REVIEW` / `BLOCKED`)
- Overall score: uncapped weighted score, then policy-adjusted score if a cap applies
- Dimension scores (10 dimensions)
- Findings ordered by severity
- Positive findings (evidence-backed only)
- Required changes
- Recommended improvements
- Validation plan
- Final recommendation

For deeper accessibility guidance, reference:
[`skills/animation-accessibility/SKILL.md`](../animation-accessibility/SKILL.md)

---

## Warnings

- ❌ If `prefers-reduced-motion` is absent for meaningful or non-decorative motion, apply an explicit **Overall Score policy cap of 7.0** (see Scoring Formula for the full rule)
- ❌ If active cleanup is missing and retained work or resources are evidenced, apply an explicit **Overall Score policy cap of 6.5** (see Scoring Formula); missing cleanup is a lifecycle defect — severity depends on evidence of retained resources, repeated mounting, or measurable resource growth
- ❌ Never set `Production Status: PASS` when a Critical WCAG failure, confirmed crash risk, persistent post-teardown animation leak, or uncontrollable render loop is present — set `BLOCKED`
- ⚠️ Animating layout properties (`width`, `height`, `top`, `left`, `margin`, `padding`) is not automatically a failure — assess rendering frequency, affected area, device impact, and whether `transform` can replace it before penalising
- ⚠️ Review observed code and evidence. Distinguish verified defects from risks and assumptions
- ⚠️ Do not recommend a full rewrite when a focused fix resolves the issue
- ⚠️ Do not inflate severity for style preferences — `Critical` and `High` require concrete production risk

---

## Context Dump

See [`.github/prompts/review-animation.prompt.md`](../../.github/prompts/review-animation.prompt.md) for the full extended review rubric.

---

### Review Principles

The reviewer must:

1. Review only the supplied code and evidence — not imagined runtime behaviour
2. Distinguish verified defects from risks, suggestions, and style preferences
3. Cite file paths and line numbers when available
4. Identify the highest-risk issue first
5. Provide a specific fix for every blocking or critical finding
6. Avoid score inflation — a 10/10 means no known issues
7. Recognise valid trade-offs rather than penalising reasonable decisions
8. Avoid recommending architectural rewrites when a small, targeted fix is sufficient
9. State explicitly when evidence is insufficient to draw a firm conclusion
10. Prioritise production risk over personal style throughout

---

### Severity Definitions

| Severity | Meaning |
|---|---|
| **Critical** | Confirmed issue creating serious accessibility failure, security vulnerability, data loss, crash, or production-blocking risk. An intentionally continuous animation loop is not automatically Critical — block only when the loop continues after the owning component is torn down, runs outside its owner's lifecycle, or lacks any controllable termination path. Sets Production Status to `BLOCKED`. |
| **High** | Likely production defect, major memory or GPU leak, broken lifecycle, severe performance problem, or significant accessibility failure. Does not automatically set `BLOCKED` but may when evidence is strong. |
| **Medium** | Maintainability, correctness, compatibility, or measurable performance issue. Should be fixed but may not independently block release. |
| **Low** | Small improvement with limited operational impact. |
| **Informational** | Optional guidance, clarification, or future-improvement suggestion. Not a defect. |

The reviewer must never classify style preferences as Critical or High.

---

### Production Readiness Status

Every review must declare exactly one status:

| Status | Meaning |
|---|---|
| **PASS** | No blocking issues. Suitable for production. |
| **PASS WITH CONDITIONS** | No critical issue, but specific fixes or validation are required before the next release. |
| **NEEDS REVIEW** | Important risks remain unresolved or evidence is insufficient to confirm safety. |
| **BLOCKED** | A confirmed Critical accessibility, security, correctness, lifecycle, or performance issue exists. Must be remediated and re-reviewed before shipping. |

The status must include a one-sentence justification referencing the highest-risk finding.

---

### Scoring Formula

Score each of the following 10 dimensions independently on a 0–10 scale, then apply the weights below. Round the weighted result to one decimal place.

| Dimension | Weight |
|---|---|
| Correctness | 20% |
| Accessibility | 20% |
| Performance | 15% |
| Cleanup and lifecycle | 15% |
| Security | 10% |
| Maintainability | 10% |
| Architecture | 5% |
| Testing | 3% |
| Bundle and dependency impact | 1% |
| Developer experience | 1% |

**Formula:**
```
Overall = (Correctness × 0.20) + (Accessibility × 0.20) + (Performance × 0.15)
        + (Cleanup × 0.15) + (Security × 0.10) + (Maintainability × 0.10)
        + (Architecture × 0.05) + (Testing × 0.03) + (Bundle × 0.01) + (DX × 0.01)
```

**Score gates (explicit policy caps — separate from and applied after the weighted calculation):**

For each review, always calculate and display the uncapped weighted score first, then show the policy-adjusted score if a cap applies.

| Condition | Dimension cap | Overall policy cap |
|---|---|---|
| `prefers-reduced-motion` absent for meaningful motion | Accessibility ≤ 4 | Overall ≤ 7.0 |
| Active cleanup missing with evidence of retained resources | Cleanup and lifecycle ≤ 3 | Overall ≤ 6.5 |
| Both conditions apply | Both dimension caps | Lower cap applies (Overall ≤ 6.5) |

**These caps are explicit policy rules, not mathematical consequences of the weighted formula.** Other dimensions could receive high scores and still produce a weighted result above 7.0 — the cap overrides that result when the condition is confirmed.

**Required output format when a cap applies:**
```
Uncapped weighted score: N.N / 10
Policy-adjusted score:   N.N / 10  (cap applied: [reason])
```

If a Critical issue is confirmed → Production Status becomes `BLOCKED`. The uncapped and policy-adjusted scores are always calculated and displayed independently; production status is declared separately from both.

A numeric score alone never determines production safety. Always declare Production Status separately.

---

### Finding Structure

Every finding must contain all of the following fields:

| Field | Description |
|---|---|
| **ID** | Unique identifier (e.g. `F-01`) |
| **Severity** | Critical / High / Medium / Low / Informational |
| **Category** | Correctness, Accessibility, Performance, Cleanup, Security, Maintainability, Architecture, Testing, Bundle, or Developer Experience |
| **Confidence** | High (confirmed in code) / Medium (strongly implied) / Low (assumed — context unavailable) |
| **Location** | File path and line number(s), or "not available" |
| **Evidence** | The specific code, pattern, or observable fact supporting the finding |
| **Impact** | The concrete consequence if this is not fixed |
| **Fix** | A specific, actionable resolution including corrected code where applicable |
| **Verification** | How to confirm the fix worked (test, profiling step, manual check) |

If full runtime context is unavailable, mark Confidence: Low and state what additional evidence is needed.

---

### Architecture Review

Evaluate the following for every animated component or system:

- Does the animation belong at this layer, or should it live in a parent, wrapper, or dedicated animation layer?
- Is animation logic separated from business logic and application state?
- Who owns the timeline or animation instance, and is that ownership clear?
- Are lifecycle boundaries respected — does the animation start and stop with the component that creates it?
- Is the code reusable without premature abstraction? One-off animations do not require a shared abstraction.
- Is a library genuinely required, or could CSS or WAAPI achieve the same result with less complexity?
- Are server and client boundaries handled correctly (SSR safety, `typeof window` guards)?
- Does the implementation define explicit error and fallback behaviour?
- Is `prefers-reduced-motion` handled at the architecture level or scattered ad hoc per component?
- Does the static render state produce meaningful visible content before any JavaScript runs?

---

### Framework-Specific Review Guidance

#### React
- **Effect dependencies:** Follow the React Hooks dependency rules. Stable refs, module-level constants, and values intentionally captured through documented patterns may not require the same treatment as reactive props and state. Review linter output (`react-hooks/exhaustive-deps`) and runtime intent rather than applying a mechanical "add everything" rule.
- **React Strict Mode:** In development, `useEffect` runs twice (mount → cleanup → mount). Libraries that do not clean up inside the effect return create duplicate instances. Test with Strict Mode enabled.
- **Stable refs:** Animation targets via `useRef` must be assigned before the effect runs. Confirm `ref.current` is not null at the point of use.
- **Re-render restarts:** Review whether inline variant or config objects cause the specific component to re-trigger unnecessarily. Move variants outside the component or memoize them when profiling or inspection confirms unwanted re-triggering — do not optimise mechanically.
- **Reduced-motion hooks:** Use `useReducedMotion()` from `motion/react` or a custom hook — not a module-level constant — so the value responds to preference changes in supported client environments.
- **Cleanup:** Every `useEffect` that creates an animation must return a cleanup function that cancels or destroys the instance.

#### Next.js
- **Client component boundaries:** Use a narrow `"use client"` boundary for animation code that depends on browser APIs. Confirm the directive is present where needed and the boundary is as narrow as possible.
- **SSR/hydration:** Never derive animation initial state from server-rendered HTML — this can cause hydration mismatches and visual flicker. Initialise client-side in `useEffect` or `useLayoutEffect`.
- **Dynamic imports:** Use a narrow Client Component boundary for animation code that depends on browser APIs. Use `dynamic(() => import(...), { ssr: false })` only when the component or dependency cannot be safely prerendered, or when client-only lazy loading is intentionally required. Do not disable SSR automatically — this is an architectural choice, not a universal library requirement.
- **CLS (Cumulative Layout Shift):** Opacity changes do not normally alter layout geometry and therefore do not themselves create CLS. Review CLS when animation changes element dimensions, position in document flow, font metrics, image sizing, or inserts content after initial render. Hydration mismatches and visual flicker are separate concerns.
- **Route transitions:** After a route change animation, focus must move to the new page heading or skip-link target.

#### Vue / Nuxt
- **Lifecycle cleanup:** Cancel animations in `onUnmounted()`. Confirm no RAF or timer runs after component destruction.
- **Template refs:** Confirm `ref.value` is non-null before accessing in `onMounted`.
- **SSR guards:** Place browser-dependent code in client lifecycle hooks or use the SSR guard supported by the installed Vue/Nuxt version. (`process.client` is available in Nuxt; browser lifecycle hooks such as `onMounted` are the standard Vue approach.)
- **`<Transition>` hooks:** Custom JavaScript hooks (`@enter`, `@leave`) must call `done()` or the transition stalls indefinitely.
- **Watcher cleanup:** Watchers that start animations must be stopped in `onUnmounted`.

#### Svelte / SvelteKit
- **`onMount` cleanup:** Return a cleanup function from `onMount` to cancel animations on component destroy.
- **SSR guards:** Wrap `window` access in `typeof window !== "undefined"` or inside `onMount`.
- **Reactive re-triggering:** Reactive statements (`$:`) re-run on every dependency change. Confirm animation re-triggers are intentional.
- **Built-in transitions:** Svelte's `fly`, `slide`, and `draw` are appropriate for simple transitions. Confirm they are conditionally disabled under `prefers-reduced-motion`.

#### Angular
- **Lifecycle cleanup:** Use `DestroyRef` (Angular 16+) or `ngOnDestroy` to cancel animations and remove listeners.
- **`AnimationBuilder`:** Confirm `AnimationPlayer.destroy()` is called in `ngOnDestroy`.
- **Zone cost:** Angular Animations run inside NgZone by default. For performance-sensitive work, consider `NgZone.runOutsideAngular()`.
- **Reduced-motion:** Check `prefers-reduced-motion` in `ngOnInit` and expose through a shared service rather than re-querying per component.

#### Vanilla JavaScript
- **Listener removal:** Every `addEventListener` must have a corresponding `removeEventListener` with the same function reference.
- **Observer disconnection:** `IntersectionObserver`, `ResizeObserver`, and `MutationObserver` must be `.disconnect()`ed when no longer needed.
- **RAF cancellation:** Store every `requestAnimationFrame` ID and call `cancelAnimationFrame(id)` in cleanup.
- **DOM availability:** Guard all DOM access for environments without a document (SSR, test environments, web workers).
- **Idempotent initialisation:** If init may be called more than once, guard against duplicate instances.

---

### Library-Specific Review Guidance

#### GSAP
- **Plugin registration:** `gsap.registerPlugin(ScrollTrigger, ...)` must appear once before the plugin is used. Do not call it inside a component render function — this registers the plugin on every render in React.
- **Context / scoped selectors:** In React, use `gsap.context(() => { ... }, rootRef)` to scope queries to the component root. Prevents selecting elements outside the component.
- **Timeline ownership:** Each component should own its own timeline. Avoid shared global timelines mutated by multiple components.
- **ScrollTrigger cleanup:** Use a `gsap.context` and call `.revert()` in cleanup — this kills all tweens and ScrollTriggers created within that context.
- **`gsap.matchMedia` cleanup:** The returned `mm` object must have `.revert()` called in cleanup. Failing to do so leaves media query listeners alive.
- **Duplicate timelines:** Check `useEffect` without cleanup that creates a new timeline on every render. In React Strict Mode this creates two timelines on mount.

#### Motion for React (v11+)
- **Package name:** From v11 the canonical import is `"motion/react"`. Flag imports from `"framer-motion"` as a potential version mismatch if the installed package is `motion` v11+. Verify against `package.json`.
- **`useReducedMotion()`:** Use for any non-decorative animation. `useReducedMotion()` reflects the user's reduced-motion preference and responds to preference changes in supported client environments. Review server-rendered initial states separately and ensure hydration remains stable — do not assume a specific server return value without verifying the installed version's documented behaviour.
- **`AnimatePresence`:** Required for exit animations. Animated children must have a stable `key` prop and be direct children of `AnimatePresence`.
- **Stable variants:** Review whether inline variant objects cause the specific component to re-trigger unnecessarily. Move variants outside the component or memoize them when stability is required or profiling shows unwanted re-triggering.
- **Layout animations:** The `layout` prop triggers layout recalculation. Confirm it is intentional and applied to the minimum required elements.

#### Three.js
- **RAF cancellation:** Store the ID from `requestAnimationFrame` and call `cancelAnimationFrame(id)` in cleanup.
- **Disposal:** Call `.dispose()` on application-owned `BufferGeometry`, `Material`, `Texture`, and `WebGLRenderTarget` instances. The `WebGLRenderer` must also be `.dispose()`d. Note: textures referenced by materials or loaded via `GLTFLoader` may require explicit disposal when the application owns them — `material.dispose()` alone does not release textures, and `scene.clear()` does not free GPU resources automatically.
- **Resize listener:** Any `window` resize listener updating the camera or renderer must be removed in cleanup.
- **`AnimationMixer`:** Call `mixer.stopAllAction()` before cleanup to release animation clip references.
- **GPU memory:** Scenes with many large textures can exhaust GPU memory on mobile. Flag if total texture memory is uncontrolled.
- **Context loss:** Production scenes should handle the `webglcontextlost` event to avoid silent failures.
- **`forceContextLoss()`:** This is optional diagnostic or aggressive teardown behaviour. Use `renderer.dispose()` and explicit resource disposal as the standard cleanup path. Apply `forceContextLoss()` only when justified and tested — do not treat it as a default cleanup requirement.
- **Static fallback:** Under `prefers-reduced-motion: reduce`, stop the RAF loop after the first frame. Mark `<canvas>` as `aria-hidden="true"` and provide a static image fallback where the scene is non-essential.

#### Rive
- **Cleanup:** _(Version-sensitive: verify the teardown API and recommended sequence against the installed `@rive-app/canvas` or `@rive-app/webgl` package version. Common teardown involves calling a cleanup or destroy method on the runtime instance, but the exact API and required sequence vary between major versions — do not assume a fixed method name without package evidence.)_
- **State machine lifecycle:** Consult the installed Rive runtime documentation for the recommended state-machine teardown sequence before calling cleanup.
- **Trusted asset origin:** `.riv` files must be loaded from a trusted, approved, integrity-controlled source (same-origin/CDN describes delivery, not trust). Do not accept user-supplied `.riv` URLs.
- **Static fallback:** Under `prefers-reduced-motion: reduce`, set `autoplay: false`, do not attach state machines, and pause at the static artboard rest frame.

#### Lottie (`lottie-web`)
- **Instance destruction:** Call `animation.destroy()` in cleanup. This removes the instance from Lottie's internal registry, stops the RAF loop, and cleans up event listeners.
- **Manual event listeners:** Listeners added via `animation.addEventListener` must be removed with `animation.removeEventListener` before `destroy()`.
- **Trusted JSON assets:** `.json` files must be loaded from a trusted, approved, integrity-controlled source (same-origin/CDN describes delivery, not trust). Do not load from user-supplied URLs.
- **Renderer choice:** The `svg` renderer creates DOM-based SVG output, but that output is not automatically accessible or meaningful. Decorative animations must be hidden from assistive technology (`aria-hidden="true"` on the container). Informational animations require accessible names, descriptions, or equivalent HTML content. The `canvas` renderer has the same requirements and additionally needs an HTML alternative for informational content.
- **Reduced-motion fallback:** Under `prefers-reduced-motion: reduce`, set `autoplay: false`, `loop: false`, and call `animation.goToAndStop(0, true)` after `DOMLoaded`.

#### Anime.js
- **Instance cancellation:** _(Version-sensitive: verify the cancellation API against the installed Anime.js package. In v3, `anime.remove(targets)` cancels animations on specific targets. Confirm the available API surface and whether additional cleanup steps are required for the installed major version.)_
- **No built-in reduced-motion support:** All reduced-motion handling must be implemented manually using `window.matchMedia`.

#### Motion (standalone, outside React)
- **Lifecycle method:** Use the lifecycle method exposed by the installed Motion version to stop and clean up animation instances. Verify the method name (`cancel`, `stop`, or equivalent) against the package types or official documentation for the installed version — do not assume a universal method name across versions.
- **Reduced-motion:** Check `window.matchMedia("(prefers-reduced-motion: reduce)")` manually — the standalone package does not apply this automatically.

> **Version-sensitivity and source discipline:** For every library-specific finding: (1) inspect `package.json`; (2) inspect the lockfile; (3) inspect installed type definitions when available; (4) use official documentation for that exact major version when needed; (5) if the version is unknown, mark the finding version-sensitive; (6) never classify an API as deprecated, missing, or incorrect based only on general knowledge without package evidence.

---

### Performance Review

- **Compositor-friendly properties:** `transform` and `opacity` generally avoid layout and paint, keeping animation work on the compositor thread. Animating `width`, `height`, `top`, `left`, `margin`, or `padding` triggers layout recalculation — this is not automatically a failure, but assess frequency, scope, and whether `transform` can replace the property.
- **Layout thrash:** DOM reads and writes interleaved inside a RAF callback force synchronous layout. Read all positions first; then write.
- **`will-change` lifecycle:** Apply `will-change: transform` only when animation is imminent; set `will-change: auto` after. Permanent `will-change` on static elements wastes GPU memory.
- **Multiple RAF loops:** More than one uncoordinated RAF loop running simultaneously wastes CPU. Animation libraries should coordinate through a single tick (GSAP does this by default).
- **Scroll event frequency:** Raw `scroll` listeners fire on every scroll event. Use `IntersectionObserver` for enter/leave; use RAF to throttle position reads.
- **Passive listeners:** Scroll and touch listeners should use `{ passive: true }` when the handler never needs to call `preventDefault()` and browser behaviour remains correct. Do not mark all scroll or touch listeners as passive without confirming they have no default-prevention requirement.
- **DOM query repetition:** `document.querySelector` inside a RAF callback queries the DOM on every frame. Cache outside the loop.
- **Canvas resolution:** Confirm `renderer.setPixelRatio(window.devicePixelRatio)` is used appropriately. Oversized canvases on high-DPI screens waste GPU memory.
- **Three.js draw calls:** Excessive draw calls from unbatched geometry or too many unique materials degrade frame rate, especially on mobile.
- **Core Web Vitals:** Entrance animations that delay LCP or produce CLS must be flagged.
- **Bundle size:** Report approximate library weight. Flag when a library is imported for a single effect achievable with CSS.

---

### Accessibility Review

Reference [`skills/animation-accessibility/SKILL.md`](../animation-accessibility/SKILL.md) for full implementation patterns. This review must check:

- `prefers-reduced-motion` handled for all meaningful motion; high-risk patterns eliminated under `reduce` — not slowed
- Content visible in the static default state before animation runs; critical content never hidden behind an entrance animation
- Auto-play animations >5s have a visible pause or stop control (WCAG 2.2.2)
- No content flashes more than 3 times per second (WCAG 2.3.1)
- Focus indicators never animated away or hidden during transitions
- All interactive animated content keyboard-accessible (WCAG 2.1.1)
- Decorative animations carry `aria-hidden="true"`; loading indicators use `role="status"` or `aria-live="polite"`
- ARIA live regions positioned outside animated containers
- Decorative `<canvas>` elements carry `aria-hidden="true"`; informational canvas has an accessible HTML alternative
- After animated route changes, focus moves to page heading or skip-link target
- After modal or drawer close, focus returns to the triggering element
- No state change communicated by motion alone — static text or icon alternative required

---

### Security Review

- **Untrusted asset URLs:** Lottie `.json`, Rive `.riv`, GLTF/GLB, texture, video, and SVG assets must be loaded from a trusted, approved, integrity-controlled source (e.g. bundled or a reviewed, versioned, integrity-pinned host) — same-origin alone is not a trust guarantee; never from user-supplied URLs without validation. Unvalidated remote asset URLs can create privacy, tracking, availability, CORS, and content-trust risks. Severity depends on the trust boundary, validation in place, resource limits, credentials policy, and demonstrated impact — user-controlled remote URLs are not automatically Critical; classify based on actual data flow and exposure.
- **Unsafe HTML or SVG injection:** Any `innerHTML` / `outerHTML` insertion of SVG animation content must be sanitised (e.g. with DOMPurify)
- **Dynamic script loading:** Animation libraries loaded via dynamic `<script>` tags must use Subresource Integrity (SRI) hashes
- **Unpinned CDN dependencies:** CDN libraries without version pins and SRI hashes are a supply-chain risk
- **User-controlled parameters:** Animation target selectors, URLs, positions, and scales derived from user input must be validated and sanitised
- **Resource exhaustion:** Lottie and Three.js files of unbounded size can crash browser tabs — enforce server-side file-size limits for any user-uploaded animation asset
- **Information leakage:** Check for secrets, tokens, or internal URLs hardcoded in animation configuration objects or JSON files

Never reproduce discovered secrets in review output. Report file path and issue type only.

---

### AI-Generated Code Validation

When reviewing AI-generated animation code, check for:

- **Invented APIs:** Confirm every method, property, and plugin name against package documentation or installed types. Common: non-existent GSAP plugin names, fabricated Rive methods, invented `lottie-web` options.
- **Mixed library versions:** Imports from `"framer-motion"` in a `motion` v11 project; GSAP v2 syntax in a GSAP v3 project; deprecated `addListener` where `addEventListener` is required.
- **Incorrect cleanup methods:** e.g. `ctx.clear()` instead of `ctx.revert()` for GSAP, or `animation.stop()` instead of `animation.destroy()` for Lottie.
- **Missing imports:** Variables or functions used but not imported — common in AI snippets that omit boilerplate.
- **Undefined variables:** References to `rafId`, `mm`, `ctx`, `tl`, or similar never declared in the supplied scope.
- **Impossible framework combinations:** React hooks inside Vue `setup()`; Angular decorators in a Svelte component.
- **Placeholder comments as implementation:** `// handle cleanup here` or `// add reduced motion` without backing code.
- **Hallucinated plugin names:** e.g. `gsap.registerPlugin(AnimationPlugin)` where `AnimationPlugin` does not exist.

When an API cannot be confirmed, state that explicitly and recommend verification against `package.json`, the lockfile, or official documentation.

---

### Testing Review

Check for the following. Do not demand tests that provide no meaningful value.

- **Lifecycle tests:** Does the test suite verify animation instances are created on mount and cleaned up on unmount? This is the highest-value animation test.
- **Reduced-motion tests:** Is there a test that mocks `prefers-reduced-motion: reduce` (via `window.matchMedia` mock) and confirms animations are disabled?
- **State and transition tests:** Are animated state transitions (modal open/close, route change) tested for correct DOM output?
- **Focus tests:** Is focus placement after animated transitions tested (e.g. with Testing Library `userEvent`)?
- **Visual regression:** Appropriate for complex or brand-critical animations. Not required for simple utility animations.
- **Error and fallback tests:** If the animation can fail (network-loaded assets, WASM init), is the fallback state tested?
- **Mobile simulation:** Performance-sensitive animations benefit from profiling on real mobile hardware or with CPU throttling in DevTools.

---

### Anti-Patterns

The reviewer must flag any of the following immediately upon detection.

| Anti-Pattern | Risk | Preferred Fix |
|---|---|---|
| Animation instance created on every render (no dep array, no ref guard) | Memory leak, duplicate animations | Create once in `useEffect` with `[]` dep array; store in ref; clean up in return function |
| Multiple unmanaged RAF loops | CPU/battery drain, loop stacking on re-mount | Consolidate to one RAF loop; store and cancel the ID on cleanup |
| Missing unmount cleanup for library instances | Lifecycle defect; may retain active animation work, listeners, or GPU resources depending on the library and mount frequency | Implement the documented cleanup method for the installed library version (`ctx.revert` for GSAP; `animation.destroy` for Lottie; verify Rive, Anime.js, and Motion against installed package types) |
| Critical content hidden behind animation entrance | Invisible if JS fails, is slow, or reduced-motion is active | Default to `opacity: 1`; treat animation as progressive enhancement |
| Scrolljacking (overriding native scroll) | High-risk interaction pattern that can create keyboard, focus, operability, motion, and predictability failures — evaluate against the applicable WCAG success criteria rather than assigning an automatic generic violation | Remove scroll override; use scroll-linked animations that respect native scroll |
| Global `document.querySelector` inside reusable component | Selects wrong elements when component is used multiple times | Scope queries to the component root ref |
| Permanent `will-change: transform` on static elements | Wastes GPU memory, can degrade compositing for other layers | Apply only before animation; restore with `will-change: auto` after |
| Full animation library for a single CSS-achievable effect | Unnecessary bundle weight | Use CSS `@keyframes` or WAAPI |
| User-controlled asset URL loaded into Lottie, Rive, or Three.js | Unvalidated remote URLs create content-trust, privacy, tracking, CORS, and resource-exhaustion risks — severity depends on the application's trust boundary | Validate and allowlist asset URLs server-side |
| Animation state and business state coupled in the same variable | Can cause animation re-triggers on unrelated state changes; harder to test and maintain | Separate animation state (playing/paused/done) from business state |
| Large 3D scene or Lottie file loaded on initial page render | Delays LCP, high bandwidth cost on mobile | Lazy-load or defer below-the-fold animation content. In Next.js, use a narrow Client Component boundary; apply `next/dynamic` with `ssr: false` only when the component cannot safely be prerendered or deliberate client-only loading is required — not as a default for every animation asset |
| ARIA live region inside an animated container | Screen reader may miss announcements during transition | Move live regions to a stable, non-animated ancestor |

---

### Standard Review Output

Every review must use this structure exactly.

```markdown
# Animation Code Review

## Executive Summary
[One to three sentences: what was reviewed, the most significant finding, overall production status.]

## Production Status
[PASS | PASS WITH CONDITIONS | NEEDS REVIEW | BLOCKED]
Justification: [One sentence referencing the highest-risk finding.]

## Overall Score
Uncapped weighted score: N.N / 10
Policy-adjusted score:   N.N / 10  (cap applied: [reason], or "no cap applies")
Calculation: [Show each dimension score × weight, summed to the uncapped total.]

## Dimension Scores
| Dimension | Score /10 | Notes |
|---|---|---|
| Correctness | | |
| Accessibility | | |
| Performance | | |
| Cleanup and lifecycle | | |
| Security | | |
| Maintainability | | |
| Architecture | | |
| Testing | | |
| Bundle and dependency impact | | |
| Developer experience | | |

## Findings
[Ordered by severity. Each finding: ID, Severity, Category, Confidence, Location, Evidence, Impact, Fix, Verification.]

## Positive Findings
[Evidence-backed strengths only.]

## Required Changes
[Minimum changes required before approval. Reference finding IDs.]

## Recommended Improvements
[Non-blocking improvements, ordered by expected value.]

## Validation Plan
[Specific commands, test cases, profiling steps, and manual checks for this code.]

## Final Recommendation
[Ship as-is | Fix before shipping | Re-review after changes | Block — do not ship]
```

---

### Refactor Rules

Provide refactored code only when:

1. The user explicitly requests it, **or**
2. The overall score is below 7 **and** sufficient source context exists to produce a correct, complete refactor, **or**
3. A concise patch directly resolves a Critical or High finding and is shorter than a prose description

Otherwise provide a focused diff, a replacement snippet for the affected section only, or an implementation outline. Never rewrite correct, unrelated code. Never introduce new dependencies in a refactor without noting them.

---

### Full Review Checklist

#### Correctness
- [ ] Animation achieves the intended visual effect
- [ ] Animation plays in the correct sequence
- [ ] All state changes are handled correctly
- [ ] Initial and final states are explicitly defined
- [ ] No FOUC or invisible content on initial page load

#### Accessibility
- [ ] `prefers-reduced-motion` handled for all meaningful motion
- [ ] High-risk patterns completely disabled under reduce — not slowed
- [ ] Static fallback exists; content is visible without animation
- [ ] No content flashes more than 3 times per second (WCAG 2.3.1)
- [ ] Auto-play >5s has a visible pause or stop control (WCAG 2.2.2)
- [ ] Decorative animations carry `aria-hidden="true"`
- [ ] Loading indicators use `role="status"` or `aria-live="polite"`
- [ ] ARIA live regions are outside animated containers
- [ ] Canvas / WebGL decorative elements carry `aria-hidden="true"`
- [ ] Focus managed correctly: modal open, modal close, route transitions
- [ ] Focus indicator never animated away or hidden
- [ ] No information conveyed by motion alone

#### Performance
- [ ] `transform` and `opacity` used where layout-triggering properties can be avoided
- [ ] No forced synchronous layout inside animation loops
- [ ] `will-change` applied only when animation is imminent and removed after
- [ ] No multiple uncoordinated RAF loops
- [ ] No animation loop running after component unmount
- [ ] Scroll event listeners are passive where appropriate
- [ ] DOM queries cached outside animation loops
- [ ] Bundle size justified for the requirement
- [ ] LCP and CLS impact assessed

#### Cleanup and Lifecycle
- [ ] GSAP: `ctx.revert()` called in cleanup; `mm.revert()` if `gsap.matchMedia` used
- [ ] Motion for React: imperative animation instances cancelled in cleanup
- [ ] Three.js: RAF cancelled; geometry, material, texture, renderer `.dispose()`d
- [ ] Rive: the installed runtime's documented teardown method called and verified against package types or official documentation
- [ ] Lottie: `animation.destroy()` called
- [ ] Anime.js: the installed major version's documented cancellation and cleanup method used — verify against `package.json` and official documentation
- [ ] Motion (standalone): the installed version's returned animation controls stopped using the documented lifecycle method — verify method name against package types or official documentation
- [ ] All event listeners and observers removed in cleanup
- [ ] React Strict Mode double-invoke tested

#### Security
- [ ] No Lottie, Rive, GLTF, SVG, or video assets from untrusted or user-supplied URLs
- [ ] No unsafe HTML or SVG injection without sanitisation
- [ ] CDN libraries pinned with version and SRI hash
- [ ] No user input used as animation selectors or parameters
- [ ] No secrets in animation config or JSON assets
- [ ] File-size limits enforced for user-uploaded animation assets

#### Code Quality and Maintainability
- [ ] No magic numbers — all durations, delays, distances are named constants
- [ ] No TypeScript `any` in animation code
- [ ] No `console.log` in production code
- [ ] Variant and config objects defined outside component (Motion for React)
- [ ] GSAP plugins registered once before use
- [ ] No inline styles for complex or stateful animations
- [ ] AI-generated API calls verified against package version

#### Architecture
- [ ] Animation logic separated from business logic
- [ ] Timeline or instance ownership is clear
- [ ] Library use justified over CSS/WAAPI
- [ ] SSR / client boundaries handled correctly
- [ ] Static render state produces visible, useful content

#### Testing
- [ ] Lifecycle (mount/unmount) tests present
- [ ] Reduced-motion test present (`window.matchMedia` mocked)
- [ ] Focus placement after animated transitions tested
- [ ] Fallback and error states tested

---

## RTCF

**Role:** Senior frontend animation architect, accessibility reviewer, performance engineer, security reviewer, and open-source maintainer.

**Task:** Review animation code using evidence-based findings, the weighted scoring formula, severity definitions, production readiness gates, framework and library-specific guidance, and actionable verification steps. Every finding must include evidence, impact, a specific fix, and a verification method.

**Constraints:**
- Review only the supplied code and repository evidence — not imagined runtime behaviour
- Distinguish verified defects from risks and assumptions — state confidence per finding
- Do not inflate severity — Critical and High require concrete production risk
- Do not invent framework or library APIs — verify against package manifests or documentation
- Do not recommend a full rewrite when a focused fix resolves the issue
- Produce Production Readiness Status separately from the numeric score
- A confirmed Critical issue sets Production Status to `BLOCKED` regardless of numeric score

**Format:** Use the Standard Review Output exactly. Order findings by production risk (Critical → High → Medium → Low → Informational).

---

## Few-Shot Examples

---

### Example 1 — React + GSAP: duplicate timelines, missing cleanup, no reduced-motion handling

**Input:**
```tsx
// HeroAnimation.tsx
import { useEffect } from "react";
import { gsap } from "gsap";

export function HeroAnimation() {
  useEffect(() => {
    gsap.from(".hero-title", { opacity: 0, y: 40, duration: 0.8 });
    gsap.from(".hero-subtitle", { opacity: 0, y: 20, duration: 0.6, delay: 0.2 });
  }); // ← no dependency array, no cleanup

  return (
    <section>
      <h1 className="hero-title">Welcome</h1>
      <p className="hero-subtitle">Discover our product.</p>
    </section>
  );
}
```

**Output:**

```markdown
# Animation Code Review

## Executive Summary
`HeroAnimation` runs GSAP entrance animations on every render with no cleanup and no
reduced-motion handling. Because there is no dependency array, the effect re-runs on
every render and no cleanup function is returned — new tween instances accumulate in
GSAP's ticker and conflict with each other. In React Strict Mode the effect fires
twice on mount. Content begins at `opacity: 0`; if JavaScript execution is delayed
or fails after GSAP applies its starting values, both elements remain invisible.

## Production Status
NEEDS REVIEW
Justification: F-01 and F-02 are confirmed High defects requiring remediation before
shipping; no single finding in the supplied code meets the Critical definition of
crash, data loss, confirmed severe accessibility failure, or security vulnerability.

## Overall Score
Uncapped weighted score: 3.6 / 10
Policy-adjusted score:   3.6 / 10
(Accessibility ≤ 4 and Cleanup ≤ 3 caps both apply; the uncapped result of 3.6 is
already below 6.5 so the policy cap does not alter the displayed score.)

Calculation:
  Correctness     4 × 0.20 = 0.80
  Accessibility   2 × 0.20 = 0.40
  Performance     5 × 0.15 = 0.75
  Cleanup         0 × 0.15 = 0.00
  Security        8 × 0.10 = 0.80
  Maintainability 5 × 0.10 = 0.50
  Architecture    4 × 0.05 = 0.20
  Testing         2 × 0.03 = 0.06
  Bundle          6 × 0.01 = 0.06
  DX              5 × 0.01 = 0.05
  Uncapped = 3.62 → 3.6 / 10

## Dimension Scores
| Dimension | Score /10 | Notes |
|---|---|---|
| Correctness | 4 | Effect re-runs on every render — animations stack and conflict |
| Accessibility | 2 | No reduced-motion handling; content starts at opacity: 0 |
| Performance | 5 | GSAP appropriate; global selector is a multi-instance risk |
| Cleanup and lifecycle | 0 | No cleanup — confirmed lifecycle defect |
| Security | 8 | No untrusted assets; no injection risk |
| Maintainability | 5 | Readable but structurally broken |
| Architecture | 4 | Animation and render logic coupled; global selector |
| Testing | 2 | No evidence of tests |
| Bundle and dependency impact | 6 | GSAP core is justified for multi-element entrance |
| Developer experience | 5 | Readable; missing structure reduces confidence |

## Findings

### F-01 — High | Cleanup and Lifecycle | Confidence: High
**Location:** `HeroAnimation.tsx`, `useEffect` — no dependency array, no return
**Evidence:** `useEffect` without a dependency array runs after every render.
No cleanup function is returned. Each call creates new GSAP tween instances.
In React Strict Mode the effect fires twice on mount.
**Impact:** Repeated renders create duplicate active tweens and conflicting animation
behaviour. Missing cleanup creates a lifecycle defect: GSAP will hold those tweens
until they complete or the owning GSAP context is explicitly reverted. In a component
that re-renders frequently or mounts and unmounts repeatedly, active tween count
grows and conflicts accumulate. This does not constitute a confirmed permanent memory
leak without evidence of retained resources after animation completion, but the
lifecycle is demonstrably broken.
**Fix:** Use a single `gsap.matchMedia()` call scoped to the component root. This
provides selector scoping, reduced-motion handling, and cleanup in one object.
Do not nest a separate `gsap.context()` inside the matchMedia callback — the
matchMedia scope already handles scoping and cleanup when given a root element.

```tsx
import { useEffect, useRef } from "react";
import { gsap } from "gsap";

export function HeroAnimation() {
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const mm = gsap.matchMedia();

    mm.add(
      "(prefers-reduced-motion: no-preference)",
      () => {
        // Selector queries are scoped to sectionRef by the third argument
        gsap.from(".hero-title", { opacity: 0, y: 40, duration: 0.8 });
        gsap.from(".hero-subtitle", { opacity: 0, y: 20, duration: 0.6, delay: 0.2 });
      },
      sectionRef // third argument scopes all selectors to this element
    );

    // Under reduce: no animation is registered — normally rendered content stays visible

    return () => mm.revert(); // kills tweens, removes media listener
  }, []);

  return (
    <section ref={sectionRef}>
      <h1 className="hero-title">Welcome</h1>
      <p className="hero-subtitle">Discover our product.</p>
    </section>
  );
}
```

> **Version note:** Verify that the installed GSAP version supports the three-argument
> `gsap.matchMedia().add(query, callback, scope)` signature against `package.json`
> before using it.

**Verification:** Enable React Strict Mode. Mount and unmount the component. Confirm
`gsap.globalTimeline.getChildren().length` returns 0 after unmount. Confirm only one
animation plays on initial mount.

### F-02 — High | Accessibility | Confidence: High
**Location:** `HeroAnimation.tsx` — both `gsap.from` calls; no CSS context supplied
**Evidence:** Both `gsap.from` calls start with `opacity: 0`. No `prefers-reduced-motion`
check is present. No CSS in the supplied code establishes a visible default.
**Impact:** When `gsap.from()` starts, GSAP applies an inline `opacity: 0` as the
starting state and animates toward the element's natural state. If JavaScript is fully
disabled, GSAP never applies those inline values and normally styled content remains
visible. The more relevant risks are: (a) if execution is interrupted after GSAP has
applied its starting values, an inline `opacity: 0` will override a CSS `opacity: 1`
rule — a CSS default alone does not protect against an already-applied GSAP inline
style; (b) users with `prefers-reduced-motion: reduce` receive no static alternative.
The primary fixes are reduced-motion gating (which prevents GSAP from applying the
starting values at all), reliable cleanup, and ensuring interrupted animations restore
their intended final state.
**Fix:** Gate all GSAP entrance animations behind the `no-preference` matchMedia scope
as shown in the F-01 fix. Under `reduce`, GSAP registers nothing — the normally
rendered content is immediately visible. No additional CSS default is required when
the reduced-motion path registers no animation.

**Verification:** (1) Enable macOS Reduce Motion — confirm both elements are immediately
visible without animation. (2) Throttle JavaScript in DevTools — under `no-preference`,
confirm elements are visible in their default state before GSAP starts.

### F-03 — Medium | Architecture | Confidence: High
**Location:** `gsap.from(".hero-title", ...)` — global class selector
**Evidence:** `.hero-title` queries the entire document. If two `HeroAnimation`
instances are rendered simultaneously, both will animate all matching elements.
**Fix:** Scope with the `sectionRef` third argument to `mm.add()` as shown in F-01.
**Verification:** Render two instances simultaneously — confirm only each component's
own elements animate.

## Positive Findings
- GSAP is a reasonable choice for coordinated multi-element entrance animation
- Semantic HTML structure (`<h1>`, `<p>`) is correct
- No untrusted asset loading or injection risk identified

## Required Changes
1. F-01: Replace bare `useEffect` with `gsap.matchMedia()` scoped to `sectionRef`, returning `mm.revert()` in cleanup
2. F-02: Gate all entrance animation behind `(prefers-reduced-motion: no-preference)` — leave normally rendered content visible under `reduce`

## Recommended Improvements
- F-03: Confirmed resolved by the F-01 fix (third argument to `mm.add` scopes selectors)
- Move duration and offset values to named constants

## Validation Plan
- React Strict Mode: confirm no duplicate animations after mount/unmount cycle
- DevTools JS throttle: confirm elements visible before animation begins
- macOS Reduce Motion enabled: confirm both elements immediately visible
- DevTools Memory: snapshot before/after unmount — confirm no retained GSAP nodes

## Final Recommendation
Fix before shipping and re-review.
```

---

### Example 2 — Three.js scene: uncancelled RAF, undisposed GPU resources, untrusted model URL, no static fallback

**Input:**
```typescript
// ProductViewer.ts
import * as THREE from "three";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";

export function initProductViewer(canvas: HTMLCanvasElement, modelUrl: string) {
  const renderer = new THREE.WebGLRenderer({ canvas });
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, canvas.width / canvas.height, 0.1, 100);
  camera.position.set(0, 1, 3);

  const loader = new GLTFLoader();
  loader.load(modelUrl, (gltf) => {
    scene.add(gltf.scene);
  });

  const animate = () => {
    requestAnimationFrame(animate);
    scene.rotation.y += 0.005;
    renderer.render(scene, camera);
  };
  animate();
}
```

**Output:**

```markdown
# Animation Code Review

## Executive Summary
`initProductViewer` accepts a caller-supplied `modelUrl` with no origin validation,
returns `void` with no cleanup contract, never disposes the WebGL renderer or
application-owned GPU resources, never cancels its RAF loop, and applies continuous
auto-rotation with no `prefers-reduced-motion` handling. All defects are confirmed in
the supplied code.

## Production Status
NEEDS REVIEW
Justification: F-02 — the function returns `void` with no cleanup contract, the RAF
loop is never cancelled, and the WebGL renderer is never disposed. In a single-page
application where this viewer is mounted and unmounted, this becomes a Critical
lifecycle failure. In a one-time full-page use the impact is lower. Because the
calling context is not supplied, the severity is High and the status is NEEDS REVIEW
pending lifecycle confirmation; treat as Critical and BLOCKED if repeated mounting is
confirmed.

## Overall Score
Uncapped weighted score: 2.0 / 10
Policy-adjusted score:   2.0 / 10
(Both policy caps apply; the uncapped result of 2.0 is already well below 6.5.)

Calculation:
  Correctness     3 × 0.20 = 0.60
  Accessibility   1 × 0.20 = 0.20
  Performance     3 × 0.15 = 0.45
  Cleanup         0 × 0.15 = 0.00
  Security        1 × 0.10 = 0.10
  Maintainability 4 × 0.10 = 0.40
  Architecture    3 × 0.05 = 0.15
  Testing         1 × 0.03 = 0.03
  Bundle          5 × 0.01 = 0.05
  DX              4 × 0.01 = 0.04
  Uncapped = 2.02 → 2.0 / 10

## Dimension Scores
| Dimension | Score /10 | Notes |
|---|---|---|
| Correctness | 3 | Scene renders; lifecycle and cleanup are broken |
| Accessibility | 1 | No reduced-motion; canvas not aria-hidden; no fallback |
| Performance | 3 | Auto-rotation loop runs forever; no resize handler |
| Cleanup and lifecycle | 0 | No disposal of renderer or application-owned GPU resources; RAF never cancelled |
| Security | 1 | Unvalidated caller-supplied URL — risk level depends on trust boundary |
| Maintainability | 4 | Readable but structurally unsafe |
| Architecture | 3 | No error handling, no fallback, no cleanup contract |
| Testing | 1 | No evidence of tests |
| Bundle and dependency impact | 5 | Three.js appropriate for a 3D product viewer |
| Developer experience | 4 | Simple API; produces unsafe usage pattern |

## Findings

### F-01 — High | Security | Confidence: High
**Location:** `ProductViewer.ts` — `loader.load(modelUrl, ...)`
**Evidence:** `modelUrl` is passed from the caller with no origin validation.
**Impact:** Unvalidated remote asset URLs can create privacy, tracking, availability,
CORS, and content-trust risks. Whether the browser sends credentials depends on fetch
configuration, browser policy, URL origin, and server behaviour. Resource exhaustion
is possible with an unbounded or malformed GLTF file. Classify as Critical if
`modelUrl` can originate from user-controlled input with no server-side validation;
keep as High if the URL originates from application configuration or a trusted internal
source.
**Fix:**
```typescript
const ALLOWED_ORIGINS = ["https://assets.yourdomain.com"];

function isTrustedModelUrl(url: string): boolean {
  try {
    return ALLOWED_ORIGINS.includes(new URL(url).origin);
  } catch {
    return false;
  }
}

if (!isTrustedModelUrl(modelUrl)) {
  // Do not log the rejected URL — it may contain sensitive query parameters
  console.error("Model URL origin is not in the allowed list.");
  return () => {};
}
```
**Verification:** Pass a URL from an external origin — confirm it is rejected.
Pass a URL from the allowed origin — confirm the model loads.

### F-02 — High | Cleanup and Lifecycle | Confidence: High
**Location:** `ProductViewer.ts` — no `.dispose()` calls, function returns `void`, RAF ID not stored
**Evidence:** `WebGLRenderer` is created but never `.dispose()`d. Application-owned
geometry and materials added by the GLTF loader are not disposed. The function returns
`void` — there is no cleanup contract. The RAF ID is not stored and the loop cannot be
cancelled.
**Impact:** The RAF loop and WebGL context are never released. In a single-page
application where this viewer is mounted and unmounted, the loop continues consuming
CPU and GPU after the canvas is removed, GPU resources accumulate across mounts, and
on mobile this can exhaust GPU memory and crash the tab — meeting the Critical
threshold. In a one-time full-page render the immediate impact is lower. Classify as
**Critical and BLOCKED** if the calling context confirms repeated mounting; keep as
**High and NEEDS REVIEW** otherwise.
**Fix:**
```typescript
export function initProductViewer(
  canvas: HTMLCanvasElement,
  modelUrl: string
): () => void {
  const renderer = new THREE.WebGLRenderer({ canvas });
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(60, canvas.width / canvas.height, 0.1, 100);
  camera.position.set(0, 1, 3);

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let rafId: number | undefined;

  const loader = new GLTFLoader();
  loader.load(modelUrl, (gltf) => {
    scene.add(gltf.scene);
    // If reduced motion is active, render one static frame after the model loads
    if (prefersReduced) {
      renderer.render(scene, camera);
    }
  });

  if (prefersReduced) {
    // Render one static frame immediately with whatever is in the scene
    renderer.render(scene, camera);
    // No RAF loop started — no cancellation needed
  } else {
    const animate = () => {
      scene.rotation.y += 0.005;
      renderer.render(scene, camera);
      rafId = requestAnimationFrame(animate);
    };
    animate();
  }

  return function cleanup() {
    if (rafId !== undefined) cancelAnimationFrame(rafId);

    // Dispose application-owned geometry, materials, and their textures.
    // Dispose only resources owned by this viewer.
    // Shared cached textures or materials require separate ownership management.
    scene.traverse((obj) => {
      const mesh = obj as THREE.Mesh;
      if (!mesh.isMesh) return;

      mesh.geometry.dispose();

      const mats = Array.isArray(mesh.material) ? mesh.material : [mesh.material];
      mats.forEach((m) => {
        // Dispose texture maps explicitly — material.dispose() alone does not
        // release textures referenced by the material.
        const tex = m as THREE.MeshStandardMaterial;
        (["map", "normalMap", "roughnessMap", "metalnessMap", "emissiveMap"] as const)
          .forEach((key) => {
            if (tex[key]) tex[key]!.dispose();
          });
        m.dispose();
      });
    });

    renderer.dispose();
    // renderer.forceContextLoss() is not part of standard cleanup.
    // Use it only as an explicit, tested teardown step when required.
  };
}
```
**Verification:** Mount and unmount. Inspect Chrome DevTools Memory panel — confirm
renderer resources are released. Confirm via the Performance panel that no RAF
callbacks fire after cleanup is called.

### F-03 — High | Accessibility | Confidence: High
**Location:** `scene.rotation.y += 0.005` — continuous auto-rotation, no guard
**Evidence:** No `prefers-reduced-motion` check. No `aria-hidden` on canvas.
No static fallback provided.
**Impact:** Continuous 3D rotation is a high-risk vestibular trigger. The canvas
element is present in the accessibility tree without meaningful semantics. Under
`prefers-reduced-motion: reduce`, users receive no accommodation.
**Fix:**
```typescript
// Apply to the canvas element before starting
canvas.setAttribute("aria-hidden", "true");

if (prefersReduced) {
  canvas.style.display = "none";
  document.getElementById("product-fallback")?.removeAttribute("hidden");
}
// Reduced-motion path renders one static frame in the F-02 fix above
```
```html
<!-- In the calling page HTML -->
<canvas id="product-viewer" aria-hidden="true"></canvas>
<img src="/product-static.jpg" alt="Product — front view"
     id="product-fallback" hidden />
```
**Verification:** Enable OS Reduce Motion — confirm canvas is hidden, static image
is visible, and no RAF callbacks fire.

## Positive Findings
- Three.js and `GLTFLoader` are the correct tools for a 3D product viewer
- Camera position and field of view are reasonable for a product display context

## Required Changes
1. F-02 (High, escalates to Critical if SPA mount/unmount confirmed): Return a cleanup function; cancel RAF; dispose renderer and application-owned GPU resources including material textures
2. F-03: Add `prefers-reduced-motion` guard; `aria-hidden` on canvas; static image fallback
3. F-01 (conditional): Add origin allowlist if `modelUrl` can originate from user-controlled input

## Recommended Improvements
- Add `webglcontextlost` handler for mobile resilience
- Add `ResizeObserver` to update `camera.aspect` and `renderer.setSize` on canvas resize
- Enforce server-side file-size limit for GLTF assets to prevent resource exhaustion

## Validation Plan
- Pass an external-origin URL — confirm rejected without logging the URL (F-01)
- Mount and unmount — Chrome Memory panel before/after — confirm renderer released (F-02)
- Performance panel after cleanup — confirm no further RAF callbacks (F-02)
- macOS Reduce Motion enabled — confirm canvas hidden, static image visible (F-03)
- VoiceOver enabled — confirm canvas is not announced

## Final Recommendation
Fix before shipping and re-review. If the calling context confirms repeated SPA mounting, escalate F-02 to Critical and treat status as BLOCKED.
```
