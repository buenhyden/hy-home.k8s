---
title: "W03 Service README Form"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0174"
---

# W03 Service README Form Technical Specification (Spec)

## Overview

This approved change contract is the sixth phase-2 package of the W03 stage of the external v14.7 execution package and the third of the README packages. It gives the Service README role its COMMON-DOC-FORM-1 1.0.0 form in the Stage 99 registry and moves 21 documents and two templates to the form without changing meaning: the 20 READMEs of `common/readme-implementation` and `.github/repository-surface.md` (`common/readme-runtime-governance`). The 20 READMEs are the 16 code and configuration READMEs that W03-D10 binds to this role and the four agent and provider READMEs (`.agents/`, `.claude/`, `.codex/`, `.agents/evaluations/`), which W03-D16 deferred; on 2026-11-13 the user answered "Service README (Recommended)" to their binding question, so they move with the others and W03-D10 is amended for them (W03-D17). It reuses the model of SPEC-0169 to SPEC-0173 (derived heading lists, TemplateDefinition `tables`, table checks, navigation in a form H3, the H4 document-content reader; recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). The user's decisions W03-D01, W03-D08, W03-D10, W03-D11 and W03-D16 are recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md); W03-D17 is recorded in this package's Task and added to that table by this package's first commit. The [Task](tasks/tsk-0001-w03-service-readme-form.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json`; the two templates `docs/99.templates/templates/common/readme-implementation.template.md` and `readme-runtime-governance.template.md`; the 21 documents named above; `tests/test_common_form_tree.py`, `tests/test_readme_navigation.py`, `tests/test_repository_quality_rules.py` and any test that pins these profiles' H2 lists or navigation section; the forms sentence of `.agents/governance/document-authoring.md` and the Common forms bullet of `docs/99.templates/README.md`; the W03-D17 row, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only); each edited document with its frontmatter `version` and `updated`; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: the Workspace README and Reference Pack README roles, which keep their H2 lists; `AGENTS.md`, `SKILL.md` and Policy; the retirement of the list-mode `README_H2_*` rule IDs, which stay for the remaining list profiles; phase 3.
- Form-only migration (W03-D01): no sentence changes meaning, no fact is added, every command and link target stays; where an H3 has no source text, one Korean none-with-reason line states that none exists, listed in the Task for the user. No push, PR or merge without separate approval. Open question: none.

## Contracts

