#!/usr/bin/env bash
# check-secret-handling.sh — scan for plaintext secret patterns in manifests
# Idempotent: safe to run multiple times.
# Usage: bash scripts/check-secret-handling.sh [repo-root]
# Exit 0 = clean. Exit 1 = plaintext secrets found.
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_INPUT="${1:-${PROJECT_DIR}}"
EXIT_CODE=0

if [[ ! -d "$TARGET_INPUT" ]]; then
  echo "ERR repo root does not exist: $TARGET_INPUT" >&2
  exit 1
fi

TARGET="$(cd "$TARGET_INPUT" && pwd)"

for required_dir in gitops infrastructure examples; do
  if [[ ! -d "$TARGET/$required_dir" ]]; then
    echo "ERR expected repo root at $TARGET_INPUT; missing $required_dir/ under that root" >&2
    echo "Usage: bash scripts/check-secret-handling.sh [repo-root]" >&2
    exit 1
  fi
done

if ! command -v python3 &>/dev/null; then
  echo "ERR python3 is required for Kubernetes kind detection" >&2
  exit 1
fi

if ! python3 -c 'import yaml' &>/dev/null; then
  echo "ERR python3 PyYAML package is required for Kubernetes kind detection" >&2
  exit 1
fi

echo "=== check-secret-handling ==="
echo "Target : $TARGET"

SECRET_SCAN_ROOTS=()
add_scan_root() {
  local candidate="$1"
  [[ -d "$candidate" ]] || return 0
  local existing
  for existing in "${SECRET_SCAN_ROOTS[@]}"; do
    [[ "$existing" == "$candidate" ]] && return 0
  done
  SECRET_SCAN_ROOTS+=("$candidate")
}

add_scan_root "$TARGET/gitops"
add_scan_root "$TARGET/infrastructure"
add_scan_root "$TARGET/examples/sample-app"
while IFS= read -r -d '' example_dir; do
  add_scan_root "$example_dir"
done < <(find "$TARGET/examples" -type d \( -name "gitops" -o -name "kubernetes" \) -print0 2>/dev/null)

mapfile -d '' SECRET_SCAN_FILES < <(find "${SECRET_SCAN_ROOTS[@]}" \( -name "*.yaml" -o -name "*.yml" \) -print0 2>/dev/null)

if [[ "${#SECRET_SCAN_FILES[@]}" -eq 0 ]]; then
  echo "ERR no YAML manifests matched under repo root: $TARGET" >&2
  exit 1
fi

echo "Files  : ${#SECRET_SCAN_FILES[@]}"

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
    FILE="${match%%:*}"
    REST="${match#*:}"
    LINE_NO="${REST%%:*}"
    MATCH_TEXT="${REST#*:}"
    TRIMMED="${MATCH_TEXT#"${MATCH_TEXT%%[![:space:]]*}"}"
    if [[ "$TRIMMED" == \#* ]]; then
      continue
    fi
    KIND=$(python3 -c 'import sys, yaml
docs = [d for d in yaml.safe_load_all(open(sys.argv[1])) if isinstance(d, dict)]
print(docs[0].get("kind", "") if docs else "")' "$FILE" 2>/dev/null || echo "")
    if [[ "$KIND" =~ ^(ExternalSecret|SealedSecret|SecretStore|ClusterSecretStore)$ ]]; then
      continue
    fi
    KEY=$(printf '%s\n' "$MATCH_TEXT" | sed -E 's/^[[:space:]-]*([A-Za-z0-9_.-]+):.*/\1/')
    if [[ "$KEY" == "$MATCH_TEXT" ]]; then
      KEY="<unknown>"
    fi
    REL_FILE="${FILE#"$TARGET"/}"
    echo "  WARN ${REL_FILE}:${LINE_NO} kind=${KIND:-Unknown} key=${KEY} value=<redacted>"
    FOUND=1
  done < <(grep -rn --include="*.yaml" --include="*.yml" -E "$pat" "${SECRET_SCAN_ROOTS[@]}" 2>/dev/null || true)
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
