---
title: "W03 Full TemplateDefinition Record Plan"
version: "1.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-11-14"
artifact_id: "SPEC-0196-PLAN-0001"
parent_ids: ["SPEC-0196"]
---

# W03 Full TemplateDefinition Record Implementation Plan

## Global Constraints

This approved work order follows the [approved Spec](spec.md) and inherits all of its boundaries. It adds four constraints: no form, profile heading list, template or governed document body changes; no test or script reads `_workspace/`; the diagnostics of the four strict document validators over the tree are equal before and after; and nothing is removed before its replacement refusal is in place and consumer-zero is shown. The five design choices follow W03-D56.

## Overview

Add the schema copy and the stored `contract_version`, write the function that derives the 19-field record and the registry rule that validates it for every template, test it over every template, retire the heading-line table path that no real template uses, update the policy texts, and close W03-H15 and W03-H28. [Task 0001](tasks/tsk-0001-w03-full-template-definition.md) owns execution and evidence.

## Context

A read of `main` at `de64c58d` (after SPEC-0186) found 87 profiles, 39 of them templates and 33 with a `template_definition` of the same ten keys; the six without one are the SDLC templates of W03-H13. Every template with a definition names one source profile, the key lists of template and source are equal, and all 22 `frontmatter_keys` entries name at least one consumer; 14 of them have an empty condition. The 18 forms carry one shared `language_rule` and ten `local_h3` extensions. A prototype of the derivation, run in a scratch folder against the package schema (SHA-256 beginning `e490cf40`), produced 33 records and nine findings, all `minItems` on `headings` for the templates whose role had no form: three `provider-native`, three governance and three reference templates. Nine tables in the three reference templates were the only tables named by a heading line. The registry `schema_version` 10 dates from 2026-10-05, and `template_definition` and `frontmatter_keys` were added later without changing it. The `stage99-machine-contracts` route already covers any JSON file under `docs/99.templates/contracts/`, and the commit hooks check JSON without reformatting it.

The expected landed state differs: SPEC-0187 deletes the governance contract template, SPEC-0188 and SPEC-0189 give five templates a form and move the nine tables to section ids, SPEC-0191 adds the work residue ledger, SPEC-0193 adds `relationship_contract` with the `policy-authority`, `consumer-impact` and `verification-evidence` relations that the derived `relationships` field reads, SPEC-0207 changes `schema_version` to a SemVer string right after SPEC-0191 (W03-D66), and SPEC-0195 adds the Requirement form and definition. Every count is read again from the landed registry before the tests are written.

## Goals & In-Scope

- Schema copy with its pinned digest; `contract_version` in the profile schema and in every definition.
- `template_definition_record`, `REGISTRY_TEMPLATE_RECORD`, `REGISTRY_TEMPLATE_EXTENSION` with the extension record of the three `provider-native` definitions, and the record and negative tests.
- The replacement refusal for a table on a role without a form; removal of the heading-line rule, branch, helpers, synthetic tests and wording.
- Policy texts; the W03-D56 row, evidence rows and the closure of W03-H15 and W03-H28 in the SPEC-0161 Task with their ledger entries.

## Non-Goals & Out-of-Scope

