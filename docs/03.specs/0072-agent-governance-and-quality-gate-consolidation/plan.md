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
- Reuse the existing validation registry as the sole command/limit owner; QA
  profiles select existing gate IDs rather than copying argv or timeout fields.
- Preserve bounded output, cancellation and descendant/pipe cleanup.
- Keep this branch and worktree; push, PR creation and hosted dispatch remain unauthorized.
- Review historical and in-progress content for current authority conflicts; preserve
  historical facts and valid archive isolation, not obsolete current instructions.
- Do not perform live provider, credential, cluster, deployment, release, or reconciliation actions.
- Commit every independently reviewable logical unit separately.

## Overview

This plan executes [SPEC-0072](spec.md) in four reviewable work packages: define
terminal authority, migrate agent assets, replace QA/gate orchestration, and
simplify GitHub Actions plus current guidance.

## Context

The current branch starts from main commit
`bb73116b7b09c4f257fc81baa12cfa8359495fc0`. Existing governance is split
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

### Approved Execution Refinements (2026-09-05)

- [ ] WP-001: repair Plan/Task criterion links, Stage 03/Decision navigation
  and Requirement reciprocity; record the PR 56 implementation gap and current
  baseline in the existing Task.
- [ ] WP-002: move registry/schema and canonical role bodies into Stage 00
  roles, native skill packages into Stage 00 skills, then switch adapters,
  profiles, validators and fixtures before removing the old tree. Use explicit
  Codex reads; do not claim automatic discovery from a provider skill link.
- [ ] WP-002: use direct canonical read instructions in native role files.
  Keep provider model/effort/tool metadata native. No projection framework
  is needed when native bodies only point to shared owners.
- [ ] WP-003: make QA select existing validator IDs, preserve bounded execution,
  provide useful redacted failure summaries, preserve the invoking Python
  environment and validate a separate staged index snapshot.
- [ ] WP-003: prove distinct negative cases for invalid profiles/registries,
  duplicate gates, missing tools, timeout/output/cancellation/child cleanup,
  input path changes and full/ci membership parity. Retire only proven
  duplicate or consumer-zero gates and fixtures.
- [ ] WP-004: reduce CI to branch policy, one QA job and fail-closed ci-summary;
  use immutable event commits, check-only formatting and pinned dependencies.
  Remove QA/pre-commit recursion and repeated unit discovery.
- [ ] WP-004: audit templates, current/historical ownership and in-progress
  packages; validate the final tree, record costs and local commits, retain
  the worktree and leave unauthorized hosted execution DEFER.

## Verification Plan

WP-002 uses focused registry/path tests before moving production assets. WP-003
adds failing tests for registry validation, profile parity, duplicate gates,
timeouts, and child failure propagation before implementing the runner. WP-004
validates YAML, workflow security, branch policy, local/CI profile parity, and
then relies on the pull-request workflow for hosted evidence.

After implementation, run `quick` for changed working-tree paths and verify
`--list`; run `full` once over the final tree. Tests assert that `ci` has the
same blocking gate set. Do not repeat the identical full suite through `ci`
or a second pre-commit invocation on unchanged bytes. Required index checks
use an actual staged snapshot; hosted/provider/live evidence remains separate.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Current consumers still point to `.agents/` | Search current executable and active guidance surfaces; fail the governance test on any match |
| Deleting validators removes a unique rule | Inventory each deleted gate, retain durable rules in Stage 00 or a focused replacement test |
| Full QA becomes slower after consolidation | Run each gate once, keep `quick` focused, cache pre-commit in Actions |
| Workflow change passes locally but fails hosted | Run workflow static checks locally; inspect existing logs; leave a new hosted run DEFER without separate authorization |
| Historical records become invalid | Review current authority claims and archive isolation; preserve historical facts and recoverable Git provenance |

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
| [VAL-AGQ-001](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-002](spec.md#success-criteria--verification-plan) | WP-002 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-003](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-004](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-005](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-006](spec.md#success-criteria--verification-plan) | WP-004 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-007](spec.md#success-criteria--verification-plan) | WP-004 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
| [VAL-AGQ-008](spec.md#success-criteria--verification-plan) | WP-003 | [SPEC-0072-TSK-0001](tasks/tsk-0001-consolidate-governance-and-quality-gates.md) |
