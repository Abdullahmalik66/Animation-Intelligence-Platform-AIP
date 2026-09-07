"""`aip route` and `aip context` — the two commands an agent calls.

Both are deterministic, offline, and dependency-free.

  route    request text  -> which technology, and which context keys to load
  context  topic key     -> the packaged knowledge for that key, and nothing else

Knowledge lives in `aip/data/` inside the installed package. It is never copied
into the user's repository.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .paths import DATA

# --------------------------------------------------------------------------
# Context topics. A topic is a stable, memorable name -> (file, headings).
# Headings are matched case-insensitively against `## ` sections.
# `None` means "the whole file" (used for short reference docs).
# --------------------------------------------------------------------------
TOPICS: dict[str, tuple[str, list[str] | None]] = {
    # Cross-cutting references — always small, always whole.
    "accessibility": ("references/accessibility.md", None),
    "performance": ("references/performance.md", None),
    "security": ("references/security.md", None),
    "browser-support": ("references/browser-support.md", None),
    "decision-matrix": ("references/library-decision-matrix.md", None),
    # Library knowledge — sectioned, because these files are large.
    "gsap": ("skills/gsap/SKILL.md", [
        "Version and Package Gate", "Implementation Strategy",
        "Accessibility Strategy", "Lifecycle and Cleanup Strategy",
        "Performance Considerations"]),
    "scrolltrigger": ("skills/gsap/SKILL.md", [
        "Router Integration", "Lifecycle and Cleanup Strategy",
        "Performance Considerations"]),
    "motion-react": ("skills/motion-react/SKILL.md", [
        "Version and Package Gate", "Implementation Strategy",
        "Accessibility Strategy", "Lifecycle and Cleanup Strategy"]),
    "motion": ("skills/motion/SKILL.md", [
        "Version and Package Gate", "Implementation Strategy",
        "Accessibility Strategy", "Lifecycle and Cleanup Strategy"]),
    "threejs": ("skills/threejs/SKILL.md", [
        "Version and Package Gate", "Implementation Strategy",
        "Lifecycle and Cleanup Strategy", "Performance Considerations"]),
    "lottie": ("skills/lottie/SKILL.md", [
        "Version and Package Gate", "Implementation Strategy",
        "Accessibility Strategy", "Lifecycle and Cleanup Strategy"]),
    "rive": ("skills/rive/SKILL.md", [
        "Version and Package Gate", "Implementation Strategy",
        "Lifecycle and Cleanup Strategy"]),
    "animejs": ("skills/animejs/SKILL.md", [
        "Version and Package Gate", "Implementation Strategy",
        "Accessibility Strategy", "Lifecycle and Cleanup Strategy"]),
    "css": ("references/performance.md", None),
    "waapi": ("references/browser-support.md", None),
}

# Technology -> the context topics worth loading for it.
_TECH_CONTEXT: dict[str, list[str]] = {
    "gsap": ["gsap", "accessibility", "performance"],
    "motion-react": ["motion-react", "accessibility", "performance"],
    "motion": ["motion", "accessibility", "performance"],
    "threejs": ["threejs", "performance"],
    "lottie": ["lottie", "accessibility", "security"],
    "rive": ["rive", "accessibility", "security"],
    "animejs": ["animejs", "accessibility", "performance"],
    "css": ["css", "accessibility"],
    "waapi": ["waapi", "accessibility", "performance"],
}


def _read(rel: str) -> str:
    path = DATA / rel
    if not path.is_file():
        raise FileNotFoundError(f"packaged knowledge missing: {rel}")
    return path.read_text(encoding="utf-8")


def _sections(text: str, headings: list[str]) -> str:
    """Extract `## ` sections whose title starts with any requested heading."""
    wanted = [h.lower() for h in headings]
    parts = re.split(r"(?m)^## ", text)
    out = []
    for part in parts[1:]:
        title = part.split("\n", 1)[0].strip().lower()
        if any(title.startswith(w) for w in wanted):
            out.append("## " + part.rstrip())
    return "\n\n".join(out)


def get_context(topic: str) -> str:
    """Return packaged knowledge for `topic`. Raises KeyError if unknown."""
    key = topic.strip().lower()
    if key not in TOPICS:
        raise KeyError(key)
    rel, headings = TOPICS[key]
    text = _read(rel)
    return text if headings is None else _sections(text, headings)


def list_topics() -> list[str]:
    return sorted(TOPICS)


# --------------------------------------------------------------------------
# Routing
# --------------------------------------------------------------------------
def route_request(request: str, project_dir: str | None = None) -> dict:
    """Deterministic technology decision + the context keys to load.

    Reuses the existing hybrid router and project inspector. No model call.
    """
    from .state import AnimationProjectState
    from .hybrid_router import route as _route
    from .inspector import inspect_project

    state = AnimationProjectState(raw_user_request=request, user_mode="expert")
    if project_dir:
        try:
            inspect_project(project_dir, state)
        except (OSError, ValueError):
            pass  # An unreadable project is not a routing failure.

    decision = _route(state)
    tech = decision.technology

    installed = sorted(set(state.installed_packages) & set(_TECH_CONTEXT))

    if tech is None:
        # The router refused to guess. Say so, and load context for whatever
        # animation libraries the project actually has.
        ctx = []
        for t in installed:
            ctx += _TECH_CONTEXT.get(t, [])
        ctx = ctx or ["decision-matrix", "accessibility", "performance"]
        complexity = "unknown"
    else:
        ctx = _TECH_CONTEXT.get(tech, ["accessibility", "performance"])
        # ScrollTrigger has its own cleanup contract, so scroll work needs it.
        scrolly = (any(s.value == "scroll" for s in decision.signals)
                   or re.search(r"scroll|pin\b|scrub|parallax|sticky",
                                request, re.I))
        if tech == "gsap" and scrolly:
            ctx = ["scrolltrigger"] + ctx
        complexity = ("low" if tech in ("css", "waapi", "no-animation")
                      else "high" if tech in ("threejs", "rive") else "medium")

    signals = sorted({s.value for s in decision.signals})

    return {
        "technology": tech,
        "architecture": decision.architecture,
        "workflow": decision.workflow,
        "complexity": complexity,
        "confidence": decision.confidence.value
        if hasattr(decision.confidence, "value") else str(decision.confidence),
        "decided_by": decision.decided_by,
        "required_context": list(dict.fromkeys(ctx)),
        "signals": signals,
        "rationale": decision.rationale,
        "installed": sorted(state.installed_packages),
    }
