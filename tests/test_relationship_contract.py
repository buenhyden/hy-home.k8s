"""SPEC-0193: the relationship contract, its registry rules and the supersession walk."""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import document_authority as AUTHORITY  # noqa: E402
import document_contracts as CONTRACTS  # noqa: E402
from document_lifecycle import (  # noqa: E402
    LifecycleDocument,
    LifecycleEvidenceContext,
    LifecycleEvidenceDocument,
    compare_lifecycle,
    supersession_cycle_diagnostics,
)

REGISTRY_FILE = ROOT / "docs/99.templates/registry.json"
KINDS = (
    "authority",
    "structural-ownership",
    "constraint",
    "traceability",
    "promotion",
    "supersession",
    "change-impact",
)
RELATIONS = (
    "parent",
    "requirement-basis",
    "design-constraint",
    "promotion",
    "supersession",
    "verification-evidence",
    "policy-authority",
    "consumer-impact",
)
LINK_TYPES = ("normative", "evidence", "historical", "navigation")


def _load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MARKDOWN = _load_script("relationship_markdown", "validate-markdown-profiles.py")


def raw_registry() -> dict:
    return json.loads(REGISTRY_FILE.read_text("utf-8"))


def contract_rules(raw: dict) -> set[str]:
    return {
        item.rule_id
        for item in CONTRACTS.current_registry_diagnostics(ROOT, raw)
        if item.rule_id.startswith("REGISTRY_RELATION")
    }


def relation(raw: dict, relation_id: str) -> dict:
    return next(
        item
        for item in raw["relationship_contract"]["relations"]
        if item["id"] == relation_id
    )


