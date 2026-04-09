#!/usr/bin/env bash
# check-secret-handling.sh — scan for plaintext secret patterns in manifests
# Idempotent: safe to run multiple times.
# Usage: bash scripts/check-secret-handling.sh [path]
# Exit 0 = clean. Exit 1 = plaintext secrets found.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="${1:-${PROJECT_DIR}}"
EXIT_CODE=0

echo "=== check-secret-handling ==="
echo "Target : $TARGET"

# Patterns that indicate plaintext secrets in k8s manifests
# Excludes: {template}, <placeholder>, $variable (ArgoCD/Helm refs), empty values
DANGEROUS_PATTERNS=(
  'stringData:$'
  'password: [^{<$"]'
  'token: [^{<$"]'
  'apiKey: [^{<$"]'
  'privateKey: [^{<$"]'
  'secret: [^{<$"]'
)

echo ""
echo "--- scanning for plaintext secret patterns ---"
FOUND=0
for pat in "${DANGEROUS_PATTERNS[@]}"; do
  while IFS= read -r match; do
    # Skip ExternalSecret, SealedSecret, and comment lines
    FILE=$(echo "$match" | cut -d: -f1)
    KIND=$(python3 -c "
import yaml, sys
try:
  docs = list(yaml.safe_load_all(open('$FILE')))
  print(docs[0].get('kind','') if docs else '')
except Exception:
  print('')
" 2>/dev/null || echo "")
    if [[ "$KIND" =~ ^(ExternalSecret|SealedSecret|SecretStore|ClusterSecretStore)$ ]]; then
      continue
    fi
    echo "  WARN $match"
    FOUND=1
  done < <(grep -rn --include="*.yaml" --include="*.yml" -E "$pat" "$TARGET/gitops" "$TARGET/infrastructure" 2>/dev/null | grep -v "^.*#" || true)
done

if [[ $FOUND -eq 0 ]]; then
  echo "  OK  no plaintext secret patterns found"
else
  echo ""
  echo "  ERR plaintext secrets detected — review findings above"
  EXIT_CODE=1
fi

echo ""
echo "=== done (exit: $EXIT_CODE) ==="
exit $EXIT_CODE
