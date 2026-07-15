---
title: 'GitHub 앱 GitOps 온보딩 가이드'
type: sdlc/guide
status: active
owner: platform
updated: 2026-05-26
---

# GitHub 앱 GitOps 온보딩 가이드

## Overview

이 문서는 GitHub에 소스 코드가 있는 애플리케이션을 `hy-home.k8s` 클러스터에 GitOps 방식으로 온보딩하는 방법을 설명한다.

**현재 플랫폼 패턴** (2026-03 기준):

- **배포**: Argo Rollout (canary 전략) — Deployment 대신 사용
- **분석**: AnalysisTemplate (Prometheus kube-state-metrics 기반)
- **보안**: Istio PeerAuthentication STRICT (apps namespace 전체 적용)
- **TLS**: cert-manager + mkcert-ca-issuer
- **시크릿**: ExternalSecret → Vault (선택 사항)

> **참조 구현**: `gitops/workloads/adminer/` — stable/canary Service와 Istio routing까지 포함한 현재 active reference
> **템플릿**: `examples/sample-app/` — 복사 & 수정용 최소 온보딩 템플릿

## Guide Type

`how-to`

## Target Audience

- 홈 랩 운영자 (Platform Engineer / Solo Developer)
- GitHub 레포에서 빌드한 컨테이너 이미지를 클러스터에 배포하려는 사용자

### Purpose

GitHub 레포에서 빌드한 컨테이너 이미지를 현재 플랫폼의 Rollout, AnalysisTemplate, Istio mTLS, ingress/TLS 패턴에 맞춰 온보딩할 수 있게 한다.

## Prerequisites

### 필수 도구

```bash
kubectl version --client   # v1.28+
argocd version             # ArgoCD CLI
git --version
```

### 클러스터 상태 확인

```bash
# apps-generator ApplicationSet 동작 확인
kubectl -n argocd get applicationset apps-generator

# apps namespace 상태 확인
kubectl get namespace apps --show-labels
# 출력에 istio-injection=enabled 포함 확인

# Argo Rollouts 컨트롤러 동작 확인
kubectl -n argo-rollouts get pods
```

### GitHub 레포 요건

- GitHub Actions로 컨테이너 이미지를 빌드하여 `ghcr.io/<owner>/<appname>:<tag>`로 Push
- ghcr.io 패키지를 **Public**으로 설정 (또는 imagePullSecret 구성)

---

## Step-by-step Instructions

아래 Step 1-6을 순서대로 수행한다. 운영 중 즉시 실행/복구가 필요한 경우에는 관련 런북을 우선한다.

### Step 1: GitHub Actions CI 파이프라인 설정

앱 GitHub 레포에 다음 workflow를 추가한다.

```yaml
# .github/workflows/build-push.yml
name: Build and Push

on:
  push:
    tags: ['v*'] # 태그 push 시 빌드
  workflow_dispatch:

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to GitHub Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix=sha-

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

빌드 완료 후 `ghcr.io/<owner>/<appname>:v1.0.0` 형태의 이미지가 생성된다.

---

### Step 2: GitOps 매니페스트 생성

`examples/sample-app/`을 복사하여 플레이스홀더를 교체한다. 이 경로는 최소 온보딩 시작점이며, stable/canary Service나 Istio routing까지 필요한 경우 `gitops/workloads/adminer/` 패턴과 비교해 보강한다.

```bash
# 1. 예시 복사
cp -r examples/sample-app gitops/workloads/<appname>

# 2. 플레이스홀더 일괄 교체
APP=<appname>
OWNER=<github-owner>
TAG=v1.0.0
PORT=8080

