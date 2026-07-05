---
title: 'Reference: Harness and Loop Implementation Audit'
type: content/reference
status: draft
owner: platform
updated: 2026-07-02
---

# Reference: Harness and Loop Implementation Audit

## Overview

This dated audit compares the harness and loop engineering benchmark model to
current repo-backed implementation evidence in `hy-home.k8s` as checked on
2026-07-02. It is descriptive reference material for maintainers and future
agents.

This audit does not change active governance policy, provider runtime behavior,
CI semantics, scripts, templates, manifests, approval boundaries, or live
cluster procedure.

## Purpose

- Record whether the researched harness and loop engineering model is
  implemented in current repository surfaces.
- Separate benchmark expectations, repo-backed evidence, gaps, automation
  opportunities, and residual risks.
- Provide a bounded follow-up checklist without redefining active policy or
  claiming live runtime readiness.

## Reference Type

- Type: durable-concept / external-standard-snapshot
- Source checked: 2026-07-02
- Refresh trigger: harness catalog, implementation map, subagent protocol,
  agentic rules, memory routing, validation-loop, MCP/tool-boundary, audit
  benchmark, or audit-index changes.

## Authority Boundary

- **Authoritative for**:
  - Harness and loop implementation audit findings as checked on 2026-07-02.
  - Repo-backed evidence paths used for this dated comparison.
  - Candidate follow-up routes for future specs, plans, tasks, validators,
    provider adapters, or operations documents.
- **Not authoritative for**:
  - Active governance policy, provider runtime configuration, CI enforcement
    semantics, approval boundaries, scripts, templates, or operations runbooks.
  - Live k3d, ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, secret, paid
    job, or external-service readiness.
  - New provider roles, hooks, validators, MCP servers, tool permissions, or
    automation changes.

## Scope

- Covers instruction/settings surfaces, architecture constraints, feedback
  loops, knowledge stores, observe/plan/act/verify/learn loops, eval/review
  loops, subagent/worktree/review practices, MCP/tool boundary implications,
  and automation opportunities.
- Uses the harness and loop engineering research reference as the benchmark and
  current repository files as local implementation evidence.
- Excludes live environment checks, provider-runtime execution tests, secret
  reads, policy changes, script changes, workflow changes, runtime adapter
  changes, and MCP server installation or configuration.

## Definitions / Facts

### Benchmark Model

The benchmark model treats harness engineering as the environment that lets an
agent act safely and usefully, and loop engineering as the repeated control
cycle that moves work from intent to verified handoff. It expects four linked
harness elements: instruction/settings surfaces, architecture constraints,
feedback loops, and knowledge stores.

The benchmark also expects an observe/plan/act/verify/learn loop, deterministic
repo-static evidence before handoff, scoped repair loops, explicit eval/review
evidence, conservative subagent and worktree practices, least-privilege tool
boundaries, and clear separation between static repository validation and live
runtime readiness.

### Implementation Matrix

