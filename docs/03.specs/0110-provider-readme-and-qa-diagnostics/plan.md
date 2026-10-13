---
title: "Provider README Language and QA Tool Diagnostics Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "in-review"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0110-PLAN-0001"
parent_ids: ["SPEC-0110"]
---

# Provider README Language and QA Tool Diagnostics Implementation Plan

## Global Constraints

- Keep headings, links, role IDs and native values; translate prose only.
- A missing tool stays a FAIL; only its diagnostic becomes visible.
- No remote ruleset, workflow or publication change.

## Overview

This plan executes [SPEC-0110](spec.md) on branch
`feat/task-summary-roles-ko` after the approved SPEC-0108 commits.

## Context

Two read-only investigations on 2026-10-13 found that the local style gates
fail because `/usr/bin/python3` lacks `pre_commit`, not because of PATH,
and that the lane runner withholds the reason. The documented validation
environment was built with `uv` from the hashed lock because the system
Python lacks `ensurepip`.

## Goals & In-Scope

- Translate the eight pending READMEs.
- Surface the missing-tool cause in the style and nonstyle gates.
- Record keep decisions for findings already satisfied.

## Non-Goals & Out-of-Scope

Shared memory, native memory disablement and Codex `config.toml`
([SPEC-0109](../0109-shared-workspace-memory/spec.md)); splitting the PR
title check into another required workflow.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PRQA-001](spec.md#success-criteria--verification-plan) | Translate the eight pending READMEs | None | [Task](tasks/tsk-0001-provider-readme-and-qa-diagnostics.md) | Profile validator and staged QA |
| WORK-002 | [VAL-PRQA-002](spec.md#success-criteria--verification-plan) | Missing-tool diagnostics and README sentence | None | [Task](tasks/tsk-0001-provider-readme-and-qa-diagnostics.md) | Focused tests and staged QA |
| WORK-003 | [VAL-PRQA-003](spec.md#success-criteria--verification-plan) | Record keep decisions for satisfied findings | None | [Task](tasks/tsk-0001-provider-readme-and-qa-diagnostics.md) | Source review recorded in the Task |

## Verification Plan

Each work unit runs its focused check, then `qa.py staged` from the
validation environment on the exact index before commit.

## Risks & Mitigations

- Passing tool output through could leak content: only the fixed label form
  is admitted.
- Translation drift: headings and links are compared against the previous
  version.

## Completion Criteria

All three criteria have concrete PASS evidence and an accepted decision in
the Task; hosted CI and push remain separate operator actions.
