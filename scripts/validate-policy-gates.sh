#!/usr/bin/env bash
# validate-policy-gates.sh — run the Conftest deployment-safety policy
# Usage: bash scripts/validate-policy-gates.sh [repo-root]
#
# Conftest is required, not optional. A second built-in implementation of the
# same rules used to run alongside it, which meant the gate could report a
# clean result from an engine that had never evaluated the owning policy.
# `policy/conftest/` is now the only owner of these rules.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEFAULT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

usage() {
  printf 'Usage: bash scripts/validate-policy-gates.sh [repo-root]\n'
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "$#" -gt 1 ]]; then
  echo "ERR unexpected argument(s): $*" >&2
  usage >&2
  exit 2
fi

ROOT_INPUT="${1:-$DEFAULT_ROOT}"
if [[ ! -d "$ROOT_INPUT" ]]; then
  echo "ERR repo root does not exist: $ROOT_INPUT" >&2
  exit 1
fi
ROOT_DIR="$(cd "$ROOT_INPUT" && pwd)"
POLICY_DIR="$ROOT_DIR/policy/conftest"

for required_path in \
  "$ROOT_DIR/gitops" \
  "$ROOT_DIR/infrastructure" \
  "$ROOT_DIR/examples" \
  "$ROOT_DIR/traefik" \
  "$POLICY_DIR"; do
  if [[ ! -e "$required_path" ]]; then
    echo "ERR expected repo root at $ROOT_INPUT; missing ${required_path#"$ROOT_DIR"/}" >&2
    usage >&2
    exit 1
  fi
done

# The validation runner resolves and validates the executable, then names it
# here. A direct invocation falls back to the caller's search path.
CONFTEST="${HY_HOME_K8S_CONFTEST_EXECUTABLE:-}"
if [[ -z "$CONFTEST" ]]; then
  CONFTEST="$(command -v conftest || true)"
fi
if [[ -z "$CONFTEST" || ! -x "$CONFTEST" ]]; then
  echo "ERR conftest is required for policy validation and was not found" >&2
  echo "    install it on the system path or at ~/.local/bin/conftest" >&2
  exit 1
fi

mapfile -d '' POLICY_TARGETS < <(
  find \
    "$ROOT_DIR/gitops" \
    "$ROOT_DIR/infrastructure" \
    "$ROOT_DIR/examples" \
    "$ROOT_DIR/traefik" \
    -type f \( -name '*.yaml' -o -name '*.yml' \) -print0 |
    sort -z
)

if ((${#POLICY_TARGETS[@]} == 0)); then
  echo "ERR no policy target YAML files found" >&2
  exit 1
fi

echo "=== validate-policy-gates ==="
echo "Target : $ROOT_DIR"
echo "Policy : $POLICY_DIR"
echo "Files  : ${#POLICY_TARGETS[@]}"
echo ""

# Prove the rules still fire before trusting a clean manifest result.
echo "--- conftest verify ---"
"$CONFTEST" verify --policy "$POLICY_DIR"

echo ""
echo "--- conftest test ---"
"$CONFTEST" test --policy "$POLICY_DIR" "${POLICY_TARGETS[@]}"

echo ""
echo "=== done (exit: 0) ==="
