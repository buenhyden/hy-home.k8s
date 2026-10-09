from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import sys
import tempfile
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

    def test_native_binding_path_is_exact_provider_owner(self) -> None:
        mutated = self.registry_copy()
        mutated["providers"][0]["bindings"] = "../untrusted/bindings.json"
        self.assert_rule(mutated, "AGENT-REGISTRY-SCHEMA")

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
        cls.bindings = cls.validator.load_provider_bindings(
            REPOSITORY_ROOT, cls.registry
        )

    def test_a_model_departure_is_declared_rather_than_implied(self) -> None:
        for role in self.registry["roles"]:
            tier = role["capability_tier_ref"].rsplit("#", 1)[-1]
            for provider in role["supported_providers"]:
                resolved = self.validator._bound_model(self.bindings, role, provider)
                binding = self.bindings[provider]
                with self.subTest(role=role["id"], provider=provider):
                    self.assertEqual(
                        resolved,
                        binding["role_overrides"]
                        .get(role["id"], {})
                        .get("model", binding["capability_models"][tier]),
                    )

    def test_a_model_override_replaces_only_its_own_provider(self) -> None:
        role = {
            "id": "synthetic-model-departure",
            "capability_tier_ref": ".agents/governance/model-selection.md#worker",
        }
        bindings = copy.deepcopy(self.bindings)
        bindings["codex"]["role_overrides"][role["id"]] = {"model": "override-model"}
        self.assertEqual(
            self.validator._bound_model(bindings, role, "codex"), "override-model"
        )
        self.assertEqual(
            self.validator._bound_model(bindings, role, "claude"),
            bindings["claude"]["capability_models"]["worker"],
        )

    def test_a_claude_model_override_replaces_only_claude(self) -> None:
        role = {
            "id": "synthetic-claude-model-departure",
            "capability_tier_ref": ".agents/governance/model-selection.md#worker",
        }
        bindings = copy.deepcopy(self.bindings)
        bindings["claude"]["role_overrides"][role["id"]] = {"model": "fable"}
        self.assertEqual(self.validator._bound_model(bindings, role, "claude"), "fable")
        self.assertEqual(
            self.validator._bound_model(bindings, role, "codex"),
            bindings["codex"]["capability_models"]["worker"],
        )


