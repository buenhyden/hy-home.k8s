---
title: "Stage 99 Contract Cleanup"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-05"
layer: "specs"
artifact_id: "SPEC-0142"
---

# Stage 99 Contract Cleanup Technical Specification (Spec)

## Overview

On 2026-11-05 the operator asked to check `docs/99.templates/` against its
governance, its forms and the current repository, to correct what conflicts
and to remove contradictions and repetition inside each file, choosing the
low-risk cleanup scope. A form, registry or schema change is a contract
change (`docs/99.templates/AGENTS.md` rule 1), so this package owns the
changes. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-stage99-contract-cleanup.md) records it.

## Strategic Boundaries & Non-goals

- In scope:
  - the retired Stage 00 owner in the Plan form, the Plan promotion check of
    `scripts/validate-document-lifecycle.py` and the governance sentence that
    names it;
  - the ADR form's Lifecycle Traceability cells, which put the document's own
    `{{ARTIFACT_ID}}` where the predecessor ID belongs and omit the deleted-Spec
    wording of Stage 02 rule 4;
  - the profile modes `evidence` and `generated`, which no profile uses, with
    their schema enum values and dead validator branches;
  - the unreferenced schema definition `requirementMemberId`;
  - the `document_language.english_sections` entry `Agent Harness
    Requirements`, which no document or rule uses;
  - prose corrections in `docs/99.templates/README.md`,
    `docs/99.templates/templates/README.md` and `docs/99.templates/AGENTS.md`.
- Non-goals:
  - the `readme_navigation` and `document_language` pending and exempt path
    lists: they are empty but remain an active exemption mechanism;
  - Spec and Plan lifecycle states, supersession keys, registry
    de-duplication and `shared_contract` verification;
  - changing any current document's status or body.

## Contracts

- A Plan Promotion row may name an owner under `.agents/`,
  `docs/01.requirements/`, `docs/02.architecture/` or `docs/05.operations/`;
  a target under `docs/00.agent-governance/` is refused.
- The ADR form's Replacement relation and Affected Spec cells are author
  prompts that ask for the predecessor ADR ID and, for a deleted Spec, the
  form `N/A — SPEC-xxxx left the tree; Git history recovers it`.
- A profile mode is one of `authored`, `router`, `template`, `native` and
  `non-target`; the schema refuses any other value.
- The schemas and registry carry no definition or entry without a consumer.
- Every current document still passes the strict document checks.

## Core Design

Each change removes a value or a branch that no current document reaches, or
replaces a wrong prompt. The validators keep their structure; only the
unreachable `evidence` branches and the Stage 00 path go.

## Data Modeling & Storage Strategy

`registry.json` loses one list entry; `document-profile.schema.json` loses two
enum values; `frontmatter.schema.json` loses one `$defs` entry. Moving lines in
`registry.json` shifts the baselined secret-scan finding, so the
`.secrets.baseline` line number moves first in its own commit (rule 6).

## Interfaces & Data Structures

No command-line interface changes. The schema `mode` enum narrows to the five
modes in use.

## Edge Cases & Error Handling

- Normal: every current document and form validates as before.
- Error: a Plan that promotes to `docs/00.agent-governance/` and a profile
  with mode `evidence` are refused with the existing rule codes.
- Boundary: the comparison base still holds the old registry; the lifecycle
  check reads it in staged mode without failing.

## Failure Modes & Fallback / Human Escalation

A failing document check after the change means a document relied on a
removed value; revert the implementing commit and reopen the scope.

## Verification Commands

- `python3 scripts/run-contract-tests.py --root . --suite document`
- `python3 scripts/validate-document-contract-registry.py --root . --mode strict`
- the strict Markdown-profile, link and lifecycle checks
- `python3 scripts/qa.py staged` on each commit

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-S99-001 | A regression test shows a Plan promotion to `docs/00.agent-governance/` refused; the Plan form and governance text name no Stage 00 |
| VAL-S99-002 | The ADR form cells ask for the predecessor ID and the deleted-Spec wording; template checks PASS |
| VAL-S99-003 | A regression test shows mode `evidence` refused; no `evidence` or `generated` branch remains; `requirementMemberId` and `Agent Harness Requirements` are gone |
| VAL-S99-004 | The README and AGENTS prose matches the registry; the document suite and strict document checks PASS |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0012](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-S99-001 | Lifecycle regression test |
| [REQ-0003-FR-0013](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-S99-002 | Template and profile checks |
| [REQ-0003-FR-0024](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-S99-003 | Schema regression test and code search |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-S99-004 | Document suite and strict document checks |
