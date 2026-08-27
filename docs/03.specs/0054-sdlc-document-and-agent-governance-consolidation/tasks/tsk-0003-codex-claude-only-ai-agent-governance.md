---
title: 'Task: Codex Claude-only AI agent governance'
type: sdlc/task
status: blocked
owner: platform
updated: 2026-08-22
artifact_id: "TSK-0054-0003"
---

# Task: Codex Claude-only AI agent governance

## Overview

This is the terminal Task record for WP-003. It remains dependency-blocked and
is not the active execution Task.

## Inputs

- [Common execution contract](../README.md#common-execution-contract)
- [Spec 0054](../spec.md)
- [Plan 0054](../plan.md)
- [WP-003 execution boundary](../plan.md#wp-003--codexclaude-only-ai-agent-governance)

## Task Table

**Plan label:** WP-003

**Depends on:** WP-004

**Current state:** `blocked`

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-054-003 | VAL-SDLC-005, VAL-SDLC-011, VAL-SDLC-012 | Create the `.agents` authority, converge Stage 00 on Codex/Claude-only support, and remove Gemini/Antigravity. | platform | Blocked | Waits only for WORK-054-004 document lifecycle and generic migration/recovery authority; resumes immediately afterward. | Agent registry/policy/projection/provider-evidence/consumer-zero gates; focused tests; two logical commits |

## Approval and Safety Boundaries

The [common execution contract](../README.md#common-execution-contract) applies
without exception. WP-003's Codex/Claude-only scope, live/provider mutation
boundary, reviews, rollback, and two ordered commits are owned by its linked
Plan section.

## Verification Summary

WP-003 is blocked solely on WORK-054-004 and must resume immediately after that
dependency closes.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-054-003](../plan.md#wp-003--codexclaude-only-ai-agent-governance) | Blocked. | Waits for WORK-054-004 authorities; predecessor candidate is input only and no completion evidence is claimed. |
