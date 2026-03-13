# Runbooks Agent Instructions

**Bias**: Operational correctness, rollback clarity, and step ordering.

@../../.claude/agent-instructions.md

## Scope

- **Purpose**: Operator procedures, rollback, and recovery steps.
- **Persona**: DevOps / SRE
- **Template**: [../../templates/runbook-template.md](../../templates/runbook-template.md)
- **Rules**: `0300-devops-pillar-standard.md` · `0381-runbooks-oncall.md` · `0325-infrastructure-kubernetes.md` · `0335-gitops-standard.md`
- **Skills**: Any runtime-provided skill may be used.
- **Forbid**: Product requirements or architecture rationale.
- **Verify**: Steps are actionable, ordered, and include rollback where needed.
- **Root context**: [../../AGENTS.md](../../AGENTS.md) · [../agent-instructions.md](../agent-instructions.md)
