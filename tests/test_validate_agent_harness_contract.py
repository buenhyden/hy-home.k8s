from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    REPOSITORY_ROOT / "scripts" / "validate-agent-harness-contract.py"
)


def load_validator():
    specification = importlib.util.spec_from_file_location(
        "agent_harness_contract_test_target", VALIDATOR_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError("agent harness contract validator could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


class AgentHarnessContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.contract = cls.validator.load_json(
            REPOSITORY_ROOT, cls.validator.CONTRACT_PATH
        )
        cls.fixture = cls.validator.load_json(
            REPOSITORY_ROOT, cls.validator.FIXTURE_PATH
        )

    def contract_copy(self):
        return copy.deepcopy(self.contract)

    def assert_rule(self, contract, code: str) -> None:
        with self.assertRaises(self.validator.HarnessError) as raised:
            self.validator.validate_contract(
                REPOSITORY_ROOT, contract, check_files=False
            )
        self.assertEqual(raised.exception.code, code)

    def test_production_contract_has_exact_current_and_target_counts(self) -> None:
        counts = self.validator.validate_contract(REPOSITORY_ROOT)
        self.assertEqual(
            counts,
            {
                "currentRoles": 10,
                "currentSurfaces": 3,
                "currentProjections": 30,
                "targetRoles": 12,
                "targetSurfaces": 4,
                "targetProjections": 48,
                "evidenceClasses": 4,
                "memoryClasses": 4,
                "consumers": 11,
            },
        )

    def test_canonical_target_order_matches_spec_044(self) -> None:
        canonical = tuple(
            role["id"] for role in self.contract["canonicalRoles"]
        )
        target = tuple(self.contract["targetInventory"]["roleIds"])
        self.assertEqual(canonical, self.validator.TARGET_ROLES)
        self.assertEqual(target, self.validator.TARGET_ROLES)
        self.assertEqual(
            self.validator.TARGET_ROLES,
            (
                "supervisor",
                "code-reviewer",
                "doc-writer",
                "gitops-reviewer",
                "incident-responder",
                "k8s-implementer",
                "network-reviewer",
                "observability-reviewer",
                "security-auditor",
                "wiki-curator",
                "docs-researcher",
                "quality-engineer",
            ),
        )

    def test_projection_order_is_exact_role_by_surface_product(self) -> None:
        for inventory_name, roles, surfaces, state in (
            (
                "currentInventory",
                self.validator.CURRENT_ROLES,
                self.validator.CURRENT_SURFACES,
                "current",
            ),
            (
                "targetInventory",
                self.validator.TARGET_ROLES,
                self.validator.TARGET_SURFACES,
                "target-only",
            ),
        ):
            expected = tuple(
                self.validator._expected_projection(role, surface, state)
                for role in roles
                for surface in surfaces
            )
            actual = tuple(
                self.validator._projection_tuple(projection)
                for projection in self.contract[inventory_name]["projections"]
            )
            self.assertEqual(actual, expected)

    def test_all_fixture_mutations_fail_with_the_declared_rule(self) -> None:
        self.validator._validate_fixture(self.fixture)
        for case in self.fixture["mutations"]:
            with self.subTest(case=case["name"]):
                mutated = self.contract_copy()
                self.validator._apply_mutation(mutated, case["name"])
                self.assert_rule(mutated, case["expectedRule"])

    def test_duplicate_json_keys_are_input_boundary_failures(self) -> None:
        duplicate = '{"outer":{"role":"one","role":"two"}}'
        with self.assertRaises(self.validator.HarnessError) as raised:
            self.validator.decode_json_text(duplicate, "<unit-fixture>")
        self.assertEqual(raised.exception.code, "HARNESS-DUPLICATE-KEY")
        self.assertEqual(raised.exception.exit_code, 2)

    def test_unknown_nested_keys_are_rejected_by_closed_schema(self) -> None:
        mutated = self.contract_copy()
        mutated["canonicalRoles"][0]["evalSuite"]["unexpected"] = True
        self.assert_rule(mutated, "HARNESS-SCHEMA")

    def test_current_target_state_conflation_is_rejected(self) -> None:
        mutated = self.contract_copy()
        mutated["canonicalRoles"][-1]["admissionState"] = "current"
        self.assert_rule(mutated, "HARNESS-INVENTORY-STATE")

    def test_evidence_classes_and_remote_live_mapping_are_non_transitive(self) -> None:
        self.assertEqual(
            tuple(item["id"] for item in self.contract["evidenceClasses"]),
            self.validator.EVIDENCE_CLASSES,
        )
        mapping = {
            item["evidenceClass"]: item
            for item in self.contract["routingContract"]["evidenceMapping"]
        }
        self.assertIsNone(mapping["provider-runtime"]["validationSurfaceLane"])
        self.assertEqual(
            mapping["remote-live"]["validationSurfaceLane"], "remote/live"
        )
        self.assertTrue(
            all(
                item["crossClassInferenceAllowed"] is False
                for item in self.contract["evidenceClasses"]
            )
        )

    def test_consumer_set_and_legacy_subset_are_exact(self) -> None:
        observed = tuple(
            (
                consumer["id"],
                consumer["path"],
                consumer["selectedContract"],
                consumer["selectedVersion"],
                consumer["migrationState"],
            )
            for consumer in self.contract["consumers"]
        )
        self.assertEqual(observed, self.validator.CONSUMERS)
        self.assertEqual(
            tuple(self.contract["compatibility"]["legacyConsumers"]),
            self.validator.LEGACY_CONSUMERS,
        )
        self.assertEqual(
            self.contract["compatibility"]["removalOwnerSpec"],
            self.validator.REMOVAL_OWNER_SPEC,
        )

    def test_memory_classes_have_closed_authority_and_promotion(self) -> None:
        classes = {
            item["id"]: item for item in self.contract["memory"]["classes"]
        }
        self.assertEqual(tuple(classes), self.validator.MEMORY_CLASSES)
        self.assertEqual(
            classes["provider-local-auxiliary"]["authority"]["mode"],
            "advisory-only",
        )
        self.assertFalse(
            classes["provider-local-auxiliary"]["authority"][
                "repositoryFacts"
            ]
        )
        self.assertEqual(
            classes["provider-local-auxiliary"]["promotion"]["targetClass"],
            "working-short-term",
        )
        self.assertEqual(
            classes["working-short-term"]["promotion"]["targetClass"],
            "durable-long-term",
        )
        for memory_class in classes.values():
            self.assertEqual(
                tuple(memory_class["prohibitedContent"]),
                self.validator.PROHIBITED_CONTENT,
            )
            self.assertIn(
                self.validator.LOOP_LIFECYCLE_SPEC.as_posix(),
                memory_class["lifecyclePolicyRefs"],
            )

    def test_policy_labels_do_not_trigger_sensitive_payload_detection(self) -> None:
        policy_only = {
            "prohibitedActions": [
                "Never store credentials, tokens, secrets, raw prompts, "
                "full provider transcripts, auth files, or shell history.",
                "Observed shell history must never be recorded.",
                "Auth file content belongs outside tracked memory.",
                "Private diagnostic payloads are prohibited.",
                "Environment dumps and user configuration are not memory.",
            ],
            "prohibitedContent": list(self.validator.PROHIBITED_CONTENT),
        }
        self.validator.scan_sensitive_payload(policy_only)

    def test_conversational_payload_is_rejected_without_storing_one(self) -> None:
        payload = "Raw " + "prompt" + ": synthetic fixture material"
        with self.assertRaises(self.validator.HarnessError) as raised:
            self.validator.scan_sensitive_payload({"purpose": payload})
        self.assertEqual(raised.exception.code, "HARNESS-SENSITIVE")

    def test_each_sensitive_payload_shape_is_rejected(self) -> None:
        for name in (
            "sensitive-payload",
            *self.validator.SENSITIVE_MUTATIONS,
        ):
            with self.subTest(name=name):
                mutated = self.contract_copy()
                self.validator._apply_mutation(mutated, name)
                self.assert_rule(mutated, "HARNESS-SENSITIVE")

    def _write_current_projection_fixture(self, root: Path) -> None:
        for projection in self.contract["currentInventory"]["projections"]:
            target = root / projection["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("synthetic adapter\n", encoding="utf-8")

    def test_current_projection_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_current_projection_fixture(root)
            projection = self.contract["currentInventory"]["projections"][0]
            target = root / projection["path"]
            target.unlink()
            outside = root / "outside.md"
            outside.write_text("synthetic outside\n", encoding="utf-8")
            target.symlink_to(outside)
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator.validate_current_projection_files(
                    root, self.contract["currentInventory"]["projections"]
                )
            self.assertEqual(raised.exception.code, "HARNESS-FILE")

    def test_current_projection_parent_symlink_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            root = temporary_root / "repository"
            root.mkdir()
            self._write_current_projection_fixture(root)
            outside = temporary_root / "outside-agents"
            (root / ".agents").rename(outside)
            (root / ".agents").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator.validate_current_projection_files(
                    root, self.contract["currentInventory"]["projections"]
                )
            self.assertEqual(raised.exception.code, "HARNESS-FILE")
            self.assertIn("symlink path component", raised.exception.detail)

    def test_json_loader_rejects_contract_parent_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            root = temporary_root / "repository"
            outside = temporary_root / "outside-docs"
            root.mkdir()
            outside.mkdir()
            (outside / "contract.json").write_text("{}\n", encoding="utf-8")
            (root / "docs").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator.load_json(
                    root, PurePosixPath("docs/contract.json")
                )
            self.assertEqual(raised.exception.code, "HARNESS-INPUT")
            self.assertEqual(raised.exception.exit_code, 2)

    def test_consumer_parent_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            temporary_root = Path(temporary)
            root = temporary_root / "repository"
            outside = temporary_root / "outside-scripts"
            root.mkdir()
            outside.mkdir()
            (outside / "consumer.py").write_text(
                "synthetic consumer\n", encoding="utf-8"
            )
            (root / "scripts").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator._safe_repo_regular_file(
                    root,
                    PurePosixPath("scripts/consumer.py"),
                    "HARNESS-CONSUMER",
                    "synthetic consumer",
                )
            self.assertEqual(raised.exception.code, "HARNESS-CONSUMER")
            self.assertIn("symlink path component", raised.exception.detail)

    def test_current_projection_orphan_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._write_current_projection_fixture(root)
            orphan = root / ".agents/agents/orphan.md"
            orphan.write_text("synthetic orphan\n", encoding="utf-8")
            with self.assertRaises(self.validator.HarnessError) as raised:
                self.validator.validate_current_projection_files(
                    root, self.contract["currentInventory"]["projections"]
                )
            self.assertEqual(raised.exception.code, "HARNESS-FILE")

    def test_target_files_are_not_required_for_current_validation(self) -> None:
        missing_target_paths = [
            projection["path"]
            for projection in self.contract["targetInventory"]["projections"]
            if not (REPOSITORY_ROOT / projection["path"]).exists()
        ]
        self.assertGreater(len(missing_target_paths), 0)
        self.validator.validate_contract(REPOSITORY_ROOT)

    def test_cli_distinguishes_input_boundary_from_findings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            missing = Path(temporary) / "missing-root"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = self.validator.main(["--root", str(missing)])
        self.assertEqual(result, 2)
        self.assertIn("HARNESS-INPUT", stderr.getvalue())

    def test_cli_production_and_self_test_pass(self) -> None:
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            production = self.validator.main(
                ["--root", str(REPOSITORY_ROOT)]
            )
        self.assertEqual(production, 0)
        self.assertIn("current=10/3/30", stdout.getvalue())

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self_test = self.validator.main(
                ["--root", str(REPOSITORY_ROOT), "--self-test"]
            )
        self.assertEqual(self_test, 0)
        self.assertIn("cases=33", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
