---
description: "Assemble a review request over the local difference."
allowed-tools: "Bash(python3 scripts/prompt-input.py change-review:*)"
---

Run `python3 scripts/prompt-input.py change-review` from the repository root and
use its output as the request. The builder reads only the inputs
`.agents/prompts/change-review.md` declares, makes no model call, and writes
nothing to the repository or to Git state. When it exits non-zero, report its
diagnostic instead of producing a draft.
