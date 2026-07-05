---
title: 'Reference: Provider Harness and Loop Implementation Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-02
---

# Reference: Provider Harness and Loop Implementation Audit

## Overview

This dated audit compares the provider harness and loop benchmark model to
current repo-backed implementation evidence in `hy-home.k8s` as checked on
2026-07-02. It covers Claude, Codex, Gemini, and common provider parity.

This audit is descriptive reference material. It does not change active
governance policy, provider runtime behavior, hook wiring, scripts, CI
semantics, templates, credentials, manifests, approval boundaries, or
operations procedure.

Static repository evidence does not prove live provider-runtime behavior, live
cluster readiness, cloud readiness, secret readiness, paid-job readiness, or
external-service readiness.

## Purpose

- Record whether the researched provider harness and loop model is implemented
  in current repository surfaces.
- Separate upstream provider capability, local repo-backed implementation
  evidence, gaps, automation opportunities, and residual risks.
- Preserve known non-parity boundaries so future work does not assume Claude,
  Codex, and Gemini enforce the same controls in the same way.
- Provide a bounded implementation checklist without redefining active policy
  or claiming live runtime readiness.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-02
- Refresh trigger: Claude, Codex, Gemini, Stage 00 provider notes, gateway
  files, runtime baselines, provider agents, hook wiring, shared `.agents/**`
  assets, MCP configuration, audit benchmark, or audit-index changes.

## Authority Boundary

- **Authoritative for**:
  - Provider harness and loop implementation audit findings as checked on
    2026-07-02.
  - Repo-backed evidence paths used for this dated comparison.
  - Candidate follow-up routes for future specs, plans, tasks, provider
    adapter updates, validators, or operations documents.
- **Not authoritative for**:
  - Active governance policy, provider runtime configuration, CI enforcement
    semantics, hook enforcement semantics, approval boundaries, scripts,
    templates, or operations runbooks.
  - Live Claude, Codex, Gemini, k3d, ArgoCD, Vault, ESO, Kubernetes, cloud,
    deployment, secret, paid-job, or external-service readiness.
  - New provider roles, hooks, validators, MCP servers, tool permissions,
    credentials, workflow changes, or automation changes.

## Scope

- Covers Claude, Codex, Gemini, and common parity across
  instruction/settings, agents/subagents, hooks/permissions, skills/MCP/tooling,
  feedback loops, known non-parity boundaries, and automation opportunities.
- Uses `docs/90.references/research/2026-07-04-wer/provider-implementation-status.md` as the
  benchmark model and current repository files as local implementation
  evidence.
- Records missing tracked provider surfaces, such as absent local MCP or
  provider settings files, as evidence boundaries rather than inferring
  runtime state.
- Excludes live provider-runtime checks, live cluster checks, secret reads,
  external service checks, paid-job checks, policy changes, script changes,
  workflow changes, runtime adapter changes, and MCP server configuration.

## Definitions / Facts

### Benchmark Model

The benchmark model expects provider harness implementation to be assessed in
two separate lanes:

- **Upstream/provider capability**: Claude, Codex, and Gemini may each support
  settings, agents, hooks, skills, MCP, sandboxing, approvals, and evaluation
  loops differently.
- **Local repository implementation**: a capability counts as implemented only
  when a tracked repository surface implements or routes it for this workspace.

The benchmark also expects shared behavior through the Stage 00 canonical
adapter model. Gateway files, provider notes, runtime baselines, agent mirrors,
hook wiring, shared `.agents/**` assets, validation scripts, task evidence, and
progress memory are local evidence surfaces. External provider documentation
may inform the benchmark, but it does not prove local implementation.

### Implementation Matrix

