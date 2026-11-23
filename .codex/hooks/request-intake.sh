#!/usr/bin/env bash
# request-intake.sh — Codex UserPromptSubmit adapter for the request brief (SPEC-0231).
# It forwards the payload to scripts/request_brief.py, which keeps a digest of
# the prompt, never its text, and returns the model instruction to show and
# record a brief before the first change. The program is resolved from this
# adapter's own checkout. Intake never blocks a prompt: any failure exits 0
# with no output, and the write guard then refuses the first change instead.
ADAPTER_DIR="$(cd "${BASH_SOURCE[0]%/*}" && pwd)" || exit 0
INTAKE="$ADAPTER_DIR/../../scripts/request_brief.py"
[[ -f "$INTAKE" ]] || exit 0
bound=()
command -v timeout >/dev/null 2>&1 && bound=(timeout 8)
"${bound[@]}" python3 "$INTAKE" intake --provider codex 2>/dev/null || true
exit 0
