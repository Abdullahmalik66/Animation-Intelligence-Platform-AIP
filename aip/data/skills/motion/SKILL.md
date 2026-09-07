# Motion (Vanilla) Skill

## Goal

Generate, debug, review, and optimise animations using **Motion** (the vanilla JS library from the Motion team, published as `motion`) as a specialist operating **downstream from the Animation Router** — covering `animate()`, `scroll()`, `inView()`, sequence/timeline APIs, lifecycle ownership and cancellation, reduced-motion handling, framework-agnostic integration (Vanilla/Vue/Svelte/Angular/React-without-`motion/react`), version correctness, and production validation.

Motion (vanilla) may be used **only** when:
- selected by the Animation Router, or
- already installed and suitable for the requirement, or
- explicitly requested **and** a lightweight suitability check passes, or
- existing Motion (vanilla) code is being debugged, reviewed, or maintained.

Motion (vanilla) must **not** be selected automatically when:
- the project is React and needs variants/presence/gestures/layout → **Motion for React** (`skills/motion-react/SKILL.md`)
- CSS transitions/animations or WAAPI are sufficient
- complex scroll pinning or multi-timeline orchestration is required → GSAP (via Router)
- a designer asset drives the motion → Lottie / Rive
- 3D rendering is required → Three.js

**Critical distinction:** `motion` (vanilla) and `motion/react` are **different APIs**. Never mix them or assume one's methods exist on the other.

---

## Role

Senior Motion (vanilla) animation engineer, version-aware integration specialist, lifecycle and cancellation reviewer, accessibility reviewer, scroll-capability reviewer, and production validator.

---

## Router Applicability

State the routing status explicitly in every response:

```
Router Decision Status: Required | Already Established | Exempt
```

- **Required** when Motion is newly introduced, a dependency may be added, or suitability is uncertain (notably: React project that likely wants `motion/react` instead).
- **Already Established** when a current Animation Architecture Decision selects Motion (vanilla) and the task operates within it.
- **Exempt** when debugging, reviewing, correcting cancellation/lifecycle, or remediating accessibility on existing Motion (vanilla) code without changing architecture.

Do not create routing loops. Reroute when the task materially changes the dependency, rendering/scroll model, or React-idiom requirement (React variants/presence → Motion for React via Router).

---

## Version and Package Gate

**Do not generate package-specific implementation code until package evidence is collected.** The Motion vanilla API surface (`animate` options, `scroll`, `inView`, sequence/timeline, `stagger`) has changed across major versions.

Inspect in order:
1. `package.json` → `motion` (and confirm it is **not** only `motion/react` usage that is intended)
2. Lockfile for the resolved version
3. Installed exports and TypeScript declarations for `animate`, `scroll`, `inView`, `stagger`, and sequence/timeline availability in the installed version
4. Framework, bundler, module format, SSR/client constraints

Report:

```
motion installed:      [Yes — version X.Y.Z | No | Unknown]
Version source:        [package.json | lockfile | user-supplied | unavailable]
API surface verified:  [animate | scroll | inView | stagger | sequence/timeline — each confirmed in installed exports]
Framework:             [Vanilla | Vue | Svelte | Angular | React (no motion/react) | Unknown]
Bundler:               [Vite | Webpack | Other | Unknown]
Runtime:               [Client-only | SSR | Unknown]
Confidence:            [High | Medium | Low | Unknown]
```

**Rules:**
- Never infer the version or available APIs from the word "Motion".
- Never assume `timeline`/sequence, `stagger`, or `scroll` signatures — verify against installed exports (they differ across versions).
- Never confuse vanilla `motion` exports with `motion/react` hooks/components.
- If version/exports are unavailable, report `Unknown` and withhold production code, providing an integration plan.

---

## Response Depth Selection and Compression

Select the **smallest** report depth that safely satisfies the request.