| Area | Benchmark expectation | Current implementation | Status | Evidence | Gap or risk | Follow-up route |
| --- | --- | --- | --- | --- | --- | --- |
| Claude instruction/settings | Claude should have a thin gateway, provider notes, local runtime baseline, settings surface, and shared governance loading path. | Root `CLAUDE.md`, provider notes, `.claude/CLAUDE.md`, `.claude/settings.json`, and Stage 00 rules define the Claude loading path, runtime baseline, command permissions, and hook wiring. | Implemented | [CLAUDE.md](../../../../CLAUDE.md), [Claude provider notes](../../../00.agent-governance/providers/claude.md), [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md), [.claude/settings.json](../../../../.claude/settings.json), [bootstrap.md](../../../00.agent-governance/rules/bootstrap.md) | Repo evidence does not prove the live Claude runtime loaded these files in this session. | Keep Claude settings and baseline changes in `.claude/**` plus Stage 00 provider notes, with task evidence and validation. |
| Claude subagents/agents | Claude agents should have native provider files with role, model, scope, guardrails, and least-privilege tools. | Eight tracked `.claude/agents/*.md` files exist and use Markdown frontmatter with model and `tools:` fields; the subagent protocol defines mirror and tool-scope requirements. | Implemented | [.claude/agents/supervisor.md](../../../../.claude/agents/supervisor.md), [.claude/agents/k8s-implementer.md](../../../../.claude/agents/k8s-implementer.md), [subagent protocol](../../../00.agent-governance/subagent-protocol.md), [harness catalog](../../../00.agent-governance/harness-catalog.md) | Static file presence does not prove live subagent dispatch or provider enforcement. | Keep agent roster changes aligned across `.claude/agents/`, `.agents/agents/`, `.codex/agents/`, and the catalog. |
| Claude hooks/permissions | Claude should have native permission and hook settings that route through shared lifecycle scripts. | `.claude/settings.json` has allow/deny command policy plus SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop, and PreCompact hook wiring to shared scripts. | Implemented | [.claude/settings.json](../../../../.claude/settings.json), [Claude provider notes](../../../00.agent-governance/providers/claude.md), [common governance](../../../00.agent-governance/common-governance.md), [lifecycle guard](../../../00.agent-governance/hooks/lifecycle-guard.sh) | Exact blocking behavior still depends on active Claude runtime semantics and hook event execution. | Route any hook or permission change through Stage 00, shared hook scripts, validation, and task evidence. |
| Claude skills/MCP/tooling | Claude should expose shared skills and tooling while keeping MCP changes explicit and least-privilege. | Shared skills, workflows, and output styles resolve through `.agents/**` via `.claude/**` symlinks; no tracked `.mcp.json` was found in this checkout. | Partial | [.agents skills](../../../../.agents/skills/workspace-harness-audit/skill.md), [.agents workflows](../../../../.agents/workflows/qa-cicd-workflow.md), [common governance](../../../00.agent-governance/common-governance.md), [provider research](../../research/2026-07-04-wer/provider-implementation-status.md) | Local shared skill evidence exists, but tracked Claude MCP server configuration is absent. | Add or change MCP configuration only through a future approved task with least-privilege and credential-boundary review. |
| Claude feedback loops | Claude should turn work into deterministic signals through hooks, scripts, task evidence, and review. | Claude hooks route to shared scripts, the runtime baseline requires repo-static validation, and Stage 04 task evidence records command results. | Implemented | [.claude/settings.json](../../../../.claude/settings.json), [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md), [task record](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md), [harness implementation map](../../../00.agent-governance/harness-implementation-map.md) | Hook and static validation evidence does not prove live provider-runtime, cluster, cloud, secret, paid-job, or external-service readiness. | Keep feedback-loop evidence in Stage 04 and use approved operations paths for separate live checks. |
| Codex instruction/settings | Codex should have a thin gateway, provider notes, local runtime baseline, trusted project configuration where needed, and shared governance loading path. | `AGENTS.md`, Codex provider notes, `.codex/CODEX.md`, `.codex/hooks.json`, and `.codex/agents/*.toml` exist; this checkout does not track `.codex/config.toml`. | Partial | [AGENTS.md](../../../../AGENTS.md), [Codex provider notes](../../../00.agent-governance/providers/codex.md), [.codex/CODEX.md](../../../../.codex/CODEX.md), [.codex/hooks.json](../../../../.codex/hooks.json), [provider research](../../research/2026-07-04-wer/provider-implementation-status.md) | Repo instructions reference a trusted project `.codex/config.toml` baseline, but no tracked file proves local Codex config or MCP/project-agent registration. | If Codex project config becomes required, add it through a scoped provider-adapter task and preserve user config boundaries. |
| Codex subagents/agents | Codex should expose provider-native agent mirrors aligned with the common roster and sandbox/approval model. | Eight tracked `.codex/agents/*.toml` mirrors exist and preserve role, scope, guardrails, postflight, model, and reasoning-effort fields. | Partial | [.codex/agents/supervisor.toml](../../../../.codex/agents/supervisor.toml), [.codex/agents/k8s-implementer.toml](../../../../.codex/agents/k8s-implementer.toml), [subagent protocol](../../../00.agent-governance/subagent-protocol.md), [harness catalog](../../../00.agent-governance/harness-catalog.md) | Agent TOML files are present, but no tracked `.codex/config.toml` proves registration or live multi-agent runtime behavior. | Keep mirrors aligned through repo-quality gates; add registration evidence only through a future approved Codex config task. |
| Codex hooks/permissions | Codex should use sandbox/approval controls and lifecycle hook wiring without being treated as a Claude permission-gate clone. | `.codex/hooks.json` wires the shared lifecycle scripts and provider notes explicitly state it is context/validation wiring, not a permission gate. | Partial | [.codex/hooks.json](../../../../.codex/hooks.json), [Codex provider notes](../../../00.agent-governance/providers/codex.md), [.codex/CODEX.md](../../../../.codex/CODEX.md), [common governance](../../../00.agent-governance/common-governance.md) | Codex hook wiring does not prove native blocking permission parity with Claude settings. | Keep permission claims tied to Codex sandbox/approval behavior and explicit command validation, not hook wiring alone. |
| Codex skills/MCP/tooling | Codex should expose shared skills and MCP/tooling through trusted config while preserving least-privilege review. | `.codex/skills`, `.codex/workflows`, and `.codex/output-styles` are symlinks to `.agents/**`; no tracked `.codex/config.toml` proves enabled local Codex MCP servers. | Partial | [.agents skills](../../../../.agents/skills/workspace-harness-audit/skill.md), [.agents workflows](../../../../.agents/workflows/qa-cicd-workflow.md), [common governance](../../../00.agent-governance/common-governance.md), [provider research](../../research/2026-07-04-wer/provider-implementation-status.md) | Shared skills exist, but Codex MCP/tool configuration is not repo-backed in this checkout. | Route MCP additions through a future task with explicit approval for external or mutation-capable tools. |
| Codex feedback loops | Codex should run explicit repo-static validation and use hook wiring as supporting context where available. | `.codex/CODEX.md` requires explicit QA/CI validation; `.codex/hooks.json` routes shared lifecycle scripts; the task record stores command evidence. | Partial | [.codex/CODEX.md](../../../../.codex/CODEX.md), [.codex/hooks.json](../../../../.codex/hooks.json), [task record](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md), [harness implementation map](../../../00.agent-governance/harness-implementation-map.md) | Feedback is repo-static and behavioral; it does not prove live Codex runtime behavior or live environment readiness. | Continue recording explicit validation commands in Stage 04; use separate approved evidence for live/provider checks. |
| Gemini instruction/settings | Gemini should have a thin gateway, provider notes, local runtime baseline, workspace settings where needed, and shared governance loading path. | Root `GEMINI.md`, Gemini provider notes, `.agents/GEMINI.md`, `.agents/hooks.json`, and `.agents/agents/*.md` exist; no tracked `.gemini/settings.json` or `.gemini/` directory was found. | Partial | [GEMINI.md](../../../../GEMINI.md), [Gemini provider notes](../../../00.agent-governance/providers/gemini.md), [.agents/GEMINI.md](../../../../.agents/GEMINI.md), [.agents/hooks.json](../../../../.agents/hooks.json), [provider research](../../research/2026-07-04-wer/provider-implementation-status.md) | Runtime baseline evidence exists, but tracked native Gemini settings evidence is absent; individual Gemini agent files reference `AGENTS.md` even though the root Gemini path says `AGENTS.md` is not part of Gemini loading. | Reconcile Gemini agent bootstrap wording or add tracked settings only through a future provider-adapter task. |
| Gemini agents/subagents | Gemini should expose aligned provider agent files or clearly state behavioral delegation boundaries. | Eight tracked `.agents/agents/*.md` files exist and align role/scope/guardrail content with Claude and Codex mirrors. | Partial | [.agents/agents/supervisor.md](../../../../.agents/agents/supervisor.md), [.agents/agents/k8s-implementer.md](../../../../.agents/agents/k8s-implementer.md), [subagent protocol](../../../00.agent-governance/subagent-protocol.md), [harness catalog](../../../00.agent-governance/harness-catalog.md) | Repo evidence shows mirror files, not verified Gemini-native subagent dispatch or permission enforcement equivalent to Claude. | Keep `.agents/agents/` aligned and document any future Gemini-native delegation support before marking stronger parity. |
| Gemini hooks/permissions | Gemini should route shared pre/post validation where the runtime honors it and avoid overclaiming native permission parity. | `.agents/hooks.json` wires the shared lifecycle scripts and `.agents/GEMINI.md` states Gemini has no native permission-gate equivalent to Claude settings. | Partial | [.agents/hooks.json](../../../../.agents/hooks.json), [.agents/GEMINI.md](../../../../.agents/GEMINI.md), [Gemini provider notes](../../../00.agent-governance/providers/gemini.md), [common governance](../../../00.agent-governance/common-governance.md) | Hook wiring is behavioral and runtime-dependent; it is not a Claude-style permission gate. | Keep Gemini permission claims bounded to documented behavior and explicit validation evidence. |
| Gemini skills/MCP/tooling | Gemini should use shared skills and route MCP/tool changes through workspace settings and least-privilege review. | Shared `.agents/skills`, `.agents/workflows`, and `.agents/output-styles` exist; no tracked `.gemini/settings.json` proves local Gemini MCP server configuration. | Partial | [.agents skills](../../../../.agents/skills/workspace-harness-audit/skill.md), [.agents workflows](../../../../.agents/workflows/qa-cicd-workflow.md), [.agents output style](../../../../.agents/output-styles/hy-home-k8s.md), [provider research](../../research/2026-07-04-wer/provider-implementation-status.md) | Shared skills/tooling surfaces exist, but native Gemini MCP/tool settings are not repo-backed in this checkout. | Add Gemini MCP/tool configuration only through future approved work with least-privilege and credential-boundary review. |
| Gemini feedback loops | Gemini should preserve the observe/plan/act/verify loop through shared validation, hooks where honored, task evidence, and progress memory. | `.agents/GEMINI.md` requires repo-static validation; `.agents/hooks.json` wires shared lifecycle scripts; Stage 04 task evidence records validation results. | Partial | [.agents/GEMINI.md](../../../../.agents/GEMINI.md), [.agents/hooks.json](../../../../.agents/hooks.json), [task record](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md), [harness implementation map](../../../00.agent-governance/harness-implementation-map.md) | Feedback is repo-static and behavioral; it does not prove live Gemini runtime behavior or live environment readiness. | Continue recording validation evidence separately from live/provider readiness. |
| Common environment/rule/system parity | Shared governance should define one canonical model while provider adapters expose native or mirrored surfaces. | Stage 00 rules, common governance, harness catalog, implementation map, subagent protocol, gateway files, shared `.agents/**` assets, and validators define the common provider model. | Partial | [common governance](../../../00.agent-governance/common-governance.md), [harness catalog](../../../00.agent-governance/harness-catalog.md), [harness implementation map](../../../00.agent-governance/harness-implementation-map.md), [subagent protocol](../../../00.agent-governance/subagent-protocol.md), [AGENTS.md](../../../../AGENTS.md) | The common model is repo-backed, but native enforcement differs across providers. | Keep common rules in Stage 00 and provider-specific mechanics in provider adapters with validation evidence. |
| Known non-parity boundaries | The audit should explicitly identify provider differences rather than smoothing them into false equivalence. | Repo sources state Claude has native permission plus event wiring, while Codex and Gemini hook JSON files are context/validation or behavioral wiring; output-style and MCP evidence also differ. | Implemented | [common governance](../../../00.agent-governance/common-governance.md), [harness catalog](../../../00.agent-governance/harness-catalog.md), [Codex provider notes](../../../00.agent-governance/providers/codex.md), [Gemini provider notes](../../../00.agent-governance/providers/gemini.md), [provider research](../../research/2026-07-04-wer/provider-implementation-status.md) | Future edits could overstate parity if they count upstream capability without local repo surfaces. | Preserve non-parity notes in provider docs and audits; require repo-backed evidence before upgrading any status. |
| Automation opportunities | Repeated provider parity checks should become deterministic where feasible. | Repo-quality gates already check broad mirror and governance contracts, but this audit still required manual matrix review and local file-inventory checks. | Partial | [task record](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md), [harness catalog](../../../00.agent-governance/harness-catalog.md), [harness implementation map](../../../00.agent-governance/harness-implementation-map.md), [audits README](../README.md) | No dedicated validator proves every provider audit row has required evidence, absence findings, or provider-specific non-parity notes. | Add audit/provider parity validators only through a future Spec, Plan, Task, script change, and validation record. |

