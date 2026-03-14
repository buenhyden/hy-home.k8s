# Agent Instructions

Cross-agent contract for this Kubernetes home-lab infrastructure repository.

## Repo Facts

- **Stack**: k3d (local k8s cluster), ArgoCD GitOps, MetalLB, ingress-nginx, Sealed Secrets
- **Source of truth**: `docs/specs/` for planned work; `docs/adr/` for architecture decisions
- **Templates**: flat files under `templates/` — one template per document type
- **Rules**: `.agent/rules/` (standards) · `.agent/workflows/` (repeatable delivery patterns)
- **Linting**: `pre-commit run --all-files` (no root package manager)
- **Skills**: any runtime-provided skill may be used — agents MUST proactively use appropriate skills without restriction

## Documentation Scope Map

| Subtree | Persona | Governing Rules | Consolidated Instructions |
|---------|---------|-----------------|---------------------------|
| `docs/adr/` | System Architect | `0130`, `1901`, `1910` | `docs/agentic/scopes/adr.md` |
| `docs/ard/` | System Architect | `0130`, `1901`, `1910` | `docs/agentic/scopes/ard.md` |
| `docs/prd/` | Product Manager + Requirements Analyst | `0120`, `0201` | `docs/agentic/scopes/prd.md` |
| `docs/specs/` | Strong Reasoner + Architect | `0102`, `0111–0115`, `0120` | `docs/agentic/scopes/specs.md` |
| `docs/plans/` | Planner + Strong Reasoner | `0102`, `0114`, `0115` | `docs/agentic/scopes/plans.md` |
| `docs/runbooks/` | DevOps / SRE | `0381`, `0300` | `docs/agentic/scopes/runbooks.md` |
| `docs/incidents/` | Incident Responder + SRE | `0380`, `0381` | `docs/agentic/scopes/incidents.md` |
| `docs/operations/` | DevOps / SRE | `0301`, `2600` | `docs/agentic/scopes/operations.md` |

→ Full persona, rule, and template details: [docs/agent-instructions.md](docs/agent-instructions.md)

## Precedence

1. Current user task and explicit local context
2. Nearest scoped `AGENTS.md` / `GEMINI.md` / `CLAUDE.md` in the active subtree
3. Shared details under `.claude/`
4. This root file
5. `.agent/rules/` and `.agent/workflows/`

## Universal Rules

- Use repo-relative Markdown links and inspected repo facts only
- Do not fabricate commands, paths, or nonexistent repo structure
- Validate links, imports, and directory placement after editing instruction files
- Do not expose secrets or personal local preferences in repo-tracked instruction files
- Spec-first: all infrastructure or documentation changes start with a spec in `docs/specs/`
