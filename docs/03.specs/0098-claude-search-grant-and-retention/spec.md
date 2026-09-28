---
title: "Claude Search Grant and Package Retention Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "completed"
owner: "platform"
updated: "2026-09-27"
layer: "specs"
artifact_id: "SPEC-0098"
---

# Claude Search Grant and Package Retention Technical Specification (Spec)

## Overview

On 2026-09-27 the request owner asked for two things: give search to the
Claude roles that have none, and retain the finished packages still waiting
in Stage 03.

- **Search**: [SPEC-0097](../../98.archive/completed/03.specs/0097-claude-model-and-effort-binding/spec.md)
  recorded that native macOS and Linux builds from Claude Code 2.1.117 removed
  the `Grep` and `Glob` tools, moved search into Bash, and drop the unknown
  names silently. Four Claude scopes carried no `Bash`: docs-researcher
  (`read-only-research`), supervisor (`orchestration`), and incident-responder
  and observability-reviewer, which narrowed `read-only-evidence` to drop the
  shell. On a native build those roles cannot search at all.
- **Retention**: SPEC-0095, SPEC-0096, and SPEC-0097 are `done`, and the
  default branch holds their final trees at `fc469fd1`.

## Strategic Boundaries & Non-goals

In scope: the Claude `permission_scopes` for `read-only-research` and
`orchestration`, the two Claude `native_scope_override` entries, the four
projections, the two role guardrails that stated no shell, their tests, the
Claude provider note, the retention of the three packages, and this package.

Out of scope: Codex sandbox modes, which already give every role a search path
through the shell; mutation or delegation rights; network reach; tier or model
bindings; SPEC-0008, which stays `active` by design.

## Contracts

- Every Claude role's resolved scope contains `Bash`. `Grep` and `Glob` stay in
  every scope for the builds that still ship them.
- A shell can write, so a read-only role's restraint is policy that its
  guardrails state, observed advisorily by the write guard. incident-responder
  and observability-reviewer confine the shell to read-only repository search
  and keep their prohibition on live state.
- Retention follows [ADR-0040](../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md):
  each `done` package moves whole to `completed/` under an envelope that the
  default branch reaches, with one catalog row each, and current citations are
  repointed.

## Core Design

| Change | Before | After |
| --- | --- | --- |
| `read-only-research` (Claude) | `Read, Grep, Glob, WebFetch, WebSearch` | `Read, Grep, Glob, Bash, WebFetch, WebSearch` |
| `orchestration` (Claude) | `Read, Grep, Glob, Task` | `Read, Grep, Glob, Bash, Task` |
| incident-responder, observability-reviewer | override `Read, Grep, Glob` | no override; class default `Read, Grep, Glob, Bash` |
| SPEC-0095, SPEC-0096, SPEC-0097 | `docs/03.specs/` | `docs/98.archive/completed/03.specs/`, envelope `fc469fd1` |

## Data Modeling & Storage Strategy

The registry holds the scopes, and each projection restates them. Git holds the
retained bytes, and the catalog row is the only recovery reference.

## Interfaces & Data Structures

Four Claude projections change their `tools`. The Stage 98 index gains three
catalog rows, and the Stage 03 index loses three entries.

## Edge Cases & Error Handling

A Windows or npm build still exposes `Grep` and `Glob`, so a role can search
with them there. A running session keeps the definitions it loaded at start, so
a changed scope is verified from a new session.

## Failure Modes & Fallback / Human Escalation

If a role uses its shell for live state against its guardrails, the write guard
reports it and does not stop it. Narrowing the role again needs the request
owner's decision, and it costs that role its search on native builds.

## Verification Commands

```bash
python3 scripts/validate-agent-governance.py --root .
python3 -m unittest tests.test_agent_governance tests.test_validate_agent_registry
python3 scripts/qa.py staged
python3 scripts/run-archive-contract-tests.py --root .
python3 scripts/archive_cutover.py --root .
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-CSR-001 | Every Claude role's resolved scope and projection carry `Bash` | Unit tests and governance validator |
| VAL-CSR-002 | incident-responder and observability-reviewer state the search-only limit | Unit test and role bodies |
| VAL-CSR-003 | Spawned roles in a new session have `Bash` | Session record in the Task |
| VAL-CSR-004 | SPEC-0095, SPEC-0096, and SPEC-0097 are retained as exact units with one catalog row each | Lifecycle and archive gates |

## Traceability

The [Implementation Plan](plan.md) owns order and risk. The
[Task](tasks/tsk-0001-grant-search-and-retain-packages.md) owns the evidence.

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CSR-001 | Unit tests and validator |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CSR-002 | Unit test and role bodies |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CSR-003 | Session record |
| [REQ-0003-FR-0020](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-CSR-004 | Lifecycle and archive gates |
