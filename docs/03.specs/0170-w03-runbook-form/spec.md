---
title: "W03 Runbook Form"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-12"
layer: "specs"
artifact_id: "SPEC-0170"
---

# W03 Runbook Form Technical Specification (Spec)

## Overview

This approved change contract is the second phase-2 package of the W03 stage of the external v14.7 execution package. It gives the Runbook role its COMMON-DOC-FORM-1 1.0.0 form in the Stage 99 registry, with its TemplateDefinition and table contract, and moves the runbook template and the ten current runbooks to the form without changing their meaning. It reuses the model and checks that SPEC-0169 added for Guide (recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)): heading lists derived from the form, the TemplateDefinition `tables` contract and the `BODY-TABLE-COLUMNS` and `BODY-TABLE-ROWS` checks. The user's decisions W03-D01, W03-D03, W03-D04, W03-D08 and W03-D11 are recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md); W03-D13, the user's decision of 2026-11-12 on non-rollback recovery, is recorded in this package's Task and added to that table by this package's first commit. The [Task](tasks/tsk-0001-w03-runbook-form.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03): `docs/99.templates/registry.json`, `docs/99.templates/templates/operations/runbook.template.md`, the ten runbooks `docs/05.operations/runbooks/0001`, `0002`, `0003`, `0004`, `0007`, `0008`, `0009`, `0010`, `0011` and `0012`, `tests/test_common_form_tree.py`, the W03-D13 row of the SPEC-0161 Task, the Guide, Policy and Runbook paragraph of `.agents/governance/document-authoring.md`, the Operations forms entry of `docs/99.templates/README.md`, the section names in `.agents/skills/ops-runbook/SKILL.md` (Workflow Steps 2 to 6 and the sentence after them) and in `docs/05.operations/runbooks/README.md` Usage Instructions steps 2 and 3, which already name headings no runbook has (`When to Use`, `Procedure or Checklist`, `Verification Steps`, `Observability and Evidence Sources`) and become the form's section names, each with its frontmatter `version` and `updated` where it has frontmatter; this package, the Stage 03 README and reviewed `.secrets.baseline` entries. No code change is expected: the SPEC-0169 model already covers a second form; if a check needs code, the author stops and reports.
- Not in this package: every other role, which keeps its H2 lists; the `SKILL.md` form itself (a later package); README rule IDs; phase 3.
- Form-only migration (W03-D01): no sentence of a runbook changes meaning, no fact, command or approval is added, and command boundary markers stay with their commands. Where the form asks for content a runbook does not hold, the section states that none exists and why (`explain_none_or_not_applicable`); every such line is written in Korean, as `document_language` requires for `operation/runbook`, and listed in the Task for the user's review.
- No push, PR or merge without separate approval. Open question: none.

## Contracts

