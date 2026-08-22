---
title: 'Audit: AI Agents, Integrated and Role-specific Agents'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: AI Agents, Integrated and Role-specific Agents

## Overview

This report audits the exact integrated and role-specific agent system at
observation commit `50628b84165479b03efc0a25be075a49c91a9aef`. The starting
implementation commit `e4ed34d56f7b90a12771232c7bfe54d5c4d6f94e` has no drift
from that observation in the reviewed harness, roster, evaluation, model,
provider-evidence, protocol, catalog, or four adapter families.

## Reference Type

Dated repository-static agent-system audit. It is not a roster admission,
evaluation result, model promotion, provider registration, dispatch record, or
proof of authenticated execution.

## Authority Boundary

The harness contract owns roles, surfaces, permissions, evidence, and current
inventory. The roster-admission, evaluation, and model-fitness contracts own
their respective states. Provider evidence and provider notes own deeper-lane
claims. This report changes none of those owners and cannot dispatch an agent,
admit a role, select a model, or infer native consumption from tracked files.

## Scope

Included: 12 current roles, four tracked adapter surfaces, 48 projections,
responsibility/input/output/prohibition/stop/handoff semantics, model mapping,
evaluation and admission state, and supervisor delegation, isolation,
checkpoint, escalation, and completion. Excluded: provider discovery,
authentication, account/model availability, effective model resolution,
delegated execution, evaluation runs/adjudication, hosted CI, remote or live
actions, secrets, and canonical remediation.

## Definitions / Facts

### AI Agents

The machine owner selects exactly 12 current roles, four current surfaces, and
48 current projections. The surface contract is syntax and semantic parity,
not provider-runtime parity.

| Surface | Exact root / schema | Count | Repository-static claim boundary |
| --- | --- | ---: | --- |
| Local | `.agents/agents`; local Markdown frontmatter | 12 | Tracked local projection; not Gemini-native runtime evidence. |
| Claude | `.claude/agents`; Claude Markdown frontmatter | 12 | Tracked Claude syntax and semantics; discovery/execution require provider observation. |
| Codex | `.codex/agents`; Codex role TOML | 12 | Tracked TOML and semantics; model fitness and execution require provider observation. |
| Gemini | `.gemini/agents`; Gemini Markdown frontmatter | 12 | Tracked native-role-shaped projection; discovery, model resolution, and execution require provider observation. |

Model mapping readiness is `PASS` for 21 of 48 tuples and `DEFER` for 27. All
48 configured tuples have `observedValue: DEFER`, and fitness, promotion,
canary, and runtime decisions remain `DEFER`. All 12 role corpora are
`repository-static-evaluation-ready`; independent-adjudication readiness is
`PASS`, while executed evaluation and final admission are `DEFER`. Adapter
`admissionState: current` means current tracked inventory, not runtime admission.

### Integrated AI Agent

The supervisor is the only orchestrator. Its contract is complete at the
repository-static layer and deliberately lacks mutation authority.

| Concern | As-is owner and behavior | Audit result |
| --- | --- | --- |
| Delegation | `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles[id=supervisor]` selects roles, assigns disjoint ownership, preserves parent authority, sequences reviews, and reconciles conflicts. | Bounded orchestration is explicit. |
| Isolation | `docs/00.agent-governance/subagent-protocol.md#tool-scoping` restricts the Claude supervisor to Read/Grep/Glob/Task and denies Bash/Edit/Write; workers retain separate permission classes and owned paths. | Supervisor orchestration does not confer worker mutation authority. |
| Checkpoint | `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#checkpointBoundary` requires repository-wins, exact identity axes, one writer, no duplicate resume, and compare-generation/digest overwrite. | Static resume and isolation semantics are closed; actual checkpoint I/O is unobserved. |
| Escalation | `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#noProgressPolicy` escalates the second identical no-progress result; missing authority, destructive risk, conflicts, and exhausted budgets stop automatic work. | Retry and escalation are deterministic repository-statically. |
| Completion | `docs/00.agent-governance/rules/quality-standards.md#canonical-completion-sequence` and `docs/00.agent-governance/rules/postflight-checklist.md#validation-and-refresh` require distinct validation lanes and complete handoff evidence before return. | Completion gates are explicit; no runtime run was performed. |

