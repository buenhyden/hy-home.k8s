---
title: "VAL-WER-004, VAL-WER-005, VAL-WER-007"
version: "1.0.0"
type: sdlc/task
layer: "specs"
status: done
owner: platform
updated: 2026-08-09
artifact_id: "SPEC-0053-TSK-0008"
---

# SPEC-0053-TSK-0008: VAL-WER-004, VAL-WER-005, VAL-WER-007

## Overview

Append-only Task record for legacy work item `WERPC-006` from the package's
decomposed monolithic ledger. The exact row below preserves its criterion,
dependency, owner, result, and evidence.

## Inputs

- [Package router](../README.md)
- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [Migration recovery ledger](../../../98.archive/migrations/0004-document-authority-convergence.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WERPC-006 | VAL-WER-004, VAL-WER-005, VAL-WER-007 | Research AI agents, pinned agency-agents, model routing, and memory tiers | docs-researcher | Done | Three references separate local static roster/model/memory contracts from provider/runtime evidence; the Agency Agents comparison is pinned to `ebe9c99acb5c96f9468de368d8bead775387d1a7`; `SRC-WERPC-045`–`052` and `CLM-WERPC-006-01`–`08` record limits | Focused diff/profile/strict-link/harness-semantics/model-fitness checks PASS; fresh review Approved; full-gate RED for two upstream script URLs misclassified as local paths was fixed by one pinned upstream-directory link; exact staged Reference IA, cached diff, and complete repository gate PASS; no provider execution, install, credential, remote, hosted, or live action occurred; this logical commit. |

## Approval and Safety Boundaries

The shared approval, safety, and rollback contract is preserved once in the
[owning Plan](../plan.md#legacy-task-approval-and-rollback-boundaries). This
record does not broaden that contract.

## Verification Summary

The row-specific validation/result/evidence is preserved verbatim above. The
shared verification context is in the
[owning Plan](../plan.md#legacy-task-verification-evidence).

## Traceability

- Stable Task: `SPEC-0053-TSK-0008`
- Legacy work item: `WERPC-006`
- Package inventory: [README](../README.md#task-records)
- Legacy bytes: [MIG-0004](../../../98.archive/migrations/0004-document-authority-convergence.md)
