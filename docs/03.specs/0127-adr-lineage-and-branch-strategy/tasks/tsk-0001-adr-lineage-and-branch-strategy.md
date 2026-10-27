---
title: "ADR Lineage and Branch Strategy"
version: "0.4.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0127-TSK-0001"
parent_ids: ["SPEC-0127-PLAN-0001"]
---

# Task: ADR Lineage and Branch Strategy

## Overview

Reject supersession chains without a current decision, add the ADR form
prompts and numbering rule, and record the branch strategy. It executes
[SPEC-0127](../spec.md) through [WORK-001–004](../plan.md#work-breakdown).

## Inputs

- Request: the operator said on 2026-10-27 to proceed as recommended; slice
  B of the SPEC-0125 status table covers CR-09.06 and CR-13.07.
- Research read on 2026-10-27: adr.github.io template overview, Nygard
  (2011-11-15), MADR 4.0.0 (`adr/madr` HEAD `ba75bb1b`), the Y-statement
  form, Trunk-Based Development, GitHub flow and Driessen's git-flow with its
  2020 note.
- Start: main `0058fe3c`, branch `feat/adr-lineage-and-branch-strategy`.

### ADR Form Comparison

| Field or rule | Nygard | MADR 4.0.0 | Y-statement | This repository |
| --- | --- | --- | --- | --- |
| Context, decision, consequences | yes | yes | one sentence | Required sections |
| Considered alternatives | no | Considered Options, Pros and Cons | neglected options (long form) | Required `Alternatives` |
| Status and supersession | proposed, accepted, deprecated or superseded, old record kept | status string such as `superseded by ADR-0123` | none | `status` plus reciprocal `supersedes` and `superseded_by` |
| Decision makers, consulted, informed | no | optional front matter | no | `owner` only; prompt added |
| Decision date | no | optional `date` | no | `updated` only; prompt added |
| Confirmation | no | optional section | no | Prompt added |
| Numbering | sequential, never reused | not stated | none | Never reused, now stated in the ADR log |
| Explicit non-goals, `retired` status | no | no | no | Repository conventions without a source basis |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AB-001](../spec.md#success-criteria--verification-plan) | Reject supersession chains without a current decision | platform | in-progress | PASS | EVD-005 closes EVD-001 |
| WORK-002 | [VAL-AB-002](../spec.md#success-criteria--verification-plan) | Add the template prompt and the numbering rule | platform | in-progress | PASS | EVD-006 closes EVD-002 |
| WORK-003 | [VAL-AB-003](../spec.md#success-criteria--verification-plan) | Record ADR-0052 and link it from `git.md` | platform | in-progress | PASS | EVD-008 closes EVD-003 |
| WORK-004 | [VAL-AB-004](../spec.md#success-criteria--verification-plan) | Run staged QA and observe the hosted checks | platform | in-progress | PASS | EVD-009 closes EVD-004 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AB-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Supersession tests and strict validation | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-AB-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Template tests and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-AB-003](../spec.md#success-criteria--verification-plan) | WORK-003 | ADR review and acceptance | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-004 | [VAL-AB-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Staged QA and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |
| EVD-005 | [VAL-AB-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Supersession tests and strict validation | Branch `feat/adr-lineage-and-branch-strategy`: `python3 -m unittest tests.test_document_lifecycle_archive_cutover` before and after the `scripts/document_lifecycle.py` change; `python3 scripts/validate-document-lifecycle.py --mode strict` | PASS | Before the change the new cycle test failed: two ADRs superseding each other produced no diagnostic. After it, the cycle fails `LIFECYCLE-EVIDENCE` on both ADRs, the reciprocal supersession test passes, and all 38 tests in the module pass. Strict lifecycle validation passes on the repository; ruff check and format pass | yes | EVD-001 |
| EVD-006 | [VAL-AB-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Template tests and review | Same branch: `python3 scripts/validate-document-contract-registry.py`, `python3 -m unittest tests.test_repository_form_contracts` | PASS | The decision template asks for decision makers, decision date and confirmation as a prompt; the ADR log states that numbers are never reused and that MIG-0002 and approved Archive removals do not rewrite them; the comparison with Nygard, MADR 4.0.0 and Y-statement is in Inputs. The registry passes 976 paths and the form tests pass | yes | EVD-002 |
| EVD-007 | [VAL-AB-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Supersession tests and strict validation | PR #182 independent review of `8c598166`; then `python3 -m unittest tests.test_document_lifecycle_archive_cutover`, `python3 scripts/validate-document-lifecycle.py --mode strict` and the reviewer's scratch reproduction on the fix | PASS | The review found that the first walk followed only the first reciprocal link, so a chain that listed its superseded predecessor first, or two supersessions in one change, failed although they pass on main. New tests for both failed on `8c598166`. The rule now searches every reciprocal path and passes when any reaches a document whose status is not superseded; predecessors share the superseded status, so cycles still fail. With a three-document cycle test added, all 41 tests pass, the reviewer's reproduction passes, strict validation passes, and ruff passes | yes | none |
| EVD-008 | [VAL-AB-003](../spec.md#success-criteria--verification-plan) | WORK-003 | ADR review and acceptance | PR #182 independent review of `8c598166` and `d6e3d5fb`; `gh api repos/buenhyden/hy-home.k8s/branches` | PASS | The review confirmed ADR-0052's facts: `main` is the only long-lived branch, ADR-0029's twelve `targetRevision: main` declarations, `scripts/release.py` as release producer and the merge checks in `git.md`, and found the Trunk-Based Development, GitHub flow and git-flow sources represented accurately. Its wording findings (open feature branches, the `release/<tag>` preparation branch, the Git policy as the merge rule) were applied in `d6e3d5fb` and approved. `git.md` states the rule; its link to ADR-0052 waits for acceptance because governance may link only current owners | yes | EVD-003 |
| EVD-009 | [VAL-AB-004](../spec.md#success-criteria--verification-plan) | WORK-004 | Staged QA and hosted checks | PR #182 heads `8c598166` (CI run `40510854088`) and `d6e3d5fb` (CI run `40514040098`); pre-commit staged QA on commits `d61fc680`, `c170d31f`, `8c598166` and `d6e3d5fb` | PASS | `ci-summary` and `style-pr` passed on both heads, and the PR checks list `label` and GitGuardian as passed. Staged QA passed on all four commits. The second review approved with one low note: link reachability is undirected, as it was on main, so a stricter directed rule needs a directed link source | yes | EVD-004 |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AB-001](../spec.md#success-criteria--verification-plan) | pending | none | Validator change and tests remain | platform |
| [VAL-AB-002](../spec.md#success-criteria--verification-plan) | pending | none | Template prompt and rule remain | platform |
| [VAL-AB-003](../spec.md#success-criteria--verification-plan) | pending | none | ADR-0052 and operator decision remain | platform |
| [VAL-AB-004](../spec.md#success-criteria--verification-plan) | pending | none | Staged QA and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index,
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`,
  `scripts/document_lifecycle.py`,
  `tests/test_document_lifecycle_archive_cutover.py`,
  `docs/99.templates/templates/architecture/decision.template.md`,
  `docs/02.architecture/decisions/README.md`,
  `docs/02.architecture/decisions/0052-single-main-trunk-branch-strategy.md`
  and `.agents/governance/git.md`.
- **Forbidden Paths**: branch protection, rulesets, GitHub settings,
  provider settings and credentials.
- **Approval Required**: the operator said on 2026-10-27 to proceed as
  recommended; accepting ADR-0052 is a separate operator decision. Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: focused tests, strict lifecycle validation and
  `qa.py staged`.
- **Live Validation**: none.
- **Secret / Vault Handling**: no secret is read or written.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
