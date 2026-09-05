"""QA routes keep common agent authority inside the existing static gates."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "profile_routes", ROOT / "scripts/validate-affected-surfaces.py"
)
ROUTES = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ROUTES
SPEC.loader.exec_module(ROUTES)


class ValidationProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(
            (ROOT / "scripts/validation/registry.json").read_text()
        )

    def test_common_and_provider_authority_select_all_document_gates(self):
        cases = {
            ".agents/README.md": "governance-documents",
            ".agents/governance/quality.md": "governance-documents",
            ".agents/workflows/work-lifecycle.md": "governance-documents",
            ".agents/roles/registry.json": "agent-shared",
            ".agents/skills/k8s-validate/SKILL.md": "agent-shared",
            ".agents/skills/k8s-validate/agents/openai.yaml": "agent-shared",
            ".claude/provider.md": "agent-claude",
            ".codex/provider.md": "agent-codex",
        }
        expected = {
            "agent-governance",
            "document-contract-registry",
            "document-lifecycle",
            "links-and-owners",
            "markdown-profiles",
            "repository-quality",
        }
        for path, owner in cases.items():
            with self.subTest(path=path):
                surface = ROUTES.classify_path(self.contract, path)
                self.assertEqual(surface["id"], owner)
                self.assertEqual(set(surface["validators"]), expected)
                self.assertEqual(surface["protectedLevel"], "protected")

    def test_retired_governance_root_has_no_functional_selector(self):
        for path in (
            "docs/00.agent-governance/README.md",
            "docs/00.agent-governance/roles/registry.json",
            "docs/00.agent-governance/skills/k8s-validate/SKILL.md",
        ):
            with self.subTest(path=path), self.assertRaises(ROUTES.ContractError):
                ROUTES.classify_path(self.contract, path)

    def test_full_and_ci_keep_the_same_nineteen_unique_gates(self):
        expected = {
            "affected-surface-contract",
            "archive-cutover",
            "agent-governance",
            "ci-python-contract",
            "document-contract-registry",
            "document-lifecycle",
            "gitops-change-set",
            "gitops-structure",
            "infrastructure-contracts",
            "k8s-manifests",
            "links-and-owners",
            "markdown-profiles",
            "policy-gates",
            "repository-quality",
            "workspace-boundary",
            "secret-handling",
            "vault-eso-contracts",
            "unit-tests",
            "pre-commit",
        }
        full = self.contract["profiles"]["full"]
        self.assertEqual(full, self.contract["profiles"]["ci"])
        self.assertEqual(len(full), len(expected))
        self.assertEqual(set(full), expected)

    def test_shell_hooks_only_select_existing_shell_owners(self):
        config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text())
        hooks = {hook["id"]: hook for repo in config["repos"] for hook in repo["hooks"]}
        for identifier in ("shellcheck", "shfmt"):
            with self.subTest(hook=identifier):
                pattern = hooks[identifier]["files"]
                for path in (
                    "scripts/validate-harness.sh",
                    "infrastructure/bootstrap-local.sh",
                ):
                    self.assertIsNotNone(re.search(pattern, path))
                for path in (
                    "docs/00.agent-governance/hooks/test.sh",
                    ".agents/hooks/test.sh",
                    ".agents/skills/test/example.sh",
                    "docs/example.sh",
                ):
                    self.assertIsNone(re.search(pattern, path))


class SkillAdapterPathTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="skill-route-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / ".agents/skills/example/SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("# Example\n")
        registry = self.root / ".agents/roles/registry.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(
            json.dumps(
                {
                    "skills": [
                        {"id": "example", "path": ".agents/skills/example/SKILL.md"}
                    ]
                }
            )
        )
        self.link = self.root / ".claude/skills/example"
        self.link.parent.mkdir(parents=True)
        self.link.symlink_to("../../.agents/skills/example")

    def test_registered_individual_skill_adapter_is_a_supported_tracked_path(self):
        ROUTES.reject_symlink_traversal(
            self.root, ".claude/skills/example", require_present=True
        )

    def assert_registry_swap_rejected(self, *, parent):
        temporary = tempfile.TemporaryDirectory(prefix="registry-outside-")
        self.addCleanup(temporary.cleanup)
        outside = Path(temporary.name)
        registry = self.root / ".agents/roles/registry.json"
        sentinel = outside / registry.name
        sentinel.write_bytes(registry.read_bytes())
        checked = ROUTES.reject_symlink_traversal
        swapped = False

        def check(root, path, **kwargs):
            nonlocal swapped
            checked(root, path, **kwargs)
            if path == ".agents/roles/registry.json" and not swapped:
                swapped = True
                replaced = registry.parent if parent else registry
                replaced.rename(replaced.with_name(replaced.name + "-original"))
                replaced.symlink_to(outside if parent else sentinel)

        with mock.patch.object(ROUTES, "reject_symlink_traversal", side_effect=check):
            with self.assertRaises(ROUTES.ContractError):
                ROUTES.reject_symlink_traversal(self.root, ".claude/skills/example")
        self.assertTrue(swapped)

    def test_registry_leaf_swap_after_path_check_is_rejected(self):
        self.assert_registry_swap_rejected(parent=False)

    def test_registry_parent_swap_after_path_check_is_rejected(self):
        self.assert_registry_swap_rejected(parent=True)

    def test_registry_duplicate_keys_are_rejected(self):
        registry = self.root / ".agents/roles/registry.json"
        original = json.loads(registry.read_text())
        registry.write_text(
            '{"skills":[],"skills":' + json.dumps(original["skills"]) + "}"
        )
        with self.assertRaises(ROUTES.ContractError) as raised:
            ROUTES.reject_symlink_traversal(self.root, ".claude/skills/example")
        self.assertEqual(raised.exception.code, "SURFACE-JSON-DUPLICATE-KEY")

    def test_registry_read_has_a_finite_byte_budget(self):
        with mock.patch.object(ROUTES, "MAX_JSON_INPUT_BYTES", 8):
            with self.assertRaises(ROUTES.ContractError) as raised:
                ROUTES.reject_symlink_traversal(self.root, ".claude/skills/example")
        self.assertEqual(raised.exception.code, "SURFACE-JSON")

    def test_adapter_rejects_escape_alias_and_unregistered_package(self):
        for path, target in (
            ("example", "/tmp/outside"),
            ("alias", "../../.agents/skills/example"),
            ("unregistered", "../../.agents/skills/unregistered"),
        ):
            with self.subTest(path=path, target=target):
                link = self.link.parent / path
                if link.is_symlink():
                    link.unlink()
                link.symlink_to(target)
                with self.assertRaises(ROUTES.ContractError) as raised:
                    ROUTES.reject_symlink_traversal(
                        self.root, link.relative_to(self.root).as_posix()
                    )
                self.assertEqual(raised.exception.code, "SURFACE-PATH-SYMLINK")

    def test_whole_directory_adapter_is_retired(self):
        self.link.unlink()
        self.link.parent.rmdir()
        self.link.parent.symlink_to("../docs/00.agent-governance/skills")
        with self.assertRaises(ROUTES.ContractError) as raised:
            ROUTES.reject_symlink_traversal(self.root, ".claude/skills")
        self.assertEqual(raised.exception.code, "SURFACE-PATH-SYMLINK")

    def test_registered_target_must_exist_without_symlink_parents(self):
        self.skill.unlink()
        with self.assertRaises(ROUTES.ContractError):
            ROUTES.reject_symlink_traversal(self.root, ".claude/skills/example")
        self.skill.parent.rmdir()
        self.skill.parent.symlink_to("../../outside")
        with self.assertRaises(ROUTES.ContractError):
            ROUTES.reject_symlink_traversal(self.root, ".claude/skills/example")


if __name__ == "__main__":
    unittest.main()
