# AGENTS.md

Instructions for AI coding agents working **on this repository** (the `aip`
tool itself). For instructions AIP installs into *user* projects, see
`aip/claude.py` — that is the single source of truth, rendered per agent by
`aip/adapters.py`.

## What this repository is

`aip` is a zero-config linter for web animation code (PyPI: `aip`, npm shim:
`aip-cli`). Python 3.10+, stdlib only, zero runtime dependencies. No AI, no
network calls, anywhere.

## Commands

```bash
python3 -m unittest discover tests -v   # full test suite
python3 scripts/smoke.py                # cold-start sanity checks
python3 -m aip check tests/fixtures/bad-animations.jsx   # see the linter fire
```

## Rules of this codebase

1. Zero dependencies. No third-party imports in `aip/` — stdlib only.
2. Add a rule only when it catches a real, recurring bug class. Every rule
   states its fix in one sentence.
3. A new rule requires a positive case in `tests/fixtures/bad-animations.*`,
   a negative case in `tests/fixtures/good-animations.*`, and unit tests in
   `tests/test_check.py`.
4. False positives are worse than missed bugs — a noisy linter gets disabled.
5. Comments explain *why*, not *what*. No debug prints in shipped code.
6. `aip route` and `aip context` are deterministic and offline. Never add a
   network or model call.
7. Knowledge topics are declared in `TOPICS` (`aip/knowledge.py`) and point at
   files under `aip/data/`. Keep topics small — context is a budget, not a
   dump. CI verifies every topic resolves.
8. `npm/package.json` version must always match `aip/__init__.py`; the shim
   pins `aip==<its own version>`.

## Layout

```
aip/check.py       the linter — rules, autofix, output formats
aip/knowledge.py   aip route and aip context
aip/claude.py      the canonical agent instruction body
aip/adapters.py    aip init — per-agent delivery (file / managed-block modes)
aip/cli.py         argparse entry point
aip/data/          knowledge pack shipped inside the wheel
npm/               npx shim (bootstraps Python, delegates to the CLI)
tests/             unit tests + good/bad fixtures
scripts/smoke.py   cold-start sanity checks
```

`archive/` is a local-only internal archive (gitignored, never published).
