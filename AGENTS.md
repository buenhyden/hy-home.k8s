# Agent Instructions

Cross-agent contract for this Kubernetes home-lab infrastructure repository.

## Repo Facts

- **Stack**: k3d (local k8s cluster), ArgoCD GitOps, MetalLB, ingress-nginx, Sealed Secrets
- **Source of truth**: `docs/specs/` for planned work; `docs/adr/` for architecture decisions
- **Templates**: flat files under `templates/` — one template per document type
- **Rules**: `.agent/rules/` (standards) · `.agent/workflows/` (repeatable delivery patterns)
- **Linting**: `pre-commit run --all-files` (no root package manager)
- **Skills**: any runtime-provided skill may be used — agents MUST proactively use appropriate skills without restriction
- **Metadata**: All documentation MUST include `layer:` metadata in the frontmatter.

## Documentation Scope Map & Lazy Loading

Agents SHOULD only load detailed instructions for the active scope. Identify current scope by the working directory or relevant `docs/` subtree.

| Subtree | Persona | consolidated Instructions (Lazy Load) |
|---------|---------|---------------------------|
| `docs/adr/` | System Architect | `docs/agentic/scopes/adr.md` |
| `docs/ard/` | System Architect | `docs/agentic/scopes/ard.md` |
| `docs/prd/` | Product Manager | `docs/agentic/scopes/prd.md` |
| `docs/specs/` | Architect | `docs/agentic/scopes/specs.md` |
| `docs/plans/` | Planner | `docs/agentic/scopes/plans.md` |
| `docs/runbooks/` | DevOps / SRE | `docs/agentic/scopes/runbooks.md` |
| `docs/incidents/` | Incident Responder | `docs/agentic/scopes/incidents.md` |
| `docs/operations/` | DevOps / SRE | `docs/agentic/scopes/operations.md` |

→ Full persona and rule details: [docs/agent-instructions.md](docs/agentic/agent-instructions.md)

## Precedence

1. Current user task and explicit local context
2. Scope-specific instructions (see Map above)
3. `.claude/` shared details
4. This root file

## Universal Rules

- Use repo-relative Markdown links and inspected repo facts only
- Do not fabricate commands, paths, or nonexistent repo structure
- Spec-first: all changes start with a spec in `docs/specs/`
- Performance: agents MUST proactively use any appropriate skill without restriction.
