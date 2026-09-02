---
title: 'Platform Currency Defect Closure Technical Specification'
version: "1.0.0"
type: sdlc/spec
layer: "specs"
status: done
owner: platform
updated: 2026-08-18
artifact_id: "SPEC-0060"
---

# Platform Currency Defect Closure Technical Specification (Spec)

## Overview

This specification designs a bounded remediation cycle over the platform's
version-currency surface. It follows the 2026-08-17 full-corpus research refresh,
whose evaluation of two fired refresh triggers surfaced defects that the triggers
themselves did not name.

The evaluation examined every versioned dependency the repository declares and
found six drift items: four pinned images (`adminer` at `4.8.1`,
`grafana/alloy` at `v1.13.1`, `rancher/k3s` at `v1.35.0-k3s1`, and
`kube-state-metrics` at `v2.14.0`) and two Helm charts installed with no version
pin at all (`metallb` and `argo-cd`). It also produced a fit assessment for Argo
CD's newly GA `sourceIntegrity` facility.

This cycle deliberately separates defect closure from version upgrade. Two of the
six items are live defects that exist independently of any upgrade, and one is a
design decision that can be settled now. The four version upgrades are deferred,
because their success is `live-cluster` blocked and their evaluation is
incomplete.

The scoping correction matters more than the individual fixes. The fired triggers
pointed at `kube-state-metrics` and Argo CD `sourceIntegrity`. Neither was the
most urgent finding. The most urgent was a missing RBAC grant that had nothing to
do with a version bump, and the highest-leverage was a contract hole that made
bootstrap non-reproducible. A cycle scoped to the triggers alone would have
missed both.

Direct human approval on 2026-08-18 authorizes this standalone execution relation.
That approval selected defect closure plus the decision record over a wider scope
that included version upgrades, and confirmed the concrete change set before any
manifest was edited.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.

## Strategic Boundaries & Non-goals

### In scope

- Granting `kube-state-metrics` the RBAC its default collectors require:
  `certificates.k8s.io/certificatesigningrequests` and
  `coordination.k8s.io/leases`, both `list` and `watch`.
- Pinning the two bootstrap-phase Helm installs in
  `infrastructure/bootstrap-local.sh` to explicit chart versions.
- Extending `docs/90.references/data/tech-stack-version-inventory.md` with a
  `bootstrap_helm_charts` contract so the inventory covers the two charts that
  GitOps does not own.
- Recording the decision not to adopt Argo CD `sourceIntegrity` as
  [ADR-0029](../../02.architecture/decisions/0026-argo-cd-source-integrity-non-adoption.md).
- Repository-static validation evidence and logical-unit commits.

### Out of scope and non-goals

- Upgrading `kube-state-metrics`, `rancher/k3s`, `adminer`, or `grafana/alloy`.
  Each is deferred to a separate cycle with its own evaluation.
- Granting `discovery.k8s.io/endpointslices`. It becomes a default resource only
  at `kube-state-metrics` `v2.18.0`; at the pinned `v2.14.0` the already-granted
  core `endpoints` rule is what the default set uses, so granting it now would
  be an unused permission.
- Adopting `sourceIntegrity`, configuring GPG keys, or establishing a
  commit-signing workflow.
- Pinning `targetRevision` to commit SHAs. It is the stronger control for the
  recorded identity gap and is named as the preferred alternative in ADR-0026,
  but it is a separate design change affecting twelve declarations.
- Any live k3d, ArgoCD, Vault, ESO, cluster, or registry action. No cluster is
  contacted and no reconciliation is triggered.
- Verifying that every value path in `infrastructure/argocd/values-local.yaml`
  remains valid in chart `10.4.0`. That risk is identical with and without the
  pin and belongs to the deferred upgrade evaluation.
- Pushing any branch to a remote or publishing any artifact.

## Contracts

### C-PCDC-001 — defect closure is not upgrade

A change qualifies for this cycle only if it corrects a condition that is already
wrong at the currently pinned versions. A change whose purpose is to move to a
newer version is out of scope regardless of how small it is.

### C-PCDC-002 — no speculative permission

An RBAC rule is added only when a collector that runs at the current pin requires
it. A rule required only after a future upgrade is recorded as that upgrade's
prerequisite, not granted in advance.

### C-PCDC-003 — pin to the resolved current version

