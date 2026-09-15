---
title: "Move Registry Routes, Archive Forms, and Validators"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0079-TSK-0002"
---

# Task: Move Registry Routes, Archive Forms, and Validators

## Overview

This Task owns the machine step of Spec 0079: the registry, archive forms, lint
configuration, validators, and tests move to the six-disposition model in one
change, with every frozen Stage 98 record passing unmodified. The request owner
authorized it on 2026-09-15 together with ADR-0038 acceptance.

## Inputs

- [Spec](../spec.md) owns the contract and criteria, and [Plan](../plan.md)
  owns WP-005.
- [ADR-0038](../../../02.architecture/decisions/0038-six-disposition-archive-stage.md)
  must be accepted before this Task starts.
- The governance step recorded by
  [tsk-0001](tsk-0001-state-the-six-disposition-contract.md) states the
  contract this Task implements.
- Observed on 2026-09-15: the retention-class list is hardcoded as `completed`
  in `scripts/archive_validation.py` (`RETENTION_CLASSES`),
  `scripts/validate-document-lifecycle.py` (`RETENTION_CLASS_SOURCE_STATES`),
  and the archive boundary of `scripts/validate-links-and-owners.py`;
  `scripts/archive_recovery.py` refuses an architecture decision route with
  `ARCHIVE-DISPOSITION-ADR`; and the `archive/tombstone` path pattern matches
  every Stage 98 path outside `migrations/` and `completed/`.

## Task Table

| ID       | Upstream criterion | Work item                                                                                                                                                                                                                                                                                                                                                                  | Owner    | Status | Result       | Evidence                                           |
| -------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------ | ------------ | -------------------------------------------------- |
| WORK-001 | VAL-SDA-005        | Registry: add the `superseded/`, `retired/`, and `resolved/` retention alternatives to the origin profiles of Stages 01, 02, 03, 05, 90, and 99; split the frozen record generation from a body-less tombstone route disposition; give new migration records a body-less form while frozen ledgers keep their generation; bind each class to the terminal states it admits | platform | Queued | Not executed | Registry gate and index parity                     |
| WORK-002 | VAL-SDA-005        | Forms and configuration: the archive tombstone and migration forms, the archive paragraphs of the Stage 99 guide, and the `retired/` and `resolved/` entries in `.markdownlint-cli2.yaml`                                                                                                                                                                                  | platform | Queued | Not executed | Profile gate and pre-commit manual stage           |
| WORK-003 | VAL-SDA-005        | Validators: generation-first classification, retention rehome for every class, the link boundary admitting `resolved/`, the architecture decision route, and the catalog Retention Envelope parser; remove the three hardcoded class lists                                                                                                                                 | platform | Queued | Not executed | Strict profile, link, lifecycle, and archive gates |
| WORK-004 | VAL-SDA-005        | Tests: a positive and a negative case per family, a frozen record for each frozen form that must pass unmodified, and a rejected second recovery ledger                                                                                                                                                                                                                    | platform | Queued | Not executed | Unit discovery under full QA                       |
| WORK-005 | VAL-SDA-006        | Evidence: staged QA over the exact cutover index and one full QA on the final tree                                                                                                                                                                                                                                                                                         | platform | Queued | Not executed | This record                                        |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/99.templates/registry.json`,
  `docs/99.templates/templates/archive/`, `docs/99.templates/README.md`,
  `.markdownlint-cli2.yaml`, `scripts/archive_validation.py`,
  `scripts/archive_recovery.py`, `scripts/archive_cutover.py`,
  `scripts/document_lifecycle.py`, `scripts/validate-document-lifecycle.py`,
  `scripts/validate-links-and-owners.py`, `scripts/validate-markdown-profiles.py`,
  the archive and lifecycle tests under `tests/`, and this package.
- **Forbidden Paths**: every frozen record, ledger, and retained package under
  `docs/98.archive/`, the manifest comment and record table of
  `docs/98.archive/README.md`, `gitops/`, `infrastructure/`, `policy/`,
  `secrets/`, `.github/`.
- **Approval Required**: ADR-0038 accepted, and the request owner's approval to
  start. Weakening a gate, rewriting frozen content, and executing a
  disposition are not approved by this Task.
- **Static Validation**: `python3 scripts/qa.py staged` over the exact index and
  one `python3 scripts/qa.py full` on the final tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed; frozen payloads are validated, not displayed.
- **Rollback Plan**: The cutover is one commit that reverts alone.
- **Evidence Location**: This Task record.

## Verification Summary

Started. The entry gate holds: ADR-0038 was accepted in the change that moved
this Task to in-progress.

## Traceability

Each work item carries its result once executed.

### Lifecycle Traceability

| Criterion / work item                 | Result        | Evidence         |
| ------------------------------------- | ------------- | ---------------- |
| [WORK-001](../plan.md#work-breakdown) | Not executed. | Entry gate open. |
| [WORK-002](../plan.md#work-breakdown) | Not executed. | Entry gate open. |
| [WORK-003](../plan.md#work-breakdown) | Not executed. | Entry gate open. |
| [WORK-004](../plan.md#work-breakdown) | Not executed. | Entry gate open. |
| [WORK-005](../plan.md#work-breakdown) | Not executed. | Entry gate open. |
