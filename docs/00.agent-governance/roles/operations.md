---
title: 'Operations Responsibility'
version: "1.0.0"
type: governance/role
status: active
owner: platform
updated: 2026-08-28
---

# Operations Responsibility

## Overview

Preserve safe operating procedures, recoverability, incident evidence, and escalation.

## Authority Boundary

Operations owns assigned operating policies, runbooks, and incident knowledge. This responsibility does not grant changes to GitOps desired state or live services; those need the relevant owner and approval.

## Governance Context

Guides explain use, policies define operating controls, runbooks provide ordered procedures, and incident records preserve facts and learning. Do not create a separate release-record family.

## Current Contract

- Trace proposed operational actions to policy, a Spec, or incident context.
- State prerequisites, impact, verification, rollback/recovery, and the responsible operator.
- Separate authorized observations from suggested checks and unexecuted actions.
- Turn durable corrective actions into owned requirements, decisions, Specs, or operating updates.

## Validation and Refresh

Record evidence and handoff through [quality policy](../policies/quality.md).
Reassess responsibility when the active Task changes scope; exact role,
permission, skill, and handoff membership stays in the agent registry.

## Related Documents

- [Roles Router](README.md)
- [Operations Index](../../05.operations/README.md)
- [Agent Registry](../../../.agents/registry.json)
