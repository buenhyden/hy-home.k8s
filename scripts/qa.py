#!/usr/bin/env python3
"""Run selected repository QA over an isolated working-tree or exact-index snapshot."""

from __future__ import annotations

import argparse
from contextlib import contextmanager, nullcontext
import hashlib
import importlib.util
import importlib.metadata
import json
import re
import os
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence
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
PROFILES = ("quick", "staged")
SNAPSHOT_FILE_LIMIT_BYTES = 8 * 1024 * 1024
GIT_INDEX_LIMIT_BYTES = 16 * 1024 * 1024


def git(root: Path, *args: str, optional: bool = False) -> bytes | None:
    environment = runner.closed_subprocess_environment()
    environment.update(
        GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL="/dev/null", GIT_OPTIONAL_LOCKS="0"
    )
    index_context = (
        _disposable_git_index(root) if args and args[0] == "diff" else nullcontext(None)
    )
    with index_context as disposable_index:
        if disposable_index is not None:
            environment["GIT_INDEX_FILE"] = str(disposable_index)
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


@contextmanager
def _disposable_git_index(root: Path):
    """Let read-only diffs refresh a copy, never the source or private index."""
    canonical = index_file(root)
    before = read_bounded_bytes(canonical, max_bytes=GIT_INDEX_LIMIT_BYTES)
    temporary = tempfile.NamedTemporaryFile(
        mode="w+b", prefix="qa-read-index-", dir=canonical.parent, delete=False
    )
    disposable = Path(temporary.name)
    try:
        with temporary:
            temporary.write(before)
            temporary.flush()
        yield disposable
        if read_bounded_bytes(canonical, max_bytes=GIT_INDEX_LIMIT_BYTES) != before:
            raise ValueError("Git source index changed during read")
    finally:
        disposable.unlink(missing_ok=True)


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


def head_snapshot_leaf(root: Path, path: str) -> bool:
    entry = git(root, "--literal-pathspecs", "ls-tree", "-z", "HEAD", "--", path)
    metadata, _, name = entry.rstrip(b"\0").partition(b"\t")
    fields = metadata.split()
    return (
        name == os.fsencode(path)
        and len(fields) == 3
        and fields[0] in (b"100644", b"100755", b"120000")
        and fields[1] == b"blob"
    )


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


def merge_head_bytes(root: Path) -> bytes | None:
    path = Path(
        os.fsdecode(
            git(root, "rev-parse", "--path-format=absolute", "--git-path", "MERGE_HEAD")
        ).strip()
    )
    return read_bounded_bytes(path, max_bytes=128) if os.path.lexists(path) else None


@contextmanager
def repository_snapshot(root: Path, *, staged: bool = False):
    """Copy only Git-selected bytes; never write the source worktree or index."""
    root = root.resolve()
    head = git(root, "rev-parse", "HEAD")
    source_index = index_file(root)
    index_bytes = read_bounded_bytes(source_index, max_bytes=GIT_INDEX_LIMIT_BYTES)
    merge_head = merge_head_bytes(root)
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
        # The clone maps the source's branches to remote-tracking refs and
        # drops the source's own remote-tracking refs. A checkout whose default
        # branch exists only as `origin/<name>`, as in CI, would lose it, and
        # archive envelopes resolve against that branch (ADR-0040).
        # The shared clone already holds the objects, so the refs are written
        # directly; a fetch would spawn a transport process the bounded runner
        # rejects as an escaped descendant.
        remote_refs = git(
            root, "for-each-ref", "--format=%(objectname) %(refname)", "refs/remotes/"
        )
        for line in remote_refs.decode("ascii").splitlines():
            object_name, reference = line.split(" ", 1)
            git(snapshot, "update-ref", "--no-deref", reference, object_name)
        if merge_head is not None:
            merge_path = Path(
                os.fsdecode(
                    git(
                        snapshot,
                        "rev-parse",
                        "--path-format=absolute",
                        "--git-path",
                        "MERGE_HEAD",
                    )
                ).strip()
            )
            write_snapshot_file(merge_path, merge_head)
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
            or merge_head_bytes(root) != merge_head
        ):
            raise ValueError("source index or HEAD changed during snapshot")
        if before is not None and tree_identity(root) != before:
            raise ValueError("source files changed during snapshot")
        yield snapshot


