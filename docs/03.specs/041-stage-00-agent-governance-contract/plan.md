---
title: 'Stage 00 Agent Governance Contract Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-07-28
artifact_id: "PLAN-041"
---

# Stage 00 Agent Governance Contract Implementation Plan

## Overview

This Plan executed [Spec 041](spec.md)
as the first PRD-003 tranche. It activated a reciprocal
[Task](tasks.md), introduced
one provider-neutral harness contract without prematurely changing the current
10-role/30-adapter runtime inventory, migrated named consumers, and closed the
tranche only after deterministic validation and independent review.

Terminal closure was observed at
`1a3232ce73a653371634e99d773d71ab03f87967` with parent
`e85b7829cd120742c5f62712259a037134e2db7a`. Parent-to-closure explicit-ref
lifecycle and clean-tree aggregate passed; this postflight evidence update does
not claim its own future commit SHA.

## Context

The preceding PRD-006 program closed in terminal commit
`c5adc27b13893d7cbd1266c9225372cfb7df79e9`; postflight evidence update
`4335ea6076a68fe0bbed3526a21b92a39180faa7` records the correct atomic
explicit-ref interval and clean-tree aggregate. At activation, the then-current
role-semantics compatibility owner represented ten roles and three tracked
adapter surfaces. `validation-surfaces.json` independently owns
path-to-validator routing.

Spec 041 must create a closed harness schema, current/target inventory split,
consumer/version ledger, result-class boundary, and four-class project-memory
contract. It must not manufacture Gemini runtime readiness, promote the target
12-role/48-adapter roster, delete compatibility inputs, or implement the loop
checkpoint runtime owned by Spec 043.

This Plan, its Task, the Spec/index changes, both Stage 04 indexes, the shared
progress handoff, and the registry relation form one exact eight-path
activation proposal. No activation commit identity or provider-runtime result
is claimed before observation.

## Goals & In-Scope

- Enroll PRD-003, AD-0006, and ordered Specs 041–046 under current accepted
  ADR-0013 in the registry while activating only Spec 041; keep ADR-0019 as
  the proposed successor until Spec 046 acceptance.
- Add a closed `harness-contract.json` schema and deterministic focused
  validator with negative fixtures.
- Encode the exact current 10-role/30-adapter inventory and target-only
  12-role/48-adapter inventory without changing adapter files.
- Declare working/short-term, durable/long-term, domain-scoped, and
  provider-local auxiliary memory with explicit authority, provenance,
  sensitivity, promotion, and lifecycle-policy references.
- Migrate current validators and human-readable projections to select one
  contract version while retaining the legacy semantics input until Spec 045
  proves zero consumers.
- Add validation routing and aggregate coverage without merging routing
  ownership into the harness contract.

## Non-Goals & Out-of-Scope

- Provider installation, authentication, account/model resolution, native
  runtime canaries, or readiness claims owned by Spec 042.
- Checkpoint runtime, bounded retry, compaction/resume, archive/GC execution,
  or loop fixtures owned by Spec 043.
- New roles, Gemini adapters, model promotion, eval admission, or 12/48 current
  parity owned by Spec 044.
- Legacy deletion and CI cutover owned by Spec 045, or program closure owned by
  Spec 046.
- Push, merge, workflow dispatch, dependency installation, secret access, or
  provider, GitHub, Kubernetes, GitOps, Vault, ESO, Argo CD, cloud, remote, or
  live mutation.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| SAGC-000 | Activate reciprocal Spec 041 planning and PRD-003 lineage | Spec 040 postflight | `4335ea60` is observed and tree is clean | Exact-eight lifecycle/strict/aggregate/all-files PASS, independent review, and one observed activation commit |
| SAGC-001 | Add harness schema, focused validator, and negative fixtures | SAGC-000 | Active reciprocal Plan/Task | Closed schema rejects unknown keys, invalid enums, duplicates, missing projections, unbounded rules, unsupported versions, and sensitive content |
| SAGC-002 | Add current/target harness data and memory declarations | SAGC-001 | Schema and validator are green | Exact current 10/30, non-current target 12/48, four result classes, and four memory classes validate |
| SAGC-003 | Migrate named current consumers | SAGC-002 | New contract is readable and current data is exact | Each consumer selects one contract version; legacy semantics remains compatibility input with an explicit removal owner |
| SAGC-004 | Align derived governance and validation routing | SAGC-003 | Consumer ledger has no ambiguous owner | Catalog/provider notes/maps/inventories agree; routing stays separately owned and aggregate coverage includes the focused validator |
| SAGC-005 | Run whole-tranche QA, review, and terminal closure | SAGC-004 | Stable implementation proposal | Focused/affected/strict/lifecycle/aggregate/all-files/diff PASS; independent requirements/quality/security approval; atomic Spec/Plan/Task closure and postflight |

