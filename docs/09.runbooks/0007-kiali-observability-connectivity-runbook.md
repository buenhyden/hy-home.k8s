# Kiali Observability 연결 복구 Runbook

## Runbook Type

`WSL2 k3d/k3s 운영 핫픽스 및 복구`

## Overview (KR)

이 런북은 Kiali에서 Grafana, Prometheus, Tempo 등 외부 관측성 서비스가 Unreachable로 표시되는 장애를 진단하고 복구하는 절차를 제공한다.

주된 원인은 두 가지다:

1. **Docker 네트워크 재할당**: k3d-hyhome 네트워크가 재시작되면 외부 컨테이너(infra-grafana 등)의 IP가 변경된다. `gitops/platform/external-services/` 아래의 EndpointSlice YAML과 Kiali ConfigMap의 Grafana URL이 구 IP를 가리키게 되어 연결이 끊긴다.
2. **ArgoCD EndpointSlice 제외**: ArgoCD는 `discovery.k8s.io/EndpointSlice` 리소스를 기본 resource.exclusions에 포함하여 직접 관리하지 않는다. 따라서 YAML을 수정하고 커밋해도 EndpointSlice가 자동으로 클러스터에 동기화되지 않는다. 수동 `kubectl apply`가 필수다.

## When to Use

- Kiali에서 Grafana/Prometheus/Tempo가 unreachable로 표시될 때
- EndpointSlice IP가 변경된 후
- Docker 네트워크 재시작 후 컨테이너 IP가 변경되었을 때
- `kubectl get endpointslice -n platform`에서 alloy, loki, grafana의 주소가 비어있거나 없을 때

---

## k3d-hyhome 올바른 IP 할당표

| 컨테이너         | IP          | 포트        |
| ---------------- | ----------- | ----------- |
| infra-prometheus | 172.18.0.10 | 9090        |
| infra-alloy      | 172.18.0.11 | 4317 / 4318 |
| infra-tempo      | 172.18.0.12 | 3200        |
| infra-loki       | 172.18.0.13 | 3100        |
| infra-grafana    | 172.18.0.14 | 3000        |

> IP가 변경되었다면 먼저 실제 할당 IP를 확인한 뒤 아래 절차를 진행한다.

---

## Procedure 1: 연결 상태 진단

### 1-1. 현재 EndpointSlice IP 확인

```bash
kubectl get endpointslice -n platform
```

출력 예시에서 `ENDPOINTS` 컬럼이 비어있거나 구 IP를 가리키면 문제 있음.

### 1-2. 컨테이너 실제 IP 확인 (WSL2 호스트에서)

```bash
docker inspect infra-grafana --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
docker inspect infra-alloy   --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
docker inspect infra-loki    --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

### 1-3. Kiali 파드에서 직접 연결 테스트

`nc`는 Kiali 컨테이너 내에서 오동작할 수 있으므로 반드시 `bash /dev/tcp`를 사용한다.

```bash
KIALI_POD=$(kubectl get pod -n istio-system -l app=kiali -o jsonpath='{.items[0].metadata.name}')

# Grafana 연결 테스트
kubectl exec -n istio-system "$KIALI_POD" -- \
  bash -c 'timeout 5 bash -c "echo >/dev/tcp/172.18.0.14/3000" && echo OK || echo FAIL'

# Prometheus 연결 테스트
kubectl exec -n istio-system "$KIALI_POD" -- \
  bash -c 'timeout 5 bash -c "echo >/dev/tcp/172.18.0.10/9090" && echo OK || echo FAIL'
```

### 1-4. ArgoCD resource.exclusions 확인

```bash
kubectl get configmap argocd-cm -n argocd \
  -o jsonpath='{.data.resource\.exclusions}'
```

출력에 `EndpointSlice`가 포함되어 있으면 ArgoCD가 해당 리소스를 동기화하지 않음을 확인한다.

---

## Procedure 2: EndpointSlice IP 업데이트

### 2-1. 기존 EndpointSlice 패치 (즉시 적용)

```bash
# Grafana
kubectl patch endpointslice grafana-external-1 -n platform --type=json \
  -p='[{"op":"replace","path":"/endpoints/0/addresses/0","value":"172.18.0.14"}]'

# Alloy (EndpointSlice가 없으면 2-2 참고)
kubectl patch endpointslice alloy-external-1 -n platform --type=json \
  -p='[{"op":"replace","path":"/endpoints/0/addresses/0","value":"172.18.0.11"}]'

# Loki (EndpointSlice가 없으면 2-2 참고)
kubectl patch endpointslice loki-external-1 -n platform --type=json \
  -p='[{"op":"replace","path":"/endpoints/0/addresses/0","value":"172.18.0.13"}]'
