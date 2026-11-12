---
title: "W02 Safe Disposition"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0167-TSK-0001"
parent_ids: ["SPEC-0167-PLAN-0001"]
---

# Task: W02 Safe Disposition

## Overview

This Task records the W02 safe disposition change for [SPEC-0167](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user pasted the v14.7 W02 prompt (package `_workspace/workspace_execution_tasks/tasks/TASK-hy-home-k8s-W02.md`). The prompt approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w02-v14-7-archive` created from `main` at `b4925358` (PR #230 merge); worktree clean; hook environment `hyhome.validationVenv` set; no LFS, submodule or Git filter (SPEC-0161 ARC-05).
- **Decisions reused:** SPEC-0161 EVD-018 (current v14.7 requirements prevail; Q-08 path kept); ADR-0057 and the user's 2026-11-11 choice of an event-scoped exit check over a presence check; ADR-0056 manual review.

### Survey

Read-only survey at `b4925358` by a delegated general-purpose agent, with the lifecycle lines, README lines, Stage 02 `AGENTS.md` and ADR-0057 rejection lines re-read by the author. Read fully: `document-lifecycle.md`, W02 package sections 2 to 11, `docs/98.archive/README.md` and its tree (README and `.gitkeep` only). Read partially: ADR-0053, ADR-0056, ADR-0057, Stage 01 and 03 READMEs and `AGENTS.md`, Stage 02 `AGENTS.md`, `sdlc.md` item 5, glossary TERM-RETIREMENT to TERM-HOLD, registry lifecycle domains, `scripts/document_lifecycle.py` `package_exit_diagnostics`, `validate-document-lifecycle.py`, and a grep of `scripts/` and `tests/`. Not read: ADR-0055 body, `ci.yml`, `tests/test_document_lifecycle_cumulative_history.py`, `context-and-memory.md`. Stage 01 to 03 statuses: 33 accepted, 8 active, 4 approved; none non-current; `docs/03.specs` holds only SPEC-0161 plus its routers.

| Item | Current owner | Finding | Action | Writer |
| --- | --- | --- | --- | --- |
| ARC-01 | `document-lifecycle.md:160-188`; ADR-0056 | Policy, consumers and the exit route exist; Git-only exit reused | KEEP | none |
| ARC-02 authority | `docs/AGENTS.md:48`; `document-authoring.md:69`; `document-lifecycle.md:202-209` | Archive is never current authority; provider files cite archived evidence only as `git show` recovery | KEEP | none |
| ARC-02 active-only | registry Stage 01 and 02 status domains; `document_lifecycle.py:826-925` | No superseded, retired or deprecated state; event-scoped exit check; presence check rejected by ADR-0057; but an ADR may stay `rejected` in the tree | ADD rejected-ADR exit; registry state to W03, W04 | W02, W03, W04 |
| ARC-03 | `formatting-and-linting.md:88`; ADR-0053; `03.specs/AGENTS.md:40` | Archive bodies excluded from fixers; completed evidence not rewritten; no rule for frozen package text | ADD | W02 |
| ARC-04 | `document-lifecycle.md:163-170`; ADR-0056 | Existing Task and `Archived Lineage`; no new Spec or ledger | KEEP | none |
| ARC-05, W02-A | `document-lifecycle.md:180-188` | Uncommitted source, hold, authority named; reflog-only, shallow and squash-lost sources only implied | ADD | W02 |
| ARC-06 | `document-lifecycle.md:196-201` | Stage 01 to 03 and 99 Git-only; others may move; no Q-02 conflict | KEEP | none |
| ARC-07 | `document-lifecycle.md:202-209`; `scripts/validation/registry.json:1038-1051` | `archive-documents` is secret scanning only; no retention, catalog or migration validator | KEEP | none |
| ARC-08 | `validate-links-and-owners.py:4095`; `scripts/validation/current_executable_references.py:21` | Status branches for `done` and `archived`, which no registry domain holds; reachability unverified | DEFER to W05 | W05 |
| ARC-09 | ADR-0056 Non-goals only | Policy owner does not exclude service data, backups, credentials, Vault or the shared memory store | ADD | W02 |
| QA-C04 | `docs/AGENTS.md:48`; `formatting-and-linting.md:88`; ADR-0056 | Archive not loaded, not formatted; unapproved deletion caught by manual review | KEEP | none |
| W02-B | ADR-0056; ADR-0057; `document-lifecycle.md:212-222` | Manual review and automatic shape check are separate | KEEP | none |
| R147-08 | SPEC-0161 COVERED | Existing exit reused | KEEP | none |
| Section 7 items 5.1 to 5.4 | `sdlc.md` item 5; glossary; `document-lifecycle.md:119-128` | Separate meanings and active-only text present | KEEP | none |
| Section 7 items 5.5, 11 | `document-lifecycle.md:160-188`; `03.specs/AGENTS.md:46-53` | Order, freeze before final commit and proof in surviving owner written; staged `LIFECYCLE-PACKAGE-EXIT` covers the impact step | KEEP | none |
| ARC-02 router exceptions | registry navigation profile; `tests/test_readme_navigation.py:87-227`; `tests/test_repository_quality_rules.py:96` | README and router exceptions are tested: direct-folder routers pass, pending and exempt READMEs, folder `AGENTS.md` needs its human router | KEEP | none |
| ARC-03 recovery boundary | `approval-and-safety.md:85-86`; `document-lifecycle.md:180-188` | A recovery is evidence only; it grants no write or disposition authority | KEEP | none |
| Index wording | `docs/01.requirements/README.md:92,99` | Says the Architecture Description's `Archived Lineage`; policy and practice use the owning current document | CHANGE | W02 |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-DISPOSE-001](../spec.md#success-criteria--verification-plan), [VAL-DISPOSE-002](../spec.md#success-criteria--verification-plan) | Edit the three W02 files the Spec names. | platform | ready | NOT_RUN | Waits for the Spec and Plan approval. |
| WORK-002 | [VAL-DISPOSE-003](../spec.md#success-criteria--verification-plan) | Record the handoffs and the exact-index QA. | platform | ready | NOT_RUN | Waits for WORK-001. |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-DISPOSE-001](../spec.md#success-criteria--verification-plan), [VAL-DISPOSE-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package; spec.md `5fc92614…`, plan.md `a472e591…`; 2026-11-12 | PASS | APPROVE with no BLOCK; FIXes: rejected-ADR rule needed the deferral condition; Stage 02 rule 2 listed `rejected` as a kept state; ARC-02 router-exception tests had no row; anchor search needed collapsed whitespace. NOTEs: `.secrets.baseline` scope alignment, presence-check wording, open-package count, FR-0030 mapping. All applied before approval except the FR-0030 note, kept by reasoning. | no | none |
| EVD-002 | [VAL-DISPOSE-001](../spec.md#success-criteria--verification-plan), [VAL-DISPOSE-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"868089f4d3375c4040e2f7887387d97c78d98c14e3fe242c376c03f406333763","plan_sha256":"2d8825f6d7ee5d52871a3e25a96e5c7686769e1ecf48c51c4bbad772b3fe2953"} | PASS | Same reviewer, round 2, 2026-11-12: both hashes matched; every round-1 FIX present; verdict APPROVE with no BLOCK or FIX. NOTEs: the ARC-03 recovery-boundary row is acceptable rather than strong; FR-0012 is not named for the W03/W04 registry handoff. The reviewer is independent of the author; this row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-DISPOSE-001](../spec.md#success-criteria--verification-plan), [VAL-DISPOSE-002](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0167 question naming spec.md 868089f4 and plan.md 2d8825f6 dated 2026-11-12 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0167","SPEC-0167-PLAN-0001"],"reviewed_spec_sha256":"868089f4d3375c4040e2f7887387d97c78d98c14e3fe242c376c03f406333763","reviewed_plan_sha256":"2d8825f6d7ee5d52871a3e25a96e5c7686769e1ecf48c51c4bbad772b3fe2953","validity":"confirmed","revocation":"none"} | PASS | No message UUID was supplied or invented. This receipt accepts no criterion and authorizes no push, PR or merge. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-DISPOSE-001](../spec.md#success-criteria--verification-plan) | pending | none | Lifecycle anchors and KEEP evidence | platform |
| [VAL-DISPOSE-002](../spec.md#success-criteria--verification-plan) | pending | none | README phrase search, Stage 02 rule, document checks | platform |
| [VAL-DISPOSE-003](../spec.md#success-criteria--verification-plan) | pending | none | Handoffs and exact-index QA | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the three W02 files the Spec names, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: registry, schema, templates, `scripts/`, `tests/`, `.github/`, accepted ADR bodies, `docs/98.archive/`, completed Archived Lineage rows
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge; any disposition of a current document
- **Static Validation**: strict document validators, `document` suite, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed; Vault records are outside this change
- **Rollback Plan**: revert the implementation commit
- **Evidence Location**: this Task

## Verification Summary

Not started; waits for the Spec and Plan approval. Risk class `medium` (policy change).
