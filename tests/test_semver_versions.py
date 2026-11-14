"""SPEC-0208: version comparison, tag order and the producer and consumer matrix.

No test here holds a value of the current registry: every value derives from
`REGISTRY_MAJOR` and from the registry file, so a later MAJOR step edits no case.
Each pure case reaches the new entry points by attribute, so a missing entry
point fails the case alone.
"""

from __future__ import annotations

import contextlib
import copy
import datetime as dt
import importlib.util
import inspect
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_authority as AUTHORITY  # noqa: E402
import document_contracts as CONTRACTS  # noqa: E402
import document_lifecycle as LIFECYCLE  # noqa: E402
import semver_grammar as GRAMMAR  # noqa: E402
from scripts import release  # noqa: E402
from tests.git_fixture import GitFixture  # noqa: E402

REGISTRY_FILE = ROOT / "docs/99.templates/registry.json"
SCHEMA_FILE = ROOT / "docs/99.templates/contracts/document-profile.schema.json"
FRONTMATTER_SCHEMA = ROOT / "docs/99.templates/contracts/frontmatter.schema.json"
REGISTRY_PATH = "docs/99.templates/registry.json"
MODE = "explicit-ref"
DOWNGRADE = "LIFECYCLE-VERSION-DOWNGRADE"
EDITION = "LIFECYCLE-VERSION-EDITION-CHANGED"
OTHER_DIGEST = "sha256:" + "0" * 64


def _load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_script("semver_versions_lifecycle", "validate-document-lifecycle.py")
GUARD = _load_script("semver_versions_guard", "provider_write_guard.py")
PROFILES = _load_script("semver_versions_profiles", "validate-markdown-profiles.py")
REGISTRY = CONTRACTS.load_registry(ROOT)
MAJOR = AUTHORITY.REGISTRY_MAJOR


def raw_registry() -> dict:
    return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))


def raw_schema() -> dict:
    return json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))


def level(old: str, new: str) -> str:
    """The increment class two release strings show, read through `precedence`."""
    before, after = GRAMMAR.precedence(old), GRAMMAR.precedence(new)
    if before == after:
        return "NO_CHANGE"
    return ("MAJOR", "MINOR", "PATCH", "PRERELEASE", "PRERELEASE")[
        next(index for index in range(5) if before[index] != after[index])
    ]


class PrecedenceTests(unittest.TestCase):
    ORDER = (
        "1.0.0-alpha",
        "1.0.0-alpha.1",
        "1.0.0-alpha.beta",
        "1.0.0-beta",
        "1.0.0-beta.2",
        "1.0.0-beta.11",
        "1.0.0-rc.1",
        "1.0.0",
        "1.9.0",
        "1.10.0",
        "2.0.0",
    )

    def test_the_shared_function_orders_by_semver_not_text(self) -> None:
        for lower, higher in zip(self.ORDER, self.ORDER[1:]):
            with self.subTest(lower=lower, higher=higher):
                self.assertLess(GRAMMAR.precedence(lower), GRAMMAR.precedence(higher))

    def test_build_metadata_never_changes_precedence(self) -> None:
        self.assertEqual(
            GRAMMAR.precedence("1.2.3+build.1"), GRAMMAR.precedence("1.2.3+build.2")
        )
        self.assertEqual(
            GRAMMAR.precedence("1.2.3-rc.1+a"), GRAMMAR.precedence("1.2.3-rc.1")
        )

    def test_a_value_outside_the_grammar_is_refused(self) -> None:
        for value in ("v1.2.3", "v14.7", "1.2", "01.2.3", "1.2.3-", "SPEC-0208", ""):
            with self.subTest(value=value), self.assertRaises(ValueError):
                GRAMMAR.precedence(value)

    def test_release_keeps_a_thin_wrapper_over_the_shared_function(self) -> None:
        for value in self.ORDER + ("1.2.3+build.9",):
            with self.subTest(value=value):
                self.assertEqual(
                    release._precedence(release.parse_version("v" + value)),
                    GRAMMAR.precedence(value),
                )
        self.assertNotIn("isdecimal", inspect.getsource(release))


