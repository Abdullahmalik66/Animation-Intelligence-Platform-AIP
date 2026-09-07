"""Local deterministic retrieval store (Workstreams 5 + 12).

Executable retrieval pointers over approved repository content only:
- path allowlist, traversal rejection
- provenance + trust + hash on every chunk
- budget enforcement, deduplication, stale-hash surfacing
- audit log of every retrieval with reason
"""
from __future__ import annotations

import hashlib
import re
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .paths import DATA

ROOT = DATA
ALLOWED_ROOTS = ("skills/", "references/", "shared/", "examples/", "integrations/")


class RetrievalError(ValueError):
    pass


@dataclass
class RetrievedChunk:
    retrieval_key: str
    source: str
    heading: str
    text: str
    source_hash: str
    trust: str = "repository"
    estimated_tokens: int = 0


@dataclass
class RetrievalStore:
    max_tokens_per_request: int = 4000
    max_total_tokens: int = 20000
    _served: set[str] = field(default_factory=set)
    _total: int = 0
    _log: list[dict] = field(default_factory=list)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    @staticmethod
    def make_key(source: str, heading: str) -> str:
        return f"{source}#{heading}"

    @staticmethod
    def file_hash(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]

    def _resolve_path(self, source: str) -> Path:
        if source.startswith("/") or ".." in Path(source).parts:
            raise RetrievalError(f"Forbidden path: {source!r}")
        if not source.startswith(ALLOWED_ROOTS):
            raise RetrievalError(f"Path outside allowlist: {source!r}")
        path = (ROOT / source).resolve()
        if not str(path).startswith(str(ROOT.resolve())):
            raise RetrievalError(f"Path traversal rejected: {source!r}")
        if not path.is_file():
            raise RetrievalError(f"No such source: {source!r}")
        return path

    def retrieve(self, retrieval_key: str, reason: str,
                 maximum_tokens: Optional[int] = None,
                 expected_hash: Optional[str] = None) -> RetrievedChunk:
        """Retrieve one section by key `source#heading`. Thread-safe."""
        with self._lock:
            if "#" not in retrieval_key:
                raise RetrievalError(f"Invalid retrieval key: {retrieval_key!r} (want source#heading)")
            source, heading = retrieval_key.split("#", 1)
            path = self._resolve_path(source)

            actual_hash = self.file_hash(path)
            stale = expected_hash is not None and expected_hash != actual_hash

            if retrieval_key in self._served:
                raise RetrievalError(f"Duplicate retrieval rejected: {retrieval_key!r}")

            text = path.read_text(encoding="utf-8")
            parts = re.split(r"(?m)^## ", text)
            match = next((p for p in parts if p.lower().startswith(heading.lower())), None)
            if match is None:
                raise RetrievalError(f"Heading {heading!r} not found in {source}")
            chunk_text = "## " + match.strip()

            est = max(1, len(chunk_text) // 4)
            cap = min(maximum_tokens or self.max_tokens_per_request,
                      self.max_tokens_per_request)
            if est > cap:
                chunk_text = chunk_text[: cap * 4] + "\n[truncated to retrieval budget]"
                est = cap
            if self._total + est > self.max_total_tokens:
                raise RetrievalError(
                    f"Retrieval budget exceeded ({self._total}+{est} > {self.max_total_tokens})")

            self._served.add(retrieval_key)
            self._total += est
            self._log.append({"key": retrieval_key, "reason": reason,
                              "tokens_est": est, "stale_hash": stale})
            return RetrievedChunk(retrieval_key=retrieval_key, source=source,
                                  heading=heading, text=chunk_text,
                                  source_hash=actual_hash,
                                  estimated_tokens=est)

    @property
    def audit_log(self) -> list[dict]:
        return list(self._log)
