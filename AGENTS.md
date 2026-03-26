# Agent Framework Contract

Thin gateway for `hy-home.k8s` agent execution.

## Protocol

Load governance JIT in this order:

1. [bootstrap.md](docs/00.agent-governance/rules/bootstrap.md)
2. [preflight-checklist.md](docs/00.agent-governance/rules/preflight-checklist.md)
3. [persona.md](docs/00.agent-governance/rules/persona.md)
4. matching scope in `docs/00.agent-governance/scopes/`
5. provider notes in `docs/00.agent-governance/providers/`
6. [postflight-checklist.md](docs/00.agent-governance/rules/postflight-checklist.md) before completion

## Directives

- Respond to users in Korean.
- Keep `docs/00.agent-governance/*` in English.
- Keep human-facing READMEs in Korean.
- Treat `docs/01~99` as authored SSoT; modify only when explicitly requested by a human.
- Keep gateway files minimal and avoid duplicating rule text.
