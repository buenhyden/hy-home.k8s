---
title: 'GitHub 앱 GitOps 온보딩 런북'
type: sdlc/runbook
status: active
owner: platform
updated: 2026-05-26
---

# GitHub 앱 GitOps 온보딩 런북

## Runbook Type

`onboarding`

## Overview

이 런북은 GitHub 레포 기반 애플리케이션을 `hy-home.k8s` 클러스터에 GitOps 방식으로 온보딩하는
단계별 운영 절차를 제공한다. `examples/sample-app/`은 최소 온보딩 템플릿이고,
`gitops/workloads/adminer/`는 stable/canary Service와 Istio routing까지 포함한 현재 active reference다.

## Purpose

신규 GitHub 앱을 `gitops/workloads/`에 추가하고 PR review 이후 ArgoCD reconciliation으로 배포/검증/rollback할 수 있게 한다.

## Canonical References

- [`../guides/0008-github-app-gitops-onboarding-guide.md`](../guides/0008-github-app-gitops-onboarding-guide.md)
- [`../policies/0007-app-gitops-onboarding-policy.md`](../policies/0007-app-gitops-onboarding-policy.md)
- [`../../../gitops/workloads/adminer`](../../../gitops/workloads/adminer) — fuller active reference pattern
- [`../../../examples/sample-app`](../../../examples/sample-app) — minimal onboarding template

## When to Use

- GitHub Container Registry(ghcr.io) 이미지를 클러스터에 처음 배포할 때
- `gitops/workloads/`에 신규 workload 디렉토리를 추가할 때
- canary 배포 실패 후 rollback 및 재배포가 필요할 때
- Vault 시크릿 연동 초기 설정이 필요할 때

---

## 사전 점검

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

# Prometheus 접근 확인 (AnalysisTemplate 전제)
kubectl exec -n argo-rollouts deploy/argo-rollouts -- \
  wget -qO- http://prometheus-external.platform.svc.cluster.local:9090/-/healthy
# 출력: Prometheus is Healthy.
```

---

## Procedure or Checklist

아래 Procedure 1-5를 순서대로 수행한다. 배포 변경은 feature branch와 PR review를 거쳐 GitOps reconciliation으로 반영한다.

## Procedure 1: GitOps 매니페스트 생성 및 배포

### 1-1. 예시 복사 및 플레이스홀더 교체

```bash
# 변수 설정
APP=<appname>          # 예: my-api
OWNER=<github-owner>   # 예: buenhyden
TAG=<tag>              # 예: v1.0.0
PORT=<port>            # 예: 8080

# 예시 복사
cp -r examples/sample-app gitops/workloads/${APP}

