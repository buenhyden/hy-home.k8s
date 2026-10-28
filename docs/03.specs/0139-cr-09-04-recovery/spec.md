---
title: "CR-09.04 Recovery"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0139"
---

# CR-09.04 Recovery Technical Specification (Spec)

## Overview

[SPEC-0138](../0138-remaining-decisions-closeout/spec.md) kept CR-09.04
`EXTERNAL`: at 08:47Z on 2026-10-28 the `vault-backend` ClusterSecretStore
could not log in to OpenBao, and four platform applications were Degraded.
On 2026-10-28 the operator chose a read-only root-cause check. The check
found that the backend had already recovered. This Spec records the cause,
the recovery and a fresh live observation, and closes CR-09.04. The
[Plan](plan.md) orders the work and
[Task 0001](tasks/tsk-0001-cr-09-04-recovery.md) records it.

## Strategic Boundaries & Non-goals

- In scope: this package, the Stage 03 README index and the REQ-0003 trace
  links.
- Non-goals:
  - changing another repository, the cluster, a secret or the OpenBao service;
  - the OpenBao container restart policy and the other stopped containers,
    which `hy-home.docker` owns;
  - rewriting the SPEC-0138 record, which stays true for its observation time.

## Contracts

- The cause names its sources, which are cluster status, controller log
  lines without values, host probes and the owner's record in
  `hy-home.docker`.
- The live observation names its time, its read-only commands and each
  result.
- No cluster object, secret or other repository changes.

## Core Design

The cause, the recovery timeline and the observation are tables in the Task.

## Data Modeling & Storage Strategy

No stored data.

## Interfaces & Data Structures

None.

## Edge Cases & Error Handling

- If the backend fails again before review, the observation is recorded as
  failed and CR-09.04 stays `EXTERNAL`.

## Failure Modes & Fallback / Human Escalation

A recurrence goes to the operator with RUN-0002 for the cluster side and
`hy-home.docker` RUN-0103 for OpenBao.

## Verification Commands

- Read-only `kubectl get`, `kubectl logs` and `kubectl config current-context`.
- Host-side `curl`, `openssl s_client`, `docker ps` and `git log`/`git show`
  in `hy-home.docker`.
- `python3 scripts/qa.py staged` on each commit.

## Success Criteria & Verification Plan

| Criterion | Acceptance evidence |
| --- | --- |
| VAL-CR-001 | The Task records the cause of the CR-09.04 failure and its recovery, with sources and times, and no value was read. |
| VAL-CR-002 | The Task records a passing read-only live observation, and CR-09.04 is closed. |
| VAL-CR-003 | An independent reviewer confirms the records, re-reading the live state read-only, and the pull request's hosted checks pass. |

## Traceability

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CR-001 | Cause record and review |
| [REQ-0003-FR-0021](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CR-002 | Live observation record and review |
| [REQ-0003-FR-0018](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CR-003 | Review and hosted checks |
