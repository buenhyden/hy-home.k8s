# Project Agent Guide

This file is the root constitution for AI agents working in this repository.

## Authority Order

When instructions conflict, apply them in this order:

1. The current user task and explicit local context
2. Shared agent manuals in [.claude/](.claude/)
3. Project-specific manuals in [docs/manuals/](docs/manuals/)
4. Lifecycle guides in [docs/guides/](docs/guides/)
5. This root guide
6. Model-specific adapters in [GEMINI.md](GEMINI.md) and [CLAUDE.md](CLAUDE.md)
7. Shared automation rules and workflows in [.agent/rules/](.agent/rules/) and [.agent/workflows/](.agent/workflows/)

## Core Invariants

- Use approved specifications from [docs/specs/](docs/specs/) as the implementation source of truth.
- Create or update governed documents from the flattened templates in [templates/](templates/).
- Base changes on inspected repo evidence, not assumed structure or commands.
- Prefer project-specific manuals and guides when they narrow or override generic rules.
- Use runtime-provided skills when available; inspect `.agent/skills/` only if that directory exists in this repo.

## Navigation

- Shared governance details: [.claude/governance.md](.claude/governance.md)
- Delivery phases and handoffs: [.claude/lifecycle.md](.claude/lifecycle.md)
- Repo discovery and safe inspection: [.claude/repo-navigation.md](.claude/repo-navigation.md)
- Shared index for agent docs: [.claude/README.md](.claude/README.md)
- Gemini-specific execution profile: [GEMINI.md](GEMINI.md)
- Claude/CLI-specific execution profile: [CLAUDE.md](CLAUDE.md)

## Known Repo Facts

- This repository is documentation-heavy and governance-heavy.
- `.claude/` is the shared detailed instruction layer for agent-facing docs.
- No root `package.json` was found during inspection.
- Repo automation rules live under [.agent/rules/](.agent/rules/).
- Repo workflows live under [.agent/workflows/](.agent/workflows/).
- `.agent/skills/` is not currently present in this repository.

---
Last updated: March 2026
