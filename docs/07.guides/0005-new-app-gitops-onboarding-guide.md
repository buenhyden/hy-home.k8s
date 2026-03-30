# New App GitOps Onboarding Guide

## Overview (KR)

이 문서는 `hy-home.k8s` 클러스터에 새로운 사용자 애플리케이션을 GitOps 방식으로 온보딩하는 방법을 설명한다.
ArgoCD `apps` AppProject와 `apps-generator` ApplicationSet을 활용하여,
앱 소스 레포에 GitOps 디렉토리를 추가하거나 이 레포의 `gitops/workloads/` 아래에 workload를 등록하면
ArgoCD가 자동으로 감지하여 클러스터에 배포한다.
필요에 따라 Vault 시크릿 연동(ESO)과 NetworkPolicy 제한도 추가할 수 있다.

## Guide Type

`how-to`

## Target Audience

- 홈 랩 운영자 (Platform Engineer / Solo Developer)
- 새로운 서비스를 k3d 클러스터에 배포하려는 사용자

## Purpose

새로운 애플리케이션을 ArgoCD GitOps 흐름에 등록하고,
Vault 시크릿 연동 및 네트워크 정책 설정까지 포함한 전체 온보딩 절차를 재현 가능하게 수행한다.

## Prerequisites

### 필수 도구

```bash
kubectl version --client   # v1.28 이상 권장
argocd version             # ArgoCD CLI
vault version              # HashiCorp Vault CLI
git --version
```

### 클러스터 상태 확인

```bash
# ArgoCD 정상 동작 확인
kubectl -n argocd get pods | grep -v Completed

# apps AppProject 확인
argocd proj get apps

# apps-generator ApplicationSet 확인
kubectl -n argocd get applicationset apps-generator
```

### 사전 조건 요약

- `hy-home.k8s` k3d 클러스터가 정상 동작 중이어야 한다.
- ArgoCD가 `gitops/workloads/` 경로를 자동 감지하는 `apps-generator` ApplicationSet이 동작 중이어야 한다.
- 외부 앱 레포를 사용하는 경우: `apps` AppProject의 `sourceRepos`에 해당 레포 URL이 허용되어야 한다.
  현재 `sourceRepos`는 `https://github.com/buenhyden/hy-home.k8s.git` 단일 레포만 허용한다.
  외부 레포를 추가하려면 `gitops/clusters/local/appproject-apps.yaml`을 수정해야 한다.
- Vault가 접근 가능한 상태여야 한다 (`VAULT_ADDR`, `VAULT_TOKEN` 환경 변수 설정).

## Step-by-step Instructions

### Step 1: `gitops/workloads/` 에 앱 디렉토리 추가

`apps-generator` ApplicationSet은 `gitops/workloads/*` 경로를 자동 스캔한다.
이 레포에 workload 디렉토리를 추가하는 것이 가장 간단한 방법이다.

```
gitops/workloads/
└── <appname>/
    ├── kustomization.yaml
    ├── deployment.yaml
    └── service.yaml
```

#### 1-1. 디렉토리 생성

```bash
mkdir -p gitops/workloads/<appname>
```

#### 1-2. `kustomization.yaml` 작성

```yaml
# gitops/workloads/<appname>/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
```

#### 1-3. `deployment.yaml` 작성 (예시)

```yaml
# gitops/workloads/<appname>/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: <appname>
  namespace: apps
spec:
  replicas: 1
  selector:
    matchLabels:
      app: <appname>
  template:
    metadata:
      labels:
        app: <appname>
    spec:
      containers:
        - name: <appname>
          image: ghcr.io/buenhyden/<appname>:latest
          ports:
            - containerPort: 8080
```

#### 1-4. `service.yaml` 작성 (예시)

```yaml
# gitops/workloads/<appname>/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: <appname>
  namespace: apps
spec:
  selector:
    app: <appname>
  ports:
    - port: 80
      targetPort: 8080
```

> **참고**: `apps-generator` ApplicationSet이 자동으로 이 디렉토리를 감지하여 ArgoCD Application을 생성한다.
> destination namespace는 `apps`로 고정되어 있다. 별도 namespace가 필요하면 Step 3을 참고한다.

---

