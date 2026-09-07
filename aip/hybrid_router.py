"""Hybrid two-stage router (Workstream 6).

Deterministic multi-signal extraction (never stops at first match), explicit
technology/negation/maintenance detection, high-confidence deterministic
decisions, and a structured escalation path: uncertain cases return either a
clarification (guided) or an LLM-assisted routing request — never a guess.
The canonical skills/animation-router/SKILL.md remains the semantic authority
for the LLM-assisted path.
"""
from __future__ import annotations

import re
from typing import Optional

from .state import AnimationProjectState
from .inspector import installed_animation_technologies
from .types import Confidence, IntentSignal, RoutingDecision, NeedsClarification

SIGNAL_PATTERNS: list[tuple[str, str, str]] = [
    # (kind, value, regex)
    ("negation", "no-animation", r"\b(don'?t|do not|stop|remove|without) (the )?animat"),
    ("choreography", "staggered", r"one (at a time|by one)|stagger"),
    ("trigger", "scroll", r"\bscroll(s|ing|ed)?\b"),
    ("trigger", "hover", r"\bhover|mouse over\b"),
    ("trigger", "load", r"\bwhile.*load|loading\b"),
    ("choreography", "entrance", r"\b(appear|fade in|show up|entrance|enter|reveal)\b"),
    ("choreography", "exit", r"\b(disappear|fade out|removed|exit)\b"),
    ("choreography", "loop", r"\b(spin|rotat|loop)\w*\b"),
    ("target", "3d", r"\b3.?d\b|product viewer|webgl"),
    ("target", "designer-asset", r"after effects|lottie file|\.json animation|\.riv|designer (made|export)"),
    ("target", "interactive-asset", r"interactive character|reacts to (cursor|mouse|click)"),
    ("technology", "gsap", r"\bgsap|scrolltrigger\b"),
    ("technology", "motion-react", r"\bframer.?motion|motion for react|animatepresence\b"),
    ("technology", "motion", r"\bmotion (library|one|vanilla)|vanilla motion\b"),
    ("technology", "animejs", r"\banime\.?js\b"),
    ("technology", "lottie", r"\blottie\b"),
    ("technology", "rive", r"\brive\b|\.riv\b"),
    ("technology", "threejs", r"\bthree\.?js\b"),
    ("technology", "waapi", r"\bwaapi|web animations api|without a library|no.?dependency\b"),
    ("technology", "css", r"\b(just|plain|pure) css\b"),
    ("workflow", "maintenance", r"\b(my|our|existing|current) .{0,30}(animation|code)\b"),
]

WORKFLOW_PATTERNS: list[tuple[str, str]] = [
    (r"\b(fix|broken|not working|debug|why (does|is))\b", "debugging"),
    (r"\b(review|audit|check (my|this))\b", "code-review"),
    (r"\b(accessib|reduced motion|screen reader|a11y)\b", "accessibility-review"),
    (r"\b(slow|jank|performance|fps|dropped frames)\b", "performance-review"),
    (r"\b(migrate|convert|switch (from|to)|replace .* with)\b", "migration"),
    (r"\b(secure|security|csp|trusted|provenance)\b", "security-review"),
    (r"\b(production.?ready|ready to ship|launch)\b", "production-readiness"),
]


def extract_signals(text: str) -> list[IntentSignal]:
    """Collect ALL matching signals — multi-intent preserved."""
    low = text.lower()
    out = []
    for kind, value, pattern in SIGNAL_PATTERNS:
        m = re.search(pattern, low)
        if m:
            out.append(IntentSignal(kind=kind, value=value, source_span=m.group(0)))
    return out


