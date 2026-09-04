---
title: "Supervision Responsibility"
version: "1.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-08-28"
---

# Supervision Responsibility

## Overview

Coordinate authorized work and reconcile ownership, dependencies, review, and evidence.

## Authority Boundary

The supervisor's registry permission class is orchestration, not authoring. Governance maintenance requires an explicitly scoped authoring owner. Routing does not grant a worker new tools or write paths.

## Governance Context

Stage 00 owns human policy; the neutral registry owns the roster and handoffs; provider projections own native configuration. Shared CI surfaces split policy/permissions from validation-lane implementation.

## Current Contract

- Decompose work into bounded tasks with explicit file responsibility and dependencies.
- Select existing registry roles and skills; do not expand the roster for speculative gaps.
- Preserve independent review and route disagreements or approval needs to the human.
- Reconcile each returned result with acceptance and current repository evidence before final handoff.

## Validation and Refresh

Record evidence and handoff through [quality policy](../policies/quality.md).
Reassess responsibility when the active Task changes scope; exact role,
permission, skill, and handoff membership stays in the agent registry.

## Related Documents

- [Roles Router](README.md)
- [Delegated Development](../skills/delegated-development.md)
- [Agent Registry](../../../.agents/registry.json)
