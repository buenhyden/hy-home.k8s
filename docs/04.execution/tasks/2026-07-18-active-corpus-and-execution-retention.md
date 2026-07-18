---
title: 'Task: Active Corpus and Execution Retention'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-18
---

# Task: Active Corpus and Execution Retention

## Overview

This Task is the execution, verification, review, and rollback ledger for
ACER-001 through ACER-006. It activates the reciprocal Spec 037 execution pair
from repository baseline `a12aedfb71ccabd329dabc83bd2863474d1126b0` and keeps
every implementation package Queued until its own RED/GREEN evidence,
independent reviews, and logical commit exist.

The parent `a12aedf` activation input records 54 authored Plans plus 56 authored
Tasks, for 110 candidates. This staged reciprocal pair raises the proposed
corpus to 55 Plans and 57 Tasks (112 records) and remains a separately retained
active control. ACER-001 must reconcile the frozen 104-record baseline with the
six later records created for Specs 034 through 036. No candidate is eligible
merely because it is terminal, old, or counted. The prior Stage 05 input is 24
authored records (eight Guides, seven Policies, and nine Runbooks), with zero
real authored Incident and Postmortem records. The earlier helper Tests
inventory is an input to recompute rather than activation PASS evidence.

## Inputs

- [Active Corpus and Execution Retention Implementation Plan](../plans/2026-07-18-active-corpus-and-execution-retention.md)
- [Spec 037](../../03.specs/037-active-corpus-and-execution-retention/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Archive index](../../98.archive/README.md)
- [Migration evidence ledger](../../90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md)
- [Predecessor Spec 036 Task](./2026-07-17-archive-record-and-workspace-boundary.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| ACER-001 | VAL-ACER-001, VAL-ACER-003, VAL-ACER-007 | Build the closed current census and disposition contract for the 104-record baseline plus six-record delta, current Stage 05 input, and recomputed helper Tests corpus. | platform | Queued | Not executed. | Parent activation input only: 54 Plans + 56 Tasks = 110; frozen 104 + later six = 110; proposed pair yields 55/57 and is retained separately; Stage 05 input 8 Guides + 7 Policies + 9 Runbooks = 24; real authored Incident/Postmortem records 0/0. |
| ACER-002 | VAL-ACER-001, VAL-ACER-004, VAL-ACER-005 | Implement fail-closed eligibility and residue validation plus deterministic dry-run ledger output. | platform | Queued | Not executed. | Must begin with negative fixtures for terminal/age/count-only, ambiguous lineage, current consumer, missing provenance/link/rollback, and unowned residue cases. |
| ACER-003 | VAL-ACER-002, VAL-ACER-006 | Migrate eligible execution records in atomic per-lineage full-body archive batches. | platform | Queued | Not executed. | Each batch must couple source removal, archive creation, index/link repair, ledger evidence, provenance validation, review, rollback, and one logical commit. |
| ACER-004 | VAL-ACER-007 | Audit Stage 05 and helper Tests roles and apply only bounded evidence-backed remediation. | platform | Queued | Not executed. | Recompute current inventories; preserve real operations facts; forbid synthetic events and a second Stage 04 tracker. |
| ACER-005 | VAL-ACER-003 through VAL-ACER-007 | Close retain/DEFER rows and enforce active owner, execution cardinality, and residue rules. | platform | Queued | Not executed. | Every remaining exception requires reason, owner, trigger, and current-authority evidence; unexplained residue must be zero. |
| ACER-006 | VAL-ACER-001 through VAL-ACER-007 | Run full repository-static QA and independent review, prepare atomic lifecycle closure, commit, and record postflight. | platform | Queued | Not executed. | Requires staged lifecycle, strict registry/Markdown/cross-document, archive/residue/census gates, aggregate, applicable pre-commit, fresh requirements/quality verdicts, closure commit, and explicit postflight. |

## Approval and Safety Boundaries

- **Allowed Paths**: Spec 037 and its Stage 03 index; this reciprocal Plan and
  Task plus Stage 04 indexes; eligible Stage 04 execution sources; their exact
  mirrored full-body archive records and archive index; current consumers that
  require link repair; the migration evidence ledger; Stage 05 and helper Tests
  documents with an ACER-004 evidence-backed role finding; focused validators,
  fixtures, and their script/test indexes; directly implicated documentation
  contracts required by a reviewed package.
- **Forbidden Paths**: accepted ADR movement; still-current done Spec movement;
  age/count-only deletion; fabricated Incident/Postmortem or live evidence;
  ignored `_workspace` children; secrets, credentials, tokens, kubeconfigs,
  Vault data, auth files, shell history, and unrelated implementation surfaces;
  CI/FIFO changes owned by Spec 039; Specs 038 and 040 Plan/Task activation.
- **Approval Required**: Remote GitHub changes, push, merge, publication, live
  system action, secret handling, dependency installation, or scope expansion
  beyond the approved Spec/Plan requires separate explicit human approval.
- **Static Validation**: Closed census and disposition checks, eligibility and
  residue negatives, dry-run and batch validators, archive provenance and
  historical/current links, strict registry/Markdown/cross-document/lifecycle,
  changed Markdownlint, diff check, repository aggregate, and applicable
  pre-commit lanes.
- **Live Validation**: `DEFER`. No repository-static package may claim provider,
  remote, Kubernetes, Vault, ESO, Argo CD, or runtime readiness.
- **Secret / Vault Handling**: Do not print or preserve secret-bearing payloads
  through ordinary migration. Use the approved redacted classifier boundary;
  detection blocks the row. Never inspect ignored scratch for evidence or
  secrets.
- **Rollback Plan**: Activation rollback restores parent `a12aedf`. Later
  packages roll back newest-first. Each migration inverse must restore the
  active source, current consumers, indexes, and ledger atomically before the
  archive authority is removed or superseded.
- **Evidence Location**: This Task, reviewed logical commits, per-lineage
  archive/index records, durable migration-ledger rows, focused fixtures, and
  terminal closure evidence. Temporary dry-run output is not closure evidence.

## Verification Summary

The intentional activation RED staged only the new Plan. The lifecycle
validator exited 1 with `LIFECYCLE-CREATE`: it expected exactly one active Plan
and one active Task creation and observed `Plan count 1, Task count 0`. The
complete seven-file activation proposal adds the reciprocal Task, updates Spec
037 and the three indexes, and updates/adds the three exact 14-column ledger
records. The registry relation was already active and is unchanged.

Local activation GREEN is repository-static and staged: lifecycle validation
passes; the registry self-test passes 119 cases and strict mode classifies 436
paths (`baseline=433`, `new=65`, two programs, uncovered 0, ambiguous 0);
strict Markdown reports zero violations; strict cross-document validation is
valid; changed-file Markdownlint and `git diff --cached --check` pass. The exact
proposal contains seven staged paths and zero unstaged paths. JSON validation
is not applicable because this activation changes no JSON file.

Fresh independent activation requirements review returned exact verdict
`REQUIREMENTS COMPLIANT`; activation quality review returned exact verdict
`QUALITY APPROVED`; findings were none. This is planning activation approval,
not package or closure approval. ACER-001 through ACER-006 remain Queued, and
no migration, helper-role remediation, closure, remote, or live result is
claimed.

Predecessor closure commit `855fa78` and postflight commits `cdac53c` and
`a12aedf` are inputs only. ACER implementation and migration results, current
helper Tests disposition, remote/live state, CI/FIFO remediation, and ignored
scratch content remain unclaimed.

## Traceability

- **Plan**: [Active Corpus and Execution Retention Implementation Plan](../plans/2026-07-18-active-corpus-and-execution-retention.md)
- **Spec**: [Spec 037](../../03.specs/037-active-corpus-and-execution-retention/spec.md)
- **Predecessor Task**: [Archive Record and Workspace Boundary Task](./2026-07-17-archive-record-and-workspace-boundary.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [ACER-001](../plans/2026-07-18-active-corpus-and-execution-retention.md#work-breakdown) | Queued. | The parent activation records the 110-record candidate input and 104+6 reconciliation obligation; the proposed pair raises the corpus to 112 and remains active; closed dispositions have not been computed. |
| [ACER-002](../../03.specs/037-active-corpus-and-execution-retention/spec.md) | Queued. | Eligibility, residue, negative fixtures, and dry-run ledger are not implemented. |
| N/A — ACER-003 shares the Plan linked in ACER-001 | Queued. | No execution record has moved and no per-lineage batch result is claimed. |
| N/A — ACER-004 shares the Plan linked in ACER-001 | Queued. | The 24-record Stage 05 input and prior helper Tests inventory still require recomputation and role review. |
| N/A — ACER-005 shares the Plan linked in ACER-001 | Queued. | Retain/DEFER closure and residue cardinality evidence do not yet exist. |
| N/A — ACER-006 shares the Plan linked in ACER-001 | Queued. | Whole-tranche QA, independent review, atomic closure, commit, and postflight are pending. |

The lifecycle table renders the Plan relationship once. Package-level text
provides the remaining navigation without inventing duplicate reciprocal
evidence.
