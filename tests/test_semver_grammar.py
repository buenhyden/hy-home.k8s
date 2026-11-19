"""Numeric authoring versions and the separate product tag grammar."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from scripts import release  # noqa: E402
from semver_grammar import (  # noqa: E402
    NUMERIC_VERSION_PATTERN,
    SEMVER_PATTERN,
    is_numeric_version,
    is_semver,
    numeric_version_order,
)

SPEC = importlib.util.spec_from_file_location(
    "semver_agent_governance", ROOT / "scripts/validate-agent-governance.py"
)
assert SPEC is not None and SPEC.loader is not None
GOVERNANCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GOVERNANCE)

VALID = ("0.1.0", "1.2.3", "1.0.0-rc.1", "1.2.3+build.007", "1.2.3-rc.1+sha.abc")
INVALID = (
    "1.2",
    "01.2.3",
    "1.02.3",
    "1.2.03",
    "v1.2.3",
    "1.2.3-01",
    "1.2.3-",
    "1.2.3+",
    "1.2.3.4",
)
CORE = "^" + NUMERIC_VERSION_PATTERN + r"(?![\s\S])"
NUMERIC_VALID = ("0.0.0", "0.1.0", "1.2.3", "1.10.0")
NUMERIC_INVALID = (
    INVALID
    + VALID[2:]
    + (
        " 1.2.3",
        "1.2.3 ",
        "1.2.3\n",
        "1.2.3\r",
        "١.2.3",
        "1.２.3",
    )
)


def _schema(name: str) -> dict:
    path = ROOT / "docs/99.templates/01.contracts" / (name + ".schema.json")
    return json.loads(path.read_text(encoding="utf-8"))


class SemverGrammarTests(unittest.TestCase):
    def test_document_schema_rejects_suffixes_and_trailing_newline(self) -> None:
        pattern = _schema("frontmatter")["properties"]["version"]["pattern"]
        for value in ("1.2.3-rc.1", "1.2.3+build.1", "1.2.3\n"):
            with self.subTest(value=value):
                self.assertIsNone(re.search(pattern, value))

    def test_module_accepts_and_refuses_the_cases(self) -> None:
        for value in VALID:
            with self.subTest(value=value):
                self.assertTrue(is_semver(value))
        for value in INVALID + (" 1.2.3", "1.2.3 ", "1.2.3\n"):
            with self.subTest(value=value):
                self.assertFalse(is_semver(value))

    def test_pattern_has_the_five_groups_release_reads(self) -> None:
        match = re.fullmatch(SEMVER_PATTERN, "1.2.3-rc.1+sha.abc")
        assert match is not None
        self.assertEqual(match.groups(), ("1", "2", "3", "rc.1", "sha.abc"))

    def test_release_tag_pattern_derives_from_the_module(self) -> None:
        self.assertEqual(release._VERSION.pattern, "v" + SEMVER_PATTERN + r"\Z")
        for value in VALID:
            self.assertEqual(release.parse_version("v" + value).tag, "v" + value)
        for value in INVALID:
            with self.subTest(value=value), self.assertRaises(release.ReleaseError):
                release.parse_version("v" + value)

    def test_every_schema_pattern_equals_the_anchored_grammar(self) -> None:
        profile = _schema("document-profile")
        core = profile["$defs"]["numeric_version"]
        self.assertEqual(core["pattern"], CORE)
        for key in ("shared_contract", "common_forms"):
            rule = profile["properties"][key]["properties"]["version"]
            self.assertEqual(rule["$ref"], "#/$defs/numeric_version")
        definition = profile["$defs"]["template_definition"]["properties"]
        self.assertEqual(
            definition["contract_version"]["$ref"], "#/$defs/numeric_version"
        )
        self.assertEqual(_schema("frontmatter")["properties"]["version"], core)
        self.assertEqual(
            _schema("template-definition")["properties"]["contract_version"], core
        )

    def test_every_schema_pattern_accepts_and_refuses_the_cases(self) -> None:
        for values, expected in ((NUMERIC_VALID, True), (NUMERIC_INVALID, False)):
            for value in values:
                with self.subTest(value=value):
                    self.assertEqual(re.search(CORE, value) is not None, expected)
                    self.assertEqual(is_numeric_version(value), expected)
                    self.assertEqual(numeric_version_order(value) is not None, expected)
        self.assertFalse(is_numeric_version(123))
        self.assertIsNone(numeric_version_order(None))
        self.assertLess(numeric_version_order("1.9.0"), numeric_version_order("1.10.0"))
        self.assertIsNotNone(numeric_version_order("1" * 5000 + ".0.0"))

    def test_skill_envelope_refuses_an_invalid_version(self) -> None:
        registry = GOVERNANCE.load_json(ROOT, GOVERNANCE.REGISTRY_PATH)
        skill = ".agents/skills/k8s-validate/SKILL.md"
        original = GOVERNANCE._read_text
        text = (ROOT / skill).read_text()
        current = re.search(r'^  version: "([^"]*)"$', text, re.M)
        assert current is not None

        def check(value: str) -> None:
            quoted = json.dumps(value, ensure_ascii=False)
            changed = text.replace(current.group(0), f"  version: {quoted}")

            def read(root: Path, path: str, code: str) -> str:
                return changed if path == skill else original(root, path, code)

            with mock.patch.object(GOVERNANCE, "_read_text", read):
                GOVERNANCE.validate_native_assets(ROOT, registry)

        for value in NUMERIC_VALID:
            with self.subTest(value=value):
                check(value)
        for value in NUMERIC_INVALID:
            with self.subTest(value=value):
                with self.assertRaises(GOVERNANCE.HarnessError) as raised:
                    check(value)
                self.assertEqual(raised.exception.code, "AGENT-REGISTRY-SKILL")

    def test_precedence_follows_semver_not_text_order(self) -> None:
        def key(value: str) -> tuple[object, ...]:
            return release._precedence(release.parse_version("v" + value))

        self.assertLess(key("1.9.0"), key("1.10.0"))
        self.assertLess(key("1.0.0-rc.2"), key("1.0.0-rc.10"))
        self.assertLess(key("1.0.0-rc.10"), key("1.0.0"))
        self.assertEqual(key("1.2.3+build.1"), key("1.2.3+build.2"))


if __name__ == "__main__":
    unittest.main()
