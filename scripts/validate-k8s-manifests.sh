#!/usr/bin/env bash
# validate-k8s-manifests.sh — kube-linter + YAML syntax check on gitops/ and infrastructure/
# Idempotent: safe to run multiple times.
# Usage: bash scripts/validate-k8s-manifests.sh [path]
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-${PROJECT_DIR}}"
CONFIG="${PROJECT_DIR}/.kube-linter.yaml"
EXIT_CODE=0
declare -a YAML_TARGETS=(
  "$TARGET/gitops"
  "$TARGET/infrastructure"
  "$TARGET/examples/sample-app"
  "$TARGET/traefik"
)

while IFS= read -r path; do
  YAML_TARGETS+=("$path")
done < <(find "$TARGET/examples" -type d -path '*/kubernetes' 2>/dev/null)

while IFS= read -r path; do
  YAML_TARGETS+=("$path")
done < <(find "$TARGET/examples" -type d -path '*/gitops' 2>/dev/null)

echo "=== validate-k8s-manifests ==="
echo "Target : $TARGET"
echo "Config : $CONFIG"

# YAML syntax check via python (no external deps)
echo ""
echo "--- YAML syntax check ---"
if command -v python3 &>/dev/null; then
  find "${YAML_TARGETS[@]}" \( -name "*.yaml" -o -name "*.yml" \) 2>/dev/null | \
    while read -r f; do
      if python3 -c "import sys, yaml; yaml.safe_load_all(open('$f'))" 2>&1; then
        echo "  OK  $f"
      else
        echo "  ERR $f"; EXIT_CODE=1
      fi
    done
else
  echo "(python3 not available — skipping YAML syntax check)"
fi

# kube-linter
echo ""
echo "--- kube-linter ---"
if command -v kube-linter &>/dev/null; then
  kube-linter lint "${YAML_TARGETS[@]}" --config "$CONFIG" || EXIT_CODE=1
else
  echo "(kube-linter not installed — skipping)"
fi

echo ""
echo "=== done (exit: $EXIT_CODE) ==="
exit $EXIT_CODE
