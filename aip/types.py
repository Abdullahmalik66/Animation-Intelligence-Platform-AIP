"""Typed contracts for the deterministic router."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Confidence(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    UNKNOWN = "Unknown"


@dataclass
class IntentSignal:
    """One extracted feature — multi-signal extraction never collapses to a
    single label."""
    kind: str          # target | choreography | trigger | technology | negation | workflow
    value: str
    source_span: str = ""


@dataclass
class RoutingDecision:
    value_classification: str
    architecture: Optional[str]
    technology: Optional[str]
    workflow: str
    signals: list[IntentSignal] = field(default_factory=list)
    clarification_needed: Optional[str] = None   # one plain-language question
    rationale: str = ""
    evidence_used: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    confidence: Confidence = Confidence.MEDIUM
    decided_by: str = "deterministic"            # deterministic | llm-assisted


@dataclass
class NeedsClarification:
    """One question, no speculative code."""
    question: str
    why_it_matters: str
    options: list[str] = field(default_factory=list)
