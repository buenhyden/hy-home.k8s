---
title: 'Platform Currency Defect Closure Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-08-18
artifact_id: "SPEC-0060-PLAN-0001"
---

# Platform Currency Defect Closure Plan (Plan)

## Overview

This plan executes the bounded remediation designed by
[Spec 0060](../../03.specs/0060-platform-currency-defect-closure/spec.md). It closes
two live version-currency defects, settles the Argo CD Source Integrity adoption
question, and defers four version upgrades with their evaluation recorded.

## Context

The 2026-08-17 full-corpus research refresh evaluated two fired refresh triggers.
Evaluating them properly meant inventorying every versioned dependency, which
surfaced six drift items rather than two, and showed that neither fired trigger
was the most urgent finding.

The two defects closed here exist at the currently pinned versions and are
independent of any upgrade. `kube-state-metrics` lacks RBAC for two of its own
default collectors. The two bootstrap-phase Helm installs carry no version pin, so
bootstrap is non-reproducible, and the version inventory's contract covered the
eight GitOps-managed charts but neither bootstrap chart.

Source Integrity is settled rather than deferred, because the evaluation produced a
clear answer: it authenticates whichever commit sits at a mutable branch tip and
therefore does not address the gap's cause.

### Legacy Task ledger inputs

This Task records execution evidence for `PCDC-001` through `PCDC-004`, defined by
[Spec 0060](../../03.specs/0060-platform-currency-defect-closure/spec.md) and its
reciprocal [Plan](plan.md).

All evidence is repository-static or public-documentation evidence. No cluster,
registry, or CI run was contacted, and no reconciliation is claimed.

- [Spec 0060](../../03.specs/0060-platform-currency-defect-closure/spec.md)
- [Plan](plan.md)
- [ADR-0029](../../02.architecture/decisions/0026-argo-cd-source-integrity-non-adoption.md)
- [Kubernetes infrastructure and security research](../../90.references/research/0001-workspace-engineering/kubernetes-infrastructure-and-security.md)
- [Kubernetes, infrastructure, and security research](../../90.references/research/0001-workspace-engineering/kubernetes-infrastructure-and-security.md)

### Drift inventory that scoped this cycle

Evaluating the two fired refresh triggers required inventorying every versioned
dependency the repository declares. Six items were found, not two.

| Component            | Declared       | Upstream on 2026-08-18 | Disposition |
| -------------------- | -------------- | ---------------------- | ----------- |
| `adminer`            | `4.8.1`        | `6.0.1` (2026-08-14)   | deferred    |
| `grafana/alloy`      | `v1.13.1`      | `v1.18.1` (2026-08-06) | deferred    |
| `rancher/k3s`        | `v1.35.0-k3s1` | `v1.35.7` / `v1.36.3`  | deferred    |
| `kube-state-metrics` | `v2.14.0`      | `v2.19.1` (2026-06-10) | deferred    |
| `metallb` chart      | **no pin**     | chart `0.16.1`         | **pinned**  |
| `argo-cd` chart      | **no pin**     | chart `10.4.0`         | **pinned**  |

Neither fired trigger was the most urgent finding. The most urgent was a missing
RBAC grant unrelated to any version bump. The highest-leverage was a contract hole
that made bootstrap non-reproducible. A cycle scoped to the triggers alone would
have closed neither.

### PCDC-001 evidence — kube-state-metrics RBAC

`gitops/platform/monitoring/kube-state-metrics.yaml` gained two ClusterRole rules:
`certificates.k8s.io/certificatesigningrequests` and
`coordination.k8s.io/leases`, both `list` and `watch`.

Both are documented **default** resources in the upstream default `--resources`
set, and both were default at the pinned `v2.14.0`. The Deployment declares no
`args:`, so it inherits the image default collector set and has been running both
collectors without the permissions they require for the life of the current pin.
This is a live defect, not an upgrade prerequisite.

`discovery.k8s.io/endpointslices` was deliberately **not** granted. It becomes a
default only at `v2.18.0`; at `v2.14.0` the default set uses core `endpoints`,
which the ClusterRole already grants. Granting it now would be an unused
permission and is recorded as a prerequisite for the deferred upgrade instead.

Verification: the file parses to six YAML documents and the ClusterRole carries ten
rules, with `certificates.k8s.io` and `coordination.k8s.io` both present.

