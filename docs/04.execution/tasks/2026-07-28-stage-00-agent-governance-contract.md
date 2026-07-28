---
title: 'Task: Stage 00 Agent Governance Contract'
type: sdlc/task
status: active
owner: platform
updated: 2026-07-28
---

# Task: Stage 00 Agent Governance Contract

## Overview

This Task is the durable result ledger for the
[Spec 041 Plan](../plans/2026-07-28-stage-00-agent-governance-contract.md).
It tracks reciprocal activation, closed schema and fixtures, current/target
contract data, explicit memory classes, consumer migration, derived governance,
complete repository QA, independent review, and atomic tranche closure.

Spec 040 closure `c5adc27b13893d7cbd1266c9225372cfb7df79e9` and
postflight evidence update `4335ea6076a68fe0bbed3526a21b92a39180faa7`
are observed prerequisites. Exact eight-path activation
`9e6fc553fa6d6b700e628ecd59306ab2a55777c1` and its postflight are observed.
No provider runtime, hosted CI, remote, credential-bearing, or live PASS is
claimed; those evidence lanes remain `DEFER`.

## Inputs

- [Stage 00 Agent Governance Contract Implementation Plan](../plans/2026-07-28-stage-00-agent-governance-contract.md)
- [Spec 041](../../03.specs/041-stage-00-agent-governance-contract/spec.md)
- [PRD-003](../../01.requirements/003-workspace-agent-governance-platform.md)
- [ARD-0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- Spec 040 closure content commit `c5adc27b` and postflight evidence update
  `4335ea60`
- [Current role semantics](../../00.agent-governance/contracts/agent-role-semantics.json)
- [Independent validation routing owner](../../00.agent-governance/contracts/validation-surfaces.json)
- [Memory boundary](../../00.agent-governance/memory/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| SAGC-000 | VAL-SAGC-001 | Enroll PRD-003/ARD-0006/Specs041–046 under current accepted ADR-0013, retain ADR-0019 as the proposed successor, and activate the reciprocal Spec/Plan/Task frontier as one exact eight-path proposal. | platform | Done | PASS — reciprocal activation and postflight are observed without promoting provider/runtime evidence. | Activation `9e6fc553fa6d6b700e628ecd59306ab2a55777c1`; parent `48d8f731d062f5e29fe58c7084fe134ddf2740b3`; exact eight paths; strict/lifecycle/aggregate/all-files/diff PASS; requirements compliant; quality approved; explicit-ref and clean-tree postflight PASS. |
| SAGC-001 | VAL-SAGC-002, VAL-SAGC-003 | Implement the closed harness schema, focused validator, and negative fixtures while preserving independent route ownership. | platform | Queued | Not executed. | Schema cases, fixture mutations, focused command output, and routing comparison will be recorded here. |
| SAGC-002 | VAL-SAGC-005, VAL-SAGC-006, VAL-SAGC-007, VAL-SAGC-009 | Add exact current/target contract data, evidence classes, and four explicit memory-class declarations. | platform | Queued | Not executed. | Exact 10/30 current, 12/48 target-only, memory authority/provenance/sensitivity/promotion boundaries, and redaction cases will be recorded here. |
| SAGC-003 | VAL-SAGC-004 | Migrate named validators and readers to one selected harness contract version while retaining explicit legacy compatibility input. | platform | Queued | Not executed. | Consumer/version ledger, focused regressions, compatibility boundary, and rollback evidence will be recorded here. |
| SAGC-004 | VAL-SAGC-003, VAL-SAGC-008 | Align catalog, provider notes, implementation maps, inventories, validation routing, and aggregate coverage. | platform | Queued | Not executed. | Derived-prose parity, affected selection, aggregate integration, and no-duplicate-owner results will be recorded here. |
| SAGC-005 | VAL-SAGC-001 through VAL-SAGC-009 | Run whole-tranche QA/review, close Spec/Plan/Task atomically, and perform explicit-ref/clean-tree postflight. | platform | Queued | Not executed. | Exact digest/range, all validation lanes, reviewer verdicts, observed commits, rollback chain, and external limitations will be recorded here. |

## Approval and Safety Boundaries

- **Allowed Paths**: Spec 041 and reciprocal execution/index/progress lineage;
  PRD-003 registry relation; Stage 00 harness contract/schema; focused
  validators and fixtures; named current contract consumers; derived
  catalog/provider/map/inventory/routing/aggregate surfaces owned by this Plan.
- **Forbidden Paths**: New or promoted provider adapters, `.gemini/**`, current
  12/48 roster, role admission, provider canary execution, model promotion,
  checkpoint runtime, legacy deletion, unrelated CI, Kubernetes/GitOps desired
  state, infrastructure, Vault, ESO, Argo CD, deployment, release, credentials,
  secrets, auth files, tokens, kubeconfigs, shell history, and ignored private
  diagnostics.
- **Approval Required**: Push, merge, workflow dispatch, GitHub/provider
  settings, dependency installation, publication, live commands, credentials,
  secrets, remote state, and any expansion beyond the Plan require separate
  explicit human approval.
- **Static Validation**: Focused harness/legacy validators; affected-surface
  checks; lifecycle self-test/staged/explicit-ref; strict registry,
  Markdown, links/owners; aggregate; all-files pre-commit; formatter/status and
  both diff checks.
- **Live Validation**: `DEFER`. Provider runtime, hosted Actions, remote,
  Kubernetes, Vault, ESO, Argo CD, cloud, deployment, and credential results
  are not authorized or inferred.
- **Secret / Vault Handling**: Do not open, print, copy, hash, store, or report
  secret values, credentials, auth data, environment dumps, shell history,
  full prompts/transcripts, or private diagnostics. Fixtures use synthetic
  redaction markers only.
- **Rollback Plan**: Revert newest logical units in SAGC dependency order and
  rerun focused plus aggregate checks after each. Revert activation last.
  Never reset, clean, rewrite shared history, or overwrite unrelated work.
- **Evidence Location**: This Task owns results; the Plan owns order; Spec 041
  owns criteria; the harness contract owns machine declarations; Spec 043 owns
  executable checkpoint lifecycle.

## Verification Summary

SAGC-000 activation `9e6fc553fa6d6b700e628ecd59306ab2a55777c1`
has the single parent `48d8f731d062f5e29fe58c7084fe134ddf2740b3`
and changes only the declared Spec/index, reciprocal Plan/Task and indexes,
shared progress entry, and registry relation. Registry self-test/strict (`119`
cases; `453` selected paths), Markdown, links/owners, lifecycle self-test/staged
(`668` cases), ACER, affected surfaces, aggregate, all-files pre-commit, and
both diff checks passed. Independent requirements and quality reviews approved
the remediated proposal. Explicit-ref lifecycle for the observed commit interval
and clean-tree aggregate postflight passed. Contract data, scripts, tests,
adapters, provider settings, CI, and live surfaces remain unchanged until their
owning work package; provider runtime, hosted CI, remote, credentials, and live
evidence remain `DEFER`.

## Traceability

- **Plan**: [Stage 00 Agent Governance Contract Implementation Plan](../plans/2026-07-28-stage-00-agent-governance-contract.md)
- **Spec**: [Stage 00 Agent Governance Contract](../../03.specs/041-stage-00-agent-governance-contract/spec.md)
- **Program**: [PRD-003](../../01.requirements/003-workspace-agent-governance-platform.md) / [ARD-0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **Governing decision**: [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Proposed successor decision**: [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [SAGC-000](../plans/2026-07-28-stage-00-agent-governance-contract.md#work-breakdown) | PASS — activation and postflight observed. | `48d8f731d062f5e29fe58c7084fe134ddf2740b3` → `9e6fc553fa6d6b700e628ecd59306ab2a55777c1`; exact eight paths; all declared repository-static gates and independent reviews PASS. |
| [VAL-SAGC-002](../../03.specs/041-stage-00-agent-governance-contract/spec.md#success-criteria--verification-plan) | Queued. | Closed schema, negative fixtures, and separate routing-owner evidence. |
| N/A — SAGC-002 shares the Plan and Spec sources linked above | Queued. | Current/target, result-class, memory-class, and redaction evidence. |
| N/A — SAGC-003 shares the Plan and Spec sources linked above | Queued. | Consumer/version migration and compatibility-removal ledger. |
| N/A — SAGC-004 shares the Plan and Spec sources linked above | Queued. | Derived parity, affected routing, and aggregate evidence. |
| N/A — SAGC-005 shares the Plan and Spec sources linked above | Queued. | Whole-tranche QA/review, atomic closure, postflight, and rollback evidence. |
