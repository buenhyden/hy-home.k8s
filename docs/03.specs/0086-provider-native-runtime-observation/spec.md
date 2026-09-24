---
title: "Provider Native Runtime Observation Technical Specification"
version: "0.1.0"
type: "sdlc/spec"
status: "draft"
owner: "platform"
updated: "2026-09-24"
layer: "specs"
artifact_id: "SPEC-0086"
---

# Provider Native Runtime Observation Technical Specification (Spec)

## Overview

[SPEC-0072](../0072-agent-governance-and-quality-gate-consolidation/spec.md)
consolidated agent governance and shared QA and proved every static half of
its acceptance criteria VAL-AGQ-001 through VAL-AGQ-007. Its Task recorded one
native runtime half those criteria still name — discovery, invocation, model
access, sandbox enforcement, and event delivery for both the Claude and Codex
providers — as `WORK-009`, deferred to an operator-authorized native session
that no repository-static run can supply. SPEC-0072 closed on 2026-09-24 with
that deferral transferred here rather than claimed as passed.

This Spec owns exactly that native-runtime observation: it names the
acceptance an operator-authorized session must satisfy, and it authorizes no
agent to satisfy it statically. A static declaration — a role projection, a
permission-scope entry, a hook registration file — is configuration intent,
not proof that a client discovered the skill, resolved the declared model,
delivered the hook event, or enforced the declared sandbox.

## Strategic Boundaries & Non-goals

- **Owns**: the native-runtime observation contract for Claude and Codex —
  discovery, invocation, model access, sandbox enforcement, and event
  delivery — and the recorded evidence of an operator-authorized session
  against it.
- **Consumes**: SPEC-0072's static acceptance evidence, `.claude/provider.md`,
  `.codex/provider.md`, `.agents/roles/registry.json`, and the provider notes'
  own dated native observations.
- **Does not own**: any further governance, QA, or gate consolidation
  behavior change; those remain SPEC-0072's closed scope.
- **Non-goals**: promoting a repository-static or hosted-CI result to runtime
  evidence; running an unauthorized native session; widening any role's
  permission class; changing hook registration or sandbox configuration
  outside what an observed defect requires.

## Contracts

- **C-PNRO-001 — no static promotion.** A registry entry, a projection file, a
  hook registration, or a passing repository-static test never substitutes for
  an observed native-runtime result. Each criterion below requires a dated,
  attributed session record.
- **C-PNRO-002 — operator authority.** Only an operator-authorized session may
  produce the observation; no agent may authorize, simulate, or infer it on
  the operator's behalf.
- **C-PNRO-003 — per-provider evidence.** Claude and Codex are observed
  separately; a result for one provider proves nothing about the other.

## Core Design

The observation proceeds per provider, per criterion, in one authorized
session each: confirm the client discovers the intended role/skill set,
confirm one explicit invocation resolves the declared model binding, confirm
the declared sandbox/permission boundary is actually enforced against a
representative write and a representative denied action, and confirm the
declared hook fires and its payload matches the documented contract. Each
result is recorded with the exact client version, session boundary, and
command/payload observed.

## Data Modeling & Storage Strategy

Results are recorded only in this package's Task; no new registry, contract
file, or fixture is introduced. No credential, session log, or private
configuration is retained — only the client identity, the command issued, and
the observed outcome.

## Interfaces & Data Structures

| Interface | Input | Output |
| --- | --- | --- |
| Native discovery check | Client identity, worktree | Enabled skill/role count and any reported discovery error |
| Native invocation check | Declared model binding | Resolved model identity or an explicit failure |
| Sandbox enforcement check | A representative write and a representative denied action | Enforced/not-enforced with exact observed behavior |
| Event delivery check | A registered hook and a triggering action | Delivered/not-delivered with the exact payload shape observed |

## Edge Cases & Error Handling

- A client version change invalidates a prior observation; re-observe rather
  than carry forward a dated result across an unreviewed version change.
- A rejected or trust-blocked session is a recorded limitation, not a passing
  or failing result for the criterion it was meant to observe.
- An operator declining to authorize a session leaves the criterion `DEFER`
  with this Task as the visible next owner; it is never silently dropped.

## Failure Modes & Fallback / Human Escalation

A missing or expired native session stays `DEFER` with the operator named as
next owner. No agent may close this package by reasoning from static evidence
alone; doing so would repeat the exact promotion SPEC-0072's Task refused to
make.

## Verification Commands

```text
No repository-static command exists for this Spec's acceptance criteria.
Verification is an operator-authorized native session per provider, recorded
in the owning Task with client identity, exact command, and observed result.
```

## Success Criteria & Verification Plan

| ID | Criterion | Evidence |
| --- | --- | --- |
| VAL-PNRO-001 | Native discovery is observed and recorded for Claude | Dated session record naming client version and discovered set |
| VAL-PNRO-002 | Native discovery is observed and recorded for Codex | Dated session record naming client version and discovered set |
| VAL-PNRO-003 | Native invocation and model access are observed for Claude | Dated session record naming the resolved model identity |
| VAL-PNRO-004 | Native invocation and model access are observed for Codex | Dated session record naming the resolved model identity |
| VAL-PNRO-005 | Sandbox/permission enforcement is observed for Claude | Dated session record naming the enforced or not-enforced boundary |
| VAL-PNRO-006 | Sandbox/permission enforcement is observed for Codex | Dated session record naming the enforced or not-enforced boundary |
| VAL-PNRO-007 | Hook event delivery is observed for Claude | Dated session record naming the delivered payload shape |
| VAL-PNRO-008 | Hook event delivery is observed for Codex | Dated session record naming the delivered payload shape |

## Traceability

- **Predecessor**: [SPEC-0072](../0072-agent-governance-and-quality-gate-consolidation/spec.md), whose Task transferred `WORK-009` here on 2026-09-24.
- **Plan**: [Provider Native Runtime Observation Implementation Plan](plan.md)
- **Task**: [Provider Native Runtime Observation Task](tasks/tsk-0001-observe-provider-native-runtime.md)

### Lifecycle Traceability

| Requirement ID | Spec criterion | Verification method |
| --- | --- | --- |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNRO-001 | Operator-authorized native session record |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNRO-002 | Operator-authorized native session record |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNRO-003 | Operator-authorized native session record |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNRO-004 | Operator-authorized native session record |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNRO-005 | Operator-authorized native session record |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNRO-006 | Operator-authorized native session record |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNRO-007 | Operator-authorized native session record |
| [REQ-0003-FR-0025](../../01.requirements/0003-workspace-agent-governance-platform.md) | VAL-PNRO-008 | Operator-authorized native session record |
