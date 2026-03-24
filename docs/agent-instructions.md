---
layer: "meta"
---
# Agent Instructions Hub

**Bias**: Use this subtree for durable project knowledge. Keep file category and `layer:` metadata correct.

@./agentic/agent-instructions.md

**Skills**: Any runtime-provided skill may be used. Agents MUST proactively use appropriate skills without restriction.
**Rules source**: `.agent/rules/` — categorized standards for each persona.
**Workflows source**: `.agent/workflows/` — repeatable delivery and troubleshooting patterns.

## Documentation Scope Map

| Category | Persona | Consolidated Instructions | Governing Rules |
|----------|---------|---------------------------|-----------------|
| `docs/adr/` | System Architect | `docs/agentic/scopes/adr.md` | `0130`, `1901`, `1910` |
| `docs/ard/` | System Architect | `docs/agentic/scopes/ard.md` | `0130`, `1901`, `1910` |
| `docs/prd/` | Product Manager | `docs/agentic/scopes/prd.md` | `0120`, `0201` |
| `docs/specs/` | Strong Reasoner | `docs/agentic/scopes/specs.md` | `0102`, `0111–0113`, `0120` |
| `docs/plans/` | Planner | `docs/agentic/scopes/plans.md` | `0102`, `0114`, `0115` |
| `docs/runbooks/` | DevOps / SRE | `docs/agentic/scopes/runbooks.md` | `0300`, `0325`, `0335` |
| `docs/incidents/` | SRE | `docs/agentic/scopes/incidents.md` | `0380`, `0381` |
| `docs/postmortems/` | SRE | `docs/agentic/scopes/operations.md` | `0380`, `0385` |
| `docs/manuals/` | End User / Dev | `docs/agentic/scopes/operations.md` | `0301`, `2100`, `2600` |

---

## Flattened Structure Rule

All files within the categories above must reside directly in the category folder (e.g., `docs/prd/[filename].md`).
Distinguish between infrastructure, GitOps, or application layers using the `layer:` metadata in frontmatter.

---

## Universal Rules (Cross-Subtree)

| Category | Rules |
|----------|-------|
| Security | `2200-security-pillar.md` · `2205-devsecops.md` · `2207-security-checklist.md` |
| Observability | `2600-observability-pillar.md` · `2610-observability-strategy.md` |
| Documentation | `2100-documentation-pillar.md` · `2110-doc-core-std.md` · `0160-documentation-standards.md` |
| Engineering | `0104-engineering-standard.md` · `0140-engineering-excellence-standard.md` |
| DevOps / k8s | `0325-infrastructure-kubernetes.md` · `0335-gitops-standard.md` · `0326-ingress-tls.md` |