def require_unchanged_private_snapshot(
    root: Path,
    *,
    head_before: bytes,
    raw_index_before: bytes,
    tree_before: dict[str, tuple[int, bytes] | None],
) -> None:
    """Catch HEAD, index, and file changes without refreshing the private index."""
    changed: list[str] = []
    if git(root, "rev-parse", "HEAD") != head_before:
        changed.append("HEAD")
    if (
        read_bounded_bytes(index_file(root), max_bytes=GIT_INDEX_LIMIT_BYTES)
        != raw_index_before
    ):
        changed.append("raw-index")
    if tree_identity(root) != tree_before:
        changed.append("file-bytes")
    if changed:
        raise ValueError("QA private snapshot changed: " + ",".join(changed))


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
            if head_snapshot_leaf(root, path):
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
        if directory and (
            indexed_snapshot_leaf(root, path) or head_snapshot_leaf(root, path)
        ):
            children = {
                candidate for candidate in inventory if candidate.startswith(path + "/")
            }
            if children and children <= selected:
                # The old leaf is absent from the temporary index. Its independently
                # selected children retain routing and node-safety validation.
                continue
        result.append(path)
    return result


def gate_input_identity(
    snapshot: Path,
    gate: Mapping[str, Any],
    *,
    lane: str,
    paths: Sequence[str],
    base_ref: str,
    environment: Mapping[str, str],
) -> str:
    """Hash a versioned, bounded canonical description of an audited gate input."""
    if lane not in ("affected", "staged"):
        raise ValueError("unsupported reuse lane")
    mode = gate.get("reuse", {}).get("mode")
    if mode not in ("same-lane", "change-scoped"):
        raise ValueError("gate has no reuse contract")
    canonical_lane = (
        "change-scoped"
        if mode == "change-scoped" and lane in ("affected", "staged")
        else lane
    )
    tree = tree_identity(snapshot)
    if len(tree) > 100_000:
        raise ValueError("reuse input has too many files")
    files = [
        [
            path,
            None
            if value is None
            else [
                stat.S_IFMT(value[0]),
                stat.S_IMODE(value[0]),
                hashlib.sha256(value[1]).hexdigest(),
            ],
        ]
        for path, value in sorted(tree.items())
    ]
    # These declarations are deliberately conservative: any repository edit,
    # ref movement, or installed Python distribution change causes a miss.
    versions = sorted(
        (distribution.metadata.get("Name", ""), distribution.version)
        for distribution in importlib.metadata.distributions()
    )
    executable = Path(sys.executable).resolve(strict=True)
    executable_stat = executable.stat()
    fields = {
        "version": 1,
        "gate": gate["id"],
        "lane": canonical_lane,
        "paths": sorted(set(paths)),
        "base": base_ref,
        "argv": gate["argv"],
        "reuse": gate["reuse"],
        "environment": sorted(environment.items()),
        "python": [
            str(executable),
            sys.version,
            executable_stat.st_size,
            executable_stat.st_mtime_ns,
            versions,
        ],
        "gitVersion": git(snapshot, "--version").decode("ascii").strip(),
        "head": git(snapshot, "rev-parse", "HEAD").decode("ascii").strip(),
        "refs": git(
            snapshot, "for-each-ref", "--format=%(refname) %(objectname)"
        ).decode("ascii"),
        "files": files,
    }
    if any(
        len(str(value).encode("utf-8", "surrogateescape")) > 1024 * 1024
        for value in (
            gate["id"],
            base_ref,
            *paths,
            *gate["argv"],
            *(item for pair in environment.items() for item in pair),
        )
    ):
        raise ValueError("reuse identity field exceeds byte budget")
    payload = json.dumps(
        fields, sort_keys=True, ensure_ascii=True, separators=(",", ":")
    ).encode()
    if len(payload) > 16 * 1024 * 1024:
        raise ValueError("reuse identity exceeds byte budget")
    return hashlib.sha256(payload).hexdigest()


