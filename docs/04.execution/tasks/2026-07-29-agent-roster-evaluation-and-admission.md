---
title: 'Task: Agent Roster Evaluation and Admission'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-29
---

# Task: Agent Roster Evaluation and Admission

## Overview

This Task tracks the executable Spec 044 work stream that promotes the
repository-static AI Agent roster from the completed 10-role / 3-surface
baseline to a validated 12-role / 4-surface / 48-adapter current inventory.
Provider/model evidence remains fixed at the Spec 042
`2026-07-10 10:00 Asia/Seoul` cutoff, and repository-static promotion does not
claim provider discovery, model resolution, or execution.

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

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AREA-000 | VAL-AREA-001 | Activate reciprocal Spec/Plan/Task path and registry relation | platform | In Progress | Activation proposal staged in this task stream | Spec/Plan/Task/index/registry/progress diff |
| AREA-001 | VAL-AREA-001..008 | Implement closed admission, evaluation, and model-fitness schemas, validators, and synthetic negative fixtures before promotion | platform | Queued | Not executed | Three focused validators, schemas/contracts, fixtures, and unit tests |
| AREA-002 | VAL-AREA-001..004 | Admit `docs-researcher` and `quality-engineer`; promote exact 12/4/48 repository-static roster and native projections | platform | Queued | Not executed | Harness contract, 48 adapter files, admission decisions, and set-equality evidence |
| AREA-003 | VAL-AREA-005, VAL-AREA-006 | Implement versioned four-class role evaluation coverage, independent adjudication, and rollback records | platform | Queued | Not executed | Evaluation manifests/corpora, validator, fixtures, and reviewed decisions |
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

AREA-000 is the only active work item. The exact-eight activation proposal does
not change adapters, contracts, validators, models, provider settings,
workflow/CI, runtime, remote, live, or ignored checkpoint state and does not
claim future validation or commit results.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AREA-000](../plans/2026-07-29-agent-roster-evaluation-and-admission.md#work-breakdown) | In Progress | Activation diff and validation will be recorded before commit. |
| [AREA-001](../../03.specs/044-agent-roster-evaluation-and-admission/spec.md#success-criteria--verification-plan) | Not executed | Pending closed contracts, validators, and synthetic fixtures. |
| N/A — AREA-002 shares the Plan source above | Not executed | Pending two-role admission and exact repository-static adapter promotion. |
| N/A — AREA-003 shares the Plan source above | Not executed | Pending versioned eval, adjudication, and rollback evidence. |
| N/A — AREA-004 shares the Plan source above | Not executed | Pending fixed-cutoff candidate model/effort fitness evidence; runtime resolution remains `DEFER`. |
| N/A — AREA-005 shares the Plan source above | Not executed | Pending QA and independent review. |
