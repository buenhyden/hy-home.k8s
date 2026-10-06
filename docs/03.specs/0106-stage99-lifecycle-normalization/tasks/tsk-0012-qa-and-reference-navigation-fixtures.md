---
title: "QA and Reference Navigation Fixtures"
version: "0.1.1"
type: "sdlc/task"
status: "ready"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0012"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: QA and Reference Navigation Fixtures

## Overview

Repair the synthetic platform report and reference navigation prerequisites
without changing their execution, reuse or navigation refusals.

## Inputs

- [Spec VAL-P02-012](../spec.md#success-criteria--verification-plan) and
  [Plan WORK-012](../plan.md#work-breakdown).
- PR133 run 37395364180 at the accepted
  [Task0011](tsk-0011-authority-lifecycle-state-fixtures.md) endpoint: unit-tests
  failed while document-lifecycle and pre-commit reported PASS. Its displayed
  preview is capped; no retained exhaustive failure artifact exists.
- Independent review confirms the synthetic report version prerequisite and
  current reference pack/collection declarations. The knowledge collection
  shares the same section prerequisite.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-012 | [VAL-P02-012](../spec.md#success-criteria--verification-plan) | Correct bounded QA and navigation fixture prerequisites | platform | frontmatter | NOT_RUN | pending | Implementation evidence pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-120 | [VAL-P02-012](../spec.md#success-criteria--verification-plan) | WORK-012 | Three bounded REDs and independent cause audit | Unchanged accepted Task0011 endpoint | FAIL | External `hy-p01-cc3e3633-named-red.receipt.json` and `.causes.json`; `/root/p02_independent_review` | rejected |
| EVD-P02-122 | [VAL-P02-012](../spec.md#success-criteria--verification-plan) | WORK-012 | Observed draft index and exact message checks with final independent audit | Accepted draft index only; own ready checks pending | PASS | External `hy-p01-task12-c1-staged.receipt.json` and `hy-p01-task12-c1-message.receipt.json` | accepted |
| EVD-P02-124 | [VAL-P02-012](../spec.md#success-criteria--verification-plan) | WORK-012 | Cached and committed registered-form first appearance | C012 from unchanged declared regular template; target absent before creation | PASS | Ignored `p01-task12-c1-preflight.json`, full NUL metadata and `p01-task12-c1-postcommit.json` | accepted |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0106-stage99-lifecycle-normalization/spec.md`,
  `docs/03.specs/0106-stage99-lifecycle-normalization/plan.md`,
  `docs/03.specs/0106-stage99-lifecycle-normalization/tasks/tsk-0012-qa-and-reference-navigation-fixtures.md`,
  `tests/test_qa_runner.py`, `tests/test_readme_navigation.py`.
- **Forbidden Paths**: Production code, published Registry/schema, security
  settings, completed evidence and unrelated files.
- **Approval Required**: Existing scoped shipping permission covers this repair;
  conditional closing still requires prospective review/completion and fresh
  actual checks plus independent review. Protected merges require hosted acceptance.
- **Static Validation**: Four named sixty-second methods, pinned scoped hooks
  before final-byte GREEN, creation metadata and every logical index's fresh
  staged/message checks and separate review. No repository full/affected run.
- **Live Validation**: DEFER; this is offline fixture evidence.
- **Secret / Vault Handling**: Public inputs only; private raw diagnostics remain
  outside tracked source and no credentials are read.
- **Rollback Plan**: Reviewed forward correction with prior commits retained.
- **Evidence Location**: This Task records outcomes; external raw receipts and
  ignored proposal scratch retain exact inputs without future self-identities.

## Verification Summary

Three REDs terminated within sixty seconds with unchanged inputs and complete
cleanup. The report version violates the static version-2 owner prerequisite;
redirected internal gate output was NOT_CAPTURED and later CI variants were
NOT_RUN after the first full assertion. Collection and pack results reflect
their stale heading/profile. GREEN must observe the existing synthetic full/CI
gate counts, deliberate failure, interception and no-reuse assertions. Navigation
must preserve depth refusal and meaningful missing-member/valid controls.

The draft index passed six fresh canonical gates and its exact configured
message. Independent final raw audit preceded the normal draft commit; streams
and cleanup completed with stable source/index/refs. Copied message configs and
captured disposable semantic entries matched; changed raw disposable index
bytes have an unknown cause and were not an acceptance prerequisite.

Cached and committed full Git metadata identify C012 from the registered Task
form, with equal declared bindings and unchanged regular source before/after
creation. The prior target was absent. Readiness uses ignored
`p01-task12-focused-manifest.json` for four existing methods and
`p01-task12-selection.json` for five paths: seven validators, unmatched zero,
selection only. Its observation records copied tool stdout and the absence of
an originally redirected raw file; no selection or validator rerun is claimed.
Selected gates use their existing commands/budgets. Python hooks are separate
because the staged profile does not include the pre-commit gate.

Own ready, focused implementation and terminal checks are NOT_RUN/pending.
An isolated terminal proposal requires completion and review; its reflected
actual index requires fresh staged/completion/message and final review before
commit. Local outcomes do not establish hosted or integrated-main acceptance.