class TagOrderTests(unittest.TestCase):
    """TAG object: the release order check, mapped here because no test held it."""

    def check(self, tag: str, previous: tuple[str, ...]) -> None:
        release._check_order(
            release.parse_version(tag),
            tuple(release.parse_version(item) for item in previous),
            False,
        )

    def refused(self, tag: str, previous: tuple[str, ...]) -> None:
        with self.assertRaises(release.ReleaseError) as caught:
            self.check(tag, previous)
        self.assertEqual(caught.exception.code, "RELEASE-VERSION-NOT-INCREASING")

    def test_a_lower_or_equal_tag_is_refused(self) -> None:
        self.refused("v0.1.0", ("v0.1.0",))
        self.refused("v0.9.0", ("v1.0.0",))
        self.refused("v1.9.0", ("v1.10.0",))
        self.refused("v1.0.0-rc.1", ("v1.0.0",))
        self.refused("v1.2.3+other", ("v1.2.3",))

    def test_a_higher_tag_is_accepted(self) -> None:
        self.check("v1.0.1", ("v1.0.0",))
        self.check("v1.10.0", ("v1.9.0", "v0.1.0"))
        self.check("v1.0.0", ("v1.0.0-rc.2",))

    def test_a_tag_outside_the_grammar_is_refused(self) -> None:
        for value in ("1.0.0", "v1.0", "v01.0.0", "v1.0.0-"):
            with self.subTest(value=value), self.assertRaises(release.ReleaseError):
                release.parse_version(value)


def document_text(version: str | None, artifact_id: str | None = None) -> str:
    key = f'version: "{version}"\n' if version is not None else ""
    identity = f'artifact_id: "{artifact_id}"\n' if artifact_id else ""
    kind = "sdlc/spec" if artifact_id else "governance/rule"
    status = "approved" if artifact_id else "active"
    return (
        f'---\ntitle: "Case"\n{key}type: "{kind}"\nstatus: "{status}"\n'
        f'owner: "platform"\nupdated: "2026-11-14"\n{identity}---\n\n# Case\n'
    )


RULE_PATH = PurePosixPath(".agents/governance/quality.md")
SPEC_PATH = PurePosixPath("docs/03.specs/0208-w03-semver-tests/spec.md")


def compare(
    base: str | None, proposed: str | None, path: PurePosixPath = RULE_PATH
) -> set[str]:
    """Version rule IDs of the base-to-proposed comparison of one scratch pair."""
    base_documents = {}
    proposed_documents = {}
    if base is not None:
        base_documents[path] = LIFECYCLE.document_from_text(
            REGISTRY, path, base, base_side=True
        )
    if proposed is not None:
        proposed_documents[path] = LIFECYCLE.document_from_text(
            REGISTRY, path, proposed
        )
    return {
        item.rule_id
        for item in LIFECYCLE.compare_lifecycle(
            REGISTRY, base_documents, proposed_documents, base_mode=MODE
        )
        if item.rule_id.startswith("LIFECYCLE-VERSION")
    }


def read_version(text: str, path: PurePosixPath = RULE_PATH) -> str | None:
    return LIFECYCLE.document_from_text(REGISTRY, path, text).version


