# Agent Instructions

Cross-agent root contract for this repository's documentation, planning, and operations work.

## Project Overview

- This repo is documentation-heavy and governance-heavy.
- **Spec-Driven Development (SDD)**: `docs/specs/` uniquely drives all implementation.
- **6 Core Pillars**: Security (`2200`), Performance (`2300`), Observability (`2600`), Compliance (`2400`), Documentation (`2100`), Localization (`2500`).
- Canonical work domains live under `docs/`: `adr`, `ard`, `prd`, `plans`, `specs`, `incidents`, `runbooks`, `operations`, `manuals`.
- Canonical templates are flat files under `templates/`.
- `.claude/` is the shared detailed instruction layer for agent-facing docs.

## Precedence

Apply instructions in this order:

1. Current user task and explicit local context
2. Nearest scoped `AGENTS.md`, `GEMINI.md`, or `CLAUDE.md` in the working subtree
3. Shared agent files in `.claude/`
4. Project manuals in `docs/manuals/`
5. This root file
6. `.agent/rules/` and `.agent/workflows/`

## Commands

Only documented commands verified in this repo:

```bash
git status --short
find .agent/rules -maxdepth 2 -type f | sort
find .agent/workflows -maxdepth 2 -type f | sort
find templates -maxdepth 2 -type f | sort
rg --files docs
```

No root package manifest was found during inspection, so do not invent root build, test, or package-manager commands.

## Code Style

- Use repo-relative Markdown links.
- Do not use absolute file URI links.
- Base edits on inspected repo facts, not inherited template assumptions.
- Keep root instruction files concise; move shared detail into `.claude/`.

## Testing

- Treat `docs/specs/` as the implementation source of truth.
- Validate links, imports, and path references after instruction changes.
- For doc work under `docs/`, rely on nearest scoped instruction files for local constraints.

## Security

- Do not expose secrets or personal local preferences in repo-tracked instruction files.
- Do not fabricate commands, paths, or nonexistent repo structure.

## Extra Instructions

- Skills are allowed without whitelist restriction and should be chosen contextually at runtime.
- Use runtime-provided skills first; inspect `.agent/skills/` only if that directory exists locally.
- Use the persona mappings encoded in `.claude/rules/personas.md` and the nearest scoped doc file for the active subtree.

## Navigation

- Human index: [.claude/README.md](.claude/README.md)
- Shared governance: [.claude/governance.md](.claude/governance.md)
- Human lifecycle guide: [.claude/lifecycle.md](.claude/lifecycle.md)
- Repo navigation: [.claude/repo-navigation.md](.claude/repo-navigation.md)
- Claude runtime entrypoint: [.claude/CLAUDE.md](.claude/CLAUDE.md)
- Gemini runtime entrypoint: [.claude/GEMINI.md](.claude/GEMINI.md)

---
Last updated: March 2026
