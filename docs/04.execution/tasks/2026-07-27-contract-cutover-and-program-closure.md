---
title: 'Task: Contract Cutover and Program Closure'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-27
---

# Task: Contract Cutover and Program Closure

## Overview

This Task is the evidence owner for the
[Spec 040 Plan](../plans/2026-07-27-contract-cutover-and-program-closure.md).
It tracks reciprocal activation, strict-only active-reader cutover, final
closure-matrix and Current-audit reconciliation, whole-branch QA and reviews,
and atomic PRD-006 program closure. Work is repository-local unless a
separately approved action explicitly changes that boundary.

The predecessor closure commit
`e1d1e910840337327a557ab4b84e86f8fced11d6` passed explicit-ref lifecycle and
clean-tree repository-static postflight. Evidence update
`11a020d9b299ae91b7af9278c22ed89ffccb5cfc` hands the active frontier to Spec
040. Hosted run `29982910320` remains historical FAIL for its older SHA, and
current hosted, provider, remote, and live evidence remains `DEFER`. The
activation package was committed as
`5c7bb820d9b424577eda3eb3a5c368f0c7cfc656`; explicit-ref lifecycle from the
evidence-update commit and the clean-tree repository-static aggregate passed.

## Inputs

- [Contract Cutover and Program Closure Implementation Plan](../plans/2026-07-27-contract-cutover-and-program-closure.md)
- [Spec 040](../../03.specs/040-contract-cutover-and-program-closure/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- [ADR-0018](../../02.architecture/decisions/0018-full-body-archive-record-and-retention.md)
- [Document profile registry](../../99.templates/support/document-profiles.json)
- [Current implementation audit index](../../90.references/audits/README.md)
- [Settled migration snapshot](../../90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md)
- Spec 039 closure `e1d1e910840337327a557ab4b84e86f8fced11d6`
  and evidence update `11a020d9b299ae91b7af9278c22ed89ffccb5cfc`
- [Document quality standards](../../00.agent-governance/rules/quality-standards.md)
- [Git workflow](../../00.agent-governance/rules/git-workflow.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| CCPC-000 | Activation gate | Activate the reciprocal Spec 040 Plan/Task pair, direct backlinks, both Stage 04 indexes, and shared progress handoff as one exact six-path package without registry or migration-ledger drift. | platform | Done | Plan-only lifecycle RED, exact-six lifecycle/strict/aggregate GREEN, all-files PASS, independent requirements/quality approval, activation commit, explicit-ref lifecycle, and clean-tree aggregate are observed. | Plan-only `LIFECYCLE-CREATE` exit `1` at Plan `1` / Task `0`; exact-six lifecycle PASS; registry self-test `119`, strict registry `450`, strict Markdown zero, links/owners PASS, residue active `2/1` and findings `0`, diff-check and aggregate PASS; all applicable all-files hooks PASS with Dockerfile no-file `SKIP`; `/root/spec040_activation_requirements` `REQUIREMENTS COMPLIANT`; `/root/spec040_activation_quality` `QUALITY APPROVED`; activation `5c7bb820d9b424577eda3eb3a5c368f0c7cfc656`; explicit-ref and clean-tree aggregate PASS. |
| CCPC-001 | VAL-CCPC-001, VAL-CCPC-002 | Make current document readers strict-only, retire active compatibility behavior and stale wording, and preserve only pinned finite historical-transition proof fixtures. | platform | In Progress | Focused RED and GREEN, strict-only implementation, current contract updates, exact helper admission remediation, staged QA, and independent requirements/quality approvals are observed; the logical implementation commit and post-commit evidence remain pending. | RED: 6 tests with 14 intended failures; first staged aggregate rejected the new regression with `ROLE-AUDIT-HELPER-ADMISSION`. GREEN: focused 6/6; registry self-test `119`; Markdown and links/owners self-tests PASS; all three validators pass no-mode and explicit strict production; all three reject compatibility with exit `2`; strict registry `450`, Markdown zero, links/owners PASS; role-audit tests `36`, self-test `28`, production helpers `44/33/11` and formats `16/21/6/1`; lifecycle, aggregate, all applicable all-files hooks, and both diff-checks PASS; Dockerfile no-file `SKIP`; reviewed pre-evidence digest `f83ec5afb90b6c2cb7d35e9c5259d5c8358697e6d7304bfa9cde39ddf9c1b360`; `/root/spec040_ccpc001_final_requirements` `REQUIREMENTS COMPLIANT`; `/root/spec040_ccpc001_final_quality` `QUALITY APPROVED`. |
| CCPC-002 | VAL-CCPC-002 through VAL-CCPC-005 | Build the final requirement/criterion closure matrix, rerun archive/migration/reference/workflow evidence, and reconcile the Current audit with owners, limitations, and rollback. | platform | Queued | No implementation result is claimed. | Final closure matrix, Current audit overlay, deterministic command results, settled-ledger verification, and reviewable diffs will be recorded here. |
| CCPC-003 | VAL-CCPC-006 | Run focused, affected, lifecycle, strict, aggregate, all-files, formatter, and diff lanes; obtain independent whole-branch requirements and quality/security reviews; remediate findings. | platform | Queued | No validation or review result is claimed. | Exact proposal digest, command result matrix, formatter/status inspection, reviewer verdicts, and remediation commits will be recorded here. |
| CCPC-004 | VAL-CCPC-001 through VAL-CCPC-006 | Close PRD-006, ARD-0009, Spec/Plan/Task, indexes, decision evidence, and final program relation atomically; create the logical closure commit; run explicit-ref and clean-tree postflight. | platform | Queued | No terminal transition, closure commit, or postflight result is claimed. | Exact terminal path set, lifecycle transition evidence, observed commit identity, explicit-ref result, clean-tree postflight, rollback chain, and retained DEFER rows will be recorded here. |

## Approval and Safety Boundaries

- **Allowed Paths**: Spec 040 and its reciprocal Plan/Task/index/progress
  lineage; current document validators and their focused tests/fixtures;
  current Stage 99 support, script/test inventories, Current audit overlay,
  closure-matrix evidence, PRD-006/ARD-0009/ADR-0017 lifecycle evidence,
  document registry final relation, and directly affected repository-static
  QA surfaces authorized by the Plan.
- **Forbidden Paths**: Specs 041-046 implementation; provider adapters, models,
  roster, and shared-provider memory; `.gemini/**`; Kubernetes/GitOps desired
  state; infrastructure, Vault, ESO, Argo CD, deployment, release, credentials,
  secret values, ignored `_workspace` children, auth files, tokens,
  kubeconfigs, and shell history.
- **Approval Required**: Push, merge, workflow dispatch, GitHub setting
  mutation, publication, dependency installation, live command, credential or
  secret access, and any expansion outside the Plan require separate explicit
  human approval.
- **Static Validation**: Focused tests; affected-surface checks; lifecycle
  self-test, staged, and explicit-ref modes; strict registry/profile/link
  checks; archive, migration, reference, generated-output, workflow and
  selector gates; repository aggregate; unqualified all-files pre-commit;
  formatter/status inspection; cached and unstaged diff checks.
- **Live Validation**: `DEFER`. No current hosted GitHub Actions, provider,
  remote, Kubernetes, Vault, ESO, Argo CD, cloud, deployment, or credential
  result is authorized by this Task.
- **Secret / Vault Handling**: Do not open, print, copy, hash, or report secret
  values. Evidence is limited to stable rule IDs, repository-relative paths,
  bounded counts, public run identifiers, and observed Git identities.
- **Rollback Plan**: Revert the newest observed logical unit first, rerun its
  focused and aggregate gates, and continue through the recorded chain only as
  needed. Revert activation last. Never reset, clean, rewrite shared history,
  or overwrite unrelated work.
- **Evidence Location**: This Task is the result ledger. The reciprocal Plan
  owns execution order; the Spec owns criteria; reviewed logical commits,
  exact tests/fixtures, the Current audit overlay, closure matrix, and progress
  ledger retain supporting evidence.

## Verification Summary

The current input state is observed: Spec 039 closure
`e1d1e910840337327a557ab4b84e86f8fced11d6` and its clean-tree
repository-static postflight are PASS, and evidence update
`11a020d9b299ae91b7af9278c22ed89ffccb5cfc` is the base for this activation.
Current hosted, provider, remote, and live lanes remain `DEFER`; historical
hosted run `29982910320` remains FAIL for its older SHA.

The Spec 040 activation is observed in
`5c7bb820d9b424577eda3eb3a5c368f0c7cfc656`. Plan-only lifecycle exited `1`
with `LIFECYCLE-CREATE`, Plan count `1`, and Task count `0`. Exact-six staging
then passed lifecycle; registry self-test `119` and strict registry
`450` with zero uncovered/ambiguous routes; strict Markdown with zero
findings; strict links/owners; residue closure at active controls `2/1`,
terminal controls `4/2`, terminal Specs `2`, and findings `0`; diff-check; and
the repository aggregate final marker. `pre-commit run --all-files` passed
every applicable hook, Dockerfile lint was a no-file `SKIP`, and no formatter
mutation remained. Reviewer `/root/spec040_activation_requirements` returned
`REQUIREMENTS COMPLIANT`; `/root/spec040_activation_quality` returned
`QUALITY APPROVED` after its sole stale-fallback finding was fixed. The
activation commit then passed explicit-ref lifecycle from
`11a020d9b299ae91b7af9278c22ed89ffccb5cfc` and the clean-tree aggregate.

CCPC-001 began with 6 focused tests and 14 intentional RED failures. The
strict-only implementation now passes all 6 tests, registry self-test `119`,
Markdown and cross-document self-tests, and all three validators in both
no-mode and explicit strict production. Each retired compatibility invocation
is rejected by argparse with exit `2`; strict registry reports `450` paths,
strict Markdown reports zero findings, strict links/owners passes, and
diff-check passes. The finite Spec 033 retirement guard remains closed and the
retired semantic-debt fixture remains absent. Reviewer
`/root/spec040_ccpc001_requirements` returned `REQUIREMENTS COMPLIANT`, and
`/root/spec040_ccpc001_quality` returned `QUALITY APPROVED`. The CCPC-001
regression initially failed the staged aggregate with
`ROLE-AUDIT-HELPER-ADMISSION`; its identity-bound post-closure admission now
passes role-audit tests `36`, self-test `28`, and production with helpers
`44/33/11`, formats `16/21/6/1`, and findings `0`. The CCPC-001 logical commit
proposal then passed staged lifecycle, the repository aggregate final marker,
and every applicable all-files hook; Dockerfile lint was a no-file `SKIP`,
neither formatter nor unstaged drift changed the proposal, and both diff
checks passed. Reviewers `/root/spec040_ccpc001_final_requirements` and
`/root/spec040_ccpc001_final_quality` returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED` for pre-evidence digest
`f83ec5afb90b6c2cb7d35e9c5259d5c8358697e6d7304bfa9cde39ddf9c1b360`.
The CCPC-001 logical commit and post-commit evidence remain unobserved and unclaimed;
CCPC-002 through CCPC-004 remain queued.

## Traceability

- **Plan**: Contract Cutover and Program Closure Implementation Plan
- **Spec**: Contract Cutover and Program Closure Technical Specification
- **Predecessor evidence**: Spec 039 closure
  `e1d1e910840337327a557ab4b84e86f8fced11d6` and evidence update
  `11a020d9b299ae91b7af9278c22ed89ffccb5cfc`
- **Program**:
  [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
  and
  [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [CCPC-000](../plans/2026-07-27-contract-cutover-and-program-closure.md#ccpc-000--reciprocal-activation) | Done — Plan-only RED, exact-six lifecycle/strict/aggregate/all-files GREEN, both independent approvals, activation commit, explicit-ref lifecycle, and clean-tree aggregate observed. | `LIFECYCLE-CREATE` Plan `1` / Task `0`; lifecycle, registry `119/450`, Markdown, links/owners, residue active `2/1`, diff-check, aggregate, and applicable all-files PASS; requirements/quality approved; activation `5c7bb820d9b424577eda3eb3a5c368f0c7cfc656`. |
| [VAL-CCPC-001](../../03.specs/040-contract-cutover-and-program-closure/spec.md#success-criteria--verification-plan) | In Progress — strict-only implementation, staged QA, and final reviews pass; commit/postflight pending. | RED `6/14` plus helper-admission aggregate RED; GREEN focused `6/6`, role audit `36/28/44`, registry self-test `119`, three no-mode and strict production PASS, three compatibility exit `2`, strict registry `450`, Markdown zero, links/owners, lifecycle, aggregate, all-files, and diff checks PASS; final requirements/quality approved. |
| N/A — VAL-CCPC-002 shares the Spec 040 source linked in VAL-CCPC-001 | In Progress — strict ownership/link evidence passes; closure matrix pending. | CCPC-001 strict ownership/link results are observed; CCPC-002 closure matrix will be recorded in this Task. |
| N/A — VAL-CCPC-003 shares the Spec 040 source linked in VAL-CCPC-001 | Queued. | CCPC-002 archive provenance and historical-link results will be recorded in this Task. |
| N/A — VAL-CCPC-004 shares the Spec 040 source linked in VAL-CCPC-001 | Queued. | CCPC-002 final execution-disposition and rollback results will be recorded in this Task. |
| N/A — VAL-CCPC-005 shares the Spec 040 source linked in VAL-CCPC-001 | Queued. | CCPC-002/003 reference, generated-output, workflow, selector, and result-class results will be recorded in this Task. |
| N/A — VAL-CCPC-006 shares the Spec 040 source linked in VAL-CCPC-001 | Queued. | CCPC-003 reviews and QA plus CCPC-004 atomic closure/postflight will be recorded in this Task. |
