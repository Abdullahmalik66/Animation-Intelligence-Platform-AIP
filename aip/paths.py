"""Canonical location of packaged knowledge.

Knowledge (skills, references, governance, manifests, schemas) ships *inside*
the wheel under `aip/data/`. It is never copied into a user's repository — it is
reached through `aip context`.
"""
from __future__ import annotations

from pathlib import Path

#: Root of the bundled knowledge pack.
DATA = Path(__file__).resolve().parent / "data"

#: Repository root. Only meaningful in a source checkout; used by dev tooling
#: (inventory, schema_check), never on a user's install path.
ROOT = Path(__file__).resolve().parent.parent
