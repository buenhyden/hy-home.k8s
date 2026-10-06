---
title: "Local Quality and Release Lifecycle"
version: "0.1.0"
type: "sdlc/task"
status: "ready"
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
  Draft admission was committed normally at `21009bf2`; actual check attempts
  are recorded below. This ready edit changes the index and requires its own
  staged and message checks.

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
| EVD-LOCAL-QA-008 | [VAL-LOCAL-QA-004](../spec.md#success-criteria--verification-plan) | WORK-001 | Fourth draft staged admission | Corrected Spec without its reciprocal Plan link; exact index retained by root | FAIL | Root's staged receipt: five gates PASS, links-and-owners FAIL for missing Spec to Plan link | rejected |
| EVD-LOCAL-QA-009 | [VAL-LOCAL-QA-004](../spec.md#success-criteria--verification-plan) | WORK-001 | C1 draft admission and normal commit | Final five-document C1 index at commit `21009bf2`; Python 3.12.3; staged log `/tmp/hy-qa-0107-draft-admission-staged.log` | PASS | Focused links PASS; `python3 -u scripts/qa.py staged` six gates PASS, rc0; pinned Commitizen message PASS; normal commit succeeded. This result covers C1 input only; no workspace hook output observed. | accepted |
| EVD-LOCAL-QA-010 | [VAL-LOCAL-QA-004](../spec.md#success-criteria--verification-plan) | WORK-001 | Initial C2 ready-index staged admission | Ready Spec/Plan/Task index before acceptance-cell repair; root retains exact index/log | FAIL | Five selected gates PASS; markdown-profiles TASK-EVIDENCE-ACCEPTANCE FAIL because EVD-LOCAL-QA-009 used an unregistered acceptance literal. Current repaired input not rechecked. | rejected |

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
  become a blanket exception to the retirement audit. The repo-tooling owner
  receives explicit registered Archive cutover gate/caller handoff after
  ongoing Archive integrity coverage is transferred. The shared
  `.agents/skills/archive-cutover/SKILL.md` Step 6 and current `.agents/roles/`
  definitions may change for this demonstrated succession only; no role
  permission is widened. File ownership stays disjoint during writes.
- **Forbidden Paths**: Frozen or completed Spec/Task bodies and evidence,
  sealed Archive content, private/global configuration, real secret values,
  unrelated user changes, live cluster/cloud/Vault, and other repositories.
- **Approval Required**: The latest user instruction authorizes this scoped
  policy repair, local commits, normal push/main merge and owned development
  cleanup after valid evidence and preservation. It does not authenticate
  a remote setting or authorize a specific Release publication, Project
  mutation, credential/native trust change or live operation. Recheck actual
  external authority under approval-and-safety before any dependent action.
- **Static Validation**: Intake found Python 3.12.3, PyYAML 6.0.1,
  jsonschema 4.10.3, pre-commit 4.6.2, pinned kustomize v5.8.1,
  gitleaks 8.30, git-cliff 2.14.2 and `gh`; Commitizen 4.15.1 is available
  in the pinned check environment, not proven as a global hook. Mandatory
  child limits are 1200 seconds, stdout 4 MiB, stderr 1 MiB and cleanup
  2 seconds; unit and pre-commit entries allow 2400 seconds. Focused named
  checks start with a 60-second budget; extend only for a measured changed
  input via the normal runner, not guard evasion. Run focused RED/GREEN,
  affected quick, actual-index staged and configured message per logical
  commit, final local full once for this global-QA change, completion and
  independent read-only semantic review. Tool and budget readiness is not
  result evidence for the ready or implementation index.
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
operation had run for this package. Selected tool versions and limits are now
recorded in the ready preflight above. Runner approval, independent reviewer,
final snapshot and next owner remain tied to the actual implementation.
Current implementation checks stay `NOT_RUN`; remote settings and publication
stay `DEFER` until observed.

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
attempt. A fourth staged run passed five gates and failed links-and-owners
because the Spec lacked its Plan backlink. The inline Plan link repaired that
input. The fifth C1 run then passed all six staged gates, the focused links
check and the pinned Commitizen message check, followed by normal commit
`21009bf2`. No workspace hook output was observed. Those results apply only
to C1 input; this changed ready index and later implementation indexes need
their own checks. The first C2 ready-index attempt passed five gates and
failed markdown-profiles because EVD-LOCAL-QA-009's Acceptance cell contained
an unregistered qualifier; its registered value is now `accepted`, with the
C1-only limit kept in Location. The repaired C2 index remains `NOT_RUN` until
checked. Failed receipts remain factual evidence, not final passes.
