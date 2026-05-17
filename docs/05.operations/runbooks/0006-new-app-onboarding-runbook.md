---
title: 'New App GitOps Onboarding Runbook'
type: runbook
status: active
owner: platform
updated: 2026-05-09
---

# New App GitOps Onboarding Runbook

## Runbook Type

`WSL2 k3d/k3s GitOps 앱 온보딩`

## Overview (KR)

이 런북은 `hy-home.k8s` 클러스터에 새로운 애플리케이션을 GitOps 방식으로 온보딩하는
단계별 운영 절차를 제공한다. `apps-generator` ApplicationSet 기반 자동 감지 방식(권장)과
Application CR 수동 등록 방식을 모두 다룬다.
Vault 시크릿 연동(ESO), 동기화 검증, 트러블슈팅 절차를 포함한다.

## Purpose

신규 애플리케이션을 `gitops/workloads/` 또는 승인된 외부 repo Application으로 등록하고, PR review 이후 ArgoCD reconciliation으로 배포 상태를 검증한다.

## Canonical References

- [`../guides/0005-new-app-gitops-onboarding-guide.md`](../guides/0005-new-app-gitops-onboarding-guide.md)
- [`../../../gitops/clusters/local/appproject-apps.yaml`](../../../gitops/clusters/local/appproject-apps.yaml)
- [`../../../gitops/clusters/local/applicationset-apps.yaml`](../../../gitops/clusters/local/applicationset-apps.yaml)

## When to Use

- 새로운 사용자 애플리케이션을 `apps` AppProject에 등록할 때
- `gitops/workloads/` 에 신규 workload 디렉토리를 추가할 때
- 외부 레포 앱을 Application CR로 수동 등록할 때
- ArgoCD sync 실패 후 앱 온보딩 복구가 필요할 때
- Vault 시크릿 연동(ESO) 초기 설정이 필요할 때

---

## Procedure or Checklist

아래 절차는 workload 디렉토리 생성, 선택적 외부 repo Application 등록, Vault secret 연동, 커밋 및 동기화 검증 순서로 수행한다.

## Procedure 1: 앱 Workload 디렉토리 구조 생성

`apps-generator` ApplicationSet이 `gitops/workloads/*`를 자동 스캔하므로,
이 레포에 workload 디렉토리를 추가하는 것이 가장 간단한 방법이다.

```bash
# 1. workload 디렉토리 생성
mkdir -p gitops/workloads/<appname>

# 2. kustomization.yaml 작성
cat > gitops/workloads/<appname>/kustomization.yaml << 'EOF'
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
  - deployment.yaml
  - service.yaml
EOF

# 3. deployment.yaml 작성 (앱에 맞게 수정)
cat > gitops/workloads/<appname>/deployment.yaml << 'EOF'
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
EOF

# 4. service.yaml 작성
cat > gitops/workloads/<appname>/service.yaml << 'EOF'
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
EOF

# 5. 파일 확인
ls -la gitops/workloads/<appname>/
```

> **참고**: `apps-generator` ApplicationSet은 destination namespace를 `apps`로 고정한다.
> 별도 namespace를 사용하려면 Procedure 1-A를 참고한다.

### Procedure 1-A: (선택) 별도 Namespace 추가

```bash
# 1. Namespace 매니페스트 생성
cat > gitops/platform/namespaces/namespace-<appname>.yaml << 'EOF'
apiVersion: v1
kind: Namespace
metadata:
  name: <appname>
EOF

# 2. kustomization.yaml 업데이트
# gitops/platform/namespaces/kustomization.yaml 에 항목 추가
# resources: 섹션 마지막에 추가:
#   - namespace-<appname>.yaml

# 3. appproject-apps.yaml destinations 업데이트 (필요 시)
# gitops/clusters/local/appproject-apps.yaml 에서
# destinations 섹션에 신규 namespace 추가

# 4. 확인
cat gitops/platform/namespaces/kustomization.yaml
```

---

## Procedure 2: (선택) 외부 레포 앱 Application CR 등록

외부 GitHub 레포 앱을 등록할 때 사용한다.
이 레포 내 workload 방식(Procedure 1)과는 다른 경로이다.

```bash
# 1. appproject-apps.yaml sourceRepos 수정 (외부 레포인 경우)
# gitops/clusters/local/appproject-apps.yaml 의 sourceRepos에 추가:
#   - https://github.com/buenhyden/<appname>.git

# 2. Application CR 파일 생성
cat > gitops/apps/root/<appname>-app.yaml << 'EOF'
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
EOF

# 3. kustomization.yaml 업데이트
# gitops/apps/root/kustomization.yaml 의 resources 섹션에 추가:
#   - <appname>-app.yaml

# 4. 변경 확인
cat gitops/apps/root/kustomization.yaml
cat gitops/apps/root/<appname>-app.yaml
```