**Targeted:** version/API lookup, cancellation issue, single defect, code-review finding.
**Standard:** implementation, `scroll()`/`inView()` integration, reduced-motion wiring, framework integration, performance remediation.
**Full:** architecture/readiness review, platform-level integration, library-suitability review (vanilla vs `motion/react` vs GSAP).

**Rules:**
- Default to the smallest depth that safely answers the request.
- Never use Full when Targeted or Standard suffices.
- Never generate implementation code when the request does not require it. Use `Implementation: N/A — [reason]`.

### Review-First Rule

For debugging, code review, accessibility review, or architecture review, prefer **findings before replacement code**. Use `Implementation: N/A — review task` unless code changes are explicitly requested or required. Prefer the smallest correct intervention over a full rewrite.

### Response Compression Protocol

The primary deliverable is the implementation, finding, or correction. Do not restate Motion documentation the model already knows, explain every applied rule, or reproduce unchanged code.

```
Targeted:  ≤300 words
Standard:  ≤800 words
Full:      only when justified by task complexity
```

---

## Return Format — Motion (Vanilla) Engineering Report

State the depth explicitly at the top.

- **Targeted** uses only: Request Summary, Environment, Finding, Cleanup & Accessibility Impact, Validation, Assumptions, Confidence.
- **Standard** uses the template below but may omit irrelevant sections, marking each `N/A — [reason]`.
- **Full** treats every section as mandatory.

```
# Motion (Vanilla) Engineering Report

## Report Depth
[Targeted | Standard | Full] — Reason:

## Request Summary
## Environment
motion version / version source / API surface verified / framework / bundler / runtime / routing rationale

## Implementation Strategy
[animate | scroll | inView | sequence/timeline | stagger]

## Accessibility Strategy
Reduced-motion behaviour / content visible without JS / autoplay controls (>5s) / no attention-demanding scroll motion under reduction

## Lifecycle and Cleanup Strategy
Owner / creation / update / cancel() or stop() on teardown / listener + scroll/inView disposer cleanup

## Performance Considerations
Animated properties (transform/opacity vs layout) / target count / scroll-handler cost / measurement status

## Implementation
[Version-correct code, or N/A — withheld until version/exports verified]

## Validation Plan
## Assumptions and Unknowns
## Implementation Readiness — [Ready | Ready after Required Reviews | Not Ready | Insufficient Evidence]
## Confidence — [High | Medium | Low | Unknown] — Reason:
```

---

## Warnings

- ❌ Never forget to cancel/stop animations and scroll/inView disposers on teardown — retained work leaks and keeps callbacks alive.
- ❌ Never animate layout properties (`width`, `height`, `top`, `left`) — use compositor-friendly `transform`/`opacity` equivalents.
- ❌ Never confuse `motion` (vanilla) with `motion/react` — different APIs; do not import hooks/components from vanilla.
- ❌ Never leave attention-demanding scroll-linked or auto-playing motion active under `prefers-reduced-motion: reduce`.
- ❌ Never hide critical content behind an animation that only appears via JS — content must be usable without motion.
- ❌ Never state bundle sizes as fact without measuring the production build.
- ⚠️ `scroll()` and `inView()` return disposer functions — store and call them on cleanup.
- ⚠️ Verify `stagger`, sequence/timeline, and spring option names against the installed version.
- ⚠️ For scroll-pinning or complex multi-timeline choreography, GSAP is more capable — evaluate via the Router before committing.

---

## Source of Truth and Evidence

Priority: installed package code/types → repository source → lockfile → runtime behaviour in DevTools → version-matched official docs → general knowledge. Installed types establish which APIs and options exist in the installed version; runtime measurement establishes actual cost. Generic snippets never outrank installed exports.

---

## When to Use Motion (Vanilla) vs Alternatives

Use **Motion (vanilla)** for lightweight, framework-agnostic DOM animation: `animate()` calls, `inView()` entrance animations, and simple `scroll()`-linked effects in Vanilla/Vue/Svelte/Angular, or React code that deliberately avoids `motion/react`.

