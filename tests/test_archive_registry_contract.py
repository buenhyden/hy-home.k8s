#!/usr/bin/env python3
"""ADR-0039 Stage 98 registry contract: units, modes, citation table, legacy set."""

from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import archive_dispositions as dispositions  # noqa: E402
from document_contracts import (  # noqa: E402
    DocumentContractError,
    load_registry,
    validate_registry,
)


RAW = json.loads((ROOT / "docs/99.templates/registry.json").read_text(encoding="utf-8"))
REGISTRY = load_registry(ROOT)
RETENTION_CLASSES = frozenset({"completed", "superseded", "retired", "resolved"})


def rule_ids(raw: dict) -> set[str]:
    try:
        validate_registry(ROOT, raw)
    except DocumentContractError as error:
        return {item.rule_id for item in error.diagnostics}
    return set()


def mode_entry(raw: dict, name: str) -> dict:
    return next(item for item in raw["retention_modes"] if item["mode"] == name)


class RetentionUnitTests(unittest.TestCase):
    def units(self):
        return {unit.name: unit for unit in REGISTRY.retention_units}

    def test_registry_declares_package_and_incident_units(self) -> None:
        units = self.units()
        self.assertEqual(set(units), {"spec-package", "incident-bundle"})
        self.assertEqual(units["spec-package"].anchor, "spec.md")
        self.assertEqual(units["spec-package"].required_members, ("spec.md",))
        self.assertEqual(units["incident-bundle"].anchor, "incident.md")
        self.assertEqual(
            units["incident-bundle"].required_members,
            ("incident.md", "postmortem.md"),
        )
        self.assertEqual(
            dict(units["incident-bundle"].member_admitted_states),
            {"postmortem.md": frozenset({"published"})},
        )

    def test_unit_root_matches_only_its_stage_directory(self) -> None:
        units = self.units()
        package = units["spec-package"].root
        self.assertIsNotNone(
            package.fullmatch("docs/03.specs/0082-unit-archive-retention-contract")
        )
        self.assertIsNone(package.fullmatch("docs/03.specs/0082-x/tasks"))
        self.assertIsNone(package.fullmatch("docs/05.operations/incidents"))
        self.assertIsNotNone(
            units["incident-bundle"].root.fullmatch(
                "docs/05.operations/incidents/2026/inc-0001-disk-full"
            )
        )

    def test_duplicate_or_undeclared_unit_fields_are_rejected(self) -> None:
        duplicate = copy.deepcopy(RAW)
        duplicate["retention_units"].append(
            copy.deepcopy(duplicate["retention_units"][0])
        )
        self.assertIn("REGISTRY_RETENTION_UNIT", rule_ids(duplicate))
        extra = copy.deepcopy(RAW)
        extra["retention_units"][0]["digest"] = "a" * 64
        self.assertTrue(rule_ids(extra))

    def test_member_state_must_be_declared_by_a_lifecycle_domain(self) -> None:
        raw = copy.deepcopy(RAW)
        unit = next(
            item for item in raw["retention_units"] if item["unit"] == "incident-bundle"
        )
        unit["member_admitted_states"]["postmortem.md"] = ["reviewed"]
        self.assertIn("REGISTRY_RETENTION_UNIT", rule_ids(raw))


class RetentionClassTests(unittest.TestCase):
    def test_each_class_admits_only_its_anchor_states(self) -> None:
        classes = dispositions.retention_classes_by_name(REGISTRY)
        self.assertEqual(
            {name: item.admitted_states for name, item in classes.items()},
            {
                "completed": frozenset({"done"}),
                "superseded": frozenset({"superseded"}),
                "retired": frozenset(
                    {"withdrawn", "retired", "rejected", "invalidated"}
                ),
                "resolved": frozenset({"closed"}),
            },
        )


