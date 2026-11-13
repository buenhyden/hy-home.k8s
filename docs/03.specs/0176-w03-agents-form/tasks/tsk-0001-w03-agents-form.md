---
title: "W03 AGENTS Form"
version: "0.3.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0176-TSK-0001"
parent_ids: ["SPEC-0176-PLAN-0001"]
---

# Task: W03 AGENTS Form

## Overview

This Task records the eighth phase-2 package of W03, the AGENTS form, for [SPEC-0176](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-13 (Asia/Seoul) the user asked to continue the remaining W03 items and said W03 must be complete before W04. The request approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-agents-form` from `8df46a30` (SPEC-0175 closure, contained in `main` after PR #240 merged as `094eb1c6`); worktree clean apart from this package.
- **Decisions reused:** SPEC-0161 W03-D01, W03-D08 and W03-D10; EVD-018 (current v14.7 requirements prevail).
- **Decision taken in this package:** asked whether the root `AGENTS.md` takes the AGENTS form although the 30-line thin-gateway rule would refuse it, the user answered on 2026-11-13 "follow the requirements"; DOC-02 and COMMON-DOC-FORM-1 give every `AGENTS.md` the AGENTS role, so the root file takes the form and the gateway rule counts content lines (W03-D18). A staged QA routing gap found in review is handed to W05 (W03-H12), following the work split the requirements set.
- **Required form:** COMMON-DOC-FORM-1 1.0.0 AGENTS (`_workspace/workspace_execution_tasks/dependencies/contracts/COMMON-SECTION-CONTRACT.json`, roles[14]); conditional content from `COMMON-ROLE-FORMS`; read-only inputs.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | Registry form, template profile, TemplateDefinition, table, patterns and binding; gateway rule; tests. | platform | completed | PASS | EVD-004 |
| WORK-002 | [VAL-AGENTS-002](../spec.md#success-criteria--verification-plan) | 16 files and the template moved with the map; policy texts; regression and exact-index QA. | platform | completed | PASS | EVD-005, EVD-006, EVD-007; implementation commit `6cb7c216` passed exact-index QA and the hooks |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review round 1 | Read-only code-reviewer that wrote none of the package, over spec.md `3e70d053…`, plan.md `bf299adc…`, with a scratch simulation of the proposed registry, template, formed root file and gateway rule; 2026-11-13 | FAIL | REJECT: BLOCK six document-suite failures from test pins the Spec did not name (form constants and loop, the policy-role test, the template placeholder grammar, the root-file residue assertion); FIXes on the template twin's frontmatter, the folder preamble paragraph, the exact gateway count with a heading cap, two stale policy sentences, PR #240 being merged, a staged QA routing gap, consumer paths and the stated reading of the requirements. The reviewer confirmed that the requirements bind the root file, that native profiles can carry the form and template, and that a formed root file passes with the changed count. | no | none |
| EVD-002 | [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"4efeeba527de43cbb6ca836ad2bf2e03be7845dc569516e444bef9e6528caf20","plan_sha256":"b094721c76ad01dc39e360fd4552b555792faa3cc18e32486ee4fb862bf5c858"} | PASS | Same reviewer, round 2, 2026-11-13: every round-1 item closed (the routing gap by the requirements' work split, handed to W05 as W03-H12); one wording fix in the Interfaces bullet, applied without changing meaning; verdict APPROVE. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0176 approval question naming spec.md 4efeeba5 and plan.md b094721c dated 2026-11-13 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0176","SPEC-0176-PLAN-0001"],"reviewed_spec_sha256":"4efeeba527de43cbb6ca836ad2bf2e03be7845dc569516e444bef9e6528caf20","reviewed_plan_sha256":"b094721c76ad01dc39e360fd4552b555792faa3cc18e32486ee4fb862bf5c858","validity":"confirmed","revocation":"none"} | PASS | Approves the Spec and Plan bytes only; accepts no criterion. | yes | none |
| EVD-004 | [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Registry form, template profile, table, patterns, gateway rule and tests, red then green | Working tree over `6eb3a2ad`; implementer repo-tooling-engineer subagent, re-run by the author with `hyhome.validationVenv/bin` on `PATH`; 2026-11-13 | PASS | Red (implementer log): `tests.test_agent_governance` 4 failing subtests in the new gateway test (the formed gateway refused and 17 headings accepted, for both providers; 31 content lines were refused before and after); `test_common_form_tree`, `test_repository_quality_rules` and `test_document_language` 13 failures and 4 errors of 216. Green: 63 and 216 OK (one skipped base). The AGENTS form is built from COMMON-DOC-FORM-1 1.0.0 roles[14] by the mapping that reproduces the eight existing forms; `common/folder-agents-guide` selects every `AGENTS.md` outside the archive with `document_role` `agents` and the new template; `common/root-provider-shim` selects only `CLAUDE.md`; `common/template-agents-guide` carries frontmatter `absent`, the `Tool Rules` table and 31 regular consumer paths; `AGENT-NATIVE-REFERENCE` refuses more than 30 content lines or 16 heading lines with its other conditions unchanged. | yes | none |
| EVD-005 | [VAL-AGENTS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | 16 files and the template meaning map | Implementer map (doc-writer subagent) and a sorted line comparison of every file against `HEAD`, read by the author | PASS | Removed lines are only the old H2 headings; old H3 headings in `examples/azure/AGENTS.md` became H4; rule lists, numbering, links and every `Read ... before acting.` line are unchanged; the folder preamble paragraph stays under the H1. The root `AGENTS.md` has 23 content lines and 16 headings. Added lines are English pointer or none lines only; the author read the clause-only pointers against their rules. Placement calls for owner review: Canonical Sources and Inspect and Change lines in every folder file point to the opening paragraph and Local Obligations; Non-goals and Protected Actions in `docs/AGENTS.md` point to the Purpose sentence that agents here do not change runtime state; Stop and Escalate in `scripts/AGENTS.md` points to rule 2 (never weaken a gate or a test to finish); the root file states none for Allowed Surface, Non-goals, Local Obligations, Handoff, Required Checks, Protected Actions and Stop and Escalate. | yes | none |
| EVD-006 | [VAL-AGENTS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Regression over the tree, suites and lint | Author run over the staged index after `d4f1eb8a`, 2026-11-13 | PASS | The four strict document validators and `validate-agent-governance.py` exit 0 with output equal to the before run at `6eb3a2ad`. `quality.py` PASS; markdownlint over the edited Markdown 0 issues; `ruff check scripts tests` and `ruff format --check scripts tests` clean; `tests.test_k8s_pre_edit_hook` OK; `graphify update .` rc 0. Suites: `agent-governance` 105, `ci-metadata` 87, `cluster-gate` 72, `document` 503, `document-lifecycle` 18, `release` 29, `tooling` 166, `validation-routing` 173 OK; `qa-runner` not re-run (known W03-H11 error). Staged QA routing for some folder `AGENTS.md` is the known W03-H12 limitation; this whole-tree run is its evidence. `.secrets.baseline` registry `source_revision` line 6924 moved to 7054 in `d4f1eb8a`. | yes | none |
| EVD-007 | [VAL-AGENTS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Semantic review: risk class and core-diff checklist | Diff of 26 files over `d4f1eb8a` | PASS | Risk class `medium` (registry, one provider gate, tests and the 16 instruction files agents load). Checklist: scope matches the Spec; one writer per file; the form equals the external contract; W03-D18 applied; the gateway keeps its required references, loader lines and catalog ban and stays at 23 content lines; root `CLAUDE.md` and folder imports untouched; provider notes and `agent-execution.md` unchanged; policy text `document-authoring.md` 3.14.0 and `docs/99.templates/README.md` 0.26.0; no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow changed. | yes | none |
| EVD-008 | [VAL-AGENTS-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Manual package-exit decision freeze | This package's `spec.md`, `plan.md` and Task; the consumers named below; the user's 2026-11-13 standing approval of commit, push, PR and merge; Git-history-only method | PASS | The consumer, preservation, hold, authority and method decision is frozen below before this package's final source commit. Each file's committed `commit:path`, retained-ref reachability, temporary restoration and byte comparison are recorded in REQ-0003 Archived Lineage before deletion. An unresolved condition defers the affected deletion. | no | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-AGENTS-001](../spec.md#success-criteria--verification-plan) | accepted | EVD-004 | Accepted by the user on 2026-11-13 (direct message "accept" after the placement calls of EVD-005 were presented; recorded once every check in EVD-006 passed) | platform |
| [VAL-AGENTS-002](../spec.md#success-criteria--verification-plan) | accepted | EVD-005, EVD-006, EVD-007 | Accepted by the user on 2026-11-13 (direct message "accept" after the placement calls of EVD-005 were presented; recorded once every check in EVD-006 passed) | platform |

### Frozen Package Disposition Decision

- **Target and method**: After the final source commit, retire only this Stage 03 package (`spec.md`, `plan.md` and this Task) through Git-history-only recovery. No other document is selected.
- **Consumers and preservation**: The durable contract is promoted to the document authoring policy, the registry and `scripts/validate-agent-governance.py` (Plan Promotion row). W03-D18 and W03-H12 stay recorded in the SPEC-0161 Task. Current consumers: the Stage 03 README entry and this Task's `.secrets.baseline` entries, which the closure change removes. Registry text, code comments and test docstrings name SPEC-0176 as an identifier, not a link, and stay.
- **Hold and authority**: The current repository documents and the user's request identify no hold on these files. The user's 2026-11-13 standing approval of commit, push, PR and merge is the disposition authority. If a hold or unmet consumer is identified before deletion, the affected deletion is deferred and its source kept. Remote retention is not inferred from local refs.
- **Proof handoff**: This Task freezes the decision before its final source commit. After that commit, each file's exact `commit:path`, blob availability, reachability from the retained local ref and a temporary byte comparison with the source still in the tree are recorded in REQ-0003 Archived Lineage before any file is deleted. This Task cannot contain that proof without changing its own bytes.

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, the W03-D18 and evidence rows and the frontmatter `version` and `updated` of the completed SPEC-0161 Task (appended rows only), `.secrets.baseline` (this Task's reviewed digests and moved registry lines only)
- **Forbidden Paths**: every other document or template body, root and folder `CLAUDE.md`, `.claude/`, `.codex/`, `.github/` other than `.github/AGENTS.md`, hooks, accepted ADR bodies, `docs/98.archive/`, `_workspace/workspace_execution_tasks/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, agent-governance validator, `document`, `document-lifecycle`, `agent-governance` and `validation-routing` suites, repository quality gate, markdownlint, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface; native loading is W07 evidence
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit; before that, delete the package commit
- **Evidence Location**: this Task

## Verification Summary

Spec and Plan reviewed (EVD-001, EVD-002); approved by the user at their exact bytes (EVD-003). WORK-001 and WORK-002 implemented with PASS evidence (EVD-004 to EVD-007); implementation commit `6cb7c216`. The user accepted both criteria on 2026-11-13, and the standing approval of commit, push and PR covers the package exit (EVD-008). Risk class `medium`. Next owner: W03 for the Skill package.
