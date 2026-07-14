#!/usr/bin/env python3
"""Report GitOps object identity changes without emitting manifest content."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

import yaml


WORKTREE_REVISION = "WORKTREE"
EMPTY_REVISION = "EMPTY"
ZERO_REVISION = "0" * 40
COMMIT_RE = re.compile(r"[0-9a-f]{40}\Z")
SAFE_REF_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/-]*\Z")
DNS_LABEL = r"[a-z0-9](?:[-a-z0-9]*[a-z0-9])?"
API_VERSION_RE = re.compile(rf"(?:{DNS_LABEL}(?:\.{DNS_LABEL})*/)?[a-z][a-z0-9]*\Z")
KIND_RE = re.compile(r"[A-Za-z][A-Za-z0-9]*\Z")
IDENTITY_TOKEN_RE = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9._@+-]*[A-Za-z0-9])?\Z")
PATH_TOKEN_RE = re.compile(r"[A-Za-z0-9._@+/-]+\Z")
KUSTOMIZATION_NAME = "kustomization.yaml"
KUSTOMIZATION_API_VERSION = "kustomize.config.k8s.io/v1beta1"
KUSTOMIZATION_KIND = "Kustomization"
ALLOWED_KUSTOMIZATION_KEYS = frozenset(("apiVersion", "kind", "resources"))


def _is_safe_repository_path(value: str) -> bool:
    if not value or not PATH_TOKEN_RE.fullmatch(value):
        return False
    candidate = PurePosixPath(value)
    return (
        not candidate.is_absolute()
        and candidate.as_posix() == value
        and bool(candidate.parts)
        and all(part not in ("", ".", "..") for part in candidate.parts)
    )


def _diagnostic_path(value: str) -> str:
    return value if value == "." or _is_safe_repository_path(value) else "."


class GitOpsValidationError(Exception):
    """A fail-closed error whose diagnostic contains only a code and path."""

    def __init__(self, code: str, path: str) -> None:
        safe_path = _diagnostic_path(path)
        super().__init__(code, safe_path)
        self.code = code
        self.path = safe_path


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.nodes.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(None, None, "invalid key", key_node.start_mark) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(None, None, "duplicate key", key_node.start_mark)
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


@dataclass(frozen=True, order=True)
class ObjectIdentity:
    api_version: str
    kind: str
    namespace: str
    name: str


@dataclass(frozen=True)
class RenderedObject:
    identity: ObjectIdentity
    path: str


@dataclass(frozen=True)
class ChangeSet:
    added: tuple[RenderedObject, ...]
    deleted: tuple[RenderedObject, ...]
    retained: tuple[RenderedObject, ...]


def _run_git(repo: Path, arguments: list[str]) -> subprocess.CompletedProcess[bytes]:
    try:
        return subprocess.run(
            ["git", "-C", str(repo), *arguments],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except OSError as exc:
        raise GitOpsValidationError("GIT_UNAVAILABLE", ".") from exc


def _git_root(root: Path) -> Path:
    result = _run_git(root, ["rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        raise GitOpsValidationError("GIT_ROOT", ".")
    try:
        repo = Path(os.fsdecode(result.stdout.rstrip(b"\n"))).resolve()
        root.resolve().relative_to(repo)
    except (UnicodeDecodeError, ValueError) as exc:
        raise GitOpsValidationError("GIT_ROOT", ".") from exc
    return repo


def _resolve_commit(repo: Path, revision: str) -> str:
    if (
        not isinstance(revision, str)
        or not SAFE_REF_RE.fullmatch(revision)
        or ".." in revision
        or "//" in revision
        or revision.endswith(("/", "."))
    ):
        raise GitOpsValidationError("BASE_REF", ".")
    result = _run_git(
        repo,
        ["rev-parse", "--verify", "--quiet", "--end-of-options", f"{revision}^{{commit}}"],
    )
    if result.returncode != 0:
        raise GitOpsValidationError("BASE_REF", ".")
    try:
        candidate = result.stdout.decode("ascii").strip()
    except UnicodeDecodeError as exc:
        raise GitOpsValidationError("BASE_REF", ".") from exc
    if not COMMIT_RE.fullmatch(candidate):
        raise GitOpsValidationError("BASE_REF", ".")
    return candidate


def _resolve_base_revision(root: Path, base_ref: str) -> str:
    repo = _git_root(root)
    if base_ref == ZERO_REVISION:
        head = _resolve_commit(repo, "HEAD")
        commit = _run_git(repo, ["cat-file", "-p", head])
        if commit.returncode != 0:
            raise GitOpsValidationError("BASE_REF", ".")
        header = commit.stdout.split(b"\n\n", 1)[0]
        parents = [line[7:] for line in header.splitlines() if line.startswith(b"parent ")]
        if not parents:
            return EMPTY_REVISION
        try:
            first_parent = parents[0].decode("ascii")
        except UnicodeDecodeError as exc:
            raise GitOpsValidationError("BASE_REF", ".") from exc
        if not COMMIT_RE.fullmatch(first_parent):
            raise GitOpsValidationError("BASE_REF", ".")
        return _resolve_commit(repo, first_parent)
    return _resolve_commit(repo, base_ref)


def _stable_path(path: PurePosixPath) -> str:
    value = path.as_posix()
    return _diagnostic_path(value)


class _ManifestSource:
    def __init__(self, root: Path, resolved_commit: str | None = None) -> None:
        if root.is_symlink():
            raise GitOpsValidationError("ROOT_SYMLINK", ".")
        if not root.exists():
            raise GitOpsValidationError("ROOT_MISSING", ".")
        if not root.is_dir():
            raise GitOpsValidationError("ROOT_NOT_DIRECTORY", ".")
        self.root = root.resolve()
        self.repo: Path | None = None
        self.root_in_repo = PurePosixPath(".")
        if resolved_commit is None:
            self.revision = WORKTREE_REVISION
        else:
            if not COMMIT_RE.fullmatch(resolved_commit):
                raise GitOpsValidationError("BASE_REF", ".")
            self.repo = _git_root(self.root)
            try:
                relative = self.root.relative_to(self.repo)
            except ValueError as exc:
                raise GitOpsValidationError("GIT_ROOT", ".") from exc
            self.root_in_repo = PurePosixPath(relative.as_posix())
            self.revision = resolved_commit

    def _repo_path(self, path: PurePosixPath) -> PurePosixPath:
        if self.root_in_repo == PurePosixPath("."):
            return path
        return self.root_in_repo / path

    def _worktree_entry_kind(self, path: PurePosixPath) -> str:
        current = self.root
        for part in path.parts:
            current = current / part
            try:
                info = current.lstat()
            except FileNotFoundError as exc:
                raise GitOpsValidationError("RESOURCE_MISSING", _stable_path(path)) from exc
            if stat.S_ISLNK(info.st_mode):
                raise GitOpsValidationError("RESOURCE_SYMLINK", _stable_path(path))
            if part != path.parts[-1] and not stat.S_ISDIR(info.st_mode):
                raise GitOpsValidationError("RESOURCE_NOT_REGULAR", _stable_path(path))
        if stat.S_ISREG(info.st_mode):
            return "file"
        if stat.S_ISDIR(info.st_mode):
            return "directory"
        raise GitOpsValidationError("RESOURCE_NOT_REGULAR", _stable_path(path))

    def _git_entry_kind(self, path: PurePosixPath) -> str:
        assert self.repo is not None
        repo_path = self._repo_path(path)
        for index in range(1, len(repo_path.parts) + 1):
            prefix = PurePosixPath(*repo_path.parts[:index])
            result = _run_git(
                self.repo,
                ["ls-tree", "-z", self.revision, "--", prefix.as_posix()],
            )
            if result.returncode != 0 or not result.stdout:
                raise GitOpsValidationError("RESOURCE_MISSING", _stable_path(path))
            record = result.stdout.split(b"\0", 1)[0]
            try:
                header, listed_path = record.split(b"\t", 1)
                mode, object_type, _object_id = header.split(b" ", 2)
                exact = listed_path.decode("utf-8") == prefix.as_posix()
            except (UnicodeDecodeError, ValueError) as exc:
                raise GitOpsValidationError("GIT_OBJECT", _stable_path(path)) from exc
            if not exact:
                raise GitOpsValidationError("GIT_OBJECT", _stable_path(path))
            if mode == b"120000":
                raise GitOpsValidationError("RESOURCE_SYMLINK", _stable_path(path))
            if index < len(repo_path.parts):
                if object_type != b"tree":
                    raise GitOpsValidationError("RESOURCE_NOT_REGULAR", _stable_path(path))
                continue
            if object_type == b"tree" and mode == b"040000":
                return "directory"
            if object_type == b"blob" and mode in (b"100644", b"100755"):
                return "file"
            raise GitOpsValidationError("RESOURCE_NOT_REGULAR", _stable_path(path))
        raise GitOpsValidationError("RESOURCE_MISSING", _stable_path(path))

    def entry_kind(self, path: PurePosixPath) -> str:
        if path.is_absolute() or ".." in path.parts:
            raise GitOpsValidationError("RESOURCE_ESCAPE", _stable_path(path))
        if not path.parts or path == PurePosixPath("."):
            return "directory"
        if self.revision == WORKTREE_REVISION:
            return self._worktree_entry_kind(path)
        return self._git_entry_kind(path)

    def read_text(self, path: PurePosixPath) -> str:
        if self.entry_kind(path) != "file":
            raise GitOpsValidationError("RESOURCE_NOT_REGULAR", _stable_path(path))
        if self.revision == WORKTREE_REVISION:
            try:
                return (self.root / Path(path.as_posix())).read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                raise GitOpsValidationError("RESOURCE_READ", _stable_path(path)) from exc
        assert self.repo is not None
        repo_path = self._repo_path(path)
        result = _run_git(
            self.repo,
            ["show", "--no-ext-diff", "--no-textconv", f"{self.revision}:{repo_path.as_posix()}"],
        )
        if result.returncode != 0:
            raise GitOpsValidationError("RESOURCE_READ", _stable_path(path))
        try:
            return result.stdout.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise GitOpsValidationError("RESOURCE_READ", _stable_path(path)) from exc

    def repository_roots(self) -> tuple[PurePosixPath, ...]:
        gitops = PurePosixPath("gitops")
        try:
            if self.entry_kind(gitops) != "directory":
                raise GitOpsValidationError("ROOT_NOT_DIRECTORY", "gitops")
        except GitOpsValidationError as exc:
            if exc.code == "RESOURCE_MISSING":
                raise GitOpsValidationError("KUSTOMIZATION_ROOT_MISSING", ".") from exc
            raise

        roots: list[PurePosixPath] = []
        if self.revision == WORKTREE_REVISION:
            start = self.root / "gitops"
            for directory, directory_names, file_names in os.walk(start, followlinks=False):
                relative_directory = Path(directory).relative_to(self.root)
                for name in list(directory_names):
                    candidate = Path(directory) / name
                    if candidate.is_symlink():
                        relative = PurePosixPath(candidate.relative_to(self.root).as_posix())
                        raise GitOpsValidationError("RESOURCE_SYMLINK", _stable_path(relative))
                if KUSTOMIZATION_NAME in file_names:
                    roots.append(
                        PurePosixPath((relative_directory / KUSTOMIZATION_NAME).as_posix())
                    )
        else:
            assert self.repo is not None
            prefix = self._repo_path(gitops).as_posix()
            result = _run_git(
                self.repo,
                ["ls-tree", "-r", "-z", "--name-only", self.revision, "--", prefix],
            )
            if result.returncode != 0:
                raise GitOpsValidationError("GIT_OBJECT", "gitops")
            for raw_path in result.stdout.split(b"\0"):
                if not raw_path:
                    continue
                try:
                    repo_path = PurePosixPath(raw_path.decode("utf-8"))
                    if self.root_in_repo == PurePosixPath("."):
                        relative = repo_path
                    else:
                        relative = repo_path.relative_to(self.root_in_repo)
                except (UnicodeDecodeError, ValueError) as exc:
                    raise GitOpsValidationError("GIT_OBJECT", "gitops") from exc
                if relative.name == KUSTOMIZATION_NAME:
                    roots.append(relative)
        if not roots:
            raise GitOpsValidationError("KUSTOMIZATION_ROOT_MISSING", "gitops")
        return tuple(sorted(set(roots), key=lambda item: item.as_posix()))


def _load_documents(source: _ManifestSource, path: PurePosixPath) -> list[Any]:
    try:
        documents = list(yaml.load_all(source.read_text(path), Loader=_UniqueKeyLoader))
    except yaml.YAMLError as exc:
        raise GitOpsValidationError("YAML_MALFORMED", _stable_path(path)) from exc
    if not documents or any(document is None for document in documents):
        raise GitOpsValidationError("YAML_DOCUMENT", _stable_path(path))
    return documents


def _manifest_source(root: Path, revision: str) -> _ManifestSource:
    if revision == WORKTREE_REVISION:
        return _ManifestSource(root)
    repo = _git_root(root)
    return _ManifestSource(root, _resolve_commit(repo, revision))


def _resource_path(raw: str, owner: PurePosixPath) -> PurePosixPath:
    if (
        not raw
        or not PATH_TOKEN_RE.fullmatch(raw)
        or "\\" in raw
        or "?" in raw
        or "#" in raw
        or "://" in raw
        or raw.startswith(("//", "git@"))
        or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", raw)
    ):
        raise GitOpsValidationError("RESOURCE_REFERENCE", _stable_path(owner))
    candidate = PurePosixPath(raw)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise GitOpsValidationError("RESOURCE_ESCAPE", _stable_path(owner))
    if (
        not candidate.parts
        or candidate.as_posix() != raw
        or any(part in ("", ".") for part in candidate.parts)
    ):
        raise GitOpsValidationError("RESOURCE_REFERENCE", _stable_path(owner))
    return candidate


def _validate_identity_tokens(
    api_version: Any,
    kind: Any,
    namespace: Any,
    name: Any,
    path: PurePosixPath,
) -> ObjectIdentity:
    if not all(isinstance(value, str) for value in (api_version, kind, namespace, name)):
        raise GitOpsValidationError("IDENTITY_MISSING", _stable_path(path))
    if (
        not API_VERSION_RE.fullmatch(api_version)
        or not KIND_RE.fullmatch(kind)
        or not IDENTITY_TOKEN_RE.fullmatch(name)
        or (namespace and not IDENTITY_TOKEN_RE.fullmatch(namespace))
    ):
        raise GitOpsValidationError("IDENTITY_TOKEN", _stable_path(path))
    return ObjectIdentity(api_version, kind, namespace, name)


def _identity(document: Any, path: PurePosixPath) -> ObjectIdentity:
    if not isinstance(document, dict):
        raise GitOpsValidationError("MANIFEST_DOCUMENT", _stable_path(path))
    api_version = document.get("apiVersion")
    kind = document.get("kind")
    metadata = document.get("metadata")
    if not isinstance(metadata, dict):
        raise GitOpsValidationError("IDENTITY_MISSING", _stable_path(path))
    name = metadata.get("name")
    namespace = metadata.get("namespace", "")
    required = (api_version, kind, name)
    if any(not isinstance(value, str) or not value for value in required):
        raise GitOpsValidationError("IDENTITY_MISSING", _stable_path(path))
    if not isinstance(namespace, str):
        raise GitOpsValidationError("IDENTITY_MISSING", _stable_path(path))
    return _validate_identity_tokens(api_version, kind, namespace, name, path)


def _render_roots(
    source: _ManifestSource, roots: Iterable[PurePosixPath]
) -> dict[ObjectIdentity, RenderedObject]:
    graph: dict[ObjectIdentity, RenderedObject] = {}
    completed_kustomizations: set[PurePosixPath] = set()
    active_kustomizations: set[PurePosixPath] = set()

    def add_manifest(path: PurePosixPath) -> None:
        for document in _load_documents(source, path):
            identity = _identity(document, path)
            if identity in graph:
                raise GitOpsValidationError("IDENTITY_DUPLICATE", _stable_path(path))
            graph[identity] = RenderedObject(identity, _stable_path(path))

    def visit_kustomization(path: PurePosixPath) -> None:
        if path in active_kustomizations:
            raise GitOpsValidationError("KUSTOMIZATION_CYCLE", _stable_path(path))
        if path in completed_kustomizations:
            return
        active_kustomizations.add(path)
        documents = _load_documents(source, path)
        if len(documents) != 1 or not isinstance(documents[0], dict):
            raise GitOpsValidationError("KUSTOMIZATION_DOCUMENT", _stable_path(path))
        document = documents[0]
        if set(document) - ALLOWED_KUSTOMIZATION_KEYS:
            raise GitOpsValidationError("KUSTOMIZATION_UNSUPPORTED", _stable_path(path))
        if (
            document.get("kind") != KUSTOMIZATION_KIND
            or document.get("apiVersion") != KUSTOMIZATION_API_VERSION
        ):
            raise GitOpsValidationError("KUSTOMIZATION_UNSUPPORTED", _stable_path(path))
        resources = document.get("resources", [])
        if not isinstance(resources, list) or any(
            not isinstance(resource, str) for resource in resources
        ):
            raise GitOpsValidationError("KUSTOMIZATION_RESOURCES", _stable_path(path))
        for raw_resource in resources:
            relative = _resource_path(raw_resource, path)
            target = path.parent / relative
            kind = source.entry_kind(target)
            if kind == "directory":
                visit_kustomization(target / KUSTOMIZATION_NAME)
            elif target.name == KUSTOMIZATION_NAME:
                visit_kustomization(target)
            else:
                add_manifest(target)
        active_kustomizations.remove(path)
        completed_kustomizations.add(path)

    for kustomization in roots:
        visit_kustomization(kustomization)
    return dict(sorted(graph.items()))


def _render_path_root(
    root: Path, revision: str
) -> dict[ObjectIdentity, RenderedObject]:
    if revision == EMPTY_REVISION:
        return {}
    source = _manifest_source(root, revision)
    return _render_roots(source, (PurePosixPath(KUSTOMIZATION_NAME),))


def render_identity_graph(
    root: Path, revision: str
) -> dict[ObjectIdentity, RenderedObject]:
    """Render repository GitOps resources to a four-field identity graph."""

    if revision == EMPTY_REVISION:
        return {}
    source = _manifest_source(root, revision)
    return _render_roots(source, source.repository_roots())


def diff_identities(
    base: dict[ObjectIdentity, RenderedObject],
    head: dict[ObjectIdentity, RenderedObject],
) -> ChangeSet:
    """Diff identity keys, retaining the correct side's path as evidence."""

    base_keys = set(base)
    head_keys = set(head)
    return ChangeSet(
        added=tuple(head[identity] for identity in sorted(head_keys - base_keys)),
        deleted=tuple(base[identity] for identity in sorted(base_keys - head_keys)),
        retained=tuple(head[identity] for identity in sorted(base_keys & head_keys)),
    )


