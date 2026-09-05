#!/usr/bin/env python3
"""Run shared repository QA over an isolated final-tree or exact-index snapshot."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib.util
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import sys
import tempfile

_spec = importlib.util.spec_from_file_location("qa_validation_runner", Path(__file__).with_name("run-validation-lane.py"))
runner = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = runner
_spec.loader.exec_module(runner)
contract_module = runner.load_contract_module()


def git(root: Path, *args: str, optional: bool = False) -> bytes | None:
    environment = runner.closed_subprocess_environment()
    environment.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null", GIT_OPTIONAL_LOCKS="0")
    result = runner.run_bounded_command(
        ["/usr/bin/git", "-c", "core.hooksPath=/dev/null", "-c", "core.fsmonitor=false", *args],
        cwd=root, env=environment,
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
        if not parts or path.startswith("/") or any(p in (".", "..", ".git") for p in parts) or str(PurePosixPath(path)) != path:
            raise ValueError("unsafe snapshot path")
    return sorted(set(paths))


def source_paths(root: Path) -> list[str]:
    return paths_from(git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z"))


def file_identity(root: Path, path: str):
    target = root / path
    for parent in target.parents:
        if parent == root:
            break
        if parent.is_symlink():
            raise ValueError("snapshot path traverses a symlink")
    try:
        metadata = target.lstat()
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(metadata.st_mode):
        link = os.readlink(target)
        if os.path.isabs(link) or not target.resolve().is_relative_to(root):
            raise ValueError("snapshot symlink escapes repository")
        payload = os.fsencode(link)
    elif stat.S_ISREG(metadata.st_mode):
        digest = hashlib.sha256()
        with target.open("rb") as source:
            for chunk in iter(lambda: source.read(1024 * 1024), b""):
                digest.update(chunk)
        payload = digest.digest()
    else:
        raise ValueError("snapshot supports regular files and symlinks only")
    return metadata.st_mode, payload


def tree_identity(root: Path):
    return {path: file_identity(root, path) for path in source_paths(root)}


def index_file(root: Path) -> Path:
    return Path(os.fsdecode(git(root, "rev-parse", "--path-format=absolute", "--git-path", "index")).strip())


@contextmanager
def repository_snapshot(root: Path, *, staged: bool = False):
    """Copy only Git-selected bytes; never write the source worktree or index."""
    root = root.resolve()
    head = git(root, "rev-parse", "HEAD")
    source_index = index_file(root)
    index_bytes = source_index.read_bytes()
    before = None if staged else tree_identity(root)
    with tempfile.TemporaryDirectory(prefix="hy-qa-") as directory:
        snapshot = Path(directory) / "repository"
        git(root, "clone", "--quiet", "--shared", "--no-checkout", "--", str(root), str(snapshot))
        if git(snapshot, "rev-parse", "HEAD") != head:
            raise ValueError("source HEAD changed during snapshot")
        if staged:
            index_file(snapshot).write_bytes(index_bytes)
            shared = git(root, "rev-parse", "--shared-index-path").strip()
            if shared:
                shared_path = Path(os.fsdecode(shared))
                if not shared_path.is_absolute():
                    shared_path = root / shared_path
                shutil.copyfile(shared_path, index_file(snapshot).parent / shared_path.name)
            git(snapshot, "checkout-index", "--all", "--force")
            tree_identity(snapshot)  # Reject escaping index symlinks as well.
        else:
            git(snapshot, "read-tree", "HEAD")
            for path, identity in before.items():
                if identity is None:
                    continue
                source = root / path
                target = snapshot / path
                target.parent.mkdir(parents=True, exist_ok=True)
                if stat.S_ISLNK(identity[0]):
                    target.symlink_to(os.fsdecode(identity[1]))
                else:
                    shutil.copyfile(source, target, follow_symlinks=False)
                    target.chmod(stat.S_IMODE(identity[0]))
                if file_identity(snapshot, path) != identity:
                    raise ValueError("source files changed during snapshot")
            git(snapshot, "add", "--all", "--", ".")
        if source_index.read_bytes() != index_bytes or git(root, "rev-parse", "HEAD") != head:
            raise ValueError("source index or HEAD changed during snapshot")
        if before is not None and tree_identity(root) != before:
            raise ValueError("source files changed during snapshot")
        yield snapshot


def require_unchanged_snapshot(root: Path) -> None:
    if git(root, "diff", "--name-only", "-z") or git(root, "ls-files", "--others", "--exclude-standard", "-z"):
        raise ValueError("QA modified snapshot files; review formatter changes before rerunning")


def base_revision(root: Path, profile: str, value: str | None) -> str:
    if value and set(value) == {"0"}:
        return "EMPTY"
    if value:
        if value.startswith("-") or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._/-" for character in value):
            raise ValueError("unsafe base reference")
        return git(root, "rev-parse", "--verify", value + "^{commit}").decode().strip()
    if profile == "ci":
        parent = git(root, "rev-parse", "--verify", "HEAD^", optional=True)
        return parent.decode().strip() if parent else "EMPTY"
    baseline = git(root, "merge-base", "HEAD", "origin/main", optional=True)
    return baseline.decode().strip() if baseline else git(root, "rev-parse", "HEAD").decode().strip()


def changed_paths(root: Path, *, staged: bool) -> list[str]:
    args = ["diff", "--name-only", "--no-renames", "-z"]
    args += ["--cached"] if staged else ["HEAD"]
    payload = git(root, *args)
    if not staged:
        payload += git(root, "ls-files", "--others", "--exclude-standard", "-z")
    return paths_from(payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", choices=("quick", "staged", "full", "ci"))
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--base-ref")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
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
        paths = changed_paths(root, staged=args.profile == "staged") if args.profile in ("quick", "staged") else None
        with repository_snapshot(root, staged=args.profile == "staged") as snapshot:
            contract = contract_module.validate_contract(snapshot)
            lane = {"quick": "affected", "staged": "staged", "full": "all-files", "ci": "all-files"}[args.profile]
            if paths is None:
                paths = source_paths(snapshot)
            selected = contract_module.select_paths(contract, paths, lane, snapshot)
            ids = contract["profiles"][args.profile]
            if args.profile in ("quick", "staged"):
                ids = [identifier for identifier in ids if identifier in selected["validators"]]
            print(f"[INFO] qa profile={args.profile} snapshot={'index' if args.profile == 'staged' else 'working-tree'} gates={len(ids)}")
            result = runner.run_selected(snapshot, lane, paths, contract, contract_module, validator_ids=ids, base_ref=baseline)
            require_unchanged_snapshot(snapshot)
            return result
    except (OSError, ValueError) as exc:
        print("[FAIL] qa: " + runner.encoded(str(exc)[:1024]), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
