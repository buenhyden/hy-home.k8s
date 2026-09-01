#!/usr/bin/env bash
# validate-repo-quality-gates.sh — dispatch repository-static validation owners
# Usage: bash scripts/validate-repo-quality-gates.sh [repo-root]
set -euo pipefail

ROOT_INPUT="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
ROOT_DIR="$(cd "$ROOT_INPUT" && pwd)"

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERR python3 is required for repository quality validation" >&2
  exit 1
fi

if ! python3 -c 'import yaml' >/dev/null 2>&1; then
  echo "ERR python3 PyYAML package is required for repository quality validation" >&2
  exit 1
fi

if ! python3 -c 'import jsonschema' >/dev/null 2>&1; then
  echo "ERR python3 jsonschema package is required for repository quality validation" >&2
  exit 1
fi

python3 "$ROOT_DIR/scripts/run-validation-lane.py" \
  --root "$ROOT_DIR" \
  --lane all-files

echo "[PASS] repository quality gates passed"
