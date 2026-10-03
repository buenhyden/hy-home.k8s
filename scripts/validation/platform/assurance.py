#!/usr/bin/env python3
"""Offline, pinned render and built-in API schema evidence for local GitOps roots."""

from __future__ import annotations

import argparse
import hashlib
from importlib.metadata import version
import json
from pathlib import Path, PurePosixPath
import platform
import re
import shutil
import subprocess
import sys
from typing import Any

import yaml

from ingress import validate as validate_ingress


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
    ("rbac.authorization.k8s.io", "ClusterRole"),
    ("rbac.authorization.k8s.io", "ClusterRoleBinding"),
}
GVK_PATTERN = re.compile(
    r"^[a-z0-9.-]+(?:/v[0-9]+(?:alpha|beta)?[0-9]*)?:[A-Z][A-Za-z0-9]*$"
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


def _local_path(root: Path, base: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or ":" in value or "\\" in value:
        raise AssuranceError("nonlocal resource reference")
    candidate = PurePosixPath(value)
    if candidate.is_absolute() or any(part in (".", "..") for part in candidate.parts):
        raise AssuranceError("unsafe resource path")
    path = base.joinpath(*candidate.parts)
    if not path.is_relative_to(root):
        raise AssuranceError("resource escapes repository")
    for member in (path, *path.parents):
        if member == root.parent:
            break
        if member.is_symlink():
            raise AssuranceError("linked resource path")
    if not path.is_relative_to(base):
        raise AssuranceError("resource escapes Kustomize root")
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


def validate_project_scope(rendered: dict[str, list[dict[str, Any]]]) -> set[str]:
    """Check rendered repository roots against their declared Argo project pairs."""

    roots = set(rendered)
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


def run(root: Path, binary: Path) -> list[dict[str, str]]:
    roots = discover_roots(root)
    rows: list[dict[str, str]] = []
    tool_ready = _tool_is_pinned(binary)
    all_documents: dict[tuple[str, str, str], dict[str, Any]] = {}
    rendered_by_root: dict[str, list[dict[str, Any]]] = {}
    all_rendered = tool_ready
    conflicting_roots: set[str] = set()
    for relative in roots:
        target = relative.as_posix()
        rows.append(
            _row(target, "syntax", "none", "none", "separate-required-gate", "DEFER")
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
                    conflicting_roots.add(target)
                all_documents[identity] = document
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
    project_failed: set[str] = set()
    ingress_failed = False
    if all_rendered:
        project_failed = validate_project_scope(
            {
                name: docs
                for name, docs in rendered_by_root.items()
                if name.startswith("gitops/")
            }
        )
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
                    target, "product-semantic", "none", "none", "not-applicable", "SKIP"
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
    args = parser.parse_args()
    binary_name = shutil.which("kustomize")
    try:
        rows = run(
            Path(args.root).resolve(),
            Path(binary_name) if binary_name else Path("/nonexistent/kustomize"),
        )
    except (AssuranceError, OSError):
        print("platform assurance internal failure", file=sys.stderr)
        return 1
    sys.stdout.write(
        json.dumps({"version": 1, "results": rows}, separators=(",", ":")) + "\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
