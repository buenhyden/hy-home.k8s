---
title: "W03 Incident and Postmortem Forms"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0171"
---

# W03 Incident and Postmortem Forms Technical Specification (Spec)

## Overview

This approved change contract is the third phase-2 package of the W03 stage of the external v14.7 execution package. It gives the Incident and Postmortem roles their COMMON-DOC-FORM-1 1.0.0 forms in the Stage 99 registry, with TemplateDefinitions and table contracts, and moves both templates to the forms without losing any author instruction. No incident or postmortem document exists, so only the templates, their consumers and one validator rule move. It reuses the SPEC-0169 model (derived heading lists, the TemplateDefinition `tables` contract and the table checks; recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). The user's decisions W03-D01, W03-D03, W03-D08 and W03-D12 are recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md); W03-D14 (one package for both roles, an exception to W03-H01) and W03-D15 (a registered `What Went Well` local H3), the user's answers of 2026-11-13 to this package's review questions, are recorded in this package's Task and added to that table by this package's first commit. W03-H10's heading-list consumers are covered by the derived lists of SPEC-0169. The [Task](tasks/tsk-0001-w03-incident-postmortem-forms.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for the validator rule): `docs/99.templates/registry.json`, `docs/99.templates/templates/operations/incident.template.md`, `docs/99.templates/templates/operations/postmortem.template.md`, `scripts/validate-markdown-profiles.py` (the `INCIDENT-RESOLUTION-EVIDENCE` section lookup), `tests/test_common_form_tree.py`, `tests/test_native_skill_envelope.py`, `tests/test_document_terminal_contract.py`, the forms paragraph of `.agents/governance/document-authoring.md`, the Operations forms entry of `docs/99.templates/README.md`, the Expected Record Shape of `docs/05.operations/incidents/README.md`, and the section names in `.agents/skills/incident-postmortem/SKILL.md` (Phase 5 and any other heading reference), each with its frontmatter `version` and `updated` where it has one; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Two roles in one change: the SPEC-0161 W03-H01 interface says one role form per change. Both roles share the incident folder, have no current document, and their consumers (the incidents README, the skill and the terminal-contract test) name both; the user approved one package as an exception (W03-D14).
- Not in this package: every other role, which keeps its H2 lists; README rule IDs; phase 3; the incident and postmortem status domains and frontmatter, which stay unchanged.
- Template migration keeps every author instruction's meaning; no new rule, field or status is added. No push, PR or merge without separate approval. Open question: none.

## Contracts

