# Gemini Execution Profile

This file defines Gemini-specific behavior for this repository. Shared policy lives in [AGENTS.md](AGENTS.md) and the manuals under [.claude/](.claude/).

## Use Gemini For

- long-context planning and synthesis
- dependency mapping across large documentation sets
- evidence-backed reasoning before implementation

## Gemini-Specific Guidance

- Plan first for complex or multi-file tasks.
- Summarize reasoning, decisions, and milestones without exposing private chain-of-thought.
- Use the long context window deliberately: compress prior findings before moving deeper into implementation.
- Search first when a path, workflow, or technology detail is uncertain.
- Treat missing repo paths as missing until inspection proves otherwise.

## Navigation

- Root policy: [AGENTS.md](AGENTS.md)
- Shared governance: [.claude/governance.md](.claude/governance.md)
- Lifecycle guidance: [.claude/lifecycle.md](.claude/lifecycle.md)
- Repo discovery: [.claude/repo-navigation.md](.claude/repo-navigation.md)
- Repo workflows: [.agent/workflows/](.agent/workflows/)

---
Target models: Gemini 2.x to 3.x, March 2026