### Individual AI Agents

Each row below is derived from the current machine owner and now includes its
exact `permissionClass` and `requiredEvidence`. “Eval ready” means only a
validated static corpus. All rows remain evaluation/admission/runtime `DEFER`.
Model cells list `local; Claude; Codex; Gemini`, followed by mapping readiness.

| Role / responsibility | Inputs / outputs | Prohibited actions / stop conditions | Downstream handoff / exact adapters | Permission class / required evidence | Model rule / evaluation, admission, boundary |
| --- | --- | --- | --- | --- | --- |
| `supervisor` — route bounded work, enforce dependencies/permissions, reconcile evidence. | **In:** intent, Spec/Plan, repo state, roster, dependencies, approvals, evidence. **Out:** delegation/dependency plan, reconciled evidence, completion decision, limits, next owner. | **No:** broaden parent authority, hide conflicts, replace specialist review. **Stop:** governance conflict, unresolved ownership, repeated no-progress, missing approval, destructive risk. | code-reviewer, doc-writer, k8s-implementer, quality-engineer, security-auditor. `.agents/agents/supervisor.md`; `.claude/agents/supervisor.md`; `.codex/agents/supervisor.toml`; `.gemini/agents/supervisor.md`. | **Permission:** `orchestration`. **Required evidence:** Record selected roles, routing rationale, ownership, delegated results, conflicts, gates, and escalation decisions. | Top tier: Gemini 3.1 Pro `PASS`; opus 4.8 `PASS`; gpt-5.5/xhigh `DEFER`; native Gemini model not configurable `DEFER`. Current adapter; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `code-reviewer` — review correctness, maintainability, and policy without implementation authority. | **In:** task scope, paths, contracts, validation, risk. **Out:** prioritized path/location/severity/evidence/remediation findings. | **No:** mutate or approve without separate human-authorized task. **Stop:** security-critical defect, missing authority, unreviewable boundary. | security-auditor, supervisor. `.agents/agents/code-reviewer.md`; `.claude/agents/code-reviewer.md`; `.codex/agents/code-reviewer.toml`; `.gemini/agents/code-reviewer.md`. | **Permission:** `read-only-evidence`. **Required evidence:** Cite each finding to repository evidence and distinguish observed defects from unresolved uncertainty. | Worker: Gemini 3.5 Flash `PASS`; sonnet 4.6 `DEFER`; gpt-5.3-codex/high `DEFER`; native Gemini model not configurable `DEFER`. Current adapter; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `doc-writer` — route and author governed documents at canonical owners. | **In:** document intent, evidence, profile, lineage, paths, criteria. **Out:** governed docs with required metadata, sections, links, lifecycle evidence. | **No:** invent policy in README, memory, or provider adapter. **Stop:** type, owner, template, source, or authority ambiguity. | docs-researcher, supervisor, wiki-curator. `.agents/agents/doc-writer.md`; `.claude/agents/doc-writer.md`; `.codex/agents/doc-writer.toml`; `.gemini/agents/doc-writer.md`. | **Permission:** `scoped-authoring`. **Required evidence:** Report the canonical target, template route, upstream references, source basis, and every validation result. | Worker: Gemini 3.5 Flash `PASS`; sonnet 4.6 `DEFER`; gpt-5.3-codex/medium `DEFER`; native Gemini model not configurable `DEFER`. Current adapter; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `gitops-reviewer` — review desired-state composition, Argo CD targeting, rollout, drift, and rollback. | **In:** desired-state paths, rendered/static output, hierarchy, release constraints. **Out:** sync/composition/rollout/drift/rollback findings. | **No:** direct cluster mutation, live sync, implementation. **Stop:** missing target, unsafe rollout, sensitive boundary. | k8s-implementer, security-auditor, supervisor. `.agents/agents/gitops-reviewer.md`; `.claude/agents/gitops-reviewer.md`; `.codex/agents/gitops-reviewer.toml`; `.gemini/agents/gitops-reviewer.md`. | **Permission:** `read-only-evidence`. **Required evidence:** Identify affected sync targets, composition paths, validation results, rollout risks, and the evidence class. | Worker: Gemini 3.5 Flash `PASS`; sonnet 4.6 `PASS`; gpt-5.3-codex/high `DEFER`; native Gemini model not configurable `DEFER`. Current adapter; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `incident-responder` — reconstruct incidents from approved evidence and prepare remediation handoff. | **In:** observations, manifests, redacted log summaries, scope, safety. **Out:** timeline, impact/confidence, containment options, questions, handoff. | **No:** live remediation, sensitive output, unsupported facts. **Stop:** indicated breach, unsafe live action, insufficient evidence. | security-auditor, k8s-implementer, supervisor. `.agents/agents/incident-responder.md`; `.claude/agents/incident-responder.md`; `.codex/agents/incident-responder.toml`; `.gemini/agents/incident-responder.md`. | **Permission:** `read-only-evidence`. **Required evidence:** Preserve timestamps, source class, affected scope, confidence, contradictions, and approved references for each conclusion. | Worker: Gemini 3.5 Flash `PASS`; sonnet 4.6 `PASS`; gpt-5.3-codex/high `DEFER`; native Gemini model not configurable `DEFER`. Current adapter; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `k8s-implementer` — make bounded Kubernetes desired-state changes. | **In:** approved scope, owned manifests, architecture, policy, validation. **Out:** scoped edits, validation, rollout considerations, GitOps handoff. | **No:** plaintext sensitive data, live cluster mutation, remote controller/credential changes. **Stop:** live action, sensitive material, unclear owner, out-of-scope desired state. | gitops-reviewer, security-auditor, supervisor. `.agents/agents/k8s-implementer.md`; `.claude/agents/k8s-implementer.md`; `.codex/agents/k8s-implementer.toml`; `.gemini/agents/k8s-implementer.md`. | **Permission:** `scoped-authoring`. **Required evidence:** List changed paths, rendered or static checks, policy results, limitations, and the required reviewer handoff. | Worker: Gemini 3.5 Flash `PASS`; sonnet 4.6 `PASS`; gpt-5.3-codex/high `DEFER`; native Gemini model not configurable `DEFER`. Current adapter; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `network-reviewer` — review ingress, routing, NetworkPolicy, DNS, TLS, and service relationships. | **In:** authorized manifests, routing/policy/service/certificate evidence. **Out:** routing/isolation/DNS/TLS findings, limits, escalation. | **No:** live probing or mutation, sensitive access, unauthorized security judgment. **Stop:** live/sensitive need or scope beyond static authority. | security-auditor, gitops-reviewer, supervisor. `.agents/agents/network-reviewer.md`; `.claude/agents/network-reviewer.md`; `.codex/agents/network-reviewer.toml`; `.gemini/agents/network-reviewer.md`. | **Permission:** `read-only-evidence`. **Required evidence:** Cite routing, policy, DNS, or TLS paths and the static relationship or command supporting each finding. | Worker: Gemini 3.5 Flash `PASS`; sonnet 4.6 `PASS`; gpt-5.3-codex/high `DEFER`; native Gemini model not configurable `DEFER`. Current adapter; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `observability-reviewer` — review telemetry, alerting, and SLO wiring. | **In:** manifests, dashboards, SLOs, alerts, static evidence. **Out:** telemetry/SLO/ownership findings and static/runtime gaps. | **No:** live query, scrape, or dashboard mutation. **Stop:** live/sensitive requirement or security-isolation judgment. | gitops-reviewer, security-auditor, supervisor. `.agents/agents/observability-reviewer.md`; `.claude/agents/observability-reviewer.md`; `.codex/agents/observability-reviewer.toml`; `.gemini/agents/observability-reviewer.md`. | **Permission:** `read-only-evidence`. **Required evidence:** Cite scrape, alert, dashboard, telemetry, or SLO paths and identify the evidence class for each conclusion. | Worker: Gemini 3.5 Flash `PASS`; sonnet 4.6 `PASS`; gpt-5.3-codex/high `DEFER`; native Gemini model not configurable `DEFER`. Current adapter; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `security-auditor` — audit RBAC, isolation, sensitive-data, and supply-chain controls. | **In:** paths, policies, RBAC/network data, supply metadata, validation. **Out:** severity, evidence, control/remediation, residual risk. | **No:** weaken least privilege, expose secrets, approve exceptions, remediate. **Stop:** plaintext sensitive exposure or unauthorized access need. | k8s-implementer, supervisor. `.agents/agents/security-auditor.md`; `.claude/agents/security-auditor.md`; `.codex/agents/security-auditor.toml`; `.gemini/agents/security-auditor.md`. | **Permission:** `read-only-evidence`. **Required evidence:** Cite each finding to a path or approved observation, severity, affected control, evidence class, and remediation basis. | Worker: Gemini 3.5 Flash `PASS`; sonnet 4.6 `PASS`; gpt-5.3-codex/high `DEFER`; native Gemini model not configurable `DEFER`. Current adapter; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `wiki-curator` — maintain discovery maps without duplicating canonical authority. | **In:** owner paths, taxonomy, generator contract, stale-link evidence, scope. **Out:** discovery/index updates, links, freshness, no duplicate authority. | **No:** new retrieval runtime, duplicate policy, generated output as source. **Stop:** ambiguous ownership, duplicate contract, unapproved runtime. | doc-writer, supervisor. `.agents/agents/wiki-curator.md`; `.claude/agents/wiki-curator.md`; `.codex/agents/wiki-curator.toml`; `.gemini/agents/wiki-curator.md`. | **Permission:** `scoped-authoring`. **Required evidence:** Identify each changed entrypoint, canonical owner target, generation source, stale-link result, and freshness check. | Worker: Gemini 3.5 Flash `PASS`; sonnet 4.6 `DEFER`; gpt-5.3-codex/medium `DEFER`; native Gemini model not configurable `DEFER`. Current adapter; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `docs-researcher` — verify current primary sources and cutoff evidence. | **In:** research question, source constraints, cutoff, consumer, risk. **Out:** source ledger, synthesis, citations, limits, freshness. | **No:** turn external prose into authority or claim recency beyond evidence. **Stop:** unavailable primary source, material date conflict, unauthorized external action. | doc-writer, supervisor. `.agents/agents/docs-researcher.md`; `.claude/agents/docs-researcher.md`; `.codex/agents/docs-researcher.toml`; `.gemini/agents/docs-researcher.md`. | **Permission:** `read-only-evidence`. **Required evidence:** Record source identity, direct link, observation date, supported claim, conflicting evidence, and inference labels. | Worker: Gemini 3.1 Pro `PASS`; Sonnet 5 `PASS`; gpt-5.6-terra/high `DEFER`; native Gemini model not configurable `DEFER`. Current adapter and roster candidate projected; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |
| `quality-engineer` — design deterministic fixtures, validation lanes, and result classification. | **In:** acceptance criteria, contracts, paths, failure rules, environment. **Out:** fixture plan, negative sensitivity, results, limits, admission/rollback recommendation. | **No:** formatter-as-proof, skip-as-pass, cross-class inference, self-adjudication. **Stop:** untestable criteria, unavailable lane, inconsistent evidence. | code-reviewer, security-auditor, supervisor. `.agents/agents/quality-engineer.md`; `.claude/agents/quality-engineer.md`; `.codex/agents/quality-engineer.toml`; `.gemini/agents/quality-engineer.md`. | **Permission:** `scoped-authoring`. **Required evidence:** Record fixture identity, command, environment boundary, expected and actual rule, result class, and repeatability. | Worker: Gemini 3.5 Flash `PASS`; Sonnet 5 `PASS`; gpt-5.6-terra/high `DEFER`; native Gemini model not configurable `DEFER`. Current adapter and roster candidate projected; eval ready/readiness `PASS`; evaluation/admission/runtime `DEFER`; repo-static only. |

