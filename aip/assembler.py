"""Context assembler + budget manager (Phase 7) and optional compression
interface (Phase 9).

Selects the smallest safe context: shared governance rules (release-gating
rules are never dropped), technology modules per manifest load_when rules,
workflow modules, and examples only when policy allows. Emits an inspectable
context manifest. Token figures are ESTIMATES (chars/4) — marked as such.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .state import AnimationProjectState
from .paths import DATA

ROOT = DATA
DEFAULT_BUDGETS = {"targeted": 8000, "standard": 20000, "full": 60000}
RELEASE_GATING = {"GOV-VERSION", "GOV-OWNERSHIP", "GOV-A11Y", "GOV-SECURITY", "GOV-READINESS"}


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:16]


# --- Optional compression (Phase 9): provider-neutral, failure-safe ---------

class ContextCompressor:
    """Interface. Default is a pass-through; Headroom (or another provider)
    can be plugged in later. Compression must never drop release-gating
    content; on any failure the uncompressed context is used."""

    def compress(self, chunks: list[str], policy: Optional[dict] = None):
        return chunks, [], {"compressed": False, "provider": "none"}

    def retrieve(self, handle: str) -> str:
        raise KeyError(f"No stored content for handle {handle!r}")


# --- Governance parsing ------------------------------------------------------

def load_governance_rules() -> dict[str, str]:
    """Parse shared/governance.md into {rule_id: text}."""
    text = (ROOT / "shared" / "governance.md").read_text(encoding="utf-8")
    rules: dict[str, str] = {}
    current_id, buf = None, []
    for line in text.splitlines():
        m = re.match(r"^## (GOV-[A-Z0-9-]+)", line)
        if m:
            if current_id:
                rules[current_id] = "\n".join(buf).strip()
            current_id, buf = m.group(1), [line]
        elif current_id:
            buf.append(line)
    if current_id:
        rules[current_id] = "\n".join(buf).strip()
    return rules


def extract_sections(source_path: str, sections: list[str]) -> str:
    """Extract named ## sections from a canonical Markdown file. If a section
    is not found, a retrieval pointer is emitted instead of silently dropping."""
    path = ROOT / source_path
    if not path.is_file():
        return f"[MISSING SOURCE: {source_path}]"
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"(?m)^## ", text)
    out = []
    for wanted in sections:
        found = next((p for p in parts if p.lower().startswith(wanted.lower())), None)
        if found:
            out.append("## " + found.strip())
        else:
            out.append(f"[Retrieval pointer: section '{wanted}' in {source_path} — load on demand]")
    return "\n\n".join(out)


# --- Assembly ----------------------------------------------------------------

@dataclass
class AssembledContext:
    chunks: list[str] = field(default_factory=list)
    manifest: dict = field(default_factory=dict)

    @property
    def text(self) -> str:
        return "\n\n---\n\n".join(self.chunks)


def assemble_context(state: AnimationProjectState,
                     depth: str = "standard",
                     implementation_requested: Optional[bool] = None,
                     compressor: Optional[ContextCompressor] = None,
                     budgets: Optional[dict[str, int]] = None) -> AssembledContext:
    budgets = budgets or DEFAULT_BUDGETS
    budget = budgets.get(depth, budgets["standard"])
    workflow = state.selected_workflow or "implementation"
    tech = state.selected_technology
    if implementation_requested is None:
        implementation_requested = workflow == "implementation"

    workflows = json.loads((ROOT / "manifests" / "workflows.json").read_text())["workflows"]
    wf = workflows.get(workflow, workflows["implementation"])
    governance = load_governance_rules()

    included, excluded, chunks = [], [], []

    # 1. Shared governance for this workflow + technology (deduplicated set).
    needed_rules = set(wf["shared"])
    manifest_path = ROOT / "manifests" / f"{tech}.json"
    tech_manifest = json.loads(manifest_path.read_text()) if tech and manifest_path.is_file() else None
    if tech_manifest:
        needed_rules |= set(tech_manifest["required_shared_modules"])
    for rid in sorted(needed_rules):
        if rid in governance:
            chunks.append(governance[rid])
            included.append({"id": rid, "kind": "shared", "release_gating": rid in RELEASE_GATING})

    # 2. Technology modules matching load_when conditions.
    conditions = {workflow, f"framework:{state.framework}", f"intent:{_intent_tag(state)}"}
    if tech_manifest:
        for mod in tech_manifest["modules"]:
            if set(mod["load_when"]) & conditions:
                chunks.append(extract_sections(mod["source"], mod["sections"]))
                included.append({"id": mod["id"], "kind": "technology", "source": mod["source"]})
            else:
                excluded.append({"id": mod["id"], "reason": f"no load_when match ({sorted(mod['load_when'])})"})

    # 3. Workflow skill entrypoint pointer (canonical file stays retrievable, not inlined).
    if wf.get("skill"):
        chunks.append(f"[Workflow module: {wf['skill']} — retrieve sections on demand]")
        included.append({"id": workflow, "kind": "workflow", "source": wf["skill"]})

    # 4. Examples — only under policy.
    examples_meta = json.loads((ROOT / "manifests" / "examples.json").read_text())
    if implementation_requested and wf["examples_allowed"]:
        for ex in examples_meta["examples"]:
            if ex["technology"] == tech:
                p = ROOT / ex["path"]
                if p.is_file():
                    chunks.append(f"## Example: {ex['id']} ({ex['path']})\n```\n{p.read_text()}\n```")
                    included.append({"id": ex["id"], "kind": "example"})
                    state.selected_examples.append(ex["id"])
    else:
        excluded.append({"id": "examples/*", "reason": "workflow policy: examples not loaded"})

    uncompressed = sum(estimate_tokens(c) for c in chunks)

    # 5. Budget enforcement: trim non-gating chunks only; never drop release-gating rules.
    trimmed = []
    droppable = [i for i, meta in enumerate(included)
                 if meta["kind"] in ("example", "technology")]
    while droppable and sum(estimate_tokens(c) for c in chunks) > budget:
        idx = droppable.pop()  # drop last-added non-gating chunk first
        trimmed.append({**included[idx], "reason": "budget trim — retrieval pointer retained"})
        chunks[idx] = f"[Retrieval pointer: {included[idx]['id']} omitted for budget; retrieve on demand]"
        included[idx] = {**included[idx], "trimmed": True}
    # If only safety-critical content remains, the budget is exceeded deliberately.

    assembled = sum(estimate_tokens(c) for c in chunks)

    # 6. Optional compression — failure-safe.
    compressed_tokens = None
    if compressor:
        try:
            new_chunks, _handles, metrics = compressor.compress(chunks)
            if metrics.get("compressed"):
                chunks = new_chunks
                compressed_tokens = sum(estimate_tokens(c) for c in chunks)
        except Exception:  # noqa: BLE001 — compression must never fail the task
            pass

    manifest = {
        "request_id": state.request_id,
        "task": workflow,
        "selected_technology": tech,
        "selected_workflow": workflow,
        "included": included,
        "excluded": excluded + trimmed,
        "source_hashes": {m.get("source", m["id"]): _sha(c) for m, c in zip(included, chunks)},
        "uncompressed_token_estimate": uncompressed,
        "assembled_token_estimate": assembled,
        "compressed_token_estimate": compressed_tokens,
        "token_note": "chars/4 estimates — not exact model tokenisation",
        "budget": budget,
        "budget_exceeded": assembled > budget,
    }
    state.selected_modules = [m["id"] for m in included]
    state.context_manifest = manifest
    return AssembledContext(chunks=chunks, manifest=manifest)


def _intent_tag(state: AnimationProjectState) -> str:
    intent = state.normalised_intent or ""
    if "scroll" in intent:
        return "scroll"
    if "entrance" in intent:
        return "enter-exit"
    return intent