| Area | Benchmark expectation | Current implementation | Status | Evidence | Gap or risk | Follow-up route |
| --- | --- | --- | --- | --- | --- | --- |
| Instruction/settings surfaces | Agents load thin gateways, provider baselines, scope docs, templates, and task context before acting. | The repository defines thin gateway routing, JIT loading, Codex runtime baseline, provider notes, and the four-element harness model. | Implemented | [AGENTS.md](../../../../AGENTS.md), [.codex/CODEX.md](../../../../.codex/CODEX.md), [bootstrap.md](../../../00.agent-governance/rules/bootstrap.md), [codex.md](../../../00.agent-governance/providers/codex.md), [harness-catalog.md](../../../00.agent-governance/harness-catalog.md) | Instruction compliance still depends on the active agent loading the right scoped context. | Keep gateway and provider changes in Stage 00 and runtime adapter owners, with Stage 04 evidence for repo-changing work. |
| Architecture constraints | The harness blocks or routes unsafe, off-domain, stale, or unsupported action. | Agentic rules, subagent protocol, documentation routing, approval boundaries, and the implementation map define sandbox, GitOps-first, template, live-mutation, and evidence boundaries. | Implemented | [agentic.md](../../../00.agent-governance/rules/agentic.md), [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md), [documentation-protocol.md](../../../00.agent-governance/rules/documentation-protocol.md), [approval-boundaries.md](../../../00.agent-governance/rules/approval-boundaries.md), [harness-implementation-map.md](../../../00.agent-governance/harness-implementation-map.md) | Provider-native enforcement is not identical across Claude, Codex, and Gemini. | Keep constraint changes in canonical governance owners and update provider adapters only through a future scoped task. |
| Feedback loops | Edits produce repeatable signals through validators, hooks, CI, task evidence, and review. | Repo-static validation scripts, Codex hook wiring, task evidence, CI lanes, and the implementation map provide feedback paths for documentation and infrastructure changes. | Implemented | [scripts/README.md](../../../../scripts/README.md), [.codex/hooks.json](../../../../.codex/hooks.json), [harness-implementation-map.md](../../../00.agent-governance/harness-implementation-map.md), [task record](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md), [.github/workflows/ci.yml](../../../../.github/workflows/ci.yml) | Static feedback does not prove live runtime readiness or subjective content quality. | Keep validation evidence in Stage 04 and use approved runbooks for separate live-runtime checks. |
| Knowledge stores | Durable context feeds future sessions without making memory a policy override. | The catalog, implementation map, memory README, progress ledger, research references, and task records separate current runtime truth, navigation, reusable memory, and execution evidence. | Implemented | [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), [harness-implementation-map.md](../../../00.agent-governance/harness-implementation-map.md), [memory README](../../../00.agent-governance/memory/README.md), [progress.md](../../../00.agent-governance/memory/progress.md), [task record](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md) | This task's explicit write scope does not include updating progress memory. | Record task-specific evidence in the scoped Stage 04 task; update progress memory in a future task whose write scope includes it. |
| Observe/plan/act/verify/learn loop | Agents should observe evidence, plan scoped work, act in approved files, verify deterministically, and route lessons to owners. | Bootstrap, preflight, persona/scope routing, agentic rules, task evidence, validations, and memory routing document the loop for repo-changing work. | Implemented | [bootstrap.md](../../../00.agent-governance/rules/bootstrap.md), [preflight-checklist.md](../../../00.agent-governance/rules/preflight-checklist.md), [persona.md](../../../00.agent-governance/rules/persona.md), [agentic.md](../../../00.agent-governance/rules/agentic.md), [memory README](../../../00.agent-governance/memory/README.md) | The loop is mostly procedural and evidence-driven, not a single automated orchestrator. | Keep repeated drift fixes routed to the smallest owner: rule, template, hook, validator, README, archive index, task evidence, or memory. |
| Eval/review loops | Completion should be based on explicit command evidence, task criteria, graders/checks, or recorded human/operator approval. | The harness catalog defines the agent eval completion contract, the task record stores evidence, and validation scripts/CI provide repeatable regression checks. | Partial | [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), [task record](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md), [scripts/README.md](../../../../scripts/README.md), [.github/workflows/ci.yml](../../../../.github/workflows/ci.yml), [agentic.md](../../../00.agent-governance/rules/agentic.md) | There is no dedicated trace/eval suite for audit matrix quality, subjective review, or harness-loop behavior beyond repo-static gates and manual review. | Add audit/eval automation only through a future Spec, Plan, Task, validator, or CI update. |
| Subagent/worktree/review-loop practices | Delegated work should be scoped, evidence-backed, reviewable, and isolated where practical. | The subagent protocol defines Task-tool dispatch, least-privilege tool scoping, mirror requirements, file ownership, postflight, and coordination; the catalog records local agents and mirror checks. | Partial | [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md), [harness-catalog.md](../../../00.agent-governance/harness-catalog.md), [harness-implementation-map.md](../../../00.agent-governance/harness-implementation-map.md), [agentic.md](../../../00.agent-governance/rules/agentic.md) | The repository documents task-by-task commits and subagent boundaries, but does not provide worktree automation or a dedicated review-loop runner for this audit pack. | Future multi-agent/worktree automation should start from Stage 04 evidence needs and preserve least-privilege file ownership. |
| MCP/tool boundary implications | Tool access should be least-privilege, consent-aware, scoped, auditable, and resistant to misleading tool metadata. | The repo has approval boundaries, subagent tool scoping, Codex hook wiring, graphify advisory rules, and read-only/default live boundaries, but no dedicated MCP inventory or MCP-specific security checklist in the required evidence set. | Partial | [approval-boundaries.md](../../../00.agent-governance/rules/approval-boundaries.md), [subagent-protocol.md](../../../00.agent-governance/subagent-protocol.md), [.codex/hooks.json](../../../../.codex/hooks.json), [graphify rule](../../../../.agents/rules/graphify.md), [harness-catalog.md](../../../00.agent-governance/harness-catalog.md) | Local MCP/tool security is bounded through general approval and tool-scope rules; MCP-specific poisoning, server update, and scope review are not implemented as a dedicated repo check. | Route MCP-specific hardening to a future security/governance task before adding or changing MCP servers. |
| Automation opportunities | Repeated loop, evidence, and audit checks should become deterministic where feasible. | Broad repository quality gates, generated-index checks, CI, and hook wiring exist; audit-specific matrix/evidence validation remains manual for this task. | Partial | [scripts/README.md](../../../../scripts/README.md), [harness-implementation-map.md](../../../00.agent-governance/harness-implementation-map.md), [.github/workflows/ci.yml](../../../../.github/workflows/ci.yml), [.codex/hooks.json](../../../../.codex/hooks.json), [audits README](../README.md) | No current validator proves every audit matrix row has evidence, required row coverage, or current README availability after a file is created. | Open a future implementation task before adding audit-specific validators, generated summaries, or hook/CI changes. |

### Comparison Analysis

- The core four-element harness model is implemented as a repo-backed control
  model with gateway/runtime instructions, Stage 00 constraints, validation
  feedback, and durable knowledge stores.
- The observe/plan/act/verify/learn loop is present as governance procedure,
  task evidence, validation commands, and memory routing. It is not a single
  automated loop engine.
