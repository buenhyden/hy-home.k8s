---
title: 'Audit: AI Agents, Integrated and Role-specific Agents'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: AI Agents, Integrated and Role-specific Agents

## Overview

This report owns the audit of the AI-agent system, integrated supervisor and
orchestration behavior, every current role, adapter coverage, model routing,
handoff, admission, evaluation, runtime limits, and stop conditions. WGIA-001
records the pinned inventory; WGIA-007 owns the complete role matrix and review.

## Reference Type

Dated repository-static agent-system audit. It is not an agent roster, adapter,
model policy, admission decision, runtime registration, or provider execution
record.

## Authority Boundary

The harness contract owns exact machine inventory; the harness catalog and
Stage 00 rules own current human routing and semantics; model-fitness and
admission contracts own their exact values; provider-native/local files remain
tracked adapters. This report cannot admit a role, select a model, dispatch an
agent, or infer provider consumption from adapter presence.

## Scope

Included: shared agent system, supervisor/integrated orchestration, current role
responsibilities, inputs, outputs, prohibited actions, stop/handoff, adapters,
models, evaluation, admission, promotion, and rollback. Excluded: provider
authentication, runtime discovery, actual delegated execution, account/model
availability, roster changes, and conclusions before WGIA-007 review.

## Definitions / Facts

### AI Agents

`docs/00.agent-governance/contracts/harness-contract.json` is the exact machine
owner. `docs/00.agent-governance/harness-catalog.md`, subagent protocol, model
policy, fitness/admission contracts, adapter roots, validators, and fixtures
are supporting tracked surfaces.

### Integrated AI Agent

Supervisor/orchestrator behavior is routed through the current subagent
protocol and supervisor adapter family. Tracked orchestration definitions do
not prove that a provider discovered, authorized, or executed them.

### Individual AI Agents

The observation tree contains 12 adapter files in each of `.agents/agents/`,
`.claude/agents/`, `.codex/agents/`, and `.gemini/agents/`. This is a
repository-static 12-role/four-surface inventory; WGIA-007 must derive the
exact role matrix from the machine owner and review each responsibility and
handoff rather than infer parity from file count.

### Canonical-owner Inventory

| Role | Current evidence surface | Foundation use |
| --- | --- | --- |
| Machine roster owner | `docs/00.agent-governance/contracts/harness-contract.json` | Exact role/surface adapter inventory. |
| Human catalog | `docs/00.agent-governance/harness-catalog.md` | Role and routing explanation. |
| Orchestration policy | `docs/00.agent-governance/subagent-protocol.md` | Dispatch, review, and handoff boundary. |
| Model/admission machine owners | agent model-fitness and roster-admission contracts | Configured/observed decision evidence. |
| Provider/local adapters | four tracked adapter roots | Repository-static declarations only. |
| Evidence producers | harness, semantics, fitness, admission, and currentness validators | Synthetic deterministic checks. |

### Finding Convention

Every material finding uses the complete pack field set and closed audit
verdict/evidence-depth vocabularies. Role inventory, adapter parity, model
configuration, evaluation result, admission, and provider-runtime evidence are
separate facts and cannot promote one another.

#### WGA-AGT-001 — Agent-system source inventory established

- **Request IDs**: AI Agents, Integrated AI Agent, and Individual AI Agents coverage rows in the pack index.
- **Scope**: pinned machine roster, catalog, orchestration, adapter, model, admission, validator, and fixture inventory.
- **Expected state**: WGIA-007 can produce one reviewed matrix for the integrated system and every machine-owned role without static-to-runtime inference.
- **Observed state**: the 12-role/four-surface tracked adapter inventory and current owner families are identified; role semantics and runtime evidence remain pending.
- **Evidence**: `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles`; `docs/00.agent-governance/contracts/harness-contract.json#surfaces`; `docs/00.agent-governance/contracts/harness-contract.json#currentInventory`; `docs/00.agent-governance/harness-catalog.md#agents`; `docs/00.agent-governance/subagent-protocol.md#dispatch-rules`; `docs/00.agent-governance/contracts/agent-model-fitness.json#roleProfiles`; `docs/00.agent-governance/contracts/agent-roster-admission.json#currentInventory`; `.agents/agents/supervisor.md#name=supervisor`; `.claude/agents/supervisor.md#name=supervisor`; `.codex/agents/supervisor.toml#description`; `.gemini/agents/supervisor.md#name=supervisor`; `scripts/validate-agent-harness-semantics.py#main`; `scripts/validate-agent-roster-currentness.py#main`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: exact later review can be routed, but responsibility, handoff, model fitness, admission, and runtime completeness are not yet established.
- **Disposition**: `Keep`.
- **Canonical owner**: current Stage 00 harness, role, model, admission, and provider-adapter owners.
- **Verification**: harness semantics, model-fitness, roster-admission/currentness checks and WGIA-007 role-by-role review.
- **Uncertainty**: semantic parity, evaluation outcomes, provider discovery, model resolution, permissions, and delegated execution are unobserved.
- **Blocker**: none; unavailable provider/runtime evidence remains `DEFER`.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-AGT-001 | machine owner | `docs/00.agent-governance/contracts/harness-contract.json#canonicalRoles`; `docs/00.agent-governance/contracts/harness-contract.json#surfaces`; `docs/00.agent-governance/contracts/agent-model-fitness.json#roleProfiles`; `docs/00.agent-governance/contracts/agent-roster-admission.json#currentInventory` | Exact tracked roster/model/admission evidence. |
| SRC-WGA-AGT-002 | policy owner | `docs/00.agent-governance/subagent-protocol.md#dispatch-rules`; `docs/00.agent-governance/subagent-protocol.md#delegated-handoff-evidence`; `docs/00.agent-governance/model-policy.md#model-tiers-july-2026-local-baseline`; `docs/00.agent-governance/providers/codex.md#permission--hook-boundary`; `docs/00.agent-governance/rules/agentic.md#execution-contract` | Current behavior and boundary routing. |
| SRC-WGA-AGT-003 | human index | `docs/00.agent-governance/harness-catalog.md#agents`; `docs/00.agent-governance/harness-catalog.md#native-and-local-role-adapters` | Current role catalog. |
| SRC-WGA-AGT-004 | evidence producer | `scripts/validate-agent-harness-contract.py#main`; `scripts/validate-agent-harness-semantics.py#main`; `scripts/validate-agent-model-fitness.py#main`; `scripts/validate-agent-roster-admission.py#main`; `scripts/validate-agent-roster-currentness.py#main`; `tests/fixtures/agent-harness-semantics.json#mutations`; `tests/fixtures/agent-model-fitness.json#mutations`; `tests/fixtures/agent-roster-admission.json#mutations` | Synthetic repository-static results. |

## Review and Freshness

- Review status: `Pending` for WGIA-007 independent topic review.
- Review disposition: `DEFER`; no role or orchestration conclusion is approved.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: Stage 00 harness/catalog/protocol/model/admission
  contracts and tracked provider/local adapters.
- Refresh triggers: roster, responsibility, input, output, prohibited action,
  stop, handoff, adapter, model, evaluation, admission, provider, source,
  observation commit, or verdict change.
- Provider-runtime, hosted, remote, authenticated, credential-bearing, and live
  evidence remains `DEFER`.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Subagent Protocol](../../../00.agent-governance/subagent-protocol.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
