---
name: "__ROLE_NAME__"
description: "One sentence naming the bounded responsibility this role executes."
model: "__CLAUDE_MODEL_ID__"
tools: "__READ_GREP_GLOB__"
---

Read the canonical role at `__CANONICAL_ROLE_PATH__`, `.agents/roles/registry.json`,
`.agents/workflows/work-lifecycle.md`, and each registered skill procedure
explicitly before acting.
Apply their permission and handoff boundaries.
