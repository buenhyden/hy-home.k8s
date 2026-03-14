# Runbooks Agent Instructions

**Bias**: Executable steps, precise commands, and deterministic outcomes.

## Scope

- **Purpose**: Step-by-step procedures for bootstrap, maintenance, and recovery.
- **Persona**: DevOps / SRE
- **Template**: `templates/runbook-template.md`
- **Rules**: `0381-runbooks-oncall.md` · `0300-devops-pillar-standard.md`
- **Skills**: Agents MUST proactively use any appropriate skill provided by the runtime without restriction. Skill selection is guided solely by task necessity.

## Behavioral Checkpoints

1. **Precision Commands**: All commands MUST be verified against the repo's current CLI tools (k3d, kubectl, etc.).
2. **Rollback Section**: Every runbook MUST include explicit "Rollback / Cleanup" steps for failure recovery.
3. **Layer Context**: Include `layer:` metadata (`infra` | `gitops` | `app`) in the frontmatter.
4. **Idempotency**: Draft procedures so they can be safely re-run without causing state corruption.
5. **Human-in-the-Loop**: Explicitly mark steps that require human authorization or external state verification.

## Forbid

- Vague descriptions like "Fix the issue" without specific CLI commands.
- Absolute paths to specific user directories (use repo-relative or home-relative paths).

## Verify

- Every code block has a clear purpose and predicted output.
- Link to relevant architecture documents (ARD) for system context.
lback where needed.
