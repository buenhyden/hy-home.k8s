---
title: "Archive Check Removal"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-03"
layer: "specs"
artifact_id: "SPEC-0140-TSK-0001"
parent_ids: ["SPEC-0140-PLAN-0001"]
---

# Task: Archive Check Removal

## Overview

Remove every check of `docs/98.archive/` and every migration check, then
delete the archived files and keep the README and structure. It executes
[SPEC-0140](../spec.md) through [WORK-001–005](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-03): minimize, and delete where possible, every CI/CD
  check of the files and entries in `docs/98.archive/`, together with the
  migration checks. The operator chose full deletion over disabling gates.
- Follow-up (2026-11-03): after that, delete the files in `docs/98.archive/`
  and keep only its README and directory structure.
- Follow-up (2026-11-03): in every folder a README is for human readers and
  an `AGENTS.md` is for AI agents, reflected in the workspace governance and
  rules. The operator chose an `AGENTS.md` only where a folder has agent
  rules of its own.
- Follow-up (2026-11-03): summarize the deleted archive content in the
  relevant documents of `docs/01.requirements/` and `docs/02.architecture/`,
  then confirm other branches and worktrees are contained in this branch,
  clean them up, and bring `main` and `origin/main` up to date.
- Follow-up (2026-11-03): delete legacy and deprecated parts of QA and CI/CD
  and one-time scripts, tests and QA checks. The operator chose to retire the
  completed SPEC-0105, SPEC-0106 and SPEC-0107 packages so the legacy Task
  binding can be deleted.
- Follow-up (2026-11-03): Stages 01, 02 and 03 admit no legacy or deprecated
  document state or form; existing ones are investigated and cleaned up, and
  the rule is reflected in governance. The operator chose to forbid document
  states only.
- Follow-up (2026-11-03): each folder `AGENTS.md` references the matching
  `.agents`, `.claude` and `.codex` files and states the folder's purpose; an
  `AGENTS.md` exists only where the folder's role needs one, governance states
  when a folder holds both files or a README alone, and the `AGENTS.md` files
  under `examples/azure/` subfolders are removed.
- Follow-up (2026-11-03): delete the completed Spec, Plan and Task documents in
  `docs/03.specs/`.
- Follow-up (2026-11-03): the operator chose logical commits, a pushed branch
  and a pull request; merge waits for a separate request.
- Start: main `69445fca`, branch `refactor/archive-check-removal`.
- Hosted CI (`.github/workflows/ci.yml`) already ran no archive check; the
  checks lived in the local QA registry and the document validators.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ARC-001](../spec.md#success-criteria--verification-plan) | Remove archive and migration checks, their tests, registry entries and policy text | platform | ready | NOT_RUN | EVD-001 |
| WORK-002 | [VAL-ARC-002](../spec.md#success-criteria--verification-plan) | Delete archived files, keep README and structure, repoint current links, summarize them in Stage 01 and 02 owners | platform | ready | NOT_RUN | EVD-002 |
| WORK-003 | [VAL-ARC-003](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | ready | NOT_RUN | EVD-003 |
| WORK-005 | [VAL-ARC-005](../spec.md#success-criteria--verification-plan) | Delete legacy, deprecated and one-time QA and CI/CD items, refuse legacy document states in Stages 01 to 03, and delete completed Spec packages | platform | ready | NOT_RUN | EVD-005 |
| WORK-004 | [VAL-ARC-004](../spec.md#success-criteria--verification-plan) | Separate README (human) and AGENTS.md (agent) audiences | platform | ready | NOT_RUN | EVD-004 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ARC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Validators, test suites and QA | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-ARC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Tree listing and link check | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-ARC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-ARC-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Contract suites, validators and QA | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-ARC-004](../spec.md#success-criteria--verification-plan) | WORK-004 | README search, registry and link checks | Exact revision | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ARC-001](../spec.md#success-criteria--verification-plan) | pending | EVD-001 | Awaiting evidence | platform |
| [VAL-ARC-002](../spec.md#success-criteria--verification-plan) | pending | EVD-002 | Awaiting evidence | platform |
| [VAL-ARC-003](../spec.md#success-criteria--verification-plan) | pending | EVD-003 | Awaiting evidence | platform |
| [VAL-ARC-005](../spec.md#success-criteria--verification-plan) | pending | EVD-005 | Awaiting evidence | platform |
| [VAL-ARC-004](../spec.md#success-criteria--verification-plan) | pending | EVD-004 | Awaiting evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/`, `tests/`, `docs/99.templates/`,
  `docs/98.archive/`, `.pre-commit-config.yaml`, `.markdownlint-cli2.yaml`,
  `.agents/`, `.claude/`, `.codex/`, governance READMEs, REQ-0003, ADR-0040,
  ADR-0053, current documents that link into the archive, READMEs and folder
  `AGENTS.md` files, Stage 01 and 02 documents that receive archived
  lineage, completed Spec packages in `docs/03.specs/`, and this package.
- **Forbidden Paths**: `.github/workflows/`, cluster objects, secrets and
  other repositories.
- **Approval Required**: the operator's requests above. Commit, push, pull
  request and merge each need the operator's request.
- **Static Validation**: strict document validators, the affected
  contract-test suites and `python3 scripts/qa.py staged`.
- **Live Validation**: none; no cluster object changes.
- **Secret / Vault Handling**: no secret is read; secret scanning stays.
- **Rollback Plan**: revert the commits; `git show <commit>:<path>` recovers
  one file.
- **Evidence Location**: this Task.

## Verification Summary

Pending.
