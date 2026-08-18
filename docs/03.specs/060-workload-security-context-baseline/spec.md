---
title: 'Workload Security Context Baseline Technical Specification'
type: sdlc/spec
status: done
owner: platform
updated: 2026-08-18
---

# Workload Security Context Baseline Technical Specification (Spec)

## Overview

This specification designs a bounded closure over one asymmetry in the
repository's workload security posture. It follows the Spec 059 handoff, which
recorded that `adminer` declares no `securityContext` and ranked it first by risk
among the deferred items.

A kind-agnostic sweep for pod templates found three workloads under `gitops/`
and `examples/`. Both platform workloads, `kube-state-metrics` and
`alloy-k8s-logs`, carry an identical hardening pattern. `adminer` carries none.
The pattern is therefore a real convention that one workload escaped.

Two findings reframe the work beyond fixing that one workload.

First, the convention is not enforced anywhere. No namespace declares a
`pod-security.kubernetes.io` label, and the repository installs no policy engine.
The hardening exists only as copied YAML, so escaping it requires no override —
only omission.

Second, the sample workload template under `examples/sample-app/` has the same
omission. That template is what new workloads are copied from, so the gap
propagates by construction. Closing the template matters more than closing the
instance.

The cycle also corrects an assumption made when its own scope was approved. The
approved change set applied `runAsNonRoot: true` to `adminer` while deferring
`runAsUser`. Verification against the image definition and the kubelet source
showed those two fields are coupled, and that applying the first without the
second would stop the container from starting. The correction is recorded in
`C-WSCB-002` and is the reason this cycle applies less to `adminer` than approved
and more to the template.

Direct human approval on 2026-08-18 authorizes this standalone execution relation.
That approval selected template plus staged `adminer` hardening over a wider scope
that included Pod Security Standards admission enforcement.
No separate PRD or ARD is required or part of this standalone lifecycle.

## Strategic Boundaries & Non-goals

### In scope

- Apply the security controls that hold independently of image UID and filesystem
  writability to the `adminer` Rollout.
- Apply the complete hardening baseline to the sample workload template, including
  the coupled fields, so the template stops teaching the omission.
- Record the fields that were deliberately not applied to `adminer`, each with the
  specific prerequisite that would admit it.
- Refine the deferred `adminer` image upgrade record to name the image line rather
  than the upstream source release.

### Out of scope and non-goals

- Adding `pod-security.kubernetes.io` labels or any admission enforcement.
- Installing a policy engine.
- Upgrading the `adminer` image.
- Changing `examples/azure/**`, which targets a different platform and is not the
  template that `gitops/workloads/` copies from.
- Adding authentication in front of `adminer`.
- Any live cluster, registry, or reconciliation action.
- Pushing any branch to a remote.

## Contracts

### C-WSCB-001 — apply only what is statically decidable

A control may be applied to a running workload only when its safety follows from
the manifest and the image definition alone. A control whose safety depends on
runtime filesystem or identity behavior is deferred with its prerequisite named.

### C-WSCB-002 — `runAsNonRoot` and `runAsUser` are one unit

Where an image declares its user by name rather than numeric UID, `runAsNonRoot`
must not be set without `runAsUser`. The kubelet cannot resolve a username to a
UID before start and rejects the container. These two fields are applied together
or not at all.

### C-WSCB-003 — a template carries the complete pattern

An example template is not a running workload, so it takes the full baseline
including coupled fields. A template that shows a partial pattern teaches the
partial pattern.

### C-WSCB-004 — deferral names its prerequisite

Every control excluded by `C-WSCB-001` is recorded with the specific observation
that would admit it, not with a general statement that verification is pending.

### C-WSCB-005 — no live claim

Repository-static validation establishes declared intent only. No admission,
scheduling, reconciliation, or container-start outcome is claimed.

### C-WSCB-006 — logical work units

Each work package lands as its own commit with its own evidence, except where two
packages are validated by a single lane.

## Core Design

The design separates the three workloads by what can be decided about them.

`adminer` runs a known image whose definition is readable. That definition fixes
what is decidable: the container already runs as a non-root user, listens on a
port above 1024, and needs no setuid behavior. `allowPrivilegeEscalation: false`
and `capabilities.drop: [ALL]` therefore hold with no runtime observation. The
identity and filesystem controls do not, and are deferred.

The sample template names no image, so nothing about it is undecidable. It takes
the full baseline, and its comments carry the coupling rule forward so the next
author does not rediscover it by outage.

The platform workloads are already correct and are not touched.

