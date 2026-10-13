---
title: "SDLC Document Sync and Remaining v9 Gaps"
version: "0.1.0"
type: "sdlc/spec"
status: "in-review"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0113"
---

# SDLC Document Sync and Remaining v9 Gaps Technical Specification (Spec)

## Overview

An operator review on 2026-10-13 found two problems. First, the
requirements, architecture and Spec documents were not fully updated after
SPEC-0108 to SPEC-0112. Second, the earlier keep decisions for F02, F05,
F18, F22 and F39 in
[SPEC-0110](../0110-provider-readme-and-qa-diagnostics/spec.md) did not
follow every instruction of the v9 prompt. Three read-only investigations
on main `86daf815` found the stale text and the narrow gaps that this
package closes. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-sdlc-sync-and-v9-gaps.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - the stale SPEC-0109 body;
  - the memory store in AD-0006;
  - REQ-0003 metadata, prose and missing link cells;
  - successor notes in SPEC-0106 and SPEC-0108 and a clarification in ADR-0036;
  - post-merge dispositions in the SPEC-0108 to SPEC-0112 Tasks;
  - F22 frozen-exclusion cross-checks and a fix recipe;
  - F05 claim statuses;
  - the F18 evidence correction;
  - the F39 stale route;
  - the F02 gateway section order.
- Non-goals:
  - generating the pre-commit configuration;
  - a Stage 99 schema change;
  - moving Codex reads out of `AGENTS.md`, because Codex has no verified loader for a second file;
  - the sibling-repository Docker comparison;
  - rewriting the history of completed packages.

## Contracts

- A current owner never states a pre-implementation state that later work
  replaced. A completed package keeps its history and gains only a dated
  successor note.
- The pre-commit frozen-Archive exclusion stays the authoring source. A
  test fails when its sealed migration list or the markdownlint ignores
  differ from what the Registry declares.
- The Stage 99 README states separately the approval, the original-source
  verification, the local acceptance and the four-repository adoption of
  `WGOV-CORE / 3.0.0`, each with its evidence or an explicit unverified
  status.
- Notification workflow success is never QA evidence.
- `AGENTS.md` lists the common core first and the Codex-only reads in a
  labelled block, keeping the validated reference set.

## Core Design

Every change is a document correction or a test assertion. The F22 test
compares the `0001` to `00NN` migration alternation in `.pre-commit-config.yaml`
with the `archive/migration` profile `path_pattern` list in
`docs/99.templates/registry.json`. It also compares the markdownlint
`ignores` with the retention-class directories plus `migrations/` and the
two harness globs. F39 removes the `.hadolint.yaml` route, whose file was
deleted in `1014bba7` and which no other consumer names.

## Data Modeling & Storage Strategy

No stored data changes.

## Interfaces & Data Structures

- A new test in `tests/test_validation_tooling_ownership.py`.
- `scripts/README.md`: a copyable explicit fix command.

## Edge Cases & Error Handling

If a body edit of an approved or completed document is rejected by the
lifecycle validator, the note moves to the nearest current owner instead.
The Task records that move.

## Failure Modes & Fallback / Human Escalation

Rollback is a forward revert of the package commits.

## Verification Commands

- `python3 -m unittest tests.test_validation_tooling_ownership tests.test_agent_governance`
  from the documented validation environment.
- `"$VALIDATION_VENV/bin/python" scripts/qa.py staged` per logical commit.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-SYNC-001 | The audited stale statements in REQ-0003, AD-0006, ADR-0036 and SPEC-0106, SPEC-0108 and SPEC-0109 are corrected or annotated, the Tasks record their merge, and the profile, link and lifecycle validators pass. |
| VAL-SYNC-002 | A new test fails on a sealed migration missing from the pre-commit exclusion or a changed markdownlint ignore, and passes on the current files; the fix recipe is documented. |
| VAL-SYNC-003 | The Stage 99 README names a status and evidence location for each of the four F05 claims. |
| VAL-SYNC-004 | The SPEC-0110 Task records that the `greeting` and `label` results are not QA evidence. |
| VAL-SYNC-005 | The `.hadolint.yaml` route is gone and the validation registry tests pass. |
| VAL-SYNC-006 | `AGENTS.md` shows a common block and a labelled Codex-only block, and the governance validator and tests pass unchanged. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SYNC-001 | Each document keeps its purpose and current state; document validators. |
| [REQ-0003-FR-0028](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SYNC-002 | Deterministic negative test for exclusion drift. |
| [REQ-0003-FR-0026](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SYNC-003 | Approval, source, local and cross-repository evidence kept apart. |
| [REQ-0003-FR-0017](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SYNC-004 | Hosted results never certify local QA. |
| [REQ-0003-IF-0001](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SYNC-005 | No orphan route on an active surface. |
| [REQ-0003-FR-0002](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SYNC-006 | Thin provider gateway boundary; governance validator. |
