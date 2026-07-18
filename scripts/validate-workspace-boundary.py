#!/usr/bin/env python3
"""Validate the `_workspace` boundary without reading its worktree children."""

from __future__ import annotations

import argparse
import builtins
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import NamedTuple
from unittest import mock


GIT_TIMEOUT_SECONDS = 10
MAX_ROOT_IGNORE_BYTES = 65_536
GIT_EXECUTABLE = "/usr/bin/git"
WORKSPACE_ROOT = "_workspace"
WORKSPACE_README = "_workspace/README.md"
WORKSPACE_PROBE = "_workspace/probe.log"
ROOT_IGNORE = ".gitignore"
INDEX_ARGUMENTS = ("ls-files", "--stage", "-z", "--", WORKSPACE_ROOT)
ROOT_IGNORE_INDEX_ARGUMENTS = ("ls-files", "--stage", "-z", "--", ROOT_IGNORE)
ISOLATED_INIT_ARGUMENTS = ("init", "--quiet")
PROBE_IGNORE_ARGUMENTS = (
    "check-ignore",
    "--no-index",
    "--quiet",
    "--",
    WORKSPACE_PROBE,
)
README_IGNORE_ARGUMENTS = (
    "check-ignore",
    "--no-index",
    "--quiet",
    "--",
    WORKSPACE_README,
)
ALLOWED_GIT_ARGUMENTS = frozenset(
    (
        INDEX_ARGUMENTS,
        ROOT_IGNORE_INDEX_ARGUMENTS,
        ISOLATED_INIT_ARGUMENTS,
        PROBE_IGNORE_ARGUMENTS,
        README_IGNORE_ARGUMENTS,
    )
)
CLOSED_GIT_ENVIRONMENT = {
    "GIT_CONFIG_COUNT": "2",
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_KEY_0": "core.excludesFile",
    "GIT_CONFIG_KEY_1": "core.fsmonitor",
    "GIT_CONFIG_NOSYSTEM": "1",
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_CONFIG_VALUE_0": os.devnull,
    "GIT_CONFIG_VALUE_1": "false",
    "GIT_NO_LAZY_FETCH": "1",
    "GIT_NO_REPLACE_OBJECTS": "1",
    "GIT_OPTIONAL_LOCKS": "0",
    "GIT_PAGER": "cat",
    "GIT_TERMINAL_PROMPT": "0",
    "HOME": "/nonexistent",
    "LANG": "C",
    "LC_ALL": "C",
    "PAGER": "cat",
    "PATH": "/usr/bin:/bin",
}
LITERAL_INDEX_GIT_ENVIRONMENT = {
    **CLOSED_GIT_ENVIRONMENT,
    "GIT_LITERAL_PATHSPECS": "1",
}
_INDEX_HEADER = re.compile(
    rb"(?P<mode>[0-9]{6}) (?P<object>[0-9a-f]+) (?P<stage>[0-9])\Z"
)
_SAFE_WORKSPACE_PATH = re.compile(r"_workspace(?:/[A-Za-z0-9._@+-]+)+\Z")
_FULL_OBJECT_ID = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})\Z")


class WorkspaceBoundaryError(ValueError):
    """One stable diagnostic containing only a code and repository path."""

    def __init__(self, code: str, path: str) -> None:
        super().__init__(code, path)
        self.code = code
        self.path = path

    def __str__(self) -> str:
        return f"{self.code} {self.path}"


GitRunner = Callable[[str, tuple[str, ...]], subprocess.CompletedProcess[bytes]]


class IndexEntry(NamedTuple):
    mode: str
    object_id: str
    stage: int
    path: str


def _query_path(arguments: tuple[str, ...]) -> str:
    if arguments == PROBE_IGNORE_ARGUMENTS:
        return WORKSPACE_PROBE
    if arguments == README_IGNORE_ARGUMENTS:
        return WORKSPACE_README
    if arguments == INDEX_ARGUMENTS:
        return WORKSPACE_ROOT
    if arguments == ISOLATED_INIT_ARGUMENTS:
        return ROOT_IGNORE
    if arguments == ROOT_IGNORE_INDEX_ARGUMENTS or (
        len(arguments) == 3
        and arguments[:2] in {("cat-file", "-s"), ("cat-file", "blob")}
    ):
        return ROOT_IGNORE
    return WORKSPACE_ROOT


