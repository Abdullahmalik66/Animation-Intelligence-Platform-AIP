"""Tests for `aip route`, `aip context`, and `aip init`."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from aip.claude import (SKILL, SKILL_REL, init, remove, render_skill,
                        resolve_command, skill_path)
from aip.knowledge import TOPICS, get_context, list_topics, route_request


class TestInspector(unittest.TestCase):
    """Salvaged from test_platform.py — inspector remains a core engine."""

    def test_lockfile_resolution(self):
        from aip.state import AnimationProjectState
        from aip.inspector import (inspect_project,
                                   installed_animation_technologies)
        with tempfile.TemporaryDirectory() as td:
            Path(td, "package.json").write_text(json.dumps(
                {"dependencies": {"gsap": "^3.12.0", "react": "^18.0.0"}}))
            Path(td, "package-lock.json").write_text(json.dumps(
                {"packages": {"node_modules/gsap": {"version": "3.12.5"}}}))
            s = inspect_project(td, AnimationProjectState(raw_user_request="x"))
            self.assertEqual(s.resolved_versions["gsap"], "3.12.5")
            self.assertEqual(s.framework, "react")
            self.assertEqual(installed_animation_technologies(s), ["gsap"])

    def test_missing_project_marks_unknown(self):
        from aip.state import AnimationProjectState
        from aip.inspector import inspect_project
        s = AnimationProjectState(raw_user_request="x")
        with tempfile.TemporaryDirectory() as td:
            inspect_project(td, s)
        self.assertTrue(any("package.json" in u for u in s.unknowns))


class TestContext(unittest.TestCase):
    def test_every_topic_resolves(self):
        """Every advertised topic must return real, non-empty content."""
        for topic in list_topics():
            with self.subTest(topic=topic):
                text = get_context(topic)
                self.assertGreater(len(text), 200, f"{topic} too small")

    def test_sectioned_topics_are_not_whole_files(self):
        """Sectioned topics must be a genuine subset — context is a budget."""
        for topic, (rel, headings) in TOPICS.items():
            if headings is None:
                continue
            with self.subTest(topic=topic):
                whole = (Path(__file__).parent.parent / "aip" / "data" / rel
                         ).read_text(encoding="utf-8")
                self.assertLess(len(get_context(topic)), len(whole))

    def test_unknown_topic_raises(self):
        with self.assertRaises(KeyError):
            get_context("does-not-exist")


class TestRoute(unittest.TestCase):
    def test_explicit_technology_wins(self):
        r = route_request("use gsap scrolltrigger to pin the hero")
        self.assertEqual(r["technology"], "gsap")
        self.assertIn("scrolltrigger", r["required_context"])

    def test_hover_stays_native(self):
        r = route_request("button grows slightly on hover")
        self.assertEqual(r["technology"], "css")
        self.assertEqual(r["complexity"], "low")

    def test_scroll_reveal_routes_deterministically(self):
        r = route_request("scroll reveal cards")
        self.assertIsNotNone(r["technology"])
        self.assertEqual(r["decided_by"], "deterministic")
        self.assertIn("accessibility", r["required_context"])

    def test_scroll_reveal_prefers_installed_library(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / "package.json").write_text(
                '{"dependencies":{"gsap":"^3.12.5"}}')
            r = route_request("scroll reveal cards", td)
            self.assertEqual(r["technology"], "gsap")

    def test_never_guesses(self):
        """When the router cannot decide, technology is null — not a guess."""
        r = route_request("make the thing feel nicer somehow")
        if r["technology"] is None:
            self.assertEqual(r["decided_by"], "llm-assisted-required")
            self.assertTrue(r["required_context"])  # still gives Claude something

    def test_context_keys_are_all_valid(self):
        """Anything route recommends must be retrievable by context."""
        for request in ["gsap scroll reveal", "3d product viewer",
                        "lottie loading spinner", "fade in a card",
                        "rive interactive character", "spinner that loops"]:
            with self.subTest(request=request):
                for key in route_request(request)["required_context"]:
                    self.assertIn(key, TOPICS)

    def test_reads_installed_packages(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / "package.json").write_text(
                '{"dependencies":{"gsap":"^3.12.5"}}')
            self.assertIn("gsap", route_request("animate cards", td)["installed"])


class TestInit(unittest.TestCase):
    def test_creates_exactly_one_file(self):
        with tempfile.TemporaryDirectory() as td:
            init(td)
            files = [p for p in Path(td).rglob("*") if p.is_file()]
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].relative_to(td), SKILL_REL)

    def test_idempotent(self):
        with tempfile.TemporaryDirectory() as td:
            init(td)
            self.assertEqual(init(td)[1], "unchanged")

    def test_never_clobbers_user_edits(self):
        with tempfile.TemporaryDirectory() as td:
            path, _ = init(td)
            path.write_text("my own notes")
            self.assertEqual(init(td)[1], "exists")
            self.assertEqual(path.read_text(), "my own notes")
            self.assertEqual(init(td, force=True)[1], "updated")

    def test_remove_leaves_nothing(self):
        with tempfile.TemporaryDirectory() as td:
            init(td)
            remove(td)
            self.assertEqual(list(Path(td).rglob("*")), [])

    def test_skill_references_only_real_commands(self):
        """The skill must not instruct Claude to run commands that don't exist."""
        for cmd in ["aip route", "aip context", "aip check"]:
            self.assertIn(cmd, SKILL)
        self.assertNotIn("aip ask", SKILL)
        self.assertNotIn("aip generate", SKILL)

    def test_skill_topics_exist(self):
        """Topics named in the skill must be retrievable."""
        self.assertIn("decision-matrix", TOPICS)


