---
title: "Review Decisions and C4 Prompt"
version: "0.1.0"
type: "sdlc/spec"
status: "approved"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0133"
---

# Review Decisions and C4 Prompt Technical Specification (Spec)

## Overview

SPEC-0125 left two kinds of survey item open for the operator. CR-02.07 asks
for a decision on each `DERIVED_PROPOSAL` cell of the m0012 source-support
matrix. Eight `EXTERNAL` CRs need the other repositories, the cluster or an
operator action. On 2026-10-28 the operator reviewed both and decided three
things:
- adopt the C4 diagram checks in the architecture-description author prompt;
- record the read-only evidence for CR-12.01;
- record the action that each other `EXTERNAL` CR waits on.

This Spec records those decisions and makes the one template change. The
[Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-review-decisions-and-c4-prompt.md) records it.

## Strategic Boundaries & Non-goals

- In scope: this package, the Stage 03 README index, the REQ-0003 trace
  links and the diagram author prompt in
  `docs/99.templates/templates/architecture/description.template.md`.
- Non-goals:
  - closing any `EXTERNAL` CR, changing another repository, a GitHub
    setting or a token scope;
  - adopting a new template, an external role catalogue or a memory tool;
  - reading private repository contents beyond metadata.

## Contracts

- Each `DERIVED_PROPOSAL` cell and each named external catalogue has one
  decision: adopted with its owner, already covered with its owner, or not
  adopted with a reason.
- The C4 prompt adds element and relationship checks to the existing prompt
  and adds no template, section or validator rule.
- Each `EXTERNAL` CR names what is observable now and the action that would
  close it. CR-12.01 records metadata read from GitHub on 2026-10-28.

## Core Design

The decisions are tables in the Task. The template change edits one author
prompt line.

## Data Modeling & Storage Strategy

No stored data.

## Interfaces & Data Structures

None.

## Edge Cases & Error Handling

- Branch protection on the private repositories cannot be read on the
  current GitHub plan; the record says so instead of inferring it.

## Failure Modes & Fallback / Human Escalation

Reverting the pull request restores the prompt line.

## Verification Commands

- `python3 scripts/qa.py staged` on each commit.
- Read-only `gh api` GET calls for CR-12.01.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-RD-001 | The architecture-description author prompt asks for element labels and relationship direction and labels, and staged QA passes on the template change. |
| VAL-RD-002 | The Task records one decision for each of the five `DERIVED_PROPOSAL` cells and the two external catalogues. |
| VAL-RD-003 | The Task records the CR-12.01 read-only evidence and the closing action for the other seven `EXTERNAL` CRs. |
| VAL-RD-004 | An independent reviewer confirms the records and the prompt, and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0014](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RD-001 | Prompt change and staged QA |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RD-002 | Decision record and review |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RD-003 | External record and review |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RD-004 | Review and hosted checks |
