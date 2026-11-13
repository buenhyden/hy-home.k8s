---
title: "W03 AGENTS Form"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0176"
---

# W03 AGENTS Form Technical Specification (Spec)

## Overview

This approved change contract is the eighth phase-2 package of the W03 stage of the external v14.7 execution package. It gives the AGENTS role its COMMON-DOC-FORM-1 1.0.0 form in the Stage 99 registry, adds the role's template, and moves 16 documents form-only: the root `AGENTS.md` (the Codex gateway) and the 15 folder `AGENTS.md` files. DOC-02 makes every `AGENTS.md` the agent instructions of its directory, and W03-D10 binds the root file with the folder files. The repository's thin-gateway rule (`AGENT-NATIVE-REFERENCE`, at most 30 lines in a root gateway) predates the form and would refuse the root file once it carries the form headings; on 2026-11-13 the user answered "follow the requirements" to that conflict, so the current requirement prevails (EVD-018) and the rule is changed to count content lines, not heading lines, keeping its other conditions (W03-D18). The reading rests on DOC-02 (each directory's agent instructions), the COMMON-ROLE-FORMS AGENTS role and W03-D10, which already bind the root file, and holds against COMMON-STANDARD section 7, which treats `AGENTS.md` both as the work-scope file and as a provider-supported file; the profile id `common/folder-agents-guide` therefore also selects one non-folder file. Staged QA does not route every folder `AGENTS.md` to the form check; that routing belongs to W05 and is handed off as W03-H12. It applies W03-D01, W03-D08 and W03-D10 recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md) and reuses the model of SPEC-0169 to SPEC-0175 (recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). The [Task](tasks/tsk-0001-w03-agents-form.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json`; a new template `docs/99.templates/templates/common/agents.template.md`; the 16 documents named above; `scripts/validate-agent-governance.py` (the gateway line rule); `tests/test_common_form_tree.py`, `tests/test_agent_governance.py`, `tests/test_repository_quality_rules.py`, `tests/test_document_terminal_contract.py` (only if the template name needs it), `tests/test_document_language.py` and any test that pins these profiles' patterns, roles or templates; in `.agents/governance/document-authoring.md` the forms sentence and the gateway and folder-guide sentences, and in `docs/99.templates/README.md` the forms bullet and the gateway sentence; the W03-D18 and W03-H12 rows, an evidence row and the frontmatter `version` and `updated` of the SPEC-0161 Task (appended rows only); this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: the root `CLAUDE.md` and the folder `CLAUDE.md` import files, which stay native with no common role (DOC-02, W03-D10); `SKILL.md` and workflows; native discovery and loading evidence, which is W07; `.claude/`, `.codex/` and provider settings; the Workspace and Reference Pack README roles; phase 3.
- Form-only migration (W03-D01): no sentence changes meaning, no rule, permission or command is added, every link target stays; where an H3 has no source text, one English line states that none exists or points to the existing text that covers it, listed in the Task for the user. AGENTS files carry no frontmatter, so no version is bumped. No push, PR or merge without separate approval. Open question: none.

## Contracts

- **AGENTS form.** `common_forms.forms` gains the AGENTS form exactly as COMMON-DOC-FORM-1 1.0.0 defines it (`roles[14]`): `form_id` `agents`, `title` `AGENTS`, Scope (Allowed Surface, Non-goals), Required Policies (Canonical Sources, Local Obligations), Workflow (Inspect and Change, Handoff), Verification (Required Checks, Evidence and Limits), Safety (Protected Actions, Stop and Escalate), every section required, `link_only` false everywhere. No extension.
- **Profiles and binding (W03-D10).** `common/folder-agents-guide` widens its path pattern to also select the root `AGENTS.md` (still excluding `docs/98.archive/`) and gains `document_role` `agents` and `template_source` `docs/99.templates/templates/common/agents.template.md`; `common/root-provider-shim` narrows to the root `CLAUDE.md` only and keeps no role. A new template profile `common/template-agents-guide` (mode `template`, frontmatter `absent`, `placeholder_policy` `template-only`, an exact path route) selects the template, names `common/folder-agents-guide` as its source, so the template parity check holds, and carries `document_role` `agents` and the TemplateDefinition. The template has no frontmatter, an H1 with an uppercase placeholder such as `{{AGENTS_SCOPE_NAME}}`, and an author prompt under each H2. All three carry empty H2 lists; the AGENTS profiles stay `native`, so frontmatter stays absent and empty sections are enforced by review, not by `BODY-SECTION-EMPTY`.
- **Table (W03-D08).** COMMON-ROLE-FORMS names the AGENTS conditional content as tool-specific rules with a rule/trigger/effect table. The TemplateDefinition carries `Tool Rules` in `agents-required-policies-local-obligations` with keys `Rule`, `Trigger` and `Effect` (all required), `minimum_rows` 0, row identity `Rule`. No current table in the 16 documents starts with a `Rule` header.
- **Gateway rule (W03-D18).** `AGENT-NATIVE-REFERENCE` refuses a root gateway with more than 30 content lines or more than 16 heading lines (one H1 and the AGENTS form's 5 H2 and 10 H3), instead of more than 30 lines in all. A heading line is an ATX heading (`^ {0,3}#{1,6}(\s|$)`) outside fenced code; a content line is any other non-blank line. The required references, the ban on catalog headings and the exact loader references are unchanged, and the rule still applies to both provider gateways. This keeps REQ-0003-FR-0002 (gateways copy no common policy and stay thin): the root file's form H3 lines hold only pointers. Failing cases first in `tests/test_agent_governance.py`: 31 content lines are refused, 17 heading lines are refused, and a formed gateway of 30 content lines with its 16 headings is accepted.
- **TemplateDefinition.** It carries purpose, responsibility, non-goals, policy references (`document-authoring.md`, `agent-execution.md`), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, every real consumer path (registry, schema, the template, the 16 documents, Stage 99 README, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-document-contract-registry.py`, `scripts/validate-agent-governance.py`, `scripts/provider_write_guard.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py` and the tests), validation cases, migration and `tables`.
- **Meaning map, applied per document.** Every old H2 heading is removed and its body moves under the form H3 named below; an old H3 becomes an H4; plain text precedes the H4s inside a form H3; a paragraph or list is never split, so a numbered rule list keeps its numbering.
  - Folder files: the paragraph between the H1 and the first H2 stays directly under the H1, unchanged, because the pre-edit hook test pins its chain markers; `Purpose` and the whole body of `Responsibilities and Projections` go to Scope > Allowed Surface; `Rules` and the `examples/azure` `Folder Rules` go whole to Required Policies > Local Obligations; `Checks` goes to Verification > Required Checks.
  - Root file: the lines before the H1 stay before it, because the gateway loader reads them; the line after the H1 and the policy-pointer list go to Required Policies > Canonical Sources together with the Codex-only reads; the sentence on tracked projections goes to Verification > Evidence and Limits; the closing read instruction goes to Workflow > Inspect and Change. Every `Read ... before acting.` line keeps its exact text.
  - Every other form H3 gets one English line: a pointer to the item that already covers it (for example, a rule-list item on protected actions, handoff or checks) or a statement that the file states none; the line never adds a rule, permission or command.
  - The Task records each document's placements and added lines.
- **Policy text.** `document-authoring.md` adds AGENTS to the roles that use their registry forms and corrects its sentences that keep the root `AGENTS.md` on the gateway shim and limit `common/folder-agents-guide` to folder files; `docs/99.templates/README.md` says in its forms bullet that `AGENTS.md` files use the AGENTS form and corrects its sentence that keeps the root `AGENTS.md` on `common/root-provider-shim`; the root `CLAUDE.md` and folder imports stay native. `agent-execution.md` (thin gateways) and the provider notes stay true and are not edited.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes. Provider loading reads each `AGENTS.md` whole, so a heading change does not change what is loaded; W07 observes native loading.

## Data Modeling & Storage Strategy

Registry data: one form, one new template profile with its TemplateDefinition and table, two path patterns, one role binding. Code: one counting rule.

## Interfaces & Data Structures

- `scripts/validate-agent-governance.py`: the gateway rule counts content lines (blank and heading lines excluded) and caps heading lines at 16.
- `tests/test_common_form_tree.py`: the eight-form constant and the tests named for it become nine forms; `ROLE_BINDINGS`, `FORM_PROFILES` and `FORM_TEMPLATES` gain the AGENTS profiles; the per-form loop gains an AGENTS row (tree, no extension, `Tool Rules`, no body section); synthetic cases cover the AGENTS tree and the `Tool Rules` table.
- `tests/test_repository_quality_rules.py`: the assertion that the root `AGENTS.md` owns no generic template residue flips, because a form now gives it headings, or names another native file.
- `tests/test_document_terminal_contract.py`: the template H1 uses the uppercase placeholder grammar, so the test needs no change unless the name does.
- `tests/test_document_language.py`: the case that resolves the root `AGENTS.md` to `common/root-provider-shim` resolves it to `common/folder-agents-guide`.
- `tests/test_agent_governance.py`: the 31-content-line and 17-heading refusals and the formed-gateway acceptance.
- Known limitation (W03-H12, W05): staged QA routes `policy/`, `scripts/` and `tests/` `AGENTS.md` to surfaces without the markdown-profile or registry validator, and `.github/`, `examples/`, `gitops/` and `infrastructure/` `AGENTS.md` without the registry validator; until W05 changes the routing, the whole-tree strict run in this package and in later ones is the evidence.

## Edge Cases & Error Handling

- A folder file without a `Checks` section (`docs/AGENTS.md`) points Required Checks to its rule that names the checks.
- A gateway preamble before the H1 is kept and counted as content.

## Failure Modes & Fallback / Human Escalation

If any document outside the 16 and the template gains a diagnostic, or the agent-governance validator refuses a gateway for anything but the changed count, the change is wrong and is fixed before commit. If a sentence cannot be placed without changing its meaning, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators and `python3 scripts/validate-agent-governance.py --root .` over the whole tree; after must equal before.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance` and `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-AGENTS-001 | The registry holds the AGENTS form, the template profile with its TemplateDefinition and table, the widened and narrowed path patterns and the role binding; the gateway rule counts content lines; tests fail first and then pass. |
| VAL-AGENTS-002 | The 16 documents and the template pass the tree, agent-governance, link, quality and markdownlint checks; each document's map and added lines are recorded in the Task; the policy texts are updated; validator output over the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGENTS-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry, form and gateway tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-AGENTS-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
