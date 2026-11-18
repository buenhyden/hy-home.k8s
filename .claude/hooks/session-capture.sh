#!/usr/bin/env bash
# session-capture.sh — Claude adapter for local session capture (W08-CAPTURE).
# Registered for the session lifecycle events. It forwards the hook payload to
# scripts/session_capture.py, which keeps pointers and structure only, never
# prompt or response text. The program is resolved from this adapter's own
# checkout. Capture is advisory: it prints nothing on stdout, and any failure,
# including a timeout, exits 0 so capture never stops a session.
ADAPTER_DIR="$(cd "${BASH_SOURCE[0]%/*}" && pwd)" || exit 0
CAPTURE="$ADAPTER_DIR/../../scripts/session_capture.py"
[[ -f "$CAPTURE" ]] || exit 0
# Without coreutils timeout (for example on macOS) the client's own hook
# timeout still bounds the run.
bound=()
command -v timeout >/dev/null 2>&1 && bound=(timeout 2.5)
"${bound[@]}" python3 "$CAPTURE" hook --provider claude >/dev/null 2>&1 || true
exit 0
