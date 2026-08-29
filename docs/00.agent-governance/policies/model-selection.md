---
title: 'Model Selection Policy'
type: governance/reference
status: active
owner: platform
updated: 2026-08-28
---

# Model Selection Policy

## Overview

Use capability appropriate to the task without turning model age, role names,
or static configuration into claims of observed fitness.

## Authority Boundary

The [agent registry](../../../.agents/registry.json) owns each role's
capability-tier reference. This policy defines the tier meanings and escalation
boundary. Claude and Codex native configuration owns configured model and
reasoning values; it does not prove availability, entitlement, resolution, or
execution.

## Governance Context

Capability, permissions, and responsibility are independent. Escalating a
bounded task to a stronger permitted model does not grant new tools, writes,
delegation, or approval, and does not change the role's registry membership.

## Current Contract

### Top

Use the strongest permitted capability for high-risk synthesis, orchestration,
or complex security and incident judgment. The stable anchor is `#top`;
resolve membership from the registry rather than inferring it from a role name.

### Worker

Use a bounded capable model for focused implementation, documentation,
validation, or review. The stable anchor is `#worker`; a difficult assignment
may justify explicit escalation without reclassifying the role.

### Selection and escalation

- Preserve configured native model and effort values during a documentation
  or routing change. Model promotion requires separately authorized scope and
  task-relevant evidence.
- Shared reasoning intent is not a universal provider enum. Check the intended
  client's supported native configuration when a model or effort change is
  actually requested.
- Record the selection rationale, expected quality/cost boundary, and any
  unavailable runtime verification in the owning Task.
- Do not maintain dated per-model fitness snapshots, branch pins, or copied
  role censuses as current policy. Evidence belongs to its dated owner and
  cannot promote static configuration into runtime success.

## Validation and Refresh

Validate registry tier references and provider-native metadata after changes.
Assess model behavior with authorized, secret-free task evidence before
claiming improved fitness or successful provider resolution.

## Related Documents

- [Agent Registry](../../../.agents/registry.json)
- [Codex Provider](../providers/codex.md)
- [Claude Provider](../providers/claude.md)
- [Quality Policy](quality.md)
