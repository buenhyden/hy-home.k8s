from __future__ import annotations

import copy
import importlib.util
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate-agent-governance.py"


def load_validator():
    specification = importlib.util.spec_from_file_location(
        "agent_registry_test_target", VALIDATOR_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError("agent registry validator could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    sys.path.insert(0, str(VALIDATOR_PATH.parent))
    try:
        specification.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


class AgentRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.registry = cls.validator.load_json(
            REPOSITORY_ROOT, cls.validator.REGISTRY_PATH
        )

    def registry_copy(self):
        return copy.deepcopy(self.registry)

    def assert_rule(self, registry, code: str) -> None:
        with self.assertRaises(self.validator.HarnessError) as raised:
            self.validator.validate_registry(
                REPOSITORY_ROOT, registry, check_files=False
            )
        self.assertEqual(raised.exception.code, code)

    def test_role_skill_assignments_preserve_domain_and_read_only_boundaries(self):
        roles = {row["id"]: row for row in self.registry["roles"]}
        for role, inappropriate in (
            ("network-reviewer", "k8s-security-audit"),
            ("observability-reviewer", "ops-runbook"),
            ("ci-workflow-engineer", "vulnerability-patterns"),
            ("agent-evaluator", "workspace-harness-audit"),
        ):
            with self.subTest(role=role):
                self.assertNotIn(inappropriate, roles[role]["skill_refs"])
        self.assertEqual(roles["agent-evaluator"]["skill_refs"], [])

    def test_third_provider_is_rejected(self) -> None:
        mutated = self.registry_copy()
        mutated["providers"].append(
            {
                "id": "gemini",
                "gateway": "GEMINI.md",
                "projection_root": ".gemini/agents",
            }
        )
        self.assert_rule(mutated, "AGENT-REGISTRY-SCHEMA")

    def test_duplicate_role_owner_is_rejected(self) -> None:
        mutated = self.registry_copy()
        mutated["roles"].append(copy.deepcopy(mutated["roles"][0]))
        self.assert_rule(mutated, "AGENT-REGISTRY-ROLE")

    def test_unknown_permission_class_is_rejected(self) -> None:
        mutated = self.registry_copy()
        mutated["roles"][0]["permission_class"] = "unbounded-write"
        self.assert_rule(mutated, "AGENT-REGISTRY-PERMISSION")

    def test_native_scope_override_may_narrow_its_permission_class(self) -> None:
        mutated = self.registry_copy()
        role = next(item for item in mutated["roles"] if item["id"] == "code-reviewer")
        role["native_scope_override"] = {"claude": ["Read", "Grep"]}
        self.validator.validate_registry(REPOSITORY_ROOT, mutated, check_files=False)

    def test_native_scope_override_cannot_widen_its_permission_class(self) -> None:
        mutated = self.registry_copy()
        role = next(item for item in mutated["roles"] if item["id"] == "code-reviewer")
        role["native_scope_override"] = {"claude": ["Read", "Grep", "WebSearch"]}
        self.assert_rule(mutated, "AGENT-REGISTRY-PERMISSION")

    def test_unknown_handoff_is_rejected(self) -> None:
        mutated = self.registry_copy()
        mutated["roles"][0]["handoff_to"].append("unknown-role")
        self.assert_rule(mutated, "AGENT-REGISTRY-HANDOFF")

    def test_duplicate_skill_identity_is_rejected(self) -> None:
        mutated = self.registry_copy()
        mutated["skills"].append(copy.deepcopy(mutated["skills"][0]))
        self.assert_rule(mutated, "AGENT-REGISTRY-SKILL")

    def test_retired_skill_and_neutral_role_paths_are_rejected(self) -> None:
        for collection, key, value in (
            ("skills", "path", "docs/00.agent-governance/skills/risk-report/SKILL.md"),
            (
                "roles",
                "capability_tier_ref",
                "docs/00.agent-governance/policies/model-selection.md#top",
            ),
        ):
            with self.subTest(collection=collection):
                mutated = self.registry_copy()
                mutated[collection][0][key] = value
                self.assert_rule(mutated, "AGENT-REGISTRY-SCHEMA")

    def test_unknown_skill_reference_is_rejected(self) -> None:
        mutated = self.registry_copy()
        mutated["roles"][0]["skill_refs"].append("unknown-skill")
        self.assert_rule(mutated, "AGENT-REGISTRY-SKILL")

    def test_projection_outside_provider_root_is_rejected(self) -> None:
        mutated = self.registry_copy()
        mutated["roles"][0]["projections"]["claude"] = ".agents/agents/supervisor.md"
        self.assert_rule(mutated, "AGENT-REGISTRY-SCHEMA")

    def test_extra_registry_metadata_is_rejected(self) -> None:
        mutated = self.registry_copy()
        mutated["runtime_discovered"] = True
        self.assert_rule(mutated, "AGENT-REGISTRY-SCHEMA")

    def test_repo_static_runtime_claim_is_rejected(self) -> None:
        mutated = self.registry_copy()
        mutated["roles"][0]["responsibility"] = (
            "Authenticated provider execution was discovered and verified."
        )
        self.assert_rule(mutated, "AGENT-REGISTRY-EVIDENCE")


class CapabilityModelBindingTests(unittest.TestCase):
    """Every projection carries the model its role's capability tier declares."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.registry = cls.validator.load_json(
            REPOSITORY_ROOT, cls.validator.REGISTRY_PATH
        )

    def test_a_model_departure_is_declared_rather_than_implied(self) -> None:
        bindings = {
            provider["id"]: provider["capability_models"]
            for provider in self.registry["providers"]
        }
        for role in self.registry["roles"]:
            tier = role["capability_tier_ref"].rsplit("#", 1)[-1]
            declared = role.get("native_model_override", {})
            for provider in role["supported_providers"]:
                resolved = self.validator._bound_model(self.registry, role, provider)
                with self.subTest(role=role["id"], provider=provider):
                    self.assertEqual(
                        resolved, declared.get(provider, bindings[provider][tier])
                    )

    def test_a_model_override_replaces_only_its_own_provider(self) -> None:
        role = {
            "capability_tier_ref": ".agents/governance/model-selection.md#worker",
            "native_model_override": {"codex": "override-model"},
        }
        bindings = {
            provider["id"]: provider["capability_models"]["worker"]
            for provider in self.registry["providers"]
        }
        self.assertEqual(
            self.validator._bound_model(self.registry, role, "codex"), "override-model"
        )
        self.assertEqual(
            self.validator._bound_model(self.registry, role, "claude"),
            bindings["claude"],
        )

    def test_a_claude_model_override_replaces_only_claude(self) -> None:
        role = {
            "capability_tier_ref": ".agents/governance/model-selection.md#worker",
            "native_model_override": {"claude": "fable"},
        }
        codex_worker = next(
            provider["capability_models"]["worker"]
            for provider in self.registry["providers"]
            if provider["id"] == "codex"
        )
        self.assertEqual(
            self.validator._bound_model(self.registry, role, "claude"), "fable"
        )
        self.assertEqual(
            self.validator._bound_model(self.registry, role, "codex"), codex_worker
        )


class CodexReasoningBindingTests(unittest.TestCase):
    """Every projected reasoning effort resolves from the registry."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.registry = cls.validator.load_json(
            REPOSITORY_ROOT, cls.validator.REGISTRY_PATH
        )

    def test_a_departure_is_declared_rather_than_implied(self) -> None:
        binding = next(
            entry["capability_reasoning"]
            for entry in self.registry["providers"]
            if entry["id"] == "codex"
        )
        for role in self.registry["roles"]:
            tier = role["capability_tier_ref"].rsplit("#", 1)[-1]
            declared = role.get("native_reasoning_override", {}).get("codex")
            resolved = self.validator._bound_reasoning(self.registry, role)
            with self.subTest(role=role["id"]):
                if declared is None:
                    self.assertEqual(resolved, binding[tier])
                else:
                    self.assertEqual(resolved, declared)


class ClaudeReasoningBindingTests(unittest.TestCase):
    """Every Claude projection's effort resolves from the registry."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.registry = cls.validator.load_json(
            REPOSITORY_ROOT, cls.validator.REGISTRY_PATH
        )

    def test_a_claude_effort_override_replaces_only_claude(self) -> None:
        role = {
            "capability_tier_ref": ".agents/governance/model-selection.md#top",
            "native_reasoning_override": {"claude": "medium"},
        }
        codex_top = next(
            entry["capability_reasoning"]["top"]
            for entry in self.registry["providers"]
            if entry["id"] == "codex"
        )
        self.assertEqual(
            self.validator._bound_reasoning(self.registry, role, "claude"), "medium"
        )
        self.assertEqual(
            self.validator._bound_reasoning(self.registry, role), codex_top
        )


if __name__ == "__main__":
    unittest.main()
