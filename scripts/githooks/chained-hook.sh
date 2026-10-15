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
# Neither is selected by anything a commit under review can write.
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

run_hook() {
  local label="$1" hook="$2" stdin_file="$3" canonical status
  shift 3
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
  if [ -n "$stdin_file" ]; then
    "$hook" "$@" <"$stdin_file"
  else
    "$hook" "$@"
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
  run_hook global "$GLOBAL_HOOKS_PATH/$HOOK_NAME" "$STDIN_FILE" "$@"
fi

run_hook workspace "$GIT_COMMON_DIR/hooks/$HOOK_NAME" "$STDIN_FILE" "$@"
