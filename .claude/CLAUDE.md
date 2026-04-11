# Local Runtime Baseline

This file is the runtime baseline for local agent execution in `hy-home.k8s`.

## Purpose

- Anchor the local `.claude/**` runtime contract.
- Point agents to the canonical governance documents.
- Keep runtime roster and model hierarchy easy to resolve without duplicating policy text.

## Loading Order

Start from the repository gateway files, then follow the governance JIT sequence:

1. `AGENTS.md`
2. `docs/00.agent-governance/rules/bootstrap.md`
3. `docs/00.agent-governance/rules/preflight-checklist.md`
4. `docs/00.agent-governance/rules/persona.md`
5. `docs/00.agent-governance/scopes/<layer>.md`
6. `docs/00.agent-governance/providers/<provider>.md`
7. `docs/00.agent-governance/rules/postflight-checklist.md`

## Runtime Roster

- Agents: see `docs/00.agent-governance/harness-catalog.md`
- Skills: see `docs/00.agent-governance/harness-catalog.md`

## Model Hierarchy

- `supervisor.md` uses `opus`
- All worker agents use `sonnet`

## Relationship to Gateway Files

- `AGENTS.md` is the shared gateway contract.
- Root `CLAUDE.md` and `GEMINI.md` are thin provider shims.
- This file is the local runtime baseline, not a replacement for governance policy.
