# AI Agent Governance Hub

Central governance for AI agents operating in `hy-home.k8s`.

## Directory Structure

- `rules/`: global policy, quality gates, persona routing, documentation protocol.
- `scopes/`: layer-specific execution rules (product, architecture, backend, frontend, infra, ops, security, QA, docs, meta).
- `providers/`: model-specific notes for Claude and Gemini.
- `memory/`: reusable lessons and non-obvious operational findings.

## Runtime Protocol

Start from repository root shims (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) and load rules JIT:
1. `rules/bootstrap.md`
2. `rules/persona.md`
3. `scopes/<layer>.md`
4. `providers/<engine>.md`
5. `memory/` entries when relevant

## Compliance

- Keep all files under `docs/00.agent-governance/` in English.
- Keep user-facing responses in Korean.
- Treat `docs/01~99` as authored SSoT and non-mutable unless explicitly approved by humans.
