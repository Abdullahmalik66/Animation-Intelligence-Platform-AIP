"""`aip init` — install the Claude Code animation skill.

Writes exactly one file: `.claude/skills/animation/SKILL.md` (project) or
`~/.claude/skills/animation/SKILL.md` (--global).
Nothing else is created, and nothing existing is touched.

The skill is rendered with whichever command actually reaches AIP on this
machine (`aip` on PATH, or the `npx aip-cli` shim), so it works for pipx,
pip, npm, and npx users alike.
"""
from __future__ import annotations

import shutil
from pathlib import Path

SKILL_REL = Path(".claude/skills/animation/SKILL.md")

# One-line summary used by every adapter that supports a description field.
DESCRIPTION = ("Use when writing, reviewing, or fixing web animation code — "
               "CSS transitions, keyframes, GSAP, Motion/Framer Motion, "
               "Three.js, Lottie, Rive, Anime.js, requestAnimationFrame "
               "loops, scroll effects, or any UI motion.")

_FRONTMATTER = """---
name: animation
description: >-
  Use when writing, reviewing, or fixing web animation code — CSS transitions,
  keyframes, GSAP, Motion/Framer Motion, Three.js, Lottie, Rive, Anime.js,
  requestAnimationFrame loops, scroll effects, or any UI motion.
---

"""

# The canonical, platform-neutral instruction body. Single source of truth
# for every agent adapter (Claude, Copilot, Cursor, Windsurf, AGENTS.md, …).
BODY = """# Animation Engineering

You already know how to write animation code. The `aip` tool supplies the three
things you cannot get from the model alone: which technology this project can
actually use, the library-specific lifecycle rules, and a deterministic check on
what you wrote.

Follow this loop whenever the task involves motion.

## 1. Route

Before choosing a technology, run:

```bash
aip route "<the user's request>"
```

It returns JSON: `technology`, `architecture`, `complexity`, `required_context`,
`signals`, and `installed`. It reads the project's `package.json` and lockfile,
so `technology` reflects what is genuinely installed. Prefer it over your own
guess — if it says `css`, do not reach for GSAP.

Two cases need judgement from you:

- **`"technology": null`** — the router refused to guess. Decide yourself, using
  `installed` and `aip context decision-matrix`. Prefer the lightest tool that
  does the job; prefer what is already installed over a new dependency.
- **`"architecture": "needs-disambiguation"`** — the request is genuinely
  ambiguous (usually scroll-linked scrubbing vs. play-once-on-entry). Ask the
  user which they want before writing code. Do not silently pick one.

## 2. Load context

For each key in `required_context`:

```bash
aip context <key>
```

Load only those. They contain the version gates, cleanup requirements, and
accessibility rules for that specific library. Do not load everything.

## 3. Write the code

Apply what the context told you. Non-negotiable, regardless of library:

- Every animation needs a `prefers-reduced-motion` path.
- Everything created in an effect must be destroyed in its cleanup: GSAP
  contexts reverted, rAF loops cancelled, observers disconnected, listeners
  removed, WebGL geometries/materials/textures disposed.
- Animate `transform` and `opacity`. Not `left`, `top`, `width`, `height`, or
  `margin` — those trigger layout on every frame.

## 4. Check

Always, before you present the code:

```bash
aip check <file> --format json
```

Exit code `0` means clean. Non-zero means there are findings.

## 5. Repair

Each finding has `rule`, `message`, `line`, and `fix_hint`. The `fix_hint` states
the specific repair. Apply it and run `aip check` again.

Repeat until clean, up to **three** attempts. Then stop:

- **Clean** — present the code. Mention briefly that it passes `aip check`.
- **Still failing after 3 attempts** — present the code anyway, followed by the
  remaining findings, verbatim, and say plainly which ones you could not fix.
  Never present failing code as if it passed. Never stay silent about a finding.

If the same finding survives two attempts, stop early — repeating the edit will
not help. Say what is blocking you.

## Notes

- `aip check` also works on existing files. Use it when asked to review or fix
  animation code, before proposing changes.
- If a command errors (`aip: command not found`, unknown topic), do not fake the
  output. Say the tool is unavailable and proceed with your own knowledge,
  applying the three non-negotiables above.
- `aip check --fix` applies only mechanical, behaviour-preserving fixes. Anything
  requiring judgement is reported, not rewritten.
"""


def resolve_command() -> str:
    """Return the invocation that actually reaches AIP on this machine.

    Preference order:
      1. `aip`      — pipx / pip / npm -g installs put it on PATH.
      2. `npx aip-cli` — the npm shim; works for npx-only users.
    Falls back to `aip` (with the skill's own error-handling clause covering
    the truly-broken case) rather than ever writing a command we invented.
    """
    if shutil.which("aip"):
        return "aip"
    if shutil.which("npx"):
        return "npx aip-cli"
    return "aip"


def render_body(command: str = "aip") -> str:
    """Render the canonical instruction body with a concrete AIP invocation."""
    if command == "aip":
        return BODY
    import re
    return re.sub(r"\baip (route|context|check)\b", f"{command} \\1", BODY)


def render_skill(command: str = "aip") -> str:
    """Render the Claude skill (frontmatter + body)."""
    return _FRONTMATTER + render_body(command)


# Canonical rendering — used by tests and by installs where `aip` is on PATH.
SKILL = render_skill("aip")


def skill_path(target_dir: str | None = ".") -> Path:
    """Resolve the skill location. `None` targets the global ~/.claude."""
    base = Path.home() if target_dir is None else Path(target_dir).expanduser().resolve()
    return base / SKILL_REL


def init(target_dir: str | None = ".", force: bool = False,
         command: str | None = None) -> tuple[Path, str]:
    """Write the Claude skill. Returns (path, action).

    `target_dir=None` installs globally to ~/.claude/skills/animation/.
    `command=None` auto-detects how AIP is reachable on this machine.
    """
    path = skill_path(target_dir)
    content = render_skill(command if command is not None else resolve_command())

    if path.exists() and not force:
        if path.read_text(encoding="utf-8") == content:
            return path, "unchanged"
        return path, "exists"

    path.parent.mkdir(parents=True, exist_ok=True)
    action = "updated" if path.exists() else "created"
    path.write_text(content, encoding="utf-8")
    return path, action


def remove(target_dir: str | None = ".") -> tuple[Path, str]:
    """Remove the skill file and any directories it alone occupied."""
    path = skill_path(target_dir)
    if not path.exists():
        return path, "absent"
    path.unlink()
    for parent in (path.parent, path.parent.parent, path.parent.parent.parent):
        try:
            parent.rmdir()  # Only succeeds when empty — never removes user files.
        except OSError:
            break
    return path, "removed"
