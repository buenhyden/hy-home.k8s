"""Commit syntax and changelog disposition share native configuration owners."""

import re
import os
import shutil
import subprocess
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CommitContractTests(unittest.TestCase):
    def setUp(self):
        self.settings = tomllib.loads((ROOT / ".cz.toml").read_text())["tool"][
            "commitizen"
        ]
        self.cz = self.settings["customize"]
        self.cliff = tomllib.loads((ROOT / "cliff.toml").read_text())["git"]

    def test_generated_message_exceptions_remain_explicit(self):
        self.assertEqual(
            self.settings["allowed_prefixes"],
            ["Merge", "Revert", "Pull request", "fixup!", "squash!", "amend!"],
        )
        self.assertTrue(self.cliff["filter_unconventional"])

    def test_supported_messages_and_rejections(self):
        pattern = re.compile(self.cz["schema_pattern"])
        for message in (
            "fix(gitops): preserve namespace ownership",
            "docs: Explain the rollback boundary",
            "feat(policy): change admission rules\n\nBREAKING CHANGE: deny unowned namespaces",
            "feat(gitops)!: change admission",
            "fix!: remove fallback",
            "feat(운영): 한글 범위 유지",
            "revert(gitops): restore the prior route\n\nThis reverts commit abcdef0.",
            "docs: " + "long guidance " * 9 + "remains a recommendation",
        ):
            with self.subTest(message=message):
                self.assertIsNotNone(pattern.fullmatch(message))
        for message in (
            "invalid subject",
            "fix: trailing period.",
            "fix: ",
            "fix:    ",
            "fix: repair\rroute",
            "fix(): empty scope",
            "fix: subject\nbody without separator",
        ):
            with self.subTest(message=message):
                self.assertIsNone(pattern.fullmatch(message))

    def test_historical_parser_retains_prior_punctuation(self):
        message = "fix(gitops): preserve old history."
        self.assertIsNone(re.fullmatch(self.cz["schema_pattern"], message))
        parsed = re.fullmatch(self.cz["commit_parser"], message)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed["scope"], "gitops")
        self.assertIsNotNone(
            re.fullmatch(self.cz["commit_parser"], "feat(gitops)!: remove route")
        )

    def test_changelog_first_match_covers_supported_types(self):
        def disposition(subject, body="", breaking=False):
            for parser in self.cliff["commit_parsers"]:
                if parser.get("field") == "breaking" and re.search(
                    parser["pattern"], str(breaking).lower()
                ):
                    return parser
                if "message" in parser and re.search(parser["message"], subject):
                    return parser
                if "body" in parser and re.search(parser["body"], body):
                    return parser
            self.fail("supported commit has no changelog disposition: " + subject)

        self.assertTrue(disposition("chore(release): prepare version").get("skip"))
        for kind in self.cz["change_type_map"]:
            with self.subTest(kind=kind):
                self.assertIn("group", disposition(kind + "(gitops): update contract"))
        self.assertEqual(
            disposition("feat(policy): change admission", breaking=True)["group"],
            "Breaking Changes",
        )
        self.assertEqual(
            disposition(
                "docs: describe migration",
                body="This is not a BREAKING CHANGE instruction.",
            )["group"],
            "Documentation",
        )
        self.assertEqual(
            disposition(
                "feat(policy): change admission",
                body="Migration notes.\n\nBREAKING CHANGE: deny old route",
                breaking=True,
            )["group"],
            "Breaking Changes",
        )

    def test_native_changelog_distinguishes_prose_and_breaking_commits(self):
        cliff = shutil.which("git-cliff")
        if cliff is None:
            self.skipTest("git-cliff is unavailable; native proof is separate")
        self.assertFalse(Path(cliff).resolve().is_relative_to(ROOT))
        with tempfile.TemporaryDirectory(prefix="commit-contract-") as temporary:
            root = Path(temporary)
            environment = {
                "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_CONFIG_PARAMETERS": "",
                "GIT_CONFIG_COUNT": "0",
                "GIT_AUTHOR_NAME": "Fixture",
                "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                "GIT_COMMITTER_NAME": "Fixture",
                "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
                "HOME": temporary,
            }

            def run(*argv):
                result = subprocess.run(
                    argv,
                    cwd=root,
                    env=environment,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=20,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                return result.stdout

            run("/usr/bin/git", "init", "--quiet")
            for message in (
                "docs: describe migration\n\nThis is not a BREAKING CHANGE instruction.",
                "feat(core): change API\n\nBREAKING CHANGE: remove old API",
                "feat(core)!: remove route",
                "fix!: remove fallback",
            ):
                run("/usr/bin/git", "commit", "--allow-empty", "--quiet", "-m", message)
            changelog = run(cliff, "--config", str(ROOT / "cliff.toml"), "--unreleased")
            headings = list(re.finditer(r"(?m)^### (.+)$", changelog))
            sections = {}
            for index, heading in enumerate(headings):
                end = headings[index + 1].start() if index + 1 < len(headings) else None
                sections[heading.group(1)] = changelog[heading.end() : end]
            self.assertIn("Describe migration", sections.get("Documentation", ""))
            breaking = sections.get("Breaking Changes", "")
            for subject in ("Change API", "Remove route", "Remove fallback"):
                self.assertIn(subject, breaking)
            self.assertNotIn("Describe migration", breaking)


if __name__ == "__main__":
    unittest.main()
