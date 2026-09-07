# Motion for React Skill

## Goal

Generate, debug, review, and optimise animations using **Motion for React** (formerly Framer Motion, now published as `motion/react`) as a specialist operating **downstream from the Animation Router** — covering variants, gestures, `AnimatePresence` exit animations, layout and shared-element transitions, spring physics, motion values, scroll-linked hooks, reduced-motion accessibility, lifecycle correctness, SSR/hydration, version verification, and production validation.

Motion for React may be used **only** when:
- selected by the Animation Router, or
- already installed and suitable for the requirement, or
- explicitly requested **and** a lightweight suitability check passes, or
- existing Motion for React code is being debugged, reviewed, or maintained.

Motion for React must **not** be selected automatically when:
- a CSS transition/animation or WAAPI is sufficient (hover/focus/simple entrance)
- the animation involves no React state, presence, gesture, or layout change → CSS / vanilla `motion`
- complex scroll pinning or scrubbed multi-timeline orchestration is required → GSAP (via Router)
- a designer asset drives the motion → Lottie / Rive
- 3D rendering is required → Three.js

**Critical distinction:** `motion/react` and vanilla `motion` are **different APIs**. Never mix them.

---

## Role

Senior Motion for React engineer, React lifecycle and presence specialist, layout-animation reviewer, accessibility reviewer, performance investigator (motion values vs re-render), and production validator.

---

## Router Applicability

State the routing status explicitly in every response:

```
Router Decision Status: Required | Already Established | Exempt
```

- **Required** when Motion for React is newly introduced, a dependency may be added, or suitability is uncertain (e.g. a CSS hover would suffice, or GSAP is needed for scroll pinning).
- **Already Established** when a current Animation Architecture Decision selects Motion for React and the task operates within it.
- **Exempt** when debugging, reviewing, correcting presence/lifecycle, or remediating accessibility on existing Motion for React code without changing architecture.

Do not create routing loops. Reroute when the task materially changes the dependency, rendering/scroll model, or animation responsibility (scroll pinning → GSAP via Router).

---

## Version and Package Gate

**Do not generate package-specific implementation code until package evidence is collected.** The package moved from `framer-motion` to `motion`; import paths, `AnimatePresence` modes, and some hook APIs differ across versions.

Inspect in order:
1. `package.json` → `motion` or legacy `framer-motion`; confirm the correct import path (`motion/react`)
2. Lockfile for the resolved version
3. Installed exports and TypeScript declarations for the hooks/components used (`useReducedMotion`, `AnimatePresence`, `useMotionValue`, `useScroll`, `LayoutGroup`, etc.)
4. React version, Next.js App vs Pages router, SSR/RSC constraints (`"use client"` required)

Report:

```
Package:               [motion | framer-motion (legacy) | Unknown]
Package version:       [X.Y.Z | Unknown]
Version source:        [package.json | lockfile | user-supplied | unavailable]
Import path verified:  [motion/react | framer-motion | Unknown]
APIs verified:         [list hooks/components confirmed in installed exports]
React version:         [X | Unknown]
Framework:             [React | Next.js App Router | Next.js Pages Router | Unknown]
Runtime:               [Client-only | SSR / RSC | Unknown]
Confidence:            [High | Medium | Low | Unknown]
```

**Rules:**
- Never assume the import path — `motion/react` vs legacy `framer-motion` must be verified.
- Never assume a hook/component or its options exist — verify against installed declarations.
- Never confuse `motion/react` with vanilla `motion`.
- If version/exports are unavailable, report `Unknown` and withhold production code, providing an integration plan.

---

## Response Depth Selection and Compression

Select the **smallest** report depth that safely satisfies the request.

**Targeted:** version/API lookup, `AnimatePresence`/exit debugging, single defect, code-review finding.
**Standard:** component implementation, variants/gestures/layout, reduced-motion wiring, scroll-linked hook integration, performance remediation.
**Full:** architecture/readiness review, layout-animation-heavy audit, SSR/hydration assessment, library-suitability review (Motion for React vs GSAP vs CSS).

**Rules:**
- Default to the smallest depth that safely answers the request.
- Never use Full when Targeted or Standard suffices.
- Never generate implementation code when the request does not require it. Use `Implementation: N/A — [reason]`.

### Review-First Rule

For debugging, code review, accessibility review, or architecture review, prefer **findings before replacement code**. Use `Implementation: N/A — review task` unless code changes are explicitly requested or required. Prefer the smallest correct intervention over a full component rewrite.

