# Agent Governance

Human-readable governance companion for the runtime rules under [rules/](rules/).

## Scope and Precedence

- `AGENTS.md` is the cross-agent root contract.
- `.claude/` is the primary shared detail layer for agent-facing documentation.
- Nearest scoped files under `docs/` provide subtree-specific local guidance.
- Project manuals under [docs/manuals/](../docs/manuals/) remain the human-facing process layer.

## Canonical Paths

- Specs: [docs/specs/](../docs/specs/)
- PRDs: [docs/prd/](../docs/prd/)
- ADRs: [docs/adr/](../docs/adr/)
- ARDs: [docs/ard/](../docs/ard/)
- Plans: [docs/plans/](../docs/plans/)
- Incidents: [docs/incidents/](../docs/incidents/)
- Runbooks: [docs/runbooks/](../docs/runbooks/)
- Operations: [docs/operations/](../docs/operations/)
- Templates: [templates/](../templates/)

## Documentation Rules

- Use repo-relative Markdown links.
- Do not use absolute file URI links.
- Do not invent build, test, or package-manager commands.
- Treat `.agent/skills/` as optional and runtime-dependent.
- Keep shared runtime rules in `.claude/rules/`, not in long root files.

## Current Repo Facts

- `.agent/rules/` and `.agent/workflows/` exist.
- `.agent/skills/` is not present locally.
- No root `package.json` was found during inspection.
- The retired guides layer should not be reintroduced through new references.