class CodexReasoningBindingTests(unittest.TestCase):
    """Every projected reasoning effort resolves from the registry."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.registry = cls.validator.load_json(
            REPOSITORY_ROOT, cls.validator.REGISTRY_PATH
        )
        cls.bindings = cls.validator.load_provider_bindings(
            REPOSITORY_ROOT, cls.registry
        )

    def test_a_departure_is_declared_rather_than_implied(self) -> None:
        binding = self.bindings["codex"]
        for role in self.registry["roles"]:
            tier = role["capability_tier_ref"].rsplit("#", 1)[-1]
            declared = (
                binding["role_overrides"].get(role["id"], {}).get("reasoning_effort")
            )
            resolved = self.validator._bound_reasoning(self.bindings, role)
            with self.subTest(role=role["id"]):
                if declared is None:
                    self.assertEqual(resolved, binding["capability_reasoning"][tier])
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
        cls.bindings = cls.validator.load_provider_bindings(
            REPOSITORY_ROOT, cls.registry
        )

    def test_a_claude_effort_override_replaces_only_claude(self) -> None:
        role = {
            "id": "synthetic-claude-reasoning-departure",
            "capability_tier_ref": ".agents/governance/model-selection.md#top",
        }
        bindings = copy.deepcopy(self.bindings)
        bindings["claude"]["role_overrides"][role["id"]] = {
            "reasoning_effort": "medium"
        }
        self.assertEqual(
            self.validator._bound_reasoning(bindings, role, "claude"), "medium"
        )
        self.assertEqual(
            self.validator._bound_reasoning(bindings, role),
            bindings["codex"]["capability_reasoning"]["top"],
        )


class ProviderBindingLoaderTests(unittest.TestCase):
    """Provider-owned native values cannot widen the neutral role authority."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.registry = cls.validator.load_json(
            REPOSITORY_ROOT, cls.validator.REGISTRY_PATH
        )

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory(prefix="agent-native-binding-")
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        sources = (
            self.validator.REGISTRY_SCHEMA_PATH,
            *(Path(provider["bindings"]) for provider in self.registry["providers"]),
        )
        for source in sources:
            target = self.root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPOSITORY_ROOT / source, target)

    def binding_path(self, provider: str) -> Path:
        return self.root / next(
            row["bindings"]
            for row in self.registry["providers"]
            if row["id"] == provider
        )

    def mutate_binding(self, provider: str, change) -> None:
        path = self.binding_path(provider)
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def assert_binding_rule(self, code: str) -> None:
        with self.assertRaises(self.validator.HarnessError) as raised:
            self.validator.load_provider_bindings(self.root, self.registry)
        self.assertEqual(raised.exception.code, code)

    def test_current_tables_bind_without_widening_and_keep_advisory_bash(self) -> None:
        bindings = self.validator.load_provider_bindings(self.root, self.registry)
        self.assertEqual(
            set(bindings), {row["id"] for row in self.registry["providers"]}
        )
        self.assertIn(
            "Bash", bindings["claude"]["permission_scopes"]["read-only-evidence"]
        )
        self.assertEqual(
            bindings["codex"]["permission_scopes"]["read-only-evidence"],
            "read-only",
        )

    def test_narrower_codex_class_scope_is_valid(self) -> None:
        self.mutate_binding(
            "codex",
            lambda data: data["permission_scopes"].__setitem__(
                "scoped-authoring", "read-only"
            ),
        )
        self.assertEqual(
            self.validator.load_provider_bindings(self.root, self.registry)["codex"][
                "permission_scopes"
            ]["scoped-authoring"],
            "read-only",
        )

    def test_provider_scope_cannot_widen_read_only_class(self) -> None:
        for provider, scope in (
            ("claude", ["Read", "Grep", "Glob", "Bash", "Write"]),
            ("codex", "workspace-write"),
        ):
            with self.subTest(provider=provider):
                original = self.binding_path(provider).read_bytes()
                self.mutate_binding(
                    provider,
                    lambda data: data["permission_scopes"].__setitem__(
                        "read-only-evidence", scope
                    ),
                )
                self.assert_binding_rule("AGENT-NATIVE-PERMISSION")
                self.binding_path(provider).write_bytes(original)

    def test_unknown_role_override_and_skill_policy_type_reject(self) -> None:
        for provider, policy in (
            ("claude", "disable-model-invocation"),
            ("codex", "allow_implicit_invocation"),
        ):
            with self.subTest(provider=provider):
                path = self.binding_path(provider)
                original = path.read_bytes()
                self.mutate_binding(
                    provider,
                    lambda data: data["role_overrides"].__setitem__(
                        "unknown-role", {"model": "unowned"}
                    ),
                )
                self.assert_binding_rule("AGENT-NATIVE-BINDING")
                path.write_bytes(original)
                self.mutate_binding(
                    provider,
                    lambda data: data["skill_policy"].__setitem__(policy, "false"),
                )
                self.assert_binding_rule("AGENT-NATIVE-BINDING")
                path.write_bytes(original)

    def test_role_override_cannot_widen_read_only_class(self) -> None:
        for provider, scope in (
            ("claude", ["Read", "Grep", "Glob", "Bash", "Write"]),
            ("codex", "workspace-write"),
        ):
            with self.subTest(provider=provider):
                path = self.binding_path(provider)
                original = path.read_bytes()
                self.mutate_binding(
                    provider,
                    lambda data: data["role_overrides"].__setitem__(
                        "code-reviewer", {"scope": scope}
                    ),
                )
                self.assert_binding_rule("AGENT-NATIVE-PERMISSION")
                path.write_bytes(original)

    def test_wrong_provider_and_duplicate_json_key_reject(self) -> None:
        path = self.binding_path("codex")
        original = path.read_bytes()
        self.mutate_binding(
            "codex", lambda data: data.__setitem__("provider", "claude")
        )
        self.assert_binding_rule("AGENT-NATIVE-BINDING")
        path.write_bytes(original)
        path.write_text(
            path.read_text().replace(
                '"provider":', '"provider": "codex", "provider":', 1
            )
        )
        self.assert_binding_rule("AGENT-REGISTRY-INPUT")
        path.write_bytes(original)

    def test_missing_or_symlinked_binding_rejects(self) -> None:
        path = self.binding_path("codex")
        original = path.read_bytes()
        path.unlink()
        self.assert_binding_rule("AGENT-NATIVE-BINDING")
        path.symlink_to(self.binding_path("claude"))
        self.assert_binding_rule("AGENT-NATIVE-BINDING")
        path.unlink()
        path.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
