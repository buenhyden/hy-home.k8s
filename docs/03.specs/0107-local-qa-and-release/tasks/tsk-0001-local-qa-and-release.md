---
title: "Local Quality and Release Lifecycle"
version: "0.1.0"
type: "sdlc/task"
status: "draft"
owner: "platform"
updated: "2026-10-07"
layer: "specs"
artifact_id: "SPEC-0107-TSK-0001"
parent_ids: ["SPEC-0107-PLAN-0001"]
---

# Task: Local Quality and Release Lifecycle

## Overview

Record actual execution for the local QA retirement and delivery contract,
Commitizen and SemVer release path, and Issue/Project responsibility update.
This Task alone owns commands, results, acceptance, integration and handoff.
The original SPEC-0106 Tasks and their `NOT_RUN` results remain historical.

## Inputs

- [WORK-001](../plan.md#work-breakdown) and the four criteria
  [VAL-LOCAL-QA-001](../spec.md#success-criteria--verification-plan),
  [VAL-LOCAL-QA-002](../spec.md#success-criteria--verification-plan),
  [VAL-LOCAL-QA-003](../spec.md#success-criteria--verification-plan), and
  [VAL-LOCAL-QA-004](../spec.md#success-criteria--verification-plan).
- [REQ-0003](../../../01.requirements/0003-workspace-agent-governance-platform.md),
  [AD-0006](../../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md),
  current [quality policy](../../../../.agents/governance/quality.md),
  [validation registry](../../../../scripts/validation/registry.json),
  [Git policy](../../../../.agents/governance/git.md) and
  [GitHub surface](../../../../.github/repository-surface.md).
- Current scoped user instruction: retire proven one-off, legacy,
  deprecated, duplicate, conflicting and excessive QA; run public-repository
  QA locally; align delivery stages, Commitizen, SemVer Release/tag,
  main `CHANGELOG.md`, and Issue/Spec/Task/Project responsibilities.
- Intake snapshot: clean main `2c9c5546bc10502284fc3c67150e33f090371223`;
  isolated `codex/qa-local-lifecycle` at `.worktrees/qa-local-lifecycle`.
  The draft records source inspection only; no current validation ran.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Acceptance | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-LOCAL-QA-001](../spec.md#success-criteria--verification-plan), [VAL-LOCAL-QA-002](../spec.md#success-criteria--verification-plan), [VAL-LOCAL-QA-003](../spec.md#success-criteria--verification-plan), [VAL-LOCAL-QA-004](../spec.md#success-criteria--verification-plan) | Retire proven obsolete QA with coverage transfer; route local validation, commit and release, and work tracking to current owners | platform | frontmatter | NOT_RUN | pending | EVD-LOCAL-QA-001, EVD-LOCAL-QA-002, EVD-LOCAL-QA-003, EVD-LOCAL-QA-004 pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-LOCAL-QA-001 | [VAL-LOCAL-QA-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Consumer and coverage succession audit; dated official source → claim → local decision | Base `2c9c5546`; current scripts, tests, registry, workflows and primary source URL/date to be recorded | NOT_RUN | Pending source inventory, research mapping and focused results | pending |
| EVD-LOCAL-QA-002 | [VAL-LOCAL-QA-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Stage routing, preflight and local QA; dated official source → claim → local decision | Actual changed index/tree, tools, budget, mode, trust and primary source URL/date to be recorded | NOT_RUN | Pending exact commands, research mapping and receipts | pending |
| EVD-LOCAL-QA-003 | [VAL-LOCAL-QA-003](../spec.md#success-criteria--verification-plan) | WORK-001 | Commit and SemVer release contract | Actual message, release source and consumer fixtures to be recorded | NOT_RUN | Pending focused results; remote publication separate | pending |
| EVD-LOCAL-QA-004 | [VAL-LOCAL-QA-004](../spec.md#success-criteria--verification-plan) | WORK-001 | Owner/links, independent review and delivery | Final diff, review identity and Git result to be recorded | NOT_RUN | Pending evidence and handoff | pending |
| EVD-LOCAL-QA-005 | [VAL-LOCAL-QA-004](../spec.md#success-criteria--verification-plan) | WORK-001 | First draft staged document admission | Initial three-file draft index; exact index and receipt held by root for attachment | FAIL | Root's retained staged receipt: four selected gates PASS; links-and-owners BODY-LINK-RECIPROCAL and markdown-profiles BODY-CONTRACT-IDENTIFIER FAIL | rejected |
| EVD-LOCAL-QA-006 | [VAL-LOCAL-QA-004](../spec.md#success-criteria--verification-plan) | WORK-001 | Corrected draft staged document admission | Five-file corrected draft index; exact index and receipt held by root for attachment | FAIL | Root's retained staged receipt: five selected gates PASS; markdown-profiles BODY-HEADING-UNSUPPORTED for Spec Related Documents | rejected |
| EVD-LOCAL-QA-007 | [VAL-LOCAL-QA-004](../spec.md#success-criteria--verification-plan) | WORK-001 | Draft snapshot guard | Third draft staged attempt; source index or HEAD changed during snapshot, exact identity held by root | FAIL | Snapshot guard failed before child gates; selected local gates NOT_RUN for this attempt | rejected |

## Approval and Safety Boundaries

- **Allowed Paths**: This package's `spec.md`, `plan.md` and this Task are the
  document writer's initial exclusive scope. After the ready transition, the
  delegated CI workflow engineer owns `.github/workflows/ci.yml`,
  `.github/workflows/qa-verifier.yml`,
  `.github/workflows/generate-changelog.yml`, direct workflow tests,
  `.github/repository-surface.md`, `.github/rulesets/main-protection.md`,
  `.github/PULL_REQUEST_TEMPLATE.md` and current `.github/ISSUE_TEMPLATE/`
  request forms. The archive/quality owner owns
  `scripts/validation/registry.json`, its schema, affected selector,
  Archive-specific ongoing checks and direct fixtures; Stage 99's
  `docs/99.templates/registry.json` and existing frontmatter contracts admit
  a root `CHANGELOG.md` profile as an additive, uniquely classified current
  document without rewriting frozen generation-10 evidence. The root
  quality/tooling writer owns `scripts/qa.py`, `tests/test_qa_runner.py`,
  commit/release tooling and associated direct QA consumers. The
  architecture owner handles current REQ-0003/AD-0006/ADR changes. The
  governance owner handles common `.agents/` policy. This document writer
  may receive later explicit delegation for `scripts/README.md`,
  `tests/README.md`, the current Stage 05 QA guide/runbook and
  `docs/03.specs/README.md`. Stale workflow/provenance, changelog and
  publisher consumers are in scope only after the caller and active recovery
  map identifies them. Agent-evaluation cases remain only where the current
  governance safety/evaluation contract has a distinct consumer; they do not
  become a blanket exception to the retirement audit. File ownership stays
  disjoint during writes.
- **Forbidden Paths**: Frozen or completed Spec/Task bodies and evidence,
  sealed Archive content, private/global configuration, real secret values,
  unrelated user changes, live cluster/cloud/Vault, and other repositories.
- **Approval Required**: The latest user instruction authorizes this scoped
  policy repair, local commits, normal push/main merge and owned development
  cleanup after valid evidence and preservation. It does not authenticate
  a remote setting or authorize a specific Release publication, Project
  mutation, credential/native trust change or live operation. Recheck actual
  external authority under approval-and-safety before any dependent action.
- **Static Validation**: Preflight selected tools/hooks and runner time/output
  envelope before implementation; changed-behavior focused RED/GREEN, affected
  quick, actual-index staged and configured message per logical commit, final
  local full once, completion and independent read-only semantic review when
  applicable. Current command inputs/results are pending, not PASS.
- **Live Validation**: DEFER, no live environment or authority in this scope.
- **Secret / Vault Handling**: Reference metadata only; no value read or
  transcript/credential capture. Operator owns any later protected action.
- **Rollback Plan**: Use normal forward corrective commits. Keep Git,
  original SPEC-0106 evidence and Archive recovery identity intact. Remove
  an owned branch/worktree only after actual main reachability, clean state
  and retained evidence are verified.
- **Evidence Location**: This Task's evidence table and verification summary;
  bounded check receipts may be cited by exact location, not copied as raw logs.

## Verification Summary

At draft intake the source audit identified a `ciJobs` entry for a nonexistent
hosted `qa` job, Git policy claiming hosted final full QA, inactive verifier
and SHA-tag publication logic, and prior full QA marked `NOT_RUN`. These
are findings to resolve against exact current consumers, not executed-check
results. At initial authoring no QA, hook, completion, release or remote
operation had run for this package. Selected tool versions, time/output limits, runner approval,
independent reviewer, exact final snapshot and next owner are pending the
ready/implementation transitions. Current required check results stay
`NOT_RUN`; remote settings and publication stay `DEFER` until observed.

The first staged admission of the draft ran six selected gates: four passed,
and links-and-owners plus markdown-profiles failed. The new Spec lacked its
REQ-0003 reciprocal link, and its Requirement ID cells combined multiple
links and an Architecture ID where one requirement ID is required. The
reciprocal Requirement link, Stage 03 navigation and one-ID-per-row trace
have now been corrected. This is a changed input; its refreshed staged result
was the second staged attempt: five gates passed, while the unsupported Spec
heading failed. The heading was removed. A third staged attempt then failed
the snapshot guard before any selected child gate ran because index or HEAD
changed during snapshot preparation; its gates remain `NOT_RUN` for that
attempt. The failed receipts remain factual evidence and are not treated as
a final pass. Another stabilized-input staged result remains `NOT_RUN`.
