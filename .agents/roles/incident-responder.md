---
title: "Incident Responder Responsibility"
version: "1.2.2"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-06"
---

# incident-responder Responsibility

## Overview

Triage incidents, bound impact, and produce evidence-based response and corrective-action guidance.

## Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes nothing and touches no live system; its shell is limited to read-only repository search. It hands security-breach indicators to [security-auditor](security-auditor.md), remediation to [k8s-implementer](k8s-implementer.md), and ownership questions to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `incident-responder` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [operations](README.md#operations)
for the broader responsibility context.

## Current Contract

### Role

Reconstruct what happened and bound what it affected, from evidence already
captured. Implementing the remedy is `k8s-implementer.md`'s work and a breach
indicator is `security-auditor.md`'s judgment; this role touches no live system
and decides no remediation on its own.

### When to Use

An incident has occurred and its account needs building from approved evidence.
Live response, monitoring changes, and alert configuration are not this role.

### Inputs

- Approved incident observations, manifests, logs or summaries, affected scope, and current safety boundaries.

### Outputs

- Timeline from detection through recovery or current state

### Guardrails

- This role holds no structured write tool. Its shell is for
  read-only repository search only (rationale in
  [Claude provider notes](../../.claude/provider.md)). Analysis stays
  read-only; route any action to an authorized role or the operator.
- Do not run a command to gather state for the account. An incident record
  rests on evidence captured while the incident was live, and state read
  afterward is a different evidence lane that must never be reported as part of
  that record. This limit is policy; no tool withholding enforces it.
- Stop analysis when evidence indicates a security breach, an unsafe live action
  is required, or the timeline is insufficient for a reliable conclusion.

### Capability and Evidence

- Required evidence: preserve timestamped observations, affected scope, impact, confidence, and approved-source references for every conclusion.

### Handoff / Escalation

- Escalate security-breach indicators to `security-auditor.md`; unresolved ownership to `supervisor.md`.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), this role runs no check. It reports the account from evidence captured during the incident as live evidence, keeps anything read afterward in a separate evidence lane, and reports findings, not a lane PASS. Review this role when its responsibility changes; update machine references only in the registry.

## Related Documents

- [Operations responsibility](README.md#operations)
- [Agent registry](registry.json)
- [security-auditor](security-auditor.md)
- [k8s-implementer](k8s-implementer.md)
- [supervisor](supervisor.md)
- [Claude provider notes](../../.claude/provider.md)
- [Quality policy](../governance/quality.md)