### Comparison Analysis

- Claude has the strongest local provider implementation evidence for native
  settings, command permissions, event hooks, and agent tool scoping because
  those surfaces are tracked in `.claude/settings.json` and
  `.claude/agents/*.md`.
- Codex has tracked gateway, runtime baseline, hook wiring, and agent TOML
  mirrors, but this checkout does not track `.codex/config.toml`. Local status
  should therefore stay conservative for Codex project configuration, agent
  registration, MCP, and permission parity.
- Gemini has tracked gateway, runtime baseline, hook wiring, shared assets, and
  agent mirror files, but this checkout does not track `.gemini/settings.json`
  or a `.gemini/` settings directory. Gemini hooks are explicitly behavioral
  where the runtime honors them, not a Claude-style permission gate.
- Shared `.agents/**` assets give all providers a common skill, workflow, and
  output-style source of truth, but shared assets do not prove identical native
  runtime enforcement.
- Repo-backed evidence outranks upstream provider capability. Upstream Claude,
  Codex, Gemini, or Google capability can inform the benchmark, but it does not
  prove local implementation without a tracked repository surface.
- Static validation and local file review do not prove live provider-runtime
  behavior, live cluster/cloud/secret readiness, paid-job readiness, or
  external-service readiness.

### Automation Opportunities

