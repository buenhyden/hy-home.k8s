---
title: 'Workload Security Context Baseline Plan'
version: "1.0.0"
type: sdlc/plan
layer: "specs"
status: done
owner: platform
updated: 2026-08-18
artifact_id: "SPEC-0061-PLAN-0001"
---

# Workload Security Context Baseline Plan (Plan)

## Overview

This plan executes the bounded closure designed by
[Spec 0061](./spec.md). It
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

### Legacy Task ledger inputs

This Task records execution evidence for `WSCB-001` through `WSCB-004`, defined by
[Spec 0061](./spec.md) and its
reciprocal [Plan](./plan.md).

All evidence is repository-static or public-source evidence. No cluster, registry,
or CI run was contacted, and no container start is claimed.

- [Spec 0061](./spec.md)
- [Plan](./plan.md)
- Predecessor Spec: `docs/03.specs/0060-platform-currency-defect-closure/spec.md`
- [Kubernetes infrastructure and security research](../../../../90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md)

### Workload sweep that scoped this cycle

The first sweep enumerated built-in workload kinds and reported zero gaps. It was
wrong. `adminer` is an Argo `Rollout`, a custom resource carrying the same pod
template under a different `kind`, so a kind-keyed sweep skipped it silently.

The second sweep searched by structure — any document whose spec contains a pod
template with containers — and found all three workloads regardless of kind.

| Workload             | Kind         | Pod SC | Container SC | Limits |
| -------------------- | ------------ | ------ | ------------ | ------ |
| `kube-state-metrics` | `Deployment` | yes    | yes          | yes    |
| `alloy-k8s-logs`     | `Deployment` | yes    | yes          | yes    |
| `adminer`            | `Rollout`    | no     | no           | yes    |

Both platform workloads carry an identical pattern: pod `runAsNonRoot: true`,
`runAsUser: 65534`, `fsGroup: 65534`; container `allowPrivilegeEscalation: false`,
`capabilities.drop: [ALL]`, `readOnlyRootFilesystem: true`. The pattern is a real
convention that one workload escaped.

Nothing enforces it. No file under `gitops/` or `infrastructure/` declares a
`pod-security.kubernetes.io` label, and no Kyverno, Gatekeeper, or
ValidatingAdmissionPolicy resource exists. Escaping the convention requires no
override, only omission.

Exposure is bounded. The `adminer` Ingress host is `adminer.127.0.0.1.nip.io`,
which resolves to loopback.

### WSCB-001 evidence — adminer container controls

`gitops/workloads/adminer/rollout.yaml` gained a container `securityContext` with
`allowPrivilegeEscalation: false` and `capabilities.drop: [ALL]`.

Both hold from the image definition alone. The official image Dockerfile creates a
system account and ends with `USER adminer`, and its command is
`php -S [::]:8080 -t /var/www/html`. A non-root listener above port 1024 needs no
retained capability and no setuid transition.

No identity or filesystem control was applied. The reason is recorded below and is
the correction this cycle made to its own approved scope.

Verification: the file parses to one document; the container `securityContext`
equals `{allowPrivilegeEscalation: False, capabilities: {drop: [ALL]}}`; the pod
`securityContext` is absent.

### WSCB-002 evidence — sample template baseline

`examples/sample-app/rollout.yaml` gained the complete baseline: pod
`runAsNonRoot: true`, `runAsUser: 65534`, `fsGroup: 65534`, and container
`allowPrivilegeEscalation: false`, `capabilities.drop: [ALL]`,
`readOnlyRootFilesystem: true`.

A template is not a running workload, so nothing about it is undecidable, and a
template that shows a partial pattern teaches the partial pattern. Its comments
carry the coupling rule and the `emptyDir` requirement forward.

This is the higher-leverage half of the cycle. The template is what new workloads
are copied from, so the omission propagated by construction.

Verification: the file parses to one document; the pod `securityContext` carries
both coupled fields; the container `securityContext` carries all three controls.

### WSCB-003 evidence — deferred controls and image line

