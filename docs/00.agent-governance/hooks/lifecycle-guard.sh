#!/usr/bin/env bash
# lifecycle-guard.sh - completion and compaction guard for repo-backed work.
# Stop/SubagentStop may block objective validation failures. PreCompact is advisory only.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}}"
SELFTEST="${HY_HOME_K8S_LIFECYCLE_GUARD_SELFTEST:-0}"
INPUT_FILE="$(mktemp)"
EVENT_FILE="$(mktemp)"
CHANGED_FILE="$(mktemp --suffix=.nul)"
TRACKED_FILE="$(mktemp --suffix=.nul)"
UNTRACKED_FILE="$(mktemp --suffix=.nul)"
RUNNER_LOG="$(mktemp)"
trap 'rm -f "$INPUT_FILE" "$EVENT_FILE" "$CHANGED_FILE" "$TRACKED_FILE" "$UNTRACKED_FILE" "$RUNNER_LOG"' EXIT
cat >"$INPUT_FILE"

cd "$PROJECT_DIR"

export INPUT_FILE EVENT_FILE
python3 - <<'PY'
import json
import os
from pathlib import Path

raw = Path(os.environ["INPUT_FILE"]).read_text(encoding="utf-8")
event = os.environ.get("HY_HOME_K8S_HOOK_EVENT", "")
try:
    data = json.loads(raw) if raw else {}
except Exception:
    data = {}
if isinstance(data, dict):
    event = data.get("hook_event_name") or data.get("event") or event
Path(os.environ["EVENT_FILE"]).write_text((event or "Stop") + "\n", encoding="utf-8")
PY
IFS= read -r event_name <"$EVENT_FILE"

declare -a CHANGED_PATHS=()
declare -a TRACKED_CHANGED_PATHS=()

if [[ "$SELFTEST" == "1" ]]; then
  export CHANGED_FILE TRACKED_FILE HY_HOME_K8S_CHANGED_PATHS="${HY_HOME_K8S_CHANGED_PATHS:-}"
  python3 - <<'PY'
import os
from pathlib import Path

records = [item for item in os.environ["HY_HOME_K8S_CHANGED_PATHS"].splitlines() if item]
payload = b"".join(item.encode("utf-8") + b"\0" for item in records)
Path(os.environ["CHANGED_FILE"]).write_bytes(payload)
Path(os.environ["TRACKED_FILE"]).write_bytes(payload)
PY
else
  git diff --no-renames --name-only -z HEAD >"$TRACKED_FILE"
  git ls-files --others --exclude-standard -z >"$UNTRACKED_FILE"
  export CHANGED_FILE TRACKED_FILE UNTRACKED_FILE
  python3 - <<'PY'
import os
from pathlib import Path

records: list[bytes] = []
for name in ("TRACKED_FILE", "UNTRACKED_FILE"):
    payload = Path(os.environ[name]).read_bytes()
    records.extend(item for item in payload.split(b"\0") if item and not item.startswith(b".agent-work/"))
unique = sorted(set(records))
Path(os.environ["CHANGED_FILE"]).write_bytes(b"".join(item + b"\0" for item in unique))
PY
fi

mapfile -d '' -t CHANGED_PATHS <"$CHANGED_FILE"
mapfile -d '' -t TRACKED_CHANGED_PATHS <"$TRACKED_FILE"

emit_json() {
  local payload_type="$1"
  local message="$2"
  PAYLOAD_TYPE="$payload_type" MESSAGE="$message" python3 - <<'PY'
import json
import os

payload_type = os.environ["PAYLOAD_TYPE"]
message = os.environ["MESSAGE"]
if payload_type == "block":
    print(json.dumps({"decision": "block", "reason": message}))
else:
    print(json.dumps({"systemMessage": message}))
PY
}

if [[ "$event_name" == "PreCompact" ]]; then
  if [[ "${#TRACKED_CHANGED_PATHS[@]}" -eq 0 ]]; then
    emit_json advisory "Lifecycle guard: no uncommitted tracked changes detected. Suggested validation remains: git diff --check and bash scripts/validate-repo-quality-gates.sh . when repo files changed."
  else
    emit_json advisory "Lifecycle guard: ${#TRACKED_CHANGED_PATHS[@]} uncommitted tracked path(s) before compaction. Suggested validation: git diff --check; bash scripts/validate-repo-quality-gates.sh .; run manifest/secret checks when GitOps or YAML paths changed. Task-unit commit discipline: do not auto-commit; when the human requested commits, split commits by logical task/spec IDs, stage only files for that unit, review git diff --cached, and use Conventional Commit messages. If the dirty state spans multiple SDD overlays, runtime docs, hooks, validators, or env contracts, split it before committing; if a broad commit is already published, record a forward-only exception instead of rewriting public history."
  fi
  exit 0
fi

case "$event_name" in
Stop | SubagentStop) ;;
*) exit 0 ;;
esac

if [[ "${#CHANGED_PATHS[@]}" -eq 0 ]]; then
  exit 0
fi

# Shared implementations remain under docs/00.agent-governance/hooks. The
# canonical selector covers .agents/* and runtime config paths such as
# .agents/hooks.json; the selected repository-quality argv owns detailed checks.

declare -a FAILURES=()

run_check() {
  local label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    return 0
  fi
  FAILURES+=("$label")
}

if [[ "$SELFTEST" == "1" ]]; then
  if [[ "${HY_HOME_K8S_FORCE_FAIL:-0}" == "1" ]]; then
    FAILURES+=("self-test forced failure")
  fi
else
  run_check "diff whitespace" git diff --check
  if ! python3 scripts/run-validation-lane.py --root . --lane affected \
    --paths-file "$CHANGED_FILE" --delimiter nul >"$RUNNER_LOG" 2>&1; then
    FAILURES+=("affected-surface validation lane")
  fi
fi

if [[ "${#FAILURES[@]}" -ne 0 ]]; then
  reason="$(printf '%s; ' "${FAILURES[@]}")"
  emit_json block "Lifecycle guard blocked ${event_name} because validation failed: ${reason%'; '}. Run the listed validation category, fix the repo-state failure, then retry."
fi

if [[ "${#TRACKED_CHANGED_PATHS[@]}" -ne 0 ]]; then
  emit_json advisory "Lifecycle guard: validation passed with ${#TRACKED_CHANGED_PATHS[@]} uncommitted tracked path(s). Task-unit commit discipline: do not auto-commit; when the human requested commits, split commits by logical task/spec IDs, stage only files for that unit, review git diff --cached, and use Conventional Commit messages. If the dirty state spans multiple SDD overlays, runtime docs, hooks, validators, or env contracts, split it before committing; if a broad commit is already published, record a forward-only exception instead of rewriting public history. If work intentionally remains uncommitted, the final response must name the files and reason."
fi

exit 0
