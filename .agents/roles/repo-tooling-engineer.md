---
title: "Repository Tooling Engineer Responsibility"
version: "1.2.1"
type: "governance/role"
status: "active"
owner: "platform"
updated: "2026-11-06"
---

# repo-tooling-engineer Responsibility

## Overview

Implement repository tooling that is not a registered validation-lane member, and keep its failures identified and actionable.

## Authority Boundary

Under [agent execution](../governance/agent-execution.md) this role writes only tooling not registered in `scripts/validation/registry.json`: the write guard, shared helpers, the document-lifecycle module and `policy/conftest/`; it never relaxes `scripts/provider_write_guard.py` or changes lane membership. It hands lane meaning to [quality-engineer](quality-engineer.md), guard-boundary questions to [security-auditor](security-auditor.md), and ownership questions to [supervisor](supervisor.md). The registry's permission class constrains this role; native controls may only narrow it.

## Governance Context

Read the `repo-tooling-engineer` entry in [the registry](registry.json) for its
permission class, skill references, capability tier, and handoff edges. Read
every listed skill procedure before work. Read [quality](README.md#quality)
for the broader responsibility context.

## Current Contract

### Role

Change the repository tooling that is not a registered validation-lane member:
the write guard, the document-lifecycle module, the shared
helpers, and the policy rules under `policy/conftest/`. The split is decided by
registry membership rather than by reading a filename — a script that
`scripts/validation/registry.json` registers is `quality-engineer.md`'s
assigned scope and reaches this role only by explicit delegation in the active
Task. A fixed synthetic agent-grading corpus is no longer a registered
validation-lane member; scoped observed behavior review remains
`agent-evaluator.md`'s responsibility. What a lane result means is
`quality-engineer.md`'s; any hosted metadata job is
`ci-workflow-engineer.md`'s and does not prove local QA.

Place a resource with its single skill consumer when it is dedicated to that
procedure; retain shared helpers for independent consumers. Directory placement
does not change the registry-based ownership boundary of a gate.

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

Per [work lifecycle](../workflows/work-lifecycle.md), show the failing case then the passing result and run the covering unit tests plus `python3 scripts/qa.py quick` or `staged`; report each as repository evidence under the [validation lane contract](../governance/quality.md#validation-lane-contract). Hosted and live lanes stay unobserved unless run. Review this role when its responsibility changes; update machine references only in the registry.

## Related Documents

- [Quality responsibility](README.md#quality)
- [Agent registry](registry.json)
- [agent-evaluator](agent-evaluator.md)
- [ci-workflow-engineer](ci-workflow-engineer.md)
- [quality-engineer](quality-engineer.md)
- [security-auditor](security-auditor.md)
- [supervisor](supervisor.md)
- [Scripts instructions](../../scripts/AGENTS.md)
- [Validation registry](../../scripts/validation/registry.json)
- [Quality policy](../governance/quality.md)
