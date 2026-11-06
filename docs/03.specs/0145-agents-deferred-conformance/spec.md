---
title: "Agent Surface Deferred Conformance"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0145"
---

# Agent Surface Deferred Conformance Technical Specification (Spec)

## Overview

SPEC-0144 corrected `.agents/` and deferred six items. On 2026-11-06 the
operator asked to handle the deferred items and finish. A registry schema,
validator and Stage 03 record change needs this package. The [Plan](plan.md)
orders the work and [Task 0001](tasks/tsk-0001-agents-deferred-conformance.md)
records it.

## Strategic Boundaries & Non-goals

- In scope:
  - the shared Authority Boundary, Validation and Refresh, and Related
    Documents sections of the 17 role bodies, which repeat one paragraph
    instead of answering their template prompts;
  - the `### Item Index` and `### Add and Find` subsections of the
    collection-index READMEs under `.agents/` that lack them;
  - the per-role registry fields `supported_providers` and `projections`,
    whose only allowed values are derived from the role ID and the provider
    table;
  - the `governance/contract` profile of `.agents/governance/sdlc.md`;
  - the CIS control numbers in the `vulnerability-patterns` catalog;
  - the sibling `hy-home.docker` revision pinned in the external service
    contract.
- Non-goals:
  - the `providers` table, which stays the single declaration of each
    provider's gateway, projection root and bindings path;
  - any change to role responsibility, permission class, skills or handoffs;
  - any live, hosted or provider-runtime change.

## Contracts

- Each role body's Authority Boundary names the surfaces the role may write
  (or that it writes none) and the actions it hands back; its Validation and
  Refresh names the checks it runs and the lane each result is reported
  under; its Related Documents links its upstream, downstream and validation
  owners.
- Each `.agents/` collection-index README lists its direct members once under
  `### Item Index` and says how to add and find one under `### Add and Find`.
- The registry carries no per-role `supported_providers` or `projections`; the
  agent-governance validator derives each projection path as
  `<projection_root>/<role id><suffix>` and still rejects a missing or stale
  projection.
- `sdlc.md` keeps the `governance/contract` profile, and its Authority
  Boundary states the invariant it owns: each change kind maps to one record
  set, check set and approval.
- Every CIS reference names CIS Kubernetes Benchmark v1.9 and matches its
  control text; a pattern without a matching control carries no CIS number.
- The external service contract names the sibling revision whose Compose
  publications were rechecked.
- Every current document still passes the strict document checks.

## Core Design

Prose changes answer the template prompts with facts each role body or
registry already holds. The registry change removes data the validator can
derive and moves the derivation into the validator, with a failing test
first.

## Data Modeling & Storage Strategy

`registry.json` loses two keys from each of 17 roles; `registry.schema.json`
loses their definitions. No document schema changes.

## Interfaces & Data Structures

`scripts/validate-agent-governance.py` gains one helper that returns a role's
projection paths; its command-line interface and summary counts are
unchanged.

## Edge Cases & Error Handling

- Normal: the validator reports the same 51 projections.
- Error: a deleted or stale projection file, or a registry role that still
  carries `projections`, is refused.
- Boundary: a third provider stays refused by the providers table rules.

## Failure Modes & Fallback / Human Escalation

A failing check after a change means a consumer relied on the removed field
or the old text; revert that commit and reopen the item.

## Verification Commands

- `python3 scripts/validate-agent-governance.py --root .`
- `python3 -m unittest tests.test_agent_governance tests.test_validate_agent_registry`
- the strict registry, Markdown-profile, link and lifecycle checks
- `python3 scripts/qa.py staged` on each commit

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-DEF-001 | The 17 role bodies' three shared sections are role-specific; strict document checks and the agent-governance tests PASS |
| VAL-DEF-002 | The `.agents/` collection-index READMEs carry `Item Index` and `Add and Find`; strict document checks PASS |
| VAL-DEF-003 | A regression test fails before and passes after the per-role field removal; the agent-governance validator PASS with 51 projections |
| VAL-DEF-004 | `sdlc.md` states the invariant it owns as a contract; the CIS numbers match CIS Kubernetes Benchmark v1.9; the external service contract names the rechecked sibling revision |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0010](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DEF-001 | Strict document checks and agent-governance tests |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DEF-002 | Strict document checks |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DEF-003 | Regression test red then green |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-DEF-004 | Source comparison recorded in the Task |
