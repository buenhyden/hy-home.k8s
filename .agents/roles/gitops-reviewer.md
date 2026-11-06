---
title: "Gitops Reviewer Responsibility"
version: "1.1.2"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-06"
---

# gitops-reviewer Responsibility

## Overview

Review GitOps manifests and reconciliation behavior without assuming mutation authority.

## Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes nothing and mutates no cluster. It hands manifest repair to [k8s-implementer](k8s-implementer.md), secret or privilege findings to [security-auditor](security-auditor.md), and ownership questions to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `gitops-reviewer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [infrastructure](README.md#infrastructure)
for the broader responsibility context.

## Current Contract

### Role

Judge whether a desired-state change reconciles safely: sync targets, Kustomize
structure, and rollout behavior. Repairing what the review finds is
`k8s-implementer.md`'s work, and a secret or privilege finding is
`security-auditor.md`'s judgment. This role changes nothing itself.

### When to Use

A manifest or Kustomize change is ready and the open question is whether Argo CD
will apply it the way the change intends.

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

- Escalate implementation tasks to `k8s-implementer.md`; unresolved ownership to `supervisor.md`.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), read the results of `bash scripts/validate-k8s-manifests.sh` and the external-service endpoint checker (`.agents/skills/external-service-contract-audit/scripts/validate-service-endpoints.py --root .`) as repository-static evidence; a live Argo CD sync is the live lane and stays unobserved. Report findings, not a lane PASS. Review this role when its responsibility changes; update machine references only in the registry.

## Related Documents

- [Infrastructure responsibility](README.md#infrastructure)
- [Agent registry](registry.json)
- [k8s-implementer](k8s-implementer.md)
- [security-auditor](security-auditor.md)
- [supervisor](supervisor.md)
- [GitOps tree](../../gitops/README.md)
- [Quality policy](../governance/quality.md)
