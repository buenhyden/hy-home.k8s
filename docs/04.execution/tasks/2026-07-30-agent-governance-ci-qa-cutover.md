---
title: 'Task: Agent Governance CI and QA Cutover'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-30
---

# Task: Agent Governance CI and QA Cutover

## Overview

This Task tracks the executable Spec 045 workstream that adds a dedicated
agent-governance repository-static CI/QA lane, closed CI and legacy-cutover
validation, consumer-first legacy removal, canonical GitHub hub routing, local
QA inventory alignment, and synthetic concurrent checkpoint and durable memory
policy.

The fixed provider/model/source cutoff remains
`2026-07-10T10:00:00+09:00` / `2026-07-10T01:00:00Z`. The date
`2026-07-30` is the activation observation only. AGQC-000 is the only active
package; `validate-agent-governance-ci.py` and
`validate-agent-legacy-cutover.py` are planned and do not exist at activation.

Spec 045 completion remains repository-static. Hosted CI, branch protection,
provider runtime/auth/model discovery, actual evaluation/admission/promotion,
provider resume/handoff canaries, remote execution, and live evidence remain
`DEFER` and are reserved for Spec 046.

## Inputs

- Parent Spec:
  [Spec 045](../../03.specs/045-agent-governance-ci-qa-cutover/spec.md)
- Parent Plan:
  [Agent Governance CI and QA Cutover Implementation Plan](../plans/2026-07-30-agent-governance-ci-qa-cutover.md)
- CI foundation: Spec 039
- Loop/checkpoint foundation: Spec 043
- Roster/evaluation predecessor: Spec 044
- Observed prerequisite commits: Spec 044 closure
  `42864832c966744ac4e5cf8c28baa5bf31ac2765` and postflight
  `279f81032528dbf732acc3a1a8bc232d11d2c246`
- Fixed cutoff owner:
  [provider-runtime-evidence.json](../../00.agent-governance/contracts/provider-runtime-evidence.json)
- Current machine owners:
  [harness-contract.json](../../00.agent-governance/contracts/harness-contract.json),
  [validation-surfaces.json](../../00.agent-governance/contracts/validation-surfaces.json),
  and
  [agent-loop-lifecycle.json](../../00.agent-governance/contracts/agent-loop-lifecycle.json)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| AGQC-000 | VAL-AGQC-001, VAL-AGQC-010 | Activate the reciprocal Spec/Plan/Task path and single program-lineage relation after observed Spec 044 closure/postflight | platform | In Progress | Exact eight-file activation is staged and validated without an activation-SHA preclaim | Staged lifecycle, strict registry `465` with `0/0` uncovered/ambiguous, Markdown, link/owner, JSON, aggregate, all-files pre-commit, and diff gates PASS |
| AGQC-001 | VAL-AGQC-001, VAL-AGQC-002 | Add dedicated agent-governance selector output, static job, and `ci-summary` topology | platform | Queued | Not executed | Planned workflow, selector, validation-surface, security, fixture, and aggregate evidence |
| AGQC-002 | VAL-AGQC-001..004 | Implement closed `validate-agent-governance-ci.py` contract/schema/fixture/tests and route it through local/CI owners | platform | Queued | Not implemented; the named validator is planned and absent at activation | Planned contract/schema, validator, fixture, focused tests, self-test/production, affected, aggregate, pre-commit, CI, and inventory evidence |
| AGQC-003 | VAL-AGQC-007, VAL-AGQC-008 | Implement consumer-first `validate-agent-legacy-cutover.py`, prove zero consumers, remove legacy role-semantics ownership/tests, and rename `.github/ABOUT.md` to `.github/README.md` | platform | Queued | Not implemented; no legacy file or GitHub hub is removed by activation | Planned zero-consumer fixtures, active-reference scan, atomic removal/rename diff, registry/quality/docs/inventory updates, and rollback evidence |
| AGQC-004 | VAL-AGQC-005, VAL-AGQC-006 | Align local QA order, repository-quality/pre-commit behavior, and script/test/GitHub/docs inventories | platform | Queued | Not executed | Targeted → affected → staged → tests → all-files → formatter review → rerun → diff evidence and current inventory checks |
| AGQC-005 | VAL-AGQC-009 | Add repository-static concurrent checkpoint/provider identity and durable memory retention/compaction/archive policy | platform | Queued | Not executed; actual provider checkpoint/resume/handoff remains `DEFER` | Planned closed contract/schema/fixture/test updates for identity collisions, retention, sensitivity, replacement, archive/GC, conflict, and handoff |
| AGQC-006 | VAL-AGQC-001..010 | Reconcile semantic owners, complete independent reviews and full local QA, then record reciprocal closure/postflight | platform | Queued | Not executed | Requirements/quality/security verdicts; focused/affected/staged/tests/all-files/formatter-rerun/diff results; exact closure/postflight identities; Spec 046 limitations |

