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
`2026-07-30` is the activation observation only. AGQC-000 through AGQC-005 are
complete and AGQC-006 is the active package. The closed
`validate-agent-governance-ci.py` and `validate-agent-legacy-cutover.py`
owners exist. The consumer-first cutover proves zero active consumers, retains
only closed superseding/archive evidence, removes legacy role-semantics
ownership, and establishes the canonical GitHub hub. The local QA contract now
owns the exact eight-step completion order, affected/staged runner separation,
plain staged and all-files pre-commit commands, both diff checks, formatter
rerun semantics, and current machine inventories.

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
- Observed Spec 045 activation:
  `c677321d9c0afee2cce7a8485c58e23d4a3bf18c`
- Observed Spec 045 postflight and implementation: activation postflight
  `46c8e6b64097cce1c403b8c22989b11226f21263` and AGQC-001
  `12c5578747ef37afb9a1e65afe41bee6aca0e473`; AGQC-001 postflight
  `25688ec6e321a0458437f83bdc914b339fe28c2d` and AGQC-002
  `be0a12ecd8d51b73f251004b34be6e8288159eb5`; AGQC-002 postflight
  `a3cf5836e46cb2e53f9ec5ddf4150559d2643d39` and AGQC-003
  `38a2fe6b90bad694d0a9a021c7edce8d800e03ea`; AGQC-003 postflight
  `dc7dccbfcb907ae38cc0f7c91b59b6556e4fe888` and AGQC-004
  `baf4df962cb70c55eefd20b5fe76ee07e7ff8be0`
- Observed AGQC-005 implementation: checkpoint isolation and memory lifecycle
  `781ebb82b64d2f63d6b9630b6b3e48115dc5a791`; closed static CI evidence
  ownership `4c7b87718aa41f680ef8f5e63c4396565b1c5e0b`
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
| AGQC-000 | VAL-AGQC-001, VAL-AGQC-010 | Activate the reciprocal Spec/Plan/Task path and single program-lineage relation after observed Spec 044 closure/postflight | platform | Done | Exact eight-file activation committed and clean-tree postflight observed | Activation `c677321d9c0afee2cce7a8485c58e23d4a3bf18c`; focused, aggregate, all-files, diff, and final independent review PASS |
| AGQC-001 | VAL-AGQC-001, VAL-AGQC-002 | Add dedicated agent-governance selector output, static job, and `ci-summary` topology | platform | Done | Four-job selector/workflow/summary topology is repository-statically enforced and all required owner classes select the lane | `12c5578747ef37afb9a1e65afe41bee6aca0e473`; affected `22/22`, `19` selections, `6` CI ranges, `37` mutations, `806` paths, `0/0`; focused/aggregate/all-files/review PASS |
| AGQC-002 | VAL-AGQC-001..004 | Implement closed `validate-agent-governance-ci.py` contract/schema/fixture/tests and route it through local/CI owners | platform | Done | Closed Draft 2020-12 contract, exact CI topology and command sequence, delegated checks, result/evidence vocabularies, and fail-closed security controls are repository-statically enforced | `be0a12ecd8d51b73f251004b34be6e8288159eb5`; `22` focused tests, `6` truth and `38` mutation self-test cases, `12` route classes, `13` delegated checks, affected `22/22` and `811` staged paths with `0/0` uncovered/ambiguous; aggregate/all-files/diff/final review PASS |
| AGQC-003 | VAL-AGQC-007, VAL-AGQC-008 | Implement consumer-first `validate-agent-legacy-cutover.py`, prove zero consumers, remove legacy role-semantics ownership/tests, and establish `.github/README.md` as the canonical GitHub hub | platform | Done | Consumer-first removal and canonical hub cutover are closed; exact active references are zero and protected historical evidence requires a verified superseding relation before scanning | `38a2fe6b90bad694d0a9a021c7edce8d800e03ea`; `20` focused tests, `3` positive/`22` mutation self-test cases, `810` scanned files, `43` evidence references, `0` active consumers; RIA `87`, aggregate/all-files/diff/requirements/security/integration PASS |
| AGQC-004 | VAL-AGQC-005, VAL-AGQC-006 | Align local QA order, repository-quality/pre-commit behavior, and script/test/GitHub/docs inventories | platform | Done | The canonical eight-step order, exact affected/staged runner behavior, plain staged/all-files pre-commit boundaries, formatter rerun rule, both diff checks, and current inventories are closed and fail-closed validated | `baf4df962cb70c55eefd20b5fe76ee07e7ff8be0`; runner `22`, CI `24`, self-test `6/43`, production `12/16/6/2/10`, legacy `3/22` and `810/43/0`; affected/staged `15` paths, aggregate/plain pre-commit/all-files/diff/final reviews PASS |
| AGQC-005 | VAL-AGQC-009 | Add repository-static concurrent checkpoint/provider identity and durable memory retention/compaction/archive policy | platform | Done | Repository-static checkpoint/provider identity and four-class memory lifecycle policy are closed; independent review approved | `781ebb82b64d2f63d6b9630b6b3e48115dc5a791` checkpoint: `20` focused tests, `110` negative mutations, four memory classes; `4c7b87718aa41f680ef8f5e63c4396565b1c5e0b` loop: `22` focused tests, `66` self-test cases; deterministic repository, worktree, task, provider surface, provider-session-instance, namespace, writer/generation/previous-checkpoint isolation; four-class sensitivity, retention/expiry, compaction source/replacement, archive/GC, conflict, and handoff |
| AGQC-006 | VAL-AGQC-001..010 | Reconcile semantic owners, complete independent reviews and full local QA, then record reciprocal closure/postflight | platform | In Progress | Active package; results not yet claimed | Requirements/quality/security verdicts; focused/affected/staged/tests/all-files/formatter-rerun/diff results; exact closure/postflight identities; Spec 046 limitations |

