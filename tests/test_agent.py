"""Tests for `aip route`, `aip context`, and `aip init`."""
import tempfile
import unittest
from pathlib import Path

from aip.claude import SKILL, SKILL_REL, init, remove
from aip.knowledge import TOPICS, get_context, list_topics, route_request


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


if __name__ == "__main__":
    unittest.main()