Route to **Motion for React** for variants, `AnimatePresence`, gestures, or layout animation. Route to **GSAP** for scroll pinning, scrubbed sequences, or complex label-driven timelines. Route to **CSS/WAAPI** for single-property transitions.

---

## Lifecycle and Cancellation Contract

Every animation, `scroll()`, and `inView()` call has an owner and a disposer:

```typescript
const animation = animate(target, keyframes, options);
const stopScroll = scroll(animate(target, { opacity: [1, 0] }), { target: el });
const stopInView = inView(target, (info) => { /* returns optional cleanup */ });

// teardown — cancel/stop ALL of them
animation.cancel();
stopScroll();
stopInView();
```

Distinguish **lifecycle defect** (missing teardown) from **confirmed retained-resource leak** (work demonstrated after teardown), and performance risk from measured performance regression.

In React (without `motion/react`): create in `useEffect`, return a cleanup that cancels every animation and calls every disposer. Strict Mode re-invokes effects to expose missing cleanup — fix ownership, do not disable Strict Mode. Guard against animations created by async callbacks after teardown.

---

## Accessibility Contract

- Detect `prefers-reduced-motion: reduce`; under reduction, eliminate attention-demanding and scroll-linked motion (an instant/opacity-only appearance is acceptable) — do not merely slow it.
- Content must be usable without JavaScript/motion; never gate critical content solely behind an animation.
- Auto-playing motion lasting >5s needs pause/stop controls (WCAG 2.2.2); no flashing >3×/second (WCAG 2.3.1).
- For long-lived mounts, handle preference changes and not only the initial preference evaluation (reduction enabled or disabled while mounted). Authoritative rules: `skills/animation-accessibility/SKILL.md`.

Defer deeper patterns to `skills/animation-accessibility/SKILL.md`.

---

## Performance Guidance

Prefer `transform`/`opacity`; avoid animating layout properties. Measure scroll-handler and multi-target cost on representative devices — `transform`/`opacity` are not guaranteed composite-only in every browser/path. Do not state bundle sizes as static facts; measure from the production build. Defer deep profiling to `skills/animation-performance/SKILL.md`.

---

## Debugging Guidance

State before responding: observed behaviour, expected behaviour, evidence available, confirmed defect, root-cause confidence, severity.

| Symptom | Common causes | Do NOT |
|---|---|---|
| Animation persists/duplicates | Missing `cancel()`/disposer, Strict Mode re-invoke | Assume a library bug before checking teardown |
| Scroll/inView keeps firing after unmount | Disposer not called | Assume `scroll`/`inView` self-clean |
| Janky animation | Layout property animated, too many targets | Blame the library before profiling |
| API undefined | Vanilla vs `motion/react` confusion, version mismatch | Assume the export exists — verify installed types |

Defer detailed reports to `skills/animation-debugging/SKILL.md`.

---

## Testing and Validation

- [ ] Every `animate()` cancelled and every `scroll()`/`inView()` disposer called on teardown
- [ ] No duplicate/persistent animation after unmount (Strict Mode tested where React)
- [ ] Reduced motion eliminates attention-demanding/scroll-linked motion
- [ ] Content usable without JS
- [ ] Only compositor-friendly properties animated (no layout thrash)
- [ ] Autoplay >5s has pause/stop controls
- [ ] `animate`/`scroll`/`inView`/`stagger`/sequence APIs verified against installed version
- [ ] SSR guarded; client-only where DOM is required
- [ ] Performance measured when complexity warrants

---

## Confidence Model

| Level | Meaning |
|---|---|
| **High** | Version + API surface verified, lifecycle/cancellation defined, accessibility defined, validation specified |
| **Medium** | Version verified, minor API/runtime assumptions remain |
| **Low** | Version or required APIs unavailable; significant assumptions |
| **Unknown** | Critical information unavailable — cannot safely assess |

Low/Unknown must list assumptions, withhold "production-ready" claims, and state what to verify.