`docs-researcher` and `quality-engineer` retain historical candidate records in
the admission contract while their four projections are current. That is not a
contradiction: the records preserve admission rationale and rollback, while
the final decision explicitly keeps evaluation and runtime admission `DEFER`.

### Blockers

| ID | Cause | Impact | Affected request IDs | Release condition | Owner | Evidence depth | Classification |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BLK-WGA-AGT-001 | Provider discovery, authentication, runtime, effective model resolution, evaluation execution/adjudication, hosted CI, remote action, and live action were outside the authorized repository-static audit. | Static parity/readiness cannot become native consumption, fitness, admission, or execution evidence. | `REQ-WGA-028`, `REQ-WGA-029`, `REQ-WGA-030` | Authorized redacted provider-runtime and evaluation evidence passes the existing model/evaluation/admission gates without cross-class inference. | Provider-runtime operator and current model/evaluation/admission owners. | `provider-runtime` | `DEFER` evidence limitation, not a blocker to WGIA-007 static completion. |

### Finding Convention

Every material finding uses the closed pack fields. Evidence depth is one of
`repository-static`, `provider-runtime`, `hosted`, or `live`; unavailable
deeper evidence remains `DEFER`. A blocker is either a complete object above or
the explicit value `none`.

#### WGA-AGT-001 — Exact role and adapter inventory aligns

