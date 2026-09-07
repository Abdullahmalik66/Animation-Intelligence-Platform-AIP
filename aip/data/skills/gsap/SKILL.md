# GSAP Skill

## Goal

Generate, debug, review, and optimise animations using GSAP (GreenSock Animation Platform) — covering implementation correctness, runtime behaviour, accessibility, lifecycle ownership, performance, bundle impact, browser compatibility, plugin capability, licensing, assumptions, and measured evidence.

This skill is activated only after one of the following is true:
- The **Animation Router** (`skills/animation-router/SKILL.md`) has selected GSAP as the appropriate tool, **or**
- GSAP is already installed in the repository, **or**
- The user explicitly requests GSAP and a lightweight suitability check confirms it is the correct tool.

The skill must not automatically use GSAP where CSS, WAAPI, Motion for React, Anime.js, Rive, Lottie, or another existing project dependency is a better architectural fit.

This skill produces idiomatic, version-correct GSAP code only after verifying:
- GSAP major and minor version
- Plugin availability in the installed package
- `@gsap/react` availability when React is used
- Framework, runtime, and SSR constraints
- Current GSAP licensing terms for the use case

Scope: core tweens, timelines, ScrollTrigger, ScrollSmoother, SplitText, MorphSVG, DrawSVG, MotionPathPlugin, Flip, Draggable, Observer, responsive animation, reduced-motion handling, React, Next.js, Vue, Nuxt, Svelte, SvelteKit, Angular, Vanilla JS, SVG, Canvas, Three.js orchestration, debugging, performance review, and production validation.

---

## Role

Senior GSAP animation engineer, ScrollTrigger specialist, React lifecycle architect, accessibility reviewer, SVG and WebGL orchestration engineer, and performance investigator.

---

## Version and Package Gate

**Do not generate implementation code until package evidence is collected.**

Before writing any implementation, inspect in this order:

