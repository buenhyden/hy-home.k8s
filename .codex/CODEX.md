# Local Runtime Baseline (Codex)

This file is the runtime baseline for local agent execution via Codex (GPT) in `hy-home.k8s`, a
WSL2+k3d cluster repository managed through ArgoCD GitOps.

## Purpose

- Anchor the local `.codex/**` runtime contract.
- Point agents to the canonical governance documents.
- Make repo-backed GitOps validation the default execution model.

## Loading Order

Start from the repository gateway files, then follow the governance JIT sequence:

1. `AGENTS.md`
2. `docs/00.agent-governance/rules/bootstrap.md`
3. `docs/00.agent-governance/rules/preflight-checklist.md`
4. `docs/00.agent-governance/rules/persona.md`
5. `docs/00.agent-governance/scopes/<layer>.md`
6. `docs/00.agent-governance/providers/codex.md`
7. `docs/00.agent-governance/memory/progress.md`
8. `docs/00.agent-governance/rules/postflight-checklist.md`

## Workspace Contract

- Plan and implement from repo evidence: `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/99.templates`, `gitops/`, `infrastructure/`, `scripts/`, and current validators.
- Record repo-changing work progress and reusable memory in `docs/00.agent-governance/memory/progress.md`.
- Use `docs/00.agent-governance/rules/agentic.md` as the Agent-first Engineering execution contract.
- Treat `.codex/agents/*.toml` as Codex mirrors of the primary agent definitions; keep them aligned.
- Treat `.codex/hooks.json` as Codex event wiring for repo-local context and validation hooks, not as an equivalent permission gate to Claude's `settings.json`.
- Use `RTK.md` as cross-agent SSOT for shell commands.

## Codex/GPT Capabilities & Constraints

- **System Context**: Codex heavily utilizes `.toml` for configuration and function mapping.
- **Skill Usage**: Ensure `/imp` style prompts are mapped internally to Codex tool execution behaviors if native tool mapping is not present.
- **Code Assistance**: Prioritize inline completions and context-aware suggestions during coding tasks.

## Runtime Roster

- Agents & Skills: see `docs/00.agent-governance/harness-catalog.md`

## Relationship to Gateway Files

- `AGENTS.md` is the shared gateway contract.
- This file is the local runtime baseline for Codex, not a replacement for shared governance policy.