class RelationshipRegistryTests(unittest.TestCase):
    def test_the_repository_registry_holds_the_contract(self) -> None:
        raw = raw_registry()
        contract = raw["relationship_contract"]
        self.assertEqual(
            [item["id"] for item in contract["relation_kinds"]], list(KINDS)
        )
        self.assertEqual(
            [item["id"] for item in contract["relations"]], list(RELATIONS)
        )
        self.assertEqual(
            [item["id"] for item in contract["link_types"]], list(LINK_TYPES)
        )
        self.assertEqual(contract_rules(raw), set())
        direction = {
            item["id"]: item["direction"] for item in contract["relation_kinds"]
        }
        for item in contract["relations"]:
            with self.subTest(relation=item["id"]):
                self.assertIn(
                    item["direction"], {"source_to_target", "owner_to_consumer"}
                )
                self.assertEqual(item["direction"], direction[item["kind"]])
                self.assertTrue(item["canonical_owners"])
                self.assertTrue(item["consumer_paths"])
                self.assertTrue(item["checks"])
                for field in ("positive_test", "negative_test"):
                    self.assertEqual(set(item[field]), {"module", "test"})

    def test_a_missing_section_is_refused(self) -> None:
        raw = raw_registry()
        del raw["relationship_contract"]
        self.assertIn("REGISTRY_RELATION", contract_rules(raw))

    def test_the_entry_sets_are_exact(self) -> None:
        for section in ("relation_kinds", "relations", "link_types"):
            with self.subTest(section=section, change="remove"):
                raw = raw_registry()
                del raw["relationship_contract"][section][0]
                self.assertIn("REGISTRY_RELATION", contract_rules(raw))
            with self.subTest(section=section, change="duplicate"):
                raw = raw_registry()
                entries = raw["relationship_contract"][section]
                entries.append(copy.deepcopy(entries[0]))
                self.assertIn("REGISTRY_RELATION", contract_rules(raw))
            with self.subTest(section=section, change="stray"):
                raw = raw_registry()
                entries = raw["relationship_contract"][section]
                entries.append({**copy.deepcopy(entries[0]), "id": "stray"})
                self.assertIn("REGISTRY_RELATION", contract_rules(raw))

    def test_direction_is_an_enumerated_value_that_matches_its_kind(self) -> None:
        raw = raw_registry()
        relation(raw, "parent")["direction"] = "sideways"
        self.assertIn("REGISTRY_RELATION", contract_rules(raw))
        raw = raw_registry()
        relation(raw, "parent")["direction"] = "owner_to_consumer"
        self.assertIn("REGISTRY_RELATION", contract_rules(raw))
        raw = raw_registry()
        raw["relationship_contract"]["relation_kinds"][0]["direction"] = "sideways"
        self.assertIn("REGISTRY_RELATION", contract_rules(raw))

    def test_an_undeclared_reference_is_refused(self) -> None:
        mutations = {
            "kind": lambda item: item.update(kind="no-such-kind"),
            "source profile": lambda item: item["source_profile_ids"].append("no/such"),
            "target profile": lambda item: item["target_profile_ids"].append("no/such"),
            "owner profile": lambda item: item["canonical_owners"][0].update(
                profile_id="no/such"
            ),
            "frontmatter key": lambda item: item["canonical_owners"][0].update(
                key="no_such_key"
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                raw = raw_registry()
                mutate(relation(raw, "parent"))
                self.assertIn("REGISTRY_RELATION", contract_rules(raw))
        for label, relation_id, key in (
            ("body-contract column", "requirement-basis", "No Such Column"),
            ("section", "promotion", "No Such Section"),
            ("registry key", "consumer-impact", "template_definition.no_such_field"),
        ):
            with self.subTest(label=label):
                raw = raw_registry()
                relation(raw, relation_id)["canonical_owners"][0]["key"] = key
                self.assertIn("REGISTRY_RELATION", contract_rules(raw))

    def test_a_consumer_check_path_and_rule_must_resolve(self) -> None:
        mutations = {
            "empty consumers": lambda item: item.update(consumer_paths=[]),
            "missing consumer": lambda item: item.update(
                consumer_paths=["scripts/no-such-consumer.py"]
            ),
            "directory consumer": lambda item: item.update(consumer_paths=["scripts"]),
            "missing check path": lambda item: item["checks"][0].update(
                path="scripts/no-such-check.py"
            ),
            "absent rule": lambda item: item["checks"][0].update(
                rule_id="NO-SUCH-RULE-ID"
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                raw = raw_registry()
                mutate(relation(raw, "parent"))
                self.assertIn("REGISTRY_RELATION_CONSUMER", contract_rules(raw))
        raw = raw_registry()
        link = raw["relationship_contract"]["link_types"][0]
        link["checks"][0]["rule_id"] = "NO-SUCH-RULE-ID"
        self.assertIn("REGISTRY_RELATION_CONSUMER", contract_rules(raw))

    def test_a_test_reference_must_resolve(self) -> None:
        mutations = {
            "module": {"module": "tests/test_no_such_module.py"},
            "name": {"test": "test_no_such_test"},
        }
        for label, change in mutations.items():
            for field in ("positive_test", "negative_test"):
                with self.subTest(label=label, field=field):
                    raw = raw_registry()
                    item = relation(raw, "parent")
                    item[field] = {**item[field], **change}
                    self.assertIn("REGISTRY_RELATION_TEST", contract_rules(raw))
                    raw = raw_registry()
                    link = raw["relationship_contract"]["link_types"][0]
                    link[field] = {**link[field], **change}
                    self.assertIn("REGISTRY_RELATION_TEST", contract_rules(raw))

    def test_the_ownership_graph_must_be_a_forest(self) -> None:
        self.assertEqual(contract_rules(raw_registry()), set())
        # Plan is the parent of Task and Task is the parent of Plan: a cycle.
        raw = raw_registry()
        item = relation(raw, "parent")
        item["source_profile_ids"] = ["sdlc/task", "sdlc/plan"]
        item["target_profile_ids"] = ["sdlc/plan", "sdlc/task"]
        self.assertIn("REGISTRY_RELATION_CYCLE", contract_rules(raw))
        # A profile that is its own parent.
        raw = raw_registry()
        item = relation(raw, "parent")
        item["source_profile_ids"] = ["sdlc/plan"]
        item["target_profile_ids"] = ["sdlc/plan"]
        item["canonical_owners"] = [item["canonical_owners"][0]]
        self.assertIn("REGISTRY_RELATION_CYCLE", contract_rules(raw))
        # Two owner entries for the Task: never two direct owners.
        raw = raw_registry()
        item = relation(raw, "parent")
        task_owner = next(
            owner
            for owner in item["canonical_owners"]
            if owner["profile_id"] == "sdlc/task"
        )
        item["canonical_owners"].append(copy.deepcopy(task_owner))
        self.assertIn("REGISTRY_RELATION_CYCLE", contract_rules(raw))
        # Each source has the one target that owns it.
        raw = raw_registry()
        relation(raw, "parent")["target_profile_ids"].append("sdlc/requirement")
        self.assertIn("REGISTRY_RELATION_CYCLE", contract_rules(raw))
        # A supersession relation names one profile set on both sides and is
        # left to the document walk.
        item = relation(raw_registry(), "supersession")
        self.assertEqual(item["source_profile_ids"], item["target_profile_ids"])

    def test_the_registry_object_exposes_the_section_and_a_base_without_it_loads(
        self,
    ) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        contract = registry.relationship_contract
        self.assertIsNotNone(contract)
        self.assertEqual([item.id for item in contract.relation_kinds], list(KINDS))
        self.assertEqual([item.id for item in contract.relations], list(RELATIONS))
        self.assertEqual([item.id for item in contract.link_types], list(LINK_TYPES))
        raw = raw_registry()
        del raw["relationship_contract"]
        loaded = CONTRACTS.validate_registry(ROOT, raw)
        self.assertIsNone(loaded.relationship_contract)

    def test_the_authority_guard_admits_the_section_and_nothing_beside_it(
        self,
    ) -> None:
        raw = raw_registry()
        AUTHORITY.validate_registry_authority(raw)
        del raw["relationship_contract"]
        AUTHORITY.validate_registry_authority(raw)
        raw["relationship_contracts"] = {}
        with self.assertRaisesRegex(AUTHORITY.AuthorityError, "REGISTRY_TOP_LEVEL"):
            AUTHORITY.validate_registry_authority(raw)

    def test_the_schema_refuses_an_unknown_or_missing_relation_field(self) -> None:
        for mutate in (
            lambda item: item.update(vibes="x"),
            lambda item: item.pop("reverse_view"),
            lambda item: item["cardinality"].update(per_source="several"),
        ):
            raw = raw_registry()
            mutate(relation(raw, "parent"))
            with self.assertRaises(CONTRACTS.DocumentContractError) as caught:
                CONTRACTS.validate_registry(ROOT, raw)
            self.assertTrue(
                any(
                    item.rule_id.startswith("REGISTRY_SCHEMA")
                    for item in caught.exception.diagnostics
                )
            )

    def test_policy_authority_is_read_from_template_definition_policy_refs(
        self,
    ) -> None:
        raw = raw_registry()
        item = relation(raw, "policy-authority")
        defined = [
            profile for profile in raw["profiles"] if profile.get("template_definition")
        ]
        self.assertEqual(
            set(item["source_profile_ids"]), {profile["id"] for profile in defined}
        )
        for profile in defined:
            self.assertTrue(
                profile["template_definition"]["policy_refs"], profile["id"]
            )
        defined[0]["template_definition"]["policy_refs"] = []
        with self.assertRaises(CONTRACTS.DocumentContractError):
            CONTRACTS.validate_registry(ROOT, raw)


def _view(
    name: str,
    artifact_id: str,
    *,
    status: str = "active",
    profile: str = "governance/rule",
    supersedes: tuple[str, ...] = (),
    superseded_by: tuple[str, ...] = (),
) -> tuple[PurePosixPath, LifecycleEvidenceDocument]:
    path = PurePosixPath(f".agents/governance/{name}.md")
    document = LifecycleDocument(path, profile, status, None, artifact_id)
    return path, LifecycleEvidenceDocument(
        document=document,
        all_local_links=(),
        relationship_links=(),
        unresolved_relationship_links=(),
        body_table_links=(),
        relationship_section_valid=True,
        body_contract_valid=True,
        task_terminal_evidence_valid=False,
        supersedes_ids=supersedes,
        superseded_by_ids=superseded_by,
    )


def _tree(*views) -> dict[PurePosixPath, LifecycleEvidenceDocument]:
    return dict(views)


def _cycles(tree: dict) -> set[str]:
    return {
        item.path.stem
        for item in supersession_cycle_diagnostics(tree, base_mode="staged")
        if item.rule_id == "LIFECYCLE-EVIDENCE"
        and item.observed_transition == "supersession cycle"
    }


class SupersessionCycleTests(unittest.TestCase):
    def test_a_linear_chain_and_a_diamond_pass(self) -> None:
        chain = _tree(
            _view("one", "POL-0001", status="superseded", superseded_by=("POL-0002",)),
            _view("two", "POL-0002", supersedes=("POL-0001",)),
        )
        self.assertEqual(_cycles(chain), set())
        diamond = _tree(
            _view("one", "POL-0001", status="superseded"),
            _view("two", "POL-0002", supersedes=("POL-0001",)),
            _view("three", "POL-0003", supersedes=("POL-0001",)),
        )
        self.assertEqual(_cycles(diamond), set())

    def test_a_self_reference_fails(self) -> None:
        for field in ("supersedes", "superseded_by"):
            with self.subTest(field=field):
                tree = _tree(_view("one", "POL-0001", **{field: ("POL-0001",)}))
                self.assertEqual(_cycles(tree), {"one"})

    def test_a_two_and_a_three_document_loop_of_current_documents_fails(self) -> None:
        two = _tree(
            _view("one", "POL-0001", supersedes=("POL-0002",)),
            _view("two", "POL-0002", supersedes=("POL-0001",)),
        )
        self.assertEqual(_cycles(two), {"one", "two"})
        three = _tree(
            _view("one", "POL-0001", supersedes=("POL-0002",)),
            _view("two", "POL-0002", supersedes=("POL-0003",)),
            _view("three", "POL-0003", supersedes=("POL-0001",)),
            _view("four", "POL-0004", supersedes=("POL-0001",)),
        )
        self.assertEqual(_cycles(three), {"one", "two", "three"})

    def test_a_loop_that_uses_only_superseded_by_fails(self) -> None:
        tree = _tree(
            _view("one", "POL-0001", superseded_by=("POL-0002",)),
            _view("two", "POL-0002", superseded_by=("POL-0001",)),
        )
        self.assertEqual(_cycles(tree), {"one", "two"})

    def test_a_reciprocal_pair_is_not_a_loop(self) -> None:
        tree = _tree(
            _view("one", "POL-0001", status="superseded", superseded_by=("POL-0002",)),
            _view("two", "POL-0002", supersedes=("POL-0001",)),
            _view("three", "POL-0003", supersedes=("POL-0002",)),
        )
        self.assertEqual(_cycles(tree), set())

    def test_a_loop_through_an_absent_document_fails(self) -> None:
        tree = _tree(
            _view(
                "one",
                "POL-0001",
                supersedes=("POL-0009",),
                superseded_by=("POL-0009",),
            )
        )
        self.assertEqual(_cycles(tree), {"one"})

    def test_a_cycle_in_an_unchanged_part_fails_while_another_document_changes(
        self,
    ) -> None:
        loop = [
            _view("one", "POL-0001", supersedes=("POL-0002",)),
            _view("two", "POL-0002", supersedes=("POL-0001",)),
        ]
        other_path, other = _view("other", "POL-0005", status="active")
        base = {path: view.document for path, view in loop}
        base[other_path] = LifecycleDocument(
            other_path, "governance/rule", "draft", None, "POL-0005"
        )
        tree = _tree(*loop, (other_path, other))
        context = LifecycleEvidenceContext(
            base_documents=base,
            proposed_documents=tree,
            changed_paths=frozenset({other_path}),
            status_changed_paths=frozenset({other_path}),
            body_changed_paths=frozenset(),
            created_paths=frozenset(),
        )
        found = compare_lifecycle(
            CONTRACTS.load_registry(ROOT),
            base,
            {path: view.document for path, view in tree.items()},
            base_mode="staged",
            evidence_context=context,
        )
        self.assertEqual(
            {
                item.path.stem
                for item in found
                if item.rule_id == "LIFECYCLE-EVIDENCE"
                and item.observed_transition == "supersession cycle"
            },
            {"one", "two"},
        )

    def test_a_domain_without_a_superseded_state_lets_the_successor_carry_it(
        self,
    ) -> None:
        # ADR states are proposed, accepted and rejected: no superseded state, so
        # the accepted predecessor is never edited and the successor alone names it.
        adr = {"status": "accepted", "profile": "sdlc/architecture-decision"}
        tree = _tree(
            _view("one", "ADR-0001", **adr),
            _view("two", "ADR-0002", supersedes=("ADR-0001",), **adr),
        )
        self.assertEqual(_cycles(tree), set())
        looped = _tree(
            _view("one", "ADR-0001", supersedes=("ADR-0002",), **adr),
            _view("two", "ADR-0002", supersedes=("ADR-0001",), **adr),
        )
        self.assertEqual(_cycles(looped), {"one", "two"})

    def test_a_task_whose_parent_names_itself_fails_parent_identity(self) -> None:
        registry = CONTRACTS.load_registry(ROOT)
        profile = next(
            item for item in registry.profiles if item.profile_id == "sdlc/task"
        )
        path = PurePosixPath("docs/03.specs/0999-example/tasks/tsk-0001-example.md")
        text = "\n".join(
            (
                "---",
                'title: "Example"',
                'version: "0.1.0"',
                'type: "sdlc/task"',
                'status: "draft"',
                'owner: "platform"',
                'updated: "2026-11-14"',
                'artifact_id: "SPEC-0999-TSK-0001"',
                'parent_ids: ["SPEC-0999-TSK-0001"]',
                "---",
                "# Task: Example",
                "",
            )
        )

        def rules(source: str) -> set[str]:
            return {
                item.rule_id
                for item in MARKDOWN.validate_document_text(
                    source, path, profile, "strict"
                )
            }

        self.assertIn("PARENT-IDENTITY", rules(text))
        self.assertNotIn(
            "PARENT-IDENTITY",
            rules(text.replace('SPEC-0999-TSK-0001"]', 'SPEC-0999-PLAN-0001"]')),
        )


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
