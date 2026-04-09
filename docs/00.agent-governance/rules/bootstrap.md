# Agent Bootstrap Governance (March 2026)

Universal entry point for all agents in `hy-home.k8s`.

## Core Rules

- Use spec-driven execution anchored to `docs/01.prd/` and `docs/04.specs/`.
- Load governance just-in-time, not full-repository-first.
- Complete [Preflight Checklist](preflight-checklist.md) before substantial work.
- Complete [Postflight Checklist](postflight-checklist.md) before final response.
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

Use [stage-authoring-matrix.md](stage-authoring-matrix.md) as the canonical authoring matrix for stages `00~11`.

## Definition of Done for Governance Tasks

- Policy changes are reflected in the correct file under `rules/`, `scopes/`, or `providers/`.
- `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` remain thin gateways.
- English-only policy is preserved under `docs/00.agent-governance/`.
- References to checklist and matrix docs remain valid.
- No new files created without explicit human request.
