#!/usr/bin/env python3
"""Run shared repository QA over an isolated final-tree or exact-index snapshot."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import tempfile

_spec = importlib.util.spec_from_file_location(
    "qa_validation_runner", Path(__file__).with_name("run-validation-lane.py")
)
runner = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = runner
_spec.loader.exec_module(runner)
contract_module = runner.load_contract_module()
from validation.repository.bounded_io import (  # noqa: E402
    open_parent,
    read_bytes as read_bounded_bytes,
    read_regular_file,
    stable_file_state,
)

# Match the existing governance candidate reader's per-file bound. Git indexes
# contain the whole path table and receive a separate finite metadata allowance.
SNAPSHOT_FILE_LIMIT_BYTES = 8 * 1024 * 1024
GIT_INDEX_LIMIT_BYTES = 16 * 1024 * 1024


def git(root: Path, *args: str, optional: bool = False) -> bytes | None:
    environment = runner.closed_subprocess_environment()
    environment.update(
        GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null", GIT_OPTIONAL_LOCKS="0"
    )
    result = runner.run_bounded_command(
        [
            "/usr/bin/git",
            "-c",
            "core.hooksPath=/dev/null",
            "-c",
            "core.fsmonitor=false",
            *args,
        ],
        cwd=root,
        env=environment,
    )
    if result.status != "completed" or not result.cleanup_complete:
        raise ValueError("Git snapshot command failed: " + runner.observation(result))
    if result.returncode:
        if optional:
            return None
        raise ValueError("Git snapshot command failed: " + runner.observation(result))
    return result.stdout.retained


def paths_from(payload: bytes) -> list[str]:
    paths = [os.fsdecode(item) for item in payload.split(b"\0") if item]
    for path in paths:
        parts = PurePosixPath(path).parts
        if (
            not parts
            or path.startswith("/")
            or any(p in (".", "..", ".git") for p in parts)
            or str(PurePosixPath(path)) != path
        ):
            raise ValueError("unsafe snapshot path")
    return sorted(set(paths))


def source_paths(root: Path) -> list[str]:
    return paths_from(
        git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    )


def indexed_snapshot_leaf(root: Path, path: str) -> bool:
    entries = git(root, "ls-files", "--stage", "-z", "--", path)
    for entry in entries.split(b"\0"):
        fields, _, name = entry.partition(b"\t")
        metadata = fields.split()
        if (
            name == os.fsencode(path)
            and len(metadata) == 3
            and metadata[0] in (b"100644", b"100755", b"120000")
            and metadata[2] == b"0"
        ):
            return True
    return False


def file_identity(root: Path, path: str):
    paths_from(os.fsencode(path) + b"\0")
    target = root / path
    observed = False
    try:
        with open_parent(target) as (parent, name):
            metadata = os.stat(name, dir_fd=parent, follow_symlinks=False)
            observed = True
            if stat.S_ISLNK(metadata.st_mode):
                link = os.readlink(name, dir_fd=parent)
                if os.path.isabs(link) or not target.resolve().is_relative_to(root):
                    raise ValueError("snapshot symlink escapes repository")
                if stable_file_state(metadata) != stable_file_state(
                    os.stat(name, dir_fd=parent, follow_symlinks=False)
                ):
                    raise ValueError("snapshot symlink changed during inspection")
                payload = os.fsencode(link)
            elif stat.S_ISREG(metadata.st_mode):
                metadata, contents = read_regular_file(
                    parent, name, max_bytes=SNAPSHOT_FILE_LIMIT_BYTES
                )
                payload = hashlib.sha256(contents).digest()
            else:
                if stat.S_ISDIR(metadata.st_mode):
                    # Retire only an exact old index leaf; copy selected children
                    # separately. Gitlinks and untracked directories stay invalid.
                    if indexed_snapshot_leaf(root, path):
                        return None
                raise ValueError("snapshot supports regular files and symlinks only")
            return metadata.st_mode, payload
    except FileNotFoundError as exc:
        if observed:
            raise ValueError("snapshot input changed during inspection") from exc
        return None


def write_snapshot_file(path: Path, payload: bytes, mode: int = 0o600) -> None:
    """Create a private snapshot leaf without following a replaced parent or file."""
    with open_parent(path, create=True) as (parent, name):
        descriptor = os.open(
            name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
            mode,
            dir_fd=parent,
        )
        with os.fdopen(descriptor, "wb") as target:
            target.write(payload)
            target.flush()
            os.fchmod(target.fileno(), mode)
            if stable_file_state(os.fstat(target.fileno())) != stable_file_state(
                os.stat(name, dir_fd=parent, follow_symlinks=False)
            ):
                raise ValueError("snapshot output changed during copy")


def tree_identity(root: Path):
    return {path: file_identity(root, path) for path in source_paths(root)}


def index_file(root: Path) -> Path:
    return Path(
        os.fsdecode(
            git(root, "rev-parse", "--path-format=absolute", "--git-path", "index")
        ).strip()
    )


@contextmanager
def repository_snapshot(root: Path, *, staged: bool = False):
    """Copy only Git-selected bytes; never write the source worktree or index."""
    root = root.resolve()
    head = git(root, "rev-parse", "HEAD")
    source_index = index_file(root)
    index_bytes = read_bounded_bytes(source_index, max_bytes=GIT_INDEX_LIMIT_BYTES)
    before = None if staged else tree_identity(root)
    with tempfile.TemporaryDirectory(prefix="hy-qa-") as directory:
        snapshot = Path(directory) / "repository"
        git(
            root,
            "clone",
            "--quiet",
            "--shared",
            "--no-checkout",
            "--",
            str(root),
            str(snapshot),
        )
        if git(snapshot, "rev-parse", "HEAD") != head:
            raise ValueError("source HEAD changed during snapshot")
        if staged:
            write_snapshot_file(index_file(snapshot), index_bytes)
            shared = git(root, "rev-parse", "--shared-index-path").strip()
            if shared:
                shared_path = Path(os.fsdecode(shared))
                if not shared_path.is_absolute():
                    shared_path = root / shared_path
                write_snapshot_file(
                    index_file(snapshot).parent / shared_path.name,
                    read_bounded_bytes(shared_path, max_bytes=GIT_INDEX_LIMIT_BYTES),
                )
            git(snapshot, "checkout-index", "--all", "--force")
            tree_identity(snapshot)  # Reject escaping index symlinks as well.
        else:
            git(snapshot, "read-tree", "HEAD")
            for path, identity in before.items():
                if identity is None:
                    continue
                source = root / path
                target = snapshot / path
                if stat.S_ISLNK(identity[0]):
                    with open_parent(target, create=True) as (parent, name):
                        os.symlink(os.fsdecode(identity[1]), name, dir_fd=parent)
                else:
                    with open_parent(source) as (parent, name):
                        metadata, contents = read_regular_file(
                            parent, name, max_bytes=SNAPSHOT_FILE_LIMIT_BYTES
                        )
                    if (
                        metadata.st_mode,
                        hashlib.sha256(contents).digest(),
                    ) != identity:
                        raise ValueError("source files changed during snapshot")
                    write_snapshot_file(target, contents, stat.S_IMODE(identity[0]))
                if file_identity(snapshot, path) != identity:
                    raise ValueError("source files changed during snapshot")
            git(snapshot, "add", "--all", "--", ".")
        if (
            read_bounded_bytes(source_index, max_bytes=GIT_INDEX_LIMIT_BYTES)
            != index_bytes
            or git(root, "rev-parse", "HEAD") != head
        ):
            raise ValueError("source index or HEAD changed during snapshot")
        if before is not None and tree_identity(root) != before:
            raise ValueError("source files changed during snapshot")
        yield snapshot


def require_unchanged_snapshot(root: Path) -> None:
    if git(root, "diff", "--name-only", "-z") or git(
        root, "ls-files", "--others", "--exclude-standard", "-z"
    ):
        raise ValueError(
            "QA modified snapshot files; review formatter changes before rerunning"
        )


def base_revision(root: Path, profile: str, value: str | None) -> str:
    if value and set(value) == {"0"}:
        return "EMPTY"
    if value:
        if value.startswith("-") or any(
            character
            not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._/-"
            for character in value
        ):
            raise ValueError("unsafe base reference")
        return git(root, "rev-parse", "--verify", value + "^{commit}").decode().strip()
    if profile == "ci":
        parent = git(root, "rev-parse", "--verify", "HEAD^", optional=True)
        return parent.decode().strip() if parent else "EMPTY"
    baseline = git(root, "merge-base", "HEAD", "origin/main", optional=True)
    return (
        baseline.decode().strip()
        if baseline
        else git(root, "rev-parse", "HEAD").decode().strip()
    )


def changed_paths(root: Path, *, staged: bool) -> list[str]:
    args = ["diff", "--name-only", "--no-renames", "-z"]
    args += ["--cached"] if staged else ["HEAD"]
    payload = git(root, *args)
    if not staged:
        payload += git(root, "ls-files", "--others", "--exclude-standard", "-z")
    paths = paths_from(payload)
    if staged:
        inventory = set(paths_from(git(root, "ls-files", "--cached", "-z")))
        selected = set(paths)
        replaced = set()
        for path in paths:
            children = {
                candidate for candidate in inventory if candidate.startswith(path + "/")
            }
            if not children or not children <= selected:
                continue
            entry = git(
                root, "--literal-pathspecs", "ls-tree", "-z", "HEAD", "--", path
            )
            metadata, _, name = entry.rstrip(b"\0").partition(b"\t")
            fields = metadata.split()
            if (
                name == os.fsencode(path)
                and len(fields) == 3
                and fields[0] in (b"100644", b"100755", b"120000")
                and fields[1] == b"blob"
            ):
                # Use only HEAD/index metadata, never the unstaged filesystem.
                replaced.add(path)
        return [path for path in paths if path not in replaced]
    inventory = set(source_paths(root))
    selected = set(paths)
    result = []
    for path in paths:
        try:
            with open_parent(root / path) as (parent, name):
                directory = stat.S_ISDIR(
                    os.stat(name, dir_fd=parent, follow_symlinks=False).st_mode
                )
        except FileNotFoundError:
            directory = False
        if directory and indexed_snapshot_leaf(root, path):
            children = {
                candidate for candidate in inventory if candidate.startswith(path + "/")
            }
            if children and children <= selected:
                # The old leaf is absent from the temporary index. Its independently
                # selected children retain routing and node-safety validation.
                continue
        result.append(path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", choices=("quick", "staged", "full", "ci"))
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--base-ref")
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args()
    if not args.profile and not args.list:
        parser.error("a profile or --list is required")
    root = args.root.resolve()
    try:
        if args.list:
            contract = contract_module.validate_contract(root)
            for profile, identifiers in contract["profiles"].items():
                print(profile + ": " + ", ".join(identifiers))
            return 0
        baseline = base_revision(root, args.profile, args.base_ref)
        paths = (
            changed_paths(root, staged=args.profile == "staged")
            if args.profile in ("quick", "staged")
            else None
        )
        with repository_snapshot(root, staged=args.profile == "staged") as snapshot:
            contract = contract_module.validate_contract(snapshot)
            lane = {
                "quick": "affected",
                "staged": "staged",
                "full": "all-files",
                "ci": "all-files",
            }[args.profile]
            if paths is None:
                paths = source_paths(snapshot)
            selected = contract_module.select_paths(contract, paths, lane, snapshot)
            ids = contract["profiles"][args.profile]
            if args.profile in ("quick", "staged"):
                ids = [
                    identifier
                    for identifier in ids
                    if identifier in selected["validators"]
                ]
            print(
                f"[INFO] qa profile={args.profile} snapshot={'index' if args.profile == 'staged' else 'working-tree'} gates={len(ids)}"
            )
            result = runner.run_selected(
                snapshot,
                lane,
                paths,
                contract,
                contract_module,
                validator_ids=ids,
                base_ref=baseline,
            )
            require_unchanged_snapshot(snapshot)
            return result
    except (OSError, ValueError) as exc:
        print("[FAIL] qa: " + runner.encoded(str(exc)[:1024]), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
