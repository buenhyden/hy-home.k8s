# AI Agent Governance Hub

Central governance for AI agents operating in `hy-home.k8s`.

## Directory Structure

- `rules/`: global policy, quality gates, persona routing, documentation protocol, and execution checklists.
- `scopes/`: layer-specific execution rules (product, architecture, backend, frontend, infra, ops, security, QA, docs, meta).
- `providers/`: model-specific notes for Claude and Gemini.
- `memory/`: reusable lessons and non-obvious operational findings.

## Runtime Protocol

Start from repository root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) and load rules JIT:

1. `rules/bootstrap.md`
2. `rules/preflight-checklist.md`
3. `rules/persona.md`
4. `scopes/<layer>.md`
5. `providers/<engine>.md`
6. `rules/postflight-checklist.md`
7. `memory/` entries when relevant

## Governance Entry Points

- [Preflight Checklist](rules/preflight-checklist.md)
- [Postflight Checklist](rules/postflight-checklist.md)
- [Stage Authoring Matrix (00-11)](rules/stage-authoring-matrix.md)
- [Stage Checklists](rules/stage-checklists.md)

## Compliance

- Keep all files under `docs/00.agent-governance/` in English.
- Keep user-facing responses in Korean.
- Treat `docs/01~99` as authored SSoT unless a human explicitly requests changes.