### PCDC-002 evidence — bootstrap chart version pins

`infrastructure/bootstrap-local.sh` previously ran both bootstrap-phase Helm
installs with no `--version`, so every bootstrap could resolve a different chart.
The version inventory pinned all eight GitOps-managed charts by `targetRevision`
but had no entry for either bootstrap chart — the contract's boundary stopped at
what GitOps owns, leaving a hole exactly where it does not yet own the surface.

| Install                                     | Pin added          | Source of the value                     |
| ------------------------------------------- | ------------------ | --------------------------------------- |
| `metallb/metallb` (step `[5/11]`, line 215) | `--version 0.16.1` | `metallb.github.io/metallb/index.yaml`  |
| `argo/argo-cd` (step `[8/11]`, line 251)    | `--version 10.4.0` | `argo-helm` `charts/argo-cd/Chart.yaml` |

A `bootstrap_helm_charts` block was added to the inventory recording `repoURL`,
`chart`, `version`, `appVersion`, and `installedBy` for both, so the script and the
contract must agree.

Both pins record the version an unpinned install resolves to today, so pinning
changes what a run installs in no way. It only makes the result deterministic. The
pin is therefore risk-neutral and determinism-positive.

One source conflict was resolved rather than averaged. The `metallb` GitHub release
page reported a 2024 date for chart `0.16.1` while the Helm repository index
reported `2026-05-27`. The index was taken as authoritative, because it is what
`helm` actually resolves against. `metallb`'s `main` branch `Chart.yaml` carries the
placeholder `0.0.0`, filled by its release process, so it could not be used.

Verification: `bash -n infrastructure/bootstrap-local.sh` exits clean; both
`--version` values appear at lines 215 and 251; the inventory YAML block parses and
its `metallb` and `argo-cd` versions equal the script values.

### PCDC-003 evidence — sourceIntegrity non-adoption

[ADR-0029](../../02.architecture/decisions/0026-argo-cd-source-integrity-non-adoption.md)
records the decision not to adopt Argo CD Source Integrity, with status `accepted`.

The decisive finding is that the facility does not address the gap's cause. Twelve
declarations track `targetRevision: main`, a mutable reference that Argo CD
re-resolves to the branch tip every reconciliation. Source Integrity verifies the
signature on whichever commit sits at that tip. It does not pin a revision, does
not prevent a force-push whose new tip is also signed by a trusted key, and does
not make a run reproducible. A mutable branch under signature verification is an
authenticated moving target, not a pinned one.

Its scope is also narrower than the recorded gap: as implemented in `3.5.0` and
`3.5.1` it covers GPG-based Git commit signatures only, leaving Helm chart
provenance and OCI image digest or signature verification untouched.

The ADR records the strongest case for adoption as required by `C-PCDC-005`: it is
free to configure, needs no new controller, is present in the now-pinned chart
`10.4.0` / `v3.5.1`, and genuinely answers whether a commit was authored by a
trusted key — the one threat a solo operator cannot rule out. It also names the
reversal condition and the preferred alternative, commit-SHA pinning of
`targetRevision`, which addresses the cause rather than the symptom and needs no
key management.

Adoption was declined rather than deferred so the fired trigger stops recurring,
in the same way the prior cycle's blocking-class closure stopped structurally
unreachable rows from being re-tested.

### Deferred upgrade record

| Component            | Current        | Evaluated target         | Prerequisite                                                  | Blocking class |
| -------------------- | -------------- | ------------------------ | ------------------------------------------------------------- | -------------- |
| `kube-state-metrics` | `v2.14.0`      | `v2.19.1`                | grant `discovery.k8s.io/endpointslices`; re-check 128Mi limit | live-cluster   |
| `rancher/k3s`        | `v1.35.0-k3s1` | `v1.35.7` then `v1.36.3` | delete-and-recreate the k3d cluster; no in-place path         | live-cluster   |
| `adminer`            | `4.8.1`        | not evaluated            | evaluate `6.x`; the workload also lacks a securityContext     | live-cluster   |
| `grafana/alloy`      | `v1.13.1`      | not evaluated            | evaluate `v1.18.1`                                            | live-cluster   |