---

## Procedure 3: Vault 시크릿 + ExternalSecret 설정

앱이 시크릿을 필요로 하는 경우에만 수행한다.

```bash
# 1. Vault 연결 확인
export VAULT_ADDR="https://vault.127.0.0.1.nip.io"
export VAULT_TOKEN="<token>"
vault status

# 2. 앱 시크릿 저장 (경로 규칙: secret/apps/<appname>/...)
# external secret operation; human-approved only
vault kv put secret/apps/<appname>/config \
  db_password="<password>" \
  api_key="<key>"

# 3. 저장 확인
vault kv get secret/apps/<appname>/config

# 4. ExternalSecret 매니페스트 생성
cat > gitops/workloads/<appname>/external-secret.yaml << 'EOF'
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
EOF

# 5. kustomization.yaml 에 ExternalSecret 추가
# gitops/workloads/<appname>/kustomization.yaml 의 resources에:
#   - external-secret.yaml
```

> **주의**: Vault 시크릿 경로는 `secret/apps/<appname>/...` 형식을 반드시 준수한다.
> ClusterSecretStore `vault-backend`의 `path` 접두사가 `secret/`이므로
> ExternalSecret의 `remoteRef.key`는 `secret/apps/<appname>/config`처럼 전체 경로를 지정한다.

---

## Procedure 4: 커밋 및 동기화 검증

```bash
# 1. 변경 파일 스테이징
git add gitops/workloads/<appname>/
# 외부 레포 등록 시 추가:
# git add gitops/apps/root/<appname>-app.yaml
# git add gitops/apps/root/kustomization.yaml
# git add gitops/clusters/local/appproject-apps.yaml

# 2. 커밋 및 feature branch push 후 PR review/merge 진행
git commit -m "feat: add <appname> gitops workload"
git push origin feat/<appname>-gitops

# 3. ArgoCD 감지 대기 (기본 폴링 주기: 3분) 또는 수동 새로고침
argocd app list
argocd app get apps-generator --refresh 2>/dev/null || true

# 4. 새 Application 생성 확인
argocd app list | grep <appname>

# 5. Application sync 상태 확인
argocd app get <appname>

# 6. operator-triggered reconciliation only
argocd app sync <appname>

# 7. Pod 상태 확인
kubectl get pods -n apps -l app=<appname>

# 8. ESO 동기화 확인 (시크릿 연동 시)
kubectl -n apps get externalsecret <appname>-secret
kubectl -n apps describe externalsecret <appname>-secret | grep -A5 "Conditions"
kubectl -n apps get secret <appname>-secret
```

### 검증 체크리스트

- [ ] ArgoCD Application 상태: `Synced` / `Healthy`
- [ ] Pod 상태: `Running` (apps namespace)
- [ ] ExternalSecret 상태: `SecretSynced` (시크릿 연동 시)
- [ ] Kubernetes Secret 생성 확인 (시크릿 연동 시)
- [ ] `argocd app list`에 앱이 표시됨

---

## Verification Steps

- [ ] workload 디렉토리에 `kustomization.yaml`과 필요한 manifest가 존재한다.
- [ ] feature branch push 후 PR review/merge 흐름을 거친다.
- [ ] `argocd app get <appname>` 결과가 `Synced` / `Healthy`다.
- [ ] secret 연동 시 ExternalSecret과 generated Secret이 정상 상태다.

## Observability and Evidence Sources

- **Signals**: ArgoCD Application health, ApplicationSet generator logs, pod readiness, ExternalSecret conditions.
- **Evidence to Capture**: PR link, ArgoCD app status, pod event output, ExternalSecret status.

## Safe Rollback or Recovery Procedure

- 앱 온보딩 실패 시 workload directory 또는 Application manifest를 되돌리는 PR을 작성한다.
- secret 연동 실패 시 Vault path와 ExternalSecret mapping을 먼저 검증하고, plaintext secret을 커밋하지 않는다.
- 배포가 비정상 상태이면 ArgoCD sync를 중단하고 이전 image/tag 또는 이전 manifest revision으로 되돌린다.

## Troubleshooting

### ImagePullBackOff

```bash
# Pod 이벤트 확인
kubectl -n apps describe pod -l app=<appname> | tail -20

# 이미지 이름 오타 확인
kubectl -n apps get deployment <appname> -o jsonpath='{.spec.template.spec.containers[0].image}'

# private 레지스트리인 경우 imagePullSecret 확인
kubectl -n apps get secrets | grep pull
```

원인 및 해결:

