"""Independent fixture tests for affected-surface routing."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.affected_surface_mutations import apply_mutation

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts/validate-affected-surfaces.py"
FIXTURE_PATH = ROOT / "tests/fixtures/validation-surfaces.json"


def load_validator():
    spec = importlib.util.spec_from_file_location(
        "validate_affected_surfaces", SCRIPT_PATH
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class AffectedSurfaceFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()
        cls.contract = cls.validator.validate_contract(ROOT)
        cls.fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))

    def test_surface_cases(self) -> None:
        for case in self.fixture["surfaceCases"]:
            with self.subTest(case=case["name"]):
                self.assertEqual(
                    self.validator.classify_path(self.contract, case["path"])["id"],
                    case["expectedSurface"],
                )

    def test_selection_cases(self) -> None:
        for case in self.fixture["selectionCases"]:
            with self.subTest(case=case["name"]):
                self.assertEqual(
                    self.validator.select_paths(
                        self.contract,
                        case["paths"],
                        case["lane"],
                        ROOT,
                    ),
                    case["expected"],
                )

    def test_authored_task_does_not_run_agent_projection_validator(self) -> None:
        result = self.validator.select_paths(
            self.contract,
            ["docs/03.specs/route-probe/tasks/task.md"],
            "affected",
            ROOT,
        )
        self.assertNotIn("agent-governance", result["validators"])
        self.assertIn("document-lifecycle", result["validators"])
        self.assertNotIn("repository-quality", result["validators"])

    def test_ordinary_documents_route_only_to_document_content_checks(self) -> None:
        expected = [
            "document-contract-registry",
            "document-lifecycle",
            "links-and-owners",
            "markdown-profiles",
            "selected-nonstyle",
            "selected-style",
        ]
        for path in (
            "docs/03.specs/route-probe/spec.md",
            "README.md",
            "infrastructure/README.md",
            "gitops/workloads/README.md",
            "docs/99.templates/README.md",
            ".github/repository-surface.md",
            ".agents/evaluations/README.md",
            ".agents/evaluations/results.md",
            ".agents/evaluations/harnesses/route-probe/task.md",
            ".agents/evaluations/harnesses/route-probe/score.md",
        ):
            with self.subTest(path=path):
                selected = self.validator.select_paths(
                    self.contract, [path], "staged", ROOT
                )
                self.assertEqual(selected["validators"], expected)

    def test_contract_paths_keep_their_focused_gate_selection(self) -> None:
        for path, required in (
            ("docs/99.templates/registry.json", "agent-governance"),
            (
                "docs/99.templates/templates/evaluations/evaluation-task.template.md",
                "document-contract-registry",
            ),
            (".agents/governance/quality.md", "agent-governance"),
            (".codex/provider.md", "agent-governance"),
            ("gitops/clusters/local/root-application.yaml", "k8s-manifests"),
        ):
            with self.subTest(path=path):
                selected = self.validator.select_paths(
                    self.contract, [path], "staged", ROOT
                )
                self.assertIn(required, selected["validators"])

        mixed = self.validator.select_paths(
            self.contract,
            ["README.md", "gitops/clusters/local/root-application.yaml"],
            "staged",
            ROOT,
        )
        self.assertIn("document-contract-registry", mixed["validators"])
        self.assertIn("k8s-manifests", mixed["validators"])

    def test_selected_style_is_global_only_at_the_staged_boundary(self) -> None:
        for path in ("README.md", "gitops/clusters/local/root-application.yaml"):
            with self.subTest(path=path):
                staged = self.validator.select_paths(
                    self.contract, [path], "staged", ROOT
                )
                affected = self.validator.select_paths(
                    self.contract, [path], "affected", ROOT
                )
                self.assertIn("selected-style", staged["validators"])
                self.assertIn("selected-nonstyle", staged["validators"])
                self.assertNotIn("selected-style", affected["validators"])
                self.assertNotIn("selected-nonstyle", affected["validators"])
        self.assertIn("selected-style", self.contract["profiles"]["staged"])
        self.assertIn("selected-nonstyle", self.contract["profiles"]["staged"])
        self.assertNotIn("selected-style", self.contract["profiles"]["quick"])
        self.assertNotIn("selected-nonstyle", self.contract["profiles"]["quick"])

    def test_stage99_machine_contract_keeps_archive_gate_without_form_replay(
        self,
    ) -> None:
        for path in (
            "docs/99.templates/registry.json",
            "docs/99.templates/contracts/document-profile.schema.json",
        ):
            with self.subTest(path=path):
                selected = self.validator.select_paths(
                    self.contract, [path], "staged", ROOT
                )
                self.assertIn("archive-contract-tests", selected["validators"])
        form = self.validator.select_paths(
            self.contract,
            ["docs/99.templates/templates/evaluations/evaluation-task.template.md"],
            "staged",
            ROOT,
        )
        self.assertNotIn("archive-contract-tests", form["validators"])
        self.assertIn("document-contract-registry", form["validators"])

    def test_purpose_checks_follow_their_changed_surfaces_without_full_sweep(self):
        cases = (
            (
                ".github/workflows/ci.yml",
                {"ci-python-contract", "github-actions-security"},
            ),
            (".github/requirements/ci-validation.in", {"ci-python-contract"}),
            (
                "docs/98.archive/completed/03.specs/route-probe/spec.md",
                {"archive-integrity"},
            ),
            ("docs/99.templates/registry.json", {"affected-surface-contract"}),
            ("gitops/apps/root/kustomization.yaml", {"platform-assurance"}),
            ("_workspace/README.md", {"workspace-boundary"}),
        )
        for lane in ("affected", "staged"):
            for path, required in cases:
                with self.subTest(lane=lane, path=path):
                    selected = self.validator.select_paths(
                        self.contract, [path], lane, ROOT
                    )
                    self.assertTrue(required <= set(selected["validators"]))

    def test_only_selected_profiles_and_no_blanket_discovery_gate(self) -> None:
        self.assertEqual(set(self.contract["profiles"]), {"quick", "staged"})
        self.assertNotIn("profileAliases", self.contract)
        self.assertFalse(
            {"unit-tests", "pre-commit"}
            & {row["id"] for row in self.contract["validators"]}
        )
        self.assertFalse(any("coveredBy" in row for row in self.contract["validators"]))

    def test_root_changelog_uses_document_surface(self) -> None:
        self.assertEqual(
            self.validator.classify_path(self.contract, "CHANGELOG.md")["id"],
            "authored-documents",
        )

    def test_rejection_cases(self) -> None:
        for case in self.fixture["rejectionCases"]:
            with self.subTest(case=case["name"]):
                root = ROOT
                temporary = None
                if case["name"] in {"unmatched-tracked-path", "symlink-traversal"}:
                    temporary = tempfile.TemporaryDirectory(
                        prefix="affected-unmatched-"
                    )
                    self.addCleanup(temporary.cleanup)
                    root = Path(temporary.name)
                    target = root / case["paths"][0]
                    if case["name"] == "symlink-traversal":
                        target.parent.parent.mkdir(parents=True)
                        target.parent.symlink_to("../outside")
                    else:
                        target.parent.mkdir(parents=True)
                        target.write_text("unmatched\n", encoding="utf-8")
                with self.assertRaises(self.validator.ContractError) as raised:
                    self.validator.select_paths(
                        self.contract, case["paths"], "affected", root
                    )
                self.assertEqual(raised.exception.code, case["expectedError"])

    def test_direct_script_argv_cases(self) -> None:
        for case in self.fixture["argvPositiveCases"]:
            with self.subTest(case=case["name"]):
                mutated = copy.deepcopy(self.contract)
                apply_mutation(
                    mutated,
                    {
                        "kind": "replace-argv",
                        "validatorId": case["validatorId"],
                        "argv": case["argv"],
                    },
                )
                self.validator.validate_contract(ROOT, mutated)

    def test_mutation_cases(self) -> None:
        for case in self.fixture["mutationCases"]:
            with self.subTest(case=case["name"]):
                mutated = copy.deepcopy(self.contract)
                apply_mutation(mutated, case["mutation"])
                with self.assertRaises(self.validator.ContractError) as raised:
                    validated = self.validator.validate_contract(ROOT, mutated)
                    self.validator.select_paths(
                        validated, case["paths"], "affected", ROOT
                    )
                self.assertEqual(raised.exception.code, case["expectedError"])

    def test_optional_tool_requires_defer_and_next_owner(self) -> None:
        contract = copy.deepcopy(self.contract)
        validator = next(
            row for row in contract["validators"] if row["id"] == "ci-python-contract"
        )
        validator["optional"] = True
        validator["fallback"] = {
            "status": "DEFER",
            "reason": "tool unavailable",
            "nextOwner": "quality-engineer",
        }
        self.validator.validate_contract(ROOT, contract)
        del validator["fallback"]["nextOwner"]
        with self.assertRaises(self.validator.ContractError) as raised:
            self.validator.validate_contract(ROOT, contract)
        self.assertEqual(raised.exception.code, "SURFACE-FALLBACK")

    def test_ci_rename_range(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="affected-surface-ci-rename-"
        ) as directory:
            root = Path(directory)

            def git(*arguments: str, capture: bool = False) -> str:
                completed = subprocess.run(
                    ["git", *arguments],
                    cwd=root,
                    check=True,
                    stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=10,
                )
                return completed.stdout.strip() if capture else ""

            git("init", "--quiet")
            old_path = Path("gitops/rename-probe.yaml")
            new_path = Path("docs/03.specs/999-rename-probe/spec.md")
            old_target = root / old_path
            old_target.parent.mkdir(parents=True)
            old_target.write_text("kind: ConfigMap\n", encoding="utf-8")
            git("add", "--", old_path.as_posix())
            git(
                "-c",
                "user.name=CI Rename Probe",
                "-c",
                "user.email=ci-rename-probe@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "base",
            )
            base = git("rev-parse", "HEAD", capture=True)
            new_target = root / new_path
            new_target.parent.mkdir(parents=True)
            old_target.rename(new_target)
            git("add", "-A")
            git(
                "-c",
                "user.name=CI Rename Probe",
                "-c",
                "user.email=ci-rename-probe@example.invalid",
                "commit",
                "--quiet",
                "-m",
                "rename",
            )
            head = git("rev-parse", "HEAD", capture=True)
            completed = subprocess.run(
                ["git", "diff", "--no-renames", "--name-only", "-z", base, head],
                cwd=root,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
            )
            self.assertTrue(completed.stdout.endswith(b"\0"))
            self.assertEqual(
                {value.decode("utf-8") for value in completed.stdout[:-1].split(b"\0")},
                {old_path.as_posix(), new_path.as_posix()},
            )

    def test_nul_path_transport(self) -> None:
        with tempfile.TemporaryDirectory(prefix="affected-surface-") as directory:
            path = Path(directory) / "paths.nul"
            path.write_bytes(b"README.md\0gitops/README.md\0")
            self.assertEqual(
                self.validator.read_nul_paths(path),
                ["README.md", "gitops/README.md"],
            )
            path.write_bytes(b"README.md\n")
            with self.assertRaises(self.validator.ContractError) as raised:
                self.validator.read_nul_paths(path)
            self.assertEqual(raised.exception.code, "SURFACE-PATH-TRANSPORT")

    def test_nul_path_transport_rejects_fifo_oversize_and_invalid_utf8(self) -> None:
        with tempfile.TemporaryDirectory(prefix="affected-surface-input-") as directory:
            root = Path(directory)
            fifo = root / "paths.fifo"
            if hasattr(os, "mkfifo"):
                os.mkfifo(fifo)
                with self.assertRaises(self.validator.ContractError) as raised:
                    self.validator.read_nul_paths(fifo)
                self.assertEqual(raised.exception.code, "SURFACE-PATH-TRANSPORT")

            oversized = root / "oversized.nul"
            oversized.write_bytes(b"x" * (self.validator.MAX_PATH_INPUT_BYTES + 1))
            with self.assertRaises(self.validator.ContractError) as raised:
                self.validator.read_nul_paths(oversized)
            self.assertEqual(raised.exception.code, "SURFACE-PATH-TRANSPORT")

            invalid = root / "invalid.nul"
            invalid.write_bytes(b"\xff\0")
            with self.assertRaises(self.validator.ContractError) as raised:
                self.validator.read_nul_paths(invalid)
            self.assertEqual(raised.exception.code, "SURFACE-PATH-TRANSPORT")

    def test_git_inventory_maps_output_limit_and_timeout_to_domain_error(self) -> None:
        for failure in (
            self.validator.BoundedOutputError("stdout exceeds its byte budget"),
            subprocess.TimeoutExpired(["git", "ls-files"], 1),
        ):
            with (
                self.subTest(failure=type(failure).__name__),
                mock.patch.object(
                    self.validator, "run_bounded_process", side_effect=failure
                ),
            ):
                with self.assertRaises(self.validator.ContractError) as raised:
                    self.validator.tracked_paths(ROOT)
                self.assertEqual(raised.exception.code, "SURFACE-GIT-INVENTORY")


if __name__ == "__main__":
    unittest.main()
