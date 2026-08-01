---
title: 'Agent Governance Program Closure Implementation Plan'
type: sdlc/plan
status: active
owner: platform
updated: 2026-08-01
---

# Agent Governance Program Closure Implementation Plan

## Overview

This Plan executes
[Spec 046](../../03.specs/046-agent-governance-program-closure/spec.md) as the
final repository-local closure tranche. It activates the reciprocal execution
path, implements one closed closure contract, routes it through local QA/CI,
runs independent whole-branch review, records reciprocal closure, and finishes
the already-authorized local `main` merge and isolated-worktree cleanup.

## Context

Spec 045 closed at
`de9a88e4550b87542eb7221c5ae7416fe5075763` with sole parent
`ed89228546501dd11a7f4abad28e8ebb094fbd97`; postflight
`060396112abaddbbcf79a33c8a04ae775cce66a1` observed that edge. The fixed
provider/model/source cutoff remains `2026-07-10T10:00:00+09:00` /
`2026-07-10T01:00:00Z`.

Specs 041-045 closed repository-static harness, provider-source, loop/memory,
12-role/48-adapter readiness, and CI/QA controls. They did not observe provider
runtime/auth/model discovery, current hosted CI or branch protection, actual
evaluation/admission/promotion, remote execution, or live platform state.

## Goals & In-Scope

- Activate reciprocal Spec 046, Plan, Task, indexes, lineage, and progress.
- Add the closure contract, schema, positive fixture, validator, self-test, and
  focused unit tests.
- Keep repository-static/local PASS non-transitive across external lanes.
- Reconcile 12/48 roster, provider canaries, model/reasoning configuration, and
  the four memory classes without reading private state.
- Route one closure owner through validation surfaces, pre-commit, CI, and
  script/test documentation.
- Complete local QA, independent review, reciprocal closure/postflight, local
  merge, and safe worktree cleanup as separate logical commits.

## Non-Goals & Out-of-Scope

- No provider login, credential inspection/change, authenticated canary, or
  provider-local memory read.
- No hosted workflow dispatch, branch-protection mutation, push, PR, remote
  merge, release, paid action, or live cluster mutation.
- No actual evaluation, admission, model-fitness, threshold, or promotion PASS
  claim without separately observed evidence.
- No reading ignored checkpoint content, auth files, tokens, shell history,
  transcripts, provider response bodies, or secret values.

## Work Breakdown

| ID | Work package | Depends on | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- |
| AGPC-000 | Activate reciprocal Spec 046 execution path | Spec 045 closure/postflight | Clean branch worktree | Exact eight-file Spec/Plan/Task/index/profile/progress activation is active and validated |
| AGPC-001 | Implement closure contract package | AGPC-000 | Current contract/schema/test patterns are reviewed | Contract, schema, fixture, self-test, validator, and focused tests pass |
| AGPC-002 | Route the gate and reconcile evidence owners | AGPC-001 | Closure validator passes | Validation surfaces, CI/QA, inventories, implementation map, catalog, and provider notes point to one owner |
| AGPC-003 | Run final QA and independent reviews | AGPC-002 | Focused and routed gates pass | Affected/staged/all-files/aggregate/diff gates pass and reviewers approve |
| AGPC-004 | Close reciprocal documents and postflight | AGPC-003 | No open findings or formatter mutation | Exact lifecycle closure and observed postflight are recorded without self-SHA preclaim |
| AGPC-005 | Finish the local branch | AGPC-004 | Clean worktree and safe dirty-main assessment | `main` contains the branch locally; isolated worktree and finished branch are cleaned safely |

## Verification Plan

```bash
python3 scripts/validate-agent-governance-closure.py --root . --self-test
python3 scripts/validate-agent-governance-closure.py --root .
python3 -m unittest tests/test_validate_agent_governance_closure.py
python3 scripts/validate-agent-harness-contract.py --root .
python3 scripts/validate-agent-provider-canaries.py --root .
python3 scripts/validate-agent-loop-lifecycle.py --root .
python3 scripts/validate-agent-roster-admission.py --root .
python3 scripts/validate-agent-evaluations.py --root .
python3 scripts/validate-agent-model-fitness.py --root .
python3 scripts/validate-agent-governance-ci.py --root .
python3 scripts/validate-agent-legacy-cutover.py --root .
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-links-and-owners.py --root . --mode strict --body-contracts registry
bash scripts/validate-repo-quality-gates.sh .
pre-commit run --all-files
git diff --check
```

AGPC-001 owns the first three commands. Other commands retain their existing
repository-static or local-validation evidence class and cannot establish an
external/runtime PASS.

## Risks & Mitigations

| Risk | Mitigation |
| --- | --- |
| Static PASS becomes provider/hosted/live PASS | Require explicit lane classification and prohibit cross-lane promotion. |
| Configured model/effort is called observed fitness | Validate configuration completeness only; retain actual evaluation and promotion as `DEFER`. |
| Memory prose becomes a duplicate authority | Reference the existing four-class machine owner and validate lifecycle fields rather than redefine it. |
| Closure duplicates predecessor evidence | Store concise unique criterion rows and canonical evidence links, not raw logs. |
| Final QA changes files after review | Review formatter output and rerun affected, staged, all-files, diff, and impacted reviews. |
| Dirty `main` contains unrelated user work | Inspect and preserve it; use a safe integration route or stop if overlap prevents local merge. |

## Completion Criteria

- Spec 046 activates and closes through separate, validated lifecycle commits.
- The closure contract package rejects missing, duplicate, stale, ownerless,
  and cross-lane-promoted evidence.
- Provider, hosted, remote, live, and actual-evaluation results stay honestly
  classified.
- Four memory classes and provider model/reasoning configuration validate at
  their repository-static boundary.
- Final reviews approve, `main` is locally integrated, no push occurs, and the
  isolated worktree/finished branch are cleaned when safe.

## Traceability

- **Spec**: [Agent Governance Program Closure](../../03.specs/046-agent-governance-program-closure/spec.md)
- **Task**: [Task: Agent Governance Program Closure](../tasks/2026-08-01-agent-governance-program-closure.md)
- **Predecessor**: Spec 045 closure `de9a88e4` and postflight `06039611`
- **Program**: [PRD 003](../../01.requirements/003-workspace-agent-governance-platform.md),
  [ARD 0006](../../02.architecture/requirements/0006-workspace-agent-governance-platform.md),
  and [ADR 0019](../../02.architecture/decisions/0019-provider-native-agent-harness-and-loop-model.md)

### Lifecycle Traceability

| Spec criterion | Work package | Expected Task |
| --- | --- | --- |
| [VAL-AGPC-001](../../03.specs/046-agent-governance-program-closure/spec.md#success-criteria--verification-plan) | AGPC-000 | [Activation evidence](../tasks/2026-08-01-agent-governance-program-closure.md#task-table) |
| N/A — VAL-AGPC-002 shares the Spec source above | AGPC-001 | N/A — reciprocal Task is linked in VAL-AGPC-001 |
| N/A — VAL-AGPC-003 through VAL-AGPC-007 share the Spec source above | AGPC-002 | N/A — reciprocal Task is linked in VAL-AGPC-001 |
| N/A — VAL-AGPC-008 and VAL-AGPC-009 share the Spec source above | AGPC-003 | N/A — reciprocal Task is linked in VAL-AGPC-001 |
| N/A — VAL-AGPC-010 shares the Spec source above | AGPC-004, AGPC-005 | N/A — reciprocal Task is linked in VAL-AGPC-001 |