Two upgrade facts are worth carrying forward. `kube-state-metrics` `v2.18.0`
replaced `endpoints` with `endpointslices` in the default set, and because the
Deployment declares no `args:` that change arrives silently with the new image and
would not appear in a Deployment-spec diff; a repository-wide search for
`kube_endpoints_` returns zero matches outside the research pack, so no tracked
dashboard, rule, or alert consumes what would stop being emitted. And
`bootstrap-local.sh` step `[1/11]` creates the k3d cluster only when it does not
already exist, so editing the k3s image tag and re-running bootstrap silently does
nothing to a running cluster — the local upgrade path is delete-and-recreate, and
k3d offers no `upgrade` command.

The pinned `kube-state-metrics` `v2.14.0` ships client-go `v1.31` while the
repository declares k3s `v1.35.0-k3s1`, so the current pin already sits four minor
versions outside the documented compatibility matrix. Upstream states neither that
this works nor that it breaks.
## Goals & In-Scope

- Grant `kube-state-metrics` `list` and `watch` on
  `certificates.k8s.io/certificatesigningrequests` and
  `coordination.k8s.io/leases`.
- Pin both bootstrap Helm installs to explicit chart versions read from the
  authoritative index.
- Add a `bootstrap_helm_charts` contract to the version inventory so the script and
  the contract must agree.
- Record Source Integrity non-adoption, with the case for adoption and a named
  reversal condition.
- Record the four deferred upgrades with target, prerequisite, and blocking class.
- Land logical-unit commits with repository-static validation evidence.

## Non-Goals & Out-of-Scope

- Upgrading `kube-state-metrics`, `rancher/k3s`, `adminer`, or `grafana/alloy`.
- Granting `discovery.k8s.io/endpointslices`, which no collector uses at the
  current pin.
- Adopting Source Integrity or establishing a commit-signing workflow.
- Pinning `targetRevision` to commit SHAs.
- Any live cluster, registry, or reconciliation action.
- Verifying `values-local.yaml` compatibility with chart `10.4.0`.
- Pushing any branch to a remote.

## Work Breakdown

| ID       | Package                      | Depends on | Commit unit |
| -------- | ---------------------------- | ---------- | ----------- |
| PCDC-001 | kube-state-metrics RBAC      | none       | shared      |
| PCDC-002 | Bootstrap chart version pins | none       | shared      |
| PCDC-003 | sourceIntegrity non-adoption | none       | own         |
| PCDC-004 | Lifecycle registration       | 001..003   | own         |

### PCDC-001 — kube-state-metrics RBAC

Add the two missing default-collector rules to the ClusterRole. Verify the file
still parses and that the added apiGroups are present. Do not add
`endpointslices`.

### PCDC-002 — bootstrap chart version pins

Read the resolved chart version for each bootstrap install from its Helm
repository index or `Chart.yaml`, add `--version` to both commands, and add a
matching `bootstrap_helm_charts` block to the inventory. Verify the script passes
`bash -n` and that every pin matches its contract entry.

`PCDC-001` and `PCDC-002` share one commit because both are version-currency
defect closures validated by the same lane.

### PCDC-003 — sourceIntegrity non-adoption

Author ADR-0026 recording the decision, the case for adoption, the preferred
alternative, and the reversal condition.

### PCDC-004 — lifecycle registration

Add the Stage 03 and Stage 04 index rows and tree entries, the
`standaloneExecutions` entry, the ADR 0022 lineage row, the
`POST_CLOSURE_SPEC_AUTHORITY_PATHS` allowlist entry with its mirrored fixture, and
the durable progress ledger record.

## Verification Plan

| ID           | Package       | Verification                                              |
| ------------ | ------------- | --------------------------------------------------------- |
| VAL-PCDC-001 | PCDC-001      | ClusterRole parses; both new apiGroups present            |
| VAL-PCDC-002 | PCDC-001      | No rule added that the current pin does not use           |
| VAL-PCDC-003 | PCDC-002      | Both installs carry `--version`; `bash -n` passes         |
| VAL-PCDC-004 | PCDC-002      | Each `--version` matches its inventory entry              |
| VAL-PCDC-005 | PCDC-002      | Each pin equals the currently resolved upstream version   |
| VAL-PCDC-006 | PCDC-003      | ADR records the adoption case and a reversal condition    |
| VAL-PCDC-007 | PCDC-003      | Deferred upgrades recorded with target and blocking class |
| VAL-PCDC-008 | PCDC-004      | Full verification lane passes; no cluster contacted       |
| VAL-PCDC-009 | PCDC-001..004 | One commit per logical unit with its own evidence         |

