from __future__ import annotations

import contextlib
import copy
import importlib.util
import io
import os
import re
import stat
import sys
import tempfile
import unittest
from pathlib import Path, PurePosixPath
from unittest import mock


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


def load_script(name: str, relative_path: str):
    path = REPOSITORY_ROOT / relative_path
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise AssertionError(f"{relative_path} could not be loaded")
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
        cls.role_validator = load_script(
            "agent_harness_semantics_consumer_test_target",
            "scripts/validate-agent-harness-semantics.py",
        )
        cls.roster_validator = load_script(
            "agent_roster_currentness_consumer_test_target",
            "scripts/validate-agent-roster-currentness.py",
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
                "currentRoles": 12,
                "currentSurfaces": 4,
                "currentProjections": 48,
                "targetRoles": 12,
                "targetSurfaces": 4,
                "targetProjections": 48,
                "evidenceClasses": 4,
                "memoryClasses": 4,
                "consumers": 14,
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

    def test_source_observation_cutoff_matches_authoritative_instant(
        self,
    ) -> None:
        self.assertEqual(
            self.contract["sourceObservationCutoff"],
            "2026-07-10T10:00:00+09:00",
        )

    def test_all_eval_suites_record_repository_static_readiness(self) -> None:
        observed = tuple(
            role["evalSuite"]["admissionState"]
            for role in self.contract["canonicalRoles"]
        )
        self.assertEqual(len(observed), 12)
        self.assertEqual(
            observed,
            ("repository-static-evaluation-ready",) * 12,
        )

    def test_claude_supervisor_has_orchestration_only_tools(self) -> None:
        text = (
            REPOSITORY_ROOT / ".claude" / "agents" / "supervisor.md"
        ).read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        metadata = dict(
            line.split(": ", 1)
            for line in frontmatter.splitlines()
            if ": " in line
        )
        self.assertEqual(metadata["tools"], "Read, Grep, Glob, Task")
        self.assertTrue(
            {"Bash", "Edit", "Write"}.isdisjoint(
                item.strip() for item in metadata["tools"].split(",")
            )
        )

    def test_supervisor_tool_owners_share_the_least_privilege_mapping(
        self,
    ) -> None:
        expected_tools = ("Read", "Grep", "Glob", "Task")
        prohibited_tools = ("Bash", "Edit", "Write")

        adapter_text = (
            REPOSITORY_ROOT / ".claude" / "agents" / "supervisor.md"
        ).read_text(encoding="utf-8")
        adapter_frontmatter = adapter_text.split("---", 2)[1]
        adapter_metadata = dict(
            line.split(": ", 1)
            for line in adapter_frontmatter.splitlines()
            if ": " in line
        )
        adapter_tools = tuple(
            item.strip() for item in adapter_metadata["tools"].split(",")
        )

        quality_text = (
            REPOSITORY_ROOT / "scripts" / "validate-repo-quality-gates.sh"
        ).read_text(encoding="utf-8")
        quality_section = quality_text.split(
            "expected_claude_agent_tools = {", 1
        )[1].split("}", 1)[0]
        quality_line = next(
            line.strip()
            for line in quality_section.splitlines()
            if line.strip().startswith('"supervisor": ')
        )
        quality_tools = tuple(
            item.strip() for item in quality_line.split('"')[3].split(",")
        )

        protocol_text = (
            REPOSITORY_ROOT
            / "docs"
            / "00.agent-governance"
            / "subagent-protocol.md"
        ).read_text(encoding="utf-8")
        protocol_lines = protocol_text.splitlines()
        protocol_index = next(
            index
            for index, line in enumerate(protocol_lines)
            if line.startswith("- `supervisor`:")
        )
        protocol_line = protocol_lines[protocol_index]
        protocol_context = " ".join(
            " ".join(
                protocol_lines[protocol_index : protocol_index + 3]
            ).split()
        )
        protocol_tools = tuple(
            re.findall(r"`([^`]+)`", protocol_line)[1:]
        )

        self.assertEqual(adapter_tools, expected_tools)
        self.assertEqual(quality_tools, expected_tools)
        self.assertEqual(protocol_tools, expected_tools)
        self.assertNotIn("full toolset", protocol_context)
        self.assertIn("delegates mutation and validation", protocol_context)
        self.assertIn(
            "has no `Bash`, `Edit`, or `Write` authority",
            protocol_context,
        )
        self.assertTrue(
            set(prohibited_tools).isdisjoint(
                adapter_tools + quality_tools + protocol_tools
            )
        )

    def test_currentness_mutations_have_stable_rule_ids(self) -> None:
        cases = {
            case["name"]: case["expectedRule"]
            for case in self.fixture["mutations"]
        }
        self.assertEqual(
            {
                name: cases.get(name)
                for name in (
                    "stale-source-observation-cutoff",
                    "stale-eval-admission-state",
                )
            },
            {
                "stale-source-observation-cutoff": "HARNESS-CUTOFF",
                "stale-eval-admission-state": "HARNESS-EVAL",
            },
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
                "current",
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
        mutated["targetInventory"]["state"] = "current"
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

    def test_harness_validator_registration_and_surface_routes_are_exact(
        self,
    ) -> None:
        routing = self.validator.load_json(
            REPOSITORY_ROOT, self.validator.ROUTING_PATH
        )
        harness_validators = [
            validator
            for validator in routing["validators"]
            if validator["id"] == "agent-harness-contract"
        ]
        self.assertEqual(
            harness_validators,
            [self.validator.HARNESS_VALIDATOR],
        )
        routed = tuple(
            surface["id"]
            for surface in routing["surfaces"]
            if "agent-harness-contract" in surface["validators"]
        )
        self.assertEqual(routed, self.validator.HARNESS_ROUTED_SURFACES)

    def test_readme_owner_rows_name_exact_eight_surface_routing(self) -> None:
        expected_surfaces = (
            "provider-gateways",
            "agent-shared",
            "agent-claude",
            "agent-codex",
            "agent-gemini",
            "governance-documents",
            "scripts",
            "tests",
        )
        self.assertEqual(len(expected_surfaces), 8)
        self.assertEqual(
            self.validator.HARNESS_ROUTED_SURFACES,
            expected_surfaces,
        )
        owners = (
            (
                REPOSITORY_ROOT / "scripts" / "README.md",
                "| `python3 scripts/validate-agent-harness-contract.py "
                "--self-test`;",
            ),
            (
                REPOSITORY_ROOT / "tests" / "README.md",
                "| Agent harness contract fixture |",
            ),
        )
        for path, prefix in owners:
            with self.subTest(path=path.relative_to(REPOSITORY_ROOT)):
                rows = [
                    line
                    for line in path.read_text(encoding="utf-8").splitlines()
                    if line.startswith(prefix)
                ]
                self.assertEqual(len(rows), 1)
                self.assertIn("exact eight-surface routing", rows[0])
                self.assertNotIn("seven-surface routing", rows[0])

    def test_consumer_set_is_exact_and_current(self) -> None:
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
        self.assertTrue(
            all(
                (
                    consumer["selectedContract"],
                    consumer["selectedVersion"],
                    consumer["migrationState"],
                ) == ("harness-contract", "1.0.0", "current")
                for consumer in self.contract["consumers"]
            )
        )

    def test_no_canonical_role_remains_target_only_after_area002(self) -> None:
        current = set(self.contract["currentInventory"]["roleIds"])
        targets = [
            role for role in self.contract["canonicalRoles"]
            if role["id"] not in current
        ]
        self.assertEqual(targets, [])

    def _single_role_surface_contract(self):
        mutated = self.contract_copy()
        projection = copy.deepcopy(
            mutated["currentInventory"]["projections"][0]
        )
        mutated["currentInventory"].update(
            {
                "expectedRoleCount": 1,
                "expectedSurfaceCount": 1,
                "expectedProjectionCount": 1,
                "roleIds": [projection["roleId"]],
                "surfaceIds": [projection["surfaceId"]],
                "projections": [projection],
            }
        )
        return mutated, projection

    def test_role_semantics_consumer_follows_mutated_harness_selection(self) -> None:
        mutated, projection = self._single_role_surface_contract()
        canonical = next(
            role for role in mutated["canonicalRoles"]
            if role["id"] == projection["roleId"]
        )
        migrated_claim = canonical["adapterSemantics"]["responsibilities"][0]
        canonical["adapterSemantics"]["responsibilities"] = [
            "Synthetic harness-selected responsibility for consumer routing."
        ]
        selection = self.role_validator.select_current_harness(mutated)
        self.assertEqual(selection.role_ids, (projection["roleId"],))
        self.assertEqual(selection.surface_ids, (projection["surfaceId"],))
        path, source = self.role_validator.adapter_source(
            REPOSITORY_ROOT,
            selection,
            projection["surfaceId"],
            projection["roleId"],
        )
        adapter = self.role_validator.parse_adapter_text(
            projection["surfaceId"], path, source
        )
        diagnostics = self.role_validator.validate_adapter(
            selection.roles[projection["roleId"]], adapter
        )
        self.assertEqual(
            [diagnostic.code for diagnostic in diagnostics],
            ["ROLE-RESPONSIBILITY"],
        )
        self.assertIn(migrated_claim, source)
        self.assertEqual(
            self.role_validator.CONTRACT_PATH,
            PurePosixPath(
                "docs/00.agent-governance/contracts/harness-contract.json"
            ),
        )

    def test_roster_consumer_follows_mutated_harness_selection(self) -> None:
        mutated, projection = self._single_role_surface_contract()
        roster = self.roster_validator.select_current_harness(mutated)
        catalog = (
            REPOSITORY_ROOT / "docs/00.agent-governance/harness-catalog.md"
        ).read_text(encoding="utf-8")
        errors = self.roster_validator.validate_contract(
            {projection["surfaceId"]: {projection["roleId"]}},
            catalog,
            roster,
        )
        self.assertEqual(errors, [])
        self.assertEqual(len(roster.projection_paths), 1)
        self.assertEqual(
            self.roster_validator.HARNESS_CONTRACT_PATH,
            PurePosixPath(
                "docs/00.agent-governance/contracts/harness-contract.json"
            ),
        )

    def test_semantic_consumer_rejects_unsafe_surface_root(self) -> None:
        mutated, projection = self._single_role_surface_contract()
        surface = next(
            surface for surface in mutated["surfaces"]
            if surface["id"] == projection["surfaceId"]
        )
        surface["pathRoot"] = "../.agents/agents"
        projection["path"] = "../.agents/agents/supervisor.md"
        with self.assertRaises(self.role_validator.ContractError) as caught:
            self.role_validator.select_current_harness(mutated)
        self.assertIn("ROLE-ADAPTER-SURFACES", str(caught.exception))

    def test_roster_consumer_rejects_non_adapter_extension(self) -> None:
        mutated, projection = self._single_role_surface_contract()
        surface = next(
            surface for surface in mutated["surfaces"]
            if surface["id"] == projection["surfaceId"]
        )
        surface["extension"] = ".json"
        projection["path"] = (
            f"{surface['pathRoot']}/{projection['roleId']}.json"
        )
        with self.assertRaises(ValueError) as caught:
            self.roster_validator.select_current_harness(mutated)
        self.assertIn("location differs", str(caught.exception))

    def test_semantic_consumer_rejects_symlink_adapter_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "repo"
            outside = Path(tmpdir) / "outside"
            root.mkdir()
            outside.mkdir()
            (root / ".agents").symlink_to(outside, target_is_directory=True)
            selection = self.role_validator.HarnessSelection(
                role_ids=("supervisor",),
                surface_ids=("local",),
                roles={},
                locations={"local": (PurePosixPath(".agents/agents"), ".md")},
                projection_paths={
                    ("supervisor", "local"): PurePosixPath(
                        ".agents/agents/supervisor.md"
                    )
                },
            )
            with self.assertRaises(self.role_validator.ContractError) as caught:
                self.role_validator.adapter_source(
                    root, selection, "local", "supervisor"
                )
            self.assertIn("symlink path component", str(caught.exception))

    def test_roster_consumer_rejects_symlink_surface_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "repo"
            outside = Path(tmpdir) / "outside"
            root.mkdir()
            outside.mkdir()
            (root / ".agents").symlink_to(outside, target_is_directory=True)
            roster = self.roster_validator.HarnessRoster(
                role_ids=("supervisor",),
                surface_ids=("local",),
                locations={"local": (PurePosixPath(".agents/agents"), ".md")},
                projection_paths=frozenset({
                    PurePosixPath(".agents/agents/supervisor.md")
                }),
            )
            with self.assertRaises(ValueError) as caught:
                self.roster_validator.repository_inputs(root, roster)
            self.assertIn("symlink path component", str(caught.exception))

    def test_semantic_consumer_rejects_symlink_contract_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "repo"
            outside = Path(tmpdir) / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "harness-contract.json").write_text(
                "{}\n", encoding="utf-8"
            )
            (root / "docs").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(self.role_validator.ContractError) as caught:
                self.role_validator.load_json(
                    root,
                    PurePosixPath("docs/harness-contract.json"),
                )
            self.assertIn("symlink path component", str(caught.exception))

    def test_roster_consumer_rejects_symlink_contract_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "repo"
            outside = Path(tmpdir) / "outside"
            contract_parent = outside / "00.agent-governance" / "contracts"
            root.mkdir()
            contract_parent.mkdir(parents=True)
            (contract_parent / "harness-contract.json").write_text(
                "{}\n", encoding="utf-8"
            )
            (root / "docs").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError) as caught:
                self.roster_validator.load_harness_contract(root)
            self.assertIn("symlink path component", str(caught.exception))

    def test_roster_consumer_rejects_symlink_fixture_parent(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir) / "repo"
            outside = Path(tmpdir) / "outside"
            root.mkdir()
            outside.mkdir()
            (outside / "agent-roster-currentness.json").write_text(
                "{}\n", encoding="utf-8"
            )
            (root / "tests").mkdir()
            (root / "tests" / "fixtures").symlink_to(
                outside, target_is_directory=True
            )
            roster = self.roster_validator.HarnessRoster(
                role_ids=("supervisor",),
                surface_ids=("local",),
                locations={"local": (PurePosixPath(".agents/agents"), ".md")},
                projection_paths=frozenset({
                    PurePosixPath(".agents/agents/supervisor.md")
                }),
            )
            with self.assertRaises(ValueError) as caught:
                self.roster_validator.run_self_test(root, roster)
            self.assertIn("symlink path component", str(caught.exception))

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

    def test_domain_memory_lifecycle_refs_dedupe_converged_routes(self) -> None:
        classes = {
            item["id"]: item for item in self.contract["memory"]["classes"]
        }
        self.assertEqual(
            classes["domain-scoped"]["lifecyclePolicyRefs"],
            [
                "docs/00.agent-governance/rules/document-authoring.md",
                self.validator.LOOP_LIFECYCLE_SPEC.as_posix(),
            ],
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
                self.validator.validate_projection_files(
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
                self.validator.validate_projection_files(
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

    def test_json_read_uses_opened_descriptor_after_final_path_swap(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            nested = root / "nested"
            nested.mkdir()
            payload = nested / "input.json"
            payload.write_text('{"source":"inside"}\n', encoding="utf-8")
            outside = root / "outside.json"
            outside.write_text('{"source":"outside"}\n', encoding="utf-8")
            payload_inode = payload.stat().st_ino
            original_fstat = os.fstat
            swapped = False

            def swap_after_check(descriptor: int):
                nonlocal swapped
                metadata = original_fstat(descriptor)
                if (
                    not swapped
                    and stat.S_ISREG(metadata.st_mode)
                    and metadata.st_ino == payload_inode
                ):
                    swapped = True
                    payload.rename(nested / "input-original.json")
                    payload.symlink_to(outside)
                return metadata

            with mock.patch.object(
                self.validator.os,
                "fstat",
                side_effect=swap_after_check,
            ):
                loaded = self.validator.load_json(
                    root,
                    PurePosixPath("nested/input.json"),
                )

            self.assertTrue(swapped)
            self.assertEqual(loaded, {"source": "inside"})

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
                self.validator.validate_projection_files(
                    root, self.contract["currentInventory"]["projections"]
                )
            self.assertEqual(raised.exception.code, "HARNESS-FILE")

    def test_target_inventory_paths_are_now_current_projection_paths(self) -> None:
        target_paths = [
            projection["path"]
            for projection in self.contract["targetInventory"]["projections"]
        ]
        current_paths = [
            projection["path"]
            for projection in self.contract["currentInventory"]["projections"]
        ]
        self.assertEqual(target_paths, current_paths)
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
        self.assertIn("current=12/4/48", stdout.getvalue())

        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            self_test = self.validator.main(
                ["--root", str(REPOSITORY_ROOT), "--self-test"]
            )
        self.assertEqual(self_test, 0)
        self.assertIn("cases=38", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
