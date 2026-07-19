---
title: 'Active Corpus and Execution Retention Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-19
---

# Active Corpus and Execution Retention Implementation Plan

## Overview

This Plan records Spec 037 execution in six dependency-ordered packages. It replaces
folder-size assumptions with a closed census and disposition contract, moves
only eligible closed-lineage execution records into full-body archive records,
and audits Stage 05 and helper Tests for role ownership without fabricating
operational evidence.

The activation baseline and rollback parent are
`a12aedfb71ccabd329dabc83bd2863474d1126b0`. Predecessor Spec 036 closed in
commit `855fa78`; repository-static postflight corrections `cdac53c` and
`a12aedf` made that committed closure the current planning input. This
activation changes documentation lineage only. It does not classify a Plan or
Task as archive-eligible, move a record, or claim a validator result.

Fresh independent planning-activation reviews returned exact verdicts
`REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, with no findings. Those
verdicts approved the original active execution decomposition only. ACER-001
through ACER-005 later completed with the reviewed evidence recorded in the
reciprocal Task. ACER-006 now records the terminal staged-closure proposal: the
Plan/Task pair is done and retained as owned Stage 04 `DEFER` evidence until
exact successor migration evidence exists. Exact local staged QA passed the
focused, residue, lifecycle, strict document, archive, aggregate,
changed-file pre-commit, and cached diff gates. Initial independent
requirements and quality reviews required changes; the remediated proposal
then received `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no blocking
findings. Raw all-files pre-commit remains bounded by the Spec 039-owned
`os.mkfifo` `Errno 95`; no FIFO or CI success is claimed. The closure commit and
clean-tree post-commit/postflight do not yet exist and remain pending and
unclaimed.

## Context

The parent `a12aedf` activation input is 54 Plans plus 56 Tasks, for 110
documents. The frozen Spec 037 design baseline covers 104 records (51 Plans
plus 53 Tasks). Six later records are the three reciprocal Plan/Task pairs
created for Specs 034, 035, and 036. At activation, this staged pair raised the
proposed corpus to 55 Plans plus 57 Tasks, or 112 documents. ACER-001 reconciled
the 104-record baseline and six-record delta in one closed census before any
candidate became eligible; the new Spec 037 pair was then a retained active
control, not a migration candidate. The current done pair is terminal owned
`DEFER` evidence with no active execution authority. Its reason is
`terminal-spec-037-lineage-awaiting-successor-migration-evidence`, and its
refresh trigger is `exact-successor-migration-evidence-change`.

The prior Stage 05 input contains 24 authored documents: eight Guides, seven
Policies, and nine Runbooks. There are zero real authored Incident records and
zero real authored Postmortem records. Empty event collections are valid until
a real event exists, so this Plan forbids synthetic records. The earlier helper
Tests inventory is also an input to ACER-001 and ACER-004, but must be
recomputed against the current tracked corpus before it can support a PASS or
remediation claim.

Accepted ADRs and done Specs can remain current authority. Terminal state,
file age, and folder count are never sufficient archive predicates. Spec 039
owns CI integration and the known all-files FIFO portability boundary. Specs
038 and 040 remain active design contracts without Plan/Task activation.

## Goals & In-Scope

- Produce a closed 110-record pre-activation Stage 04 candidate census that
  reconciles the frozen 104 baseline with the six later execution records and
  gives every row an owned `eligible`, `retain`, or `DEFER` disposition; record
  that the Spec 037 pair was the separate active control at activation, then
  preserve its done records as terminal owned `DEFER` without active authority.
- Implement fail-closed eligibility and active-residue validation, including
  explicit closure, current-consumer, source-recovery, link, rollback, and
  exception evidence predicates.
- Migrate eligible records atomically by lineage with full-body archive
  payloads, current index/link repair, durable ledger evidence, and a bounded
  rollback commit for each batch.
- Audit the 24-document Stage 05 input and recomputed helper Tests inventory
  for role overlap, stale current claims, copied template residue, and owner
  gaps while preserving real facts.
- Close the tranche only when every census row and active residue has a
  validated disposition or an owned bounded DEFER.

## Non-Goals & Out-of-Scope

- Moving accepted ADRs or still-current done Specs solely because they are
  terminal, old, or numerous.
- Deleting or archiving by age, count, naming pattern, or subjective staleness
  without lineage and authority evidence.
- Fabricating Incident, Postmortem, live operations, provider, remote, cluster,
  Vault, ESO, Argo CD, or secret evidence.
