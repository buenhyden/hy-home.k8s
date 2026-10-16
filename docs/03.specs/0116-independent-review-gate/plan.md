---
title: "Independent Review Merge Gate Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0116-PLAN-0001"
parent_ids: ["SPEC-0116"]
---

# Independent Review Merge Gate Implementation Plan

## Global Constraints

- Every work unit inherits the [Spec](spec.md) contracts and non-goals: no AI
  model API, no hosted reviewer workflow, and no review credential in GitHub.
- Remote changes (App creation, installation, protection update) are operator
  actions or need the operator's exact approval with before/after read-back.

## Overview

This plan executes [SPEC-0116](spec.md) on branch
`codex/evd-012-independent-review` from main `26508fe2`.

## Context

The research (Task EVD-001) found that the ruleset "require workflows"
rule is documented for organizations only, that GitHub App reviews and Copilot
reviews do not reliably count toward required approvals, and that a check
bound to an App ID other than `15368` can only be produced with that App's
credential. The operator chose the review App and check-run route and excluded
model API use.

## Goals & In-Scope

Close VAL-IR-001 to VAL-IR-004.

## Non-Goals & Out-of-Scope

The non-goals listed in the Spec.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-IR-001](spec.md#success-criteria--verification-plan) | Publisher script and focused tests | None | [Task](tasks/tsk-0001-independent-review-gate.md) | Unit tests, Ruff, staged QA, independent review |
| WORK-002 | [VAL-IR-002](spec.md#success-criteria--verification-plan) | RUN-0013 and README routes | WORK-001 | [Task](tasks/tsk-0001-independent-review-gate.md) | Selected document checks and independent review |
| WORK-003 | [VAL-IR-003](spec.md#success-criteria--verification-plan) | Operator creates and installs the review App; first check run on this package's PR | WORK-002 | [Task](tasks/tsk-0001-independent-review-gate.md) | Observed check run App ID and installation scope |
| WORK-004 | [VAL-IR-004](spec.md#success-criteria--verification-plan) | Require the check in main protection and record the EVD-012 disposition | WORK-003 | [Task](tasks/tsk-0001-independent-review-gate.md) | Protection read-back and observed blocked/mergeable states |

## Verification Plan

WORK-001 runs `tests/test_independent_review.py`, Ruff and `qa.py staged`
on the exact index. WORK-002 runs the selected Markdown, link and lifecycle
checks. WORK-003 and WORK-004 are remote observations recorded with their
time, account and fields; repository QA does not stand in for them.

## Risks & Mitigations

- The new required check blocks every merge if the App or key breaks: the
  runbook names recovery, and the protection change happens only after a
  successful check run has been observed.
- A check run published for a stale head: the publisher refuses unless the
  verdict SHA equals the PR's current head; a later push leaves the new head
  without the check.
- A pull request that edits the publisher to force success or leak the key:
  the publisher runs only from the `origin/main` copy, with this package's PR
  as the stated bootstrap exception.
- The author session runs the reviewer itself: the runbook requires a fresh
  reviewer session with a read-only role; this remains procedural and is
  recorded as residual risk.

## Completion Criteria

All four criteria have PASS evidence and an accepted decision in the Task;
push, pull request and merge remain operator-requested actions.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| none | none | No durable contract was introduced |