def route(state: AnimationProjectState,
          clarification_answer: Optional[str] = None) -> RoutingDecision:
    signals = extract_signals(state.raw_user_request)
    installed = installed_animation_technologies(state)
    sig = {(s.kind, s.value) for s in signals}
    values = lambda k: [s.value for s in signals if s.kind == k]  # noqa: E731

    workflow = _workflow(state.raw_user_request)

    # Negation → deliberate no-animation outcome.
    if ("negation", "no-animation") in sig:
        return _decision(state, signals, "no-animation", None, "no-animation",
                         workflow, "User asked not to animate", Confidence.HIGH)

    # Explicit technology request wins Stage 1 (suitability check stays with LLM/GOV-ROUTING).
    explicit = values("technology")
    if explicit:
        tech = explicit[0]
        conf = Confidence.HIGH if tech in installed or tech in ("css", "waapi") else Confidence.MEDIUM
        return _decision(state, signals, "functional", "explicit-request", tech,
                         workflow, f"Explicit request for {tech}", conf,
                         assumptions=[] if conf is Confidence.HIGH
                         else [f"{tech} not verified as installed"])

    # Multi-intent: staggered + scroll → materially ambiguous (scroll-linked vs viewport-entry).
    if "staggered" in values("choreography") and "scroll" in values("trigger"):
        if clarification_answer:
            if "linked" in clarification_answer.lower() or "scrub" in clarification_answer.lower():
                tech = _pick(installed, ["gsap"], "css")
                return _decision(state, signals, "functional", "scroll-linked", tech,
                                 workflow, "Clarified: scroll-linked/scrubbed", Confidence.HIGH)
            tech = _pick(installed, ["motion-react", "gsap"], "css") \
                if state.framework in ("react", "nextjs") else "css"
            return _decision(state, signals, "functional", "viewport-triggered", tech,
                             workflow, "Clarified: trigger once on viewport entry", Confidence.HIGH)
        d = _decision(state, signals, "functional", "needs-disambiguation", None,
                      workflow, "Staggered + scroll: continuous scroll-linked vs "
                      "viewport-entry materially changes the implementation",
                      Confidence.MEDIUM)
        d.clarification_needed = ("Should the cards move continuously as you scroll "
                                  "(tied to scroll position), or simply appear once "
                                  "when they come into view?")
        return d

    # Single-signal deterministic routes.
    if ("target", "interactive-asset") in sig:
        return _decision(state, signals, "functional", "designer-runtime", "rive",
                         workflow, "Stateful designer asset", Confidence.HIGH)
    if ("target", "designer-asset") in sig:
        return _decision(state, signals, "functional", "designer-runtime",
                         _pick(installed, ["lottie", "rive"], "lottie"),
                         workflow, "Linear designer asset", Confidence.MEDIUM)
    if ("target", "3d") in sig:
        return _decision(state, signals, "functional", "webgl", "threejs",
                         workflow, "3D scene", Confidence.HIGH)
    if ("trigger", "hover") in sig:
        return _decision(state, signals, "functional", "native-css", "css",
                         workflow, "Micro-interaction — CSS sufficient", Confidence.HIGH)
    if ("choreography", "loop") in sig:
        return _decision(state, signals, "decorative", "value-challenge", "css",
                         workflow, "Decorative loop — value must be challenged (GOV-ROUTING)",
                         Confidence.MEDIUM)
    if ("trigger", "load") in sig:
        return _decision(state, signals, "communicative", "status-semantics-first",
                         _pick(installed, ["lottie", "rive"], "css"),
                         workflow, "Status indicator — semantics first", Confidence.MEDIUM)
    if "staggered" in values("choreography"):
        tech = _pick(installed, ["motion-react", "gsap"], "css") \
            if state.framework in ("react", "nextjs") else _pick(installed, ["gsap", "animejs"], "css")
        return _decision(state, signals, "functional", "library" if tech != "css" else "native-css",
                         tech, workflow, "Staggered entrance", Confidence.MEDIUM)
    if "exit" in values("choreography") and state.framework in ("react", "nextjs"):
        return _decision(state, signals, "functional", "library",
                         _pick(installed, ["motion-react"], "css"),
                         workflow, "Enter/exit presence in React", Confidence.MEDIUM)
    if "entrance" in values("choreography") and "scroll" in values("trigger"):
        tech = _pick(installed, ["motion-react"], "") \
            if state.framework in ("react", "nextjs") else ""
        tech = tech or _pick(installed, ["gsap", "animejs"], "css")
        return _decision(state, signals, "functional",
                         "viewport-triggered" if tech != "css" else "native-css",
                         tech, workflow, "Scroll-triggered reveal on viewport entry",
                         Confidence.MEDIUM)
    if "entrance" in values("choreography"):
        return _decision(state, signals, "functional", "native-css", "css",
                         workflow, "Simple entrance — CSS first", Confidence.MEDIUM)

    # Maintenance of existing code with a review-ish workflow: tech from installed set.
    if workflow != "implementation" and len(installed) == 1:
        return _decision(state, signals, "functional", "existing", installed[0],
                         workflow, "Single installed animation library", Confidence.MEDIUM)

    # Uncertain → escalate (LLM-assisted path), never guess.
    d = _decision(state, signals, "unknown", "unrouted", None, workflow,
                  "No high-confidence deterministic route — requires LLM-assisted "
                  "routing with canonical router governance", Confidence.UNKNOWN)
    d.decided_by = "llm-assisted-required"
    state.unknowns.append("Routing requires LLM-assisted interpretation")
    return d


def _workflow(text: str) -> str:
    low = text.lower()
    for pattern, wf in WORKFLOW_PATTERNS:
        if re.search(pattern, low):
            return wf
    return "implementation"


def _pick(installed: list[str], preferred: list[str], fallback: str) -> str:
    for t in preferred:
        if t in installed:
            return t
    return fallback


def _decision(state, signals, value_cls, arch, tech, workflow, rationale,
              confidence, assumptions=None) -> RoutingDecision:
    d = RoutingDecision(value_classification=value_cls, architecture=arch,
                        technology=tech, workflow=workflow, signals=signals,
                        rationale=rationale, confidence=confidence,
                        assumptions=assumptions or [],
                        evidence_used=[e.claim for e in state.evidence])
    state.selected_technology = tech or "insufficient-evidence"
    state.selected_architecture = arch
    state.selected_workflow = workflow
    state.animation_value_classification = value_cls
    state.normalised_intent = ", ".join(f"{s.kind}:{s.value}" for s in signals) or "unclassified"
    return d


def clarification_from(decision: RoutingDecision) -> Optional[NeedsClarification]:
    if decision.clarification_needed:
        return NeedsClarification(
            question=decision.clarification_needed,
            why_it_matters="The answer changes which approach is correct and how it behaves.",
            options=["Appear once when they come into view",
                     "Move continuously tied to scroll position"])
    return None
