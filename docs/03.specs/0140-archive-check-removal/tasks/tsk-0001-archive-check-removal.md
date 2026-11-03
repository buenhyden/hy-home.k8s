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
- Follow-up (2026-11-03): after completion, check every README.md and
  AGENTS.md, the subfolders of `.agents`, `.claude` and `.codex`, and the
  subfolders of `docs/01.requirements`, `docs/02.architecture`,
  `docs/05.operations` and `docs/99.templates` for text that differs from or
  conflicts with the current implementation, and correct and complete it.
- Approval (2026-11-03): the operator accepted ADR-0048.
- Approval (2026-11-03): the operator accepted VAL-ARC-001 to VAL-ARC-005
  after the published independent review of PR #197.
- Follow-up (2026-11-03): each of `docs/01.requirements`,
  `docs/02.architecture`, `docs/03.specs`, `docs/05.operations`,
  `docs/90.references` and `docs/99.templates` holds an `AGENTS.md` written
  for that folder's purpose and role in the `AGENTS.md` form.
- Start: main `69445fca`, branch `refactor/archive-check-removal`.
- Hosted CI (`.github/workflows/ci.yml`) already ran no archive check; the
  checks lived in the local QA registry and the document validators.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ARC-001](../spec.md#success-criteria--verification-plan) | Remove archive and migration checks, their tests, registry entries and policy text | platform | completed | PASS | EVD-006 |
| WORK-002 | [VAL-ARC-002](../spec.md#success-criteria--verification-plan) | Delete archived files, keep README and structure, repoint current links, summarize them in Stage 01 and 02 owners | platform | completed | PASS | EVD-007 |
| WORK-003 | [VAL-ARC-003](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | completed | PASS | EVD-010 |
| WORK-005 | [VAL-ARC-005](../spec.md#success-criteria--verification-plan) | Delete legacy, deprecated and one-time QA and CI/CD items, refuse legacy document states in Stages 01 to 03, and delete completed Spec packages | platform | completed | PASS | EVD-008 |
| WORK-004 | [VAL-ARC-004](../spec.md#success-criteria--verification-plan) | Separate README (human) and AGENTS.md (agent) audiences | platform | completed | PASS | EVD-009 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ARC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Validators, test suites and QA | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-ARC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Tree listing and link check | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-ARC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-ARC-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Contract suites, validators and QA | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-ARC-004](../spec.md#success-criteria--verification-plan) | WORK-004 | README search, registry and link checks | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-006 | [VAL-ARC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Validators, test suites and QA | Exact revision | PASS | Commits `9e7cf390` and `dcbbf84a`: staged QA hook, strict link, Markdown-profile, lifecycle and repository-quality checks | yes | EVD-001 |
| EVD-007 | [VAL-ARC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Tree listing and link check | Exact revision | PASS | Commit `dcbbf84a`: `docs/98.archive/` holds README and `.gitkeep` only; strict link check passes | yes | EVD-002 |
| EVD-008 | [VAL-ARC-005](../spec.md#success-criteria--verification-plan) | WORK-005 | Contract suites, validators and QA | Exact revision | PASS | Commits `dcbbf84a` and `13f6115c`: staged QA hook, contract suites and strict lifecycle check | yes | EVD-005 |
| EVD-009 | [VAL-ARC-004](../spec.md#success-criteria--verification-plan) | WORK-004 | README search, registry and link checks | Exact revision | PASS | Commits `dcbbf84a` and `13f6115c`: README audience search, registry profile, agent-governance and link checks | yes | EVD-004 |
| EVD-010 | [VAL-ARC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review and hosted checks | Exact pull request head | PASS | PR #197 head `5d7b7641`: RUN-0013 `independent-review` check run `125945829687` (App `5341483`, success); `ci-summary` and `style-pr` run `41642458090` pass | yes | EVD-003 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ARC-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-006 | Operator accepted on 2026-11-03 | platform |
| [VAL-ARC-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-007 | Operator accepted on 2026-11-03 | platform |
| [VAL-ARC-003](../spec.md#success-criteria--verification-plan) | accepted | EVD-010 | Operator accepted on 2026-11-03 | platform |
| [VAL-ARC-005](../spec.md#success-criteria--verification-plan) | accepted | EVD-008 | Operator accepted on 2026-11-03 | platform |
| [VAL-ARC-004](../spec.md#success-criteria--verification-plan) | accepted | EVD-009 | Operator accepted on 2026-11-03 | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `scripts/`, `tests/`, `docs/99.templates/`,
  `docs/98.archive/`, `.pre-commit-config.yaml`, `.secrets.baseline`,
  `.markdownlint-cli2.yaml`,
  `.agents/`, `.claude/`, `.codex/`, governance READMEs, REQ-0003, ADR-0040,
  ADR-0053, current documents that link into the archive, READMEs and folder
  `AGENTS.md` files, Stage 01 and 02 documents that receive archived
  lineage, Stage 01, 02, 05 and 90 documents whose text describes the removed
  model, completed Spec packages in `docs/03.specs/`, and this package.
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

- Every commit passed `python3 scripts/qa.py staged` through the pre-commit
  hook on its exact index; platform live and syntax depths stay DEFER with
  their named fallbacks.
- `9e7cf390` fixed a pre-existing false positive: the kubeconfig rule flagged
  read-only `kubectl config current-context`. A regression case covers it.
- The non-style gate scans against the HEAD secret baseline, so the registry
  baseline line moved one commit ahead of the profile removal.
- Residual risk: the cancelled-Task `not-required` waiver lost its direct
  regression test, and native runtime behavior was not observed.
- An in-session review of `13f6115c` reported no blocking issue; its two
  medium and actionable low findings are fixed in `6275f513`. It is not the
  independent review.
- The RUN-0013 independent review of PR #197 head `1a0148bd` from a separate
  session returned `approve` with one medium and two low findings and was
  not published. This change fixes the medium finding (stale SPEC-0115 and
  SPEC-0116 owners in `.github/rulesets/main-protection.md`) and the
  `.gitignore` comment, so the final head needs a new review.
- Residual risk accepted under ADR-0053: no hook or validator stops a write
  under `docs/98.archive/` or a recreated `docs/00.agent-governance/`
  Markdown file; non-Markdown paths there still fail surface selection.
- Left as is: the SPEC-0123 comment in `.github/workflows/ci.yml` is outside
  the allowed paths, and `.codex/rules/default.rules` is digest-pinned by
  the agent-governance validator.
- The second RUN-0013 review of head `5d7b7641` returned `approve` with one
  low finding (the two comments above) and was published as check run
  `125945829687`; every hosted check passed on that head.
- The operator accepted all five criteria on 2026-11-03.