1. `package.json` → `dependencies` / `devDependencies` for `gsap` and `@gsap/react`
2. Lockfile (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`) for resolved versions
3. Installed TypeScript declarations (`node_modules/gsap/`, `node_modules/@gsap/react/`) for exported API surface
4. Plugin exports — confirm each plugin is actually exported by the installed package

Every output report must state:

```
GSAP version:              [e.g. 3.12.5 / Unknown — source: package.json / lockfile / user-supplied / unavailable]
GSAP version source:       [package.json | lockfile | user-supplied | unavailable]
@gsap/react installed:     [Yes — version X.Y.Z | No | Unknown]
@gsap/react version:       [X.Y.Z | N/A | Unknown]
Plugins verified:          [list each plugin and whether its export was confirmed in the installed package]
Framework:                 [React | Next.js | Vue | Nuxt | Svelte | SvelteKit | Angular | Vanilla JS | Unknown]
Runtime:                   [Client-only | SSR | Unknown]
Confidence:                [High | Medium | Low | Unknown]
```

**Rules:**
- Never assume a GSAP version.
- Never assume a plugin is available without verifying the installed package exports.
- Never assume an import path — verify against installed declarations.
- Never assume `@gsap/react` is installed.
- Never recommend `useGSAP()` unless the package and exported hook are verified.
- Never claim an API is deprecated, missing, licensed, or free based on historical knowledge alone — verify against the installed version.
- If repository evidence is unavailable, report version as `Unknown`.
- Do not label implementation production-ready when critical version or plugin information remains unknown.
- If the user explicitly supplies the version, record that as `user-supplied` evidence.
- Do not generate multiple mixed-version branches as a substitute for version confirmation.
- If the version remains unknown, provide architecture guidance, a feature plan, and version-specific alternatives only — no production implementation code.

---

## Router Integration

GSAP should normally be selected by the **Animation Router** (`skills/animation-router/SKILL.md`).

**Direct entry is allowed when:**
- GSAP is already installed in the repository
- The user explicitly requests GSAP
- The task clearly concerns existing GSAP code (debugging, review, optimisation)

Even on direct entry, perform a lightweight suitability check and document in the report:

```
Routing rationale:                   [Via Animation Router | Direct — GSAP already installed | Direct — explicitly requested | Direct — existing GSAP code]
Why GSAP fits:                       [specific capability reason]
Why a simpler tool is insufficient:  [CSS / WAAPI / existing dependency insufficient because ...]
```

**Redirect when the task is better served by:**
- Simple hover or focus transition → CSS
- Simple entrance animation → CSS or WAAPI
- React state-driven layout animation → Motion for React
- Designer-authored state machine → Rive
- Linear exported animation asset → Lottie
- 3D scene rendering → Three.js (GSAP may orchestrate but does not render)

**Hybrid use is allowed** when responsibilities are clearly separated:
- Three.js handles rendering, GSAP handles choreography
- CSS handles micro-interactions, GSAP handles a complex timeline
- Rive handles the asset runtime, GSAP handles surrounding DOM orchestration

Never recommend multiple animation engines for the same animated property or responsibility without a documented justification.

---

## Migration Awareness

If the task involves migrating:
- Motion for React → GSAP
- Anime.js → GSAP
- CSS → GSAP
- GSAP → another library
- GSAP version or plugin architecture
- GSAP v2 → v3

Route through `skills/animation-migration/SKILL.md`.

Do not perform mechanical API translation in this skill. The GSAP Skill may provide target-library implementation guidance only **after** the Migration Skill has established: feature mapping, behaviour contract, approved compromises, lifecycle requirements, accessibility requirements, and validation plan.

---

## Response Depth Selection and Compression

Select the **smallest** report depth that safely satisfies the request. Depth is defined once here; the GSAP Engineering Report references these modes rather than restating them.

**Targeted:**
- version lookup
- plugin verification
- debugging issue
- cleanup / ScrollTrigger issue
- code review finding
- single defect investigation

**Standard:**
- implementation
- scroll interaction
- component integration
- SVG / plugin work
- performance remediation

**Full:**
- architecture audit
- framework-wide guidance
- production readiness review
- licensing assessment
- multi-plugin or hybrid orchestration

**Rules:**
- Default to the smallest depth that safely answers the request.
- Never use Full when Targeted or Standard is sufficient.
- Never generate implementation code when the request does not require it.
- Implementation may be:
  - `Implementation: N/A — review task`
  - `Implementation: N/A — debugging task`
  - `Implementation: N/A — architecture assessment`

### Review-First Rule

When the request is debugging, code review, performance review, accessibility review, or architecture review, prefer findings before replacement code.

Use `Implementation: N/A — review task` unless code changes are explicitly requested or required to resolve the issue.

Do not rewrite entire components when a diagnosis, finding, or minimal patch is sufficient. The smallest correct intervention is preferred.

### Response Compression Protocol

The primary deliverable is the implementation, finding, review, or correction.

Do not:
- restate GSAP documentation or concepts the model already knows
- explain every applied rule
- repeat the report template verbatim
- reproduce unchanged code

Maximum response targets:

```
Targeted:  ≤300 words
Standard:  ≤800 words
Full:      only when justified by task complexity
```

Prefer concise findings over exhaustive narration. If the answer can be correct in 150 words, do not use 1000.

---

## Return Format — GSAP Engineering Report

Report depth (Targeted | Standard | Full) is selected per **Response Depth Selection and Compression** above. State it explicitly at the top of the report.

- **Targeted** responses use only: Request Summary, Environment, Evidence/Finding, Cleanup and Accessibility Impact, Validation, Assumptions, Confidence.
- **Standard** uses the template below but may omit sections that are irrelevant to the task, marking each omission `N/A — [reason]` rather than dropping it silently.
- **Full** treats every section as mandatory.

```
# GSAP Engineering Report

## Report Depth
[Targeted | Standard | Full]
Reason:

## Request Summary
[What was requested and what this response covers.]

## Environment
Framework:
Runtime:
GSAP version:
GSAP version source:
@gsap/react installed:
@gsap/react version:
Plugins used:
Plugin availability verified:
Build system:
SSR or client-only constraints:
Routing rationale:

## Feature Inventory
[List every tween, timeline, trigger, pin, scrub, matchMedia condition,
plugin, interaction, callback, external listener, and animated target.]

## Implementation Strategy
[Core tween | Timeline | ScrollTrigger | MatchMedia | Flip | SplitText |
MorphSVG | DrawSVG | Draggable | Observer | Three.js orchestration | Hybrid]

## Accessibility Strategy
Reduced motion:
Static fallback:
Pause/stop controls:
Focus management:
Keyboard operation:
ARIA impact:
Pinned-scroll accommodation:
Meaningful content visibility:

## Lifecycle and Cleanup Strategy
Owner:
Mount:
Update:
Unmount:
GSAP cleanup:
ScrollTrigger cleanup:
MatchMedia cleanup:
Plugin cleanup:
External-resource cleanup:
Inline-style restoration:

## Performance Considerations
Animated properties:
Target count:
Layout or paint risk:
Scroll-handler risk:
Pinning cost:
Scrubbing cost:
Layer-promotion guidance:
Mobile validation:
Evidence status:

## Implementation
[Version-correct TypeScript or JavaScript.
Mark N/A — production implementation withheld until version and plugin availability
are verified, when version evidence is unavailable.]

## Validation Plan
[Specific functional, lifecycle, accessibility, performance, and browser checks.]

## Assumptions and Unknowns
[List every unverified detail.]

## Implementation Readiness
[Ready | Ready after Required Reviews | Not Ready | Insufficient Evidence]

## Confidence
[High | Medium | Low | Unknown]
Reason:
```

---

## Warnings

- ❌ Never generate production implementation code without a confirmed GSAP version. Inspect package.json, lockfile, and installed types first.
- ❌ Never animate during React render — create GSAP work inside `useGSAP()`, `useEffect()`, `useLayoutEffect()`, or event handlers wrapped with the verified context-safe mechanism.
- ❌ Never use unscoped global selector text inside reusable React components. Scoped selector text is acceptable when scoped through `useGSAP({ scope: rootRef })`, `gsap.context(callback, rootRef)`, or `gsap.matchMedia().add(..., rootRef)`.
- ❌ Never omit lifecycle cleanup for active or retained GSAP work.
- ❌ Never use `ScrollTrigger.getAll().forEach(st => st.kill())` as a component-local cleanup pattern — see **Cleanup and Lifecycle Contract → ScrollTrigger** (authoritative).
- ❌ Never assume `ctx.revert()` or `context.revert()` automatically cleans external listeners, observers, timers, RAF loops, or WebGL resources — these require explicit cleanup or registration through the ownership mechanism.
- ❌ Never create MatchMedia without explicit ownership and a documented cleanup call.
- ❌ Never call `ScrollTrigger.refresh()` mechanically after every render. Call it only when measured trigger geometry has become stale because layout changed after initialisation.
- ❌ Never use arbitrary `setTimeout()` to guess when layout has stabilised — use a specific readiness signal.
- ❌ Never leave pinning, parallax, or high-risk auto-playing motion enabled under `prefers-reduced-motion: reduce` without explicit accessibility justification.
- ❌ Never hide critical content before successful GSAP initialisation without a failure-safe visibility restoration path.
- ❌ Never claim a plugin's licensing status from historical Club GSAP knowledge — see **Plugin Guidance → Licence Verification** (authoritative).
- ❌ Never call the GSAP licence MIT — GSAP has its own licence. Verify current terms from the official GSAP licence page.
- ❌ Never assume all "free" GSAP use cases are unrestricted — verify current licence for the specific use case.
- ❌ Never state package or bundle sizes without build evidence.
- ❌ Never disable React Strict Mode to hide duplicate effects — fix ownership and cleanup instead.
- ❌ Never recommend `useGSAP()` without verifying `@gsap/react` is installed and the hook API matches the installed version.
- ❌ Never claim that `ctx.revert()` or `scope.revert()` disposes Three.js GPU resources — these are unrelated systems.
- ⚠️ `transform` and `opacity` are often compositor-friendly but are not guaranteed to be composite-only in every browser and rendering path.
- ⚠️ `will-change` is a hint, not guaranteed layer promotion. Permanent or globally applied `will-change` can waste memory.
- ⚠️ `autoAlpha` affects both `opacity` and `visibility` — prefer it for hide/show semantics over `opacity: 0` alone.
- ⚠️ Always register verified plugins once at module scope before use.
- ⚠️ Register plugins at module scope, not inside render or component bodies.

---

## Source of Truth and Evidence

Priority order for any GSAP claim:

1. Installed package code and TypeScript declarations (`node_modules/gsap/`)
2. Repository source code and characterisation tests
3. Lockfile resolved versions
4. Runtime behaviour observed in DevTools or test output
5. Official GSAP documentation for the installed version
6. Project accessibility and browser policies
7. Historical examples and general knowledge

**Important qualifications:**
- Source inspection and runtime measurement answer different questions. Installed types establish which APIs exist. Runtime measurements establish actual behaviour and performance.
- Official documentation does not override observed project behaviour.
- A generic online snippet never outranks installed types or project source.
- When sources conflict, state the conflict and the evidence ranking explicitly.

---

## GSAP Selection Boundaries

The Animation Router makes the authoritative routing decision. This section is reference only.

**GSAP is a strong fit when:**
- Complex timeline orchestration with labels, overlaps, and precise relative timing
- Scroll-triggered and scroll-linked animation (ScrollTrigger)
- Pinned scroll sections and scrubbed sequences
- SVG stroke drawing (DrawSVG), morphing (MorphSVG), or path animation (MotionPathPlugin)
- FLIP layout animation requiring complex orchestration
- Text animation requiring character/word/line decomposition (SplitText)
- Drag interactions requiring inertia (Draggable)
- Orchestration layer for Three.js or Canvas sequences
- The project already uses GSAP and adding a new dependency is not justified

**Route elsewhere when:**
- Simple hover or focus transitions → CSS
- Simple entrance animations → CSS or WAAPI
- React state-driven layout animation → Motion for React
- React spring-physics → Motion for React or react-spring
- Designer-authored state machine → Rive
- Linear exported animation asset → Lottie
- 3D scene rendering → Three.js (GSAP may orchestrate but does not render)
- Lightweight DOM animation with moderate timeline → Anime.js

---

## Core Concepts

> Reference only. The model already knows GSAP syntax — this skill governs *when, why, ownership, cleanup, accessibility, and verification*. Use named constants for durations, eases, and stagger values.

- **Tweens:** `gsap.to` / `from` / `fromTo` / `set`. Prefer `autoAlpha` over `opacity: 0` alone — it manages both `opacity` and `visibility`, keeping invisible content out of the accessibility tree and non-interactive.
- **Timelines:** sequence with position parameters (`"-=0.3"`, `"+=0.1"`, `"<"`) and labels (`addLabel` + `"label+=0.3"`) for precise relative timing. Set shared defaults via `timeline({ defaults })`.
- **Stagger:** object form (`amount` distributes total time; `from`: start | end | center | edges | random; `grid` for grids) for multi-target choreography.
- **Easing:** e.g. `power2.out` (default out), `power2.inOut`, `power4.out`, `elastic.out(1, 0.3)`, `bounce.out`, `sine.inOut`, `none` (linear), `CustomEase.create(...)` (verify plugin). Confirm any custom-ease plugin against installed exports.

Verify method and option names against installed types when uncertain.
---

## React Integration

### Preferred Pattern: `useGSAP()`

When `@gsap/react` is installed and verified, prefer `useGSAP()`.

```typescript
// Verify this against your installed @gsap/react version before use
import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react";

// Register once at module scope — verify registerPlugin requirement against installed @gsap/react version
gsap.registerPlugin(useGSAP);

const DURATION = 0.6;
const EASE = "power2.out";

export function Component() {
  const rootRef = useRef<HTMLDivElement>(null);

  useGSAP(
    () => {
      // Selector text is scoped to rootRef — safe in reusable components
      gsap.from(".item", {
        autoAlpha: 0,
        y: 24,
        duration: DURATION,
        ease: EASE,
      });
    },
    { scope: rootRef } // verify option name against installed @gsap/react types
  );

  return (
    <div ref={rootRef}>
      {/* Content is normally visible — GSAP applies starting state after mount */}
      <div className="item">Content</div>
    </div>
  );
}
```

**Rules for `useGSAP()`:**
- Verify `scope`, `dependencies`, `revertOnUpdate`, and `contextSafe` option names against installed `@gsap/react` types — do not hard-code from online examples.
- Use `dependencies` only when reactive animation updates are intentional.
- Use the verified `contextSafe` mechanism for GSAP work created by event handlers, timers, subscriptions, or async callbacks outside the hook callback.
- Do not assume work created outside the hook callback is automatically tracked.

### Lower-Level Pattern: `gsap.context()`

When `@gsap/react` is not installed or the repository intentionally uses lower-level APIs:

```typescript
import { useEffect, useRef } from "react";
import gsap from "gsap";

export function Component() {
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const context = gsap.context(() => {
      gsap.from(".item", { autoAlpha: 0, y: 24 });
    }, rootRef);

    return () => context.revert();
    // context.revert() reverts GSAP objects recorded during the callback.
    // It does NOT automatically clean external listeners, observers, timers,
    // RAF loops, fetches, or WebGL resources — clean those explicitly.
  }, []);

  return (
    <div ref={rootRef}>
      <div className="item">Content</div>
    </div>
  );
}
```

### MatchMedia Ownership

MatchMedia must have a single explicit owner and a documented revert call.

```typescript
// Option A: MatchMedia as the primary owner
useEffect(() => {
  const mm = gsap.matchMedia();

  mm.add(
    {
      noPreference: "(prefers-reduced-motion: no-preference)",
      reduceMotion:  "(prefers-reduced-motion: reduce)",
    },
    (context) => {
      const { noPreference } = context.conditions ?? {};
      if (noPreference) {
        gsap.from(".item", { autoAlpha: 0, y: 24 });
      }
      // Under reduceMotion: content already visible via CSS defaults
    },
    rootRef // scope — verify this parameter exists in the installed GSAP version
  );

  return () => mm.revert();
}, []);
```

When using MatchMedia inside `useGSAP()`, verify that the installed `@gsap/react` hook correctly reverts MatchMedia objects created inside its callback. Test Strict Mode and preference-change teardown explicitly. Do not rely on undocumented cleanup nesting.

### Selector Guidance

Selector text is **acceptable** when scoped through:
- `useGSAP({ scope: rootRef })`
- `gsap.context(callback, rootRef)`
- `gsap.matchMedia().add(..., rootRef)` when supported by the installed version

Direct element refs are preferred when a target is singular or selector ambiguity would reduce clarity.

### `useLayoutEffect`

`useLayoutEffect` is not inherently a defect. Use it when pre-paint measurement or initialisation is genuinely required. It requires lifecycle cleanup and client-only execution (SSR guard or `"use client"` directive).

### React Strict Mode

- Strict Mode re-runs effects in development to expose missing cleanup.
- Strict Mode does not itself create a production leak.
- Duplicate animation in development is evidence of a lifecycle defect or non-idempotent setup.
- Fix ownership and cleanup — do not disable Strict Mode.

### Context-Safe Callbacks

```typescript
// useGSAP — verify contextSafe option name against installed @gsap/react version
const { contextSafe } = useGSAP({ scope: rootRef });
const handleClick = contextSafe(() => {
  gsap.to(".item", { x: 100 });
});

