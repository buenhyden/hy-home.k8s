"""SPEC-0207: the Registry Schema Version is a SemVer string read by its MAJOR number.

No test here holds a version literal for the current registry: every value
derives from `REGISTRY_MAJOR` and `READABLE_REGISTRY_MAJORS`, so a later MAJOR
step edits the constants and no test. The integers 1 to 10 are the one fixed
fact, the mapping of the earlier generations (REQ:890).
"""

from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_authority as AUTHORITY  # noqa: E402
import document_contracts as CONTRACTS  # noqa: E402
from semver_grammar import SEMVER_PATTERN  # noqa: E402
from tests.git_fixture import GitFixture  # noqa: E402

REGISTRY_FILE = ROOT / "docs/99.templates/registry.json"
SCHEMA_FILE = ROOT / "docs/99.templates/contracts/document-profile.schema.json"
LAST_INTEGER_GENERATION = 10


def _load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


VALIDATOR = _load_script(
    "registry_schema_version_lifecycle", "validate-document-lifecycle.py"
)
GUARD = _load_script("registry_schema_version_guard", "provider_write_guard.py")


def raw_registry() -> dict:
    return json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))


def raw_schema() -> dict:
    return json.loads(SCHEMA_FILE.read_text(encoding="utf-8"))


def current_value() -> str:
    return f"{AUTHORITY.REGISTRY_MAJOR}.0.0"


def previous_value() -> str:
    return f"{AUTHORITY.REGISTRY_MAJOR - 1}.0.0"


def next_value() -> str:
    return f"{AUTHORITY.REGISTRY_MAJOR + 1}.0.0"


def release_groups(value: object) -> tuple[str, ...] | None:
    """The release triple of a value the repository grammar accepts, else None."""
    if type(value) is not str:
        return None
    match = re.fullmatch(SEMVER_PATTERN, value)
    if match is None or match.group(4) is not None or match.group(5) is not None:
        return None
    return match.groups()[:3]


def load_diagnostics(raw: dict, schema: dict | None = None) -> list:
    templates = frozenset(
        PurePosixPath(profile["template_source"])
        for profile in raw["profiles"]
        if profile.get("template_source")
    )
    try:
        CONTRACTS.load_internal_payload(
            ROOT,
            raw_registry=raw,
            raw_schema=raw_schema() if schema is None else schema,
            template_regular_paths=templates,
        )
    except CONTRACTS.DocumentContractError as error:
        return list(error.diagnostics)
    return []


def rules_of_load(raw: dict, schema: dict | None = None) -> set[str]:
    return {item.rule_id for item in load_diagnostics(raw, schema)}


