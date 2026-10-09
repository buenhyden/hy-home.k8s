---
title: "GitHub 앱 GitOps 온보딩 런북"
version: "1.2.0"
type: "operation/runbook"
status: "active"
owner: "platform"
updated: "2026-10-09"
layer: "operations"
artifact_id: "RUN-0010"
---

# GitHub 앱 GitOps 온보딩 런북

## Purpose

이 런북은 GitHub 레포 기반 애플리케이션을 `hy-home.k8s` 클러스터에 GitOps 방식으로 온보딩하는
단계별 운영 절차를 제공한다. `examples/sample-app/`은 최소 온보딩 템플릿이고,
`gitops/workloads/adminer/`는 stable/canary Service와 Istio routing까지 포함한 현재 active reference다.

## Trigger and Preconditions

- GitHub Container Registry(ghcr.io) 이미지를 클러스터에 처음 배포할 때
- `gitops/workloads/`에 신규 workload 디렉토리를 추가할 때
- canary 배포 실패 후 rollback 및 재배포가 필요할 때
- Vault 시크릿 연동 초기 설정이 필요할 때

---

### 사전 점검

```bash
# apps-generator ApplicationSet 동작 확인
kubectl -n argocd get applicationset apps-generator

# apps namespace 라벨 확인 (istio-injection 포함)
kubectl get namespace apps --show-labels

# PeerAuthentication STRICT 확인
kubectl get peerauthentication -n apps default

# Argo Rollouts 컨트롤러 확인
kubectl -n argo-rollouts get pods | grep argo-rollouts
# 출력: argo-rollouts-<hash>   1/1   Running

# Prometheus API 접근 전제 (AnalysisTemplate, ADR-0046)
# controller는 https://prometheus.hy.home.arpa를 Basic Auth header로 호출한다.
kubectl -n apps get externalsecret prometheus-api-auth
kubectl -n argo-rollouts get configmap hy-home-root-ca
```

Prometheus 수집 상태가 필요하면 외부 observability 운영자에게
[RUN-0009](./0009-k8s-observability-runbook.md)의 승인된 인증 조회 경로에서
`up{cluster="k3d-hyhome"}` 결과를 요청한다. 이 저장소의 절차는 인증정보
파일이나 임의의 조회 helper를 읽지 않는다. 조회가 미실행이면 그 사실을
남기고 AnalysisRun 결과를 성공으로 추정하지 않는다.

---

## Procedure

아래 Procedure 1-5를 순서대로 수행한다. 배포 변경은 feature branch와 PR review를 거쳐 GitOps reconciliation으로 반영한다.

### Procedure 1: GitOps 매니페스트 생성 및 배포

### 1-1. 예시 복사 및 플레이스홀더 교체

```bash
# 실제 대상에 맞게 값을 검토한 뒤 교체한다. 이 네 줄은 유효한 예시다.
APP=my-api
OWNER=buenhyden
TAG=v1.0.0
PORT=8080

# 경로·이미지·치환 입력은 제한된 값만 받는다.
[[ "$APP" =~ ^[a-z0-9]([a-z0-9-]*[a-z0-9])?$ ]] &&
  (( ${#APP} <= 63 )) || exit 2
[[ "$OWNER" =~ ^[A-Za-z0-9]([A-Za-z0-9-]*[A-Za-z0-9])?$ ]] || exit 2
[[ "$TAG" =~ ^[A-Za-z0-9_][A-Za-z0-9_.-]*$ ]] &&
  (( ${#TAG} <= 128 )) || exit 2
[[ "$PORT" =~ ^[1-9][0-9]{0,4}$ ]] && (( PORT <= 65535 )) || exit 2

# 예시 manifest만 복사 (README는 ApplicationSet 감지 경로에 두지 않는다)
git switch -c "feat/${APP}-gitops"
mkdir -p "gitops/workloads/${APP}"
cp examples/sample-app/*.yaml "gitops/workloads/${APP}/"

# 플레이스홀더 일괄 교체
for f in "gitops/workloads/${APP}/"*.yaml; do
  sed -i \
    "s|<appname>|${APP}|g; \
     s|<owner>|${OWNER}|g; \
     s|<tag>|${TAG}|g; \
     s|<port>|${PORT}|g" \
    "$f"
done

# 결과 확인
rg 'image:' "gitops/workloads/${APP}/rollout.yaml"
```

