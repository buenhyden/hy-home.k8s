---
title: 'Task: GitHub CI and QA Evidence'
type: sdlc/task
status: done
owner: platform
updated: 2026-07-27
---

# Task: GitHub CI and QA Evidence

## Overview

This Task is the execution, verification, review, rollback, and handoff evidence
owner for GCQE-000 through GCQE-006. It records
[Spec 039](spec.md) from approved
design, activation, and rollback parent
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

GCQE-001 through GCQE-005 are complete through reviewed implementation and
integration evidence at `aaee364`. Test-only final-tranche lifecycle-fixture
commit `096c5c48e364663c616a1984089c11a1fe5b3b61` received `REQUIREMENTS
COMPLIANT` / `QUALITY APPROVED` from
`/root/gcqe006_selftest_rapid_review`. Active-corpus frontier commit
`b5c3eea128b8b3be7c858f70803f83994be1fc77` received `REQUIREMENTS
COMPLIANT` from `/root/gcqe006_frontier_requirements_review` and `QUALITY
APPROVED` from `/root/gcqe006_frontier_quality_review`. Test-only
index-bound current/advanced assertion commit
`39e6150a6f7a79b710d0e2cd7bc2dee8349f871a` received fresh `REQUIREMENTS
COMPLIANT` from `/root/gcqe006_test_compat_requirements_review` and `QUALITY
APPROVED` from `/root/gcqe006_test_compat_fresh_quality`. These approvals are
scoped to their compatibility changes, not the whole terminal tranche.

GCQE-006 closed on 2026-07-27 in
`e1d1e910840337327a557ab4b84e86f8fced11d6`. That commit contains exactly the
Spec, Plan, Task, their three indexes, the document-profile registry, and
shared progress paths listed by Plan Task 6; the registry-owned PRD-006
program-lineage state for Spec 039 is terminal while Spec 040 remains
`active`. The 46-test residue class, 84-test module, 22-case residue self-test,
exact advanced production frontier, repository aggregate, 668-case lifecycle
self-test, and Step 2 staged/strict gates passed; the settled migration
snapshot remains byte-identical. After the sole invalid explicit-ref finding
was closed, `/root/gcqe006_final_requirements` returned `REQUIREMENTS
COMPLIANT` and `/root/gcqe006_final_quality` returned `QUALITY APPROVED`, with
no findings against corrected patch digest
`58640a0d26c08b4ab5872c0a69be2966610f796b4b1e906a5e3ebae0033758cc`.
Step 6 then passed explicit-ref lifecycle using the raw activation and closure
OIDs, CI Python production at `3` jobs / `3` pins, GitHub Actions security,
GitOps self-test, clean-tree repository aggregate, and all applicable
all-files hooks. Dockerfile lint was a no-file `SKIP`; status, diff, and
diff-check inspection were clean. Hosted run `29982910320` remains historical
FAIL evidence for its older SHA, while current hosted, provider, and live
evidence remains `DEFER`. This later evidence update does not identify or
claim its own commit.

## Inputs

