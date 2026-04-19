# Agent Framework Contract

Thin gateway for `hy-home.k8s` agent execution.

## §1 Bootstrap

Load governance JIT in this order:

1. [bootstrap.md](docs/00.agent-governance/rules/bootstrap.md)
2. [preflight-checklist.md](docs/00.agent-governance/rules/preflight-checklist.md)
3. [persona.md](docs/00.agent-governance/rules/persona.md)
4. matching scope in `docs/00.agent-governance/scopes/`
5. provider notes in `docs/00.agent-governance/providers/`
6. [postflight-checklist.md](docs/00.agent-governance/rules/postflight-checklist.md) before completion

Local runtime baseline: [`.claude/CLAUDE.md`](.claude/CLAUDE.md)

## §2 Constraints

- Respond to users in Korean.
- Keep `docs/00.agent-governance/*` in English.
- Keep human-facing READMEs in Korean.
- Treat `docs/01~99` as authored SSoT; modify only when explicitly requested by a human.
- Keep gateway files minimal and avoid duplicating rule text.
- GitOps-First: all infra changes via PR → ArgoCD; never `kubectl apply` directly.
- Secrets: never write plaintext k8s secrets.
- In-place refactor only; no file proliferation without explicit human request.

## §3 Agent Catalog

Subagents in `.claude/agents/` implement the local harness catalog for this cluster.
See `docs/00.agent-governance/harness-catalog.md`.

| Agent File              | Role                                     |
| ----------------------- | ---------------------------------------- |
| `supervisor.md`         | Agent supervision, orchestration control |
| `k8s-implementer.md`    | k8s IaC, kube-linter, manifest authoring |
| `gitops-reviewer.md`    | ArgoCD pipeline, GitOps PR review        |
| `security-auditor.md`   | RBAC, network policy, secret audit       |
| `incident-responder.md` | Cluster incident, timeline, remediation  |
| `code-reviewer.md`      | YAML/Helm/script quality review          |
| `doc-writer.md`         | Runbook, guide, postmortem authoring     |

Each agent `@import`s the matching scope from `scopes/<layer>.md`.

## §4 Skill Catalog

Runtime skills live under `.claude/skills/`.
Use `docs/00.agent-governance/harness-catalog.md` as the canonical skill roster.

## §5 Orchestration

- Dispatch subagents via Task tool only; never inline role definitions.
- Run [postflight-checklist.md](docs/00.agent-governance/rules/postflight-checklist.md) before every completion.
- Subagent protocol: [subagent-protocol.md](docs/00.agent-governance/subagent-protocol.md).

## §6 Documentation

See [documentation-protocol.md](docs/00.agent-governance/rules/documentation-protocol.md) for Docs 3 Rules (HALT triggers).

## §7 Linting

All lint and format checks: `.pre-commit-config.yaml`. Never run lint tools manually outside pre-commit.

## §8 Settings

- `settings.json` — team shared, git tracked.
- `settings.local.json` — personal overrides only, `.gitignore`d.
- No duplication between the two files.

## §9 Role Separation

- `scopes/*.md` — policy SSOT for each layer.
- `.claude/agents/*.md` — runtime bridge; each `@import`s one scope.
- Never embed policy text in agent files.

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
