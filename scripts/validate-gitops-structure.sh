#!/usr/bin/env bash
# validate-gitops-structure.sh — verify ArgoCD GitOps structural invariants
# Idempotent: safe to run multiple times.
# Usage: bash scripts/validate-gitops-structure.sh
set -euo pipefail

if [[ "$#" -ne 0 ]]; then
  echo "ERR unexpected argument(s): $*" >&2
  echo "Usage: bash scripts/validate-gitops-structure.sh" >&2
  exit 2
fi

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXIT_CODE=0

if ! command -v python3 &>/dev/null; then
  echo "ERR python3 is required for YAML structure validation" >&2
  exit 1
fi

if ! python3 -c 'import yaml' &>/dev/null; then
  echo "ERR python3 PyYAML package is required for YAML structure validation" >&2
  exit 1
fi

yaml_kind() {
  python3 -c 'import sys, yaml
docs = [d for d in yaml.safe_load_all(open(sys.argv[1])) if isinstance(d, dict)]
print(docs[0].get("kind", "UNKNOWN") if docs else "EMPTY")' "$1" 2>/dev/null || echo "PARSE_ERR"
}

echo "=== validate-gitops-structure ==="

# 1. Root application must exist
ROOT_APP="${PROJECT_DIR}/gitops/clusters/local/root-application.yaml"
if [[ -f "$ROOT_APP" ]]; then
  echo "  OK  root-application.yaml exists"
  ROOT_KIND="$(yaml_kind "$ROOT_APP")"
  if [[ "$ROOT_KIND" == "Application" ]]; then
    echo "  OK  root-application.yaml kind is Application"
  else
    echo "  ERR root-application.yaml kind mismatch: $ROOT_KIND"
    EXIT_CODE=1
  fi
else
  echo "  ERR root-application.yaml MISSING: $ROOT_APP"
  EXIT_CODE=1
fi

# 2. Every gitops/apps/root/*.yaml must be a valid ArgoCD Application or ApplicationSet
echo ""
echo "--- ArgoCD Application kind check ---"
shopt -s nullglob
ROOT_APP_MANIFEST_COUNT=0
for f in "${PROJECT_DIR}/gitops/apps/root/"*.yaml; do
  BASENAME="$(basename "$f")"
  KIND="$(yaml_kind "$f")"
  if [[ "$BASENAME" != "kustomization.yaml" && "$KIND" =~ ^(Application|ApplicationSet|AppProject)$ ]]; then
    ROOT_APP_MANIFEST_COUNT=$((ROOT_APP_MANIFEST_COUNT + 1))
  fi
  if [[ "$KIND" =~ ^(Application|ApplicationSet|AppProject|Kustomization)$ ]]; then
    echo "  OK  $KIND — $BASENAME"
  else
    echo "  ERR unexpected kind '$KIND' in $BASENAME"
    EXIT_CODE=1
  fi
done
shopt -u nullglob
if [[ "$ROOT_APP_MANIFEST_COUNT" -gt 0 ]]; then
  echo "  OK  root app manifest count: $ROOT_APP_MANIFEST_COUNT"
else
  echo "  ERR no non-kustomization ArgoCD root app manifests found in gitops/apps/root"
  EXIT_CODE=1
fi

# 3. Root app, platform app, and workload ApplicationSet hierarchy must stay separated.
echo ""
echo "--- GitOps hierarchy contract check ---"
if python3 - "$PROJECT_DIR" <<'PY'
import pathlib
import sys

import yaml

root = pathlib.Path(sys.argv[1])
errors: list[str] = []