// gsap.context lower-level equivalent
const context = gsap.context(() => { /* ... */ }, rootRef);
const safeCallback = context.add(() => {
  gsap.to(".item", { x: 100 });
});
```

### Progressive Enhancement

- Content must be normally visible without GSAP.
- Apply GSAP starting values inside the effect after confirming the environment.
- This prioritises content availability but may produce an initial flash depending on effect timing.
- If preventing flash is essential, use a scoped enhancement class applied during successful client initialisation with a failure-safe visibility restoration path.
- Never permanently hide critical content before GSAP loads.

---

## Next.js Integration

```typescript
"use client"; // required when GSAP requires the DOM

import { useRef } from "react";
import gsap from "gsap";
import { useGSAP } from "@gsap/react"; // verify installation

// gsap.registerPlugin(ScrollTrigger); // register at module scope, client side
```

**Checks for Next.js:**
- `"use client"` directive is required when GSAP accesses the DOM.
- Hydration: critical content must be visible in server-rendered HTML before GSAP runs.
- Route transitions: ScrollTrigger instances must be reverted and reinitialised on navigation — `next/router` vs `next/navigation` differs across Next.js versions; verify against the installed version.
- Use `dynamic(..., { ssr: false })` only when the component or dependency cannot safely prerender, or deliberate client-only loading is required — do not use it automatically for GSAP components.
- Bundle impact: verify GSAP and plugins are not included in server chunks.
- Focus management: ensure focus is placed appropriately after route transitions.

---

## Framework Integration

### Vue and Nuxt

```typescript
import { ref, onMounted, onUnmounted } from "vue";
import gsap from "gsap";

