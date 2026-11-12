---
title: "W03 Common Form Model"
version: "0.2.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0168-TSK-0001"
parent_ids: ["SPEC-0168-PLAN-0001"]
---

# Task: W03 Common Form Model

## Overview

This Task records phase 1 of W03, the common form model, for [SPEC-0168](../spec.md) under its [Plan](../plan.md).

## Inputs

- **Request:** on 2026-11-12 (Asia/Seoul) the user pasted the v14.7 W03 prompt (package `_workspace/workspace_execution_tasks/tasks/TASK-hy-home-k8s-W03.md`) and asked to continue. The prompt approves no Spec bytes, criterion, push, PR or merge.
- **Base:** branch `claude/w03-v14-7-templates` created from `main` at `0281409b` (PR #232 merge), then `9e03b720` and `dcff9dc5` recording decisions in SPEC-0161; worktree clean; hook environment `hyhome.validationVenv` set.
- **Decisions reused:** SPEC-0161 EVD-018 (current v14.7 requirements prevail; Q-07 display numbers; Q-08 path kept), EVD-025 and EVD-026 (W03-D01 to W03-D05).

### Survey

Two read-only delegated surveys at `0281409b` and `9e03b720`. Read in part: the W03 package task (sections 2 to 11), the package `COMMON-SECTION-CONTRACT.json`, `COMMON-ROLE-FORMS.json`, `TEMPLATE-DEFINITION.schema.json` and `TEMPLATE-DEFINITION-CONTRACT.md` (queried, not read whole); `registry.json` (queried); `document-profile.schema.json` lines 25-110; `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/document_lifecycle.py` and `scripts/validate-document-contract-registry.py` at located lines; Stage 02 and 03 `AGENTS.md`; `document-lifecycle.md`; `sdlc.md`. Not read: `COMMON-SECTION-CONTRACT.md` body, template bodies, most tests.

| Item | Current owner | Finding | Action | Phase |
| --- | --- | --- | --- | --- |
| Section tree (R147-04, DOC-05) | registry `sections`; `HeadingContract` | H2 lists only; `ordered` on 4 profiles; no H3, parent, condition or empty policy | ADD model | 1 |
| TemplateDefinition (R45-10, DOC-11) | template profiles | Absent | ADD model; fill per role | 1, 2, 3 |
| Role binding (POLICY-ROLE, DOC-04) | `sdlc.md:95` text | No registry record | ADD `document_role` | 1 |
| Authority guard | `scripts/document_authority.py:22-72,122-170` | Exact profile key set; closed top-level keys; bans `role`, `roles`, `skill` and other agent field names anywhere | CHANGE: three optional keys; ban kept | 1 |
| Registry generation | `document_contracts.py:2034` pins 10; ADR-0033 current-state note lists generation-10 keys | Adding keys makes the note false; `provider_write_guard.py:378-380` and `validate-document-lifecycle.py:1934` also pin 10 | ADR-0059 amends the key list; generation stays 10, as for earlier optional keys | 1 |
| Shared contract (W01 handoff) | registry `shared_contract`; schema; `document_contracts.py:714,1572-1582,1753`; `document_lifecycle.py:782`; `tests/test_task_acceptance_contract.py`; `document-authoring.md:239-241` | No approval fields; no `approved` stage; extensions are strings looked up by name | CHANGE with one name accessor | 1 |
| Table columns (W03 package) | registry body contracts | Not modelled | DEFER | 2 |
| Frontmatter parser (DOC-04, RS-01, RS-02) | `validate-markdown-profiles.py:101-160,1056-1080,1417-1428` | Rejects duplicate keys (`FM-DUPLICATE-KEY`), invalid dates (`FM-DATE`), unregistered keys (`FM-KEYSET`) | KEEP | none |
| Fenced and commented headings (RS-51) | `scan_headings` (`validate-markdown-profiles.py:300`) | Skips fences and HTML comments; quotes and indented code excluded by the heading pattern | KEEP; add negative tests | 1 |
| Release role (R45-06) | registry, templates | No Release profile, template or generator; `scripts/release.py` publishes the changelog and GitHub Release | KEEP | none |
| Generator | none | No generator; templates copied by hand | Record reason; no build | 1 |
| Role forms and document migration | 84 profiles; about 129 documents in 16 roles | All differ from COMMON-DOC-FORM-1 | CHANGE | 2, 3 |
| Retired identity reservation (W02-H01) | `document_lifecycle.py:408-445` | Base-only reservation | DEFER to W05 | after 1 |
| ADR `rejected` state | registry ADR domain | Stored terminal state | DEFER to W04 | W04 |

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-FORMMODEL-001](../spec.md#success-criteria--verification-plan) | Schema, registry and parser model with registry negative tests. | platform | in-progress | PASS | EVD-004 |
| WORK-002 | [VAL-FORMMODEL-002](../spec.md#success-criteria--verification-plan) | Heading-tree diagnostics with positive and negative tests. | platform | in-progress | PASS | EVD-005 |
| WORK-003 | [VAL-FORMMODEL-003](../spec.md#success-criteria--verification-plan) | Regression over the current tree, handoffs and exact-index QA. | platform | in-progress | PASS | EVD-006, EVD-007; exact-index QA and hooks run on the implementation commit |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-FORMMODEL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Pre-approval review rounds 1 and 2 | Read-only code-reviewer that wrote none of the package; round 1 over spec.md `442ea0c5…`, plan.md `02a9c113…`; round 2 over `e54924d9…`, `b8a9b4a6…`; 2026-11-12 | FAIL | Round 1 REJECT: BLOCK the authority guard (`document_authority.py`) rejects a bare `role` key and any non-listed profile or top-level key; BLOCK extension objects break name lookups in `document_contracts.py`, `document_lifecycle.py` and `test_task_acceptance_contract.py`; FIXes on table columns, TemplateDefinition field mapping, link-only and form-level fields, ADR-0033's stale key list, `document-authoring.md` scope, extension values, handoff resume conditions and verification commands. Round 2 REJECT: BLOCK a `schema_version` 11 bump breaks `provider_write_guard.py` and the history reader in `validate-document-lifecycle.py`; FIX no generation branch. | no | none |
| EVD-002 | [VAL-FORMMODEL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Independent semantic review | {"spec_sha256":"4dbe9f01884bc477d6125e932f93ce50bf24659ac360fbbb8dc17b9cc21d293a","plan_sha256":"f4029377336367e517dedfc241e8adf567e6f12cdc5796e4f4ace02ec307fad0"} | PASS | Same reviewer, round 3 and round 4, 2026-11-12: round 4 confirmed the only plan.md change after round 3 is the Promotion table (target moved to `.agents/governance/document-authoring.md` after `PLAN-PROMOTION` refused a proposed ADR and a Stage 99 target); both hashes matched; every round-1 and round-2 finding closed (renamed keys, optional authority keys with the agent-field ban kept, one extension accessor, generation 10 kept, ADR-0059 amending ADR-0033's key list without editing its body); verdict APPROVE with no BLOCK or FIX. NOTEs: the Plan's phrase about tests pinning generation 10 is vestigial (no such test needs a change); the receipt row below is required before commit. This row records a review, not a second approval. | yes | none |
| EVD-003 | [VAL-FORMMODEL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Spec/Plan first-record approval | {"actor":"user","approval_ref":"Direct current-session user answer Approve these bytes to the SPEC-0168 re-approval question naming spec.md 4dbe9f01 and plan.md f4029377 dated 2026-11-12 Asia/Seoul","review_ref":"EVD-002","scope":["SPEC-0168","SPEC-0168-PLAN-0001"],"reviewed_spec_sha256":"4dbe9f01884bc477d6125e932f93ce50bf24659ac360fbbb8dc17b9cc21d293a","reviewed_plan_sha256":"f4029377336367e517dedfc241e8adf567e6f12cdc5796e4f4ace02ec307fad0","validity":"confirmed","revocation":"none"} | PASS | Earlier user answers approving `e54924d9…`/`b8a9b4a6…` and `4dbe9f01…`/`f50b0420…` lapsed when those bytes changed; this receipt names the current bytes. It does not accept ADR-0059, accepts no criterion and authorizes no push, PR or merge. | yes | none |
| EVD-004 | [VAL-FORMMODEL-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Registry model, authority guard and shared contract, red then green | Working tree over `1bc7c0f1`; implementer quality-engineer subagent, re-run by the author; 2026-11-12 | PASS | Red: `python3 -m unittest tests.test_common_form_tree tests.test_shared_contract_binding tests.test_document_terminal_contract tests.test_task_acceptance_contract` ran 83 tests with 6 failures and 53 errors before the code (implementer log). Green: 92 tests OK. Groups: form registry negatives (bad parent, level, order, conditional `always`, legacy lists, duplicate form, extension without owner, agent fields, bare `role`, differing Policy roles, twin parity), TemplateDefinition, shared-contract approval fields (`approved` without facts, `unverified` without `approval_ref`, extension shape, unique names, one accessor, bare-string historical registry). Registry: 28 profiles carry `document_role`; WGOV-CORE `approved_by`, `approved_at`, `effective_from`, `scope`, `migration`, `rollback` are `unverified` and `consumer_version` is `3.0.0` (author added the four fields the implementer had left absent, per W03-D05, and rewrote the pinning test to check them). `schema_version` 10 kept. | yes | none |
| EVD-005 | [VAL-FORMMODEL-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Heading-tree checks, red then green | `python3 -m unittest tests.test_common_form_tree`; 2026-11-12 | PASS | Red: 51 tests, 2 failures and 31 errors before the code (implementer log). Green: 51 tests OK. Covers `BODY-H3-PARENT`, `BODY-H3-UNSUPPORTED`, `BODY-H3-DUPLICATE`, `BODY-H3-ORDER`, `BODY-H3-REQUIRED`, `BODY-SECTION-EMPTY` (bare `N/A` fails, `N/A` with reason passes, present-but-empty conditional fails), link-only sections, headings in fences, HTML comments and quotes ignored, extension placement, ADR retained form applied only to `accepted`, and an end-to-end run in a temporary directory. | yes | none |
| EVD-006 | [VAL-FORMMODEL-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Regression over the current tree | Author re-run over the working tree after `1bc7c0f1` with `hyhome.validationVenv/bin` on `PATH`; 2026-11-12 | PASS | Strict registry (292 paths), Markdown profile, link/owner and lifecycle validators exit 0 with 0 FAIL lines, byte-identical to the implementer's before run; agent governance PASS; affected surfaces PASS (uncovered 0, ambiguous 0). Suites: `document` 377 tests OK (313 before), `agent-governance` 104 OK (104 before), `document-lifecycle` 18 OK, `tooling` 166 OK, `validation-routing` 173 OK. `ruff check scripts tests` clean. `.secrets.baseline` registry line moved 5988 to 6017 in `1bc7c0f1`, then corrected to 6016 (detect-secrets counts from the line above the `grep -n` number, as 5988 did for 5989) in `f4abea64` after the staged nonstyle check refused 6017. | yes | none |
| EVD-007 | [VAL-FORMMODEL-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Semantic review: risk class and core-diff checklist | Diff of 14 files over `1bc7c0f1` (about 1,660 lines added, 110 removed) | PASS | Risk class `medium` (registry, authority guard, validator and test change). Checklist: scope matches the Spec's list; one writer per file; consistent with ADR-0033 as amended by proposed ADR-0059 and with the W01 extension and approval rules; no check weakened (the agent-field ban and exact required profile keys stay; `BODY-HEADING-EMPTY` unchanged for current profiles); no secret read; recovery is reverting the implementation commit. No permission, trigger, hook or workflow changed; `provider_write_guard.py` untouched. Interpretations recorded: approval fields required are `approved_by`, `approved_at`, `effective_from`; the typed reader accepts bare-string extensions only for historical registries; profile `sections` stays inline in the schema for an out-of-scope subschema test; tree mode reuses the current H1/H2 rule IDs, README rule IDs are a phase-2 decision. NOTE: the Plan's phrase about tests pinning generation 10 needed no change. | yes | none |
| EVD-008 | [VAL-FORMMODEL-003](../spec.md#success-criteria--verification-plan) | WORK-003 | ADR-0059 acceptance | Direct current-session user answer "Accept ADR-0059" to the question naming its decisions, 2026-11-12 Asia/Seoul | PASS | ADR-0059 moves from `proposed` to `accepted` in the implementation commit; its Overview records the acceptance. This accepts no SPEC-0168 criterion. | yes | none |

### Handoffs

| Item | Owner | Interface | Resume condition |
| --- | --- | --- | --- |
| Phase 2 forms (Guide, Runbook, Policy, Incident, Postmortem, READMEs, `AGENTS.md`, `SKILL.md`) and table column contracts | W03 | One role form per change in `common_forms`, TemplateDefinitions filled, documents moved form-only | This package accepted |
| Phase 3 forms (Requirement, Architecture, ADR with W03-D02, Spec, Plan, Task) and removal of the generation-10 H2 lists | W03 | Consumer renames and the `TASK-EVIDENCE-RETENTION` heading map | Phase 2 accepted; if W04 starts first, record the slip in SPEC-0161 |
| Retired-identity reservation (SPEC-0161 W02-H01) | W05 | Reserve IDs named in the owners' `Archived Lineage`; refusal test for a retired SPEC ID | This package accepted |
| Generator reason | W05 | Verify that template parity and the template-mode tree check stand in for a generator | This package accepted |
| ADR `rejected` state | W04 | Keep or remove the stored state given the W02 exit rule | W04 starts |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-FORMMODEL-001](../spec.md#success-criteria--verification-plan) | pending | none | Registry model and negatives | platform |
| [VAL-FORMMODEL-002](../spec.md#success-criteria--verification-plan) | pending | none | Heading-tree checks | platform |
| [VAL-FORMMODEL-003](../spec.md#success-criteria--verification-plan) | pending | none | Zero new diagnostics and handoffs | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: the files the Spec's scope names, this package, `docs/03.specs/README.md`, `.secrets.baseline` (this Task's reviewed digests only)
- **Forbidden Paths**: any current document or template body, `.github/`, `.claude/settings.json`, hooks, accepted ADR bodies, `docs/98.archive/`
- **Approval Required**: Spec and Plan bytes; criterion acceptance; any push, PR or merge
- **Static Validation**: strict document validators, `document` and `agent-governance` suites, `ruff check scripts tests`, staged lifecycle check, `python3 scripts/qa.py staged`
- **Live Validation**: DEFER; no live surface
- **Secret / Vault Handling**: no secret read or printed
- **Rollback Plan**: revert the implementation commit
- **Evidence Location**: this Task

## Verification Summary

WORK-001 to WORK-003 implemented; EVD-004 to EVD-007 PASS. The user accepted ADR-0059 on 2026-11-12 (EVD-008); criterion acceptance is pending. Risk class `medium` (registry, authority guard, validator and test change; no permission, trigger, hook, workflow or protected action).
