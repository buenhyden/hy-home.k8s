#!/usr/bin/env bash
# validate-gitops-structure.sh — verify ArgoCD GitOps structural invariants
# Idempotent: safe to run multiple times.
# Usage: bash scripts/validate-gitops-structure.sh
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EXIT_CODE=0

echo "=== validate-gitops-structure ==="

# 1. Root application must exist
ROOT_APP="${PROJECT_DIR}/gitops/clusters/local/root-application.yaml"
if [[ -f "$ROOT_APP" ]]; then
  echo "  OK  root-application.yaml exists"
else
  echo "  ERR root-application.yaml MISSING: $ROOT_APP"
  EXIT_CODE=1
fi

# 2. Every gitops/apps/root/*.yaml must be a valid ArgoCD Application or ApplicationSet
echo ""
echo "--- ArgoCD Application kind check ---"
for f in "${PROJECT_DIR}/gitops/apps/root/"*.yaml; do
  KIND=$(python3 -c "import yaml; d=list(yaml.safe_load_all(open('$f'))); print(d[0].get('kind','UNKNOWN') if d else 'EMPTY')" 2>/dev/null || echo "PARSE_ERR")
  if [[ "$KIND" =~ ^(Application|ApplicationSet|AppProject|Kustomization)$ ]]; then
    echo "  OK  $KIND — $(basename "$f")"
  else
    echo "  WARN unexpected kind '$KIND' in $(basename "$f")"
  fi
done

# 3. All kustomization.yaml files must be parseable
echo ""
echo "--- Kustomization syntax check ---"
find "${PROJECT_DIR}/gitops" -name "kustomization.yaml" | while read -r k; do
  if python3 -c "import yaml; yaml.safe_load(open('$k'))" 2>&1; then
    echo "  OK  $k"
  else
    echo "  ERR $k"; EXIT_CODE=1
  fi
done

echo ""
echo "=== done (exit: $EXIT_CODE) ==="
exit $EXIT_CODE