- [GitHub CI and QA Evidence Implementation Plan](plan.md)
- [Spec 039](spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [ADR-0017](../../02.architecture/decisions/0017-program-follow-up-lineage-semantics.md)
- [Affected-surface contract](../../00.agent-governance/contracts/validation-surfaces.json)
- [Agent quality standards](../../00.agent-governance/rules/quality-standards.md)
- [Git workflow](../../00.agent-governance/rules/git-workflow.md)
- [GitHub configuration hub](../../../.github/README.md)
- [Technology version inventory](../../90.references/data/tech-stack-version-inventory.md)
- `docs/90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md`; [current lookup](../../90.references/research/2026-08-08-wer/source-coverage-and-migration-ledger.md)
- [Predecessor Spec 038 Task](../038-reference-information-architecture/tasks.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| GCQE-000 | Activation gate | Preserve the settled migration snapshot, then activate the reciprocal Spec 039 Plan/Task pair, direct backlinks, Stage 04 indexes, and shared progress handoff as one exact six-path package. | platform | Done | Plan-only lifecycle RED, the ledger/admission contract collision, prerequisite commit `cd726e0`, exact-six reciprocal GREEN, activation commit `2ddfe4b`, and post-commit aggregate PASS are observed. | `LIFECYCLE-CREATE`, Plan count 1/Task count 0; protected-ledger RIA failure; rollback parent `cd726e0`; staged lifecycle/registry/profile/link/RIA PASS; exact-six commit `2ddfe4b`; HEAD aggregate PASS; raw all-files fails only at the existing FIFO limitation. |
| GCQE-001 | VAL-GCQE-004 | Add a capability-aware FIFO/directory non-regular fixture, preserve `RESOURCE_NOT_REGULAR`, and re-raise unexpected filesystem errors. | platform | Done | Portable FIFO/directory fallback and regular nested-Kustomization dispatch are implemented in `d0d788d`; the first review finding was corrected and fresh re-review approved. | Focused six-test GREEN, GitOps self-test/production, aggregate, staged and all-files PASS; rollback unit `d0d788d`. |
| GCQE-002 | VAL-GCQE-001, VAL-GCQE-002, VAL-GCQE-003 | Add the exact CI Python requirements owner and validator; pin Python 3.12; replace `pre-commit/action`; preserve workflow entry, aggregate, and full-document selection. | platform | Done | Exact three-pin CI owner, Python 3.12/full-history workflow contract, explicit all-files execution, selector fixture, and fail-closed outside-job ownership are implemented in `b2bf4a8`; fresh re-review approved. | Final 12-test CI-contract GREEN, self-test `7` rules/`9` cases, production `3` jobs/`3` pins, affected/Actions/aggregate/all-files PASS; rollback unit `b2bf4a8`. |
| GCQE-003 | VAL-GCQE-003 | Enforce integer seven-day retention on every upload-artifact step and set the changelog preview producer accordingly. | platform | Done | Exact integer seven-day retention, hostile container-shape handling, and case-insensitive upload-artifact matching are implemented in `bca57ae`; two review corrections received final fresh approval. | Four external fixture cases plus internal hostile regressions, Actions self-test/production, aggregate, staged and all-files PASS; rollback unit `bca57ae`. |
| GCQE-004 | VAL-GCQE-005, VAL-GCQE-006 | Prove four-state runner semantics and require all-files pre-commit, formatter review, rerun, and lane-by-lane handoff across canonical governance and consumers. | platform | Done | Four-state semantics and the canonical eight-step completion sequence are implemented in `8621e88`; the coupled guide-index correction was included and independent review approved. | Final 16-test runner/result/provider GREEN, strict documents, aggregate, staged and unqualified all-files PASS; rollback unit `8621e88`. |
| GCQE-005 | VAL-GCQE-001 through VAL-GCQE-006 | Run focused, affected, staged, production, strict, aggregate, and unqualified all-files lanes; obtain independent requirements and quality/security reviews; remediate findings. | platform | Done | The first cumulative affected lane exposed the closed-environment classifier failure; `b329016` added securely discovered Gitleaks and hosted static provisioning. Reviewer `/root/gcqe_005_remediation_reviewer` requested changes for effective execute classes; follow-up `7b536d1` corrected them and fresh re-review approved. Whole-tranche requirements and quality/security reviews then approved the exact staged proposal. | Initial affected result: `9` PASS/`1` FAIL at 26 paths; the later `MM` index-boundary FAIL is preserved. Final focused/direct, 30-path affected, staged, aggregate, unqualified all-files, formatter, and diff gates passed. Reviewer `/root/gcqe_005_requirements_review` returned REQUIREMENTS COMPLIANT; reviewer `/root/gcqe_005_quality_security_review` returned QUALITY APPROVED. Both reported no findings against package `f4d50ec…`; hosted/provider/live remain DEFER. |
| GCQE-006 | VAL-GCQE-001 through VAL-GCQE-006 | Close Spec/Plan/Task and program lineage atomically, run explicit-ref lifecycle and clean-tree postflight, and retain hosted CI as historical FAIL/current DEFER. | platform | Done | Exact eight-file closure commit `e1d1e910840337327a557ab4b84e86f8fced11d6` and Steps 2 through 6 passed. | From base `39e6150a6f7a79b710d0e2cd7bc2dee8349f871a`, compatibility commits `096c5c4`, `b5c3eea`, and `39e6150` retain scoped approved reviews. Advanced verification passed residue class `46`, module `84`, self-test `22`, production `active=0/0`, `terminal=4/2`, terminal Specs `2`, guards `13/29`, aggregate final marker, lifecycle `668`, staged lifecycle, registry self-test `119`/strict `448`, Markdown strict, strict links/owners, and diff checks. Spec/Plan/Task, three indexes, and registry program-lineage Spec 039 are `done`; Spec 040 remains `active`, and the settled snapshot is unchanged. The sole invalid explicit-ref finding is closed; `/root/gcqe006_final_requirements` returned `REQUIREMENTS COMPLIANT` and `/root/gcqe006_final_quality` returned `QUALITY APPROVED` with no findings against digest `58640a0d…`. Explicit-ref lifecycle passed from activation `2ddfe4b7697e998b41d3125be94cdc4cee295388` to closure `e1d1e910840337327a557ab4b84e86f8fced11d6`; CI Python reported `3` jobs / `3` pins; Actions security, GitOps self-test, clean-tree aggregate, and applicable all-files hooks passed; Dockerfile lint was a no-file `SKIP`; status/diff/diff-check inspection was clean. Historical hosted run `29982910320` remains FAIL for its older SHA; current hosted/provider/live remains `DEFER`. |

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
- **Rollback Plan**: Revert closure commit
  `e1d1e910840337327a557ab4b84e86f8fced11d6` first, then
  `39e6150`, `b5c3eea`, `096c5c4`, `aaee364`, `7b536d1`, `b329016`,
  `8621e88`, `bca57ae`, `b2bf4a8`, `d0d788d`, `4aaaa4b`, `50d04e4`,
  `9bb74ce`, and activation `2ddfe4b` last. This is the complete exact
  newest-first chain. Rerun focused and aggregate checks after every revert.
  Do not rewrite shared history or use destructive reset/clean operations.
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
GCQE-005 is Done. GCQE-006 has prepared the refreshed exact eight-file terminal
proposal at base HEAD `39e6150a6f7a79b710d0e2cd7bc2dee8349f871a`.
The review history remains explicit:

- First-pass requirements reviewer
  `/root/gcqe006_terminal_requirements_review` returned `NOT COMPLIANT`, and
  rapid quality reviewer `/root/gcqe006_terminal_quality_rapid` returned
  `CHANGES REQUESTED`, because the rollback chain omitted reviewed commits.
- Original quality reviewer `/root/gcqe006_terminal_quality_review` returned
  `QUALITY NOT APPROVED` because the old active-corpus frontier made the
  aggregate fail against the staged advanced proposal.
- Commit `b5c3eea` remediated that frontier and received scoped frontier
  requirements/quality approval. Its first staged full-class run then exposed
  three old-state production assertions. The first test-compat review also
  raised a P1 because current/advanced expectations were not bound to exact
  index object identities.
- Commit `39e6150` remediated the three assertions and index-OID P1. Fresh
  test-compat reviewers returned `REQUIREMENTS COMPLIANT` and `QUALITY
  APPROVED`; these are scoped compatibility verdicts, not terminal approval.
- Final whole-tranche reviewer `/root/gcqe006_final_requirements` returned
  `REQUIREMENTS NOT COMPLIANT`, and reviewer
  `/root/gcqe006_final_quality` returned `QUALITY NOT APPROVED`, solely because
  Plan Task 6 Step 6 used invalid explicit-ref flag names and passed
  `git-sha1:` evidence labels where the CLI requires raw refs or OIDs. Step 6
  now uses `--from-ref` and `--to-ref`, fixes the activation side to the exact
  raw 40-hex OID, and requires replacement of the closure placeholder with its
  observed raw 40-hex OID before execution.
- Fresh whole-tranche reviewer `/root/gcqe006_final_requirements` returned
  `REQUIREMENTS COMPLIANT`, and reviewer `/root/gcqe006_final_quality`
  returned `QUALITY APPROVED`, with no findings against corrected staged patch
  digest
  `58640a0d26c08b4ab5872c0a69be2966610f796b4b1e906a5e3ebae0033758cc`.
  The sole invalid explicit-ref finding is closed and Step 3 is complete.

The refreshed proposal passed the residue class `46/46`, full module `84/84`,
residue self-test `22`, exact advanced production counts, repository aggregate
with `[PASS] repository quality gates passed`, lifecycle self-test `668`,
staged lifecycle, registry self-test/strict, strict Markdown, strict
links/owners, and both diff checks. Fresh whole-tranche terminal reviews are
approved. The terminal repository quality gate and unqualified all-files
pre-commit passed with every applicable hook green, Dockerfile lint skipped
for no files, no formatter mutation, exactly eight staged paths, no unstaged
changes, and both diff checks green. Step 5 produced exact eight-path closure
commit `e1d1e910840337327a557ab4b84e86f8fced11d6`. Step 6 passed explicit-ref
lifecycle from raw activation OID
`2ddfe4b7697e998b41d3125be94cdc4cee295388` to that raw closure OID, CI Python
production at `3` jobs / `3` pins, GitHub Actions security, GitOps self-test,
the clean-tree repository aggregate, and every applicable all-files hook.
Dockerfile lint remained a no-file `SKIP`; status, diff, and diff-check
inspection were clean. Hosted run `29982910320` remains historical FAIL for
its exact older SHA, while the current branch hosted, provider, and live lanes
remain `DEFER`. This evidence update does not identify or claim its own commit.

## Traceability

- **Plan**:
  [GitHub CI and QA Evidence Implementation Plan](plan.md)
- **Spec**:
  [Spec 039](spec.md)
- **Predecessor Task**:
  [Reference Information Architecture Task](../038-reference-information-architecture/tasks.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [GCQE-000](plan.md#task-0-gcqe-000--reciprocal-spec-039-planning-activation) | Done — Plan-only lifecycle RED, prerequisite `cd726e0`, exact-six reciprocal GREEN, activation `2ddfe4b`, and post-commit aggregate PASS observed. | Rule `LIFECYCLE-CREATE`, Plan 1/Task 0, rollback parent `cd726e0`, staged lifecycle/registry/profile/link/RIA PASS, exact-six commit `2ddfe4b`, and HEAD aggregate PASS. |
| [VAL-GCQE-004](spec.md#success-criteria--verification-plan) | Done in `d0d788d`. | Portable non-regular fixture, exact diagnostic, focused six-test GREEN, and fresh review approval observed. |
| N/A — GCQE-002 shares the Plan linked in GCQE-000 | Done in `b2bf4a8`. | Exact CI Python owner/workflow/selector contract, final 12-test GREEN, aggregate/all-files PASS, and fresh review approval observed. |
| N/A — GCQE-003 shares the Plan linked in GCQE-000 | Done in `bca57ae`. | Exact seven-day retention, hostile-shape/case regressions, aggregate/all-files PASS, and final fresh review approval observed. |
| N/A — GCQE-004 shares the Plan linked in GCQE-000 | Done in `8621e88`. | Four-state and eight-step completion evidence, strict/aggregate/all-files PASS, and independent approval observed. |
| N/A — GCQE-005 shares the Plan linked in GCQE-000 | Done through `7b536d1` plus the reviewed staged evidence proposal. | Initial classifier and index-boundary failures, remediation `b329016`, reviewer CHANGES REQUESTED, follow-up `7b536d1`, fresh remediation APPROVED, final cumulative repository-static PASS, REQUIREMENTS COMPLIANT, and QUALITY APPROVED are observed. |
| N/A — GCQE-006 shares the Plan linked in GCQE-000 | Done through Step 6. | Exact eight-file closure `e1d1e910840337327a557ab4b84e86f8fced11d6` retains advanced residue `46/84/22`, exact `0/0` active and `4/2` terminal controls, aggregate, lifecycle `668`, staged/strict document gates, terminal repository quality/all-files gates, and diff checks. Rollback, old-frontier, three old-state assertion, index-OID P1, and sole invalid explicit-ref findings remain recorded and remediated. Reviewers `/root/gcqe006_final_requirements` and `/root/gcqe006_final_quality` returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with no findings against digest `58640a0d…`. Explicit-ref lifecycle passed from activation `2ddfe4b7697e998b41d3125be94cdc4cee295388`; CI Python `3` jobs / `3` pins, Actions security, GitOps self-test, clean-tree aggregate, and applicable all-files hooks passed; Dockerfile lint was a no-file `SKIP`; status/diff/diff-check inspection was clean. Spec 040 remains active, the settled snapshot is unchanged, and current hosted/provider/live remains `DEFER`. |