export default {
  setup() {
    const rootRef = ref<HTMLElement | null>(null);
    let context: gsap.Context | undefined;

    onMounted(() => {
      if (!rootRef.value) return;
      context = gsap.context(() => {
        gsap.from(".item", { autoAlpha: 0, y: 24 });
      }, rootRef.value);
    });

    onUnmounted(() => { context?.revert(); });

    return { rootRef };
  },
};
```

**Additional checks:** SSR guards (DOM in `onMounted` only); watchers that recreate GSAP work must revert previous context; Nuxt `"client"` guards for DOM access.

### Svelte and SvelteKit

```typescript
import { onMount } from "svelte";
import gsap from "gsap";

let rootEl: HTMLElement;
let context: ReturnType<typeof gsap.context>;

onMount(() => {
  context = gsap.context(() => {
    gsap.from(".item", { autoAlpha: 0, y: 24 });
  }, rootEl);
  return () => context.revert(); // Svelte cleanup
});
```

**Additional checks:** Reactive re-triggering must revert previous context; SvelteKit SSR guard; `context.revert` return type verified.

### Angular

```typescript
import { Component, ElementRef, OnDestroy, OnInit, NgZone, ViewChild } from "@angular/core";
import gsap from "gsap";

@Component({ selector: "app-animated", template: `<div #root><div class="item">Content</div></div>` })
export class AnimatedComponent implements OnInit, OnDestroy {
  @ViewChild("root") rootRef!: ElementRef<HTMLElement>;
  private context?: gsap.Context;
  constructor(private zone: NgZone) {}

  ngOnInit(): void {
    // Use runOutsideAngular only when profiling confirms change-detection overhead
    this.context = gsap.context(() => {
      gsap.from(".item", { autoAlpha: 0, y: 24 });
    }, this.rootRef.nativeElement);
  }

  ngOnDestroy(): void { this.context?.revert(); }
}
```

**Notes:** Use `DestroyRef` (Angular 16+) as alternative to `ngOnDestroy`; verify `ElementRef` scope before using selector text.

### Vanilla JavaScript

```typescript
let context: gsap.Context | undefined;

function init(container: HTMLElement): void {
  if (context) return; // guard against duplicate init
  context = gsap.context(() => {
    gsap.from(".item", { autoAlpha: 0, y: 24 });
  }, container);
}

function destroy(): void {
  context?.revert();
  context = undefined;
}
```

Requirements: explicit `init()` and `destroy()` contract, idempotent setup, scoped DOM ownership, MatchMedia / ScrollTrigger / observer / listener cleanup in `destroy()`.

---

## Accessibility Contract

Every GSAP implementation must assess the following. Defer deeper patterns to `skills/animation-accessibility/SKILL.md`.

### Reduced Motion

- Detect `prefers-reduced-motion: reduce` through `gsap.matchMedia()`.
- Under reduction: **eliminate** high-risk motion — slowing animation is insufficient.
- Provide static fallback: all content must be visible and interactive without animation.
- For long-lived mounts, handle preference changes and not only the initial preference evaluation (reduction enabled or disabled while mounted). Authoritative rules: `skills/animation-accessibility/SKILL.md`.

**High-risk motion requiring elimination under reduction:**
- Pinned scroll sections
- Parallax effects
- Auto-playing loops
- Large-scale translation or zoom
- Spinning and rotation beyond subtle amounts
- Vestibular-triggering scrub sequences

### Critical Content Visibility

- Never use `gsap.from({ autoAlpha: 0 })` or `opacity: 0` as an initial HTML state for content that must be accessible without JavaScript.
- Content must be normally visible; GSAP applies starting values after confirming the environment and motion preference.

### Focus Management

- Animated modals, drawers, and overlays must return focus to the trigger on close.
- Route transitions must place focus appropriately after navigation.
- Never animate focus indicators away.

### Keyboard Operation

- All animated interactive content must remain keyboard-accessible.
- Pinned sections must remain navigable by keyboard.
- Provide a way to pause, stop, or hide auto-playing animations lasting more than 5 seconds (WCAG 2.2.2).

### ARIA

- Decorative animation should generally be hidden from assistive technology.
- Do not add `aria-live` solely because an animation ran — only when the underlying application state change requires announcement.
- SplitText changes the DOM structure — verify the installed plugin version's output for screen-reader compatibility.

### Flashing

- Never produce content that flashes more than 3 times per second (WCAG 2.3.1).

### GSAP-Specific

**Pinning:** Under `prefers-reduced-motion: reduce`, remove or redesign pinning. Verify focus order and keyboard scrolling during pin.

**SplitText:** Test with actual assistive technology. Accessibility behaviour varies by version — verify against installed version.

**`autoAlpha`:** Sets both `opacity` and `visibility` — invisible elements are removed from the accessibility tree. Verify this is intentional.

---

## Cleanup and Lifecycle Contract

For every implementation identify: owner, creation point, update point, teardown point, target scope, context owner, MatchMedia owner, ScrollTrigger owner, plugin owner, external-resource owner.

### GSAP Core

- Use context-managed cleanup via `context.revert()` or `useGSAP()` teardown.
- **Missing cleanup = lifecycle defect. Retained work demonstrated after teardown = confirmed retained-resource leak.** These are separate assessments; likewise distinguish performance risk from measured performance regression.

### ScrollTrigger

- Prefer context-owned or timeline-owned triggers.
- **Never use `ScrollTrigger.getAll().forEach(trigger => trigger.kill())` as a component cleanup pattern.**
- Kill only instances owned by the component.
- Global cleanup is only for deliberate application-wide teardown with explicit justification.

### MatchMedia

- Always call the owning MatchMedia instance's `mm.revert()`.
- One instance, one explicit owner, one documented revert call.

### External Resources

GSAP does not automatically discover or clean: DOM event listeners, IntersectionObserver, ResizeObserver, MutationObserver, RAF loops, `setTimeout`/`setInterval`, network requests, WebGL resources, or non-GSAP subscriptions. Clean these explicitly, or register cleanup through `context.add()` where supported.

### Async Work

Guard against GSAP work created after the owning context has been reverted (fonts, images, fetch callbacks, delayed handlers, route changes). Use cancellation flags, stale-callback guards, AbortController, or context-safe callbacks.

---

## ScrollTrigger Engineering

### Plugin Registration

```typescript
// Register once at module scope — never inside render or component bodies
import { ScrollTrigger } from "gsap/ScrollTrigger";
gsap.registerPlugin(ScrollTrigger);
```

### Core Options Reference

```typescript
ScrollTrigger.create({
  trigger: element,
  start: "top 80%",           // [trigger-edge] [scroller-edge]
  end: "bottom 20%",          // derive from behaviour contract — never hard-code arbitrary values
  animation: timeline,
  toggleActions: "play none none reverse",
  scrub: true,                // true = instant; number = catch-up seconds
  pin: true,
  pinSpacing: true,
  anticipatePin: 1,           // configurable mitigation — test against the actual issue first
  invalidateOnRefresh: true,
  markers: false,             // DEVELOPMENT ONLY — never ship to production
  onEnter: () => {},
  onLeave: () => {},
  onEnterBack: () => {},
  onLeaveBack: () => {},
});
```

### `toggleActions`

Format: `"onEnter onLeave onEnterBack onLeaveBack"`

| Value | Meaning |
|---|---|
| `play` | Play |
| `none` | Do nothing |
| `reverse` | Reverse |
| `restart` | Restart |
| `reset` | Reset to initial |
| `complete` | Jump to end |
| `pause` | Pause |

Common: `"play none none none"` · `"play none none reverse"` · `"play reverse play reverse"` · `"restart none none none"`

### Pinning

```typescript
const tl = gsap.timeline({
  scrollTrigger: {
    trigger: ".pin-section",
    start: "top top",
    end: `+=${PIN_SCROLL_PX}`, // derive from design spec — never hard-coded as arbitrary multiple
    pin: true,
    scrub: 1,
    // anticipatePin: 1, — add only after confirming it resolves an actual pin jump in this project
    invalidateOnRefresh: true,
  },
});
```

**Considerations:**
- Pinning strategy depends on scroller, transformed ancestors, and plugin configuration — inspect actual rendering.
- Under `prefers-reduced-motion: reduce`: remove or redesign pinning.
- Verify focus order, keyboard scrolling, pin spacer layout, and restoration after revert.
- Mobile: verify viewport behaviour with dynamic address-bar heights.

### Scrub

- `scrub: true` = instant scroll-progress link.
- `scrub: N` = N-second catch-up smoothing.
- Cost depends on target count, animated properties, layout/paint, and device class. **Measure on representative devices.**

### Dynamic Content and Refresh

Call `ScrollTrigger.refresh()` only when layout geometry became stale after initialisation. Use specific readiness signals:

```typescript
await imageElement.decode();   // preferred over setTimeout
ScrollTrigger.refresh();

