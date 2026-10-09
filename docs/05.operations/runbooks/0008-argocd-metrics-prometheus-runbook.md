---
title: "ArgoCD 메트릭 Prometheus 수집 복구 Runbook"
version: "2.3.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-10-09"
layer: "operations"
artifact_id: "RUN-0008"
---

# ArgoCD 메트릭 Prometheus 수집 복구 Runbook

## Purpose

이 런북은 외부 Prometheus에서 ArgoCD 메트릭이 조회되지 않을 때 ArgoCD 쪽 원인을
진단하고 복구하는 절차를 제공한다.

ArgoCD 메트릭은 cluster 안 Alloy가 pod IP로 scrape해 외부 Prometheus로 remote
write한다([ADR-0045](../../02.architecture/decisions/0045-in-cluster-telemetry-collection.md)).
job 이름은 `kubernetes-pods`이고 component는 `app` label로 구분한다. NodePort
static scrape(`30082-30086`)는 폐지되었다. Alloy 자체, remote write, egress 장애는
[RUN-0009](./0009-k8s-observability-runbook.md)가 소유한다.

| component (`app`) | container port |
| --- | --- |
| `argocd-application-controller` | `8082` |
| `argocd-server` | `8083` |
| `argocd-repo-server` | `8084` |
| `argocd-applicationset-controller` | `8080` |
| `argocd-notifications-controller` | `9001` |

주된 원인은 세 가지다:

1. **ArgoCD pod 미기동**: component가 Running이 아니면 relabel 규칙이 target에서 뺀다.
2. **label 또는 port 변경**: chart 업그레이드로 `app.kubernetes.io/name`이나 metrics
   port가 바뀌면 `discovery.relabel "platform_pods"` 규칙과 어긋난다.
3. **수집 경로 장애**: 다른 k8s 메트릭도 함께 비어 있으면 ArgoCD 문제가 아니다.

## Trigger and Preconditions

- `argocd_app_info{cluster="k3d-hyhome"}`가 조회되지 않을 때
- `kubernetes-pods` job에서 ArgoCD component 일부가 빠졌을 때
- ArgoCD Helm chart를 업그레이드한 뒤

---

## Procedure

외부 Prometheus 쿼리는 [RUN-0009](./0009-k8s-observability-runbook.md)의
승인된 인증 조회 경로로 외부 observability 운영자에게 요청한다. 여기서는
PromQL과 비밀값을 제외한 집계 결과만 공유한다. 인증 경로가 없으면 쿼리
결과를 `DEFER`하고 아래 Kubernetes metadata 대조를 진행한다.

### Procedure 1: 범위 판단

PromQL: `count by (job) (up{cluster="k3d-hyhome"})`

job 자체가 없으면 ArgoCD가 아니라 수집 경로 문제다. RUN-0009로 이동한다.

### Procedure 2: ArgoCD component target 확인

PromQL: `up{cluster="k3d-hyhome",namespace="argocd"}`

```bash
kubectl get pods -n argocd -L app.kubernetes.io/name
```

- 빠진 component의 pod가 Running이 아니면 pod 상태부터 복구한다.
- pod는 Running인데 target이 없으면 Procedure 3으로 이동한다.

### Procedure 3: label과 port 대조

```bash
kubectl get pods -n argocd \
  -o custom-columns='NAME:.metadata.labels.app\.kubernetes\.io/name,PORTS:.spec.containers[*].ports[*].containerPort'
rg -n 'argocd-\(' gitops/platform/monitoring/alloy-k8s-logs.yaml
```

위 표와 다르면 `gitops/platform/monitoring/alloy-k8s-logs.yaml`의 `platform_pods`
규칙을 고치고 커밋한 뒤 reconciliation으로 반영한다.

```bash
# operator-triggered reconciliation only
argocd app sync platform-monitoring
```

---

## Verification

| PromQL | 기대 관측 |
| --- | --- |
| `count by (app) (up{cluster="k3d-hyhome",namespace="argocd"} == 1)` | 위 표의 component 다섯 개 |
| `count(argocd_app_info{cluster="k3d-hyhome"})` | `gitops/apps/root`가 정의한 Application 수 이상 |

현재 조회 결과가 없으면 이 런북의 원격 메트릭 수용을 `DEFER`한다.

---

- **Signals**: ArgoCD component pod readiness, `up{namespace="argocd"}` by `app`, `argocd_app_info` count.
- **Evidence to Capture**: query output, pod label and port listing, changed relabel rule diff.

## Recovery and Escalation

- Incorrect relabel rule changes should be reverted through GitOps.
- ArgoCD chart changes that renamed components are reverted in `infrastructure/argocd/values-local.yaml` or the relabel rule is updated to match.
- Do not reintroduce metrics NodePort Services; the static check rejects them.

---

## Related Documents

- **k8s Observability Runbook**: [`./0009-k8s-observability-runbook.md`](./0009-k8s-observability-runbook.md)
- [Operations Policy](../policies/0005-observability-platform-operations-policy.md)
- [Alloy configuration](../../../gitops/platform/monitoring/alloy-k8s-logs.yaml)

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [Observability Platform Operations Policy](../policies/0005-observability-platform-operations-policy.md) | ArgoCD component targets or `argocd_app_info` are missing from the in-cluster collection. | Platform operator records component target, pod, and query evidence; GitOps owner restores ArgoCD pods or the Alloy relabel rule. |