현재 최소 예시의 Ingress backend는 `8080`으로 고정돼 있다. 다른 `PORT`를
선택하면 치환 대상뿐 아니라 `ingress.yaml`의 backend port와 Service,
Rollout의 모든 port·probe를 함께 검토·수정하고 정적 검사를 통과해야 한다.
예시 파일을 복사했다는 사실만으로 임의 port 지원이나 배포 성공을
판정하지 않는다.

### 1-2. 접속 이름 확인

앱은 k8s 전용 router가 받는 `${APP}.hy-k8s.home.arpa`로 노출되므로 외부
저장소 변경이 없다. 이름 해석(`/etc/hosts` 또는 DNS)이 `192.168.0.14`를 가리키는지
operator가 확인한다. `hy-k8s.home.arpa/${APP}` 진입이 필요하면
`gitops/platform/ingress-routes/apex-redirects.yaml`에 redirect Ingress를 추가한다.

### 1-3. GitOps 커밋 & 푸시

`apps-generator`는 `main`의 `gitops/workloads/*`를 읽고 생성한 Application에
`automated.prune: true`, `selfHeal: true`를 적용한다. 따라서 PR을 `main`에
merge하면 수동 `argocd app sync`를 기다리지 않고 배포·삭제·복구가 시작될
수 있다. 원격 push와 별도로, 운영자는 **merge 전에** 대상 앱·이미지·
리소스 변경 범위, 자동 prune 영향과 복구 경로를 검토하고 배포 권한을
확인한다. merge 후의 수동 승인 단계로 배포를 보류할 수 없다.

```bash
git add "gitops/workloads/${APP}/"
git commit -m "feat: add ${APP} to GitOps"
# 검토된 commit·원격 저장소·branch 대상과 별도 push 승인을 운영자가 확인한 경우에만
git push origin "feat/${APP}-gitops"
```

PR 검토·승인된 merge와 실제 `main` 반영 뒤 자동 reconciliation의 결과를
읽는다. 로컬 commit이나 push만으로 Application이 생성되었다고 판정하지
않는다.

### 1-4. ArgoCD Application 생성 확인

```bash
# apps-generator가 path.basename 이름의 새 Application을 생성했는지 확인
kubectl -n argocd get application "$APP"

# apps-generator는 ApplicationSet이므로 app sync 대상이 아니다.
kubectl -n argocd describe applicationset apps-generator
```

자동 동기화가 실패하거나 멈춘 **이미 생성된** Application을 운영자가 별도
승인 범위에서 수동 재조정할 때만 다음 명령을 사용한다. 생성 전 기본 배포
단계로 실행하지 않는다.

```bash
# operator-approved manual reconciliation only
argocd app sync "$APP"
```

---

### Procedure 2: 배포 상태 검증

```bash
# Rollout 진행 상황 실시간 확인
kubectl argo rollouts get rollout ${APP} -n apps --watch

# 대상 workload manifest의 컨테이너와 기대 Istio sidecar에 맞는 ready/desired 확인
kubectl get pods -n apps -l app.kubernetes.io/name=${APP}

# AnalysisRun 확인 (canary 단계에서 자동 생성)
kubectl get analysisrun -n apps

# Ingress 확인
kubectl get ingress -n apps ${APP}
```

```bash
# 신뢰된 로컬 CA로 TLS와 HTTP 성공을 함께 확인한다.
curl --fail --silent --show-error --cacert secrets/certs/rootCA.pem \
  -o /dev/null -w '%{http_code}' "https://${APP}.hy-k8s.home.arpa/"
```

