---
title: "Pinned Package Fixtures in Lifecycle Tests Plan"
version: "0.1.0"
type: "sdlc/plan"
status: "approved"
owner: "platform"
updated: "2026-10-13"
layer: "specs"
artifact_id: "SPEC-0112-PLAN-0001"
parent_ids: ["SPEC-0112"]
---

# Pinned Package Fixtures in Lifecycle Tests Implementation Plan

## Global Constraints

- Change tests only; never remove or loosen an assertion.

## Overview

This plan executes [SPEC-0112](spec.md) on branch `fix/live-fixture-reads`
from main `bceca1b7`.

## Context

The SPEC-0111 review listed the three remaining working-tree reads of
completed package documents.

## Goals & In-Scope

Pin the three package reads to Git objects.

## Non-Goals & Out-of-Scope

Live Registry, schema and template reads; archiving any package.

## Work Breakdown

### Lifecycle Traceability

| Work Unit | Criteria | Work | Dependencies | Task | Verification |
| --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-PIN-001](spec.md#success-criteria--verification-plan) | Pin the three package reads | None | [Task](tasks/tsk-0001-pinned-package-fixtures.md) | Archive simulation, focused tests and staged QA |

## Verification Plan

Record the failing run with the packages moved in a scratch clone, the
passing run after the change there and in the repository, then
`qa.py staged` on the exact index.

## Risks & Mitigations

- A stale pin could hide a later contract change: the Registry and
  validators stay live, so contract changes still reach these tests.

## Completion Criteria

The criterion has PASS evidence and an accepted decision in the Task; push
and pull request remain operator actions.