class RetentionModeTests(unittest.TestCase):
    def test_four_modes_are_declared(self) -> None:
        self.assertEqual(
            {mode.name for mode in REGISTRY.retention_modes},
            {
                "move-frozen-body",
                "sealed-record",
                "retain-in-place",
                "git-history-only",
            },
        )

    def test_each_profile_binds_to_at_most_the_mode_it_may_use(self) -> None:
        for profile_id, expected in (
            ("sdlc/spec", "move-frozen-body"),
            ("sdlc/architecture-decision", "move-frozen-body"),
            ("operation/incident", "move-frozen-body"),
            ("reference/research", "move-frozen-body"),
            ("archive/tombstone", "sealed-record"),
            ("archive/migration", "sealed-record"),
            ("common/readme-stage-index", "retain-in-place"),
            ("common/template-sdlc-spec", "git-history-only"),
        ):
            with self.subTest(profile=profile_id):
                mode = dispositions.retention_mode_of(REGISTRY, profile_id)
                assert mode is not None
                self.assertEqual(mode.name, expected)
        for profile_id in (
            "governance/rule",
            "archive/route-tombstone",
            "archive/scope-migration",
            "common/readme-research-pack",
        ):
            with self.subTest(profile=profile_id):
                self.assertIsNone(dispositions.retention_mode_of(REGISTRY, profile_id))

    def test_only_moving_a_frozen_body_admits_retention_classes(self) -> None:
        modes = {mode.name: mode for mode in REGISTRY.retention_modes}
        self.assertEqual(modes["move-frozen-body"].classes, RETENTION_CLASSES)
        for name in ("sealed-record", "retain-in-place", "git-history-only"):
            with self.subTest(mode=name):
                self.assertEqual(modes[name].classes, frozenset())

    def test_overlapping_selectors_are_rejected(self) -> None:
        overlap = copy.deepcopy(RAW)
        mode_entry(overlap, "retain-in-place")["profile_id_pattern"] = "^common/"
        self.assertIn("REGISTRY_RETENTION_MODE", rule_ids(overlap))

    def test_a_mode_that_binds_nothing_is_declared_but_cannot_be_applied(self) -> None:
        raw = copy.deepcopy(RAW)
        mode_entry(raw, "git-history-only")["profile_id_pattern"] = "^nothing/"
        self.assertEqual(rule_ids(raw), set())
        registry = validate_registry(ROOT, raw)
        self.assertIsNone(
            dispositions.retention_mode_of(registry, "common/template-sdlc-spec")
        )

    def test_a_moved_body_profile_needs_a_stage98_mirror(self) -> None:
        raw = copy.deepcopy(RAW)
        mode_entry(raw, "move-frozen-body")["profile_id_pattern"] = (
            "^(sdlc|operation|reference|governance)/"
        )
        self.assertIn("REGISTRY_RETENTION_MODE", rule_ids(raw))


class CitationTableTests(unittest.TestCase):
    def test_rules_are_ordered_and_default_to_rejection(self) -> None:
        table = REGISTRY.archive_citation
        self.assertEqual(table.index, PurePosixPath("docs/98.archive/README.md"))
        self.assertEqual(table.default, "reject")
        self.assertEqual(
            [(rule.source, rule.target, rule.decision) for rule in table.rules],
            [
                ("archive", "any", "admit"),
                ("any", "index", "admit"),
                ("any", "retained-body", "reject"),
                ("any", "retained-body", "reject"),
                ("any", "route-record", "reject"),
                ("any", "sealed-record", "reject"),
                ("profiles", "retained-body", "admit"),
                ("any", "retained-body", "admit"),
            ],
        )
        # ADR-0040: availability and judgment decide before any class admission.
        self.assertEqual(
            table.rules[2].target_assessments,
            frozenset({"withdrawn", "invalidated"}),
        )
        self.assertEqual(
            table.rules[3].target_availabilities,
            frozenset({"git-history-only", "purged"}),
        )
        self.assertEqual(table.rules[2].target_classes, RETENTION_CLASSES)
        self.assertEqual(table.rules[3].target_classes, RETENTION_CLASSES)
        self.assertEqual(
            table.rules[6].source_profile_ids,
            frozenset({"operation/incident", "operation/postmortem"}),
        )
        self.assertEqual(table.rules[6].target_classes, RETENTION_CLASSES)
        self.assertEqual(
            table.rules[7].target_classes, frozenset({"completed", "resolved"})
        )

    def test_rule_naming_an_unknown_profile_or_class_is_rejected(self) -> None:
        profile = copy.deepcopy(RAW)
        profile["archive_citation"]["rules"][6]["source_profile_ids"].append(
            "operation/forgotten"
        )
        self.assertIn("REGISTRY_ARCHIVE_CITATION", rule_ids(profile))
        retention = copy.deepcopy(RAW)
        retention["archive_citation"]["rules"][7]["target_classes"].append("forgotten")
        self.assertTrue(rule_ids(retention))


