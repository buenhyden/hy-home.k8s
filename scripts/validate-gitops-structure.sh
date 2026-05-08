#!/usr/bin/env bash
# validate-gitops-structure.sh — verify ArgoCD GitOps structural invariants
# Idempotent: safe to run multiple times.
# Usage: bash scripts/validate-gitops-structure.sh
set -euo pipefail

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
for f in "${PROJECT_DIR}/gitops/apps/root/"*.yaml; do
  KIND="$(yaml_kind "$f")"
  if [[ "$KIND" =~ ^(Application|ApplicationSet|AppProject|Kustomization)$ ]]; then
    echo "  OK  $KIND — $(basename "$f")"
  else
    echo "  ERR unexpected kind '$KIND' in $(basename "$f")"
    EXIT_CODE=1
  fi
done
shopt -u nullglob

# 3. All kustomization.yaml files must be parseable
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

echo ""
echo "=== done (exit: $EXIT_CODE) ==="
exit $EXIT_CODE
