---
title: "Reference Pack Route Fixtures"
version: "0.2.0"
type: "sdlc/task"
status: "ready"
owner: "platform"
updated: "2026-10-06"
layer: "specs"
artifact_id: "SPEC-0106-TSK-0013"
parent_ids: ["SPEC-0106-PLAN-0001"]
---

# Task: Reference Pack Route Fixtures

## Overview

Correct two obsolete pack-profile expectations while preserving template
selection, numbered member ownership and route/topology refusals.

## Inputs

- [Spec VAL-P02-013](../spec.md#success-criteria--verification-plan) and
  [Plan WORK-013](../plan.md#work-breakdown).
- PR133 run 37403355260 at the completed
  [Task0012](tsk-0012-qa-and-reference-navigation-fixtures.md) endpoint reports
  unit-tests FAIL. Its displayed diagnostic is capped and nonexhaustive.
- The current Registry assigns the three numbered pack READMEs to authored
  reference profiles with unchanged registered templates and publication states.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-013 | [VAL-P02-013](../spec.md#success-criteria--verification-plan) | Align pack route fixture expectations with current owners | platform | frontmatter | NOT_RUN | pending | Pending final-byte and actual-index evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P02-130 | [VAL-P02-013](../spec.md#success-criteria--verification-plan) | WORK-013 | Two named REDs and independent cause audit | Unchanged Task0012 endpoint and declared Stage90 material | FAIL | External `hy-p01-task13-reference-pack-red.receipt.json` and `-red-causes.json`; `/root/p02_independent_review` | rejected |
| EVD-P02-131 | [VAL-P02-013](../spec.md#success-criteria--verification-plan) | WORK-013 | Cached and committed registered-form creation | C012 from unchanged declared regular Task template; target absent before creation | PASS | Ignored `p01-task13-c1-preflight.json`, full metadata and `p01-task13-c1-postcommit.json` | accepted |
| EVD-P02-132 | [VAL-P02-013](../spec.md#success-criteria--verification-plan) | WORK-013 | Observed draft index and exact message with independent raw audit | Draft logical index only; own ready and later checks pending | PASS | External `hy-p01-task13-c1-staged.receipt.json` and `hy-p01-task13-c1-message.receipt.json` | accepted |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0106-stage99-lifecycle-normalization/spec.md`,
  `docs/03.specs/0106-stage99-lifecycle-normalization/plan.md`,
  `docs/03.specs/0106-stage99-lifecycle-normalization/tasks/tsk-0013-reference-pack-route-fixtures.md`,
  `tests/test_reference_pack_routes.py`.
- **Forbidden Paths**: Published Registry, forms, reference material, production
  code, security/gate settings and prior completed evidence.
- **Approval Required**: Persistent scoped shipping authorization covers this
  fixture repair; protected delivery remains subject to exact hosted acceptance.
  Closing requires reviewed prospective completion and fresh actual checks.
- **Static Validation**: Actual registered-form first appearance, pinned
  hook-first checks, two named sixty-second methods, each logical index's
  staged and exact message checks with independent review, then scoped closing.
- **Live Validation**: DEFER; route fixtures provide repository evidence only.
- **Secret / Vault Handling**: No credential access; raw CI diagnostics remain
  private outside tracked content.
- **Rollback Plan**: Reviewed forward correction preserving existing commits.
- **Evidence Location**: This Task records observed outcomes; external raw
  receipts and ignored creation metadata bind their actual inputs.

## Verification Summary

Both named REDs completed with unchanged public inputs, declared reference
inventory, full streams and cleanup. The category test failed all three old
profile equalities before its template assertions. The material test rejected
the current research-pack identity; its exact failing path was NOT_CAPTURED
and later traversal checks were NOT_REACHED. These observations do not establish
an exhaustive hosted failure count or PASS for cases absent from that preview.

Independent review read the entire implicated class and current owners. The
other eight methods retain member, uncovered-route, category-directory,
duplicate/missing/nonregular, index/content drift and historical wiki controls.
Implementation will change only the two expected pack identities and may check
their authored reference lifecycle binding. Two final-byte focused methods,
hooks, own ready/implementation index evidence and terminal checks are
NOT_RUN/pending. No production or reference corpus change is planned.

The draft index passed six fresh canonical gates and its exact configured
message before independent final raw audit and the normal commit. Streams and
cleanup completed with stable inputs/index/refs. Copied message configuration
and captured disposable semantic entries matched; raw disposable index byte
change has an unknown cause and is not an acceptance prerequisite.
Full cached and committed metadata agree on C012 from the registered form,
with unchanged regular source and both bindings, and an absent prior target.

Readiness uses `p01-task13-focused-manifest.json` for the two changed methods
and the actual selector stdout in `p01-task13-selection-observation.json`:
four declared paths, seven validators, unmatched zero, selection only.
No affected validator ran. Own ready staged/message, focused/hooks,
implementation and terminal outcomes remain NOT_RUN/pending.
