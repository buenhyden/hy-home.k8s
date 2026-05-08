# Agent Bootstrap Governance (March 2026)

Universal entry point for all agents in `hy-home.k8s`.

## Core Rules

- Workspace purpose: this repository is a WSL2+k3d home-lab platform managed through ArgoCD GitOps.
- Plan from repo-backed evidence: `docs/01-10`, `docs/90.references`, `docs/99.templates`, `gitops/`, `infrastructure/`, `scripts/`, tests, and current manifests.
- Use [Agentic Execution Rules](agentic.md) as the Agent-first Engineering contract for non-trivial work.
- Use spec-driven execution anchored to `docs/01.prd/` and `docs/04.specs/`.
- Load governance just-in-time, not full-repository-first.
- Complete [Preflight Checklist](preflight-checklist.md) before substantial work.
- Complete [Postflight Checklist](postflight-checklist.md) before final response.
- GitOps-first is mandatory: do not mutate the live cluster directly unless a human explicitly approves an emergency path.
- Define validation evidence before editing, and report unavailable tools or skipped live checks.
- `.codex/agents/*.toml` mirrors `.claude/agents/*.md`; keep both runtime surfaces aligned.
- **In-place refactor only.** Modify existing files rather than creating new ones unless explicitly requested by a human.

## JIT Loading Sequence

1. Load `rules/bootstrap.md`.
2. Load `rules/preflight-checklist.md`.
3. Resolve persona via `rules/persona.md`.
4. Load one layer scope from `scopes/`.
5. Load provider notes from `providers/` when needed.
6. Load `memory/` entries only if relevant.
7. Load `rules/postflight-checklist.md` before completion.

## Stage Taxonomy

Use [stage-authoring-matrix.md](stage-authoring-matrix.md) as the canonical authoring matrix for stages `00-10, 90, 99`.

## Definition of Done for Governance Tasks

- Policy changes are reflected in the correct file under `rules/`, `scopes/`, or `providers/`.
- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` remain thin gateways.
- English-only policy is preserved under `docs/00.agent-governance/`.
- References to checklist and matrix docs remain valid.
- GitOps-first and no-direct-cluster-mutation constraints remain visible.
- Validation evidence or limitations are reported.
- No new files created without explicit human request.