- Eval and review evidence is strongest for deterministic repository checks.
  Manual review remains necessary for benchmark comparison, matrix judgment,
  and subjective documentation quality.
- Subagent and tool boundaries are documented, but worktree automation,
  provider-runtime execution tests, and MCP-specific security automation remain
  future work.
- Static repository validation is a useful feedback lane, but it does not prove
  live k3d, ArgoCD, Vault, ESO, Kubernetes, deployment, secret, paid-job, or
  external-service readiness.

### Automation Opportunities

- Add a future audit-matrix validator that checks required row labels, allowed
  audit status values, and evidence links for every `Implemented` and
  `Partial` row.
- Add a future README-index check that flags planned audit filenames once the
  corresponding report exists.
- Add a future harness-loop checklist generator that maps Stage 04 task
  evidence to observe/plan/act/verify/learn phases without changing active
  policy.
- Add a future MCP/tool-boundary checklist before adding or changing local MCP
  server configuration.
- Add a future review-loop lane for audit reports if repeated packs require
  model/human reviewer sign-off beyond manual matrix review.

### Implementation Checklist

- [x] Used `docs/99.templates/templates/common/reference.template.md` as the authoring base.
- [x] Included the required reference-template sections.
- [x] Included the required audit subsections under `Definitions / Facts`.
- [x] Covered instruction/settings surfaces, architecture constraints,
  feedback loops, knowledge stores, observe/plan/act/verify/learn loops,
  eval/review loops, subagent/worktree/review-loop practices, MCP/tool boundary
  implications, and automation opportunities in the implementation matrix.
- [x] Used only `Implemented`, `Partial`, `Gap`, and `Not in scope` as audit
  status values.
- [x] Cited repo-backed evidence paths for every `Implemented` and `Partial`
  matrix claim.
- [x] Kept the audit descriptive and bounded to repository evidence.
- [ ] Future work: automate audit matrix evidence, row-coverage, and
  status-vocabulary checks if recurring audit packs need stronger mechanical
  review.

### Residual Risks

- This audit is a 2026-07-02 repository snapshot. It can become stale when
  Stage 00 governance, provider adapters, templates, scripts, CI workflows,
  operations guides, MCP/tooling surfaces, or research benchmarks change.
- Static repo gates and local validation evidence do not prove live k3d,
  ArgoCD, Vault, ESO, Kubernetes, cloud, deployment, secret, paid-job, or
  external-service readiness.
- Provider runtime behavior can diverge from documented expectations if a
  provider ignores behavioral instructions or lacks a native permission gate.
- MCP/tool-boundary controls are currently general harness controls, not a
  dedicated MCP security inventory or automated poisoning/scope review.
- Audit-specific automation remains future work; current assurance combines
  manual matrix review with broad repository quality gates.

## Sources

- [Harness and Loop Engineering Research](../../research/2026-07-04-workspace-engineering-research-pack/harness-and-loop-engineering.md)
- [Workspace Harness Implementation Audit Pack Spec](../../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md)
- [Workspace Harness Implementation Audit Pack Plan](../../../04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md)
- [AGENTS.md](../../../../AGENTS.md)
- [.codex/CODEX.md](../../../../.codex/CODEX.md)
- [.codex/hooks.json](../../../../.codex/hooks.json)
- [Local Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Harness Implementation Map](../../../00.agent-governance/harness-implementation-map.md)
- [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
- [Agentic Execution Rules](../../../00.agent-governance/rules/agentic.md)
- [Approval Boundaries](../../../00.agent-governance/rules/approval-boundaries.md)
- [Memory README](../../../00.agent-governance/memory/README.md)
- [Scripts README](../../../../scripts/README.md)
- [GitHub CI Workflow](../../../../.github/workflows/ci.yml)
- [Reference Template](../../../99.templates/templates/common/reference.template.md)

## Review and Freshness

- Review cadence: on source change
- Last reviewed: 2026-07-02
- Next review trigger: harness catalog, implementation map, subagent protocol,
  agentic rules, memory routing, validation-loop, MCP/tool-boundary, audit
  benchmark, or audit-index change.
- Refresh this report when the benchmark, repo-backed evidence, status
  vocabulary, audit index, or static-vs-live evidence boundary changes.

## Related Documents

- **Audits README**: [README.md](../README.md)
- **Research benchmark**: [Harness and Loop Engineering Research](../../research/2026-07-04-workspace-engineering-research-pack/harness-and-loop-engineering.md)
- **Parent Spec**: [Workspace Harness Implementation Audit Pack Spec](../../../03.specs/010-workspace-harness-implementation-audit-pack/spec.md)
- **Parent Plan**: [Workspace Harness Implementation Audit Pack Plan](../../../04.execution/plans/2026-07-02-workspace-harness-implementation-audit-pack.md)
- **Task record**: [Workspace Harness Implementation Audit Pack Task](../../../04.execution/tasks/2026-07-02-workspace-harness-implementation-audit-pack.md)
- **Progress memory**: [Agent Progress and Memory Ledger](../../../00.agent-governance/memory/progress.md)
- **Reference maintenance runbook**: [Reference Maintenance Runbook](../../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
