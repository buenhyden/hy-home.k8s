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

Local baselines: [`.claude/CLAUDE.md`](.claude/CLAUDE.md), [`.codex/CODEX.md`](.codex/CODEX.md), [`.agents/GEMINI.md`](.agents/GEMINI.md)

## §2 Constraints

All detailed constraints, including Language Policy, GitOps-first execution, Secret handling, and In-place refactoring rules, are documented in:
- [Agent Standards](docs/00.agent-governance/rules/standards.md)
- [Agentic Rules](docs/00.agent-governance/rules/agentic.md)

**Core Rules:**
- Follow `docs/00.agent-governance/` for agent policy, retaining it in English.
- User-facing responses and READMEs must be in Korean.
- Route detailed policy changes to governance docs instead of bloating gateway files.

## §3 Routing

- Agents, skills, models, and `.codex` mirrors: [harness-catalog.md](docs/00.agent-governance/harness-catalog.md)
- Delegation and handoff rules: [subagent-protocol.md](docs/00.agent-governance/subagent-protocol.md)
- Agent-first execution rules: [agentic.md](docs/00.agent-governance/rules/agentic.md)
- Documentation protocol: [documentation-protocol.md](docs/00.agent-governance/rules/documentation-protocol.md)
- Generated document routing: [document-stage-routing.md](docs/00.agent-governance/rules/document-stage-routing.md)
- Git workflow: [git-workflow.md](docs/00.agent-governance/rules/git-workflow.md)
- Tooling note: [RTK.md](RTK.md)