- Add a future provider audit validator that checks required matrix row labels,
  allowed audit status values, and evidence links for every provider row.
- Add a future file-inventory check that reports whether `.codex/config.toml`,
  `.mcp.json`, `.gemini/settings.json`, or other provider settings files are
  tracked before any audit claims local MCP or native settings implementation.
- Add a future provider-agent parity check that compares role names, scope
  imports, guardrails, postflight language, model-tier routing, and known
  non-parity notes across `.claude/agents/`, `.codex/agents/`, and
  `.agents/agents/`.
- Add a future README-index check that flags planned audit filenames once the
  corresponding report exists.
- Keep any automation behind a separate Spec, Plan, Task, script update, and
  validation record; this audit does not implement automation.

### Implementation Checklist

- [x] Used `docs/99.templates/templates/common/reference.template.md` as the authoring base.
- [x] Included the required reference-template sections.
- [x] Included the required audit subsections under `Definitions / Facts`.
- [x] Covered Claude instruction/settings, subagents/agents,
  hooks/permissions, skills/MCP/tooling, and feedback loops.
- [x] Covered Codex instruction/settings, subagents/agents,
  hooks/permissions, skills/MCP/tooling, and feedback loops.
- [x] Covered Gemini instruction/settings, agents/subagents,
  hooks/permissions, skills/MCP/tooling, and feedback loops.
