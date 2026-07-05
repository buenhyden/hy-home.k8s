---
title: 'Reference: Governance Harness Loop Provider Implementation Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-05
---

# Reference: Governance Harness Loop Provider Implementation Audit

## Overview

This dated audit compares the governance, harness, loop, and provider adapter
benchmark model to current repo-backed implementation evidence in
`hy-home.k8s` as checked on 2026-07-05.

This audit is descriptive reference material. It does not change active
governance policy, provider runtime configuration, hook behavior, CI semantics,
scripts, templates, manifests, approval boundaries, or live operations
procedure.

## Purpose

- Record whether the researched governance, harness, loop, and provider model
  is implemented in current repository surfaces.
- Separate benchmark expectations, repo-backed implementation evidence,
  provider non-parity, automation opportunities, and residual risks.
- Preserve a bounded follow-up route without claiming live-runtime readiness.

## Reference Type

- Type: dated-implementation-audit / external-standard-snapshot
- Source checked: 2026-07-05
- Refresh trigger: Stage 00 governance, provider adapters, harness catalog,
  implementation map, hook wiring, shared `.agents/**` assets, validation
  scripts, research benchmark, or audit-index changes.

## Authority Boundary

- **Authoritative for**:
  - Governance, harness, loop, and provider implementation audit findings as
    checked on 2026-07-05.
  - Repo-backed evidence paths used for this dated comparison.
  - Candidate follow-up routes for future specs, plans, tasks, validators,
    provider adapters, or operations documents.
- **Not authoritative for**:
  - Active governance policy, provider runtime permissions, CI enforcement
    semantics, approval boundaries, scripts, templates, or operations runbooks.
  - Live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, secret,
    paid-job, or external-service readiness.
  - New provider roles, hooks, validators, MCP servers, tool permissions,
    automation changes, or third-party mutations.

## Scope

- Covers workspace purpose, governance rules, template and script routing,
  harness instruction/settings surfaces, architecture constraints, feedback
  loops, knowledge stores, observe/plan/act/verify/learn loops, eval/review
  loops, Claude, Codex, Gemini, common provider parity, and known non-parity
  boundaries.
- Uses the 2026-07-04 research pack as benchmark context and current repository
  files as local implementation evidence.
- Excludes live runtime checks, external provider runtime execution, secret
  reads, network mutation, policy changes, script changes, workflow changes,
  provider adapter rewrites, and MCP server installation or configuration.

## Definitions / Facts

### Benchmark Model

The benchmark model expects a repo-first governance and harness system for a
WSL2+k3d home-lab platform managed through ArgoCD GitOps. The workspace should
use thin gateway files, Stage 00 governance, provider adapters, template-first
documentation, explicit repo-static validation, separate live-runtime evidence
lanes, and Stage 04 task evidence.

The harness benchmark expects four linked elements: instruction/settings
surfaces, architecture constraints, feedback loops, and knowledge stores. The
loop benchmark expects observe/plan/act/verify/learn behavior, explicit
eval/review evidence, least-privilege tool boundaries, and scoped repair loops.

The provider benchmark expects Claude, Codex, and Gemini to route through a
shared canonical core while preserving native provider differences. Upstream
provider capability is benchmark context only. Local implementation status
requires repo-backed evidence in tracked gateway files, provider baselines,
provider notes, adapter files, hooks, shared assets, governance docs, scripts,
task evidence, or managed runtime configuration.

### Implementation Matrix

