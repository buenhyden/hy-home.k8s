"""Independent structural contracts for Spec 0066 validation ownership."""

from __future__ import annotations

import ast
import json
import re
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
REGISTRY = SCRIPTS / "validation" / "registry.json"
TRANSITION_WRAPPERS = (
    "agent_registry_compat.py",
    "validate-agent-evaluations.py",
    "validate-agent-governance-closure.py",
    "validate-agent-model-fitness.py",
    "validate-agent-roster-admission.py",
    "validate-agent-roster-currentness.py",
)
TRANSITION_VALIDATORS = {
    "agent-evaluations",
    "agent-governance-closure",
    "agent-model-fitness",
    "agent-roster-admission",
    "agent-roster-currentness",
}
MUTABLE_CURRENT_IDENTIFIERS = (
    "BASELINE_SHA",
    "SUMMARY_RUN_SHA256",
    "PROVIDER_EVIDENCE_AGGREGATE_SHA256",
    "EXPECTED_CI_PYTHON_LOCK_SHA256",
)
TEST_ONLY_PRODUCTION_HELPERS = {
    "validate-github-actions-security.py": {
        "_write_self_test_case",
        "_write_artifact_retention_case",
        "_write_artifact_retention_shape_case",
        "_run_repository_boundary_case",
        "_write_required_write_case",
        "_write_uses_shape_case",
    },
    "validate-gitops-change-set.py": {
        "_create_non_regular_fixture",
        "_expect_self_test_error",
        "_write_self_test_case",
        "_render_self_test_case",
        "_run_self_test_git",
        "_self_test_boundaries",
    },
    "validate-vault-eso-contracts.py": {
        "_valid_contracts",
        "_apply_fixture_mutation",
        "_contract_diagnostics",
        "_load_fixture_cases",
        "_run_internal_boundaries",
    },
}


def top_level_function_names(tree: ast.Module) -> set[str]:
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def directly_called_names(tree: ast.Module) -> set[str]:
    return {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }


def production_sources() -> tuple[Path, ...]:
    return tuple(
        sorted(
            path
            for path in SCRIPTS.rglob("*")
            if path.is_file() and path.suffix in {".py", ".sh"}
        )
    )


