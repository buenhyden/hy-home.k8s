#!/usr/bin/env bash
# chained-hook.sh — run both the user's global Git hook and this workspace's.
#
# Each entry in this directory names its hook and forwards the payload here.
# Git honours exactly one hook directory. A user-global `core.hooksPath` makes
# every repository's own `.git/hooks` unreachable, so a workspace that installs
# hooks through pre-commit silently loses them: here that removed the commit
# message check and every staged formatter. Pointing this repository's
# `core.hooksPath` at this directory restores both sides, in a stated order,
# instead of choosing one.
#
# Order: the global hook runs first because it is the cheap outer safety net,
# then the workspace hook runs its own checks. The first non-zero status ends
# the chain and is returned unchanged, so neither side can be skipped and
# neither side's failure is downgraded.
#
# Trust boundary: the workspace hook is resolved from this repository's own
# `.git/hooks`, and the global hook only from the user's global configuration.
# Neither is selected by anything a commit under review can write. The
# workspace hook runs with the validation environment named by the Git option
# `hyhome.validationVenv` first on PATH; Git configuration is not tracked, and
# the environment must lie outside every worktree, belong to the invoking
# account or root, and carry no group- or other-write bit (Git policy).
set -euo pipefail

HOOK_NAME="$1"
shift
case "$HOOK_NAME" in
pre-commit | commit-msg | pre-push) ;;
*)
  printf '[git hook] HOOK-NAME: unsupported hook %s; use a scripts/githooks entry\n' "$HOOK_NAME" >&2
  exit 2
  ;;
esac
if [ -n "${HY_HOME_CHAINED_HOOK_ACTIVE:-}" ]; then
  printf '[git hook] HOOK-RECURSION: %s called this dispatcher again; fix the hook chain\n' "$HOOK_NAME" >&2
  exit 2
fi
export HY_HOME_CHAINED_HOOK_ACTIVE=1
REPOSITORY_ROOT="$(git rev-parse --show-toplevel)"
GIT_COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"

env_refuse() {
  local lock="$REPOSITORY_ROOT/.github/requirements/ci-validation.txt"
  printf '[git hook] HOOK-ENV: %s\n' "$1" >&2
  printf '[git hook] set hyhome.validationVenv to a validation environment outside every checkout, once per account:\n' >&2
  # The commands print \$HOME literally, ready to copy.
  printf "  umask 022 && python3 -m venv \"\$HOME/.venvs/hyhome-validation\"\n" >&2
  printf "  \"\$HOME/.venvs/hyhome-validation/bin/python\" -m pip install --only-binary :all: --require-hashes -r %q\n" "$lock" >&2
  printf "  git config --global hyhome.validationVenv \"\$HOME/.venvs/hyhome-validation\"\n" >&2
  printf '[git hook] if Python later writes group-writable files there, run: chmod -R go-w <environment>\n' >&2
  exit 2
}