def format_identity(change: str, rendered: RenderedObject) -> str:
    identity = rendered.identity
    if change not in ("ADD", "DELETE", "RETAIN"):
        raise GitOpsValidationError("OUTPUT_CHANGE", ".")
    if not isinstance(rendered.path, str) or not _is_safe_repository_path(rendered.path):
        raise GitOpsValidationError("OUTPUT_PATH", ".")
    _validate_identity_tokens(
        identity.api_version,
        identity.kind,
        identity.namespace,
        identity.name,
        PurePosixPath(rendered.path),
    )
    namespace = identity.namespace or "_cluster"
    return f"{change} {identity.api_version} {identity.kind} {namespace}/{identity.name} {rendered.path}"


def _format_change_set(change_set: ChangeSet) -> list[str]:
    rows: list[str] = []
    for change, rendered_objects in (
        ("ADD", change_set.added),
        ("DELETE", change_set.deleted),
        ("RETAIN", change_set.retained),
    ):
        rows.extend(format_identity(change, rendered) for rendered in rendered_objects)
    return rows


def _render_diff(
    base_root: Path,
    base_revision: str,
    head_root: Path,
    head_revision: str,
) -> list[str]:
    base = render_identity_graph(base_root, base_revision)
    head = render_identity_graph(head_root, head_revision)
    return _format_change_set(diff_identities(base, head))