**The coupling correction.** The approved change set applied `runAsNonRoot: true`
to `adminer` while deferring `runAsUser`. That is not a valid staging. The
Kubernetes kubelet, in `pkg/kubelet/kuberuntime/security_context_others.go`,
returns an error when `runAsNonRoot` is set, no `runAsUser` is given, and the image
declares a username:

> `container has runAsNonRoot and image has non-numeric user (%s), cannot verify user is non-root`

A dedicated test, `RunAsNonRoot should fail for non-numeric username`, asserts the
behavior. The `adminer` image declares `USER adminer` — a name, created by
`adduser -S -G adminer adminer`, which assigns an unpinned system UID. Applying
`runAsNonRoot` alone would therefore have stopped the container from starting.

The two fields are one unit. `C-WSCB-002` records this, and the cycle applied less
to `adminer` than approved as a result.

| Control                        | Workload  | Prerequisite observation                                                                                     | Blocking class |
| ------------------------------ | --------- | ------------------------------------------------------------------------------------------------------------ | -------------- |
| `runAsNonRoot` + `runAsUser`   | `adminer` | the numeric UID of `adminer` in the image, or that `/var/www/html` is world-readable under an overriding UID | live-cluster   |
| `readOnlyRootFilesystem: true` | `adminer` | the PHP session save path, and an `emptyDir` mounted there                                                   | live-cluster   |

**Image-line refinement.** The Spec 059 handoff recorded upstream `adminer`
`6.0.1`. That is correct for the source release, published 2026-08-14, but it is
not an available upgrade target. The official image repository carries only image
lines `4` and `5`.

| Layer                      | Version                 |
| -------------------------- | ----------------------- |
| Source release             | `6.0.1` (2026-08-14)    |
| Newest official image line | `5`, at adminer `5.5.1` |
| Current image line `4`     | adminer `4.17.1`        |
| Repository pin             | `4.8.1`                 |

The deferred upgrade target is therefore the image line, not the source release.
Both image lines end with `USER adminer`, so the coupling above survives any
upgrade and is not resolved by one.
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
[Spec 0061](./spec.md).

### Legacy Task verification evidence

- `python3` YAML parse of `gitops/workloads/adminer/rollout.yaml` → 1 document;
  container `securityContext` carries exactly the two applied controls; pod
  `securityContext` absent
- `python3` YAML parse of `examples/sample-app/rollout.yaml` → 1 document; pod
  `securityContext` carries `runAsNonRoot`, `runAsUser`, `fsGroup`; container
  `securityContext` carries all three controls
- `bash scripts/validate-repo-quality-gates.sh .` → `[PASS] repository quality gates passed`
- `python3 scripts/validate-links-and-owners.py --root . --mode strict` → `PASS CROSS-DOCUMENT`
- `python3 scripts/validate-markdown-profiles.py --root . --mode strict` → `PASS SUMMARY . - actual="0"`
- `python3 scripts/validate-affected-surfaces.py --root .` → `[PASS] surfaces=22/22 uncovered=0`

These are repository-static results. They establish declared intent only and
promote no admission, scheduling, reconciliation, or container-start outcome.
## Risks & Mitigations

| Risk                                          | Mitigation                                                      |
| --------------------------------------------- | --------------------------------------------------------------- |
| A hardening field stops the workload starting | `C-WSCB-001` admits only statically decidable controls          |
| `runAsNonRoot` applied without `runAsUser`    | `C-WSCB-002` binds the two fields into one unit                 |
| The template teaches a partial pattern        | `C-WSCB-003` gives the template the complete baseline           |
| A deferral is recorded too vaguely to act on  | `C-WSCB-004` requires a named observation, not a pending status |
| A static PASS is read as live confirmation    | `C-WSCB-005` keeps every live outcome blocked                   |
| Scope drifts into admission enforcement       | Enforcement is an explicit non-goal needing separate approval   |

### Legacy Task approval and rollback boundaries

- Direct human approval on 2026-08-18 authorized this cycle, selecting template
  plus staged `adminer` hardening over a wider scope including Pod Security
  Standards admission enforcement.
- The approved change set was corrected before any manifest was edited, because
  verification showed one approved field would have broken the workload. The
  correction narrowed what was applied; it did not widen scope.
- No k3d, kubectl, helm, argocd, docker, or registry command was run. No cluster
  was contacted and no image was pulled.
