# Local Runtime Baseline

This file is the runtime baseline for local agent execution in `hy-home.k8s`, a
WSL2+k3d cluster repository managed through ArgoCD GitOps.

## Purpose

- Anchor the local `.claude/**` runtime contract.
- Point agents to the canonical governance documents.
- Keep runtime roster and model hierarchy easy to resolve without duplicating policy text.
- Make repo-backed GitOps validation the default execution model.

## Loading Order

Start from the repository gateway files, then follow the governance JIT sequence:

1. `AGENTS.md`
2. `docs/00.agent-governance/rules/bootstrap.md`
3. `docs/00.agent-governance/rules/preflight-checklist.md`
4. `docs/00.agent-governance/rules/persona.md`
5. `docs/00.agent-governance/scopes/<layer>.md`
6. `docs/00.agent-governance/providers/<provider>.md`
7. `docs/00.agent-governance/memory/progress.md`
8. `docs/00.agent-governance/rules/postflight-checklist.md`

## Workspace Contract

- Plan and implement from repo evidence: `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/99.templates`, `gitops/`, `infrastructure/`, `scripts/`, and current validators.
- Record repo-changing work progress and reusable memory in `docs/00.agent-governance/memory/progress.md`.
- Use `docs/00.agent-governance/rules/agentic.md` as the Agent-first Engineering execution contract.
- Keep infrastructure changes repo-backed; never mutate the live cluster directly unless a human explicitly approves an emergency path.
- Do not write plaintext Kubernetes secrets.
- Treat `.codex/agents/*.toml` as Codex mirrors of `.claude/agents/*.md`; keep both sides aligned.

## Runtime Roster

- Agents: see `docs/00.agent-governance/harness-catalog.md`
- Skills: see `docs/00.agent-governance/harness-catalog.md`

## Validation and Tooling

- Use `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, `scripts/*.sh`, and `infrastructure/tests/*.sh` as validation sources.
- Use `RTK.md` for shell-command guidance. If `rtk` is not on PATH, run the underlying command directly and report the limitation.
- If `graphify-out/GRAPH_REPORT.md` exists, read it before architecture or codebase answers. If graphify data or the `graphify` CLI is unavailable, use repo inspection and report the limitation.

## Model Hierarchy

- `supervisor.md` uses `opus`
- All worker agents use `sonnet`

## Relationship to Gateway Files

- `AGENTS.md` is the shared gateway contract.
- Root `CLAUDE.md` and `GEMINI.md` are thin provider shims.
- This file is the local runtime baseline, not a replacement for governance policy.
