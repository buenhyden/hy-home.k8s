#!/usr/bin/env bash
# session-start.sh — Claude SessionStart adapter, registered for compact|resume.
# A compacted or resumed conversation may keep earlier folder AGENTS.md rules
# only as a summary, so this re-injects the instruction to read them again.
# It runs no QA and calls no agent (see PROVIDER_HOOK_EVENTS in
# scripts/validate-agent-governance.py), and it never blocks: any failure
# exits 0 with no output.
cat >/dev/null 2>&1 || true
printf '%s\n' '{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"The conversation was compacted or resumed, so folder AGENTS.md rules loaded earlier may survive only as a summary. Before reading or changing files in a folder, read every AGENTS.md from the repository root down to that folder again. A folder CLAUDE.md that imports its AGENTS.md is documented to reload on the next file access there, and the pre-action guard names the AGENTS.md paths on every write."}}' || true
exit 0
