# Claude Execution Profile

This file defines Claude and CLI-specific behavior for this repository. Shared policy lives in [AGENTS.md](AGENTS.md) and the manuals under [.claude/](.claude/).

## Claude-Specific Guidance

- Prefer terminal inspection and concise evidence synthesis over speculative explanation.
- Use repo facts, not assumed build or test commands.
- Discover existing patterns through [.agent/workflows/](.agent/workflows/) before inventing new ones.
- Treat skill discovery as conditional: use runtime-provided skills first, and inspect `.agent/skills/` only if it exists locally.
- Preserve findings during long investigations so context survives tool transitions.
- Verify recovery paths before any destructive action.

## Quick Commands

Use these when orienting inside this repo:

```bash
git status --short
find .agent/workflows -maxdepth 2 -type f | sort
find templates -maxdepth 2 -type f | sort
rg --files docs
```

## Repo Navigation

- Root policy: [AGENTS.md](AGENTS.md)
- Shared governance: [.claude/governance.md](.claude/governance.md)
- Lifecycle guidance: [.claude/lifecycle.md](.claude/lifecycle.md)
- Repo discovery: [.claude/repo-navigation.md](.claude/repo-navigation.md)
- Rules: [.agent/rules/](.agent/rules/)
- Workflows: [.agent/workflows/](.agent/workflows/)
- Templates: [templates/](templates/)

## Notes

- No root package manifest was found during inspection, so this file intentionally does not prescribe root build or test commands.
- Keep this file model-specific; move shared detail into the linked manuals instead of growing this root file.

---
Target tooling: Claude Code and CLI-driven agents, March 2026
