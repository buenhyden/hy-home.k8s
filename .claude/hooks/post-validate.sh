#!/usr/bin/env bash
# post-validate.sh — scoped post-edit repository validation.
# Runs at PostToolUse for Write|Edit|MultiEdit.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
INPUT="$(cat || true)"
export PROJECT_DIR INPUT CLAUDE_TOOL_INPUT_FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-}" CLAUDE_TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

mapfile -t CHANGED_PATHS < <(
  python3 - <<'PY'
import json
import os

project_dir = os.environ.get("PROJECT_DIR", "")
raw = os.environ.get("INPUT", "")
if not raw.strip():
    raw = os.environ.get("CLAUDE_TOOL_INPUT", "")

paths: list[str] = []


def add_path(value):
    if isinstance(value, str) and value.strip():
        path = value.strip()
        if project_dir and path.startswith(project_dir + "/"):
            path = path[len(project_dir) + 1 :]
        if path.startswith("./"):
            path = path[2:]
        if path not in paths:
            paths.append(path)


try:
    data = json.loads(raw) if raw.strip() else {}
except Exception:
    data = {}

tool_input = data.get("tool_input", {}) if isinstance(data, dict) else {}
if isinstance(tool_input, dict):
    add_path(tool_input.get("file_path") or tool_input.get("path"))
    for key in ("files", "paths"):
        value = tool_input.get(key)
        if isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    add_path(item)
                elif isinstance(item, dict):
                    add_path(item.get("file_path") or item.get("path"))

    edits = tool_input.get("edits")
    if isinstance(edits, list):
        for edit in edits:
            if isinstance(edit, dict):
                add_path(edit.get("file_path") or edit.get("path"))

add_path(os.environ.get("CLAUDE_TOOL_INPUT_FILE_PATH", ""))

for path in paths:
    print(path)
PY
)

if [[ "${#CHANGED_PATHS[@]}" -eq 0 ]]; then
  exit 0
fi

cd "$PROJECT_DIR"

run_json=0
run_shell=0
run_manifest=0
run_repo_quality=0

for path in "${CHANGED_PATHS[@]}"; do
  case "$path" in
    .claude/settings.json|.codex/hooks.json)
      run_json=1
      ;;
  esac

  case "$path" in
    .claude/hooks/*.sh|scripts/*.sh|infrastructure/*.sh)
      run_shell=1
      ;;
  esac

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

  case "$path" in
    AGENTS.md|CLAUDE.md|GEMINI.md|README.md|docs/*|.github/*|\
.claude/*|.codex/*|scripts/*|.pre-commit-config.yaml|\
infrastructure/k3d/k3d-cluster.yaml|gitops/apps/root/*|examples/*)
      run_repo_quality=1
      ;;
  esac
done

failure=0

run_check() {
  local label="$1"
  shift
  local log_file
  log_file="$(mktemp)"
  if "$@" >"$log_file" 2>&1; then
    printf '[hook] PASS %s\n' "$label"
  else
    printf '[hook] FAIL %s\n' "$label" >&2
    cat "$log_file" >&2
    failure=1
  fi
  rm -f "$log_file"
}

if [[ "$run_json" -eq 1 ]]; then
  run_check "runtime JSON parse" python3 -m json.tool .claude/settings.json
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

if [[ "$failure" -ne 0 ]]; then
  exit 2
fi

exit 0
