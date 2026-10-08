---
title: "Current Archive and QA Retirement Reappraisal"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0107-TSK-0002"
parent_ids: ["SPEC-0107-PLAN-0001"]
---

# Task: Current Archive and QA Retirement Reappraisal

## Overview

Own the bounded current execution for [WORK-002](../plan.md#work-breakdown)
and [VAL-LOCAL-QA-005](../spec.md#success-criteria--verification-plan).
Inventory actual validation and Archive consumers before any keep, transfer,
retire or protected disposition decision. This is a draft intake, not an
implementation result. [Task 0001](tsk-0001-local-qa-and-release.md) retains
its completed original delivery facts, including its historical failures and
unexecuted checks. The parent Spec and Plan remain completed historical
authority records with this explicitly linked follow-up; no old state is reset.

## Inputs

- Current [Spec](../spec.md), [Plan](../plan.md),
  [quality policy](../../../../.agents/governance/quality.md),
  [validation registry](../../../../scripts/validation/registry.json),
  [Archive router](../../../98.archive/README.md) and
  [Stage 99 Registry](../../../99.templates/registry.json) are the local
  source owners to inspect before an implementation decision.
- F19 is already locally resolved as active RUN-0012 with actual publication
  still separate; this Task does not promote it again. F20's required-check
  migration has a read-back, while HIGH `SEC-P01-001` workflow-control risk
  remains with the security/CI owner. F22 is an unverified whole-call-graph
  inventory, not a proved deletion list. F28 requires current instructions to
  live at current owners and completed facts to retain their original meaning.
- The shared `WGOV-CORE / 3.0.0-draft.3` C06/C09/C11 candidate has proposed
  owner `buenhyden`, proposed Project-Template path
  `.agents/governance/shared-standard.md`, and inspected SHA-256 digest
  `3f46c63daae094649edccec33682ecba99844b184c4b78b558281c7c05ff3271`.
  The digest identifies review content only; final approval, repository
  adoption and joint adoption are not evidenced by it.
- On 2026-10-09, the coordinator reported a read-only remote main
  `5cfd420b723cba7417a0d24c8abb94c4f329caa9` and branch protection
  requiring `ci-summary` and `style-pr` from GitHub Actions/App 15368 with
  strict mode, no `qa-provenance` requirement and no applied branch rules.
  PR 136 at head `a639120b8548f4835a716a082696f01038870d27` had successful
  `ci-summary` and `style-pr` jobs in run 37785109216, including the actual
  lint/format step, on its earlier input. Main's `style-pr` was skipped; the
  absence of classic statuses did not report a failed check. The separate
  GitGuardian/App 46505 success was not a required check. These are intake
  observations, not checks on the future WORK-002 input or independent
  workflow-control proof.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-002 | [VAL-LOCAL-QA-005](../spec.md#success-criteria--verification-plan) | Map current QA and Archive consumers, transfer unique guarantees, retire only proven obsolete surfaces, and record protected disposition separately | platform | frontmatter | NOT_RUN | EVD-P04-001 intake only; implementation and current-input verification pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P04-001 | [VAL-LOCAL-QA-005](../spec.md#success-criteria--verification-plan) | WORK-002 | Read-only owner and follow-up identity inspection | Current SPEC-0106/0107 Spec, Plan, Task paths; Stage 99 modern Task form; F19/F20/F22/F28 and C06/C09/C11 attached review texts; WGOV draft.3 file digest, 2026-10-09 | PASS | This Task Inputs and current 0107 Spec/Plan WORK-002 links; no QA runtime, complete consumer census or disposal proof observed | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LOCAL-QA-005](../spec.md#success-criteria--verification-plan) | pending | EVD-P04-001 | Complete the actual producer/consumer and Archive disposition audit, perform supported local changes and selected checks, then review the changed input; preserve unresolved protected actions with named owners | platform; security/CI operator for SEC-P01-001; Archive owner for any protected whole-unit decision |

## Approval and Safety Boundaries

- **Allowed Paths**: current QA policy, validation Registry and direct
  consumers; current Archive policy/catalog/route metadata and direct
  consumers; this Spec, Plan and Task. Any later implementation path must
  follow an actual owner and consumer audit.
- **Forbidden Paths**: frozen Archive payloads, historical completed Task
  facts, credentials, private or native trust state, live Kubernetes/Vault
  operations and unrelated product implementation.
- **Approval Required**: the persisted user instruction already authorizes
  local P04 audit, reversible implementation, normal commits, local main
  integration and owned branch/worktree cleanup after evidence preservation.
  A whole-unit Archive move or Git-history-only
  deletion needs its actual target, authorizing actor/reference, hold clearance
  and reachable recovery coordinate. Remote protection changes, push/PR,
  release/tag publication and live execution require their separate actual
  authority and inputs. No draft common edition grants these actions.
- **Static Validation**: inspect active registry and callers before selecting
  focused changed-rule negative/boundary regressions, affected purpose and
  document/Archive checks, actual-index style and message checks; record exact
  input, command and result in later evidence rows.
- **Live Validation**: DEFER to the operating owner; no live input or result
  supplied for WORK-002. Prior PR success belongs to a different input.
- **Secret / Vault Handling**: inspect only non-secret source and metadata;
  do not read, print or transmit credentials or Vault data.
- **Rollback Plan**: make forward corrections on the isolated branch while
  preserving historical Task and Archive content; any protected disposition
  requires its own reversible/recovery decision before execution.
- **Evidence Location**: this Task and actual reviewed commits; no second
  progress ledger or fabricated remote result.

## Verification Summary

Only EVD-P04-001's read-only intake mapping is recorded here. The complete
QA leaf/caller/import/discovery/fixture graph, selected local checks,
independent review and any disposition approval are pending. The coordinator
reported that initial Python virtual-environment creation failed because
`ensurepip` was unavailable; an attempt to use `uv` on that partial path
also failed. A new `_workspace/p04-qa-venv` was then created successfully
with `uv 0.12.18`, seeded `pip 26.2.1` and Python 3.12.3, without an apt or
trust-setting change. Selected QA remains unrun on this draft input.
`SEC-P01-001` HIGH stays open with the security/CI operator.
No Archive unit was moved or removed, and no remote or live action was run
by this Task.
