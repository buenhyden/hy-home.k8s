---
title: "Cut Over the Registry and Validators"
version: "0.1.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0082-TSK-0002"
---

# Task: Cut Over the Registry and Validators

## Overview

This Task records the second integration: accepting ADR-0039 and moving the
registry, validators, forms, and governance prose to the unit retention
contract. It records observed results only and never promotes a
repository-static result to hosted, provider-runtime, or live evidence.

## Inputs

- [Spec](../spec.md) owns the contract, and [Plan](../plan.md) owns order.
- Entry gate: the proposal integration has merged, and the request owner has
  accepted ADR-0039.
- On 2026-09-15 the request owner approved accepting ADR-0039 once the
  proposal merged. Pull request #64 merged as `b16f23f9`, and the proposal
  commits `c07ee272`, `cd3139e6`, `97a2101b`, and `b7ba5db2` are reachable from
  `origin/main`. The cutover branch is `feat/archive-unit-retention-cutover`.
- The proposal Task records the survey findings each regression starts from.

## Task Table

| ID       | Upstream criterion | Work item                                                                                        | Owner    | Status | Result       | Evidence                     |
| -------- | ------------------ | ------------------------------------------------------------------------------------------------ | -------- | ------ | ------------ | ---------------------------- |
| WORK-001 | VAL-UAR-011        | Accept ADR-0039, supersede ADR-0038, activate this package, and close SPEC-0080 and SPEC-0081    | platform | Done   | ADR-0039 accepted, ADR-0038 superseded, SPEC-0080 and SPEC-0081 done | Lifecycle gate               |
| WORK-002 | VAL-UAR-004        | Declare units, modes, the citation table, and the legacy set in the registry, schema, and loader | platform | Done   | Declared in `1bf091be`; fifteen registry regressions pass | Registry regressions         |
| WORK-003 | VAL-UAR-006        | Decide citation in the shared resolver for the link and archive validators                | platform | Done   | One decision in `32ce8496`; both validators consume it | Link and archive regressions |
| WORK-004 | VAL-UAR-005        | Compare units as Git objects and admit a class by anchor state                                   | platform | Done   | Entry-for-entry comparison in `f33efb5f`; membership, byte, mode, type, and reachability faults rejected | Lifecycle regressions        |
| WORK-005 | VAL-UAR-007        | Admit identity-preserving moves between active stages                                            | platform | Done   | Identity lineage in `f33efb5f`; a changed or ambiguous identity stays rejected | Lifecycle regressions        |
| WORK-006 | VAL-UAR-008        | Re-verify every catalog row on the full lane                                                     | platform | Done   | `catalog_envelope_diagnostics` in `f33efb5f`; a missing, unreachable, or mistyped object fails | Archive cutover regressions  |
| WORK-007 | VAL-UAR-009        | State the adopted contract in governance, indexes, the skill, and forms, and add the fast gate   | platform | In progress | Prose and the `archive-contract-tests` gate are written; QA is pending | Staged and full QA           |

## Approval and Safety Boundaries

- **Allowed Paths**: the cutover scope named in the [Spec](../spec.md).
- **Forbidden Paths**: frozen records, ledgers, and retained packages under
  `docs/98.archive/`, the sixteen ADR-0038 retained bodies, `gitops/`,
  `infrastructure/`, `policy/`, `secrets/`, `.github/`.
- **Approval Required**: accepting ADR-0039 before any work item starts. Push,
  pull request, and merge are not approved.
- **Static Validation**: focused regressions per work item,
  `python3 scripts/qa.py staged` per logical commit, and one
  `python3 scripts/qa.py full` on the final tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed.
- **Rollback Plan**: Revert the cutover commits before integration.
- **Evidence Location**: This Task record.

## Verification Summary

Observed on 2026-09-16 on `feat/archive-unit-retention-cutover`. Each result is
a repository-static result from this workstation; no hosted CI result is
claimed for this branch.

- `python3 -m unittest discover -s tests -t .` passed 1095 tests, 4 skipped, on
  the WP-008 tree.
- `python3 scripts/qa.py staged` passed its eleven gates before each of
  `1bf091be`, `32ce8496`, and `f33efb5f`.
- `python3 scripts/validate-links-and-owners.py --root . --mode strict` passed
  over the whole corpus, so no current citation depended on the exemption the
  citation table narrows.
- `python3 scripts/archive_cutover.py --root .` passed with `records=25`,
  `historical_links=198`, and `secret_clean=25`, with every catalog row
  re-verified against the history it names.
- `python3 scripts/run-archive-contract-tests.py --root .` passed 87 tests.
- A review of the staged WP-008 diff reported one HIGH fail-open finding, where
  two unreadable entry listings compared equal; the comparison now fails closed
  and a regression covers it.
- `python3 scripts/qa.py full` has not run on the final tree yet.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item                 | Result        | Evidence                      |
| ------------------------------------- | ------------- | ----------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Done. | Lifecycle gate.               |
| [WORK-002](../plan.md#work-breakdown) | Done. | Registry regressions.         |
| [WORK-003](../plan.md#work-breakdown) | Done. | Link and archive regressions. |
| [WORK-004](../plan.md#work-breakdown) | Done. | Lifecycle regressions.        |
| [WORK-005](../plan.md#work-breakdown) | Done. | Lifecycle regressions.        |
| [WORK-006](../plan.md#work-breakdown) | Done. | Archive cutover regressions.  |
| [WORK-007](../plan.md#work-breakdown) | In progress. | Staged and full QA.           |
