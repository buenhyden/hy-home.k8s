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
- Resolve memory through the four classes in
  `docs/00.agent-governance/memory/README.md`: `working-short-term`,
  `durable-long-term`, `domain-scoped`, and `provider-local-auxiliary`.
  `docs/00.agent-governance/memory/progress.md` is the canonical progress ledger,
  serving as the durable shared ledger and the only tracked `progress.md`;
  `.agent-work/checkpoint.json`
  is ignored, temporary, and advisory, and repository evidence wins conflicts.
- Treat provider-local memory as auxiliary only. Spec 043 owns the not-yet-
  implemented executable promotion, refresh, expiry, archive/GC, redaction,
  conflict, and resume controls.
- Use `docs/00.agent-governance/rules/agentic.md` as the Agent-first Engineering execution contract.
- Author stage documents Template-First: use `docs/99.templates/support/template-routing.md` for route selection, then read the matching template under `docs/99.templates/templates/` before writing into `docs/01.requirements`–`docs/05.operations` and `docs/99.templates`; `docs/99.templates/README.md` is the index summary.
- If `graphify-out/GRAPH_REPORT.md` exists, read it before architecture or codebase answers.
- Treat `.codex/agents/*.toml` and `.claude/agents/*.md` as provider-native role adapters, and `.agents/agents/*.md` as the local/Antigravity adapter for the same roster; keep repo-static role parity aligned without reporting it as Gemini CLI runtime parity.
- Treat `.codex/hooks.json` as Codex event wiring for repo-local context and validation hooks, not as an equivalent permission gate to Claude's `settings.json`.
- `.codex/` carries Codex-native real files (`agents/*.toml`, `hooks.json`); its `skills/`, `workflows/`, and `output-styles/` are symlinks to the `.agents/` SSoT for byte-identical shared content.
- Use `RTK.md` as cross-agent SSOT for shell commands.
- Verification: Codex MUST implement explicit QA and CI/static validation phases prior to task completion, mirroring Gemini and Claude.
- Agent eval completion follows
  `docs/00.agent-governance/rules/quality-standards.md`; report its validation
  lanes, result vocabulary, and handoff fields without copying a command matrix
  into this baseline.

## Harness Four-Element Runtime Contract

Codex implements the shared four-element harness model from
`docs/00.agent-governance/harness-catalog.md` as follows:

1. **Instruction and settings documents**: load `AGENTS.md`,
   `docs/00.agent-governance/rules/bootstrap.md`, provider notes, this runtime
   baseline, and the relevant scope before substantial work.
2. **Architecture constraints**: honor Codex filesystem/network sandboxing,
   escalation approvals, GitOps-first boundaries, template routing, and
   `.codex/agents/*.toml` provider-native role adapters. `.codex/hooks.json` supplies context and
   validation wiring, not a Claude-style permission gate.
3. **Feedback loops**: run explicit repo-static validation commands before
   handoff and use `.codex/hooks.json` shared script wiring as additional
   feedback where the runtime supports it. Report each canonical lane
   separately. Do not infer live k3d, ArgoCD,
   Vault, ESO, or deployment readiness from static checks. If a repeated error
   appears, update the smallest shared harness surface that would have
   prevented it instead of treating the failure as only an agent mistake.
4. **Knowledge stores**: read and update
   `docs/00.agent-governance/memory/progress.md` for repo-changing work, use
   the owning Spec/Runbook/Incident/Postmortem for domain-scoped knowledge, and
   keep working or provider-local memory non-authoritative. Record RTK
   PATH/database limitations without inspecting private runtime state.
   Preserve compact reviewed lessons in durable owners, while keeping current
   policy in Stage 00 and current implementation truth in the owning docs,
   scripts, and manifests.

## Codex/GPT Capabilities & Constraints

- **Skill routing**: Use the `.codex/skills/**` roster (a symlink to the `.agents/` SSoT) via the Task-to-Skill routing in `docs/00.agent-governance/harness-catalog.md`.
- **Hook behavior**: `.codex/hooks.json` reuses the shared `docs/00.agent-governance/hooks/*.sh` scripts for context and validation wiring where supported. It can surface Template Routing and CI/static QA checks through `customInstructions`, but explicit validation commands remain required before handoff.
- **Provider tuning**: Keep Codex/GPT-specific tuning in `docs/00.agent-governance/providers/codex.md`; do not introduce policy here.

## Model Hierarchy

- See `docs/00.agent-governance/model-policy.md` for the canonical model tier policy (e.g., `gpt-5.5` for `top`, `gpt-5.3-codex` for `worker`).
- The canonical cross-provider mapping is the Model Tier Mapping table in `docs/00.agent-governance/harness-catalog.md`.

## Validation and Tooling

- Canonical selection: `docs/00.agent-governance/contracts/validation-surfaces.json`.
- Canonical lane/result/handoff semantics: `docs/00.agent-governance/rules/quality-standards.md`.
- Native sandboxing and approval boundaries: Codex configuration and
  `docs/00.agent-governance/providers/codex.md`; command guidance: `RTK.md`.

The presence of `.codex/agents/*.toml` or `.codex/hooks.json` is repo-static
evidence only. It does not prove native Codex discovery, context/validation wiring
delivery, or role consumption. `.codex/hooks.json` remains not a
Claude-style permission gate.

## Runtime Roster

- Agents & Skills: see `docs/00.agent-governance/harness-catalog.md`

## Relationship to Gateway Files

- `AGENTS.md` is the Codex/GPT gateway contract.
- This file is the local runtime baseline for Codex, not a replacement for shared governance policy.
