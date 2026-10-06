---
title: "Reference Pack Route Fixtures"
version: "1.0.0"
type: "sdlc/task"
status: "in-progress"
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
| EVD-P02-132 | [VAL-P02-013](../spec.md#success-criteria--verification-plan) | WORK-013 | Observed draft/ready indices and exact messages with independent raw audits | Two accepted logical indices only; own implementation and terminal checks pending | PASS | External `hy-p01-task13-c1-staged.receipt.json`, `hy-p01-task13-c2-staged.receipt.json` and corresponding message receipts | accepted |
| EVD-P02-133 | [VAL-P02-013](../spec.md#success-criteria--verification-plan) | WORK-013 | Two final-byte focused methods, pinned hooks and independent raw audits | Tested pack-route fixture and complete declared public inputs/reference inventory | PASS | External `hy-p01-task13-focused.receipt.json` and `hy-p01-task13-hooks.receipt.json` | accepted |

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
Implementation changes only the two expected pack identities and checks their
authored reference lifecycle binding. Own implementation-index, whole Work
and terminal acceptance remain NOT_RUN/pending. Production and reference
corpus bytes are unchanged.

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
No affected validator ran. The ready index then separately passed six fresh
canonical gates and its exact configured message with independent final raw
audit, complete streams/cleanup and stable source/index/refs. EVD-P02-132
accepts these observed draft/ready results only.

Final fixture SHA256
`b7870c447fe3711ae58e7f510b2f21a101ef844af9596a0eb96cef31839acd0d`
passed the three pinned scoped hooks without formatter delta before two fresh
named methods passed within their sixty-second bounds. Independent direct
audits accepted hook receipt SHA256
`b8bb84a7d85f03b9c3b2f0783ad0bd023a283b0d1e1a3c43158b816a8ca4361e`
and focused receipt SHA256
`5c8aecef2e362fbe2e36f3d86944fc8767700a41e6acd1e1f4aaf2bc53d6656b`.
The complete declared input maps, reference inventory and template facts
matched in both lanes. Template selection, authored reference publication
binding and the actual material iteration now passed; earlier RED's unreached
checks remain historical. The other eight unchanged methods were not rerun.

This in-progress candidate accepts only focused/hooks and prior draft/ready
observations. Its own implementation Markdown, staged/message checks and
independent final review remain NOT_RUN/pending before the normal commit.
Work completion, scoped terminal checks and hosted admission remain separate.