- **Request IDs**: `REQ-WGA-028`, `REQ-WGA-030`.
- **Scope**: 12 canonical roles, four surfaces, 48 current projections, per-role semantics, and adapter parity.
- **Expected state**: one machine owner selects a closed current inventory and every role has responsibility, inputs, outputs, prohibitions, stops, handoffs, permissions, evidence, adapters, and evaluation binding.
- **Observed state**: the harness selects exactly 12/4/48; the role matrix above closes every required field; focused contract, semantics, and currentness checks pass; no relevant observation-to-current drift exists.
- **Evidence**: `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles`; `docs/00.agent-governance/contracts/harness-contract.json#surfaces`; `docs/00.agent-governance/contracts/harness-contract.json#currentInventory`; `docs/00.agent-governance/subagent-protocol.md#agent-file-requirement`; `scripts/validate-agent-harness-contract.py#main`; `scripts/validate-agent-harness-semantics.py#main`; `scripts/validate-agent-roster-currentness.py#main`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: role ownership, least privilege, handoff, and four-surface static parity are reviewable and deterministic.
- **Disposition**: `Keep`.
- **Canonical owner**: `docs/00.agent-governance/contracts/harness-contract.json`.
- **Verification**: harness contract/semantics and roster-currentness self-tests, production checks, and focused unit tests.
- **Uncertainty**: native discovery and execution remain unobserved.
- **Blocker**: none for repository-static inventory.