# 플레이스홀더 일괄 교체
for f in gitops/workloads/${APP}/*.yaml; do
  sed -i \
    "s|<appname>|${APP}|g; \
     s|<owner>|${OWNER}|g; \
     s|<tag>|${TAG}|g; \
     s|<port>|${PORT}|g" \
    "$f"
done

# 결과 확인
cat gitops/workloads/${APP}/rollout.yaml | grep image
```

### 1-2. Traefik 설정 추가 (hy-home.docker 레포)

```bash
# traefik-k3d.yaml.example은 hy-home.docker 레포에 추가
DOCKER_REPO=/path/to/hy-home.docker

cp examples/sample-app/traefik-k3d.yaml.example \
  ${DOCKER_REPO}/infra/01-gateway/traefik/dynamic/${APP}-k3d.yaml

sed -i "s|<appname>|${APP}|g" \
  ${DOCKER_REPO}/infra/01-gateway/traefik/dynamic/${APP}-k3d.yaml

# hy-home.docker 레포 커밋
cd ${DOCKER_REPO}
git add infra/01-gateway/traefik/dynamic/${APP}-k3d.yaml
git commit -m "feat: add traefik router for ${APP}"
# feature branch로 push한 뒤 PR review/merge를 거친다
git push origin feat/${APP}-traefik
cd -
```

### 1-3. GitOps 커밋 & 푸시

```bash
git add gitops/workloads/${APP}/
git commit -m "feat: add ${APP} to GitOps"
# feature branch로 push한 뒤 PR review/merge를 거친다
git push origin feat/${APP}-gitops
```

### 1-4. ArgoCD Application 생성 확인

```bash
# apps-generator가 새 Application을 생성하는지 확인 (최대 3분)
watch argocd app list | grep ${APP}

# operator-triggered reconciliation only
argocd app sync argocd/apps-generator
```

---

## Verification Steps

Procedure 2의 명령으로 Rollout, Pod, AnalysisRun, Ingress, HTTPS 접근 상태를 확인한다.

## Procedure 2: 배포 상태 검증

```bash
# Rollout 진행 상황 실시간 확인
kubectl argo rollouts get rollout ${APP} -n apps --watch

# Pod 상태 확인 (2/2 Running = app + istio-proxy)
kubectl get pods -n apps -l app.kubernetes.io/name=${APP}

# AnalysisRun 확인 (canary 단계에서 자동 생성)
kubectl get analysisrun -n apps

# Ingress 확인
kubectl get ingress -n apps ${APP}
```

### 기대 상태

| 항목        | 기대값                               |
| ----------- | ------------------------------------ |
| Rollout     | `Healthy` / `Stable`                 |
| Pod         | `2/2 Running`                        |
| ArgoCD      | `Synced` / `Healthy`                 |
| AnalysisRun | `Successful`                         |
| Ingress     | HOSTS에 `<appname>.127.0.0.1.nip.io` |

```bash
# 브라우저 접속 확인
curl -sk https://${APP}.127.0.0.1.nip.io | head -5
```

---

## Procedure 3: canary 배포 업데이트 (이미지 버전 갱신)

```bash
NEW_TAG=v1.1.0

# rollout.yaml 태그 업데이트
sed -i "s|ghcr.io/${OWNER}/${APP}:.*|ghcr.io/${OWNER}/${APP}:${NEW_TAG}|" \
  gitops/workloads/${APP}/rollout.yaml

git add gitops/workloads/${APP}/rollout.yaml
git commit -m "chore: bump ${APP} to ${NEW_TAG}"
# feature branch로 push한 뒤 PR review/merge를 거친다
git push origin chore/${APP}-${NEW_TAG}

# canary 진행 상황 확인
kubectl argo rollouts get rollout ${APP} -n apps --watch
```

---

## Procedure 4: canary 실패 → rollback

AnalysisTemplate 실패 또는 수동 abort 시 이전 버전으로 자동 rollback된다.

```bash
# 수동 abort (즉시 rollback)
kubectl argo rollouts abort ${APP} -n apps

# rollback 확인
kubectl argo rollouts get rollout ${APP} -n apps
# STATUS: Degraded → 이전 stable 버전으로 복귀

# 안정화 후 rollout 재개 (수정된 이미지로 재배포 필요)
# rollout.yaml 이미지 수정 후 커밋 & 푸시
```

---

## Safe Rollback or Recovery Procedure

Procedure 4의 abort/rollback 절차를 우선 사용한다. GitOps manifest 수정이 필요한 경우 이미지 태그 또는 설정을 수정한 뒤 feature branch PR flow로 재배포한다.

## Procedure 5: Vault 시크릿 연동 추가

```bash
# 1. Vault에 시크릿 등록
export VAULT_ADDR=http://172.18.0.8:8200
vault login
# external secret operation; human-approved only
vault kv put secret/apps/${APP}/config \
  db_password="changeme" api_key="changeme" # pragma: allowlist secret

# 2. Vault 정책 갱신
cat >> infrastructure/vault/policies/eso-read.hcl << EOF

path "secret/data/apps/${APP}/*" {
  capabilities = ["read"]
}
EOF
# external secret operation; human-approved policy change only
vault policy write eso-read infrastructure/vault/policies/eso-read.hcl

# 3. kustomization.yaml에서 external-secret.yaml 주석 해제 후 커밋
# (rollout.yaml에 envFrom 추가도 필요)
#    ExternalSecret remoteRef.key는 apps/${APP}/config 형식이다.
#    Vault CLI 경로 secret/apps/${APP}/config에서 mount prefix secret/은 제외한다.

# 4. ExternalSecret 동기화 확인
kubectl get externalsecret -n apps ${APP}-secret
# 출력: READY=True, STATUS=SecretSynced
```

---

## Troubleshooting

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

# Prometheus 연결 확인
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl -s http://prometheus-external.platform.svc.cluster.local:9090/api/v1/query \
  --data-urlencode 'query=up'
```

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

## Observability and Evidence Sources

- **Signals**: ArgoCD Application health/sync, Rollout status, AnalysisRun result, Pod readiness, Ingress certificate status
- **Evidence to Capture**: PR diff, ArgoCD app status, rollout history, relevant events/log snippets, HTTPS verification output

## Agent Operations (If Applicable)

- **Prompt Rollback**: 최근 agent-generated manifest 변경을 PR diff 기준으로 되돌린다.
- **Model Fallback**: 검증 실패 시 sample-app/adminer 패턴에 맞춘 최소 변경만 유지한다.
- **Tool Disable / Revoke**: 실패 중 live cluster mutation 또는 secret write 자동화를 중지한다.
- **Eval Re-run**: GitOps structure, manifest validation, secret handling gate를 재실행한다.
- **Trace Capture**: 온보딩 task 또는 PR에 검증 명령과 결과를 남긴다.

## Related Documents

- **Guide**: [`../guides/0008-github-app-gitops-onboarding-guide.md`](../guides/0008-github-app-gitops-onboarding-guide.md)
- **Operations 정책**: [`../policies/0007-app-gitops-onboarding-policy.md`](../policies/0007-app-gitops-onboarding-policy.md)
- **ESO/Vault Recovery**: [`./0002-argocd-eso-vault-recovery-runbook.md`](./0002-argocd-eso-vault-recovery-runbook.md)
- **예시 템플릿**: [`../../../examples/sample-app`](../../../examples/sample-app)
