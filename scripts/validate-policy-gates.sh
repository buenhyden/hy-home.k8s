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
# Without a host binary, run the same release as CI from its official image,
# pinned by digest, with no network and the repository mounted read-only.
CONFTEST_IMAGE="openpolicyagent/conftest:v0.69.0@sha256:a38ba21668929a00dce2fe6ee43d1312228340bce5fd243f47dd0ce90516e558"
CONFTEST_MODE="binary"
if [[ -z "$CONFTEST" || ! -x "$CONFTEST" ]]; then
  if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
    CONFTEST_MODE="container"
  else
    echo "ERR conftest is required for policy validation and was not found" >&2
    echo "    install it on the system path or at ~/.local/bin/conftest," >&2
    echo "    or make a Docker daemon available to run $CONFTEST_IMAGE" >&2
    exit 1
  fi
fi

run_conftest() {
  if [[ "$CONFTEST_MODE" == "binary" ]]; then
    "$CONFTEST" "$@"
    return
  fi
  docker run --rm --network none --read-only --tmpfs /tmp \
    --user "$(id -u):$(id -g)" \
    -v "$ROOT_DIR:/project:ro" -w /project \
    "$CONFTEST_IMAGE" "$@"
}

mapfile -d '' POLICY_TARGETS < <(
  find \
    "$ROOT_DIR/gitops" \
    "$ROOT_DIR/infrastructure" \
    "$ROOT_DIR/examples" \
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
echo "Engine : conftest ($CONFTEST_MODE)"
echo ""

# Prove the rules still fire before trusting a clean manifest result.
echo "--- conftest verify ---"
if [[ "$CONFTEST_MODE" == "container" ]]; then
  # The container sees the repository at /project, so pass relative paths.
  POLICY_ARG="policy/conftest"
  POLICY_TARGETS=("${POLICY_TARGETS[@]#"$ROOT_DIR"/}")
else
  POLICY_ARG="$POLICY_DIR"
fi
run_conftest verify --policy "$POLICY_ARG"

echo ""
echo "--- conftest test ---"
run_conftest test --policy "$POLICY_ARG" "${POLICY_TARGETS[@]}"

echo ""
echo "=== done (exit: 0) ==="