- **Runbook form.** `common_forms.forms` gains the Runbook form exactly as COMMON-DOC-FORM-1 1.0.0 defines it (`roles[7]`): `form_id` `runbook`, `title` `Runbook`, its `h1`, `language_rule` and `extension_policy`, and five required H2 sections in order: Purpose (Trigger and Outcome, Scope), Preconditions (Authority and Access, Safety Checks), Steps (Actions, Stop Conditions), Validation (Service Checks, Evidence), Recovery (Rollback, conditional; Escalation). Each section keeps the contract's fields; `link_only` is false everywhere. The template keeps its H1 `# [Topic Name] Runbook`.
- **Recovery Procedures extension (W03-D13).** One `local_h3` extension, `runbook-recovery-procedures`, titled `Recovery Procedures` under `runbook-recovery`, placed before `Rollback` in documents by convention (no check enforces its position): condition "a runbook holds recovery or remediation procedures that are not an undo of its steps"; owner `platform`; verification "the form tree check"; review "when the Runbook form version changes"; removal "when the common Runbook form gains an H3 for non-rollback recovery". It is conditional: a runbook without such procedures omits it, and a present but empty one fails `BODY-SECTION-EMPTY`.
- **Lifecycle Traceability extension (W03-D03, W03-D04).** One `local_h3` extension, `runbook-lifecycle-traceability`, titled `Lifecycle Traceability` under `runbook-validation`: condition "a runbook in a status the body contract enforces (draft, in-review, active, deprecated) states its promoted owner or an N/A reason"; owner `platform`; verification "the body-contract check"; review "when the Runbook form version changes"; removal "when runbook lineage has another registered owner".
- **Profiles.** `operation/runbook` and `common/template-operation-runbook` carry empty H2 lists and drop `substantive_body` and `ordered`. Their `body_contract.section` becomes `Validation`; table heading, columns and source rules stay. Their heading lists are derived from the form (SPEC-0169).
- **Table contract (W03-D08).** The runbook TemplateDefinition `tables`: `Triggers` in `runbook-steps-actions` with keys `Trigger`, `Action`, `Rollback` (the contract's conditional trigger/action/rollback), `minimum_rows` 0, row identity `Trigger`; `Lifecycle Traceability` in `runbook-lifecycle-traceability` with keys `Promoted owner`, `Trigger or control`, `Evidence or recovery owner`, `minimum_rows` 1, row identity `Promoted owner`.
- **Template step table.** The current template's `Step | Action | Expected result | Stop / escalate when` table conflicts with W03-D08, which names trigger/action/rollback for this role; per SPEC-0161 EVD-018 the current requirement prevails. The template replaces it with an optional `Trigger | Action | Rollback` table; its expected-result and stop meanings move to the Validation and Stop Conditions prompts. Runbook 0012 keeps its existing four-column table unchanged as form-only content; its first header is `Step`, so the table check does not identify it.
- **TemplateDefinition.** The runbook template profile carries its definition: purpose, responsibility, non-goals, policy references (`document-authoring.md`, `sdlc.md`, `approval-and-safety.md`), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, every real consumer path (registry, schema, template, Stage 99 README, the ten runbooks, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py`, `tests/test_common_form_tree.py`, the ops-runbook skill), validation cases, migration and `tables`.
- **Template.** Five H2 and twelve H3 headings (the ten form H3, with Rollback conditional, plus the two local extensions `Recovery Procedures`, marked optional in its prompt, and `Lifecycle Traceability`), a Korean author prompt per H3 drawn from its `required_content` (keeping the current prompts' meanings: executor and safe end state, stop conditions, escalation boundary, evidence location, roll-forward recovery), the optional Triggers table under Actions, and `Lifecycle Traceability` with its table under Validation.
- **Runbook meaning map (W03-D11).** For each runbook:
  - Purpose: goal, outcome and failure-cause sentences go to Trigger and Outcome; system, environment and impact-range sentences go to Scope; executor, type and authority-boundary sentences (for example 0012's Type, Executor and Boundary lines) go to Preconditions > Authority and Access.
  - Trigger and Preconditions: trigger sentences go to Purpose > Trigger and Outcome; owner, approval, permission and environment items to Preconditions > Authority and Access; backup, availability, concurrency and secret-protection items to Safety Checks; its own H3 headings become H4 where they land.
  - Procedure: content goes to Steps > Actions; sentences that are only stop or additional-approval conditions go to Stop Conditions.
  - Heading levels: every moved H3 keeps its relative order and becomes H4, or H5 under the H4 that was its logical parent (a `Procedure N` heading for its `N-M.` sub-steps and other subsections such as 0009's external Prometheus query subsection and 0004's k8s router path check; a `Troubleshooting` heading for 0007's three question headings). No level is skipped. The Task states the choice per runbook.
  - Troubleshooting blocks stay with their source H2's mapped H3 as H4 (0007 `Troubleshooting` under Actions, 0001 `Troubleshooting Matrix` under Service Checks); those already under Recovery and Escalation go to Recovery Procedures. A block is not moved between H2s.
  - Verification: content goes to Validation > Service Checks, with its H3 headings as H4; sentences that name observed evidence, its location or remaining limits go to Evidence.
  - Recovery and Escalation: recovery, remediation and troubleshooting procedures go to Recovery Procedures with their H3 headings as H4 (0001, 0002, 0003, 0004 and 0010 have them); rollback and undo content goes to Rollback (omitted when a runbook has none); escalation owners and hand-off go to Escalation; introductory recovery sentences stay as `## Recovery` body.
  - Related Documents leaves, and each link moves inline by its DOC-07 type: ADR, policy, decision and control-surface links such as the main-protection ruleset and `.github/workflows/ci.yml` (normative) to Preconditions > Authority and Access; evidence links to Validation > Evidence; architecture, index, companion-runbook and code or configuration reference links such as `CHANGELOG.md`, `scripts/release.py` and service directories (navigation) to Purpose > Scope; a link already inline is not repeated.
  - Pointers: runbook 0010's intra-document link `[Recovery and Escalation](#recovery-and-escalation)` is retargeted to the heading that now holds that content; textual section pointers that name a renamed section (0007 "RUN-0002 Procedure step 4" and the Korean pointer in 0002 to Procedure step 4) are renamed to the new section names only. These are form-only pointer edits listed in the Task. `docs/01.requirements/0003-workspace-agent-governance-platform.md` Archived Lineage rows that name old runbook sections are history and stay.
  - Lifecycle Traceability moves under Validation unchanged.
  - No Requirement or Spec link exists in any runbook, so the lineage owner read from the body-contract section is unchanged.
- **Policy and skill text.** `document-authoring.md` and `docs/99.templates/README.md` say Guide and Runbook use their registry forms, Runbook with Lifecycle Traceability under Validation; Policy keeps Related Documents until its package. `ops-runbook` names the new sections: Preconditions, Steps > Actions with the stop conditions, Validation, Recovery with Rollback and Escalation, and links placed inline by type instead of a Related Documents list.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes.

## Data Modeling & Storage Strategy

Registry data only: one form, two extensions, one TemplateDefinition with two tables, and the two runbook profiles' lists and body-contract section.

## Interfaces & Data Structures

- No script interface changes. `scripts/validation/repository/quality.py` (command boundary markers under `docs/05.operations/runbooks`) and `form_contracts.py` read the moved documents and the derived lists unchanged.
- `tests/test_common_form_tree.py`: `test_repository_registry_binds_clear_roles_and_carries_only_the_guide_form`, `test_repository_registry_loads_with_only_the_guide_form` and `CurrentRegistryUnchangedTests` are rewritten to name exactly the Guide and Runbook forms and definitions (runbook tables `Triggers` and `Lifecycle Traceability`, copied to the source profile) and no other profile with a form; synthetic positive and negative cases cover the Triggers table and the Recovery Procedures extension, since no current runbook has a Triggers table.

## Edge Cases & Error Handling

- A runbook without rollback content omits `### Rollback` (conditional); a present but empty Rollback fails `BODY-SECTION-EMPTY`.
- H4 and H5 headings are not checked by the tree. No link from another file targets an anchor inside a runbook; the one intra-document anchor (0010) is retargeted, because the link validator skips anchors and markdownlint MD051 is disabled.
- No heading level is skipped, so markdownlint MD001 passes; `Recovery Procedures` is a registered local H3, so the tree check accepts it.

## Failure Modes & Fallback / Human Escalation

If any document other than the ten runbooks and the template gains a diagnostic, the change is wrong and is fixed before commit. If a runbook sentence cannot be placed without changing its meaning, or a command boundary marker would separate from its command, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators over the whole tree; after must equal before.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle` and `--suite agent-governance`.
- `python3 scripts/validation/repository/quality.py --root .`; `markdownlint-cli2 --config .markdownlint-cli2.yaml` over the template and the ten runbooks; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-RUNBOOKFORM-001 | The registry holds the Runbook form, its two extensions, its TemplateDefinition and tables, and the runbook profiles carry no H2 lists; their derived heading lists equal the form's H2 titles; the repository-registry tests name exactly the Guide and Runbook forms. |
| VAL-RUNBOOKFORM-002 | The runbook template and all ten runbooks pass the tree, table, body-contract, author-prompt, residue, command-boundary and markdownlint checks; the per-runbook meaning map with every added none-with-reason line is recorded in the Task; the policy and skill texts are updated; validator output over the rest of the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RUNBOOKFORM-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry tests and strict registry check. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RUNBOOKFORM-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
