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
| GCQE-001 | VAL-GCQE-004 | Add a capability-aware FIFO/directory non-regular fixture, preserve `RESOURCE_NOT_REGULAR`, and re-raise unexpected filesystem errors. | platform | Done | Portable FIFO/directory fallback and regular nested-Kustomization dispatch are implemented in `d0d788d`; the first review finding was corrected and fresh re-review approved. | Focused six-test GREEN, GitOps self-test/production, aggregate, staged and all-files PASS; rollback unit `d0d788d`. |
| GCQE-002 | VAL-GCQE-001, VAL-GCQE-002, VAL-GCQE-003 | Add the exact CI Python requirements owner and validator; pin Python 3.12; replace `pre-commit/action`; preserve workflow entry, aggregate, and full-document selection. | platform | Done | Exact three-pin CI owner, Python 3.12/full-history workflow contract, explicit all-files execution, selector fixture, and fail-closed outside-job ownership are implemented in `b2bf4a8`; fresh re-review approved. | Final 12-test CI-contract GREEN, self-test `7` rules/`9` cases, production `3` jobs/`3` pins, affected/Actions/aggregate/all-files PASS; rollback unit `b2bf4a8`. |
| GCQE-003 | VAL-GCQE-003 | Enforce integer seven-day retention on every upload-artifact step and set the changelog preview producer accordingly. | platform | Done | Exact integer seven-day retention, hostile container-shape handling, and case-insensitive upload-artifact matching are implemented in `bca57ae`; two review corrections received final fresh approval. | Four external fixture cases plus internal hostile regressions, Actions self-test/production, aggregate, staged and all-files PASS; rollback unit `bca57ae`. |
| GCQE-004 | VAL-GCQE-005, VAL-GCQE-006 | Prove four-state runner semantics and require all-files pre-commit, formatter review, rerun, and lane-by-lane handoff across canonical governance and consumers. | platform | Done | Four-state semantics and the canonical eight-step completion sequence are implemented in `8621e88`; the coupled guide-index correction was included and independent review approved. | Final 16-test runner/result/provider GREEN, strict documents, aggregate, staged and unqualified all-files PASS; rollback unit `8621e88`. |
| GCQE-005 | VAL-GCQE-001 through VAL-GCQE-006 | Run focused, affected, staged, production, strict, aggregate, and unqualified all-files lanes; obtain independent requirements and quality/security reviews; remediate findings. | platform | Done | The first cumulative affected lane exposed the closed-environment classifier failure; `b329016` added securely discovered Gitleaks and hosted static provisioning. Reviewer `/root/gcqe_005_remediation_reviewer` requested changes for effective execute classes; follow-up `7b536d1` corrected them and fresh re-review approved. Whole-tranche requirements and quality/security reviews then approved the exact staged proposal. | Initial affected result: `9` PASS/`1` FAIL at 26 paths; the later `MM` index-boundary FAIL is preserved. Final focused/direct, 30-path affected, staged, aggregate, unqualified all-files, formatter, and diff gates passed. Reviewer `/root/gcqe_005_requirements_review` returned REQUIREMENTS COMPLIANT; reviewer `/root/gcqe_005_quality_security_review` returned QUALITY APPROVED. Both reported no findings against package `f4d50ec…`; hosted/provider/live remain DEFER. |
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
GCQE-004 are complete in `d0d788d`, `b2bf4a8`, `bca57ae`, and `8621e88`.
GCQE-005 first reproduced the closed-runner classifier failure rather than
substituting an ambient aggregate PASS. Remediation `b329016` made Gitleaks
available without broadening the closed PATH, and reviewer
`/root/gcqe_005_remediation_reviewer` then returned CHANGES REQUESTED for an
Important effective-execute-class gap. Follow-up `7b536d1` corrected that gap;
fresh remediation re-review is APPROVED. The current staged integration passed
focused, direct, strict, 30-path cumulative affected, staged, aggregate, and
unqualified all-files lanes with no formatter mutation. Requirements reviewer
`/root/gcqe_005_requirements_review` returned REQUIREMENTS COMPLIANT with no
finding; quality/security reviewer `/root/gcqe_005_quality_security_review`
returned QUALITY APPROVED with no finding. Both matched review package SHA-256
`f4d50ec45e7d977b22c55cd18f6d8e56bc6cf7436713980d1b1f09f38632cb38`.
GCQE-005 is Done. GCQE-006 is the queued next owner; terminal closure and
clean-tree postflight have not been observed. Hosted run `29982910320` remains
historical FAIL for its exact SHA, while the current branch hosted, provider,
and live lanes remain DEFER.

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
| [VAL-GCQE-004](../../03.specs/039-github-ci-qa-evidence/spec.md#success-criteria--verification-plan) | Done in `d0d788d`. | Portable non-regular fixture, exact diagnostic, focused six-test GREEN, and fresh review approval observed. |
| N/A — GCQE-002 shares the Plan linked in GCQE-000 | Done in `b2bf4a8`. | Exact CI Python owner/workflow/selector contract, final 12-test GREEN, aggregate/all-files PASS, and fresh review approval observed. |
| N/A — GCQE-003 shares the Plan linked in GCQE-000 | Done in `bca57ae`. | Exact seven-day retention, hostile-shape/case regressions, aggregate/all-files PASS, and final fresh review approval observed. |
| N/A — GCQE-004 shares the Plan linked in GCQE-000 | Done in `8621e88`. | Four-state and eight-step completion evidence, strict/aggregate/all-files PASS, and independent approval observed. |
| N/A — GCQE-005 shares the Plan linked in GCQE-000 | Done through `7b536d1` plus the reviewed staged evidence proposal. | Initial classifier and index-boundary failures, remediation `b329016`, reviewer CHANGES REQUESTED, follow-up `7b536d1`, fresh remediation APPROVED, final cumulative repository-static PASS, REQUIREMENTS COMPLIANT, and QUALITY APPROVED are observed. |
| N/A — GCQE-006 shares the Plan linked in GCQE-000 | Not executed. | Terminal lifecycle and clean-tree postflight evidence is pending. |
