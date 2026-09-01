---
title: 'Infrastructure Responsibility'
version: "1.0"
type: governance/reference
layer: "00.agent-governance"
status: active
owner: platform
updated: 2026-08-28
---

# Infrastructure Responsibility

## Overview

Keep Kubernetes and GitOps desired state reproducible, isolated, and aligned with approved system contracts.

## Authority Boundary

Scoped implementation may cover assigned infrastructure or GitOps manifests and their automation. Review roles remain read-only. This responsibility grants no live mutation and does not own upstream requirements or governance.

## Governance Context

The local cluster assets are under infrastructure, and GitOps reconciliation begins at gitops/clusters/local/root-application.yaml. Operations policy and runbooks describe the operating boundary.

## Current Contract

- Preserve secure secret-reference handling and network isolation.
- Validate affected manifest syntax, policy, and reconciliation structure using repository checks.
- Record operational effects and rollback in the owning Plan/Task and hand runbook changes to operations.
- Keep cluster bring-up and reconciliation operator-bound under explicit approval.

## Validation and Refresh

Record evidence and handoff through [quality policy](../policies/quality.md).
Reassess responsibility when the active Task changes scope; exact role,
permission, skill, and handoff membership stays in the agent registry.

## Related Documents

- [Roles Router](README.md)
- [Approval and Safety](../policies/approval-and-safety.md)
- [Agent Registry](../../../.agents/registry.json)
