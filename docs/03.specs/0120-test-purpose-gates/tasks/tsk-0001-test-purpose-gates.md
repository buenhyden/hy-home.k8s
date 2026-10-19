---
title: "Test Module Purpose Gates Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-20"
layer: "specs"
artifact_id: "SPEC-0120-TSK-0001"
parent_ids: ["SPEC-0120-PLAN-0001"]
---

# Task: Test Module Purpose Gates Execution

## Overview

Execute [SPEC-0120](../spec.md) through [WORK-001–003](../plan.md#work-breakdown):
a shared suite runner with a coverage guard, two test cost and stability
fixes, and a registered purpose gate for every unrun test module.

## Inputs

- The operator's 2026-10-16 instruction to review and proceed with purpose
  gates for the 63 test modules that no lane runs, and the 2026-10-19
  instruction to continue from where the work stopped.
- Start: main `a29c836f` (PR #161 merge), branch
  `test/spec-0120-purpose-gates` in a separate worktree.
- The read-only scoping report of 2026-10-16.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PG-001](../spec.md#success-criteria--verification-plan) | Shared suite runner and coverage guard | platform | completed | PASS | EVD-004 guard, EVD-011 review |
| WORK-002 | [VAL-PG-002](../spec.md#success-criteria--verification-plan) | Link-boundary rewrite and lane test budgets | platform | completed | PASS | EVD-002, EVD-008 tests, EVD-003 staged QA, EVD-012 review |
| WORK-003 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | Register and route the suite gates | platform | completed | PASS | EVD-005, EVD-010 suite runs, EVD-006 selection tests, EVD-009 staged QA resolving EVD-007, EVD-013 review |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Suite gate runs | `scripts/run-contract-tests.py` for every suite on this branch | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-PG-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Focused tests | Commit `8cb8980a`: `tests/test_documentation_link_boundary.py`, `tests/test_run_validation_lane.py` | PASS | The placeholder link test now runs the link pass over the two Stage 99 forms only, with the historical owner edges stubbed: those edges only exempt archived links. The module took 263 s and now takes 22 s (35 OK), and the three malformed placeholders still produce `LINK-BROKEN`. The two escaped-descendant tests got wider budgets and an atomic child write. Under 30 busy loops on 12 cores, the three escape tests passed 10 of 10. Idle, the lane module passed 3 of 3 (90 OK) | yes | none |
| EVD-003 | [VAL-PG-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Selected staged QA | Commit `8cb8980a` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | The pre-commit staged QA, `commitizen check` and the generated-message exception hook passed | yes | none |
| EVD-004 | [VAL-PG-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Coverage guard | `test_every_test_module_runs_in_one_gate_selected_by_its_file` before and after the registry change | PASS | 74 subtests failed first; the two direct gates keep their own argv. With 11 suites registered, each of the 76 modules has exactly one gate, and its own file selects that gate in both lanes. The old archive and document runners are removed. `run-contract-tests.py --suite nope` exits 2 with an argparse error | yes | none |
| EVD-005 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Suite gate runs | `python3 scripts/run-contract-tests.py --root . --suite <id>` for every suite, run serially on the working tree that became commit `774b13bb`, with pinned tools first on `PATH` | PASS | archive: 13 modules, 286 tests, 124 s; archive-validation: 1/86, 430 s; document: 21/325, 225 s; document-lifecycle: 3/71, 98 s; validation-routing: 8/192, 54 s; qa-runner: 1/38, 569 s; ci-metadata: 3/84, 9 s; release: 2/27, 34 s; agent-governance: 5/147, 47 s; tooling: 9/156, 15 s; cluster-gate: 8 modules OK in the foreground | yes | EVD-001 |
| EVD-006 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selection tests and classification | Commit `774b13bb`: `registry.json`, the fixture, and the selection and registry tests | PASS | `validate-affected-surfaces.py --root .` PASS: 1,361 paths, uncovered 0, ambiguous 0. New surfaces: `validation-routing-scripts`, `qa-runner`, `lane-runner`, `contract-test-runner` and `archive-test-modules`. Two cluster test helpers moved to `cluster-gate-scripts`. A registry edit selects `validation-routing-tests` but not `qa-runner-tests`, and `qa.py` no longer pulls the broad script gates. Every changed fixture expectation adds only the newly intended gate. `test_validate_affected_surfaces`, `test_document_scope_selection`, `test_archive_registry_contract` and `test_validation_profiles` all OK | yes | none |
| EVD-007 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selected staged QA | First commit attempt on the same index, with pinned tools first on `PATH` and SIGINT reset to default, while another repository's validation loaded the host | FAIL | 24 gates passed. `validation-routing-tests` failed one test, `test_successful_leader_closes_silent_owned_process_group`, which used the shared helper's 2 s timeout and 0.5 s cleanup. The same suite passed on an exported index snapshot, with and without the closed `HOME` and `PATH` | yes | none |
| EVD-008 | [VAL-PG-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Load test of the bounded-command class | Commit `774b13bb`: the shared `_run_python` defaults widened to 15 s timeout and 3 s cleanup; the per-test overrides from `8cb8980a` removed | PASS | Under 30 busy loops on 12 cores, the bounded-command class failed 5 to 7 tests per run across 9 tests with the old defaults, and 0 to 2 with the new ones. The remaining failures are only the two interrupt-count tests. The lane module passes idle (90 OK, 20 s) | yes | none |
| EVD-009 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Selected staged QA | Commit `774b13bb` with pinned tools first on `PATH` and SIGINT reset to default | PASS | The pre-commit staged QA, `commitizen check` and the generated-message exception hook passed | yes | EVD-007 |
| EVD-010 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Suite gate runs | `python3 scripts/run-contract-tests.py --root . --suite cluster-gate` at commit `a4043d9d`, in the foreground with pinned tools first on `PATH` | PASS | `[PASS] cluster-gate contract regressions passed: modules=8 tests=71`, 13 s | yes | none |
| EVD-011 | [VAL-PG-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff a29c836f a4043d9d`, head `a4043d9d25897a3c592ad92be19ccb12f20e5fbe` | PASS | `approve`, no blocker or major. It compared old and new selection for every tracked non-document path in both lanes; no gate is lost for the carved scripts that other validators read. Every module has exactly one gate selected by its own file. The link test still rejects the malformed placeholders. Minor findings, dispositioned under Criterion Acceptance: the quality.py routing gap, staged QA cost, EVD-006 and EVD-008 wording, and the Spec wording for the link test and the budgets | yes | none |
| EVD-012 | [VAL-PG-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff a29c836f a4043d9d`, head `a4043d9d25897a3c592ad92be19ccb12f20e5fbe` | PASS | `approve`, no blocker or major. It compared old and new selection for every tracked non-document path in both lanes; no gate is lost for the carved scripts that other validators read. Every module has exactly one gate selected by its own file. The link test still rejects the malformed placeholders. Minor findings, dispositioned under Criterion Acceptance: the quality.py routing gap, staged QA cost, EVD-006 and EVD-008 wording, and the Spec wording for the link test and the budgets | yes | none |
| EVD-013 | [VAL-PG-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff a29c836f a4043d9d`, head `a4043d9d25897a3c592ad92be19ccb12f20e5fbe` | PASS | `approve`, no blocker or major. It compared old and new selection for every tracked non-document path in both lanes; no gate is lost for the carved scripts that other validators read. Every module has exactly one gate selected by its own file. The link test still rejects the malformed placeholders. Minor findings, dispositioned under Criterion Acceptance: the quality.py routing gap, staged QA cost, EVD-006 and EVD-008 wording, and the Spec wording for the link test and the budgets | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-PG-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004, EVD-011 | One runner runs each suite; the old runners are removed; the guard failed first and now passes | platform |
| [VAL-PG-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-002, EVD-003, EVD-008, EVD-012 | The link test takes 22 s and still rejects malformed placeholders; the bounded-command budgets hold far better under load, with two interrupt-count tests as residual risk | platform |
| [VAL-PG-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-001, EVD-005, EVD-006, EVD-007, EVD-009, EVD-010, EVD-013 | Every suite gate passes and every module selects its gate. EVD-001 is resolved by EVD-005, and EVD-007 by EVD-009 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0120-test-purpose-gates/**`,
  `docs/03.specs/README.md`, `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `scripts/validation/registry.json`, `scripts/run-contract-tests.py`,
  `scripts/run-archive-contract-tests.py`,
  `scripts/run-document-contract-tests.py`, `scripts/README.md`, `tests/**`.
- **Forbidden Paths**: `.github/workflows/**`, provider settings, other Spec
  packages' evidence, credentials.
- **Approval Required**: The operator's 2026-10-16 instruction to review and
  proceed is recorded as approval of SPEC-0120 and its Plan as written on
  2026-10-19. The operator may revoke or amend it. Push, pull request and
  merge follow RUN-0013.
- **Static Validation**: Focused tests, Ruff and `qa.py staged` on the exact
  index.
- **Live Validation**: None.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the commits through Git.
- **Evidence Location**: This Task.

## Verification Summary

All three criteria are accepted. Each of the 76 test modules now runs in
exactly one gate. The 74 suite modules run through
`scripts/run-contract-tests.py`, and the two direct gates are unchanged. A
module's own file selects its gate, and so does its product where the product
has a surface (VAL-PG-001, VAL-PG-003). The placeholder link test takes 22 s
instead of 263 s. The shared bounded-command budgets are wider, and the
escape tests write their child file atomically (VAL-PG-002). The independent
review approved with minor findings only.

Departures from the Spec text, disclosed:
- The link test was not moved to a temporary root. It runs the link pass on
  the real forms only, and stubs the historical owner edges. The stub would
  hide an archived link added to the forms later.
- The budgets were widened in the shared helper default for every positive
  path, not only in the one load-sensitive case. Boundary tests keep their
  own short values.

Corrections to the retained evidence:
- EVD-006 also moves `qa.py` and `bounded_io.py` to new surfaces. It replaces
  the hook case on the catch-all with `tests/__init__.py`. It also drops
  `agent-governance` from the hook test's forbidden set.
- `quality.py`, `validate-workspace-boundary.py` and
  `validate-knowledge-surface.py` moved to `tooling-scripts`. They no longer
  select archive-contract-tests, gitops-structure, infrastructure-contracts,
  k8s-manifests, policy-gates or secret-handling. They have no importers, and
  their own validators are kept.
- EVD-008's PASS covers the improvement, not a clean result under load.
  Under 30 busy loops on 12 cores, two interrupt-count tests still fail in 0
  to 2 cases per run.

Residual risk:
- Editing `quality.py` does not select `validation-routing-tests`, although
  two modules in that suite read it.
- No dedicated surface selects the matching suite for: the provider hook
  adapters, the external-service skill script, `validate-links-and-owners.py`
  for `archive-validation`, `json_schema_validation.py`, the gitops seeds read
  by `test_platform_ingress`, and the test fixtures on the catch-all.
- Editing the shared runner selects all 11 suites, about 1,600 s serial.
  `qa-runner` (569 s) and `archive-validation` (430 s) are under the 1,200 s
  validator timeout with about a 2x margin. The `document` suite (225 s)
  fires on template and Stage 99 edits.
- The two interrupt-count lane tests can fail under heavy load.
- A background job must reset SIGINT to default, or
  `test_infrastructure_tempfiles` fails.

Next owner: platform.
