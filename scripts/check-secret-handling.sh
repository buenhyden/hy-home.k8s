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

echo ""
echo "--- scanning for plaintext secret patterns ---"
if SCAN_TARGET="$TARGET" python3 - "${SECRET_SCAN_FILES[@]}" <<'PY'
import os
import re
import sys
import yaml

target = os.environ["SCAN_TARGET"]
excluded_kinds = {"ExternalSecret", "SealedSecret", "SecretStore", "ClusterSecretStore"}
sensitive_keys = {"password", "token", "apiKey", "privateKey", "secret"}
key_line = re.compile(r"^\s*-?\s*([A-Za-z0-9_.-]+)\s*:\s*(.*)$")
findings = []


def load_kinds(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            docs = [doc for doc in yaml.safe_load_all(handle) if isinstance(doc, dict)]
    except Exception:
        return []
    return [str(doc.get("kind", "")) for doc in docs if doc.get("kind")]


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1].strip()
    return value


def strip_inline_comment(value):
    in_single = False
    in_double = False
    for idx, char in enumerate(value):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return value[:idx].rstrip()
    return value


def allowed_placeholder(value):
    normalized = unquote(value)
    if not normalized or normalized.lower() in {"null", "~"}:
        return True
    if normalized in {"{}", "[]"}:
        return True
    return normalized.startswith(("{", "<", "$"))


for path in sys.argv[1:]:
    kinds = load_kinds(path)
    if kinds and all(kind in excluded_kinds for kind in kinds):
        continue

    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError:
        continue

    display_kind = ",".join(kinds) if kinds else "Unknown"
    for line_no, line in enumerate(lines, start=1):
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue

        match = key_line.match(line)
        if not match:
            continue

        key, raw_value = match.groups()
        if key == "stringData":
            rel = os.path.relpath(path, target)
            findings.append((rel, line_no, display_kind, key))
            continue

        if key not in sensitive_keys:
            continue

        raw_value = strip_inline_comment(raw_value.strip()).strip()
        if raw_value.startswith("#") or allowed_placeholder(raw_value):
            continue

        rel = os.path.relpath(path, target)
        findings.append((rel, line_no, display_kind, key))

for rel, line_no, kind, key in findings:
    print(f"  WARN {rel}:{line_no} kind={kind} key={key} value=<redacted>")

sys.exit(1 if findings else 0)
PY
then
  FOUND=0
else
  FOUND=1
fi

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
