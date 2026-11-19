#!/usr/bin/env python3
"""Offline, pinned render and built-in API schema evidence for local GitOps roots."""

from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import stat
import subprocess
import sys
from typing import Any, Sequence

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from validation.platform.ingress import validate as validate_ingress  # noqa: E402


KUSTOMIZE_SHA256 = "f7b1605aa5143e0dcbd754a4d43c47ad7a560c540b1356b064d69fe236164494"
KUSTOMIZE_VERSION = "v5.8.1"
SCHEMA_SOURCE_COMMIT = "8df8a883b68a24a104b4a9e43c1288090ae60b3b"
SOURCE_REPO = "https://github.com/buenhyden/hy-home.k8s.git"
SOURCE_REVISION = "main"
SCHEMA_DIR = Path(__file__).resolve().parent / "schemas"
KNOWN_CR = {
    "argoproj.io/v1alpha1:AnalysisTemplate",
    "argoproj.io/v1alpha1:AppProject",
    "argoproj.io/v1alpha1:Application",
    "argoproj.io/v1alpha1:ApplicationSet",
    "argoproj.io/v1alpha1:Rollout",
    "cert-manager.io/v1:ClusterIssuer",
    "external-secrets.io/v1beta1:ClusterSecretStore",
    "external-secrets.io/v1beta1:ExternalSecret",
    "networking.istio.io/v1beta1:DestinationRule",
    "networking.istio.io/v1beta1:VirtualService",
    "security.istio.io/v1beta1:PeerAuthentication",
}
CLUSTER_KINDS = {
    ("", "Namespace"),
    ("cert-manager.io", "ClusterIssuer"),
    ("external-secrets.io", "ClusterSecretStore"),
    ("networking.k8s.io", "IngressClass"),
    ("rbac.authorization.k8s.io", "ClusterRole"),
    ("rbac.authorization.k8s.io", "ClusterRoleBinding"),
}
GVK_PATTERN = re.compile(
    r"^[a-z0-9.-]+(?:/v[0-9]+(?:alpha|beta)?[0-9]*)?:[A-Z][A-Za-z0-9]*$"
)
MAX_MANIFEST_WALK_ENTRIES = 100_000
INGRESS_CONSUMER_ROOTS = frozenset(
    {
        Path("gitops/platform/ingress-routes"),
        Path("gitops/platform/cert-manager"),
        Path("gitops/platform/headlamp"),
        Path("gitops/platform/kiali"),
        Path("gitops/workloads/adminer"),
    }
)
PROJECT_CONTROL_ROOTS = frozenset(
    {Path("gitops/apps/root"), Path("gitops/clusters/local")}
)
SCOPED_DEPENDENCY_KEYS = frozenset(
    {"components", "patches", "patchesStrategicMerge", "patchesJson6902"}
)
RAW_SCOPE_COMMON_SOURCES = frozenset(
    {
        "scripts/validation/platform/assurance.py",
        "scripts/run-validation-lane.py",
        "scripts/validation/registry.json",
    }
)


class AssuranceError(ValueError):
    """A value-free failure that is safe to classify in QA evidence."""


class UniqueSafeLoader(yaml.SafeLoader):
    def construct_mapping(self, node: yaml.MappingNode, deep: bool = False) -> dict:
        result: dict = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str) or key in result:
                raise AssuranceError("duplicate or invalid YAML key")
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def _read_regular(path: Path, limit: int) -> bytes:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > limit:
        raise AssuranceError("missing, linked, or oversized local input")
    return path.read_bytes()


def _walk_no_follow(directory: Path):
    """Yield tree entries without following linked directories or hiding read errors."""
    stack = [directory]
    visited = 0
    while stack:
        current = stack.pop()
        try:
            with os.scandir(current) as entries:
                for entry in entries:
                    visited += 1
                    if visited > MAX_MANIFEST_WALK_ENTRIES:
                        raise AssuranceError("manifest candidate walk limit exceeded")
                    try:
                        mode = entry.stat(follow_symlinks=False).st_mode
                    except OSError as exc:
                        raise AssuranceError(
                            "manifest candidate node unavailable"
                        ) from exc
                    path = Path(entry.path)
                    yield path, mode
                    if stat.S_ISDIR(mode):
                        stack.append(path)
        except OSError as exc:
            raise AssuranceError("manifest candidate directory unavailable") from exc


