---
title: 'Delegated Development'
type: governance/reference
status: active
owner: platform
updated: 2026-08-28
---

# Delegated Development

## Overview

Delegate bounded work through a supported runtime mechanism while preserving
responsibility, least privilege, and independent evidence.

## Authority Boundary

The [agent registry](../../../.agents/registry.json) owns exact role IDs,
permission classes, handoff edges, capability-tier references, skill references,
and projection paths. This procedure explains their use without duplicating the
roster or tool inventory.

## Governance Context

Neutral role and skill content lives in `.agents/`; Claude and Codex
projections add native metadata only. Tracked files do not prove that a runtime
discovers, loads, or enforces them. Delegation requires explicit user or
applicable instruction authorization and an available runtime mechanism.

## Current Contract

1. Resolve the role, permission class, skills, and native projection from the
   registry. Read that projection and its imported responsibility owners.
2. Give the worker one concrete task, allowed paths, acceptance IDs,
   dependencies, validation expectations, and next owner. State that other
   workers' changes must be preserved.
3. Treat write scope as the intersection of authorization, registry permission,
   responsibility boundary, and task ownership. Read-only roles remain
   read-only; an orchestration role delegates mutation rather than acquiring it.
4. Do not inline a replacement role definition, expand tools, or silently route
   to an undeclared handoff. Escalate an unresolved responsibility or authority
   conflict to the supervising workflow or human.
5. Run independent tasks concurrently only when their ownership is disjoint;
   serialize dependent implementation and reconcile shared boundaries.
6. Require returning workers to report the
   [quality handoff fields](../policies/quality.md#handoff-evidence-contract).
   Review actual changes and commands; a worker's assertion alone is not
   verification.
7. Keep durable results in the owning Task and bounded temporary coordination
   in approved ignored scratch. Do not create another progress authority.

Subagents never perform live mutation or secret-value operations. A higher
capability tier does not grant broader permission. Provider-native runtime
evidence remains distinct from repository-static projection parity.

## Validation and Refresh

Run registry, projection/config, and semantic/permission checks when a role,
import, permission, handoff, skill, or provider projection changes. Confirm the
actual provider mechanism separately before claiming native delegation.

## Related Documents

- [Roles](../roles/README.md)
- [Model Selection](../policies/model-selection.md)
- [Work Lifecycle](work-lifecycle.md)
- [Approval and Safety](../policies/approval-and-safety.md)
