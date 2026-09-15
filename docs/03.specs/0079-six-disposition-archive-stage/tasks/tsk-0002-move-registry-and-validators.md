---
title: "Move Registry Routes, Archive Forms, and Validators"
version: "1.0.0"
type: "sdlc/task"
status: "done"
owner: "platform"
updated: "2026-09-15"
layer: "specs"
artifact_id: "SPEC-0079-TSK-0002"
---

# Task: Move Registry Routes, Archive Forms, and Validators

## Overview

This Task owns the machine step of Spec 0079: the registry, archive forms, lint
configuration, validators, and tests moved to the six-disposition model in one
change, with every frozen Stage 98 record, ledger, and retained package passing
unmodified. The request owner authorized it on 2026-09-15 together with ADR-0038
acceptance.

## Inputs

- [Spec](../spec.md) owns the contract and criteria, and [Plan](../plan.md)
  owns WP-005.
- [ADR-0038](../../../02.architecture/decisions/0038-six-disposition-archive-stage.md)
  was accepted in the change before this one.
- The governance step recorded by
  [tsk-0001](tsk-0001-state-the-six-disposition-contract.md) states the
  contract this Task implements.
- Observed on 2026-09-15: every migration ledger row admitted a document move,
  not only archive retention, so the request owner chose a body-less scope
  migration that names the moved scope and its current owner, with Git history
  carrying the bytes.

## Task Table

| ID       | Upstream criterion | Work item                                                                                                                                                                                                                                  | Owner    | Status | Result                                                                                                    | Evidence                                           |
| -------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------ | --------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| WORK-001 | VAL-SDA-005        | Registry: retention classes bound to their source states, mirrored retention routes on the origin profiles of Stages 01, 02, 03, 05, and 90, frozen records and ledgers routed by exact path, and the body-less route disposition profiles | platform | Done   | `retention_classes`, mirrored routes, exact frozen routes, `route-disposition` family, two route profiles | Registry gate: 778 paths, 0 ambiguous              |
| WORK-002 | VAL-SDA-005        | Forms and configuration: the route tombstone and scope migration forms, the archive paragraphs of the Stage 99 guide, and the `retired/` and `resolved/` entries in `.markdownlint-cli2.yaml`                                              | platform | Done   | Two forms and their template profiles; guide, form index, and lint ignores                                | Profile gate and pre-commit manual stage           |
| WORK-003 | VAL-SDA-005        | Validators: generation-first classification, catalog-proved retention and scope moves, the link boundary admitting `resolved/`, and catalog parity; no current class list is hardcoded                                                     | platform | Done   | `scripts/archive_dispositions.py` shared by the archive, cutover, link, and lifecycle validators          | Strict profile, link, lifecycle, and archive gates |
| WORK-004 | VAL-SDA-005        | Tests: positive and negative cases per family, frozen fixtures that still pass, and a rejected second recovery identity                                                                                                                    | platform | Done   | Owner, lifecycle, and link tests; frozen-generation fixtures run under the legacy generation registry     | Unit discovery under full QA                       |
| WORK-005 | VAL-SDA-006        | Evidence: staged QA over the exact cutover index and one full QA on the final tree                                                                                                                                                         | platform | Done   | Recorded below                                                                                            | This record                                        |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/99.templates/registry.json`,
  `docs/99.templates/contracts/document-profile.schema.json`,
  `docs/99.templates/templates/archive/`, `docs/99.templates/README.md`,
  `docs/99.templates/templates/README.md`, `.markdownlint-cli2.yaml`,
  `scripts/archive_dispositions.py`, `scripts/archive_validation.py`,
  `scripts/archive_cutover.py`, `scripts/document_authority.py`,
  `scripts/document_contracts.py`, `scripts/document_lifecycle.py`,
  `scripts/validate-document-lifecycle.py`,
  `scripts/validate-links-and-owners.py`, `scripts/validate-markdown-profiles.py`,
  the archive, lifecycle, link, identity, and registry tests under `tests/`,
  the transition sentences the governance step left in common governance and
  the stage indexes, and this package. The schema, the authority key check, and
  the typed registry were added because the registry could not carry the class
  binding without them; the prose was added because the boundary it stated no
  longer holds.
- **Forbidden Paths**: every frozen record, ledger, and retained package under
  `docs/98.archive/`, the manifest comment and record table of
  `docs/98.archive/README.md`, `gitops/`, `infrastructure/`, `policy/`,
  `secrets/`, `.github/`.
- **Approval Required**: ADR-0038 accepted and the request owner's approval to
  start, both given. Weakening a gate, rewriting frozen content, executing a
  disposition, push, pull request, and merge are not approved by this Task.
- **Static Validation**: `python3 scripts/qa.py staged` over the exact index and
  one `python3 scripts/qa.py full` on the final tree.
- **Live Validation**: DEFER. No live cluster, provider runtime, or network
  action is authorized.
- **Secret / Vault Handling**: No secret, credential, or private configuration
  file is read or printed; frozen payloads are validated, not displayed.
- **Rollback Plan**: The cutover is one commit that reverts alone.
- **Evidence Location**: This Task record.

## Verification Summary

Final: `python3 scripts/qa.py full` returned `EXIT=0` with 22 of 22 gates
`PASS` on the staged cutover tree, including unit discovery and the pre-commit
manual stage. `python3 scripts/qa.py staged` passed 12 of 12 gates over the
exact index before this summary was written.

Repairs during the work: staging removed the index and worktree drift
diagnostics that direct archive runs report on uncommitted changes; the first
full run found `ruff-format` drift, an eager `document_contracts` import that
broke `from scripts import archive_validation`, and a widened stage grammar
check that contradicted the root README contract, so the registry owner now
loads lazily and grammar coverage stays where it was before the cutover.

Tests: 164 failures appeared when the registry closed the frozen generation,
because synthetic ledgers and records no longer route. Regressions that
exercise the frozen machinery now run under the registry of `c652331c`, the
last merged commit before the cutover; current-registry assertions were kept
or added beside them. New cases cover classification, catalog parsing and
parity, lifecycle admission, immutability, and citability.

Review: an independent read-only review confirmed three defects, each fixed
test-first: retained bodies and route records were not immutable after their
disposition, a route disposition's envelope was not bound to the base object,
and the lifecycle gate did not require a resolved Incident and its Postmortem
together. It also noted that a scope migration proves ownership, state, and
identity rather than bytes; that is recorded as accepted residual risk.

Residual risk: moved-document content changes rely on Git diff review;
frozen-generation regressions need the full history CI already fetches
(`fetch-depth: 0`); the fifteen superseded decisions and pre-acceptance
citations enumerated by tsk-0001 remain pending dispositions.

## Traceability

Each work item carries its observed result.

### Lifecycle Traceability

| Criterion / work item                 | Result | Evidence                                            |
| ------------------------------------- | ------ | --------------------------------------------------- |
| [WORK-001](../plan.md#work-breakdown) | Done.  | Registry gate: 778 paths, 0 ambiguous.              |
| [WORK-002](../plan.md#work-breakdown) | Done.  | Profile gate and pre-commit manual stage.           |
| [WORK-003](../plan.md#work-breakdown) | Done.  | Strict profile, link, lifecycle, and archive gates. |
| [WORK-004](../plan.md#work-breakdown) | Done.  | Unit discovery under full QA.                       |
| [WORK-005](../plan.md#work-breakdown) | Done.  | This record.                                        |