---

### Procedure 3: canary 배포 업데이트 (이미지 버전 갱신)

이 이미지 변경도 `main` merge 직후 자동으로 canary가 시작될 수 있다.
운영자는 merge 전에 이미지·분석·롤백 범위와 배포 권한을 확인한다.

```bash
NEW_TAG=v1.1.0
[[ "$NEW_TAG" =~ ^[A-Za-z0-9_][A-Za-z0-9_.-]*$ ]] || exit 2
git switch -c "chore/${APP}-${NEW_TAG}"

# rollout.yaml 태그 업데이트
sed -i "s|ghcr.io/${OWNER}/${APP}:.*|ghcr.io/${OWNER}/${APP}:${NEW_TAG}|" \
  "gitops/workloads/${APP}/rollout.yaml"

git add "gitops/workloads/${APP}/rollout.yaml"
git commit -m "chore: bump ${APP} to ${NEW_TAG}"
# 검토된 commit·원격 저장소·branch 대상과 별도 push 승인을 운영자가 확인한 경우에만
git push origin "chore/${APP}-${NEW_TAG}"

# merge 전 자동 배포 영향을 검토·승인하고, merge 후 자동 reconciliation 결과 확인
kubectl argo rollouts get rollout ${APP} -n apps --watch
```

---

### Procedure 4: 실패 시 복구 경로로 전환

