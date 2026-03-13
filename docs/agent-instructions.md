# Agent Instructions Hub

**Bias**: Use this subtree for durable project knowledge. Keep local path placement and document type correct.

@../.claude/agent-instructions.md

**Skills**: Any runtime-provided skill may be used. Do not restrict skill selection.
**Rules source**: `.agent/rules/` — categorized standards for each persona.
**Workflows source**: `.agent/workflows/` — repeatable delivery and troubleshooting patterns.

## Docs Scope

- **Purpose**: Durable project knowledge, not executable runtime logic.
- **Persona**: Documentation Specialist + Strong Reasoner
- **Templates**: Choose from [../templates/](../templates/) by document type.
- **Rules**: `2100-documentation-pillar.md` · `2110-doc-core-std.md` · `0160-documentation-standards.md`
- **Forbid**: Scripts, runtime code, or operational procedures disguised as reference docs.
- **Verify**: Links resolve and the file is stored in the correct `docs/` subtree.

---

Lazy-loading reference for all documentation scopes in this repository.
Navigate to the relevant section and follow the link to load its full scope context.

---

## Architecture Decisions (`docs/adr/`)

→ [Scope file](adr/AGENTS.md)

| Field | Value |
|-------|-------|
| **Purpose** | Record architecture decisions, rationale, and consequences |
| **Persona** | System Architect |
| **Template** | [`templates/adr-template.md`](../templates/adr-template.md) |
| **Rules** | `0130-architecture-standard.md` · `1901-architecture-rules.md` · `1910-architecture-documentation.md` |
| **Forbid** | Low-level implementation steps without decision context |
| **Verify** | Decision, rationale, and consequences are explicit |

---

## Architecture Reference (`docs/ard/`)

→ [Scope file](ard/AGENTS.md)

| Field | Value |
|-------|-------|
| **Purpose** | Architecture reference structure, boundaries, and diagrams |
| **Persona** | System Architect |
| **Template** | [`templates/ard-template.md`](../templates/ard-template.md) |
| **Rules** | `0130-architecture-standard.md` · `1901-architecture-rules.md` · `1910-architecture-documentation.md` |
| **Forbid** | Decision logs that belong in ADRs |
| **Verify** | Structural references aligned with current repo and ADR context |

---

## Product Requirements (`docs/prd/`)

→ [Scope file](prd/AGENTS.md)

| Field | Value |
|-------|-------|
| **Purpose** | Product requirements, personas, metrics, scope, and acceptance framing |
| **Persona** | Product Manager + Requirements Analyst |
| **Template** | [`templates/prd-template.md`](../templates/prd-template.md) |
| **Rules** | `0120-requirements-and-specifications-standard.md` · `0201-project-management-standard.md` |
| **Forbid** | Technical implementation prescription |
| **Verify** | Metrics are measurable and scope is explicit |

---

## Implementation Specs (`docs/specs/`)

→ [Scope file](specs/AGENTS.md)

| Field | Value |
|-------|-------|
| **Purpose** | Exact implementation instructions, interfaces, file paths, and verification |
| **Persona** | Strong Reasoner + Architect + Requirements Analyst |
| **Templates** | [`templates/spec-template.md`](../templates/spec-template.md) · [`templates/plan-template.md`](../templates/plan-template.md) · [`templates/api-spec-template.md`](../templates/api-spec-template.md) |
| **Rules** | `0102-implementation-plan-standard.md` · `0111-impl-task-spec.md` · `0112-impl-workflow.md` · `0113-impl-traceability.md` · `0120-requirements-and-specifications-standard.md` |
| **Forbid** | Vague product vision without implementation detail |
| **Verify** | Exact paths, interfaces, and verification expectations are explicit |

---

## Execution Plans (`docs/plans/`)

→ [Scope file](plans/AGENTS.md)

| Field | Value |
|-------|-------|
| **Purpose** | Execution roadmaps derived from approved specs |
| **Persona** | Planner + Strong Reasoner |
| **Template** | [`templates/plan-template.md`](../templates/plan-template.md) |
| **Rules** | `0102-implementation-plan-standard.md` · `0114-impl-estimation.md` · `0115-impl-templates.md` |
| **Forbid** | Replacing approved specs as the source of truth |
| **Verify** | Plan references real files, steps, and validation |

---

## Runbooks (`docs/runbooks/`)

→ [Scope file](runbooks/AGENTS.md)

| Field | Value |
|-------|-------|
| **Purpose** | Operator procedures, rollback, and recovery steps |
| **Persona** | DevOps / SRE |
| **Template** | [`templates/runbook-template.md`](../templates/runbook-template.md) |
| **Rules** | `0300-devops-pillar-standard.md` · `0381-runbooks-oncall.md` · `0325-infrastructure-kubernetes.md` · `0335-gitops-standard.md` |
| **Forbid** | Product requirements or architecture rationale |
| **Verify** | Steps are actionable, ordered, and include rollback where needed |

---

## Incidents (`docs/incidents/`)

→ [Scope file](incidents/AGENTS.md)

| Field | Value |
|-------|-------|
| **Purpose** | Incident records, timelines, and follow-up actions |
| **Persona** | Incident Responder + SRE |
| **Templates** | [`templates/incident-template.md`](../templates/incident-template.md) · [`templates/postmortem-template.md`](../templates/postmortem-template.md) |
| **Rules** | `0380-incident-response.md` · `0381-runbooks-oncall.md` · `0385-risk-management-standard.md` · `2600-observability-pillar.md` |
| **Forbid** | Speculative blame or runbook procedures |
| **Verify** | Timeline, impact, response, and follow-up actions are clear |

---

## Operations (`docs/operations/`)

→ [Scope file](operations/AGENTS.md)

| Field | Value |
|-------|-------|
| **Purpose** | Strategic operations agreements and blueprints |
| **Persona** | DevOps / SRE |
| **Template** | [`templates/operations-guide-template.md`](../templates/operations-guide-template.md) |
| **Rules** | `0301-operations-blueprint-standard.md` · `2600-observability-pillar.md` · `2610-observability-strategy.md` · `2620-logging-std.md` · `2630-alerting-std.md` |
| **Forbid** | Detailed runbook steps or incident reports |
| **Verify** | Operational policy stays strategic and distinct from execution playbooks |

---

## Cross-Cutting Rules (All Scopes)

| Category | Rules |
|----------|-------|
| Security | `2200-security-pillar.md` · `2205-devsecops.md` · `2207-security-checklist.md` |
| Observability | `2600-observability-pillar.md` · `2610-observability-strategy.md` |
| Documentation | `2100-documentation-pillar.md` · `2110-doc-core-std.md` · `0160-documentation-standards.md` |
| Engineering | `0104-engineering-standard.md` · `0140-engineering-excellence-standard.md` |
| DevOps / k8s | `0325-infrastructure-kubernetes.md` · `0335-gitops-standard.md` · `0326-ingress-tls.md` |
