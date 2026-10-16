---
title: "Local QA Phase Two"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0118"
---

# Local QA Phase Two Technical Specification (Spec)

## Overview

[SPEC-0117](../0117-local-qa-rightsizing/spec.md) closed phase one of the
operator's 2026-10-16 local QA review. A read-only scoping review of phase two
found three problems:
- Only 8 of 75 test modules are executed by any registered lane. The four
  modules that broke silently in SPEC-0117 are among the 67 that nothing runs.
- The `scripts` and `tests` catch-all surfaces select gates that cannot be
  affected by most of their paths. Some cluster validators are not selected
  by their own scripts.
- Workflow checks are split across `quality.py` and
  `validate-github-actions-security.py`. Several `quality.py` rules protect
  nothing that a single owner does not already hold.
This Spec owns those repairs. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-qa-phase-two.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - removing dead or duplicated workflow rules from
    `scripts/validation/repository/quality.py`, and moving `timeout-minutes`
    to `scripts/validate-github-actions-security.py`;
  - removing the `.github/zizmor.yml` guard for a file that does not exist;
  - renaming `tests/test_ci_qa_workflow.py` to its current purpose and
    removing its duplicate tests;
  - narrowing the `scripts` and `tests` catch-all surfaces with dedicated
    cluster, archive and tooling script surfaces;
  - a `document-contract-tests` gate for the four lifecycle modules, and
    `test_generic_migration_recovery` in the archive contract runner.
- Non-goals:
  - purpose gates for the other unrun modules (separate Spec);
  - removing `agent-governance` from `scripts`, `.github` or root
    configuration, because its whole-tree retired-token scan reads them;
  - document gates on ordinary prose, which quality policy sanctions;
  - any change to `.github/workflows/**`.

## Contracts

- Each workflow rule has one owner. `validate-github-actions-security.py` owns
  pinning, permissions and `timeout-minutes` for every workflow.
  `validate-ci-python-contract.py` keeps its exact `ci.yml` structure.
- Every tracked path still classifies to exactly one surface. A script with a
  new, unknown name stays on the broad `scripts` catch-all.
- Editing a cluster validator script selects that validator.
- The four lifecycle modules run when their real inputs change: document
  readers, Stage 99 contracts and templates.
- No gate is weakened: zizmor and actionlint stay at the staged boundary, and
  `archive-contract-tests` stays on archive, Stage 99 and `tests` inputs.

## Core Design

New surfaces carve exact or bounded routes out of the catch-all regexes, so
surface exclusivity is preserved. The new gate is a runner script that is a
copy of `scripts/run-archive-contract-tests.py`, because a validator is
identified by its script and the argv grammar rejects `-m`.

## Data Modeling & Storage Strategy

Registry and fixture entries only.

## Interfaces & Data Structures

New validator ID `document-contract-tests`; new surfaces
`cluster-gate-scripts`, `archive-scripts` and `tooling-scripts`. Existing rule
IDs are unchanged.

## Edge Cases & Error Handling

- An unknown new script path stays on `scripts` and keeps the broad gate set.
- A runner whose module fails to import prints FAIL and exits non-zero.

## Failure Modes & Fallback / Human Escalation

If a removal or narrowing cannot name a remaining owner, it is deferred and
the Task records why.

## Verification Commands

- `python -m unittest` on each changed test module and on the registry and
  selection tests.
- `python scripts/validate-affected-surfaces.py --root .` for full-tree
  classification.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-QP2-001 | Workflow rules have one owner each; the security and quality tests pass; the validators pass on the repository. |
| VAL-QP2-002 | The renamed CI metadata test passes, and its duplicate cases are removed without losing behavior coverage. |
| VAL-QP2-003 | Narrowed surfaces classify every tracked path exactly once. Selection tests show the reduced gate sets and the fixed under-selection. |
| VAL-QP2-004 | `document-contract-tests` runs the four lifecycle modules on their inputs. The archive runner includes generic migration recovery. Selection and registry tests pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QP2-001 | Focused tests and staged QA |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QP2-002 | Focused tests and staged QA |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QP2-003 | Selection tests and full-tree classification |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-QP2-004 | Registry and selection tests, runner execution |