class ValidationToolingOwnershipTests(unittest.TestCase):
    def test_native_shell_hooks_share_existing_shell_validation(self) -> None:
        config = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text())
        hooks = {hook["id"]: hook for repo in config["repos"] for hook in repo["hooks"]}
        for identifier in ("shellcheck", "shfmt"):
            pattern = re.compile(hooks[identifier]["files"])
            with self.subTest(hook=identifier):
                self.assertIsNotNone(pattern.search(".claude/hooks/k8s-pre-edit.sh"))
                self.assertIsNotNone(pattern.search("scripts/check-secret-handling.sh"))
                self.assertIsNone(pattern.search(".claude/settings.local.json"))

    def test_production_clis_do_not_embed_self_test_modes(self) -> None:
        offenders = [
            path.relative_to(ROOT).as_posix()
            for path in production_sources()
            if "--self-test" in path.read_text(encoding="utf-8")
        ]
        self.assertEqual(offenders, [])

    def test_production_sources_do_not_depend_on_top_level_tests(self) -> None:
        offenders: list[str] = []
        for path in production_sources():
            text = path.read_text(encoding="utf-8")
            if path.suffix == ".sh":
                if re.search(
                    r"(?:open|read_text|read_bytes|load_json)\([^\n]*tests/",
                    text,
                ):
                    offenders.append(path.relative_to(ROOT).as_posix())
                continue
            tree = ast.parse(text, filename=str(path))
            imported_tests = any(
                (
                    isinstance(node, ast.Import)
                    and any(
                        alias.name == "tests" or alias.name.startswith("tests.")
                        for alias in node.names
                    )
                )
                or (
                    isinstance(node, ast.ImportFrom)
                    and bool(node.module)
                    and (node.module == "tests" or node.module.startswith("tests."))
                )
                for node in ast.walk(tree)
            )
            tainted_names: set[str] = set()
            for node in ast.walk(tree):
                if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                    continue
                value = node.value
                if value is None or not any(
                    isinstance(child, ast.Constant)
                    and isinstance(child.value, str)
                    and child.value.startswith("tests/")
                    for child in ast.walk(value)
                ):
                    continue
                targets = (
                    node.targets if isinstance(node, ast.Assign) else [node.target]
                )
                tainted_names.update(
                    target.id for target in targets if isinstance(target, ast.Name)
                )

            def references_tests(node: ast.AST) -> bool:
                return any(
                    (
                        isinstance(child, ast.Constant)
                        and isinstance(child.value, str)
                        and child.value.startswith("tests/")
                    )
                    or (isinstance(child, ast.Name) and child.id in tainted_names)
                    for child in ast.walk(node)
                )

            reads_tests = False
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                function = node.func
                name = function.id if isinstance(function, ast.Name) else ""
                attribute = function.attr if isinstance(function, ast.Attribute) else ""
                if name not in {
                    "open",
                    "load_json",
                    "load_json_document",
                } and attribute not in {
                    "open",
                    "read_bytes",
                    "read_text",
                }:
                    continue
                if references_tests(node):
                    reads_tests = True
                    break
            if imported_tests or reads_tests:
                offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(offenders, [])

    def test_transition_wrappers_and_registry_aliases_are_absent(self) -> None:
        wrappers = [name for name in TRANSITION_WRAPPERS if (SCRIPTS / name).exists()]
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        validators = {row["id"] for row in registry["validators"]}
        self.assertEqual(wrappers, [])
        self.assertEqual(sorted(validators & TRANSITION_VALIDATORS), [])

    def test_current_state_sha_and_generated_digest_identifiers_are_absent(
        self,
    ) -> None:
        offenders: dict[str, list[str]] = {}
        for path in production_sources():
            text = path.read_text(encoding="utf-8")
            present = [name for name in MUTABLE_CURRENT_IDENTIFIERS if name in text]
            if present:
                offenders[path.relative_to(ROOT).as_posix()] = present
        self.assertEqual(offenders, {})

    def test_subprocess_run_calls_declare_a_timeout(self) -> None:
        offenders: list[str] = []
        for path in production_sources():
            if path.suffix != ".py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call):
                    continue
                function = node.func
                if not (
                    isinstance(function, ast.Attribute)
                    and isinstance(function.value, ast.Name)
                    and function.value.id == "subprocess"
                    and function.attr in {"run", "check_call", "check_output"}
                ):
                    continue
                if not any(keyword.arg == "timeout" for keyword in node.keywords):
                    offenders.append(
                        f"{path.relative_to(ROOT).as_posix()}:{node.lineno}"
                    )
        self.assertEqual(offenders, [])

    def test_every_test_fixture_has_an_independent_test_consumer(self) -> None:
        test_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "tests").glob("test_*.py"))
        )
        fixture_root = ROOT / "tests" / "fixtures"

        def has_consumer(path: Path) -> bool:
            relative = path.relative_to(fixture_root)
            candidates = (relative, *relative.parents)
            return any(
                candidate != Path(".")
                and (
                    f"tests/fixtures/{candidate.as_posix()}" in test_text
                    or f"fixtures/{candidate.as_posix()}" in test_text
                )
                for candidate in candidates
            )

        orphans = [
            path.relative_to(ROOT).as_posix()
            for path in sorted(fixture_root.rglob("*"))
            if path.is_file() and not has_consumer(path)
        ]
        self.assertEqual(orphans, [])

    def test_production_validators_do_not_own_test_case_builders(self) -> None:
        offenders: dict[str, list[str]] = {}
        for filename, forbidden in TEST_ONLY_PRODUCTION_HELPERS.items():
            path = SCRIPTS / filename
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            present = sorted(
                node.name
                for node in ast.walk(tree)
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                and node.name in forbidden
            )
            if present:
                offenders[filename] = present
        self.assertEqual(offenders, {})

    def test_test_called_mutation_helpers_are_not_production_only_dead_code(
        self,
    ) -> None:
        test_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((ROOT / "tests").glob("test_*.py"))
        )
        offenders: dict[str, list[str]] = {}
        for path in production_sources():
            if path.suffix != ".py":
                continue
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            defined = top_level_function_names(tree)
            called = directly_called_names(tree)
            test_only = sorted(
                name
                for name in defined - called
                if "mutation" in name
                and re.search(rf"(?:\.|\b){re.escape(name)}\(", test_text)
            )
            if test_only:
                offenders[path.relative_to(ROOT).as_posix()] = test_only
        self.assertEqual(offenders, {})

    def test_repository_aggregate_dispatches_without_embedded_rule_logic(self) -> None:
        aggregate = (SCRIPTS / "validate-repo-quality-gates.sh").read_text(
            encoding="utf-8"
        )
        self.assertNotIn("<<'PY'", aggregate)
        self.assertNotIn("<<PY", aggregate)
        self.assertEqual(
            aggregate.count("scripts/run-validation-lane.py"),
            1,
        )
        self.assertIn("--lane all-files", aggregate)
        embedded_validators = re.findall(
            r"scripts/(?:validate-[a-z0-9-]+\.(?:py|sh)|archive_cutover\.py)",
            aggregate,
        )
        self.assertEqual(
            [
                path
                for path in embedded_validators
                if path != "scripts/validate-repo-quality-gates.sh"
            ],
            [],
        )

        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        quality = next(
            row for row in registry["validators"] if row["id"] == "repository-quality"
        )
        self.assertEqual(
            quality["argv"],
            [
                "python3",
                "scripts/validation/repository/quality.py",
                "--root",
                ".",
            ],
        )

    def test_full_qa_has_one_quality_gate_without_duplicate_pre_commit_hooks(
        self,
    ) -> None:
        pre_commit = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(registry["profiles"]["full"].count("repository-quality"), 1)
        self.assertEqual(registry["profiles"]["full"].count("pre-commit"), 1)
        for duplicate in (
            "id: strict-repository-quality",
            "id: validate-agent-governance-ci",
            "id: validate-agent-legacy-cutover",
            "id: validate-affected-surfaces",
        ):
            self.assertNotIn(duplicate, pre_commit)

    def test_repository_quality_does_not_require_readme_inventory_ledgers(self) -> None:
        owner = (SCRIPTS / "validation" / "repository" / "quality.py").read_text(
            encoding="utf-8"
        )
        legacy_ledgers = (
            "Script Inventory",
            "Script Classification Matrix",
            "Kube-linter Exclusion Matrix",
        )
        self.assertEqual(
            [heading for heading in legacy_ledgers if heading in owner],
            [],
        )

    def test_repository_quality_delegates_agent_summary_semantics(self) -> None:
        owner = (SCRIPTS / "validation" / "repository" / "quality.py").read_text(
            encoding="utf-8"
        )
        delegated_markers = (
            "AGENT_GOVERNANCE_STATIC_SELECTED",
            'case "$branch_policy_selected:$BRANCH_POLICY_RESULT" in',
            "one or more required CI gates failed closed",
        )
        self.assertEqual(
            [marker for marker in delegated_markers if marker in owner],
            [],
        )


if __name__ == "__main__":
    unittest.main()
