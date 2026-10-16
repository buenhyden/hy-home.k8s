---
title: "Ingress Controller Identity Execution"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-16"
layer: "specs"
artifact_id: "SPEC-0119-TSK-0001"
parent_ids: ["SPEC-0119-PLAN-0001"]
---

# Task: Ingress Controller Identity Execution

## Overview

Execute [SPEC-0119](../spec.md) through [WORK-001–002](../plan.md#work-breakdown):
one declared ingress controller identity in the validator and no duplicated
shell assertions.

## Inputs

- The operator's 2026-10-16 instruction to proceed as recommended: phase two
  of the local QA review and item 18 (nginx hard-wiring) before the ingress
  replacement ADR.
- Start: main `ad3e187f` (PR #157 merge), branch
  `refactor/spec-0119-ingress-controller-identity`.
- A read-only `network-reviewer` scoping report of the same date.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | Declared controller identity in `ingress.py` | platform | completed | PASS | EVD-003 tests resolving EVD-001, EVD-004 assurance, EVD-005 staged QA, EVD-009 review |
| WORK-002 | [VAL-ICI-002](../spec.md#success-criteria--verification-plan) | Remove duplicated shell assertions | platform | completed | PASS | EVD-006 mutation proof, EVD-007 shell validator, EVD-008 staged QA, EVD-010 review |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Ingress focused tests | `scripts/validation/platform/ingress.py`, `tests/test_platform_ingress.py` on this branch | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Literal inventory | `git grep` of nginx identity literals at main `ad3e187f` | PASS | 35 hits in `scripts/validation/platform/ingress.py`, 6 in `scripts/validate-infrastructure-contracts.sh`; none in `policy/`, `.kube-linter.yaml` or `scripts/validation/registry.json` | no | none |
| EVD-003 | [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Ingress focused tests | `scripts/validation/platform/ingress.py`, `tests/test_platform_ingress.py` at commit `a97f4ad1` | PASS | Three identity-swap tests (ingress class, namespace, redirect annotation) errored before the change and pass after; `Ran 15 tests ... OK` with the 12 existing tests unchanged; Ruff check and format clean. `nginx` now appears only in `CONTROLLER` and the `ingress-nginx` kind check | yes | EVD-001 |
| EVD-004 | [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Platform assurance | `python scripts/validation/platform/assurance.py --root .` at commit `a97f4ad1` | PASS | rc 0; 46 PASS, 45 DEFER (existing external CRD schema, live-check and pre-commit fallbacks), 1 NOT_APPLICABLE, 0 FAIL | yes | none |
| EVD-005 | [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Selected staged QA | Commit `a97f4ad1` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | `Validate Staged QA Snapshot`, `commitizen check` and the generated-message exception hook passed | yes | none |
| EVD-006 | [VAL-ICI-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Mutation proof | Session script mutating each field a removed shell assertion checked, run against `ingress.py` at `a97f4ad1` | PASS | All 17 mutations fail `ingress.py`: adminer class (`INGRESS_ROUTE`), `service-upstream` and `upstream-vhost` (`INGRESS_MESH`), controller Service type and both NodePorts (`INGRESS_OWNER`), and each of five apex redirects and paths (`INGRESS_REDIRECT`, `INGRESS_ROUTE`); the unmutated baseline is clean | yes | none |
| EVD-007 | [VAL-ICI-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Shell validator | `bash scripts/validate-infrastructure-contracts.sh` and `shellcheck` at commit `4d3ac644` | PASS | `[PASS] static contract verification passed`, rc 0; shellcheck clean. Removed the LoadBalancer, adminer class and mesh annotation, NodePort and apex redirect assertions and the unused `APEX_REDIRECTS`; the admission Job sidecar check now uses `$INGRESS_APP`; the k3d serverlb bindings stay | yes | none |
| EVD-008 | [VAL-ICI-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Selected staged QA | Commit `4d3ac644` with pinned `/tmp/hyhome-r10-validation/bin` first on `PATH` | PASS | `Validate Staged QA Snapshot`, `commitizen check` and the generated-message exception hook passed | yes | none |
| EVD-009 | [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff ad3e187f a318ba1e`, head `a318ba1ec4c53605bb983597108cd8ce2045f5fa` | PASS | `approve`, no critical, high or medium finding. Behavior is equivalent for the current identity: routes, annotation keys and the chart-value block rebuild to the same values. LOW: a controller of another kind needs only parseable values, and the default `CONTROLLER` argument is shared but never mutated | yes | none |
| EVD-010 | [VAL-ICI-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Independent branch review | Fresh `code-reviewer` session, read-only, `git diff ad3e187f a318ba1e`, head `a318ba1ec4c53605bb983597108cd8ce2045f5fa` | PASS | `approve`, no critical, high or medium finding. The reviewer reran the mutation script, and all 16 mutations were caught. `gitops-desired-state` selects both `infrastructure-contracts` and `platform-assurance` for every path a removed line read. LOW: EVD-006 counts 17 mutations; the script runs 16 plus a clean baseline | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-001, EVD-002, EVD-003, EVD-004, EVD-005, EVD-009 | One declared identity; existing behavior unchanged; EVD-001 is resolved by EVD-003 | platform |
| [VAL-ICI-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-006, EVD-007, EVD-008, EVD-010 | Duplicated shell assertions removed after mutation proof; the mutation count is 16 plus a clean baseline, not 17 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/03.specs/0119-ingress-controller-identity/**`,
  `docs/03.specs/README.md`, `docs/01.requirements/0004-current-local-gitops-platform.md`,
  `scripts/validation/platform/ingress.py`,
  `scripts/validate-infrastructure-contracts.sh`, `tests/test_platform_ingress.py`.
- **Forbidden Paths**: `gitops/**`, `infrastructure/**`, `policy/**`,
  `.github/workflows/**`, credentials.
- **Approval Required**: The operator's "proceed as recommended" is recorded
  as approval of SPEC-0119 and its Plan as written on 2026-10-16; the operator
  may revoke or amend it. Push, pull request and merge follow RUN-0013.
- **Static Validation**: Focused tests, assurance, the shell validator, Ruff
  and `qa.py staged` on the exact index.
- **Live Validation**: None; no cluster access.
- **Secret / Vault Handling**: No secret is read or written.
- **Rollback Plan**: Revert the commits through Git.
- **Evidence Location**: This Task.

## Verification Summary

Both criteria are accepted. `ingress.py` declares the ingress controller
identity once and keeps today's ingress-nginx behavior: the 12 existing tests
pass unchanged, three identity-swap tests pass, and platform assurance has no
FAIL (VAL-ICI-001). The shell assertions that duplicated it are removed after
16 mutations were caught by `ingress.py` (VAL-ICI-002). An independent review
approved the branch.

Residual risk: a controller of another kind is checked only for a matching
Application and parseable values. The controller-swap change must add that
controller's value checks and replace the remaining HTTPS port literal. The
change that admits Gateway API kinds must add their validators in the same
change. Next owner: platform, for the ingress replacement ADR.
