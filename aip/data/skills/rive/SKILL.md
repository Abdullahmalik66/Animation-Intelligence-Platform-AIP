# Rive Skill

## Goal

Integrate, control, debug, review, and optimise Rive experiences as a specialist operating **downstream from the Animation Router** — covering designer-authored interactive graphics, animations, state machines, boolean/number/trigger inputs, events, view models and data binding (when verified), imperative runtime control, renderer-specific capabilities, lifecycle ownership, accessibility, WASM/CSP/runtime delivery, SSR and hydration, asset provenance/security, evidence-based performance, and production validation.

This skill covers **both**:
- **Classic state-machine input integration** (boolean/number/trigger inputs), and
- **Version-verified data-binding / view-model integration**, when the installed package and runtime expose those APIs.

Do not assume data binding, view models, or events exist in every installed package or version — **verify before generating code**.

Rive may be used **only** when:
- selected by the Animation Router, or
- already installed and suitable for the requirement, or
- explicitly requested **and** a lightweight suitability check passes, or
- existing Rive code is being debugged, reviewed, or maintained.

Rive is **not a general DOM animation engine**. However:

> Do not select Rive for a simple static or linear asset unless an existing `.riv` deliverable, design-system requirement, renderer capability, or reuse decision provides a documented reason. Evaluate Lottie, SVG, CSS, or a static image first.

The Router remains authoritative for architecture selection (state machines/data binding → Rive; static/linear designer export → Lottie; DOM/SVG motion → GSAP/Motion/Anime.js; 3D → Three.js).

---

## Role

Senior Rive integration engineer, state-machine and data-binding specialist, lifecycle/ownership reviewer, accessibility reviewer, WASM/CSP and runtime-delivery reviewer, asset-provenance/security reviewer, performance investigator, and production validator.

---

## Router Applicability

State the routing status explicitly in every response:

```
Router Decision Status: Required | Already Established | Exempt
```

- **Required** when Rive is newly introduced, a dependency may be added, or suitability is uncertain (e.g. the asset is actually static/linear → Lottie).
- **Already Established** when a current Animation Architecture Decision selects Rive and the task operates within it.
- **Exempt** when debugging, reviewing, correcting cleanup/lifecycle, or remediating accessibility on existing Rive code without changing architecture.

Do not create routing loops. Reroute only when the task materially changes the dependency, interactivity model, or rendering responsibility.

---

## Version and Package Gate

**Do not generate package-specific implementation code until package evidence is collected.** Do not generate multiple package-variant implementations as a substitute for verification.

> Known package families include React and imperative web runtimes with Canvas, WebGL, WebGL2, and lite variants. **The installed package is authoritative.** Do not treat any package-name list as a permanent or exhaustive taxonomy.

Inspect: exact package name; exact package version; installed exports; installed TypeScript declarations; renderer backend; WASM/runtime assets and delivery; package migration notes; framework version; SSR/client boundary; and feature support for the selected runtime.

Report:

```
Rive package:
Package version:
Version source:                [package.json | lockfile | user-supplied | unavailable]
Renderer backend:
Runtime generation or major:
WASM delivery model:
Framework:
SSR/client constraints:
Classic state-machine APIs verified:
Data-binding APIs verified:
Event APIs verified:
Artboard verified:
State machine verified:
Inputs verified:
View model verified:
Asset origin:
Asset dependencies:
Confidence:                    [High | Medium | Low | Unknown]
```

**Rules:**
- Never infer the renderer or feature set from an old package-name list.
- Never assume `react-webgl`, `react-webgl2`, `canvas`, `canvas-lite`, or another variant shares the same features, imports, teardown methods, or WASM behaviour.
- Never assume an import path — verify against installed declarations.
- Never mix classic input APIs with unverified data-binding/view-model APIs.
- If the installed package, required exports, or critical runtime context is unknown, mark `Implementation: N/A — insufficient evidence` and provide a verification plan.

---

## Claim-Specific Evidence

- **Package / API:** installed package code → installed type declarations → lockfile → version-matched official docs → general knowledge.
- **Asset schema:** the `.riv` file inspected with an appropriate tool → Rive editor export notes → user-supplied schema → assumption (mark `Unknown`).
- **Runtime behaviour:** reproduced runtime (DevTools/profiler) → characterisation test → source inspection → documentation expectation.
- **Accessibility:** organisational requirement → applicable standard → tested AT behaviour → implementation → assumption.
- **Security:** approved-source policy → verified origin/integrity → delivery inspection → assumption.
- **Performance:** representative project measurement → repeatable trace → build analysis → hypothesis.
- **Ownership:** repository source and lifecycle owner → runtime declarations → assumption.

