# Agent Framework Contract

Thin gateway for `hy-home.k8s` agent execution.

## §1 Bootstrap

Load governance just-in-time in this order:

1. [bootstrap.md](docs/00.agent-governance/rules/bootstrap.md)
2. [preflight-checklist.md](docs/00.agent-governance/rules/preflight-checklist.md)
3. [persona.md](docs/00.agent-governance/rules/persona.md)
4. matching scope in `docs/00.agent-governance/scopes/`
5. provider notes in `docs/00.agent-governance/providers/`
6. [progress.md](docs/00.agent-governance/memory/progress.md)
7. [postflight-checklist.md](docs/00.agent-governance/rules/postflight-checklist.md)

Runtime baseline: [`.claude/CLAUDE.md`](.claude/CLAUDE.md)

## §2 Constraints

- Respond to users in Korean.
- Keep `docs/00.agent-governance/**`, `.claude/**`, and `.codex/**` runtime/policy docs in English.
- Keep human-facing READMEs in Korean.
- Treat `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, and `docs/99.templates` as authored SSoT; modify only when explicitly requested by a human.
- Keep gateway files minimal and route detailed policy to governance docs.
- GitOps-first: all infra changes go through repository review and ArgoCD reconciliation; never run direct cluster mutation such as `kubectl apply`.
- Secrets: never write plaintext Kubernetes secrets.
- In-place refactor only; no file proliferation without explicit human request.

## §3 Routing

- Agents, skills, models, and `.codex` mirrors: [harness-catalog.md](docs/00.agent-governance/harness-catalog.md)
- Delegation and handoff rules: [subagent-protocol.md](docs/00.agent-governance/subagent-protocol.md)
- Agent-first execution rules: [agentic.md](docs/00.agent-governance/rules/agentic.md)
- Documentation protocol: [documentation-protocol.md](docs/00.agent-governance/rules/documentation-protocol.md)
- Generated document routing: [document-stage-routing.md](docs/00.agent-governance/rules/document-stage-routing.md)
- Git workflow: [git-workflow.md](docs/00.agent-governance/rules/git-workflow.md)
- Tooling note: [RTK.md](RTK.md)
