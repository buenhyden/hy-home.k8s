---
title: "W03 Policy Form"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0175"
---

# W03 Policy Form Technical Specification (Spec)

## Overview

This approved change contract is the seventh phase-2 package of the W03 stage of the external v14.7 execution package. It gives the Policy role its COMMON-DOC-FORM-1 1.0.0 form in the Stage 99 registry and moves 14 documents and two templates to the form without changing meaning: the nine `governance/rule` documents under `.agents/governance/` and the five `operation/policy` documents under `docs/05.operations/policies/`, which SPEC-0168 bound to one `policy` role. It applies the user's decisions W03-D01, W03-D03, W03-D04, W03-D06, W03-D08 and W03-D11 recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md), resolves the Policy part of W03-H10, and reuses the model of SPEC-0169 to SPEC-0174 (derived heading lists, TemplateDefinition `tables`, table checks, registered local H3 extensions, the H4 document-content reader; recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). The [Task](tasks/tsk-0001-w03-policy-form.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json`; the templates `docs/99.templates/templates/governance/rule.template.md` and `docs/99.templates/templates/operations/policy.template.md`; the 14 documents named above; `scripts/document_contracts.py` (the template-twin table rule); `tests/test_common_form_tree.py` and any test that pins these profiles' H2 lists, body contract or tables; anchor-only link edits in `.agents/governance/sdlc.md`, `docs/05.operations/README.md` and `docs/05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`; the forms sentence of `.agents/governance/document-authoring.md` (itself one of the 14) and the Governance and Operations forms bullets of `docs/99.templates/README.md`; each edited document with its frontmatter `version` and `updated`; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: `AGENTS.md`, `SKILL.md` and workflows; the Workspace and Reference Pack README roles; the retirement of the list-mode rule IDs for the remaining list profiles; phase 3, including the Plan part of W03-H10.
- Form-only migration (W03-D01): no sentence changes meaning, no rule is invented, every command and link target file stays; where an H3 has no source text, one none-with-reason line in the document's language (Korean for `operation/policy`, English for `governance/rule`) states that none exists, listed in the Task for the user. No push, PR or merge without separate approval. Open question: none.

## Contracts

