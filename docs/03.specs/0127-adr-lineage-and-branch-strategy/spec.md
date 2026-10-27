---
title: "ADR Lineage and Branch Strategy"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0127"
---

# ADR Lineage and Branch Strategy Technical Specification (Spec)

## Overview

SPEC-0125 left CR-09.06 partial and CR-13.07 as a gap. The lifecycle
validator requires each superseded ADR to link reciprocally to a successor,
but it accepts two ADRs that supersede each other, which leaves no current
decision. The decision template has no prompt for decision makers or
confirmation, the ADR log does not state that numbers are never reused, and
no ADR records why `main` is the only long-lived branch. This Spec closes
those four points. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-adr-lineage-and-branch-strategy.md) records it.

## Strategic Boundaries & Non-goals

- In scope: `scripts/document_lifecycle.py` and its test, the decision
  template, the ADR log README, ADR-0052, one line in
  `.agents/governance/git.md`, this package and the Stage 03 README index.
- Non-goals:
  - new required ADR sections or frontmatter keys, which would invalidate
    existing ADRs;
  - changing branch protection, rulesets, the deployment model or the
    release producer;
  - rewriting existing ADR numbers or approvals.

## Contracts

- A superseded document whose successor chain can only return to a
  document already visited, or that has no reciprocal successor, fails
  `LIFECYCLE-EVIDENCE`; a chain that reaches a non-superseded successor
  passes.
- The template asks for decision makers and decision date when they differ
  from `owner` and `updated`, and for how compliance is confirmed, as
  prompts only.
- ADR numbers are never reused; MIG-0002's one-time conversion and approved
  Archive removals are separate decisions that do not rewrite numbers.
- [ADR-0052](../../02.architecture/decisions/0052-single-main-trunk-branch-strategy.md)
  records the branch strategy; it takes effect only when the operator
  accepts it.

## Core Design

The validator follows reciprocal successors from a newly superseded
document, skipping documents already visited, until it reaches a successor
whose status is not superseded. The template and README changes reuse the
Nygard and MADR fields that SPEC-0127's research compared with the current
form.

## Data Modeling & Storage Strategy

No stored data.

## Interfaces & Data Structures

- `_reciprocal_successor` and `_terminal_supersession_evidence` in
  `scripts/document_lifecycle.py`.
- Two tests in `tests/test_document_lifecycle_archive_cutover.py`.

## Edge Cases & Error Handling

- A legitimate chain (A superseded by B, B superseded by C, C accepted)
  passes because the walk skips the visited predecessor.
- A successor missing from the proposed snapshot ends the walk as before.

## Failure Modes & Fallback / Human Escalation

Reverting the pull request restores the previous rule. If the operator does
not accept ADR-0052, it stays proposed and `git.md` does not cite it as
accepted.

## Verification Commands

- `python3 -m unittest tests.test_document_lifecycle_archive_cutover`.
- `python3 scripts/validate-document-lifecycle.py --mode strict`.
- `python3 scripts/validate-document-contract-registry.py`.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-AB-001 | A supersession cycle fails and a reciprocal supersession passes in new tests that fail before the change for the cycle, and strict lifecycle validation passes on the repository. |
| VAL-AB-002 | The template prompt and the never-reuse rule are in place, the comparison with Nygard, MADR and Y-statement is recorded, and the registry and form tests pass. |
| VAL-AB-003 | ADR-0052 compares the branch models with cited sources and repository facts, `git.md` links it, and the operator accepts it. |
| VAL-AB-004 | Staged QA passes on every commit and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AB-001 | Lifecycle tests and strict validation |
| [REQ-0003-FR-0023](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AB-002 | Template and README review |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AB-003 | ADR review and operator acceptance |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AB-004 | Staged QA and hosted checks |
