# AIP

A zero-config linter for web animation code — catches the memory leaks, accessibility violations, layout thrashing, and performance bugs that tests miss, and shows the fix.

```bash
npx aip-cli check src/
```

```
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

No AI. No network. No API keys. No config file. Zero dependencies.

---

## Why AIP Exists

Animation bugs are uniquely invisible. They don't throw. Tests pass. Types
check. The page just gets slower with every navigation — or it makes a user
with a vestibular disorder physically sick.

Existing tooling doesn't reach them:

- ESLint doesn't know a GSAP timeline needs `revert()`.
- Lighthouse tells you the page is slow, not which `@keyframes` did it.
- Type checkers can't see that your `IntersectionObserver` outlives the component.

AIP encodes the review checklist of an experienced animation engineer —
lifecycle cleanup, accessibility, performance, asset security — and runs it in
milliseconds, on every commit.

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

### Integrations

One command installs the routing, context, and check loop into your coding
agent:

```bash
aip init                          # Claude Code (default)
aip init --agent copilot          # GitHub Copilot
aip init --agent cursor           # Cursor
aip init --agent windsurf         # Windsurf
aip init --agent cline            # Cline / Roo Code
aip init --agent codex            # Codex & generic agents (AGENTS.md block)
aip init --agent gemini           # Gemini CLI (GEMINI.md block)
aip init --agent all              # everything above
```

| Agent | File written |
| --- | --- |
| Claude Code | `.claude/skills/animation/SKILL.md` |
| GitHub Copilot | `.github/instructions/animation.instructions.md` |
| Cursor | `.cursor/rules/animation.mdc` |
| Windsurf | `.windsurf/rules/animation.md` |
| Cline / Roo Code | `.clinerules/animation.md` |
| Codex & generic agents | managed block in `AGENTS.md` |
| Gemini CLI | managed block in `GEMINI.md` |

Each install writes exactly one file — or, for `AGENTS.md`/`GEMINI.md`, a
marker-delimited managed block. Your own content is never touched.
`aip init --agent <x> --remove` takes it back out. `--global` installs to your
home directory instead of the project.

---

## Example Agent Workflow

From then on, when you ask your agent for animation work, it:

1. runs `aip route "<request>"` to pick a technology based on what your project
   actually has installed,
2. runs `aip context <key>` to load only the lifecycle and accessibility rules
   for that library,
3. writes the code,
4. runs `aip check` and repairs its own findings (max 3 attempts) before
   showing you anything.

Any agent without a dedicated integration gets the same loop through
`aip check --format json`: each finding carries `rule`, `message`, and
`fix_hint`, which is everything a model needs to repair its own output.

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

---

## Supported Platforms

- **Agents:** Claude Code, GitHub Copilot, Cursor, Windsurf, Cline/Roo Code,
  OpenAI Codex, Gemini CLI — plus any agent via `aip check --format json`.
- **Languages scanned:** CSS (`.css`, `.scss`, `.sass`, `.less`) and
  JavaScript/TypeScript (`.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs`).
- **Runtimes:** Python 3.10+ (the tool); Node 16+ (the npx shim only).
- **OS:** macOS, Linux, Windows.

---

## Architecture

One routing engine, one context engine, one linter — no model calls anywhere.

```
            ┌─────────────────────────────────────────────┐
request ──► │ aip route     package.json + lockfile →     │
            │               technology + context keys     │
            │                                             │
            │ aip context   packaged knowledge, section-  │
            │               level, offline                │
            │                                             │
  code  ──► │ aip check     12 rules → findings + fixes   │
            └─────────────────────────────────────────────┘
```

```
aip/check.py       the linter — rules, autofix, output formats
aip/knowledge.py   aip route and aip context
aip/claude.py      the canonical agent instruction body (single source of truth)
aip/adapters.py    aip init — per-agent delivery (file or managed-block modes)
aip/cli.py         command line entry point
aip/data/          knowledge pack — ships inside the wheel, never in your repo
npm/               npx shim (bootstraps Python, delegates to the CLI)
```

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
- **No AI, no network.** Deterministic and offline. Route and context never
  call a model.
- **Fix over complaint.** A finding that cannot state its fix in one sentence
  is not ready to ship.
- **False positives are worse than missed bugs.** A noisy linter gets disabled.
- **Only mechanical autofixes.** `--fix` never rewrites anything requiring
  judgement.
- **Knowledge ships in the wheel.** `aip data/` is never copied into your
  repository.

### What this is not

- **Not an AI code generator.** AIP never calls a model. Your coding agent
  writes the code; AIP routes, informs, and validates it.
- **Not a runtime profiler.** It reads source code. It never executes your app,
  so it cannot measure actual frame rate.
- **Not a replacement for testing on real hardware.** It catches known-bad
  patterns, not everything.

---

## Contributing

```bash
git clone https://github.com/Abdullahmalik66/aip
cd aip
python3 -m unittest discover tests -v   # test suite
python3 scripts/smoke.py                # cold-start sanity check
python3 -m aip check tests/fixtures/    # see the linter fire
```

Good first contributions: a new rule (with a positive and a negative fixture),
a sharper fix hint, a new context topic. See
[`CONTRIBUTING.md`](CONTRIBUTING.md) and
[`SECURITY.md`](SECURITY.md) for the details.

## License

[MIT](LICENSE)