def _render_path_diff(base_root: Path, head_root: Path) -> list[str]:
    base = _render_path_root(base_root, WORKTREE_REVISION)
    head = _render_path_root(head_root, WORKTREE_REVISION)
    return _format_change_set(diff_identities(base, head))


def _expect_self_test_error(code: str, operation: Any) -> None:
    try:
        operation()
    except GitOpsValidationError as exc:
        if exc.code != code or _diagnostic_path(exc.path) != exc.path:
            raise GitOpsValidationError("SELF_TEST_MISMATCH", ".") from exc
    else:
        raise GitOpsValidationError("SELF_TEST_MISMATCH", ".")


def _write_self_test_case(
    parent: Path,
    name: str,
    kustomization: str,
    files: tuple[tuple[str, str], ...] = (),
) -> Path:
    root = parent / name
    root.mkdir()
    (root / KUSTOMIZATION_NAME).write_text(kustomization, encoding="utf-8")
    for relative, content in files:
        (root / relative).write_text(content, encoding="utf-8")
    return root


def _render_self_test_case(root: Path) -> dict[ObjectIdentity, RenderedObject]:
    return _render_path_root(root, WORKTREE_REVISION)


def _run_self_test_git(repo: Path, arguments: list[str]) -> str:
    result = _run_git(repo, arguments)
    if result.returncode != 0:
        raise GitOpsValidationError("SELF_TEST_MISMATCH", ".")
    try:
        return result.stdout.decode("ascii").strip()
    except UnicodeDecodeError as exc:
        raise GitOpsValidationError("SELF_TEST_MISMATCH", ".") from exc


