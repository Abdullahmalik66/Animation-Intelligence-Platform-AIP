"""`aip init` — install the Claude Code animation skill.

Writes exactly one file: `.claude/skills/animation/SKILL.md`.
Nothing else is created, and nothing existing is touched.
"""
from __future__ import annotations

from pathlib import Path

SKILL_REL = Path(".claude/skills/animation/SKILL.md")

SKILL = """---
name: animation
description: >-
  Use when writing, reviewing, or fixing web animation code — CSS transitions,
  keyframes, GSAP, Motion/Framer Motion, Three.js, Lottie, Rive, Anime.js,
  requestAnimationFrame loops, scroll effects, or any UI motion.
---

# Animation Engineering

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


def init(target_dir: str = ".", force: bool = False) -> tuple[Path, str]:
    """Write the Claude skill. Returns (path, action)."""
    path = Path(target_dir).expanduser().resolve() / SKILL_REL

    if path.exists() and not force:
        if path.read_text(encoding="utf-8") == SKILL:
            return path, "unchanged"
        return path, "exists"

    path.parent.mkdir(parents=True, exist_ok=True)
    action = "updated" if path.exists() else "created"
    path.write_text(SKILL, encoding="utf-8")
    return path, action


def remove(target_dir: str = ".") -> tuple[Path, str]:
    """Remove the skill file and any directories it alone occupied."""
    path = Path(target_dir).expanduser().resolve() / SKILL_REL
    if not path.exists():
        return path, "absent"
    path.unlink()
    for parent in (path.parent, path.parent.parent, path.parent.parent.parent):
        try:
            parent.rmdir()  # Only succeeds when empty — never removes user files.
        except OSError:
            break
    return path, "removed"