## Approval and Safety Boundaries

- **Recorded AGQC-000 Activation Paths**:
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
- **Static Validation**: AGQC-000 used the existing strict registry, isolated
  proposed-index lifecycle, Markdown/frontmatter, link/owner, JSON, and
  diff/scope checks. AGQC-001 and AGQC-002 now add affected-surface topology
  and the closed agent-governance CI contract; each later validator runs only
  after its contract, schema, fixture, tests, and implementation exist
- **Live Validation**: `DEFER`; no hosted, provider-runtime, remote, or live
  operation is authorized
- **Secret / Vault Handling**: no secret reads or prints, no auth inspection,
  no credential fixture values, and synthetic/redacted fixtures only
- **Rollback Plan**: discard or revert only the exact AGQC unit in reverse
  dependency order; restore the legacy owner and former GitHub hub name
  together if zero-consumer or rename validation fails; revert AGQC-000 last
  without reset, clean, or overwrite of unrelated work
- **Evidence Location**: this Task and
  `../../00.agent-governance/memory/progress.md`

## Verification Summary

AGQC-000 through AGQC-003 are complete at activation `c677321d`, CI topology
implementation `12c55787`, closed CI contract implementation `be0a12ec`,
consumer-first cutover `38a2fe6b`, and local QA closure `baf4df96`.
The affected-surface contract owns four CI jobs and all required
agent-governance owner classes select `agent-governance-static`. The closed
validator enforces the exact job, step, environment, permissions, defaults,
command, pin, result, evidence, and delegated-check shapes; the summary
accepts only selected-success and unselected-skipped combinations and fails
closed otherwise.

The AGQC-003 legacy-cutover contract, schema, fixture, tests, and validator
prove zero active consumers before the atomic legacy deletion and GitHub hub
rename. Protected historical snapshots are accepted only through exact digest,
lifecycle, source, retired-reference count, and superseding-replacement
evidence. Missing evidence and retired-reference removal fail closed.

AGQC-004 adds `staged` to the closed local runner, propagates exact staged
Markdown paths to every selected document validator, and makes
`quality-standards.md` the sole eight-step local completion owner. The closed
CI contract now validates `6` truth cases, `43` mutations, `16` delegated
checks, `1` deferred owner solely for Spec 046, `10` QA surfaces, the separate plain staged and
all-files pre-commit commands, and both worktree and cached diff checks.
AGQC-005 closes repository-static concurrent checkpoint/provider identity and
the working short-term, durable long-term, domain scoped, and provider-local
auxiliary memory lifecycle policy. Checkpoint evidence reports `20` focused
tests and `110` negative mutations; loop evidence reports `22` focused tests
and `66` self-test cases. Independent review approved the implementation.

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
| [AGQC-000](../plans/2026-07-30-agent-governance-ci-qa-cutover.md#work-breakdown) | Done | Activation `c677321d`; lifecycle, strict registry `465` with `0/0` uncovered/ambiguous, Markdown, link/owner, JSON, aggregate, all-files pre-commit, diff, and final independent review PASS. |
| [AGQC-001](../../03.specs/045-agent-governance-ci-qa-cutover/spec.md#success-criteria--verification-plan) | Done | `12c55787`; affected `22/22`, `19` selections, `6` CI ranges, `37` mutations, `806` paths, `4` jobs, `0/0`; CI Python/GitHub security/aggregate/all-files/final review PASS. |
| N/A — AGQC-002 shares the Plan and Spec sources above | Done | `be0a12ec`; `22` focused tests, self-test `6` truth/`38` mutation cases, production `12` route classes/`13` delegated checks, affected `22/22` and `811` staged paths with `0/0`, aggregate/all-files/diff/final review PASS. |
| N/A — AGQC-003 shares the Plan and Spec sources above | Done | `38a2fe6b`; `20` focused tests, self-test `3/22`, production `810` scanned files/`43` evidence references/`0` active consumers, RIA `87`, aggregate/all-files/diff/final requirements/security/integration review PASS. |
| N/A — AGQC-004 shares the Plan and Spec sources above | Done | `baf4df96`; runner `22`, CI `24`, self-test `6/43`, production `12/16/6/2/10`, legacy `3/22` and `810/43/0`, affected/staged `15` paths, aggregate/plain pre-commit/all-files/diff/final review PASS, formatter mutation `0`. |
| N/A — AGQC-005 shares the Plan and Spec sources above | Done | `781ebb82`; checkpoint `20` focused tests/`110` negative mutations/four memory classes. `4c7b8771`; loop `22` focused tests/`66` self-test cases, deterministic identity isolation and four-class sensitivity, retention/expiry, compaction source/replacement, archive/GC, conflict, and handoff; independent review approved. |
| N/A — AGQC-006 shares the Plan and Spec sources above | In Progress | Active package; pending semantic reconciliation, independent reviews, full QA, reciprocal closure/postflight, and explicit Spec 046 handoff. |
