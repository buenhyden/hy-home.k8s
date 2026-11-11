---
title: "Package Exit Shape Check Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-11"
layer: "specs"
artifact_id: "SPEC-0159-PLAN-0001"
parent_ids: ["SPEC-0159"]
---

# Package Exit Shape Check Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds three execution constraints. First, no repository file changes outside this package, the Stage 03 README, one back-link sentence in the Traceability section of [REQ-0003](../../01.requirements/0003-workspace-agent-governance-platform.md#traceability), `scripts/document_lifecycle.py`, `scripts/validate-document-lifecycle.py`, `tests/test_document_lifecycle_package_exit.py`, `scripts/run-contract-tests.py`, one exact route in `scripts/validation/registry.json`, a new proposed `docs/02.architecture/decisions/0057-package-exit-shape-check.md` with the decisions README entry and, once the user accepts it, one entry in the AD-0006 decision list with its patch `version` bump and `updated` date, one sentence in `.agents/governance/document-lifecycle.md` with its patch `version` bump and `updated` date, rule 7 of `docs/03.specs/AGENTS.md`, and `.secrets.baseline` entries marking this Task's reviewed SHA-256 document digests as non-secret. Second, every test fixture is an isolated temporary Git repository outside the working tree. Third, the rule, its wiring, the policy sentence and rule 7 are committed only after the user accepts ADR-0057, so that no commit enforces or states a rule the accepted decisions do not yet allow.

## Overview

Add the `LIFECYCLE-PACKAGE-EXIT` rule defined in [SPEC-0159](spec.md). [Task 0001](tasks/tsk-0001-package-exit-shape-check.md) owns execution evidence and criterion acceptance.

## Context

The W02 intake on 2026-11-11 found ARC-02 open. The user chose an event-scoped rule over a presence gate or no check, and authorized the exit of SPEC-0154 to SPEC-0158, which commits `a6f44976` (freeze) and `c8a891fb` (closure) carried out by hand on branch `claude/w02-package-exit`. That closure is the shape this rule admits. [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) and accepted [ADR-0056](../../02.architecture/decisions/0056-manual-document-disposition-review.md) constrain the design; ADR-0057 amends ADR-0056 Decision 6 for this rule only.

## Goals & In-Scope

- Write failing tests first on isolated fixtures, then the rule and its staged wiring, and register and route the module.
- Draft ADR-0057 as proposed and add it to the decisions README; the user decides acceptance.
- State the rule in the lifecycle policy and update `docs/03.specs/AGENTS.md` rule 7.
- Add this package to the Stage 03 README and link it from REQ-0003 Traceability.

## Non-Goals & Out-of-Scope

- CI or explicit-ref coverage, per-commit replay, presence or age checks, deferral markers, recovery-proof parsing and archive reads.
- Registry schema, Stage 99 forms and any other governance text.
- Any push, PR, merge or package exit without separate user approval.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-EXIT-001](spec.md#success-criteria--verification-plan) | Write the focused tests, see them fail, implement and wire the rule, see them pass, register the module. | Approved Spec and Plan. | [Task 0001](tasks/tsk-0001-package-exit-shape-check.md) | `python3 -m unittest tests.test_document_lifecycle_package_exit`, RED then GREEN. |
| WORK-002 | [VAL-EXIT-002](spec.md#success-criteria--verification-plan), [VAL-EXIT-003](spec.md#success-criteria--verification-plan) | Run the lifecycle suites; write ADR-0057, the policy sentence and rule 7; obtain independent review and the user's ADR decision; run commit checks. | WORK-001. | [Task 0001](tasks/tsk-0001-package-exit-shape-check.md) | Suites, independent review, strict document checks and commit hooks. |

## Verification Plan

- Focused tests fail before the implementation and pass after it, covering R1 to R4 and the three admitted shapes.
- `python3 scripts/run-contract-tests.py --root . --suite document-lifecycle` stays green.
- An independent read-only reviewer checks the code, tests, ADR-0057, policy sentence and rule 7.
- Strict document checks, the staged lifecycle check and the active commit hooks run on the exact index.
- Architecture compliance: ADR-0056 is not edited; ADR-0057 is the only architecture change and stays proposed until the user accepts it.

## Risks & Mitigations

- **A legitimate change is refused.** Mitigation: the admitted shapes are tested, including the `c8a891fb` closure shape; a refusal returns to Spec review.
- **Staged-only coverage is bypassed by a commit without hooks.** Mitigation: stated as a limit; replay coverage is left to W05.

## Completion Criteria

All three criteria need observed PASS evidence, no unresolved required failure, an independent review with no blocking finding, the user's decision on ADR-0057, and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| A Stage 03 package leaves the tree only whole, finished and named in Archived Lineage, checked at staged commit | [Document lifecycle policy](../../../.agents/governance/document-lifecycle.md) | Validation and Refresh, enforced by `LIFECYCLE-PACKAGE-EXIT` |
