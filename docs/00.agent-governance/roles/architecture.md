---
title: "Architecture Responsibility"
version: "1.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-08-28"
---

# Architecture Responsibility

## Overview

Keep system structure and important decisions consistent with durable requirements and change-specific contracts.

## Authority Boundary

Architecture Descriptions and ADRs own structural views and durable choices. A Spec owns change-specific behavior. This responsibility does not own infrastructure manifests or Stage 00 policy.

## Governance Context

Review stakeholder concerns, boundaries, data flows, deployment views, quality attributes, alternatives, and consequences.

## Current Contract

- Trace structural changes to complete Requirement Package IDs and affected Specs.
- Use a successor ADR for a changed accepted decision; retain superseded ADRs in the decision log.
- Hand implementation, operational, and security consequences to their responsible owners. Do not claim ownership of all documentation.

## Validation and Refresh

Record evidence and handoff through [quality policy](../policies/quality.md).
Reassess responsibility when the active Task changes scope; exact role,
permission, skill, and handoff membership stays in the agent registry.

## Related Documents

- [Roles Router](README.md)
- [Architecture Index](../../02.architecture/README.md)
- [Agent Registry](../../../.agents/registry.json)
