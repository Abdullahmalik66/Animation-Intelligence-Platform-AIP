"""AIP command line interface.

Usage:
  aip check PATH [--fix] [--format human|json|sarif|github]
  aip route "<request>" [--project DIR]
  aip context [TOPIC]
  aip init [PATH] [--agent NAME|all] [--global] [--force] [--remove]

Everything is deterministic and offline: no AI, no network, no credentials.
"""
from __future__ import annotations

import argparse
import json
import sys

from . import __version__
from .check import check_path, format_report


def cmd_check(args) -> int:
    try:
        report = check_path(args.path, fix=args.fix)
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    use_colour = args.format == "human" and sys.stdout.isatty()
    print(format_report(report, fmt=args.format, color=use_colour))
    return 1 if report.error_count else 0


def cmd_route(args) -> int:
    from .knowledge import route_request
    print(json.dumps(route_request(args.request, args.project), indent=2))
    return 0


def cmd_context(args) -> int:
    from .knowledge import get_context, list_topics
    if args.topic is None:
        print("\n".join(list_topics()))
        return 0
    try:
        print(get_context(args.topic))
    except KeyError:
        print(f"aip: unknown topic '{args.topic}'.\n"
              f"Available: {', '.join(list_topics())}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"aip: {exc}", file=sys.stderr)
        return 2
    return 0


def cmd_init(args) -> int:
    from .adapters import ADAPTERS, AGENT_IDS, install, uninstall
    from .claude import resolve_command

    agents = AGENT_IDS if args.agent == "all" else [args.agent]
    target = None if getattr(args, "global_", False) else args.path

    if args.remove:
        for agent in agents:
            path, action = uninstall(agent, target)
            print(f"{action}: {path}" if action == "removed"
                  else f"nothing to remove at {path}")
        return 0

    command = resolve_command()
    rc = 0
    for agent in agents:
        path, action = install(agent, target, force=args.force, command=command)
        if action == "exists":
            print(f"aip: {path} already exists and differs.\n"
                  f"     Re-run with --force to overwrite.", file=sys.stderr)
            rc = 1
        elif action == "unchanged":
            print(f"already up to date: {path}")
        else:
            print(f"{action}: {path}  ({ADAPTERS[agent].label})")
    if rc == 0 and not args.remove:
        note = ("" if command == "aip" else
                f"\nNote: `aip` is not on PATH, so the instructions invoke AIP via "
                f"`{command}`.\nInstall with `pipx install aip` for the direct command.")
        print(f"\nYour agent will now route, load context, and validate animation\n"
              f"code automatically. Those are the only files AIP added.{note}")
    return rc


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        prog="aip",
        description="Lint web animation code for memory leaks, jank, "
                    "and accessibility violations.")
    ap.add_argument("--version", action="version", version=f"aip {__version__}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    chk = sub.add_parser("check", help="Lint animation code. No AI required.")
    chk.add_argument("path", nargs="?", default=".")
    chk.add_argument("--fix", action="store_true",
                     help="Apply safe mechanical fixes.")
    chk.add_argument("--format", default="human",
                     choices=["human", "json", "sarif", "github"])
    chk.set_defaults(func=cmd_check)

    rt = sub.add_parser("route", help="Decide the technology for a request.")
    rt.add_argument("request")
    rt.add_argument("--project", default=".",
                    help="Project to inspect for installed libraries.")
    rt.set_defaults(func=cmd_route)

    ctx = sub.add_parser("context", help="Print packaged animation knowledge.")
    ctx.add_argument("topic", nargs="?", default=None,
                     help="Topic key. Omit to list all topics.")
    ctx.set_defaults(func=cmd_context)

    ini = sub.add_parser("init", help="Install animation instructions for an AI coding agent.")
    ini.add_argument("path", nargs="?", default=".")
    ini.add_argument("--agent", default="claude",
                     choices=["claude", "copilot", "cursor", "windsurf",
                              "cline", "codex", "gemini", "all"],
                     help="Which agent to install for (default: claude).")
    ini.add_argument("--global", dest="global_", action="store_true",
                     help="Install to the home directory instead of the project.")
    ini.add_argument("--force", action="store_true",
                     help="Overwrite an existing, modified skill file.")
    ini.add_argument("--remove", action="store_true",
                     help="Remove the skill file.")
    ini.set_defaults(func=cmd_init)
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(
        list(sys.argv[1:] if argv is None else argv))
    return args.func(args)
