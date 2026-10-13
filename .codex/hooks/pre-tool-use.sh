#!/usr/bin/env bash
# pre-tool-use.sh — Codex adapter for the shared pre-action write boundary.
# Registered in .codex/hooks.json for Bash|apply_patch. It names its provider
# and forwards the payload; the boundary itself is owned by
# scripts/provider_write_guard.py so no provider directory owns a control both
# providers depend on.
# Trust boundary: the guard program is resolved from this adapter's own
# checkout, never from a tool-supplied root, so the guarded tree can supply
# data but never the executable.
# Registration alone is not evidence that the installed client discovered,
# loaded, or delivered this hook; see .codex/provider.md.
# Fail closed: the runtime blocks only on exit 2, so any adapter failure exits 2.
set -euo pipefail
trap 'echo "[FAIL] HOOK-ADAPTER: the write guard could not run" >&2; exit 2' ERR

ADAPTER_DIR="$(cd "${BASH_SOURCE[0]%/*}" && pwd)"
GUARD="$ADAPTER_DIR/../../scripts/provider_write_guard.py"
PROJECT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
command -v python3 >/dev/null
[[ -f "$GUARD" ]]

exec python3 "$GUARD" --provider codex --project-dir "$PROJECT_DIR"
