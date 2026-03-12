# Agent Governance

This manual defines shared policy for agent-facing documentation in this repository. It extends [AGENTS.md](../AGENTS.md) and should be preferred over generic external defaults when it is more specific.

## Scope and Precedence

- `AGENTS.md` is the root constitution and index.
- This manual holds shared detailed governance that does not belong in model-specific files.
- [GEMINI.md](../GEMINI.md) and [CLAUDE.md](../CLAUDE.md) should only add model-specific execution behavior.
- Project manuals and guides under [docs/manuals/](../docs/manuals/) and [docs/guides/](../docs/guides/) override generic guidance when they are more specific.

## Canonical Paths

Use these paths consistently in touched documentation:

- Specs: [docs/specs/](../docs/specs/)
- PRDs: [docs/prd/](../docs/prd/)
- ADRs: [docs/adr/](../docs/adr/)
- ARDs: [docs/ard/](../docs/ard/)
- Runbooks: [docs/runbooks/](../docs/runbooks/)
- Templates: [templates/](../templates/)

## Resolved Contradictions

- Legacy bare spec-directory references are stale for this repo. Use `docs/specs/` instead.
- Legacy nested template paths are stale for this repo. Use the flattened files in `templates/*.md`.
- Skill discovery must be conditional. Use runtime-provided skills when available, and only inspect `.agent/skills/` if that directory actually exists in the repository.

## Documentation Rules

- Use repo-relative Markdown links. Do not use absolute file URI links.
- Do not invent build, test, or package-manager commands that are not grounded in the current repo.
- Document only commands and paths confirmed by inspection.
- Keep root files short and index-like; move shared detail into linked manuals.
- Prefer repo facts and current directory structure over inherited template wording.

## Current Repo Facts That Matter

- The repo contains `.agent/rules/` and `.agent/workflows/`.
- The repo does not currently contain `.agent/skills/`.
- The repo did not expose a root `package.json` during inspection.
- The repo already uses `docs/manuals/` as a project-specific governance override layer.

## Out of Scope

This refactor does not fix stale references elsewhere in the repo, including `ARCHITECTURE.md`, `OPERATIONS.md`, and older docs under `docs/specs/` and `docs/guides/`.
