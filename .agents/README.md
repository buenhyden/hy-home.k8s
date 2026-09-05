---
title: "Common Agent Governance"
version: "1.0.0"
type: "common/readme-implementation"
status: "active"
owner: "platform"
updated: "2026-09-06"
---

# Common Agent Governance

## Overview

This is the single common policy, role and skill authority for this GitOps
workspace. Its files are read through explicit gateways or native skill
loaders; the entire directory is not an automatic instruction loader.

## Structure

| Path | Responsibility |
| --- | --- |
| [governance/sdlc.md](governance/sdlc.md) | Normative lifecycle and terminology |
| `governance/` | Approval, safety, quality, Git, documents, context and model policy |
| [roles/README.md](roles/README.md) | Responsibility selection and common handoff contracts |
| [roles/registry.json](roles/registry.json) | Role IDs, permissions, skill references and native paths |
| `skills/<id>/SKILL.md` | Callable common procedures; registry determines the package set |
| `workflows/` | Ordinary lifecycle/delegation procedures, explicitly read |

## Configuration Boundary

Provider differences and native adapters live in [.claude/](../.claude/README.md)
and [.codex/](../.codex/README.md). Edit common meaning here; retain native syntax
there. No role copies or provider generator own a second policy. Optional
memory, rule, prompt and script directories are not adopted. MIG-0009's memory
retirement remains effective.

## Validation

Run `python3 scripts/validate-agent-governance.py --root .` for role, skill,
permission and routing contracts; run `python3 scripts/qa.py full` for final
repository-static evidence. No generator is used. Native discovery, invocation,
permissions and hook delivery require separate evidence from a fresh session.

## Operations

Read [work lifecycle](workflows/work-lifecycle.md),
[agent execution](governance/agent-execution.md) and
[approval and safety](governance/approval-and-safety.md) before acting. Select
[roles](roles/README.md), then explicitly read the chosen role and its required
skills. Both providers expose the same common skill packages for explicit
invocation. A skill does not grant permission to write, send, deploy or read
secrets. [Quality](governance/quality.md) owns evidence semantics, while the
execution registry owns mutable gate commands and limits.

## Related Documents

- [Document profiles and templates](../docs/99.templates/README.md)
- [Repository documentation](../docs/README.md)
- [Memory retirement](../docs/98.archive/migrations/0009-governance-memory-retirement.md)
- [Authority decision](../docs/02.architecture/decisions/0035-common-agents-authority-and-native-skill-routing.md)