class RegistryValueTests(unittest.TestCase):
    def test_registry_carries_a_semver_string_of_the_implemented_major(self) -> None:
        value = raw_registry()["schema_version"]
        groups = release_groups(value)
        self.assertIsNotNone(groups, value)
        self.assertEqual(int(groups[0]), AUTHORITY.REGISTRY_MAJOR)

    def test_schema_const_equals_the_registry_value(self) -> None:
        self.assertEqual(
            raw_schema()["properties"]["schema_version"],
            {"const": raw_registry()["schema_version"]},
        )

    def test_readable_majors_include_the_implemented_major(self) -> None:
        majors = AUTHORITY.READABLE_REGISTRY_MAJORS
        self.assertIn(AUTHORITY.REGISTRY_MAJOR, majors)
        self.assertEqual(majors, tuple(sorted(set(majors))))
        self.assertTrue(all(type(major) is int for major in majors))

    def test_registry_dataclass_carries_the_string(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        self.assertEqual(registry.schema_version, raw_registry()["schema_version"])


class ReaderFunctionTests(unittest.TestCase):
    def test_each_integer_generation_maps_to_n_zero_zero(self) -> None:
        for generation in range(1, LAST_INTEGER_GENERATION + 1):
            with self.subTest(generation=generation):
                self.assertEqual(
                    CONTRACTS.registry_schema_version({"schema_version": generation}),
                    f"{generation}.0.0",
                )

    def test_generation_ten_does_not_map_to_one_zero_zero(self) -> None:
        mapped = CONTRACTS.registry_schema_version(
            {"schema_version": LAST_INTEGER_GENERATION}
        )
        self.assertEqual(mapped, f"{LAST_INTEGER_GENERATION}.0.0")
        self.assertNotEqual(mapped, "1.0.0")
        self.assertEqual(
            CONTRACTS.registry_schema_version({"schema_version": 1}), "1.0.0"
        )

    def test_a_grammar_string_is_returned_as_is(self) -> None:
        for value in (current_value(), f"{AUTHORITY.REGISTRY_MAJOR}.4.7", next_value()):
            with self.subTest(value=value):
                self.assertEqual(
                    CONTRACTS.registry_schema_version({"schema_version": value}),
                    value,
                )

    def test_values_outside_the_contract_are_refused(self) -> None:
        major = AUTHORITY.REGISTRY_MAJOR
        refused = (
            True,
            False,
            0,
            -1,
            LAST_INTEGER_GENERATION + 1,
            major,
            None,
            1.0,
            [],
            "",
            f"{major}",
            f"v{major}.0.0",
            f"{major}.0",
            f"{major}.0.0-rc.1",
            f"{major}.0.0+build.1",
            f"0{major}.0.0",
            f" {major}.0.0",
            f"{major}.0.0\n",
        )
        for value in refused:
            with self.subTest(value=value):
                with self.assertRaises(CONTRACTS.DocumentContractError) as caught:
                    CONTRACTS.registry_schema_version({"schema_version": value})
                self.assertEqual(
                    {item.rule_id for item in caught.exception.diagnostics},
                    {"REGISTRY_SCHEMA"},
                )

    def test_a_missing_key_and_the_old_spelling_are_refused(self) -> None:
        for raw in ({}, {"schemaVersion": 8}):
            with self.subTest(raw=raw):
                with self.assertRaises(CONTRACTS.DocumentContractError):
                    CONTRACTS.registry_schema_version(raw)


class LoaderTests(unittest.TestCase):
    def test_the_repository_registry_loads_through_supplied_inputs(self) -> None:
        self.assertEqual(rules_of_load(raw_registry()), set())

    def test_an_integer_is_refused_with_a_message_that_names_the_mapping(self) -> None:
        previous = AUTHORITY.REGISTRY_MAJOR - 1
        raw = raw_registry()
        raw["schema_version"] = previous
        diagnostics = load_diagnostics(raw)
        self.assertEqual({item.rule_id for item in diagnostics}, {"REGISTRY_SCHEMA"})
        self.assertIn(
            f"{previous}.0.0",
            " ".join(f"{item.expected} {item.actual}" for item in diagnostics),
        )

    def test_another_major_number_is_refused(self) -> None:
        for value in (previous_value(), next_value()):
            with self.subTest(value=value):
                raw = raw_registry()
                raw["schema_version"] = value
                self.assertEqual(rules_of_load(raw), {"REGISTRY_SCHEMA"})

    def test_malformed_strings_are_refused(self) -> None:
        major = AUTHORITY.REGISTRY_MAJOR
        for value in (
            f"{major}",
            f"v{major}.0.0",
            f"{major}.0",
            f"{major}.0.0-rc.1",
        ):
            with self.subTest(value=value):
                raw = raw_registry()
                raw["schema_version"] = value
                self.assertEqual(rules_of_load(raw), {"REGISTRY_SCHEMA"})

    def test_the_strict_schema_pins_the_exact_current_value(self) -> None:
        raw = raw_registry()
        raw["schema_version"] = f"{AUTHORITY.REGISTRY_MAJOR}.1.0"
        self.assertNotEqual(rules_of_load(raw), set())
        schema = raw_schema()
        schema["properties"]["schema_version"] = {"const": raw["schema_version"]}
        self.assertEqual(rules_of_load(raw, schema), set())


class HistoryReaderTests(unittest.TestCase):
    """`registry_at` reads each readable MAJOR with its own typed reading."""

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="registry-version-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repository"
        self.root.mkdir()
        self.git = GitFixture(self.root)
        self.current = CONTRACTS.load_registry(ROOT)

    def own_blob(self, mutate) -> dict:
        """A registry that differs from the current one by a dropped profile."""
        raw = copy.deepcopy(raw_registry())
        raw["profiles"] = raw["profiles"][:-1]
        mutate(raw)
        return raw

    def commit_registry(self, raw: dict) -> str:
        commit, _ = self.git.commit(
            "docs/99.templates/registry.json", json.dumps(raw).encode()
        )
        return commit

    def registry_at(self, commit: str):
        cache = VALIDATOR._CumulativeHistoryCache(self.root, self.current)
        return cache.registry_at(commit)

    def profile_ids(self, raw: dict) -> tuple[str, ...]:
        return tuple(profile["id"] for profile in raw["profiles"])

    def test_an_integer_generation_ten_blob_yields_its_own_profiles(self) -> None:
        raw = self.own_blob(
            lambda value: value.update(schema_version=LAST_INTEGER_GENERATION)
        )
        result = self.registry_at(self.commit_registry(raw))
        self.assertIsNot(result, self.current)
        own = tuple(profile.profile_id for profile in result.profiles)
        self.assertEqual(own, self.profile_ids(raw))
        self.assertNotEqual(
            own, tuple(profile.profile_id for profile in self.current.profiles)
        )
        self.assertEqual(result.schema_version, f"{LAST_INTEGER_GENERATION}.0.0")

    def test_every_readable_major_is_read_as_itself(self) -> None:
        for major in AUTHORITY.READABLE_REGISTRY_MAJORS:
            with self.subTest(major=major):
                raw = self.own_blob(
                    lambda value, major=major: value.update(
                        schema_version=f"{major}.0.0"
                    )
                )
                result = self.registry_at(self.commit_registry(raw))
                self.assertIsNot(result, self.current)
                self.assertEqual(
                    tuple(profile.profile_id for profile in result.profiles),
                    self.profile_ids(raw),
                )
                self.assertEqual(result.schema_version, f"{major}.0.0")

    def test_a_blob_of_an_unreadable_major_falls_back_to_the_current_registry(
        self,
    ) -> None:
        unreadable = (
            min(AUTHORITY.READABLE_REGISTRY_MAJORS) - 1,
            f"{min(AUTHORITY.READABLE_REGISTRY_MAJORS) - 1}.0.0",
            f"{max(AUTHORITY.READABLE_REGISTRY_MAJORS) + 1}.0.0",
        )
        for value in unreadable:
            with self.subTest(value=value):
                raw = self.own_blob(
                    lambda item, value=value: item.update(schema_version=value)
                )
                self.assertIs(self.registry_at(self.commit_registry(raw)), self.current)

    def test_the_old_spelling_and_malformed_values_fall_back(self) -> None:
        def old_spelling(raw: dict) -> None:
            raw["schemaVersion"] = raw.pop("schema_version")

        cases = {"spelling": old_spelling}
        for label, value in {
            "text": "ten",
            "boolean": True,
            "zero": 0,
            "above-mapping": LAST_INTEGER_GENERATION + 1,
            "prerelease": f"{AUTHORITY.REGISTRY_MAJOR}.0.0-rc.1",
            "null": None,
        }.items():
            cases[label] = lambda raw, value=value: raw.update(schema_version=value)
        for label, mutate in cases.items():
            with self.subTest(case=label):
                raw = self.own_blob(mutate)
                self.assertIs(self.registry_at(self.commit_registry(raw)), self.current)

    def test_a_commit_without_a_registry_falls_back(self) -> None:
        commit, _ = self.git.commit("note.txt", b"no registry\n")
        self.assertIs(self.registry_at(commit), self.current)


class GuardTests(unittest.TestCase):
    """The write guard runs from the checkout with the standard library only."""

    def routes_for(self, value: object) -> object:
        with tempfile.TemporaryDirectory(prefix="registry-guard-") as directory:
            root = Path(directory)
            (root / "docs/99.templates").mkdir(parents=True)
            (root / "docs/99.templates/registry.json").write_text(
                json.dumps(
                    {
                        "schema_version": value,
                        "profiles": [
                            {
                                "id": "sdlc/requirement",
                                "path_pattern": r"^docs/01\.requirements/[a-z-]+\.md$",
                                "template_source": None,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            return GUARD.load_document_routes(str(root))

    def test_one_major_number_is_shared_by_the_guard_the_code_and_the_files(
        self,
    ) -> None:
        schema_value = raw_schema()["properties"]["schema_version"]["const"]
        registry_value = raw_registry()["schema_version"]
        self.assertEqual(schema_value, registry_value)
        self.assertEqual(
            {
                GUARD.DOC_REGISTRY_MAJOR,
                AUTHORITY.REGISTRY_MAJOR,
                int(release_groups(schema_value)[0]),
                int(release_groups(registry_value)[0]),
            },
            {AUTHORITY.REGISTRY_MAJOR},
        )

    def test_the_guard_accepts_the_current_value_and_a_minor_step(self) -> None:
        for value in (current_value(), f"{AUTHORITY.REGISTRY_MAJOR}.3.0"):
            with self.subTest(value=value):
                routes = self.routes_for(value)
                self.assertEqual(
                    [route["id"] for route in routes], ["sdlc/requirement"]
                )

    def test_the_guard_refuses_every_other_value(self) -> None:
        major = AUTHORITY.REGISTRY_MAJOR
        for value in (
            major - 1,
            major,
            previous_value(),
            next_value(),
            f"{major}",
            f"v{major}.0.0",
            f"{major}.0.0-rc.1",
            True,
            None,
        ):
            with self.subTest(value=value):
                with self.assertRaises(SystemExit) as caught:
                    self.routes_for(value)
                self.assertEqual(caught.exception.code, 2)

    def test_the_guard_grammar_matches_the_repository_grammar_over_a_corpus(
        self,
    ) -> None:
        major = AUTHORITY.REGISTRY_MAJOR
        corpus = (
            f"{major}.0.0",
            f"{major}.1.2",
            "0.0.0",
            "1.0.0",
            f"{major}.0.0-rc.1",
            f"{major}.0.0-alpha",
            f"{major}.0.0+build.5",
            f"{major}.0.0-rc.1+build.5",
            f"0{major}.0.0",
            f"{major}.00.0",
            f"{major}.0.00",
            f"{major}",
            f"{major}.0",
            f"{major}.0.0.0",
            f"v{major}.0.0",
            f" {major}.0.0",
            f"{major}.0.0 ",
            f"{major}.0.0\n",
            "",
            "a.b.c",
            True,
            False,
            None,
            major,
            1.5,
            [],
        )
        for value in corpus:
            with self.subTest(value=value):
                expected = release_groups(value)
                observed = GUARD.registry_version_major(value)
                self.assertEqual(
                    observed, None if expected is None else int(expected[0])
                )


if __name__ == "__main__":
    unittest.main()