for f in gitops/workloads/${APP}/*.yaml; do
  sed -i \
    "s|<appname>|${APP}|g; \
     s|<owner>|${OWNER}|g; \
     s|<tag>|${TAG}|g; \
     s|<port>|${PORT}|g" \
    "$f"
done
```

### 생성되는 파일 구조

```
gitops/workloads/<appname>/
├── kustomization.yaml        ← Kustomize 진입점
├── rollout.yaml              ← Argo Rollout (canary 20→60→100%)
├── service.yaml              ← Service (http- 포트 명명)
├── ingress.yaml              ← Ingress (nginx TLS)
└── analysis-template.yaml   ← canary 안정성 검사
```

### 파일별 주요 확인 사항

#### rollout.yaml

```yaml
# 이미지 태그를 latest 대신 고정 태그 사용 (재현성 보장)
image: ghcr.io/<owner>/<appname>:v1.0.0

# canary 전략: 20% → AnalysisTemplate 검사 → 30s pause → 60% → 30s pause → 100%
strategy:
  canary:
    steps:
      - setWeight: 20
      - analysis:
          templates:
            - templateName: <appname>-stability
      - pause: { duration: 30s }
      - setWeight: 60
      - pause: { duration: 30s }
      - setWeight: 100
```

#### service.yaml

```yaml
ports:
  - name: http-<appname> # Istio 프로토콜 감지: http- 접두사 필수
    port: 8080
```

#### ingress.yaml

```yaml
annotations:
  cert-manager.io/cluster-issuer: mkcert-ca-issuer # 로컬 TLS 인증서
  nginx.ingress.kubernetes.io/ssl-redirect: 'true'
spec:
  ingressClassName: nginx
  rules:
    - host: <appname>.127.0.0.1.nip.io
```

---

### Step 3: Traefik 설정 추가 (hy-home.docker 레포)

외부 Traefik이 `127.0.0.1:443`에 바인딩되므로, 새 앱마다 Traefik router 규칙이 필요하다.

```bash
# hy-home.docker 레포에 Traefik 설정 추가
cp examples/sample-app/traefik-k3d.yaml.example \
  /path/to/hy-home.docker/infra/01-gateway/traefik/dynamic/<appname>-k3d.yaml

# 플레이스홀더 교체
sed -i "s|<appname>|${APP}|g" \
  /path/to/hy-home.docker/infra/01-gateway/traefik/dynamic/<appname>-k3d.yaml
```

Traefik은 dynamic config 디렉토리를 watch하므로 **재시작 없이 자동 반영**된다.

---

### Step 4: (선택) Vault 시크릿 연동

앱이 DB 비밀번호, API 키 등 시크릿을 필요로 하는 경우 Vault ESO 연동을 추가한다.

현재 `infrastructure/vault/policies/eso-read.hcl`은 검증된 여섯 개 플랫폼
경로만 허용하며 wildcard 앱 경로를 허용하지 않는다. 따라서 새 앱의 Vault
경로, 정책, credential을 이 가이드의 명령으로 생성하거나 기존 HCL에
인라인으로 추가하지 않는다. 별도 승인된 보안 변경에서 외부 Vault 운영자가
HTTPS와 검증된 CA를 사용해 경로/정책을 준비하고, Kubernetes auth role에
`bound_audiences=vault`를 설정한 뒤 아래 GitOps 변경을 진행한다.
기존 샘플의 논리 경로 식별자 `secret/apps/<appname>/config`와
ExternalSecret key `apps/<appname>/config`는 별도 승인 전 실행 가능한
프로비저닝 명령이 아니다.

`vault-backend`가 사용하는 클러스터 내부 HTTP는 현재 로컬 k3d 전용
예외이며 production TLS 구성을 의미하지 않는다. 외부 Vault 작업에는
비대화형, credential argv, 인증서 검증 생략 fallback을 사용하지 않는다.

### 4-1. ExternalSecret 활성화

`kustomization.yaml`에서 `external-secret.yaml` 주석을 해제한다:

```yaml
resources:
  - rollout.yaml
  - service.yaml
  - ingress.yaml
  - analysis-template.yaml
  - external-secret.yaml # 주석 해제
```

`vault-backend` ClusterSecretStore는 Vault mount path를 `secret`으로 고정하므로
ExternalSecret의 `remoteRef.key`는 승인된 외부 Vault 경로에서 mount prefix를
제외한 값을 사용한다.

`rollout.yaml` container spec에 시크릿 참조를 추가한다:

```yaml
envFrom:
  - secretRef:
      name: <appname>-secret
```

---

### Step 5: 커밋 & 푸시

```bash
git add gitops/workloads/<appname>/
git commit -m "feat: add <appname> to GitOps"
git push origin feat/<appname>-gitops
```

ArgoCD `apps-generator` ApplicationSet이 `gitops/workloads/*`를 자동 스캔하여
PR review 후 `main`에 merge되면 3분 이내(또는 webhook 설정 시 즉시) `<appname>` Application을 생성하고 배포한다.

---

### Step 6: 배포 확인

```bash
# ArgoCD Application 상태 확인
argocd app list | grep <appname>
argocd app get <appname>

# Rollout 상태 확인
kubectl argo rollouts status <appname> -n apps
kubectl argo rollouts get rollout <appname> -n apps --watch

# Pod 상태 확인 (sidecar 포함 2/2 Running 확인)
kubectl get pods -n apps -l app.kubernetes.io/name=<appname>

# Ingress 확인
kubectl get ingress -n apps <appname>
```

### 정상 상태

```
ArgoCD Application: Synced / Healthy
Rollout: Healthy (Stable)
Pod: 2/2 Running    ← adminer(app) + istio-proxy(sidecar)
Ingress: ADDRESS 가 LoadBalancer IP로 설정
```

### 브라우저 접속

```
https://<appname>.127.0.0.1.nip.io
```

---

### Istio mTLS 확인 (apps namespace)

`apps` namespace에 PeerAuthentication STRICT가 적용되어 있으므로,
모든 pod-to-pod 통신은 mTLS로 암호화된다.

```bash
# PeerAuthentication 상태 확인
kubectl get peerauthentication -n apps

# Kiali에서 확인: https://kiali.127.0.0.1.nip.io
# Graph > apps namespace > 서비스 간 Lock 아이콘으로 mTLS 확인
```

---

### AnalysisTemplate 동작 확인

canary 배포 중 AnalysisTemplate이 실행된다.

```bash
# AnalysisRun 상태 확인 (canary 중 자동 생성)
kubectl get analysisrun -n apps
kubectl describe analysisrun -n apps <analysisrun-name>

# 실패 시 자동 rollback 확인
kubectl argo rollouts get rollout <appname> -n apps
# STATUS: Degraded → Rollout이 이전 버전으로 복귀
```

---

### 이미지 업데이트 (배포 갱신)

새 버전 배포 시 `rollout.yaml`의 이미지 태그를 업데이트한다.

```bash
# 방법 1: 파일 직접 수정 후 커밋
sed -i "s|<appname>:v1.0.0|<appname>:v1.1.0|" gitops/workloads/<appname>/rollout.yaml
git add gitops/workloads/<appname>/rollout.yaml
git commit -m "chore: bump <appname> to v1.1.0"
# feature branch로 push한 뒤 PR review/merge를 거친다
git push origin chore/<appname>-v1.1.0

# 방법 2: operator-triggered break-glass only
kubectl argo rollouts set image <appname> \
  <appname>=ghcr.io/<owner>/<appname>:v1.1.0 -n apps
```

---

## Common Pitfalls

### ghcr.io 이미지 Pull 실패 (ImagePullBackOff)

- GitHub 패키지 가시성을 **Public**으로 설정 확인
- Private 레지스트리라면 imagePullSecret 추가 필요

### Rollout이 canary에서 멈추는 경우

```bash
# AnalysisRun 실패 확인
kubectl get analysisrun -n apps
kubectl describe analysisrun -n apps <name>

# Prometheus 접근 가능 여부 확인
kubectl exec -n argo-rollouts deploy/argo-rollouts -- \
  wget -qO- http://prometheus-external.platform.svc.cluster.local:9090/-/healthy
```

### Istio sidecar 미주입 (1/1 Running)

```bash
# namespace 라벨 확인
kubectl get namespace apps --show-labels
# istio-injection=enabled 없으면:
kubectl label namespace apps istio-injection=enabled
```

### cert-manager TLS 인증서 미발급

```bash
kubectl get certificate -n apps
kubectl describe certificate <appname>-tls -n apps
# ClusterIssuer 상태 확인
kubectl get clusterissuer mkcert-ca-issuer
```

---

## Traceability

- **템플릿**: [`../../../examples/sample-app`](../../../examples/sample-app)
- **참조 구현**: [`../../../gitops/workloads/adminer`](../../../gitops/workloads/adminer)
- **Runbook**: [`../runbooks/0010-github-app-gitops-onboarding-runbook.md`](../runbooks/0010-github-app-gitops-onboarding-runbook.md)
- **Operations 정책**: [`../policies/0007-app-gitops-onboarding-policy.md`](../policies/0007-app-gitops-onboarding-policy.md)
- **AppProject**: [`../../../gitops/clusters/local/appproject-apps.yaml`](../../../gitops/clusters/local/appproject-apps.yaml)
- **ApplicationSet**: [`../../../gitops/clusters/local/applicationset-apps.yaml`](../../../gitops/clusters/local/applicationset-apps.yaml)

### Lifecycle Traceability

| Promoted owner | Audience outcome | Operating surface |
| --- | --- | --- |
| N/A — app onboarding is promoted from the current policy and runbook plus the sample/adminer implementations, with no eligible upstream document carrying a reciprocal guide link | Home-lab operators can onboard a GitHub-hosted image through reviewed GitOps changes with Rollout analysis, mTLS, TLS ingress, and bounded optional Vault/ESO integration. | `examples/sample-app`, `gitops/workloads/<appname>`, apps ApplicationSet/AppProject, external Traefik routing, and Argo Rollouts |
