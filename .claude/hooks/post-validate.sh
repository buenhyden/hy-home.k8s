#!/usr/bin/env bash
# post-validate.sh — kube-linter auto-run on edited manifest files
# Runs at PostToolUse for Write|Edit|MultiEdit. Exits 0 always (non-blocking).
set -euo pipefail

FILE="${CLAUDE_TOOL_INPUT_FILE_PATH:-}"
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
K8S_MANIFEST_REGEX='(gitops/.*\.ya?ml|infrastructure/.*\.ya?ml|examples/sample-app/.*\.ya?ml|examples/.*/gitops/.*\.ya?ml|examples/.*/kubernetes/.*\.ya?ml|traefik/.*\.ya?ml)$'

if [[ -z "$FILE" ]]; then
  exit 0
fi

# Only lint k8s YAML manifests
if ! echo "$FILE" | grep -qE "$K8S_MANIFEST_REGEX"; then
  exit 0
fi

# Run kube-linter if available
if command -v kube-linter &>/dev/null; then
  echo "--- kube-linter: $FILE ---"
  kube-linter lint "$FILE" --config "$PROJECT_DIR/.kube-linter.yaml" 2>&1 || \
    echo "kube-linter reported issues (see above)."
else
  echo "(kube-linter not installed — skipping manifest lint)"
fi

exit 0