A newly introduced version pin records the version an unpinned install resolves
to at the time of pinning, read from the authoritative repository index or
`Chart.yaml`. This makes the pin determinism-positive and risk-neutral: it cannot
change what a run installs today, only freeze it.

### C-PCDC-004 — script and contract must agree

Every `--version` value in `infrastructure/bootstrap-local.sh` has a matching
entry in the `bootstrap_helm_charts` block of the version inventory. A
disagreement is a defect.

### C-PCDC-005 — decision records state the case against themselves

An ADR that declines a capability records the strongest argument for adoption,
not only the argument against, and names what would reverse the decision.

### C-PCDC-006 — no live claim

Static manifest, script, and contract changes establish declared intent only.
Effective RBAC, admission, reconciliation, chart resolution, and cluster state
remain `live-cluster` blocked and are not promoted by any result in this cycle.

### C-PCDC-007 — logical work units

Each work package is one commit with its own validation evidence.

## Core Design

The cycle runs as four work packages.

| ID       | Package                      | Surface                                        |
| -------- | ---------------------------- | ---------------------------------------------- |
| PCDC-001 | kube-state-metrics RBAC      | `gitops/platform/monitoring/`                  |
| PCDC-002 | Bootstrap chart version pins | `infrastructure/`, version inventory           |
| PCDC-003 | sourceIntegrity non-adoption | `docs/02.architecture/decisions/`              |
| PCDC-004 | Lifecycle registration       | Stage 03/04 indexes, profiles, progress ledger |

`PCDC-001` and `PCDC-002` were committed as one logical unit because both are
version-currency defect closures on the same surface class and share one
validation lane. `PCDC-003` lands separately because it is a decision record
rather than a code change.

## Data Modeling & Storage Strategy

This cycle adds no new storage location. Each change lands with its existing
canonical owner.

| Artifact                   | Owner                                                     |
| -------------------------- | --------------------------------------------------------- |
| ClusterRole rules          | `gitops/platform/monitoring/kube-state-metrics.yaml`      |
| Bootstrap chart pins       | `infrastructure/bootstrap-local.sh`                       |
| Bootstrap version contract | `docs/90.references/data/tech-stack-version-inventory.md` |
| Non-adoption decision      | `docs/02.architecture/decisions/0023-*.md`                |
| Deferred upgrade evidence  | the 2026-08-08 research pack's dated sections             |
| Durable cycle record       | `docs/00.agent-governance/memory/progress.md`             |

## Interfaces & Data Structures

### Bootstrap chart contract entry

Each entry describes an operator-approved bootstrap install. Recording the command
shape here is contract documentation; no agent executes it.

| Field         | Meaning                                                        |
| ------------- | -------------------------------------------------------------- |
| `repoURL`     | Helm repository the bootstrap script adds                      |
| `chart`       | chart name as passed to `helm upgrade --install`               |
| `version`     | exact chart version, matching the script's `--version`         |
| `appVersion`  | application version the chart ships, recorded for traceability |
| `installedBy` | the exact bootstrap step that installs it                      |

### Deferred upgrade record

| Field           | Meaning                           |
| --------------- | --------------------------------- |
| `component`     | pinned dependency                 |
| `current`       | version pinned today              |
| `target`        | evaluated recommendation          |
| `prerequisite`  | what must land before the upgrade |
| `blockingClass` | evidence class that gates success |

## Edge Cases & Error Handling

- **A pin value disagrees between script and inventory.** Treated as a defect
  under `C-PCDC-004` and fixed before the package commits.
- **An upstream index reports a different version than a release page.** The
  repository index or `Chart.yaml` wins, because that is what `helm` resolves
  against. This occurred: a release page reported a 2024 date for the `metallb`
  chart while the repository index reported `2026-05-27`.
- **A chart version is a placeholder.** `metallb`'s `main` branch `Chart.yaml`
  carries `0.0.0`, filled by its release process. The released version is read
  from the repository index instead.
- **An RBAC addition turns out to be needed only after upgrade.** Recorded as an
  upgrade prerequisite under `C-PCDC-002` and not granted.
- **The values file may not match the pinned chart.** Recorded as a limitation
  rather than silently assumed compatible, because the same risk exists unpinned.

## Failure Modes & Fallback / Human Escalation