| Area | Benchmark expectation | Current implementation | Status | Evidence | Gap or risk | Follow-up route |
| --- | --- | --- | --- | --- | --- | --- |
| workspace purpose and operating model | Agents operate from repo-backed desired state for a WSL2+k3d ArgoCD GitOps home-lab and separate repo-static evidence from live-runtime readiness. | Thin gateway files, runtime baselines, the research baseline, catalog, and implementation map state the GitOps-first domain, repo-backed work model, validation-first handoff, and static/live evidence split. | Implemented | [AGENTS.md](../../../../AGENTS.md), [CLAUDE.md](../../../../CLAUDE.md), [GEMINI.md](../../../../GEMINI.md), [.codex/CODEX.md](../../../../.codex/CODEX.md), [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), [harness-implementation-map.md](../../../00.agent-governance/harness-implementation-map.md) | Repo-static documentation does not prove live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, or secret readiness. | Keep operating-model changes in Stage 00 gateway/runtime owners and record validation in Stage 04. |
| rules and governance system | Agents load bootstrap, preflight, persona/scope, provider notes, memory, and postflight before substantial work. | Stage 00 rules define JIT loading, preflight, persona/scope routing, agentic execution, approval boundaries, documentation routing, quality standards, and postflight. | Implemented | [bootstrap.md](../../../00.agent-governance/rules/bootstrap.md), [preflight-checklist.md](../../../00.agent-governance/rules/preflight-checklist.md), [persona.md](../../../00.agent-governance/rules/persona.md), [agentic.md](../../../00.agent-governance/rules/agentic.md), [approval-boundaries.md](../../../00.agent-governance/rules/approval-boundaries.md), [postflight-checklist.md](../../../00.agent-governance/rules/postflight-checklist.md) | Compliance still depends on the active agent honoring loaded context and running validation. | Route rule changes to the smallest Stage 00 owner, with task evidence and quality-gate validation. |
| template and script routing | Authored docs use stage templates and scripts provide deterministic repo-static validation. | Documentation protocol, document-stage routing, templates README, reference template, script inventory, and quality gates define Template-First writing and validation routing. | Implemented | [documentation-protocol.md](../../../00.agent-governance/rules/documentation-protocol.md), [document-stage-routing.md](../../../00.agent-governance/rules/document-stage-routing.md), [templates README](../../../99.templates/README.md), [reference.template.md](../../../99.templates/templates/common/reference.template.md), [scripts README](../../../../scripts/README.md) | Static validators cannot judge all subjective audit quality and do not prove live-runtime readiness. | Keep template changes in `docs/99.templates/**`; keep validator semantics in `scripts/**` plus Stage 04 evidence. |
| harness instruction/settings surfaces | Each provider has a thin gateway and runtime baseline that route to canonical governance without duplicating policy. | Root shims and provider baselines route Claude, Codex, and Gemini into Stage 00, provider notes, progress memory, and postflight. | Implemented | [CLAUDE.md](../../../../CLAUDE.md), [AGENTS.md](../../../../AGENTS.md), [GEMINI.md](../../../../GEMINI.md), [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md), [.codex/CODEX.md](../../../../.codex/CODEX.md), [.agents/GEMINI.md](../../../../.agents/GEMINI.md), [providers](../../../00.agent-governance/providers/) | Instruction loading is procedural and provider-dependent; a runtime can still ignore or miss context. | Update gateway, provider notes, runtime baseline, catalog, and task evidence together when routing changes. |
| harness architecture constraints | The harness blocks or routes unsafe, off-domain, stale, or unsupported action through approval boundaries, sandboxing, provider permissions, and template/rule constraints. | Approval boundaries, agentic rules, subagent protocol, model policy, documentation protocol, and provider settings/hook wiring define no-live-mutation, no-secret, GitOps-first, model, tool, and document boundaries. | Partial | [approval-boundaries.md](../../../00.agent-governance/rules/approval-boundaries.md), [agentic.md](../../../00.agent-governance/rules/agentic.md), [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md), [model-policy.md](../../../00.agent-governance/model-policy.md), [.claude/settings.json](../../../../.claude/settings.json), [.codex/hooks.json](../../../../.codex/hooks.json), [.agents/hooks.json](../../../../.agents/hooks.json) | Claude has tracked native permissions; Codex and Gemini hook JSON are context/validation wiring, not equivalent permission gates. | Preserve provider-native enforcement differences in provider notes and route stronger enforcement to a future scoped provider task. |
| harness feedback loops | Edits produce repeatable signals through hooks, validators, CI, task records, and review. | Shared hook scripts, provider hook wiring, repository quality gates, CI lanes, and Stage 04 task records provide repo-static feedback and evidence. | Implemented | [.claude/settings.json](../../../../.claude/settings.json), [.codex/hooks.json](../../../../.codex/hooks.json), [.agents/hooks.json](../../../../.agents/hooks.json), [hooks](../../../00.agent-governance/hooks/), [scripts README](../../../../scripts/README.md), [GitHub CI workflow](../../../../.github/workflows/ci.yml), [task record](../../../04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md) | Static feedback does not prove live runtime readiness or external provider availability. | Record command evidence in Stage 04 and use approved operations runbooks for live checks. |
| harness knowledge stores | Durable context feeds future sessions without making memory or references active policy. | Progress memory, memory README, harness catalog, implementation map, research references, audit references, generated wiki index, and task records separate runtime truth, evidence, reference, and memory. | Implemented | [memory README](../../../00.agent-governance/memory/README.md), [progress.md](../../../00.agent-governance/memory/progress.md), [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), [harness-implementation-map.md](../../../00.agent-governance/harness-implementation-map.md), [research pack](../../research/2026-07-04-wer/README.md), [audits README](../README.md) | References can become stale when canonical owners change. | Refresh dated references on source change and route durable behavior changes to canonical owners. |
| observe/plan/act/verify/learn loop | Agents observe evidence, plan scoped work, act in approved files, verify deterministically, and route lessons to owners. | Bootstrap, preflight, agentic rules, task evidence, validation scripts, postflight, memory routing, and the harness research pack document the loop. | Implemented | [bootstrap.md](../../../00.agent-governance/rules/bootstrap.md), [preflight-checklist.md](../../../00.agent-governance/rules/preflight-checklist.md), [agentic.md](../../../00.agent-governance/rules/agentic.md), [postflight-checklist.md](../../../00.agent-governance/rules/postflight-checklist.md), [harness-and-loop-engineering.md](../../research/2026-07-04-wer/harness-and-loop-engineering.md), [task record](../../../04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md) | The loop is procedural and evidence-driven, not a single automated orchestrator. | Convert repeated misses into rules, templates, hooks, validators, task evidence, or memory updates. |
| eval/review loop | Completion is based on explicit command evidence, task criteria, graders/checks, or recorded human/operator approval. | Harness catalog defines agent eval completion from explicit command evidence or approval; scripts, CI, task records, and review agents provide review surfaces. | Partial | [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), [scripts README](../../../../scripts/README.md), [GitHub CI workflow](../../../../.github/workflows/ci.yml), [.claude/agents/code-reviewer.md](../../../../.claude/agents/code-reviewer.md), [.codex/agents/code-reviewer.toml](../../../../.codex/agents/code-reviewer.toml), [.agents/agents/code-reviewer.md](../../../../.agents/agents/code-reviewer.md) | There is no dedicated audit-matrix grader proving required row coverage, status vocabulary, or subjective audit quality beyond manual review and repo quality gates. | Add audit-specific eval automation only through a future Spec, Plan, Task, validator, or CI update. |
| Claude instruction/settings, agents, hooks/permissions, skills/MCP/tooling, feedback loops | Claude should route through shared governance while using native settings, agents, hooks, permissions, shared assets, and validation evidence. | Claude has root and local baselines, provider notes, tracked native settings with allow/deny policy, eight `.claude/agents/*.md` role adapters, shared hook scripts, and symlinked skills/workflows/output styles. | Implemented | [CLAUDE.md](../../../../CLAUDE.md), [.claude/CLAUDE.md](../../../../.claude/CLAUDE.md), [providers/claude.md](../../../00.agent-governance/providers/claude.md), [.claude/settings.json](../../../../.claude/settings.json), [.claude/agents](../../../../.claude/agents/), [.claude/skills](../../../../.claude/skills), [.claude/workflows](../../../../.claude/workflows), [.claude/output-styles](../../../../.claude/output-styles) | Exact blocking behavior still depends on current Claude runtime semantics, event type, and user/managed settings outside this repo. | Keep Claude enforcement changes in `.claude/settings.json`, shared hooks, provider notes, catalog, and task evidence. |
| Codex instruction/settings, agents, hooks/permissions, skills/MCP/tooling, feedback loops | Codex should route through AGENTS.md, Codex baseline, sandbox/approval model, native agents, hooks, shared assets, and explicit validation. | Codex has AGENTS.md, `.codex/CODEX.md`, provider notes, `.codex/agents/*.toml`, `.codex/hooks.json`, and symlinked shared assets. Repo docs state Codex hook JSON is context/validation wiring and explicit validation remains required. | Partial | [AGENTS.md](../../../../AGENTS.md), [.codex/CODEX.md](../../../../.codex/CODEX.md), [providers/codex.md](../../../00.agent-governance/providers/codex.md), [.codex/hooks.json](../../../../.codex/hooks.json), [.codex/agents](../../../../.codex/agents/), [.codex/skills](../../../../.codex/skills), [.codex/workflows](../../../../.codex/workflows), [.codex/output-styles](../../../../.codex/output-styles) | No tracked `.codex/config.toml` is present in this checkout, and `.codex/hooks.json` is not a Claude-style permission gate. Upstream Codex MCP/config capability is not proof of enabled local MCP servers. | Route Codex config, MCP, permission, or hook changes through a future scoped provider task with human approval where external mutation or credentials are involved. |
| Gemini instruction/settings, agents, hooks/permissions, skills/MCP/tooling, feedback loops | Gemini should route through Gemini gateway, local `.agents/**` baseline, shared assets, hook wiring, and explicit validation while preserving native limitations. | Gemini has root and `.agents/GEMINI.md` baselines, provider notes, `.agents/agents/*.md`, `.agents/hooks.json`, shared skills/workflows/output styles, workspace rules, and QA workflow docs. | Partial | [GEMINI.md](../../../../GEMINI.md), [.agents/GEMINI.md](../../../../.agents/GEMINI.md), [providers/gemini.md](../../../00.agent-governance/providers/gemini.md), [.agents/hooks.json](../../../../.agents/hooks.json), [.agents/agents](../../../../.agents/agents/), [.agents/skills](../../../../.agents/skills/), [.agents/workflows](../../../../.agents/workflows/), [.agents/rules/workspace-rules.md](../../../../.agents/rules/workspace-rules.md) | Repo evidence does not prove Gemini has Claude-style native permission-gate parity or that Google ADK/Gemini Code Assist capabilities are active in this checkout. | Keep Gemini parity claims tied to `.agents/**`, provider notes, catalog evidence, and explicit validation. |
| common provider environment/rule/system parity | Common behavior should come from a canonical core plus provider adapters, not copied policy in every provider file. | Harness catalog defines the canonical adapter ownership model; root shims, provider notes, runtime baselines, provider agent files, shared `.agents/**` assets, hooks, scripts, and quality gates implement parity at the repo-static layer. | Implemented | [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), [common-governance.md](../../../00.agent-governance/common-governance.md), [providers](../../../00.agent-governance/providers/), [AGENTS.md](../../../../AGENTS.md), [CLAUDE.md](../../../../CLAUDE.md), [GEMINI.md](../../../../GEMINI.md), [.agents](../../../../.agents/) | Parity means role/rule/system alignment plus validation evidence, not identical native provider enforcement. | Update catalog, implementation map, provider notes, adapters, shared assets, and task evidence together when parity changes. |
| known non-parity boundaries | Similar provider nouns such as hooks, skills, agents, MCP, settings, and evals must not be treated as identical enforcement. | Provider research and local docs distinguish Claude settings/hooks/agents, Codex sandbox/approval/hooks/agents, Gemini `.agents/**` behavioral mirrors, and shared static validation. | Partial | [provider-implementation-status.md](../../research/2026-07-04-wer/provider-implementation-status.md), [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), [providers/claude.md](../../../00.agent-governance/providers/claude.md), [providers/codex.md](../../../00.agent-governance/providers/codex.md), [providers/gemini.md](../../../00.agent-governance/providers/gemini.md), [.claude/settings.json](../../../../.claude/settings.json), [.codex/hooks.json](../../../../.codex/hooks.json), [.agents/hooks.json](../../../../.agents/hooks.json) | Provider runtime behavior, MCP availability, managed settings, and live external integrations can diverge from repo-static documentation. | Keep non-parity explicit in future reports and require repo-backed evidence before marking provider features Implemented. |

