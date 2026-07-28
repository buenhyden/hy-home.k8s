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
| SAGC-001 | VAL-SAGC-002, VAL-SAGC-003 | Implement the closed harness schema, focused validator, and negative fixtures while preserving independent route ownership. | platform | Done | PASS — the closed schema, focused validator, and mutation fixtures reject malformed or unsupported contract states while routing remains separately owned. | Implementation `8d5a4c50468c07d1f3574e53a1d32ca5a39f642d`; harness self-test/production PASS; unknown-key, enum, duplicate-role, projection, stop-rule, version, path, and sensitive-content mutations PASS. |
| SAGC-002 | VAL-SAGC-005, VAL-SAGC-006, VAL-SAGC-007, VAL-SAGC-009 | Add exact current/target contract data, evidence classes, and four explicit memory-class declarations. | platform | Done | PASS — current and target inventories, four non-transitive evidence classes, and four memory classes validate without promoting target or runtime state. | Implementation `8d5a4c50468c07d1f3574e53a1d32ca5a39f642d`; current `10/3/30`; target-only `12/4/48`; evidence `4`; memory `4`; redaction and provider-local advisory boundaries PASS. |
| SAGC-003 | VAL-SAGC-004 | Migrate named validators and readers to one selected harness contract version while retaining explicit legacy compatibility input. | platform | Done | PASS — all named semantic consumers select `harness-contract/1.0.0`; the legacy role contract is readable compatibility input with no current semantic consumer. | Migration `52a4ab6c2e1e4436486a74ec13f35109150161a1`; consumers `11`; `legacyConsumers=[]`; harness, role-semantics, roster, unit, aggregate, path-safety, requirements, and quality review PASS. |
| SAGC-004 | VAL-SAGC-003, VAL-SAGC-008 | Align catalog, provider notes, implementation maps, inventories, validation routing, and aggregate coverage. | platform | Done | PASS — derived governance consumes the harness owner, seven exact affected surfaces route the focused validator, and the aggregate runs it before compatibility checks. | Integration `8c342ce6011c465e138c4cec0ab796ee6c83bdb3`; harness/affected/role/roster/strict/aggregate and staged hooks PASS; requirements `COMPLIANT`; quality `APPROVED`; no Gemini-native, infrastructure, CI-job, adapter, or provider-setting promotion. |
| SAGC-005 | VAL-SAGC-001 through VAL-SAGC-009 | Run whole-tranche QA/review, close Spec/Plan/Task atomically, and perform explicit-ref/clean-tree postflight. | platform | In Progress | Focused and aggregate repository-static QA pass; stable all-files, final independent review, atomic lifecycle closure, and postflight remain required. | Implementation evidence HEAD `7098a3242ac40e757c86ccac9b986e3253766f23`; focused/affected/strict/lifecycle/aggregate PASS; first all-files run detected concurrent staging and exited nonzero despite individual hook PASS; requirements review correctly found SAGC-005 still queued at committed HEAD; stable rerun and final requirements/quality/security verdicts pending; provider/runtime/hosted/remote/live lanes remain `DEFER`. |

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
shared progress entry, and registry relation. Its postflight evidence update is
`5d4dd5cf`.

SAGC-001 and SAGC-002 implementation `8d5a4c50` adds the closed machine
contract, schema, focused validator, fixtures, exact current `10/3/30` and
target-only `12/4/48` inventories, four evidence classes, and four memory
classes. SAGC-003 migration `52a4ab6c` moves all eleven named semantic consumers
to `harness-contract/1.0.0`, leaves `legacyConsumers=[]`, and retains the old
role contract only as readable compatibility input until Spec 045. SAGC-004
integration `8c342ce6` aligns the derived governance, routes the focused
validator through exactly seven affected surfaces, and places harness checks
before compatibility validators in the aggregate. Focused harness, role,
roster, affected-surface, strict document, aggregate, staged-hook, path-safety,
requirements, and quality checks passed for their owning proposals.

Current inventory remains `10/3/30`; target `12/4/48`, Gemini-native admission,
provider installation/runtime, model promotion, hosted CI, remote,
credential-bearing, and live evidence remain non-current or `DEFER`. Executable
checkpoint promotion, retry, resume, expiry, archive/GC, conflict, and redaction
behavior remains owned by Spec 043.

Whole-tranche SAGC-005 repository-static QA began after implementation evidence
commit `7098a3242ac40e757c86ccac9b986e3253766f23`. The aggregate
`bash scripts/validate-repo-quality-gates.sh .` ended with
`[PASS] repository quality gates passed`. The first all-files run observed every
individual check pass but exited nonzero because this QA evidence draft was
staged concurrently while the strict hook was running. Requirements review
correctly found that committed HEAD still had SAGC-005 queued. Stable all-files,
formatter/status and diff inspections, remediation review, quality, and
security verdicts remain required before any terminal lifecycle status commit.
No provider runtime, hosted CI, remote, credential-bearing, Kubernetes/GitOps,
Vault/ESO, or live result is inferred from these repository-static PASS lanes.

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
| [VAL-SAGC-002](../../03.specs/041-stage-00-agent-governance-contract/spec.md#success-criteria--verification-plan) | PASS — closed schema and mutation fixtures observed. | `8d5a4c50`; focused harness self-test/production and negative fixtures PASS; routing remains independently owned. |
| N/A — SAGC-002 shares the Plan and Spec sources linked above | PASS — exact inventories, evidence classes, and memory classes observed. | `8d5a4c50`; current `10/3/30`, target-only `12/4/48`, evidence `4`, memory `4`, and redaction boundaries PASS. |
| N/A — SAGC-003 shares the Plan and Spec sources linked above | PASS — named consumers select one current contract. | `52a4ab6c`; consumers `11`, `legacyConsumers=[]`, compatibility input retained for Spec 045 removal proof. |
| N/A — SAGC-004 shares the Plan and Spec sources linked above | PASS — derived governance and validation routing integrated. | `8c342ce6`; seven exact surfaces, aggregate ordering, focused/affected/strict/aggregate checks, requirements `COMPLIANT`, quality `APPROVED`. |
| N/A — SAGC-005 shares the Plan and Spec sources linked above | In Progress — focused and aggregate QA pass; stable all-files, final reviews, atomic closure, and postflight remain. | Focused/affected/strict/lifecycle/aggregate PASS; first all-files run detected concurrent staging; requirements finding open; final requirements/quality/security verdicts pending; external/provider/live lanes `DEFER`. |