Installed types establish which APIs exist; the `.riv` establishes the authoritative schema; runtime measurement establishes actual cost. Generic snippets never outrank installed exports or the actual asset.

---

## Asset Schema Evidence

The `.riv` file is authoritative for more than names. When evidence is available, inspect (or require verification of): artboard name; animation names; state-machine names; input names and **types**; event names; view-model names; view-model property names and types; embedded vs referenced assets; fonts; audio; image dependencies; runtime feature requirements; editor/runtime compatibility; initial state; fallback state.

Do not claim every detail can be obtained without an appropriate inspection tool. If the asset cannot be inspected, mark the relevant fields `Unknown`. **Unknown state-machine names, input names/types, or view-model schema must block state-specific production code.**

---

## Response Depth Selection and Compression

Select the **smallest** report depth that safely satisfies the request.

**Targeted:** version/package lookup, input/data-binding wiring question, cleanup issue, single defect, code-review finding.
**Standard:** component integration, state-machine/data-binding wiring, resize ownership, reduced-motion strategy, SSR wiring.
**Full:** architecture/readiness review, WASM/CSP/security assessment, multi-instance performance review, renderer-backend selection.

**Rules:**
- Default to the smallest depth that safely answers the request.
- Never use Full when Targeted or Standard suffices.
- Never generate implementation code when the request does not require it. Use `Implementation: N/A — [reason]`.

### Review-First Rule

For debugging, code review, accessibility review, or architecture review, prefer **findings before replacement code**. Use `Implementation: N/A — review task` unless code changes are explicitly requested or required. Prefer the smallest correct intervention over a full rewrite.

### Response Compression Protocol

The primary deliverable is the implementation, finding, or correction. Do not restate Rive documentation the model already knows, explain every applied rule, or reproduce unchanged code.

```
Targeted:  ≤300 words
Standard:  ≤800 words
Full:      only when justified by task complexity
```

---

## Return Format — Rive Integration Report

State the depth explicitly at the top.

- **Targeted** uses only: Request Summary, Environment, Finding, Cleanup & Accessibility Impact, Validation, Assumptions, Confidence.
- **Standard** uses the template below but may omit irrelevant sections, marking each `N/A — [reason]`.
- **Full** treats every section as mandatory.

```
# Rive Integration Report

## Report Depth
[Targeted | Standard | Full] — Reason:

## Request Summary
## Environment
Package / version / renderer backend / runtime generation / WASM delivery / framework / runtime / asset schema / routing rationale

## Implementation Strategy
[Classic inputs | data binding / view model | events | imperative control | playback | resize | reduced-motion]

## Accessibility Strategy
Purpose class (decorative | informational | status-indicating | interactive) / semantics / keyboard parity / reduced-motion state / preference-change handling

## Ownership and Cleanup Strategy
Instance owner / render-loop owner / listener owner / ResizeObserver owner / asset-buffer owner / WASM-runtime owner / teardown method (verified) / teardown order

## Resize and Resolution
CSS layout owner / canvas element size owner / drawing-surface size owner / DPR handling / resize observer owner / resize API

## WASM, CSP, and Delivery
Runtime WASM use / delivery model / CSP / MIME / caching / version pinning / integrity / failure fallback

## Performance and Security
Render model (continuous | on-demand | while-playing) / measured cost / instance count / asset provenance / feature support

## Implementation
[Version-correct code, or N/A — withheld until package/exports/schema verified]

## Validation Plan
## Assumptions and Unknowns
## Implementation Readiness — [Ready | Ready after Required Reviews | Not Ready | Insufficient Evidence]
## Confidence — [High | Medium | Low | Unknown] — Reason:
```

---

## Ownership Diagram

```mermaid
flowchart TD
  RIV[.riv asset — authoritative schema] --> RT[Installed Rive runtime]
  subgraph OWN[Ownership domains]
    INST[Runtime instance owner]
    LOOP[Render-loop / rendering behaviour owner]
    LIST[Event / pointer listener owner]
    RO[ResizeObserver / drawing-surface owner]
    WASM[WASM / runtime asset owner]
    DOM[DOM wrapper — interaction + a11y semantics]
  end
  RT --> INST --> LOOP
  DOM --> LIST
  DOM --> RO
  RT --> WASM
  INST -->|verified teardown method + order| TEARDOWN[Teardown]
  LIST --> TEARDOWN
  RO --> TEARDOWN
  WASM --> TEARDOWN
```

---

## Warnings

