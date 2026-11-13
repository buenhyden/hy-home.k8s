---
title: "W03 YAML 1.2.2 Frontmatter Loader"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0183-TSK-0001"
parent_ids: ["SPEC-0183-PLAN-0001"]
---

# Task: W03 YAML 1.2.2 Frontmatter Loader

## Overview

This Task records handoff W03-H26, the YAML 1.2 frontmatter loader, for [SPEC-0183](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to fix anything decided or built differently from the W00 to W03 requirements, to present decisions with options, to start work that can run in parallel, and approved commit, push, PR and merge in that request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-yaml-frontmatter-loader` from `534ddae7` (the SPEC-0182 closure; PR #247 open), stacked on that PR and checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-D29 (YAML 1.2.2), W03-H17 and W03-H26, and EVD-018; SPEC-0181's `frontmatter_dialect` and its dialect tests.
- **Dialect strings:** `frontmatter_dialect` keeps the target `YAML 1.2.2` and records the current dialect as `YAML 1.2 (ruamel.yaml 0.19.1, with stated refusals)`; the dialect test is updated to these strings and asserts the target.
- **Amendment of W03-H26:** W03-H26 named four loaders with unchanged timestamp rules; the read found five frontmatter loads, and this package keeps timestamps as text in all five.
- **Accepted deviations from YAML 1.2 recorded here:** `ruamel.yaml` accepts the numeric forms `1_000` and `0b11`, which the loader keeps; every explicit tag, including core tags such as `!!str`, is refused.
- **User action:** before the implementation commit the user installs the library into the local validation environment with the command in the Git policy.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | Loader module, five call sites, tests, one-time comparison. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-YAML-002](../spec.md#success-criteria--verification-plan) | Lock, dialect record, policy text; the user's install; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `9c15185b…` and plan.md `c692e5e2…`, with scratch environments for `ruamel.yaml` 0.18.17 and 0.19.1, a `pip-compile` regeneration of the lock and a comparison of all tracked frontmatter blocks; 2026-11-13 | FAIL | REJECT: BLOCK the hook does not compare the environment with the lock, so a missing library fails as an import in the validators; BLOCK the drafts conflicted with SPEC-0181's dialect record and tests; FIXes on the call sites' diagnostics, refusals ruamel does not make by default, the pin, the one-time comparison, routing and README rows, CI checks and the risk scoring. The reviewer found 248 of 248 frontmatter blocks equal and the lock regeneration adding one entry. | no | none |
| EVD-002 | [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"aede0a841e7f1df061a05ca02c24b6399222ee7b8402248844c5b938f7468a11","plan_sha256":"73f46abfc621b3303bd959c2a495faf1dcae8f263d3a786270ee08c7e5ff03c1"} | PASS | Same reviewer, round 2, 2026-11-13: every round-1 finding verified fixed over spec.md `19b18b0d…`; verdict APPROVE with NITs. The author then added the SPEC-0181 dependency sentence and the explicit-tag wording to the Spec as two of those NITs, giving the bytes named here; the other NITs are recorded under Inputs. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0183 approval question naming spec.md aede0a84 and plan.md 73f46abf dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0183","SPEC-0183-PLAN-0001"],"reviewed_spec_sha256":"aede0a841e7f1df061a05ca02c24b6399222ee7b8402248844c5b938f7468a11","reviewed_plan_sha256":"73f46abfc621b3303bd959c2a495faf1dcae8f263d3a786270ee08c7e5ff03c1","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-YAML-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-YAML-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, an evidence row and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: non-frontmatter YAML loaders, `.github/workflows/`, document bodies, `_workspace/workspace_execution_tasks/`, `.claude/`, `.codex/`, hooks, accepted ADR bodies, `docs/98.archive/`; installing into the user's environment
- **Approval Required**: Spec and Plan bytes; criterion acceptance; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, `validate-ci-python-contract.py`, `validate-github-actions-security.py`, `document`, `document-lifecycle`, `agent-governance`, `ci-metadata`, `validation-routing` and `tooling` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started.
