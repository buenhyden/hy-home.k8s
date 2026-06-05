# Local Runtime Baseline

This file is the runtime baseline for local agent execution in `hy-home.k8s`, a
WSL2+k3d cluster repository managed through ArgoCD GitOps.

## Purpose

- Anchor the local `.claude/**` runtime contract.
- Point agents to the canonical governance documents.
- Keep runtime roster and model hierarchy easy to resolve without duplicating policy text.
- Make repo-backed GitOps validation the default execution model.

## Loading Order

Start from the repository gateway files, then follow the governance JIT sequence:

1. `AGENTS.md`
2. `docs/00.agent-governance/rules/bootstrap.md`
3. `docs/00.agent-governance/rules/preflight-checklist.md`
4. `docs/00.agent-governance/rules/persona.md`
5. `docs/00.agent-governance/scopes/<layer>.md`
6. `docs/00.agent-governance/providers/<provider>.md`
7. `docs/00.agent-governance/memory/progress.md`
8. `docs/00.agent-governance/rules/postflight-checklist.md`

## Workspace Contract

- Plan and implement from repo evidence: `docs/01.requirements`, `docs/02.architecture`, `docs/03.specs`, `docs/04.execution`, `docs/05.operations`, `docs/90.references`, `docs/99.templates`, `gitops/`, `infrastructure/`, `scripts/`, and current validators.
- Record repo-changing work progress and reusable memory in `docs/00.agent-governance/memory/progress.md`.
- Treat `docs/00.agent-governance/memory/progress.md` as the canonical progress ledger and the only tracked `progress.md`; standalone memory files may exist only under the memory template contract with a related progress entry.
- Use `docs/99.templates/memory.template.md` for standalone files under `docs/00.agent-governance/memory/`, and update the related `progress.md` entry in the same change.
- Use `docs/00.agent-governance/rules/agentic.md` as the Agent-first Engineering execution contract.
- Treat `docs/90.references/llm-wiki/wiki-index.md` as generated Markdown maintained by `scripts/generate-llm-wiki-index.sh`; route policy and procedure changes to canonical owner files.
- Keep infrastructure changes repo-backed. Agents and subagents do not mutate live clusters by default; human-approved bootstrap or break-glass actions are operator-bound and must record scope, rollback, and verification evidence.
- Do not write plaintext Kubernetes secrets.
- Treat `.codex/agents/*.toml` as Codex mirrors of `.claude/agents/*.md`; keep both sides aligned.
- Treat `.codex/hooks.json` as Codex event wiring for repo-local context and validation hooks, not as an equivalent permission gate to `.claude/settings.json`.
- `.agents/` is the single source of truth for provider-neutral shared content (`skills/`, `workflows/`, `output-styles/`); `.claude/skills`, `.claude/workflows`, and `.claude/output-styles` are symlinks to it so every provider stays byte-identical. Provider-specific agents are real files per provider: `.claude/agents/*.md` (Claude models + `tools:`), `.agents/agents/*.md` (Gemini), `.codex/agents/*.toml` (GPT).
- Workspace Structures: Use `.claude/skills/`, `.claude/agents/`, `.claude/workflows/`, `.claude/output-styles/`, `docs/00.agent-governance/hooks/`, and `docs/00.agent-governance/rules/` consistently; shared structures resolve to the `.agents/` SSoT via symlinks where applicable.
- Verification: Implement explicit QA and CI/CD validation phases prior to task completion.
- Agent eval completion is explicit command evidence from repo-static gates, changed-file checks, or recorded human/operator approval; do not infer live runtime readiness from static validation.
- Treat `.claude/*.local.md`, including Hookify rules, as ignored local warning files. Claude hooks/settings are shared enforcement when tracked through `.claude/settings.json`, shared scripts, `.codex/hooks.json`, `.agents/hooks.json`, and repository validators; Hookify local advisory files are not shared policy.
- Treat `docs/00.agent-governance/hooks/lifecycle-guard.sh` as the shared lifecycle validation surface wired by `.claude/settings.json`: Stop/SubagentStop may block objective repo-state failures and advise task-unit commit discipline for uncommitted tracked changes, while PreCompact reports uncommitted tracked changes, suggested validation, and the same commit discipline without blocking compaction.

## Harness Four-Element Runtime Contract

Claude implements the shared four-element harness model from
`docs/00.agent-governance/harness-catalog.md` as follows:

1. **Instruction and settings documents**: load `CLAUDE.md`,
   `docs/00.agent-governance/rules/bootstrap.md`, provider notes, this runtime
   baseline, and the relevant scope before substantial work.
2. **Architecture constraints**: use the native allow/deny policy in
   `.claude/settings.json`, least-privilege `.claude/agents/*.md` `tools:`,
   GitOps boundaries, template routing, and shared hooks to block unsafe live
   mutation, secret handling, model drift, and off-taxonomy documents.
3. **Feedback loops**: treat PostToolUse and lifecycle hooks plus
   `scripts/*.sh`, `infrastructure/tests/*.sh`, and CI as completion evidence;
   report skipped live checks separately from repo-static validation. If a
   repeated error appears, update the smallest shared harness surface that
   would have prevented it instead of treating the failure as only an agent
   mistake.
4. **Knowledge stores**: read and update
   `docs/00.agent-governance/memory/progress.md` for repo-changing work, use
   `harness-catalog.md` as current runtime truth, and route generated wiki or
   graphify findings back to canonical owner files. Preserve compact durable
   lessons there, while keeping current policy in Stage 00 and current
   implementation truth in the owning docs, scripts, and manifests.

## Runtime Roster

- Agents: see `docs/00.agent-governance/harness-catalog.md`
- Skills: see `docs/00.agent-governance/harness-catalog.md`

## Validation and Tooling

- Use `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, `scripts/*.sh`, and `infrastructure/tests/*.sh` as validation sources.
- Keep `docs/00.agent-governance/hooks/post-validate.sh` as the PostToolUse surface for scoped auto-formatting, style checks, and repository validation after file edits.
- Keep `scripts/validate-repo-quality-gates.sh .` as the regression gate for structural template coverage, README `Link Basis` / `Related Documents`, hook wiring, lifecycle hook payload simulation, and local Hookify ignore/frontmatter checks.
- Use `RTK.md` for shell-command guidance. If `rtk` is not on PATH, check `/home/hy/.local/bin/rtk --version`; if that works but `rtk gain` cannot initialize its tracking database, run the underlying command directly and report the PATH/DB limitation.
- If `graphify-out/GRAPH_REPORT.md` exists, read it before architecture or codebase answers. If graphify data or the `graphify` CLI is unavailable, use repo inspection and report the limitation.

## Model Hierarchy

- See `docs/00.agent-governance/model-policy.md` for the canonical model tier policy (e.g., `opus 4.8` for supervisor, `sonnet 4.6` for workers).
- The detailed cross-provider catalog is in `docs/00.agent-governance/harness-catalog.md`.

## Relationship to Gateway Files

- `AGENTS.md` is the shared gateway contract.
- Root `CLAUDE.md` and `GEMINI.md` are thin provider shims.
- This file is the local runtime baseline, not a replacement for governance policy.
