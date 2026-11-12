---
title: "W03 Runbook Form"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0170-TSK-0001"
parent_ids: ["SPEC-0170-PLAN-0001"]
---

# Task: W03 Runbook Form

## Overview

This Task records the second phase-2 package of W03, the Runbook form, for [SPEC-0170](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user again asked to investigate every remaining, unverified, unreviewed, unconfirmed, unprogressed, conflicting and missing W03 item, review each and continue, fixing existing rules that conflict with current requirements. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-runbook-form` from `8b9d54a6` (SPEC-0169 closure, merged into `main` by PR #234); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D03, W03-D04, W03-D08 and W03-D11; EVD-018 (current v14.7 requirements prevail).
- **Decision taken in this package:** W03-D13, the user's direct answer "Register local H3 (Recommended)" on 2026-11-12 to the question of where non-rollback recovery procedures go: a registered conditional local H3 `Recovery Procedures` under Recovery.
- **Required form:** COMMON-DOC-FORM-1 1.0.0 Runbook (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[7]); read-only input.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | Registry form, extension, TemplateDefinition and tables; repository-registry tests. | platform | in-progress | PASS | EVD-004 |
| WORK-002 | [VAL-RUNBOOKFORM-002](../spec.md#success-criteria--verification-plan) | Template and ten runbooks moved form-only with the meaning map; policy, README and skill text; regression and exact-index QA. | platform | in-progress | PASS | EVD-005, EVD-006, EVD-007 |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `be71c941…`, plan.md `bcd402f9…`; 2026-11-12 | FAIL | REJECT: BLOCK recovery procedures as H4 directly under the Recovery H2 fail markdownlint MD001 (reproduced) in five runbooks; BLOCK the claim of no anchor link is false (0010 links `#recovery-and-escalation`, which the link validator skips); FIXes: PR #234 stated open but merged, heading-level rule too narrow, troubleshooting placement, untyped control-surface and tooling links, Korean none-lines and markdownlint command; NOTEs on named tests, executor sentences, H3 count and the stale runbooks README. | no | none |
| EVD-002 | [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"c82ae4154f804acc002a6d5dd2e49a9d3aa32b70029b8bdb0a3e377731d6d3b1","plan_sha256":"252b893e1b41d628685bd464307b039f3b6b007a12adf432e56187b8e39acecc"} | PASS | Same reviewer, rounds 2 and 3, 2026-11-12: round 2 confirmed every round-1 finding closed, including the user's W03-D13 `Recovery Procedures` local H3 (checked against the tree and registry extension checks), and APPROVE with four wording items; the author applied them; round 3 confirmed both hashes and that only those edits changed, verdict APPROVE; the first package commit was then refused by `LANG-ENGLISH-FIRST` because spec.md quoted Korean runbook text on two lines, which the author replaced with English descriptions; round 4 confirmed only those two lines changed with unchanged meaning, verdict APPROVE with no open finding. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0170 re-approval question naming spec.md c82ae415 and plan.md 252b893e dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0170","SPEC-0170-PLAN-0001"],"reviewed_spec_sha256":"c82ae4154f804acc002a6d5dd2e49a9d3aa32b70029b8bdb0a3e377731d6d3b1","reviewed_plan_sha256":"252b893e1b41d628685bd464307b039f3b6b007a12adf432e56187b8e39acecc","validity":"confirmed","revocation":"none"} | PASS | The earlier answer approving spec.md `db5c7b5e…` lapsed when those bytes changed; this receipt names the current bytes. Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Registry form, extensions, TemplateDefinition and tables, red then green | Working tree over `57cc11df`; implementer repo-tooling-engineer subagent, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log): `tests.test_common_form_tree` 88 tests with 11 failures and 2 errors before the registry change. Green: 88 OK. The author compared the registry Runbook form with COMMON-DOC-FORM-1 1.0.0 roles[7] (sections, `h1`, `language_rule`, `extension_policy`): equal. Extensions `runbook-recovery-procedures` under `runbook-recovery` and `runbook-lifecycle-traceability` under `runbook-validation`. Tests: the three repository-registry tests rewritten to assert exactly the Guide and Runbook forms; 13 `RunbookFormTests` cases cover the Triggers table (header-only passes, reordered or missing columns fail, the four-column Step table is not identified, tables outside Actions ignored), Recovery Procedures (accepted under Recovery, wrong parent fails, absent passes, empty fails), Lifecycle Traceability placement, derived heading lists and tables copied to `operation/runbook`. The `with_form` helper now replaces a form in place so two forms keep their order; tests that used `operation/runbook` as the no-form example now use `operation/policy`; no assertion weakened. | yes | none |
| EVD-005 | [VAL-RUNBOOKFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Runbook meaning map and added lines | Ten runbooks at `57cc11df` against the working tree; two doc-writer subagents built each file by copying source line ranges; author word-multiset comparison per runbook (frontmatter, headings, rules and list markers ignored) | PASS | Removed words are only links already inline elsewhere in the same runbook with their labels (0003, 0007, 0008, 0009, 0010, 0011) and renamed section pointers. Added words are only the "related documents" line prefixes and the none-with-reason lines. Per runbook: Purpose split into Trigger and Outcome and Scope (executor, type and boundary lines of 0011 and 0012 to Authority and Access); Trigger and Preconditions bullets to Trigger and Outcome, Safety Checks or Authority and Access (0010 pre-check block as H4 in Safety Checks; 0012 stop sentence to Stop Conditions); Procedure to Actions with H3 as H4 and logical children as H5 (0004 router check under Procedure 4; 0007 sub-steps and Troubleshooting questions; 0009 external Prometheus query and 3-1 to 3-3; 0010 1-1 to 1-4); Verification to Service Checks and Evidence (0001 Troubleshooting Matrix as H4 in Service Checks); Recovery and Escalation to Recovery Procedures (0001, 0002, 0003, 0004, 0007, 0010, 0011, 0012), Rollback (undo content in 0001, 0002, 0004, 0007, 0008, 0009, 0010, 0011) and Escalation; Lifecycle Traceability under Validation unchanged. Pointer edits: 0010 anchor retargeted to Rollback; section names Procedure and Verification renamed to Steps and Validation in 0002, 0003, 0007 and 0009 pointer sentences. Added lines, all Korean none-with-reason: Stop Conditions in nine runbooks (no separate list; checks stay in Actions; on failure follow Recovery and Escalation; 0011 points to its step 6 hold condition); Safety Checks in eight; Authority and Access in six; Escalation in six; Scope in 0007. The author replaced the implementers' first Stop Conditions line, which was untrue for 0001, and removed a stale section name from the Escalation lines. Reviewer notes kept for the user: 0009 Rollback keeps a bullet on reviewed AppProject changes with the undo bullets; 0004 moves two departed-Spec identifiers to Scope. | yes | none |
| EVD-006 | [VAL-RUNBOOKFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Author run over the working tree after `d6e41b86`, 2026-11-13 | PASS | The four strict document validators exit 0 with output byte-identical to the before run at `57cc11df`. `python3 scripts/validation/repository/quality.py --root .` PASS (command boundary markers found); `form_contracts.py` rc 0; markdownlint over the ten runbooks, the template and the skill reports 0 issues; `ruff check scripts tests` clean; `graphify update .` rc 0. Suites: `agent-governance` 104, `ci-metadata` 87, `cluster-gate` 72, `document` 414, `document-lifecycle` 18, `release` 29, `tooling` 166, `validation-routing` 173 OK; `qa-runner` 37 with the one pre-existing default-branch error handed to W05 as SPEC-0161 W03-H11. `.secrets.baseline` registry `source_revision` line 6100 moved to 6197 in `d6e41b86`. | yes | none |
| EVD-007 | [VAL-RUNBOOKFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 17 files over `d6e41b86` (about 1,570 lines added, 570 removed) | PASS | Risk class `medium` (registry, test and governed document change across ten operating documents). Checklist: scope matches the Spec; one writer per file; the form equals the external contract; ADR-0033 and ADR-0059 unchanged; no script changed; no check weakened; policy text `document-authoring.md` 3.8.0, `docs/99.templates/README.md` 0.20.0, runbooks README 0.4.0 and `ops-runbook` skill 1.1.0 name the new sections; no runbook command, approval or boundary marker added or removed; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow changed. | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RUNBOOKFORM-001](../spec.md#success-criteria--verification-plan) | pending | EVD-004 | Awaiting the operator's acceptance | platform |
| [VAL-RUNBOOKFORM-002](../spec.md#success-criteria--verification-plan) | pending | EVD-005, EVD-006, EVD-007 | Awaiting the operator's acceptance | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (including the W03-D13 row of the SPEC-0161 Task), this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document`, `document-lifecycle` and `agent-governance` suites, repository quality gate, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface and no runbook command is run
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); both criteria await the operator's acceptance. Risk class `medium`. Residual risk: the none-with-reason lines and two placement judgements in EVD-005 await the user's review. Next owner: the operator.