### Step 2: (선택) 외부 레포 앱의 경우 Application CR 수동 등록

외부 GitHub 레포(`https://github.com/buenhyden/<appname>.git`)의 앱을 등록하는 경우,
`apps-generator`가 감지할 수 없으므로 Application CR을 직접 `gitops/apps/root/`에 추가한다.

> **주의**: 현재 `appproject-apps.yaml`의 `sourceRepos`는 이 레포(`hy-home.k8s.git`)만 허용한다.
> 외부 레포를 추가하기 전에 `gitops/clusters/local/appproject-apps.yaml`의 `sourceRepos`를 먼저 수정한다.

#### 2-1. `appproject-apps.yaml` `sourceRepos` 수정 (필요 시)

```yaml
# gitops/clusters/local/appproject-apps.yaml
spec:
  sourceRepos:
    - https://github.com/buenhyden/hy-home.k8s.git
    - https://github.com/buenhyden/<appname>.git # 추가
```

#### 2-2. Application CR 작성

```yaml
# gitops/apps/root/<appname>-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: <appname>
  namespace: argocd
spec:
  project: apps
  source:
    repoURL: https://github.com/buenhyden/<appname>.git
    path: gitops/deploy
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: apps
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
    retry:
      limit: 3
      backoff:
        duration: 10s
        factor: 2
        maxDuration: 3m
```

#### 2-3. `gitops/apps/root/kustomization.yaml` 업데이트

```yaml
# gitops/apps/root/kustomization.yaml 에 추가
resources:
  # ... 기존 항목들 ...
  - <appname>-app.yaml
```

---

### Step 3: (선택) 별도 Namespace가 필요한 경우

`apps` namespace 외에 앱 전용 namespace가 필요하다면 다음 파일을 생성한다.

#### 3-1. Namespace 매니페스트 생성

```yaml
# gitops/platform/namespaces/namespace-<appname>.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: <appname>
```

#### 3-2. `gitops/platform/namespaces/kustomization.yaml` 업데이트

```yaml
# gitops/platform/namespaces/kustomization.yaml 에 추가
resources:
  # ... 기존 항목들 ...
  - namespace-<appname>.yaml
```

> **참고**: 현재 `apps` AppProject의 `destinations`는 `namespace: apps`로만 제한되어 있다.
> 별도 namespace를 사용하려면 `appproject-apps.yaml`의 `destinations`도 함께 수정해야 한다.

---

### Step 4: (선택) Vault 시크릿 등록 + ExternalSecret 추가

앱이 시크릿(DB 비밀번호, API 키 등)을 필요로 하는 경우 Vault와 ESO를 활용한다.

#### 4-1. Vault에 시크릿 저장

```bash
export VAULT_ADDR="https://vault.127.0.0.1.nip.io"
export VAULT_TOKEN="<token>"

# 앱 시크릿 저장 (경로 규칙: secret/apps/<appname>/...)
vault kv put secret/apps/<appname>/config \
  db_password="supersecret" \
  api_key="myapikey"

# 확인
vault kv get secret/apps/<appname>/config
```

#### 4-2. ExternalSecret 매니페스트 작성

```yaml
# gitops/workloads/<appname>/external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: <appname>-secret
  namespace: apps
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: <appname>-secret
    creationPolicy: Owner
  data:
    - secretKey: db_password
      remoteRef:
        key: secret/apps/<appname>/config
        property: db_password
    - secretKey: api_key
      remoteRef:
        key: secret/apps/<appname>/config
        property: api_key
```

#### 4-3. `kustomization.yaml`에 ExternalSecret 추가

```yaml
# gitops/workloads/<appname>/kustomization.yaml
resources:
  - deployment.yaml
  - service.yaml
  - external-secret.yaml # 추가
```

#### 4-4. Deployment에서 시크릿 참조

```yaml
# deployment.yaml 의 container spec에 추가
envFrom:
  - secretRef:
      name: <appname>-secret
```

---

### Step 5: commit → push → ArgoCD 자동 sync 확인

```bash
# 변경 파일 스테이징
git add gitops/workloads/<appname>/
# 또는 외부 레포 등록 시:
# git add gitops/apps/root/<appname>-app.yaml gitops/apps/root/kustomization.yaml

# 커밋
git commit -m "feat: add <appname> to GitOps"

# push (ArgoCD가 자동 감지)
git push origin main
```