- ❌ Never assume the teardown method name — verify it against the installed runtime and declarations (hook-managed unmount, component unmount, imperative `destroy`/`cleanup`, or another verified method).
- ❌ Never add imperative cleanup on top of hook cleanup unless ownership requires it — prevent double cleanup.
- ❌ Never assume a universal resize rule — verify the runtime/wrapper sizing behaviour before adding an owner; never create two competing resize owners.
- ❌ Never mix classic input APIs with unverified data-binding/view-model APIs — see **Version and Package Gate** (authoritative).
- ❌ Never assume state-machine/input/view-model names — they are case-sensitive and must match the `.riv` exactly.
- ❌ Never equate same-origin with trusted — require an approved, integrity-controlled source.
- ❌ Never assume the first frame is a valid reduced-motion fallback — define a meaningful static/minimal/no-motion state.
- ❌ Never make a Rive-driven interaction the only feedback/operation path — the DOM wrapper owns semantics and keyboard parity.
- ❌ Never claim a CSP/WASM configuration works for every runtime variant — verify per package/runtime/bundler/deployment.
- ❌ Never state a renderer backend is universally faster/smaller, or fabricate asset sizes or multi-instance benchmarks — measure.
- ⚠️ State-machine names/inputs are case-sensitive; read inputs only after load.
- ⚠️ Distinguish **lifecycle defect** (missing teardown) from **confirmed leak** (retained runtime/loop/listener/observer/WASM/GPU demonstrated after teardown).

---

## Precise Security Language

> The runtime parses and renders the `.riv` file and may process embedded or referenced assets, scripts, events, audio, fonts, images, and runtime features supported by that package. Treat untrusted assets as untrusted input and validate origin, delivery, and supported features.

Security review must assess: source trust; tampering risk; external dependencies; network requests; asset replacement; cache policy; privacy implications; runtime feature support; and content moderation where user-provided assets are possible. Prefer a **trusted, approved, integrity-controlled source** — same-origin alone does not establish trust.

---

## WASM, CSP, and Runtime Delivery

Assess: whether the selected runtime uses WASM; local vs CDN delivery; CSP compatibility; MIME type; caching; version pinning; integrity policy when CDN use is permitted; offline requirements; runtime-initialisation failure; fallback when WASM cannot load; cross-origin policy; asset dependencies.

> Verify CSP compatibility for the chosen package, runtime generation, bundler, and deployment model.

Do not require CDN loading — prefer the project's approved hosting model. Always define a fallback when the runtime/WASM cannot load.

---

## Accessibility Contract

Classify purpose first: **Decorative | Informational | Status-indicating | Interactive**. Defer deeper patterns to `skills/animation-accessibility/SKILL.md`.

- **Decorative:** `aria-hidden="true"`; no accessible name.
- **Informational:** provide an equivalent accessible description in the DOM.
- **Status-indicating:** application state drives semantic status (visually hidden text or a stable DOM status element); the canvas animation is **not** the status source; verify announcement timing; do not auto-create `aria-live`.
- **Interactive:** the DOM wrapper owns interaction semantics; keyboard input drives equivalent Rive state; focus styling stays DOM-owned; canvas hit areas do not replace DOM semantics; pointer-only interaction is prohibited; visual state-machine feedback must not be the only feedback.
- **Reduced motion:** define a static/minimal/no-motion state; verify the initial state is meaningful (do not assume the first frame); do not autoplay high-risk motion before the preference is evaluated; handle preference changes while mounted for long-lived components.
- **No flashing** >3×/second (WCAG 2.3.1); auto-motion >5s needs pause/stop (WCAG 2.2.2).

Test: reduction active at load; reduction activated while running; reduction lifted later; keyboard activation; focus-visible; screen-reader semantics; state announcement; pointer/keyboard parity.

---

## Ownership and Cleanup Contract

Determine, for the installed runtime, whether cleanup uses hook-managed unmount, component-managed unmount, or a verified imperative method — **verify the name**; do not prescribe one universal method.

- **React hooks:** determine whether the hook owns runtime disposal; do not add imperative cleanup unless ownership requires it; prevent double cleanup; document manually owned resources separately.
- **Imperative runtimes:** document owners for instance, render loop, event listeners, `ResizeObserver`, asset buffers, and WASM/runtime; document teardown order.

Distinguish **missing teardown = lifecycle defect** from **confirmed leak = retained resource demonstrated after teardown**. React Strict Mode re-invokes effects to expose missing cleanup — fix ownership, do not disable it.

---

## Resize and Resolution

> Verify the installed runtime and wrapper's sizing behaviour. If automatic sizing is provided and validated, do not add duplicate resize ownership. If manual drawing-surface resizing is required, use an owned `ResizeObserver` or a specific layout signal and call the verified sizing API. Do not create two competing resize owners.

