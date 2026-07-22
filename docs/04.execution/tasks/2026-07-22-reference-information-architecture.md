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
Stage 04 document, so this pair raised the corpus to 50 Plans and 52 Tasks.
RIA-000 and RIA-001 are Completed from observed commits and clean final reviews.
RIA-002 is In Progress at reviewed design correction only; its implementation
RED has not begun. Later rows remain Queued until their own test-first result,
independent reviews, and logical commit are directly observed.

The activation preserves the existing registry as the sole Current audit and
research pack owner. It authorizes a separate reference-information contract
only for observation immutability, Current overlay mutability, source and
freshness evidence, generator relations, and duplicate-owner rules. It does
not authorize observation rewriting, CI/FIFO work, live checks, ignored
scratch inspection, or Specs 039-046 activation.

RIA-002 design preflight at reviewed RIA-001 head
`15bba3d436ee2818f29d6f6880c7d5c4901aa0fe` found that the original
`8fb9821497aaa93d9ed5fc1a69b60c628b047b47` Current baseline could not pass:
activation commit `cb0c1f6` changed the protected research migration ledger's
inventory boundary from 444 to 446 outside all allowed projections. Work
stopped before RIA-002 RED or implementation. This correction requires schema
version 2, separate Historical and Current baselines, and a one-shot
transition/durable-settlement chain; it records no implementation result.
Design correction commit `08cf17d` received `QUALITY CHANGES REQUIRED` with
four Important findings. This follow-up proposal addresses settlement lineage,
stage-zero proposed authority, the code-owned root FSM, and execution-status
truth; clean follow-up approval is not yet claimed.

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
| RIA-000 | Activation gate | Commit the exact seven-file reciprocal Plan/Task activation with staged lifecycle, complete per-commit QA, independent planning re-reviews, evidence baseline `8fb9821`, and rollback parent `fdc86ee`. | platform | Completed | Activation completed. | Commit `cb0c1f6`; exact seven-file scope; Plan-only `LIFECYCLE-CREATE` RED, focused GREEN, final `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, findings none. |
| RIA-001 | VAL-RIA-001 | Add the closed Draft 2020-12 reference schema/contract, safe loader, stable diagnostics, CLI self-test, and hostile boundary fixtures without duplicating Current member paths, digests, or pointers. | platform | Completed | Contract bootstrap and safe validator completed. | Commits `68e46fc`, `566c74f`, `15bba3d`; focused unit, CLI self-test/production, schema/instance PASS; final `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, findings none. Historical raw hook output and remote/live PASS are not claimed. |
| RIA-002 | VAL-RIA-002, VAL-RIA-003 | Implement schema-v2 Historical/Current separation, stage-zero proposed authority, exact root FSM, bounded overlay, and one-shot ledger transition/durable settlement lineage. | platform | In Progress | Design correction reviewed; implementation RED not begun. | Preflight: `8fb9821` fails the `cb0c1f6` ledger 444 -> 446 change; immutable Current root is `15bba3d`. `08cf17d` review returned four Important findings; this follow-up incorporates bounded staged C2 equality, literal C3 parent proof, index/worktree hostility, and root/open/settled tests. Follow-up approval and implementation remain pending. |
| RIA-003 | VAL-RIA-004 | Enforce repo evidence, HTTPS source, checked date, adopted/rejected scope, and refresh trigger for every current data asset. | platform | Queued | Not executed. | Named source-ledger RED selectors, production data inventory, complete commit gate, and task review are required. |
| RIA-004 | VAL-RIA-005 | Enforce one fixed-argv generator/input/output/check relation and zero LLM Wiki drift. | platform | Queued | Not executed. | Named generator relation/command/drift RED selectors, direct no-diff, complete commit gate, and task review are required. |
| RIA-005 | VAL-RIA-001, VAL-RIA-006 | Reject duplicate Current and generated/manual owners plus normalized active-policy copies, with only exact pair-scoped structural exceptions. | platform | Queued | Not executed. | Named duplicate/copy/exception-reuse RED selectors, zero production findings, complete commit gate, and task review are required. |
| RIA-006 | VAL-RIA-001 through VAL-RIA-006 | Integrate self-test-before-production validation into repository aggregate QA and command inventories. | platform | Queued | Not executed. | Exact aggregate invocation RED/GREEN, full aggregate, complete commit gate, independent review, and logical integration commit are required. |
| RIA-007 | VAL-RIA-001 through VAL-RIA-006 | Run full/all-files QA and independent whole-tranche review, then close through C1 six-file lifecycle closure, C2 eight-file postflight ledger transition, and C3 contract-only settlement. | platform | Queued | Not executed. | Requires exact verdicts and gates, C1 postflight with ledger untouched, C2 open transition with no self-claim, C3 proof naming literal C2, terminal `--require-settled-baselines`, rollback C3 -> C2 -> C1, and clean status. |

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
  formatter-diff review, `git diff --check`, and terminal
  `--require-settled-baselines` validation.