## Approval and Safety Boundaries

- **Current AGQC-000 Allowed Paths**:
  `docs/03.specs/045-agent-governance-ci-qa-cutover/spec.md`,
  `docs/04.execution/plans/2026-07-30-agent-governance-ci-qa-cutover.md`,
  `docs/04.execution/tasks/2026-07-30-agent-governance-ci-qa-cutover.md`,
  `docs/03.specs/README.md`, `docs/04.execution/plans/README.md`,
  `docs/04.execution/tasks/README.md`,
  `docs/99.templates/support/document-profiles.json`, and
  `docs/00.agent-governance/memory/progress.md`
- **Later Planned Paths**: `.github/**`, `.pre-commit-config.yaml`,
  root provider shims, `.agents/**`, `.claude/**`, `.codex/**`, `.gemini/**`,
  `docs/00.agent-governance/**`, the reciprocal Spec/Plan/Task/index owners,
  `docs/99.templates/support/document-profiles.json`, `scripts/**`, and
  `tests/**`; each later package requires its own bounded implementation scope
- **Forbidden Paths**: credentials, auth caches/files, shell history, provider
  response bodies, private prompts/transcripts, Vault/ESO values, live
  Kubernetes/GitOps state, provider account state, actual provider-local
  memory, and actual `.agent-work/**` checkpoint content
- **Approval Required**: provider login/authenticated run, hosted workflow
  dispatch or remote GitHub mutation, branch-protection change, push/PR/merge,
  paid or credential-bearing action, provider resume/handoff canary, live
  cluster mutation, or credential change
- **Static Validation**: AGQC-000 uses existing strict registry, isolated
  proposed-index lifecycle, Markdown/frontmatter, link/owner, JSON, and
  diff/scope checks; planned Spec 045 validators run only after their files
  exist
- **Live Validation**: `DEFER`; no hosted, provider-runtime, remote, or live
  operation is authorized
- **Secret / Vault Handling**: no secret reads or prints, no auth inspection,
  no credential fixture values, and synthetic/redacted fixtures only
- **Rollback Plan**: discard or revert only the exact AGQC unit in reverse
  dependency order; restore the legacy owner and `.github/ABOUT.md` together if
  zero-consumer or rename validation fails; revert AGQC-000 last without reset,
  clean, or overwrite of unrelated work
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`

## Verification Summary

AGQC-000 is the only active work item. Its exact-eight proposal changes no
workflow, selector, contract implementation, schema, validator, fixture, test,
pre-commit hook, provider adapter, provider setting, model assignment,
checkpoint behavior, legacy file, `.github` hub, credential, remote resource,
or live surface.

The activation observes Spec 044 closure `42864832` and postflight `279f8103`;
it does not claim its own future content-addressed commit SHA. The two planned
Spec 045 validators are absent and no future focused, aggregate, hosted, or
provider result is preclaimed.

The provider/model/source cutoff remains the fixed 2026-07-10 timestamp.
Hosted CI, branch protection, provider runtime/auth/model discovery, actual
evaluation/admission/promotion, provider resume/handoff canaries, remote, and
live evidence are `DEFER`. Independent implementation reviewers are assigned
only in AGQC-006.

## Traceability

- **Successor**: Spec 046

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [AGQC-000](../plans/2026-07-30-agent-governance-ci-qa-cutover.md#work-breakdown) | In Progress | Exact-eight staged activation; lifecycle, strict registry `465` with `0/0` uncovered/ambiguous, Markdown, link/owner, JSON, aggregate, all-files pre-commit, and diff gates PASS; activation SHA unclaimed. |
| [AGQC-001](../../03.specs/045-agent-governance-ci-qa-cutover/spec.md#success-criteria--verification-plan) | Not executed | Pending dedicated selector/job/`ci-summary` topology and repository-static fixtures. |
| N/A — AGQC-002 shares the Plan and Spec sources above | Not executed | Planned CI contract/schema/validator/fixture/tests do not exist at activation. |
| N/A — AGQC-003 shares the Plan and Spec sources above | Not executed | Pending zero-consumer proof before legacy removal and `.github/ABOUT.md` to `.github/README.md` cutover. |
| N/A — AGQC-004 shares the Plan and Spec sources above | Not executed | Pending QA-order and repository-quality/pre-commit/docs inventory alignment. |
| N/A — AGQC-005 shares the Plan and Spec sources above | Not executed | Pending repository-static concurrent checkpoint/provider identity and durable memory policy; actual provider resume/handoff remains `DEFER`. |
| N/A — AGQC-006 shares the Plan and Spec sources above | Not executed | Pending semantic reconciliation, independent reviews, full QA, reciprocal closure/postflight, and explicit Spec 046 handoff. |
