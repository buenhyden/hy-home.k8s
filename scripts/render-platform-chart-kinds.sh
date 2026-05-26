#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

python3 - "$ROOT_DIR" "$TMP_DIR" <<'PY'
import pathlib
import os
import subprocess
import sys

import yaml

root = pathlib.Path(sys.argv[1]).resolve()
tmp_dir = pathlib.Path(sys.argv[2]).resolve()
apps_root = root / "gitops/apps/root"
platform_project_path = root / "gitops/clusters/local/appproject-platform.yaml"
helm_env = os.environ.copy()
helm_env["HELM_CACHE_HOME"] = str(tmp_dir / "helm-cache")
helm_env["HELM_CONFIG_HOME"] = str(tmp_dir / "helm-config")
helm_env["HELM_DATA_HOME"] = str(tmp_dir / "helm-data")
(tmp_dir / "helm-cache").mkdir(parents=True, exist_ok=True)
(tmp_dir / "helm-config").mkdir(parents=True, exist_ok=True)
(tmp_dir / "helm-data").mkdir(parents=True, exist_ok=True)

cluster_scoped_kinds = {
    "APIService",
    "ClusterAnalysisTemplate",
    "ClusterIssuer",
    "ClusterRole",
    "ClusterRoleBinding",
    "CustomResourceDefinition",
    "IngressClass",
    "IPAddressPool",
    "L2Advertisement",
    "MutatingWebhookConfiguration",
    "Namespace",
    "PriorityClass",
    "StorageClass",
    "ValidatingWebhookConfiguration",
}


def load_yaml(path: pathlib.Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def api_group(api_version: str) -> str:
    return "" if "/" not in api_version else api_version.split("/", 1)[0]


platform_project = load_yaml(platform_project_path)
spec = platform_project.get("spec") or {}
cluster_allowed = {
    (item.get("group") or "", item.get("kind") or "")
    for item in spec.get("clusterResourceWhitelist", [])
    if isinstance(item, dict)
}
namespace_allowed = {
    (item.get("group") or "", item.get("kind") or "")
    for item in spec.get("namespaceResourceWhitelist", [])
    if isinstance(item, dict)
}

chart_apps = []
for path in sorted(apps_root.glob("*.yaml")):
    document = load_yaml(path)
    if not isinstance(document, dict) or document.get("kind") != "Application":
        continue
    source = (document.get("spec") or {}).get("source") or {}
    chart = source.get("chart")
    if not chart:
        continue
    metadata = document.get("metadata") or {}
    helm = source.get("helm") or {}
    destination = (document.get("spec") or {}).get("destination") or {}
    chart_apps.append(
        {
            "name": metadata.get("name"),
            "repo": source.get("repoURL"),
            "chart": chart,
            "version": source.get("targetRevision"),
            "release": helm.get("releaseName") or metadata.get("name"),
            "namespace": destination.get("namespace") or "default",
            "values": helm.get("values") or "",
        }
    )

if not chart_apps:
    raise SystemExit("no Helm chart Applications found under gitops/apps/root")

rows = []
violations = []
for app in chart_apps:
    values_path = None
    if app["values"]:
        values_path = tmp_dir / f"{app['name']}-values.yaml"
        values_path.write_text(app["values"], encoding="utf-8")

    command = [
        "helm",
        "template",
        str(app["release"]),
        str(app["chart"]),
        "--repo",
        str(app["repo"]),
        "--version",
        str(app["version"]),
        "--namespace",
        str(app["namespace"]),
        "--include-crds",
    ]
    if values_path is not None:
        command.extend(["-f", str(values_path)])

    result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False, env=helm_env)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        raise SystemExit(result.returncode)

    rendered = []
    for document in yaml.safe_load_all(result.stdout):
        if not isinstance(document, dict):
            continue
        kind = document.get("kind")
        api_version = document.get("apiVersion")
        if not isinstance(kind, str) or not isinstance(api_version, str):
            continue
        group = api_group(api_version)
        rendered.append((group, kind))
        allowed = cluster_allowed if kind in cluster_scoped_kinds else namespace_allowed
        if (group, kind) not in allowed:
            violations.append(f"{app['name']}: {group or 'core'}/{kind}")

    rendered_kinds = ", ".join(
        f"{group + '/' if group else ''}{kind}" for group, kind in sorted(set(rendered))
    )
    rows.append(
        [
            str(app["name"]),
            str(app["chart"]),
            str(app["version"]),
            str(app["namespace"]),
            rendered_kinds,
        ]
    )

print("| Application | Chart | Target revision | Namespace | Rendered apiVersion/kinds |")
print("| --- | --- | --- | --- | --- |")
for row in rows:
    print("| " + " | ".join(row) + " |")

if violations:
    print()
    print("[FAIL] rendered chart kinds missing from platform AppProject:")
    for violation in violations:
        print(f"- {violation}")
    raise SystemExit(1)

print()
print("[PASS] rendered platform chart kinds are covered by the platform AppProject allow-lists")
PY