def validate_manifest_candidates(root: Path) -> None:
    """Keep the former all-files manifest node boundary without reparsing YAML."""
    required = []
    for name in ("gitops", "infrastructure"):
        directory = root / name
        try:
            mode = directory.lstat().st_mode
        except OSError as exc:
            raise AssuranceError("required manifest root unavailable") from exc
        if not stat.S_ISDIR(mode):
            raise AssuranceError("required manifest root is not a directory")
        required.append(directory)

    inspected = 0
    yaml_seen = False
    for directory in required:
        for path, mode in _walk_no_follow(directory):
            inspected += 1
            if inspected > MAX_MANIFEST_WALK_ENTRIES:
                raise AssuranceError("manifest candidate walk limit exceeded")
            if path.suffix not in {".yaml", ".yml"}:
                continue
            if not stat.S_ISREG(mode):
                raise AssuranceError("manifest candidate must be a regular file")
            yaml_seen = True

    examples = root / "examples"
    try:
        examples_mode = examples.lstat().st_mode
    except FileNotFoundError:
        examples_mode = None
    except OSError as exc:
        raise AssuranceError("examples manifest root unavailable") from exc
    if examples_mode is not None:
        if not stat.S_ISDIR(examples_mode):
            raise AssuranceError("examples manifest root is not a regular directory")
        eligible_dirs: set[Path] = set()
        for path, mode in _walk_no_follow(examples):
            inspected += 1
            if inspected > MAX_MANIFEST_WALK_ENTRIES:
                raise AssuranceError("manifest candidate walk limit exceeded")
            eligible = path.parent in eligible_dirs
            if stat.S_ISDIR(mode) and (
                eligible
                or path == examples / "sample-app"
                or path.name in {"gitops", "kubernetes"}
            ):
                eligible_dirs.add(path)
            if eligible and path.suffix in {".yaml", ".yml"}:
                if not stat.S_ISREG(mode):
                    raise AssuranceError("manifest candidate must be a regular file")
                yaml_seen = True
    if not yaml_seen:
        raise AssuranceError("no manifest YAML candidate")


def _raw_eligible(path: Path, *, policy: bool) -> bool:
    if path.suffix not in {".yaml", ".yml"}:
        return False
    if path.parts[0] in {"gitops", "infrastructure"}:
        return True
    if path.parts[0] != "examples":
        return False
    return (
        policy
        or path.parts[:2] == ("examples", "sample-app")
        or any(part in {"kubernetes", "gitops"} for part in path.parts[1:-1])
    )


def _existing_regular(root: Path, relative: Path) -> bool:
    current = root
    for index, part in enumerate(relative.parts):
        current /= part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            return False
        except OSError as exc:
            raise AssuranceError("manifest path unavailable") from exc
        if stat.S_ISLNK(mode):
            raise AssuranceError("linked manifest path")
        if index < len(relative.parts) - 1 and not stat.S_ISDIR(mode):
            raise AssuranceError("manifest parent is not a directory")
    if not stat.S_ISREG(mode):
        raise AssuranceError("manifest candidate must be a regular file")
    if current.stat().st_size > 2_000_000:
        raise AssuranceError("manifest candidate is oversized")
    return True


def manifest_paths(
    root: Path, changed_paths: Sequence[str] | None = None, *, policy: bool = False
) -> list[Path]:
    """Return bounded repo-relative YAML inputs for syntax or Conftest consumers."""
    if (
        any(member.is_symlink() for member in (root, *root.parents))
        or not root.is_dir()
    ):
        raise AssuranceError("repository root unavailable")
    directories = ("gitops", "infrastructure", "examples")
    for name in directories if policy else directories[:2]:
        directory = root / name
        if directory.is_symlink() or not directory.is_dir():
            raise AssuranceError("required manifest root unavailable")
    paths = (
        None
        if changed_paths is None
        else [_changed_path(item) for item in changed_paths]
    )
    source_change = paths is not None and any(
        path.as_posix() in RAW_SCOPE_COMMON_SOURCES
        or path.as_posix().startswith(".github/requirements/")
        or (
            policy
            and (
                path.as_posix() == "scripts/validate-policy-gates.sh"
                or path.as_posix().startswith("policy/conftest/")
            )
        )
        or (not policy and path.as_posix() == "scripts/validate-k8s-manifests.sh")
        for path in paths or []
    )
    if paths is not None and not source_change:
        return sorted(
            {
                path
                for path in paths
                if _raw_eligible(path, policy=policy) and _existing_regular(root, path)
            }
        )
    selected: list[Path] = []
    inspected = 0
    for name in directories:
        directory = root / name
        if not directory.exists():
            continue
        for path, mode in _walk_no_follow(directory):
            inspected += 1
            if inspected > MAX_MANIFEST_WALK_ENTRIES:
                raise AssuranceError("manifest candidate walk limit exceeded")
            relative = path.relative_to(root)
            if not _raw_eligible(relative, policy=policy):
                continue
            if not stat.S_ISREG(mode):
                raise AssuranceError("manifest candidate must be a regular file")
            if path.stat().st_size > 2_000_000:
                raise AssuranceError("manifest candidate is oversized")
            selected.append(relative)
    if not selected:
        raise AssuranceError("no YAML manifests matched")
    return sorted(set(selected))


