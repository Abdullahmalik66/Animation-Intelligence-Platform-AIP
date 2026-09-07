# Changelog

All notable changes to `aip` will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

---

## [3.0.0] — 2026-09-07

The project is now a product: an agent-agnostic animation intelligence layer
for coding agents, delivered as a zero-config linter for web animation code.
Installable from PyPI, runnable via `npx aip-cli`.

### Added

- `aip check` — 12 static-analysis rules across memory leaks (`leak/*`),
  accessibility (`a11y/*`), performance (`perf/*`), and dependency hygiene
  (`sec/*`, `arch/*`). No AI, no network, no config file.
- `--fix` — safe, behaviour-preserving autofixes only.
- Output formats: `human`, `json`, `sarif`, `github`.
- `aip route` — deterministic, offline technology decision from a plain-language
  request, based on the project's actual `package.json` and lockfile.
- `aip context` — packaged, section-level animation knowledge (15 topics) served
  on demand; ships inside the wheel, never copied into user projects.
- Multi-agent `aip init` / `aip init --remove` — one canonical instruction body
  delivered to Claude Code, GitHub Copilot, Cursor, Windsurf, Cline/Roo Code,
  OpenAI Codex (managed block in `AGENTS.md`), and Gemini CLI (managed block in
  `GEMINI.md`). Supports `--global` and `--force`; managed blocks are edited
  surgically, user content is never touched.
- `npx aip-cli` shim — bootstraps a private Python environment on first run.
- Knowledge pack (7 library skills + 5 references) bundled as package data
  under `aip/data/`.
- CI check that every `aip context` topic resolves against the knowledge pack.

### Changed

- Wheel is 114 KB with zero runtime dependencies (Python stdlib only).

### Removed

- Legacy provider architecture: `gateway`, `orchestrator`, `assembler`,
  `backends/`, `retrieval`, `validators`, `schema_check`, `inventory`.
- Manifests, JSON schemas, example projects, and per-framework integration
  docs from the knowledge pack.
- `validate-skills` workflow — it enforced the pre-3.0 prompt-file layout that
  no longer exists; the topic-resolution check replaces it.

---

## [1.0.0] — 2026-08-12

### Added

#### Core Skills (MVP)
- `skills/animation-router/SKILL.md` — Library selection decision tree
- `skills/gsap/SKILL.md` — GSAP animation patterns with React, ScrollTrigger, and matchMedia
- `skills/motion-react/SKILL.md` — Motion for React with variants, AnimatePresence, and accessibility
- `skills/threejs/SKILL.md` — Three.js scene setup, disposal, and React integration
- `skills/rive/SKILL.md` — Rive state machine integration and cleanup
- `skills/animejs/SKILL.md` — Anime.js lightweight animation patterns
- `skills/motion/SKILL.md` — Motion vanilla animate(), scroll(), inView() patterns
- `skills/lottie/SKILL.md` — Lottie-web integration with renderer selection and cleanup
- `skills/animation-accessibility/SKILL.md` — WCAG 2.2 compliance for animations
- `skills/animation-performance/SKILL.md` — GPU compositing, layout thrashing, bundle size
- `skills/animation-debugging/SKILL.md` — Systematic debug workflows and issue catalogue
- `skills/animation-migration/SKILL.md` — Cross-library migration guide
- `skills/animation-code-review/SKILL.md` — Structured review rubric

#### Prompts (GitHub Copilot)
- `.github/prompts/animation-router.prompt.md`
- `.github/prompts/animate.prompt.md`
- `.github/prompts/fix-animation.prompt.md`
- `.github/prompts/review-animation.prompt.md`
- `.github/prompts/optimize-animation.prompt.md`
- `.github/prompts/migrate-animation.prompt.md`

#### Agent Instructions
- `.github/copilot-instructions.md` — GitHub Copilot global instructions
- `AGENTS.md` — Universal agent instructions
- `adapters/claude/CLAUDE.md` — Claude-specific adapter
- `adapters/cursor/.cursorrules` — Cursor-specific adapter
- `adapters/generic/AGENTS.md` — Generic adapter (Kimi, Qwen, Windsurf, etc.)

#### References
- `references/library-decision-matrix.md`
- `references/accessibility.md`
- `references/performance.md`
- `references/browser-support.md`
- `references/security.md`

#### Integrations
- `integrations/react/README.md`
- `integrations/nextjs/README.md`

#### Examples
- `examples/basic/css-fade-in.css`
- `examples/basic/gsap-stagger.tsx`
- `examples/basic/motion-react-list.tsx`

#### Evals
- `evals/cases/router-001-css-hover.md`
- `evals/cases/gsap-001-cleanup.md`
- `evals/rubrics/implementation-quality.md`

#### Documentation
- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `docs/architecture.md`
- `docs/skill-authoring.md`
