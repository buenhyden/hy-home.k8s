# Local Runtime Baseline (Gemini)

This file is the runtime baseline for local agent execution via Gemini in `hy-home.k8s`, a
WSL2+k3d cluster repository managed through ArgoCD GitOps.

## Purpose

- Anchor the local `.agents/**` runtime contract as a shared surface and moderate-shim.
- Point agents to the canonical governance documents.
- Make repo-backed GitOps validation the default execution model.

## Loading Order

Start from the root Gemini provider shim, then follow the governance JIT sequence:

1. `GEMINI.md`
2. `docs/00.agent-governance/rules/bootstrap.md`
3. `docs/00.agent-governance/rules/preflight-checklist.md`
4. `docs/00.agent-governance/rules/persona.md`
5. `docs/00.agent-governance/scopes/<layer>.md`
6. `docs/00.agent-governance/providers/gemini.md`
7. `docs/00.agent-governance/memory/progress.md`
8. `docs/00.agent-governance/rules/postflight-checklist.md`

## Workspace Contract

- Plan and implement from repo evidence: `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/99.templates`, `gitops/`, `infrastructure/`, `scripts/`, and current validators.
- Record repo-changing work progress and reusable memory in `docs/00.agent-governance/memory/progress.md`.
- Use `docs/00.agent-governance/rules/agentic.md` as the Agent-first Engineering execution contract.
- Author stage documents Template-First: use `docs/99.templates/support/template-routing.md` for route selection, then read the matching template under `docs/99.templates/templates/` before writing into `docs/01.requirements`–`docs/05.operations` and `docs/99.templates`; `docs/99.templates/README.md` is the index summary.
- If `graphify-out/GRAPH_REPORT.md` exists, read it before architecture or codebase answers; see `.agents/rules/graphify.md` for the full graphify contract.
- The `.agents/` folder is the git-tracked single source of truth for provider-neutral shared content (`skills/`, `workflows/`, `output-styles/`). `.claude/skills`, `.claude/workflows`, `.claude/output-styles`, `.codex/skills`, `.codex/workflows`, and `.codex/output-styles` are symlink views; provider-native files such as `.claude/agents/*`, `.codex/agents/*`, `.claude/settings.json`, `.codex/hooks.json`, and `.agents/hooks.json` are real adapter/runtime surfaces. `.agents/agents/*.md` are the Gemini-tier agent files.
- The `.agents/agents/*.md` files serve as Gemini agent reference indexes.
- `.agents/hooks.json` provides Gemini event/context wiring where the runtime honors it. It routes to shared hook scripts for Template-First guidance and QA/CI/CD validation, but it is not a Claude-style permission gate and does not replace explicit validation commands.
- Use `RTK.md` as cross-agent SSOT for shell commands.
- See `.agents/rules/workspace-rules.md` for Gemini-specific workspace rules and `.agents/workflows/qa-cicd-workflow.md` for QA/CI/CD workflows.

## Gemini Capabilities & Constraints

- **Skill routing**: Use the repo-local `.agents/skills/**` SSoT via the Task-to-Skill routing in `docs/00.agent-governance/harness-catalog.md`; provider symlink views under `.claude/skills` and `.codex/skills` must remain byte-identical. Do not rely on user-global skills for cluster work.
- **Hook behavior**: Gemini has no native permission-gate equivalent to Claude `settings.json`; honor the shared behavior contract (preflight, Template-First edits, post-edit validation, postflight) defined in governance and wired through `.agents/hooks.json` plus the shared `docs/00.agent-governance/hooks/*.sh` scripts where supported.
- **Provider tuning**: Keep Gemini-specific tuning in `docs/00.agent-governance/providers/gemini.md`; do not introduce policy here.

## Model Hierarchy

- See `docs/00.agent-governance/model-policy.md` for the canonical model tier policy (e.g., `Gemini 3.1 Pro` for `top`, `Gemini 3.5 Flash` for `worker`).
- The canonical cross-provider mapping is the Model Tier Mapping table in `docs/00.agent-governance/harness-catalog.md`.

## Validation and Tooling

- Use `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, `scripts/*.sh`, and `infrastructure/tests/*.sh` as validation sources.
- Run `scripts/validate-repo-quality-gates.sh .` as the repo-backed regression gate before handoff.
- Use `RTK.md` for shell-command guidance; if `rtk` is not on PATH, check `/home/hy/.local/bin/rtk --version`. If that works but `rtk gain` cannot initialize its tracking database, run the underlying command directly and report the PATH/DB limitation.

## Runtime Roster

- Agents & Skills: see `docs/00.agent-governance/harness-catalog.md`

## Relationship to Gateway Files

- Root `GEMINI.md` is the Gemini provider shim pointing here.
- `AGENTS.md` is the Codex/GPT gateway contract and is not part of the Gemini loading path.
- This file is the local runtime baseline for Gemini, not a replacement for shared governance policy.