def discover_roots(root: Path) -> list[Path]:
    gitops = root / "gitops"
    if not gitops.is_dir() or gitops.is_symlink():
        raise AssuranceError("GitOps root unavailable")
    roots = {p.parent.relative_to(root) for p in gitops.rglob("kustomization.yaml")}
    example = Path("examples/sample-app")
    if (root / example / "kustomization.yaml").exists():
        roots.add(example)
    if not roots:
        raise AssuranceError("no local Kustomize roots")
    return sorted(roots)


def _changed_path(value: str) -> Path:
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
        raise AssuranceError("invalid changed path")
    pure = PurePosixPath(value)
    if (
        pure.is_absolute()
        or pure.as_posix() != value
        or any(part in (".", "..") for part in pure.parts)
    ):
        raise AssuranceError("unsafe changed path")
    return Path(*pure.parts)


def _root_dependencies(root: Path, relative: Path) -> set[Path]:
    dependencies: set[Path] = set()
    completed: set[Path] = set()
    active: set[Path] = set()

    def visit(directory: Path) -> None:
        path = directory / "kustomization.yaml"
        if path in active:
            raise AssuranceError("cyclic Kustomize root")
        if path in completed:
            return
        active.add(path)
        dependencies.add(path)
        try:
            document = yaml.load(_read_regular(path, 65536), Loader=UniqueSafeLoader)
        except (yaml.YAMLError, UnicodeError) as exc:
            raise AssuranceError("malformed Kustomization") from exc
        if not isinstance(document, dict) or set(document) - (
            {"apiVersion", "kind", "resources"} | SCOPED_DEPENDENCY_KEYS
        ):
            raise AssuranceError("unsupported Kustomization fields")
        resources = document.get("resources", [])
        if not isinstance(resources, list) or any(
            not isinstance(item, str) for item in resources
        ):
            raise AssuranceError("invalid Kustomization resources")
        components = document.get("components", [])
        strategic = document.get("patchesStrategicMerge", [])
        if any(
            not isinstance(items, list)
            or any(not isinstance(item, str) for item in items)
            for items in (components, strategic)
        ):
            raise AssuranceError("invalid Kustomization dependencies")
        for item in [*resources, *components, *strategic]:
            target = _local_path(root, directory, item)
            dependencies.add(target)
            if item in (*resources, *components) and target.is_dir():
                visit(target)
        for field in ("patches", "patchesJson6902"):
            entries = document.get(field, [])
            if not isinstance(entries, list):
                raise AssuranceError("invalid Kustomization patches")
            for entry in entries:
                if not isinstance(entry, dict):
                    raise AssuranceError("invalid Kustomization patch")
                patch_path = entry.get("path")
                if patch_path is not None:
                    dependencies.add(_local_path(root, directory, patch_path))
        active.remove(path)
        completed.add(path)

    visit(root / relative)
    return dependencies


def affected_roots(root: Path, changed_paths: list[str]) -> list[Path]:
    """Select local Kustomize roots whose inputs or directory changed."""
    paths = [_changed_path(path) for path in changed_paths]
    roots = discover_roots(root)
    if any(
        path.as_posix().startswith(
            ("infrastructure/", "charts/", "crds/", "scripts/validation/platform/")
        )
        or path.as_posix()
        in {
            "scripts/validate-gitops-change-set.py",
            "scripts/render-platform-chart-kinds.sh",
            "scripts/validation/registry.json",
            ".kube-linter.yaml",
        }
        for path in paths
    ):
        return roots
    selected = []
    for relative in roots:
        dependencies = _root_dependencies(root, relative)
        if any(
            path.is_relative_to(relative)
            or any(
                (root / path).is_relative_to(dependency) for dependency in dependencies
            )
            for path in paths
        ):
            selected.append(relative)
    if set(selected) & (INGRESS_CONSUMER_ROOTS | {Path("gitops/apps/root")}):
        selected = sorted(set(selected) | (INGRESS_CONSUMER_ROOTS & set(roots)))
    if selected and any(relative.parts[0] == "gitops" for relative in selected):
        selected = sorted(set(selected) | (PROJECT_CONTROL_ROOTS & set(roots)))
    if not selected:
        for path in paths:
            if path.parts[0] != "gitops":
                continue
            try:
                (root / path).lstat()
            except FileNotFoundError:
                continue  # A deleted root is checked against the base identity graph.
            except OSError as exc:
                raise AssuranceError("changed GitOps path unavailable") from exc
            raise AssuranceError("changed GitOps path has no Kustomize owner")
    return selected