class DocumentComparisonTests(unittest.TestCase):
    def accepted(self, base: str, proposed: str) -> None:
        self.assertEqual(read_version(document_text(base)), base)
        self.assertEqual(read_version(document_text(proposed)), proposed)
        self.assertEqual(compare(document_text(base), document_text(proposed)), set())

    def refused(self, base: str, proposed: str) -> None:
        self.assertEqual(
            compare(document_text(base), document_text(proposed)), {DOWNGRADE}
        )

    def test_a_lower_version_is_refused(self) -> None:
        for base, proposed in (
            ("1.2.0", "1.1.0"),
            ("1.2.3", "1.2.2"),
            ("2.0.0", "1.9.9"),
            ("1.10.0", "1.9.0"),
            ("1.0.0", "1.0.0-rc.2"),
            ("1.0.0-rc.10", "1.0.0-rc.2"),
        ):
            with self.subTest(base=base, proposed=proposed):
                self.refused(base, proposed)

    def test_an_unchanged_or_risen_version_is_accepted(self) -> None:
        for base, proposed in (
            ("1.2.0", "1.2.0"),
            ("1.2.0", "1.2.1"),
            ("1.2.0", "1.3.0"),
            ("1.2.0", "2.0.0"),
            ("1.9.0", "1.10.0"),
            ("1.0.0-rc.2", "1.0.0-rc.10"),
            ("1.0.0-rc.2", "1.0.0"),
        ):
            with self.subTest(base=base, proposed=proposed):
                self.accepted(base, proposed)

    def test_a_build_metadata_difference_alone_is_accepted(self) -> None:
        self.accepted("1.2.0+build.1", "1.2.0+build.2")
        self.accepted("1.2.0", "1.2.0+build.2")
        self.accepted("1.2.0+build.2", "1.2.0")

    def test_a_new_or_deleted_document_has_no_pair(self) -> None:
        text = document_text("1.0.0")
        self.assertEqual(read_version(text), "1.0.0")
        self.assertEqual(compare(None, text), set())
        self.assertEqual(compare(text, None), set())

    def test_a_value_outside_the_grammar_is_not_compared(self) -> None:
        for base, proposed in (("v14.7", "1.0.0"), ("1.0.0", "v14.7"), ("1.2", "1.1")):
            with self.subTest(base=base, proposed=proposed):
                self.assertEqual(
                    compare(document_text(base), document_text(proposed)), set()
                )
        self.assertEqual(read_version(document_text("v14.7")), "v14.7")
        self.assertEqual(compare(document_text("1.0.0"), document_text(None)), set())
        self.assertEqual(compare(document_text(None), document_text("1.0.0")), set())

    def test_a_non_stateful_document_is_compared(self) -> None:
        path = PurePosixPath("docs/03.specs/README.md")
        base, proposed = document_text("1.2.0"), document_text("1.1.0")
        self.assertEqual(read_version(base, path), "1.2.0")
        self.assertEqual(compare(base, proposed, path), {DOWNGRADE})
        self.assertEqual(compare(proposed, base, path), set())

    def test_the_skill_envelope_version_is_not_compared(self) -> None:
        path = PurePosixPath(".agents/skills/k8s-validate/SKILL.md")

        def skill(version: str) -> str:
            return (
                '---\nname: "k8s-validate"\ndescription: "x"\nmetadata:\n'
                f'  title: "x"\n  version: "{version}"\n  type: "governance/skill"\n'
                '  status: "active"\n  owner: "platform"\n  updated: "2026-11-14"\n---\n'
            )

        self.assertIsNone(read_version(skill("1.2.0"), path))
        self.assertEqual(compare(skill("1.2.0"), skill("1.1.0"), path), set())


class NumberingSeparationTests(unittest.TestCase):
    """Q-07 numbering is not a version (task file line 864)."""

    def test_a_renumbered_identity_with_an_unchanged_version_is_accepted(self) -> None:
        base = document_text("1.2.0", "SPEC-0208")
        proposed = document_text("1.2.0", "SPEC-0001")
        self.assertEqual(read_version(proposed, SPEC_PATH), "1.2.0")
        self.assertEqual(compare(base, proposed, SPEC_PATH), set())

    def test_a_renumber_that_resets_the_version_is_refused(self) -> None:
        base = document_text("1.2.0", "SPEC-0208")
        proposed = document_text("0.1.0", "SPEC-0001")
        self.assertEqual(compare(base, proposed, SPEC_PATH), {DOWNGRADE})

    def test_a_package_edition_label_is_not_a_version(self) -> None:
        self.assertFalse(GRAMMAR.is_semver("v14.7"))
        with self.assertRaises(ValueError):
            GRAMMAR.precedence("v14.7")
        for identity in ("SPEC-0208", "SPEC-0208-PLAN-0001", "REQ-0003-FR-0027"):
            with self.subTest(identity=identity):
                self.assertFalse(GRAMMAR.is_semver(identity))
        label = document_text("v14.7", "SPEC-0208")
        self.assertEqual(compare(label, label, SPEC_PATH), set())


