---
title: "External Item Decisions"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0135-TSK-0001"
parent_ids: ["SPEC-0135-PLAN-0001"]
---

# Task: External Item Decisions

## Overview

Record the operator's 2026-10-28 decisions and the read-only observations for
five of the eight `EXTERNAL` survey CRs. It executes [SPEC-0135](../spec.md)
through [WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request: on 2026-10-28 the operator chose to read the private archive
  layouts, granted `read:project`, accepted the rewritten survey text, accepted
  a mock-only provider-limit record and accepted the CR-12.01 setup.
- Start: `7142c6a8`, branch `docs/external-item-decisions`.

### Decisions

| CR | Decision | Effect |
| --- | --- | --- |
| CR-01.02 | The operator accepts the rewritten survey text in place of the original attachment | Closed |
| CR-12.01 | The operator accepts the observed visibility, required checks, runners and QA routes recorded in SPEC-0133 as the target; private branch protection stays unavailable on the current plan | Closed; the plan limit is accepted residual risk |
| CR-18.06 | The operator accepts a mock-only record. No repository code calls an LLM provider, so no provider-limit mock or live response exists. The nearest repository tests bound processes, such as the timeout and pipe-overflow tests in `tests/test_agent_governance_consumers.py` and `tests/test_archive_integrity.py`. This record is not operational evidence | Closed as mock-only, not operational |

### CR-08.01 Archive Layouts

Top-level entries of `docs/98.archive/`, read on 2026-10-28.

| Repository | Branch | Source | Entries |
| --- | --- | --- | --- |
| `hy-home.k8s` | `main` | local tree | `README.md`, `completed`, `migrations`, `superseded` |
| `hy-home.docker` | `main` | local clone | `README.md`, `completed`, `migrations`, `retention-catalog.md`, `retired`, `superseded`, `tombstones` |
| `blog-data` | `main` and `dev` | `gh api` contents | `README.md`, `catalog.md`, `completed`, `retired`, `superseded` |
| `Project-Template` | `dev` | local clone and `gh api` contents | `README.md`, `completed`, `retired`, `superseded` |
| `Project-Template` | `main` | `gh api` contents | `README.md` only |

Unifying them still needs the joint edition approval that CR-03.06 and
CR-03.07 wait on, so CR-08.01 stays `EXTERNAL` with the layouts recorded.

### CR-14.03 Projects Observation

A GraphQL `projectsV2` query with the `read:project` scope on 2026-10-28
returned one user Project, number 1, untitled, closed, private, last updated
2026-01-09, with 0 items. No Project is linked to `hy-home.k8s`. No projection
exists to test, so CR-14.03 is not applicable until the operator chooses one.

### Remaining

CR-03.06 and CR-03.07 wait on a joint edition approval across the four
repositories. CR-09.04 waits on live cluster and certificate acceptance.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-XD-001](../spec.md#success-criteria--verification-plan) | Record the three operator decisions | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-XD-002](../spec.md#success-criteria--verification-plan) | Record the archive layouts and the Projects observation | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-XD-003](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | draft | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-XD-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Decision record and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-XD-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Observation record and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-XD-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-XD-001](../spec.md#success-criteria--verification-plan) | pending | none | Review remains | platform |
| [VAL-XD-002](../spec.md#success-criteria--verification-plan) | pending | none | Review remains | platform |
| [VAL-XD-003](../spec.md#success-criteria--verification-plan) | pending | none | Review and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index and
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`.
- **Forbidden Paths**: other repositories, GitHub settings, Projects, tokens,
  validators and the registry.
- **Approval Required**: the operator decided on 2026-10-28 (Inputs). Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: `python3 scripts/qa.py staged` on each commit.
- **Live Validation**: none.
- **Secret / Vault Handling**: no secret, credential or private file content
  is read; only directory names and Project metadata.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
