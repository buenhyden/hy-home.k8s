---
title: 'Audit: Harness, Loop, Fixtures, Scripts, and Blockers'
type: content/reference
status: draft
owner: platform
updated: 2026-08-09
---

# Audit: Harness, Loop, Fixtures, Scripts, and Blockers

## Overview

This report owns the audit of harness and loop state machines, fixtures,
operating scripts, retry/recovery/stop behavior, checkpoints, handoffs,
blockers, and script-to-validator ownership. WGIA-001 records the pinned
inventory; WGIA-005 owns full analysis and independent review.

## Reference Type

Dated repository-static harness and loop audit. It does not own execution
policy, provider behavior, machine schemas, or actual runtime state.

## Authority Boundary

Stage 00 machine contracts, schemas, rules, scripts, tests, fixtures, and
provider adapters retain their current roles. Synthetic validator PASS proves
only repository-static contract behavior; it cannot establish actual provider
discovery, checkpoint execution, event delivery, authentication, or live work.

## Scope

Included: harness inventory, lifecycle state machine, retries, stop and
recovery, checkpoints, handoff, fixtures, scripts, blockers, and validator
ownership. Excluded: running provider agents, reading ignored checkpoints,
inspecting private runtime state, changing current contracts, and conclusions
before WGIA-005 review.

## Definitions / Facts

### Harness Engineering

`docs/00.agent-governance/contracts/harness-contract.json` and schema are the
machine inventory owners. `docs/00.agent-governance/harness-catalog.md`,
provider adapters, harness validators, and fixtures are current supporting
surfaces at the observation commit.

### Loop Engineering

`docs/00.agent-governance/contracts/agent-loop-lifecycle.json` and schema own
the repository-static lifecycle representation. Loop and checkpoint validators
test synthetic state; actual provider loop execution remains unobserved.

### Fixtures

`tests/fixtures/` contains contract fixtures for harness, loop, checkpoint,
model, roster, legacy, governance closure, and validation surfaces. Fixture
presence does not prove production parity until WGIA-005 traces each consumer
and negative path.

### Blockers

A material blocker must name cause, impact, release condition, owner, affected
request scope, and evidence depth. Pending planned work is not automatically a
blocker; unavailable authority or evidence is recorded as `DEFER`.

### Scripts

The observation tree contains 48 tracked files under `scripts/`.
`scripts/README.md` is the human inventory; exact invocation, owner, caller,
fallback, failure, and retirement analysis remains pending. Script count alone
does not prove active consumption.

### Canonical-owner Inventory

| Role | Current evidence surface | Foundation use |
| --- | --- | --- |
| Machine owner | harness, loop, checkpoint, roster, model, and closure contracts | Exact repository-static shapes. |
| Policy owner | Stage 00 agentic, quality, approval, memory, and provider rules | Execution semantics and boundaries. |
| Evidence producer | harness/loop/checkpoint validators and tests | Synthetic deterministic results. |
| Human index | `docs/00.agent-governance/harness-catalog.md`; `scripts/README.md`; `tests/README.md` | Reader routing and inventory. |
| Provider adapter | four tracked provider/local adapter roots | Declared configuration only. |

### Finding Convention

Every material finding requires the complete pack field set. Verdicts and
evidence depths are closed; blocker objects require cause, release condition,
and owner, while a non-blocker uses the explicit value `none`.

#### WGA-HAR-001 — Harness and loop source inventory established