### Comparison Analysis

- The core governance and harness model is implemented as repo-backed
  documentation, provider baselines, shared assets, hook wiring, validators,
  CI lanes, and Stage 04 task evidence.
- The strongest implementation evidence is repo-static. It supports
  traceability, template routing, validation, and handoff, but it does not
  prove live-runtime, provider-runtime, Kubernetes, cloud, secret, or external
  readiness.
- The four-element harness model is present across common owners and provider
  adapters: instructions/settings, architecture constraints, feedback loops,
  and knowledge stores.
- The observe/plan/act/verify/learn loop is implemented as governance
  procedure and evidence practice. It is not a single automated runtime engine.
- Provider parity is intentionally bounded. Claude has tracked native
  settings/permissions, Codex has sandbox/approval plus context/validation hook
  wiring, and Gemini has `.agents/**` behavioral mirrors and shared assets.
- MCP and upstream provider capabilities remain benchmark context unless a
  tracked local adapter, config, script, task record, or managed runtime owner
  proves implementation.

### Automation Opportunities

- Add a future audit-matrix validator for required rows, exact column headers,
  allowed status vocabulary, and evidence links on `Implemented` and `Partial`
  rows.
- Add a future audit-pack README check that turns planned code literals into
  Markdown links when reports are created.
- Add a future provider non-parity check that flags language claiming Codex or
  Gemini hook JSON is equivalent to Claude native permission gates.
