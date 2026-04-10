#!/usr/bin/env bash
# k8s-pre-edit.sh — warn before editing k8s manifest files
# Runs at PreToolUse for Write|Edit|MultiEdit. Exits 0 always (non-blocking).
set -euo pipefail

FILE="${CLAUDE_TOOL_INPUT_FILE_PATH:-}"
K8S_MANIFEST_REGEX='(gitops/.*\.ya?ml|infrastructure/.*\.ya?ml|examples/sample-app/.*\.ya?ml|examples/.*/gitops/.*\.ya?ml|examples/.*/kubernetes/.*\.ya?ml|traefik/.*\.ya?ml)$'

if [[ -z "$FILE" ]]; then
  exit 0
fi

# Warn if editing a k8s manifest
if echo "$FILE" | grep -qE "$K8S_MANIFEST_REGEX"; then
  echo "WARNING: Editing k8s manifest: $FILE"
  echo "  - Ensure change is GitOps-First (PR → ArgoCD, no kubectl apply)."
  echo "  - Ensure no plaintext secrets are introduced."
  echo "  - kube-linter will run after save (post-validate hook)."
fi

# Warn if editing a secret-adjacent file
if echo "$FILE" | grep -qiE '(secret|credential|password|token)'; then
  echo "WARNING: File name suggests secrets: $FILE"
  echo "  - Never write plaintext secret values."
  echo "  - Use ExternalSecret / SealedSecret patterns only."
fi

exit 0
