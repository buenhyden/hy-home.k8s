---
title: "SDLC Cross-Artifact Conformance"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0146-TSK-0001"
parent_ids: ["SPEC-0146-PLAN-0001"]
---

# Task: SDLC Cross-Artifact Conformance

## Overview

Close the governance gaps the [audit](../../../90.references/audits/0001-sdlc-governance/m0001-sdlc-governance-audit.md)
found. It executes [SPEC-0146](../spec.md) through
[WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request (2026-11-06): audit the workspace engineering governance and apply
  the well-founded improvements directly, without remote Git, deployment or
  deletion.
- Approval (2026-11-06): the operator's reply approving the proposed commits approves SPEC-0146 and
  its Plan, drafted in `f3d71d9a`, and the local commits; push and merge are
  not approved. Criterion acceptance stays the operator's.
- Environment (2026-11-06): the operator approved a scratch venv with the
  hashed `.github/requirements/ci-validation.txt` pins, because no installed
  interpreter had both `pre_commit` and `jsonschema` for the style gates.
- Start: branch `docs/sdlc-cross-artifact-conformance` from `main` at
  `3ec90be8`, clean worktree.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SDLC-001](../spec.md#success-criteria--verification-plan) | `sdlc.md` Cross-artifact conformance | platform | in-progress | PASS | EVD-004 |
| WORK-002 | [VAL-SDLC-002](../spec.md#success-criteria--verification-plan) | Spec, Plan and ADR template prompts | platform | in-progress | PASS | EVD-005 |
| WORK-003 | [VAL-SDLC-003](../spec.md#success-criteria--verification-plan) | Audit pack AUD-0001 | platform | in-progress | PASS | EVD-006 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SDLC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Strict document and link checks | Pending Spec approval | NOT_RUN | Pending; pre-approval observation in the audit Verification State | yes | none |
| EVD-002 | [VAL-SDLC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict profile checks and document unit tests | Pending Spec approval | NOT_RUN | Pending; pre-approval observation in the audit Verification State | yes | none |
| EVD-003 | [VAL-SDLC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict checks and independent review | Pending Spec approval | NOT_RUN | Pending; pre-approval observation in the audit Verification State | yes | none |
| EVD-004 | [VAL-SDLC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Strict document and link checks | Staged index on `4fcdf22a` with the `sdlc.md` and template changes | PASS | Local run, 2026-11-06T05:36Z: contract-registry (267 paths), Markdown-profile, links-and-owners and lifecycle `--mode strict` PASS; `sdlc.md` carries `Cross-artifact conformance` | yes | EVD-001 |
| EVD-005 | [VAL-SDLC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Strict profile checks and document unit tests | Staged index on `4fcdf22a` with the `sdlc.md` and template changes | PASS | Local run, 2026-11-06T05:36Z to 05:37Z: strict profile check PASS; `unittest discover -p 'test_document*.py'` 153 OK; form, task-execution and acceptance tests 52 OK | yes | EVD-002 |
| EVD-006 | [VAL-SDLC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Strict checks and independent review | Staged index on `4fcdf22a` with the `sdlc.md` and template changes | PASS | code-reviewer report 2026-11-06: one BLOCK (audit claimed an unrecorded run) and advisories, all fixed before `f3d71d9a`; strict checks PASS at 05:36Z | yes | EVD-003 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SDLC-001](../spec.md#success-criteria--verification-plan) | pending | EVD-004 | Awaiting operator acceptance | platform |
| [VAL-SDLC-002](../spec.md#success-criteria--verification-plan) | pending | EVD-005 | Awaiting operator acceptance | platform |
| [VAL-SDLC-003](../spec.md#success-criteria--verification-plan) | pending | EVD-006 | Awaiting operator acceptance | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: `.agents/governance/sdlc.md`,
  `docs/99.templates/templates/specs/`,
  `docs/99.templates/templates/architecture/decision.template.md`,
  `docs/90.references/audits/`, `docs/03.specs/`,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`
- **Forbidden Paths**: `docs/99.templates/registry.json` and contracts,
  `scripts/`, `tests/`, product manifests, `secrets/`, provider settings
- **Approval Required**: commits, push and merge each need a separate request
- **Static Validation**: the Spec's Verification Commands
- **Live Validation**: not applicable
- **Secret / Vault Handling**: none
- **Rollback Plan**: delete the branch, or revert its commits
- **Evidence Location**: this Task

## Verification Summary

- Static lane: strict registry, profile, link and lifecycle checks PASS;
  document, form and Task-contract unit tests PASS (EVD-004, EVD-005).
- Review: independent read-only review, its BLOCK and advisories fixed
  (EVD-006).
- Each commit passed `python3 scripts/qa.py staged` in the approved scratch
  venv; without it the style gates fail with `STYLE-TOOL` (environment limit,
  not a repository defect).
- Not run: hosted, provider-runtime and live lanes (not applicable); Codex
  loading (audit F-06).
- Residual risk: the new rules are prose; no validator checks a Spec's
  architecture links (audit D-1).
- Next owner: operator, for criterion acceptance, push and merge. Rollback:
  revert the branch commits.
