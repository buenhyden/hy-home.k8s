---
title: 'Workload Security Context Baseline Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-08-18
artifact_id: "PLAN-0061"
---

# Workload Security Context Baseline Plan (Plan)

## Overview

This plan executes the bounded closure designed by
[Spec 0061](../../03.specs/0061-workload-security-context-baseline/spec.md). It
closes the workload hardening asymmetry that the Spec 059 handoff named, stops the
sample template from propagating it, and records what was deliberately not applied.

## Context

A kind-agnostic sweep for pod templates was necessary because the first sweep,
written against built-in workload kinds, silently missed `adminer`. `adminer` is an
Argo `Rollout`, a custom resource carrying the same pod template under a different
`kind`. Searching by structure rather than by kind found all three workloads.

Of those three, both platform workloads carry an identical hardening pattern and
`adminer` carries none. Nothing enforces the pattern: no namespace declares a
`pod-security.kubernetes.io` label and no policy engine is installed, so the
convention survives only by copying.

The exposure is bounded and should not be overstated. The `adminer` Ingress host is
`adminer.127.0.0.1.nip.io`, which resolves to loopback, so this is not an
internet-reachable database console.

## Goals & In-Scope

- Apply `allowPrivilegeEscalation: false` and `capabilities.drop: [ALL]` to the
  `adminer` Rollout.
- Apply the complete baseline to `examples/sample-app/rollout.yaml`, with the
  coupled identity fields set together.
- Record each deferred control against its prerequisite observation.
- Refine the deferred `adminer` upgrade record to name the official image line.
- Land logical-unit commits with repository-static validation evidence.

## Non-Goals & Out-of-Scope

- Pod Security Standards labels, admission enforcement, or a policy engine.
- Upgrading the `adminer` image.
- Applying identity or filesystem controls to `adminer`.
- Changing `examples/azure/**`.
- Any live cluster, registry, or reconciliation action.
- Pushing any branch to a remote.

## Work Breakdown

| ID       | Package                    | Depends on | Commit unit |
| -------- | -------------------------- | ---------- | ----------- |
| WSCB-001 | adminer container controls | none       | shared      |
| WSCB-002 | sample template baseline   | none       | shared      |
| WSCB-003 | deferred control record    | 001, 002   | own         |
| WSCB-004 | Lifecycle registration     | 001..003   | own         |

### WSCB-001 — adminer container controls

Add the two controls whose safety follows from the image definition. Add a comment
recording why the remaining house-pattern fields were excluded. Verify the file
parses and that no excluded field is present.

### WSCB-002 — sample template baseline

Add the full baseline to the template pod and container spec, with `runAsNonRoot`
and `runAsUser` set together and a comment stating the coupling rule. Verify the
file parses and both coupled fields are present.

`WSCB-001` and `WSCB-002` share one commit because both are manifest hardening
edits validated by the same lane.

### WSCB-003 — deferred control record

Record each excluded control with the observation that would admit it and its
blocking class, and record the `adminer` image-line refinement.

### WSCB-004 — lifecycle registration

Add the Stage 03 and Stage 04 index rows and tree entries, the
`standaloneExecutions` entry, the ADR 0022 lineage row, the post-closure spec
authority allowlist entry with its mirrored fixture, and the durable progress
ledger record.

## Verification Plan

| ID           | Package       | Verification                                              |
| ------------ | ------------- | --------------------------------------------------------- |
| VAL-WSCB-001 | WSCB-001..002 | Both manifests parse and carry the applied controls       |
| VAL-WSCB-002 | WSCB-001      | No excluded control present in the adminer container spec |
| VAL-WSCB-003 | WSCB-002      | Template carries both coupled identity fields             |
| VAL-WSCB-004 | WSCB-003      | Every deferred control names a prerequisite observation   |
| VAL-WSCB-005 | WSCB-003      | Image line recorded distinctly from the source release    |
| VAL-WSCB-006 | WSCB-004      | Full lane passes; no cluster or registry contacted        |
| VAL-WSCB-007 | WSCB-001..004 | One commit per logical unit with its own evidence         |

Verification commands are owned by
[Spec 0061](../../03.specs/0061-workload-security-context-baseline/spec.md).

## Risks & Mitigations

| Risk                                          | Mitigation                                                      |
| --------------------------------------------- | --------------------------------------------------------------- |
| A hardening field stops the workload starting | `C-WSCB-001` admits only statically decidable controls          |
| `runAsNonRoot` applied without `runAsUser`    | `C-WSCB-002` binds the two fields into one unit                 |
| The template teaches a partial pattern        | `C-WSCB-003` gives the template the complete baseline           |
| A deferral is recorded too vaguely to act on  | `C-WSCB-004` requires a named observation, not a pending status |
| A static PASS is read as live confirmation    | `C-WSCB-005` keeps every live outcome blocked                   |
| Scope drifts into admission enforcement       | Enforcement is an explicit non-goal needing separate approval   |

## Completion Criteria

- All four packages committed, with `WSCB-001` and `WSCB-002` sharing one commit.
- All seven `VAL-WSCB` criteria satisfied or explicitly recorded as not met.
- Full validation lane green.
- Durable progress ledger records the cycle, its evidence, and its handoff.
- No live, hosted, provider-runtime, remote, secret-value, push, or deployment
  evidence claimed.

## Traceability

### Lifecycle Traceability

| Spec criterion                                                                | Work package  | Expected Task                                                                                                      |
| ----------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------ |
| [VAL-WSCB-001](../../03.specs/0061-workload-security-context-baseline/spec.md) | WSCB-001..002 | [WSCB-001](tasks.md) will record both parse results               |
| [VAL-WSCB-002](../../03.specs/0061-workload-security-context-baseline/spec.md) | WSCB-001      | [WSCB-001](tasks.md) will record the excluded-field assertion     |
| [VAL-WSCB-003](../../03.specs/0061-workload-security-context-baseline/spec.md) | WSCB-002      | [WSCB-002](tasks.md) will record the coupled-field assertion      |
| [VAL-WSCB-004](../../03.specs/0061-workload-security-context-baseline/spec.md) | WSCB-003      | [WSCB-003](tasks.md) will record the deferred control table       |
| [VAL-WSCB-005](../../03.specs/0061-workload-security-context-baseline/spec.md) | WSCB-003      | [WSCB-003](tasks.md) will record the image-line evidence          |
| [VAL-WSCB-006](../../03.specs/0061-workload-security-context-baseline/spec.md) | WSCB-004      | [WSCB-004](tasks.md) will record the full lane results            |
| [VAL-WSCB-007](../../03.specs/0061-workload-security-context-baseline/spec.md) | WSCB-001..004 | [WSCB-001..004](tasks.md) will record one commit per logical unit |

### Related Documents

The owning Spec and the reciprocal Task already link reciprocally in the
`### Lifecycle Traceability` table above, so they are recorded here as code
literals rather than duplicated links.

- Owning Spec: `docs/03.specs/0061-workload-security-context-baseline/spec.md`
- Reciprocal Task:
  `docs/04.execution/tasks/2026-08-18-workload-security-context-baseline.md`
- Predecessor Spec: `docs/03.specs/0060-platform-currency-defect-closure/spec.md`
