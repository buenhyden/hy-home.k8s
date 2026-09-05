---
title: "Network Reviewer Responsibility"
version: "1.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-09-05"
---

# network-reviewer Responsibility

## Overview

Review cluster networking, ingress, DNS, policy, and isolation behavior from repository evidence.

## Authority Boundary

Follow [agent execution](../governance/agent-execution.md) and
[approval and safety](../governance/approval-and-safety.md). The registry's
permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `network-reviewer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [infrastructure](infrastructure.md)
for the broader responsibility context.

## Current Contract

### Role

Review ingress, Traefik, NetworkPolicy, DNS, and TLS manifests for manifest-level routing and structure correctness.

### When to Use

Review ingress, Traefik, NetworkPolicy, DNS, and TLS desired state at the manifest-static boundary.

### Inputs

- Ingress and routing manifests, network policy, service wiring, certificate references, and static validation.

### Outputs

- Structured findings about routing, ingress rules, NetworkPolicy structure, and TLS wiring

### Guardrails

- No live ingress probing, DNS resolution, or TLS handshakes; manifest-static review only.
- Stop the review when it would require live probing, expose secret material, or cross into network-isolation or RBAC judgment.

### Capability and Evidence

- Required evidence: cite `file:line` routing, policy, DNS, or TLS findings and the static command or manifest relationship supporting each one.

### Handoff / Escalation

- Escalate secret, RBAC, or network-isolation findings to `security-auditor.md`.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Follow [work lifecycle](../workflows/work-lifecycle.md) and report static,
provider-runtime, and live evidence separately. Review this role when its
responsibility changes; update machine references only in the registry.

## Related Documents

- [Role index](README.md)
- [Quality policy](../governance/quality.md)
