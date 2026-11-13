"""One SemVer 2.0.0 grammar serves the release tag, schemas and skill envelope."""

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
from semver_grammar import SEMVER_PATTERN, is_semver  # noqa: E402

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
FULL = "^" + SEMVER_PATTERN + "$"
CORE = "^" + SEMVER_PATTERN.split("(?:-", 1)[0] + "$"
SCHEMAS = ("frontmatter.schema.json", "document-profile.schema.json")


def _version_patterns(node: object) -> list[str]:
    """Every `version` property pattern in a schema, at any depth."""

    found: list[str] = []
    if isinstance(node, dict):
        version = node.get("version")
        if isinstance(version, dict) and "pattern" in version:
            found.append(version["pattern"])
        for child in node.values():
            found.extend(_version_patterns(child))
    elif isinstance(node, list):
        for child in node:
            found.extend(_version_patterns(child))
    return found


def _schema_patterns() -> dict[str, list[str]]:
    contracts = ROOT / "docs/99.templates/contracts"
    return {
        name: _version_patterns(json.loads((contracts / name).read_text()))
        for name in SCHEMAS
    }


class SemverGrammarTests(unittest.TestCase):
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
        patterns = _schema_patterns()
        self.assertEqual(patterns["frontmatter.schema.json"], [FULL])
        # The adopted-binding branch keeps its final-edition guard: the numeric
        # core of the grammar, with no prerelease or build metadata.
        self.assertEqual(
            sorted(patterns["document-profile.schema.json"]), sorted([FULL, FULL, CORE])
        )

    def test_every_schema_pattern_accepts_and_refuses_the_cases(self) -> None:
        for name, found in _schema_patterns().items():
            for pattern in found:
                final = pattern == CORE
                for value in VALID:
                    expected = not (final and re.search(r"[-+]", value))
                    with self.subTest(schema=name, value=value):
                        self.assertEqual(
                            re.search(pattern, value) is not None, expected
                        )
                for value in INVALID:
                    with self.subTest(schema=name, value=value):
                        self.assertIsNone(re.search(pattern, value))

    def test_skill_envelope_refuses_an_invalid_version(self) -> None:
        registry = GOVERNANCE.load_json(ROOT, GOVERNANCE.REGISTRY_PATH)
        skill = ".agents/skills/k8s-validate/SKILL.md"
        original = GOVERNANCE._read_text
        text = (ROOT / skill).read_text()
        current = re.search(r'^  version: "([^"]*)"$', text, re.M)
        assert current is not None

        def check(value: str) -> None:
            changed = text.replace(current.group(0), f'  version: "{value}"')

            def read(root: Path, path: str, code: str) -> str:
                return changed if path == skill else original(root, path, code)

            with mock.patch.object(GOVERNANCE, "_read_text", read):
                GOVERNANCE.validate_native_assets(ROOT, registry)

        for value in VALID:
            with self.subTest(value=value):
                check(value)
        for value in INVALID:
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
