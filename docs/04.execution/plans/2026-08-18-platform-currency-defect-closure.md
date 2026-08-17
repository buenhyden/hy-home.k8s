---
title: 'Platform Currency Defect Closure Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-08-18
---

# Platform Currency Defect Closure Plan (Plan)

## Overview

This plan executes the bounded remediation designed by
[Spec 059](../../03.specs/059-platform-currency-defect-closure/spec.md). It closes
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

Author ADR 0023 recording the decision, the case for adoption, the preferred
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
[Spec 059](../../03.specs/059-platform-currency-defect-closure/spec.md).

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
| [VAL-PCDC-001](../../03.specs/059-platform-currency-defect-closure/spec.md) | PCDC-001      | [PCDC-001](../tasks/2026-08-18-platform-currency-defect-closure.md) will record the ClusterRole parse and rule check |
| [VAL-PCDC-002](../../03.specs/059-platform-currency-defect-closure/spec.md) | PCDC-001      | [PCDC-001](../tasks/2026-08-18-platform-currency-defect-closure.md) will record why endpointslices was excluded      |
| [VAL-PCDC-003](../../03.specs/059-platform-currency-defect-closure/spec.md) | PCDC-002      | [PCDC-002](../tasks/2026-08-18-platform-currency-defect-closure.md) will record the pins and the shell syntax result |
| [VAL-PCDC-004](../../03.specs/059-platform-currency-defect-closure/spec.md) | PCDC-002      | [PCDC-002](../tasks/2026-08-18-platform-currency-defect-closure.md) will record the script-to-contract comparison    |
| [VAL-PCDC-005](../../03.specs/059-platform-currency-defect-closure/spec.md) | PCDC-002      | [PCDC-002](../tasks/2026-08-18-platform-currency-defect-closure.md) will record the upstream version evidence        |
| [VAL-PCDC-006](../../03.specs/059-platform-currency-defect-closure/spec.md) | PCDC-003      | [PCDC-003](../tasks/2026-08-18-platform-currency-defect-closure.md) will record the decision and reversal condition  |
| [VAL-PCDC-007](../../03.specs/059-platform-currency-defect-closure/spec.md) | PCDC-003      | [PCDC-003](../tasks/2026-08-18-platform-currency-defect-closure.md) will record the deferred upgrade table           |
| [VAL-PCDC-008](../../03.specs/059-platform-currency-defect-closure/spec.md) | PCDC-004      | [PCDC-004](../tasks/2026-08-18-platform-currency-defect-closure.md) will record the full lane results                |
| [VAL-PCDC-009](../../03.specs/059-platform-currency-defect-closure/spec.md) | PCDC-001..004 | [PCDC-001..004](../tasks/2026-08-18-platform-currency-defect-closure.md) will record one commit per logical unit     |

### Related Documents

The owning Spec and the reciprocal Task already link reciprocally in the
`### Lifecycle Traceability` table above, so they are recorded here as code
literals rather than duplicated links.

- Owning Spec: `docs/03.specs/059-platform-currency-defect-closure/spec.md`
- Reciprocal Task:
  `docs/04.execution/tasks/2026-08-18-platform-currency-defect-closure.md`
- [ADR 0023 — Argo CD source integrity non-adoption](../../02.architecture/decisions/0023-argo-cd-source-integrity-non-adoption.md)
- [Tech stack version inventory](../../90.references/data/tech-stack-version-inventory.md)
