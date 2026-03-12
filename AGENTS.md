# Agent Instructions
Cross-agent root contract for this repository's documentation, planning, and operations work.

## Quick Reference

- Shared detail layer: [.claude/README.md](.claude/README.md)
- Companion docs: [.claude/governance.md](.claude/governance.md), [.claude/lifecycle.md](.claude/lifecycle.md), [.claude/repo-navigation.md](.claude/repo-navigation.md)
- Runtime entrypoints: [.claude/CLAUDE.md](.claude/CLAUDE.md), [.claude/GEMINI.md](.claude/GEMINI.md)

## Repo Facts

- This repo is documentation-heavy and governance-heavy; `docs/specs/` is the implementation source of truth for planned work.
- The 6 core pillars are Security (`2200`), Performance (`2300`), Observability (`2600`), Compliance (`2400`), Documentation (`2100`), and Localization (`2500`).
- Canonical work domains live under `docs/`: `adr`, `ard`, `prd`, `plans`, `specs`, `incidents`, `runbooks`, `operations`, `manuals`.
- Canonical templates are flat files under `templates/`.
- Nearest scoped instruction files under `docs/` take precedence for local work.

## Precedence

1. Current user task and explicit local context
2. Nearest scoped `AGENTS.md`, `GEMINI.md`, or `CLAUDE.md` in the active subtree
3. Shared agent files under `.claude/`
4. Project manuals under `docs/manuals/`
5. This root file
6. `.agent/rules/` and `.agent/workflows/`

## Verified Commands

```bash
git status --short
find .agent/rules -maxdepth 2 -type f | sort
find .agent/workflows -maxdepth 2 -type f | sort
find templates -maxdepth 2 -type f | sort
rg --files docs
```

No root package manifest was found during inspection, so do not invent root build, test, or package-manager commands.

## Universal Rules

- Use repo-relative Markdown links and inspected repo facts only.
- Keep root instruction files concise and push shared detail into `.claude/` or scoped files.
- Validate links, imports, and path references after instruction changes.
- Do not expose secrets or personal local preferences in repo-tracked instruction files.
- Do not fabricate commands, paths, or nonexistent repo structure.
- Use runtime-provided skills first; inspect `.agent/skills/` only if that directory exists locally.
- Use the persona mappings in `.claude/rules/personas.md` together with the nearest scoped doc file for the active subtree.

---
Last updated: March 2026