- No secret value was read, echoed, or recorded.
- GitOps-first is preserved: manifest changes declare desired state.
  Reconciliation and any live effect remain operator-owned and are not claimed.
- No branch was pushed to a remote and no artifact was published.

### Recorded limitations

- Whether the `adminer` container currently retains any capability, or would
  behave differently under the two applied controls, was **not** observed. Only
  the manifest and image definitions were read.
- The numeric UID that `adduser -S` assigns to `adminer` was not determined. It
  requires reading the image filesystem, which is a registry action.
- The PHP session save path in the running image was not read. The deferral names
  it as the prerequisite rather than asserting a default.
- `examples/azure/kubernetes/sample-app.yaml` was observed to have the same
  omission and was **not** changed. It targets a different platform and is not the
  template `gitops/workloads/` copies from. It remains open.
- Whether any admission controller would accept or reject these manifests is
  unverified; the repository declares none.
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
| [VAL-WSCB-001](./spec.md) | WSCB-001..002 | [WSCB-001](./tasks/tsk-0001-wscb-001.md) will record both parse results               |
| [VAL-WSCB-002](./spec.md) | WSCB-001      | [WSCB-001](./tasks/tsk-0001-wscb-001.md) will record the excluded-field assertion     |
| [VAL-WSCB-003](./spec.md) | WSCB-002      | [WSCB-002](./tasks/tsk-0002-wscb-002.md) will record the coupled-field assertion      |
| [VAL-WSCB-004](./spec.md) | WSCB-003      | [WSCB-003](./tasks/tsk-0003-wscb-003.md) will record the deferred control table       |
| [VAL-WSCB-005](./spec.md) | WSCB-003      | [WSCB-003](./tasks/tsk-0003-wscb-003.md) will record the image-line evidence          |
| [VAL-WSCB-006](./spec.md) | WSCB-004      | [WSCB-004](./tasks/tsk-0004-wscb-004.md) will record the full lane results            |
| [VAL-WSCB-007](./spec.md) | WSCB-001..004 | [WSCB-001..004](./plan.md) will record one commit per logical unit |

### Related Documents

The owning Spec and the reciprocal Task already link reciprocally in the
`#### Lifecycle Traceability` table above, so they are recorded here as code
literals rather than duplicated links.

- Owning Spec: `docs/03.specs/0061-workload-security-context-baseline/spec.md`
- Reciprocal Task:
  `docs/03.specs/0061-workload-security-context-baseline/README.md#task-records`
- Predecessor Spec: `docs/03.specs/0060-platform-currency-defect-closure/spec.md`

### Legacy Task traceability

#### Lifecycle Traceability

| Criterion / work item                                                     | Result  | Evidence                                                         |
| ------------------------------------------------------------------------- | ------- | ---------------------------------------------------------------- |
| [VAL-WSCB-001](./plan.md) | Done    | Both manifests parse and carry the applied controls              |
| [VAL-WSCB-002](./plan.md) | Done    | No excluded control present in the adminer container spec        |
| [VAL-WSCB-003](./plan.md) | Done    | Template pod spec carries both coupled identity fields           |
| [VAL-WSCB-004](./plan.md) | Done    | Each deferred control names a prerequisite observation           |
| [VAL-WSCB-005](./plan.md) | Done    | Image line recorded distinctly from the `6.0.1` source release   |
| [VAL-WSCB-006](./plan.md) | Done    | Full lane green at closure; no cluster or registry contacted |
| [VAL-WSCB-007](./plan.md) | Done    | Three commits: `2da9eca4` manifests, `ca6be7d1` lifecycle, this closure |

### Related Documents

The owning Spec and the reciprocal Plan already link reciprocally in
`## Inputs` and in the table above, so they are recorded here as code literals
rather than duplicated links.

- Owning Spec: `docs/03.specs/0061-workload-security-context-baseline/spec.md`
- Reciprocal Plan:
  `docs/03.specs/0061-workload-security-context-baseline/plan.md`
- [ADR 0022 — direct-approval standalone execution lineage](../../../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Durable progress ledger](../../../../00.agent-governance/memory/progress.md)