Verification commands are owned by
[Spec 0060](../../03.specs/0060-platform-currency-defect-closure/spec.md).

### Legacy Task verification evidence

- `bash -n infrastructure/bootstrap-local.sh` → exit 0
- `python3` YAML parse of the ClusterRole → 6 documents, 10 rules, both new
  apiGroups present
- `python3` YAML parse of the inventory `Version Contracts` block →
  `bootstrap_helm_charts` present with `metallb` `0.16.1` and `argo-cd` `10.4.0`,
  matching the script
- `bash scripts/validate-repo-quality-gates.sh .` → `[PASS] repository quality gates passed`
- `python3 scripts/validate-links-and-owners.py --root . --mode strict` → `PASS CROSS-DOCUMENT`
- `python3 scripts/validate-markdown-profiles.py --root . --mode strict` → `PASS SUMMARY . - actual="0"`
- `python3 scripts/validate-affected-surfaces.py --root .` → `[PASS] paths=866 surfaces=22/22 uncovered=0`
- `python3 scripts/validate-vault-eso-contracts.py --root .` → `PASS vault-eso-contracts repository validation`

These are repository-static results. They establish declared intent only and
promote no live, admission, reconciliation, or chart-resolution outcome.
## Risks & Mitigations

| Risk                                           | Mitigation                                                         |
| ---------------------------------------------- | ------------------------------------------------------------------ |
| A pin changes what bootstrap installs          | `C-PCDC-003` permits only the currently resolved version           |
| Upstream sources disagree on a version         | The repository index wins; it is what `helm` resolves against      |
| A speculative RBAC grant widens permissions    | `C-PCDC-002` forbids granting what the current pin does not use    |
| Script and contract drift apart later          | `C-PCDC-004` makes disagreement a defect; both are edited together |
| The values file may not match the pinned chart | Recorded as a limitation; the risk is identical unpinned           |
| A static PASS is read as live confirmation     | `C-PCDC-006` keeps every live outcome blocked                      |
| The deferred upgrades are forgotten            | Recorded in the Task and the durable progress handoff              |

### Legacy Task approval and rollback boundaries

- Direct human approval on 2026-08-18 authorized this cycle, selecting defect
  closure plus the decision record over a wider scope including version upgrades,
  and separately confirming the concrete change set before any manifest was edited.
- No k3d, kubectl, helm, argocd, docker, or registry command was run. No cluster
  was contacted and no workflow was dispatched.
- No secret value was read, echoed, or recorded.
- Research subagents were granted `Read`, `Grep`, `Glob`, `WebFetch`, and
  `WebSearch` only, so they could not write. All edits were made by the
  orchestrating session.
- GitOps-first is preserved: manifest and script changes declare desired state.
  Reconciliation and any live effect remain operator-owned and are not claimed.
- No branch was pushed to a remote and no artifact was published.

### Recorded limitations

- Whether every value path in `infrastructure/argocd/values-local.yaml` remains
  valid in chart `10.4.0` was **not** verified. The risk is identical with and
  without the pin, because an unpinned run today resolves to the same chart, so the
  pin neither introduces nor removes it. Verifying it belongs to the deferred
  upgrade evaluation.
- Whether the two newly granted collectors previously logged, degraded, or crashed
  under a forbidden response is unverified. Only the manifest gap was observable.
- `adminer` and `grafana/alloy` upgrade paths were not evaluated; only their
  currency delta was measured.
- Whether the external Docker-hosted Prometheus consumes any metric affected by the
  deferred `kube-state-metrics` upgrade remains outside tracked paths and stays
  `DEFER`.
## Completion Criteria

- All four packages committed, with `PCDC-001` and `PCDC-002` sharing one commit.
- All nine `VAL-PCDC` criteria satisfied or explicitly recorded as not met.
- Full validation lane green.
- Durable progress ledger records the cycle, its evidence, and its handoff.
- No live, hosted, provider-runtime, remote, secret-value, push, or deployment
  evidence claimed.

## Traceability

### Lifecycle Traceability