# Resolve and check the validation environment; set VALIDATION_BIN.
resolve_validation_env() {
  local value status venv entry tree tool python_target offender list
  local -a entries
  if value="$(git config --path --get hyhome.validationVenv)"; then
    :
  else
    status=$?
    if [ "$status" -ne 1 ]; then
      printf '[git hook] HOOK-CONFIG: cannot read hyhome.validationVenv; fix the Git config\n' >&2
      exit "$status"
    fi
    value=""
  fi
  [ -n "$value" ] || env_refuse "hyhome.validationVenv is unset or empty"
  case "$value" in
  /*) ;;
  *) env_refuse "hyhome.validationVenv must be an absolute path, not $value" ;;
  esac
  if ! venv="$(realpath -e -- "$value" 2>/dev/null)" || [ ! -d "$venv" ]; then
    env_refuse "hyhome.validationVenv names no directory: $value"
  fi
  list="$(mktemp)"
  if ! git worktree list --porcelain -z >"$list"; then
    rm -f "$list"
    env_refuse "cannot list the worktrees of this repository"
  fi
  mapfile -d '' -t entries <"$list"
  rm -f "$list"
  for entry in "${entries[@]}"; do
    case "$entry" in
    "worktree "*)
      tree="$(realpath -m -- "${entry#worktree }")"
      case "$venv/" in
      "$tree"/*) env_refuse "hyhome.validationVenv $venv lies inside the worktree $tree" ;;
      esac
      ;;
    esac
  done
  for tool in python3 pre-commit; do
    if [ ! -f "$venv/bin/$tool" ] || [ ! -x "$venv/bin/$tool" ]; then
      env_refuse "hyhome.validationVenv $venv has no executable bin/$tool"
    fi
  done
  if ! python_target="$(realpath -e -- "$venv/bin/python3")"; then
    env_refuse "cannot resolve $venv/bin/python3"
  fi
  # Mode bits, not -w (always true for root); -quit stops at the first offender.
  if ! offender="$(find "$venv" "$python_target" ! -type l \( -perm /022 -o \( ! -uid "$(id -u)" ! -uid 0 \) \) -print -quit)"; then
    env_refuse "cannot inspect $venv"
  fi
  if [ -n "$offender" ]; then
    env_refuse "hyhome.validationVenv $venv is unsafe: $offender is writable by group or other, or owned by another account"
  fi
  VALIDATION_BIN="$venv/bin"
}

run_hook() {
  local label="$1" hook="$2" stdin_file="$3" hook_path="$4" canonical status
  shift 4
  if [ ! -e "$hook" ] && [ ! -L "$hook" ]; then
    if [ "$label" = workspace ] && [ "$HOOK_NAME" != pre-push ]; then
      printf '[git hook] HOOK-MISSING: required workspace %s is absent at %s; install or restore it\n' "$HOOK_NAME" "$hook" >&2
      return 2
    fi
    return 0
  fi
  if [ ! -f "$hook" ] || [ ! -x "$hook" ]; then
    printf '[git hook] HOOK-NONEXEC: %s %s at %s is not an executable file; repair it\n' "$label" "$HOOK_NAME" "$hook" >&2
    return 2
  fi
  canonical="$(realpath -e -- "$hook")" || {
    printf '[git hook] HOOK-PATH: cannot resolve %s %s at %s; repair it\n' "$label" "$HOOK_NAME" "$hook" >&2
    return 2
  }
  [ "$canonical" != "${EXECUTED_HOOK_PATH:-}" ] || return 0
  EXECUTED_HOOK_PATH="$canonical"
  # PATH is set on the hook command only; the dispatcher keeps the caller's.
  if [ -n "$stdin_file" ]; then
    PATH="$hook_path" "$hook" "$@" <"$stdin_file"
  else
    PATH="$hook_path" "$hook" "$@"
  fi || {
    status=$?
    printf '[git hook] %s %s failed with status %d\n' "$label" "$HOOK_NAME" "$status" >&2
    return "$status"
  }
}

# Only pre-push receives a payload on stdin. Capture it once so both sides read
# the same bytes; a second reader of a consumed pipe would otherwise see none.
STDIN_FILE=""
if [ "$HOOK_NAME" = "pre-push" ]; then
  STDIN_FILE="$(mktemp)"
  trap 'rm -f "$STDIN_FILE"' EXIT
  cat >"$STDIN_FILE"
fi

# A pre-push without a workspace hook is a no-op and needs no environment.
WORKSPACE_HOOK="$GIT_COMMON_DIR/hooks/$HOOK_NAME"
VALIDATION_BIN=""
if [ "$HOOK_NAME" != pre-push ] || [ -e "$WORKSPACE_HOOK" ] || [ -L "$WORKSPACE_HOOK" ]; then
  resolve_validation_env
fi

GLOBAL_HOOKS_PATH=""
if GLOBAL_HOOKS_PATH="$(git config --global --path --get core.hooksPath)"; then
  [ -n "$GLOBAL_HOOKS_PATH" ] || {
    printf '[git hook] HOOK-CONFIG: global core.hooksPath is empty; fix the Git config\n' >&2
    exit 2
  }
else
  status=$?
  if [ "$status" -ne 1 ]; then
    printf '[git hook] HOOK-CONFIG: cannot read global core.hooksPath; fix the Git config\n' >&2
    exit "$status"
  fi
fi
if [ -n "$GLOBAL_HOOKS_PATH" ]; then
  case "$GLOBAL_HOOKS_PATH" in
  /*) ;;
  *) GLOBAL_HOOKS_PATH="$REPOSITORY_ROOT/$GLOBAL_HOOKS_PATH" ;;
  esac
  if [ ! -d "$GLOBAL_HOOKS_PATH" ]; then
    printf '[git hook] HOOK-GLOBAL-DIR: configured global hook directory %s is absent; fix core.hooksPath\n' "$GLOBAL_HOOKS_PATH" >&2
    exit 2
  fi
  run_hook global "$GLOBAL_HOOKS_PATH/$HOOK_NAME" "$STDIN_FILE" "$PATH" "$@"
fi

run_hook workspace "$WORKSPACE_HOOK" "$STDIN_FILE" "${VALIDATION_BIN:+$VALIDATION_BIN:}$PATH" "$@"
