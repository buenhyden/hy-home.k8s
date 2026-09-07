---
description: "Locate the canonical owner for a change and request a difference against it."
allowed-tools: "Bash(python3 scripts/prompt-input.py doc-update:*)"
---

Run `python3 scripts/prompt-input.py doc-update` from the repository root and use
its output as the request. The builder reads only the inputs
`.agents/prompts/doc-update.md` declares, makes no model call, and writes nothing
to the repository or to Git state. When it exits non-zero, report its diagnostic
instead of producing a draft.
