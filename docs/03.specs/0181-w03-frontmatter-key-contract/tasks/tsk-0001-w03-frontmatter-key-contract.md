---
title: "W03 Frontmatter Key Contract"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0181-TSK-0001"
parent_ids: ["SPEC-0181-PLAN-0001"]
---

# Task: W03 Frontmatter Key Contract

## Overview

This Task records handoffs W03-H07, W03-H14 and W03-H17 and two conformance-audit corrections for [SPEC-0181](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items, to investigate remaining, unverified, unreviewed, unconfirmed, unstarted, conflicting and missing items, to review whether anything was decided or built differently from the W00 to W03 requirements and fix it to them, to present decisions with options, to check existing work first, to do now anything due before W03, to start work that can run in parallel, and approved commit, push, PR and merge in that same request. The request approves no Spec bytes or criterion.
- **Base:** branch `claude/w03-frontmatter-keys` from `2842579e` (`main` merge of PR #245); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D05, W03-D22, W03-D23 and EVD-018 (current v14.7 requirements prevail).
- **Decisions recorded with this package:** the user's direct 2026-11-13 answers W03-D25 (adopt the GOV-06 machine ledger), W03-D26 (build local forms for the nine local roles), W03-D27 (move `sdlc.md` to the Policy role and add rule IDs), W03-D28 (keep CI-SCOPE staged for W06), W03-D29 (move the YAML loaders to YAML 1.2.2), W03-D30 (Q-07 renumbering only after all `docs/` work, with the current numbering kept until then) and W03-D31 (keep accurate pointer lines); the follow-up handoff rows; the 2026-11-13 conformance-audit rows.
- **Requirement basis:** the W03 task's metadata table, W03-A, line 18 (extension conditions) and the TemplateDefinition contract; read-only inputs under `_workspace/workspace_execution_tasks/`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | Authority admission, key entries, dialect, key-table projection, Codex twin, registry checks and tests. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-KEYS-002](../spec.md#success-criteria--verification-plan) | Extension texts; policy texts; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `997fa118…`, plan.md `daa6ec08…`, with simulations in a scratch copy of the tree; 2026-11-13 | FAIL | REJECT: BLOCK the registry authority guard refuses new top-level sections, so `scripts/document_authority.py` must be in scope; BLOCK the full TemplateDefinition record cannot validate without invented heading content for the form-less and provider-native templates, and the six SDLC templates were unaddressed; BLOCK the WGOV-CORE count is seven, a binding test pins `unverified`, and `scope`, `migration` and `rollback` have no source. FIXes on the TOML twin (feasible), key tests, the four loaders, follow-up handoff rows and the policy paragraphs; NITs on risk scoring, the Task, native allowed values and the approval citation. | no | none |
| EVD-002 | [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"8941ea5b7122b9bfd6ec4e91b26fcc651730162473c01231a4d450547c59776b","plan_sha256":"f258872826f29f16a29feb6517ace22df773bccc84059008acd07bc656b00ca9"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: every round-1 finding verified fixed, with W03-H15 handed to the local-forms package and phase 3 and the extension texts left for the user's acceptance; round 3 confirmed by diff that only four requested edits changed; verdict APPROVE. The acceptance question must show the actual extension texts, and VAL-KEYS-002 is not met by the Spec's approval alone. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0181 approval question naming spec.md 8941ea5b and plan.md f2588728 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0181","SPEC-0181-PLAN-0001"],"reviewed_spec_sha256":"8941ea5b7122b9bfd6ec4e91b26fcc651730162473c01231a4d450547c59776b","reviewed_plan_sha256":"f258872826f29f16a29feb6517ace22df773bccc84059008acd07bc656b00ca9","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and no extension text. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-KEYS-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-KEYS-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002, record PASS evidence and show the extension texts at acceptance | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D25 to W03-D31, handoff, conformance-audit and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every document and template body other than the two policy texts, `_workspace/workspace_execution_tasks/`, `.github/`, `.claude/`, `.codex/`, hooks, accepted ADR bodies, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance with the extension texts; push, PR and merge are approved by the user's 2026-11-13 request in Inputs
- **Static Validation**: strict document validators, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). Implementation not started.