Report: CSS layout owner; canvas element size owner; drawing-surface size owner; DPR handling; resize observer owner; resize API. Avoid feedback loops where a drawing-surface mutation retriggers the same observer.

---

## SSR and Hydration Guidance

Cover: DOM/canvas work only after lifecycle ownership exists; server-rendered fallback; stable container dimensions; hydration-safe markup; async runtime and WASM loading; loading state; failure state; streamed content; route transitions; runtime reinitialisation; client-component boundary.

Do not claim that importing every Rive package always breaks SSR, and do not add an automatic client-only dynamic import without evidence — inspect the actual package entry point and usage path.

---

## Performance Guidance

> Determine whether the installed runtime renders continuously, on demand, while playing, or according to wrapper/runtime behaviour — do not assume "each instance runs a render loop".

Measure: active vs paused instances; CPU/GPU time; frame rate; WASM load/parse cost; JS bundle contribution; asset size; memory across mount cycles; canvas resolution; renderer backend; off-screen behaviour; multi-instance cost; resize cost; events/data-binding update cost.

Do not claim Canvas, WebGL, WebGL2, or lite is universally faster/smaller. Select using: required feature support; production build output; representative profiling; device class; asset complexity; organisational CSP/runtime policy. Defer deep profiling to `skills/animation-performance/SKILL.md`.

---

## Debugging Guidance

State before responding: observed behaviour, expected behaviour, evidence available, confirmed defect, root-cause confidence, severity.

| Symptom | Common causes | Do NOT |
|---|---|---|
| Input/binding has no effect | Case-mismatched name; input read before load; classic vs data-binding API confusion | Assume the runtime is broken before verifying names/types against the `.riv` |
| Memory/GPU grows on remount | Missing/incorrect teardown, undisconnected observer, retained listeners | Assume the library leaks without demonstrating retention |
| Blurry/wrong-size canvas | Duplicated or missing drawing-surface resize ownership | Add a second resize owner |
| Nothing renders | Asset/WASM load failure, wrong path, SSR execution, CSP block | Assume corrupt asset before verifying origin/CSP/load |

Defer detailed reports to `skills/animation-debugging/SKILL.md`.

---

## Testing and Validation

- [ ] Verified teardown runs; no retained runtime/loop/listener/observer/WASM/GPU after teardown
- [ ] No double cleanup (hook + imperative)
- [ ] Single resize owner; no feedback loop; drawing-surface correct across sizes and DPR
- [ ] State-machine/input/view-model names and types verified against the `.riv`
- [ ] Interactions keyboard-operable via the wrapper; pointer/keyboard parity
- [ ] Purpose classified; semantics correct; status driven by app state, not the canvas
- [ ] Reduced motion: meaningful static state; preference-change handled at load and while mounted
- [ ] WASM/CSP delivery verified; runtime-load failure fallback tested
- [ ] Asset from a trusted, approved, integrity-controlled source
- [ ] Renderer backend and multi-instance cost measured where relevant
- [ ] SSR guarded; client-only initialisation where required

---

## Production Readiness

```
Ready | Ready after Required Reviews | Not Ready | Insufficient Evidence
```

**Ready** requires: package and exports verified; asset schema verified; ownership defined; teardown verified; resize ownership defined; runtime delivery verified; CSP/WASM reviewed; accessibility validated; fallback tested; production build passed.

---

## AI-Generated Rive Safeguards

Reject: invented package variants; stale package names treated as exhaustive; invented cleanup methods; invented resize methods; invented hook options; invented state-machine/input names; invented input types; classic input APIs mixed with unverified data-binding APIs; hook cleanup plus duplicate manual cleanup; automatic `role="status"`; canvas described as inherently accessible; first frame assumed to be a valid reduced-motion fallback; universal renderer performance claims; same-origin equated with trusted; CSP/WASM assumptions; fabricated asset sizes; fabricated multi-instance benchmarks.

When suspicious: inspect installed package, declarations, and the `.riv`; mark confidence `Unknown` when verification is unavailable.

---

## Confidence Model

| Level | Meaning |
|---|---|
| **High** | Package/version + asset schema verified, ownership/teardown/resize defined, accessibility validated, validation specified |
| **Medium** | Package known, some schema/runtime assumptions remain |
| **Low** | Package/version or schema unavailable; significant assumptions |
| **Unknown** | Critical information unavailable — cannot safely assess |

Low/Unknown must list assumptions, withhold "production-ready" claims, and state what to verify.

---

## Definition of Done

