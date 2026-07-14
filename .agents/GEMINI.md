# Local Adapter Baseline (Antigravity / Gemini-Family)

This file is the tracked local/Antigravity adapter baseline for `hy-home.k8s`,
a WSL2+k3d cluster repository managed through ArgoCD GitOps. It is not a Gemini
CLI native configuration surface.

## Purpose

- Anchor the local `.agents/**` adapter contract as a shared surface and moderate-shim.
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
- The `.agents/` folder is the git-tracked single source of truth for provider-neutral shared content (`skills/`, `workflows`, `output-styles`) and local/Antigravity adapters. `.claude/skills`, `.claude/workflows`, `.claude/output-styles`, `.codex/skills`, `.codex/workflows`, and `.codex/output-styles` are symlink views; `.claude/agents/*`, `.codex/agents/*`, `.claude/settings.json`, and `.codex/hooks.json` remain provider-native files. `.agents/agents/*.md` and `.agents/hooks.json` are local adapter surfaces, not Gemini CLI native files.
- The `.agents/agents/*.md` files serve as local/Antigravity role adapters and reference indexes.
- `.agents/hooks.json` provides local behavioral/event-context wiring where a compatible runtime honors it. It routes to shared hook scripts for Template-First guidance and QA/CI/static validation, but it is neither a Claude-style permission gate nor Gemini CLI native settings and does not replace explicit validation commands.
- Gemini CLI native project agents and settings are reserved for `.gemini/agents/**` and `.gemini/settings.json`. Both are absent; native discovery, event delivery, policy loading, and model resolution remain `DEFER` pending a separately approved PRD/ARD/Spec/Plan/Task, or at minimum Spec/Plan/Task.
- Use `RTK.md` as cross-agent SSOT for shell commands.
- See `.agents/rules/workspace-rules.md` for local/Antigravity workspace rules
  and `.agents/workflows/qa-cicd-workflow.md` for shared QA/CI workflow steps.
- Resolve validation lanes, result terms, and handoff evidence fields from
  `docs/00.agent-governance/rules/quality-standards.md`; do not restate a
  provider-local command matrix here.

## Harness Four-Element Runtime Contract

The local/Antigravity adapter implements the repo-static portion of the shared four-element harness model from
`docs/00.agent-governance/harness-catalog.md` as follows:

1. **Instruction and settings documents**: load `GEMINI.md`,
   `docs/00.agent-governance/rules/bootstrap.md`, provider notes, this runtime
   baseline, and the relevant scope before substantial work.
2. **Architecture constraints**: honor the tracked `.agents/**` adapter
   baseline, GitOps-first boundaries, template routing, native Claude/Codex
   agent files, and `.agents/hooks.json` local behavioral wiring. Local hook
   JSON is not Gemini CLI native configuration or a Claude-style permission
   gate.
3. **Feedback loops**: run explicit repo-static validation commands before
   handoff and use `.agents/hooks.json` shared script wiring as additional
   feedback where the runtime supports it. Report lanes through the canonical
   quality contract. Do not infer live k3d, ArgoCD, Vault, ESO, or deployment
   readiness from static checks.
4. **Knowledge stores**: read and update
   `docs/00.agent-governance/memory/progress.md` for repo-changing work, use
   `harness-catalog.md` as current runtime truth, and route generated wiki or
   graphify findings back to canonical owner files.

## Gemini Capabilities & Constraints

- **Skill routing**: Use the repo-local `.agents/skills/**` SSoT via the Task-to-Skill routing in `docs/00.agent-governance/harness-catalog.md`; provider symlink views under `.claude/skills` and `.codex/skills` must remain byte-identical. Do not rely on user-global skills for cluster work.
- **Hook behavior**: Honor the shared behavior contract (preflight, Template-First edits, post-edit validation, postflight) through `.agents/hooks.json` plus the shared `docs/00.agent-governance/hooks/*.sh` scripts only where a compatible local/Antigravity runtime supports that adapter. Do not infer Gemini CLI native event or policy behavior.
- **Provider tuning**: Keep Gemini-specific tuning in `docs/00.agent-governance/providers/gemini.md`; do not introduce policy here.

## Model Hierarchy

- See `docs/00.agent-governance/model-policy.md` for the canonical model tier policy (e.g., `Gemini 3.1 Pro` for `top`, `Gemini 3.5 Flash` for `worker`).
- The canonical cross-provider mapping is the Model Tier Mapping table in `docs/00.agent-governance/harness-catalog.md`.

## Validation and Tooling

- Canonical selection: `docs/00.agent-governance/contracts/validation-surfaces.json`.
- Canonical lane/result/handoff semantics: `docs/00.agent-governance/rules/quality-standards.md`.
- Canonical command guidance and provider limitations: `RTK.md` and
  `docs/00.agent-governance/providers/gemini.md`.

The presence of `.agents/agents/*.md` or `.agents/hooks.json` is local adapter
repo-static evidence only. It does not prove Gemini CLI native discovery,
event delivery, policy loading, model resolution, or role consumption.

## Runtime Roster

- Agents & Skills: see `docs/00.agent-governance/harness-catalog.md`

## Relationship to Gateway Files

- Root `GEMINI.md` is the Gemini provider shim pointing here.
- `AGENTS.md` is the Codex/GPT gateway contract and is not part of the Gemini loading path.
- This file is the local/Antigravity adapter baseline, not a Gemini CLI native runtime baseline or a replacement for shared governance policy.
