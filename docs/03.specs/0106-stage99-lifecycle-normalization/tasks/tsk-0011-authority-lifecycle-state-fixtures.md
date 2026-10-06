---
title: "Authority Lifecycle State Fixtures"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0011"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Authority Lifecycle State Fixtures

## Overview

Adjust three test prerequisites to the published role vocabularies. The required
body-maintenance and reciprocal-evidence behavior is unchanged.

## Inputs

- [Spec VAL-P02-011](../spec.md#success-criteria--verification-plan) and
  [Plan WORK-011](../plan.md#work-breakdown).
- The accepted [Task0010](tsk-0010-completed-state-and-navigation-fixtures.md)
  endpoint and the next executed PR133 run 37387514174, failed job 112024384725.
  Unit-tests failed; document-lifecycle and pre-commit reported PASS. The displayed
  preview is capped and supplies no exhaustive unittest summary.
- Independent review read all twelve methods in the implicated authority class.
  Three named REDs confirm invalid Spec active prerequisites and a reference
  completed state wrongly expected to exercise noninitial publication.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-011 | [VAL-P02-011](../spec.md#success-criteria--verification-plan) | Align authority state fixtures with their published roles | platform | frontmatter | NOT_RUN | pending | Implementation has not started |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-110 | [VAL-P02-011](../spec.md#success-criteria--verification-plan) | WORK-011 | Three named REDs and independent diagnosis | Unchanged Task0010 endpoint; bounded individual invocations | FAIL | External `hy-p01-7959d52f-named-red.receipt.json` and causes receipt; `/root/p02_independent_review` | rejected |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0106-stage99-lifecycle-normalization/spec.md`,
  `docs/03.specs/0106-stage99-lifecycle-normalization/plan.md`,
  `docs/03.specs/0106-stage99-lifecycle-normalization/tasks/tsk-0011-authority-lifecycle-state-fixtures.md`,
  `tests/test_document_lifecycle_archive_cutover.py`.
- **Forbidden Paths**: Every production contract, security/trust setting,
  frozen Archive unit, completed document and unrelated file.
- **Approval Required**: The explicit commit/push/merge request and scoped
  four-path delegation cover these fixtures. Existing conditional closing
  permission requires prospective review/completion followed by actual checks
  and separate final review before commit. Hosted protection still governs merges.
- **Static Validation**: Three existing named methods with current-state,
  publication and reciprocal boundaries, each within sixty seconds; scoped
  pinned hooks; fresh staged and exact message checks plus independent review
  for every logical index. Local full/affected execution is excluded.
- **Live Validation**: DEFER; repository evidence does not establish live readiness.
- **Secret / Vault Handling**: Public fixture inputs only; retain raw CI diagnostics
  privately and report safe classifications without credential access.
- **Rollback Plan**: A reviewed forward correction preserves the existing history;
  destructive Git operations and provenance exceptions are outside this Task.
- **Evidence Location**: Execution facts belong here. External raw receipts and
  ignored proposal scratch retain tested identities without embedding this
  document's own future commit identity.

## Verification Summary

The intake establishes three prerequisite failures, not a production defect.
Keep maintenance at draft/in-progress/completed, audit draft admission with
active/completed STATE and published CREATE refusals, and approved supersession
with missing EVIDENCE versus exact reciprocal acceptance.

The first uncommitted draft's actual source metadata was C012 from Task0010 and
did not qualify as registered-form creation. Its bytes and preflight remain in
ignored `p01-task11-c1-ordinary-copy-candidate.md` and
`p01-task11-c1-creation-preflight.json`. This replacement uses the canonical form
with concise intake facts; its actual origin still needs inspection.

Draft/ready/implementation and terminal results remain unobserved. An isolated
completion proposal and its review precede any closing reflection; that reflected
index needs fresh staged, completion, exact message and final independent review
before its normal commit. Final hosted PR and integrated-main results remain
separate from every local observation.
