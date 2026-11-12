---
title: "W03 Root README Form"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0172-TSK-0001"
parent_ids: ["SPEC-0172-PLAN-0001"]
---

# Task: W03 Root README Form

## Overview

This Task records the fourth phase-2 package of W03, the Root README form, for [SPEC-0172](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-readme-forms` from `40b44bd4` (SPEC-0171 closure; PR #236 open); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D08, W03-D10 and W03-D11; handoff W03-H10; EVD-018 (current v14.7 requirements prevail).
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Root README (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[11]); read-only input.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | Registry form, TemplateDefinition, table and navigation section; navigation rule and reader; optional trailing columns; tests. | platform | in-progress | PASS | EVD-004 |
| WORK-002 | [VAL-ROOTREADME-002](../spec.md#success-criteria--verification-plan) | `README.md` and template moved with the map; policy texts; regression and exact-index QA. | platform | in-progress | PASS | EVD-005, EVD-006, EVD-007 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `92ac2a6e…`, plan.md `35a9061f…`; 2026-11-13 | FAIL | APPROVE in substance but five FIXes changed text: README counts (44, 26, 17 H3), the reader level and duplicate-title ambiguity, the policy text targets (the Common forms bullet), the optional-column order rule in the registry, and the risk-report scale; notes on navigation coverage, the cloud-example paragraph, the Support and Ownership none-line, a raw registry without `common_forms` and the terminal-contract consumer. | no | none |
| EVD-002 | [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"e8802a7dfd7603906e7ffd95b073cecd3e88638bf25386e2daa3e15b5f80189a","plan_sha256":"df5879f83595fe95ea68633f5df355b151333e8a0e3358027afc55208b24a603"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-13: round 2 confirmed the round-1 fixes and asked two more (the navigation link count four to one, and a reader that needs no form data: first H2, else first H3); the author applied them and four notes; round 3 confirmed both hashes and that only those edits changed, verdict APPROVE with no open finding. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0172 approval question naming spec.md e8802a7d and plan.md df5879f8 dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0172","SPEC-0172-PLAN-0001"],"reviewed_spec_sha256":"e8802a7dfd7603906e7ffd95b073cecd3e88638bf25386e2daa3e15b5f80189a","reviewed_plan_sha256":"df5879f83595fe95ea68633f5df355b151333e8a0e3358027afc55208b24a603","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Registry form, navigation rule and reader, optional columns, red then green | Working tree over `a693e1b5`; implementer repo-tooling-engineer subagent, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log): `tests.test_readme_navigation` 36 tests with 3 failures (H3 section links and H4 content, H3 exclusion, registry accepting a form H3); `tests.test_common_form_tree` 9 failures (five-form registry tests, optional trailing column and required-after-optional cases, new `RootReadmeFormTests`). The repeated-title test was shown not vacuous by removing the uniqueness check, which failed it. Green: 156 tests OK (one shared base skipped). The author compared the registry Root README form with COMMON-DOC-FORM-1 1.0.0 roles[11]: equal; navigation section `Directories`, `complete` false. | yes | none |
| EVD-005 | [VAL-ROOTREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | README.md meaning map | `README.md` 0.3.1 against 0.4.0; implementer map and word-multiset comparison, read by the author | PASS | Project Role: blockquote, Overview and Audience. Boundaries: In Scope, Out of Scope and the current implementation boundary as H4. Directories: the tree block, Top-level Areas and Tech Stack (with the cloud-example paragraph) as H4. Canonical Entry Points: Documentation Map, Repository Workflow and Common Workflows as H4. Prerequisites: the tool and runtime list. First Verified Path: steps 1 to 5 and Verification as H4. Current Documentation: Related Documents links, Language Policy and Relative Link Rules as H4. Support and Ownership: the Canonical Owners list and one added Korean none-with-reason line stating that the repository holds no separate inquiry or error-reporting route. Word comparison: only frontmatter version and date and that line differ. The Stage 99 guide link and the strings `docs/README.md` and `Plan/Task` stay. | yes | none |
| EVD-006 | [VAL-ROOTREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Author run over the working tree after `126c2f53`, 2026-11-13 | PASS | The four strict document validators exit 0 with output byte-identical to the before run at `a693e1b5`, so the root README navigation result is unchanged. `quality.py` PASS; `form_contracts.py` rc 0; markdownlint over the four edited Markdown files 0 issues; `ruff check scripts tests` and `ruff format --check scripts tests` clean; `graphify update .` rc 0. Suites: `agent-governance` 104, `ci-metadata` 87, `cluster-gate` 72, `document` 454, `document-lifecycle` 18, `release` 29, `tooling` 166, `validation-routing` 173 OK; `qa-runner` 37 with the known default-branch error (SPEC-0161 W03-H11). `.secrets.baseline` registry `source_revision` line 6374 moved to 6437 in `126c2f53`. | yes | none |
| EVD-007 | [VAL-ROOTREADME-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 10 files over `126c2f53` | PASS | Risk class `medium` (registry, validator code, tests and the repository entry document). Checklist: scope matches the Spec; one writer per file; the form equals the external contract; ADR-0033 and ADR-0059 unchanged; the navigation reader prefers H2 and falls back to H3 only, the registry confines H3 names to form profiles and refuses absent or repeated titles; optional columns only trail required ones; no check weakened; policy text `document-authoring.md` 3.10.0 and `docs/99.templates/README.md` 0.22.0; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow changed. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-ROOTREADME-001](../spec.md#success-criteria--verification-plan) | pending | EVD-004 | Awaiting the operator's acceptance | platform |
| [VAL-ROOTREADME-002](../spec.md#success-criteria--verification-plan) | pending | EVD-005, EVD-006, EVD-007 | Awaiting the operator's acceptance | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); both criteria await the operator's acceptance. Risk class `medium`. Next owner: the operator.
