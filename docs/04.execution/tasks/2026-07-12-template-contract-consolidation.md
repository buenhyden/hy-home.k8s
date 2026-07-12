---
title: 'Task: Template Contract Consolidation'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-12
---

# Task: Template Contract Consolidation

## Overview

This document tracks the six implementation and verification units that align
Stage 99 support and non-README forms with the document profile registry. It
preserves reciprocal Spec, Plan, Task, and index lineage throughout the Spec
027 compatibility window.

## Inputs

- **Parent Spec**:
  [../../03.specs/027-template-contract-consolidation/spec.md](../../03.specs/027-template-contract-consolidation/spec.md)
- **Parent Plan**:
  [../plans/2026-07-12-template-contract-consolidation.md](../plans/2026-07-12-template-contract-consolidation.md)
- **Completed Registry Task**:
  [./2026-07-12-document-contract-registry.md](./2026-07-12-document-contract-registry.md)

## Working Rules

- Record failing assertions before each deterministic contract change.
- Publish the type-to-source evidence row before changing a template family.
- Link exact machine facts to the registry instead of copying complete tables
  into support prose.
- Keep all currently required Task headings until TCC-005 establishes the
  explicit compatibility contract.
- Restrict Stage 99 README changes to inventory and target-link rows; Spec 028
  owns README body design.
- Treat repository-static evidence as bounded evidence, not live runtime
  readiness.

## Task Table

| Task ID | Description | Type | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| TCC-001 | Start reciprocal execution lineage | doc | Six links and index rows | platform | Done |
| TCC-002 | Publish type-to-source decision ledger | research | Ten family rows with required evidence | platform | Queued |
| TCC-003 | Consolidate support ownership | governance | No copied complete registry tables | platform | Queued |
| TCC-004 | Normalize canonical non-README forms | template | Heading matrix and native-format checks | platform | Queued |
| TCC-005 | Delete legacy Task form and establish compatibility | migration | Zero active legacy refs; old/new gates green | platform | Queued |
| TCC-006 | Close evidence and hand off README body ownership | validation | Full QA and explicit Spec 028 handoff | platform | Queued |

## Suggested Types

- `doc`: reciprocal Spec, Plan, Task, and index lineage work.
- `research`: type-to-source evidence ledger work.
- `governance`: support ownership consolidation work.
- `template`: canonical non-README form normalization work.
- `migration`: legacy form removal and compatibility work.
- `validation`: closure QA and explicit Spec 028 handoff work.

## Agent-specific Types (If Applicable)

- No agent-specific task types apply to TCC-001 through TCC-006; the tranche
  uses the topic-specific types above.

## Phase View (Optional)

### Phase 1: Execution Lineage

- [x] TCC-001 Start reciprocal execution lineage.

### Phase 2: Contract Consolidation

- [ ] TCC-002 Publish type-to-source decision ledger.
- [ ] TCC-003 Consolidate support ownership.
- [ ] TCC-004 Normalize canonical non-README forms.
- [ ] TCC-005 Delete legacy Task form and establish compatibility.

### Phase 3: Closure

- [ ] TCC-006 Close evidence and hand off README body ownership.

## Verification Summary

- **Test Commands**: The six-link reciprocal lineage assertion in Plan Task 1.
- **Eval Commands**: Focused changed-file pre-commit validation and the
  repository quality gate.
- **Logs / Evidence Location**: This Task table and the logical task commits.
- **Safety Boundary**: No live Kubernetes, Argo CD, Vault, ESO,
  provider-runtime, credential, secret-value, remote, publish, push, merge, or
  third-party mutation is authorized by this Task.

## Related Documents

- **Spec**:
  [../../03.specs/027-template-contract-consolidation/spec.md](../../03.specs/027-template-contract-consolidation/spec.md)
- **Plan**:
  [../plans/2026-07-12-template-contract-consolidation.md](../plans/2026-07-12-template-contract-consolidation.md)
- **Previous Tranche**:
  [./2026-07-12-document-contract-registry.md](./2026-07-12-document-contract-registry.md)
