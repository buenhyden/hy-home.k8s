---
title: 'Task: GitHub CI and QA Evidence'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-26
---

# Task: GitHub CI and QA Evidence

## Overview

This Task is the execution, verification, review, rollback, and handoff evidence
owner for GCQE-000 through GCQE-006. It activates
[Spec 039](../../03.specs/039-github-ci-qa-evidence/spec.md) from approved
design and rollback parent
`cd726e05fdb9d33727314d316aadb5ebbec0942d`.

The Plan-only staged lifecycle probe is directly observed. It exited `1` with
`LIFECYCLE-CREATE`, expected exactly one active Plan and one active Task, and
observed Plan count `1` and Task count `0`. This reciprocal Task closes that
intentional creation RED. No implementation package, hosted CI rerun, review
approval, closure commit, or live result is claimed at activation.

The latest hosted evidence remains GitHub Actions run `29982910320`, an
observed FAIL for commit
`bd93374d7f531317c3bd061eb1ef567c1e2e0084`. It exposed missing Python
dependencies in the pre-commit job and a transitive Node.js warning from
`pre-commit/action`. A post-change hosted result remains DEFER until a
separately approved push or workflow dispatch is directly observed.

## Inputs

- [GitHub CI and QA Evidence Implementation Plan](../plans/2026-07-26-github-ci-qa-evidence.md)
- [Spec 039](../../03.specs/039-github-ci-qa-evidence/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- [Affected-surface contract](../../00.agent-governance/contracts/validation-surfaces.json)
- [Agent quality standards](../../00.agent-governance/rules/quality-standards.md)
- [Git workflow](../../00.agent-governance/rules/git-workflow.md)
- [GitHub configuration hub](../../../.github/ABOUT.md)
- [Technology version inventory](../../90.references/data/tech-stack-version-inventory.md)
- [Settled migration snapshot](../../90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md)
- [Predecessor Spec 038 Task](./2026-07-22-reference-information-architecture.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| GCQE-000 | Activation gate | Preserve the settled migration snapshot, then activate the reciprocal Spec 039 Plan/Task pair, direct backlinks, Stage 04 indexes, and shared progress handoff as one exact six-path package. | platform | Done | Plan-only lifecycle RED, the ledger/admission contract collision, prerequisite commit `cd726e0`, exact-six reciprocal GREEN, activation commit `2ddfe4b`, and post-commit aggregate PASS are observed. | `LIFECYCLE-CREATE`, Plan count 1/Task count 0; protected-ledger RIA failure; rollback parent `cd726e0`; staged lifecycle/registry/profile/link/RIA PASS; exact-six commit `2ddfe4b`; HEAD aggregate PASS; raw all-files fails only at the existing FIFO limitation. |
| GCQE-001 | VAL-GCQE-004 | Add a capability-aware FIFO/directory non-regular fixture, preserve `RESOURCE_NOT_REGULAR`, and re-raise unexpected filesystem errors. | platform | Queued | Not executed. | Focused unit RED/GREEN, unqualified GitOps self-test, aggregate, and all-files evidence will be recorded here. |
| GCQE-002 | VAL-GCQE-001, VAL-GCQE-002, VAL-GCQE-003 | Add the exact CI Python requirements owner and validator; pin Python 3.12; replace `pre-commit/action`; preserve workflow entry, aggregate, and full-document selection. | platform | Queued | Not executed. | CI contract unit/self-test/production, selector fixture, workflow security, aggregate, and all-files evidence will be recorded here. |
| GCQE-003 | VAL-GCQE-003 | Enforce integer seven-day retention on every upload-artifact step and set the changelog preview producer accordingly. | platform | Queued | Not executed. | Artifact-retention fixture RED/GREEN and repository Actions security evidence will be recorded here. |
| GCQE-004 | VAL-GCQE-005, VAL-GCQE-006 | Prove four-state runner semantics and require all-files pre-commit, formatter review, rerun, and lane-by-lane handoff across canonical governance and consumers. | platform | Queued | Not executed. | Runner/result unit tests, governance assertion RED/GREEN, strict docs, aggregate, and all-files evidence will be recorded here. |
| GCQE-005 | VAL-GCQE-001 through VAL-GCQE-006 | Run focused, affected, staged, production, strict, aggregate, and unqualified all-files lanes; obtain independent requirements and quality/security reviews; remediate findings. | platform | Queued | Not executed. | Exact commands, per-lane results, reviewer identities/dispositions, commits, limitations, and residual risk will be recorded here. |
| GCQE-006 | VAL-GCQE-001 through VAL-GCQE-006 | Close Spec/Plan/Task and program lineage atomically, run explicit-ref lifecycle and clean-tree postflight, and retain hosted CI as historical FAIL/current DEFER. | platform | Queued | Not executed. | Terminal lifecycle package, closure commit, explicit-ref and clean-tree repository-static evidence will be recorded here. |

## Approval and Safety Boundaries

- **Allowed Paths**: Spec 039 and its reciprocal Stage 04 Plan/Task/index
  lineage; the settled migration snapshot is read-only validation input;
  `.github/workflows/ci.yml`,
  `.github/workflows/generate-changelog.yml`,
  `.github/requirements/ci-validation.txt`, `.github/ABOUT.md`,
  `.github/PULL_REQUEST_TEMPLATE.md`; the focused CI, GitOps, Actions,
  affected-surface, aggregate, runner, hook-result, unit-test, fixture,
  governance, operations-guide, script/test inventory, technology-inventory,
  and shared progress paths named in the Plan.
- **Forbidden Paths**: Provider gateways/adapters/models/roster; `.gemini/**`;
  Specs 040-046 implementation; Kubernetes/GitOps desired-state changes;
  infrastructure, Vault, ESO, Argo CD, deployment, release publication,
  branch-protection, credentials, secret values, ignored `_workspace`
  children, auth files, kubeconfigs, tokens, and shell history.
- **Approval Required**: Dependency installation, push, workflow dispatch,
  GitHub setting mutation, merge, publication, live command, credential access,
  secret handling, or expansion outside the exact Spec 039 paths requires
  separate explicit human approval.
- **Static Validation**: Focused unit tests; GitOps, CI-contract,
  affected-surface, Actions-security self-test and production modes; staged and
  explicit-ref lifecycle; strict registry/Markdown/link checks; repository
  aggregate; unqualified all-files pre-commit; formatter/status review; both
  diff checks.
- **Live Validation**: DEFER. No post-change hosted GitHub Actions, provider,
  Kubernetes, Vault, ESO, Argo CD, cloud, deployment, or credential result is
  authorized by this Task.
- **Secret / Vault Handling**: Do not open, print, copy, hash, or report secret
  values. Diagnostics and evidence contain only stable rule IDs,
  repository-relative paths, bounded metadata, commit identities, and public
  run identifiers.
- **Rollback Plan**: Revert the newest reviewed logical commit first: terminal
  closure, guidance/result contract, artifact retention, CI dependency and
  explicit pre-commit contract, FIFO portability, then activation last. Rerun
  focused and aggregate checks after every revert. Do not rewrite shared
  history or use destructive reset/clean operations.
- **Evidence Location**: This Task, the reciprocal Plan, reviewed logical
  commits, exact test/fixture files, repository-static command output,
  the byte-verified settled migration snapshot, and shared progress ledger.
  Temporary logs, subagent scratch, and hosted results for other SHAs are not
  current closure evidence.

## Verification Summary

Activation evidence contains the intentional creation RED:

```text
FAIL LIFECYCLE-CREATE
docs/04.execution/plans/2026-07-26-github-ci-qa-evidence.md
expected="exactly one Plan and one Task creation in the same proposal state 'active'"
observed="Plan count 1, Task count 0"
base_mode="staged"
```

The exact six-path reciprocal proposal passes staged lifecycle, registry
self-test and strict mode, strict Markdown profiles, strict cross-document
validation, settled RIA validation, cached diff check, and repository
aggregate. Activation commit
`2ddfe4b7697e998b41d3125be94cdc4cee295388` contains exactly those six paths,
and the post-commit repository aggregate passes at that HEAD. GCQE-001 through
GCQE-006 implementation results, terminal closure, and final clean-tree
postflight have not yet been observed. Raw all-files still fails only at the
Spec 039-owned FIFO limitation; strict-skip all-files rerun is used only after
direct aggregate proof for this activation package. Hosted run `29982910320`
remains historical FAIL for its exact SHA, while the current branch hosted lane
is DEFER.

## Traceability

- **Plan**:
  [GitHub CI and QA Evidence Implementation Plan](../plans/2026-07-26-github-ci-qa-evidence.md)
- **Spec**:
  [Spec 039](../../03.specs/039-github-ci-qa-evidence/spec.md)
- **Predecessor Task**:
  [Reference Information Architecture Task](./2026-07-22-reference-information-architecture.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [GCQE-000](../plans/2026-07-26-github-ci-qa-evidence.md#task-0-gcqe-000--reciprocal-spec-039-planning-activation) | Done — Plan-only lifecycle RED, prerequisite `cd726e0`, exact-six reciprocal GREEN, activation `2ddfe4b`, and post-commit aggregate PASS observed. | Rule `LIFECYCLE-CREATE`, Plan 1/Task 0, rollback parent `cd726e0`, staged lifecycle/registry/profile/link/RIA PASS, exact-six commit `2ddfe4b`, and HEAD aggregate PASS. |
| [VAL-GCQE-004](../../03.specs/039-github-ci-qa-evidence/spec.md#success-criteria--verification-plan) | Not executed. | GCQE-001 portable fixture unit/self-test evidence is pending. |
| N/A — GCQE-002 shares the Plan linked in GCQE-000 | Not executed. | CI dependency, workflow, selector, and validator evidence is pending. |
| N/A — GCQE-003 shares the Plan linked in GCQE-000 | Not executed. | Artifact-retention fixture and repository evidence is pending. |
| N/A — GCQE-004 shares the Plan linked in GCQE-000 | Not executed. | Four-state and all-files/formatter guidance evidence is pending. |
| N/A — GCQE-005 shares the Plan linked in GCQE-000 | Not executed. | Aggregate lanes and independent review evidence is pending. |
| N/A — GCQE-006 shares the Plan linked in GCQE-000 | Not executed. | Terminal lifecycle and clean-tree postflight evidence is pending. |
