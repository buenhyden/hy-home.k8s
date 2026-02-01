#!/usr/bin/env bash
set -u
set -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

fail=0
skip_python=0

for arg in "$@"; do
  case "$arg" in
    --skip-python)
      skip_python=1
      ;;
    --help|-h)
      echo "Usage: $0 [--skip-python]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $arg"
      exit 2
      ;;
  esac
done

run() {
  local name="$1"
  shift
  echo "==> ${name}"
  if "$@"; then
    echo "==> ${name} ok"
  else
    echo "==> ${name} failed"
    fail=1
  fi
}

skip() {
  local name="$1"
  local reason="$2"
  echo "==> ${name} skipped (${reason})"
}

has() {
  command -v "$1" >/dev/null 2>&1
}

note_go_path() {
  if ! has go; then
    return 0
  fi
  local go_bin
  go_bin="$(go env GOBIN)"
  if [ -z "$go_bin" ]; then
    go_bin="$(go env GOPATH)/bin"
  fi
  case ":$PATH:" in
    *":$go_bin:"*) ;;
    *) echo "==> NOTE: add $go_bin to PATH to use Go-installed tools." ;;
  esac
}

note_python_path() {
  local python_cmd="$1"
  local base
  base="$("$python_cmd" -m site --user-base 2>/dev/null || true)"
  if [ -z "$base" ]; then
    return 0
  fi
  local scripts="${base}/bin"
  case ":$PATH:" in
    *":$scripts:"*) ;;
    *) echo "==> NOTE: add $scripts to PATH to use Python user-installed tools." ;;
  esac
}

if has markdownlint-cli2; then
  skip "markdownlint-cli2" "already installed"
elif has npm; then
  run "markdownlint-cli2" npm install -g markdownlint-cli2
else
  skip "markdownlint-cli2" "npm not installed"
  fail=1
fi

if has actionlint; then
  skip "actionlint" "already installed"
elif has go; then
  run "actionlint" go install github.com/rhysd/actionlint/cmd/actionlint@latest
  note_go_path
else
  skip "actionlint" "go not installed"
  fail=1
fi

if has kube-linter; then
  skip "kube-linter" "already installed"
elif has go; then
  run "kube-linter" go install golang.stackrox.io/kube-linter/cmd/kube-linter@latest
  note_go_path
else
  skip "kube-linter" "go not installed"
  fail=1
fi

if [ "$skip_python" -eq 1 ]; then
  skip "python tools" "skip-python set"
else
  python_cmd=""
  if has python3; then
    python_cmd="python3"
  elif has python; then
    python_cmd="python"
  fi

  if has ruff; then
    skip "ruff" "already installed"
  elif has pipx; then
    run "ruff" pipx install ruff
  elif [ -n "$python_cmd" ]; then
    run "ruff" "$python_cmd" -m pip install --user ruff
    note_python_path "$python_cmd"
  else
    skip "ruff" "python or pipx not installed"
    fail=1
  fi

  if has mypy; then
    skip "mypy" "already installed"
  elif has pipx; then
    run "mypy" pipx install mypy
  elif [ -n "$python_cmd" ]; then
    run "mypy" "$python_cmd" -m pip install --user mypy
    note_python_path "$python_cmd"
  else
    skip "mypy" "python or pipx not installed"
    fail=1
  fi
fi

if [ "$fail" -ne 0 ]; then
  echo "==> One or more tools were not installed. See messages above."
  exit 1
fi
