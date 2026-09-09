---
title: "Close the Documentation Entry Point and the Gaps It Exposed"
version: "1.0.2"
type: "sdlc/task"
status: "in-progress"
owner: "platform"
updated: "2026-09-09"
layer: "specs"
artifact_id: "SPEC-0072-TSK-0003"
---

# Task: Close the Documentation Entry Point and the Gaps It Exposed

## Overview

Execute [WP-011](../plan.md#wp-011-close-the-documentation-entry-point-and-the-gaps-it-exposed)
as five bounded units. The approved request adds one contract, `C-AGQ-014`, and
the sweep it required surfaced four defects in surfaces this Spec already owns.
This Task also records the per-gate timing that
[SPEC-0072-TSK-0001](tsk-0001-consolidate-governance-and-quality-gates.md)
left as a `DEFER`; it neither reopens nor completes that Task's native stream.

The lifecycle domain owns creation, so this record opened at the
zero-indegree `queued` state and moves through `in-progress` while the units
run; it reaches `done` once the final full-profile result is recorded. The work items below already carry their focused
evidence and implementation commits.

## Inputs

- [SPEC-0072](../spec.md), criterion `VAL-AGQ-020` and contract `C-AGQ-014`.
- [SPEC-0072-PLAN-0001](../plan.md), `WP-011A` through `WP-011E`.
- [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md):
  `REQ-0003-FR-0012` and `REQ-0003-NFR-0002`.
- Branch `refactor/governance-qa-consolidation`, clean baseline `80a0ce68`,
  which is also `main` and `origin/main` at intake.
- The prior Task's recorded limitation: full QA used the existing cache and
  "cache-miss/setup and per-gate timing were not separately instrumented, so a
  controlled cold/warm comparison remains DEFER".

## Task Table

| ID       | Upstream criterion | Work item                                                                                                                      | Owner    | Status | Result                                                                  | Evidence                                                                              |
| -------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------ | -------- | ------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| WORK-015 | VAL-AGQ-020        | Report a numbered stage link written outside `docs/` and convert the existing 99 links to plain-text stage references          | platform | Done   | PASS: focused RED/GREEN, exact-index staged QA                          | `ce423abd`; `LINK-STAGE-BOUNDARY` observed on a reintroduced link, then absent        |
| WORK-016 | VAL-AGQ-020        | Bind the pre-action selector bound to the registered hook budget and scope the Claude runtime variables to the Claude provider | platform | Done   | PASS: focused RED/GREEN, 54 guard tests, exact-index staged QA          | `4dbedfe1`; `60 not less than or equal to 10` observed before the fix                 |
| WORK-017 | VAL-AGQ-020        | Apply the stage index contract to the Archive index and narrow the retained-payload exemption                                  | platform | Done   | PASS: focused RED/GREEN, exact-index staged QA                          | `f1c1a711`; `FM-DELIMITER` observed on the index once the exemption was narrowed      |
| WORK-018 | VAL-AGQ-019        | Correct four current statements that described absent behavior and move the asserted template phrase with them                 | platform | Done   | PASS: focused contract checks, exact-index staged QA                    | `f484ab5e`; the quality gate rejected the stale phrase and accepted the corrected one |
| WORK-019 | VAL-AGQ-014        | Give the shared Git object fixture one owner and remove the test-module-as-library imports                                     | platform | Done   | PASS: 220 tests across the five affected modules, exact-index staged QA | `c9f5cd29`                                                                            |
| WORK-020 | VAL-AGQ-003        | Instrument per-gate timing and record the full profile baseline the prior Task deferred                                        | platform | Done   | PASS: two instrumented full runs on the same warm cache                 | Recorded below; cold-cache comparison remains `DEFER`                                 |
| WORK-021 | VAL-AGQ-002 | Give the Codex reasoning effort a registry owner and declare every departure as data | platform | Done | PASS: focused RED/GREEN and 18 registry tests | Binding `{top: xhigh, worker: high}` with four declared overrides; no observed value changed |
| WORK-022 | VAL-AGQ-019 | Close the remaining current-guidance gaps the review surfaced | platform | Done | PASS: focused governance and quality checks | Supported-version claim, Codex prompt-projection gap, and CI lock refresh ownership |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/validate-links-and-owners.py`,
  `scripts/provider_write_guard.py`, `scripts/validate-markdown-profiles.py`,
  `scripts/validation/repository/quality.py`, `tests/git_fixture.py`,
  `tests/test_documentation_link_boundary.py`,
  `tests/test_k8s_pre_edit_hook.py`,
  `tests/test_common_agents_document_routes.py`, the five archive/lifecycle
  test modules that shared the duplicated fixture, `tests/README.md`,
  `.agents/governance/document-authoring.md`, `.claude/README.md`,
  `.github/repository-surface.md`, `.github/PULL_REQUEST_TEMPLATE.md`,
  `docs/98.archive/README.md`, the 24 documents that carried a stage link, and
  this package's Spec, Plan and Task records.
- **Protected Actions Not Taken**: no push, pull request, merge, tag, remote
  workflow dispatch, branch or worktree removal, branch-protection change,
  cluster, Argo CD, Vault or cloud mutation, and no user global configuration
  change. `core.hooksPath` was inspected and left untouched.
- **Commit Messages**: the effective `core.hooksPath` resolves to a user-owned
  directory that registers `pre-commit` and `pre-push` but no `commit-msg`, so
  the repository's Commitizen hook does not run on commit. Each message was
  therefore validated in the pinned environment with
  `pre-commit run commitizen --hook-stage commit-msg --commit-msg-filename`
  against the exact file used for the commit, and every commit ran through the
  active hooks without `--no-verify`.
- **Live Validation**: `DEFER` — not required or authorized for this scope.

## Verification Summary

### Focused evidence

Each behavior-changing unit reproduced its defect before the fix:

| Unit    | Failing observation before the change                                                                                                                                     | Passing observation after                                                                                                                     |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| WP-011A | `FAIL LINK-STAGE-BOUNDARY scripts/README.md ... actual="docs/02.architecture/decisions/0031-current-corpus-retention-and-validation-ownership.md"` on a reintroduced link | `PASS CROSS-DOCUMENT` with the link written as a plain-text reference                                                                         |
| WP-011B | `AssertionError: 60 not less than or equal to 10`                                                                                                                         | 54 guard tests pass, 4 skipped                                                                                                                |
| WP-011C | `'FM-DELIMITER' not found in set()` — the index produced no diagnostic at all                                                                                             | `FAIL FM-DELIMITER docs/98.archive/README.md common/readme-stage-index` once the exemption was narrowed, then `PASS` with frontmatter present |
| WP-011D | `ERR .github/PULL_REQUEST_TEMPLATE.md missing GitHub/GitOps review phrase`                                                                                                | `[PASS] repository quality gates passed`                                                                                                      |
| WP-011E | Not a defect reproduction: a behavior-preserving merge, verified by running all five affected modules                                                                     | 220 tests pass in 530 s                                                                                                                       |

### Per-gate timing

Two instrumented `python3 scripts/qa.py full` runs on the same warm
pre-commit cache, one process, gates executed sequentially by the runner.
Times are the elapsed interval between consecutive result lines, so each
value includes that gate's process start and teardown.

| Gate                                  | Baseline `80a0ce68` | After `c9f5cd29`                    |
| ------------------------------------- | ------------------- | ----------------------------------- |
| unit-tests                            | 753.4 s             | recorded in the final handoff below |
| document-lifecycle                    | 107.6 s             | recorded in the final handoff below |
| links-and-owners                      | 88.1 s              | recorded in the final handoff below |
| agent-governance                      | 43.0 s              | recorded in the final handoff below |
| pre-commit                            | 32.4 s              | recorded in the final handoff below |
| archive-cutover                       | 12.7 s              | recorded in the final handoff below |
| the remaining fifteen gates, combined | under 15 s          | recorded in the final handoff below |
| **profile total**                     | **1051.2 s**        | recorded in the final handoff below |

Four gates hold roughly ninety-five per cent of everything except the test
suite, and the suite itself holds about seventy per cent of the profile. The
structural cause is recorded rather than acted on here: nineteen of the
twenty-two registered validators declare no path input, so they scan the whole
repository in every lane, and `document-lifecycle` and `agent-governance` are
selected into `quick` and `staged` as well. Within the suite, six archive and
lifecycle modules hold every temporary Git repository the suite builds.

No target figure is proposed from these numbers. A cold-cache comparison,
hosted runner timing and any per-validator profiling below the gate boundary
remain `DEFER`; the runs above shared the machine with other work, so they
bound the gate ranking rather than establish a precise absolute cost.

### Limitations

| Lane                    | Result                      | Basis                                                                                                                  |
| ----------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Repository-static local | See the final handoff below | Instrumented `full` on the final tree                                                                                  |
| Hosted CI               | `DEFER`                     | No authorized remote execution for this branch; the baseline hosted run belongs to a different commit                  |
| Provider native runtime | `DEFER`                     | Guard changes are covered by static regressions; hook delivery, discovery and model resolution need a separate session |
| Live and cross-platform | `DEFER`                     | No live invocation and no untested-platform guarantee                                                                  |

### Reviewed limitations and their disposition

| Item | Disposition | Basis |
| --- | --- | --- |
| Hosted CI for these commits | `DEFER` | No authorized push or remote dispatch. The merge performed here is local, so no hosted run exists for this work. |
| Provider native runtime | `DEFER` | The guard and projection changes carry static regressions. Discovery, hook delivery, model and effort resolution need a fresh authorized session on each client. |
| Live cluster, Argo CD and Vault | `DEFER` | Out of scope and unauthorized; no live command was issued. |
| Cold-cache timing comparison | `DEFER` | Clearing the shared pre-commit cache would destroy a 4.2 GB user-owned cache and rebuild every hook environment from source. Not performed for a measurement. |
| Automated Python dependency updates | Closed as documented, not automated | `scripts/validate-ci-python-contract.py` asserts the exact resolved pins, so an automated bump would open a pull request that cannot pass its own gate. The manual refresh ownership is now stated. |
| `greetings.yml` job permissions | No change | The job omits `contents: read`, which withholds rather than grants. Adding it would widen the token. |
| `DEBT_PATH` naming a `tests/fixtures` path | No change | The path is asserted absent as a retired-source denylist entry, the same shape as the other retired paths; nothing is read as runtime input. |
| Brittle corpus-count and pinned-SHA assertions in the suite | Recorded, not changed | Roughly thirty assertions pin counts or commit identifiers against the repository's own test guidance. Changing them is a suite-wide contract decision with its own review, not a side effect of this scope. |
| `scripts/validate-infrastructure-contracts.sh` classified as a validator under a `tests/` path | Recorded, not moved | Moving it touches the execution registry argv, the shell hook selectors and two READMEs; it is a separate reviewable change. |
| Two remaining test-module-as-library imports | Recorded, not changed | `load_validator` and one validator handle are single definitions imported by one consumer each, not duplicated definitions. |

## Traceability

[SPEC-0072](../spec.md) owns `C-AGQ-014` and `VAL-AGQ-020`;
[SPEC-0072-PLAN-0001](../plan.md) owns `WP-011`. The
[original Task](tsk-0001-consolidate-governance-and-quality-gates.md) keeps its
native follow-up stream, and the
[repair Task](tsk-0002-repair-governance-and-validation-contracts.md) keeps the
completed `WORK-010` stream. Neither is reopened here.

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-015](../plan.md#wp-011-close-the-documentation-entry-point-and-the-gaps-it-exposed) | Done / PASS for the approved local scope. | `VAL-AGQ-020`; `ce423abd`; focused RED/GREEN and exact-index staged QA |
| [WORK-016](../plan.md#wp-011-close-the-documentation-entry-point-and-the-gaps-it-exposed) | Done / PASS for the approved local scope. | `VAL-AGQ-020`; `4dbedfe1`; focused RED/GREEN and 54 guard tests |
| [WORK-017](../plan.md#wp-011-close-the-documentation-entry-point-and-the-gaps-it-exposed) | Done / PASS for the approved local scope. | `VAL-AGQ-020`; `f1c1a711`; focused RED/GREEN and exact-index staged QA |
| [WORK-018](../plan.md#wp-011-close-the-documentation-entry-point-and-the-gaps-it-exposed) | Done / PASS for the approved local scope. | `VAL-AGQ-019`; `f484ab5e`; asserted template phrase moved with its prose |
| [WORK-019](../plan.md#wp-011-close-the-documentation-entry-point-and-the-gaps-it-exposed) | Done / PASS for the approved local scope. | `VAL-AGQ-014`; `c9f5cd29`; 220 tests across the five affected modules |
| [WORK-020](../plan.md#wp-011-close-the-documentation-entry-point-and-the-gaps-it-exposed) | Done / PASS locally; cold-cache and hosted timing DEFER. | `VAL-AGQ-003`; two instrumented full runs on one warm cache |
| [WORK-021](../plan.md#wp-011-close-the-documentation-entry-point-and-the-gaps-it-exposed) | Done / PASS for the approved local scope. | `VAL-AGQ-002`; registry binding, four declared overrides and 18 registry tests |
| [WORK-022](../plan.md#wp-011-close-the-documentation-entry-point-and-the-gaps-it-exposed) | Done / PASS for the approved local scope. | `VAL-AGQ-019`; governance and repository-quality checks |
