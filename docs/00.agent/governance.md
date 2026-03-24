---
layer: "meta"
---

# Agent Governance

Human-readable governance companion for the runtime rules under [rules/](rules/).

## Scope and Precedence

- `AGENTS.md` is the cross-agent root contract.
- `docs/00.agent/` is the primary shared detail layer for agent-facing documentation.
- Nearest scoped files under `docs/` provide subtree-specific local guidance.
- Project manuals in [docs/08.ops/](../08.ops/) contain the human-facing processes.

## Canonical Paths

- PRDs: [docs/01.prd/](../01.prd/) (Flattened with `layer:` metadata)
- ADRs: [docs/02.adr/](../02.adr/) (Flattened with `layer:` metadata)
- ARDs: [docs/03.ard/](../03.ard/) (Flattened with `layer:` metadata)
- Specs: [docs/04.specs/](../04.specs/) (Flattened with `layer:` metadata)
- Plans: [docs/05.plans/](../05.plans/)
- Runbooks: [docs/08.ops/](../08.ops/)
- Operations: [docs/08.ops/](../08.ops/)
- Incidents: [docs/10.inc/](../10.inc/)
- Templates: [templates/](../../templates/)
- **Workflows**: [workflows/](../../.agent/workflows/).

## Skill Selection

- **No Restriction**: Agents MUST proactively use any appropriate skill provided by the runtime.
- **Goal-Oriented**: Skill selection should align with the task objective.

## Documentation Rules

- Use repo-relative Markdown links.
- Do not use absolute file URI links.
- Do not invent build, test, or package-manager commands.
- Treat `.agent/skills/` as optional and runtime-dependent.
- Every doc MUST include `layer:` metadata.

## Current Repo Facts

- `.agent/rules/` and `.agent/workflows/` exist.
- `.agent/skills/` is not present locally.
- No root `package.json` was found during inspection.
- The retired guides layer should not be reintroduced.