- **Request IDs**: harness engineering, loop engineering, fixtures, blockers, and scripts coverage rows in the pack index.
- **Scope**: pinned machine-contract, policy, adapter, fixture, test, and script inventory.
- **Expected state**: WGIA-005 can map state, ownership, transitions, recovery, stop, handoff, fixture, and script consumers without runtime inference.
- **Observed state**: current source families and 48 tracked script files are identified; exact consumer and behavior analysis is pending.
- **Evidence**: `docs/00.agent-governance/contracts/harness-contract.json#currentInventory`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#stateMachine`; `docs/00.agent-governance/contracts/agent-checkpoint.schema.json#properties`; `docs/00.agent-governance/harness-catalog.md#machine-contract-and-inventory-boundary`; `scripts/README.md#script-inventory`; `tests/fixtures/agent-harness-contract.json#mutations`; `tests/fixtures/agent-loop-lifecycle.json#mutations`; `scripts/validate-agent-harness-contract.py#main`; `scripts/validate-agent-loop-lifecycle.py#main`; `scripts/validate-agent-checkpoint.py#main`.
- **Evidence depth**: `repository-static`.
- **Verdict**: `Partial`.
- **Impact**: later analysis is bounded, but harness/loop completeness and script activity are not yet established.
- **Disposition**: `Keep`.
- **Canonical owner**: current Stage 00 contracts, rules, scripts, tests, and adapters.
- **Verification**: focused harness/loop/checkpoint/script inventory checks plus WGIA-005 review.
- **Uncertainty**: consumer reachability, recovery semantics, negative paths, ignored checkpoint behavior, and provider execution remain unreviewed.
- **Blocker**: none; deeper lanes remain explicit `DEFER`.

## Sources

Source roles are closed to `policy owner`, `machine owner`, `human index`,
`evidence producer`, and `historical snapshot`.

| Source ID | Source role | Evidence at the observation commit | Use |
| --- | --- | --- | --- |
| SRC-WGA-HAR-001 | machine owner | `docs/00.agent-governance/contracts/harness-contract.json#currentInventory`; `docs/00.agent-governance/contracts/agent-loop-lifecycle.json#stateMachine`; `docs/00.agent-governance/contracts/agent-checkpoint.schema.json#properties` | Exact tracked shapes. |
| SRC-WGA-HAR-002 | policy owner | `docs/00.agent-governance/rules/agentic.md#execution-contract`; `docs/00.agent-governance/rules/quality-standards.md#canonical-completion-sequence`; `docs/00.agent-governance/rules/approval-boundaries.md#approval-matrix`; `docs/00.agent-governance/memory/README.md#four-memory-classes`; `docs/00.agent-governance/providers/codex.md#permission--hook-boundary` | Execution expectations and limits. |
| SRC-WGA-HAR-003 | evidence producer | `scripts/validate-agent-harness-contract.py#main`; `scripts/validate-agent-loop-lifecycle.py#main`; `scripts/validate-agent-checkpoint.py#main`; `tests/fixtures/agent-harness-contract.json#mutations`; `tests/fixtures/agent-loop-lifecycle.json#mutations`; `tests/fixtures/agent-checkpoint.json#negativeMutations` | Deterministic synthetic evidence. |
| SRC-WGA-HAR-004 | human index | `docs/00.agent-governance/harness-catalog.md#harness-engineering-matrix`; `scripts/README.md#script-inventory`; `tests/README.md#validation-model` | Current inventory routing. |

## Review and Freshness

- Review status: `Pending` for WGIA-005 independent topic review.
- Review disposition: `DEFER`; source inventory is not a complete harness audit.
- Evidence observed: 2026-08-09 at the exact observation commit.
- Current-truth owners: Stage 00 machine contracts, policies, scripts, tests,
  fixtures, and tracked adapters.
- Refresh triggers: state, transition, retry, stop, recovery, checkpoint,
  handoff, blocker, fixture, script, adapter, source, or observation change.
- Provider-runtime, hosted, remote, credential-bearing, and live evidence
  remains `DEFER`; no ignored checkpoint was read or written.

## Related Documents

- [Pack Index](README.md)
- [Spec 054](../../../03.specs/054-workspace-governance-audit-and-remediation/spec.md)
- [Harness Catalog](../../../00.agent-governance/harness-catalog.md)
- [Memory Contract](../../../00.agent-governance/memory/README.md)
- [Implementation Task](../../../04.execution/tasks/2026-08-09-workspace-governance-audit-and-remediation.md)