### Response Compression Protocol

The primary deliverable is the implementation, finding, or correction. Do not restate Motion documentation the model already knows, explain every applied rule, or reproduce unchanged code.

```
Targeted:  ≤300 words
Standard:  ≤800 words
Full:      only when justified by task complexity
```

---

## Return Format — Motion for React Engineering Report

State the depth explicitly at the top.

- **Targeted** uses only: Request Summary, Environment, Finding, Accessibility & Lifecycle Impact, Validation, Assumptions, Confidence.
- **Standard** uses the template below but may omit irrelevant sections, marking each `N/A — [reason]`.
- **Full** treats every section as mandatory.

```
# Motion for React Engineering Report

## Report Depth
[Targeted | Standard | Full] — Reason:

## Request Summary
## Environment
Package / version / import path / APIs verified / React + framework / runtime / routing rationale

## Implementation Strategy
[Variants | AnimatePresence | layout/layoutId | gestures | motion values | scroll hooks | spring]

## Accessibility Strategy
useReducedMotion applied / reduced variants / focus management / gesture keyboard equivalents / autoplay controls (>5s)

## Lifecycle and Presence Strategy
Variants defined outside component / stable keys under AnimatePresence / exit correctness / motion-value subscription cleanup / SSR + "use client"

## Performance Considerations
Motion values vs re-render / layout-animation cost / transform-vs-layout properties / measurement status

## Implementation
[Version-correct code, or N/A — withheld until version/import path verified]

## Validation Plan
## Assumptions and Unknowns
## Implementation Readiness — [Ready | Ready after Required Reviews | Not Ready | Insufficient Evidence]
## Confidence — [High | Medium | Low | Unknown] — Reason:
```

---

## Warnings

- ❌ Never put complex animation values inline in the `animate` prop — define `variants` outside the component (stable reference, no recreation per render).
- ❌ Never skip `AnimatePresence` for exit animations — the exit will not play if the element unmounts directly.
- ❌ Never omit `useReducedMotion()` — reduced-motion handling is an accessibility requirement, not optional.
- ❌ Never use Motion for React for animation that involves no React state, gesture, presence, or layout change — route to CSS/WAAPI/vanilla `motion`.
- ❌ Never give `AnimatePresence` children unstable/index keys — changing keys causes unmount/remount instead of exit animation.
- ❌ Never rely on pointer-only gesture states (`whileHover`/`whileTap`) for operable controls — provide keyboard/focus equivalents.
- ❌ Never animate layout-triggering CSS directly when `layout`/transform can express it; do not claim compositor-only behaviour without measurement.
- ❌ Never import from `framer-motion` when the project is on `motion` (or vice-versa) without verifying the installed package.
- ⚠️ `layout` animations require all animating siblings to also carry `layout` for correct behaviour.
- ⚠️ `useMotionValue`/`useTransform` avoid re-renders — prefer them for scroll/drag-derived values; subscriptions must be cleaned up.
- ⚠️ In Next.js App Router, `motion` components need `"use client"`; critical content must exist in server HTML before animation.
- ⚠️ For complex scroll choreography (pinning, scrubbing), prefer GSAP ScrollTrigger via the Router.

---

## Source of Truth and Evidence

Priority: installed package code/types → repository source → lockfile → runtime behaviour in DevTools/React profiler → version-matched official docs → general knowledge. Installed types establish which hooks/props exist in the installed version; the React profiler establishes re-render cost. Generic snippets never outrank installed exports.

---

## When to Use Motion for React vs Alternatives

Use **Motion for React** for React state-driven animation, presence/exit (`AnimatePresence`), gestures, layout and shared-element (`layoutId`) transitions, and spring physics.

Route to **CSS/WAAPI** for simple hover/focus/entrance; **vanilla `motion`** for non-React or non-stateful DOM animation; **GSAP** for scroll pinning, scrubbed sequences, or complex label-driven timelines; **Lottie/Rive** for designer assets.

---

## Core Patterns (Reference)

> Reference only — the model knows the syntax. This skill governs *when, ownership, accessibility, presence correctness, and verification*.