ArgoCD는 기본적으로 3분 주기로 레포를 폴링하며, webhook이 설정된 경우 즉시 감지한다.

수동으로 즉시 sync하려면:

```bash
# apps-generator가 새 Application을 생성했는지 확인
argocd app list | grep <appname>

# 수동 sync (필요 시)
argocd app sync <appname>
```

## Verification (검증 절차)

```bash
# ArgoCD Application 상태 확인
argocd app list
argocd app get <appname>

# Pod 상태 확인
kubectl get pods -n apps
# 또는 별도 namespace를 사용하는 경우
kubectl get pods -n <appname>

# ESO 동기화 확인 (시크릿 연동 시)
kubectl -n apps get externalsecret <appname>-secret
kubectl -n apps get secret <appname>-secret

# ArgoCD sync 상태 확인
argocd app get <appname> --refresh
```

정상 상태:

- ArgoCD Application: `Synced` / `Healthy`
- Pod: `Running`
- ExternalSecret: `SecretSynced` (시크릿 연동 시)

## Common Pitfalls

### AppProject `sourceRepos` 제한

현재 `apps` AppProject는 `https://github.com/buenhyden/hy-home.k8s.git` 레포만 허용한다.
외부 앱 레포를 등록하기 전에 `gitops/clusters/local/appproject-apps.yaml`에서 `sourceRepos`를 먼저 수정하고
ArgoCD sync가 완료된 후 Application CR을 추가해야 한다. 순서가 바뀌면 sync 오류가 발생한다.

### AppProject `destinations` namespace 제한

`apps` AppProject의 `destinations.namespace`가 `apps`로 고정되어 있다.
별도 namespace(예: `<appname>`)에 배포하려면 `appproject-apps.yaml`의 `destinations` 섹션에
해당 namespace를 추가해야 한다.

### `apps-generator` ApplicationSet destination 고정

`apps-generator` ApplicationSet은 destination namespace를 `apps`로 고정한다.
workload 디렉토리 내의 매니페스트에서 `namespace: apps`를 명시하거나,
`CreateNamespace=true` syncOption을 활용한다.

### ExternalSecret `SecretSynced: False`

Vault 경로가 `secret/apps/<appname>/...` 형식을 따르는지 확인한다.
ClusterSecretStore `vault-backend`가 정상 동작하는지 확인:

```bash
kubectl get clustersecretstore vault-backend -o jsonpath='{.status.conditions[0].type}'
# 출력: Ready
```

### ImagePullBackOff

이미지 레지스트리가 private인 경우 imagePullSecret을 추가하거나,
Vault에 레지스트리 자격증명을 저장하고 ESO로 연동해야 한다.

### ArgoCD가 새 Application을 생성하지 않는 경우

`apps-generator` ApplicationSet이 `gitops/workloads/*` 를 스캔하므로
디렉토리에 유효한 `kustomization.yaml` 또는 k8s 매니페스트가 있어야 한다.
빈 디렉토리는 감지되지 않는다.

## Related Documents

- **AppProject 정책**: [`../../gitops/clusters/local/appproject-apps.yaml`](../../gitops/clusters/local/appproject-apps.yaml)
- **ApplicationSet**: [`../../gitops/clusters/local/applicationset-apps.yaml`](../../gitops/clusters/local/applicationset-apps.yaml)
- **Namespace 매니페스트**: [`../../gitops/platform/namespaces/`](../../gitops/platform/namespaces/)
- **NetworkPolicy 패턴**: [`../../gitops/platform/network-policies/`](../../gitops/platform/network-policies/)
- **Runbook**: [`../09.runbooks/0006-new-app-onboarding-runbook.md`](../09.runbooks/0006-new-app-onboarding-runbook.md)
- **ESO/Vault Recovery Runbook**: [`../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md`](../09.runbooks/0002-argocd-eso-vault-recovery-runbook.md)
- **Bootstrap Guide**: [`./0001-wsl-k3d-argocd-bootstrap-guide.md`](./0001-wsl-k3d-argocd-bootstrap-guide.md)