def _self_test_boundaries() -> None:
    supported = (
        f"apiVersion: {KUSTOMIZATION_API_VERSION}\n"
        f"kind: {KUSTOMIZATION_KIND}\n"
    )
    manifest = "apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: safe\n"

    with tempfile.TemporaryDirectory(prefix="gitops-change-set-") as raw_temp:
        temp = Path(raw_temp)

        traversal = _write_self_test_case(
            temp, "traversal", supported + "resources: [../outside.yaml]\n"
        )
        _expect_self_test_error(
            "RESOURCE_ESCAPE", lambda: _render_self_test_case(traversal)
        )

        remote = _write_self_test_case(
            temp, "remote", supported + "resources: [https://example.invalid/object.yaml]\n"
        )
        _expect_self_test_error(
            "RESOURCE_REFERENCE", lambda: _render_self_test_case(remote)
        )

        symlink = _write_self_test_case(
            temp,
            "symlink",
            supported + "resources: [linked.yaml]\n",
            (("target.yaml", manifest),),
        )
        (symlink / "linked.yaml").symlink_to("target.yaml")
        _expect_self_test_error(
            "RESOURCE_SYMLINK", lambda: _render_self_test_case(symlink)
        )

        non_regular = _write_self_test_case(
            temp, "non-regular", supported + "resources: [pipe.yaml]\n"
        )
        os.mkfifo(non_regular / "pipe.yaml")
        _expect_self_test_error(
            "RESOURCE_NOT_REGULAR", lambda: _render_self_test_case(non_regular)
        )

        cycle = _write_self_test_case(
            temp, "cycle", supported + "resources: [kustomization.yaml]\n"
        )
        _expect_self_test_error(
            "KUSTOMIZATION_CYCLE", lambda: _render_self_test_case(cycle)
        )

        duplicate_identity = _write_self_test_case(
            temp,
            "duplicate-identity",
            supported + "resources: [one.yaml, two.yaml]\n",
            (("one.yaml", manifest), ("two.yaml", manifest)),
        )
        _expect_self_test_error(
            "IDENTITY_DUPLICATE", lambda: _render_self_test_case(duplicate_identity)
        )

        duplicate_key = _write_self_test_case(
            temp,
            "duplicate-key",
            supported + "resources: [object.yaml]\n",
            (("object.yaml", manifest + "kind: Service\n"),),
        )
        _expect_self_test_error(
            "YAML_MALFORMED", lambda: _render_self_test_case(duplicate_key)
        )

        identity_mutations = (
            (
                "numeric",
                "apiVersion: 1\nkind: ConfigMap\nmetadata: {name: safe}\n",
                "IDENTITY_MISSING",
            ),
            (
                "null",
                "apiVersion: null\nkind: ConfigMap\nmetadata: {name: safe}\n",
                "IDENTITY_MISSING",
            ),
            (
                "mapping",
                "apiVersion: v1\nkind: {unsafe: value}\nmetadata: {name: safe}\n",
                "IDENTITY_MISSING",
            ),
            (
                "list",
                "apiVersion: v1\nkind: ConfigMap\n"
                "metadata: {name: safe, namespace: [bad]}\n",
                "IDENTITY_MISSING",
            ),
            (
                "newline",
                'apiVersion: v1\nkind: ConfigMap\nmetadata: {name: "bad\\nspec:"}\n',
                "IDENTITY_TOKEN",
            ),
            (
                "space",
                "apiVersion: v1\nkind: 'Config Map'\nmetadata: {name: safe}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "data-token",
                "apiVersion: v1\nkind: ConfigMap\nmetadata: {name: 'data:'}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "spec-token",
                "apiVersion: v1\nkind: ConfigMap\n"
                "metadata: {name: safe, namespace: 'spec:'}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "kind-slash",
                "apiVersion: v1\nkind: Config/Map\nmetadata: {name: safe}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "name-slash",
                "apiVersion: v1\nkind: ConfigMap\nmetadata: {name: unsafe/name}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "namespace-slash",
                "apiVersion: v1\nkind: ConfigMap\n"
                "metadata: {name: safe, namespace: unsafe/name}\n",
                "IDENTITY_TOKEN",
            ),
            (
                "api-slashes",
                "apiVersion: unsafe/group/v1\nkind: ConfigMap\nmetadata: {name: safe}\n",
                "IDENTITY_TOKEN",
            ),
        )
        for name, content, expected_code in identity_mutations:
            mutation = _write_self_test_case(
                temp,
                f"identity-{name}",
                supported + "resources: [object.yaml]\n",
                (("object.yaml", content),),
            )
            _expect_self_test_error(
                expected_code, lambda mutation=mutation: _render_self_test_case(mutation)
            )

        unsafe_path = _write_self_test_case(
            temp, "unsafe-path", supported + "resources: ['bad path.yaml']\n"
        )
        _expect_self_test_error(
            "RESOURCE_REFERENCE", lambda: _render_self_test_case(unsafe_path)
        )
        _expect_self_test_error(
            "OUTPUT_PATH",
            lambda: format_identity(
                "RETAIN",
                RenderedObject(ObjectIdentity("v1", "ConfigMap", "safe", "safe"), "bad path.yaml"),
            ),
        )

        unsupported_version = _write_self_test_case(
            temp,
            "unsupported-version",
            "apiVersion: kustomize.config.k8s.io/v1\nkind: Kustomization\nresources: []\n",
        )
        _expect_self_test_error(
            "KUSTOMIZATION_UNSUPPORTED",
            lambda: _render_self_test_case(unsupported_version),
        )

        unsupported_kind = _write_self_test_case(
            temp,
            "unsupported-kind",
            f"apiVersion: {KUSTOMIZATION_API_VERSION}\nkind: ConfigMap\nresources: []\n",
        )
        _expect_self_test_error(
            "KUSTOMIZATION_UNSUPPORTED", lambda: _render_self_test_case(unsupported_kind)
        )

        unsupported_directive = _write_self_test_case(
            temp,
            "unsupported-directive",
            supported + "resources: []\ngenerators: []\n",
        )
        _expect_self_test_error(
            "KUSTOMIZATION_UNSUPPORTED",
            lambda: _render_self_test_case(unsupported_directive),
        )

        multi_document = _write_self_test_case(
            temp,
            "multi-document",
            supported + "resources: [objects.yaml]\n",
            (
                (
                    "objects.yaml",
                    "apiVersion: v1\nkind: ConfigMap\nmetadata: {name: one}\n"
                    "---\napiVersion: v1\nkind: Service\nmetadata: {name: two}\n",
                ),
            ),
        )
        multi_graph = _render_self_test_case(multi_document)
        if len(multi_graph) != 2 or {item.path for item in multi_graph.values()} != {
            "objects.yaml"
        }:
            raise GitOpsValidationError("SELF_TEST_MISMATCH", ".")

        history = temp / "history"
        history.mkdir()
        _run_self_test_git(history, ["init", "--quiet"])
        _run_self_test_git(history, ["config", "user.name", "GitOps Self Test"])
        _run_self_test_git(history, ["config", "user.email", "gitops-self-test@example.invalid"])
        (history / "state.txt").write_text("root\n", encoding="utf-8")
        _run_self_test_git(history, ["add", "state.txt"])
        _run_self_test_git(history, ["commit", "--quiet", "-m", "root"])
        root_commit = _run_self_test_git(history, ["rev-parse", "HEAD"])
        if _resolve_base_revision(history, ZERO_REVISION) != EMPTY_REVISION:
            raise GitOpsValidationError("SELF_TEST_MISMATCH", ".")

        for unsafe_ref in ("", "HEAD\nmain", "--help", "HEAD:state.txt", "refs//heads/main"):
            _expect_self_test_error(
                "BASE_REF",
                lambda unsafe_ref=unsafe_ref: _resolve_base_revision(history, unsafe_ref),
            )

        (history / "state.txt").write_text("second\n", encoding="utf-8")
        _run_self_test_git(history, ["add", "state.txt"])
        _run_self_test_git(history, ["commit", "--quiet", "-m", "second"])
        head_commit = _run_self_test_git(history, ["rev-parse", "HEAD"])
        push_before = _resolve_base_revision(history, root_commit)
        pull_request_base = _resolve_base_revision(history, head_commit)
        zero_before = _resolve_base_revision(history, ZERO_REVISION)
        if (push_before, pull_request_base, zero_before) != (
            root_commit,
            head_commit,
            root_commit,
        ):
            raise GitOpsValidationError("SELF_TEST_MISMATCH", ".")

        shallow = temp / "shallow"
        _run_self_test_git(
            temp,
            ["clone", "--quiet", "--depth", "1", history.resolve().as_uri(), str(shallow)],
        )
        if _run_self_test_git(shallow, ["rev-parse", "--is-shallow-repository"]) != "true":
            raise GitOpsValidationError("SELF_TEST_MISMATCH", ".")
        _expect_self_test_error(
            "BASE_REF", lambda: _resolve_base_revision(shallow, ZERO_REVISION)
        )


