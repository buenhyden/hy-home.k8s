"""Production-isolation and pure selector regressions for validation lanes."""

from __future__ import annotations

import importlib.util
import os
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "run-validation-lane.py"
SPEC = importlib.util.spec_from_file_location("run_validation_lane_tested", MODULE_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import boundary
    raise RuntimeError(f"cannot load validation runner from {MODULE_PATH}")
RUNNER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = RUNNER
SPEC.loader.exec_module(RUNNER)

SELFTEST_ENV = "HY_HOME_K8S_VALIDATION_LANE_SELFTEST"
CONTEXT_ENV = "HY_HOME_K8S_VALIDATION_LANE_CONTEXT"
POST_VALIDATE_CONTEXT = "post-validate-bounded-selftest"
QUALITY_MARKER = "[PASS] repository quality gates passed"


class _ContractModule:
    @staticmethod
    def select_paths(contract, paths, lane, root):
        del contract, paths, lane, root
        return {"validators": ["repository-quality"]}


CONTRACT = {
    "validators": [
        {
            "id": "repository-quality",
            "argv": ["bash", "scripts/validate-repo-quality-gates.sh", "."],
            "evidenceLane": "repo-static",
            "optional": False,
            "fallback": {"status": "FAIL", "reason": "required"},
        }
    ]
}


class ProductionRunnerIsolationTest(unittest.TestCase):
    def _run(
        self,
        lane: str,
        environment: dict[str, str],
        *,
        stdout: str = QUALITY_MARKER + "\n",
    ):
        completed = subprocess.CompletedProcess(
            CONTRACT["validators"][0]["argv"], 0, stdout, ""
        )
        output = StringIO()
        with (
            patch.dict(os.environ, environment, clear=False),
            patch.object(RUNNER.shutil, "which", return_value="/usr/bin/python3"),
            patch.object(RUNNER.subprocess, "run", return_value=completed) as invoked,
            redirect_stdout(output),
        ):
            result = RUNNER.run_selected(
                ROOT,
                lane,
                ["scripts/run-validation-lane.py"],
                CONTRACT,
                _ContractModule,
            )
        return result, output.getvalue(), invoked

    def test_repository_quality_requires_one_exact_success_marker(self):
        for label, stdout in (
            ("missing", ""),
            ("duplicate", f"{QUALITY_MARKER}\n{QUALITY_MARKER}\n"),
        ):
            with self.subTest(label=label):
                result, output, invoked = self._run(
                    "affected",
                    {},
                    stdout=stdout,
                )

                self.assertEqual(result, 1)
                invoked.assert_called_once()
                self.assertIn("[FAIL] repository-quality ", output)

    def test_subprocess_uses_closed_environment_and_absolute_tool(self):
        hostile = {
            "PATH": f":relative:{ROOT}:/tmp/shadow:/usr/bin",
            "BASH_ENV": "/tmp/sentinel-bash-env",
            "ENV": "/tmp/sentinel-env",
            "PYTHONPATH": "/tmp/sentinel-pythonpath",
            "PYTHONHOME": "/tmp/sentinel-pythonhome",
            "NODE_OPTIONS": "--require=/tmp/sentinel-node",
        }

        result, _output, invoked = self._run("affected", hostile)

        self.assertEqual(result, 0)
        argv = invoked.call_args.args[0]
        environment = invoked.call_args.kwargs["env"]
        self.assertTrue(Path(argv[0]).is_absolute())
        for variable in (
            "BASH_ENV",
            "ENV",
            "PYTHONPATH",
            "PYTHONHOME",
            "NODE_OPTIONS",
        ):
            self.assertNotIn(variable, environment)
        path_entries = environment["PATH"].split(os.pathsep)
        self.assertTrue(path_entries)
        self.assertTrue(all(Path(entry).is_absolute() for entry in path_entries))
        self.assertTrue(all(entry and entry != "relative" for entry in path_entries))
        self.assertTrue(
            all(not Path(entry).is_relative_to(ROOT) for entry in path_entries)
        )
        self.assertTrue(
            all(not Path(entry).is_relative_to(Path("/tmp")) for entry in path_entries)
        )

    def test_path_shadow_and_bash_env_cannot_forge_quality_success(self):
        with tempfile.TemporaryDirectory(prefix="runner-hostile-") as temporary:
            temp = Path(temporary)
            shadow = temp / "shadow"
            shadow.mkdir()
            fake_marker = temp / "fake-bash-ran"
            startup_marker = temp / "bash-env-ran"
            body_marker = temp / "aggregate-body-ran"
            fake_bash = shadow / "bash"
            fake_bash.write_text(
                f"#!/bin/sh\n: > {fake_marker}\nexit 0\n",
                encoding="utf-8",
            )
            fake_bash.chmod(0o755)
            bash_env = temp / "bash-env.sh"
            bash_env.write_text(
                f": > {startup_marker}\nexit 0\n",
                encoding="utf-8",
            )
            body = temp / "validate-repo-quality-gates.sh"
            body.write_text(
                f"#!/usr/bin/bash\nprintf '%s\\n' '{QUALITY_MARKER}'\n: > {body_marker}\n",
                encoding="utf-8",
            )
            body.chmod(0o755)
            contract = {
                "validators": [
                    {
                        **CONTRACT["validators"][0],
                        "argv": ["bash", str(body)],
                    }
                ]
            }
            output = StringIO()
            with (
                patch.dict(
                    os.environ,
                    {
                        "PATH": (
                            f":relative:{ROOT}:{shadow}:{temp}:/tmp/shadow:/usr/bin"
                        ),
                        "BASH_ENV": str(bash_env),
                        "ENV": str(bash_env),
                        "PYTHONPATH": str(temp),
                        "PYTHONHOME": str(temp),
                        "NODE_OPTIONS": "--require=sentinel",
                    },
                    clear=False,
                ),
                redirect_stdout(output),
            ):
                result = RUNNER.run_selected(
                    ROOT,
                    "affected",
                    ["scripts/run-validation-lane.py"],
                    contract,
                    _ContractModule,
                )

            self.assertEqual(result, 0)
            self.assertIn("[PASS] repository-quality ", output.getvalue())
            self.assertIn('tool="/usr/bin/bash"', output.getvalue())
            self.assertTrue(body_marker.exists())
            self.assertFalse(fake_marker.exists())
            self.assertFalse(startup_marker.exists())

    def test_post_validate_uses_isolated_runner_and_exact_log_gate(self):
        hook_text = (
            ROOT / "docs/00.agent-governance/hooks/post-validate.sh"
        ).read_text(encoding="utf-8")

        self.assertIn("/usr/bin/env -i", hook_text)
        self.assertIn("/usr/bin/python3 -I scripts/run-validation-lane.py", hook_text)
        self.assertIn("post-validate-runner-result.py", hook_text)

    def test_all_files_executes_repository_quality_with_same_bounded_environment(self):
        result, output, invoked = self._run(
            "all-files",
            {SELFTEST_ENV: "1", CONTEXT_ENV: POST_VALIDATE_CONTEXT},
        )

        self.assertEqual(result, 0)
        invoked.assert_called_once()
        self.assertIn("[PASS] repository-quality ", output)
        self.assertNotIn("[SKIP] repository-quality ", output)

    def test_affected_environment_without_post_validate_context_executes(self):
        result, output, invoked = self._run(
            "affected",
            {SELFTEST_ENV: "1", CONTEXT_ENV: ""},
        )

        self.assertEqual(result, 0)
        invoked.assert_called_once()
        self.assertIn("[PASS] repository-quality ", output)
        self.assertNotIn("[SKIP] repository-quality ", output)

    def test_affected_forged_bounded_context_still_executes_repository_quality(self):
        result, output, invoked = self._run(
            "affected",
            {SELFTEST_ENV: "1", CONTEXT_ENV: POST_VALIDATE_CONTEXT},
        )

        self.assertEqual(result, 0)
        invoked.assert_called_once()
        self.assertIn("[PASS] repository-quality ", output)
        self.assertNotIn("[SKIP] repository-quality ", output)

    def test_production_hook_and_runner_have_no_selftest_bypass(self):
        runner_text = MODULE_PATH.read_text(encoding="utf-8")
        hook_text = (
            ROOT / "docs/00.agent-governance/hooks/post-validate.sh"
        ).read_text(encoding="utf-8")

        for variable in (
            SELFTEST_ENV,
            CONTEXT_ENV,
            "HY_HOME_K8S_POST_VALIDATE_SELFTEST",
        ):
            self.assertNotIn(variable, runner_text)
            self.assertNotIn(variable, hook_text)

    def test_aggregate_does_not_execute_manual_archive_cutover(self):
        aggregate = (ROOT / "scripts/validate-repo-quality-gates.sh").read_text(
            encoding="utf-8"
        )

        self.assertNotIn(
            'python3 "$ROOT_DIR/scripts/archive_cutover.py" --root "$ROOT_DIR"',
            aggregate,
        )


class PureAffectedSelectorRunnerTest(unittest.TestCase):
    @staticmethod
    def _run(paths: list[str]):
        contract_module = RUNNER.load_contract_module()
        contract = contract_module.validate_contract(ROOT)
        completed = subprocess.CompletedProcess(
            ["validator"], 0, QUALITY_MARKER + "\n", ""
        )
        output = StringIO()
        with (
            patch.object(RUNNER.shutil, "which", return_value="/usr/bin/bash"),
            patch.object(RUNNER.subprocess, "run", return_value=completed) as invoked,
            redirect_stdout(output),
        ):
            result = RUNNER.run_selected(
                ROOT,
                "affected",
                paths,
                contract,
                contract_module,
            )
        statuses = {
            identifier: status
            for status, identifier in re.findall(
                r"^\[(PASS|SKIP|FAIL)\] ([^ ]+) ",
                output.getvalue(),
                re.MULTILINE,
            )
        }
        return result, statuses, output.getvalue(), invoked

    def test_manifest_selector_executes_every_selected_validator(self):
        path = "gitops/platform/headlamp/headlamp-ingress.yaml"
        result, statuses, output, invoked = self._run([path])

        self.assertEqual(result, 0)
        self.assertEqual(
            statuses,
            {
                "gitops-change-set": "PASS",
                "gitops-structure": "PASS",
                "infrastructure-contracts": "PASS",
                "k8s-manifests": "PASS",
                "policy-gates": "PASS",
                "repository-quality": "PASS",
                "secret-handling": "PASS",
            },
        )
        self.assertEqual(invoked.call_count, 7)
        self.assertIn('scope="affected:paths=1"', output)

    def test_docs_selector_executes_every_validator_and_propagates_path(self):
        path = "docs/04.execution/tasks/2026-07-17-archive-record-and-workspace-boundary.md"
        result, statuses, output, invoked = self._run([path])

        self.assertEqual(result, 0)
        self.assertEqual(
            statuses,
            {
                "document-contract-registry": "PASS",
                "links-and-owners": "PASS",
                "markdown-profiles": "PASS",
                "repository-quality": "PASS",
            },
        )
        self.assertEqual(invoked.call_count, 4)
        self.assertGreaterEqual(output.count(path), 3)


if __name__ == "__main__":
    unittest.main()
