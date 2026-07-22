---
title: 'Task: Reference Information Architecture'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-22
---

# Task: Reference Information Architecture

## Overview

This Task is the execution, verification, review, and rollback evidence owner
for RIA-000 through RIA-007. It activates the reciprocal Spec 038 execution
pair from reviewed activation and rollback parent
`fdc86ee9156a35f48d57916be4ecb3505e483a50`. Plan-only RED and the 49-Plan /
51-Task inventory were captured at evidence baseline
`8fb9821497aaa93d9ed5fc1a69b60c628b047b47`; prerequisite commits changed no
Stage 04 document, so this proposal raises the corpus to 50 Plans and 52 Tasks.
Every implementation row remains Queued until its own test-first result,
independent reviews, and logical commit are directly observed.

The activation preserves the existing registry as the sole Current audit and
research pack owner. It authorizes a separate reference-information contract
only for observation immutability, Current overlay mutability, source and
freshness evidence, generator relations, and duplicate-owner rules. It does
not authorize observation rewriting, CI/FIFO work, live checks, ignored
scratch inspection, or Specs 039-046 activation.

## Inputs

- [Reference Information Architecture Implementation Plan](../plans/2026-07-22-reference-information-architecture.md)
- [Spec 038](../../03.specs/038-reference-information-architecture/spec.md)
- [PRD-006](../../01.requirements/006-workspace-document-lifecycle-and-evidence-consolidation.md)
- [ARD-0009](../../02.architecture/requirements/0009-document-lifecycle-evidence-operating-model.md)
- [Current audit pack](../../90.references/audits/2026-07-11-weia/README.md)
- [Current research pack](../../90.references/research/2026-07-07-wer/README.md)
- [Document profile registry](../../99.templates/support/document-profiles.json)
- [Migration evidence ledger](../../90.references/research/2026-07-07-wer/document-migration-evidence-ledger.md)
- [Predecessor Spec 037 Task](./2026-07-18-active-corpus-and-execution-retention.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| RIA-000 | Activation gate | Commit the exact seven-file reciprocal Plan/Task activation with staged lifecycle, complete per-commit QA, independent planning re-reviews, evidence baseline `8fb9821`, and rollback parent `fdc86ee`. | platform | In Progress | Plan-only RED, focused GREEN, reviewed active-control prerequisite, full activation QA, requirements compliance, and quality approval observed; activation commit and postflight remain pending. | RED: `LIFECYCLE-CREATE`, Plan 1/Task 0. GREEN: staged lifecycle PASS, registry self-test 119, strict inventory 446, Markdown 0, links valid, active controls 2/1, changed/all-files pre-commit, Markdownlint, and both diff checks PASS. Final re-reviews: `REQUIREMENTS COMPLIANT`, `QUALITY APPROVED`, findings none. |
| RIA-001 | VAL-RIA-001 | Add the closed Draft 2020-12 reference schema/contract, safe loader, stable diagnostics, CLI self-test, and hostile boundary fixtures without duplicating Current member paths, digests, or pointers. | platform | Queued | Not executed. | Must begin with missing-target and malformed-contract RED cases, then pass focused unit, `Draft202012Validator` schema/instance, CLI self-test, production skeleton, complete commit gate, and review. |
| RIA-002 | VAL-RIA-002, VAL-RIA-003 | Protect Historical/Resolved audits, Historical research, and registry-derived Current members while allowing only the remediation body and exact table/link navigation projections. | platform | Queued | Not executed. | Must reject one-byte protected drift, fact-bearing README changes, member/digest duplication, invalid source objects, broad mutability, and exception reuse. |
| RIA-003 | VAL-RIA-004 | Enforce repo evidence, HTTPS source, checked date, adopted/rejected scope, and refresh trigger for every current data asset. | platform | Queued | Not executed. | Named source-ledger RED selectors, production data inventory, complete commit gate, and task review are required. |
| RIA-004 | VAL-RIA-005 | Enforce one fixed-argv generator/input/output/check relation and zero LLM Wiki drift. | platform | Queued | Not executed. | Named generator relation/command/drift RED selectors, direct no-diff, complete commit gate, and task review are required. |
| RIA-005 | VAL-RIA-001, VAL-RIA-006 | Reject duplicate Current and generated/manual owners plus normalized active-policy copies, with only exact pair-scoped structural exceptions. | platform | Queued | Not executed. | Named duplicate/copy/exception-reuse RED selectors, zero production findings, complete commit gate, and task review are required. |
| RIA-006 | VAL-RIA-001 through VAL-RIA-006 | Integrate self-test-before-production validation into repository aggregate QA and command inventories. | platform | Queued | Not executed. | Exact aggregate invocation RED/GREEN, full aggregate, complete commit gate, independent review, and logical integration commit are required. |
| RIA-007 | VAL-RIA-001 through VAL-RIA-006 | Run full/all-files QA and independent whole-tranche review, close Spec/Plan/Task atomically, then record clean-tree postflight in a separately gated evidence commit. | platform | Queued | Not executed. | Requires focused/production/generator, strict documents/lifecycle, aggregate, all-files, formatter/diff review, exact verdicts, closure commit, explicit-ref postflight, evidence-update gate, and clean status. |

## Approval and Safety Boundaries

- **Allowed Paths**: Spec 038 and its Stage 03 index; this reciprocal Plan and
  Task plus Stage 04 indexes; the migration evidence ledger; a focused Stage
  90 reference IA schema/contract; focused validator, tests, fixtures, and
  script/test inventories; the aggregate quality script; exact Stage 90
  category/pack/reference files only when a validator finding proves the
  bounded correction required by Spec 038.
- **Forbidden Paths**: Historical/Resolved/Current observation rewrites;
  Current pack membership or pointer duplication; CI workflow and FIFO changes
  owned by Spec 039; compatibility removal owned by Spec 040; provider-agent,
  Kubernetes, infrastructure, GitOps, secret, or live-runtime changes; ignored
  `_workspace` children; credentials, tokens, kubeconfigs, auth files, and
  shell history; Specs 039-046 activation.
- **Approval Required**: Push, merge, publication, remote GitHub action, live
  system action, secret handling, dependency installation, or scope expansion
  beyond the approved Spec/Plan requires separate explicit human approval.
- **Static Validation**: Focused unit/self-test/production reference checks,
  generated LLM Wiki no-diff, strict registry/Markdown/cross-document and
  staged lifecycle checks, repository aggregate, all-files pre-commit,
  formatter-diff review, and `git diff --check`.
- **Live Validation**: `DEFER`. Repository-static results do not prove provider,
  GitHub-hosted, Kubernetes, Vault, ESO, Argo CD, credential, or live state.
- **Secret / Vault Handling**: Do not open or print secret values. Diagnostics
  contain only stable rule IDs, repository-relative paths, and bounded facts;
  ignored scratch is never an evidence source.
- **Rollback Plan**: Reverse newest reviewed logical commit first. Before
  closure, revert the failing RIA package only. After closure, revert the
  evidence-update commit, closure, then RIA-006 through RIA-001 and activation
  last; restore each protected owner relation before removing its guard.
- **Evidence Location**: This Task, reviewed logical commits, the Stage 90
  reference IA contract, focused tests/fixtures, aggregate results, and terminal
  lifecycle records. Temporary output and subagent scratch are not closure
  evidence.

## Verification Summary

The intentional activation RED staged only the new active Plan and ran
`python3 scripts/validate-document-lifecycle.py --root . --mode staged`.
It exited `1` with `LIFECYCLE-CREATE`, expected exactly one Plan and one Task
creation in state `active`, and observed `Plan count 1, Task count 0`. No
implementation criterion, review verdict, remote/live result, or closure is
claimed from that RED.

The complete activation proposal adds this reciprocal Task, links the active
Spec to the pair, updates the Spec/Plan/Task indexes, and updates the exact
14-column migration ledger. The registry relation was already active and is
not changed. Focused activation GREEN is directly observed: staged lifecycle,
registry self-test 119, strict 446-path inventory, strict Markdown zero,
cross-document valid, changed-file Markdownlint, and cached diff all passed.
The first activation commit-gate run exposed the Spec 037
`CLOSURE-CURRENT-RESIDUE` follow-on admission defect and a Git-SHA
detect-secrets false positive. Separately reviewed prerequisite commits
`5ed6de6` and `fdc86ee` now keep the frozen 100-row terminal ledger unchanged,
reject unadmitted Stage 04 artifacts, and admit only a complete active pair.
The contract example uses `git-sha1:`. With the seven files restaged, the
residue validator passed with `active_controls=2/1`; exact changed-file and
all-files pre-commit, formatter/status inspection, and both diff checks passed
without skipped hooks or formatter changes. Clean planning re-reviews,
activation commit, and postflight remain pending.

Initial independent requirements review returned
`REQUIREMENTS CHANGES REQUIRED`: it required RIA-000 and complete
all-files/formatter/diff gates before every logical commit. Initial independent
quality review returned `QUALITY CHANGES REQUIRED`: it required runtime-derived
Current membership, Historical research and README projections, pair-scoped
exceptions, adopted/rejected source scope, exact Draft 2020-12 validation,
separate source/generator/duplicate packages, an exact aggregate test, and the
ledger freshness count correction. Those findings are incorporated into the
current proposal. The first re-review returned `REQUIREMENTS COMPLIANT` and
`QUALITY CHANGES REQUIRED`; quality required an anchored `git-sha1:`
schema/parser, immediate activation/rollback parent `fdc86ee`, and fixed
`/usr/bin/git` argv, closed environment, timeout, output/size bounds, and strict
tree/blob parsing. Those corrections are incorporated. Final focused
re-reviews returned `REQUIREMENTS COMPLIANT` and
`QUALITY APPROVED` with no Critical, Important, or Minor findings. The
activation commit and postflight remain pending.

RIA-001 through RIA-007 are Queued. The existing Current-pack validation and
LLM Wiki no-diff check are reusable baseline controls only; they do not prove
the missing immutability, overlay, source/freshness, generator-relation, or
duplicate-owner criteria.

## Traceability

- **Plan**: [Reference Information Architecture Implementation Plan](../plans/2026-07-22-reference-information-architecture.md)
- **Spec**: [Spec 038](../../03.specs/038-reference-information-architecture/spec.md)
- **Predecessor Task**: [Active Corpus and Execution Retention Task](./2026-07-18-active-corpus-and-execution-retention.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [RIA-000](../plans/2026-07-22-reference-information-architecture.md#task-0-ria-000--atomic-reciprocal-planning-activation) | In Progress. | Plan-only lifecycle RED, focused activation GREEN, reviewed active-control prerequisite, `active_controls=2/1`, changed/all-files QA PASS, requirements compliance, and quality approval are observed; commit and postflight are pending. |
| [RIA-001](../../03.specs/038-reference-information-architecture/spec.md#success-criteria--verification-plan) | Queued. | Closed contract, loader, CLI, and hostile boundary fixtures are not implemented. |
| N/A — RIA-002 shares the Plan linked in RIA-000 | Queued. | Audit/research observation and exact overlay/navigation projection guards are not implemented. |
| N/A — RIA-003 shares the Plan linked in RIA-000 | Queued. | Source/scope/freshness validation is not implemented. |
| N/A — RIA-004 shares the Plan linked in RIA-000 | Queued. | Generated ownership and no-diff validation are not implemented. |
| N/A — RIA-005 shares the Plan linked in RIA-000 | Queued. | Duplicate Current/generated/manual/policy-owner validation is not implemented. |
| N/A — RIA-006 shares the Plan linked in RIA-000 | Queued. | Aggregate integration and command inventory changes are not implemented. |
| N/A — RIA-007 shares the Plan linked in RIA-000 | Queued. | Whole-tranche review, atomic closure, postflight, and evidence update are pending. |
