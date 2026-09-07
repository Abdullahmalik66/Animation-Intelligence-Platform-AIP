# Contributing to aip

Thanks for helping make `aip` better.

## Ways to contribute

- **New lint rules** — catch a real animation bug class that `aip` misses today
- **Rule improvements** — fewer false positives, sharper fix hints
- **Bug fixes** — in the linter, the router, or the CLI
- **Context topics** — packaged knowledge served by `aip context`
- **Documentation** — clearer docs, better examples

## Getting started

```bash
git clone https://github.com/Abdullahmalik66/Animation-Intelligence-Platform-AIP
cd Animation-Intelligence-Platform-AIP
python3 -m unittest discover tests -v
python3 -m aip check tests/fixtures/bad-animations.css
```

Requires Python 3.10+. The project has zero runtime dependencies on purpose —
do not add any without discussing it first.

## Adding a lint rule

1. Implement it in `aip/check.py` and register it in `CSS_RULES` or `JS_RULES`.
2. Add a positive case to `tests/fixtures/bad-animations.*`.
3. Add a negative case to `tests/fixtures/good-animations.*`.
4. Add unit tests in `tests/test_check.py`.

False positives are worse than missed bugs — a noisy linter gets disabled. A
rule that cannot state its fix in one sentence is not ready.

## Adding a context topic

Add an entry to `TOPICS` in `aip/knowledge.py` pointing at a file under
`aip/data/` plus the `##` headings worth loading. Context is a budget, not a
dump — keep topics small and specific.

## Code style

- Python 3.10+ stdlib only; no third-party imports
- Full type hints where practical
- Comments explain *why*, not *what*
- No `console.log` / debug prints in shipped code

## Pull requests

- One rule or fix per PR.
- Include before/after output for new rules.
- All tests must pass: `python3 -m unittest discover tests -v`.

## Reporting issues

Open a GitHub issue with: the smallest code snippet that triggers the problem,
the expected result, and the actual output of `aip check --format json`.

## Code of conduct

Be respectful. Disagree constructively. Focus on the code, not the person.