def _git_arguments_allowed(arguments: tuple[str, ...]) -> bool:
    if arguments in ALLOWED_GIT_ARGUMENTS:
        return True
    return bool(
        len(arguments) == 3
        and arguments[:2] in {("cat-file", "-s"), ("cat-file", "blob")}
        and _FULL_OBJECT_ID.fullmatch(arguments[2])
    )


def _normalize_root(root: str | os.PathLike[str]) -> str:
    try:
        value = os.fspath(root)
    except TypeError as exc:
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-INVALID", ".") from exc
    if not isinstance(value, str) or not value or "\0" in value:
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-INVALID", ".")
    try:
        return os.path.abspath(value)
    except (OSError, ValueError) as exc:
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-INVALID", ".") from exc


def _run_git(
    root: str,
    arguments: tuple[str, ...],
) -> subprocess.CompletedProcess[bytes]:
    """Run one allow-listed, bounded, literal Git metadata query."""

    path = _query_path(arguments)
    if not _git_arguments_allowed(arguments):
        raise WorkspaceBoundaryError("WORKSPACE-GIT-QUERY", path)
    environment = (
        LITERAL_INDEX_GIT_ENVIRONMENT
        if arguments in {INDEX_ARGUMENTS, ROOT_IGNORE_INDEX_ARGUMENTS}
        else CLOSED_GIT_ENVIRONMENT
    )
    try:
        return subprocess.run(
            [GIT_EXECUTABLE, *arguments],
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=environment,
            timeout=GIT_TIMEOUT_SECONDS,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise WorkspaceBoundaryError("WORKSPACE-GIT-TIMEOUT", path) from exc
    except OSError as exc:
        raise WorkspaceBoundaryError("WORKSPACE-GIT-STARTUP", path) from exc


def _safe_index_path(raw_path: bytes, *, error_path: str) -> str:
    try:
        path = raw_path.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise WorkspaceBoundaryError("WORKSPACE-INDEX-MALFORMED", error_path) from exc
    if path == ROOT_IGNORE:
        return path
    if (
        not _SAFE_WORKSPACE_PATH.fullmatch(path)
        or "//" in path
        or "/./" in path
        or "/../" in path
        or path.endswith(("/.", "/.."))
        or "\\" in path
        or any(ord(character) < 32 or ord(character) == 127 for character in path)
    ):
        raise WorkspaceBoundaryError("WORKSPACE-INDEX-MALFORMED", error_path)
    return path


def _parse_index(output: bytes, *, error_path: str) -> tuple[IndexEntry, ...]:
    if not isinstance(output, bytes):
        raise WorkspaceBoundaryError("WORKSPACE-INDEX-MALFORMED", error_path)
    if not output:
        return ()
    if not output.endswith(b"\0"):
        raise WorkspaceBoundaryError("WORKSPACE-INDEX-MALFORMED", error_path)

    records = output[:-1].split(b"\0")
    if any(not record for record in records):
        raise WorkspaceBoundaryError("WORKSPACE-INDEX-MALFORMED", error_path)

    entries: list[IndexEntry] = []
    for record in records:
        if record.count(b"\t") != 1:
            raise WorkspaceBoundaryError("WORKSPACE-INDEX-MALFORMED", error_path)
        header, raw_path = record.split(b"\t", 1)
        match = _INDEX_HEADER.fullmatch(header)
        if match is None:
            raise WorkspaceBoundaryError("WORKSPACE-INDEX-MALFORMED", error_path)
        object_id = match.group("object")
        if len(object_id) not in {40, 64} or not object_id.strip(b"0"):
            raise WorkspaceBoundaryError("WORKSPACE-INDEX-MALFORMED", error_path)
        stage = int(match.group("stage"))
        if stage not in {0, 1, 2, 3}:
            raise WorkspaceBoundaryError("WORKSPACE-INDEX-MALFORMED", error_path)
        mode = match.group("mode").decode("ascii")
        entries.append(
            IndexEntry(
                mode,
                object_id.decode("ascii"),
                stage,
                _safe_index_path(raw_path, error_path=error_path),
            )
        )
    return tuple(entries)


def _validate_index(output: bytes) -> None:
    entries = _parse_index(output, error_path=WORKSPACE_ROOT)
    readme_count = 0
    for entry in entries:
        if entry.path != WORKSPACE_README:
            raise WorkspaceBoundaryError("WORKSPACE-TRACKED-EXTRA", entry.path)
        if entry.stage != 0:
            raise WorkspaceBoundaryError("WORKSPACE-INDEX-CONFLICT", entry.path)
        if entry.mode not in {"100644", "100755"}:
            raise WorkspaceBoundaryError("WORKSPACE-TRACKED-NONREGULAR", entry.path)
        if entry.mode != "100644":
            raise WorkspaceBoundaryError("WORKSPACE-README-MODE", entry.path)
        readme_count += 1

    if readme_count == 0:
        raise WorkspaceBoundaryError("WORKSPACE-README-MISSING", WORKSPACE_README)
    if readme_count != 1:
        raise WorkspaceBoundaryError("WORKSPACE-README-CARDINALITY", WORKSPACE_README)


def _require_git_success(
    result: subprocess.CompletedProcess[bytes],
    path: str,
) -> None:
    if not isinstance(result, subprocess.CompletedProcess) or result.returncode != 0:
        raise WorkspaceBoundaryError("WORKSPACE-GIT-FAILED", path)


def _load_root_ignore_blob(root: str, runner: GitRunner) -> bytes:
    index = runner(root, ROOT_IGNORE_INDEX_ARGUMENTS)
    _require_git_success(index, ROOT_IGNORE)
    entries = _parse_index(index.stdout, error_path=ROOT_IGNORE)
    if not entries:
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-IGNORE-MISSING", ROOT_IGNORE)
    if len(entries) != 1 or entries[0].path != ROOT_IGNORE:
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-IGNORE-CARDINALITY", ROOT_IGNORE)
    entry = entries[0]
    if entry.stage != 0:
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-IGNORE-CONFLICT", ROOT_IGNORE)
    if entry.mode not in {"100644", "100755"}:
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-IGNORE-NONREGULAR", ROOT_IGNORE)
    if entry.mode != "100644":
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-IGNORE-MODE", ROOT_IGNORE)

    size_result = runner(root, ("cat-file", "-s", entry.object_id))
    _require_git_success(size_result, ROOT_IGNORE)
    if not isinstance(size_result.stdout, bytes) or not re.fullmatch(
        rb"(?:0|[1-9][0-9]*)\n", size_result.stdout
    ):
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-IGNORE-SIZE", ROOT_IGNORE)
    size = int(size_result.stdout)
    if size > MAX_ROOT_IGNORE_BYTES:
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-IGNORE-SIZE", ROOT_IGNORE)

    blob_result = runner(root, ("cat-file", "blob", entry.object_id))
    _require_git_success(blob_result, ROOT_IGNORE)
    if not isinstance(blob_result.stdout, bytes) or len(blob_result.stdout) != size:
        raise WorkspaceBoundaryError("WORKSPACE-ROOT-IGNORE-BLOB", ROOT_IGNORE)
    return blob_result.stdout


def _validate_ignore_policy(blob: bytes, runner: GitRunner) -> None:
    try:
        with tempfile.TemporaryDirectory(
            prefix="workspace-ignore-policy-"
        ) as directory:
            isolated_root = os.path.abspath(directory)
            initialized = runner(isolated_root, ISOLATED_INIT_ARGUMENTS)
            _require_git_success(initialized, ROOT_IGNORE)
            (Path(isolated_root) / ROOT_IGNORE).write_bytes(blob)

            probe = runner(isolated_root, PROBE_IGNORE_ARGUMENTS)
            if not isinstance(probe, subprocess.CompletedProcess):
                raise WorkspaceBoundaryError("WORKSPACE-GIT-FAILED", WORKSPACE_PROBE)
            if probe.returncode == 1:
                raise WorkspaceBoundaryError(
                    "WORKSPACE-SCRATCH-NOT-IGNORED", WORKSPACE_PROBE
                )
            if probe.returncode != 0:
                raise WorkspaceBoundaryError("WORKSPACE-GIT-FAILED", WORKSPACE_PROBE)

            readme = runner(isolated_root, README_IGNORE_ARGUMENTS)
            if not isinstance(readme, subprocess.CompletedProcess):
                raise WorkspaceBoundaryError("WORKSPACE-GIT-FAILED", WORKSPACE_README)
            if readme.returncode == 0:
                raise WorkspaceBoundaryError(
                    "WORKSPACE-README-IGNORED", WORKSPACE_README
                )
            if readme.returncode != 1:
                raise WorkspaceBoundaryError("WORKSPACE-GIT-FAILED", WORKSPACE_README)
    except WorkspaceBoundaryError:
        raise
    except OSError as exc:
        raise WorkspaceBoundaryError("WORKSPACE-IGNORE-ISOLATION", ROOT_IGNORE) from exc


def validate_workspace_boundary(
    root: str | os.PathLike[str],
    runner: GitRunner = _run_git,
) -> None:
    """Validate index and ignore metadata without touching workspace children."""

    repository_root = _normalize_root(root)
    index = runner(repository_root, INDEX_ARGUMENTS)
    _require_git_success(index, WORKSPACE_ROOT)
    _validate_index(index.stdout)
    root_ignore = _load_root_ignore_blob(repository_root, runner)
    _validate_ignore_policy(root_ignore, runner)


def _fixture_git(root: Path, arguments: Sequence[str]) -> None:
    """Build only isolated self-test repositories; never used in production."""

    result = subprocess.run(
        [GIT_EXECUTABLE, *arguments],
        cwd=root,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=CLOSED_GIT_ENVIRONMENT,
        timeout=GIT_TIMEOUT_SECONDS,
        shell=False,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError("isolated Git fixture setup failed")


def _isolated_fixture(
    *,
    readme: str = "regular",
    force_extra: bool = False,
    root_policy: bytes = b"_workspace/*\n!_workspace/README.md\n",
    child_policy: bytes | None = None,
) -> tuple[tempfile.TemporaryDirectory[str], Path]:
    temporary = tempfile.TemporaryDirectory(prefix="workspace-boundary-")
    root = Path(temporary.name)
    _fixture_git(root, ("init", "--quiet"))
    (root / ROOT_IGNORE).write_bytes(root_policy)
    workspace = root / WORKSPACE_ROOT
    workspace.mkdir()
    if readme == "regular":
        (workspace / "README.md").write_text("fixture\n", encoding="utf-8")
    elif readme == "symlink":
        (root / "fixture-target").write_text("target\n", encoding="utf-8")
        (workspace / "README.md").symlink_to(root / "fixture-target")
    elif readme != "missing":
        raise AssertionError("unknown isolated fixture")
    add_paths = [".gitignore"]
    if readme != "missing":
        add_paths.append(WORKSPACE_README)
    _fixture_git(root, ("add", "--", *add_paths))
    if child_policy is not None:
        (workspace / ".gitignore").write_bytes(child_policy)
    if force_extra:
        (workspace / "forced.log").write_text("fixture\n", encoding="utf-8")
        _fixture_git(root, ("add", "--force", "--", "_workspace/forced.log"))
    return temporary, root


def _injected_runner(
    *,
    index: bytes,
    probe_status: int = 0,
    readme_status: int = 1,
) -> GitRunner:
    object_id = "a" * 40
    root_policy = b"_workspace/*\n!_workspace/README.md\n"

    def run(_root: str, arguments: tuple[str, ...]):
        if arguments == INDEX_ARGUMENTS:
            return subprocess.CompletedProcess(arguments, 0, index, b"")
        if arguments == ROOT_IGNORE_INDEX_ARGUMENTS:
            root_ignore_index = (
                b"100644 " + object_id.encode("ascii") + b" 0\t.gitignore\0"
            )
            return subprocess.CompletedProcess(arguments, 0, root_ignore_index, b"")
        if arguments == ("cat-file", "-s", object_id):
            size = f"{len(root_policy)}\n".encode("ascii")
            return subprocess.CompletedProcess(arguments, 0, size, b"")
        if arguments == ("cat-file", "blob", object_id):
            return subprocess.CompletedProcess(arguments, 0, root_policy, b"")
        if arguments == ISOLATED_INIT_ARGUMENTS:
            return subprocess.CompletedProcess(arguments, 0, b"", b"")
        if arguments == PROBE_IGNORE_ARGUMENTS:
            return subprocess.CompletedProcess(arguments, probe_status, b"", b"")
        if arguments == README_IGNORE_ARGUMENTS:
            return subprocess.CompletedProcess(arguments, readme_status, b"", b"")
        raise AssertionError("unexpected injected Git query")

    return run


def _expect_error(
    runner: GitRunner,
    expected: tuple[str, str],
) -> None:
    try:
        validate_workspace_boundary("/injected/repository", runner)
    except WorkspaceBoundaryError as exc:
        if (exc.code, exc.path) != expected:
            raise AssertionError("wrong injected diagnostic") from exc
    else:
        raise AssertionError("injected boundary case unexpectedly passed")


def _run_self_test() -> None:
    for fixture_options, expected in (
        ({}, None),
        (
            {"force_extra": True},
            ("WORKSPACE-TRACKED-EXTRA", "_workspace/forced.log"),
        ),
        (
            {"readme": "symlink"},
            ("WORKSPACE-TRACKED-NONREGULAR", WORKSPACE_README),
        ),
        (
            {"readme": "missing"},
            ("WORKSPACE-README-MISSING", WORKSPACE_README),
        ),
        (
            {
                "root_policy": (
                    b"_workspace/.gitignore\n"
                    b"!_workspace/probe.log\n"
                    b"!_workspace/README.md\n"
                ),
                "child_policy": b"probe.log\n",
            },
            ("WORKSPACE-SCRATCH-NOT-IGNORED", WORKSPACE_PROBE),
        ),
        (
            {
                "child_policy": b"!probe.log\nREADME.md\n",
            },
            None,
        ),
    ):
        temporary, root = _isolated_fixture(**fixture_options)
        try:
            if expected is None:
                validate_workspace_boundary(root)
            else:
                try:
                    validate_workspace_boundary(root)
                except WorkspaceBoundaryError as exc:
                    if (exc.code, exc.path) != expected:
                        raise AssertionError("wrong isolated diagnostic") from exc
                else:
                    raise AssertionError("isolated negative unexpectedly passed")
        finally:
            temporary.cleanup()

    object_id = b"a" * 40
    readme = b"100644 " + object_id + b" 0\t_workspace/README.md\0"
    _expect_error(
        _injected_runner(index=b"100644 " + object_id + b" 2\t_workspace/README.md\0"),
        ("WORKSPACE-INDEX-CONFLICT", WORKSPACE_README),
    )
    _expect_error(
        _injected_runner(index=readme.rstrip(b"\0")),
        ("WORKSPACE-INDEX-MALFORMED", WORKSPACE_ROOT),
    )
    _expect_error(
        _injected_runner(index=readme, probe_status=1),
        ("WORKSPACE-SCRATCH-NOT-IGNORED", WORKSPACE_PROBE),
    )
    _expect_error(
        _injected_runner(index=readme, readme_status=0),
        ("WORKSPACE-README-IGNORED", WORKSPACE_README),
    )

    actual_workspace = os.path.abspath("/injected/repository/_workspace")
    actual_root_ignore = os.path.abspath("/injected/repository/.gitignore")

    def is_actual_workspace(value: object) -> bool:
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

    def guard(function: Callable):
        def wrapped(value, *args, **kwargs):
            if is_actual_workspace(value):
                raise AssertionError("actual workspace traversal/open sentinel invoked")
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
        validate_workspace_boundary(
            "/injected/repository", _injected_runner(index=readme)
        )


def _parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the Git-metadata-only _workspace boundary."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--root", default=None)
    mode.add_argument("--self-test", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if arguments.self_test:
            _run_self_test()
            print("[PASS] workspace boundary self-test")
        else:
            validate_workspace_boundary(arguments.root or ".")
            print("[PASS] workspace boundary: _workspace/README.md")
    except WorkspaceBoundaryError as exc:
        print(f"ERR {exc}", file=sys.stderr)
        return 1
    except (AssertionError, OSError, subprocess.SubprocessError):
        print("ERR WORKSPACE-SELF-TEST .", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