- **Live Validation**: `DEFER`. Repository-static results do not prove provider,
  GitHub-hosted, Kubernetes, Vault, ESO, Argo CD, credential, or live state.
- **Secret / Vault Handling**: Do not open or print secret values. Diagnostics
  contain only stable rule IDs, repository-relative paths, and bounded facts;
  ignored scratch is never an evidence source.
- **Rollback Plan**: Reverse newest reviewed logical commit first. Before
  closure, revert the failing RIA package only. After closure, revert the
  contract-only C3 settlement, eight-file C2 transition/postflight evidence,
  six-file C1 closure, then RIA-006 through RIA-001 and activation last; restore
  each protected owner relation before removing its guard.
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
without skipped hooks or formatter changes. Clean planning re-reviews followed,
and activation commit `cb0c1f6` completed RIA-000.

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
`QUALITY APPROVED` with no Critical, Important, or Minor findings. Activation
commit `cb0c1f6` completed RIA-000.

RIA-001 completed through `68e46fc`, `566c74f`, and `15bba3d`. Its final
focused reviews returned `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED` with
no findings; focused unit, CLI self-test/production, and Draft 2020-12
schema/instance checks passed. Historical raw hook output, CI, remote, and live
execution are not reconstructed or claimed. RIA-003 through RIA-007 remain
Queued. Existing Current-pack validation and the LLM Wiki no-diff check remain
reusable controls only; they do not prove later criteria.

RIA-002 preflight additionally proved a design blocker, not a RED result. The
single `8fb9821` pin predates activation commit `cb0c1f6`, whose protected
Current research ledger update changed 444 inventory rows to 446 outside the
overlay model. The corrected design retains `8fb9821` only for five
Historical/Resolved audit packs and `research/2026-07-04-wer`; the immutable
code-owned Current root is `15bba3d`, and future ledger advancement requires
the root/open/settled FSM and staged/explicit-ref lineage chain. RIA-002 is In
Progress at design review only. Correction commit `08cf17d` received
`QUALITY CHANGES REQUIRED` with four Important findings; this follow-up closes
those design gaps, but follow-up approval and implementation RED/GREEN are not
claimed. No RIA-002 implementation commit, CI, remote, or live result exists.

## Traceability

- **Plan**: [Reference Information Architecture Implementation Plan](../plans/2026-07-22-reference-information-architecture.md)
- **Spec**: [Spec 038](../../03.specs/038-reference-information-architecture/spec.md)
- **Predecessor Task**: [Active Corpus and Execution Retention Task](./2026-07-18-active-corpus-and-execution-retention.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [RIA-000](../plans/2026-07-22-reference-information-architecture.md#task-0-ria-000--atomic-reciprocal-planning-activation) | Completed. | Commit `cb0c1f6`; exact seven-file activation, Plan-only lifecycle RED, focused GREEN, final `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, findings none. |
| [RIA-001](../../03.specs/038-reference-information-architecture/spec.md#success-criteria--verification-plan) | Completed. | Commits `68e46fc`, `566c74f`, and `15bba3d`; focused unit, CLI, schema/instance PASS; final `REQUIREMENTS COMPLIANT` and `QUALITY APPROVED`, findings none. Historical raw hook, CI, remote, and live PASS are not claimed. |
| N/A — RIA-002 shares the Plan linked in RIA-000 | In Progress. | Preflight blocker recorded (`8fb9821` versus `cb0c1f6`, ledger 444 -> 446); `08cf17d` review returned four Important findings. Corrected FSM/index/lineage design is pending clean follow-up approval, and implementation RED has not begun. |
| N/A — RIA-003 shares the Plan linked in RIA-000 | Queued. | Source/scope/freshness validation is not implemented. |
| N/A — RIA-004 shares the Plan linked in RIA-000 | Queued. | Generated ownership and no-diff validation are not implemented. |
| N/A — RIA-005 shares the Plan linked in RIA-000 | Queued. | Duplicate Current/generated/manual/policy-owner validation is not implemented. |
| N/A — RIA-006 shares the Plan linked in RIA-000 | Queued. | Aggregate integration and command inventory changes are not implemented. |
| N/A — RIA-007 shares the Plan linked in RIA-000 | Queued. | Whole-tranche review and the C1 six-file closure, C2 eight-file transition evidence, and C3 contract-only settlement are pending. |
