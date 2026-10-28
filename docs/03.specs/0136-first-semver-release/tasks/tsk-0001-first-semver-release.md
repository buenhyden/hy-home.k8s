---
title: "First SemVer Release"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0136-TSK-0001"
parent_ids: ["SPEC-0136-PLAN-0001"]
---

# Task: First SemVer Release

## Overview

Prepare and record the first SemVer release, `v0.1.0`, under RUN-0012. It
executes [SPEC-0136](../spec.md) through
[WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request: on 2026-10-28 the operator chose `v0.1.0` for the first SemVer
  release.
- Start: main `65f1f4e7`, branch `release/v0.1.0`.

### Release Scope

Observed on main `65f1f4e7`. No `v*` tag exists. Nine historical
`main-<SHA>` tags exist; the latest, `main-3ff0ab62`, is from 2026-10-06 and
stays as history. Since that tag, 497 non-merge commits are on `main`: 234
`docs`, 44 `fix`, 20 `refactor`, 16 `feat`, 15 `chore`, 14 `test`, 4 `ci`,
1 `style` and 1 `docs!` (`docs(platform)!: adopt external data contract
alignment`).

| Public interface | Change class in this release |
| --- | --- |
| Supported CLI and options (`scripts/qa.py`, `scripts/release.py`, validators) | Added and changed |
| JSON Schema and registries | Changed |
| Document profiles and frontmatter | Changed |
| GitOps desired state | Changed, including the Traefik ingress cutover |
| External service interfaces | Changed by the marked breaking data-contract alignment |

As the first `0.y` release, `v0.1.0` makes no compatibility promise: any
public interface may change in a later `0.y` release.

### Tool Environment

On 2026-10-28 the first `prepare` preview stopped with
`RELEASE-TOOL-UNAVAILABLE` for `git-cliff`. The only installed copy is the
npm package under the user's NVM directory, outside the trusted system and
`~/.local/bin` locations that `scripts/run-validation-lane.py` accepts.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SR-001](../spec.md#success-criteria--verification-plan) | Review the release scope and compatibility | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-SR-002](../spec.md#success-criteria--verification-plan) | Write the changelog section with the release tool | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-SR-003](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-004 | [VAL-SR-004](../spec.md#success-criteria--verification-plan) | Record the publish preview and outcome | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Scope review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-SR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Release tool output and staged QA | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-SR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-SR-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Publication observation | Exact main commit | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SR-001](../spec.md#success-criteria--verification-plan) | pending | none | Scope review remains | platform |
| [VAL-SR-002](../spec.md#success-criteria--verification-plan) | pending | none | Changelog remains | platform |
| [VAL-SR-003](../spec.md#success-criteria--verification-plan) | pending | none | Review remains | platform |
| [VAL-SR-004](../spec.md#success-criteria--verification-plan) | pending | none | Publication remains | operator |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md` and
  `CHANGELOG.md`.
- **Forbidden Paths**: historical tags, release tooling, validators and
  workflows.
- **Approval Required**: the operator chose `v0.1.0` on 2026-10-28. Push,
  pull request and merge follow RUN-0013. Tag and Release publication is the
  operator's `publish --execute`.
- **Static Validation**: `python3 scripts/qa.py staged` on each commit.
- **Live Validation**: none; a release proves no deployment.
- **Secret / Vault Handling**: no secret is read; publication uses the
  operator's own GitHub authority.
- **Rollback Plan**: revert the pull request before publication. After
  publication, a published tag is not moved; a later release supersedes it.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
