"""Commit syntax and changelog disposition share native configuration owners."""

import re
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
            "revert(gitops): restore the prior route\n\nThis reverts commit abcdef0.",
            "docs: " + "long guidance " * 9 + "remains a recommendation",
        ):
            with self.subTest(message=message):
                self.assertIsNotNone(pattern.fullmatch(message))
        for message in (
            "invalid subject",
            "fix: trailing period.",
            "feat(gitops)!: change admission",
            "fix: ",
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


if __name__ == "__main__":
    unittest.main()
