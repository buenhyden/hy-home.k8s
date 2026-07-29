---
title: 'Task: Agent Roster Evaluation and Admission'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-30
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
  `0129daf7d44c9308bcad63d4966e11ffa98d05af`; AREA-002 projection
  `138ce6ac28aa0eebac2b0295e4c50fd78d594db6` and admission-boundary
  remediation `1d03b0b44350b26cca1f7d91ebaf8f3c66b4ce1e`; AREA-003 evaluation
  readiness `3bd5759029cc49742c12a811f8751f1609c4f330`; AREA-004 model-fitness
  readiness `258955b3e0d999ec4ebc3de561d0db39ce11ac3c`

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AREA-000 | VAL-AREA-001 | Activate reciprocal Spec/Plan/Task path and registry relation | platform | Done | Activation and clean-tree postflight committed | `b8b1a3884f9948fcd4ac2aecc89ea727118ad787`; `6d9b01d51f8a198c521621bcd52ff088c397ee0b` |
| AREA-001 | VAL-AREA-001..008 | Implement closed admission, evaluation, and model-fitness schemas, validators, and synthetic negative fixtures before promotion | platform | Done | Closed gates preserve current `10/3/30`, target-only `12/4/48`, and all promotion/runtime lanes as `DEFER` | `0129daf7d44c9308bcad63d4966e11ffa98d05af`; focused `119`, aggregate/all-files PASS |
| AREA-002 | VAL-AREA-001..004 | Project `docs-researcher` and `quality-engineer` with the exact 12/4/48 repository-static roster and native projections | platform | Done | Exact tracked projection is committed with admission `DEFER`; final-admission evidence remains owned by AREA-003 | `138ce6ac28aa0eebac2b0295e4c50fd78d594db6`; boundary remediation `1d03b0b44350b26cca1f7d91ebaf8f3c66b4ce1e`; focused, aggregate, all-files, and independent review PASS |
| AREA-003 | VAL-AREA-005, VAL-AREA-006 | Implement versioned four-class role evaluation coverage, independent adjudication, rollback records, and final admission decision | platform | Done | Repository-static evaluation readiness is complete; readiness is `PASS`, while observed evaluation and final admission remain `DEFER` | `3bd5759029cc49742c12a811f8751f1609c4f330`; 48 role-specific records, 12 adjudication-readiness records, 2 source-bound rollback records, explicit final-DEFER decision, focused/aggregate/all-files/review PASS |
| AREA-004 | VAL-AREA-006..008 | Reconcile fixed cutoff and implement risk-based provider candidate model/effort fitness without runtime preclaim | platform | Done | Repository-static mapping readiness is complete: `PASS` 21 and `DEFER` 27; all 48 fitness, threshold, promotion, canary, and runtime decisions remain `DEFER` | `258955b3e0d999ec4ebc3de561d0db39ce11ac3c`; contract `1.1.0`, schema `2`, `repository-static-fitness-ready`; focused `28`, self-test `33`, production, aggregate, all-files, and independent review PASS |
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
finally admitted. Remediation commit `1d03b0b4` preserves that boundary across
the contract, schema, validators, lifecycle controls, all four provider
surfaces, and the five-field Gemini project-agent metadata projection.
Admission focused validation passed `59` self-test and `13` unit cases;
lifecycle passed `696` self-test and `6` focused cases; role semantics passed
`768` cases plus `9` Gemini metadata mutations; model fitness passed `16`
self-test and `18` focused unit cases. The active corpus audit passed with
`helpers=60`, `frozen=33`, `post_closure=27`, and formats `25/28/6/1`.
Repository aggregate and `pre-commit run --all-files` passed. Requirements
review approved Spec compliance, and final quality review reported zero
Critical or Important findings after two wording corrections.

AREA-003 commit `3bd57590` completes the versioned four-class corpus,
adjudication-readiness, rollback-source binding, and explicit final-decision
record within its repository-static readiness scope. Contract
version `1.1.0` and state `repository-static-evaluation-ready`: exact 12-role
harness suite/version binding, 48 role-specific synthetic records, 12
adjudication-readiness records, and 2 rollback records bound to the governed
roster-admission source. Readiness is `PASS`, but observed same-suite
evaluation, result adjudication, and final admission remain `DEFER`.

