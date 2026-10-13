---
title: "Shared Workspace Memory Store Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "in-review"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0109-PLAN-0001"
parent_ids: ["SPEC-0109"]
---

# Shared Workspace Memory Store Implementation Plan

## Global Constraints

- The Task, never memory, owns execution status, evidence and acceptance.
- No memory body is deleted, summarized away or moved to another tier.
- Existing native memory files are neither deleted nor imported.
- No network, credential or private session data enters the store.

## Overview

This plan executes the approved [SPEC-0109](spec.md) design on branch
`feat/task-summary-roles-ko` after commit `fc8f468c`.

## Context

The review on 2026-10-13 observed Python SQLite 3.45.1, `codex-cli
0.162.1` with `memories.generate_memories` and `memories.use_memories`
keys, Claude Code 2.1.296, and an ext4 root filesystem without project
quota. The governance validator pins `.claude/settings.json` keys and does
not check `.codex/config.toml`.

## Goals & In-Scope

- A stdlib-only store module and CLI with focused tests.
- Native memory disablement for both providers with exact validation.
- Policy and requirement text that admits the store and keeps Task
  ownership.

## Non-Goals & Out-of-Scope

Cross-machine synchronization, importing existing native memory, a new QA
gate for the store, and a filesystem quota.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-MEMORY-001](spec.md#success-criteria--verification-plan) | Store module, CLI and Git ignore entry | None | [Task](tasks/tsk-0001-shared-workspace-memory.md) | Focused store tests and staged QA |
| WORK-002 | [VAL-MEMORY-002](spec.md#success-criteria--verification-plan) | Native memory disablement and validation | None | [Task](tasks/tsk-0001-shared-workspace-memory.md) | Governance tests, validator and staged QA; native sessions observed separately |
| WORK-003 | [VAL-MEMORY-001](spec.md#success-criteria--verification-plan) | Memory policy and requirement revision | WORK-001 | [Task](tasks/tsk-0001-shared-workspace-memory.md) | Document validators and staged QA |

## Verification Plan

Each work unit records a failing focused case before repair and its passing
result, then `qa.py staged` from the documented validation environment.
VAL-MEMORY-002 needs two real provider sessions; static checks alone leave
it pending.

## Risks & Mitigations

- Losing native recall: files stay in place and the shared store replaces
  them for new entries.
- Unsafe concurrency: rollback journal, `BEGIN IMMEDIATE` and a bounded busy
  timeout.
- Second database: the store is never created implicitly; only `init`
  creates it at the resolved root.

## Completion Criteria

VAL-MEMORY-001 accepted on focused evidence; VAL-MEMORY-002 accepted only
after the cross-provider observation, otherwise left pending with its owner.
