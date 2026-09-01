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

    def test_ci_range_cases(self) -> None:
        for case in self.fixture["ciRangeCases"]:
            with self.subTest(case=case["name"]):
                actual = self.validator.select_paths(
                    self.contract, case["paths"], "ci", ROOT
                )
                self.assertEqual(actual["ciJobs"], case["expectedJobs"])
                self.assertEqual(
                    self.validator.github_output(self.contract, actual),
                    case["expectedGithubOutput"],
                )

    def test_rejection_cases(self) -> None:
        for case in self.fixture["rejectionCases"]:
            with self.subTest(case=case["name"]):
                root = ROOT
                temporary = None
                if case["name"] == "unmatched-tracked-path":
                    temporary = tempfile.TemporaryDirectory(
                        prefix="affected-unmatched-"
                    )
                    self.addCleanup(temporary.cleanup)
                    root = Path(temporary.name)
                    target = root / case["paths"][0]
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

    def test_ci_workflow_and_rename_range(self) -> None:
        self.validator.validate_ci_workflow_selector(ROOT)
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
                {
                    value.decode("utf-8")
                    for value in completed.stdout[:-1].split(b"\0")
                },
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
            with self.subTest(failure=type(failure).__name__), mock.patch.object(
                self.validator, "run_bounded_process", side_effect=failure
            ):
                with self.assertRaises(self.validator.ContractError) as raised:
                    self.validator.tracked_paths(ROOT)
                self.assertEqual(raised.exception.code, "SURFACE-GIT-INVENTORY")


if __name__ == "__main__":
    unittest.main()