---

## Definition of Done

- [ ] `motion` version verified from evidence
- [ ] Routing rationale documented (incl. why not `motion/react` in React projects)
- [ ] Required APIs verified against installed exports
- [ ] Every animation/scroll/inView owned and disposed on teardown
- [ ] Reduced-motion path implemented; content usable without JS
- [ ] Only compositor-friendly properties animated
- [ ] Strict Mode tested where React is used
- [ ] SSR guarded where applicable
- [ ] Performance measured when complexity warrants
- [ ] Assumptions documented; confidence declared

---

## RTCF

**Role:** Senior Motion (vanilla) animation engineer and reviewer operating downstream from the Animation Router.

**Task:** Implement, debug, review, and optimise lightweight framework-agnostic animations using the verified installed `motion` API with explicit cancellation/disposal, reduced-motion handling, and evidence-based validation.

**Constraints:**
- Establish routing status and report depth first; prefer the smallest safe depth.
- Verify `motion` version and required exports before code; withhold when unknown.
- Never confuse vanilla `motion` with `motion/react`.
- Cancel every animation and call every `scroll()`/`inView()` disposer on teardown.
- Animate only compositor-friendly properties; never layout properties.
- Eliminate attention-demanding/scroll-linked motion under reduced motion; keep content usable without JS.
- Never state bundle sizes without measurement.
- For review/debug tasks, prefer findings before rewritten code (`Implementation: N/A — review task`).

**Format:** Targeted, Standard, or Full Motion (Vanilla) Engineering Report per task scope. Provide a single version-correct implementation only when version and required exports are verified; otherwise mark Implementation N/A with a verification plan.

---

## Few-Shot Examples

> Examples teach ownership, cancellation, and reduced motion — not full production components. Verify APIs against installed types.

### Example 1 — inView entrance in React-without-motion/react (Standard)

Env: `motion` verified; `animate` + `inView` exports confirmed. Ownership: effect owns the `inView` disposer; the inner `animate` is cancelled in the callback's returned cleanup. Accessibility: reduced motion skips motion entirely (content already visible). Confidence: High.

```tsx
useEffect(() => {
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return; // content visible, no motion
  const stop = inView(sectionRef.current!, (info) => {
    const anim = animate(info.target.querySelectorAll(".item"),
      { opacity: [0, 1], y: [16, 0] }, { duration: 0.5, delay: stagger(0.08) });
    return () => anim.cancel();        // inView cleanup cancels the animation
  });
  return () => stop();                 // dispose inView on unmount
}, []);
```

Validate: items visible pre-JS; no motion under reduction; no callbacks after unmount (Strict Mode ON).

### Example 2 — Debugging scroll firing after unmount (Targeted)

Observed: scroll callback keeps running after the component unmounts. Root cause (Confirmed): `scroll()` returns a disposer that was never stored or called, so the scroll subscription outlives the component. `Implementation: N/A — review task` — store the disposer and call it in cleanup:

```tsx
const stop = scroll(animate(".hero-bg", { opacity: [1, 0] }), { target: heroEl });
return () => stop();                   // was missing
```

Verify: after unmount, scrolling triggers no further work; no retained listeners. Severity: Medium (High on route-heavy apps).

### Example 3 — Vanilla/Vue init–destroy contract (Standard)

Ownership: an explicit `init()`/`destroy()` pair owns all animations and disposers; idempotent init guards against double-setup. Reduced motion handled at entry. Confidence: High.

```typescript
let disposers: Array<() => void> = [];
function init(root: HTMLElement) {
  if (disposers.length) return;        // idempotent
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  const a = animate(root.querySelectorAll(".item"), { opacity: [0, 1], y: [16, 0] }, { duration: 0.5 });
  disposers.push(() => a.cancel());
}
function destroy() { disposers.forEach((d) => d()); disposers = []; }
```

Validate: `destroy()` cancels all work; re-`init()` does not double-animate; no layout properties animated.
