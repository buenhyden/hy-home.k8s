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
- Treat `docs/00.agent-governance/memory/progress.md` as the canonical progress ledger and the only tracked `progress.md`; standalone memory files may exist only under the memory template contract with a related progress entry.
- Use `docs/00.agent-governance/rules/agentic.md` as the Agent-first Engineering execution contract.
- Author stage documents Template-First: read `docs/99.templates/README.md` and the matching template before writing into `docs/01.requirements`–`docs/05.operations` and `docs/99.templates`, per `docs/00.agent-governance/rules/documentation-protocol.md` and `rules/document-stage-routing.md`.
- If `graphify-out/GRAPH_REPORT.md` exists, read it before architecture or codebase answers.
- Treat `.codex/agents/*.toml` as Codex mirrors of the primary agent definitions; keep them aligned.
- Treat `.codex/hooks.json` as Codex event wiring for repo-local context and validation hooks, not as an equivalent permission gate to Claude's `settings.json`.
- `.codex/` carries Codex-native real files (`agents/*.toml`, `hooks.json`); its `skills/`, `workflows/`, and `output-styles/` are symlinks to the `.agents/` SSoT for byte-identical shared content.
- Use `RTK.md` as cross-agent SSOT for shell commands.
- Verification: Codex MUST implement explicit QA and CI/CD validation phases prior to task completion, mirroring Gemini and Claude.
- Agent eval completion must be proven with explicit command evidence from repo-static gates, changed-file checks, or recorded human/operator approval; Codex hooks are context/validation wiring, and static checks do not imply live k3d, ArgoCD, Vault, ESO, or secret readiness.

## Harness Four-Element Runtime Contract

Codex implements the shared four-element harness model from
`docs/00.agent-governance/harness-catalog.md` as follows:

1. **Instruction and settings documents**: load `AGENTS.md`,
   `docs/00.agent-governance/rules/bootstrap.md`, provider notes, this runtime
   baseline, and the relevant scope before substantial work.
2. **Architecture constraints**: honor Codex filesystem/network sandboxing,
   escalation approvals, GitOps-first boundaries, template routing, and
   `.codex/agents/*.toml` mirrors. `.codex/hooks.json` supplies context and
   validation wiring, not a Claude-style permission gate.
3. **Feedback loops**: run explicit repo-static validation commands before
   handoff and use `.codex/hooks.json` shared script wiring as additional
   feedback where the runtime supports it. Do not infer live k3d, ArgoCD,
   Vault, ESO, or deployment readiness from static checks. If a repeated error
   appears, update the smallest shared harness surface that would have
   prevented it instead of treating the failure as only an agent mistake.
4. **Knowledge stores**: read and update
   `docs/00.agent-governance/memory/progress.md` for repo-changing work, use
   `harness-catalog.md` as current runtime truth, and record RTK PATH/database
   limitations without inspecting private runtime state. Preserve compact
   durable lessons there, while keeping current policy in Stage 00 and current
   implementation truth in the owning docs, scripts, and manifests.

## Codex/GPT Capabilities & Constraints

- **Skill routing**: Use the `.codex/skills/**` roster (a symlink to the `.agents/` SSoT) via the Task-to-Skill routing in `docs/00.agent-governance/harness-catalog.md`.
- **Hook behavior**: `.codex/hooks.json` reuses the shared `docs/00.agent-governance/hooks/*.sh` scripts for context and validation wiring, enforcing Template Routing and CI/CD checks via `customInstructions`.
- **Provider tuning**: Keep Codex/GPT-specific tuning in `docs/00.agent-governance/providers/codex.md`; do not introduce policy here.

## Model Hierarchy

- See `docs/00.agent-governance/model-policy.md` for the canonical model tier policy (e.g., `gpt-5.5` for `top`, `gpt-5.3-codex` for `worker`).
- The canonical cross-provider mapping is the Model Tier Mapping table in `docs/00.agent-governance/harness-catalog.md`.

## Validation and Tooling

- Use `.pre-commit-config.yaml`, `.github/workflows/ci.yml`, `scripts/*.sh`, and `infrastructure/tests/*.sh` as validation sources.
- Run `scripts/validate-repo-quality-gates.sh .` as the repo-backed regression gate before handoff.
- Use `RTK.md` for shell-command guidance; if `rtk` is not on PATH, check `/home/hy/.local/bin/rtk --version`. If the binary exists but `rtk gain` cannot initialize its tracking database, do not read private runtime state; run the underlying command directly and record the PATH/DB limitation.

## Runtime Roster

- Agents & Skills: see `docs/00.agent-governance/harness-catalog.md`

## Relationship to Gateway Files

- `AGENTS.md` is the Codex/GPT gateway contract.
- This file is the local runtime baseline for Codex, not a replacement for shared governance policy.