- Modifying CI workflow or pre-commit FIFO handling; Spec 039 owns that work.
- Activating Plans or Tasks for Specs 038 or 040, or performing the final
  program cutover owned by Spec 040.
- Listing, traversing, opening, hashing, moving, or deleting ignored
  `_workspace` children.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| ACER-001 | Closed census and disposition contract for the 104-record baseline plus six-record delta | None | Reciprocal Spec 037 Plan/Task activation is valid at parent `a12aedf` | Exact parent 54-Plan/56-Task census and proposed 55-Plan/57-Task control; 104+6 candidate reconciliation; current Stage 05 and helper Tests recomputation; every candidate row has a closed disposition vocabulary and owner |
| ACER-002 | Fail-closed eligibility, residue validator, and dry-run ledger | ACER-001 | Reviewed census schema and explicit evidence predicates | Negative fixtures deny terminal/age/count-only movement; dry run emits deterministic eligible/retain/DEFER rows; unexplained residue fails |
| ACER-003 | Atomic per-lineage full-body archive migration batches | ACER-002 | Eligible rows have source, consumer, link, recovery, and rollback proof | Each batch atomically creates archive payload/index evidence, repairs current links, removes the active execution source, records the ledger row, validates, reviews, and commits |
| ACER-004 | Stage 05 and helper Tests role audit with bounded remediation | ACER-001 | Current 24-document operations input and helper Tests corpus are recomputed | Role/profile/current-owner findings have repo-backed evidence; approved bounded fixes land without synthetic events or execution-tracker duplication |
| ACER-005 | Residual retain/DEFER closure and cardinality enforcement | ACER-003, ACER-004 | All eligible migration batches and role remediations are reviewed | Zero unexplained closed-lineage done Plan/Task residue; every retained or DEFER row has reason, owner, trigger, and current authority; cardinality gates pass |
| ACER-006 | Full QA, independent review, and atomic lifecycle closure | ACER-005 | All package commits and durable evidence are present | Repository-static QA, fresh requirements and quality reviews, exact Spec/Plan/Task/index/registry/ledger closure proposal, logical commit, and postflight evidence |

## Verification Plan

| Lane | Focused evidence | Required result |
| --- | --- | --- |
| Inventory | Closed Stage 04/05/helper census and delta reconciliation | Parent 54 Plans plus 56 Tasks equals 110 and 104 baseline plus six delta equals that candidate set; at activation the separate control pair yielded proposed 55/57, and it is now terminal owned `DEFER`; Stage 05 input is 8/7/9 with zero real Incident/Postmortem records |
| Eligibility | Predicate and hostile negative fixtures | No default eligible state; age/count/terminal-only, ambiguous lineage, current consumption, missing source, broken links, or missing rollback proof fail closed |
| Migration | Dry run, per-lineage batch check, and archive integrity | Source removal and full-body archive creation, index/link repair, ledger evidence, provenance, digest, historical links, and rollback are atomic |
| Residue | Active-stage cardinality and ledger join | No unexplained eligible residue; every retain/DEFER record has a bounded reason, owner, and refresh trigger |
| Operations and helper Tests | Profile/owner/content/current-implementation audit | Zero unsupported role overlap, copied prompt residue, stale claim, synthetic event, or unowned exception |
| Repository | Staged lifecycle, strict registry/Markdown/cross-document, changed Markdownlint, diff check, aggregate and applicable pre-commit lanes | Deterministic local PASS, with the Spec 039-owned FIFO condition recorded only in its existing bounded lane |
| Review | Fresh requirements review followed by quality review per package and closure | Blocking findings remediated before each logical commit and before terminal closure |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Frozen baseline is mistaken for the activation input | Six valid records are omitted or the activation control pair is misclassified | Require exact 104+6 reconciliation to the parent 110 candidate records, preserve the pair's separate activation role as historical evidence, and retain its current done records only as terminal owned `DEFER`. |
| Done is treated as disposable | Current authority or execution facts are lost | Join lineage closure, current consumers, source recovery, links, and rollback evidence; default to retain/DEFER. |
| Large migration obscures causality | Review and rollback become unsafe | Migrate only atomic per-lineage batches with an independently reviewed logical commit. |
| Operations completeness is fabricated | False incident or postmortem evidence enters the corpus | Treat zero real events as valid and forbid placeholder event creation. |
| Helper Tests become a second Task tracker | SDLC ownership and evidence diverge | Audit helper Tests as feature-local support and keep execution state only in Stage 04 Tasks. |
| CI portability work leaks into this tranche | Ownership conflict with Spec 039 | Keep CI/FIFO changes out of scope and record only observed local evidence. |