## Verification Plan

| Lane | Commands or method | Required result |
| --- | --- | --- |
| Harness contract | `python3 scripts/validate-agent-harness-contract.py --self-test`; `--root .` | Schema, fixtures, inventory, memory, consumers, and result-class boundaries pass |
| Compatibility inputs | Existing role-semantics and roster self-tests/production checks | Current 10/30 behavior remains green until the authorized cutover |
| Documents | Strict registry, Markdown profiles, links/owners, and lifecycle staged/explicit-ref modes | Zero route, profile, link, owner, or transition findings |
| Routing | Affected-surface self-test and production selection | Harness paths select the focused validator without duplicating routing data |
| Repository QA | `bash scripts/validate-repo-quality-gates.sh .`; `pre-commit run --all-files`; status and diff checks | Aggregate final marker, every applicable hook, and clean formatter/diff inspection |
| Independent review | Requirements, quality, and security reviewers inspect exact proposal digests | No unresolved Critical or Important finding |
| External evidence | Provider-runtime, hosted CI, remote, and live lanes | `DEFER`, `ABSENT`, or `BLOCKED` unless separately authorized and observed; never inferred from repo-static PASS |

## Risks & Mitigations

| Risk | Mitigation | Owner |
| --- | --- | --- |
| New target inventory becomes current too early | Validate separate `currentInventory` and `targetInventory`; only Spec 044 may promote 12/48 | platform |
| Two machine owners diverge | Record consumer/version state; new contract is current owner only for migrated fields while legacy remains an explicit compatibility input until Spec 045 | platform |
| Memory becomes a transcript or secret store | Closed sensitivity enums and negative fixtures reject prompts, transcripts, credentials, tokens, secret output, auth data, and shell history | platform |
| Provider-local memory overrides repository truth | Mark it advisory and require conflict resolution in favor of observed repository state and durable owners | platform |
| Routing and role semantics are conflated | Keep `validation-surfaces.json` independent and compare references rather than copying route definitions | platform |
| Static files are reported as runtime readiness | Preserve `repo-static`, `provider-runtime`, `ci`, and `remote-live` as non-transitive evidence classes | platform |
| Rollback overwrites later work | Commit in dependency order and revert newest logical units only; never reset or clean shared history | platform |

## Completion Criteria

- SAGC-000 through SAGC-005 have observed repository-static results in the
  reciprocal Task.
- Exactly one closed harness contract owns migrated shared role/projection,
  permission, stop, handoff, evidence, model/eval-reference, and memory
  declarations.
- Current inventory remains exactly 10 roles/30 adapters; target 12/48 remains
  non-current and owned by later tranches.
- Four memory classes declare authority, owner, provenance, sensitivity,
  promotion, and lifecycle-policy boundaries; executable checkpoint lifecycle
  remains Spec 043 work.
- Every named consumer selects one version, and legacy removal remains blocked
  until Spec 045 proves zero consumers.
- Focused, affected, lifecycle, strict document, aggregate, all-files,
  formatter, diff, and independent review gates pass.
- Spec/Plan/Task terminal transition and explicit-ref/clean-tree postflight are
  recorded as separate evidence events without promoting
  provider/runtime/hosted/remote/live evidence.

## Traceability

- **Spec**: [Stage 00 Agent Governance Contract](spec.md)
- **Task**: [Stage 00 Agent Governance Contract Task](tasks.md)
- **Program**: [PRD-003](../../01.requirements/003-workspace-agent-governance-platform.md) and [AD-0006](../../02.architecture/descriptions/ad-0006-workspace-agent-governance-platform.md)
- **Governing decision**: [ADR-0013](../../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Proposed successor decision**: [ADR-0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)
- **Prerequisite**: Spec 040 closure content commit `c5adc27b` and postflight
  evidence update `4335ea60`

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-SAGC-001](spec.md#success-criteria--verification-plan) | SAGC-000 | [Reciprocal activation and lineage evidence](tasks.md#task-table) |
| N/A — VAL-SAGC-002 through VAL-SAGC-003 share the Spec source above | SAGC-001 | N/A — the paired Task is linked in VAL-SAGC-001 |
| N/A — VAL-SAGC-004 shares the Spec source above | SAGC-003 | N/A — the paired Task is linked in VAL-SAGC-001 |
| N/A — VAL-SAGC-005 through VAL-SAGC-006 share the Spec source above | SAGC-002 | N/A — the paired Task is linked in VAL-SAGC-001 |
| N/A — VAL-SAGC-007 through VAL-SAGC-009 share the Spec source above | SAGC-002, SAGC-004, SAGC-005 | N/A — the paired Task is linked in VAL-SAGC-001 |
