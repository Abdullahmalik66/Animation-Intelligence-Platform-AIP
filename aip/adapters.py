"""Agent adapters — deliver the one canonical instruction body to any agent.

One source of truth: `aip.claude.BODY` (rendered per-machine by
`render_body`). Each adapter only decides WHERE the instructions live and
WHAT wrapper (frontmatter / managed block) the platform expects.

Two delivery modes:

  file   — AIP owns a dedicated file (Claude, Copilot, Cursor, Windsurf, Cline).
           Written whole; never merged with user content.
  block  — the platform reads a shared file the user may also own
           (AGENTS.md, GEMINI.md). AIP manages only a marker-delimited block
           and never touches anything outside it.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .claude import DESCRIPTION, render_body, render_skill

BEGIN = "<!-- aip:begin (managed by `aip init` — do not edit inside) -->"
END = "<!-- aip:end -->"


@dataclass(frozen=True)
class Adapter:
    id: str
    label: str
    rel_path: str            # relative to project root (or $HOME for global)
    mode: str                # "file" | "block"
    frontmatter: str = ""    # prepended in file mode

    def render(self, command: str) -> str:
        if self.id == "claude":
            return render_skill(command)  # keeps Claude's exact historical format
        return self.frontmatter + render_body(command)


ADAPTERS: dict[str, Adapter] = {a.id: a for a in [
    Adapter("claude", "Claude Code", ".claude/skills/animation/SKILL.md", "file"),
    Adapter("copilot", "GitHub Copilot",
            ".github/instructions/animation.instructions.md", "file",
            frontmatter=("---\n"
                         "applyTo: \"**/*.{css,scss,sass,less,js,jsx,ts,tsx,mjs,cjs,html,vue,svelte}\"\n"
                         "---\n\n")),
    Adapter("cursor", "Cursor", ".cursor/rules/animation.mdc", "file",
            frontmatter=(f"---\ndescription: {DESCRIPTION}\n"
                         "globs:\nalwaysApply: false\n---\n\n")),
    Adapter("windsurf", "Windsurf", ".windsurf/rules/animation.md", "file",
            frontmatter=("---\ntrigger: glob\n"
                         "globs: \"**/*.{css,scss,js,jsx,ts,tsx,vue,svelte}\"\n"
                         "---\n\n")),
    Adapter("cline", "Cline / Roo Code", ".clinerules/animation.md", "file"),
    Adapter("codex", "OpenAI Codex & generic agents", "AGENTS.md", "block"),
    Adapter("gemini", "Gemini CLI / Code Assist", "GEMINI.md", "block"),
]}

AGENT_IDS = sorted(ADAPTERS)


def _target(adapter: Adapter, target_dir: str | None) -> Path:
    base = Path.home() if target_dir is None else Path(target_dir).expanduser().resolve()
    return base / adapter.rel_path


def _block(content: str) -> str:
    return f"{BEGIN}\n\n{content.rstrip()}\n\n{END}\n"


def install(agent: str, target_dir: str | None = ".", force: bool = False,
            command: str = "aip") -> tuple[Path, str]:
    """Install one adapter. Returns (path, action).

    Actions: created | updated | unchanged | exists (differs; need --force).
    """
    adapter = ADAPTERS[agent]
    path = _target(adapter, target_dir)
    content = adapter.render(command)

    if adapter.mode == "file":
        if path.exists() and not force:
            if path.read_text(encoding="utf-8") == content:
                return path, "unchanged"
            return path, "exists"
        path.parent.mkdir(parents=True, exist_ok=True)
        action = "updated" if path.exists() else "created"
        path.write_text(content, encoding="utf-8")
        return path, action

    # block mode — surgically manage only our marker-delimited section.
    block = _block(content)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(block, encoding="utf-8")
        return path, "created"
    text = path.read_text(encoding="utf-8")
    if BEGIN in text and END in text:
        pre, rest = text.split(BEGIN, 1)
        _, post = rest.split(END, 1)
        new = pre + block.rstrip("\n") + post
        if new == text:
            return path, "unchanged"
        path.write_text(new, encoding="utf-8")
        return path, "updated"
    path.write_text(text.rstrip("\n") + "\n\n" + block, encoding="utf-8")
    return path, "updated"


def uninstall(agent: str, target_dir: str | None = ".") -> tuple[Path, str]:
    """Remove one adapter. Never deletes user content outside our block."""
    adapter = ADAPTERS[agent]
    path = _target(adapter, target_dir)
    if not path.exists():
        return path, "absent"

    if adapter.mode == "file":
        path.unlink()
        parent = path.parent
        for _ in range(3):  # only removes directories we alone occupied
            try:
                parent.rmdir()
            except OSError:
                break
            parent = parent.parent
        return path, "removed"

    text = path.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        return path, "absent"
    pre, rest = text.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    remainder = (pre.rstrip("\n") + "\n" + post.lstrip("\n")).strip("\n")
    if remainder:
        path.write_text(remainder + "\n", encoding="utf-8")
    else:
        path.unlink()
    return path, "removed"
