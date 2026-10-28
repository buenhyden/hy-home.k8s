---
title: "Remaining Decisions Closeout"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0138"
---

# Remaining Decisions Closeout Technical Specification (Spec)

## Overview

[SPEC-0135](../0135-external-item-decisions/spec.md) left five survey CRs open
and [SPEC-0134](../0134-archive-final-units/spec.md) kept SPEC-0103 `usable`.
On 2026-10-28 the operator chose the recommended option for each:
- the four repositories stay independent, which closes CR-03.06, CR-03.07 and
  CR-08.01;
- GitHub Projects are not used for status, which closes CR-14.03;
- SPEC-0103 stays `usable` for good;
- a read-only live check runs for CR-09.04.

This Spec records those decisions and the live observation. The
[Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-remaining-decisions-closeout.md) records it.

## Strategic Boundaries & Non-goals

- In scope: this package, the Stage 03 README index and the REQ-0003 trace
  links.
- Non-goals:
  - changing another repository, the cluster, a secret, a Project or the
    OpenBao service;
  - repairing the secret backend failure the live check found; that is a
    separate operator-approved change;
  - migrating the older-form SPEC-0105 Task.

## Contracts

- Each decision names the CR or unit it settles, the date and its effect.
- The live observation names its time, its read-only commands and each result,
  and states that acceptance fails while the secret backend is unavailable.
- No cluster object, secret or other repository changes.

## Core Design

The decisions and the observation are tables in the Task.

## Data Modeling & Storage Strategy

No stored data.

## Interfaces & Data Structures

None.

## Edge Cases & Error Handling

- A live check that would create a cluster object is out of scope even when it
  only reads; such a probe stays unrun.

## Failure Modes & Fallback / Human Escalation

The secret backend failure goes to the operator with RUN-0002 as the recovery
procedure.

## Verification Commands

- Read-only `kubectl get` and `kubectl config current-context`.
- Host-side `getent`, `curl` and `openssl s_client`.
- `python3 scripts/qa.py staged` on each commit.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-RC-001 | The Task records the decisions on CR-03.06, CR-03.07, CR-08.01, CR-14.03 and SPEC-0103, with date and effect. |
| VAL-RC-002 | The Task records the read-only CR-09.04 observation, the failed acceptance, its cause as observed and the next owner, and no cluster object changed. |
| VAL-RC-003 | An independent reviewer confirms the records, re-reading the live state read-only, and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RC-001 | Decision record and review |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RC-002 | Live observation record and review |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-RC-003 | Review and hosted checks |
