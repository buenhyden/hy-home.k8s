#!/usr/bin/env bash
# chained-hook.sh — run both the user's global Git hook and this workspace's.
#
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

HOOK_NAME="$(basename "$0")"
REPOSITORY_ROOT="$(git rev-parse --show-toplevel)"
GIT_COMMON_DIR="$(git rev-parse --path-format=absolute --git-common-dir)"

run_hook() {
  local label="$1" hook="$2" stdin_file="$3"
  shift 3
  [ -x "$hook" ] || return 0
  if [ -n "$stdin_file" ]; then
    "$hook" "$@" <"$stdin_file"
  else
    "$hook" "$@" </dev/null
  fi || {
    local status=$?
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

GLOBAL_HOOKS_PATH="$(git config --global --get core.hooksPath || true)"
if [ -n "$GLOBAL_HOOKS_PATH" ]; then
  case "$GLOBAL_HOOKS_PATH" in
  /*) ;;
  ~*) GLOBAL_HOOKS_PATH="${HOME}${GLOBAL_HOOKS_PATH#\~}" ;;
  *) GLOBAL_HOOKS_PATH="$REPOSITORY_ROOT/$GLOBAL_HOOKS_PATH" ;;
  esac
  run_hook global "$GLOBAL_HOOKS_PATH/$HOOK_NAME" "$STDIN_FILE" "$@"
fi

run_hook workspace "$GIT_COMMON_DIR/hooks/$HOOK_NAME" "$STDIN_FILE" "$@"
