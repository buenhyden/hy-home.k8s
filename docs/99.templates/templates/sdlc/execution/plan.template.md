---
title: '{Feature Name} Implementation Plan'
type: sdlc/plan
status: draft
owner: platform
updated: YYYY-MM-DD
---

<!-- Target: docs/04.execution/plans/YYYY-MM-DD-<feature>.md -->

# [Feature Name] Implementation Plan

> Use this template for `docs/04.execution/plans/YYYY-MM-DD-<feature>.md`.
>
> Rules:
>
> - Every active plan must include explicit verification criteria.
> - Plan explains execution order, risk control, and rollout strategy.
> - Write this plan in English.
> - Use relative links only, calculated from the final authored document location.

---

## Overview

This document defines the implementation plan for [Feature or Component Name].
It records work breakdown, verification, rollout, risk management, and
completion criteria.

## Context

[Why this work exists.]

## Goals & In-Scope

- **Goals**:
- **In Scope**:

## Non-Goals & Out-of-Scope

- **Non-goals**:
- **Out of Scope**:

## Work Breakdown

| Task    | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| ------- | ----------- | --------------------- | ---------- | ------------------- |
| PLN-001 | [Action]    | `path/to/file`        | REQ-001    | [Evidence]          |

## Verification Plan

| ID          | Level      | Description | Command / How to Run | Pass Criteria |
| ----------- | ---------- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Structural | [Check]     | [Command]            | [Pass]        |

## Risks & Mitigations

| Risk   | Impact | Mitigation   |
| ------ | ------ | ------------ |
| [Risk] | High   | [Mitigation] |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**:
- **Sandbox / Canary Rollout**:
- **Human Approval Gate**: [State whether live runtime validation, CI topology, provider config, model policy, GitOps manifest, secret, or template changes are in scope.]
- **Rollback Trigger**:
- **Prompt / Model Promotion Criteria**:

## Completion Criteria

- [ ] Scoped work completed
- [ ] Verification passed
- [ ] Required docs updated

## Related Documents

Target-relative examples below assume the authored file will be created at
`docs/04.execution/plans/YYYY-MM-DD-<feature>.md`.

- **PRD**: `[../../01.requirements/<###-Numbering>-<feature-or-system>.md]`
- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Spec**: `[../../03.specs/<###-Numbering>-<feature-id>/spec.md]`
- **ADR**: `[../../02.architecture/decisions/####-<short-title>.md]`
- **Tasks**: `[../tasks/YYYY-MM-DD-<feature-or-stream>.md]`
