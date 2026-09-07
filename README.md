# aip — the web animation linter

**It catches the animation bugs that don't throw, don't fail tests, and still
ship:** GSAP timelines that leak on every unmount, rAF loops that never stop,
animations that ignore `prefers-reduced-motion`, `@keyframes` that trigger
layout on every frame.

No AI. No network. No API keys. No config file.

```bash
npx aip check src/
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

Every finding comes with the fix on the `→` line, not just the complaint.

Exit code is `1` when there are errors, so it drops straight into CI.

---

## Quick start

Nothing to install if you have Node:

```bash
npx aip check src/
```

Or install it properly:

```bash
pipx install aip     # or: pip install aip
aip check src/
```

`npx aip` bootstraps a private Python environment under `~/.cache/aip` on first
run (~5s, once). It never writes into your project. Requires Python 3.10+. Zero
dependencies.

### Commands

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

---

## Why it exists

Animation bugs are uniquely invisible. They don't throw. Tests pass. Types
check. The page just gets slower every time a user navigates — or it makes
someone with a vestibular disorder physically sick.

Existing tooling doesn't reach them:

- ESLint doesn't know a GSAP timeline needs `revert()`.
- Lighthouse tells you the page is slow, not which `@keyframes` did it.
- Type checkers can't see that your `IntersectionObserver` outlives the component.

`aip` encodes the review checklist of an experienced animation engineer —
lifecycle cleanup, accessibility, performance, asset security — and runs it in
milliseconds, on every commit.

---

## Key features

12 rules in four families. Every finding names the rule and states the fix.

### Memory leaks — `leak/*` (errors)

| Rule | Catches |
| --- | --- |
| `leak/gsap-no-revert` | GSAP timeline/tween created in an effect with no `revert()` or `kill()` |
| `leak/raf-not-cancelled` | `requestAnimationFrame` loop with no `cancelAnimationFrame` |
| `leak/observer-not-disconnected` | `IntersectionObserver`/`ResizeObserver`/`MutationObserver` never disconnected |
| `leak/webgl-not-disposed` | Three.js geometries/materials/textures never `dispose()`d |
| `leak/listener-not-removed` | `addEventListener` in an effect with no matching removal |

Each one is a component that permanently retains memory after unmount, and
they compound across navigations in an SPA.

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

## CI

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
- run: pipx install aip && aip check src/ --format github
```

Failing the build on `leak/*` and `a11y/*` is the point. Those are the classes of
bug that are effectively invisible in review.

---

## For AI agents

### Claude Code

```bash
aip init
```

Writes one file — `.claude/skills/animation/SKILL.md` — and nothing else. From
then on, whenever you ask Claude for animation work, it:

1. runs `aip route "<your request>"` to pick a technology based on what your
   project actually has installed,
2. runs `aip context <key>` to load only the lifecycle and accessibility rules
   for that library,
3. writes the code,
4. runs `aip check` and repairs its own findings before showing you anything.

`aip init --remove` takes the file back out. Nothing else is left behind.

### The commands underneath

```bash
aip route "cards fade in as I scroll"     # → technology + context keys (JSON)
aip context gsap                          # → just the GSAP rules that matter
aip context                               # → list every topic
aip check <file> --format json            # → structured findings with fixes
```

`route` is deterministic and offline — it reads your `package.json` and lockfile,
not a model. When it cannot decide confidently it returns `"technology": null`
rather than guessing.

`context` reads knowledge bundled inside the installed package. Those files never
land in your repository.

### Any other agent

`aip check --format json` gives an agent a precise critique of code it just
wrote, with no model call:

1. Agent writes animation code.
2. Agent runs `aip check <file> --format json`.
3. Agent reads `rule`, `message`, and `fix_hint` and repairs its own output.

---

## What this is not

Scope, stated plainly:

- **Not an AI code generator.** A hidden, experimental `aip run` routes requests
  against a mock provider. It is not part of the product yet.
- **Not a runtime profiler.** It reads source code. It never executes your app,
  so it cannot measure actual frame rate.
- **Not a replacement for testing on real hardware.** It catches known-bad
  patterns, not everything.

The linter is the product. Everything else is in progress.

---

## Repository layout

```
aip/check.py       the linter — rules, autofix, output formats
aip/knowledge.py   `aip route` and `aip context`
aip/claude.py      `aip init` — the Claude Code skill
aip/cli.py         command line entry point
aip/data/          bundled knowledge (skills, references, manifests) — ships
                   inside the wheel, never copied into your project
npm/               npx shim (bootstraps Python, delegates to the CLI)
tests/             linter tests + good/bad fixtures
scripts/smoke.py   cold-start sanity check
```

## Development

```bash
python -m unittest discover tests -v   # test suite (no dependencies)
python scripts/smoke.py                # cold-start sanity check
python -m aip check tests/fixtures/    # see the linter fire
```

### Releasing

```bash
python -m build                        # wheel + sdist into dist/
twine upload dist/*                    # PyPI
cd npm && npm publish                  # npx shim (version must match)
```

The npm shim pins `aip==<its own version>`, so publish PyPI first.

Adding a rule: write it in `aip/check.py`, register it in `CSS_RULES` or
`JS_RULES`, then add a positive case to `tests/fixtures/bad-animations.*` **and**
a negative case to `tests/fixtures/good-animations.*`. False positives are worse
than missed bugs — a noisy linter gets disabled.

Adding a context topic: add an entry to `TOPICS` in `aip/knowledge.py` pointing
at a file under `aip/data/` and the `##` headings worth loading. Keep it small —
context is a budget, not a dump.

See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

See [`LICENSE`](LICENSE).
