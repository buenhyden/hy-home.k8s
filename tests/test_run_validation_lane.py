"""Production-isolation and pure selector regressions for validation lanes."""

from __future__ import annotations

import importlib.util
import itertools
import hashlib
import json
import os
import pwd
import re
import selectors
import signal
import stat
import subprocess
import sys
import tempfile
import time
import unittest
from types import SimpleNamespace
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


class _RemoteLiveContractModule:
    @staticmethod
    def select_paths(contract, paths, lane, root):
        del contract, paths, lane, root
        return {"validators": ["remote-live-check"]}


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


def bounded_result(stdout: str = "", stderr: str = "", returncode: int = 0) -> object:
    def stream(value: str):
        payload = value.encode("utf-8")
        return RUNNER.StreamObservation(
            observed_bytes=len(payload),
            sha256=hashlib.sha256(payload).hexdigest(),
            retained=payload,
            complete=True,
        )

    return RUNNER.BoundedCommandResult(
        status="completed",
        returncode=returncode,
        stdout=stream(stdout),
        stderr=stream(stderr),
        cleanup_complete=True,
    )


class ProductionRunnerIsolationTest(unittest.TestCase):
    def _run(
        self,
        lane: str,
        environment: dict[str, str],
        *,
        stdout: str = QUALITY_MARKER + "\n",
    ):
        completed = bounded_result(stdout)
        output = StringIO()
        with (
            patch.dict(os.environ, environment, clear=False),
            patch.object(RUNNER.shutil, "which", return_value="/usr/bin/python3"),
            patch.object(
                RUNNER, "run_bounded_command", return_value=completed
            ) as invoked,
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

    def test_repository_quality_preserves_text_splitline_marker_semantics(self):
        result, output, invoked = self._run(
            "affected",
            {},
            stdout=QUALITY_MARKER + "\u2028",
        )

        self.assertEqual(result, 0)
        invoked.assert_called_once()
        self.assertIn("[PASS] repository-quality ", output)

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

    def test_hostile_ambient_gitleaks_hint_is_not_forwarded(self):
        hostile_hint = "/tmp/attacker/gitleaks"
        with patch.object(
            RUNNER,
            "secure_gitleaks_executable",
            return_value=None,
            create=True,
        ):
            result, _output, invoked = self._run(
                "affected",
                {"HY_HOME_K8S_GITLEAKS_EXECUTABLE": hostile_hint},
            )

        self.assertEqual(result, 0)
        environment = invoked.call_args.kwargs["env"]
        self.assertNotIn("HY_HOME_K8S_GITLEAKS_EXECUTABLE", environment)
        self.assertNotIn("/tmp/attacker", environment["PATH"])

    def test_secure_passwd_home_gitleaks_is_passed_without_broadening_path(self):
        executable = "/home/alice/.local/bin/gitleaks"
        with patch.object(
            RUNNER,
            "secure_gitleaks_executable",
            return_value=executable,
            create=True,
        ):
            result, _output, invoked = self._run("affected", {})

        self.assertEqual(result, 0)
        environment = invoked.call_args.kwargs["env"]
        self.assertEqual(
            environment["HY_HOME_K8S_GITLEAKS_EXECUTABLE"],
            executable,
        )
        self.assertNotIn("/home/alice/.local/bin", environment["PATH"])

    def test_gitleaks_candidate_rejects_unsafe_shapes(self):
        metadata = {
            "/home/alice": stat.S_IFDIR | 0o750,
            "/home/alice/.local": stat.S_IFDIR | 0o755,
            "/home/alice/.local/bin": stat.S_IFDIR | 0o755,
            "/home/alice/.local/bin/gitleaks": stat.S_IFREG | 0o755,
        }
        owners = {path: 1000 for path in metadata}

        def fake_lstat(path):
            value = os.fspath(path)
            if value not in metadata:
                raise FileNotFoundError(value)
            return SimpleNamespace(
                st_mode=metadata[value],
                st_uid=owners[value],
                st_gid=1000,
            )

        with (
            patch.object(RUNNER.os, "lstat", side_effect=fake_lstat),
            patch.object(RUNNER.os, "geteuid", return_value=1000, create=True),
            patch.object(RUNNER.os, "getegid", return_value=1000, create=True),
            patch.object(RUNNER.os, "getgroups", return_value=[1000], create=True),
            patch.object(
                RUNNER.pwd,
                "getpwuid",
                return_value=pwd.struct_passwd(
                    ("alice", "x", 1000, 1000, "", "/home/alice", "/bin/sh")
                ),
            ),
        ):
            self.assertEqual(
                RUNNER.secure_gitleaks_executable(ROOT),
                "/home/alice/.local/bin/gitleaks",
            )

            for path in (
                Path("relative/gitleaks"),
                Path("/tmp/gitleaks"),
                ROOT / "gitleaks",
                Path("/home/alice/.local/bin/not-gitleaks"),
            ):
                with self.subTest(path=path):
                    self.assertFalse(
                        RUNNER.validate_gitleaks_candidate(
                            path,
                            ROOT,
                            owner_uid=1000,
                            required_chain=(
                                Path("/home/alice"),
                                Path("/home/alice/.local"),
                                Path("/home/alice/.local/bin"),
                            ),
                        )
                    )

            metadata["/home/alice/.local/bin/gitleaks"] = stat.S_IFLNK | 0o777
            self.assertIsNone(RUNNER.secure_gitleaks_executable(ROOT))
            metadata["/home/alice/.local/bin/gitleaks"] = stat.S_IFREG | 0o775
            self.assertIsNone(RUNNER.secure_gitleaks_executable(ROOT))
            metadata["/home/alice/.local/bin/gitleaks"] = stat.S_IFREG | 0o755
            owners["/home/alice/.local/bin/gitleaks"] = 1001
            self.assertIsNone(RUNNER.secure_gitleaks_executable(ROOT))

    def test_gitleaks_candidate_requires_effective_execute_and_traversal(self):
        candidate = Path("/secure/bin/gitleaks")
        chain = (Path("/secure"), Path("/secure/bin"))
        metadata = {
            "/secure": SimpleNamespace(
                st_mode=stat.S_IFDIR | 0o755, st_uid=1000, st_gid=1000
            ),
            "/secure/bin": SimpleNamespace(
                st_mode=stat.S_IFDIR | 0o755, st_uid=1000, st_gid=1000
            ),
            "/secure/bin/gitleaks": SimpleNamespace(
                st_mode=stat.S_IFREG | 0o755, st_uid=1000, st_gid=1000
            ),
        }

        def fake_lstat(path):
            value = os.fspath(path)
            if value not in metadata:
                raise FileNotFoundError(value)
            return metadata[value]

        with (
            patch.object(RUNNER.os, "lstat", side_effect=fake_lstat),
            patch.object(RUNNER.os, "geteuid", return_value=1000, create=True),
            patch.object(RUNNER.os, "getegid", return_value=1000, create=True),
            patch.object(RUNNER.os, "getgroups", return_value=[1000], create=True),
        ):
            self.assertTrue(
                RUNNER.validate_gitleaks_candidate(
                    candidate,
                    ROOT,
                    owner_uid=1000,
                    required_chain=chain,
                )
            )

            metadata[candidate.as_posix()].st_mode = stat.S_IFREG | 0o001
            self.assertFalse(
                RUNNER.validate_gitleaks_candidate(
                    candidate,
                    ROOT,
                    owner_uid=1000,
                    required_chain=chain,
                )
            )

            for path in (*chain, candidate):
                metadata[path.as_posix()].st_uid = 0
                metadata[path.as_posix()].st_gid = 2000
                metadata[path.as_posix()].st_mode = (
                    stat.S_IFDIR if path != candidate else stat.S_IFREG
                ) | 0o010
            with patch.object(RUNNER.os, "getgroups", return_value=[2000], create=True):
                self.assertTrue(
                    RUNNER.validate_gitleaks_candidate(
                        candidate,
                        ROOT,
                        owner_uid=0,
                        required_chain=chain,
                    )
                )
                metadata["/secure"].st_mode = stat.S_IFDIR | 0o100
                self.assertFalse(
                    RUNNER.validate_gitleaks_candidate(
                        candidate,
                        ROOT,
                        owner_uid=0,
                        required_chain=chain,
                    )
                )

            metadata["/secure"].st_mode = stat.S_IFDIR | 0o001
            metadata["/secure/bin"].st_mode = stat.S_IFDIR | 0o001
            metadata[candidate.as_posix()].st_mode = stat.S_IFREG | 0o100
            with patch.object(RUNNER.os, "getgroups", return_value=[], create=True):
                self.assertFalse(
                    RUNNER.validate_gitleaks_candidate(
                        candidate,
                        ROOT,
                        owner_uid=0,
                        required_chain=chain,
                    )
                )
                metadata[candidate.as_posix()].st_mode = stat.S_IFREG | 0o001
                self.assertTrue(
                    RUNNER.validate_gitleaks_candidate(
                        candidate,
                        ROOT,
                        owner_uid=0,
                        required_chain=chain,
                    )
                )

        with (
            patch.object(RUNNER.os, "lstat", side_effect=fake_lstat),
            patch.object(RUNNER.os, "geteuid", return_value=0, create=True),
            patch.object(RUNNER.os, "getegid", return_value=0, create=True),
            patch.object(RUNNER.os, "getgroups", return_value=[0], create=True),
        ):
            metadata["/secure"].st_mode = stat.S_IFDIR
            metadata["/secure/bin"].st_mode = stat.S_IFDIR
            metadata[candidate.as_posix()].st_mode = stat.S_IFREG | 0o100
            self.assertTrue(
                RUNNER.validate_gitleaks_candidate(
                    candidate,
                    ROOT,
                    owner_uid=0,
                    required_chain=chain,
                )
            )
            metadata[candidate.as_posix()].st_mode = stat.S_IFREG
            self.assertFalse(
                RUNNER.validate_gitleaks_candidate(
                    candidate,
                    ROOT,
                    owner_uid=0,
                    required_chain=chain,
                )
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

    def test_staged_lane_executes_contract_selected_validators(self):
        self.assertEqual(
            RUNNER.LOCAL_LANES,
            ("affected", "staged", "all-files"),
        )
        result, output, invoked = self._run("staged", {})

        self.assertEqual(result, 0)
        invoked.assert_called_once()
        self.assertIn("[PASS] repository-quality ", output)
        self.assertIn('scope="staged:paths=1"', output)

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

    def test_aggregate_executes_exact_archive_cutover(self):
        aggregate = (ROOT / "scripts/validate-repo-quality-gates.sh").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            'python3 "$ROOT_DIR/scripts/archive_cutover.py" --root "$ROOT_DIR"',
            aggregate,
        )

    def test_remote_live_lane_defers_without_subprocess_and_succeeds(self):
        contract = {
            "validators": [
                {
                    "id": "remote-live-check",
                    "argv": ["remote-validator", "--check"],
                    "evidenceLane": "remote/live",
                    "optional": False,
                    "fallback": {"status": "FAIL", "reason": "required"},
                }
            ]
        }
        output = StringIO()
        with (
            patch.object(RUNNER, "run_bounded_command") as invoked,
            redirect_stdout(output),
        ):
            result = RUNNER.run_selected(
                ROOT,
                "affected",
                ["scripts/run-validation-lane.py"],
                contract,
                _RemoteLiveContractModule,
            )

        self.assertEqual(result, 0)
        invoked.assert_not_called()
        self.assertEqual(
            re.findall(
                r"^\[DEFER\] remote-live-check ",
                output.getvalue(),
                re.MULTILINE,
            ),
            ["[DEFER] remote-live-check "],
        )


class BoundedValidationCommandTest(unittest.TestCase):
    @staticmethod
    def _run_python(
        source: str,
        *,
        timeout_seconds: float = 2.0,
        stdout_limit_bytes: int = 128,
        stderr_limit_bytes: int = 128,
        cleanup_seconds: float = 0.5,
    ):
        return RUNNER.run_bounded_command(
            [sys.executable, "-I", "-c", source],
            cwd=ROOT,
            env=RUNNER.closed_subprocess_environment(),
            timeout_seconds=timeout_seconds,
            stdout_limit_bytes=stdout_limit_bytes,
            stderr_limit_bytes=stderr_limit_bytes,
            cleanup_seconds=cleanup_seconds,
        )

    @staticmethod
    def _wait_for_process_exit(pid: int, timeout_seconds: float = 2.0) -> None:
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return
            status_path = Path("/proc") / str(pid) / "status"
            try:
                status = status_path.read_text(encoding="utf-8")
            except (FileNotFoundError, ProcessLookupError):
                return
            if "\nState:\tZ" in f"\n{status}":
                return
            time.sleep(0.01)
        raise AssertionError(f"process {pid} survived bounded cleanup")

    def test_normal_completion_drains_both_pipes_and_records_only_metadata(self):
        outcome = self._run_python(
            "import os; os.write(1, b'normal-out\\n'); os.write(2, b'normal-err\\n')"
        )

        self.assertEqual(outcome.status, "completed")
        self.assertEqual(outcome.returncode, 0)
        self.assertEqual(outcome.stdout.observed_bytes, len(b"normal-out\n"))
        self.assertEqual(outcome.stderr.observed_bytes, len(b"normal-err\n"))
        rendered = RUNNER.observation(outcome)
        self.assertNotIn("normal-out", rendered)
        self.assertNotIn("normal-err", rendered)
        self.assertRegex(rendered, r"stdout_sha256=[0-9a-f]{64}")
        self.assertRegex(rendered, r"stderr_sha256=[0-9a-f]{64}")

    def test_reviewed_limits_match_the_sole_quality_owner(self):
        owner = (
            ROOT / "docs/00.agent-governance/policies/quality.md"
        ).read_text(encoding="utf-8")

        self.assertEqual(RUNNER.VALIDATOR_TIMEOUT_SECONDS, 1_200.0)
        self.assertEqual(RUNNER.VALIDATOR_STDOUT_LIMIT_BYTES, 4 * 1024 * 1024)
        self.assertEqual(RUNNER.VALIDATOR_STDERR_LIMIT_BYTES, 1 * 1024 * 1024)
        self.assertEqual(RUNNER.VALIDATOR_CLEANUP_SECONDS, 2.0)
        for phrase in (
            "1,200 seconds maximum execution time per child",
            "4 MiB maximum retained stdout",
            "1 MiB maximum retained stderr",
            "2 seconds total cleanup time",
        ):
            self.assertIn(phrase, owner)

    def test_timeout_fails_closed_and_reaps_direct_child(self):
        outcome = self._run_python(
            "import signal; signal.pause()",
            timeout_seconds=0.1,
        )

        self.assertEqual(outcome.status, "timeout")
        self.assertTrue(outcome.cleanup_complete)
        self.assertIsNotNone(outcome.returncode)

    def test_selector_start_failure_does_not_launch_a_child(self):
        with (
            patch.object(
                RUNNER.selectors,
                "DefaultSelector",
                side_effect=OSError("synthetic-selector-failure"),
            ),
            patch.object(RUNNER.subprocess, "Popen") as launched,
        ):
            outcome = self._run_python("raise AssertionError('must not run')")

        launched.assert_not_called()
        self.assertEqual(outcome.status, "pipe_failure")
        self.assertTrue(outcome.cleanup_complete)

    def test_missing_ownership_primitives_fail_closed_before_spawn(self):
        with (
            patch.object(RUNNER, "_ownership_primitives_available", return_value=False),
            patch.object(RUNNER.subprocess, "Popen") as launched,
        ):
            outcome = self._run_python("raise AssertionError('must not run')")

        launched.assert_not_called()
        self.assertEqual(outcome.status, "ownership_unavailable")
        self.assertTrue(outcome.cleanup_complete)

    def test_interrupted_collection_fails_closed_and_reaps_the_child(self):
        class _InterruptedSelector:
            def register(self, *_args):
                return None

            def get_map(self):
                return {"registered": True}

            def select(self, timeout):
                self.timeout = timeout
                raise InterruptedError

            def close(self):
                return None

        selector = _InterruptedSelector()
        with patch.object(RUNNER.selectors, "DefaultSelector", return_value=selector):
            outcome = self._run_python("import signal; signal.pause()")

        self.assertEqual(outcome.status, "collection_interrupted")
        self.assertTrue(outcome.cleanup_complete)
        self.assertIsNotNone(outcome.returncode)
        self.assertLessEqual(selector.timeout, RUNNER.VALIDATOR_PIPE_POLL_SECONDS)

    def test_post_spawn_interrupt_still_finalizes_owned_child(self):
        real_popen = RUNNER.subprocess.Popen
        real_monotonic = RUNNER.time.monotonic
        spawned = []
        clock_calls = 0

        def capture_spawn(*args, **kwargs):
            process = real_popen(*args, **kwargs)
            spawned.append(process)
            return process

        def interrupt_before_collection():
            nonlocal clock_calls
            clock_calls += 1
            if clock_calls == 1:
                raise KeyboardInterrupt("post-spawn synthetic interrupt")
            return real_monotonic()

        try:
            with (
                patch.object(RUNNER.subprocess, "Popen", side_effect=capture_spawn),
                patch.object(
                    RUNNER.time,
                    "monotonic",
                    side_effect=interrupt_before_collection,
                ),
                self.assertRaises(KeyboardInterrupt),
            ):
                self._run_python("import signal; signal.pause()")

            self.assertEqual(len(spawned), 1)
            self.assertIsNotNone(spawned[0].returncode)
            self.assertTrue(spawned[0].stdout.closed)
            self.assertTrue(spawned[0].stderr.closed)
        finally:
            for process in spawned:
                if process.poll() is None:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait(timeout=2)

    def test_spawn_assignment_interrupt_reaps_child_and_closes_owned_fds(self):
        real_popen = RUNNER.subprocess.Popen
        real_restore = RUNNER._restore_interrupt_signals
        spawned = []
        child_alive_at_restore = []
        baseline_fds = len(os.listdir("/proc/self/fd"))

        def spawn_then_interrupt(*args, **kwargs):
            process = real_popen(*args, **kwargs)
            spawned.append(process)
            raise KeyboardInterrupt("synthetic pre-assignment interrupt")

        def observe_restore(mask):
            if spawned:
                child_alive_at_restore.append(
                    (Path("/proc") / str(spawned[0].pid)).exists()
                )
            return real_restore(mask)

        try:
            with (
                patch.object(
                    RUNNER.subprocess,
                    "Popen",
                    side_effect=spawn_then_interrupt,
                ),
                patch.object(
                    RUNNER,
                    "_restore_interrupt_signals",
                    side_effect=observe_restore,
                ),
                self.assertRaises(KeyboardInterrupt),
            ):
                self._run_python("import signal; signal.pause()")

            self.assertEqual(len(spawned), 1)
            with self.assertRaises(ProcessLookupError):
                os.kill(spawned[0].pid, 0)
            # The synthetic wrapper retained a Popen object that the runner
            # could not receive; mirror the external waitpid result so its
            # destructor does not emit a false live-process warning.
            spawned[0].returncode = -signal.SIGKILL
            self.assertTrue(child_alive_at_restore)
            self.assertFalse(any(child_alive_at_restore))
            self.assertEqual(len(os.listdir("/proc/self/fd")), baseline_fds)
        finally:
            for process in spawned:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def test_handle_acquisition_failure_keeps_mask_until_child_cleanup(self):
        real_popen = RUNNER.subprocess.Popen
        real_pidfd_open = RUNNER.os.pidfd_open
        real_restore = RUNNER._restore_interrupt_signals
        spawned = []
        child_alive_at_restore = []

        def capture_spawn(*args, **kwargs):
            process = real_popen(*args, **kwargs)
            spawned.append(process)
            return process

        def fail_leader_pidfd(pid, flags=0):
            if spawned and pid == spawned[0].pid:
                raise KeyboardInterrupt("synthetic leader pidfd interrupt")
            return real_pidfd_open(pid, flags)

        def observe_restore(mask):
            if spawned:
                child_alive_at_restore.append(
                    (Path("/proc") / str(spawned[0].pid)).exists()
                )
            return real_restore(mask)

        try:
            with (
                patch.object(RUNNER.subprocess, "Popen", side_effect=capture_spawn),
                patch.object(RUNNER.os, "pidfd_open", side_effect=fail_leader_pidfd),
                patch.object(
                    RUNNER,
                    "_restore_interrupt_signals",
                    side_effect=observe_restore,
                ),
                self.assertRaises(KeyboardInterrupt),
            ):
                self._run_python("import signal; signal.pause()")

            self.assertEqual(len(spawned), 1)
            with self.assertRaises(ProcessLookupError):
                os.kill(spawned[0].pid, 0)
            self.assertTrue(child_alive_at_restore)
            self.assertFalse(any(child_alive_at_restore))
        finally:
            for process in spawned:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass

    def test_stdout_overflow_fails_closed_without_retaining_over_limit(self):
        outcome = self._run_python(
            "import os; os.write(1, b'x' * 129)",
            stdout_limit_bytes=128,
        )

        self.assertEqual(outcome.status, "stdout_overflow")
        self.assertGreater(outcome.stdout.observed_bytes, 128)
        self.assertLessEqual(len(outcome.stdout.retained), 128)
        self.assertTrue(outcome.cleanup_complete)

    def test_stderr_overflow_fails_closed_without_retaining_over_limit(self):
        outcome = self._run_python(
            "import os; os.write(2, b'y' * 129)",
            stderr_limit_bytes=128,
        )

        self.assertEqual(outcome.status, "stderr_overflow")
        self.assertGreater(outcome.stderr.observed_bytes, 128)
        self.assertLessEqual(len(outcome.stderr.retained), 128)
        self.assertTrue(outcome.cleanup_complete)

    def test_zero_and_inclusive_pipe_limits_are_exact(self):
        empty = self._run_python("pass", stdout_limit_bytes=0, stderr_limit_bytes=0)
        inclusive = self._run_python(
            "import os; os.write(1, b'x' * 128); os.write(2, b'y' * 128)",
            stdout_limit_bytes=128,
            stderr_limit_bytes=128,
        )
        overflow = self._run_python(
            "import os; os.write(1, b'x')",
            stdout_limit_bytes=0,
        )

        self.assertEqual(empty.status, "completed")
        self.assertEqual(inclusive.status, "completed")
        self.assertEqual(inclusive.stdout.observed_bytes, 128)
        self.assertEqual(inclusive.stderr.observed_bytes, 128)
        self.assertEqual(overflow.status, "stdout_overflow")

    def test_selector_unregister_oserror_is_bounded_pipe_failure(self):
        real_selector = selectors.DefaultSelector()

        class _UnregisterFailureSelector:
            def register(self, *args):
                return real_selector.register(*args)

            def get_map(self):
                return real_selector.get_map()

            def select(self, timeout):
                return real_selector.select(timeout)

            def unregister(self, _pipe):
                raise OSError("synthetic-unregister-failure")

            def close(self):
                real_selector.close()

        with patch.object(
            RUNNER.selectors,
            "DefaultSelector",
            return_value=_UnregisterFailureSelector(),
        ):
            outcome = self._run_python("pass")

        self.assertEqual(outcome.status, "pipe_failure")
        self.assertTrue(outcome.cleanup_complete)

    def test_selector_close_failure_occurs_only_after_process_cleanup(self):
        real_popen = RUNNER.subprocess.Popen
        spawned = []
        close_returncodes = []

        def capture_spawn(*args, **kwargs):
            process = real_popen(*args, **kwargs)
            spawned.append(process)
            return process

        class _CloseFailureSelector:
            def register(self, *_args):
                return None

            def get_map(self):
                return {"registered": True}

            def select(self, _timeout):
                raise OSError("synthetic-select-failure")

            def close(self):
                close_returncodes.append(spawned[0].returncode)
                raise OSError("synthetic-close-failure")

        try:
            with (
                patch.object(RUNNER.subprocess, "Popen", side_effect=capture_spawn),
                patch.object(
                    RUNNER.selectors,
                    "DefaultSelector",
                    return_value=_CloseFailureSelector(),
                ),
            ):
                outcome = self._run_python("import signal; signal.pause()")

            self.assertEqual(outcome.status, "pipe_failure")
            self.assertFalse(outcome.cleanup_complete)
            self.assertTrue(close_returncodes)
            self.assertTrue(all(value is not None for value in close_returncodes))
            self.assertIsNotNone(spawned[0].returncode)
        finally:
            for process in spawned:
                if process.poll() is None:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    process.wait(timeout=2)

    def test_descendant_held_pipes_fail_closed_and_process_group_is_killed(self):
        with tempfile.TemporaryDirectory(prefix="runner-descendant-") as temporary:
            pid_path = Path(temporary) / "descendant.json"
            source = (
                "import json, subprocess, sys; "
                "child=subprocess.Popen([sys.executable, '-I', '-c', "
                "'import signal; signal.pause()']); "
                f"open({str(pid_path)!r}, 'w', encoding='utf-8').write("
                "json.dumps({'pid': child.pid})); "
                "print('leader-exit')"
            )
            outcome = self._run_python(source)

            self.assertEqual(outcome.status, "descendant_pipe_hold")
            self.assertFalse(outcome.cleanup_complete)
            descendant_pid = json.loads(pid_path.read_text(encoding="utf-8"))["pid"]
            self._wait_for_process_exit(descendant_pid)

    def test_successful_leader_closes_silent_owned_process_group(self):
        with tempfile.TemporaryDirectory(
            prefix="runner-silent-descendant-"
        ) as temporary:
            pid_path = Path(temporary) / "descendant.json"
            source = (
                "import json, os, signal, subprocess, sys; "
                "child=subprocess.Popen([sys.executable, '-I', '-c', "
                "'import signal; signal.pause()'], stdin=subprocess.DEVNULL, "
                "stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); "
                f"open({str(pid_path)!r}, 'w', encoding='utf-8').write("
                "json.dumps({'pid': child.pid, 'pgid': os.getpgrp()}))"
            )
            process_ids: dict[str, int] = {}
            try:
                outcome = self._run_python(source)
                process_ids = json.loads(pid_path.read_text(encoding="utf-8"))

                self.assertEqual(outcome.status, "completed")
                self.assertTrue(outcome.cleanup_complete)
                with self.assertRaises(ProcessLookupError):
                    os.kill(process_ids["pid"], 0)
                self.assertTrue(RUNNER._process_group_absent(process_ids["pgid"]))
            finally:
                if process_ids:
                    try:
                        os.killpg(process_ids["pgid"], signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    self._wait_for_process_exit(process_ids["pid"])

    def test_escaped_descendant_is_failed_without_post_reap_group_signal(self):
        with tempfile.TemporaryDirectory(
            prefix="runner-escaped-descendant-"
        ) as temporary:
            pid_path = Path(temporary) / "escaped.json"
            child_source = (
                "import json, os, signal; os.setsid(); "
                f"open({str(pid_path)!r}, 'w', encoding='utf-8').write("
                "json.dumps({'pid': os.getpid(), 'pgid': os.getpgrp()})); "
                "signal.pause()"
            )
            leader_source = (
                "import pathlib, subprocess, sys, time; "
                f"path=pathlib.Path({str(pid_path)!r}); "
                f"subprocess.Popen([sys.executable, '-I', '-c', {child_source!r}]); "
                "deadline=time.monotonic()+2.0\n"
                "while not path.exists():\n"
                "    assert time.monotonic() < deadline\n"
                "    time.sleep(0.01)\n"
            )
            escaped: dict[str, int] = {}
            try:
                outcome = self._run_python(leader_source, cleanup_seconds=0.2)
                escaped = json.loads(pid_path.read_text(encoding="utf-8"))

                self.assertEqual(outcome.status, "descendant_pipe_hold")
                self.assertFalse(outcome.cleanup_complete)
                with self.assertRaises(ProcessLookupError):
                    os.kill(escaped["pid"], 0)
            finally:
                if escaped:
                    try:
                        os.killpg(escaped["pgid"], signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    self._wait_for_process_exit(escaped["pid"])

    def test_escaped_devnull_descendant_is_killed_and_not_reported_completed(self):
        with tempfile.TemporaryDirectory(prefix="runner-escaped-devnull-") as temporary:
            pid_path = Path(temporary) / "escaped.json"
            child_source = (
                "import json, os, signal; os.setsid(); "
                f"open({str(pid_path)!r}, 'w', encoding='utf-8').write("
                "json.dumps({'pid': os.getpid(), 'pgid': os.getpgrp()})); "
                "signal.pause()"
            )
            leader_source = (
                "import pathlib, subprocess, sys, time; "
                f"path=pathlib.Path({str(pid_path)!r}); "
                "subprocess.Popen([sys.executable, '-I', '-c', "
                f"{child_source!r}], stdin=subprocess.DEVNULL, "
                "stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); "
                "deadline=time.monotonic()+2.0\n"
                "while not path.exists():\n"
                "    assert time.monotonic() < deadline\n"
                "    time.sleep(0.01)\n"
            )
            escaped: dict[str, int] = {}
            try:
                outcome = self._run_python(leader_source, cleanup_seconds=0.5)
                escaped = json.loads(pid_path.read_text(encoding="utf-8"))

                self.assertEqual(outcome.status, "descendant_cleanup")
                self.assertTrue(outcome.cleanup_complete)
                with self.assertRaises(ProcessLookupError):
                    os.kill(escaped["pid"], 0)
            finally:
                if escaped:
                    try:
                        os.killpg(escaped["pgid"], signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    self._wait_for_process_exit(escaped["pid"])

    def test_timeout_kills_ready_process_tree(self):
        with tempfile.TemporaryDirectory(prefix="runner-tree-") as temporary:
            pid_path = Path(temporary) / "tree.json"
            source = (
                "import json, os, signal, subprocess, sys; "
                "child=subprocess.Popen([sys.executable, '-I', '-c', "
                "'import signal; signal.pause()']); "
                f"open({str(pid_path)!r}, 'w', encoding='utf-8').write("
                "json.dumps({'leader': os.getpid(), 'child': child.pid})); "
                "signal.pause()"
            )
            real_monotonic = RUNNER.time.monotonic
            virtual_start = real_monotonic()
            barrier_observed = False

            def readiness_gated_clock():
                nonlocal barrier_observed
                try:
                    barrier_observed = pid_path.stat().st_size > 0
                except FileNotFoundError:
                    barrier_observed = False
                return virtual_start + (1.0 if barrier_observed else 0.0)

            with patch.object(
                RUNNER.time, "monotonic", side_effect=readiness_gated_clock
            ):
                outcome = self._run_python(source, timeout_seconds=0.5)

            self.assertEqual(outcome.status, "timeout")
            self.assertTrue(barrier_observed)
            process_ids = json.loads(pid_path.read_text(encoding="utf-8"))
            self._wait_for_process_exit(process_ids["leader"])
            self._wait_for_process_exit(process_ids["child"])

    def test_cleanup_waits_under_one_total_monotonic_deadline(self):
        class _Pipe:
            def __init__(self):
                self.closed = False

            def close(self):
                self.closed = True

        class _Process:
            pid = 424242

            def __init__(self):
                self.stdout = _Pipe()
                self.stderr = _Pipe()
                self.wait_timeouts: list[float] = []
                self.killed = 0

            def poll(self):
                return None

            def kill(self):
                self.killed += 1

            def wait(self, timeout):
                self.wait_timeouts.append(timeout)
                raise subprocess.TimeoutExpired(("synthetic",), timeout)

        process = _Process()
        clock = itertools.chain((10.0, 10.1, 10.2, 10.3, 10.4), itertools.repeat(10.5))
        with (
            patch.object(RUNNER.time, "monotonic", side_effect=lambda: next(clock)),
            patch.object(RUNNER.os, "killpg", side_effect=ProcessLookupError),
        ):
            complete = RUNNER.cleanup_process_group(process, 0.5)

        self.assertFalse(complete)
        self.assertGreaterEqual(len(process.wait_timeouts), 1)
        self.assertTrue(all(value >= 0 for value in process.wait_timeouts))
        self.assertTrue(all(value <= 0.5 for value in process.wait_timeouts))
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)

    def test_cleanup_reports_unexpected_process_group_signal_failure(self):
        class _Pipe:
            def close(self):
                return None

        class _Process:
            pid = 424243
            stdout = _Pipe()
            stderr = _Pipe()

            def poll(self):
                return -signal.SIGKILL

            def kill(self):
                return None

        with patch.object(
            RUNNER.os,
            "killpg",
            side_effect=PermissionError("synthetic-permission-failure"),
        ):
            complete = RUNNER.cleanup_process_group(_Process(), 0.5)

        self.assertFalse(complete)

    def test_pre_effect_group_interrupt_reuses_deadline_and_finishes_tree(self):
        with tempfile.TemporaryDirectory(prefix="runner-group-interrupt-") as temporary:
            pid_path = Path(temporary) / "child.json"
            source = (
                "import json, os, signal, subprocess, sys; "
                "child=subprocess.Popen([sys.executable, '-I', '-c', "
                "'import signal; signal.pause()'], stdin=subprocess.DEVNULL, "
                "stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); "
                f"open({str(pid_path)!r}, 'w', encoding='utf-8').write("
                "json.dumps({'pid': child.pid, 'pgid': os.getpgrp()})); "
                "signal.pause()"
            )
            real_cleanup = RUNNER.cleanup_process_group
            real_killpg = RUNNER.os.killpg
            real_popen = RUNNER.subprocess.Popen
            deadlines = []
            signal_returncodes = []
            spawned = []
            child = {}

            def capture_spawn(*args, **kwargs):
                process = real_popen(*args, **kwargs)
                spawned.append(process)
                return process

            def observed_cleanup(*args, **kwargs):
                deadlines.append(kwargs.get("deadline"))
                return real_cleanup(*args, **kwargs)

            def interrupt_before_effect(pgid, sig):
                signal_returncodes.append(spawned[0].returncode)
                if len(signal_returncodes) == 1:
                    raise KeyboardInterrupt("synthetic pre-effect interrupt")
                return real_killpg(pgid, sig)

            try:
                with (
                    patch.object(RUNNER.subprocess, "Popen", side_effect=capture_spawn),
                    patch.object(
                        RUNNER, "cleanup_process_group", side_effect=observed_cleanup
                    ),
                    patch.object(
                        RUNNER.os, "killpg", side_effect=interrupt_before_effect
                    ),
                    self.assertRaises(KeyboardInterrupt),
                ):
                    self._run_python(source, timeout_seconds=0.2)

                child = json.loads(pid_path.read_text(encoding="utf-8"))
                self.assertGreaterEqual(len(signal_returncodes), 2)
                self.assertTrue(all(value is None for value in signal_returncodes))
                self.assertGreaterEqual(len(deadlines), 2)
                self.assertIsNotNone(deadlines[0])
                self.assertTrue(all(value == deadlines[0] for value in deadlines))
                with self.assertRaises(ProcessLookupError):
                    os.kill(child["pid"], 0)
                self.assertTrue(RUNNER._process_group_absent(child["pgid"]))
            finally:
                if child:
                    try:
                        real_killpg(child["pgid"], signal.SIGKILL)
                    except ProcessLookupError:
                        pass

    def test_two_wait_interrupts_still_reap_without_post_reap_group_signal(self):
        process = subprocess.Popen(
            [sys.executable, "-I", "-c", "import signal; signal.pause()"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        real_killpg = RUNNER.os.killpg
        wait_calls = 0
        signal_returncodes = []

        class _InterruptingWaitProcess:
            def __init__(self, delegate):
                self._delegate = delegate
                self.pid = delegate.pid
                self.stdout = delegate.stdout
                self.stderr = delegate.stderr

            @property
            def returncode(self):
                return self._delegate.returncode

            def wait(self, timeout=None):
                nonlocal wait_calls
                wait_calls += 1
                if wait_calls <= 2:
                    raise KeyboardInterrupt("synthetic wait interrupt")
                return self._delegate.wait(timeout=timeout)

        wrapped = _InterruptingWaitProcess(process)

        def observed_killpg(pgid, sig):
            signal_returncodes.append(process.returncode)
            return real_killpg(pgid, sig)

        try:
            with (
                patch.object(RUNNER.os, "killpg", side_effect=observed_killpg),
                self.assertRaises(KeyboardInterrupt),
            ):
                RUNNER.cleanup_process_group(wrapped, 0.5)

            self.assertGreaterEqual(wait_calls, 3)
            self.assertIsNotNone(process.returncode)
            self.assertTrue(signal_returncodes)
            self.assertTrue(all(value is None for value in signal_returncodes))
            self.assertTrue(process.stdout.closed)
            self.assertTrue(process.stderr.closed)
        finally:
            if process.returncode is None:
                try:
                    real_killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait(timeout=2)

    def test_group_signal_precedes_reap_and_is_never_repeated_after_reap(self):
        real_popen = RUNNER.subprocess.Popen
        real_killpg = RUNNER.os.killpg
        events = []

        class _ObservedProcess:
            def __init__(self, process):
                self._process = process
                self.pid = process.pid
                self.stdout = process.stdout
                self.stderr = process.stderr

            @property
            def returncode(self):
                return self._process.returncode

            def poll(self):
                events.append("reap")
                return self._process.poll()

            def wait(self, timeout=None):
                events.append("reap")
                return self._process.wait(timeout=timeout)

            def kill(self):
                return self._process.kill()

        def observed_spawn(*args, **kwargs):
            return _ObservedProcess(real_popen(*args, **kwargs))

        def observed_group_signal(pgid, sig):
            if sig != 0:
                events.append("group-signal")
            return real_killpg(pgid, sig)

        with (
            patch.object(RUNNER.subprocess, "Popen", side_effect=observed_spawn),
            patch.object(RUNNER.os, "killpg", side_effect=observed_group_signal),
        ):
            outcome = self._run_python("pass")

        self.assertEqual(outcome.status, "completed")
        self.assertIn("group-signal", events)
        first_reap = events.index("reap")
        self.assertLess(events.index("group-signal"), first_reap)
        self.assertNotIn("group-signal", events[first_reap + 1 :])

    def test_idempotent_cleanup_never_signals_after_leader_is_reaped(self):
        process = subprocess.Popen(
            [sys.executable, "-I", "-c", "pass"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        process.wait(timeout=2)

        with patch.object(RUNNER.os, "killpg") as group_signal:
            complete = RUNNER.cleanup_process_group(process, 0.5)

        self.assertTrue(complete)
        group_signal.assert_not_called()
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)

    def test_reaped_leader_requires_signal_free_group_absence_proof(self):
        process = subprocess.Popen(
            [sys.executable, "-I", "-c", "pass"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        process.wait(timeout=2)

        with (
            patch.object(
                RUNNER, "_process_group_absent", return_value=False
            ) as group_absence,
            patch.object(RUNNER.os, "killpg") as group_signal,
        ):
            complete = RUNNER.cleanup_process_group(process, 0.1)

        self.assertFalse(complete)
        group_absence.assert_called_with(process.pid)
        group_signal.assert_not_called()
        self.assertTrue(process.stdout.closed)
        self.assertTrue(process.stderr.closed)

    def test_subreaper_and_interrupt_mask_are_restored(self):
        before_subreaper = RUNNER._get_subreaper_state()
        before_mask = signal.pthread_sigmask(signal.SIG_BLOCK, set())

        outcome = self._run_python("pass")

        after_mask = signal.pthread_sigmask(signal.SIG_BLOCK, set())
        self.assertEqual(outcome.status, "completed")
        self.assertEqual(RUNNER._get_subreaper_state(), before_subreaper)
        self.assertEqual(after_mask, before_mask)

    def test_subreaper_restore_failure_cannot_return_success(self):
        with (
            patch.object(RUNNER, "_set_subreaper_state", side_effect=(True, False)),
            self.assertRaisesRegex(RuntimeError, "subreaper state restoration"),
        ):
            self._run_python("pass")

    def test_reaped_leader_numeric_pid_is_not_reused_as_discovery_root(self):
        class _Pipe:
            closed = False

            def close(self):
                self.closed = True

        class _Process:
            pid = 424244

            def __init__(self):
                self.stdout = _Pipe()
                self.stderr = _Pipe()
                self.returncode = None

            def wait(self, timeout=None):
                del timeout
                self.returncode = 0
                return 0

        process = _Process()
        discovery_roots = []

        def observe_discovery(leader_pid, _baseline):
            discovery_roots.append(leader_pid)
            return set()

        with (
            patch.object(RUNNER, "_discover_owned_pids", side_effect=observe_discovery),
            patch.object(RUNNER, "_process_group_absent", return_value=True),
            patch.object(RUNNER.os, "killpg"),
        ):
            complete = RUNNER.cleanup_process_group(process, 0.5)

        self.assertTrue(complete)
        self.assertEqual(discovery_roots[0], process.pid)
        self.assertIn(0, discovery_roots[1:])
        first_adopted_scan = discovery_roots.index(0)
        self.assertNotIn(process.pid, discovery_roots[first_adopted_scan:])

    def test_repeated_cleanup_interrupts_do_not_skip_close_or_reap(self):
        process = subprocess.Popen(
            [sys.executable, "-I", "-c", "import signal; signal.pause()"],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
        real_killpg = RUNNER.os.killpg

        class _InterruptingPipe:
            def __init__(self, pipe):
                self._pipe = pipe

            @property
            def closed(self):
                return self._pipe.closed

            def fileno(self):
                return self._pipe.fileno()

            def close(self):
                self._pipe.close()
                raise KeyboardInterrupt("synthetic pipe-close interrupt")

        process.stdout = _InterruptingPipe(process.stdout)

        def interrupting_group_signal(pgid, sig):
            real_killpg(pgid, sig)
            raise KeyboardInterrupt("synthetic group-signal interrupt")

        try:
            with (
                patch.object(
                    RUNNER.os, "killpg", side_effect=interrupting_group_signal
                ),
                self.assertRaises(KeyboardInterrupt),
            ):
                RUNNER.cleanup_process_group(process, 0.5)

            self.assertIsNotNone(process.returncode)
            self.assertTrue(process.stdout.closed)
            self.assertTrue(process.stderr.closed)
        finally:
            if process.poll() is None:
                try:
                    real_killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait(timeout=2)


class PureAffectedSelectorRunnerTest(unittest.TestCase):
    def test_deleted_markdown_is_not_classified_for_current_include_arguments(self):
        contract_module = RUNNER.load_contract_module()
        contract = contract_module.validate_contract(ROOT)
        validator = next(
            row for row in contract["validators"] if row["id"] == "markdown-profiles"
        )
        with tempfile.TemporaryDirectory(prefix="retired-runner-") as temporary:
            with patch.object(
                contract_module,
                "classify_path",
                side_effect=AssertionError("absent document was classified"),
            ) as classify:
                actual = RUNNER.validator_argv(
                    Path(temporary),
                    "affected",
                    ["retired-policy.md"],
                    validator,
                    contract,
                    contract_module,
                )
        self.assertEqual(actual, validator["argv"])
        classify.assert_not_called()

    def test_proven_deleted_markdown_keeps_scope_and_validator_failure(self):
        contract_module = RUNNER.load_contract_module()
        contract = contract_module.validate_contract(ROOT)
        paths = ["retired-policy.md", "retired-policy.md"]
        output = StringIO()
        with (
            tempfile.TemporaryDirectory(prefix="retired-runner-") as temporary,
            patch.object(
                contract_module,
                "select_paths",
                return_value={"validators": ["markdown-profiles"]},
            ) as select,
            patch.object(
                contract_module,
                "classify_path",
                side_effect=AssertionError("absent document was classified"),
            ),
            patch.object(RUNNER.shutil, "which", return_value="/usr/bin/python3"),
            patch.object(RUNNER, "secure_gitleaks_executable", return_value=None),
            patch.object(
                RUNNER,
                "run_bounded_command",
                return_value=bounded_result(returncode=7),
            ) as invoked,
            redirect_stdout(output),
        ):
            root = Path(temporary)
            result = RUNNER.run_selected(
                root, "affected", paths, contract, contract_module
            )
            select.assert_called_once_with(contract, paths, "affected", root)
        self.assertEqual(result, 1)
        self.assertIn("[FAIL] markdown-profiles", output.getvalue())
        self.assertIn('scope="affected:paths=2"', output.getvalue())
        self.assertNotIn("--include-path", invoked.call_args.args[0])

    @staticmethod
    def _run(paths: list[str], lane: str = "affected"):
        contract_module = RUNNER.load_contract_module()
        contract = contract_module.validate_contract(ROOT)
        completed = bounded_result(QUALITY_MARKER + "\n")
        output = StringIO()
        with (
            patch.object(RUNNER.shutil, "which", return_value="/usr/bin/bash"),
            patch.object(
                RUNNER, "run_bounded_command", return_value=completed
            ) as invoked,
            redirect_stdout(output),
        ):
            result = RUNNER.run_selected(
                ROOT,
                lane,
                paths,
                contract,
                contract_module,
            )
        statuses = {
            identifier: status
            for status, identifier in re.findall(
                r"^\[(PASS|SKIP|FAIL|DEFER)\] ([^ ]+) ",
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
        path = (
            "docs/98.archive/changes/"
            "chg-0004-archive-record-and-workspace-boundary/task.md"
        )
        result, statuses, output, invoked = self._run([path])

        self.assertEqual(result, 0)
        self.assertEqual(
            statuses,
            {
                "agent-governance-ci": "PASS",
                "agent-governance-closure": "PASS",
                "agent-legacy-cutover": "PASS",
                "document-contract-registry": "PASS",
                "document-lifecycle": "PASS",
                "links-and-owners": "PASS",
                "markdown-profiles": "PASS",
                "repository-quality": "PASS",
            },
        )
        self.assertEqual(invoked.call_count, 8)
        self.assertGreaterEqual(output.count(path), 3)

    def test_staged_selector_executes_every_selected_validator(self):
        path = "docs/03.specs/0045-agent-governance-ci-qa-cutover/spec.md"
        result, statuses, output, invoked = self._run([path], lane="staged")

        self.assertEqual(result, 0)
        self.assertEqual(
            statuses,
            {
                "agent-governance-ci": "PASS",
                "agent-governance-closure": "PASS",
                "agent-legacy-cutover": "PASS",
                "document-contract-registry": "PASS",
                "document-lifecycle": "PASS",
                "links-and-owners": "PASS",
                "markdown-profiles": "PASS",
                "repository-quality": "PASS",
            },
        )
        self.assertEqual(invoked.call_count, 8)
        self.assertIn('scope="staged:paths=1"', output)
        propagated = [
            call.args[0] for call in invoked.call_args_list if path in call.args[0]
        ]
        self.assertEqual(len(propagated), 3)
        for argv in propagated:
            self.assertIn("--include-path", argv)


if __name__ == "__main__":
    unittest.main()
