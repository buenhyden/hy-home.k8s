#!/usr/bin/env bash
# k8s-pre-edit.sh — warn before editing Kubernetes or secret-adjacent files.
# Runs at PreToolUse for Write|Edit|MultiEdit. Exits 0 always (non-blocking).
set -euo pipefail

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
INPUT="$(cat || true)"
export PROJECT_DIR INPUT CLAUDE_TOOL_INPUT_FILE_PATH="${CLAUDE_TOOL_INPUT_FILE_PATH:-}" CLAUDE_TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}"

python3 - <<'PY'
import json
import os
import re

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
    edits = tool_input.get("edits")
    if isinstance(edits, list):
        for edit in edits:
            if isinstance(edit, dict):
                add_path(edit.get("file_path") or edit.get("path"))

add_path(os.environ.get("CLAUDE_TOOL_INPUT_FILE_PATH", ""))

manifest_re = re.compile(
    r"(gitops/.*\.ya?ml|infrastructure/.*\.ya?ml|examples/sample-app/.*\.ya?ml|"
    r"examples/.*/gitops/.*\.ya?ml|examples/.*/kubernetes/.*\.ya?ml|traefik/.*\.ya?ml)$"
)
secret_re = re.compile(r"(secret|credential|password|token)", re.IGNORECASE)

messages: list[str] = []
for path in paths:
    if manifest_re.search(path):
        messages.append(
            "\n".join(
                [
                    f"Editing Kubernetes manifest `{path}`.",
                    "- Keep the change GitOps-first: repository review -> ArgoCD reconciliation.",
                    "- Do not introduce plaintext Kubernetes secrets.",
                    "- The PostToolUse hook will run manifest and secret-handling validation.",
                ]
            )
        )
    if secret_re.search(path):
        messages.append(
            "\n".join(
                [
                    f"File name is secret-adjacent: `{path}`.",
                    "- Never write plaintext secret values.",
                    "- Use ExternalSecret or SealedSecret-style patterns only.",
                ]
            )
        )

if messages:
    print(json.dumps({"systemMessage": "\n\n".join(messages)}))
PY

exit 0
