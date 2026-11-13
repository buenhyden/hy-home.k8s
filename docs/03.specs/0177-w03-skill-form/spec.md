---
title: "W03 Skill Form"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0177"
---

# W03 Skill Form Technical Specification (Spec)

## Overview

This approved change contract is the ninth phase-2 package of the W03 stage of the external v14.7 execution package. It gives the Skill role its COMMON-DOC-FORM-1 1.0.0 form in the Stage 99 registry and moves 19 documents and two templates form-only: the 17 native `SKILL.md` packages under `.agents/skills/` (`common/native-skill-package`, W03-D07) and the two common workflows under `.agents/workflows/` (`governance/skill`, W03-D10, with one registered local H3 `Authority Boundary`). Provider frontmatter, skill names, bundle files and loader paths stay unchanged (DOC-02, W03-D07); the body stays an invoked procedure, not a standing rule (DOC-03); native discovery is W07 evidence. It applies W03-D01, W03-D07, W03-D08, W03-D10 and W03-D11 recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md) and reuses the model of SPEC-0169 to SPEC-0176 (recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). The [Task](tasks/tsk-0001-w03-skill-form.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json`; the template `docs/99.templates/templates/governance/skill.template.md` and a new template `docs/99.templates/templates/common/native-skill.template.md`; the 19 documents named above; `scripts/validate-markdown-profiles.py` (the frontmatter quote exemption); `tests/test_common_form_tree.py`, `tests/test_native_skill_envelope.py`, `tests/test_common_agents_document_routes.py`, `tests/test_document_terminal_contract.py` and any test that pins these profiles' lists, roles or templates; in `.agents/governance/document-authoring.md` the forms sentence and the optional-table sentence, and in `docs/99.templates/README.md` the forms bullet and the two sentences that describe `governance/skill` and `common/native-skill-package` as form-less; each edited document's frontmatter `version` and `updated` (the `metadata` block of a `SKILL.md`); this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: skill reference files (`common/native-skill-reference`) and assets, which stay native without a role; `.claude/skills` links and provider projections; skill names, descriptions and invocation flags; the Workspace and Reference Pack README roles; phase 3.
- Form-only migration (W03-D01): no sentence changes meaning, no step, permission or command is added, every link and bundle reference stays reachable from `SKILL.md`; where an H3 has no source text, one English line states that none exists or points to the text that covers it, listed in the Task. No push, PR or merge without the user's approval, which is standing for this work (2026-11-13). Open question: none.

## Contracts

- **Skill form.** `common_forms.forms` gains the Skill form exactly as COMMON-DOC-FORM-1 1.0.0 defines it (`roles[15]`): `form_id` `skill`, `title` `Skill`, Purpose and Trigger (When to Use, When Not to Use), Procedure (Steps, Failure Handling), Inputs and Outputs (Inputs, Outputs), Verification (Checks, Completion and Handoff), every section required, `link_only` false everywhere.
- **Local extension (W03-D10).** One registered conditional local H3 `Authority Boundary` under Purpose and Trigger, after When Not to Use (`skill-authority-boundary`, parent `skill-purpose-and-trigger`), for a workflow that applies existing policy and states its own authority boundary, with owner, verification (the form tree check), review (when the Skill form version changes) and removal (when the common Skill form gains an authority H3) recorded as for the other extensions.
- **Profiles and binding.** `governance/skill`, `common/native-skill-package` and their template twins carry `document_role` `skill` and empty H2 lists. `common/template-governance-skill` keeps its route and frontmatter. A new twin `common/template-native-skill` (mode `template`, an exact route with escaped hyphens to the new template, source `common/native-skill-package`, frontmatter equal to its source so template parity holds, including the constant `disable-model-invocation: true`) carries the TemplateDefinition, and `common/native-skill-package` gains `template_source` naming the new template, as the AGENTS source did. The new template has the native frontmatter with `{{UPPER_SNAKE}}` placeholder values and an author prompt under each H3. No path pattern changes; `common/native-skill-reference` and `common/native-skill-asset` keep no role.
- **Table (W03-D08).** COMMON-ROLE-FORMS names the Skill conditional content as references with a step/input/output table. Both TemplateDefinitions carry `Steps` in `skill-procedure-steps` with keys `Step`, `Input` and `Output` (all required), `minimum_rows` 0, row identity `Step`. No current table in the 19 documents starts with a `Step` header.
- **TemplateDefinitions.** Each carries purpose, responsibility, non-goals, policy references (`document-authoring.md`, `agent-execution.md`), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, every real consumer path (registry, schema, its template, its documents, Stage 99 README, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-document-contract-registry.py`, `scripts/validate-agent-governance.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py` and the tests), validation cases, migration and `tables`.
- **Meaning map, applied per document.** Every old H2 heading is removed and its body moves under the form H3 named below. An H2 whose body goes plain under a form H3 shifts its H3 children to H4; an H2 that is kept as an H4 shifts its H3 and H4 children to H5 and H6, so `Workflow` in `incident-postmortem` and `Workflow Phases` in `workspace-harness-audit` keep their phases below them. Text between the frontmatter and the H1 (the authority sentence in every `SKILL.md`) stays where it is, unchanged. A heading that the text names (`Output Format` in `rca-methodology`, which its own text and `incident-postmortem` cite) is kept as an H4 under its form H3. Plain text precedes the H4s inside a form H3; headings inside fenced code are content, not headings, and stay unchanged; a paragraph or list is never split, so numbered steps keep their numbering. A rule that names a heading wins over the rule for its old H2.
  - `SKILL.md`: text between the H1 and the first H2, and `Purpose`, go to When to Use; `When NOT to Use` goes to When Not to Use, followed by `Boundaries`, `Constraints`, `Safety Rules` and `Workspace Boundary` as H4; `Workflow Steps`, `Workflow`, `Workflow Phases`, `Execution Mode`, `Modes by Task Scale`, `Branch and Promotion Model`, `Scoring`, `Severity Classification`, `Severity Assessment for Manifest Findings` and `Pattern Catalog` go to Steps as H4 (the first of them as plain text when it is the only content); `Failure Handling` and `Error Handling` go to Failure Handling; `Reference Material` and `Data Protocol` go to Inputs; `Outputs`, `Expected Outputs`, `Output Format`, `Audit Report Format` and `Review Output Format` go to Outputs; `Test Scenarios` goes to Checks; `Related Owners` and `Related Skills` go to Completion and Handoff.
  - Five `SKILL.md` files (`docs-stage-conformance`, `docs-stage-routing`, `execution-plan`, `requirements-to-design`, `task-breakdown`) have neither intro text nor `Purpose`; their When to Use line points to the frontmatter description.
  - Workflows (`governance/skill`, as W03-D06 maps the same old headings for Policy): `Overview` goes to When to Use; `Authority Boundary` becomes the registered local H3; `Governance Context` goes to Inputs; `Current Contract` goes to Steps with its H3s as H4, so the `#completion` anchor used by 17 role files keeps its slug; `Validation and Refresh` goes to Checks; Related Documents links move inline by kind, applying W03-D11 by analogy: policy, workflow and registry links to When to Use, check and evidence links to Checks, other links to Completion and Handoff. Every current link is a policy, workflow or registry link, so Completion and Handoff gets one line of plain prose, because `governance/skill` is authored and its empty-section check refuses a heading with no prose.
  - Every other form H3 gets one English line that points to the text that covers it or states that the document has none.
  - The Task records each document's placements and added lines.
