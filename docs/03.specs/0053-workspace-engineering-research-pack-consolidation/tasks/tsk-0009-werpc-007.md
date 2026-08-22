---
title: "TSK-0053-0009: VAL-WER-008, VAL-WER-010, VAL-WER-011"
type: sdlc/task
status: done
owner: platform
updated: 2026-08-09
artifact_id: "TSK-0053-0009"
---

# TSK-0053-0009: VAL-WER-008, VAL-WER-010, VAL-WER-011

## Overview

Append-only Task record for legacy work item `WERPC-007` from the package's
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
| WERPC-007 | VAL-WER-008, VAL-WER-010, VAL-WER-011 | Migrate links, observations, indexes, machine contracts, validators, and fixtures | platform | Done | Current research navigation, RIA/agent/active-corpus contracts, validators, schemas, projections, fixtures, templates, Guide 0010, and mutable historical links are migrated; RIA-protected audit bytes remain exact and their future predecessor targets require a fail-closed sourceCommit/byte/disposition proof | Initial RIA RED: 88 tests with 10 failures/1 error; initial agent cutover RED: 37 tests with one fixture error; protected-link RED: expected no finding but got `LINK-BROKEN`; the pre-review harness attempt exposed the phase-bounded README fixture cardinality RED. Fresh review found the production disposition-header mismatch and inherited Git configuration; exact production-table and hostile-config probes failed before their fixes. The final gate then exposed closure source/current identity drift and a stale-currentness hit in the predecessor migration ledger; exact projection refresh plus a parser-gated, single-file transition exception closed them without widening to the other 24 predecessor files. GREEN: isolated staged RIA 88/88 and direct validator, agent cutover 37/37, active-corpus 19/19, registry self-test/strict, links strict/self-test, archive validation, hardened Git boundary, exact-delete-clone strict links, Python compile, cached diff, complete repository quality gate, and complete harness PASS; exact occurrence closure 732 lines/70 files and 70 reviewed rows. Three README fixture rows remain only for exact pre-deletion active54 equality and must be removed atomically in WERPC-008; Python and QA re-reviews Approved; this logical commit. |

## Approval and Safety Boundaries

The shared approval, safety, and rollback contract is preserved once in the
[owning Plan](../plan.md#legacy-task-approval-and-rollback-boundaries). This
record does not broaden that contract.

## Verification Summary

The row-specific validation/result/evidence is preserved verbatim above. The
shared verification context is in the
[owning Plan](../plan.md#legacy-task-verification-evidence).

## Traceability

- Stable Task: `TSK-0053-0009`
- Legacy work item: `WERPC-007`
- Package inventory: [README](../README.md#task-records)
- Legacy bytes: [MIG-0004](../../../98.archive/migrations/0004-document-authority-convergence.md)
