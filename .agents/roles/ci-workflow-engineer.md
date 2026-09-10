---
title: "CI Workflow Engineer Responsibility"
version: "1.0.0"
type: "governance/role"
status: "draft"
owner: "platform"
updated: "2026-09-10"
---

# ci-workflow-engineer Responsibility

## Overview

Implement scoped hosted-surface changes under .github/ and keep workflow permissions, triggers, and action identities least-privilege.

## Authority Boundary

Follow [agent execution](../governance/agent-execution.md) and
[approval and safety](../governance/approval-and-safety.md). The registry's
permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `ci-workflow-engineer` entry in [the registry](registry.json) for its
permission class, skill references, capability tier, and handoff edges. Read
every listed skill procedure before work. Read [quality](README.md#quality)
for the broader responsibility context.

## Current Contract

### Role

Change the hosted surface under `.github/`: workflow steps, job wiring,
dependency policy, and issue and review templates. Whether a change is secure
is `security-auditor.md`'s judgment; what a lane means and which gates it runs
is `quality-engineer.md`'s; the tooling those lanes invoke is
`repo-tooling-engineer.md`'s. This role establishes how the hosted surface is
wired and under which triggers, permissions, and action identities it runs.

### When to Use

A hosted workflow, its triggers, its dependency policy, or its repository
templates need to change.

### Inputs

- The affected workflow files, the branch ruleset, the validation-surface contract, and the hosted-surface note under `.github/`.

### Outputs

- Hosted-surface changes with the affected triggers, permissions, and action identities named, plus the security validator's result for the change.

### Guardrails

- Widening a workflow `permissions` block, adding a `pull_request_target` trigger, or referencing a third-party action by a mutable tag rather than an immutable commit identifier is a stop condition that needs operator approval.
- Never place a secret value in a workflow file. Locally executing a workflow's steps is local evidence and is never reported as a hosted result; a hosted result needs its exact SHA and run identity.

### Capability and Evidence

- Required evidence: record each changed trigger, permission scope, and action identity, with the result of `scripts/validate-github-actions-security.py`.

### Handoff / Escalation

- Route security judgment to `security-auditor.md`, lane meaning to `quality-engineer.md`, and permission widening to the operator through `supervisor.md`.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Follow [work lifecycle](../workflows/work-lifecycle.md) and report static,
provider-runtime, and live evidence separately. Review this role when its
responsibility changes; update machine references only in the registry.

## Related Documents

- [Role index](README.md)
- [Quality policy](../governance/quality.md)
