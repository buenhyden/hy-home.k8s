---
title: "W03 Common Form Model"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0168"
---

# W03 Common Form Model Technical Specification (Spec)

## Overview

This approved change contract is phase 1 of the W03 stage of the external v14.7 execution package. It adds the machine model that later phases use to move every current document to the COMMON-DOC-FORM-1 headings, without changing any current document's headings. The Stage 99 registry keeps generation 10 and gains, as optional keys, an opt-in section tree per document role, named form extensions, a document-role binding per profile, a TemplateDefinition per template profile, and the shared-contract approval fields W01 handed over. The Markdown profile validator gains the heading-tree checks. No role receives a form in this phase, so every current check result stays the same. [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md), proposed with this package, records the new optional registry keys and amends ADR-0033's current-state key list without editing its body. The user's W03 decisions W03-D01 to W03-D05 are recorded in [SPEC-0161](../0161-w00-v14-7-delta-intake/spec.md); the [Task](tasks/tsk-0001-w03-common-form-model.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code in the same change): `docs/99.templates/contracts/document-profile.schema.json`, `docs/99.templates/registry.json`, `scripts/document_authority.py`, `scripts/document_contracts.py`, `scripts/document_lifecycle.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-document-contract-registry.py`, `scripts/run-contract-tests.py`, `scripts/validation/registry.json`, `tests/test_common_form_tree.py` (new), `tests/test_shared_contract_binding.py`, `tests/test_task_acceptance_contract.py`, `tests/test_document_terminal_contract.py`, `.agents/governance/document-authoring.md` (the shared-contract sentence), ADR-0059; this package, the Stage 03 README and reviewed `.secrets.baseline` digests.
- Not in this phase: adding any role form to the registry and changing any document or template heading (phase 2: Guide, Runbook, Policy, Incident, Postmortem, READMEs, `AGENTS.md`, `SKILL.md`; phase 3: Requirement, Architecture, ADR, Spec, Plan, Task, with the `TASK-EVIDENCE-RETENTION` heading map). Table column contracts are deferred to phase 2 (owner W03; resume before the first role form is added).
- The H2-list model and the tree model coexist only as a bounded migration: phase 3 deletes the H2 lists, the list-built `HeadingContract.allowed` and `BODY-HEADING-EMPTY` for form profiles, and their tests. If phase 3 has not started when W04 starts, W03 records the slip and its resume condition in SPEC-0161.
- No generator is built. Templates are copied by hand and are the checked artifact: template parity and the template-mode tree check keep them equal to the registry. A generator is added only when an author must fill placeholders by machine; W05 verifies this recorded reason.
- ADR-0033's body is not edited; ADR-0059 amends its current-state key list. Accepting ADR-0059 is the operator's decision, recorded in the Task.
- Handed over, not changed here: retired-identity reservation (SPEC-0161 W02-H01, W05) and the ADR `rejected` state (W04).
- No push, PR or merge without separate approval. Open question: none; the user decided W03-D01 to W03-D05.

## Contracts

- **Registry keys (ADR-0059).** `schema_version` stays 10, as it did when `readme_navigation`, `document_language` and `shared_contract` were added as optional keys; the fail-closed pre-edit guard (`scripts/provider_write_guard.py`) and the history reader in `scripts/validate-document-lifecycle.py` pin 10 and stay unchanged. Optional top-level `common_forms` holds `contract_id`, `version` and a `forms` list; each form has `form_id` (one of the 16 common role IDs), `title`, `h1`, `language_rule`, `extension_policy` (all from COMMON-DOC-FORM-1 1.0.0), `sections` and `extensions`. Keys avoid the agent fields the authority guard forbids (`role`, `roles`, `skill` and others).
- **Authority guard (`document_authority.py`).** The required profile key set stays; `document_role` and `template_definition` become optional profile keys, and `common_forms` an optional top-level key. The agent-field ban is unchanged.
- **Section tree (R147-04, DOC-05).** A `section` has `section_id`, `level` (2 or 3), `parent_id`, `title`, `order`, `requiredness` (`required`, `conditional`, `optional`), `condition`, `content`, `required_content`, `prohibited_content`, `empty_policy` (`explain_none_or_not_applicable` or `omit_when_condition_false`), `validation_ids` and `children`, as in COMMON-DOC-FORM-1 1.0.0, plus one local field, `link_only` (default false), carried over from the current link-only treatment of `Related Documents`.
- **Form extensions (W03-D02, D03, D04).** An extension has `id`, `kind` (`local_h3` or `retained_form`), `condition`, `owner`, `verification`, `review` and `removal`; a `local_h3` names `parent_id` and `title`; a `retained_form` names the `statuses` it applies to and the retained H2 lists. These map to the TemplateDefinition schema's extension fields: `condition` and title are its `delta`, `verification` its `validation`, `review` and `removal` its `expiry_or_review`.
- **Role binding (POLICY-ROLE, DOC-04).** A profile may carry `document_role`, one of the 16 common role IDs. `governance/rule`, `operation/policy` and their template twins carry `policy`; profiles with a clear common role carry it; the others carry none. A profile whose role has a form carries no H2 lists. A template twin's role and form must equal its source profile's.
- **TemplateDefinition (R45-10, DOC-11).** A template profile may carry `template_definition` with `purpose`, `responsibility`, `non_goals`, `policy_refs`, `vocabulary_refs`, `applicability`, `consumer_paths`, `validation` and `migration`. Derived, not stored twice: `template_id` (the profile ID), `role` (`document_role`), `contract_version` (`common_forms.version`), `headings` (the form), `metadata` (frontmatter), `relationships` (body contract), `lifecycle` (status domain), `language` (`document_language`), `extensions` (form extensions); `tables` arrive with the phase-2 table contract. It becomes required for a template profile once its role has a form. Paths it names must exist; its role is never Release.
- **Shared contract (W01 handoff, W03-D05).** `stage` becomes `candidate`, `approved` or `adopted`, and local extensions apply in all three, as they do today in the two existing stages. The record gains `approved_by`, `approved_at`, `scope`, `effective_from`, `migration`, `rollback` and `consumer_version`; approval fields are required for `approved` and `adopted` and may hold `unverified` only with an `approval_ref`. Extensions become objects with `name`, `condition`, `owner`, `verification`, `review` and `removal`, and every consumer reads names through one accessor (`document_contracts.py` lifecycle-domain checks and record parsing, `document_lifecycle.py` first-record approval, `tests/test_task_acceptance_contract.py`). For WGOV-CORE 3.0.0: stage stays `adopted`; `approved_by`, `approved_at` and `effective_from` are `unverified`; each of the seven extensions keeps its name as `condition` and holds `unverified` for owner, verification, review and removal, since no record states them.
- **Heading-tree checks (QA-C02).** For a profile with a form: each H3 is a child, or a registered `local_h3` extension, of the H2 above it (`BODY-H3-PARENT`, `BODY-H3-UNSUPPORTED`); siblings are unique and ordered (`BODY-H3-DUPLICATE`, `BODY-H3-ORDER`); a missing required H3 under a present H2 fails (`BODY-H3-REQUIRED`) and a missing conditional H3 passes; a section that is empty or only `N/A` fails `BODY-SECTION-EMPTY` unless `omit_when_condition_false` applies, while `N/A` with a reason passes and a `link_only` section with links passes; headings in fenced code, HTML comments or quotes are not headings; a `retained_form` extension whose statuses include the document's status applies its retained H2 lists instead.
- **Policy sentence.** `document-authoring.md` no longer says the `approved` stage and approval fields are absent; it says they exist and that unrecorded facts are `unverified`.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md), amended by ADR-0059). Forms are keyed by document role, so two profiles bound to one role share one form. The phase-1 form model is checked against temporary registries in tests; the repository registry carries no form until phase 2.

