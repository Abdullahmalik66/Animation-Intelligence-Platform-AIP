# Shared Governance — Canonical Rules

> **Canonical, deduplicated governance.** Each rule retains provenance to its
> monolithic source (which remains authoritative until the release gate in
> `docs/migration.md` is passed). Rule IDs are stable and referenced by
> manifests, the context assembler, and validators.
> Last provenance verification: 2026-08-25.

## GOV-VERSION — Version and Package Gate
**Provenance:** `skills/{gsap,animejs,motion,motion-react,lottie,rive,threejs,animation-router}/SKILL.md § Version and Package Gate`
**Release-gating: yes (never dropped from context).**

- Do not generate package-specific implementation code until package evidence is collected (package name, exact version, installed exports/declarations, version source).
- The installed package is authoritative. Never infer APIs from package-name lists or stale taxonomies.
- Never generate multiple package-variant implementations as a substitute for verification.
- If package/version/exports are unknown: `Implementation: N/A — insufficient evidence` + a verification plan.

## GOV-EVIDENCE — Claim-Specific Evidence Hierarchy
**Provenance:** `skills/{rive,threejs,animation-router}/SKILL.md § Claim-Specific Evidence`

- Package/API: installed code → installed types → lockfile → version-matched docs → general knowledge.
- Runtime behaviour: reproduced runtime/profiler → characterisation test → source inspection → documentation expectation.
- Performance: representative measurement → repeatable trace → build analysis → hypothesis.
- Generic snippets never outrank installed exports or actual assets.

## GOV-DEPTH — Response Depth and Compression
**Provenance:** 7 technology skills § "Response Depth Selection" / "Response Compression Protocol"

- Depths: Targeted (≤300 words) | Standard (≤800 words) | Full (only when justified).
- Default to the smallest depth that safely answers the request.
- Never generate implementation code when not required: `Implementation: N/A — [reason]`.

## GOV-REVIEW-FIRST — Review-First Rule
**Provenance:** technology skills § "Review-First Rule"

- For debug/review/accessibility/architecture tasks: findings before replacement code; smallest correct intervention over rewrite.

## GOV-OWNERSHIP — Ownership and Cleanup
**Provenance:** technology skills § "Ownership and Cleanup Contract"
**Release-gating: yes.**

- Every animated resource has one documented owner: instance, loop, listeners, observers, assets, GPU/WASM resources.
- Verify the teardown method name against the installed runtime — never assume it.
- Never double-clean (hook cleanup + duplicate imperative cleanup).
- Distinguish **lifecycle defect** (missing teardown) from **confirmed leak** (demonstrated retention after teardown).

## GOV-A11Y — Accessibility Core
**Provenance:** `skills/animation-accessibility/SKILL.md`; reduced-motion sections of all technology skills
**Release-gating: yes.**

- Classify purpose first: Decorative | Informational | Status-indicating | Interactive.
- Reduced motion: define a meaningful static/minimal state (never assume first frame); handle preference changes while mounted for long-lived components.
- Keyboard parity for any interactive animation; DOM owns semantics and focus.
- No flashing >3×/second (WCAG 2.3.1); auto-motion >5s needs pause/stop (WCAG 2.2.2).
- Status is driven by application state, not by the visual animation; never auto-create `aria-live`.
- Technology-specific extensions live in each manifest (e.g. GSAP: remove/redesign pinning and parallax under reduction).

## GOV-SECURITY — Security and Provenance
**Provenance:** `references/security.md`; technology skills § security sections
**Release-gating: yes.**

- Same-origin ≠ trusted. Require approved, integrity-controlled asset sources.
- Treat designer assets (.json/.riv/.glb) as untrusted input; validate origin, delivery, decoder features.
- Verify CSP/WASM/CDN behaviour per package/bundler/deployment — never claim universal compatibility.
- Never expose secrets in animation configuration or reports.

## GOV-PERF — Performance Discipline
**Provenance:** `skills/animation-performance/SKILL.md`

- Distinguish **performance risk** (predicted) from **measured regression** (evidenced).
- Never fabricate sizes, benchmarks, or savings — measure or mark as hypothesis.
- Animate `transform`/`opacity` by default; layout-triggering properties require justification.

## GOV-READINESS — Implementation Readiness
**Provenance:** technology skills § "Production Readiness"
**Release-gating: yes.**

`Ready | Ready after Required Reviews | Not Ready | Insufficient Evidence`
— assigned only from verified gates (version, ownership, accessibility, security, validation).

## GOV-CONFIDENCE — Confidence Model
**Provenance:** all skills § "Confidence Model"

`High | Medium | Low | Unknown` — independent of readiness. Low/Unknown must list assumptions and withhold "production-ready" claims.

## GOV-ROUTING — Router Authority
**Provenance:** `skills/animation-router/SKILL.md`; technology skills § "Router Applicability"

- Router is authoritative for architecture selection; specialists state
  `Router Decision Status: Required | Already Established | Exempt`.
- Always evaluate: does animation provide genuine value? Can no-animation, CSS, or WAAPI solve it before adding a dependency?