- Add a future MCP/tool-boundary checklist before adding or changing provider
  MCP configuration.
- Add a future eval/review lane for audit subjective quality if recurring audit
  packs need model or human reviewer sign-off beyond repo-static gates.

### Implementation Checklist

- [x] Used the local reference template section model.
- [x] Included the required frontmatter exactly.
- [x] Included the required reference sections.
- [x] Included Benchmark Model, Implementation Matrix, Comparison Analysis,
  Automation Opportunities, Implementation Checklist, and Residual Risks.
- [x] Used the exact implementation matrix columns:
  `Area | Benchmark expectation | Current implementation | Status | Evidence | Gap or risk | Follow-up route`.
- [x] Covered workspace purpose, governance rules, template and script routing,
  harness surfaces, observe/plan/act/verify/learn, eval/review, Claude, Codex,
  Gemini, common provider parity, and known non-parity boundaries.
- [x] Used only `Implemented`, `Partial`, `Gap`, and `Not in scope` as audit
  status values.
- [x] Used repo-backed evidence only for implementation status claims.
- [x] Preserved the static-validation boundary: repo-static checks do not prove
  live-runtime readiness.
- [ ] Future work: automate matrix row coverage, evidence links, and status
  vocabulary checks if audit packs recur.

### Residual Risks

