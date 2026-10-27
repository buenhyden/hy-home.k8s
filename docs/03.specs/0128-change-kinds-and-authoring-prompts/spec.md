---
title: "Change Kinds and Authoring Prompts"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-27"
layer: "specs"
artifact_id: "SPEC-0128"
---

# Change Kinds and Authoring Prompts Technical Specification (Spec)

## Overview

SPEC-0125 left five CRs partial for slice C. The SDLC policy has no table of
what each kind of change requires and does not name security touchpoints or
the return of operations learning to requirements (CR-06.09, CR-06.10). The
Spec template does not ask for normal, error and boundary scenarios, and the
Plan template does not ask for architecture, interfaces, migration and
rollback (CR-06.07). The Task evidence prompt does not ask for command, tool
version, exit code and time (CR-06.04). An operations section made only of
links passes as content (CR-07.04). This Spec closes those points. The
[Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-change-kinds-and-authoring-prompts.md) records it.

## Strategic Boundaries & Non-goals

- In scope: `.agents/governance/sdlc.md`, the Spec, Plan and Task templates,
  `scripts/validate-markdown-profiles.py` and its operations section test,
  this package and the Stage 03 README index.
- Non-goals:
  - new required sections, columns or frontmatter keys;
  - rewriting existing Specs, Plans, Tasks or operations documents;
  - a filler-word list for link sentences such as "See".

## Contracts

- The change-kind table names, for each kind, the minimum records, checks
  and approval, by linking existing owners rather than restating them.
- Template changes are author prompts only, so existing documents stay
  valid.
- In a profile with substantive section bodies, a required section other
  than "Related Documents" is empty when its prose consists only of links.

## Core Design

`_substantive_section_body` removes Markdown and autolinks from a prose line
before deciding whether the line has text, except in navigation sections.
Tables and code blocks keep their current rules.

## Data Modeling & Storage Strategy

No stored data.

## Interfaces & Data Structures

- `_substantive_section_body(lines, *, links_are_content=True)` and
  `_LINK_ONLY_SECTIONS` in `scripts/validate-markdown-profiles.py`.
- Two tests in `tests/test_operations_section_contract.py`.

## Edge Cases & Error Handling

- A sentence with an instruction and a link fills a section.
- A sentence such as `See [RUN-0001](x).` still counts as text; review
  remains responsible for it.

## Failure Modes & Fallback / Human Escalation

Reverting the pull request restores the previous rule and prompts.

## Verification Commands

- `python3 -m unittest tests.test_operations_section_contract`.
- `python3 scripts/validate-markdown-profiles.py` over the repository.
- `python3 scripts/validate-document-contract-registry.py` and
  `python3 -m unittest tests.test_repository_form_contracts`.
- `python3 scripts/qa.py staged` on the exact index.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-CK-001 | `sdlc.md` has a change-kind table whose rows link existing owners, plus the security and requirement-feedback sentences, and an independent reviewer finds each row consistent with its owner. |
| VAL-CK-002 | The Spec, Plan and Task templates carry the new prompts and the registry and form tests pass. |
| VAL-CK-003 | A link-only instruction section fails in a new test that fails before the change, a navigation section may stay link-only, and the repository still passes the profile validator. |
| VAL-CK-004 | Staged QA passes on every commit and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CK-001 | Governance review |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CK-002 | Template contract tests |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CK-003 | Profile validator tests |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CK-004 | Staged QA and hosted checks |
