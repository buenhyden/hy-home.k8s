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
- Closure: CR-09.04 closes only when the operator accepts VAL-CR-002; until
  then it stays `EXTERNAL`. The `EXTERNAL` entries in earlier Tasks remain
  history.

### Cause and Recovery

All times are 2026-10-28 UTC. No secret value was read.

| Time | Event | Source |
| --- | --- | --- |
| 07:33–07:34 | A host `apt-get upgrade` stopped `containerd`; the `openbao` container exited 255 and its `unless-stopped` policy did not restart it | `hy-home.docker` SPEC-0204 Task 0006, "OpenBao outage and v2 recovery", commit `5759bdeeb` |
| 08:04:59–08:23:45 | After Docker returned, the ESO controller's log, which starts at 08:04:16, shows login failing on DNS: `lookup openbao.hy.home.arpa on 10.43.0.10:53` refused or timed out. CoreDNS last restarted at about 08:15 | `kubectl -n external-secrets logs deploy/external-secrets`, error lines only; `kubectl -n kube-system get pods -l k8s-app=kube-dns` |
| 08:30:47–09:26:48 | Store validation logged `unable to log in with Kubernetes auth: json: cannot unmarshal number into Go value of type api.Secret` about every seven minutes. A body such as `404 page not found` decodes as the number 404, which matches the HTTP 404 that SPEC-0138 saw at 08:47; which component answered is unverified | The same log; SPEC-0138 Task |
| 08:20:13–09:33:12 | Every ExternalSecret failed with `ClusterSecretStore "vault-backend" is not ready` | The same log |
| 09:31:43 | The owner started `openbao` | `docker inspect` `StartedAt`; the same `hy-home.docker` record |
| 09:32:39 | The owner unsealed it and it became active, then ran RUN-0103 `agent-restart` | The same `hy-home.docker` record |
| 09:33:50 | `vault-backend` became Ready: "store validated" | `kubectl get clustersecretstore vault-backend -o yaml` |
| 09:55:23 | `platform-kiali-config` synced, and the Ingress `istio-system/kiali` was created | `kubectl get application platform-kiali-config -n argocd` |

Inferred from the owner record and the timing: the trigger also disrupted the
cluster's DNS, which recovered by about 08:30; the failure that remained was
the stopped OpenBao server. Nothing in this repository caused it. The store
recovered 71 seconds after the unseal with no cluster change. ESO logs from
07:33 to 08:04 do not exist, so this is not a direct observation.

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
| Ingress TLS | `openssl s_client -connect 172.18.0.240:443 -servername <host> -verify_return_error` | `argo`, `headlamp`, `rollouts`, `adminer`, `kiali` and the apex host verify; the earliest expiry is 2026-12-22; Kiali answers HTTP 302 |

No cluster object was created or changed. Acceptance passes, so CR-09.04
closes on the operator's acceptance of VAL-CR-002. The record in
`hy-home.docker` keeps its own residuals there: the orphaned 10-27 Agent
token, the OpenBao metrics scrape failing since 2026-10-24, and the restart of
`crawl4ai-egress` and `airflow-dag-processor`, which were both Up again by
about 10:05.

## Task Table

### Lifecycle Traceability

| ID | Upstream criterion | Work item | Owner | Status | Result | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| WORK-001 | [VAL-CR-001](../spec.md#success-criteria--verification-plan) | Record the cause and the recovery | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-002 | [VAL-CR-002](../spec.md#success-criteria--verification-plan) | Record the post-recovery live observation | platform | in-progress | NOT_RUN | Pending named repository evidence |
| WORK-003 | [VAL-CR-003](../spec.md#success-criteria--verification-plan) | Independent review and hosted checks | platform | in-progress | NOT_RUN | Pending named repository evidence |

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

An independent read-only reviewer read `939dded1` with the approval change and
re-ran the live checks at about 10:08–10:10Z with no drift. It returned
REQUEST_CHANGES with four medium findings and several low ones:
- the unmarshal error ended at 09:26:48, not 09:33:12;
- the DNS failure phase from 08:05 to 08:24 was missing;
- the start at 09:31:43 was merged with the unseal at 09:32:39;
- closing CR-09.04 needed the operator's acceptance;
- the cause needed to be labelled an inference;
- the apex host was missing;
- the residuals were stale.

All of them are fixed in this revision.
