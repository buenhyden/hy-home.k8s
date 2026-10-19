---
title: "Test Module Purpose Gates"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-19"
layer: "specs"
artifact_id: "SPEC-0120"
---

# Test Module Purpose Gates Technical Specification (Spec)

## Overview

[SPEC-0118](../0118-qa-phase-two/spec.md) left 63 of 76 test modules without a
registered gate, so they ran only when a developer ran them by hand. A
read-only scoping review on 2026-10-16 timed every module and mapped each one
to the product it tests. This Spec gives every test module a named purpose
gate that runs when its product or its own file changes. The [Plan](plan.md)
orders the work and [Task 0001](tasks/tsk-0001-test-purpose-gates.md) records
it.

## Strategic Boundaries & Non-goals

- In scope:
  - one table-driven runner, `scripts/run-contract-tests.py --suite <id>`,
    which replaces `run-archive-contract-tests.py` and
    `run-document-contract-tests.py`;
  - a coverage guard: every `tests/test_*.py` belongs to exactly one suite or
    one direct gate, and editing it selects that gate;
  - new suite gates registered in the affected and staged lanes, routed from
    their product and test files;
  - rewriting the one 261-second pass-only link-boundary test on a temporary
    root;
  - widening the timing budgets of the load-sensitive
    `test_run_validation_lane` case.
- Non-goals:
  - change-scoped `reuse` for the slow gates (a later cost decision);
  - splitting `test_archive_validation` by class;
  - the archive validator's handling of the ignored `graphify-out/` paths;
  - any change to `.github/workflows/**` or to product behavior.

## Contracts

- Each test module runs in exactly one gate. The direct gates
  `workspace-memory-regressions` and `git-hook-chain-regressions` keep their
  two modules.
- Editing a test module selects its gate, and editing its product selects it
  where the product has a dedicated surface.
- Slow suites attach only to narrow product surfaces, never to the
  `validation/registry.json` route or to document surfaces.
- Every tracked path still classifies to exactly one surface.
- No gate is weakened. The suites keep the existing archive and document
  modules, and the rewritten link test keeps its placeholder-with-fragment
  behavior check.

## Core Design

A suite is a named tuple of test modules. A validator runs one suite through
the shared runner, so adding a suite is one table row plus one registry entry.
A module that fails to import fails the suite. New surfaces carve exact routes
out of the `scripts` and `tests` catch-alls. A carved script that the broad
gates read keeps the `scripts` validator set.

## Data Modeling & Storage Strategy

Registry and fixture entries only.

## Interfaces & Data Structures

- Runner: `python3 scripts/run-contract-tests.py --root . --suite <id>`.
- Validator IDs: `archive-contract-tests` and `document-contract-tests` keep
  their IDs. New suite gates are `archive-validation-tests`,
  `document-lifecycle-tests`, `validation-routing-tests`, `qa-runner-tests`,
  `ci-metadata-tests`, `release-tests`, `agent-governance-tests`,
  `tooling-tests` and `cluster-gate-tests`.

## Edge Cases & Error Handling

- An unknown suite ID exits non-zero.
- A new test module that no suite names fails the coverage guard.

## Failure Modes & Fallback / Human Escalation

If a suite fails on main for an environmental reason, the Task records the
cause and the owner. The gate is not weakened.

## Verification Commands

- `python3 scripts/run-contract-tests.py --root . --suite <id>` for every
  suite.
- `python -m unittest` on the changed tests and on the registry and selection
  tests.
- `python3 scripts/validate-affected-surfaces.py --root .`.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-PG-001 | The shared runner runs each suite, and the old runners are removed. The coverage guard fails on main and passes after the gates are registered. |
| VAL-PG-002 | The rewritten link test runs in seconds and still fails on a broken placeholder link. The widened lane test passes repeatedly under CPU load. |
| VAL-PG-003 | Every suite gate passes on the branch. The selection tests show each module and product selecting its gate, and the slow gates not selected by registry or document edits. Full-tree classification passes. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PG-001 | Runner execution and coverage guard |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PG-002 | Focused tests |
| [REQ-0003-FR-0016](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PG-003 | Suite runs, selection tests and classification |