- **Policy text.** `document-authoring.md` adds the Skill to the roles that use their registry forms and its optional `Steps` table to the optional-table sentence; `docs/99.templates/README.md` says in its forms bullet that workflows and native `SKILL.md` packages use the Skill form and reference files stay native, and corrects the sentences that call `governance/skill` a flat workflow type distinct from the native package and describe `common/native-skill-package` as form-less.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes. Provider loading reads each `SKILL.md` through its frontmatter and whole body, and the Claude gateway imports `work-lifecycle.md` whole, so heading changes do not change what is loaded.

## Data Modeling & Storage Strategy

Registry data: one form with one local extension, one new template profile, two TemplateDefinitions with one table each, four profiles' lists and role bindings.

## Interfaces & Data Structures

- `scripts/validate-markdown-profiles.py`: the `FM-QUOTE` exemption for an unquoted boolean frontmatter constant covers `template` profiles as well as `native` ones, so a template twin can carry its native source's `disable-model-invocation: true`; a regression near the existing frontmatter-quote cases in `tests/test_document_terminal_contract.py` fails first on a template twin with that constant and then passes, and still refuses a quoted `"true"` (`FM-VALUE-CONSTANT`) and an unquoted value that is not the constant.
- `tests/test_common_form_tree.py`: the nine-form constant, its comment and the tests named for it become ten forms; `ROLE_BINDINGS`, `FORM_PROFILES` and `FORM_TEMPLATES` gain the Skill profiles; the per-form loop gains two Skill rows, both carrying the form's one extension, each with `Steps` and no body section; the role tuple and the per-role `tables` dictionary gain `skill`; synthetic cases cover the Skill tree, the local H3 and the `Steps` table.
- `tests/test_native_skill_envelope.py` and `tests/test_common_agents_document_routes.py`: their synthetic `SKILL.md` bodies gain the form headings.
- Any other test that resolves a skill or workflow profile, its template or its role is updated in the same change.

## Edge Cases & Error Handling

- A heading inside a fenced example (`k8s-security-audit`, `rca-methodology`) stays unchanged.
- A `SKILL.md` whose only procedure heading is `Workflow Steps` holds that body directly under Steps.

## Failure Modes & Fallback / Human Escalation

If any document outside the 19 and the two templates gains a diagnostic, or the agent-governance validator reports a skill bundle, frontmatter or projection change, the change is wrong and is fixed before commit. If a sentence cannot be placed without changing its meaning, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators and `python3 scripts/validate-agent-governance.py --root .`; after must equal before.
- Before and after, the fragment search `git grep -n -E '(SKILL|work-lifecycle|delegated-development)\.md#' -- ':!docs/98.archive'`; every fragment names an existing heading after the move.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance` and `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-SKILL-001 | The registry holds the Skill form, its local extension, the new template profile, both TemplateDefinitions and tables, and the four role bindings with empty lists; tests fail first and then pass. |
| VAL-SKILL-002 | The 19 documents and two templates pass the tree, agent-governance, link, quality and markdownlint checks; frontmatter and bundle reachability are unchanged; each document's map and added lines are recorded in the Task; the policy texts are updated; validator output over the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SKILL-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry and form tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-SKILL-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
