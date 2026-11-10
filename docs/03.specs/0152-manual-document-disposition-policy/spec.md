---
title: "Manual Document Disposition Review"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-10"
layer: "specs"
artifact_id: "SPEC-0152"
---

# Manual Document Disposition Review Technical Specification (Spec)

## Overview

This approved local change contract adds a manual preservation and recovery decision before a current document is deleted or moved. [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md) owns the durable need. The [Plan](plan.md) orders the local documentation work, and [Task 0001](tasks/tsk-0001-manual-document-disposition-policy.md) records execution and acceptance. The proposed [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) records the scoped decision.

## Strategic Boundaries & Non-goals

- Scope: current documents and future dispositions in this workspace; existing governance policy, the reference runbook, their current readers, and one scoped ADR. The user's later language instruction also covers faithful English translation of all remaining Korean prose in `.agents/governance/`.
- The current user approved this Spec and Plan for local commits after the actual batch review, then separately authorized a narrow initial-approval contract and validator amendment. The owning Task records the distinct approval sources, reviewer binding and current limits. Protected deletion, remote publication, live operations, ADR acceptance and criterion acceptance remain separate decisions.
- No archive catalog, ledger, archive-disposition schema or gate, CI change, historical bulk reassessment, restoration or actual document disposition is in scope. The only added machine behavior is a contextual first-record Spec/Plan approval receipt and its focused validation. The archive body remains unvalidated; its README keeps the existing style exception.
- Other repositories, Vault records, shared memory and operational data keep their own retention owners.

## Contracts

- Before disposition, the responsible owner assesses current, historical, audit and recovery consumers; preservation value and access need; holds; authority; and transfer of current meaning. The existing Task records the decision and its evidence.
- Git-history-only disposition requires an exact source `commit:path` reachable from the intended history whose bytes match the current source being removed, plus a temporary byte-identical restoration before removal. Stage 01–03 use the current owner's Archived Lineage; other profiles use their existing relationships or disposition record. The existing Task carries the factual review for every type.
- Missing authority, unresolved hold or consumer, or failed recovery defers only that disposition. A document selected for original-body preservation is handled according to its actual consumer and protection decision, not by an automatic archive copy.
- Prior accepted decisions and completed evidence retain their dated meaning. A new disposition does not create a separate Spec solely because it is a disposition.

## Core Design

The proposed ADR-0056 narrows the disposal-without-proof language in [ADR-0053](../../02.architecture/decisions/0053-unvalidated-archive.md) and the archive clauses of [ADR-0055](../../02.architecture/decisions/0055-governance-decision-current-state-amendment.md) without replacing their other decisions. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) keeps the current system view. The document lifecycle policy owns the manual rule; the authoring policy routes evidence to the existing Task and current owner; the SDLC policy orders disposition after handoff; the reference runbook gives operators the steps. Current stage READMEs point to those owners. The Stage 99 local extension and lifecycle reader admit an approved first Git record only when the same-package Spec and Plan, independent review, user approval receipt and exact approved bytes agree; ordinary first creation remains draft.

## Data Modeling & Storage Strategy

No new persistent store or document field is introduced. The existing Task Inputs and Approval and Safety Boundaries hold the target and authority. Task Evidence holds consumer, hold, source identity, restoration observations, independent review and first-record approval receipt. The current owner's Archived Lineage retains source identification when a Stage 01–03 document leaves; other profiles retain their existing relationships or disposition record. Git holds original bytes.

## Interfaces & Data Structures

The disposition interface is the human procedure in the current documents. It accepts a named document and intended disposition, and produces a recorded allow or defer decision with its evidence in the owning Task. The separate local first-record approval interface uses an exact Stage 99 extension marker and two existing Task Evidence rows: one independent review row bound to final Spec/Plan SHA-256 values, and one user approval receipt bound to the same values and typed document identities. The lifecycle reader accepts only that contextual pair and does not authenticate the user or the approval source. Validation dispatch and archive-body exclusions remain unchanged.

## Edge Cases & Error Handling

An absent source object, shallow or unreachable history, byte mismatch, unsaved source edits, unresolved hold, unknown historical consumer or unclear authorizer yields defer. A document with no current consumer is not automatically disposable. Frozen-body preservation is considered only after identifying a real preservation consumer; this change does not introduce a frozen archive route. For first-record approval, a missing paired parent, unrelated review row, stale or mismatched digest, absent receipt, wrong approval scope or revocation prevents the exception; normal draft creation remains available.

## Failure Modes & Fallback / Human Escalation

The operator keeps the affected source untouched and names the next owner when a condition is unresolved. A policy or link check failure returns the affected change to its document owner for correction and renewed review. Any later protected deletion or live action follows its separate approval route. No old completed record is rewritten to make the new rule appear retroactive.

## Verification Commands

Run selected local document checks through `python3 scripts/qa.py quick` over changed working-tree bytes and focused document-contract regressions for the initial-approval reader. Before a requested commit, run exact-index `python3 scripts/qa.py staged` through the active hook. Inspect the changed text against the current owner and obtain an independent read-only semantic review of the final approved parent bytes. Static PASS proves only the stated repository snapshot; it does not prove a future manual recovery trial, user authenticity or operator criterion acceptance.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-DISP-001 | Current policy and runbook require a per-document consumer, preservation, hold and authority review before disposition, with a defer outcome. |
| VAL-DISP-002 | Current policy and runbook specify exact source `commit:path`, reachability and temporary byte comparison for Git-history-only disposition, with existing Task and current-owner evidence. |
| VAL-DISP-003 | Current requirement, ADR, policies and navigation agree on the scoped procedure while archive validation exclusions and prior historical evidence remain intact; all `.agents/governance/` prose is English. Focused positive and negative first-record approval regressions, selected checks and independent review of the exact approved Spec/Plan bytes report no blocking finding. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DISP-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), proposed [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Review policy and runbook against a held-document counterexample. |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DISP-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), proposed [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Review exact Git recovery steps and failed-restoration disposition. |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DISP-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), proposed [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Selected document/profile/link/lifecycle QA and independent semantic review. |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DISP-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), proposed [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Stage 99 extension and focused receipt regressions; independent review of final approved parent bytes. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DISP-003 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md), proposed [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) | Typed lifecycle reader and focused receipt regressions; independent review of final approved parent bytes. |
