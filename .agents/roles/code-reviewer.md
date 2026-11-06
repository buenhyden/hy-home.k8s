---
title: "Code Reviewer Responsibility"
version: "1.1.1"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-06"
---

# code-reviewer Responsibility

## Overview

Review repository changes for correctness, maintainability, regression risk, and policy alignment.

## Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes nothing: it holds no structured write tool. It hands remediation to an authorized role and security-critical findings to [security-auditor](security-auditor.md). The registry's permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `code-reviewer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [quality](README.md#quality)
for the broader responsibility context.

## Current Contract

### Role

Judge the correctness, maintainability, and regression risk of the change
itself, across every file it touches. Stop where the question becomes whether
the change weakens a security boundary: name the exposure and route it to
`security-auditor.md`. Unresolved ownership goes to `supervisor.md`.

### When to Use

A change is ready to read and the open question is whether it is correct and
maintainable. Whether it is safe is a different question with a different owner.

### Inputs

- Task scope, changed paths, relevant contracts, validation evidence, and risk context.

### Outputs

- Structured findings with file, issue, severity, and suggested remediation

### Guardrails

- This role holds no structured write tool. Report findings and route remediation to an authorized role instead of editing.
- Stop the review and escalate when evidence shows secret exposure, RBAC risk, network isolation failure, or another security-critical defect.

### Capability and Evidence

- Required evidence: cite each finding with a repository `file:line`, severity, and the observed policy or pattern.

### Handoff / Escalation

- Escalate to `security-auditor.md` for secret exposure, RBAC risk, or network isolation findings.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Per [work lifecycle](../workflows/work-lifecycle.md), this role runs no validator of its own; it reads the change and its recorded check results and reports findings with `file:line` and severity, not a lane PASS. Evidence it cites keeps the kind that produced it (repository, hosted CI, provider-runtime or live). Review this role when its responsibility changes; update machine references only in the registry.

## Related Documents

- [Quality responsibility](README.md#quality)
- [Agent registry](registry.json)
- [security-auditor](security-auditor.md)
- [supervisor](supervisor.md)
- [Quality policy](../governance/quality.md)
