---
title: "Evaluation owner cutover"
version: "0.1.2"
type: "sdlc/task"
status: "completed"
owner: "platform"
updated: "2026-09-29"
layer: "specs"
artifact_id: "SPEC-0102-TSK-0007"
---

# Task: Evaluation owner cutover

## Overview

Execute WP-006 of the approved [Plan](../plan.md). The request owner approved
the Spec and ADR, then approved Plan execution on 2026-09-29.
The current session implements this bounded unit under its assigned role;
the final branch receives independent review.

## Inputs

- [Spec](../spec.md)
- [Plan and work breakdown](../plan.md#work-breakdown)
- [ADR-0047](../../../02.architecture/decisions/0047-agent-contract-and-resource-ownership.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-007 | VAL-ACS-032 | WP-006: Evaluation owner cutover | platform | Completed | 19-case parity, 12 negatives and 15 exact-index gates passed | This Task |

## Approval and Safety Boundaries

- **Allowed Paths**: exact files and owner delegation in WP-006 of the linked Plan; this Task
- **Forbidden Paths**: retained historical bodies, personal/global configuration, credentials, live resources, unrelated changes
- **Approval Required**: Plan execution and logical local commits approved; push, PR, merge, live changes and governance-steward self-entry remain separately operator-owned
- **Static Validation**: Plan command set C6, affected QA, exact-index staged QA, normal Git hooks; final full QA in TSK-0008
- **Live Validation**: DEFER; no authorized runtime session
- **Secret / Vault Handling**: no secret values read, printed or retained
- **Rollback Plan**: reverse this unit's reviewed logical commit together with its consumers, after dependent changes are reversed; preserve unrelated work
- **Evidence Location**: this Task

## Verification Summary

Owner presence test failed before relocation, as expected. Branch `codex/agent-contracts`, initial base
`efc3643fdce17e0c5f454c3046e7ec8a3c37d13d`. Next owner: the assigned
Plan implementer, followed by independent branch review. Static evidence
never establishes hosted, provider, account-limit or live behavior.

### Cutover evidence

The owner-presence regression failed before the move. The corpus and dedicated
runner now live in `.agents/evaluations/`; root `evals/` and the old runner are
absent. All 19 original expectation sets and 12 negative cases are preserved.
Recorded synthetic text is data; it is never dispatched to a tool or provider.
The central registry still selects the gate and common bounded I/O remains in
`scripts/`. Native execution and model-quality claims remain DEFER.

C6 plus governance/reference regressions: 118 tests passed (exit 0). The new
runner returned exit 0 with 19 synthetic, 0 recorded, 12 negative cases. An
additional missing evaluation-command reference test first failed RED, then
passed after the shared current-reference matcher admitted the new owner.
The frozen archive-generation equality test first failed; its derivation now
reverses SPEC-0102's later skill profile additions while preserving the original
historical route and asserting byte equality with the frozen Git object.

The first affected QA rejected the deleted `evals/README.md` as unmatched.
The central surface now classifies both retired-path deletions and new paths;
this is deletion routing, not a live compatibility runner or duplicate corpus.
Affected QA then exposed the document/data boundary: newly located response
Markdown was entering current document routing and exact renames from the old,
unmanaged root lacked a base document blob. The shared document inventory and
lifecycle scope now exclude only evaluation responses; the grader still checks
those inputs. Cross-scope renames become additions or deletions in the managed
scope. The new owner README is English as required for `.agents/`. Dedicated
regressions cover data exclusion and both rename directions. The historical
response bodies remain byte-identical. A direct link check on an unstaged
registry refused index/worktree drift as designed; staged QA uses one snapshot.
Affected/staged QA is rerun on the corrected contracts.

Final cutover evidence: `python3 scripts/qa.py staged` returned 0 with all
15 selected gates PASS over 104 changed paths. Commit `c80fd050` records the
reviewed implementation and final repairs after actual-message Commitizen
validation and the normal hook chain. Its tree is
`f313097650d0429054307e7d47ca2690273b5346`. The final full run uses these same
implementation bytes; final evidence and limitations belong to TSK-0008.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-007](../plan.md#work-breakdown) | Completed | Frozen 19 expectation sets preserved; 15 staged gates passed; commit `c80fd050` |
