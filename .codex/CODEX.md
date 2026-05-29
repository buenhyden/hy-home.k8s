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
- Author stage documents Template-First: read `docs/99.templates/README.md` and the matching template before writing into `docs/01.requirements`–`docs/05.operations` and `docs/99.templates`, per `docs/00.agent-governance/rules/documentation-protocol.md` and `rules/document-stage-routing.md`.
- If `graphify-out/GRAPH_REPORT.md` exists, read it before architecture or codebase answers.
- Treat `.codex/agents/*.toml` as Codex mirrors of the primary agent definitions; keep them aligned.
- Treat `.codex/hooks.json` as Codex event wiring for repo-local context and validation hooks, not as an equivalent permission gate to Claude's `settings.json`.
- The `.codex/` folder mirrors `.claude/` structure for `skills/`, `rules/`, `workflows/`, and `output-styles/`.
- Use `RTK.md` as cross-agent SSOT for shell commands.
- Verification: Codex MUST implement explicit QA and CI/CD validation phases prior to task completion, mirroring Gemini and Claude.

## Codex/GPT Capabilities & Constraints

- **Skill routing**: Use the repo-local `.codex/skills/**` (mirrored from `.claude/skills/**`) via the Task-to-Skill routing in `docs/00.agent-governance/harness-catalog.md`.
- **Hook behavior**: `.codex/hooks.json` reuses the shared `.claude/hooks/*.sh` scripts for context and validation wiring, enforcing Template Routing and CI/CD checks via `customInstructions`.
- **Provider tuning**: Keep Codex/GPT-specific tuning in `docs/00.agent-governance/providers/codex.md`; do not introduce policy here.

## Model Hierarchy

- `top` tier (`supervisor`) uses `gpt-5.5`; `worker` tier agents use `gpt-5.4-mini`.
- The canonical cross-provider mapping is the Model Tier Mapping table in `docs/00.agent-governance/harness-catalog.md`.

## Validation and Tooling

- Use `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, `scripts/*.sh`, and `infrastructure/tests/*.sh` as validation sources.
- Run `scripts/validate-repo-quality-gates.sh .` as the repo-backed regression gate before handoff.
- Use `RTK.md` for shell-command guidance; if `rtk` is not on PATH, run the underlying command directly and report the limitation.

## Runtime Roster

- Agents & Skills: see `docs/00.agent-governance/harness-catalog.md`

## Relationship to Gateway Files

- `AGENTS.md` is the shared gateway contract.
- This file is the local runtime baseline for Codex, not a replacement for shared governance policy.