class LocalEvidenceStore:
    """One private atomic pass index under this repository's Git common dir."""

    def __init__(self, root: Path):
        common = git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
        self.path = Path(os.fsdecode(common).strip()) / "qa-local-evidence.json"

    def _passes(self) -> dict[str, str]:
        try:
            with open_parent(self.path) as (parent, name):
                metadata, payload = read_regular_file(
                    parent, name, max_bytes=128 * 1024
                )
            if (
                stat.S_IMODE(metadata.st_mode) != 0o600
                or metadata.st_uid != os.geteuid()
            ):
                return {}
            data = json.loads(payload)
            if not isinstance(data, dict):
                return {}
            passes = data.get("passes")
            if (
                set(data) != {"version", "passes"}
                or data["version"] != 1
                or not isinstance(passes, dict)
                or len(passes) > 256
            ):
                return {}
            if any(
                not isinstance(key, str)
                or re.fullmatch(r"[a-z][a-z0-9-]{0,127}", key) is None
                or not isinstance(value, str)
                or re.fullmatch(r"[0-9a-f]{64}", value) is None
                for key, value in passes.items()
            ):
                return {}
            return passes
        except (OSError, ValueError, TypeError, KeyError):
            return {}

    def matching_pass(self, gate_id: str, identity: str) -> bool:
        return self._passes().get(gate_id) == identity

    def record_pass(self, gate_id: str, identity: str) -> None:
        if (
            re.fullmatch(r"[a-z][a-z0-9-]{0,127}", gate_id) is None
            or re.fullmatch(r"[0-9a-f]{64}", identity) is None
        ):
            raise ValueError("invalid local evidence identity")
        passes = self._passes()
        passes[gate_id] = identity
        payload = json.dumps(
            {"version": 1, "passes": passes}, sort_keys=True, separators=(",", ":")
        ).encode()
        if len(payload) > 128 * 1024:
            raise ValueError("local evidence exceeds byte budget")
        descriptor, temporary = tempfile.mkstemp(
            prefix=".qa-evidence-", dir=self.path.parent
        )
        try:
            with os.fdopen(descriptor, "wb") as output:
                os.fchmod(output.fileno(), 0o600)
                output.write(payload)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, self.path)
            directory = os.open(self.path.parent, os.O_RDONLY | os.O_DIRECTORY)
            try:
                os.fsync(directory)
            finally:
                os.close(directory)
        finally:
            if os.path.lexists(temporary):
                os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("profile", nargs="?", choices=PROFILES)
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
            for profile in PROFILES:
                identifiers = contract_module.profile_gate_ids(contract, profile)
                print(profile + ": " + ", ".join(identifiers))
            return 0
        baseline = base_revision(root, args.profile, args.base_ref)
        paths = changed_paths(root, staged=args.profile == "staged")
        source_head_before = git(root, "rev-parse", "HEAD")
        source_index_path = index_file(root)
        source_index_before = read_bounded_bytes(
            source_index_path, max_bytes=GIT_INDEX_LIMIT_BYTES
        )
        source_tree_before = tree_identity(root)
        with repository_snapshot(root, staged=args.profile == "staged") as snapshot:
            contract = contract_module.validate_contract(snapshot)
            lane = "staged" if args.profile == "staged" else "affected"
            selected = contract_module.select_paths(contract, paths, lane, snapshot)
            ids = contract_module.profile_gate_ids(contract, args.profile)
            ids = [
                identifier for identifier in ids if identifier in selected["validators"]
            ]
            print(
                f"[INFO] qa profile={args.profile} snapshot={'index' if args.profile == 'staged' else 'working-tree'} gates={len(ids)}"
            )
            private_head_before = git(snapshot, "rev-parse", "HEAD")
            private_index_before = read_bounded_bytes(
                index_file(snapshot), max_bytes=GIT_INDEX_LIMIT_BYTES
            )
            private_tree_before = tree_identity(snapshot)
            store = LocalEvidenceStore(root)
            validators = {row["id"]: row for row in contract["validators"]}
            identities = {}
            candidates = {}
            for identifier in ids:
                gate = validators[identifier]
                if not gate.get("reuse"):
                    continue
                effective = dict(gate)
                effective["argv"] = runner.validator_argv(
                    snapshot, lane, paths, gate, contract, contract_module, baseline
                )
                resolved_tool = runner.resolve_tool(effective["argv"][0], snapshot)
                if resolved_tool is None:
                    continue
                effective["argv"][0] = os.path.abspath(resolved_tool)
                identity = gate_input_identity(
                    snapshot,
                    effective,
                    lane=lane,
                    paths=paths,
                    base_ref=baseline,
                    environment=runner.validation_environment(snapshot),
                )
                identities[identifier] = identity
                if store.matching_pass(identifier, identity):
                    candidates[identifier] = {"identity": identity, "source": "local"}
            completed_passes = {}
            result = runner.run_selected(
                snapshot,
                lane,
                paths,
                contract,
                contract_module,
                validator_ids=ids,
                base_ref=baseline,
                reuse_candidates=candidates,
                completed_passes=completed_passes,
            )
            require_unchanged_private_snapshot(
                snapshot,
                head_before=private_head_before,
                raw_index_before=private_index_before,
                tree_before=private_tree_before,
            )
            if (
                git(root, "rev-parse", "HEAD") != source_head_before
                or read_bounded_bytes(
                    source_index_path, max_bytes=GIT_INDEX_LIMIT_BYTES
                )
                != source_index_before
                or tree_identity(root) != source_tree_before
            ):
                raise ValueError(
                    "source HEAD, index, or selected files changed during QA"
                )
            for identifier in completed_passes:
                if identifier in identities:
                    store.record_pass(identifier, identities[identifier])
            return result
    except (OSError, ValueError) as exc:
        print("[FAIL] qa: " + runner.encoded(str(exc)[:1024]), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
