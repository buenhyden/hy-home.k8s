#!/usr/bin/env bash
set -u
set -o pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit

# fail=0

has() {
  command -v "$1" >/dev/null 2>&1
}

echo "==> Setting up pre-commit..."

if has pre-commit; then
  echo "==> pre-commit already installed"
else
  if has pipx; then
    echo "==> Installing pre-commit via pipx..."
    pipx install pre-commit
  elif has pip3; then
    echo "==> Installing pre-commit via pip3..."
    pip3 install --user pre-commit
    # Check path
    base="$(python3 -m site --user-base 2>/dev/null || true)"
    if [ -n "$base" ]; then
      case ":$PATH:" in
      *":$base/bin:"*) ;;
      *) echo "==> NOTE: add $base/bin to PATH to use pre-commit." ;;
      esac
    fi
  elif has pip; then
    echo "==> Installing pre-commit via pip..."
    pip install --user pre-commit
  elif has brew; then
    echo "==> Installing pre-commit via brew..."
    brew install pre-commit
  else
    echo "==> Error: Python pip/pip3 or pipx or brew required to install pre-commit."
    exit 1
  fi
fi

if has pre-commit; then
  echo "==> Installing git hooks..."
  pre-commit install
else
  echo "==> Error: pre-commit installation failed or not found in PATH."
  exit 1
fi

echo "==> Setup complete!"
