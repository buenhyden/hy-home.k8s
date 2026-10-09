---
title: "Commit, Release and Work Tracking Follow-up"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-09"
layer: "specs"
artifact_id: "SPEC-0107-TSK-0004"
parent_ids: ["SPEC-0107-PLAN-0001"]
---

# Task: Commit, Release and Work Tracking Follow-up

## Overview

This Task owns P06 execution for [WORK-004](../plan.md#work-breakdown) and
[VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan). Completed
[Tasks 0001–0003](../spec.md#overview) retain their original results. This
new Task will record actual commit grammar, hook, release and Issue/Project
consumer repairs and one bounded local criterion decision.

## Inputs

- Intake on 2026-10-09: clean local `main` at
  `45c2d800e6a89509bd7a4473c3382ca7ef44aa63`, with isolated branch
  `codex/p06-git-release` and worktree `.worktrees/p06-git-release` created
  from that commit. No audit SHA reset or previous Task reopening occurred.
- The current [Spec](../spec.md), [Plan](../plan.md),
  [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md),
  [ADR-0048](../../../02.architecture/decisions/0048-local-qa-and-semver-release-ownership.md),
  [Git policy](../../../../.agents/governance/git.md),
  [commit-message prompt](../../../../.agents/prompts/commit-message.md),
  [release Runbook](../../../05.operations/runbooks/0012-main-release-preparation-runbook.md),
  and [hosted surface](../../../../.github/repository-surface.md) are the
  current owners to compare with their code and direct consumers.
- The user's P06 instruction authorizes local investigation, bounded policy
  and consumer repair, selected local validation, normal logical commits,
  local main integration and owned branch/worktree cleanup. It does not
  authorize tag or Release publication, remote Issue/Project mutation,
  workflow dispatch, server settings, credentials, deployment or live action.
- The same `WGOV-CORE / 3.0.0-draft.3` common review candidate has proposed
  owner `buenhyden`, proposed source
  `Project-Template/.agents/governance/shared-standard.md` and inspected
  content digest
  `sha256:3f46c63daae094649edccec33682ecba99844b184c4b78b558281c7c05ff3271`.
  C02/C05/C07/C10 are comparison inputs. Source revision and approval
  reference remain absent; no final common edition, local adoption or joint
  adoption is claimed.
- Read-only remote input at this intake is recorded in ignored checkout-root
  `_workspace/p06-git-release/server-readback.json`, SHA-256
  `fa0fc6e1aa87d9c34e6b67f2066bac7d3d3488b4e10e6b1f1a38fd91f54bd0b2`.
  The current main branch requires `ci-summary` and `style-pr` from App 15368;
  applied branch rulesets are empty and two inherited rulesets cover only
  historical `main-*` tags. Release and Issue API lists were empty, while
  nine local historical tags exist. A main-push check run on a different input
  had `ci-summary` success and `style-pr` skipped. Classic Project returned
  404 and Project v2 read failed with `INSUFFICIENT_SCOPES` (`read:project`);
  these results do not establish that no Project exists. The immutable-Release
  setting and any P06 PR-style or publication outcome remain unobserved.
- Effective local hook topology needs actual-file and tool confirmation:
  local `core.hooksPath` points to `scripts/githooks`, user-global configuration
  names an external hooks directory, common workspace hook files were absent,
  and `commit.template` was unset on the observed input. A source file alone
  cannot prove an installed or executed hook.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-004 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | Map and repair only proven commit grammar, hook, release and work-tracking consumer differences; validate the local input and hand off external lanes | platform | frontmatter | NOT_RUN | EVD-P06-001 through EVD-P06-004 are planned checks with no P06 execution result yet |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-P06-001 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Commit grammar, prompt and actual hook boundary | Current `.cz.toml`, `.gitmessage`, prompt builder, hook path and generated-message consumers at P06 source revision; named authored/generated positive, refusal and Unicode/breaking/footer cases | NOT_RUN | Pending exact source, command and result in this Task | yes | none |
| EVD-P06-002 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Release preview, write and publication boundary | Current release CLI, Runbook, changelog, historical tags and synthetic local preview/write/refusal inputs; actual tag or Release needs separate authorization | NOT_RUN | Pending exact source, command and result in this Task | yes | none |
| EVD-P06-003 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Issue, Spec, Task and Project ownership | Current Issue forms, hosted surface, Spec/Task IDs and read-only remote observations; direct link and short-summary consumers | NOT_RUN | Pending source/consumer review and result in this Task; Project v2 scope remains unavailable to the remote owner | yes | none |
| EVD-P06-004 | [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | WORK-004 | Final local exact-index, message and independent review | The final changed index, selected named regressions, actual UTF-8 candidate message and reviewers once implementation bytes exist | NOT_RUN | Pending exact input, command, results, commit and later local integration in this Task and Git | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-LOCAL-QA-007](../spec.md#success-criteria--verification-plan) | pending | EVD-P06-001, EVD-P06-002, EVD-P06-003, EVD-P06-004 | Investigate current consumers; implement only confirmed differences; run selected local checks and independent review before one local acceptance decision. Preserve separate remote publication, Project, native and common-edition owners | platform for local source and documents; remote repository/release operator for external settings and publication; common standard owner for final edition |

## Approval and Safety Boundaries

- **Allowed Paths**: this Spec package, current Git and release governance,
  direct commit/release scripts and tests, relevant Runbook and bounded
  `.github/` consumer files assigned to one writer at a time.
- **Forbidden Paths**: frozen Archive payloads, unrelated user/provider
  configuration, actual secrets, live Kubernetes/Vault resources and another
  writer's in-progress files.
- **Approval Required**: local work, normal commits, main integration and
  owned development cleanup are in the current instruction. Tag/Release
  publication, remote Issue/Project/server mutation, dispatch, deployment,
  credential use and live operation need their actual target and operator
  authority; no standing approval follows from this Task.
- **Static Validation**: derive focused tests and selected affected/staged
  gates from actual changed paths and current Registry. Record exact inputs,
  tool/config, outputs, adverse results and same-check resolution. Validate
  the final index and actual message immediately before each normal commit.
- **Live Validation**: DEFER to the operating owner until an authorized target
  and execution evidence exist. No prior PR or main-push check is P06 PASS.
- **Secret / Vault Handling**: inspect only non-secret source and metadata;
  do not read, print or transmit credentials or Vault data.
- **Rollback Plan**: use forward correction on the isolated branch, keeping
  completed Tasks and earlier failure records. External publication requires
  its own operator rollback or compensating-release decision.
- **Evidence Location**: this Task, exact reviewed Git commits and bounded
  ignored command receipts. No parallel progress ledger.

## Verification Summary

P06 local code, document and selected index checks have not run on the new
Task input. Remote read-back is dated context, not hosted PR, Project or
publication success. Current hook configuration is an observation, not proof
of delivery. The first version, actual release, immutable setting, Project
state and common core adoption need their separate owners and evidence.
