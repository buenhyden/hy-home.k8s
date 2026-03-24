---
layer: "meta"
---
# Agent Governance

Human-readable governance companion for the runtime rules under [rules/](rules/).

## Scope and Precedence

- `AGENTS.md` is the cross-agent root contract.
- `.claude/` is the primary shared detail layer for agent-facing documentation.
- Nearest scoped files under `docs/` provide subtree-specific local guidance.
- Project manuals in [docs/operations/](../operations/) contain the human-facing processes.

## Canonical Paths

- Specs: [docs/specs/](../specs/) (Flattened with `layer:` metadata)
- PRDs: [docs/prd/](../prd/) (Flattened with `layer:` metadata)
- ADRs: [docs/adr/](../adr/) (Flattened with `layer:` metadata)
- ARDs: [docs/ard/](../ard/) (Flattened with `layer:` metadata)
- Plans: [docs/plans/](../plans/)
- Incidents: [docs/operations/incidents/](../operations/incidents/)
- Runbooks: [docs/runbooks/](../runbooks/) (Flattened with `layer:` metadata)
- Operations: [docs/operations/](../operations/)
- Templates: [templates/](../../templates/)
- **Collaborative Writing**: [collaboration-guide.md](../operations/collaboration-guide.md).
- **Quality Assurance**: [qa-security-guide.md](../operations/qa-security-guide.md).
- **Documentation Validation**: [2026-03-15-documentation-validation.md](../runbooks/2026-03-15-documentation-validation.md).
- **Incident Management**: [2026-03-19-incident-management.md](../operations/2026-03-19-incident-management.md).
- **Workflows**: [workflows/](../../.agent/workflows/).

## Skill Selection

- **No Restriction**: Agents MUST proactively use any appropriate skill provided by the runtime.
- **Goal-Oriented**: Skill selection should align with the task objective.

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
