---
title: "Provider README Language and QA Tool Diagnostics"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0110-TSK-0001"
parent_ids: ["SPEC-0110-PLAN-0001"]
---

# Task: Provider README Language and QA Tool Diagnostics

## Overview

Execute the three work units of the [Plan](../plan.md) for
[SPEC-0110](../spec.md) and record their evidence here.

## Inputs

- [SPEC-0110](../spec.md) and its [Plan](../plan.md).
- Operator instruction on 2026-10-13: approve SPEC-0108 and continue with
  the README translations, the SPEC-0109 review and K-P0, K-P3, K-P4 and
  K-P5.
- Branch head `c59940d8` before this package.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PRQA-001](../spec.md#success-criteria--verification-plan) | Translate the eight pending READMEs | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | Missing-tool diagnostics and README sentence | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-PRQA-003](../spec.md#success-criteria--verification-plan) | Record keep decisions for satisfied findings | platform | draft | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-PRQA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Profile validator and staged QA | WORK-001 commit index | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests and staged QA | WORK-002 commit index | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-PRQA-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Keep-decision source review | Current source lines named in the evidence | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-PRQA-001](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-001 checks | platform |
| [VAL-PRQA-002](../spec.md#success-criteria--verification-plan) | pending | none | Run WORK-002 checks | platform |
| [VAL-PRQA-003](../spec.md#success-criteria--verification-plan) | pending | none | Record WORK-003 review | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, `docs/03.specs/README.md`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
  (reciprocal links), the eight READMEs, `docs/99.templates/registry.json`,
  `.secrets.baseline`, `scripts/validate-selected-{style,nonstyle}.py`,
  `scripts/run-validation-lane.py`, `scripts/README.md` and their tests.
- **Forbidden Paths**: `.github/` workflows and rulesets, frozen Archive
  payloads, other Spec packages, live cluster, Vault and secret material.
- **Approval Required**: the operator directed this follow-up on
  2026-10-13; push, pull request, merge and any ruleset change await the
  operator.
- **Static Validation**: focused tests, the profile validator and staged QA
  from the documented validation environment.
- **Live Validation**: DEFER — no live surface is touched; hosted CI is not
  observed.
- **Secret / Vault Handling**: no secret is read or printed.
- **Rollback Plan**: forward revert of the package commits.
- **Evidence Location**: this Task and Git history.

## Verification Summary

Pending execution.