- [x] Covered common environment/rule/system parity, known non-parity
  boundaries, and automation opportunities.
- [x] Used only `Implemented`, `Partial`, `Gap`, and `Not in scope` as audit
  status values.
- [x] Cited repo-backed evidence paths for every `Implemented` and `Partial`
  matrix claim.
- [x] Kept the audit descriptive and bounded to repository evidence.
- [ ] Future work: automate provider audit row coverage, absence checks, and
  status-vocabulary review if recurring audit packs need stronger mechanical
  assurance.

### Residual Risks

- This audit is a 2026-07-02 repository snapshot. It can become stale when
  provider docs, Stage 00 governance, gateway files, runtime baselines, hook
  wiring, provider agents, shared `.agents/**` assets, MCP configuration,
  scripts, CI workflows, operations guides, or research benchmarks change.
- Static repo evidence does not prove live Claude, Codex, Gemini, k3d, ArgoCD,
  Vault, ESO, Kubernetes, cloud, deployment, secret, paid-job, or
  external-service readiness.
- Provider runtime behavior can diverge from documented expectations if a
  provider ignores behavioral instructions, does not load a local file, lacks a
  native permission gate, or changes upstream semantics.
- MCP/tool-boundary evidence is incomplete for local provider configuration in
  this checkout; no tracked `.mcp.json`, `.codex/config.toml`, or
  `.gemini/settings.json` was found during this audit.
