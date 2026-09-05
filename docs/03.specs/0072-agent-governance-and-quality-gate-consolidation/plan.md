---
title: "Agent Governance and Quality Gate Consolidation Implementation Plan"
version: "1.0.0"
type: "sdlc/plan"
status: "active"
owner: "platform"
updated: "2026-09-04"
layer: "specs"
artifact_id: "SPEC-0072-PLAN-0001"
---

# Agent Governance and Quality Gate Consolidation Implementation Plan

## Global Constraints

- Work from `main` through an isolated `codex/` branch; never commit directly to `main`.
- Keep common agent governance under `docs/00.agent-governance/`.
- Remove `.agents/` without a compatibility directory or redirect.
- Use one QA orchestration entrypoint locally and in GitHub Actions.
- Preserve closed and archived evidence unless it is consumed as current authority.
- Do not perform live provider, credential, cluster, deployment, release, or reconciliation actions.
- Commit every independently reviewable logical unit separately.

## Overview

This plan executes [SPEC-0072](spec.md) in four reviewable work packages: define
terminal authority, migrate agent assets, replace QA/gate orchestration, and
simplify GitHub Actions plus current guidance.

## Context

The current branch starts from main commit
`69ae876221410370f13b190c463d88f02f02932a`. Existing governance is split
between Stage 00 and `.agents/`; validation is routed through a large lane
runner and several agent-specific contracts; GitHub Actions repeats dependency
setup, validation, and unit discovery across jobs.

## Goals & In-Scope

- Establish ADR-0034 and this Spec as the current change authority.
- Move the shared registry, role bodies, and skill bodies to Stage 00.
- Remove `.agents/`, stale provider evidence, unused checkpoint contracts,
  edit-time QA hooks, and self-only validators/fixtures.
- Add a tested QA runner and compact gate registry.
- Make local `full` and GitHub Actions `ci` execute the same blocking gates.
- Update current SDLC, provider, QA, CI/CD, and template guidance.

## Non-Goals & Out-of-Scope

- Rewriting closed Specs, archived migration evidence, or dated research merely
  because they mention retired paths.
- Changing Kubernetes manifests or infrastructure behavior.
- Proving provider-runtime loading or live Argo CD reconciliation.
- Deleting unrelated historical branches or altering repository protection.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| WP-001 | Record ADR, Spec, Plan, and Task authority | None | Main baseline identified | Logical documentation commit |
| WP-002 | Migrate shared roles/skills/registry to Stage 00 and remove `.agents/` | WP-001 | ADR-0034 accepted | Governance validator tests and reference sweep |
| WP-003 | Replace legacy gate, hook, fixture, and lane orchestration with `scripts/qa.py` | WP-002 | Stage 00 registry resolves | QA runner red/green tests and local profile execution |
| WP-004 | Simplify GitHub Actions, pre-commit, current docs, SDLC indexes, and CI/CD guidance | WP-003 | QA profiles stable | actionlint/zizmor, full QA, hosted `ci-summary` |

## Verification Plan

WP-002 uses focused registry/path tests before moving production assets. WP-003
adds failing tests for registry validation, profile parity, duplicate gates,
timeouts, and child failure propagation before implementing the runner. WP-004
validates YAML, workflow security, branch policy, local/CI profile parity, and
then relies on the pull-request workflow for hosted evidence.

The final branch runs `python3 scripts/qa.py quick`, `python3 scripts/qa.py full`,
and `python3 scripts/qa.py ci`. Any unavailable hosted or live evidence is
recorded separately rather than converted to a pass.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Current consumers still point to `.agents/` | Search current executable and active guidance surfaces; fail the governance test on any match |
| Deleting validators removes a unique rule | Inventory each deleted gate, retain durable rules in Stage 00 or a focused replacement test |
| Full QA becomes slower after consolidation | Run each gate once, keep `quick` focused, cache pre-commit in Actions |
| Workflow change passes locally but fails hosted | Open a PR, inspect the workflow run and failed job logs, fix on the same branch |
| Historical records become invalid | Leave closed/archive content unchanged unless a current link must move |

## Completion Criteria

- The branch has no `.agents/` tree and all current consumers resolve to Stage 00.
- QA profiles validate and `full` equals `ci` in blocking gate membership.
- Obsolete contracts, hooks, validators, tests, and fixtures have zero current consumers.
- GitHub Actions invokes one QA path and `ci-summary` remains fail-closed.
- Focused tests, full local QA, workflow static checks, and hosted PR checks have recorded outcomes.
- Commits remain split by the four work packages.

## Traceability

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| VAL-AGQ-001 | WP-002 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| VAL-AGQ-002 | WP-002 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| VAL-AGQ-003 | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| VAL-AGQ-004 | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| VAL-AGQ-005 | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| VAL-AGQ-006 | WP-004 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| VAL-AGQ-007 | WP-004 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| VAL-AGQ-008 | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
