---
title: 'Agent Bootstrap Governance (March 2026)'
type: governance/reference
status: active
owner: platform
updated: 2026-07-14
---

# Agent Bootstrap Governance (March 2026)

## Overview

Universal entry point for all agents in `hy-home.k8s`.

### Core Rules

- Workspace purpose: this repository is a WSL2+k3d home-lab platform managed through ArgoCD GitOps.
- Plan from repo-backed evidence: `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/98.archive`, `docs/99.templates`, `gitops/`, `infrastructure/`, `scripts/`, tests, and current manifests.
- Use [Agentic Execution Rules](agentic.md) as the Agent-first Engineering contract for non-trivial work.
- Use spec-driven execution anchored to `docs/01.requirements/` and `docs/03.specs/`.
- Use `docs/00.agent-governance/memory/progress.md` as the agent progress and reusable memory ledger for repo-changing work.
- Use `docs/99.templates/templates/common/memory.template.md` for standalone files under `docs/00.agent-governance/memory/`, and update `progress.md` in the same change.
- Load governance just-in-time, not full-repository-first.
- Complete [Preflight Checklist](preflight-checklist.md) before substantial work.
- Complete [Postflight Checklist](postflight-checklist.md) before final response.
- GitOps-first is mandatory: do not mutate the live cluster directly unless a human explicitly approves an emergency path.
- Define validation evidence before editing, and report unavailable tools or skipped live checks.
- `.claude/agents/*.md` and `.codex/agents/*.toml` are provider-native role adapters; `.agents/agents/*.md` is the local/Antigravity adapter surface. Keep their role, scope imports, guardrails, handoff, and postflight statically aligned while preserving surface-specific metadata keys. The `.agents/` folder remains the git-tracked shared asset and local adapter owner; it is not Gemini CLI native configuration. Gemini CLI reserves `.gemini/agents/**` and `.gemini/settings.json`, which are absent and `DEFER` pending a separate approved PRD/ARD/Spec/Plan/Task or at minimum Spec/Plan/Task.
- **In-place refactor only.** Modify existing files rather than creating new ones unless explicitly requested by a human.

## Authority Boundary

This entry point may select and order canonical governance owners; it does not
own provider-native permissions, document-profile schemas, live-cluster
approval, or stage implementation content. Route provider behavior to
`providers/`, document structure to Stage 99 support contracts, and protected
actions to [`approval-boundaries.md`](approval-boundaries.md). Conflicting or
missing authority requires human clarification before execution.

## Governance Context

### JIT Loading Sequence

1. Load `rules/bootstrap.md`.
2. Load `rules/preflight-checklist.md`.
3. Resolve persona via `rules/persona.md`.
4. Load one layer scope from `scopes/`.
5. Load provider notes from `providers/` when needed.
6. Load `memory/progress.md` for current progress, handoff, and reusable memory context.
7. Load `rules/postflight-checklist.md` before completion.

### Stage Taxonomy

Use [stage-authoring-matrix.md](stage-authoring-matrix.md) as the canonical authoring matrix for `00.agent-governance`, `01.requirements`, `02.architecture`, `03.specs`, `04.execution`, `05.operations`, `90.references`, `98.archive`, and `99.templates`.

## Current Contract

### Definition of Done for Governance Tasks

- Policy changes are reflected in the correct file under `rules/`, `scopes/`, or `providers/`.
- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` remain thin gateways.
- English-only policy is preserved under `docs/00.agent-governance/`.
- References to checklist and matrix docs remain valid.
- Repo-changing work has a `memory/progress.md` entry, and standalone memory files use `docs/99.templates/templates/common/memory.template.md`.
- GitOps-first and no-direct-cluster-mutation constraints remain visible.
- Validation evidence or limitations are reported.
- No new files created without explicit human request.

## Validation and Refresh

Run `bash scripts/validate-repo-quality-gates.sh .` after changing the JIT
sequence, gateways, or governance routes, then run
`python3 scripts/validate-links-and-owners.py --root . --mode strict` for owner
and link integrity. Review bootstrap whenever a gateway, scope, provider,
progress owner, or postflight route changes; live and provider-runtime behavior
requires separate evidence.

## Related Documents

- [Preflight Checklist](preflight-checklist.md)
- [Persona Protocol](persona.md)
- [Postflight Checklist](postflight-checklist.md)
- [Harness Approval Boundaries](approval-boundaries.md)
- [Stage Authoring Matrix](stage-authoring-matrix.md)
