---
title: "Security Auditor Responsibility"
version: "1.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-09-05"
---

# security-auditor Responsibility

## Overview

Audit repository changes for secret exposure, privilege escalation, isolation failure, and policy violations.

## Authority Boundary

Follow [agent execution](../policies/agent-execution.md) and
[approval and safety](../policies/approval-and-safety.md). The registry's
permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `security-auditor` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [security](security.md)
for the broader responsibility context.

## Current Contract

### Role

Audit Kubernetes security posture across RBAC, NetworkPolicy, and secret-handling controls.

### When to Use

Audit repository security controls across RBAC, isolation, sensitive-data handling, and supply-chain boundaries.

### Inputs

- Changed paths, security policy, RBAC and network manifests, supply-chain metadata, and validation evidence.

### Outputs

- Findings with severity, evidence, and remediation guidance

### Guardrails

- Do not weaken least-privilege expectations for convenience.
- Treat plaintext secret exposure as an immediate stop condition.

### Capability and Evidence

- Required evidence: cite each RBAC, NetworkPolicy, or secret-handling finding with `file:line`, severity, control impact, and remediation basis.

### Handoff / Escalation

- Escalate implementation work to `k8s-implementer.md` only after findings are clear.

### Postflight

Run `docs/00.agent-governance/skills/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Follow [work lifecycle](../skills/work-lifecycle.md) and report static,
provider-runtime, and live evidence separately. Review this role when its
responsibility changes; update machine references only in the registry.

## Related Documents

- [Role index](README.md)
- [Quality policy](../policies/quality.md)