## Data Modeling & Storage Strategy

New registry keys only: `common_forms` (no forms in this phase), `document_role`, `template_definition`, and the shared-contract fields. No new file outside `tests/` and ADR-0059, no ledger.

## Interfaces & Data Structures

- `scripts/document_authority.py`: optional profile and top-level keys.
- `scripts/document_contracts.py`: frozen `FormSection`, `FormExtension`, `CommonForm`; `DocumentProfile.document_role` and `.form`; registry checks for parent nesting, levels, sibling order and uniqueness, conditional conditions, extension parents and legacy lists beside a form; `SharedContract` stage, fields and an extension-name accessor.
- `scripts/validate-markdown-profiles.py`: heading bodies with fence flags in `HeadingScan`; a form-tree diagnostic function called from the body diagnostics with the document status.
- `scripts/validate-document-contract-registry.py`: template parity includes role and form.
- Handoffs are recorded in the Task with owner and resume condition.

## Edge Cases & Error Handling

- Setext headings stay unrecognized, as today.
- An unknown `document_role` fails the schema; a `form_id` not in the 16 role IDs fails the schema.
- A comparison-base registry without the new optional keys is read unchanged, as for the earlier optional keys; no generation branch is added.

## Failure Modes & Fallback / Human Escalation

If any current document gains a diagnostic, the change is wrong for phase 1 and is fixed before commit; no current document is edited to pass. If the operator does not accept ADR-0059, the implementation is not committed.

## Verification Commands

- Before and after, record the diagnostic counts of the four strict document validators over the whole tree; after must equal before.
- `python3 scripts/run-contract-tests.py --root . --suite document` (with the new module) and `--suite agent-governance`.
- `python3 scripts/validate-document-contract-registry.py --root . --mode strict`, `validate-markdown-profiles.py`, `validate-links-and-owners.py` and `validate-document-lifecycle.py` in strict mode, and `validate-document-lifecycle.py --root . --mode staged` before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-FORMMODEL-001 | The authority guard, schema and registry accept `common_forms`, `document_role`, `template_definition` and the shared-contract fields; registry negatives (bad parent, duplicate order, conditional with `always`, legacy lists beside a form, differing Policy roles, twin parity, `approved` without approval facts, `unverified` without `approval_ref`, extension without owner, forbidden agent field) fail in tests; every extension consumer reads names through the accessor. |
| VAL-FORMMODEL-002 | The heading-tree checks pass their positive cases and fail their negative cases (wrong parent, unknown H3, duplicate and reordered siblings, missing required, empty and bare `N/A`, link-only section, fenced fake heading, extension placement, ADR retained form by status) in isolated temporary registries. |
| VAL-FORMMODEL-003 | Diagnostic counts over the current tree are unchanged; the Policy binding, WGOV-CORE fields and the policy sentence are in place; ADR-0059 is accepted by the operator; the handoffs carry owner and resume condition; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FORMMODEL-001 | [ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md), [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry schema and negative tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FORMMODEL-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Heading-tree positive and negative tests. |
| [REQ-0003-FR-0032](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FORMMODEL-003 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Diagnostic-count comparison; exact-index QA. |