def _self_test() -> int:
    fixture = Path(__file__).resolve().parents[1] / "tests/fixtures/gitops-change-set"
    cases_path = fixture / "cases.json"
    try:
        cases = json.loads(cases_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise GitOpsValidationError("SELF_TEST_FIXTURE", "cases.json") from exc
    expected = cases.get("expected")
    forbidden = cases.get("forbidden_output")
    if not isinstance(expected, list) or not all(isinstance(row, str) for row in expected):
        raise GitOpsValidationError("SELF_TEST_FIXTURE", "cases.json")
    if not isinstance(forbidden, list) or not all(isinstance(row, str) for row in forbidden):
        raise GitOpsValidationError("SELF_TEST_FIXTURE", "cases.json")
    rows = _render_path_diff(fixture / "base", fixture / "head")
    output = "\n".join(rows)
    if rows != expected or any(value in output for value in forbidden):
        raise GitOpsValidationError("SELF_TEST_MISMATCH", "cases.json")
    _self_test_boundaries()
    if rows:
        print(output)
    return 0


def _parse_args(arguments: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--base-ref", default=os.environ.get("BASE_REF", "HEAD"))
    return parser.parse_args(arguments)


def main(arguments: Iterable[str] | None = None) -> int:
    args = _parse_args(arguments)
    try:
        if args.self_test:
            return _self_test()
        base_revision = _resolve_base_revision(args.root, args.base_ref)
        rows = _render_diff(
            args.root,
            base_revision,
            args.root,
            WORKTREE_REVISION,
        )
        if rows:
            print("\n".join(rows))
        return 0
    except GitOpsValidationError as exc:
        print(f"ERROR {exc.code} {exc.path}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
