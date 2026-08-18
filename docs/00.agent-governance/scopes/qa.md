---
title: 'QA Scope'
type: governance/reference
status: active
owner: platform
updated: 2026-07-29
---

# QA Scope

## Overview

Persona: QA Engineer

## Authority Boundary

### File Ownership

| Path                                    | Owner                       | Notes                                                                                                                        |
| --------------------------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `tests/**`                              | quality-engineer            | Deterministic fixtures and focused regression tests                                                                          |
| `scripts/validate-*.py`                 | quality-engineer            | Python validation gates within an explicitly delegated QA task                                                               |
| `docs/00.agent-governance/contracts/**` | platform + quality-engineer | Contract fixtures and evaluation evidence only; policy remains platform-owned                                                |
| `.github/workflows/**`                  | meta + quality-engineer     | Lane content only — which validators run and how they are invoked. Meta owns the workflow surface, triggers, and permissions |
| `.github/requirements/**`               | meta + quality-engineer     | Pinned Python dependencies for the CI validation lane, on the same split                                                     |

The `quality-engineer` may read plans, tasks, incidents, operations guides,
infrastructure tests, shell validators, CI workflows, and manifests as QA
inputs, but those paths are not writable through this scope. It does **not**
own `gitops/` manifests, product implementation, security sign-off, shell
validators, or Stage 00 policy prose. CI workflows are the one shared surface:
`quality-engineer` may change which validators a lane runs and how they are
invoked, while the workflow surface itself — triggers, permissions, concurrency,
and every non-lane job — remains meta-owned. Broader authoring requires
a separately approved owner and scope change; a task instruction alone cannot
expand this contract.

## Governance Context

### Source of Truth

- Acceptance criteria in the owning Spec, Plan, and Task
- `tests/**`
- `scripts/validate-*.py`
- `docs/00.agent-governance/contracts/agent-evaluations.json`
- `docs/00.agent-governance/contracts/agent-roster-admission.json`

## Current Contract

### Responsibilities

- Define and execute verification paths for planned work.
- Keep test evidence and defect records traceable.
- Validate that delivered behavior matches stage artifacts.
- Review QA/CI reference guides and hand documentation changes to
  `doc-writer`.
- Treat shell validators and CI workflows as read-only evidence unless their
  owning scope explicitly delegates a separate change.
- Enforce 90% coverage policy for testable application code (or validation-matrix coverage for infrastructure) when reviewing verification evidence.

### Subagent Bridge

`quality-engineer` is the dedicated bounded QA subagent. It owns deterministic
fixture design, Python validator work, validation-lane selection, and result
classification within the exact admitted paths above. `k8s-implementer`
retains implementation postflight responsibilities but does not replace
independent QA review.

Subagent dispatch: follow the [Subagent Protocol](../subagent-protocol.md); never
inline a full role definition when an applicable native or local adapter exists.

## Validation and Refresh

### Definition of Done

- Test strategy is aligned to plan and task artifacts.
- Regression coverage is explicitly documented.
- 90% coverage target is maintained for testable application code, or validation-matrix coverage is verified for infrastructure changes.
- Defects are recorded in the proper incident/task channels.

## Related Documents

- [Quality Standards](../rules/quality-standards.md)
- [CI/CD & QA Reference Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Stage Authoring Matrix](../rules/document-authoring.md)
- [Persona Protocol](../rules/persona.md)
