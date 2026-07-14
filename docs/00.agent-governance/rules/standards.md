---
title: 'AI Agent Standards (March 2026)'
type: governance/reference
status: draft
owner: platform
updated: 2026-07-13
---

# AI Agent Standards (March 2026)

## Overview

Global standards for all agents in this repository.

## Authority Boundary

### Documentation Boundary Policy

- Treat `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/98.archive`, and `docs/99.templates` as authored source of truth by default.
- Changes to `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/98.archive`, and `docs/99.templates` must be explicitly requested by a human.
- Route governance evolution to `docs/00.agent-governance/*`.
- Do not introduce parallel authored trees such as `docs/superpowers/**`; route outputs into the official stage folders.

### Security & Infrastructure Policy

- GitOps-first: all infra changes go through repository review and ArgoCD reconciliation. Agents and subagents do not mutate live clusters; human-approved bootstrap or break-glass actions are operator-bound and must record scope, rollback, and verification evidence.
- Secrets: never write plaintext Kubernetes secrets.

## Governance Context

### Token and Context Policy

- Keep root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) minimal.
- Recommended max length for each root shim: 40 lines.
- Avoid duplicated policy text across gateway files.
- Do not embed long RTK, graphify, catalog, or role-separation blocks in root shims.
- Use JIT loading via `bootstrap -> preflight -> persona -> scope -> provider -> progress -> postflight`.
- Keep the instruction hierarchy inside repository gateway files plus runtime governance assets only:
  - root shims: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`
  - runtime bridge: `.claude/**`, `.codex/**`, and `.agents/**`
  - local baselines: `.claude/CLAUDE.md`, `.codex/CODEX.md`, `.agents/GEMINI.md`
  - policy SSoT: `docs/00.agent-governance/**`
- Do not introduce GitHub-native instruction files such as `.github/copilot-instructions.md` or `.github/instructions/**/*.instructions.md` in this repository.
- RTK guidance belongs in `RTK.md`, not in root shim bodies.

### Workspace Alignment

Infrastructure assumptions must match current workspace assets:

- WSL2+k3d home-lab platform
- ArgoCD repo-backed GitOps workflow
- `infrastructure/`
- `gitops/`
- `scripts/`
- `tests/`
- `.claude/`
- `.codex/`
- `.agents/`

`.claude/agents/*.md`, `.agents/agents/*.md`, and `.codex/agents/*.toml` are provider-native role adapters. They must keep the same role, scope imports, guardrails, handoff, and postflight requirements while preserving provider-specific metadata, tool, and permission syntax.

## Current Contract

### Language Policy

- `docs/00.agent-governance/*`: English only.
- User-facing responses: Korean only.
- Human-facing top-level docs (`README.md`, `docs/README.md`, stage READMEs): Korean.
- Technical specs under `docs/03.specs/**/spec.md`: English.
- Execution plans under `docs/04.execution/plans/*.md`: English.
- Task records under `docs/04.execution/tasks/*.md`: English.
- Operations guides, policies, runbooks, and incident records may use Korean
  for human readers, but AI-agent execution sections and tool/prompt contracts
  inside them must remain English.
- Reference documents may use Korean for human-facing overview and lookup
  explanation, but authority boundaries, source/freshness metadata, generated
  index contracts, version support boundaries, and AI-agent routing notes
  should remain English-first.

### Quality Policy

- Always keep checklist and matrix references valid:
  - `rules/preflight-checklist.md`
  - `rules/postflight-checklist.md`
  - `rules/stage-authoring-matrix.md`
  - `rules/stage-checklists.md`
- Keep scope and provider docs action-oriented and non-duplicative.
- In-place refactor only; no file proliferation without explicit human request.

## Validation and Refresh

Run `bash scripts/validate-repo-quality-gates.sh .` after changing global
language, context, gateway, security, or taxonomy standards. Run the strict
link/owner validator when routes change and the role-semantic plus roster checks
when adapter parity changes. Reconcile this summary with its canonical owner
before adding a new rule; provider-runtime and live claims require separate
evidence.

## Related Documents

- [Bootstrap Governance](bootstrap.md)
- [Documentation Protocol](documentation-protocol.md)
- [Agent Quality Standards](quality-standards.md)
- [Agentic Execution Rules](agentic.md)