def _local_path(root: Path, base: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or ":" in value or "\\" in value:
        raise AssuranceError("nonlocal resource reference")
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or any(part == "." for part in candidate.parts):
        raise AssuranceError("unsafe resource path")
    path = Path(os.path.normpath(base.joinpath(*candidate.parts)))
    if not path.is_relative_to(root):
        raise AssuranceError("resource escapes repository")
    for member in (path, *path.parents):
        if member == root.parent:
            break
        if member.is_symlink():
            raise AssuranceError("linked resource path")
    return path


def check_kustomization(
    root: Path, relative: Path, visited: set[Path] | None = None
) -> None:
    visited = set() if visited is None else visited
    directory = root / relative
    if directory in visited or directory.is_symlink() or not directory.is_dir():
        raise AssuranceError("cyclic or unavailable Kustomize root")
    visited.add(directory)
    path = directory / "kustomization.yaml"
    try:
        data = yaml.load(_read_regular(path, 65536), Loader=UniqueSafeLoader)
    except (yaml.YAMLError, UnicodeError) as exc:
        raise AssuranceError("malformed Kustomization") from exc
    if not isinstance(data, dict) or set(data) != {"apiVersion", "kind", "resources"}:
        raise AssuranceError("unsupported Kustomization fields")
    if (
        data["apiVersion"] != "kustomize.config.k8s.io/v1beta1"
        or data["kind"] != "Kustomization"
    ):
        raise AssuranceError("unsupported Kustomization identity")
    resources = data["resources"]
    if (
        not isinstance(resources, list)
        or not resources
        or len(resources) != len(set(map(str, resources)))
    ):
        raise AssuranceError("invalid Kustomization resources")
    for resource in resources:
        target = _local_path(root, directory, resource)
        if target.is_dir():
            check_kustomization(root, target.relative_to(root), visited)
        elif target.suffix in {".yaml", ".yml"}:
            if not target.is_relative_to(directory):
                raise AssuranceError("resource escapes Kustomize root")
            _read_regular(target, 2_000_000)
        else:
            raise AssuranceError("unsupported local resource")


def _schema_manifest(corpus: Path) -> dict[str, Any]:
    try:
        data = json.loads(_read_regular(corpus / "manifest.json", 16384))
    except (ValueError, UnicodeError) as exc:
        raise AssuranceError("invalid pinned schema manifest") from exc
    if not isinstance(data, dict) or (
        data.get("commit") != SCHEMA_SOURCE_COMMIT
        or data.get("profile") != "v1.35.0-standalone-strict"
        or data.get("normalization") != "append-one-final-newline-to-upstream-files"
        or not isinstance(data.get("schemas"), dict)
    ):
        raise AssuranceError("unexpected pinned schema source")
    return data["schemas"]


def schema_class(gvk: str) -> str:
    if gvk in KNOWN_CR:
        return "DEFER"
    return "PASS" if gvk in _schema_manifest(SCHEMA_DIR) else "FAIL"


def load_schema(corpus: Path, gvk: str) -> dict[str, Any]:
    record = _schema_manifest(corpus).get(gvk)
    if not isinstance(record, dict) or set(record) != {"file", "sha256"}:
        raise AssuranceError("unknown built-in schema")
    name, digest = record["file"], record["sha256"]
    if not isinstance(name, str) or not re.fullmatch(r"[a-z0-9-]+\.json", name):
        raise AssuranceError("invalid pinned schema path")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise AssuranceError("invalid pinned schema digest")
    raw = _read_regular(corpus / name, 2_000_000)
    if hashlib.sha256(raw).hexdigest() != digest:
        raise AssuranceError("pinned schema digest mismatch")
    try:
        schema = json.loads(raw)
    except (ValueError, UnicodeError) as exc:
        raise AssuranceError("invalid pinned schema JSON") from exc
    if (
        not isinstance(schema, dict)
        or schema.get("$schema") != "http://json-schema.org/schema#"
    ):
        raise AssuranceError("unexpected pinned schema format")
    api_version, kind = gvk.split(":", 1)
    group, version_id = (
        api_version.rsplit("/", 1) if "/" in api_version else ("", api_version)
    )
    if schema.get("x-kubernetes-group-version-kind") != [
        {"group": group, "kind": kind, "version": version_id}
    ]:
        raise AssuranceError("pinned schema identity mismatch")
    return schema


def schema_findings(schema: dict[str, Any], document: dict[str, Any]) -> bool:
    # The upstream generic $schema URI has no specific draft; its standalone
    # corpus uses structural keywords supported by the existing offline helper.
    shared_path = str(Path(__file__).resolve().parents[2])
    if shared_path not in sys.path:
        sys.path.insert(0, shared_path)
    from json_schema_validation import SchemaEvaluationError, schema_errors

    try:
        return bool(
            schema_errors(
                {key: value for key, value in schema.items() if key != "$schema"},
                document,
            )
        )
    except SchemaEvaluationError as exc:
        raise AssuranceError("schema evaluation unavailable") from exc


def _row(
    target: str, depth: str, tool: str, tool_version: str, fallback: str, result: str
) -> dict[str, str]:
    return {
        "target": target,
        "depth": depth,
        "tool": tool,
        "toolVersion": tool_version,
        "fallback": fallback,
        "result": result,
    }


def _tool_is_pinned(binary: Path) -> bool:
    try:
        if (
            hashlib.sha256(_read_regular(binary, 50_000_000)).hexdigest()
            != KUSTOMIZE_SHA256
        ):
            return False
        process = subprocess.run(
            [str(binary), "version"], capture_output=True, timeout=5, check=False
        )
        return (
            process.returncode == 0
            and process.stdout.strip() == KUSTOMIZE_VERSION.encode()
        )
    except (AssuranceError, OSError, subprocess.TimeoutExpired):
        return False


def _render(root: Path, relative: Path, binary: Path) -> list[dict[str, Any]]:
    check_kustomization(root, relative)
    process = subprocess.run(
        [
            str(binary),
            "build",
            "--load-restrictor",
            "LoadRestrictionsRootOnly",
            str(relative),
        ],
        cwd=root,
        capture_output=True,
        timeout=15,
        check=False,
    )
    if process.returncode or not process.stdout or len(process.stdout) > 4_000_000:
        raise AssuranceError("Kustomize render failed")
    try:
        documents = list(yaml.load_all(process.stdout, Loader=UniqueSafeLoader))
    except (yaml.YAMLError, UnicodeError) as exc:
        raise AssuranceError("malformed Kustomize output") from exc
    if not documents or any(not isinstance(doc, dict) for doc in documents):
        raise AssuranceError("empty or invalid Kustomize output")
    seen = set()
    for document in documents:
        api_version, kind = document.get("apiVersion"), document.get("kind")
        metadata = document.get("metadata")
        if (
            not isinstance(api_version, str)
            or not isinstance(kind, str)
            or not isinstance(metadata, dict)
        ):
            raise AssuranceError("rendered resource identity missing")
        gvk = f"{api_version}:{kind}"
        if not GVK_PATTERN.fullmatch(gvk) or not isinstance(metadata.get("name"), str):
            raise AssuranceError("rendered resource identity invalid")
        namespace = metadata.get("namespace", "")
        if not isinstance(namespace, str):
            raise AssuranceError("rendered resource namespace invalid")
        identity = (gvk, namespace, metadata["name"])
        if identity in seen:
            raise AssuranceError("duplicate rendered resource")
        seen.add(identity)
    return documents


def _raw_identity_index(
    root: Path, relative: Path
) -> dict[tuple[str, str, str], dict[str, Any]]:
    """Index unchanged roots under the strict resources-only Kustomization contract."""
    check_kustomization(root, relative)
    documents: dict[tuple[str, str, str], dict[str, Any]] = {}
    for path in sorted(_root_dependencies(root, relative)):
        if path.name == "kustomization.yaml" or path.suffix not in {".yaml", ".yml"}:
            continue
        try:
            parsed = list(
                yaml.load_all(_read_regular(path, 2_000_000), Loader=UniqueSafeLoader)
            )
        except (yaml.YAMLError, UnicodeError) as exc:
            raise AssuranceError("malformed unchanged manifest") from exc
        if not parsed:
            raise AssuranceError("empty unchanged manifest")
        for document in parsed:
            if not isinstance(document, dict) or document.get("kind") == "List":
                raise AssuranceError("unsupported unchanged manifest")
            api_version, kind = document.get("apiVersion"), document.get("kind")
            metadata = document.get("metadata")
            if (
                not isinstance(api_version, str)
                or not isinstance(kind, str)
                or not isinstance(metadata, dict)
                or not isinstance(metadata.get("name"), str)
            ):
                raise AssuranceError("unchanged manifest identity missing")
            gvk = f"{api_version}:{kind}"
            namespace = metadata.get("namespace", "")
            if not GVK_PATTERN.fullmatch(gvk) or not isinstance(namespace, str):
                raise AssuranceError("unchanged manifest identity invalid")
            identity = (gvk, namespace, metadata["name"])
            if identity in documents:
                raise AssuranceError("duplicate unchanged rendered resource")
            documents[identity] = document
    return documents


def validate_project_scope(
    rendered: dict[str, list[dict[str, Any]]],
    repository_roots: set[str] | None = None,
) -> set[str]:
    """Check rendered repository roots against their declared Argo project pairs."""

    roots = set(rendered) if repository_roots is None else repository_roots
    projects: dict[str, tuple[set[tuple[str, str]], set[tuple[str, str]]]] = {}
    assignments: dict[str, str] = {}
    failed: set[str] = set()

    def whitelist(value: Any) -> set[tuple[str, str]]:
        if not isinstance(value, list):
            raise AssuranceError("invalid AppProject whitelist")
        pairs = set()
        for item in value:
            if not isinstance(item, dict) or set(item) != {"group", "kind"}:
                raise AssuranceError("invalid AppProject resource pair")
            group, kind = item["group"], item["kind"]
            if (
                not isinstance(group, str)
                or not isinstance(kind, str)
                or "*" in (group, kind)
            ):
                raise AssuranceError("unsupported AppProject resource pair")
            pairs.add((group, kind))
        return pairs

    for root, documents in rendered.items():
        for doc in documents:
            if (
                doc.get("apiVersion") == "argoproj.io/v1alpha1"
                and doc.get("kind") in {"AppProject", "Application", "ApplicationSet"}
                and doc["metadata"].get("namespace") != "argocd"
            ):
                failed.add(root)
                continue
            if (
                doc.get("apiVersion") == "argoproj.io/v1alpha1"
                and doc.get("kind") == "AppProject"
            ):
                try:
                    name = doc["metadata"]["name"]
                    spec = doc["spec"]
                    pair = (
                        whitelist(spec["clusterResourceWhitelist"]),
                        whitelist(spec["namespaceResourceWhitelist"]),
                    )
                    if name in projects and projects[name] != pair:
                        raise AssuranceError("conflicting AppProject whitelist")
                    projects[name] = pair
                except (AttributeError, KeyError, TypeError, AssuranceError):
                    failed.add(root)
            if (
                doc.get("apiVersion") != "argoproj.io/v1alpha1"
                or doc.get("kind") != "Application"
            ):
                continue
            try:
                spec = doc["spec"]
                if "sources" in spec:
                    raise AssuranceError("unsupported Application sources")
                source = spec["source"]
                if not isinstance(source, dict) or not source:
                    raise AssuranceError("invalid Application source")
                if "path" not in source:
                    if not {"chart", "repoURL", "targetRevision"} <= set(
                        source
                    ) or not set(source) <= {
                        "chart",
                        "repoURL",
                        "targetRevision",
                        "helm",
                    }:
                        raise AssuranceError("unsupported Helm source")
                    if any(
                        not isinstance(source[key], str) or not source[key]
                        for key in ("chart", "repoURL", "targetRevision")
                    ):
                        raise AssuranceError("incomplete Helm source")
                    continue  # The separate chart-kind validator owns Helm output.
                if set(source) != {"path", "repoURL", "targetRevision"}:
                    raise AssuranceError("unsupported local source options")
                path = source["path"]
                project = spec["project"]
                if not isinstance(path, str) or not isinstance(project, str):
                    raise AssuranceError("invalid Application project path")
                if (
                    source.get("repoURL") != SOURCE_REPO
                    or source.get("targetRevision") != SOURCE_REVISION
                ):
                    failed.add(root)
                    continue
                if path not in roots:
                    failed.add(root)
                    continue
                previous = assignments.setdefault(path, project)
                if previous != project:
                    failed.add(path)
            except (AttributeError, KeyError, TypeError, AssuranceError):
                failed.add(root)

    for root, documents in rendered.items():
        for doc in documents:
            if (
                doc.get("apiVersion") != "argoproj.io/v1alpha1"
                or doc.get("kind") != "ApplicationSet"
            ):
                continue
            if doc["metadata"].get("namespace") != "argocd":
                failed.add(root)
                continue
            try:
                spec = doc["spec"]
                template = spec["template"]["spec"]
                generators = spec["generators"]
                if "sources" in template or set(template["source"]) != {
                    "path",
                    "repoURL",
                    "targetRevision",
                }:
                    raise AssuranceError("unsupported workload source shape")
                if template["source"]["path"] != "{{path}}" or len(generators) != 1:
                    raise AssuranceError("unsupported workload generator")
                git = generators[0]["git"]
                directories = git["directories"]
                if directories != [{"path": "gitops/workloads/*"}]:
                    raise AssuranceError("unsupported workload directory selector")
                if (
                    git.get("repoURL") != SOURCE_REPO
                    or git.get("revision") != SOURCE_REVISION
                    or template["source"].get("repoURL") != SOURCE_REPO
                    or template["source"].get("targetRevision") != SOURCE_REVISION
                ):
                    raise AssuranceError("workload generator source differs")
                project = template["project"]
                if not isinstance(project, str):
                    raise AssuranceError("invalid workload project")
                for path in roots:
                    if (
                        path.startswith("gitops/workloads/")
                        and len(PurePosixPath(path).parts) == 3
                    ):
                        previous = assignments.setdefault(path, project)
                        if previous != project:
                            failed.add(path)
            except (AttributeError, KeyError, TypeError, IndexError, AssuranceError):
                failed.add(root)

    for root, documents in rendered.items():
        project = projects.get(assignments.get(root, ""))
        if project is None:
            failed.add(root)
            continue
        cluster_pairs, namespace_pairs = project
        for doc in documents:
            api_version, kind = doc["apiVersion"], doc["kind"]
            group = api_version.split("/", 1)[0] if "/" in api_version else ""
            pair = (group, kind)
            allowed = cluster_pairs if pair in CLUSTER_KINDS else namespace_pairs
            if pair not in allowed:
                failed.add(root)
    return failed


def run(
    root: Path, binary: Path, changed_paths: list[str] | None = None
) -> list[dict[str, str]]:
    if changed_paths == []:
        if root.is_symlink() or not root.is_dir():
            raise AssuranceError("repository root unavailable")
        return []
    validate_manifest_candidates(root)
    all_roots = discover_roots(root)
    roots = all_roots if changed_paths is None else affected_roots(root, changed_paths)
    scoped = len(roots) < len(all_roots)
    rows: list[dict[str, str]] = []
    tool_ready = _tool_is_pinned(binary)
    all_documents: dict[tuple[str, str, str], dict[str, Any]] = {}
    identity_roots: dict[tuple[str, str, str], set[str]] = {}
    rendered_by_root: dict[str, list[dict[str, Any]]] = {}
    all_rendered = tool_ready
    conflicting_roots: set[str] = set()
    for relative in roots:
        target = relative.as_posix()
        rows.append(
            _row(target, "syntax", "none", "none", "pre-commit-check-yaml", "DEFER")
        )
        rows.append(
            _row(
                target,
                "live-observation",
                "none",
                "none",
                "operator-live-check",
                "DEFER",
            )
        )
        if not tool_ready:
            rows.append(
                _row(target, "render", "kustomize", KUSTOMIZE_VERSION, "none", "FAIL")
            )
            all_rendered = False
            continue
        try:
            documents = _render(root, relative, binary)
        except (AssuranceError, OSError, subprocess.TimeoutExpired):
            rows.append(
                _row(target, "render", "kustomize", KUSTOMIZE_VERSION, "none", "FAIL")
            )
            all_rendered = False
            continue
        rows.append(
            _row(target, "render", "kustomize", KUSTOMIZE_VERSION, "none", "PASS")
        )
        rendered_by_root[target] = documents
        grouped: dict[str, list[dict[str, Any]]] = {}
        for document in documents:
            gvk = f"{document['apiVersion']}:{document['kind']}"
            grouped.setdefault(gvk, []).append(document)
            if relative.parts[0] == "gitops":
                metadata = document["metadata"]
                identity = (gvk, metadata.get("namespace", ""), metadata["name"])
                previous = all_documents.get(identity)
                if previous is not None and previous != document:
                    all_rendered = False
                    conflicting_roots.update(identity_roots[identity])
                    conflicting_roots.add(target)
                all_documents[identity] = document
                identity_roots.setdefault(identity, set()).add(target)
        for gvk, entries in sorted(grouped.items()):
            row_target = f"{target}#{gvk}"
            classification = schema_class(gvk)
            if classification == "DEFER":
                rows.append(
                    _row(
                        row_target,
                        "schema-policy",
                        "none",
                        "none",
                        "external-crd-schema-unavailable",
                        "DEFER",
                    )
                )
            elif classification == "FAIL":
                rows.append(
                    _row(row_target, "schema-policy", "none", "none", "none", "FAIL")
                )
            else:
                try:
                    schema = load_schema(SCHEMA_DIR, gvk)
                    failed = any(schema_findings(schema, entry) for entry in entries)
                except AssuranceError:
                    failed = True
                rows.append(
                    _row(
                        row_target,
                        "schema-policy",
                        "jsonschema",
                        f"{version('jsonschema')}+k8s1.35.0",
                        "none",
                        "FAIL" if failed else "PASS",
                    )
                )
    if scoped and tool_ready:
        unchanged: dict[tuple[str, str, str], dict[str, Any]] = {}
        for relative in sorted(set(all_roots) - set(roots)):
            if relative.parts[0] != "gitops":
                continue
            for identity, document in _raw_identity_index(root, relative).items():
                previous = unchanged.get(identity)
                if previous is not None and previous != document:
                    raise AssuranceError("conflicting unchanged GitOps identity")
                unchanged[identity] = document
                selected = all_documents.get(identity)
                if selected is not None and selected != document:
                    all_rendered = False
                    conflicting_roots.update(identity_roots[identity])
    project_failed: set[str] = set()
    ingress_failed = False
    if scoped and all_rendered:
        for control in sorted(PROJECT_CONTROL_ROOTS & set(all_roots) - set(roots)):
            try:
                rendered_by_root[control.as_posix()] = _render(root, control, binary)
            except (AssuranceError, OSError, subprocess.TimeoutExpired):
                all_rendered = False
    if all_rendered:
        project_failed = validate_project_scope(
            {
                name: docs
                for name, docs in rendered_by_root.items()
                if name.startswith("gitops/")
            },
            {relative.as_posix() for relative in all_roots},
        )
        if not scoped or set(roots) >= (INGRESS_CONSUMER_ROOTS & set(all_roots)):
            ingress_failed = bool(validate_ingress(root, list(all_documents.values())))
    for relative in roots:
        target = relative.as_posix()
        if target not in rendered_by_root:
            continue
        if (
            target in conflicting_roots
            or target in project_failed
            or (target == "gitops/platform/ingress-routes" and ingress_failed)
        ):
            rows.append(
                _row(
                    target,
                    "product-semantic",
                    "python3",
                    platform.python_version(),
                    "none",
                    "FAIL",
                )
            )
        elif target.startswith("gitops/") and all_rendered:
            rows.append(
                _row(
                    target,
                    "product-semantic",
                    "python3",
                    platform.python_version(),
                    "none",
                    "PASS",
                )
            )
        elif target.startswith("examples/"):
            rows.append(
                _row(
                    target,
                    "product-semantic",
                    "none",
                    "none",
                    "not-applicable",
                    "NOT_APPLICABLE",
                )
            )
        else:
            rows.append(
                _row(
                    target,
                    "product-semantic",
                    "none",
                    "none",
                    "separate-required-gate",
                    "DEFER",
                )
            )
    if len(rows) > 256:
        raise AssuranceError("platform evidence row limit exceeded")
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--changed-path", action="append", default=None)
    parser.add_argument("--manifest-paths", action="store_true")
    parser.add_argument("--policy-targets", action="store_true")
    args = parser.parse_args()
    if args.policy_targets and not args.manifest_paths:
        parser.error("--policy-targets requires --manifest-paths")
    if args.manifest_paths:
        try:
            paths = manifest_paths(
                Path(args.root).absolute(),
                args.changed_path,
                policy=args.policy_targets,
            )
        except AssuranceError as exc:
            print(f"manifest path selection failed: {exc}", file=sys.stderr)
            return 1
        except OSError:
            print("manifest path selection failed: filesystem error", file=sys.stderr)
            return 1
        sys.stdout.buffer.write(
            b"".join(os.fsencode(path.as_posix()) + b"\0" for path in paths)
        )
        return 0
    binary_name = shutil.which("kustomize")
    try:
        rows = run(
            Path(args.root).resolve(),
            Path(binary_name) if binary_name else Path("/nonexistent/kustomize"),
            args.changed_path,
        )
    except (AssuranceError, OSError):
        print("platform assurance internal failure", file=sys.stderr)
        return 1
    sys.stdout.write(
        json.dumps({"version": 2, "results": rows}, separators=(",", ":")) + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
