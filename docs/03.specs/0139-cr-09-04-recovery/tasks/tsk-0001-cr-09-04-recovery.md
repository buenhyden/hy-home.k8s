---
title: "CR-09.04 Recovery"
version: "0.1.0"
type: "sdlc/task"
owner: "platform"
updated: "2026-10-28"
layer: "specs"
artifact_id: "SPEC-0139-TSK-0001"
parent_ids: ["SPEC-0139-PLAN-0001"]
---

# Task: CR-09.04 Recovery

## Overview

Record why the CR-09.04 secret store failed, how it recovered, and a fresh
read-only live observation. It executes [SPEC-0139](../spec.md) through
[WORK-001–003](../plan.md#work-breakdown).

## Inputs

- Request: on 2026-10-28 the operator chose a read-only root-cause check for
  CR-09.04.
- Start: main `be1ad711`, branch `docs/cr-09-04-recovery`.
- Prior state: [SPEC-0138 Task](../../0138-remaining-decisions-closeout/tasks/tsk-0001-remaining-decisions-closeout.md)
  observed the failure at 08:47Z.

### Cause and Recovery

All times are 2026-10-28 UTC. No secret value was read.

| Time | Event | Source |
| --- | --- | --- |
| 07:33–07:34 | A host `apt-get upgrade` stopped `containerd`; the `openbao` container exited 255 and its `unless-stopped` policy did not restart it | `hy-home.docker` SPEC-0204 Task 0006, "OpenBao outage and v2 recovery", commit `5759bdeeb` |
| until 09:33:12 | The ESO controller logged `unable to log in with Kubernetes auth: json: cannot unmarshal number into Go value of type api.Secret`: the address answered, but not with an OpenBao login response. Every ExternalSecret then failed on the store | `kubectl -n external-secrets logs deploy/external-secrets`, error lines only |
| 09:32:39 | The owner started and unsealed `openbao` under `hy-home.docker` RUN-0103 | The same `hy-home.docker` record |
| 09:33:50 | `vault-backend` became Ready: "store validated" | `kubectl get clustersecretstore vault-backend -o yaml` |
| 09:55:23 | `platform-kiali-config` synced, and the Ingress `istio-system/kiali` was created | `kubectl get application platform-kiali-config -n argocd` |

The cause was the stopped OpenBao server, not the cluster or this repository.
The cluster recovered on its own once the server was back; no cluster change
was needed.

### Live Observation

Read-only, from context `k3d-hyhome` at 2026-10-28T09:57Z.

| Check | Command | Result |
| --- | --- | --- |
| Nodes | `kubectl get nodes` | 4 Ready |
| Pods | `kubectl get pods -A` | 38, all Running |
| Argo CD applications | `kubectl get applications -n argocd` | 22, all Synced Healthy |
| Secret store | `kubectl get clustersecretstore vault-backend` | Valid, ReadWrite, Ready True |
| External secrets | `kubectl get externalsecrets -A` | 6, all `SecretSynced` |
| Secret backend from the host | `curl https://openbao.hy.home.arpa/v1/sys/health`, `/v1/sys/seal-status` | HTTP 200; initialized, unsealed |
| Backend containers | `docker ps --filter name=bao` | `openbao` and `openbao-agent` healthy |
| Certificates | `kubectl get certificates -A`, `kubectl get clusterissuers` | 5 Ready; `mkcert-ca-issuer` Ready |
| Ingress TLS | `openssl s_client -connect 172.18.0.240:443 -servername <host> -verify_return_error` | `argo`, `headlamp`, `rollouts`, `adminer` and `kiali` verify; the earliest expiry is 2026-12-22; Kiali answers HTTP 302 |

Acceptance passes, and CR-09.04 is closed. The OpenBao restart policy and the
other containers that stopped with it stay with `hy-home.docker`.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CR-001](../spec.md#success-criteria--verification-plan) | Record the cause and the recovery | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-CR-002](../spec.md#success-criteria--verification-plan) | Record the post-recovery live observation | platform | draft | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-CR-003](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | draft | NOT_RUN | Pending named repository evidence |

## Task Evidence

| Evidence | Criteria | Work Unit | Check | Input | Result | Location | Required | Resolves |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVD-001 | [VAL-CR-001](../spec.md#success-criteria--verification-plan) | WORK-001 | Cause record and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-002 | [VAL-CR-002](../spec.md#success-criteria--verification-plan) | WORK-002 | Live observation record and review | Exact revision | NOT_RUN | Pending | yes | none |
| EVD-003 | [VAL-CR-003](../spec.md#success-criteria--verification-plan) | WORK-003 | Review and hosted checks | Exact pull request head | NOT_RUN | Pending | yes | none |

## Criterion Acceptance

| Criterion | Acceptance | Evidence | Disposition | Current owner |
| --- | --- | --- | --- | --- |
| [VAL-CR-001](../spec.md#success-criteria--verification-plan) | pending | none | Review remains | platform |
| [VAL-CR-002](../spec.md#success-criteria--verification-plan) | pending | none | Review remains | platform |
| [VAL-CR-003](../spec.md#success-criteria--verification-plan) | pending | none | Review and hosted checks remain | platform |

## Approval and Safety Boundaries

- **Allowed Paths**: this package, the Stage 03 README index and
  `docs/01.requirements/0003-workspace-agent-governance-platform.md`.
- **Forbidden Paths**: other repositories, cluster objects, secrets, the
  OpenBao service, validators and the registry.
- **Approval Required**: the operator chose the read-only check on 2026-10-28
  (Inputs). Push, pull request and merge follow RUN-0013.
- **Static Validation**: `python3 scripts/qa.py staged` on each commit.
- **Live Validation**: read-only `kubectl get`, `kubectl logs` and host-side
  probes only.
- **Secret / Vault Handling**: no secret value is read; only object status,
  error lines and the owner's value-free record.
- **Rollback Plan**: revert the pull request.
- **Evidence Location**: this Task.

## Verification Summary

Not run yet.
