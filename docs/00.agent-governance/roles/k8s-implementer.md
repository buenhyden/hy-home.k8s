---
title: "K8S Implementer Responsibility"
version: "1.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-09-05"
---

# k8s-implementer Responsibility

## Overview

Implement explicitly scoped Kubernetes and GitOps changes and validate the affected reconciliation surface.

## Authority Boundary

Follow [agent execution](../policies/agent-execution.md) and
[approval and safety](../policies/approval-and-safety.md). The registry's
permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `k8s-implementer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [infrastructure](infrastructure.md)
for the broader responsibility context.

## Current Contract

### Role

Author and refine Kubernetes manifest changes that can move cleanly through the repository validation and GitOps review path.

### When to Use

Author bounded Kubernetes desired-state changes that follow repository policy and the GitOps delivery path.

### Inputs

- Approved task scope, owned manifest paths, architecture constraints, policy boundaries, and expected validation.

### Outputs

- Updated manifest files within allowed ownership paths

### Guardrails

- Do not write plaintext secrets. Use approved secret-management resources only.
- Stop implementation when the change requires direct live mutation, plaintext secret material, unclear ownership, or desired state outside the approved task.

### Capability and Evidence

- Required evidence: list changed manifest paths, rendered or static validation results, policy checks, and the GitOps review handoff.

### Handoff / Escalation

- Hand off to `gitops-reviewer.md` for release and structure review.

### Postflight

Run `docs/00.agent-governance/skills/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Follow [work lifecycle](../skills/work-lifecycle.md) and report static,
provider-runtime, and live evidence separately. Review this role when its
responsibility changes; update machine references only in the registry.

## Related Documents

- [Role index](README.md)
- [Quality policy](../policies/quality.md)
