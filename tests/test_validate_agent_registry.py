from __future__ import annotations

import copy
import importlib.util
import os
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


class ForbiddenAgentProviderSurfaceTests(unittest.TestCase):
    def test_forbidden_provider_surfaces_are_absent(self) -> None:
        forbidden = (
            REPOSITORY_ROOT / ".gemini",
            REPOSITORY_ROOT / "GEMINI.md",
            REPOSITORY_ROOT / ".agents" / "GEMINI.md",
            REPOSITORY_ROOT
            / "docs"
            / "00.agent-governance"
            / "providers"
            / "gemini.md",
        )
        self.assertEqual(
            [
                path.relative_to(REPOSITORY_ROOT).as_posix()
                for path in forbidden
                if os.path.lexists(path)
            ],
            [],
            "AGENT-PROVIDER-FORBIDDEN: retired provider surface remains",
        )


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

    def test_production_registry_is_the_closed_two_provider_authority(self) -> None:
        counts = self.validator.validate_registry(REPOSITORY_ROOT)
        role_ids = [item["id"] for item in self.registry["roles"]]
        skill_ids = [item["id"] for item in self.registry["skills"]]
        self.assertEqual(
            counts,
            {
                "providers": 2,
                "roles": len(role_ids),
                "permissionClasses": len(self.registry["permission_classes"]),
                "skills": len(skill_ids),
                "handoffs": sum(
                    len(item["handoff_to"]) for item in self.registry["roles"]
                ),
                "projections": sum(
                    len(item["projections"]) for item in self.registry["roles"]
                ),
            },
        )
        self.assertEqual(len(role_ids), len(set(role_ids)))
        self.assertEqual(len(skill_ids), len(set(skill_ids)))
        self.assertEqual(
            tuple(item["id"] for item in self.registry["providers"]),
            ("claude", "codex"),
        )

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

    def _projection_model(self, provider: str, relative: str) -> str:
        text = (REPOSITORY_ROOT / relative).read_text(encoding="utf-8")
        if provider == "claude":
            return self.validator._frontmatter(text)[0].get("model", "")
        return self.validator.tomllib.loads(text).get("model", "")

    def test_every_provider_declares_a_model_for_every_tier(self) -> None:
        tiers = {
            role["capability_tier_ref"].rsplit("#", 1)[-1]
            for role in self.registry["roles"]
        }
        for provider in self.registry["providers"]:
            with self.subTest(provider=provider["id"]):
                self.assertEqual(set(provider.get("capability_models", {})), tiers)

    def test_every_projection_model_matches_its_tier_binding(self) -> None:
        bindings = {
            provider["id"]: provider.get("capability_models", {})
            for provider in self.registry["providers"]
        }
        drift = []
        for role in self.registry["roles"]:
            tier = role["capability_tier_ref"].rsplit("#", 1)[-1]
            for provider in role["supported_providers"]:
                expected = bindings[provider].get(tier)
                observed = self._projection_model(
                    provider, role["projections"][provider]
                )
                if observed != expected:
                    drift.append(f"{role['id']}/{provider}: {observed} != {expected}")
        self.assertEqual(drift, [])


class CodexSandboxScopeTests(unittest.TestCase):
    """Codex projections declare a structured scope, not prose alone."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.registry = cls.validator.load_json(
            REPOSITORY_ROOT, cls.validator.REGISTRY_PATH
        )

    def test_codex_declares_a_sandbox_scope_for_every_permission_class(self) -> None:
        codex = next(
            provider
            for provider in self.registry["providers"]
            if provider["id"] == "codex"
        )
        declared = {entry["id"] for entry in self.registry["permission_classes"]}
        self.assertEqual(set(codex.get("permission_scopes", {})), declared)

    def test_every_codex_projection_carries_its_bound_sandbox_scope(self) -> None:
        codex = next(
            provider
            for provider in self.registry["providers"]
            if provider["id"] == "codex"
        )
        scopes = codex.get("permission_scopes", {})
        missing = []
        for role in self.registry["roles"]:
            if "codex" not in role["supported_providers"]:
                continue
            data = self.validator.tomllib.loads(
                (REPOSITORY_ROOT / role["projections"]["codex"]).read_text(
                    encoding="utf-8"
                )
            )
            expected = scopes.get(role["permission_class"])
            if data.get("sandbox_mode") != expected:
                missing.append(
                    f"{role['id']}: {data.get('sandbox_mode')!r} != {expected!r}"
                )
        self.assertEqual(missing, [])


class CodexReasoningBindingTests(unittest.TestCase):
    """Every projected reasoning effort resolves from the registry."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.registry = cls.validator.load_json(
            REPOSITORY_ROOT, cls.validator.REGISTRY_PATH
        )

    def test_every_projection_matches_its_registry_binding(self) -> None:
        import tomllib

        mismatched = []
        for role in self.registry["roles"]:
            bound = self.validator._bound_reasoning(self.registry, role)
            projection = REPOSITORY_ROOT / role["projections"]["codex"]
            observed = tomllib.loads(projection.read_text(encoding="utf-8")).get(
                "model_reasoning_effort"
            )
            if observed != bound:
                mismatched.append((role["id"], bound, observed))

        self.assertEqual(mismatched, [])

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


if __name__ == "__main__":
    unittest.main()