- 이미지 태그 오타 → `deployment.yaml` 이미지 경로 수정 후 커밋
- Private 레지스트리 자격증명 없음 → Vault에 레지스트리 토큰 저장 후 ESO로 imagePullSecret 생성

### Namespace Not Found

```bash
# namespace 존재 여부 확인
kubectl get namespace <appname> 2>/dev/null || echo "namespace not found"

# platform-namespaces ArgoCD App sync 상태 확인
argocd app get platform-namespaces
# operator-triggered reconciliation only
argocd app sync platform-namespaces

# namespace 매니페스트가 kustomization.yaml에 등록됐는지 확인
cat gitops/platform/namespaces/kustomization.yaml | grep <appname>
```

원인 및 해결:

- `namespace-<appname>.yaml`이 `gitops/platform/namespaces/kustomization.yaml`에 누락 → 추가 후 커밋
- `platform-namespaces` ArgoCD App이 아직 sync되지 않음 → 수동 sync 수행

### ESO Sync 실패 (ExternalSecret SecretSynced: False)

```bash
# ExternalSecret 상세 이벤트 확인
kubectl -n apps describe externalsecret <appname>-secret

# ClusterSecretStore 상태 확인
kubectl get clustersecretstore vault-backend -o jsonpath='{.status.conditions[0].type}'
# 정상: Ready

# Vault 경로 확인
vault kv get secret/apps/<appname>/config

# ESO controller 로그 확인
kubectl -n external-secrets get pods
kubectl -n external-secrets logs deploy/external-secrets -c external-secrets --tail=50 | grep <appname>

# ESO 강제 재동기화
kubectl -n apps annotate externalsecret <appname>-secret \
  force-sync=$(date +%s) --overwrite
```

원인 및 해결:

- Vault 경로 불일치 → `remoteRef.key`가 `secret/apps/<appname>/config` 형식인지 확인
- Vault 토큰 만료 → Vault 재인증 후 ESO ClusterSecretStore 재설정
- `property` 이름 불일치 → `vault kv get` 결과의 실제 key 이름과 `remoteRef.property` 일치 확인

### AppProject 권한 오류 (`application 'X' is not permitted in project 'apps'`)

```bash
# AppProject 현재 설정 확인
kubectl -n argocd get appproject apps -o yaml

# sourceRepos 확인
argocd proj get apps | grep "Source repos"

# destinations 확인
argocd proj get apps | grep "Destinations"
```

원인 및 해결:

- 외부 레포 URL이 `sourceRepos`에 없음 → `gitops/clusters/local/appproject-apps.yaml`의 `sourceRepos`에 추가 후 커밋
- 대상 namespace가 `destinations`에 없음 → `appproject-apps.yaml`의 `destinations`에 해당 namespace 추가
- AppProject 변경 후 ArgoCD root-application sync 필요:

```bash
# operator-triggered reconciliation only
argocd app sync root-application
# AppProject 변경이 반영될 때까지 대기 후 앱 재시도
argocd app sync <appname>
```

### ArgoCD가 새 Application을 생성하지 않는 경우 (ApplicationSet)

```bash
# apps-generator ApplicationSet 상태 확인
kubectl -n argocd get applicationset apps-generator -o yaml

# ApplicationSet generator 로그 확인
kubectl -n argocd logs deploy/argocd-applicationset-controller --tail=50 | grep <appname>

# workload 디렉토리 구조 확인 (kustomization.yaml 필수)
ls gitops/workloads/<appname>/
cat gitops/workloads/<appname>/kustomization.yaml
```

원인 및 해결:

- `kustomization.yaml`이 없거나 유효하지 않음 → 올바른 `kustomization.yaml` 추가
- 폴링 주기 대기 필요 → ArgoCD webhook 설정 또는 3분 대기
- 디렉토리가 `gitops/workloads/` 직하위가 아님 → 경로 확인 (`gitops/workloads/<appname>/`)

## Related Documents

- **Guide**: [`../guides/0005-new-app-gitops-onboarding-guide.md`](../guides/0005-new-app-gitops-onboarding-guide.md)
- **AppProject**: [`../../../gitops/clusters/local/appproject-apps.yaml`](../../../gitops/clusters/local/appproject-apps.yaml)
- **ApplicationSet**: [`../../../gitops/clusters/local/applicationset-apps.yaml`](../../../gitops/clusters/local/applicationset-apps.yaml)
- **Namespace 매니페스트**: [`../../../gitops/platform/namespaces`](../../../gitops/platform/namespaces)
- **ESO/Vault Recovery**: [`./0002-argocd-eso-vault-recovery-runbook.md`](./0002-argocd-eso-vault-recovery-runbook.md)
- **Platform Bootstrap**: [`./0001-argocd-platform-bootstrap-runbook.md`](./0001-argocd-platform-bootstrap-runbook.md)
