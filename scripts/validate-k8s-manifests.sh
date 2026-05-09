#!/usr/bin/env bash
# validate-k8s-manifests.sh — kube-linter + YAML syntax check on gitops/ and infrastructure/
# Idempotent: safe to run multiple times.
# Usage: bash scripts/validate-k8s-manifests.sh [repo-root]
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_INPUT="${1:-${PROJECT_DIR}}"
CONFIG="${PROJECT_DIR}/.kube-linter.yaml"
EXIT_CODE=0

if [[ ! -d "$TARGET_INPUT" ]]; then
  echo "ERR repo root does not exist: $TARGET_INPUT" >&2
  exit 1
fi

TARGET="$(cd "$TARGET_INPUT" && pwd)"

for required_dir in gitops infrastructure; do
  if [[ ! -d "$TARGET/$required_dir" ]]; then
    echo "ERR expected repo root at $TARGET_INPUT; missing $required_dir/ under that root" >&2
    echo "Usage: bash scripts/validate-k8s-manifests.sh [repo-root]" >&2
    exit 1
  fi
done

if ! command -v python3 &>/dev/null; then
  echo "ERR python3 is required for YAML syntax validation" >&2
  exit 1
fi

if ! python3 -c 'import yaml' &>/dev/null; then
  echo "ERR python3 PyYAML package is required for YAML syntax validation" >&2
  exit 1
fi

declare -a YAML_TARGETS=(
  "$TARGET/gitops"
  "$TARGET/infrastructure"
)

for optional_dir in "$TARGET/examples/sample-app" "$TARGET/traefik"; do
  if [[ -d "$optional_dir" ]]; then
    YAML_TARGETS+=("$optional_dir")
  fi
done

if [[ -d "$TARGET/examples" ]]; then
  while IFS= read -r path; do
    YAML_TARGETS+=("$path")
  done < <(find "$TARGET/examples" -type d -path '*/kubernetes' 2>/dev/null)

  while IFS= read -r path; do
    YAML_TARGETS+=("$path")
  done < <(find "$TARGET/examples" -type d -path '*/gitops' 2>/dev/null)
fi

mapfile -d '' YAML_FILES < <(find "${YAML_TARGETS[@]}" \( -name "*.yaml" -o -name "*.yml" \) -print0 2>/dev/null)

if [[ "${#YAML_FILES[@]}" -eq 0 ]]; then
  echo "ERR no YAML manifests matched under repo root: $TARGET" >&2
  exit 1
fi

echo "=== validate-k8s-manifests ==="
echo "Target : $TARGET"
echo "Config : $CONFIG"
echo "Files  : ${#YAML_FILES[@]}"

# YAML syntax check via python
echo ""
echo "--- YAML syntax check ---"
for f in "${YAML_FILES[@]}"; do
  if python3 -c 'import sys, yaml; list(yaml.safe_load_all(open(sys.argv[1])))' "$f" 2>&1; then
    echo "  OK  $f"
  else
    echo "  ERR $f"
    EXIT_CODE=1
  fi
done

# kube-linter
echo ""
echo "--- kube-linter ---"
if command -v kube-linter &>/dev/null; then
  kube-linter lint "${YAML_TARGETS[@]}" --config "$CONFIG" || EXIT_CODE=1
else
  echo "  SKIP optional kube-linter not installed — YAML syntax validation only"
fi

echo ""
echo "=== done (exit: $EXIT_CODE) ==="
exit $EXIT_CODE