- **Service README form.** `common_forms.forms` gains the Service README form exactly as COMMON-DOC-FORM-1 1.0.0 defines it (`roles[13]`): `form_id` `service-readme`, `title` `Service README`, Purpose (Service Role, Supported Environment), Interfaces (Inputs and Outputs, Security Boundary), Development (Local Workflow, Checks), Operations (Runbook Links, Observability and Recovery), every section required, `link_only` false everywhere as in the other forms. No extension. All 21 documents are `router` profiles, for which the tree check reports no `BODY-SECTION-EMPTY`; none-with-reason lines in them are therefore enforced by review and the Task list, not by the validator. Templates keep their H1.
- **Profiles and binding (W03-D10, W03-D17).** `common/readme-implementation`, `common/readme-runtime-governance` and their two template twins gain `document_role` `service-readme`. No path pattern changes. The four profiles carry empty H2 lists; heading lists are derived from the form.
- **Navigation.** The `readme_navigation` section for `common/readme-implementation` becomes `Service Role`, a required H3 unique in the form; `complete` stays `false`. `common/readme-runtime-governance` has no navigation entry and gains none.
- **Table (W03-D08).** COMMON-ROLE-FORMS names the Service README's conditional table as command/output. Both template TemplateDefinitions carry `Commands` in `service-readme-development-checks` with keys `Command` and `Output` (both required), `minimum_rows` 0, row identity `Command`. No current table in the 21 documents starts with a `Command` header, so the table checks find nothing to refuse.
- **Document-content tables.** `scripts/validation/document_content.py` reads fourteen matrices of `gitops/`, `gitops/platform/`, `gitops/workloads/`, `infrastructure/`, `infrastructure/verify/`, `examples/` and `.github/repository-surface.md` by title; SPEC-0173 made that reader accept H4, so the matrices that move from H3 to H4 stay checked with no code change. The owner-reference check of `.github/repository-surface.md` reads the whole text and is unaffected.
- **TemplateDefinitions.** Each of the two template profiles carries purpose, responsibility, non-goals, policy references (`document-authoring.md`, `sdlc.md`), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, every real consumer path for its profile (registry, schema, its template, its documents, Stage 99 README, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`, `scripts/validation/document_content.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py` and the tests), validation cases, migration and `tables`.
- **Meaning map, applied per document.** It is derived from the form's section `content` text (Service Role: service responsibility and owner; Supported Environment: actual environment and support range; Interfaces: the external contract; Development: the development flow; Operations: operational links). The old H2 headings `Overview`, `Scope`, `Structure`, `Usage`, `Verification` and `Related Documents` are removed and their body text moves under the form H3 named below; every old H3 becomes an H4 and every old H4 an H5 under its form H3, keeping relative order, so no level is skipped. A rule that names a heading wins over the rule for its old H2, and a paragraph is never split.
  - Purpose > Service Role: Overview prose, the lead blockquote, `Audience` and `Current authority transfer`; the Structure H2 body and its H3s (the tree, member lists, `Content Mapping`, the `scripts/` owner groups, the examples list heading, and ownership or coverage matrices such as `Service Coverage Matrix`, `Namespace Ownership Matrix`, `Platform Coverage Matrix`, `Workload Coverage Matrix`, `Infrastructure Coverage Matrix` and `Example Role Matrix`). Navigation reads this section; no child-link listing is required (`complete` false).
  - Purpose > Supported Environment: the Scope H2 body and an Overview `Scope` H3 (In Scope and Out of Scope), and runtime prerequisites such as `Host Runtime Prerequisite Matrix` and the sample app's current platform prerequisites heading. A Scope paragraph that also forbids committing credentials or state stays whole here, and Security Boundary then states in one Korean line that the boundary is written under Supported Environment.
  - Interfaces > Inputs and Outputs: external contracts, boundaries and policy matrices such as `External Service Contract Matrix`, `Workload Image and Kind Policy Matrix`, `AppProject Allow-list Rationale Matrix`, `Platform Chart Render Review Matrix`, `Bootstrap Boundary Matrix`, `Configuration Boundary`, `Boundaries`, `Policy Routing`, `Workflow Roles` and `Workflow Responsibility Matrix`. Interfaces > Security Boundary: secret, credential and permission boundaries such as `Secret Management Responsibility Matrix`.
  - Development > Local Workflow: the Usage H2 body, `Working Procedure` wherever it sits (the one under `Operations` in `tests/README.md` becomes an H4 under Local Workflow, because its old parent `Operations` stays under Observability and Recovery), numbered procedure steps, the examples usage heading, and `Link Basis` and `Reference Links`, which sit under Usage today. Development > Checks: the Verification H2 body and its H3s (for example `Reproducing the local dependency identity`), `Validation`, `Validation Note`, and tables or lists that inventory validation scripts or tests (`Infrastructure Test Inventory`, and `Test families`, `Folder files`, `Shared helper modules` and `Fixture families` in `tests/README.md`), even under the old Structure H2.
  - Operations > Observability and Recovery: `Operations` under Usage, deferrals such as `Current Hardening Deferrals`, and bootstrap and recovery notes such as `Bootstrap Note`. Operations > Runbook Links: runbook and guide links.
  - Related Documents (W03-D11): this form registers no Related Documents section, so each link moves inline by its DOC-07 type with its list text unchanged: navigation and design links to Purpose > Service Role, normative policy and contract links to Interfaces > Inputs and Outputs, evidence and check links to Development > Checks, operations links to Operations > Runbook Links. `Source Basis` in `.github/repository-surface.md`, an H3 under Related Documents, becomes an H4 under Checks. The examples implementation-reference heading goes with Link Basis under Local Workflow.
  - The Task records each document's placements and added lines.
- **Policy text.** `document-authoring.md` adds the Service README to the roles that use their registry forms; the Common forms bullet of `docs/99.templates/README.md` says implementation, agent and provider, and runtime-governance READMEs use the Service README form and keeps the shared `Overview`, `Scope`, `Structure`, `Usage`, `Related Documents` core only for the workspace README.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form and README navigation ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes.

## Data Modeling & Storage Strategy

Registry data: one form, two TemplateDefinitions with one table each, four profiles' lists and role bindings, and one navigation section.

## Interfaces & Data Structures

- No validator code changes are expected; if a check needs one, it is named in the Task with its failing case first.
- `tests/test_readme_navigation.py`: the implementation profile's navigation fixture becomes `Service Role`, and the synthetic cases that feed `## Structure` for that profile feed `### Service Role`; a service-style README with child links under `Service Role` passes and a broken child link fails.
- `tests/test_common_form_tree.py`: `ROLE_BINDINGS` gains the two authored profiles (the template twins follow from `source_profile_ids`); `FORM_TEMPLATES` gains both templates; the six-form constant becomes seven forms and the per-form `tables` expectation gains `Commands`; the `link_only` assertion over repository forms stays unchanged; synthetic cases cover the `Commands` table.
- `tests/test_repository_quality_rules.py`: the `Example Role Matrix` mutation matches the heading at H2 to H4, shown failing first against the moved document.

## Edge Cases & Error Handling

- A router README is not checked for empty sections; review and the Task list carry the none-with-reason lines.
- A README with no security, runbook or recovery content states so in one Korean line in that H3.

## Failure Modes & Fallback / Human Escalation

If any document outside the 21 and the two templates gains a diagnostic, the change is wrong and is fixed before commit. If a sentence cannot be placed without changing its meaning, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators over the whole tree; after must equal before.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance` and `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-SERVICEREADME-001 | The registry holds the Service README form, its TemplateDefinitions and tables, the four role bindings and the `Service Role` navigation section; the four profiles carry no H2 lists; tests fail first and then pass. |
| VAL-SERVICEREADME-002 | The 21 documents and two templates pass the tree, navigation, document-content, author-prompt, residue and markdownlint checks; each document's map and added lines are recorded in the Task; the policy texts are updated; validator output over the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SERVICEREADME-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry and navigation tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SERVICEREADME-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