Focused tests passed `33/33`, evaluation self-test `60/60`, staged lifecycle,
repository aggregate, all-files pre-commit, and diff checks passed. Spec review
approved with zero Critical or Important findings. Quality review's two
Important findings—symlink-root resolution and unbound rollback references—
were corrected and independently re-reviewed as addressed.

AREA-004 commit `258955b3` completes the closed provider/model mapping-readiness
contract without promoting a candidate or preclaiming model execution.
Contract version `1.1.0`, schema version `2`, and lifecycle state
`repository-static-fitness-ready` cover exactly 12 roles, 4 providers, and 48
role/provider tuples. Mapping readiness is `PASS` for 21 tuples: all 12 local
tuples and the 9 cutoff-applicable Claude high-risk tuples. It remains `DEFER`
for 27 tuples: 3 current-only Claude tuples, all 12 Codex tuples, and all 12
mixed/unresolved Gemini tuples. Every configured incumbent remains unchanged.

The fixed thresholds are quality `0.9`, safety `1`, cost `1` USD, and latency
`120000` ms. Observed fitness, threshold, promotion, canary, and runtime
decisions remain `DEFER` for all 48 tuples. Provider runtime and
authentication, hosted CI, remote/live execution, and model resolution remain
`DEFER`; every tuple rollback state is `armed-not-executed` and its execution
evidence is `DEFER`.
Focused tests passed `28/28`, the closed self-test passed `33/33`, and
production reported `roles=12`, `providers=4`, `tuples=48`,
`mappingReady=21`, `mappingDeferred=27`, `fitnessDeferred=48`,
`thresholdDeferred=48`, `promotionDeferred=48`, `canaryDeferred=48`, and
`runtimeDeferred=48`. Staged lifecycle, strict registry over `463` tracked
paths, repository aggregate, all-files pre-commit, and diff checks passed.
Final independent review reported zero Critical and zero Important findings.

The provider/model cutoff remains `2026-07-10 10:00 Asia/Seoul`; runtime,
provider discovery/authentication, model resolution, agent evaluation,
observed model fitness and promotion, hosted CI, remote, live, and ignored
checkpoint execution remain `DEFER`.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AREA-000](../plans/2026-07-29-agent-roster-evaluation-and-admission.md#work-breakdown) | Done | Activation `b8b1a388` and clean-tree postflight `6d9b01d5`. |
| [AREA-001](../../03.specs/044-agent-roster-evaluation-and-admission/spec.md#success-criteria--verification-plan) | Done | Closed admission/evaluation/model-fitness gates and postflight evidence in `0129daf7`; requirements `COMPLIANT`, security/model-path review `APPROVED`. |
| N/A — AREA-002 shares the Plan source above | Done | Commits `138ce6ac` and `1d03b0b4` project exact 12/4/48 repository-static inventory while preserving admission `DEFER`; focused, aggregate, all-files, requirements, and quality review gates passed. |
| N/A — AREA-003 shares the Plan source above | Done | Commit `3bd57590` establishes `repository-static-evaluation-ready` with 48 corpus records, 12 readiness adjudications, 2 source-bound rollback records, and explicit final admission `DEFER`; focused, aggregate, all-files, Spec, and quality review gates passed. |
| N/A — AREA-004 shares the Plan source above | Done | Commit `258955b3` establishes `repository-static-fitness-ready` for 12 roles, 4 providers, and 48 tuples; mapping is `PASS` 21 / `DEFER` 27, configured incumbents are retained, and all 48 fitness, threshold, promotion, canary, and runtime decisions remain `DEFER`; focused, lifecycle, strict-registry, aggregate, all-files, diff, and independent-review gates passed without provider/model execution; rollback state remains `armed-not-executed` with execution evidence `DEFER`. |
| N/A — AREA-005 shares the Plan source above | Not executed | Pending QA and independent review. |
