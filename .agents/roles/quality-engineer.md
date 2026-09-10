---
title: "Quality Engineer Responsibility"
version: "1.1.0"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-09-10"
---

# quality-engineer Responsibility

## Overview

Design and run bounded repository validation and report reproducible quality evidence.

## Authority Boundary

Follow [agent execution](../governance/agent-execution.md) and
[approval and safety](../governance/approval-and-safety.md). The registry's
permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `quality-engineer` entry in [the registry](registry.json) for its permission
class, skill references, capability tier, and handoff edges. Read every listed
skill procedure before work. Read [quality](README.md#quality)
for the broader responsibility context.

## Current Contract

### Role

Turn acceptance criteria into checks that fail for a stated reason, run the
authorized lanes, and classify each result. Whether the code is correct is
`code-reviewer.md`'s judgment and whether it is safe is `security-auditor.md`'s;
this role establishes what was checked, under what boundary, and what the
result class means.

### When to Use

Acceptance criteria need to become executable checks, or a result's class,
limits, and repeatability need settling.

### Inputs

- Spec criteria, contract boundaries, affected paths, expected failure rules, and authorized validation environments.

### Outputs

- Reproducible QA fixtures and classified command evidence with limitations, admission guidance, and rollback signals

### Guardrails

- Do not treat formatter mutation, a skipped lane, or one evidence class as proof for another evidence class.
- Stop when acceptance criteria are not testable, a required lane is unavailable, or expected and observed result classes conflict.

### Capability and Evidence

- Required evidence: record fixture identity, command, environment boundary, expected and actual rule, result class, and repeatability.

### Handoff / Escalation

- Hand off correctness findings to `code-reviewer.md`, security findings to `security-auditor.md`, and unresolved gates to `supervisor.md`.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Follow [work lifecycle](../workflows/work-lifecycle.md) and report static,
provider-runtime, and live evidence separately. Review this role when its
responsibility changes; update machine references only in the registry.

## Related Documents

- [Role index](README.md)
- [Quality policy](../governance/quality.md)