- Any form, profile heading list, template or document body; the SDLC templates without a definition; the H2-list model; a form for `provider-native`; the cross-repository comparison and any canonical hash; a print command or a tracked output file (W03-D56).

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-TDREC-001](spec.md#success-criteria--verification-plan) | Schema copy and digest pin; `contract_version` in the profile schema and the definitions; the `headings_extension` record of the three `provider-native` definitions; the function; `REGISTRY_TEMPLATE_RECORD` and `REGISTRY_TEMPLATE_EXTENSION`; record and negative tests. | Approved Spec and Plan; SPEC-0188 to SPEC-0195 landed; W03-D65 recorded by SPEC-0193. | [Task 0001](tasks/tsk-0001-w03-full-template-definition.md) | Failing tests first, then passing; strict registry check; the schema digest. |
| WORK-002 | [VAL-TDREC-002](spec.md#success-criteria--verification-plan) | Consumer-zero list; replacement refusal; removal of the heading-line rule, branch, helpers, tests and wording. | WORK-001. | [Task 0001](tasks/tsk-0001-w03-full-template-definition.md) | Empty consumer list; refusal test failing first; search for the removed names. |
| WORK-003 | [VAL-TDREC-003](spec.md#success-criteria--verification-plan) | Policy texts; the W03-D56 row; closure of W03-H15 and W03-H28 with the ledger; regression and exact-index QA. | WORK-002. | [Task 0001](tasks/tsk-0001-w03-full-template-definition.md) | Strict validators, suites, ledger gate, quality gate, markdownlint, ruff, staged QA and hooks. |

## Verification Plan

- Read the landed registry and record the counts of templates, definitions, forms and form-less roles; record the output of the four strict document validators before any change.
- Copy the package schema, compare its SHA-256 with the package file once by hand, and pin that digest in the test; the Task records the package revision and both digests.
- Show each record and negative test failing before its change and passing after it.
- Before any removal, list the `tables[].section` values that start with `#` and stop if the list is not empty; land the replacement refusal with its failing-first test; then remove the rule, branch, helpers, tests and wording, and record in the Task that `BODY-TABLE-SECTION` and `_TABLE_HEADING_LINE` no longer occur under `scripts/` and `tests/` and which commit recovers them.
- Record in the Task the SHA-256 of all derived records serialized by `json.dumps` with sorted keys, named as that serialization and not as RFC 8785; it is evidence of what was validated, not a tracked artifact and not a cross-repository claim.
- Commit order, four steps: (1) the baseline of the Task review digests alone; (2) the package commit with this package's entry in `docs/03.specs/README.md` and the W03-D56 row; (3) the move of any shifted registry baseline line alone; (4) the implementation with the Task evidence. Run the Spec's Verification Commands, the staged lifecycle check before each commit and `graphify update .` after the code change.
- Stop rule: a schema finding other than the tolerated one (and the tolerated one without a complete extension record), a remaining heading-line consumer or a changed validator diagnostic stops the work as the Spec states; after two failed attempts with no new information the author reports a repository defect.
- Architecture compliance: AD-0006, ADR-0033 and ADR-0059 unchanged.
- Apply the expected MAJOR bump of the Spec to the registry `schema_version`, the schema `const`, `REGISTRY_MAJOR`, `READABLE_REGISTRY_MAJORS`, the guard constant and the readable set of `registry_at` at the implementation commit, and record the level and the reason in the Task (SPEC-0207, W03-D66).
- Record the risk class (`medium`: the registry, two schemas, the contracts module, the profile validator and tests; no permission, trigger, hook or workflow) and the core-diff checklist.

## Risks & Mitigations

Risks use the risk-report scale (likelihood Likely, Possible or Unlikely; impact Severe, Moderate or Minor), rated from the pre-approval read and prototype.

- **A local role is labelled with the common contract version.** Possible, Moderate: MEDIUM, monitor. Owner: W03 author. No registry data marks a form as local today, so the stored value rests on review; the test pins the role sets and the check refuses two values on one role. Review cue: the core-diff checklist over the definitions. Signal that raises it: a `COMMON-DOC-FORM-1` value on a role of W03-D20. Rollback: correct the value.
- **The counts and shapes differ in the landed state.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. Eight packages land first and the read is from `de64c58d`. Review cue: the first step of the Verification Plan. Signal that raises it: a count that differs from the Context paragraph without a landed package explaining it. Rollback: none needed.
- **The registry edit shifts reviewed baseline lines.** Likely, Minor: MEDIUM, monitor. Owner: W03 author. One line per definition is added; step 3 of the commit order moves the lines alone. Review cue: the secrets hook. Signal that raises it: a baseline finding on an unchanged secret. Rollback: revert step 3.
- **A real consumer of the heading-line path remains.** Unlikely, Moderate: LOW, monitor. Owner: W05 code. It needs a package that lands differently from its approved Spec; the consumer-zero list runs before any removal. Review cue: that list. Signal that raises it: any `#` section. Rollback: revert the removal commit.
- **The schema copy drifts from the package.** Possible, Minor: LOW, monitor. Owner: W03 author. The package may be revised; the pinned digest makes any change deliberate and the Task names the revision. Review cue: the next package revision. Signal that raises it: a package schema digest other than the pinned one. Rollback: restore the file.
- **The extension record is bypassed or decays.** Possible, Minor: LOW, monitor. Owner: W05 code. `REGISTRY_TEMPLATE_EXTENSION` makes the tolerated finding depend on a complete five-field `headings_extension`, and its negative tests cover a missing record, an empty or non-text field and a record on a role with a form. The record names its review and removal criteria, so it is not a permanent exception (REQ:37). Review cue: the extension's `review` trigger at each `STAGE99-LOCAL-FORM-1` version change. Signal that raises it: a native format change without a review. Rollback: remove the record and the tolerance together.
- **The tolerated finding hides an empty form.** Unlikely, Minor: LOW, monitor. Owner: W05 code. The tolerance applies only to a role with no form in `common_forms`, and a negative test shows an empty `headings` on a role with a form failing. Review cue: that test. Signal that raises it: a role with a form and no section. Rollback: remove the tolerance.

Not scored, because no evidence rates it: whether W11 needs a field of the record in another shape for the comparison across repositories. It stays an open point of W03-H09 and W03-H22.

## Completion Criteria

All three criteria need PASS evidence, no unresolved required failure and the operator's acceptance.

## Promotion

| Durable contract | Promoted to | Where |
| --- | --- | --- |
| Stored and derived fields of the TemplateDefinition record | [Document authoring policy](../../../.agents/governance/document-authoring.md) | TemplateDefinition sentences; `template_definition` in `docs/99.templates/contracts/document-profile.schema.json` |
| A role without a form records no table | [Document authoring policy](../../../.agents/governance/document-authoring.md) | Forms paragraph; `REGISTRY_TABLE_SECTION` in `scripts/document_contracts.py` |