def load_one(path: pathlib.Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        docs = [doc for doc in yaml.safe_load_all(handle) if isinstance(doc, dict)]
    return docs[0] if docs else {}


def get(data: dict, dotted_path: str):
    current = data
    for part in dotted_path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def expect(path: pathlib.Path, data: dict, dotted_path: str, expected) -> None:
    actual = get(data, dotted_path)
    if actual != expected:
        errors.append(
            f"{path}: {dotted_path} must be {expected!r}, found {actual!r}"
        )


clusters_local = root / "gitops/clusters/local"
root_app_path = clusters_local / "root-application.yaml"
root_app = load_one(root_app_path)
expect(root_app_path, root_app, "kind", "Application")
expect(root_app_path, root_app, "metadata.name", "root-platform")
expect(root_app_path, root_app, "metadata.namespace", "argocd")
expect(root_app_path, root_app, "spec.project", "platform")
expect(root_app_path, root_app, "spec.source.path", "gitops/apps/root")
expect(root_app_path, root_app, "spec.destination.namespace", "argocd")

appset_path = clusters_local / "applicationset-apps.yaml"
appset = load_one(appset_path)
expect(appset_path, appset, "kind", "ApplicationSet")
expect(appset_path, appset, "metadata.name", "apps-generator")
expect(appset_path, appset, "metadata.namespace", "argocd")
expect(appset_path, appset, "spec.template.spec.project", "apps")
expect(appset_path, appset, "spec.template.spec.source.path", "{{path}}")
expect(appset_path, appset, "spec.template.spec.destination.namespace", "apps")

directories = []
for generator in get(appset, "spec.generators") or []:
    git_generator = generator.get("git") if isinstance(generator, dict) else None
    if not isinstance(git_generator, dict):
        continue
    for directory in git_generator.get("directories") or []:
        if isinstance(directory, dict) and "path" in directory:
            directories.append(directory["path"])
if directories != ["gitops/workloads/*"]:
    errors.append(
        f"{appset_path}: git directory generator must be ['gitops/workloads/*'], "
        f"found {directories!r}"
    )

cluster_kustomization = load_one(clusters_local / "kustomization.yaml")
cluster_resources = set(cluster_kustomization.get("resources") or [])
required_cluster_resources = {
    "root-application.yaml",
    "appproject-platform.yaml",
    "appproject-apps.yaml",
    "applicationset-apps.yaml",
}
missing_cluster_resources = sorted(required_cluster_resources - cluster_resources)
if missing_cluster_resources:
    errors.append(
        f"{clusters_local / 'kustomization.yaml'}: missing required cluster overlay resources: "
        + ", ".join(missing_cluster_resources)
    )

root_apps_dir = root / "gitops/apps/root"
allowed_local_prefixes = ("gitops/platform/", "gitops/clusters/local")
for application_path in sorted(root_apps_dir.glob("*.yaml")):
    if application_path.name == "kustomization.yaml":
        continue
    application = load_one(application_path)
    if application.get("kind") != "Application":
        errors.append(f"{application_path}: root app manifest must be kind Application")
        continue
    if get(application, "spec.project") != "platform":
        errors.append(f"{application_path}: root app manifest must use project 'platform'")
    source_path = get(application, "spec.source.path")
    if source_path and not source_path.startswith(allowed_local_prefixes):
        errors.append(
            f"{application_path}: local source path must stay under gitops/platform/ "
            f"or gitops/clusters/local, found {source_path!r}"
        )

if errors:
    for error in errors:
        print(f"  ERR {error}")
    sys.exit(1)

print("  OK  root Application owns gitops/apps/root")
print("  OK  apps ApplicationSet owns gitops/workloads/*")
print("  OK  root app manifests stay in platform project and allowed local source paths")
PY
then
  :
else
  EXIT_CODE=1
fi

# 4. All kustomization.yaml files must be parseable
echo ""
echo "--- Kustomization syntax check ---"
while IFS= read -r -d '' k; do
  if python3 -c 'import sys, yaml; yaml.safe_load(open(sys.argv[1]))' "$k" 2>&1; then
    echo "  OK  $k"
  else
    echo "  ERR $k"
    EXIT_CODE=1
  fi
done < <(find "${PROJECT_DIR}/gitops" -name "kustomization.yaml" -print0)

# 5. Sibling manifest files must be referenced by their kustomization.yaml.
echo ""
echo "--- Kustomization resource completeness check ---"
if python3 - "$PROJECT_DIR" <<'PY'
import pathlib
import sys

import yaml

root = pathlib.Path(sys.argv[1])
errors = 0

for kustomization in sorted((root / "gitops").rglob("kustomization.yaml")):
    try:
        data = yaml.safe_load(kustomization.read_text(encoding="utf-8")) or {}
    except Exception as exc:
        print(f"  ERR {kustomization}: {exc}")
        errors += 1
        continue

    resources = data.get("resources") or []
    if not isinstance(resources, list):
        print(f"  ERR {kustomization}: resources must be a list")
        errors += 1
        continue

    referenced = {
        item.strip().removeprefix("./")
        for item in resources
        if isinstance(item, str) and item.strip()
    }
    sibling_manifests = sorted(
        path.name
        for path in kustomization.parent.iterdir()
        if path.is_file()
        and path.name != "kustomization.yaml"
        and path.suffix in {".yaml", ".yml"}
    )
    missing = [name for name in sibling_manifests if name not in referenced]
    if missing:
        print(
            f"  ERR {kustomization}: unreferenced sibling manifest(s): "
            + ", ".join(missing)
        )
        errors += 1
    else:
        print(f"  OK  {kustomization}")

sys.exit(1 if errors else 0)
PY
then
  :
else
  EXIT_CODE=1
fi

echo ""
echo "=== done (exit: $EXIT_CODE) ==="
exit $EXIT_CODE
