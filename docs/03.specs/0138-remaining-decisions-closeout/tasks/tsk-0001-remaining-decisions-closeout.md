---
title: "Remaining Decisions Closeout"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0138-TSK-0001"
parent_ids: ["SPEC-0138-PLAN-0001"]
---

# Task: Remaining Decisions Closeout

## Overview

Record the operator's decisions on the last open survey CRs and on SPEC-0103,
and the read-only live observation for CR-09.04. It executes
[SPEC-0138](../spec.md) through [WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request: on 2026-10-28 the operator chose options 1-A, 2-A, 3-A and 4-A from
  the review of the remaining items.
- Start: main `860fccb7`, branch `docs/remaining-decisions-closeout`.

### Decisions

| Item | Decision on 2026-10-28 | Effect |
| --- | --- | --- |
| CR-03.06, CR-03.07 | The four repositories stay independent; no shared edition binds them. On 2026-10-28 they used three version schemes: SemVer here and in `Project-Template`, date tags in `blog-data`, none in `hy-home.docker` | Closed |
| CR-08.01 | Each repository keeps its own Archive contract; the layouts recorded in SPEC-0135 stay as they are | Closed |
| CR-14.03 | GitHub Projects are not used for status; the Task stays the status source. The one closed, empty user Project stays untouched | Closed as not applicable |
| SPEC-0103 | It stays `usable` for good, because the older-form SPEC-0105 Task 0003 links to it and is not migrated | Final |

### CR-09.04 Live Observation

Read-only, from context `k3d-hyhome` (server `v1.35.0+k3s1`) at
2026-10-28T08:47Z. No cluster object was created or changed. One probe that
would have created a temporary pod for in-cluster DNS was refused by the
permission layer and not rerun.

| Check | Command | Result |
| --- | --- | --- |
| Nodes | `kubectl get nodes` | 4 Ready: `k3d-hyhome-server-0` and three agents |
| Pods | `kubectl get pods -A` | 38, all Running |
| Argo CD applications | `kubectl get applications -n argocd` | 22: 18 Synced Healthy; `platform-argocd-config`, `platform-eso-config` and `platform-monitoring` Synced Degraded; `platform-kiali-config` OutOfSync Degraded, its last sync failed after three retries and its Ingress `istio-system/kiali` is absent |
| Secret store | `kubectl get clustersecretstore vault-backend` | Ready False, `InvalidProviderConfig`: "unable to create client"; server `https://openbao.hy.home.arpa`, path `secret`, KV v2, Kubernetes role `eso-read-platform` |
| External secrets | `kubectl get externalsecrets -A` | 6, all `SecretSyncedError`: "could not get secret data from provider" |
| Secret backend from the host | `getent hosts openbao.hy.home.arpa`; `curl https://openbao.hy.home.arpa/v1/sys/health` | Resolves to `192.168.0.13`; TLS verifies; HTTP 404 |
| Certificates | `kubectl get certificates -A`, `kubectl get clusterissuers` | 4 Ready; `mkcert-ca-issuer` Ready |
| Ingress TLS | `openssl s_client -connect 172.18.0.240:443 -servername <host>` | `argo`, `headlamp`, `rollouts`, `adminer` and the apex host each present a certificate whose SAN covers the host; the earliest expiry is 2026-12-22 |

Acceptance fails: the secret backend the platform depends on is unavailable,
so four platform applications are Degraded. Ingress and certificate serving
pass. Repair changes a secret, the cluster or the OpenBao service in
`hy-home.docker`, and needs a separate operator approval; RUN-0002 is the
recovery procedure. CR-09.04 stays `EXTERNAL` with the operator as next owner.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-RC-001](../spec.md#success-criteria--verification-plan) | Record the operator decisions | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-RC-002](../spec.md#success-criteria--verification-plan) | Record the read-only live observation for CR-09.04 | platform | ready | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-RC-003](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | ready | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-RC-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Decision record and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-RC-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Live observation record and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-RC-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-RC-001](../spec.md#success-criteria--verification-plan) | pending | none | Review remains | platform |
| [VAL-RC-002](../spec.md#success-criteria--verification-plan) | pending | none | Review remains | platform |
| [VAL-RC-003](../spec.md#success-criteria--verification-plan) | pending | none | Review and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index and
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`.
- **Forbidden Paths**: other repositories, cluster objects, secrets, Projects,
  validators and the registry.
- **Approval Required**: the operator decided on 2026-10-28 (Inputs). Push,
  pull request and merge follow RUN-0013.
- **Static Validation**: `python3 scripts/qa.py staged` on each commit.
- **Live Validation**: read-only `kubectl get` and host-side probes only.
- **Secret / Vault Handling**: no secret value is read; only object status and
  the store's server, path and role names.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
