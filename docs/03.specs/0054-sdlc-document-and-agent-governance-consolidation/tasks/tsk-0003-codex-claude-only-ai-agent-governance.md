---
title: 'Task: Codex Claude-only AI agent governance'
type: sdlc/task
status: in-progress
owner: platform
updated: 2026-08-31
artifact_id: "TSK-0054-0003"
---

# Task: Codex Claude-only AI agent governance

## Overview

This is the single current Spec 0054 execution Task. The Codex/Claude registry
and projection cutover is committed and current; WP-003 remains `in-progress`
for context/memory policy activation, closure evidence, and the state-only
handoff to TSK-0054-0005. Generic cumulative lifecycle behavior is implemented
and reviewed.

## Inputs

- [Common execution contract](../README.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-003 execution boundary](../plan.md#wp-003--codexclaude-only-ai-agent-governance)
- [Proposed ADR-0031 ownership boundary](../../../02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md)
- Delegated child identifier: `SPEC-0066`; relationship authority remains in
  the parent Spec, reciprocal Spec relation, ADR-0031, and Current Spec Index.

## Task Table

**Plan label:** WP-003

**Depends on:** WP-004

**Current state:** `in-progress`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-003 | VAL-SDLC-005, VAL-SDLC-011, VAL-SDLC-012 | Close Codex/Claude-only governance and activate the context/memory policy with cumulative lifecycle proof. | platform | In Progress | The agent authority cutover and generic cumulative lifecycle behavior are committed. Policy activation, broad closure, and handoff remain. | Cumulative implementation `332f0ad10cd8e8fe3f5df2f4b42dd954d2c27396..ab524c37613423555e881a0f3195ca71a89d8304`; 14 focused PASS; 74 Archive/Migration PASS in 167.533 seconds; [remaining Plan steps](../plan.md#wp-003--codexclaude-only-ai-agent-governance) |

## Approval and Safety Boundaries

The [common execution contract](../README.md#common-execution-contract) applies
without exception. WP-003 may change only the files and logical units named in
its Plan section. Validation-registry relocation, production self-test/fixture
separation, aggregate three-gate simplification, compatibility retirement, and
current-state SHA/pin retirement belong to ADR-0031-activated Spec 0066 and are
forbidden in this Task. No provider-runtime, hosted-CI, live, credential,
sealed-Migration, push, merge, or publication mutation is authorized.

Rollback is reverse logical-unit order: state-only handoff, policy/router
activation, then cumulative-history behavior. Never reset shared history or
restore Gemini/Antigravity surfaces.

## Verification Summary

- WP-004 completed at
  `bb55a1ae93c9fc3017f64b5f2246af11442265d3` and remains the comparison base
  approved by C-SDLC-007.
- `74817983629850a6e5a22a78285083342c01e37d` began the control-plane
  consolidation. `e8bb831926b28c90639aed267d0c538857cffafc`
  committed the current registry/schema, provider-neutral role and skill
  projections, thin Codex/Claude gateways, Stage 00 owners, unsupported-provider
  deletion, MIG-0005 integration, and the reviewed historical-reference fixes.
  Later current-tree closure, including Spec 0065 memory/progress retirement,
  does not reopen those completed changes.
- A current tracked-path query returns no root `GEMINI.md`, `.gemini/**`,
  `.agents/GEMINI.md`, or Gemini provider document. On 2026-08-31 these
  repository-static commands passed on the current tree:

  ```text
  python3 scripts/validate-agent-harness-contract.py --root .
  python3 scripts/validate-agent-provider-evidence.py --root .
  python3 scripts/validate-agent-harness-semantics.py --root .
  python3 scripts/validate-agent-governance-ci.py --root .
  ```

  The results prove current registry, projection, semantic, and CI-routing
  contracts only; they do not prove provider-runtime or hosted-CI behavior.
- `docs/00.agent-governance/policies/context-and-memory.md` is still `draft`.
  Its legal activation is not implied by the earlier commits or by MIG-0009.
- Generic cumulative behavior is implemented in
  `332f0ad10cd8e8fe3f5df2f4b42dd954d2c27396` through
  `ab524c37613423555e881a0f3195ca71a89d8304`. Disposable real Git fixtures
  passed 14 focused tests for `ci` and `explicit-ref`; the final
  Archive/Migration regression run passed 74 tests in 167.533 seconds.
  Focused specification, Python, and static security reviews are clean after
  four fix rounds. These commits are execution evidence, not current-state
  pins.
- Git stores snapshots rather than rename identity. Any first-appearance commit
  with a deletion is ambiguous and receives no cumulative admission. The
  historical commit that first creates `context-and-memory.md` has that shape.
  No low-level successful real-path call, approved-base path admission, path
  exception, or SHA allowlist is claimed. `--include-path` remains additive.
- Actual context-policy activation must be proved only by staged validation
  before commit and by `ci` plus `explicit-ref` over the clean committed
  adjacent `draft → active` range. Whole approved-base comparisons remain
  unclaimed and deferred to WP-009; they are neither waived nor a PASS.
- Remaining acceptance is exactly: policy/router activation; staged and both
  adjacent-range lifecycle modes against the committed activation object;
  strict, affected, aggregate, staged, pre-commit, secret-handling and diff
  checks; independent activation/closure reviews; and the final state-only
  handoff.
- No completion is claimed. TSK-0054-0003 remains `in-progress`,
  TSK-0054-0005 remains `queued`, the Spec 0054 compatibility pointer remains
  on this Task, and Spec 0066 remains inactive.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-003](../plan.md#wp-003--codexclaude-only-ai-agent-governance) | In Progress. | Codex/Claude authority and generic cumulative lifecycle implementation are committed and reviewed. Policy activation, closure validation/review, and state-only handoff remain; no completion is claimed. |