| Failure                                     | Response                                                       |
| ------------------------------------------- | -------------------------------------------------------------- |
| Shell syntax check fails                    | Fix before commit; `bash -n` gates the script change           |
| Manifest fails YAML parse or a validator    | Revert the package commit, fix, re-run the full lane           |
| An upstream version cannot be verified      | Do not pin a guessed value; escalate for a named version       |
| A pin would change the installed version    | Stop; `C-PCDC-003` permits only the currently resolved version |
| Evidence would require contacting a cluster | Stop and record the boundary; never contact the cluster        |

Escalation is to the human partner in every row. No fallback lowers the evidence
bar, and no static `PASS` promotes a `live-cluster` boundary.

## Verification Commands

```bash
bash -n infrastructure/bootstrap-local.sh
bash scripts/validate-repo-quality-gates.sh .
python3 scripts/validate-links-and-owners.py --root . --mode strict
python3 scripts/validate-markdown-profiles.py --root . --mode strict
python3 scripts/validate-document-contract-registry.py --root . --mode strict
python3 scripts/validate-affected-surfaces.py --root .
python3 scripts/validate-vault-eso-contracts.py --root .
git diff --check
```

## Success Criteria & Verification Plan

| ID           | Criterion                                                                    |
| ------------ | ---------------------------------------------------------------------------- |
| VAL-PCDC-001 | The ClusterRole grants both default-collector apiGroups and parses as YAML   |
| VAL-PCDC-002 | No permission is granted that the currently pinned version does not use      |
| VAL-PCDC-003 | Both bootstrap installs carry `--version` and the script passes `bash -n`    |
| VAL-PCDC-004 | Every script `--version` matches its `bootstrap_helm_charts` inventory entry |
| VAL-PCDC-005 | Each pinned version equals what an unpinned install resolves to today        |
| VAL-PCDC-006 | ADR-0026 records the case for adoption and a named reversal condition        |
| VAL-PCDC-007 | Deferred upgrades are recorded with target, prerequisite, and blocking class |
| VAL-PCDC-008 | The full verification lane passes and no cluster was contacted               |
| VAL-PCDC-009 | One commit per logical unit with its own evidence                            |

## Traceability

This Spec is a bounded remediation design requested directly by the human, who
approved the scope and then confirmed the concrete change set before any manifest
was edited. It creates no PRD or AD. It is the seventh typed
standalone-execution relation under ADR 0022, with a reciprocal
[Plan](plan.md)
and [Task](README.md#task-records).
Its evaluation input is the 2026-08-17 cycle recorded by
[Spec 0059](../0059-workspace-research-full-corpus-refresh/spec.md).

Direct human approval on 2026-08-18 authorizes this standalone execution relation.
No separate PRD or Architecture Description is required or part of this standalone lifecycle.

### Lifecycle Traceability

| PRD requirement                                                  | Spec criterion | Verification method                        |
| ---------------------------------------------------------------- | -------------- | ------------------------------------------ |
| N/A — direct human request to close live currency defects        | VAL-PCDC-001   | ClusterRole rule and YAML parse check      |
| N/A — direct human decision to exclude speculative permissions   | VAL-PCDC-002   | Rule-by-rule scope review                  |
| N/A — direct human request for reproducible bootstrap            | VAL-PCDC-003   | Script grep and `bash -n`                  |
| N/A — direct human request that contracts cover the same surface | VAL-PCDC-004   | Script-to-inventory value comparison       |
| N/A — direct human approval of risk-neutral pinning              | VAL-PCDC-005   | Upstream index and `Chart.yaml` comparison |
| N/A — direct human decision to settle the adoption question      | VAL-PCDC-006   | ADR content review                         |
| N/A — direct human decision to defer version upgrades            | VAL-PCDC-007   | Deferred-upgrade record review             |
| N/A — direct human request for validation evidence               | VAL-PCDC-008   | Full verification lane results             |
| N/A — direct human request for logical-unit commits              | VAL-PCDC-009   | Commit log review                          |

### Related Documents

- [ADR 0022 — direct-approval standalone execution lineage](../../02.architecture/decisions/0022-direct-approval-standalone-execution-lineage.md)
- [ADR-0026 — Argo CD source integrity non-adoption](../../02.architecture/decisions/0026-argo-cd-source-integrity-non-adoption.md)
- [Kubernetes infrastructure and security research](../../90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md)
- [Kubernetes, infrastructure, and security research](../../90.references/research/0001-workspace-engineering/m0007-kubernetes-infrastructure-and-security.md)
- [Quality standards](../../00.agent-governance/rules/quality-standards.md)
