<div align="center">

# Animation Intelligence Platform (AIP)

**The zero-config linter for web animation code.**

Catches the memory leaks, accessibility violations, layout thrashing, and
performance bugs that tests miss — and shows the fix.

```bash
npx aip-cli check src/
```

[![CI](https://github.com/Abdullahmalik66/Animation-Intelligence-Platform-AIP/actions/workflows/ci.yml/badge.svg)](https://github.com/Abdullahmalik66/Animation-Intelligence-Platform-AIP/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white)
![Node](https://img.shields.io/badge/node-16%2B-339933?logo=nodedotjs&logoColor=white)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

No AI. No network. No API keys. No config file. Zero dependencies.

</div>

```text
bad-animations.jsx
    13:5  error    ScrollTrigger created but never reverted or killed. This leaks
                   on unmount and duplicates on remount.            leak/gsap-no-revert
                   → Return () => ctx.revert() from your effect.
    33:7  error    requestAnimationFrame loop with no cancelAnimationFrame. The
                   loop keeps running after the component unmounts. leak/raf-not-cancelled
                   → Store the frame id and cancelAnimationFrame(id) on cleanup.

13 problems (10 errors, 3 warnings)
4 files scanned.
```

Every finding names its rule and states the fix on the `→` line. Exit code is
`1` when there are errors, so it drops straight into CI.

---

## Why AIP Exists

Animation bugs are uniquely invisible: they don't throw, tests pass, and the
page just gets slower with every navigation — or it makes a user with a
vestibular disorder physically sick.

- ESLint doesn't know a GSAP timeline needs `revert()`.
- Lighthouse tells you the page is slow, not which `@keyframes` did it.
- Type checkers can't see that your `IntersectionObserver` outlives the component.

AIP encodes the review checklist of an experienced animation engineer and runs
it in milliseconds, on every commit.

---

## Before / After

```jsx
// ❌ Before — leaks on every unmount, no reduced-motion path
useEffect(() => {
  gsap.registerPlugin(ScrollTrigger);

  gsap.timeline({
    scrollTrigger: { trigger: '.card', start: 'top 80%' },
  })
    .from('.card', { y: 40, opacity: 0 })
    .to('.card', { opacity: 1 });
}, []);
```

```text
before.jsx
  9:5  error  Animation defined with no `prefers-reduced-motion` fallback. …  a11y/no-reduced-motion-fallback
              → Add @media (prefers-reduced-motion: reduce) { ... }
  9:5  error  gsap.timeline() created but never reverted or killed. This leaks
              on unmount and duplicates on remount.                           leak/gsap-no-revert
              → Return () => ctx.revert() from your effect.

2 problems (2 errors, 0 warnings)
```

```jsx
// ✅ After — exit code 0
useEffect(() => {
  gsap.registerPlugin(ScrollTrigger);

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const ctx = gsap.context(() => {
    gsap.timeline({
      scrollTrigger: { trigger: '.card', start: 'top 80%' },
    })
      .from('.card', { y: 40, opacity: 0 })
      .to('.card', { opacity: 1 });
  });
  return () => ctx.revert();
}, []);
```

---

## What AIP Detects

12 rules in four families. Every finding states the fix.

### Memory leaks — `leak/*` (errors)

| Rule | Catches |
| --- | --- |
| `leak/gsap-no-revert` | GSAP timeline/tween created in an effect with no `revert()` or `kill()` |
| `leak/raf-not-cancelled` | `requestAnimationFrame` loop with no `cancelAnimationFrame` |
| `leak/observer-not-disconnected` | `IntersectionObserver`/`ResizeObserver`/`MutationObserver` never disconnected |
| `leak/webgl-not-disposed` | Three.js geometries/materials/textures never `dispose()`d |
| `leak/listener-not-removed` | `addEventListener` in an effect with no matching removal |

Each one permanently retains memory after unmount, and they compound across
navigations in an SPA.

### Accessibility — `a11y/*`

| Rule | Catches |
| --- | --- |
| `a11y/no-reduced-motion-fallback` (error) | Animation with no `prefers-reduced-motion` guard |
| `a11y/no-rapid-flash` (error) | Flashing faster than 3Hz — a seizure risk (WCAG 2.3.1) |
| `a11y/infinite-no-pause` (warning) | `infinite` animation longer than 5s with no pause control (WCAG 2.2.2) |

### Performance — `perf/*`

| Rule | Catches |
| --- | --- |
| `perf/no-layout-property` (error) | Animating `left`, `top`, `width`, `height`, `margin` — forces layout on every frame |
| `perf/no-layout-thrash` (warning) | Reading `offsetWidth`/`getBoundingClientRect` inside a rAF loop that also writes |

### Dependency hygiene — `sec/*`, `arch/*`

| Rule | Catches |
| --- | --- |
| `sec/untrusted-asset` (warning) | Lottie/Rive assets loaded from an unpinned third-party origin |
| `arch/over-engineered` (warning) | A heavy animation library imported for something CSS does natively |

---

## Quick Start

### Install

Nothing to install if you have Node:

```bash
npx aip-cli check src/
```

Or install it properly:

```bash
pipx install aip     # or: pip install aip
aip check src/
```

`npx aip-cli` bootstraps a private Python environment under `~/.cache/aip` on
first run (~5s, once). It never writes into your project. Requires Python
3.10+.

### Check

```bash
aip check <path>              # lint a file or directory
aip check src/ --fix          # apply safe, mechanical fixes
aip check src/ --format json  # machine-readable output
```

`--format` accepts `human` (default), `json`, `sarif`, and `github`:

- `json` — for scripts and agents.
- `sarif` — upload to GitHub code scanning.
- `github` — emits `::error file=...` workflow annotations.

Scanned extensions: `.css`, `.scss`, `.sass`, `.less`, `.js`, `.jsx`, `.ts`,
`.tsx`, `.mjs`, `.cjs`. `node_modules`, build output, and dotfiles are skipped.

`--fix` only applies changes that cannot alter behaviour — e.g. rewriting an
animated `left`/`top` to a `transform`, or appending a
`prefers-reduced-motion` block. Anything requiring judgement (where to put a
cleanup function) is reported, never rewritten.

### Route

```bash
aip route "cards fade in as I scroll"
```

```json
{
  "technology": "css",
  "architecture": "native-css",
  "complexity": "low",
  "confidence": "Medium",
  "required_context": ["css", "accessibility"],
  "installed": []
}
```

Route is deterministic and offline — it reads your `package.json` and lockfile,
not a model. When it cannot decide confidently it returns `"technology": null`
rather than guessing.

### Context

```bash
aip context gsap      # just the GSAP lifecycle and a11y rules that matter
aip context           # list every topic
```

15 packaged topics (7 animation libraries plus cross-cutting references) ship
inside the wheel. Knowledge is never copied into your repository.

---

## Agent Support

One command installs the full loop into your coding agent:

```bash
aip init --agent all        # or one of: claude (default) · copilot · cursor · windsurf · cline · codex · gemini
```

| Agent | AIP writes | Route | Context | Check | Repair |
| --- | --- | :-: | :-: | :-: | :-: |
| Claude Code | `.claude/skills/animation/SKILL.md` | ✅ | ✅ | ✅ | ✅ |
| GitHub Copilot | `.github/instructions/animation.instructions.md` | ✅ | ✅ | ✅ | ✅ |
| Cursor | `.cursor/rules/animation.mdc` | ✅ | ✅ | ✅ | ✅ |
| Windsurf | `.windsurf/rules/animation.md` | ✅ | ✅ | ✅ | ✅ |
| Cline / Roo Code | `.clinerules/animation.md` | ✅ | ✅ | ✅ | ✅ |
| OpenAI Codex | managed block in `AGENTS.md` | ✅ | ✅ | ✅ | ✅ |
| Gemini CLI | managed block in `GEMINI.md` | ✅ | ✅ | ✅ | ✅ |

Each install is exactly one file — or a marker-delimited managed block; your
own content is never touched. `aip init --agent <x> --remove` takes it back
out. `--global` installs to your home directory.

### The self-healing loop

```text
developer request
      ↓
aip route        →  technology + context keys
      ↓
aip context      →  lifecycle + accessibility rules
      ↓
agent writes the code
      ↓
aip check        →  findings + fix hints
      ↓
agent repairs    (max 3 attempts)
      ↓
clean ✓          →  presented to you
```

Any agent without an integration gets the same loop through
`aip check --format json`: every finding carries `rule`, `message`, and
`fix_hint` — everything a model needs to repair its own output.

---

## CI Integration

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
- run: pipx install aip && aip check src/ --format github
```

Failing the build on `leak/*` and `a11y/*` is the point. Those are the classes
of bug that are effectively invisible in review.

Supported: CSS (`.css`, `.scss`, `.sass`, `.less`) and JS/TS (`.js`, `.jsx`,
`.ts`, `.tsx`, `.mjs`, `.cjs`); Python 3.10+, Node 16+ (npx shim); macOS,
Linux, Windows.

---

## Architecture

The self-healing loop above is the whole architecture: one router, one context
engine, one linter — no model calls anywhere.

<details>
<summary>Module map</summary>

```text
aip/check.py       the linter — rules, autofix, output formats
aip/knowledge.py   aip route and aip context
aip/claude.py      the canonical agent instruction body (single source of truth)
aip/adapters.py    aip init — per-agent delivery (file or managed-block modes)
aip/cli.py         command line entry point
aip/data/          knowledge pack — ships inside the wheel, never in your repo
npm/               npx shim (bootstraps Python, delegates to the CLI)
```

</details>

---

## Commands

| Command | What it does |
| --- | --- |
| `aip check <path>` | Lint a file or directory |
| `aip check <path> --fix` | Apply safe, mechanical fixes only |
| `aip check <path> --format json\|sarif\|github\|human` | Choose the output format |
| `aip route "<request>"` | Decide the technology from project evidence |
| `aip context <topic>` | Print packaged knowledge (omit topic to list) |
| `aip init [--agent <agent>] [--global]` | Install instructions for a coding agent |
| `aip init --agent <agent> --remove` | Remove them again |

---

## Design Principles

- **Zero config.** No `.aiprc`, no setup, no accounts. It runs on first use.
- **Zero dependencies.** Python stdlib only — the wheel is ~114 KB.
- **No AI, no network.** Deterministic and offline. Route and context never call a model.
- **Fix over complaint.** A finding that cannot state its fix in one sentence is not ready to ship.
- **False positives are worse than missed bugs.** A noisy linter gets disabled.

**What this is not:** not an AI code generator (your agent writes the code;
AIP routes, informs, and validates it) · not a runtime profiler (it reads
source, never executes your app) · not a replacement for testing on real
hardware (it catches known-bad patterns, not everything).

---

## Contributing

```bash
git clone https://github.com/Abdullahmalik66/Animation-Intelligence-Platform-AIP
cd Animation-Intelligence-Platform-AIP
python3 -m unittest discover tests -v   # test suite
python3 scripts/smoke.py                # cold-start sanity check
python3 -m aip check tests/fixtures/    # see the linter fire
```

Good first contributions: a new rule (with a positive and a negative fixture),
a sharper fix hint, a new context topic. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) and [`SECURITY.md`](SECURITY.md) for the
details.

## License

[MIT](LICENSE)
