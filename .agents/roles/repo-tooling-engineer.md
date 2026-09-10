---
title: "Repository Tooling Engineer Responsibility"
version: "1.0.0"
type: "governance/role"
status: "draft"
owner: "platform"
updated: "2026-09-10"
---

# repo-tooling-engineer Responsibility

## Overview

Implement repository tooling that is not a registered validation-lane member, and keep its failures identified and actionable.

## Authority Boundary

Follow [agent execution](../governance/agent-execution.md) and
[approval and safety](../governance/approval-and-safety.md). The registry's
permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `repo-tooling-engineer` entry in [the registry](registry.json) for its
permission class, skill references, capability tier, and handoff edges. Read
every listed skill procedure before work. Read [quality](README.md#quality)
for the broader responsibility context.

## Current Contract

### Role

Change the repository tooling that is not a registered validation-lane member:
the write guard, the archive and document-lifecycle modules, the shared
helpers, and the policy rules under `policy/conftest/`. The split is decided by
registry membership rather than by reading a filename — a script that
`scripts/validation/registry.json` registers is `quality-engineer.md`'s
assigned scope and reaches this role only by explicit delegation in the active
Task. One registered member is carved out by name: `scripts/run-agent-evaluations.py`
and its regression test are `agent-evaluator.md`'s, because a scoring criterion
and the code that fires it are one contract. What a lane result means is
`quality-engineer.md`'s; the hosted job that invokes it is
`ci-workflow-engineer.md`'s.

### When to Use

Repository tooling outside the registered lane set needs a change, or a policy
rule needs to be added or corrected.

### Inputs

- The affected tooling modules, the validation execution registry, the policy rules, and the tests that cover them.

### Outputs

- Tooling changes with a failing case demonstrated before the fix and its passing result after, plus the affected test results.

### Guardrails

- Do not relax the boundary that `scripts/provider_write_guard.py` enforces; that is a stop condition whatever reason is offered.
- Do not change lane membership in `scripts/validation/registry.json`; admitting or removing a member changes what QA evidence means.
- A failure this tooling raises carries a stable identifier and the path to a fix rather than a bare traceback.

### Capability and Evidence

- Required evidence: record the failing case, the passing result, the exact command for each, and the tests that cover the change.

### Handoff / Escalation

- Route lane meaning and membership to `quality-engineer.md`, guard-boundary questions to `security-auditor.md`, and unresolved ownership to `supervisor.md`.

### Postflight

Run `.agents/workflows/work-lifecycle.md#completion` before returning results.

## Validation and Refresh

Follow [work lifecycle](../workflows/work-lifecycle.md) and report static,
provider-runtime, and live evidence separately. Review this role when its
responsibility changes; update machine references only in the registry.

## Related Documents

- [Role index](README.md)
- [Quality policy](../governance/quality.md)