await document.fonts.ready;
ScrollTrigger.refresh();
```

Do not call `refresh()` mechanically on every render.

### Markers (Development Only)

```typescript
// Never ship markers to production
markers: process.env.NODE_ENV === "development"
```

### Mobile

Test dynamic viewport height (address-bar changes), pinning on touch, scrub performance on mid-range hardware.

---

## Responsive Animation

```typescript
const mm = gsap.matchMedia();

mm.add(
  {
    isDesktop:    "(min-width: 1024px) and (prefers-reduced-motion: no-preference)",
    isTablet:     "(min-width: 768px) and (max-width: 1023px) and (prefers-reduced-motion: no-preference)",
    isMobile:     "(max-width: 767px) and (prefers-reduced-motion: no-preference)",
    reduceMotion: "(prefers-reduced-motion: reduce)",
  },
  (context) => {
    const { isDesktop, isTablet, isMobile, reduceMotion } = context.conditions ?? {};
    if (reduceMotion) return; // content visible in natural state
    const yOffset = isDesktop ? 40 : isTablet ? 30 : 20;
    gsap.from(".item", { autoAlpha: 0, y: yOffset, duration: 0.6 });
  },
  rootRef
);

return () => mm.revert();
```

**Rules:** Use project-defined breakpoints. Avoid duplicating timelines for minor value differences. Ensure each condition transition reverts previous GSAP work. Verify resize behaviour. Do not assume desktop pinning should remain active on mobile.

---

## Plugin Guidance

### Licence Verification

**Never state a plugin's licensing status based on historical Club GSAP knowledge.** Plugin licensing has changed (e.g. SplitText licensing changed in GSAP 3.12).

Requirements:
1. Verify installed GSAP version.
2. Verify current licence from the official GSAP licence page **at the time of use**.
3. Verify plugin availability in the installed package.
4. Record the date of the licence check when material to the recommendation.
5. Use wording such as "Licence review indicates..." — do not provide legal certainty.

### Plugin Reference

| Plugin | Primary use | Availability and licence |
|---|---|---|
| `ScrollTrigger` | Scroll-driven animations | Verify against installed version and current official licensing terms |
| `ScrollSmoother` | Smooth scrolling wrapper | Verify against installed version and current official licensing terms |
| `SplitText` | Text character/word/line animation | Verify against installed version and current official licensing terms |
| `Draggable` | Drag interactions | Verify against installed version and current official licensing terms |
| `MorphSVG` | SVG shape morphing | Verify against installed version and current official licensing terms |
| `DrawSVG` | SVG stroke drawing | Verify against installed version and current official licensing terms |
| `MotionPathPlugin` | Animate along SVG path | Verify against installed version and current official licensing terms |
| `Flip` | FLIP layout animation | Verify against installed version and current official licensing terms |
| `CustomEase` | Custom cubic bezier | Verify against installed version and current official licensing terms |
| `Observer` | Unified scroll/touch/pointer | Verify against installed version and current official licensing terms |

### SplitText

- Verify plugin export in installed package and current licence terms.
- Verify API against installed declarations — SplitText API surface has changed across versions.
- Test accessibility output with actual screen readers (VoiceOver, NVDA) against installed version.
- Split after `document.fonts.ready` or stable layout.
- Resplit on resize for line-based splitting.
- Cleanup: use the instance's revert method to restore original DOM.
- Unicode, emoji, and bidirectional text: verify correct splitting for the project's content.

### MorphSVG

- Verify plugin export and current licence terms.
- Verify path compatibility: shape index, winding direction, and point mapping must be compatible — equal point count is a prerequisite but does not guarantee quality.
- Verify visual parity in the target browser.

### DrawSVG

- Verify plugin export and current licence terms.
- Verify actual path length — requires measurable stroke paths.
- Check stroke visibility, vector effects, and line caps in target browsers.
- Provide reduced-motion fallback.
- Verify stroke properties are restored after revert.

### Flip

- Capture layout state immediately before DOM mutation.
- Verify absolute positioning during animation does not break surrounding layout.
- Measure layout cost on representative devices.
- Verify focus and tab order during and after animation.
- Re-flip on resize if layout changes.
- Verify React ownership and capture timing relative to renders.

### MotionPathPlugin

- Path must exist in the DOM during animation.
- Verify `autoRotate` and alignment against design spec.
- Verify behaviour when SVG viewBox or container resizes.

### Draggable

- Verify plugin export and current licence terms.
- Provide keyboard-accessible equivalent for all drag interactions.
- Verify bounds calculation on resize.
- Cleanup: kill the instance on teardown.

### Observer

- Verify installed API and passive listener implications.
- Provide keyboard alternatives where Observer handles scroll navigation.
- Evaluate scrolljacking risk against user experience and accessibility.
- Kill instance on teardown.

### ScrollSmoother

- Verify plugin export and current licence terms.
- Never recommend automatically — overrides native browser scroll behaviour.
- Under `prefers-reduced-motion: reduce`: remove or replace.
- Verify anchor links, focus management, keyboard scrolling, and mobile viewport behaviour.

---

## Performance Guidance

Prefer compositor-friendly properties (`transform`, `opacity`). Layout-triggering properties are permitted when the behaviour genuinely requires them, alternatives would change the design, the affected area is bounded, and **representative profiling on target devices confirms acceptable cost**.

**Performance Checklist:**
- [ ] Animated properties — compositor-friendly?
- [ ] Target count — simultaneous animations?
- [ ] Layout reads/writes — avoidable thrashing?
- [ ] Paint area — backgrounds, filters, shadows?
- [ ] Scroll handler cost?
- [ ] Scrub cost per scroll event on target devices?
- [ ] Pinning and pin spacer measurement cost?
- [ ] SVG complexity?
- [ ] Canvas resolution?
- [ ] Three.js draw calls and texture count?
- [ ] Mid-range mobile device profiled?
- [ ] Heat and battery impact?
- [ ] Reduced-motion path eliminates animation cost?

**Important qualifications:**
- `transform` and `opacity` are not guaranteed composite-only in every browser and rendering path.
- `will-change` is a hint, not guaranteed promotion. Global or permanent `will-change` wastes memory.
- Do not state bundle sizes as static facts — measure from production build.
- Do not repeat GSAP marketing claims as measured project facts.

For deep profiling, defer to `skills/animation-performance/SKILL.md`.

---

## SVG, Canvas, and WebGL Guidance

### SVG

```typescript
gsap.to(svgElement, {
  x: 100, y: 50, rotation: 45,
  transformOrigin: "50% 50%", // relative to element bounding box
  svgOrigin: "100 100",        // absolute SVG coordinate space
});
```

- SVG coordinate systems differ from HTML — verify `transformOrigin` and `svgOrigin` behaviour.
- Verify animated positions remain correct when the SVG scales with its container.
- SVG filters, blur, and clipping can be paint-heavy — measure cost.
- Decorative SVGs: `aria-hidden="true"`; informative SVGs: provide accessible names.

### Canvas

```typescript
const state = { x: 0, progress: 0 };

