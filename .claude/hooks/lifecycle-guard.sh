#!/usr/bin/env bash
# lifecycle-guard.sh - completion and compaction guard for repo-backed work.
# Stop/SubagentStop may block objective validation failures. PreCompact is advisory only.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-${CODEX_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}}"
INPUT="$(cat || true)"
SELFTEST="${HY_HOME_K8S_LIFECYCLE_GUARD_SELFTEST:-0}"

cd "$PROJECT_DIR"

event_name="$(
  INPUT="$INPUT" python3 - <<'PY'
import json
import os

raw = os.environ.get("INPUT", "")
event = os.environ.get("HY_HOME_K8S_HOOK_EVENT", "")
try:
    data = json.loads(raw) if raw.strip() else {}
except Exception:
    data = {}
if isinstance(data, dict):
    event = data.get("hook_event_name") or data.get("event") or event
print(event or "Stop")
PY
)"

declare -a CHANGED_PATHS=()
declare -a TRACKED_CHANGED_PATHS=()

add_unique_path() {
  local array_name="$1"
  local raw_path="$2"
  local -n target_array="$array_name"
  local path="$raw_path"

  [[ -n "$path" ]] || return 0
  path="${path#"$PROJECT_DIR"/}"
  path="${path#./}"
  [[ "$path" != .agent-work/* ]] || return 0

  local existing
  for existing in "${target_array[@]:-}"; do
    [[ "$existing" != "$path" ]] || return 0
  done
  target_array+=("$path")
}

if [[ "$SELFTEST" == "1" ]]; then
  while IFS= read -r path; do
    add_unique_path CHANGED_PATHS "$path"
    add_unique_path TRACKED_CHANGED_PATHS "$path"
  done <<<"${HY_HOME_K8S_CHANGED_PATHS:-}"
else
  while IFS= read -r line; do
    [[ -n "$line" ]] || continue
    status="${line:0:2}"
    path="${line:3}"
    if [[ "$path" == *" -> "* ]]; then
      path="${path##* -> }"
    fi
    add_unique_path CHANGED_PATHS "$path"
    if [[ "$status" != "??" ]]; then
      add_unique_path TRACKED_CHANGED_PATHS "$path"
    fi
  done < <(git status --porcelain=v1 --untracked-files=normal)
fi

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
    preview="$(printf '%s\n' "${TRACKED_CHANGED_PATHS[@]}" | head -n 12 | paste -sd ', ' -)"
    emit_json advisory "Lifecycle guard: ${#TRACKED_CHANGED_PATHS[@]} uncommitted tracked path(s) before compaction: ${preview}. Suggested validation: git diff --check; bash scripts/validate-repo-quality-gates.sh .; run manifest/secret checks when GitOps or YAML paths changed."
  fi
  exit 0
fi

case "$event_name" in
  Stop|SubagentStop) ;;
  *) exit 0 ;;
esac

if [[ "${#CHANGED_PATHS[@]}" -eq 0 ]]; then
  exit 0
fi

run_json=0
run_shell=0
run_manifest=0
run_repo_quality=0

for path in "${CHANGED_PATHS[@]}"; do
  case "$path" in
    .claude/settings.json|.codex/hooks.json)
      run_json=1
      run_repo_quality=1
      ;;
  esac

  case "$path" in
    .claude/hooks/*.sh|scripts/*.sh|infrastructure/*.sh)
      run_shell=1
      run_repo_quality=1
      ;;
  esac

  # Bash case patterns match "/" inside "*"; these root-prefixed globs cover
  # nested manifest files and intentionally mirror the CI path-filter scope.
  case "$path" in
    gitops/*.yml|gitops/*.yaml|\
infrastructure/*.yml|infrastructure/*.yaml|\
examples/sample-app/*.yml|examples/sample-app/*.yaml|\
examples/*/gitops/*.yml|examples/*/gitops/*.yaml|\
examples/*/kubernetes/*.yml|examples/*/kubernetes/*.yaml|\
traefik/*.yml|traefik/*.yaml)
      run_manifest=1
      ;;
  esac

  # Keep this broad enough for docs/runtime mirrors while relying on the repo
  # quality gate for precise contract checks.
  case "$path" in
    AGENTS.md|CLAUDE.md|GEMINI.md|README.md|docs/*|.github/*|\
.claude/*|.codex/*|scripts/*|.pre-commit-config.yaml|\
infrastructure/k3d/k3d-cluster.yaml|gitops/apps/root/*|examples/*)
      run_repo_quality=1
      ;;
  esac
done

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

  if [[ "$run_json" -eq 1 ]]; then
    run_check "Claude settings JSON parse" python3 -m json.tool .claude/settings.json
    run_check "Codex hooks JSON parse" python3 -m json.tool .codex/hooks.json
  fi

  if [[ "$run_shell" -eq 1 ]]; then
    run_check "shell syntax" bash -c 'find infrastructure scripts .claude/hooks -type f -name "*.sh" -exec bash -n {} +'
  fi

  if [[ "$run_manifest" -eq 1 ]]; then
    run_check "Kubernetes manifests" bash scripts/validate-k8s-manifests.sh .
    run_check "secret handling" bash scripts/check-secret-handling.sh .
  fi

  if [[ "$run_repo_quality" -eq 1 ]]; then
    run_check "repository quality gates" env HY_HOME_K8S_SKIP_HOOK_SIMULATION=1 bash scripts/validate-repo-quality-gates.sh .
  fi
fi

if [[ "${#FAILURES[@]}" -ne 0 ]]; then
  reason="$(printf '%s; ' "${FAILURES[@]}")"
  emit_json block "Lifecycle guard blocked ${event_name} because validation failed: ${reason%'; '}. Run the listed validation category, fix the repo-state failure, then retry."
fi

exit 0