- This audit is a 2026-07-05 repository snapshot and can become stale when
  Stage 00 governance, provider adapters, hooks, scripts, templates, CI,
  operations docs, research benchmark files, or shared `.agents/**` assets
  change.
- Static validation and repo-backed documentation do not prove live k3d,
  ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, secret, paid-job,
  provider-runtime, or external-service readiness.
- Provider runtime behavior may diverge from documented expectations if a
  provider ignores behavioral instructions, lacks native permission gates, or
  uses untracked user/managed configuration.
- The current eval/review loop is strongest for deterministic repo checks;
  audit matrix completeness and subjective documentation quality still rely on
  manual review.
- MCP/tooling claims remain conservative because upstream provider support does
  not prove enabled local servers, safe scopes, credentials, or runtime
  readiness.

## Sources

- [Workspace Governance Baseline Research](../../research/2026-07-04-wer/workspace-governance-baseline.md)
- [Harness and Loop Engineering Research](../../research/2026-07-04-wer/harness-and-loop-engineering.md)
- [Provider Harness Implementation Status Research](../../research/2026-07-04-wer/provider-implementation-status.md)
- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
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
- [AGENTS.md Provider Notes](../../../00.agent-governance/providers/agents-md.md)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-05
- Next review trigger: Stage 00 governance, provider adapter, runtime baseline,
  hook wiring, `.agents/**` shared asset, harness catalog, implementation map,
  validation script, CI workflow, research benchmark, audit-index, MCP/tooling,
  or status-vocabulary change.
- Refresh this report when repo-static evidence, provider non-parity language,
  or live-runtime boundary language changes.

## Related Documents

- **Audit pack README**: [README.md](./README.md)
- **Audits README**: [Parent audits index](../README.md)
- **Parent Plan**: [Workspace Engineering Implementation Audit Pack Plan](../../../04.execution/plans/2026-07-05-workspace-engineering-implementation-audit-pack.md)
- **Task record**: [Workspace Engineering Implementation Audit Pack Task](../../../04.execution/tasks/2026-07-05-workspace-engineering-implementation-audit-pack.md)
- **Research Pack README**: [Workspace Engineering Research Pack](../../research/2026-07-04-wer/README.md)
- **Progress memory**: [Agent Progress and Memory Ledger](../../../00.agent-governance/memory/progress.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
