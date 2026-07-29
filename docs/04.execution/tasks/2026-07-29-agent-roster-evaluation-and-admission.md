---
title: 'Task: Agent Roster Evaluation and Admission'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-29
---

# Task: Agent Roster Evaluation and Admission

## Overview

This Task tracks the executable Spec 044 work stream that projects the
repository-static AI Agent roster from the completed 10-role / 3-surface
baseline to a validated 12-role / 4-surface / 48-adapter current tracked
inventory. Provider/model evidence remains fixed at the Spec 042
`2026-07-10 10:00 Asia/Seoul` cutoff. The AREA-002 projection keeps admission
`DEFER` and does not claim provider discovery, model resolution, or execution;
AREA-003 owns the evidence required for final roster admission.

## Inputs

- Parent Spec:
  [Spec 044](../../03.specs/044-agent-roster-evaluation-and-admission/spec.md)
- Parent Plan:
  [Agent Roster Evaluation and Admission Implementation Plan](../plans/2026-07-29-agent-roster-evaluation-and-admission.md)
- Predecessor evidence: completed Specs 041 through 043, culminating in the
  observed Spec 043 closure and postflight commits below
- Current machine owner:
  [harness-contract.json](../../00.agent-governance/contracts/harness-contract.json)
- Observed prerequisite commits: Spec 043 closure
  `a0bc3565988e291980320dec8442405c7ef16eb6` and postflight
  `80ffd6d92a53990b04e413c0acf7fbc879b437d4`
- Observed Spec 044 commits: activation
  `b8b1a3884f9948fcd4ac2aecc89ea727118ad787`, activation postflight
  `6d9b01d51f8a198c521621bcd52ff088c397ee0b`, and AREA-001 implementation
  `0129daf7d44c9308bcad63d4966e11ffa98d05af`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AREA-000 | VAL-AREA-001 | Activate reciprocal Spec/Plan/Task path and registry relation | platform | Done | Activation and clean-tree postflight committed | `b8b1a3884f9948fcd4ac2aecc89ea727118ad787`; `6d9b01d51f8a198c521621bcd52ff088c397ee0b` |
| AREA-001 | VAL-AREA-001..008 | Implement closed admission, evaluation, and model-fitness schemas, validators, and synthetic negative fixtures before promotion | platform | Done | Closed gates preserve current `10/3/30`, target-only `12/4/48`, and all promotion/runtime lanes as `DEFER` | `0129daf7d44c9308bcad63d4966e11ffa98d05af`; focused `119`, aggregate/all-files PASS |
| AREA-002 | VAL-AREA-001..004 | Project `docs-researcher` and `quality-engineer` with the exact 12/4/48 repository-static roster and native projections | platform | In progress | Exact tracked projection is staged with admission `DEFER`; review remediation remains open | `138ce6ac28aa0eebac2b0295e4c50fd78d594db6`; harness contract, 48 adapter files, projection decisions, and set-equality evidence |
| AREA-003 | VAL-AREA-005, VAL-AREA-006 | Implement versioned four-class role evaluation coverage, independent adjudication, rollback records, and final admission decision | platform | Queued | Not executed | Evaluation manifests/corpora, validator, fixtures, reviewed decisions, and final admission evidence |
| AREA-004 | VAL-AREA-006..008 | Reconcile fixed cutoff and implement risk-based provider candidate model/effort fitness without runtime preclaim | platform | Queued | Not executed | Model-fitness map, baseline/threshold/fallback records, validator, fixtures, and provider evidence links |
| AREA-005 | VAL-AREA-001..008 | Reconcile catalogs, provider notes, QA, and closure | platform | Queued | Not executed | aggregate/all-files/review/closure evidence |

## Approval and Safety Boundaries

- **Allowed Paths**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.agents/**`,
  `.claude/**`, `.codex/**`, `.gemini/**`,
  `docs/00.agent-governance/**`, `docs/03.specs/**`,
  `docs/04.execution/**`, `docs/99.templates/support/document-profiles.json`,
  `scripts/**`, `tests/**`
- **Forbidden Paths**: credentials, auth caches, shell history, Vault/ESO
  values, live Kubernetes/GitOps state, provider account state, and
  `.agent-work/checkpoint.json`
- **Approval Required**: provider login, authenticated provider run, remote
  GitHub mutation, workflow/CI change, live cluster mutation, or credential
  changes
- **Static Validation**: focused Spec 044 validators, existing harness
  validators, lifecycle, strict registry, aggregate, all-files pre-commit, and
  diff checks
- **Live Validation**: `DEFER`; no live provider or cluster operation is
  authorized for this task
- **Secret / Vault Handling**: no secret reads, no secret prints, no credential
  fixture values, synthetic/redacted fixtures only
- **Rollback Plan**: revert the newest AREA unit in reverse dependency order;
  restore the last verified 10/3/30 current inventory if admission fails, and
  revert AREA-000 last without resetting or overwriting unrelated work
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`

## Verification Summary

AREA-000 and AREA-001 are complete. AREA-001 added three closed machine
contracts, schemas, validators, synthetic fixtures, focused tests, harness
consumer registration, affected-surface routing, aggregate invocation, and
exact helper admission. Focused tests `119`, helper audit `59/33/26`,
affected surfaces `21/21` with `19` validators, staged and clean-tree
repository aggregate, and staged and clean-tree all-files pre-commit passed.

AREA-002 commit `138ce6ac` materializes exact 12-role / 4-surface / 48-adapter
tracked set equality. Its corrected lifecycle result is
`repository-static-projected` / `DEFER`: the two candidates are projected, not
finally admitted. AREA-003 still owns versioned four-class evaluation,
independent adjudication, and rollback evidence. The provider/model cutoff
remains `2026-07-10 10:00 Asia/Seoul`; runtime, provider
discovery/authentication, model resolution, agent evaluation, model fitness,
hosted CI, remote, live, and ignored checkpoint execution remain `DEFER`.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AREA-000](../plans/2026-07-29-agent-roster-evaluation-and-admission.md#work-breakdown) | Done | Activation `b8b1a388` and clean-tree postflight `6d9b01d5`. |
| [AREA-001](../../03.specs/044-agent-roster-evaluation-and-admission/spec.md#success-criteria--verification-plan) | Done | Closed admission/evaluation/model-fitness gates and postflight evidence in `0129daf7`; requirements `COMPLIANT`, security/model-path review `APPROVED`. |
| N/A — AREA-002 shares the Plan source above | In progress | Commit `138ce6ac` projects exact 12/4/48 repository-static inventory; admission remains `DEFER` while review remediation is open. |
| N/A — AREA-003 shares the Plan source above | Not executed | Pending versioned evaluation, independent adjudication, rollback, and final admission evidence. |
| N/A — AREA-004 shares the Plan source above | Not executed | Pending fixed-cutoff candidate model/effort fitness evidence; runtime resolution remains `DEFER`. |
| N/A — AREA-005 shares the Plan source above | Not executed | Pending QA and independent review. |
