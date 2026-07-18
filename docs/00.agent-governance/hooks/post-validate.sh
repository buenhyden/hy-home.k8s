#!/usr/bin/env bash
# post-validate.sh — scoped post-edit repository validation.
# Runs at PostToolUse for Write|Edit|MultiEdit.
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:?CLAUDE_PROJECT_DIR is required}"
INPUT_FILE="$(mktemp)"
PATHS_FILE="$(mktemp --suffix=.nul)"
RUNNER_LOG="$(mktemp)"
trap 'rm -f "$INPUT_FILE" "$PATHS_FILE" "$RUNNER_LOG"' EXIT
cat >"$INPUT_FILE"
CLAUDE_TOOL_INPUT_FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-}"
CLAUDE_TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

if ! /usr/bin/env -i \
  HOME="$HOME" LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/usr/bin:/bin \
  PROJECT_DIR="$PROJECT_DIR" INPUT_FILE="$INPUT_FILE" PATHS_FILE="$PATHS_FILE" \
  CLAUDE_TOOL_INPUT_FILE_PATH="$CLAUDE_TOOL_INPUT_FILE_PATH" \
  CLAUDE_TOOL_INPUT="$CLAUDE_TOOL_INPUT" \
  /usr/bin/python3 -I - <<'PY'
import json
import os
import sys
from pathlib import Path, PurePosixPath

project_dir = os.environ.get("PROJECT_DIR", "")
raw = Path(os.environ["INPUT_FILE"]).read_text(encoding="utf-8")
if not raw:
    raw = os.environ.get("CLAUDE_TOOL_INPUT", "")

paths: list[str] = []


def reject(code: str) -> None:
    print(f"[FAIL] {code}", file=sys.stderr)
    raise SystemExit(2)


def add_path(value):
    if not isinstance(value, str) or not value:
        reject("HOOK-PATH-TYPE")
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        reject("HOOK-PATH-CONTROL")
    if value[0].isspace() or value[-1].isspace():
        reject("HOOK-PATH-WHITESPACE")

    path = value
    if path.startswith("/"):
        prefix = project_dir.rstrip("/") + "/"
        if not project_dir or not path.startswith(prefix):
            reject("HOOK-PATH-ROOT")
        path = path[len(prefix) :]
    posix = PurePosixPath(path)
    if (
        not path
        or path.startswith("./")
        or path.endswith("/")
        or "//" in path
        or "\\" in path
        or posix.is_absolute()
        or "." in posix.parts
        or ".." in posix.parts
        or posix.as_posix() != path
    ):
        reject("HOOK-PATH-NORMALIZATION")

    cursor = Path(project_dir)
    for part in posix.parts:
        cursor /= part
        if cursor.is_symlink():
            reject("HOOK-PATH-SYMLINK")
    if path not in paths:
        paths.append(path)


try:
    data = json.loads(raw) if raw else {}
except (TypeError, json.JSONDecodeError):
    reject("HOOK-PAYLOAD-JSON")
if not isinstance(data, dict):
    reject("HOOK-PAYLOAD-SHAPE")


def consume_scalar_alias(mapping) -> int:
    present = [key for key in ("file_path", "path") if key in mapping]
    for key in present:
        if not isinstance(mapping[key], str) or not mapping[key]:
            reject("HOOK-PATH-TYPE")
    if len(present) > 1:
        reject("HOOK-PATH-ALIAS")
    if present:
        add_path(mapping[present[0]])
    return len(present)


if "tool_input" in data and not isinstance(data["tool_input"], dict):
    reject("HOOK-PAYLOAD-SHAPE")
tool_input = data.get("tool_input", {})
scalar_count = consume_scalar_alias(tool_input)
collection_aliases = [key for key in ("files", "paths") if key in tool_input]
for key in collection_aliases:
    value = tool_input[key]
    if not isinstance(value, list):
        reject("HOOK-PATH-LIST")
    if any(not isinstance(item, str) or not item for item in value):
        reject("HOOK-PATH-TYPE")
if len(collection_aliases) > 1 or (scalar_count and collection_aliases):
    reject("HOOK-PATH-ALIAS")
for key in collection_aliases:
    value = tool_input[key]
    for item in value:
        add_path(item)

if "edits" in tool_input:
    edits = tool_input["edits"]
    if not isinstance(edits, list):
        reject("HOOK-PATH-LIST")
    for edit in edits:
        if not isinstance(edit, dict):
            reject("HOOK-PATH-TYPE")
        consume_scalar_alias(edit)