AnalysisTemplate 실패나 수동 중단이 필요하면 이후 배포를 멈추고
[Recovery and Escalation](#recovery-and-escalation)의 승인된 canary 복구
절차로 전환한다. 이전 stable 버전 복귀와 원인 수정을 확인한 뒤에만
다음 온보딩 단계를 진행한다.

---

### Procedure 5: Vault 시크릿 연동 추가

애플리케이션 시크릿이 필요하면 승인된 Vault operator가 저장소 transcript
밖의 비밀 채널에서 `secret/apps/${APP}/config`를 생성한다. 이 Runbook은
값, login, Vault write 또는 policy write 명령을 기록하지 않는다.

Git 변경에서 `external-secret.yaml`을 활성화하고 Rollout의 `envFrom`을
연결한다. Vault 경로와 `remoteRef.key` 규칙은
[POL-0007](../policies/0007-app-gitops-onboarding-policy.md)의 3-3 시크릿 관리
표가 소유한다. 승인된 operator가 Vault policy를 별도 절차로 갱신한 뒤 다음
read-only 상태만 확인한다.

```bash
kubectl get externalsecret -n apps ${APP}-secret
```

성공 기준은 `READY=True`, `STATUS=SecretSynced`이며 secret value는 출력하지
않는다.

---

## Verification

Procedure 2의 Rollout, Pod, AnalysisRun, Ingress와 CA 검증을 거친 HTTPS 결과가
아래 기대 상태를 만족하는지 확인한다. CA 파일을 사용할 수 없으면 TLS 완료
판정은 보류하고 인증서 owner에게 넘긴다. 이 서술은 live 검증 결과가 아니다.

| 항목        | 기대값                               |
| ----------- | ------------------------------------ |
| Rollout     | `Healthy` / `Stable`                 |
| Pod         | 선택한 workload의 앱 컨테이너와 기대 sidecar를 포함한 실제 ready/desired 수 일치 |
| ArgoCD      | `Synced` / `Healthy`                 |
| AnalysisRun | `Successful`                         |
| Ingress     | HOSTS에 `<appname>.hy-k8s.home.arpa` |
| HTTPS       | 신뢰된 CA 검증과 성공 응답           |

- **Signals**: ArgoCD Application health/sync, Rollout status, AnalysisRun result, Pod readiness, Ingress certificate status
- **Evidence to Capture**: PR diff, ArgoCD app status, rollout history, relevant events/log snippets, HTTPS verification output

## Recovery and Escalation

### Canary abort and rollback

AnalysisTemplate 실패나 수동 abort가 필요한 경우 승인된 운영자가 다음
명령으로 workload 범위를 한정해 중단한다. 이전 stable 버전으로의 복귀를
확인한 뒤 원인을 수정하고 feature branch PR flow로 재배포한다.

```bash
# operator-approved live abort only
kubectl argo rollouts abort ${APP} -n apps

# rollback 확인: 이전 stable 버전으로 복귀했는지 상태를 읽는다.
kubectl argo rollouts get rollout ${APP} -n apps
```

GitOps manifest 수정이 필요하면 이미지 태그 또는 설정을 수정한다.
수정 PR의 merge 전 자동 배포·prune 영향을 재평가하고 승인받는다. merge
뒤에는 자동 reconciliation 결과를 확인하며, 수동 sync가 별도로 필요한
경우에만 위의 승인된 재조정 경계를 따른다.

### ArgoCD Application이 생성되지 않는 경우

```bash
# apps-generator 이벤트 확인
kubectl -n argocd describe applicationset apps-generator

# kustomization.yaml이 유효한지 확인
kubectl kustomize gitops/workloads/${APP}/
```

### Pod가 1/1 Running (Istio sidecar 미주입)

```bash
# namespace 라벨 확인
kubectl get namespace apps --show-labels | grep istio-injection

# 라벨 누락 시 (이미 있어야 함, 이상 시 platform sync 확인)
# operator-triggered reconciliation only
argocd app sync platform-namespaces
```

### AnalysisRun 실패 (Prometheus 쿼리 오류)

```bash
# AnalysisRun 상세 확인
kubectl describe analysisrun -n apps $(kubectl get analysisrun -n apps -o name | head -1)

# AnalysisRun 오류가 401이면 apps/prometheus-api-auth, x509면 hy-home-root-ca 확인
```

외부 Prometheus의 `kube_pod_container_status_restarts_total{namespace="apps"}`
쿼리 결과가 필요하면 [RUN-0009](./0009-k8s-observability-runbook.md)의 승인된
인증 조회 경로로 요청한다. 인증정보나 원시 비밀 출력은 해당 운영 Task나
사건 기록에 복사하지 않는다.

### TLS 인증서 미발급

```bash
# Certificate 상태 확인
kubectl get certificate -n apps
kubectl describe certificate ${APP}-tls -n apps

# ClusterIssuer 확인
kubectl get clusterissuer mkcert-ca-issuer -o jsonpath='{.status.conditions[0]}'
```

### Rollout OutOfSync (AppProject 권한 오류)

```bash
# AppProject whitelist 확인
kubectl -n argocd get appproject apps -o yaml | grep -A2 "namespaceResourceWhitelist"

# human-approved AppProject bootstrap/break-glass only
kubectl apply -f gitops/clusters/local/appproject-apps.yaml
```

---

## Related Documents

- **Operations 정책**: [`../policies/0007-app-gitops-onboarding-policy.md`](../policies/0007-app-gitops-onboarding-policy.md)
- **ESO/Vault Recovery**: [`./0002-argocd-eso-vault-recovery-runbook.md`](./0002-argocd-eso-vault-recovery-runbook.md)
- **예시 템플릿**: [`../../../examples/sample-app`](../../../examples/sample-app)
- [`../../../gitops/workloads/adminer`](../../../gitops/workloads/adminer) — fuller active reference pattern

### Lifecycle Traceability

| Promoted owner | Trigger or control | Evidence or recovery owner |
| --- | --- | --- |
| [App GitOps Onboarding Policy](../policies/0007-app-gitops-onboarding-policy.md) | A new GitHub image must enter `gitops/workloads`, or a canary/analysis/ingress/secret integration needs bounded rollback and re-verification. | Application owner supplies image and PR evidence; Platform operator records ArgoCD, Rollout, AnalysisRun, Pod, and ingress/TLS results and owns GitOps rollback, while secret writes remain human-approved. |
