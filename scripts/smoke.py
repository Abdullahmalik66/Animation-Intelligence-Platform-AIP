"""Smoke test: prove a cold checkout actually works.

Run: python3 scripts/smoke.py
Exits non-zero if anything is broken.
"""
from __future__ import annotations

import io
import contextlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

FIX = ROOT / "tests" / "fixtures"
results: list[tuple[bool, str]] = []


def check(label: str, ok: bool, detail: str = "") -> None:
    results.append((ok, f"{label}{(' — ' + detail) if detail else ''}"))


# 1. Linter finds problems in bad code
from aip.check import check_path, format_report  # noqa: E402

bad = check_path(FIX / "bad-animations.jsx")
check("linter finds leaks in bad JSX", bad.error_count >= 4,
      f"{bad.error_count} errors")

badcss = check_path(FIX / "bad-animations.css")
check("linter finds problems in bad CSS", len(badcss.findings) >= 4,
      f"{len(badcss.findings)} findings")

# 2. No false positives on good code
for name in ("good-animations.css", "good-animations.jsx"):
    rep = check_path(FIX / name)
    check(f"no false positives in {name}", not rep.findings,
          str([f.rule for f in rep.findings]))

# 3. All output formats render
for fmt in ("human", "json", "sarif", "github"):
    try:
        out = format_report(bad, fmt, color=False) if fmt == "human" \
            else format_report(bad, fmt)
        check(f"format {fmt}", bool(out))
    except Exception as exc:
        check(f"format {fmt}", False, repr(exc))

# 4. CLI wiring + exit codes
cli = subprocess.run(
    [sys.executable, "-m", "aip", "check", str(FIX / "bad-animations.jsx")],
    capture_output=True, text=True, cwd=ROOT)
check("CLI exits 1 on errors", cli.returncode == 1, f"got {cli.returncode}")
check("CLI prints findings", "leak/" in cli.stdout, cli.stdout[:80])

cli_ok = subprocess.run(
    [sys.executable, "-m", "aip", "check", str(FIX / "good-animations.jsx")],
    capture_output=True, text=True, cwd=ROOT)
check("CLI exits 0 on clean code", cli_ok.returncode == 0,
      f"got {cli_ok.returncode}")

# 5. Deleted modules stay deleted
for gone in ("aip/backends", "aip/pipeline.py", "aip/router.py",
             "aip/gateway.py", "aip/orchestrator.py", "aip/assembler.py",
             "aip/retrieval.py", "aip/validators.py", "aip/schema_check.py",
             "aip/inventory.py", "platform"):
    check(f"{gone} removed", not (ROOT / gone).exists())

# 6. Test suite is green
suite = subprocess.run(
    [sys.executable, "-m", "unittest", "discover", "tests", "-v"],
    capture_output=True, text=True, cwd=ROOT)
tail = (suite.stderr or suite.stdout).strip().splitlines()
check("unittest suite passes", suite.returncode == 0,
      tail[-1] if tail else "no output")

# ---- report
passed = sum(1 for ok, _ in results if ok)
print()
for ok, label in results:
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
print(f"\n{passed}/{len(results)} checks passed")
sys.exit(0 if passed == len(results) else 1)