## Data Modeling & Storage Strategy

No data model changes. The deferred-control record is a table in the reciprocal
Task, keyed by control name, carrying the prerequisite observation and the
blocking class.

## Interfaces & Data Structures

### Applied container controls

| Control                           | `adminer` | Template | Independent of  |
| --------------------------------- | --------- | -------- | --------------- |
| `allowPrivilegeEscalation: false` | applied   | applied  | UID, filesystem |
| `capabilities.drop: [ALL]`        | applied   | applied  | UID, filesystem |
| `readOnlyRootFilesystem: true`    | deferred  | applied  | —               |
| `runAsNonRoot` + `runAsUser`      | deferred  | applied  | —               |

### Deferred control record

Each deferred row carries the control, the workload, the prerequisite observation,
and the blocking class. The prerequisite must name an observation, not an
intention.

## Edge Cases & Error Handling

An image that declares `USER` by name defeats `runAsNonRoot` alone; this is the
case that produced `C-WSCB-002`.

An image that declares `USER` numerically admits `runAsNonRoot` without
`runAsUser`, so the contract is conditional rather than absolute.

A container that writes to its root filesystem defeats `readOnlyRootFilesystem`
unless a writable volume is mounted at the written path. For a PHP application the
written path is the session save path.

Dropping all capabilities is safe for a listener above port 1024 and unsafe below
it, where `CAP_NET_BIND_SERVICE` is required.

## Failure Modes & Fallback / Human Escalation

If a deferred control is later applied and the workload fails to start, the
recovery is a Git revert of the manifest, which is this repository's standard
recovery path. No control introduced by this cycle can produce that failure,
because every applied control is independent of the runtime behavior that would
cause it.

Escalate to a human before adding any admission enforcement, because enforcement
can reject workloads that currently run.

## Verification Commands

```bash
python3 -c "import yaml; list(yaml.safe_load_all(open('gitops/workloads/adminer/rollout.yaml')))"
python3 -c "import yaml; list(yaml.safe_load_all(open('examples/sample-app/rollout.yaml')))"
bash scripts/validate-repo-quality-gates.sh .
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-affected-surfaces.py --root .
```

## Success Criteria & Verification Plan

| ID           | Criterion                                                              |
| ------------ | ---------------------------------------------------------------------- |
| VAL-WSCB-001 | Both manifests parse and carry the applied controls                    |
| VAL-WSCB-002 | `adminer` carries no control excluded by `C-WSCB-001`                  |
| VAL-WSCB-003 | The template carries the coupled fields together                       |
| VAL-WSCB-004 | Every deferred control is recorded with a named prerequisite           |
| VAL-WSCB-005 | The image-line refinement is recorded against the upstream source line |
| VAL-WSCB-006 | Full validation lane passes; no cluster or registry contacted          |
| VAL-WSCB-007 | One commit per logical unit                                            |

## Traceability

This Spec has no PRD or ARD. Its authority is the direct human approval recorded
in `## Overview`, registered through the `standaloneExecutions` entry in
`docs/99.templates/support/document-profiles.json` and the lineage row in
ADR 0022.

Its predecessor is `docs/03.specs/059-platform-currency-defect-closure/spec.md`,
whose handoff named the `adminer` `securityContext` gap.

### Lifecycle Traceability

| PRD requirement                   | Spec criterion | Verification method                                         |
| --------------------------------- | -------------- | ----------------------------------------------------------- |
| N/A — standalone, direct approval | VAL-WSCB-001   | YAML parse of both manifests with control assertions        |
| N/A — standalone, direct approval | VAL-WSCB-002   | Assert excluded control names absent from the adminer spec  |
| N/A — standalone, direct approval | VAL-WSCB-003   | Assert both coupled fields present in the template pod spec |
| N/A — standalone, direct approval | VAL-WSCB-004   | Review the deferred control table for named prerequisites   |
| N/A — standalone, direct approval | VAL-WSCB-005   | Compare the recorded image line against the source release  |
| N/A — standalone, direct approval | VAL-WSCB-006   | Full lane output recorded in the reciprocal Task            |
| N/A — standalone, direct approval | VAL-WSCB-007   | Commit log reviewed at closure                              |

### Related Documents

- [Plan](../../04.execution/plans/2026-08-18-workload-security-context-baseline.md)
- [Task](../../04.execution/tasks/2026-08-18-workload-security-context-baseline.md)
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Spec 059 — platform currency defect closure](../059-platform-currency-defect-closure/spec.md)
