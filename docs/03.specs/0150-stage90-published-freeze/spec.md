---
title: "Stage 90 Published Member Freeze"
version: "0.1.1"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-11-06"
layer: "specs"
artifact_id: "SPEC-0150"
---

# Stage 90 Published Member Freeze Technical Specification (Spec)

## Overview

`docs/90.references/AGENTS.md` rule 3 forbids rewriting a published member;
later findings go to a new member. No validator enforced it, and AUD-0001
m0001 was rewritten five times after publication (AUD-0001 F-10). On
2026-11-06 the operator asked to resolve this. A validator change needs this
package. The [Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-stage90-published-freeze.md) records it.

## Strategic Boundaries & Non-goals

- In scope: `scripts/validate-document-contract-registry.py`, the Stage 90
  topology owner, and a focused regression in
  `tests/test_reference_pack_routes.py`.
- Non-goals:
  - the lifecycle validator, which REQ-0003-FR-0027 limits to profile, state
    and edges;
  - pack and collection READMEs, which rule 4 requires to list members;
  - draft or in-review members, and members first added in the change;
  - restoring m0001's published bytes.
- Open questions: none that change a criterion.

## Contracts

- A Stage 90 member (`reference/audit`, `reference/research`,
  `reference/data`) whose HEAD version has status `published` may change in
  the index only in its frontmatter `status`, `version` and `updated`
  values and in link destinations; any other change is refused with
  `REFERENCE_PUBLISHED_REWRITE`.
- A link destination may change so a consumer can be succeeded; its link
  text may not.
- Allowed lifecycle edges themselves stay judged by the lifecycle validator.

## Core Design

A pure function compares base and staged texts after removing the three
frontmatter values and blanking every inline link destination. A thin
wrapper reads the HEAD and stage-zero blobs through the existing bounded Git
process helper for members whose object IDs differ. Constraining
architecture: [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) assigns document-form enforcement to the validators that
consume the Stage 99 registry; this change stays in the Stage 90 owner.

## Data Modeling & Storage Strategy

No data or schema changes.

## Interfaces & Data Structures

One new diagnostic `REFERENCE_PUBLISHED_REWRITE` in the existing strict
output. No command-line change.

## Edge Cases & Error Handling

- Normal: a status edge or a link destination change passes.
- Error: a changed sentence, table row or link text is refused.
- Boundary: without a HEAD commit, or for a member absent from HEAD, nothing
  is compared.

## Failure Modes & Fallback / Human Escalation

A refused rewrite moves the new content into a new dated member. A Git read
failure is reported as `REFERENCE_PACK_INDEX`, as the existing inventory
does. Rollback is reverting the implementing commit.

## Verification Commands

- `python3 -m unittest tests.test_reference_pack_routes`
- the strict registry, Markdown-profile, link and lifecycle checks
- `python3 scripts/qa.py staged` on each commit

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-FRZ-001 | Focused tests fail before and pass after: a body rewrite of a published member is refused, lifecycle values and link destinations pass, draft members pass |
| VAL-FRZ-002 | The strict checks and staged QA pass on the current tree, and a staged rewrite of the published m0001 is refused |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Architecture | Verification method |
| --- | --- | --- | --- |
| [REQ-0003-FR-0015](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FRZ-001 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Focused tests red then green |
| [REQ-0003-FR-0027](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-FRZ-002 | [AD-0006](../../02.architecture/descriptions/0006-workspace-agent-governance-platform.md) | Strict checks and an observed refusal |