class TestCommandResolution(unittest.TestCase):
    def test_prefers_aip_on_path(self):
        with mock.patch("aip.claude.shutil.which",
                        side_effect=lambda c: "/usr/bin/" + c):
            self.assertEqual(resolve_command(), "aip")

    def test_falls_back_to_npx(self):
        with mock.patch("aip.claude.shutil.which",
                        side_effect=lambda c: "/usr/bin/npx" if c == "npx" else None):
            self.assertEqual(resolve_command(), "npx aip-cli")

    def test_nothing_available_still_says_aip(self):
        """Never invent a command — the skill's error clause covers this."""
        with mock.patch("aip.claude.shutil.which", return_value=None):
            self.assertEqual(resolve_command(), "aip")

    def test_render_rewrites_every_invocation(self):
        rendered = render_skill("npx aip-cli")
        for cmd in ["npx aip-cli route", "npx aip-cli context", "npx aip-cli check"]:
            self.assertIn(cmd, rendered)
        # No bare `aip route/context/check` invocation survives.
        import re
        self.assertIsNone(re.search(r"(?<!aip-cli )\baip (route|context|check)\b",
                                    rendered.replace("npx aip-cli", "NPX")))

    def test_render_default_is_canonical(self):
        self.assertEqual(render_skill("aip"), SKILL)

    def test_init_bakes_in_resolved_command(self):
        with tempfile.TemporaryDirectory() as td:
            path, _ = init(td, command="npx aip-cli")
            self.assertIn("npx aip-cli check", path.read_text())


class TestGlobalInstall(unittest.TestCase):
    def test_global_targets_home(self):
        with tempfile.TemporaryDirectory() as td, \
             mock.patch("aip.claude.Path.home", return_value=Path(td)):
            path, action = init(None, command="aip")
            self.assertEqual(action, "created")
            self.assertEqual(path, Path(td) / SKILL_REL)
            self.assertTrue(path.is_file())
            # No duplicate: second install is a no-op.
            self.assertEqual(init(None, command="aip")[1], "unchanged")
            # Symmetric removal leaves nothing behind.
            self.assertEqual(remove(None)[1], "removed")
            self.assertEqual(list(Path(td).rglob("*")), [])

    def test_skill_path_global_vs_project(self):
        self.assertEqual(skill_path(None), Path.home() / SKILL_REL)
        self.assertNotEqual(skill_path("."), skill_path(None))


