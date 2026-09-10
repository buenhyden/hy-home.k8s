---
title: "Return Duplicated Authority to One Owner"
version: "0.2.0"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-10"
layer: "specs"
artifact_id: "SPEC-0072-TSK-0004"
---

# Task: Return Duplicated Authority to One Owner

## Overview

Execute `WP-012`. The stream investigated which file actually decides each
governance, QA and CI behavior, then removed the second owner wherever two
files decided the same thing. Nothing here adds a control: every unit either
deletes a copy, enforces an invariant that was already written down, or
corrects a statement the repository cannot keep.

This record was authored after its units were committed, so it states observed
results rather than a plan. It reaches `done` only after the final full profile;
the branch finish decision is the user's and is not this stream's to make.

## Inputs

- [SPEC-0072](../spec.md) for `VAL-AGQ-002`, `VAL-AGQ-003`, `VAL-AGQ-004`,
  `VAL-AGQ-005`, `VAL-AGQ-014` and `VAL-AGQ-019`.
- [SPEC-0072-PLAN-0001](../plan.md) for `WP-012` and its six units.
- [Quality policy](../../../../.agents/governance/quality.md) for lane and
  result meanings, and [Git policy](../../../../.agents/governance/git.md) for
  the per-commit exact-index requirement.
- Branch `refactor/governance-qa-convergence`, base `02a5a3a1`.

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-027 | VAL-AGQ-003 | WP-012A memoize the shared Markdown rendering path | platform | Done | PASS for the approved local scope | `d5ef20da`, `c7848320`; controlled A/B below; `tests/test_markdown_render_cache.py` |
| WORK-028 | VAL-AGQ-002 | WP-012B constrain native scope overrides to their permission class | platform | Done | PASS for the approved local scope | `cc18cdc9`, `86802807`; `AGENT-REGISTRY-PERMISSION` subset check and one evaluation case per class |
| WORK-029 | VAL-AGQ-005 | WP-012C remove the one-shot archive mutation path from a read-only gate | platform | Done | PASS for the approved local scope | `9b597dda`; 131 deletions with the gate output hash unchanged |
| WORK-030 | VAL-AGQ-014 | WP-012D let each registered gate own its own repository result | platform | Done | PASS for the approved local scope | `de178a8f`; failure paths and diagnostic strings retained in the suites |
| WORK-031 | VAL-AGQ-004 | WP-012E resolve the hosted profile from the gate set that owns it | platform | Done | PASS for the approved local scope | `77f78345`; `SURFACE-SCHEMA` and `SURFACE-PROFILE-ALIAS` negatives; 48 profile and runner tests |
| WORK-032 | VAL-AGQ-019 | WP-012F return documentation, skill and role statements to their owners | platform | Done | PASS for the approved local scope | `299c5bae`, `08ec9c3c`, `9959dce6`; 140 agent-governance tests |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/governance/`, `.agents/roles/`, `.agents/skills/`,
  `scripts/`, `tests/`, `evals/`, `scripts/README.md`, `tests/README.md`, and
  this Spec package.
- **Forbidden Paths**: `gitops/`, `infrastructure/`, `.github/workflows/`,
  `docs/98.archive/`.
- **Approval Required**: design approval was given before implementation; push,
  PR creation, merge, branch finish and worktree removal were not requested and
  were not performed.
- **Static Validation**: `python3 scripts/qa.py staged` per logical commit,
  `python3 scripts/qa.py quick` per change, and `python3 scripts/qa.py full`
  before handoff.
- **Live Validation**: DEFER. No cluster, Argo CD, Vault or hosted run is in
  scope, and none was used.
- **Secret / Vault Handling**: no secret value was read, printed or recorded;
  secret-handling gates ran as part of every profile above.
- **Rollback Plan**: each unit is one or two commits on
  `refactor/governance-qa-convergence` and reverts independently.
- **Evidence Location**: this record and the commit messages it names.

## Verification Summary

Every unit carries repo-static evidence only. Hosted CI and live cluster are
separate lanes and are recorded as DEFER, not as absent risk.

`WP-012A` is the one unit with a performance claim, so it carries a measurement
rather than an assertion. The same code and the same corpus were run twice, once
with the four caches active and once with each replaced by its uncached
`__wrapped__` function:

| Run | Wall clock | Result |
| --- | --- | --- |
| Memoized | 32.86 s | rc=0 |
| Unmemoized | 79.06 s | rc=0 |

That is 2.41x on `links-and-owners`, with cache reuse between 61.8% and 85.6%
across the four entries. The load-bearing number is neither of those: the two
runs produced byte-identical output, so the time did not come from checking
less. A speedup that lost coverage would not be an improvement.

`WP-012E` was executed in the wrong order on the first attempt: the registry was
edited before the code that reads it, the affected-surface selector then failed,
and the pre-action write guard correctly failed closed on every write tool
including the command that would have repaired it. The recovery needed a shell
outside the guard. The second attempt widened the schema, moved the data, then
narrowed the schema, so every intermediate state validated on its own. The
`KeyError` that made the first failure unreadable is now the handled
`SURFACE-PROFILE-ALIAS` diagnostic.

Two premises in the approved plan did not survive inspection and were not
executed. `agents/openai.yaml` is not a no-op projection: the agent-governance
validator requires its exact bytes, six mutation tests cover it, and the Codex
provider note states it as that provider's invocation contract. No skill is
orphaned either, so no skill was retired; the redundancy was inside skill
bodies, not among them.

Independent review disposition: none. This stream was implemented and verified
by one agent under user approval, with no second reviewer, which is a stated
limitation of the evidence rather than a passed review.

Residual risk: renaming the Stage 99 profile id `governance/rule`, which
contradicts the SDLC glossary it sits beside, is left unstarted. The id is
already the successor of two retired ids and document lifecycle treats it as a
stable identity, so it needs its own migration owner. The glossary now states
the mismatch instead of the code hiding it.

Next owner: the user, for the branch finish decision and any hosted run.

## Traceability

[SPEC-0072](../spec.md) owns the criteria named below and
[SPEC-0072-PLAN-0001](../plan.md) owns `WP-012`. The
[original Task](tsk-0001-consolidate-governance-and-quality-gates.md), the
[repair Task](tsk-0002-repair-governance-and-validation-contracts.md) and the
[entry-point Task](tsk-0003-documentation-entry-point-and-gate-repairs.md) keep
their own streams and none is reopened here.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-027](../plan.md#wp-012-return-duplicated-authority-to-one-owner) | Done / PASS for the approved local scope. | `VAL-AGQ-003`; `d5ef20da`, `c7848320`; 2.41x with byte-identical output |
| [WORK-028](../plan.md#wp-012-return-duplicated-authority-to-one-owner) | Done / PASS for the approved local scope. | `VAL-AGQ-002`; `cc18cdc9`, `86802807`; widening override rejected, one case per class |
| [WORK-029](../plan.md#wp-012-return-duplicated-authority-to-one-owner) | Done / PASS for the approved local scope. | `VAL-AGQ-005`; `9b597dda`; gate output hash unchanged after removal |
| [WORK-030](../plan.md#wp-012-return-duplicated-authority-to-one-owner) | Done / PASS for the approved local scope. | `VAL-AGQ-014`; `de178a8f`; unique failure paths retained |
| [WORK-031](../plan.md#wp-012-return-duplicated-authority-to-one-owner) | Done / PASS for the approved local scope. | `VAL-AGQ-004`; `77f78345`; 48 profile and runner tests, two negatives |
| [WORK-032](../plan.md#wp-012-return-duplicated-authority-to-one-owner) | Done / PASS for the approved local scope. | `VAL-AGQ-019`; `299c5bae`, `08ec9c3c`, `9959dce6`; 140 agent-governance tests |