- Gemini provider-agent bootstrap wording may need future reconciliation
  because the root Gemini runtime baseline excludes `AGENTS.md` from the Gemini
  loading path while checked Gemini agent files still mention loading it.
- Audit-specific automation remains future work; current assurance combines
  manual provider matrix review with broad repository quality gates.

## Sources

- [Provider Harness Implementation Status Research](../../research/2026-07-04-wer/provider-implementation-status.md)
- [Workspace Harness Implementation Audit Pack Spec](../../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md)
- [Workspace Harness Implementation Audit Pack Plan](../../../04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md)
- [AGENTS.md](../../../../AGENTS.md)
- [CLAUDE.md](../../../../CLAUDE.md)
- [GEMINI.md](../../../../GEMINI.md)
- [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md)
- [.codex/CODEX.md](../../../../.codex/CODEX.md)
- [.agents/GEMINI.md](../../../../.agents/GEMINI.md)
- [.claude/settings.json](../../../../.claude/settings.json)
- [.codex/hooks.json](../../../../.codex/hooks.json)
- [.agents/hooks.json](../../../../.agents/hooks.json)
- [Claude Provider Notes](../../../00.agent-governance/providers/claude.md)
- [Codex Provider Notes](../../../00.agent-governance/providers/codex.md)
- [Gemini Provider Notes](../../../00.agent-governance/providers/gemini.md)
- [Common Governance & Mappings](../../../00.agent-governance/common-governance.md)
- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)
- [Workspace Harness Implementation Audit Pack Task](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-02
- Next review trigger: Claude, Codex, Gemini, Stage 00 provider notes, gateway
  files, runtime baselines, provider agents, hook wiring, shared `.agents/**`
  assets, MCP configuration, audit benchmark, audit-index change, or provider
  runtime evidence change.
- Refresh this report when tracked provider settings appear, provider MCP
  configuration changes, provider agent registration evidence changes, or
  validation automation gains provider-audit coverage.

## Related Documents

- **Audits README**: [README.md](../README.md)
- **Research benchmark**: [Provider Harness Implementation Status Research](../../research/2026-07-04-wer/provider-implementation-status.md)
- **Parent Spec**: [Workspace Harness Implementation Audit Pack Spec](../../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md)
- **Parent Plan**: [Workspace Harness Implementation Audit Pack Plan](../../../04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md)
- **Task record**: [Workspace Harness Implementation Audit Pack Task](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md)
- **Progress memory**: [Agent Progress and Memory Ledger](../../../00.agent-governance/memory/progress.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
