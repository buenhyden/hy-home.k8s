# Local Runtime Baseline (Gemini)

This file is the runtime baseline for local agent execution via Gemini in `hy-home.k8s`, a
WSL2+k3d cluster repository managed through ArgoCD GitOps.

## Purpose

- Anchor the local `.agents/**` runtime contract as a shared surface and moderate-shim.
- Point agents to the canonical governance documents.
- Make repo-backed GitOps validation the default execution model.

## Loading Order

Start from the repository gateway files, then follow the governance JIT sequence:

1. `AGENTS.md`
2. `docs/00.agent-governance/rules/bootstrap.md`
3. `docs/00.agent-governance/rules/preflight-checklist.md`
4. `docs/00.agent-governance/rules/persona.md`
5. `docs/00.agent-governance/scopes/<layer>.md`
6. `docs/00.agent-governance/providers/gemini.md`
7. `docs/00.agent-governance/memory/progress.md`
8. `docs/00.agent-governance/rules/postflight-checklist.md`

## Workspace Contract

- Plan and implement from repo evidence: `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/99.templates`, `gitops/`, `infrastructure/`, `scripts/`, and current validators.
- Record repo-changing work progress and reusable memory in `docs/00.agent-governance/memory/progress.md`.
- Use `docs/00.agent-governance/rules/agentic.md` as the Agent-first Engineering execution contract.
- The `.agents/` folder is a git-tracked shared surface and moderate-shim for Gemini.
- The `.agents/agents/*.md` files serve as Gemini agent reference indexes.
- Gemini operates under equivalent behavior contracts to Claude hooks (e.g., preflight, postflight, validation hooks).
- Keep infrastructure changes repo-backed. Agents and subagents do not mutate live clusters by default; human-approved bootstrap or break-glass actions are operator-bound and must record scope, rollback, and verification evidence.
- Do not write plaintext Kubernetes secrets.
- Use `RTK.md` as cross-agent SSOT for shell commands.

## Runtime Roster

- Agents & Skills: see `docs/00.agent-governance/harness-catalog.md`

## Relationship to Gateway Files

- `AGENTS.md` is the shared gateway contract.
- Root `GEMINI.md` is a thin provider shim pointing here.
- This file is the local runtime baseline for Gemini, not a replacement for shared governance policy.