- **Forms.** `common_forms.forms` gains the Incident form (`roles[9]`: Summary with Event and Current Status; Impact with Affected Users and Severity and Duration; Timeline with Events and Decisions; Resolution with Mitigation and Recovery Verification; Evidence with Evidence Sources and Follow-up Owners) and the Postmortem form (`roles[10]`: Summary with Incident Reference and Review Scope; Root Cause with Causal Analysis and Contributing Factors; Impact with Observed Impact and Detection and Response; Corrective Actions with Actions and Verification; Evidence with Source Records and Review Decision), each exactly as COMMON-DOC-FORM-1 1.0.0 defines it, `form_id` `incident` and `postmortem`, `title` `Incident` and `Postmortem`, `link_only` false everywhere. Every H3 is required in the contract. The templates keep their H1. `COMMON-ROLE-FORMS.json` lists Follow-up and What Went Well as conditional content; the section contract has Follow-up Owners as a required H3 and no What Went Well H3, and the section contract governs.
- **What Went Well extension (W03-D15).** `postmortem-what-went-well`, a `local_h3` titled `What Went Well` under `postmortem-impact`, placed after Detection and Response by convention (no check enforces its position): condition "a postmortem records controls or response actions that reduced impact"; owner `platform`; verification "the form tree check"; review "when the Postmortem form version changes"; removal "when the common Postmortem form gains a What Went Well H3". It is conditional: absent passes, present but empty fails `BODY-SECTION-EMPTY`.
- **Lifecycle Traceability extensions (W03-D03, W03-D12).** `incident-lifecycle-traceability`, a `local_h3` titled `Lifecycle Traceability` under `incident-evidence`, and `postmortem-lifecycle-traceability` under `postmortem-corrective-actions`. Each: condition "a document in a status the body contract enforces states its follow-up Task or an N/A reason"; owner `platform`; verification "the body-contract check"; review "when the form version changes"; removal "when incident lineage has another registered owner".
- **Profiles.** `operation/incident`, `operation/postmortem` and their template twins carry empty H2 lists; their heading lists are derived from the forms. `body_contract.section` becomes `Evidence` (incident) and `Corrective Actions` (postmortem); table heading, columns, statuses and target rules stay.
- **Tables (W03-D08).** Incident: `Events` in `incident-timeline-events` with keys `Timestamp`, `Event`, `Actor` (the contract's timestamp/event/actor), `minimum_rows` 0, row identity `Timestamp` (row identity is recorded, not machine-checked; a timestamp may repeat); `Lifecycle Traceability` in `incident-lifecycle-traceability` with the body contract's keys, `minimum_rows` 1, row identity `Timeline or action`. Postmortem: `Actions` in `postmortem-corrective-actions-actions` with keys `Action`, `Owner`, `Verification` (action/owner/verification), `minimum_rows` 0, row identity `Action`; `Lifecycle Traceability` in `postmortem-lifecycle-traceability`, `minimum_rows` 1, row identity `Root cause or action`. The incident metadata table (first header `Field`) is not a contract table and is not checked.
- **TemplateDefinitions.** Each template profile carries purpose, responsibility, non-goals, policy references (`document-authoring.md`, `document-lifecycle.md`, `sdlc.md`), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, every real consumer path (both: registry, schema, its template, Stage 99 README, incidents README, `docs/05.operations/AGENTS.md`, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py`, `tests/test_common_form_tree.py`, `tests/test_document_terminal_contract.py` and the skill; incident only: `tests/test_native_skill_envelope.py`), validation cases, migration and `tables`.
- **Incident template map.** Overview (observed event, current state, response scope) to Summary > Event and Current Status; the metadata table with incident ID and start or detection time to Summary > Event, its current-state and next-checkpoint rows read there, and its note that allowed status values follow the registry `operation/incident` profile to Summary > Current Status; its severity scale named again in Impact > Severity and Duration; its affected-environment item to Impact > Affected Users; Roles and Coordination (commander, operations, communications and escalation owners) to Timeline > Decisions; Impact to Affected Users and Severity and Duration; Timeline to Timeline > Events with the optional Events table; Response State (mitigation, escalation, next checkpoint) to Resolution > Mitigation; Closure (the `resolved_at` rule, resolution evidence, closing owner and remaining risk) to Resolution > Recovery Verification; Evidence to Evidence Sources; Follow-up Actions (owned follow-up Tasks; no root-cause analysis here) to Follow-up Owners; the Traceability H2 prompt becomes the Lifecycle Traceability H3 prompt under Evidence.
- **Postmortem template map.** Overview to Summary > Review Scope; Incident Link and Impact Summary to Summary > Incident Reference (the link) and Impact > Observed Impact (confirmed impact only); Root Cause Analysis to Root Cause > Causal Analysis; Contributing Factors to Root Cause > Contributing Factors, with What Went Wrong (wrong assumptions; failed controls, detection or coordination) as an H4 `What Went Wrong` under it; Detection and Response Review to Impact > Detection and Response; What Went Well (controls and actions that reduced impact) to the registered `What Went Well` H3 under Impact; Action Items to Corrective Actions > Actions with the optional Actions table; Prevention and Verification and Action Closure (owner, due state, completion evidence, remaining risk) to Corrective Actions > Verification, with the closing approver to Evidence > Review Decision; Documentation Feedback Loop (routing lessons to requirement, decision, Spec, guide or policy owners) to Corrective Actions > Actions; Evidence > Source Records gains the prompt to link the incident record, logs and decisions; the Traceability H2 prompt becomes the Lifecycle Traceability H3 prompt under Corrective Actions.
- **Resolution evidence rule.** `INCIDENT-RESOLUTION-EVIDENCE` reads the unique `### Recovery Verification` section instead of `## Closure` (its parent `## Resolution` is enforced by `BODY-H3-PARENT` in the tree check, not by this lookup); its condition (a resolved incident needs concrete, non-placeholder resolution evidence) and `INCIDENT-RESOLVED-AT` stay. `document-lifecycle.md` names no section and stays.
- **Consumer text.** `document-authoring.md` and `docs/99.templates/README.md` add Incident and Postmortem to the roles that use their registry forms, with Lifecycle Traceability under Evidence and Corrective Actions; the incidents README Expected Record Shape lists the new sections; the skill names Corrective Actions > Actions and Verification and Evidence > Review Decision instead of Action Items, Prevention and Verification and Action Closure (its Phase 3 Root Cause Analysis heading belongs to `rca-methodology` and stays), with its `version` and `updated` bumped. Prose that uses action closure as a concept (`docs/05.operations/AGENTS.md` rule 4, the incidents README) is not a heading reference and stays.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes.

## Data Modeling & Storage Strategy

Registry data only: two forms, three extensions, two TemplateDefinitions with two tables each, and four profiles' lists and body-contract sections.

## Interfaces & Data Structures

- `scripts/validate-markdown-profiles.py`: the incident resolution-evidence lookup moves from the `## Closure` section to the unique `### Recovery Verification` section.
- `tests/test_native_skill_envelope.py`: the resolved-incident test fills `### Recovery Verification` instead of `## Closure` and still shows the rule failing without evidence and passing with it.
- `tests/test_document_terminal_contract.py`: the operations-template test reads the loaded profiles' derived heading lists instead of the raw H2 lists and pins form titles (for example `Resolution`, `Evidence`, `Corrective Actions`) instead of `Roles and Coordination`, `Closure`, `Detection and Response Review` and `Action Closure`.
- `tests/test_common_form_tree.py`: the repository-registry assertions name exactly the Guide, Runbook, Incident and Postmortem forms and definitions; synthetic cases cover the Events and Actions tables and the What Went Well extension.

## Edge Cases & Error Handling

- A resolved incident whose Recovery Verification holds only a placeholder still fails `INCIDENT-RESOLUTION-EVIDENCE`.
- Templates are not checked for empty sections or table rows; their placeholder rows still satisfy the template-mode body contract.

## Failure Modes & Fallback / Human Escalation

If any document other than the two templates gains a diagnostic, the change is wrong and is fixed before commit. If a template instruction cannot be placed without changing its meaning, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators over the whole tree; after must equal before.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle` and `--suite agent-governance` (the `document` suite holds `tests/test_native_skill_envelope.py`).
- `python3 scripts/validation/repository/quality.py --root .`; `markdownlint-cli2 --config .markdownlint-cli2.yaml` over the two templates and the edited texts; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-INCIDENTFORM-001 | The registry holds the Incident and Postmortem forms, their three extensions, TemplateDefinitions and tables, and the four profiles carry no H2 lists; derived heading lists equal the forms' H2 titles; the repository-registry tests name exactly the four forms. |
| VAL-INCIDENTFORM-002 | `INCIDENT-RESOLUTION-EVIDENCE` reads Recovery Verification, failing first in its test and then passing; both templates pass the tree, body-contract, author-prompt, residue and markdownlint checks with the template map recorded in the Task; the consumer texts are updated; validator output over the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-INCIDENTFORM-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry tests and strict registry check. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-INCIDENTFORM-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Rule test, strict validators and exact-index QA. |