class LegacyRetainedSetTests(unittest.TestCase):
    def test_legacy_set_is_sixteen_catalog_rows(self) -> None:
        rows, errors = dispositions.parse_catalog(
            (ROOT / "docs/98.archive/README.md").read_text(encoding="utf-8")
        )
        self.assertEqual(errors, ())
        legacy = REGISTRY.legacy_rebased_retained_paths
        self.assertEqual(len(legacy), 16)
        self.assertLessEqual(legacy, frozenset(rows))

    def test_legacy_path_must_be_a_retained_body(self) -> None:
        raw = copy.deepcopy(RAW)
        raw["legacy_rebased_retained_paths"][0] = (
            "docs/02.architecture/decisions/0039-unit-archive-retention-and-citation-table.md"
        )
        self.assertIn("REGISTRY_LEGACY_RETAINED", rule_ids(raw))

    def test_legacy_set_cannot_grow(self) -> None:
        raw = copy.deepcopy(RAW)
        raw["legacy_rebased_retained_paths"].append(
            "docs/98.archive/completed/03.specs/0052-document-taxonomy-consolidation/spec.md"
        )
        self.assertTrue(rule_ids(raw))


class FastGateTests(unittest.TestCase):
    """The archive contract regressions run in the fast local lanes."""

    def validation_registry(self) -> dict:
        return json.loads(
            (ROOT / "scripts/validation/registry.json").read_text(encoding="utf-8")
        )

    def test_archive_contract_tests_run_in_quick_and_staged(self) -> None:
        registry = self.validation_registry()
        gate = next(
            (
                item
                for item in registry["validators"]
                if item["id"] == "archive-contract-tests"
            ),
            None,
        )
        self.assertIsNotNone(gate)
        assert gate is not None
        self.assertIn("staged", gate["lanes"])
        self.assertIn("affected", gate["lanes"])
        for profile in ("quick", "staged"):
            with self.subTest(profile=profile):
                self.assertIn("archive-contract-tests", registry["profiles"][profile])
        # In full the unit discovery already runs these modules once.
        self.assertEqual(gate.get("coveredBy"), "unit-tests")
        self.assertIn("unit-tests", registry["profiles"]["full"])
        self.assertNotIn("archive-contract-tests", registry["profiles"]["full"])
        surfaces = {item["id"]: item["validators"] for item in registry["surfaces"]}
        for surface in ("scripts", "tests", "template-documents"):
            with self.subTest(surface=surface):
                self.assertIn("archive-contract-tests", surfaces[surface])

    def test_the_gate_runs_one_script_that_names_every_regression(self) -> None:
        """The contract identifies a gate by its script, never by a `-m` module."""

        gate = next(
            item
            for item in self.validation_registry()["validators"]
            if item["id"] == "archive-contract-tests"
        )
        self.assertEqual(gate["argv"][0], "python3")
        runner = gate["argv"][1]
        self.assertFalse(runner.startswith("-"))
        self.assertTrue(runner.startswith("scripts/") and runner.endswith(".py"))
        source = (ROOT / runner).read_text(encoding="utf-8")
        modules = re.findall(r'"(tests\.[a-z0-9_]+)"', source)
        self.assertTrue(modules)
        for module in modules:
            with self.subTest(module=module):
                self.assertTrue((ROOT / (module.replace(".", "/") + ".py")).is_file())


if __name__ == "__main__":  # pragma: no cover - module entry guard
    unittest.main()