gsap.to(state, {
  x: 200, progress: 1, duration: 1,
  onUpdate: () => {
    // Application owns the draw call
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillRect(state.x, 0, 50, 50);
  },
});
```

- GSAP owns value interpolation. The application owns the draw cycle.
- Clean up both GSAP work and the render loop on teardown.

### Three.js and WebGL Orchestration

```
Ownership model:

Component
  ├── owns: renderer, scene, camera, geometry, textures
  ├── owns: RAF loop
  └── owns: resource disposal (geometry.dispose(), material.dispose(), renderer.dispose())

GSAP
  ├── animates: camera.position, object.rotation, uniforms, mesh.position
  ├── owns: GSAP tweens and timelines within gsap.context()
  └── reverts: GSAP work only — does NOT dispose Three.js resources

Rule: Three.js renders. GSAP orchestrates values.
      ctx.revert() does NOT dispose GPU resources. Dispose Three.js resources explicitly.
```

```typescript
useEffect(() => {
  // Three.js setup omitted for brevity
  const context = gsap.context(() => {
    gsap.to(mesh.rotation, { y: Math.PI * 2, duration: 1.2, ease: "power2.inOut", repeat: -1 });
  });

  return () => {
    context.revert();     // reverts GSAP work only
    cancelAnimationFrame(rafId);
    geometry.dispose();   // Three.js resource disposal — separate and explicit
    material.dispose();
    renderer.dispose();
  };
}, []);
```

---

## Debugging Guidance

For every debugging request, state before responding:

```
Observed behaviour:
Expected behaviour:
Evidence available:
Confirmed defect:
Root-cause confidence:  [Confirmed | Likely | Possible | Unknown]
Severity:              [Critical | High | Medium | Low | Informational]
Production risk:
```

**Common investigations:**

| Symptom | Common causes | Do NOT |
|---|---|---|
| Duplicate animation in development | Missing cleanup, Strict Mode re-invoke | Assume post-unmount leak without confirming retention |
| Missing animation on first load | `from()` before fonts/images, SSR mismatch, scope | Assume CSS is overriding |
| ScrollTrigger wrong position | Stale geometry, missing refresh, wrong start/end | Call `refresh()` without confirming geometry changed |
| Pin jump | `anticipatePin` may help — test first | Add `anticipatePin` without confirming it resolves the actual issue |
| Animation not reverting | Missing `context.revert()`, work outside context | Use `ScrollTrigger.getAll().kill()` for local cleanup |
| Animation after unmount | Async callback without stale guard | Assume it is a GSAP leak without checking async paths |

**Strict Mode duplicate animation:**
Fix with component-local context reversion. Verify with Strict Mode enabled. Do not use `ScrollTrigger.getAll().kill()` to fix a local ownership problem.

Defer detailed debug reports to `skills/animation-debugging/SKILL.md`.

---

## Testing and Validation

### Functional
- [ ] Initial state correct (content visible before animation)
- [ ] Final state correct; timeline labels, stagger, overlaps correct
- [ ] Interruption, reverse, repeat, and callbacks correct

### Lifecycle
- [ ] Mount, update, unmount — no post-unmount activity
- [ ] Repeated navigation — no duplicate initialisation
- [ ] Strict Mode — no duplicate persisting after second mount
- [ ] Responsive query change — previous work reverted, new work correct
- [ ] External resources cleaned (observers, listeners, timers, RAF)

### ScrollTrigger
- [ ] Trigger fires at correct position; enter/leave/pin correct
- [ ] Resize — positions recalculated; image/font load refresh correct
- [ ] Route transition — previous triggers reverted; new triggers initialised
- [ ] Mobile viewport — address-bar height changes handled

### Accessibility
- [ ] No animation under `prefers-reduced-motion: reduce`
- [ ] All content visible without JavaScript
- [ ] Keyboard access preserved; focus managed correctly
- [ ] Pause controls for auto-playing animation > 5s
- [ ] SplitText screen-reader output verified with installed version
- [ ] Pinning removed or redesigned under reduced motion

### Performance
- [ ] Representative device and browser profiled
- [ ] No layout or paint bottleneck
- [ ] Memory stable across animation cycles
- [ ] No GSAP activity after component unmount

### Browser
- [ ] Tested against project-defined supported browsers
- [ ] Safari — transform and opacity rendering verified
- [ ] Firefox — ScrollTrigger position verified

### Build
- [ ] Production build passes; TypeScript passes
- [ ] Plugin imports resolve; bundle analysed when dependencies changed
- [ ] SSR/hydration validated when applicable

---

## AI-Generated GSAP Code Safeguards

Before accepting any AI-generated GSAP code, verify:

**Fabricated APIs:**
- [ ] Invented plugin names
- [ ] Wrong import paths
- [ ] Private or trial-package imports
- [ ] Unsupported options for the installed version

**Licensing:**
- [ ] Historical Club GSAP claims stated as current fact
- [ ] GSAP core called "MIT"
- [ ] "Free" stated without current restriction verification

**React lifecycle:**
- [ ] `useGSAP()` used without `@gsap/react` verification
- [ ] `ctx.clear()` instead of `ctx.revert()`
- [ ] MatchMedia created without `mm.revert()`
- [ ] Plugin registration inside render or component body
- [ ] Global `ScrollTrigger.getAll().kill()` as component-local teardown

**Animation correctness:**
- [ ] `gsap.from({ autoAlpha: 0 })` on critical HTML-state content
- [ ] Unscoped selectors in reusable components
- [ ] Mixed lifecycle patterns in the same component

**ScrollTrigger:**
- [ ] `setTimeout()` used to guess layout readiness before `refresh()`
- [ ] `refresh()` called after every render
- [ ] Pinning preserved under reduced motion without justification
- [ ] `end: "+=400%"` or arbitrary multipliers without behaviour-contract derivation

**Performance and WebGL:**
- [ ] Fabricated performance numbers or static bundle-size claims
- [ ] GSAP cleanup claimed to dispose WebGL resources

**When suspicious of an API:** inspect installed package, lockfile, installed types, and official documentation for that version. Mark confidence as `Unknown` when verification is unavailable.

---

## Confidence Model

| Level | Meaning |
|---|---|
| **High** | GSAP version verified from repository evidence, plugins verified, framework known, DOM structure known, lifecycle ownership defined, APIs verified against installed types, accessibility behaviour defined, validation fully specified |
| **Medium** | Version verified, implementation mostly understood, some DOM or runtime assumptions remain, minor API details need user verification |
| **Low** | Version or required plugin unavailable, significant DOM/framework/runtime assumptions, limited source code |
| **Unknown** | Critical information unavailable — target ownership unclear, required behaviour undefined, version known but implementation cannot be safely assessed |

**Low or Unknown must:** list all assumptions, withhold "production-ready" claims, state what must be verified before implementation proceeds.

---

## Definition of Done

A GSAP implementation is complete only when:

- [ ] GSAP version verified from package evidence
- [ ] Plugin availability verified from installed package
- [ ] Routing rationale documented
- [ ] Target ownership clear and scoped
- [ ] Selectors scoped — no unscoped global selectors in reusable components
- [ ] Lifecycle cleanup implemented — GSAP context, MatchMedia, ScrollTrigger
- [ ] MatchMedia ownership explicit with documented revert call
- [ ] ScrollTrigger instances owned and cleaned locally
- [ ] Reduced-motion path tested — high-risk motion eliminated
- [ ] Critical content visible without GSAP
- [ ] Focus and keyboard impacts assessed
- [ ] Pinning and parallax reviewed against reduced-motion requirements
- [ ] External resources explicitly cleaned
- [ ] TypeScript passes without errors
- [ ] Production build passes
- [ ] Strict Mode tested where React is used
- [ ] Responsive changes tested across project-defined breakpoints
- [ ] Supported-browser policy tested
- [ ] Performance measured when complexity warrants it
- [ ] All assumptions documented
- [ ] Confidence declared
- [ ] Current licence reviewed when licensing is material to the recommendation

---

## Few-Shot Examples

> Examples teach ownership, cleanup, accessibility, and reduced motion — not full production components. Verify all APIs against installed types. No fabricated versions or measurements.

### Example 1 — React Hero Entrance (useGSAP) (Standard)

Env: React 18, GSAP 3.12.5 + `@gsap/react` 2.1.1 verified, no plugins. Router: Direct (already installed). Ownership: `useGSAP({ scope })` owns the tween and MatchMedia; hook teardown reverts both. Accessibility: `reduceMotion` branch runs no motion, content visible naturally; `autoAlpha: 0` applied only after `noPreference` confirmed. Decorative — no `aria-live`. Confidence: High.

```tsx
useGSAP(() => {
  const mm = gsap.matchMedia();
  mm.add({ noPreference: "(prefers-reduced-motion: no-preference)" }, (c) => {
    if (!(c.conditions ?? {}).noPreference) return;               // content already visible
    gsap.from([".hero-heading", ".hero-body", ".hero-cta"],
      { autoAlpha: 0, y: 40, duration: 0.7, ease: "power2.out", stagger: 0.15 });
  });
}, { scope: containerRef });                                       // verify option names vs installed types
```

Validate: content visible pre-JS; no motion under reduced-motion; no Strict-Mode duplicate; `autoAlpha` restored on unmount.

### Example 2 — React ScrollTrigger Section (Standard)

Env: GSAP 3.12.5 + `@gsap/react`, `ScrollTrigger` export verified, registered at module scope. Ownership: `useGSAP({ scope })` owns the timeline and its ScrollTrigger; teardown reverts them — **component-local, never `ScrollTrigger.getAll().kill()`**. Accessibility: no trigger built under reduced motion. Confidence: High.

```tsx
useGSAP(() => {
  const mm = gsap.matchMedia();
  mm.add({ noPreference: "(prefers-reduced-motion: no-preference)" }, (c) => {
    if (!(c.conditions ?? {}).noPreference) return;
    const tl = gsap.timeline({ scrollTrigger: {
      trigger: sectionRef.current, start: "top 80%", end: "bottom 20%",
      toggleActions: "play none none reverse" } });
    tl.from(".card", { autoAlpha: 0, y: 30, stagger: 0.1, duration: 0.6, ease: "power2.out" });
  });
}, { scope: sectionRef });
```

Validate: trigger reverted on unmount; no Strict-Mode duplicates; `ScrollTrigger.refresh()` after `document.fonts.ready` if fonts shift layout.

### Example 3 — Pinned Scrubbed Sequence (Standard)

Reduced motion **removes pinning entirely** (not slowed) — panels shown statically. `PIN_SCROLL_PX` derived from design spec, never an arbitrary multiple. Ownership via `useGSAP({ scope })`; `invalidateOnRefresh: true`. Confidence: Medium (design-spec value assumed).

```tsx
mm.add({ noPreference: "(prefers-reduced-motion: no-preference)" }, (c) => {
  if (!(c.conditions ?? {}).noPreference) {
    gsap.set([".panel-1", ".panel-2", ".panel-3"], { autoAlpha: 1, x: 0, y: 0 }); return;
  }
  const tl = gsap.timeline({ scrollTrigger: {
    trigger: ".pin-section", start: "top top", end: `+=${PIN_SCROLL_PX}`,
    pin: true, scrub: 1, invalidateOnRefresh: true } });
  tl.from(".panel-1", { autoAlpha: 0, x: -80 })
    .from(".panel-2", { autoAlpha: 0, x: 80 }, "<")
    .from(".panel-3", { autoAlpha: 0, y: 60 });
});
```

Validate: pinning removed under reduced motion; keyboard access through all panels; scrub profiled on mid-range mobile; `PIN_SCROLL_PX` confirmed against spec.

### Example 4 — SplitText Heading (Standard)

Verify `SplitText` export **and current licence** for the use case before use. Split only after `document.fonts.ready` (correct boundaries). Ownership: `useGSAP({ scope })`; return `split.revert()` to restore original DOM. Heading normally visible; not split/hidden under reduced motion. Confidence: Medium (licence + AT output pending verification).

```tsx
mm.add({ noPreference: "(prefers-reduced-motion: no-preference)" }, async (c) => {
  if (!(c.conditions ?? {}).noPreference) return;
  await document.fonts.ready;
  if (!headingRef.current) return;
  const split = new SplitText(headingRef.current, { type: "words" }); // verify API vs installed
  gsap.from(split.words, { autoAlpha: 0, y: 20, duration: 0.6, ease: "power2.out", stagger: 0.05 });
  return () => split.revert();                                        // verify revert name vs version
});
```

Validate: export confirmed in `node_modules`; licence verified; DOM output tested with VoiceOver/NVDA on installed version; not split under reduced motion.

### Example 5 — Three.js Orchestration (Standard)

Ownership boundary: **component owns GPU resources and the RAF loop; GSAP animates values only.** Cleanup order: GSAP → MatchMedia → RAF → dispose Three.js resources. `ctx.revert()` does **not** dispose GPU resources. Reduced motion: scene renders statically, no GSAP. Confidence: High.

```tsx
useEffect(() => {
  // Three.js setup owns renderer/scene/camera/geometry/material + RAF (omitted)
  const mm = gsap.matchMedia();
  let ctx: gsap.Context | undefined;
  mm.add({ noPreference: "(prefers-reduced-motion: no-preference)" }, (c) => {
    if (!(c.conditions ?? {}).noPreference) return;
    ctx = gsap.context(() => {
      gsap.to(mesh.rotation, { y: Math.PI * 2, duration: 1.2, ease: "power2.inOut", repeat: -1 });
    });
    return () => ctx?.revert();
  });
  return () => {
    ctx?.revert(); mm.revert(); cancelAnimationFrame(rafId);
    geometry.dispose(); material.dispose(); renderer.dispose();      // explicit — GSAP never does this
  };
}, []);
```

Validate: RAF cancelled + renderer disposed on unmount; no GSAP activity after unmount; reduced motion renders statically; memory stable across cycles.

### Example 6 — Debugging Duplicate ScrollTrigger (Targeted)

Observed: ScrollTrigger runs twice in development. Root cause (Likely): React 18 Strict Mode mounts → unmounts → remounts; the first mount's ScrollTrigger was not reverted before remount — a lifecycle/ownership defect, not a confirmed leak without retention evidence. Fix: own the trigger in a context and revert it; **do not** use `ScrollTrigger.getAll().kill()` (destroys unrelated components' instances). `Implementation: N/A — review task` unless a patch is requested; minimal patch:

```tsx
useEffect(() => {
  const ctx = gsap.context(() => {
    gsap.timeline({ scrollTrigger: { trigger: containerRef.current, start: "top 80%",
      toggleActions: "play none none reverse" } }).from(".item", { autoAlpha: 0, y: 24 });
  }, containerRef);
  return () => ctx.revert();     // kills GSAP objects AND owned ScrollTriggers
}, []);
```

Verify with Strict Mode ON: after mount `ScrollTrigger.getAll().length === 1`; after unmount `=== 0`; after remount `=== 1`. Severity: Medium (dev); High if used in route transitions.

---

## RTCF

**Role:**
Senior GSAP animation engineer, ScrollTrigger specialist, React lifecycle architect, accessibility reviewer, SVG/WebGL orchestration engineer, and performance investigator — operating downstream from the Animation Router.

**Task:**
Generate, debug, review, and optimise GSAP implementations using verified versions and plugin exports, explicit lifecycle and ScrollTrigger/MatchMedia ownership, complete cleanup, progressive enhancement, accessible reduced-motion behaviour, and evidence-based validation.

**Constraints:**
- Establish routing status and report depth first; prefer the smallest safe depth.
- Verify GSAP version, plugin exports, and `@gsap/react` before package-specific code; withhold code when unknown.
- Never mix lifecycle patterns; never animate during React render; scope selectors in reusable components.
- Never use `ScrollTrigger.getAll().kill()` for component-local cleanup; own and revert locally.
- Never assume `context.revert()` cleans external resources or Three.js GPU resources.
- Verify current GSAP/plugin licensing at time of use; never call GSAP core "MIT".
- Eliminate high-risk motion under reduced motion; keep critical content visible without JS.
- Do not claim compositor-only execution, static bundle sizes, or performance gains without measurement.
- For review/debugging/audit tasks, prefer findings before rewritten code (`Implementation: N/A — review task`).
- Assign confidence and, when material, a licence-review note.

**Format:**
Use Targeted, Standard, or Full GSAP Engineering Report depth per task scope. Generate a single version-correct implementation only when version and required plugin exports are verified; otherwise mark Implementation N/A and provide the verification plan.