#### WGA-AGT-002 — Integrated supervisor orchestration aligns repository-statically

- **Request IDs**: `REQ-WGA-029`.
- **Scope**: supervisor delegation, isolation, checkpoint, escalation, and completion gates.
- **Expected state**: the sole supervisor preserves parent authority and disjoint ownership, cannot absorb worker permissions, escalates deterministic stop conditions, and returns only after evidence gates.
- **Observed state**: the harness, protocol, loop/checkpoint, quality, postflight, and four supervisor adapters express those boundaries consistently; focused checks pass.
- **Evidence**: `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles[id=supervisor]`; `docs/00.agent-governance/subagent-protocol.md#tool-scoping`; `docs/00.agent-governance/subagent-protocol.md#delegated-handoff-evidence`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#noProgressPolicy`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#checkpointBoundary`; `.claude/agents/supervisor.md#guardrails`; `.codex/agents/supervisor.toml#developer_instructions`; `docs/00.agent-governance/rules/quality-standards.md#canonical-completion-sequence`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Aligned`.
- **Impact**: static integrated-agent coordination has explicit authority, isolation, recovery, escalation, and completion semantics.
- **Disposition**: `Keep`.
- **Canonical owner**: harness contract, subagent protocol, loop lifecycle, and quality/postflight rules within their declared concerns.
- **Verification**: harness contract/semantics, loop/checkpoint, and adapter currentness checks.
- **Uncertainty**: actual delegation, concurrency isolation, checkpoint I/O, and event delivery are unobserved.
- **Blocker**: none for static orchestration; `BLK-WGA-AGT-001` limits runtime promotion.

