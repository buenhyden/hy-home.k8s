---
title: "W03 Root README Form"
version: "1.0.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-13"
layer: "specs"
artifact_id: "SPEC-0172"
---

# W03 Root README Form Technical Specification (Spec)

## Overview

This approved change contract is the fourth phase-2 package of the W03 stage of the external v14.7 execution package and the first of three README packages (Root, then Stage, then Service). It gives the Root README role its COMMON-DOC-FORM-1 1.0.0 form in the Stage 99 registry, moves the repository `README.md` and its template to the form without changing meaning, and makes the README navigation check and its registry rule accept a navigation section that is an H3 of a form, which the Stage and Service packages also need. It reuses the SPEC-0169 model (derived heading lists, TemplateDefinition `tables`, table checks; recovery in [REQ-0003 Archived Lineage](../../01.requirements/0003-workspace-agent-governance-platform.md#archived-lineage)). The user's decisions W03-D01, W03-D08, W03-D10 and W03-D11 and handoff W03-H10 are recorded in the [SPEC-0161 Task](../0161-w00-v14-7-delta-intake/tasks/tsk-0001-w00-v14-7-delta-intake.md). The [Task](tasks/tsk-0001-w03-root-readme-form.md) records execution and the [Plan](plan.md) orders the work.

## Strategic Boundaries & Non-goals

- In scope (writer W03, with W05 for validator code): `docs/99.templates/registry.json`, `docs/99.templates/templates/common/readme-repository.template.md`, `README.md`, `scripts/document_contracts.py` (the README navigation registry rule and the table-column order rule), `scripts/validate-links-and-owners.py` (the README navigation section reader), `scripts/validate-markdown-profiles.py` (optional trailing table columns), `tests/test_common_form_tree.py`, `tests/test_readme_navigation.py`, the forms sentence of `.agents/governance/document-authoring.md` ("Guide, Runbook, Incident and Postmortem use their registry forms") and the Common forms bullet of `docs/99.templates/README.md` (the shared README H2 core), each with frontmatter `version` and `updated`; `tests/test_document_terminal_contract.py` is a consumer that needs no change, because `README.md` keeps its `docs/README.md` and `Plan/Task` strings; this package, the Stage 03 README and reviewed `.secrets.baseline` entries.
- Not in this package: the Stage README role (stage, collection and agent or provider READMEs), the Service README role, Workspace README and Reference Pack README, which keep their H2 lists; the retirement of the list-mode `README_H2_*` rule IDs, which stay for README profiles without a form until the last README role moves; phase 3.
- Form-only migration (W03-D01): no sentence of `README.md` changes meaning and no fact is added; where the form asks for content the source does not hold, the section states that none exists and why, in Korean, listed in the Task for the user. No push, PR or merge without separate approval. Open question: none.

## Contracts

- **Root README form.** `common_forms.forms` gains the Root README form exactly as COMMON-DOC-FORM-1 1.0.0 defines it (`roles[11]`): `form_id` `root-readme`, `title` `Root README`, Purpose (Project Role, Boundaries), Repository Map (Directories, Canonical Entry Points), Getting Started (Prerequisites, First Verified Path), References (Current Documentation, Support and Ownership), every section required, `link_only` false. No extension. The template keeps its H1 `# {{REPOSITORY_NAME}}`.
- **Profiles.** `common/readme-repository` and `common/template-readme-repository` carry empty H2 lists; their heading lists are derived from the form. In tree mode README headings report `BODY-*` rule IDs, as the tree check already does; README H1, fence and frontmatter rules keep their `README_*` IDs.
- **Navigation section in a form.** `readme_navigation.profiles["common/readme-repository"].section` becomes `Directories`. The registry rule `REGISTRY_README_NAVIGATION` accepts an entry whose section is a required H2 of the profile's lists, or, for a profile whose role has a form (read through `document_role` and `common_forms`, which may be absent), a required H2 or H3 title that occurs once among the form's H2 and H3 titles; its expected text names both. The navigation reader in `scripts/validate-links-and-owners.py` needs no form data: it reads the first H2 whose title equals the section and, only when no such H2 exists, the first H3 with that title, up to the next heading of the same or a higher level, so H4 subsections belong to it. The registry rule confines H3 section names to form profiles. An H3 that shares a title with a list profile's H2 section therefore never displaces that H2 (current READMEs hold such H3s, for example `Item Index` in `.agents/roles/README.md`). `complete` stays `false` for the root README.
- **Optional trailing table columns.** In a TemplateDefinition table, columns with `required` false may only follow every required column; `REGISTRY_TABLE_COLUMNS` refuses a required column after an optional one. The document table check accepts a header equal to `keys[:n]` with `n` at least the number of required columns. This represents `readme_navigation.optional_index_columns` (`Owner`) for README index tables named in a TemplateDefinition, while `readme_navigation` keeps its own index-column contract for the document-content index check (`scripts/validation/document_content.py`, which accepts any distinct subset of optional columns); both name only `Owner` today, and a later change to either must change both. No current table has an optional column, so no current result changes.
- **Table (W03-D08).** The root TemplateDefinition `tables`: `Directory Index` in `root-readme-repository-map-directories` with keys `Path` and `Purpose` (required) and `Owner` (optional), `minimum_rows` 0, row identity `Path`. The current `README.md` has no such table.
- **TemplateDefinition.** The root template profile carries purpose, responsibility, non-goals, policy references (`document-authoring.md`, `sdlc.md`), vocabulary reference (`.agents/knowledge/glossary.md`), applicability, every real consumer path (registry, schema, template, `README.md`, Stage 99 README, `scripts/document_contracts.py`, `scripts/validate-markdown-profiles.py`, `scripts/validate-links-and-owners.py`, `scripts/validation/document_content.py`, `scripts/validation/repository/form_contracts.py`, `scripts/validation/repository/quality.py`, `tests/test_common_form_tree.py`, `tests/test_readme_navigation.py`), validation cases, migration and `tables`.
- **README.md meaning map (W03-D11).**
  - Purpose > Project Role: the lead blockquote, Overview and Audience.
  - Purpose > Boundaries: Scope (In Scope and Out of Scope as H4) and the current implementation boundary list (H4).
  - Repository Map > Directories: the directory tree block, Top-level Areas (H4) and Tech Stack (H4) with the Verification section's cloud-example version and Ingress NGINX retirement paragraph; Tech Stack stays in the navigation section so `README-NAV-COPY` keeps checking its table.
  - Repository Map > Canonical Entry Points: Documentation Map (H4), Repository Workflow (H4) and Common Workflows (H4).
  - Getting Started > Prerequisites: the tool and external-runtime list.
  - Getting Started > First Verified Path: the numbered steps 1 to 5 (H4, numbering and order kept) and the Verification section's QA text, commands and approval-boundary paragraph (H4).
  - References > Current Documentation: Related Documents links, Language Policy (H4) and Relative Link Rules (H4).
  - References > Support and Ownership: Canonical Owners (its list), which names the owner documents; the form also asks for inquiry and error-reporting routes, which the source does not hold, so one Korean none-with-reason line states only that the repository holds no separate inquiry or error-reporting route, listed in the Task for the user. Trade-off recorded: the Canonical Owners links leave the navigation section, so `README-NAV-DEPTH` no longer reads them; none is a deep path today.
  - The link to `docs/99.templates/README.md` that `DOC-AUTHOR-GUIDE` requires stays.
- **Template.** Four H2 and eight H3 headings with Korean author prompts drawn from each H3's `required_content`, keeping the current prompts' meanings (purpose, readers and authority; scope and owners; direct children only, one deep link per folder, no copied status, dates or counts; shortest verified path; static checks apart from live or remote evidence; owner links), and an optional `| Path | Purpose |` table under Directories.
- **Policy text.** `document-authoring.md` adds the Root README to the roles that use their registry forms; the `docs/99.templates/README.md` Common forms bullet keeps the shared `Overview`, `Scope`, `Structure`, `Usage`, `Related Documents` core only for stage, collection, implementation, workspace and runtime-governance READMEs and says the root README uses Purpose, Repository Map, Getting Started and References, reconciling the bullet's own list of README kinds; other README kinds keep their H2 lists until their packages.

## Core Design

[AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) owns the governance view; no component changes. The registry stays the single machine owner of document form and README navigation ([ADR-0033](../../02.architecture/decisions/0033-common-document-contract-v9.md) as amended by [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md)); no ADR changes.

## Data Modeling & Storage Strategy

Registry data only: one form, one TemplateDefinition with one table, two profiles' lists and one navigation entry's section.

## Interfaces & Data Structures

- `scripts/document_contracts.py`: `REGISTRY_README_NAVIGATION` checks the navigation section against the profile lists or the role form's required, unique H2 and H3 titles; `REGISTRY_TABLE_COLUMNS` refuses a required column after an optional one.
- `scripts/validate-links-and-owners.py`: the README navigation section reader handles H2 or H3 sections.
- `scripts/validate-markdown-profiles.py`: the document table check accepts omitted trailing optional columns.
- `tests/test_readme_navigation.py`: an H3 navigation section counts its links and H4 content and excludes the next H3 and H2; an H3 that shares a list profile's H2 section title does not displace the H2; the registry rule accepts a form H3, rejects a title absent from the form or repeated in it, and still works for a raw registry without `common_forms`.
- `tests/test_common_form_tree.py`: the repository-registry tests name exactly the Guide, Runbook, Incident, Postmortem and Root README forms; table cases cover an omitted and a present optional trailing column, a header that omits a required column, and a registry definition with a required column after an optional one.

## Edge Cases & Error Handling

- A navigation title must be unique among its form's H2 and H3 titles, so the reader's first match is unambiguous; the Root form has no duplicate.
- A required column after an optional one is refused in the registry.

## Failure Modes & Fallback / Human Escalation

If any document other than `README.md` and the template gains a diagnostic, the change is wrong and is fixed before commit. If a `README.md` sentence cannot be placed without changing its meaning, the author stops and asks the user.

## Verification Commands

- Before and after, record the output of the four strict document validators over the whole tree; after must equal before.
- `python3 scripts/run-contract-tests.py --root . --suite document`, `--suite document-lifecycle`, `--suite agent-governance` and `--suite validation-routing`.
- `python3 scripts/validation/repository/quality.py --root .`; markdownlint over the edited Markdown; the staged lifecycle check before each commit.
- `ruff check scripts tests`; `python3 scripts/qa.py staged` and the commit hooks on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-ROOTREADME-001 | The registry holds the Root README form, its TemplateDefinition and table and the navigation section `Directories`; the root profiles carry no H2 lists; the navigation registry rule and reader accept an H3 section and reject a title absent from the form or repeated in it; optional trailing columns behave as specified; tests fail first and then pass. |
| VAL-ROOTREADME-002 | `README.md` and the template pass the tree, navigation, document-content, author-prompt, residue and markdownlint checks; the meaning map and any added line are recorded in the Task; the policy texts are updated; validator output over the tree is unchanged; exact-index QA and the commit hooks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ROOTREADME-001 | [ADR-0059](../../02.architecture/decisions/0059-registry-common-form-model.md) | Registry and navigation tests. |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-ROOTREADME-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict validators over the tree; exact-index QA. |