```

### 2-2. 누락된 EndpointSlice 생성 (kubectl apply)

ArgoCD가 동기화하지 않으므로 직접 apply해야 한다.

```bash
kubectl apply -f gitops/platform/external-services/alloy-external.yaml
kubectl apply -f gitops/platform/external-services/loki-external.yaml
kubectl apply -f gitops/platform/external-services/grafana-external.yaml
```

### 2-3. git 파일도 올바른 IP로 수정 후 커밋

```bash
# gitops/platform/external-services/grafana-external.yaml 에서 IP 수정 후
git add gitops/platform/external-services/
git commit -m "chore: update external service endpoint IPs after network reassignment"
```

> **주의**: git 커밋만으로는 클러스터에 반영되지 않는다. `kubectl apply` 또는 `kubectl patch`를 별도로 실행해야 한다.

### 2-4. 적용 결과 확인

```bash
kubectl get endpointslice -n platform
kubectl describe endpointslice grafana-external-1 -n platform
```

---

## Procedure 3: NetworkPolicy egress 규칙 점검

NetworkPolicy의 egress `ipBlock` 규칙은 **post-DNAT 기준 IP**로 작성해야 한다. 컨테이너 IP가 바뀌면 해당 NetworkPolicy도 함께 업데이트한다.

### 3-1. 현재 egress ipBlock 확인

```bash
kubectl get networkpolicy -n istio-system -o yaml | grep -A5 ipBlock
```

### 3-2. ArgoCD egress NetworkPolicy 확인

```bash
kubectl get networkpolicy -n argocd argocd-egress-to-external-valkey -o yaml
```

### 3-3. 수정이 필요한 경우

`gitops/platform/network-policies/` 하위 NetworkPolicy YAML의 `ipBlock.cidr`를 실제 IP로 수정하고 git 커밋한다. NetworkPolicy는 ArgoCD가 정상 동기화하므로 커밋 후 ArgoCD Sync로 적용 가능하다.

```bash
# ArgoCD Sync 강제 실행
argocd app sync platform-network-policies --force
```

---

## Procedure 4: Kiali Grafana URL 설정 확인

Kiali의 Grafana 연동 URL은 ArgoCD App의 Helm values 또는 ConfigMap에서 관리된다.

### 4-1. 현재 설정된 URL 확인

```bash
# platform-kiali-app의 Grafana URL 확인
kubectl get app platform-kiali-app -n argocd -o jsonpath='{.spec.source.helm.values}'
```

또는 직접 파일에서 확인:

```bash
grep -i grafana gitops/apps/root/platform-kiali-app.yaml
```

### 4-2. URL이 구 IP를 가리키는 경우

`gitops/apps/root/platform-kiali-app.yaml`에서 Grafana URL을 현재 IP로 수정한다.

```yaml
# 예시: 구 IP → 신 IP
# 수정 전: http://172.19.0.24:3000
# 수정 후: http://172.18.0.14:3000
```

수정 후 커밋하고 ArgoCD Sync를 실행한다:

```bash
git add gitops/apps/root/platform-kiali-app.yaml
git commit -m "chore: update Kiali Grafana URL to current IP"
argocd app sync platform-kiali-app
```

### 4-3. Kiali ConfigMap 직접 확인 (선택)

```bash
kubectl get configmap kiali -n istio-system -o yaml | grep -A3 grafana
```

---

## 주의사항: ArgoCD EndpointSlice 제외

ArgoCD는 `discovery.k8s.io/EndpointSlice`를 `resource.exclusions`에 포함하여 기본적으로 관리하지 않는다.

**이로 인한 영향:**

- `gitops/platform/external-services/*.yaml`에 EndpointSlice를 커밋하고 ArgoCD Sync해도 클러스터에 반영되지 않는다.
- 클러스터에 EndpointSlice가 없어도 ArgoCD 앱 상태가 `Synced`로 표시될 수 있다.
- IP 변경 시 git 수정과 함께 반드시 `kubectl apply` 또는 `kubectl patch`를 수동으로 실행해야 한다.

**확인 방법:**

```bash
kubectl get configmap argocd-cm -n argocd \
  -o jsonpath='{.data.resource\.exclusions}'
```

---

## Troubleshooting

### `nc` 명령이 Kiali 파드 내에서 항상 OK를 반환한다

Kiali 기본 이미지의 `nc`(BusyBox)는 특정 옵션에서 오동작할 수 있다. 반드시 아래 방식을 사용한다:

```bash
kubectl exec -n istio-system "$KIALI_POD" -- \
  bash -c 'timeout 5 bash -c "echo >/dev/tcp/<IP>/<PORT>" && echo OK || echo FAIL'
```

### EndpointSlice patch 후에도 연결이 안 된다

1. NetworkPolicy가 해당 IP를 차단하고 있는지 확인한다 (Procedure 3 참고).
2. 클러스터 DNS가 Service를 제대로 해석하는지 확인한다.

```bash
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  nslookup grafana-external.platform.svc.cluster.local
```

3. Kiali 파드를 재시작하여 캐시를 초기화한다.

```bash
kubectl rollout restart deployment/kiali -n istio-system
```

### ArgoCD App이 OutOfSync로 표시된다

EndpointSlice를 직접 생성/수정하면 ArgoCD는 해당 리소스를 인식하지 못해 OutOfSync를 표시할 수 있다. 이는 resource.exclusions 설정에 의한 정상 동작이다. 필요 시 해당 리소스를 ArgoCD에서 무시 처리한다.

```bash
# App의 ignoreDifferences에 EndpointSlice 추가 (선택적)
argocd app set platform-external-services \
  --ignore-difference-kind EndpointSlice \
  --ignore-difference-group discovery.k8s.io
```

---

## 핵심 교훈 요약

| 항목                  | 내용                                                                        |
| --------------------- | --------------------------------------------------------------------------- |
| ArgoCD EndpointSlice  | ArgoCD는 EndpointSlice를 관리하지 않음. 수동 `kubectl apply` 필수           |
| 연결 테스트           | Kiali 파드에서 `nc` 대신 `bash -c 'echo >/dev/tcp/<ip>/<port>'` 사용        |
| NetworkPolicy         | egress ipBlock 규칙은 post-DNAT 기준 IP로 작성                              |
| IP 변경 시 체크리스트 | EndpointSlice YAML, Kiali Grafana URL, NetworkPolicy egress 세 곳 모두 확인 |