#### WGA-AGT-003 — Model, evaluation, and admission states are conservative but incomplete

- **Request IDs**: `REQ-WGA-028`, `REQ-WGA-030`.
- **Scope**: 48 provider tuples, 12 evaluation suites, independent adjudication readiness, roster state, promotion, and rollback.
- **Expected state**: configured labels and static readiness remain separate from observed model value, fitness, evaluation, promotion, and admission.
- **Observed state**: mapping readiness is 21 `PASS`/27 `DEFER`; all 48 observed values and fitness/promotion/canary/runtime decisions are `DEFER`; all 12 static corpora and adjudicator records are ready/PASS, but executed evaluation and final admission are `DEFER`.
- **Evidence**: `docs/00.agent-governance/contracts/agent-model-fitness.json#roleProfiles`; `docs/00.agent-governance/contracts/agent-model-fitness.json#evaluationBindings`; `docs/00.agent-governance/contracts/agent-evaluations.json#roleSuites`; `docs/00.agent-governance/contracts/agent-evaluations.json#adjudicationReadiness`; `docs/00.agent-governance/contracts/agent-evaluations.json#finalAdmissionDecision`; `docs/00.agent-governance/contracts/agent-roster-admission.json#currentInventory`; `docs/00.agent-governance/contracts/agent-roster-admission.json#candidates`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: static mapping and corpus readiness are usable without falsely claiming effective model fitness or runtime admission.
- **Disposition**: `Keep`.
- **Canonical owner**: model-fitness, evaluations, and roster-admission machine contracts.
- **Verification**: model-fitness, evaluation, roster-admission, provider-config/evidence/canary checks and same-corpus execution if later authorized.
- **Uncertainty**: provider availability, effective resolution, metrics, adjudicated evaluation, cost/latency, promotion, and rollback execution.
- **Blocker**: `BLK-WGA-AGT-001` blocks deeper evidence only.

#### WGA-AGT-004 — Native discovery and effective execution remain deferred

