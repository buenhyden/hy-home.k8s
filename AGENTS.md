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

Subagents in `.claude/agents/` adapt harness-100 patterns for this cluster.

| Agent File              | H100 Ref                    | Role                                     |
| ----------------------- | --------------------------- | ---------------------------------------- |
| `k8s-implementer.md`    | H100:26 infra-as-code       | k8s IaC, kube-linter, manifest authoring |
| `gitops-reviewer.md`    | H100:20 cicd-pipeline       | ArgoCD pipeline, GitOps PR review        |
| `security-auditor.md`   | H100:28 security-audit      | RBAC, network policy, secret audit       |
| `incident-responder.md` | H100:25 incident-postmortem | Cluster incident, timeline, remediation  |
| `code-reviewer.md`      | H100:21 code-review         | YAML/Helm/script quality review          |
| `doc-writer.md`         | H100:81 documentation       | Runbook, guide, postmortem authoring     |

Each agent `@import`s the matching scope from `scopes/<layer>.md`.

## §4 Orchestration

- Dispatch subagents via Task tool only; never inline role definitions.
- Run [postflight-checklist.md](docs/00.agent-governance/rules/postflight-checklist.md) before every completion.
- Subagent protocol: [subagent-protocol.md](docs/00.agent-governance/subagent-protocol.md).

## §5 Documentation

See [documentation-protocol.md](docs/00.agent-governance/rules/documentation-protocol.md) for Docs 3 Rules (HALT triggers).

## §6 Linting

All lint and format checks: `.pre-commit-config.yaml`. Never run lint tools manually outside pre-commit.

## §7 Settings

- `settings.json` — team shared, git tracked.
- `settings.local.json` — personal overrides only, `.gitignore`d.
- No duplication between the two files.

## §8 Role Separation

- `scopes/*.md` — policy SSOT for each layer.
- `.claude/agents/*.md` — runtime bridge; each `@import`s one scope.
- Never embed policy text in agent files.
