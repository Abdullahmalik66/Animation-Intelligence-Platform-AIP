"""Deterministic schema/config validation (Workstream 3 + 4).

Stdlib-only structural validator (jsonschema not installed — direction of
authority: Python models own the contracts; these checks enforce the invariants
that matter operationally). Malformed manifests fail loudly with actionable
errors. Also provides the section-fidelity audit used by tests and CLI.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .paths import DATA

ROOT = DATA

MANIFEST_REQUIRED = ["id", "purpose", "triggers", "exclusions",
                     "required_shared_modules", "canonical_skill", "workflows"]
MODULE_REQUIRED = ["id", "source", "sections", "load_when", "required"]
VALID_GOV = {"GOV-VERSION", "GOV-EVIDENCE", "GOV-DEPTH", "GOV-REVIEW-FIRST",
             "GOV-OWNERSHIP", "GOV-A11Y", "GOV-SECURITY", "GOV-PERF",
             "GOV-READINESS", "GOV-CONFIDENCE", "GOV-ROUTING"}


class ConfigError(ValueError):
    """Raised for invalid manifests/config with an actionable message."""


def headings(path: Path) -> list[str]:
    return [h.strip() for h in re.findall(r"(?m)^## (.+)$", path.read_text(encoding="utf-8"))]


def validate_manifest(path: Path) -> list[str]:
    """Return list of errors (empty = valid)."""
    errors: list[str] = []
    try:
        d = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path.name}: invalid JSON — {exc}"]
    for key in MANIFEST_REQUIRED:
        if key not in d:
            errors.append(f"{path.name}: missing required field '{key}'")
    for rid in d.get("required_shared_modules", []):
        if rid not in VALID_GOV:
            errors.append(f"{path.name}: unknown governance rule '{rid}'")
    cs = d.get("canonical_skill")
    if cs and not (ROOT / cs).is_file():
        errors.append(f"{path.name}: canonical_skill '{cs}' does not exist")
    for mod in d.get("modules", []):
        for key in MODULE_REQUIRED:
            if key not in mod:
                errors.append(f"{path.name}: module '{mod.get('id','?')}' missing '{key}'")
        src = ROOT / mod.get("source", "")
        if not src.is_file():
            errors.append(f"{path.name}: module '{mod.get('id')}' source missing: {mod.get('source')}")
    return errors


def audit_sections() -> list[dict]:
    """Section-fidelity audit: every manifest section ref vs real headings."""
    rows = []
    for mf in sorted((ROOT / "manifests").glob("*.json")):
        d = json.loads(mf.read_text(encoding="utf-8"))
        if "canonical_skill" not in d:
            continue
        for mod in d.get("modules", []):
            src = ROOT / mod["source"]
            heads = headings(src) if src.is_file() else []
            for section in mod["sections"]:
                matches = [h for h in heads if h.lower().startswith(section.lower())]
                status = ("exact" if any(h.lower() == section.lower() for h in matches)
                          else "prefix" if len(matches) == 1
                          else "ambiguous" if len(matches) > 1 else "missing")
                rows.append({
                    "manifest": mf.name, "module": mod["id"], "source": mod["source"],
                    "section": section, "match_type": status,
                    "matched_heading": matches[0] if len(matches) == 1 else None,
                    "required": mod.get("required", False),
                    "content_hash": hashlib.sha256(
                        src.read_bytes()).hexdigest()[:16] if src.is_file() else None,
                })
    return rows


def validate_all() -> None:
    """Fail loudly (ConfigError) if any manifest is invalid or a REQUIRED
    module section is missing/ambiguous."""
    errors: list[str] = []
    for mf in sorted((ROOT / "manifests").glob("*.json")):
        d = json.loads(mf.read_text(encoding="utf-8"))
        if "canonical_skill" in d:
            errors += validate_manifest(mf)
    for row in audit_sections():
        if row["required"] and row["match_type"] in ("missing", "ambiguous"):
            errors.append(
                f"{row['manifest']} module '{row['module']}': REQUIRED section "
                f"'{row['section']}' is {row['match_type']} in {row['source']} — "
                f"fix the manifest section name or the source heading")
    if errors:
        raise ConfigError("Configuration invalid:\n" + "\n".join(f"  - {e}" for e in errors))


if __name__ == "__main__":
    import sys
    try:
        validate_all()
        rows = audit_sections()
        missing = [r for r in rows if r["match_type"] == "missing"]
        print(f"Manifests valid. Section refs: {len(rows)}, missing(optional): {len(missing)}")
        for r in missing:
            print(f"  optional-miss: {r['module']} -> '{r['section']}'")
    except ConfigError as exc:
        print(exc)
        sys.exit(1)