- **Request IDs**: `REQ-WGA-028`, `REQ-WGA-029`, `REQ-WGA-030`.
- **Scope**: provider discovery, authentication, effective tools/models, delegation, checkpoints, evaluation runs, hosted, remote, and live behavior.
- **Expected state**: no static adapter or validator result is promoted across evidence classes without an authorized runtime record.
- **Observed state**: tracked adapters and static provider records preserve the boundary; no provider/runtime/authenticated/hosted/remote/live action was performed, so all effective behavior remains unobserved.
- **Evidence**: `docs/00.agent-governance/contracts/harness-contract.json#surfaces`; `docs/00.agent-governance/contracts/harness-contract.json#routingContract`; `docs/00.agent-governance/contracts/agent-model-fitness.json#runtimeBoundaries`; `docs/00.agent-governance/contracts/agent-evaluations.json#finalAdmissionDecision`; `docs/00.agent-governance/contracts/provider-runtime-evidence.json#providers`; `docs/00.agent-governance/subagent-protocol.md#dispatch-rules`; `scripts/validate-agent-provider-evidence.py#run`; `scripts/validate-agent-provider-canaries.py#main`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `DEFER`.
- **Impact**: repository-static confidence remains bounded and does not imply effective provider capability or authority.
- **Disposition**: `Keep`.
- **Canonical owner**: provider-runtime evidence record and current provider/model/evaluation owners.
- **Verification**: separately authorized, redacted provider-runtime discovery/auth/model/delegation/evaluation evidence.
- **Uncertainty**: every effective provider, model, tool, execution, checkpoint, hosted, remote, and live fact.
- **Blocker**: `BLK-WGA-AGT-001`.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-AGT-001 | machine owner | `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles`; `docs/00.agent-governance/contracts/harness-contract.json#currentInventory`; `docs/00.agent-governance/contracts/agent-roster-admission.json#currentInventory`; `docs/00.agent-governance/contracts/agent-evaluations.json#finalAdmissionDecision`; `docs/00.agent-governance/contracts/agent-model-fitness.json#roleProfiles` | Exact role, adapter, model, evaluation, and admission states. |
| SRC-WGA-AGT-002 | policy owner | `docs/00.agent-governance/subagent-protocol.md#tool-scoping`; `docs/00.agent-governance/subagent-protocol.md#dispatch-rules`; `docs/00.agent-governance/subagent-protocol.md#delegated-handoff-evidence`; `docs/00.agent-governance/rules/quality-standards.md#canonical-completion-sequence`; `docs/00.agent-governance/model-policy.md#model-tiers-july-2026-local-baseline` | Delegation, isolation, handoff, completion, and model boundaries. |
| SRC-WGA-AGT-003 | human index | `docs/00.agent-governance/harness-catalog.md#agents`; `docs/00.agent-governance/harness-catalog.md#native-and-local-role-adapters` | Human routing view; machine owners win. |
| SRC-WGA-AGT-004 | evidence producer | `scripts/validate-agent-harness-contract.py#main`; `scripts/validate-agent-harness-semantics.py#main`; `scripts/validate-agent-roster-currentness.py#main`; `scripts/validate-agent-roster-admission.py#main`; `scripts/validate-agent-evaluations.py#main`; `scripts/validate-agent-model-fitness.py#main`; `scripts/validate-agent-provider-config.py#main`; `scripts/validate-agent-provider-evidence.py#run`; `scripts/validate-agent-provider-canaries.py#main` | Deterministic repository-static validation only. |
| SRC-WGA-AGT-005 | machine owner | `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#stateMachine`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#noProgressPolicy`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#checkpointBoundary` | Supervisor recovery, checkpoint, escalation, and handoff interfaces. |

## Review and Freshness

- Review status: `Approved`; specification/content and fix-round quality
  reviews found no remaining Critical or Important issue after the exact
  permission/required-evidence matrix fix.
- Review disposition: `Approved` as a bounded repository-static audit; no
  roster, model, evaluation, admission, provider-runtime, roadmap, or
  disposition change is approved by this report.
- Evidence observed: 2026-08-09 at exact observation commit `50628b84165479b03efc0a25be075a49c91a9aef`, compared with starting commit `e4ed34d56f7b90a12771232c7bfe54d5c4d6f94e`.
- Current-truth owners: Stage 00 harness/protocol/catalog, roster/evaluation/model/provider machine contracts, provider notes, and tracked adapters.
- Refresh triggers: role, surface, projection, responsibility, permission, handoff, supervisor, checkpoint, evaluation, adjudication, admission, model mapping, provider evidence, observation commit, or verdict change.
- Provider-runtime, authenticated, hosted, remote, credential-bearing, secret, evaluation-execution, and live evidence remains `DEFER`.
- No provisional roadmap or disposition-ledger row is warranted: the static owners accurately represent the reviewed state and no Legacy, Deprecated, one-shot, deletion, duplication, or repair candidate was proven.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/0055-workspace-governance-audit-and-remediation/spec.md)
- [Implementation Plan](../../../03.specs/0055-workspace-governance-audit-and-remediation/plan.md)
- [Implementation Task](../../../03.specs/0055-workspace-governance-audit-and-remediation/README.md)
- [Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