| Spec criterion                                                              | Work package  | Expected Task                                                                                                        |
| --------------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------- |
| [VAL-PCDC-001](../../03.specs/0060-platform-currency-defect-closure/spec.md) | PCDC-001      | [PCDC-001](README.md#task-records) will record the ClusterRole parse and rule check |
| [VAL-PCDC-002](../../03.specs/0060-platform-currency-defect-closure/spec.md) | PCDC-001      | [PCDC-001](README.md#task-records) will record why endpointslices was excluded      |
| [VAL-PCDC-003](../../03.specs/0060-platform-currency-defect-closure/spec.md) | PCDC-002      | [PCDC-002](README.md#task-records) will record the pins and the shell syntax result |
| [VAL-PCDC-004](../../03.specs/0060-platform-currency-defect-closure/spec.md) | PCDC-002      | [PCDC-002](README.md#task-records) will record the script-to-contract comparison    |
| [VAL-PCDC-005](../../03.specs/0060-platform-currency-defect-closure/spec.md) | PCDC-002      | [PCDC-002](README.md#task-records) will record the upstream version evidence        |
| [VAL-PCDC-006](../../03.specs/0060-platform-currency-defect-closure/spec.md) | PCDC-003      | [PCDC-003](README.md#task-records) will record the decision and reversal condition  |
| [VAL-PCDC-007](../../03.specs/0060-platform-currency-defect-closure/spec.md) | PCDC-003      | [PCDC-003](README.md#task-records) will record the deferred upgrade table           |
| [VAL-PCDC-008](../../03.specs/0060-platform-currency-defect-closure/spec.md) | PCDC-004      | [PCDC-004](README.md#task-records) will record the full lane results                |
| [VAL-PCDC-009](../../03.specs/0060-platform-currency-defect-closure/spec.md) | PCDC-001..004 | [PCDC-001..004](README.md#task-records) will record one commit per logical unit     |

### Related Documents

The owning Spec and the reciprocal Task already link reciprocally in the
`#### Lifecycle Traceability` table above, so they are recorded here as code
literals rather than duplicated links.

- Owning Spec: `docs/03.specs/0060-platform-currency-defect-closure/spec.md`
- Reciprocal Task:
  `docs/03.specs/0060-platform-currency-defect-closure/README.md#task-records`
- [ADR-0026 — Argo CD source integrity non-adoption](../../02.architecture/decisions/0026-argo-cd-source-integrity-non-adoption.md)
- [Kubernetes infrastructure and security research](../../90.references/research/0001-workspace-engineering/kubernetes-infrastructure-and-security.md)

### Legacy Task traceability

#### Lifecycle Traceability

| Criterion / work item                                                   | Result | Evidence                                                              |
| ----------------------------------------------------------------------- | ------ | --------------------------------------------------------------------- |
| [VAL-PCDC-001](plan.md) | Done   | ClusterRole parses; both new apiGroups present                        |
| [VAL-PCDC-002](plan.md) | Done   | `endpointslices` excluded as unused at the current pin                |
| [VAL-PCDC-003](plan.md) | Done   | Both installs carry `--version`; `bash -n` clean                      |
| [VAL-PCDC-004](plan.md) | Done   | Script values equal the inventory contract entries                    |
| [VAL-PCDC-005](plan.md) | Done   | Both pins read from the authoritative index and `Chart.yaml`          |
| [VAL-PCDC-006](plan.md) | Done   | ADR-0026 records the adoption case and reversal condition             |
| [VAL-PCDC-007](plan.md) | Done   | Deferred upgrade table with target, prerequisite, and blocking class  |
| [VAL-PCDC-008](plan.md) | Done   | Full lane green at closure; no cluster, registry, or remote contacted |
| [VAL-PCDC-009](plan.md) | Done   | Three commits: `f79fb545` defects, `e6c9b47a` lifecycle, this closure |

### Related Documents

The owning Spec and the reciprocal Plan already link reciprocally in
`## Inputs` and in the table above, so they are recorded here as code literals
rather than duplicated links.

- Owning Spec: `docs/03.specs/0060-platform-currency-defect-closure/spec.md`
- Reciprocal Plan:
  `docs/03.specs/0060-platform-currency-defect-closure/plan.md`
- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [Durable progress ledger](../../00.agent-governance/memory/progress.md)
