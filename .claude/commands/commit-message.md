---
description: "Assemble a commit-message draft request from the staged difference only."
allowed-tools: "Bash(python3 scripts/prompt-input.py commit-message:*)"
---

Run `python3 scripts/prompt-input.py commit-message` from the repository root and
use its output as the request. The builder reads the staged difference only,
makes no model call, and never stages, commits or amends. The draft is a
proposal the user accepts, edits or discards. When it exits non-zero, report its
diagnostic instead of producing a draft.