environment_path = os.environ.get("CLAUDE_TOOL_INPUT_FILE_PATH", "")
if environment_path:
    add_path(environment_path)
Path(os.environ["PATHS_FILE"]).write_bytes(
    b"".join(path.encode("utf-8") + b"\0" for path in paths)
)
PY
then
  exit 2
fi

if ! /usr/bin/env -i \
  HOME="$HOME" LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/usr/bin:/bin \
  /usr/bin/python3 -I "$PROJECT_DIR/scripts/select-affected-surfaces.py" \
  --root "$PROJECT_DIR" --lane affected --paths-file "$PATHS_FILE" \
  --delimiter nul --format json >"$RUNNER_LOG" 2>&1; then
  printf '[hook] FAIL affected-surface path validation\n' >&2
  exit 2
fi

mapfile -d '' -t CHANGED_PATHS <"$PATHS_FILE"

cd "$PROJECT_DIR"

run_docs_template=0
run_repo_quality=0
declare -a FORMAT_FILES=()
declare -a SHELL_STYLE_FILES=()
declare -a MARKDOWN_STYLE_FILES=()
declare -a WORKFLOW_STYLE_FILES=()
declare -a DOCKER_STYLE_FILES=()

for path in "${CHANGED_PATHS[@]}"; do
  # Skip files outside the workspace root (absolute paths not under PROJECT_DIR)
  [[ "$path" = /* && "$path" != "$PROJECT_DIR/"* ]] && continue
  if [[ -f "$path" ]]; then
    FORMAT_FILES+=("$path")
    case "$path" in
    *.md)
      MARKDOWN_STYLE_FILES+=("$path")
      ;;
    docs/00.agent-governance/hooks/*.sh | scripts/*.sh | infrastructure/*.sh)
      SHELL_STYLE_FILES+=("$path")
      ;;
    .github/workflows/*.yml | .github/workflows/*.yaml)
      WORKFLOW_STYLE_FILES+=("$path")
      ;;
    Dockerfile | */Dockerfile | Dockerfile.* | */Dockerfile.*)
      DOCKER_STYLE_FILES+=("$path")
      ;;
    esac
  fi

  case "$path" in
  docs/01.requirements/*.md | docs/02.architecture/*.md | \
    docs/03.specs/*.md | docs/04.execution/*.md | \
    docs/05.operations/*.md | docs/90.references/*.md | docs/98.archive/*.md)
    run_docs_template=1
    run_repo_quality=1
    ;;
  esac

  # Keep this broad enough for docs/runtime mirrors while relying on the repo
  # quality gate for precise contract checks.
  case "$path" in
  AGENTS.md | CLAUDE.md | GEMINI.md | README.md | docs/* | .github/* | \
    .agents/* | .claude/* | .codex/* | scripts/* | .pre-commit-config.yaml | \
    infrastructure/k3d/k3d-cluster.yaml | gitops/apps/root/* | examples/*)
    run_repo_quality=1
    ;;
  esac
done

# The canonical selector covers .agents/* and runtime config paths such as
# .agents/hooks.json; repository-quality owns their detailed static parsing.

failure=0

run_pre_commit_hook() {
  local hook_id="$1"
  shift
  [[ "$#" -gt 0 ]] || return 0

  if command -v pre-commit >/dev/null 2>&1; then
    PRE_COMMIT_HOME="${PRE_COMMIT_HOME:-$HOME/.cache/pre-commit}" pre-commit run "$hook_id" --files "$@"
    return $?
  fi

  local pre_commit_python="${PRE_COMMIT_PYTHON:-$HOME/.local/share/uv/tools/pre-commit/bin/python}"
  if [[ -x "$pre_commit_python" ]]; then
    PRE_COMMIT_HOME="${PRE_COMMIT_HOME:-$HOME/.cache/pre-commit}" "$pre_commit_python" -mpre_commit run "$hook_id" --files "$@"
    return $?
  fi

  return 127
}

run_format_hook() {
  local label="$1"
  local hook_id="$2"
  shift 2
  [[ "$#" -gt 0 ]] || return 0

  local log_file rc
  log_file="$(mktemp)"
  if run_pre_commit_hook "$hook_id" "$@" >"$log_file" 2>&1; then
    printf '[hook] PASS %s\n' "$label"
  else
    rc=$?
    if [[ "$rc" -eq 127 ]]; then
      printf '[hook] SKIP %s - pre-commit unavailable\n' "$label"
    elif grep -Eiq 'files were modified by this hook|Fixing |Reformatted|would reformat|replacing' "$log_file"; then
      printf '[hook] FORMAT %s applied changes\n' "$label"
    else
      printf '[hook] FAIL %s\n' "$label" >&2
      cat "$log_file" >&2
      failure=1
    fi
  fi
  rm -f "$log_file"
}

run_style_check() {
  local label="$1"
  local hook_id="$2"
  shift 2
  [[ "$#" -gt 0 ]] || return 0

  local log_file rc
  log_file="$(mktemp)"
  if run_pre_commit_hook "$hook_id" "$@" >"$log_file" 2>&1; then
    printf '[hook] PASS %s\n' "$label"
  else
    rc=$?
    if [[ "$rc" -eq 127 ]]; then
      printf '[hook] SKIP %s - pre-commit unavailable\n' "$label"
    else
      printf '[hook] FAIL %s\n' "$label" >&2
      cat "$log_file" >&2
      failure=1
    fi
  fi
  rm -f "$log_file"
}

if [[ "${#FORMAT_FILES[@]}" -gt 0 ]]; then
  run_format_hook "format end-of-file" end-of-file-fixer "${FORMAT_FILES[@]}"
  run_format_hook "format trailing whitespace" trailing-whitespace "${FORMAT_FILES[@]}"
  run_format_hook "format mixed line endings" mixed-line-ending "${FORMAT_FILES[@]}"
fi

if [[ "${#SHELL_STYLE_FILES[@]}" -gt 0 ]]; then
  run_format_hook "format shell style" shfmt "${SHELL_STYLE_FILES[@]}"
fi

if [[ "${#MARKDOWN_STYLE_FILES[@]}" -gt 0 ]]; then
  run_style_check "Markdown style" markdownlint-cli2 "${MARKDOWN_STYLE_FILES[@]}"
fi

if [[ "${#SHELL_STYLE_FILES[@]}" -gt 0 ]]; then
  run_style_check "shell style" shellcheck "${SHELL_STYLE_FILES[@]}"
fi

if [[ "${#WORKFLOW_STYLE_FILES[@]}" -gt 0 ]]; then
  run_style_check "GitHub Actions style" actionlint "${WORKFLOW_STYLE_FILES[@]}"
  run_style_check "GitHub Actions security style" zizmor "${WORKFLOW_STYLE_FILES[@]}"
fi

if [[ "${#DOCKER_STYLE_FILES[@]}" -gt 0 ]]; then
  run_style_check "Dockerfile style" hadolint-docker "${DOCKER_STYLE_FILES[@]}"
fi

runner_rc=0
/usr/bin/env -i \
  GIT_TERMINAL_PROMPT=0 HOME="$HOME" LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  NO_COLOR=1 PATH=/usr/bin:/bin \
  PYTHONNOUSERSITE=1 TZ=UTC \
  /usr/bin/python3 -I scripts/run-validation-lane.py --root . --lane affected \
  --paths-file "$PATHS_FILE" --delimiter nul >"$RUNNER_LOG" 2>&1 || runner_rc=$?

if [[ "$runner_rc" -eq 0 ]]; then
  cat "$RUNNER_LOG"
  grep -Fq '[PASS] k8s-manifests ' "$RUNNER_LOG" && printf '[hook] PASS Kubernetes manifests\n'
  grep -Fq '[PASS] secret-handling ' "$RUNNER_LOG" && printf '[hook] PASS secret handling\n'
  repository_quality_pass=0
  if [[ "$run_repo_quality" -eq 1 ]]; then
    if /usr/bin/env -i \
      HOME="$HOME" LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/usr/bin:/bin \
      PYTHONNOUSERSITE=1 TZ=UTC \
      /usr/bin/python3 -I \
      docs/00.agent-governance/hooks/post-validate-runner-result.py \
      --log "$RUNNER_LOG" --identifier repository-quality; then
      repository_quality_pass=1
    else
      printf '[hook] FAIL repository quality result evidence\n' >&2
      failure=1
    fi
  fi
  if [[ "$repository_quality_pass" -eq 1 ]]; then
    if [[ "$run_docs_template" -eq 1 ]]; then
      printf '[hook] PASS documentation template enforcement\n'
    elif [[ "$run_repo_quality" -eq 1 ]]; then
      printf '[hook] PASS repository quality gates\n'
    fi
  fi
else
  cat "$RUNNER_LOG" >&2
  failure=1
fi

if [[ "$failure" -ne 0 ]]; then
  exit 2
fi

exit 0