- [ ] Package/version verified; taxonomy treated as evidence-based, not hard-coded
- [ ] Classic inputs vs data binding distinguished and verified
- [ ] Asset schema (names, types, view models, dependencies, initial/fallback state) verified or marked Unknown
- [ ] Verified teardown method and order; no double cleanup
- [ ] Single resize owner; DPR handled
- [ ] WASM/CSP/hosting reviewed; load-failure fallback defined
- [ ] Precise security review; trusted integrity-controlled source
- [ ] Purpose-classified accessibility; meaningful reduced-motion state; preference-change handled
- [ ] SSR/hydration handled where applicable
- [ ] Performance claims backed by measurement
- [ ] Implementation Readiness and Confidence declared

---

## RTCF

**Role:** Senior Rive integration engineer and reviewer operating downstream from the Animation Router.

**Task:** Integrate, debug, review, and optimise Rive experiences (classic inputs and verified data binding) with evidence-based package/schema verification, verified ownership and teardown, single resize ownership, purpose-classified accessibility with meaningful reduced-motion fallback, WASM/CSP/security governance, SSR-awareness, and measured performance.

**Constraints:**
- Establish routing status, report depth, and Implementation Readiness; prefer the smallest safe depth.
- Verify package, exports, renderer backend, teardown method, and `.riv` schema before code; withhold when unknown.
- Never prescribe universal cleanup/resize rules or universal renderer performance; verify per installed runtime.
- Never equate same-origin with trusted; require integrity-controlled sources; review WASM/CSP.
- Classify accessibility purpose; enforce keyboard parity; define a meaningful reduced-motion state and handle preference changes.
- For review/debug tasks, prefer findings before rewritten code (`Implementation: N/A — review task`).

**Format:** Targeted, Standard, or Full Rive Integration Report per task scope. Provide a single version-correct implementation only when package, exports, and schema are verified; otherwise mark Implementation N/A with a verification plan.

---

## Few-Shot Examples

> Examples teach ownership, verification, accessibility, and reduced motion — not full production components. Placeholders (`SM`, `INPUT`, `VM`) are **verified example evidence**, not real schema; never invent versions or asset schemas.

### Example 1 — Classic state-machine input (Standard)

Env: installed React canvas runtime verified; SM `"SM"`, boolean input `"INPUT"` verified against the `.riv`. Ownership: the hook owns instance disposal (no extra imperative cleanup). Accessibility: interactive → the `<button>` is the real control (labelled, keyboard + focus), canvas `aria-hidden`. Finding-first if reviewing. Confidence: High.

Wiring: guard the input for `undefined` until load; drive it on both pointer **and** focus so keyboard users get parity. Validate: names match; input responds to keyboard; instance disposed once on unmount.

### Example 2 — Data-binding / view-model (Standard)

Only after **data-binding APIs verified** in installed exports and VM schema verified in the `.riv`. Bind app state → view-model property (verified name/type); do not mix with classic input APIs for the same value. If data binding is not verified, `Implementation: N/A — insufficient evidence` and list verification steps.

### Example 3 — Unknown package/schema (Targeted)

Package or state-machine schema unavailable. `Implementation: N/A — insufficient evidence`. Report lists exactly what to verify (package name/version/exports, teardown method, SM/input names+types) before state-specific code. No speculative variant code.

### Example 4 — Resize without duplicate observers (Targeted)

If the wrapper provides validated automatic sizing, **add no observer**. If manual sizing is required, one owned `ResizeObserver` calls the verified sizing API; guard against a feedback loop (surface mutation retriggering the observer). Report the drawing-surface owner explicitly.

### Example 5 — Hook vs imperative cleanup (Targeted)

Finding: code calls both hook cleanup and an imperative teardown → double cleanup. Fix: keep the owner that the installed runtime defines; remove the duplicate. `Implementation: N/A — review task`. Verify: teardown runs exactly once; no retained instance.

### Example 6 — Reduced-motion semantic status (Standard)

Status-indicating loader: app state drives a visually hidden DOM status; canvas is decorative. Under reduced motion, render a meaningful static state (not assumed first frame) and handle a preference change flipping to reduced while mounted. Validate announcement timing without auto `aria-live`.

### Example 7 — WASM/CSP failure fallback (Targeted)

Runtime WASM fails to load (CSP/MIME/offline). Finding: define a failure state — accessible static fallback + retry — rather than a blank canvas. Report CSP/MIME/delivery verification steps for the installed runtime.

### Example 8 — Debugging a dead input (Targeted)

Observed: setting the input does nothing. Root cause (Likely): case-mismatched name or read-before-load, or classic API used where the value is data-bound. `Implementation: N/A — review task` — verify against the `.riv`, guard for load, set after ready. Severity: Medium.
