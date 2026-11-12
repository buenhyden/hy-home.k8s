---
title: "W03 Incident and Postmortem Forms"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0171-TSK-0001"
parent_ids: ["SPEC-0171-PLAN-0001"]
---

# Task: W03 Incident and Postmortem Forms

## Overview

This Task records the third phase-2 package of W03, the Incident and Postmortem forms, for [SPEC-0171](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-incident-forms` from `7cf95a2f` (SPEC-0170 closure; PR #235 open); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D03, W03-D08 and W03-D12; EVD-018 (current v14.7 requirements prevail); W03-H10 (covered by derived heading lists).
- **Decisions taken in this package:** on 2026-11-13 the user answered "Combine (Recommended)" to doing Incident and Postmortem in one package as an exception to W03-H01 (W03-D14), and "Register local H3 (Recommended)" to keeping What Went Well as a registered local H3 under Impact (W03-D15).
- **Required forms:** COMMON-DOC-FORM-1 1.0.0 Incident and Postmortem (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[9] and roles[10]); read-only input.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | Registry forms, extensions, TemplateDefinitions and tables; repository-registry and terminal-contract tests. | platform | completed | PASS | EVD-004 |
| WORK-002 | [VAL-INCIDENTFORM-002](../spec.md#success-criteria--verification-plan) | Resolution-evidence lookup and its test; templates moved with the maps; consumer texts; regression and exact-index QA. | platform | completed | PASS | EVD-005, EVD-006, EVD-007, EVD-008; implementation commit `a844cad4` passed exact-index QA and the hooks |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `c5cc649a…`, plan.md `c3551cf9…`; 2026-11-13 | FAIL | REJECT with no BLOCK: FIXes for unmapped incident instructions (affected environment, allowed status values, observed event), the Traceability H2 prompts, What Went Well and What Went Wrong placement (a user question, as for W03-D13), Lifecycle Traceability row identities, missing consumer paths (`quality.py`, `docs/05.operations/AGENTS.md`), decision citations (D11 does not apply; cite H01 and H10) and the W03-H01 departure as a user question. | no | none |
| EVD-002 | [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"e54e2cc30d920dd9f9ecf39017acb3c9184f8fda6400a5c9d9cb0b247502f2da","plan_sha256":"fb889f8ae4b595a22fda2a43b4f7229625d3212fd5298148239c83c40cb3dd45"} | PASS | Same reviewer, round 2, 2026-11-13: every round-1 finding closed, including the user's W03-D14 (one package) and W03-D15 (`What Went Well` local H3, checked against the registry extension and tree checks); verdict APPROVE with no BLOCK or FIX; three optional NOTEs, of which the SPEC-0161 Task `updated` date was applied outside the reviewed bytes. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0171 approval question naming spec.md e54e2cc3 and plan.md fb889f8a dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0171","SPEC-0171-PLAN-0001"],"reviewed_spec_sha256":"e54e2cc30d920dd9f9ecf39017acb3c9184f8fda6400a5c9d9cb0b247502f2da","reviewed_plan_sha256":"fb889f8ae4b595a22fda2a43b4f7229625d3212fd5298148239c83c40cb3dd45","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Registry forms, extensions, TemplateDefinitions and tables, red then green | Working tree over `1682d70b`; implementer repo-tooling-engineer subagent, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log): `tests.test_common_form_tree tests.test_native_skill_envelope tests.test_document_terminal_contract` ran 152 tests with 27 failures and 2 errors before any change. Green: 152 OK (one shared base class skipped). The author compared the registry Incident and Postmortem forms with COMMON-DOC-FORM-1 1.0.0 roles[9] and roles[10] (sections, `h1`, `language_rule`, `extension_policy`): equal. Extensions: `incident-lifecycle-traceability`, `postmortem-lifecycle-traceability`, `postmortem-what-went-well`. Repository-registry tests rewritten to assert exactly the four forms; `IncidentFormTests` and `PostmortemFormTests` cover the Events and Actions tables (registered columns pass, header-only passes, reordered, missing or extra columns fail), What Went Well (accepted under Impact, wrong parent fails, absent passes, empty fails), the What Went Wrong H4 and Lifecycle Traceability placement. The author changed their shared base to a skipped `unittest.TestCase` subclass after `test_every_declared_test_class_is_collected` refused a mixin, and replaced stale per-role wording in the Guide and Runbook TemplateDefinition regression strings with role-neutral wording. | yes | none |
| EVD-005 | [VAL-INCIDENTFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Resolution-evidence rule, red then green | Same run | PASS | After the registry and templates moved, the only remaining failure was `test_resolved_incident_requires_real_zoned_time_and_evidence` (the rule still read `## Closure`); after `INCIDENT-RESOLUTION-EVIDENCE` read `### Recovery Verification` it passed. The test now asserts the rule fires without evidence and that neither incident rule fires once Recovery Verification holds evidence (the old final assertion checked only `INCIDENT-RESOLVED-AT`). | yes | none |
| EVD-006 | [VAL-INCIDENTFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Template maps | Both templates at `1682d70b` against the working tree; implementer map, read by the author | PASS | Incident: Overview to Summary > Event and Current Status; metadata table to Event, its allowed-status note to Current Status, its severity scale to Impact > Severity and Duration, its affected environment to Impact > Affected Users; Roles and Coordination (roles, N/A only with a reason) to Timeline > Decisions; Impact to Affected Users and Severity and Duration; Timeline to Timeline > Events with the optional Events table; Response State to Resolution > Mitigation; Closure (the `resolved_at` rule, evidence, closing owner and remaining risk) to Resolution > Recovery Verification; Evidence to Evidence Sources; Follow-up Actions to Follow-up Owners; the Traceability prompt and table to Evidence > Lifecycle Traceability. Postmortem: Overview to Summary > Review Scope; Incident Link and Impact Summary to Incident Reference and Observed Impact; Root Cause Analysis to Causal Analysis; Contributing Factors there with What Went Wrong as an H4; Detection and Response Review to Impact > Detection and Response; What Went Well to the registered H3 under Impact; Action Items and Documentation Feedback Loop to Corrective Actions > Actions with the optional Actions table; Prevention and Verification and Action Closure to Corrective Actions > Verification, the closing approver to Evidence > Review Decision; Source Records prompts the incident record, logs and decisions; the Traceability prompt and table to Corrective Actions > Lifecycle Traceability. Every former instruction has a place. | yes | none |
| EVD-007 | [VAL-INCIDENTFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Author run over the working tree after `560fd1dc`, 2026-11-13 | PASS | The four strict document validators exit 0 with output byte-identical to the before run at `1682d70b`. `quality.py` PASS; `form_contracts.py` rc 0; markdownlint over the two templates and four edited texts reports 0 issues; `ruff check scripts tests` and `ruff format --check tests` clean; `graphify update .` rc 0. Suites: `agent-governance` 104, `ci-metadata` 87, `cluster-gate` 72, `document` 437, `document-lifecycle` 18, `release` 29, `tooling` 166, `validation-routing` 173 OK (after the shared-base fix); `qa-runner` 37 with the known default-branch error (SPEC-0161 W03-H11). `.secrets.baseline` registry `source_revision` line 6197 moved to 6374 in `560fd1dc`. | yes | none |
| EVD-008 | [VAL-INCIDENTFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 11 files over `560fd1dc` | PASS | Risk class `medium` (registry, one validator rule, tests and templates). Checklist: scope matches the Spec; one writer per file; the forms equal the external contract; ADR-0033 and ADR-0059 unchanged; `INCIDENT-RESOLUTION-EVIDENCE` keeps its condition and its expected text now names Recovery Verification; `INCIDENT-RESOLVED-AT` unchanged; no check weakened; texts `document-authoring.md` 3.9.0, `docs/99.templates/README.md` 0.21.0, incidents README 0.3.0, `incident-postmortem` skill 1.0.2; no status, frontmatter key or lifecycle rule changed; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow changed. | yes | none |
| EVD-009 | [VAL-INCIDENTFORM-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-13 exit authority; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability, temporary restoration and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-INCIDENTFORM-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Accepted by the user on 2026-11-13 (direct answer "Accept both" to the SPEC-0171 criterion question) | platform |
| [VAL-INCIDENTFORM-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-006, EVD-007, EVD-008 | Accepted by the user on 2026-11-13 (direct answer "Accept both" to the SPEC-0171 criterion question) | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names (including the W03-D14 and W03-D15 rows of the SPEC-0161 Task), this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document`, `document-lifecycle` and `agent-governance` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task


### Frozen Package Disposition Decision

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: The durable contract is promoted to the document authoring policy and the registry (Plan Promotion row). W03-D14 and W03-D15 are already in the SPEC-0161 Task; no new handoff arises. Current consumers: the Stage 03 README entry and this Task's `.secrets.baseline` entries, which the closure change removes. The registry TemplateDefinition text, a code comment and test docstrings name SPEC-0171 as an identifier, not a link, and stay.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The user's explicit 2026-11-13 answer "Exit, push and PR" is the disposition authority. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a temporary byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted. This Task cannot contain that proof without changing its own bytes.

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002) and approved at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-008); implementation commit `a844cad4`. The user accepted both criteria and the package exit on 2026-11-13 (EVD-009). Risk class `medium`. Next owner: W03 for the next phase-2 role.