- **Variants** defined outside the component; used via `variants` + `initial`/`animate`/`exit`, not inline objects.
- **AnimatePresence** wraps conditional/list rendering; children need stable `key`; `mode`: `"sync"` | `"wait"` | `"popLayout"`.
- **useReducedMotion()** selects a reduced variant set (opacity-only or none) — never merely a shorter duration for attention-demanding motion.
- **Layout / layoutId** for automatic layout and shared-element transitions; all animating siblings carry `layout`.
- **Motion values** (`useMotionValue`/`useTransform`/`useSpring`) for derived scroll/drag animation without triggering re-renders; clean up `.on("change", …)` subscriptions.
- **Gestures** (`whileHover`/`whileTap`/`whileFocus`) must pair pointer states with keyboard/focus equivalents.

Verify hook and prop names against installed types when uncertain.

---

## Accessibility Contract

- Apply `useReducedMotion()`; provide a reduced variant set that eliminates attention-demanding motion (opacity-only or static) — not just a faster transition.
- Manage focus for animated modals/drawers/overlays (return focus to trigger on close); place focus appropriately after route transitions.
- Gesture-driven controls must be keyboard-operable; `whileFocus` should mirror `whileHover` where the hover conveys state.
- Decorative animation hidden from assistive tech; do not add `aria-live` merely because motion ran — only when the underlying state change requires announcement.
- Auto-playing motion >5s needs pause/stop (WCAG 2.2.2); no flashing >3×/second (WCAG 2.3.1).
- For long-lived mounts, handle preference changes and not only the initial preference evaluation — confirm the reduced variant set actually swaps when the preference changes while mounted. Authoritative rules: `skills/animation-accessibility/SKILL.md`.

Defer deeper patterns to `skills/animation-accessibility/SKILL.md`.

---

## Lifecycle, Presence, and SSR Contract

- Define variants and transition constants **outside** the component for stable references.
- `AnimatePresence` children require stable unique keys; index keys cause remount, not exit.
- Clean up motion-value subscriptions (`useMotionValue().on(...)` returns an unsubscribe) and any manual scroll listeners. Distinguish **lifecycle defect** (missing teardown) from **confirmed retained-resource leak** (retention demonstrated after teardown).
- Next.js App Router: `motion` components require `"use client"`; ensure critical content is present in server-rendered HTML so animation enhances rather than gates it. Guard against hydration mismatches from motion-driven initial styles.

---

## Performance Guidance

Prefer `transform`/`opacity` and `layout` over directly animating layout-triggering CSS. Use motion values to avoid re-renders on high-frequency (scroll/drag) updates — verify with the React profiler. Layout animations have measurable cost on large trees — profile on representative devices. `transform`/`opacity` are not guaranteed composite-only in every browser/path; do not state bundle sizes without measuring the build. Defer deep profiling to `skills/animation-performance/SKILL.md`.

---

## Debugging Guidance

State before responding: observed behaviour, expected behaviour, evidence available, confirmed defect, root-cause confidence, severity.

| Symptom | Common causes | Do NOT |
|---|---|---|
| Exit animation not playing | Missing `AnimatePresence`, unstable/index key, parent unmounts | Assume a library bug before checking presence + keys |
| Layout animation jumps | Not all siblings have `layout`; measured mid-transition | Add `layout` everywhere blindly without confirming the cause |
| Scroll/drag causes re-renders | State used instead of motion values | Optimise unrelated code before checking motion-value usage |
| Import undefined | `framer-motion` vs `motion` mismatch, wrong path | Assume the export exists — verify installed package/types |
| Hydration mismatch (Next.js) | Motion-driven initial style differs server vs client | Disable SSR reflexively before understanding the mismatch |

Defer detailed reports to `skills/animation-debugging/SKILL.md`.

---

## Testing and Validation

- [ ] Variants/transitions defined outside the component
- [ ] `AnimatePresence` wraps all exit animations; children have stable keys
- [ ] `useReducedMotion()` applied; reduced variant eliminates attention-demanding motion
- [ ] Gestures keyboard/focus-operable; focus managed for modals/route changes
- [ ] Motion-value subscriptions and listeners cleaned up
- [ ] Layout animations: all animating siblings carry `layout`; cost profiled
- [ ] Correct import path (`motion/react`) verified against installed package
- [ ] Next.js: `"use client"` set; critical content in server HTML; no hydration mismatch
- [ ] Performance profiled (re-renders, layout cost) when complexity warrants
- [ ] Autoplay >5s has pause/stop controls

---

## Confidence Model

| Level | Meaning |
|---|---|
| **High** | Package/version + import path verified, APIs verified, presence/lifecycle correct, accessibility defined, validation specified |
| **Medium** | Version verified, minor API/DOM assumptions remain |
| **Low** | Version or required APIs/import path unavailable; significant assumptions |
| **Unknown** | Critical information unavailable — cannot safely assess |

