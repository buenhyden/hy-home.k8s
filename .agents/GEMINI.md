# Local Runtime Baseline (Gemini)

This file is the runtime baseline for local agent execution via Gemini in `hy-home.k8s`, a
WSL2+k3d cluster repository managed through ArgoCD GitOps.

## Purpose

- Anchor the local `.agents/**` runtime contract as a shared surface and moderate-shim.
- Point agents to the canonical governance documents.
- Make repo-backed GitOps validation the default execution model.

## Loading Order

Start from the repository gateway files, then follow the governance JIT sequence:

1. `AGENTS.md`
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
- Author stage documents Template-First: read `docs/99.templates/README.md` and the matching template before writing into `docs/01.requirements`–`docs/05.operations` and `docs/99.templates`, per `docs/00.agent-governance/rules/documentation-protocol.md` and `rules/document-stage-routing.md`.
- If `graphify-out/GRAPH_REPORT.md` exists, read it before architecture or codebase answers; see `.agents/rules/graphify.md` for the full graphify contract.
- The `.agents/` folder is the primary git-tracked Single Source of Truth (SSoT) surface for agents, skills, rules, workflows, and output-styles under the Antigravity baseline. Claude and Codex mirror or symlink this structure.
- The `.agents/agents/*.md` files serve as Gemini agent reference indexes.
- Gemini operates under equivalent behavior contracts to Claude hooks via `.agents/hooks.json` and custom instructions (e.g., preflight, QA, CI/CD validation, postflight).
- Use `RTK.md` as cross-agent SSOT for shell commands.

## Gemini Capabilities & Constraints

- **Skill routing**: Use the repo-local `.agents/skills/**` roster via the Task-to-Skill routing in `docs/00.agent-governance/harness-catalog.md`; do not rely on user-global skills for cluster work.
- **Hook behavior**: Gemini honors the same behavior contract (preflight, Template-First edits, post-edit validation, postflight) defined in governance and the shared `docs/00.agent-governance/hooks/*.sh` scripts.
- **Provider tuning**: Keep Gemini-specific tuning in `docs/00.agent-governance/providers/gemini.md`; do not introduce policy here.

## Model Hierarchy

- Please refer to `docs/00.agent-governance/model-policy.md` for the canonical model tier definitions across Claude, Gemini, and Codex.

## Validation and Tooling

- Use `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, `scripts/*.sh`, and `infrastructure/tests/*.sh` as validation sources.
- Run `scripts/validate-repo-quality-gates.sh .` as the repo-backed regression gate before handoff.
- Use `RTK.md` for shell-command guidance; if `rtk` is not on PATH, run the underlying command directly and report the limitation.

## Runtime Roster

- Agents & Skills: see `docs/00.agent-governance/harness-catalog.md`

## Relationship to Gateway Files

- `AGENTS.md` is the shared gateway contract.
- Root `GEMINI.md` is a thin provider shim pointing here.
- This file is the local runtime baseline for Gemini, not a replacement for shared governance policy.
