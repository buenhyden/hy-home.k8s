---
title: "External Item Decisions"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0135"
---

# External Item Decisions Technical Specification (Spec)

## Overview

[SPEC-0133](../0133-review-decisions-and-c4-prompt/spec.md) recorded what
each of the eight `EXTERNAL` survey CRs waits on. On 2026-10-28 the operator
acted on five of them:
- accepted the rewritten survey text (CR-01.02);
- accepted the observed repository setup as the target (CR-12.01);
- accepted a mock-only record for provider limits (CR-18.06);
- asked for the private repositories' archive layouts (CR-08.01);
- granted `read:project` for the Projects read (CR-14.03).

This Spec records those decisions and observations. The [Plan](plan.md)
orders the work and [Task 0001](tasks/tsk-0001-external-item-decisions.md)
records it.

## Strategic Boundaries & Non-goals

- In scope: this package, the Stage 03 README index and the REQ-0003 trace
  links.
- Non-goals:
  - changing another repository, a GitHub setting, a Project or a token;
  - adding provider-limit mocks for code this repository does not have;
  - deciding the joint edition that CR-03.06, CR-03.07 and the CR-08.01
    unification need, or the live acceptance CR-09.04 needs.

## Contracts

- Each decided CR names the operator decision, its date and what it closes.
- Each observation names its read-only source and time.
- A CR that still waits on an operator names its remaining action.

## Core Design

The decisions and observations are tables in the Task.

## Data Modeling & Storage Strategy

No stored data.

## Interfaces & Data Structures

None.

## Edge Cases & Error Handling

- A private repository's branches can differ; each layout names its branch.

## Failure Modes & Fallback / Human Escalation

Reverting the pull request removes the records.

## Verification Commands

- Read-only `gh api` GET and GraphQL queries.
- `python3 scripts/qa.py staged` on each commit.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-XD-001 | The Task records the operator decisions on CR-01.02, CR-12.01 and CR-18.06, and what each closes. |
| VAL-XD-002 | The Task records the four repositories' archive layouts for CR-08.01 and the Projects observation for CR-14.03, each with its source. |
| VAL-XD-003 | An independent reviewer confirms the records against the sources, and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-XD-001 | Decision record and review |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-XD-002 | Observation record and review |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-XD-003 | Review and hosted checks |
