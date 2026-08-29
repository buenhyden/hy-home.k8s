#!/usr/bin/env python3
"""Unit tests for the provider runtime/config evidence contract."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPOSITORY_ROOT / "scripts/validate-agent-provider-config.py"
AGGREGATE_PATH = REPOSITORY_ROOT / "scripts/validate-agent-provider-evidence.py"
CONTRACT_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/provider-runtime-evidence.json"
)
FIXTURE_PATH = REPOSITORY_ROOT / "tests/fixtures/agent-provider-runtime-evidence.json"
SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "docs/00.agent-governance/contracts/provider-runtime-evidence.schema.json"
)
AGENT_REGISTRY_PATH = REPOSITORY_ROOT / ".agents/registry.json"
ROUTING_PATH = (
    REPOSITORY_ROOT / "docs/00.agent-governance/contracts/validation-surfaces.json"
)
CAPABILITY_OWNER = "docs/00.agent-governance/contracts/provider-runtime-evidence.json"

GOVERNED_JSON_OWNERS = (
    (
        "contract",
        Path("docs/00.agent-governance/contracts/provider-runtime-evidence.json"),
        "contract",
    ),
    (
        "schema",
        Path(
            "docs/00.agent-governance/contracts/provider-runtime-evidence.schema.json"
        ),
        "contract",
    ),
    (
        "fixture",
        Path("tests/fixtures/agent-provider-runtime-evidence.json"),
        "fixture",
    ),
    (
        "agent-registry",
        Path(".agents/registry.json"),
        "contract",
    ),
    (
        "routing",
        Path("docs/00.agent-governance/contracts/validation-surfaces.json"),
        "contract",
    ),
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "validate_agent_provider_config", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    original_argv = sys.argv[:]
    sys.argv = [str(SCRIPT_PATH)]
    try:
        try:
            spec.loader.exec_module(module)
        except SystemExit:
            # A compatibility wrapper may still execute on import. The API
            # test below turns that incomplete behavior into an explicit RED.
            pass
    finally:
        sys.argv = original_argv
    return module


class ProviderConfigContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_module()
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def contract_copy(self):
        return copy.deepcopy(self.contract)

    def make_valid_root(self) -> Path:
        directory = tempfile.TemporaryDirectory(prefix="provider-config-boundary-")
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        owners = (
            CONTRACT_PATH,
            SCHEMA_PATH,
            FIXTURE_PATH,
            AGENT_REGISTRY_PATH,
            ROUTING_PATH,
        )
        for source in owners:
            relative = source.relative_to(REPOSITORY_ROOT)
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)

        for provider in self.contract["providers"]:
            for item in provider["projectPaths"]:
                target = root / item["path"]
                if item["state"] != "current":
                    continue
                if item["kind"] == "role-directory":
                    target.mkdir(parents=True, exist_ok=True)
                elif item["kind"] in {
                    "tracked-settings",
                }:
                    # Tracked settings are parsed for real by the validator, so
                    # a placeholder byte string would fail as JSON before the
                    # boundary rule under test could be reached.
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(REPOSITORY_ROOT / item["path"], target)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text("repository-static fixture\n", encoding="utf-8")
        registry = json.loads(AGENT_REGISTRY_PATH.read_text())
        for role in registry["roles"]:
            for provider in ("claude", "codex"):
                relative = role["projections"][provider]
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(REPOSITORY_ROOT / relative, target)
        for provider in registry["providers"]:
            relative = provider["gateway"]
            shutil.copyfile(REPOSITORY_ROOT / relative, root / relative)
        return root

    def run_boundary_owner(self, root: Path, runner: str) -> None:
        if runner == "fixture":
            self.validator.validate_fixture(root)
            return
        self.validator.validate_contract(root)

    def assert_input_rule(self, callback, forbidden_value: str = "") -> None:
        with self.assertRaises(self.validator.ProviderConfigError) as raised:
            callback()
        self.assertEqual(raised.exception.code, "PNME-INPUT")
        self.assertEqual(raised.exception.exit_code, 2)
        if forbidden_value:
            self.assertNotIn(forbidden_value, raised.exception.detail)

    def test_validator_exposes_import_safe_contract_api(self) -> None:
        self.assertTrue(
            hasattr(self.validator, "validate_contract"),
            "validator must expose validate_contract without exiting on import",
        )
        self.assertTrue(
            hasattr(self.validator, "ProviderConfigError"),
            "validator must expose typed rule failures",
        )

    def assert_rule(self, contract, expected_rule: str) -> None:
        with self.assertRaises(self.validator.ProviderConfigError) as raised:
            self.validator.validate_contract(
                REPOSITORY_ROOT, contract, check_paths=True
            )
        self.assertEqual(raised.exception.code, expected_rule)

    def test_production_contract_is_closed_and_cutoff_bounded(self) -> None:
        counts = self.validator.validate_contract(REPOSITORY_ROOT)
        self.assertEqual(counts["providers"], 2)
        self.assertEqual(counts["sources"], 7)
        self.assertEqual(counts["modelCandidates"], 4)
        self.assertEqual(counts["mcpServers"], 7)
        self.assertEqual(self.contract["cutoff"]["utc"], "2026-07-10T01:00:00Z")
        self.assertEqual(self.contract["contractVersion"], "1.0.0")

    def test_current_root_gateways_are_valid_thin_routers(self) -> None:
        self.validator.validate_contract(self.make_valid_root())

    def test_missing_root_gateways_fail_closed(self) -> None:
        for gateway in ("AGENTS.md", "CLAUDE.md"):
            with self.subTest(gateway=gateway):
                root = self.make_valid_root()
                (root / gateway).unlink()
                self.assert_input_rule(lambda: self.validator.validate_contract(root))

    def test_root_gateway_line_limit_is_preserved(self) -> None:
        for gateway in ("AGENTS.md", "CLAUDE.md"):
            with self.subTest(gateway=gateway):
                root = self.make_valid_root()
                path = root / gateway
                text = path.read_text(encoding="utf-8")
                text += "\n" * (25 - len(text.splitlines()))
                path.write_text(text, encoding="utf-8")
                self.validator.validate_contract(root)
                path.write_text(text + "\n", encoding="utf-8")
                with self.assertRaises(self.validator.ProviderConfigError) as raised:
                    self.validator.validate_contract(root)
                self.assertEqual(raised.exception.code, "PNME-GATEWAY")

    def test_root_gateways_require_current_owner_and_provider_pointers(self) -> None:
        registry = json.loads(AGENT_REGISTRY_PATH.read_text(encoding="utf-8"))
        for provider in registry["providers"]:
            provider_id = provider["id"]
            for pointer in (
                "@docs/00.agent-governance/skills/work-lifecycle.md",
                f"@docs/00.agent-governance/providers/{provider_id}.md",
                f"@.{provider_id}/{provider_id.upper()}.md",
                "@RTK.md",
                ".agents/registry.json",
            ):
                with self.subTest(provider=provider_id, pointer=pointer):
                    root = self.make_valid_root()
                    path = root / provider["gateway"]
                    text = path.read_text(encoding="utf-8")
                    self.assertIn(pointer, text)
                    path.write_text(
                        text.replace(pointer, "missing-pointer"), encoding="utf-8"
                    )
                    with self.assertRaises(
                        self.validator.ProviderConfigError
                    ) as raised:
                        self.validator.validate_contract(root)
                    self.assertEqual(raised.exception.code, "PNME-GATEWAY")

    def test_root_gateways_reject_embedded_roster_policy(self) -> None:
        for gateway in ("AGENTS.md", "CLAUDE.md"):
            for heading in ("Agent Catalog", "Role Separation", "Runtime Roster"):
                with self.subTest(gateway=gateway, heading=heading):
                    root = self.make_valid_root()
                    path = root / gateway
                    text = path.read_text(encoding="utf-8")
                    path.write_text(text + f"\n## {heading}\n", encoding="utf-8")
                    with self.assertRaises(
                        self.validator.ProviderConfigError
                    ) as raised:
                        self.validator.validate_contract(root)
                    self.assertEqual(raised.exception.code, "PNME-GATEWAY")

    def test_absent_runtime_cannot_claim_native_discovery_pass(self) -> None:
        mutated = self.contract_copy()
        self.validator.apply_mutation(mutated, "absent-runtime-native-pass")
        self.assert_rule(mutated, "PNME-UNSUPPORTED-RUNTIME")

    def test_provider_order_and_local_observations_are_exact(self) -> None:
        providers = self.contract["providers"]
        self.assertEqual(
            [provider["id"] for provider in providers],
            ["claude", "codex"],
        )
        observed = {
            provider["id"]: provider["localObservation"] for provider in providers
        }
        self.assertEqual(observed["claude"]["version"], "2.1.220 (Claude Code)")
        self.assertEqual(observed["claude"]["observedAt"], "2026-07-28")
        self.assertEqual(observed["claude"]["installation"], "present")
        self.assertEqual(observed["codex"]["version"], "codex-cli 0.140.0")
        self.assertEqual(observed["codex"]["installation"], "present")
        self.assertTrue(
            all(item["readinessClaim"] is False for item in observed.values())
        )
        self.assertTrue(
            all(item["userReported"] is False for item in observed.values())
        )
        prior = self.contract["observationHistory"][0]
        self.assertEqual(prior["observationClass"], "prior-user-report")
        self.assertEqual(
            prior["providers"]["codex"]["version"],
            "codex-cli 0.145.0-alpha.27",
        )
        self.assertEqual(prior["providers"]["claude"]["installation"], "absent")

    def test_surface_paths_match_agent_registry_without_neutral_relabeling(
        self,
    ) -> None:
        registry = json.loads(AGENT_REGISTRY_PATH.read_text(encoding="utf-8"))
        expected = {
            provider["id"]: (provider["projection_root"], "current")
            for provider in registry["providers"]
        }
        actual = {
            provider["id"]: (
                provider["trackedSurface"]["pathRoot"],
                provider["trackedSurface"]["state"],
            )
            for provider in self.contract["providers"]
        }
        self.assertEqual(actual, expected)
        self.assertNotIn(".agents/agents", {value[0] for value in actual.values()})

    def test_sources_have_dates_cutoff_classification_and_primary_claims(
        self,
    ) -> None:
        ledger = self.contract["sourceLedger"]
        self.assertEqual(
            tuple(source["id"] for source in ledger),
            self.validator.SOURCE_IDS,
        )
        self.assertEqual(
            set(source["provider"] for source in ledger),
            {"claude", "codex", "agency-agents"},
        )
        self.assertTrue(
            {
                "claude-code-changelog-2-1-154",
                "codex-release-0-145-0-alpha-2",
            }.issubset({source["id"] for source in ledger})
        )
        for source in ledger:
            self.assertTrue(source["url"].startswith("https://"))
            self.assertIn(source["publisher"], {"Anthropic", "OpenAI", "GitHub"})
            self.assertRegex(source["sourceDate"], r"^2026-\d{2}-\d{2}$")
            if source["publishedAtUtc"] is not None:
                self.assertRegex(
                    source["publishedAtUtc"],
                    r"^2026-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
                )
            self.assertIn(
                source["cutoffApplicability"],
                {"cutoff-applicable", "current-only"},
            )
            self.assertIn(source["confidence"], {"dated-primary", "current-primary"})
            self.assertTrue(source["claim"])
        exact_cutoff_source = next(
            source
            for source in ledger
            if source["id"] == "codex-release-0-145-0-alpha-2"
        )
        self.assertEqual(
            exact_cutoff_source["publishedAtUtc"],
            "2026-07-10T00:09:39Z",
        )

    def test_model_candidates_are_unpromoted_and_gate_exact_resolution(
        self,
    ) -> None:
        for provider in self.contract["providers"]:
            self.assertEqual(len(provider["modelCandidates"]), 2)
            for candidate in provider["modelCandidates"]:
                self.assertEqual(candidate["promotionState"], "candidate-only")
                self.assertIn("configuredId", candidate)
                self.assertIn("observedId", candidate)
                self.assertFalse(candidate["fallback"]["silentFallbackAllowed"])
                self.assertEqual(
                    set(candidate["gates"]),
                    {"configParse", "runtimeResolution", "spec044Fitness"},
                )

    def test_mcp_inventory_has_closed_ownership_and_trust_boundaries(self) -> None:
        inventory = self.contract["mcpInventory"]
        self.assertEqual(len(inventory), 7)
        self.assertEqual(
            {server["id"] for server in inventory},
            {
                "context7",
                "exa",
                "github",
                "memory",
                "playwright",
                "sequential-thinking",
                "supabase",
            },
        )
        for server in inventory:
            self.assertTrue(server["owner"])
            self.assertTrue(server["purpose"])
            self.assertTrue(server["transport"])
            self.assertTrue(server["trustBoundary"])
            self.assertTrue(server["allowedRoles"])
            self.assertIn(
                server["credentialClass"],
                {"none", "environment-reference", "provider-managed-auth"},
            )

    def test_duplicate_json_keys_fail_at_the_input_boundary(self) -> None:
        with self.assertRaises(self.validator.ProviderConfigError) as raised:
            self.validator.decode_json_text(
                '{"provider":{"id":"claude","id":"codex"}}',
                "<unit-fixture>",
            )
        self.assertEqual(raised.exception.code, "PNME-DUPLICATE-KEY")
        self.assertEqual(raised.exception.exit_code, 2)

    def test_symlink_repository_root_fails_closed_without_target_disclosure(
        self,
    ) -> None:
        root = self.make_valid_root()
        link = root.parent / f"{root.name}-link"
        link.symlink_to(root, target_is_directory=True)
        self.addCleanup(link.unlink)
        self.assert_input_rule(
            lambda: self.validator.validate_contract(link),
            str(root),
        )

    def test_parent_component_symlink_fails_closed_without_target_disclosure(
        self,
    ) -> None:
        root = self.make_valid_root()
        original = root / "docs"
        outside = root.parent / f"{root.name}-outside-docs"
        original.rename(outside)
        self.addCleanup(shutil.rmtree, outside, True)
        original.symlink_to(outside, target_is_directory=True)
        self.assert_input_rule(
            lambda: self.validator.validate_contract(root),
            str(outside),
        )

    def test_parent_directory_identity_swap_fails_closed(self) -> None:
        root = self.make_valid_root()
        parent = root / "docs"
        displaced = root / "docs-before-swap"
        original_open = self.validator.os.open
        triggered = False

        def swapping_open(path, flags, mode=0o777, *, dir_fd=None):
            nonlocal triggered
            if not triggered and os.fspath(path) == "docs" and dir_fd is not None:
                parent.rename(displaced)
                parent.mkdir()
                triggered = True
            return original_open(path, flags, mode, dir_fd=dir_fd)

        with mock.patch.object(
            self.validator.os,
            "open",
            side_effect=swapping_open,
        ):
            self.assert_input_rule(lambda: self.validator.validate_contract(root))
        self.assertTrue(triggered)

    def test_final_regular_file_identity_swap_fails_closed(self) -> None:
        root = self.make_valid_root()
        governed = root / GOVERNED_JSON_OWNERS[0][1]
        displaced = governed.with_name(f"{governed.name}.before-swap")
        original_open = self.validator.os.open
        trigger_paths = {str(governed), governed.name}
        triggered = False

        def swapping_open(path, flags, mode=0o777, *, dir_fd=None):
            nonlocal triggered
            if not triggered and os.fspath(path) in trigger_paths:
                governed.rename(displaced)
                shutil.copyfile(displaced, governed)
                triggered = True
            return original_open(path, flags, mode, dir_fd=dir_fd)

        with mock.patch.object(
            self.validator.os,
            "open",
            side_effect=swapping_open,
        ):
            self.assert_input_rule(lambda: self.validator.validate_contract(root))
        self.assertTrue(triggered)

    def test_each_governed_json_owner_rejects_a_final_symlink(self) -> None:
        for owner, relative, runner in GOVERNED_JSON_OWNERS:
            with self.subTest(owner=owner):
                root = self.make_valid_root()
                governed = root / relative
                outside = root.parent / f"{root.name}-{owner}-outside.json"
                shutil.copyfile(governed, outside)
                self.addCleanup(outside.unlink)
                governed.unlink()
                governed.symlink_to(outside)
                self.assert_input_rule(
                    lambda root=root, runner=runner: self.run_boundary_owner(
                        root, runner
                    ),
                    str(outside),
                )

    def test_each_governed_json_owner_rejects_a_final_directory(self) -> None:
        for owner, relative, runner in GOVERNED_JSON_OWNERS:
            with self.subTest(owner=owner):
                root = self.make_valid_root()
                governed = root / relative
                governed.unlink()
                governed.mkdir()
                self.assert_input_rule(
                    lambda root=root, runner=runner: self.run_boundary_owner(
                        root, runner
                    )
                )

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO nodes require os.mkfifo")
    def test_each_governed_json_owner_rejects_a_final_fifo(self) -> None:
        for owner, relative, runner in GOVERNED_JSON_OWNERS:
            with self.subTest(owner=owner):
                root = self.make_valid_root()
                governed = root / relative
                governed.unlink()
                os.mkfifo(governed)
                command = [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--root",
                    str(root),
                ]
                if runner == "fixture":
                    command.append("--self-test")
                result = subprocess.run(
                    command,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                self.assertEqual(
                    result.returncode,
                    2,
                    result.stdout + result.stderr,
                )
                self.assertIn("PNME-INPUT:", result.stderr)

    def test_current_role_directory_rejects_an_outside_symlink(self) -> None:
        root = self.make_valid_root()
        role_directory = root / ".claude/agents"
        for projection in role_directory.iterdir():
            projection.unlink()
        role_directory.rmdir()
        outside = root.parent / f"{root.name}-outside-roles"
        outside.mkdir()
        self.addCleanup(outside.rmdir)
        role_directory.symlink_to(outside, target_is_directory=True)
        self.assert_input_rule(
            lambda: self.validator.validate_contract(root),
            str(outside),
        )

    def test_current_provider_files_reject_outside_symlinks(self) -> None:
        current_files = (
            Path(".claude/settings.json"),
            Path("CLAUDE.md"),
        )
        for relative in current_files:
            with self.subTest(relative=relative.as_posix()):
                root = self.make_valid_root()
                governed = root / relative
                outside = root.parent / f"{root.name}-outside-file"
                outside.write_text(
                    "outside value must stay private\n", encoding="utf-8"
                )
                self.addCleanup(outside.unlink)
                governed.unlink()
                governed.symlink_to(outside)
                self.assert_input_rule(
                    lambda root=root: self.validator.validate_contract(root),
                    "outside value must stay private",
                )

    def test_declared_absent_provider_path_rejects_every_existing_final_node(
        self,
    ) -> None:
        absent = Path(".codex/config.toml")
        node_kinds = ("file", "directory", "broken-symlink")
        for node_kind in node_kinds:
            with self.subTest(node_kind=node_kind):
                root = self.make_valid_root()
                governed = root / absent
                governed.parent.mkdir(parents=True, exist_ok=True)
                if node_kind == "file":
                    governed.write_text("must remain absent\n", encoding="utf-8")
                elif node_kind == "directory":
                    governed.mkdir()
                else:
                    governed.symlink_to(root / "missing-outside-target")
                self.assert_input_rule(
                    lambda root=root: self.validator.validate_contract(root)
                )

    def test_declared_absent_path_accepts_a_missing_parent(self) -> None:
        root = self.make_valid_root()
        self.validator._inspect_governed_node(
            root,
            "uncreated-parent/config.toml",
            expected_kind="absent",
        )

    def test_declared_absent_path_rejects_an_existing_symlink_parent(
        self,
    ) -> None:
        root = self.make_valid_root()
        outside = root.parent / f"{root.name}-absent-outside"
        outside.mkdir()
        self.addCleanup(outside.rmdir)
        (root / "uncreated-parent").symlink_to(
            outside,
            target_is_directory=True,
        )
        self.assert_input_rule(
            lambda: self.validator._inspect_governed_node(
                root,
                "uncreated-parent/config.toml",
                expected_kind="absent",
            ),
            str(outside),
        )

    def test_declared_absent_path_rejects_an_existing_file_parent(self) -> None:
        root = self.make_valid_root()
        (root / "uncreated-parent").write_text(
            "a governed parent must be a directory\n",
            encoding="utf-8",
        )
        self.assert_input_rule(
            lambda: self.validator._inspect_governed_node(
                root,
                "uncreated-parent/config.toml",
                expected_kind="absent",
            )
        )

    def test_cli_symlink_root_is_an_exit_two_value_free_input_failure(self) -> None:
        root = self.make_valid_root()
        link = root.parent / f"{root.name}-cli-link"
        link.symlink_to(root, target_is_directory=True)
        self.addCleanup(link.unlink)
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--root",
                str(link),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("PNME-INPUT:", result.stderr)
        self.assertNotIn(str(root), result.stderr)

    def test_all_config_fixture_mutations_fail_with_declared_rule(self) -> None:
        for case in self.fixture["configMutations"]:
            with self.subTest(case=case["name"]):
                mutated = self.contract_copy()
                self.validator.apply_mutation(mutated, case["name"])
                self.assert_rule(mutated, case["expectedRule"])

    def test_self_test_cli_runs_real_contract_and_mutations(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--root",
                str(REPOSITORY_ROOT),
                "--self-test",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[PASS] agent provider config self-test passed", result.stdout)

    def test_provider_evidence_self_test_propagates_explicit_root_from_foreign_cwd(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(prefix="provider-evidence-root-") as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(AGGREGATE_PATH),
                    "--root",
                    str(REPOSITORY_ROOT),
                    "--self-test",
                ],
                cwd=directory,
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(
            "[PASS] agent provider evidence aggregate passed: "
            "mode=self-test validators=2",
            result.stdout,
        )

    def test_provider_evidence_aggregate_preserves_a_symlink_root(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="provider-evidence-symlink-"
        ) as directory:
            link = Path(directory) / "repository-link"
            link.symlink_to(REPOSITORY_ROOT, target_is_directory=True)
            result = subprocess.run(
                [
                    sys.executable,
                    str(AGGREGATE_PATH),
                    "--root",
                    str(link),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("PNME-INPUT:", result.stderr)
        self.assertNotIn(str(REPOSITORY_ROOT), result.stderr)

    def test_provider_evidence_aggregate_preserves_a_lexical_parent_escape(
        self,
    ) -> None:
        lexical_root = REPOSITORY_ROOT / "docs" / ".."
        result = subprocess.run(
            [
                sys.executable,
                str(AGGREGATE_PATH),
                "--root",
                str(lexical_root),
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("PNME-INPUT:", result.stderr)


if __name__ == "__main__":
    unittest.main()