class TestAdapters(unittest.TestCase):
    def test_every_adapter_installs_and_removes_cleanly(self):
        from aip.adapters import AGENT_IDS, install, uninstall
        for agent in AGENT_IDS:
            with self.subTest(agent=agent), tempfile.TemporaryDirectory() as td:
                path, action = install(agent, td)
                self.assertEqual(action, "created")
                text = path.read_text()
                for cmd in ["aip route", "aip context", "aip check"]:
                    self.assertIn(cmd, text)
                self.assertEqual(install(agent, td)[1], "unchanged")
                self.assertEqual(uninstall(agent, td)[1], "removed")
                self.assertEqual(list(Path(td).rglob("*")), [])

    def test_claude_adapter_matches_legacy_skill(self):
        """The claude adapter and the historical `init` write identical bytes."""
        from aip.adapters import install
        with tempfile.TemporaryDirectory() as td:
            path, _ = install("claude", td)
            self.assertEqual(path.read_text(), SKILL)

    def test_block_mode_preserves_user_content(self):
        from aip.adapters import install, uninstall
        with tempfile.TemporaryDirectory() as td:
            agents_md = Path(td) / "AGENTS.md"
            agents_md.write_text("# My project rules\n\nUse tabs.\n")
            install("codex", td)
            text = agents_md.read_text()
            self.assertIn("Use tabs.", text)
            self.assertIn("aip route", text)
            # Update is idempotent and stays inside the block.
            self.assertEqual(install("codex", td)[1], "unchanged")
            self.assertEqual(text.count("aip:begin"), 1)
            # Removal restores user content untouched.
            uninstall("codex", td)
            final = agents_md.read_text()
            self.assertIn("Use tabs.", final)
            self.assertNotIn("aip:begin", final)
            self.assertNotIn("aip route", final)

    def test_block_removed_entirely_when_aip_created_the_file(self):
        from aip.adapters import install, uninstall
        with tempfile.TemporaryDirectory() as td:
            install("gemini", td)
            uninstall("gemini", td)
            self.assertEqual(list(Path(td).rglob("*")), [])

    def test_adapters_render_resolved_command(self):
        from aip.adapters import install
        with tempfile.TemporaryDirectory() as td:
            path, _ = install("copilot", td, command="npx aip-cli")
            text = path.read_text()
            self.assertIn("npx aip-cli check", text)
            self.assertIn("applyTo:", text)

    def test_single_source_of_truth(self):
        """Every adapter body derives from the same canonical BODY."""
        from aip.adapters import ADAPTERS
        from aip.claude import BODY
        for adapter in ADAPTERS.values():
            self.assertIn(BODY.split("\n", 1)[0], adapter.render("aip"))


class TestSelfHealingLoop(unittest.TestCase):
    """Executable proof of route -> context -> check -> repair -> check -> pass."""

    def test_loop_closes_on_css(self):
        from aip.check import check_path
        with tempfile.TemporaryDirectory() as td:
            # 1. Route the request; confirm it points at CSS + accessibility.
            r = route_request("cards fade in on hover", td)
            self.assertEqual(r["technology"], "css")
            self.assertIn("accessibility", r["required_context"])

            # 2. Context for every required key is retrievable.
            for key in r["required_context"]:
                self.assertTrue(get_context(key))

            # 3. "Generated" code with a known violation: no reduced-motion guard.
            f = Path(td) / "cards.css"
            f.write_text("@keyframes pop { from { transform: scale(1); }\n"
                         "  to { transform: scale(1.05); } }\n"
                         ".card:hover { animation: pop 0.3s ease; }\n")
            report = check_path(td)
            rules = {x.rule for x in report.findings}
            self.assertIn("a11y/no-reduced-motion-fallback", rules)

            # 4. Repair (the mechanical fix path) and 5. re-check: clean.
            fixed = check_path(td, fix=True)
            self.assertGreaterEqual(fixed.fixed_count, 1)
            final = check_path(td)
            self.assertEqual(final.error_count, 0, [vars(x) for x in final.findings])

    def test_loop_reports_unfixable_findings_honestly(self):
        """Non-mechanical findings survive --fix and stay reported (never hidden)."""
        from aip.check import check_path
        with tempfile.TemporaryDirectory() as td:
            f = Path(td) / "leak.jsx"
            f.write_text(
                "import { useEffect } from 'react';\n"
                "export function C() {\n"
                "  useEffect(() => {\n"
                "    const loop = () => { requestAnimationFrame(loop); };\n"
                "    requestAnimationFrame(loop);\n"
                "  }, []);\n"
                "  return null;\n"
                "}\n")
            report = check_path(td, fix=True)
            rules = {x.rule for x in report.findings}
            self.assertIn("leak/raf-not-cancelled", rules)
            # And every surviving finding carries a fix_hint Claude can act on.
            for x in report.findings:
                self.assertTrue(x.fix_hint, f"{x.rule} has no fix_hint")


if __name__ == "__main__":
    unittest.main()