- **Policy form.** `common_forms.forms` gains the Policy form exactly as COMMON-DOC-FORM-1 1.0.0 defines it (`roles[8]`): `form_id` `policy`, `title` `Policy`, Purpose (Objective, Authority), Scope (Applies To, Exclusions), Rules (Requirements, Enforcement), Exceptions (Exception Conditions, Approval and Review), Ownership (Responsibilities, Change and Adoption), every section required, `link_only` false everywhere as in the other forms. Templates keep their H1.
- **Local extension (W03-D03, W03-D04).** One registered conditional local H3 `Lifecycle Traceability` under Ownership, after Change and Adoption (`policy-lifecycle-traceability`, parent `policy-ownership`), with owner, verification (the body-contract check), review (when the Policy form version changes) and removal (when policy lineage has another registered owner) recorded on the extension as for the Runbook and Guide extensions.
- **Profiles and binding.** `governance/rule`, `operation/policy` and their template twins keep `document_role` `policy`; `REGISTRY_POLICY_ROLE` stays strict. No path pattern changes. The four profiles carry empty H2 lists, and the `substantive_body` and `ordered` list flags of `operation/policy` and its twin go with the lists, as for Guide and Runbook; heading lists are derived from the form. The body contract of `operation/policy` and the copy on its template twin `common/template-operation-policy` both read `Lifecycle Traceability` under `Ownership` instead of `Related Documents`; columns and enforced statuses do not change. `governance/rule` keeps no body contract.
- **Tables (W03-D08).** COMMON-ROLE-FORMS names the Policy conditional table as rule/condition/evidence. Both template TemplateDefinitions carry `Rules` in `policy-rules-requirements` with keys `Rule`, `Condition` and `Evidence` (all required), `minimum_rows` 0, row identity `Rule`; the `operation/policy` twin also carries `Lifecycle Traceability` in `policy-lifecycle-traceability` with its current three columns, `minimum_rows` 1, row identity `Promoted owner`; the `governance/rule` twin carries `Rules` only. No current table in the 14 documents starts with a `Rule` header.
- **Template-twin tables (W03-H10).** A template's tables are inherited by each source profile it names, so two tabled twins naming one source would overwrite each other silently. The registry check refuses a source profile named by more than one template twin that carries tables (`REGISTRY_TABLE_TWIN`), with a failing case first. Policy has one twin per source profile, so it passes.
- **TemplateDefinitions.** Each of the two template profiles carries purpose, responsibility, non-goals, policy references (`document-authoring.md`, `sdlc.md`), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, every real consumer path for its profile (registry, schema, its template, its documents, Stage 99 README, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`, `scripts/validation/document_content.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py` and the tests), validation cases, migration and `tables`.
- **Meaning map (W03-D06), applied per document.** The old H2 headings are removed and their body moves under the form H3 named below; every old H3 becomes an H4 and every old H4 an H5 under its form H3, keeping relative order, so no level is skipped. Plain text precedes the H4s inside a form H3. A rule that names a heading wins over the rule for its old H2, and a paragraph is never split.
  - Purpose > Objective: `Overview` (governance) and `Purpose` (operations).
  - Purpose > Authority: `Authority Boundary`.
  - Scope > Applies To: `Governance Context` and the operations `Scope` body. Scope > Exclusions: a list item, paragraph or heading that the source itself marks as out of scope or excluded; otherwise a none-with-reason line.
  - Rules > Requirements: `Current Contract` and `Controls` with their H3s as H4. Rules > Enforcement: `Validation and Refresh` and `Verification and Review`.
  - Exceptions > Exception Conditions: the `Exceptions and Escalation` body; a whole paragraph or list in it only about who approves, reviews, escalates or revokes an exception goes to Exceptions > Approval and Review, and a paragraph that mixes conditions with approval stays whole in Exception Conditions. An H3 left without text gets a none-with-reason or pointer line.
  - Ownership > Responsibilities: an old H3 titled `Responsibilities` (operations policies 0001 and 0005 and the policy template) merges into this form H3 of the same title, its heading dropped, so its anchor keeps working. Ownership > Change and Adoption: a none-with-reason line unless the source names its own change or adoption rule as a heading. `Lifecycle Traceability` becomes the registered local H3 under Ownership.
  - Related Documents (W03-D11): each link moves inline by its DOC-07 type with its list text unchanged: normative to Purpose > Authority or Rules > Requirements, evidence to Rules > Enforcement, navigation to Scope > Applies To. Defaults by kind: ADR, architecture and peer-policy links to Authority; runbook links and implementation, manifest and validation-registry file links to Enforcement; Stage and Roles README links to Applies To; workflow, provider-note, agent-registry and document-profile-registry links to Authority; other `README.md` and archive-index links to Applies To; any other link to Applies To. A historical item that names a retired package goes, marked non-authoritative as in the source, beside the `Lifecycle Traceability` table under Ownership when that table exists, otherwise to Authority.
  - The HTML anchor `<a id="exceptions">` in POL-0001, with its two comment lines, is removed because the H2 `Exceptions` now provides that anchor.
  - The Task records each document's placements and added lines.
- **Anchor-only link edits.** Links that name a removed H2 anchor point to the new heading of the same content, with link text unchanged: `document-lifecycle.md#current-contract` (in `document-authoring.md` and `sdlc.md`) and `document-authoring.md#current-contract` (in `agent-execution.md`) become `#requirements`; `0001-k8s-gitops-operations-policy.md#exceptions-and-escalation` (in `docs/05.operations/README.md`, runbook 0004 and POL-0003, POL-0004, POL-0005 and POL-0007) becomes `#exceptions`: nine link sites in all. Anchors of old H3 headings keep working because their slugs do not change. The link validator checks no cross-file fragment, so the Task records a whole-tree search, outside `docs/98.archive/`, for fragments into the 14 documents before and after the move.
- **Policy text.** `document-authoring.md` adds the Policy to the roles that use their registry forms; the Governance and Operations forms bullets of `docs/99.templates/README.md` say governance rules and operations policies use the Policy form, and the Operations bullet's sentence that keeps `Lifecycle Traceability` under `Related Documents` until this package is rewritten to name `Ownership`.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes.

## Data Modeling & Storage Strategy

Registry data: one form with one local extension, two TemplateDefinitions with three tables, four profiles' lists, one body-contract section. Code: one registry diagnostic.

## Interfaces & Data Structures

- `scripts/document_contracts.py`: the registry check gains `REGISTRY_TABLE_TWIN`.
- `tests/test_common_form_tree.py`: the policy profiles gain their form in the registry tests, which name exactly eight forms; `FORM_TEMPLATES` gains both templates; the per-form loop gets two Policy rows, governance (no body section, `Rules` only) and operations (`Ownership`, `Rules` and `Lifecycle Traceability`); the pins that `operation/policy` has no form and no tables are rewritten, the latter with another untabled profile; synthetic cases cover the `Rules` table, the local H3 and `REGISTRY_TABLE_TWIN`; the `link_only` assertion over repository forms stays unchanged.

## Edge Cases & Error Handling

- A governance rule with no exception or ownership text under its own heading states so in one English line in each empty H3; where the document already mentions exceptions, escalation, review or change inside what becomes Requirements or Enforcement, the line points there instead of saying none, so it never contradicts the document. Each line is real prose, because these authored profiles are checked for empty sections.
- An operations policy in an enforced status keeps a `Lifecycle Traceability` table under Ownership.

## Failure Modes & Fallback / Human Escalation

If any document outside the 14, the two templates and the three anchor-only files gains a diagnostic, the change is wrong and is fixed before commit. If a sentence cannot be placed without changing its meaning, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators over the whole tree; after must equal before.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance` and `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.
- Before and after the move: `git grep -n -E '(agent-execution|approval-and-safety|context-and-memory|document-authoring|document-lifecycle|formatting-and-linting|git|model-selection|quality|0001-k8s-gitops-operations-policy|0003-service-mesh-cert-manager-policy|0004-rollouts-notifications-headlamp-policy|0005-observability-platform-operations-policy|0007-app-gitops-onboarding-policy)\.md#' -- ':!docs/98.archive'`; after the move every fragment names a heading or anchor that exists in its target.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-POLICY-001 | The registry holds the Policy form, its local extension, TemplateDefinitions and tables, and the moved body contract; the four profiles carry no H2 lists; `REGISTRY_TABLE_TWIN` refuses a doubly tabled source; tests fail first and then pass. |
| VAL-POLICY-002 | The 14 documents and two templates pass the tree, body-contract, language, link, author-prompt, residue and markdownlint checks; each document's map and added lines are recorded in the Task; the anchor edits and policy texts are made; validator output over the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-POLICY-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry and form tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-POLICY-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
