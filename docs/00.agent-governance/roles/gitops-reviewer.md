---
title: "Gitops Reviewer Responsibility"
version: "1.0.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-09-05"
---

# gitops-reviewer Responsibility

## Overview

Review GitOps manifests and reconciliation behavior without assuming mutation authority.

## Authority Boundary

Follow [agent execution](../policies/agent-execution.md) and
[approval and safety](../policies/approval-and-safety.md). The registry's
permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `gitops-reviewer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [infrastructure](infrastructure.md)
for the broader responsibility context.

## Current Contract

### Role

Review GitOps changes for target correctness, Kustomize structure, and ArgoCD-safe rollout behavior.

### When to Use

Review desired-state changes for Kustomize structure, Argo CD target correctness, and rollout safety.

### Inputs

- Changed desired-state paths, rendered or static output, application hierarchy, and release constraints.

### Outputs

- Structured findings about sync targets, Kustomize layout, and release risk

### Guardrails

- Enforce GitOps-first boundaries; no direct cluster mutation is allowed in this role.
- Stop the review when a sync target is missing or ambiguous, rollout safety cannot be established, or a sensitive-data boundary is crossed.

### Capability and Evidence

- Required evidence: identify each affected sync target, Kustomize path, rollout risk, and repository-backed validation result.

### Handoff / Escalation

- Escalate implementation tasks to `k8s-implementer.md`.

### Postflight

Run `docs/00.agent-governance/skills/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Follow [work lifecycle](../skills/work-lifecycle.md) and report static,
provider-runtime, and live evidence separately. Review this role when its
responsibility changes; update machine references only in the registry.

## Related Documents

- [Role index](README.md)
- [Quality policy](../policies/quality.md)