Low/Unknown must list assumptions, withhold "production-ready" claims, and state what to verify.

---

## Definition of Done

- [ ] Package, version, and import path verified from evidence
- [ ] Routing rationale documented
- [ ] Required hooks/components verified against installed exports
- [ ] Variants/transitions defined outside the component
- [ ] `AnimatePresence` + stable keys for all exits
- [ ] `useReducedMotion()` applied with a genuine reduced path
- [ ] Focus and keyboard impacts assessed; gestures operable
- [ ] Motion-value subscriptions and listeners cleaned up
- [ ] SSR/hydration handled where applicable (`"use client"`, server-visible content)
- [ ] Performance profiled when complexity warrants
- [ ] Assumptions documented; confidence declared

---

## RTCF

**Role:** Senior Motion for React engineer and reviewer operating downstream from the Animation Router.

**Task:** Implement, debug, review, and optimise React animations using the verified installed `motion/react` API with variants, correct `AnimatePresence` presence, layout/shared-element transitions, accessible reduced-motion behaviour, and evidence-based validation.

**Constraints:**
- Establish routing status and report depth first; prefer the smallest safe depth.
- Verify package, version, and import path (`motion/react` vs legacy `framer-motion`) before code; withhold when unknown.
- Never confuse `motion/react` with vanilla `motion`.
- Define variants outside the component; use `AnimatePresence` with stable keys for all exits.
- Always apply `useReducedMotion()` with a genuine reduced path; make gestures keyboard-operable and manage focus.
- Clean up motion-value subscriptions/listeners; handle SSR/`"use client"` and hydration.
- Prefer motion values over state for high-frequency updates; do not claim compositor-only behaviour or bundle sizes without measurement.
- For review/debug tasks, prefer findings before rewritten code (`Implementation: N/A — review task`).

**Format:** Targeted, Standard, or Full Motion for React Engineering Report per task scope. Provide a single version-correct implementation only when version and import path are verified; otherwise mark Implementation N/A with a verification plan.

---

## Few-Shot Examples

> Examples teach presence correctness, ownership, accessibility, and reduced motion — not full production components. Verify APIs against installed types.

### Example 1 — Notification list with exit (Standard)

Env: `motion` verified, import `motion/react`; `AnimatePresence`, `useReducedMotion` confirmed. Ownership: variants defined outside; stable `key` per item. Accessibility: `useReducedMotion()` swaps to opacity-only variants; `role="log"`/`aria-live="polite"` because the underlying state change (a new notification) warrants announcement — not merely because motion runs. Confidence: High.

```tsx
// VARIANTS + REDUCED_VARIANTS defined at module scope (stable references)
const variants = prefersReducedMotion ? REDUCED_VARIANTS : VARIANTS;
<AnimatePresence mode="sync">
  {notifications.map((n) => (
    <motion.div key={n.id} variants={variants} initial="initial" animate="animate" exit="exit" />
  ))}
</AnimatePresence>
```

Validate: exit plays on removal; reduced motion = opacity-only; keys stable (no remount).

### Example 2 — Debugging missing exit animation (Targeted)

Observed: removing a list item does not play the exit animation. Root cause (Likely, two candidates): (1) the list is not wrapped in `AnimatePresence`, so the element unmounts before exit; or (2) children use index keys, so React remounts instead of animating. `Implementation: N/A — review task` — wrap the list in `AnimatePresence` and use a stable unique `key={item.id}`; no component rewrite needed.

Verify: with a stable key and `AnimatePresence`, removal animates; toggling data order does not trigger spurious remounts. Severity: Medium.

### Example 3 — Scroll parallax via motion values (Standard)

Ownership: `useMotionValue`/`useTransform` derive the parallax offset **without** re-rendering; the `.on("change", …)` subscription is unsubscribed on cleanup. Reduced motion: skip the transform (identity). Note: for pinned/scrubbed choreography, route to GSAP. Confidence: Medium (scroll wiring depends on installed API).

```tsx
const y = useTransform(scrollY, [0, 300], prefersReduced ? [0, 0] : [0, -100]);
useEffect(() => scrollY.on("change", handle), [scrollY]); // returns unsubscribe
// <motion.div style={{ y }} />  — no re-render on scroll
```

Validate: no re-renders on scroll (profiler); identity transform under reduced motion; subscription cleaned up on unmount.
