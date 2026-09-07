---
description: "Assemble a work handoff request from the fields the quality policy owns."
allowed-tools: "Bash(python3 scripts/prompt-input.py handoff:*)"
---

Run `python3 scripts/prompt-input.py handoff` from the repository root and use its
output as the request. The builder reads only the inputs
`.agents/prompts/handoff.md` declares, makes no model call, and writes nothing to
the repository or to Git state. When it exits non-zero, report its diagnostic
instead of producing a draft.
