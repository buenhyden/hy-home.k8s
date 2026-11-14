---
title: "W03 Spec and Plan Forms"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0200-TSK-0001"
parent_ids: ["SPEC-0200-PLAN-0001"]
---

# Task: W03 Spec and Plan Forms

## Overview

This Task records the Spec and Plan part of handoffs W03-H02 and W03-H13, the Plan part of W03-H10 and W03-H24, and W03-D50: the COMMON-DOC-FORM-1 Spec and Plan forms, their body contracts and TemplateDefinitions, the Plan and completion readers, the one-use exemptions for the frozen Spec and Plan of SPEC-0161 and for recorded evidence rows, the moved documents and repointed links, and the retirement of both exemptions, for [SPEC-0200](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-14 (Asia/Seoul) the user asked to continue W03 phase 3 in the order of W03-D49. The request approves no Spec bytes, no criterion and no moved file; an approval of push, PR or merge is recorded here when the user gives it.
- **Base:** set at commit time; the Spec and Plan facts were read on `main` `a8c689e5` (after PR #256, SPEC-0191) and are checked against `main` before delivery.
- **Decisions reused:** SPEC-0161 W03-H02, W03-H10, W03-H13, W03-H24, W03-D01, W03-D03, W03-D04, W03-D08, W03-D30, W03-D31, W03-D32, W03-D49, W03-D50, W03-D51, W03-D52, W03-D55, W03-D56 and W03-D57.
- **Decision recorded with this package:** W03-D59 (R4 admits exactly one reviewed file for each of the two frozen SPEC-0161 paths, by sha256, after the user reviews the moved files; a one-use route treats the old and the new fragment as equal on a same-package `spec.md` link in a recorded evidence row and is retired at close; the promotion table keeps `Durable contract`, `Promoted to`, `Where`, as W03-D52 says; the criteria table header becomes `Criterion ID`, `Expected Result`, the Spec `Architecture` column becomes the body contract's target link column, and the frozen files keep their frontmatter while open packages take a major raise); user answers of 2026-11-14. The row notes that W03-D65 amends its promotion part: the table takes the common column names. The fragment route is the recorded carve-out from rule 4 of `docs/03.specs/AGENTS.md`, which otherwise forbids rewriting completed evidence: it repoints the fragment of the links in the recorded evidence rows of the SPEC-0161 Task, 58 links in 55 rows at `a8c689e5` and counted again after the rebase, and nothing else in a row.
- **Decision reused, amending W03-D59 and W03-D52:** W03-D65, recorded by the SPEC-0193 package commit, the user's answer `W03 프롬프트에 작성된대로` of 2026-11-14 to the findings of a requirement audit against the task file `tasks/TASK-hy-home-k8s-W03.md` of the v14.7 package. The promotion table takes the common column names `Promotion ID`, `Target Owner`, `Acceptance` and `Evidence` (lines 306 and 738; line 37, a further column only as a registered conditional extension), by a meaning-preserving header map that changes no recorded cell (lines 759 and 684).
- **Choices resolved from the requirements under the user's standing instruction `선택이 필요할 경우, 요구사항을 따른다` (when a choice is needed, follow the requirements); neither is part of the recorded W03-D65 row or a decision row of its own:** first, `Global Constraints` stays an H4 under Goal and Boundary, as its last block, and `PLAN-GLOBAL-CONSTRAINTS` keeps its full strength, because line 113 of the W03 prompt forbids lowering a guarantee. Second, a recorded three-column promotion table gains the `Acceptance` column: lines 306 and 738 name one table shape for the role, and lines 37 and 757 leave no second shape of a same-role table as a permanent compatibility layer, so every promotion table takes the four columns and each recorded row gains one `Acceptance` cell that states the condition its Plan already gives, `none` on the none row; the frozen SPEC-0161 Plan row changes under the W03-D50 exemption.
- **Lines to list for the user (W03-D31):** every `Acceptance` cell added to a promotion row of an open package is new prose and is listed here at the implementation commit, beside the pointer and explained-none lines.
- **Decision reused:** W03-D66, recorded by the SPEC-0207 package commit. Every registry change applies the bump rule of SPEC-0207 (lines 877 to 882 of the W03 prompt). This package's expected level is NO_CHANGE, because it changes no key, type, requiredness or enumeration of the registry and leaves the schema file untouched; the level and its reason are recorded as evidence at the implementation commit.
- **Implementation choice, not a decision:** the Plan and completion readers take the headings they read from the form by section id. The pre-approval review judged this to lie within the re-pointing that W03-D52 decides; it is recorded here and needs no decision row. The old-shape branch reads a profile's allowed H2 through one accessor function, so SPEC-0205 can rename the list field with a one-line change.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-SPECPLAN-001](../spec.md#success-criteria--verification-plan) | The three readers with the form shape and their tests first, so `PLAN-PROMOTION`, `PLAN-GLOBAL-CONSTRAINTS` and `TASK-PARENT-APPROVAL` stay active; then the forms, the extension, the profile lists, the body contracts with the design constraint link, and the TemplateDefinitions and records. | platform | ready | NOT_RUN | Pending |
| WORK-002 | [VAL-SPECPLAN-002](../spec.md#success-criteria--verification-plan) | The two one-use exemptions with their tests; the templates; the frozen Spec and Plan after the user's review; the repointed links, with the anchor strings of `tests/test_task_acceptance_contract.py`, `tests/test_task_acceptance_boundaries.py`, `tests/test_documentation_link_boundary.py` and the other consumer tests; the Spec and Plan of each open package with the inventory. | platform | ready | NOT_RUN | Pending |
| WORK-003 | [VAL-SPECPLAN-002](../spec.md#success-criteria--verification-plan) | The texts; the SPEC-0161 Task rows and ledger entries; the retirement of both exemptions in the final source commit; regression and exact-index QA. | platform | ready | NOT_RUN | Pending |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-SPECPLAN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"fc92014b9aec6d76f0d2be72c4e58384c4306e044b2f722eba9ce8dfca0c6e07","plan_sha256":"f7551671125a95370fa8ac1b2911bfac3ce698b9255b5ec76fce235ac5635837"} | PASS | Independent reviewer, round 2 on 2026-11-14: the five round-1 NITs resolved, the three anchor-holding test modules in scope, OPEN-09 kept as a recorded code-span mention, section-id heading reading recorded as an implementation choice within W03-D52; APPROVE over the bytes named here. This row records a review, not an approval. | yes | none |
| EVD-002 | [VAL-SPECPLAN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve bytes to the SPEC-0200 approval question naming spec.md fc92014b and plan.md f7551671 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-001","scope":["SPEC-0200","SPEC-0200-PLAN-0001"],"reviewed_spec_sha256":"fc92014b9aec6d76f0d2be72c4e58384c4306e044b2f722eba9ce8dfca0c6e07","reviewed_plan_sha256":"f7551671125a95370fa8ac1b2911bfac3ce698b9255b5ec76fce235ac5635837","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-003 | [VAL-SPECPLAN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"bc0a9893e5729ff285f762c594c0187bef121b7871f0ee158074640b6adf815d","plan_sha256":"5521be99acf1d29dd7e632d68274ef1c7f4d2d149a24041477d45070500b418e"} | PASS | Independent review, two rounds on 2026-11-14 (W03-D65 and W03-D66 revisions): every FIX item and the round-2 notes applied and confirmed over the bytes named here; APPROVE. This row records a review, not an approval. | yes | none |
| EVD-004 | [VAL-SPECPLAN-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve all three to the SPEC-0200, SPEC-0203 and SPEC-0205 approval question naming spec.md bc0a9893 and plan.md 5521be99 dated 2026-11-14 Asia/Seoul","review_ref":"EVD-003","scope":["SPEC-0200","SPEC-0200-PLAN-0001"],"reviewed_spec_sha256":"bc0a9893e5729ff285f762c594c0187bef121b7871f0ee158074640b6adf815d","reviewed_plan_sha256":"5521be99acf1d29dd7e632d68274ef1c7f4d2d149a24041477d45070500b418e","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-SPECPLAN-001](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-001 and record PASS evidence | platform |
| [VAL-SPECPLAN-002](../spec.md#success-criteria--verification-plan) | pending | none | Implement WORK-002 and WORK-003 and record PASS evidence | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (`docs/99.templates/registry.json`, `scripts/validate-document-lifecycle.py`, `scripts/document_lifecycle.py`, the Spec and Plan templates and the three link fragments of the Task template under `docs/99.templates/templates/specs/`, the Spec and Plan of SPEC-0161 to the reviewed bytes only, the link fragments of the SPEC-0161 Task, the Spec, Plan and Task link fragments of every open package, the named tests, among them `tests/test_task_acceptance_contract.py`, `tests/test_task_acceptance_boundaries.py` and `tests/test_documentation_link_boundary.py` for their anchor strings, and `tests/fixtures/completion-package.json`, and the named sentences of `.agents/governance/document-lifecycle.md`, `.agents/governance/document-authoring.md`, `.agents/skills/risk-report/SKILL.md`, `docs/99.templates/README.md`, `docs/03.specs/README.md` and rule 7 of `docs/03.specs/AGENTS.md`), this package, the W03-D59 row, the handoff closures, evidence rows and the frontmatter `version` and `updated` of the SPEC-0161 Task, the matching entries of the work residue ledger, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: any other content at the Spec and Plan of SPEC-0161, any cell of a recorded evidence row beyond the mapped link fragment, any Task heading or Task table shape, any Requirement, architecture description or ADR, any other script, any recorded decision or handoff rewrite, `.github/workflows/`, the external task package under `_workspace/`, `.claude/`, `.codex/`, hooks, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes, which changed after the receipts above and are awaiting re-approval of the current bytes; the two moved files of SPEC-0161 before their hashes enter the code; criterion acceptance; any change beyond the Spec's named scope, which stops the work and goes to the user; push, PR and merge
- **Static Validation**: strict document validators, the `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, `ruff check scripts tests`, markdownlint over the edited Markdown, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

The Spec and Plan keep `status: approved` and were revised after the recorded review and approval receipts (W03-D65, W03-D66); they are awaiting re-approval of the current bytes. Implementation not started.