def diagnostics(base: dict, proposed: dict) -> list:
    return list(LIFECYCLE.registry_version_diagnostics(base, proposed, base_mode=MODE))


def rules(base: dict, proposed: dict) -> set[str]:
    return {item.rule_id for item in diagnostics(base, proposed)}


def with_changes(**sections: dict) -> dict:
    raw = raw_registry()
    for name, change in sections.items():
        raw[name].update(change)
    return raw


class RegistryComparisonTests(unittest.TestCase):
    def setUp(self) -> None:
        self.current = raw_registry()

    def test_an_unchanged_registry_is_accepted(self) -> None:
        self.assertEqual(diagnostics(self.current, copy.deepcopy(self.current)), [])

    def test_a_lowered_registry_schema_version_is_refused(self) -> None:
        for value in (f"{MAJOR + 1}.0.0", f"{MAJOR}.1.0"):
            with self.subTest(value=value):
                base = {**self.current, "schema_version": value}
                found = diagnostics(base, self.current)
                self.assertEqual([item.rule_id for item in found], [DOWNGRADE])
                self.assertEqual(found[0].path, PurePosixPath(REGISTRY_PATH))

    def test_a_risen_or_integer_registry_schema_version_is_accepted(self) -> None:
        for value in (
            MAJOR - 1,
            f"{MAJOR - 1}.0.0",
            f"{MAJOR}.0.0",
            f"{MAJOR - 1}.9.9",
        ):
            with self.subTest(value=value):
                base = {**self.current, "schema_version": value}
                self.assertEqual(diagnostics(base, self.current), [])
        base = {**self.current, "schema_version": f"{MAJOR}.0.0"}
        proposed = {**self.current, "schema_version": f"{MAJOR}.1.0"}
        self.assertEqual(diagnostics(base, proposed), [])

    def test_a_schema_version_the_reader_refuses_is_not_compared(self) -> None:
        for value in ("v11.0.0", f"{MAJOR}.0.0-rc.1", 0, True, None, "x"):
            with self.subTest(value=value):
                base = {**self.current, "schema_version": value}
                self.assertEqual(diagnostics(base, self.current), [])

    def test_a_lowered_contract_version_is_refused(self) -> None:
        base = with_changes(shared_contract={"version": "3.1.0"})
        self.assertEqual(rules(base, self.current), {DOWNGRADE})

    def test_a_risen_equal_or_build_only_contract_version_is_accepted(self) -> None:
        for value in ("2.0.0", "3.0.0", "3.0.0+build.1", "3.0.0-rc.1"):
            with self.subTest(value=value):
                base = with_changes(shared_contract={"version": value})
                self.assertEqual(diagnostics(base, self.current), [])

    def test_a_changed_released_edition_is_refused(self) -> None:
        for field, value in (
            ("content_digest", OTHER_DIGEST),
            ("source_revision", "0" * 40),
            ("source", "Project-Template/other.md"),
        ):
            for stage in ("adopted", "approved"):
                with self.subTest(field=field, stage=stage):
                    base = with_changes(shared_contract={field: value, "stage": stage})
                    self.assertEqual(rules(base, self.current), {EDITION})

    def test_a_candidate_edition_may_change_under_an_unchanged_version(self) -> None:
        base = with_changes(
            shared_contract={"content_digest": OTHER_DIGEST, "stage": "candidate"}
        )
        self.assertEqual(diagnostics(base, self.current), [])

    def test_a_new_version_may_carry_new_content(self) -> None:
        base = with_changes(
            shared_contract={"content_digest": OTHER_DIGEST, "version": "2.0.0"}
        )
        self.assertEqual(diagnostics(base, self.current), [])

    def test_a_different_contract_is_not_the_same_edition(self) -> None:
        base = with_changes(
            shared_contract={"content_digest": OTHER_DIGEST, "contract_id": "X"}
        )
        self.assertEqual(diagnostics(base, self.current), [])

    def test_fields_the_comparison_does_not_read_are_not_compared(self) -> None:
        base = with_changes(shared_contract={"consumer_version": "9.0.0"})
        self.assertEqual(diagnostics(base, self.current), [])
        base = with_changes(shared_contract={"stage": "candidate"})
        self.assertEqual(diagnostics(self.current, base), [])
        self.assertEqual(diagnostics({}, self.current), [])
        self.assertEqual(diagnostics({"shared_contract": []}, self.current), [])

    def test_a_lowered_form_tree_version_is_refused(self) -> None:
        base = with_changes(common_forms={"version": "1.1.0"})
        self.assertEqual(rules(base, self.current), {DOWNGRADE})

    def test_the_form_tree_has_no_released_edition_rule(self) -> None:
        base = copy.deepcopy(self.current)
        base["common_forms"]["forms"] = base["common_forms"]["forms"][:-1]
        self.assertEqual(diagnostics(base, self.current), [])
        base = with_changes(common_forms={"version": "0.9.0"})
        self.assertEqual(diagnostics(base, self.current), [])


