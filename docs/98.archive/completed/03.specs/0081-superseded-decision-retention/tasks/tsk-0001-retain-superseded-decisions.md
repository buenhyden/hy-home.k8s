---
title: "Retain the Superseded Decisions"
version: "0.1.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0081-TSK-0001"
---

# Task: Retain the Superseded Decisions

## Overview

This Task records the retention of the fifteen remaining superseded decisions.
It records observed results only and never promotes a repository-static result
to hosted, provider-runtime, or live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order.
- On 2026-09-15 the request owner approved each disposition.
- Comparison base: `1910cff510f850a3342bdd80355872c05ee12519`.

## Task Table

| ID       | Upstream criterion | Work item                                                   | Owner    | Status | Result                                                    | Evidence                    |
| -------- | ------------------ | ----------------------------------------------------------- | -------- | ------ | --------------------------------------------------------- | --------------------------- |
| WORK-001 | VAL-SDR-002        | Name the fifteen by identifier in current documents         | platform | Done   | 59 links in 26 documents became identifiers | Link gate                   |
| WORK-002 | VAL-SDR-001        | Retain the fifteen with one catalog row each                | platform | Done   | Rebased bodies and fifteen Retention Envelopes            | Lifecycle and archive gates |
| WORK-003 | VAL-SDR-003        | Record the evidence                                         | platform | Done   | Recorded below                                            | This record                 |

## Approval and Safety Boundaries

- **Allowed Paths**: the fifteen decisions and their retained paths,
  `docs/02.architecture/decisions/README.md`, `docs/02.architecture/README.md`,
  `docs/README.md`, `docs/03.specs/README.md`, `docs/98.archive/README.md`
  outside its frozen manifest comment and record table,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`, the
  SPEC-0054 Spec, `tests/test_archive_disposition_lifecycle.py`, this package,
  and the documents whose links changed: `docs/02.architecture/decisions/0026-argo-cd-source-integrity-non-adoption.md`, `docs/02.architecture/decisions/0028-pod-security-admission-per-namespace-adoption.md`, `docs/02.architecture/decisions/0030-authority-first-sdlc-and-agent-governance-convergence.md`, `docs/02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md`, `docs/02.architecture/decisions/0033-common-document-contract-v9.md`, `docs/02.architecture/decisions/0036-common-knowledge-and-prompt-surfaces.md`, `docs/02.architecture/descriptions/0006-workspace-agent-governance-platform.md`, `docs/03.specs/0047-current-surface-and-stash-reconciliation/plan.md`, `docs/03.specs/0047-current-surface-and-stash-reconciliation/spec.md`, `docs/03.specs/0048-github-routing-and-ci-evidence/plan.md`, `docs/03.specs/0048-github-routing-and-ci-evidence/spec.md`, `docs/03.specs/0049-platform-validation-and-security-evidence/plan.md`, `docs/03.specs/0049-platform-validation-and-security-evidence/spec.md`, `docs/03.specs/0050-example-iac-and-validator-qa/plan.md`, `docs/03.specs/0050-example-iac-and-validator-qa/spec.md`, `docs/03.specs/0051-repository-assurance-integration-and-closure/plan.md`, `docs/03.specs/0051-repository-assurance-integration-and-closure/spec.md`, `docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/plan.md`, `docs/03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md`, `docs/03.specs/0062-workspace-research-full-corpus-reverification/plan.md`, `docs/03.specs/0062-workspace-research-full-corpus-reverification/spec.md`, `docs/03.specs/0070-retired-provider-residue-disposition/spec.md`, `docs/03.specs/0071-document-taxonomy-and-form-identity-normalization/spec.md`, `docs/03.specs/0072-agent-governance-and-quality-gate-consolidation/tasks/tsk-0001-consolidate-governance-and-quality-gates.md`, `docs/03.specs/0073-provider-native-enforcement-parity/tasks/tsk-0001-establish-provider-native-enforcement-parity.md`, `docs/03.specs/0075-common-knowledge-and-prompt-surfaces/spec.md`.
- **Forbidden Paths**: frozen records, ledgers, and retained packages under
  `docs/98.archive/`, `scripts/`, `gitops/`, `infrastructure/`, `policy/`,
  `secrets/`, `.github/`.
- **Approval Required**: The request owner approved each disposition. Push, pull
  request, and merge are not approved.
- **Static Validation**: `python3 scripts/qa.py staged` over the exact index and
  one `python3 scripts/qa.py full` on the final tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed.
- **Rollback Plan**: Revert the retention commit.
- **Evidence Location**: This Task record.

## Verification Summary

Final: `python3 scripts/qa.py full` returned `EXIT=0` with 22 of 22 gates
`PASS` on the staged final tree of this change, before this summary was
written. `python3 scripts/qa.py staged` returned `EXIT=0` with the 6 gates it
selected for these paths `PASS`, after the review fixes and again after this
Task-only summary. The affected unit modules for the lifecycle fixture, link
boundary, archive cutover, dispositions, and affected surfaces ran 108 tests,
all OK.

Each retained body differs from its source only in relative link prefixes,
which the lifecycle gate compares through the fifteen moves together. Under
`docs/98.archive/` only the fifteen retained bodies, their catalog rows, and
the catalog introduction changed.

Review: one independent read-only review confirmed the body equivalence, the
unchanged frozen content, the consumer count, and that no validator changed.
It reported three HIGH findings: present-tense sentences that still said
superseded decisions stay in the decision log, twice in the SPEC-0054 Spec and
once in AD-0006. A matching sentence it could not confirm in AD-0007 was the
same defect. All four now state the ADR-0038 retention. A formatter re-aligned
an unrelated AD-0006 table during that repair; the file was rebuilt so only the
sentence changed.

Kept as history: dated Plan and Task text in SPEC-0051, SPEC-0062, SPEC-0072,
SPEC-0075, and SPEC-0079 that names an old decision path without linking it.
The legacy record-route error in `scripts/archive_recovery.py` belongs to the
frozen ADR-0032 generation and applies to no retention.

Residual risk: the frozen-registry fidelity test still skips without commit
`c652331c`. Hosted CI, provider runtime, and live evidence were not observed.
SPEC-0080 and this package stay at their creation states until a closing
change.

Next owner: the request owner, for push, pull request, and merge.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item                 | Result | Evidence                     |
| ------------------------------------- | ------ | ---------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Done.  | Link gate.                   |
| [WORK-002](../plan.md#work-breakdown) | Done.  | Lifecycle and archive gates. |
| [WORK-003](../plan.md#work-breakdown) | Done.  | Full QA.                     |
