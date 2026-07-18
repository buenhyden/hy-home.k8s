from __future__ import annotations

import builtins
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = REPOSITORY_ROOT / "scripts" / "validate-workspace-boundary.py"
AGGREGATE_PATH = REPOSITORY_ROOT / "scripts" / "validate-repo-quality-gates.sh"
OBJECT_ID = b"a" * 40
README_RECORD = b"100644 " + OBJECT_ID + b" 0\t_workspace/README.md\0"
ROOT_POLICY = b"_workspace/*\n!_workspace/README.md\n"
ROOT_IGNORE_RECORD = b"100644 " + OBJECT_ID + b" 0\t.gitignore\0"


def load_validator():
    specification = importlib.util.spec_from_file_location(
        "workspace_boundary_validator_test_target", VALIDATOR_PATH
    )
    if specification is None or specification.loader is None:
        raise AssertionError("workspace boundary validator could not be loaded")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def completed(arguments: tuple[str, ...], returncode: int, stdout: bytes = b""):
    return subprocess.CompletedProcess(arguments, returncode, stdout, b"")


class InjectedGit:
    def __init__(
        self,
        *,
        index: bytes = README_RECORD,
        root_ignore_index: bytes | None = None,
        root_ignore_object_id: bytes = OBJECT_ID,
        root_policy: bytes = ROOT_POLICY,
        root_policy_size: bytes | None = None,
        probe_status: int = 0,
        readme_status: int = 1,
    ) -> None:
        self.index = index
        self.root_ignore_object_id = root_ignore_object_id
        self.root_ignore_index = (
            b"100644 " + root_ignore_object_id + b" 0\t.gitignore\0"
            if root_ignore_index is None
            else root_ignore_index
        )
        self.root_policy = root_policy
        self.root_policy_size = (
            f"{len(root_policy)}\n".encode("ascii")
            if root_policy_size is None
            else root_policy_size
        )
        self.probe_status = probe_status
        self.readme_status = readme_status
        self.calls: list[tuple[str, tuple[str, ...]]] = []

    def __call__(self, root: str, arguments: tuple[str, ...]):
        self.calls.append((root, arguments))
        if arguments == ("ls-files", "--stage", "-z", "--", "_workspace"):
            return completed(arguments, 0, self.index)
        if arguments == ("ls-files", "--stage", "-z", "--", ".gitignore"):
            return completed(arguments, 0, self.root_ignore_index)
        object_id = self.root_ignore_object_id.decode("ascii")
        if arguments == ("cat-file", "-s", object_id):
            return completed(arguments, 0, self.root_policy_size)
        if arguments == ("cat-file", "blob", object_id):
            return completed(arguments, 0, self.root_policy)
        if arguments == ("init", "--quiet"):
            return completed(arguments, 0)
        if arguments == (
            "check-ignore",
            "--no-index",
            "--quiet",
            "--",
            "_workspace/probe.log",
        ):
            return completed(arguments, self.probe_status)
        if arguments == (
            "check-ignore",
            "--no-index",
            "--quiet",
            "--",
            "_workspace/README.md",
        ):
            return completed(arguments, self.readme_status)
        raise AssertionError(f"unexpected Git arguments: {arguments!r}")


class WorkspaceBoundaryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = load_validator()

    def assert_boundary_error(
        self,
        runner: InjectedGit,
        expected: tuple[str, str],
    ) -> None:
        with self.assertRaises(self.validator.WorkspaceBoundaryError) as raised:
            self.validator.validate_workspace_boundary("/fixture/repository", runner)
        self.assertEqual((raised.exception.code, raised.exception.path), expected)
        self.assertEqual(str(raised.exception), " ".join(expected))

    def isolated_repository_with_child_ignore(
        self,
        *,
        root_policy: str,
        child_policy: str,
    ) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory(prefix="workspace-boundary-hostile-")
        root = Path(temporary.name)
        initialized = subprocess.run(
            ["/usr/bin/git", "init", "--quiet"],
            cwd=root,
            env=self.validator.CLOSED_GIT_ENVIRONMENT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        (root / ".gitignore").write_text(root_policy, encoding="utf-8")
        workspace = root / "_workspace"
        workspace.mkdir()
        (workspace / "README.md").write_text("fixture\n", encoding="utf-8")
        added = subprocess.run(
            [
                "/usr/bin/git",
                "add",
                "--",
                ".gitignore",
                "_workspace/README.md",
            ],
            cwd=root,
            env=self.validator.CLOSED_GIT_ENVIRONMENT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(added.returncode, 0, added.stderr)
        (workspace / ".gitignore").write_text(child_policy, encoding="utf-8")
        return temporary, root

    def test_ignored_child_policy_cannot_hide_wrong_root_policy(self) -> None:
        temporary, root = self.isolated_repository_with_child_ignore(
            root_policy=(
                "_workspace/.gitignore\n!_workspace/probe.log\n!_workspace/README.md\n"
            ),
            child_policy="probe.log\n",
        )
        try:
            with self.assertRaises(self.validator.WorkspaceBoundaryError) as raised:
                self.validator.validate_workspace_boundary(root)
            self.assertEqual(
                (raised.exception.code, raised.exception.path),
                ("WORKSPACE-SCRATCH-NOT-IGNORED", "_workspace/probe.log"),
            )
        finally:
            temporary.cleanup()

    def test_ignored_child_policy_cannot_override_correct_root_policy(self) -> None:
        temporary, root = self.isolated_repository_with_child_ignore(
            root_policy="_workspace/*\n!_workspace/README.md\n",
            child_policy="!probe.log\nREADME.md\n",
        )
        try:
            self.validator.validate_workspace_boundary(root)
        finally:
            temporary.cleanup()

    def test_worktree_root_policy_cannot_override_staged_blob(self) -> None:
        temporary, root = self.isolated_repository_with_child_ignore(
            root_policy="_workspace/*\n!_workspace/README.md\n",
            child_policy="",
        )
        try:
            (root / ".gitignore").write_text(
                "!_workspace/probe.log\n_workspace/README.md\n",
                encoding="utf-8",
            )
            self.validator.validate_workspace_boundary(root)
        finally:
            temporary.cleanup()

    def test_uses_only_bounded_index_blob_and_isolated_ignore_queries(self) -> None:
        runner = InjectedGit()

        self.validator.validate_workspace_boundary("/fixture/repository", runner)

        actual_root = "/fixture/repository"
        self.assertEqual(
            runner.calls[:4],
            [
                (actual_root, ("ls-files", "--stage", "-z", "--", "_workspace")),
                (actual_root, ("ls-files", "--stage", "-z", "--", ".gitignore")),
                (actual_root, ("cat-file", "-s", OBJECT_ID.decode("ascii"))),
                (actual_root, ("cat-file", "blob", OBJECT_ID.decode("ascii"))),
            ],
        )
        isolated_roots = {root for root, _ in runner.calls[4:]}
        self.assertEqual(len(isolated_roots), 1)
        isolated_root = isolated_roots.pop()
        self.assertNotEqual(isolated_root, actual_root)
        self.assertEqual(
            runner.calls[4:],
            [
                (isolated_root, ("init", "--quiet")),
                (
                    isolated_root,
                    (
                        "check-ignore",
                        "--no-index",
                        "--quiet",
                        "--",
                        "_workspace/probe.log",
                    ),
                ),
                (
                    isolated_root,
                    (
                        "check-ignore",
                        "--no-index",
                        "--quiet",
                        "--",
                        "_workspace/README.md",
                    ),
                ),
            ],
        )

    def test_never_traverses_stats_or_opens_workspace_children(self) -> None:
        runner = InjectedGit()
        actual_workspace = os.path.abspath("/fixture/repository/_workspace")
        actual_root_ignore = os.path.abspath("/fixture/repository/.gitignore")

        def is_actual_workspace(value) -> bool:
            if isinstance(value, int):
                return False
            try:
                candidate = os.path.abspath(os.fspath(value))
            except TypeError:
                return False
            return (
                candidate == actual_root_ignore
                or candidate == actual_workspace
                or candidate.startswith(actual_workspace + os.sep)
            )

        def guard(function):
            def wrapped(value, *args, **kwargs):
                if is_actual_workspace(value):
                    raise AssertionError("actual workspace sentinel invoked")
                return function(value, *args, **kwargs)

            return wrapped

        with (
            mock.patch.object(builtins, "open", guard(builtins.open)),
            mock.patch.object(os, "listdir", guard(os.listdir)),
            mock.patch.object(os, "scandir", guard(os.scandir)),
            mock.patch.object(os, "walk", guard(os.walk)),
            mock.patch.object(os, "stat", guard(os.stat)),
            mock.patch.object(Path, "glob", guard(Path.glob)),
            mock.patch.object(Path, "rglob", guard(Path.rglob)),
            mock.patch.object(Path, "iterdir", guard(Path.iterdir)),
            mock.patch.object(Path, "open", guard(Path.open)),
            mock.patch.object(Path, "read_bytes", guard(Path.read_bytes)),
            mock.patch.object(Path, "read_text", guard(Path.read_text)),
            mock.patch.object(Path, "stat", guard(Path.stat)),
            mock.patch.object(Path, "lstat", guard(Path.lstat)),
        ):
            self.validator.validate_workspace_boundary("/fixture/repository", runner)

    def test_requires_canonical_stage_zero_regular_root_ignore_entry(self) -> None:
        cases = (
            (
                b"",
                ("WORKSPACE-ROOT-IGNORE-MISSING", ".gitignore"),
            ),
            (
                ROOT_IGNORE_RECORD + ROOT_IGNORE_RECORD,
                ("WORKSPACE-ROOT-IGNORE-CARDINALITY", ".gitignore"),
            ),
            (
                b"100644 " + OBJECT_ID + b" 2\t.gitignore\0",
                ("WORKSPACE-ROOT-IGNORE-CONFLICT", ".gitignore"),
            ),
            (
                b"120000 " + OBJECT_ID + b" 0\t.gitignore\0",
                ("WORKSPACE-ROOT-IGNORE-NONREGULAR", ".gitignore"),
            ),
            (
                b"100755 " + OBJECT_ID + b" 0\t.gitignore\0",
                ("WORKSPACE-ROOT-IGNORE-MODE", ".gitignore"),
            ),
        )
        for root_ignore_index, expected in cases:
            with self.subTest(expected=expected):
                self.assert_boundary_error(
                    InjectedGit(root_ignore_index=root_ignore_index), expected
                )

    def test_accepts_full_sha1_and_sha256_root_ignore_blob_ids(self) -> None:
        for object_id in (b"a" * 40, b"b" * 64):
            with self.subTest(length=len(object_id)):
                self.validator.validate_workspace_boundary(
                    "/fixture/repository",
                    InjectedGit(root_ignore_object_id=object_id),
                )

    def test_bounds_root_ignore_size_and_blob_output(self) -> None:
        cases = (
            (
                InjectedGit(root_policy_size=b"not-a-size\n"),
                ("WORKSPACE-ROOT-IGNORE-SIZE", ".gitignore"),
            ),
            (
                InjectedGit(
                    root_policy_size=(
                        f"{self.validator.MAX_ROOT_IGNORE_BYTES + 1}\n".encode("ascii")
                    )
                ),
                ("WORKSPACE-ROOT-IGNORE-SIZE", ".gitignore"),
            ),
            (
                InjectedGit(root_policy_size=b"1\n"),
                ("WORKSPACE-ROOT-IGNORE-BLOB", ".gitignore"),
            ),
        )
        for runner, expected in cases:
            with self.subTest(expected=expected):
                self.assert_boundary_error(runner, expected)

    def test_rejects_missing_extra_force_added_and_duplicate_children(self) -> None:
        cases = (
            (b"", ("WORKSPACE-README-MISSING", "_workspace/README.md")),
            (
                README_RECORD + b"100644 " + OBJECT_ID + b" 0\t_workspace/extra.log\0",
                ("WORKSPACE-TRACKED-EXTRA", "_workspace/extra.log"),
            ),
            (
                README_RECORD + b"100644 " + OBJECT_ID + b" 0\t_workspace/forced.log\0",
                ("WORKSPACE-TRACKED-EXTRA", "_workspace/forced.log"),
            ),
            (
                README_RECORD + README_RECORD,
                ("WORKSPACE-README-CARDINALITY", "_workspace/README.md"),
            ),
        )
        for index, expected in cases:
            with self.subTest(expected=expected):
                self.assert_boundary_error(InjectedGit(index=index), expected)

    def test_rejects_conflict_symlink_gitlink_and_noncanonical_mode(self) -> None:
        cases = (
            (
                b"100644 " + OBJECT_ID + b" 2\t_workspace/README.md\0",
                ("WORKSPACE-INDEX-CONFLICT", "_workspace/README.md"),
            ),
            (
                b"120000 " + OBJECT_ID + b" 0\t_workspace/README.md\0",
                ("WORKSPACE-TRACKED-NONREGULAR", "_workspace/README.md"),
            ),
            (
                b"160000 " + OBJECT_ID + b" 0\t_workspace/README.md\0",
                ("WORKSPACE-TRACKED-NONREGULAR", "_workspace/README.md"),
            ),
            (
                b"100755 " + OBJECT_ID + b" 0\t_workspace/README.md\0",
                ("WORKSPACE-README-MODE", "_workspace/README.md"),
            ),
        )
        for index, expected in cases:
            with self.subTest(expected=expected):
                self.assert_boundary_error(InjectedGit(index=index), expected)

    def test_rejects_malformed_nul_index_records_without_leaking_values(self) -> None:
        malformed_records = (
            README_RECORD.rstrip(b"\0"),
            b"100644 " + OBJECT_ID + b" 0 _workspace/README.md\0",
            b"100644 " + b"z" * 40 + b" 0\t_workspace/README.md\0",
            b"100644 " + b"0" * 40 + b" 0\t_workspace/README.md\0",
            b"100644 " + OBJECT_ID + b" 4\t_workspace/README.md\0",
            b"100644 " + OBJECT_ID + b" 0\t_workspace/README.md\0\0",
            b"100644 " + OBJECT_ID + b" 0\t_workspace/\xff\0",
            b"100644 " + OBJECT_ID + b" 0\t_workspace/bad\nname\0",
        )
        for index in malformed_records:
            with self.subTest(index=index[-24:]):
                self.assert_boundary_error(
                    InjectedGit(index=index),
                    ("WORKSPACE-INDEX-MALFORMED", "_workspace"),
                )

    def test_requires_scratch_ignored_and_readme_unignored(self) -> None:
        self.assert_boundary_error(
            InjectedGit(probe_status=1),
            ("WORKSPACE-SCRATCH-NOT-IGNORED", "_workspace/probe.log"),
        )
        self.assert_boundary_error(
            InjectedGit(readme_status=0),
            ("WORKSPACE-README-IGNORED", "_workspace/README.md"),
        )
        self.assert_boundary_error(
            InjectedGit(probe_status=128),
            ("WORKSPACE-GIT-FAILED", "_workspace/probe.log"),
        )
        self.assert_boundary_error(
            InjectedGit(readme_status=128),
            ("WORKSPACE-GIT-FAILED", "_workspace/README.md"),
        )

    def test_default_git_runner_is_bounded_closed_and_shell_free(self) -> None:
        with mock.patch.object(
            self.validator.subprocess,
            "run",
            return_value=completed(("git",), 0),
        ) as run:
            self.validator._run_git(
                "/fixture/repository",
                ("ls-files", "--stage", "-z", "--", "_workspace"),
            )

        kwargs = run.call_args.kwargs
        self.assertEqual(
            run.call_args.args[0],
            [
                "/usr/bin/git",
                "ls-files",
                "--stage",
                "-z",
                "--",
                "_workspace",
            ],
        )
        self.assertEqual(kwargs["cwd"], "/fixture/repository")
        self.assertIs(kwargs["shell"], False)
        self.assertIs(kwargs["check"], False)
        self.assertEqual(kwargs["timeout"], self.validator.GIT_TIMEOUT_SECONDS)
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        self.assertEqual(kwargs["stdout"], subprocess.PIPE)
        self.assertEqual(kwargs["stderr"], subprocess.DEVNULL)
        environment = kwargs["env"]
        self.assertEqual(environment, self.validator.LITERAL_INDEX_GIT_ENVIRONMENT)
        self.assertEqual(environment["PATH"], "/usr/bin:/bin")
        self.assertEqual(environment["GIT_LITERAL_PATHSPECS"], "1")
        self.assertNotIn("PYTHONPATH", environment)
        self.assertNotIn("BASH_ENV", environment)

    def test_git_startup_and_timeout_errors_are_stable(self) -> None:
        with mock.patch.object(
            self.validator.subprocess,
            "run",
            side_effect=OSError("DO_NOT_EMIT_SENTINEL"),
        ):
            with self.assertRaises(self.validator.WorkspaceBoundaryError) as raised:
                self.validator._run_git(
                    "/fixture/repository",
                    ("ls-files", "--stage", "-z", "--", "_workspace"),
                )
        self.assertEqual(str(raised.exception), "WORKSPACE-GIT-STARTUP _workspace")

        with mock.patch.object(
            self.validator.subprocess,
            "run",
            side_effect=subprocess.TimeoutExpired(
                ["/usr/bin/git"], self.validator.GIT_TIMEOUT_SECONDS
            ),
        ):
            with self.assertRaises(self.validator.WorkspaceBoundaryError) as raised:
                self.validator._run_git(
                    "/fixture/repository",
                    (
                        "check-ignore",
                        "--no-index",
                        "--quiet",
                        "--",
                        "_workspace/probe.log",
                    ),
                )
        self.assertEqual(
            str(raised.exception),
            "WORKSPACE-GIT-TIMEOUT _workspace/probe.log",
        )


class WorkspaceBoundaryCliTests(unittest.TestCase):
    def test_self_test_passes(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR_PATH), "--self-test"],
            cwd=REPOSITORY_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "[PASS] workspace boundary self-test\n")
        self.assertEqual(result.stderr, "")

    def test_aggregate_runs_self_test_then_production_validator(self) -> None:
        aggregate = AGGREGATE_PATH.read_text(encoding="utf-8")
        self.assertIn(
            'python3 "$ROOT_DIR/scripts/validate-workspace-boundary.py" --self-test',
            aggregate,
        )
        self.assertIn(
            'python3 "$ROOT_DIR/scripts/validate-workspace-boundary.py" --root "$ROOT_DIR"',
            aggregate,
        )
        self.assertLess(
            aggregate.index('validate-workspace-boundary.py" --self-test'),
            aggregate.index('validate-workspace-boundary.py" --root'),
        )
        self.assertNotIn("workspace_scratch_ignore_check", aggregate)
        self.assertNotIn("workspace_tracked_paths", aggregate)


if __name__ == "__main__":
    unittest.main()
