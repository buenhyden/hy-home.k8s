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
| WORK-001 | [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | Declared controller identity in `ingress.py` | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-ICI-002](../spec.md#success-criteria--verification-plan) | Remove duplicated shell assertions | platform | in-progress | NOT_RUN | Pending named repository evidence |

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

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ICI-001](../spec.md#success-criteria--verification-plan) | pending | none | Validator change and tests remain | platform |
| [VAL-ICI-002](../spec.md#success-criteria--verification-plan) | pending | none | Mutation proof and removal remain | platform |

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

Pending.