class ValidatorIntegrationTests(unittest.TestCase):
    """The same refusals through the validator on a scratch Git history."""

    path = ".agents/governance/cumulative-history.md"

    @classmethod
    def setUpClass(cls) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="semver-versions-seed-")
        cls.addClassCleanup(temporary.cleanup)
        cls.seed = Path(temporary.name) / "repository"
        cls.seed.mkdir()
        raw = raw_registry()
        selected = {
            "governance/rule",
            "sdlc/architecture-description",
            "sdlc/spec",
            "sdlc/plan",
        }
        for domain in raw["lifecycle_domains"]:
            selected.add(domain["profile_ids"][0])
            domain["profile_ids"] = [
                item for item in domain["profile_ids"] if item in selected
            ]
        raw.pop("readme_navigation", None)
        raw.pop("document_language", None)
        raw["profiles"] = [item for item in raw["profiles"] if item["id"] in selected]
        for profile in raw["profiles"]:
            if profile["id"] == "governance/rule":
                profile["path_pattern"] = (
                    r"^\.agents/governance/cumulative-history\.md$"
                )
        cls.registry = raw
        target = cls.seed / REGISTRY_PATH
        target.parent.mkdir(parents=True)
        target.write_text(json.dumps(raw))
        templates = {
            item["template_source"]
            for item in raw["profiles"]
            if item["template_source"] is not None
        }
        for relative in {SCHEMA_FILE.relative_to(ROOT).as_posix(), *templates}:
            destination = cls.seed / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes((ROOT / relative).read_bytes())
        git = GitFixture(cls.seed)
        git.run("add", "--", "docs/99.templates")
        git.run("commit", "--quiet", "-m", "registry")

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="semver-versions-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "repository"
        subprocess.run(
            ["git", "clone", "--quiet", str(self.seed), str(self.root)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.git = GitFixture(self.root)

    def head(self) -> str:
        return self.git.run("rev-parse", "HEAD").decode("ascii").strip()

    def document(self, version: str) -> bytes:
        sections = "".join(
            f"## {heading}\n\ncase body\n\n"
            for heading in (
                "Overview",
                "Authority Boundary",
                "Governance Context",
                "Current Contract",
                "Validation and Refresh",
                "Related Documents",
            )
        )
        return (
            f'---\ntitle: "Case"\nversion: "{version}"\ntype: "governance/rule"\n'
            f'status: "active"\nowner: "platform"\nupdated: "2026-11-14"\n---\n\n'
            f"# Case\n\n{sections}"
        ).encode()

    def judge(self, start: str) -> tuple[int, str]:
        output = io.StringIO()
        arguments = [
            "--root",
            str(self.root),
            "--mode",
            MODE,
            "--from-ref",
            start,
            "--to-ref",
            self.head(),
        ]
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = VALIDATOR.main(arguments)
        return result, output.getvalue()

    def commit_registry(self, **shared: str) -> None:
        raw = copy.deepcopy(self.registry)
        raw["shared_contract"].update(shared)
        self.git.commit(REGISTRY_PATH, json.dumps(raw).encode())

    def restore_registry(self) -> None:
        self.git.commit(REGISTRY_PATH, json.dumps(self.registry).encode())

    def test_a_document_downgrade_fails_the_validator(self) -> None:
        self.git.commit(self.path, self.document("1.1.0"))
        start = self.head()
        self.git.commit(self.path, self.document("1.0.0"))
        result, output = self.judge(start)
        self.assertNotEqual(result, 0, output)
        self.assertIn(DOWNGRADE, output)
        self.assertIn(self.path, output)

    def test_a_registry_downgrade_fails_the_validator(self) -> None:
        self.commit_registry(version="3.1.0")
        start = self.head()
        self.restore_registry()
        result, output = self.judge(start)
        self.assertNotEqual(result, 0, output)
        self.assertIn(DOWNGRADE, output)
        self.assertIn(REGISTRY_PATH, output)

    def test_a_tampered_released_edition_fails_the_validator(self) -> None:
        self.commit_registry(content_digest=OTHER_DIGEST)
        start = self.head()
        self.restore_registry()
        result, output = self.judge(start)
        self.assertNotEqual(result, 0, output)
        self.assertIn(EDITION, output)

    def test_a_staged_registry_downgrade_fails_the_validator(self) -> None:
        self.commit_registry(version="3.1.0")
        self.restore_registry_in_index()
        output = io.StringIO()
        arguments = ["--root", str(self.root), "--mode", "staged"]
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = VALIDATOR.main(arguments)
        self.assertNotEqual(result, 0, output.getvalue())
        self.assertIn(DOWNGRADE, output.getvalue())

    def restore_registry_in_index(self) -> None:
        (self.root / REGISTRY_PATH).write_text(json.dumps(self.registry))
        self.git.run("add", "--", REGISTRY_PATH)

    def test_no_new_option_is_added(self) -> None:
        text = (ROOT / "scripts/validate-document-lifecycle.py").read_text()
        self.assertEqual(
            sorted(set(re.findall(r'add_argument\(\s*"(--[a-z-]+)"', text))),
            [
                "--base-ref",
                "--from-ref",
                "--include-path",
                "--mode",
                "--root",
                "--to-ref",
            ],
        )


def registry_with(value: str) -> dict:
    raw = raw_registry()
    raw["schema_version"] = value
    return raw


def schema_with(value: str) -> dict:
    schema = raw_schema()
    schema["properties"]["schema_version"] = {"const": value}
    return schema


def registry_loads(major: int, value: str, raw: dict | None = None) -> bool:
    """Whether the strict registry loader of the given MAJOR number accepts a registry."""
    raw = registry_with(value) if raw is None else raw
    templates = frozenset(
        PurePosixPath(item["template_source"])
        for item in raw["profiles"]
        if item.get("template_source")
    )
    with mock.patch.object(CONTRACTS, "REGISTRY_MAJOR", major):
        try:
            CONTRACTS.load_internal_payload(
                ROOT,
                raw_registry=raw,
                raw_schema=schema_with(value),
                template_regular_paths=templates,
            )
        except CONTRACTS.DocumentContractError:
            return False
    return True


def dotted(parts: tuple[int, int, int]) -> str:
    return ".".join(map(str, parts))


# Copied from the increment classes of the v14.7 case file, as SPEC-0190 copied
# its cases. Row: class, what the class names, old edition, new edition, the MAJOR
# number the old consumer implements, the MAJOR number the new consumer implements.
MATRIX = (
    ("NO_CHANGE", "an unchanged object", (MAJOR, 0, 0), (MAJOR, 0, 0), MAJOR, MAJOR),
    ("PATCH", "a correct refusal of an already invalid input", (MAJOR, 0, 0), (MAJOR, 0, 1), MAJOR, MAJOR),
    ("MINOR", "an optional feature that valid inputs still satisfy", (MAJOR, 0, 0), (MAJOR, 1, 0), MAJOR, MAJOR),
    ("MAJOR", "a renamed required heading", (MAJOR - 1, 0, 0), (MAJOR, 0, 0), MAJOR - 1, MAJOR),
)  # fmt: skip
ALL_PAIRS = {("old", "old"), ("old", "new"), ("new", "old"), ("new", "new")}
ACCEPTED = {"MAJOR": {("old", "old"), ("new", "new")}}


class RegistryMatrixTests(unittest.TestCase):
    """Old and new producer against old and new consumer on the three readers."""

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="semver-matrix-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "repository"
        self.root.mkdir()
        self.git = GitFixture(self.root)
        self.current = CONTRACTS.load_registry(ROOT)
        self.commits = 0

    def loader(self, major: int, value: str, raw: dict | None = None) -> bool:
        return registry_loads(major, value, raw)

    def guard(self, major: int, value: str) -> bool:
        payload = {
            "schema_version": value,
            "profiles": [
                {
                    "id": "sdlc/requirement",
                    "path_pattern": r"^docs/01\.requirements/[a-z-]+\.md$",
                    "template_source": None,
                }
            ],
        }
        with tempfile.TemporaryDirectory(prefix="semver-guard-") as directory:
            root = Path(directory)
            (root / "docs/99.templates").mkdir(parents=True)
            (root / REGISTRY_PATH).write_text(json.dumps(payload), encoding="utf-8")
            with mock.patch.object(GUARD, "DOC_REGISTRY_MAJOR", major):
                with contextlib.redirect_stderr(io.StringIO()):
                    try:
                        GUARD.load_document_routes(str(root))
                    except SystemExit:
                        return False
        return True

    def history(self, major: int, value: str) -> bool:
        raw = raw_registry()
        raw["profiles"] = raw["profiles"][:-1]
        raw["schema_version"] = value
        self.commits += 1
        raw["case"] = self.commits  # a distinct blob, so each commit is non-empty
        commit, _ = self.git.commit(REGISTRY_PATH, json.dumps(raw).encode())
        with mock.patch.object(VALIDATOR, "READABLE_REGISTRY_MAJORS", (major,)):
            cache = VALIDATOR._CumulativeHistoryCache(self.root, self.current)
            return cache.registry_at(commit) is not self.current

    def test_each_row_is_the_class_its_values_show(self) -> None:
        for name, _, old, new, *_ in MATRIX:
            with self.subTest(name=name):
                self.assertEqual(level(dotted(old), dotted(new)), name)

    def test_the_four_pairs_follow_the_class_on_every_reader(self) -> None:
        for name, meaning, old, new, old_major, new_major in MATRIX:
            produced = {"old": dotted(old), "new": dotted(new)}
            consumed = {"old": old_major, "new": new_major}
            for reader in (self.loader, self.guard, self.history):
                for producer, consumer in sorted(ALL_PAIRS):
                    with self.subTest(
                        change=name, reader=reader.__name__, pair=(producer, consumer)
                    ):
                        expected = (producer, consumer) in ACCEPTED.get(name, ALL_PAIRS)
                        self.assertEqual(
                            reader(consumed[consumer], produced[producer]),
                            expected,
                            meaning,
                        )

    def test_an_added_key_a_strict_parser_rejects_is_major_not_minor(self) -> None:
        raw = raw_registry()
        raw["optional_feature"] = {}
        value = f"{MAJOR}.0.0"
        self.assertTrue(self.loader(MAJOR, value))
        # The strict registry schema of the earlier consumer refuses the key.
        refused = not self.loader(MAJOR, value, raw)
        self.assertTrue(refused)
        required = "MAJOR" if refused else "MINOR"
        self.assertEqual(level(f"{MAJOR - 1}.0.0", f"{MAJOR}.0.0"), required)
        self.assertNotEqual(level(f"{MAJOR}.0.0", f"{MAJOR}.1.0"), required)


class DocumentMatrixTests(unittest.TestCase):
    """DOC-REV: the consumers that existed before and the comparison added here."""

    ROWS = (
        ("NO_CHANGE", "1.2.0", "1.2.0"),
        ("PATCH", "1.2.0", "1.2.1"),
        ("MINOR", "1.2.0", "1.3.0"),
        ("MAJOR", "1.2.0", "2.0.0"),
    )

    @classmethod
    def setUpClass(cls) -> None:
        schema = json.loads(FRONTMATTER_SCHEMA.read_text(encoding="utf-8"))
        cls.pattern = re.compile(schema["properties"]["version"]["pattern"])

    def old_consumer(self, value: str) -> bool:
        return self.pattern.fullmatch(value) is not None

    def new_consumer(self, base: str, proposed: str) -> bool:
        return compare(document_text(base), document_text(proposed)) == set()

    def test_the_four_pairs_accept_every_class(self) -> None:
        for name, old, new in self.ROWS:
            with self.subTest(change=name):
                self.assertEqual(level(old, new), name)
                self.assertTrue(self.old_consumer(old))  # old producer, old consumer
                self.assertTrue(self.old_consumer(new))  # new producer, old consumer
                self.assertTrue(
                    self.new_consumer(old, old)
                )  # old producer, new consumer
                self.assertTrue(
                    self.new_consumer(old, new)
                )  # new producer, new consumer

    def test_the_crossed_refusals(self) -> None:
        for value in ("1.2", "v1.2.0", "01.2.0", "1.2.0-"):
            with self.subTest(value=value):
                self.assertFalse(self.old_consumer(value))
        for name, old, new in self.ROWS:
            if name != "NO_CHANGE":
                with self.subTest(change=name):
                    self.assertFalse(self.new_consumer(new, old))


class MissingVersionTests(unittest.TestCase):
    """A missing version is refused by the existing checks (regression, not new)."""

    def test_a_document_without_a_version_fails_the_strict_profile_check(self) -> None:
        path = RULE_PATH
        profile = next(
            item
            for item in REGISTRY.profiles
            if item.profile_id == CONTRACTS.classify_path(REGISTRY, path).profile_id
        )

        def rules(text: str) -> set[str]:
            found = PROFILES.validate_document_text(
                text,
                path,
                profile,
                "strict",
                today=dt.date(2026, 11, 14),
                include_body=False,
            )
            return {item.rule_id for item in found if item.rule_id.startswith("FM-")}

        self.assertEqual(rules(document_text("1.0.0")), set())
        self.assertEqual(rules(document_text(None)), {"FM-KEYSET"})

    def test_a_contract_without_a_version_fails_the_registry_schema(self) -> None:
        value = f"{MAJOR}.0.0"
        raw = raw_registry()
        self.assertTrue(registry_loads(MAJOR, value, raw))
        del raw["shared_contract"]["version"]
        self.assertFalse(registry_loads(MAJOR, value, raw))
        raw = raw_registry()
        del raw["common_forms"]["version"]
        self.assertFalse(registry_loads(MAJOR, value, raw))

    def test_a_tag_without_a_version_is_invalid(self) -> None:
        for value in ("", "v", "v.."):
            with (
                self.subTest(value=value),
                self.assertRaises(release.ReleaseError) as c,
            ):
                release.parse_version(value)
            self.assertEqual(c.exception.code, "RELEASE-VERSION-INVALID")


if __name__ == "__main__":
    unittest.main()