Rollback before terminal closure is newest-first at a reviewed package boundary.
For an archive batch, restore the current execution record, consumers, index,
and ledger in one inverse commit; never delete an archive consumer before its
source restoration is complete. If evidence is ambiguous, stop at DEFER rather
than forcing a migration. The activation proposal can be reversed to parent
`a12aedf` without touching implementation surfaces.

## Completion Criteria

- The 104-record frozen baseline and six-record delta reconciled exactly to the
  parent 54-Plan/56-Task activation input, with no unclassified candidate; the
  observed activation proposal reached 55 Plans/57 Tasks and retained the pair
  separately. The current done pair is terminal owned `DEFER`, carries no
  active execution authority, and remains until exact successor migration
  evidence changes.
- Every eligible record has migrated by atomic lineage batch with full-body
  provenance, current-link repair, durable evidence, and rollback metadata.
- Accepted ADRs and still-current done Specs remain protected from
  terminal/age/count-only movement.
- The prior 24-document Stage 05 input and recomputed helper Tests corpus have
  zero unsupported ownership or role conflicts; no synthetic Incident or
  Postmortem exists.
- Active execution cardinality and residue checks pass, or each retained/DEFER
  exception has an explicit reason, owner, and refresh trigger.
- ACER-001 through ACER-005 have RED/GREEN, independent review, logical commit,
  and repository-static QA evidence. ACER-006 has observed staged local QA,
  remediated requirements compliance, and remediated quality approval. The
  closure commit and clean-tree post-commit/postflight remain explicit pending
  gates.
- CI/FIFO work, remote/live state, provider delivery, secrets, and ignored
  scratch remain unclaimed and outside the tranche.

## Traceability

- **Spec**: [Active Corpus and Execution Retention](../../03.specs/037-active-corpus-and-execution-retention/spec.md)
- **Task**: [Active Corpus and Execution Retention Task](../tasks/2026-07-18-active-corpus-and-execution-retention.md)
- **PRD**: [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- **ARD**: [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- **Archive decision**: [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-ACER-001](../../03.specs/037-active-corpus-and-execution-retention/spec.md#success-criteria--verification-plan) | ACER-001 | [Closed census and disposition evidence](../tasks/2026-07-18-active-corpus-and-execution-retention.md#task-table) |
| N/A — VAL-ACER-002 shares the Spec 037 source linked in VAL-ACER-001 | ACER-002, ACER-003 | N/A — the paired Task is linked in VAL-ACER-001 |
| N/A — VAL-ACER-003 shares the Spec 037 source linked in VAL-ACER-001 | ACER-001, ACER-005 | N/A — the paired Task is linked in VAL-ACER-001 |
| N/A — VAL-ACER-004 shares the Spec 037 source linked in VAL-ACER-001 | ACER-002, ACER-005 | N/A — the paired Task is linked in VAL-ACER-001 |
| N/A — VAL-ACER-005 shares the Spec 037 source linked in VAL-ACER-001 | ACER-002, ACER-005 | N/A — the paired Task is linked in VAL-ACER-001 |
| N/A — VAL-ACER-006 shares the Spec 037 source linked in VAL-ACER-001 | ACER-003, ACER-005 | N/A — the paired Task is linked in VAL-ACER-001 |
| N/A — VAL-ACER-007 shares the Spec 037 source linked in VAL-ACER-001 | ACER-004, ACER-005 | N/A — the paired Task is linked in VAL-ACER-001 |

The lifecycle table renders each reciprocal relationship target once. The
work-package anchors retain complete navigation without manufacturing extra
body-evidence cardinality.

### Detailed Package Map

| Work package | Scope |
| --- | --- |
| ACER-001 | Closed current census and frozen-baseline delta reconciliation |
| ACER-002 | Eligibility, residue, negative fixtures, and dry-run ledger |
| ACER-003 | Atomic per-lineage full-body archive migration batches |
| ACER-004 | Stage 05 and helper Tests role audit and bounded remediation |
| ACER-005 | Retain/DEFER closure and active cardinality enforcement |
| ACER-006 | Full QA, fresh review, exact lifecycle closure, and postflight |
