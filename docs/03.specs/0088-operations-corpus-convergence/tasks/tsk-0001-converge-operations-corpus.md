---
title: "Converge the Operations Corpus"
version: "0.1.0"
type: "sdlc/task"
status: "queued"
owner: "platform"
updated: "2026-09-25"
layer: "specs"
artifact_id: "SPEC-0088-TSK-0001"
---

# Task: Converge the Operations Corpus

## Overview

Execute [SPEC-0088-PLAN-0001](../plan.md). The request owner authorized the
audit, the cleanup, and logical local commits on 2026-09-25, and did not
authorize push, pull request, merge, remote protection changes, or live
actions.

## Inputs

- [Owning Spec](../spec.md)
- [Owning Plan](../plan.md)
- [ADR-0040](../../../02.architecture/decisions/0040-archive-reappraisal-and-verifiable-sources.md)
- [Operations Index](../../../05.operations/README.md)
- [Archive Index](../../../98.archive/README.md)

## Task Table

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | VAL-OCC-002, VAL-OCC-004 | Survey Stage 05, Stage 98 Operations units, and scripts | platform | Done | Survey below | This Task |
| WORK-002 | VAL-OCC-003, VAL-OCC-005 | Remove dead or duplicate validation logic and close the secret-output gap | platform | Queued | Not executed | Focused tests and staged QA |
| WORK-003 | VAL-OCC-001, VAL-OCC-002 | Converge Stage 05 ownership and facts | platform | Queued | Not executed | Document gates and staged QA |
| WORK-004 | VAL-OCC-004, VAL-OCC-006 | Record dispositions and final evidence | platform | Queued | Not executed | Full QA |

## Approval and Safety Boundaries

- **Allowed Paths**: `docs/05.operations/`, `scripts/`, the tests that are the only consumers of removed code, `docs/03.specs/README.md`, and this package
- **Forbidden Paths**: `gitops/`, `infrastructure/`, `.github/`, any Stage 98 body, frozen record, or sealed ledger, and the Stage 99 registry
- **Approval Required**: push, pull request, merge, remote protection, Stage 98 removal, and any live cluster or OpenBao action
- **Static Validation**: focused tests, document gates, `python3 scripts/qa.py staged` per commit, and `python3 scripts/qa.py full` on the final tree
- **Live Validation**: DEFER; no live system is in scope, and runbook commands were compared with manifests, not executed
- **Secret / Vault Handling**: no secret value is read; runbooks now avoid secret-value output
- **Rollback Plan**: revert each local commit; Git restores every removed byte
- **Evidence Location**: this Task

## Verification Summary

### Survey (2026-09-25, `main` at `a939999a`)

Stage 05 drift against the implementation:

| Document | Finding | Current fact |
| --- | --- | --- |
| RUN-0007 | Treated ArgoCD `resource.exclusions` of EndpointSlice as a cause and made live patching the normal path | No exclusions exist; `platform-external-services` reconciles the EndpointSlices |
| RUN-0007 | Patched `alloy-external-1` and `loki-external-1`, which Kiali does not use | Kiali reaches Prometheus and Grafana through Traefik and Tempo through `tempo-external` |
| RUN-0007 | Named NetworkPolicy `argocd-egress-to-external-valkey` and said Grafana `in_cluster_url` uses service DNS | Kiali's policy is `allow-kiali-egress-to-observability`; `in_cluster_url` is `https://grafana.hy.home.arpa` |
| RUN-0001 | Called `vault-backend` an in-cluster HTTP exception | ESO uses `https://openbao.hy.home.arpa` with the `openbao-ca` bundle |
| RUN-0001 | Required `secret/platform/postgres-app` and cited a bootstrap error string | Bootstrap reads only `platform/argocd`; it prints no such string |
| RUN-0001 | Recovery check printed a Secret with `-o yaml` | Readiness is read from the ExternalSecret |
| RUN-0002 | Rollback deleted `coredns-custom` | Deleting the zone breaks every external name; the rollback restores a snapshot |
| POL-0004 | Named app versions that no manifest pins, and a partial subscription list | Chart versions live in each Application; `defaultTriggers` and the `slack:hy-home-alerts` subscription live in the ConfigMap |
| POL-0004, RUN-0004 | Said SPEC-0004 and SPEC-0005 are retained under ADR-0039 | ADR-0040 is current; both are in `completed/` |
| POL-0007 | Omitted the `4317` OTLP egress and the Istiod ports | `allow-egress-apps` allows both |

Stage 05 duplicate ownership:

| Topic | Owners found | Single owner now |
| --- | --- | --- |
| External Service/EndpointSlice recovery | RUN-0001, RUN-0007, RUN-0009 | RUN-0001 External Endpoint Recovery |
| CoreDNS zone and gateway CA ConfigMap re-application | RUN-0002, RUN-0007, RUN-0009 | RUN-0002 Procedure step 4 |
| ArgoCD metric target recovery | RUN-0008, RUN-0009 | RUN-0008 |
| Sealed OpenBao remediation | Two sections of RUN-0002 | RUN-0002 Procedure |
| App Vault path rule | POL-0007, RUN-0010, pinned in both by the quality validator | POL-0007 |
| Hook path, lint ownership, lifecycle and citation rules | GDE-0010, RUN-0011 restating `.agents` | The `.agents` policies, linked |
| Marker rule | Stage 05 index listed a subset of what the validator accepts | Stage 05 index table mirrors the validator |

Stage 98 Operations units: only two, the Headlamp OIDC guide `tomb-GDE-0004`
and the Keycloak runbook `tomb-RUN-0005`, both frozen ADR-0032-generation
sealed records under `superseded/05.operations/`. No active document links
them. They have no Retention Catalog row, so the Retention Assessment cannot
judge them, and ADR-0040 excludes the frozen generation from reappraisal.
They are kept. Current consumer: the Archive index manifest and the archive
validators that verify every sealed record. Unique responsibility: the sealed
provenance of the retired Headlamp authentication flow. Removal condition: an
accepted decision that brings the ADR-0032 generation under reappraisal,
followed by an approved assessment row. `docs/98.archive/migrations/` is kept
for the same reason: route records carry no assessment, and validators read
MIG-0001 to MIG-0009 by path.

Scripts: every file has a current consumer, so no whole file is removed. The
round removes dead branches and duplicated rules inside live files.

## Traceability

### Lifecycle Traceability

| Criterion / work item | Result | Evidence |
| --- | --- | --- |
| [WORK-001](../plan.md#work-breakdown) | Survey recorded | This Task |
| [WORK-002](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-003](../plan.md#work-breakdown) | Not executed | Pending |
| [WORK-004](../plan.md#work-breakdown) | Not executed | Pending |
