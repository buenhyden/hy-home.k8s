---
title: 'Headlamp 인증 & OIDC 연동 Guide'
type: guide
status: active
owner: platform
updated: 2026-05-09
---

# Headlamp 인증 & OIDC 연동 Guide

## Overview (KR)

이 문서는 Headlamp Kubernetes UI의 인증 방식을 설명한다.
현재 anonymous 모드로 동작하는 Headlamp에서 ServiceAccount 토큰 로그인 및 Keycloak OIDC 연동까지 단계적으로 전환하는 방법을 다룬다.
GitOps(ArgoCD + Helm values) 기반으로 변경사항을 적용하며, Kubernetes RBAC과 Keycloak groups 매핑 방법을 포함한다.

## Guide Type

`how-to`

## Target Audience

- Platform Engineer
- Developer

## Purpose

Headlamp 인증 방식을 anonymous → 토큰(ServiceAccount) → OIDC(Keycloak) 순서로 전환하고,
Keycloak groups를 Kubernetes RBAC에 매핑하여 최소 권한 접근을 구현한다.

> **Agent execution boundary**: 이 가이드의 `kubectl create`/`kubectl apply` 예시는 운영자 승인 하의 로컬 bootstrap 또는 break-glass 절차다. Agent는 기본적으로 GitOps 변경안, RBAC 최소권한 검토, 검증 계획까지만 작성한다.

## Prerequisites

### 필수 도구

```bash
kubectl version --client
helm version    # v3.x
vault version   # Vault CLI
```

### 클러스터 상태 확인

```bash
# Headlamp 현재 상태 확인
kubectl -n headlamp get pods,ingress,svc

# Headlamp 현재 args 확인
kubectl -n headlamp get deployment headlamp -o jsonpath='{.spec.template.spec.containers[0].args}'

# ArgoCD sync 상태 확인
kubectl -n argocd get app platform-headlamp
```

### Headlamp 접근 확인

```bash
curl -ksS -o /dev/null -w '%{http_code}' https://headlamp.127.0.0.1.nip.io/
# 출력: 200
```

### 환경 변수 (OIDC 연동 시)

```bash
export VAULT_TOKEN="<token>"
export VAULT_ADDR="https://vault.127.0.0.1.nip.io"
export KEYCLOAK_URL="https://keycloak.example.com"   # 실제 Keycloak 주소로 변경
export KEYCLOAK_REALM="hyhome"
```

## Step-by-step Instructions

### 1. 현재 인증 방식 확인 (Anonymous Mode)

현재 Headlamp은 `-in-cluster` 모드로 동작하며, 로그인 화면에서 토큰 입력 없이 접근 가능한 anonymous 상태일 수 있다.

```bash
# 현재 Deployment args 확인
kubectl -n headlamp get deployment headlamp \
  -o jsonpath='{.spec.template.spec.containers[0].args}' | tr ',' '\n'
```

현재 구성된 args:

```text
-in-cluster
-in-cluster-context-name=main
-plugins-dir=/headlamp/plugins
-session-ttl=86400
```

> **참고**: `-enable-anonymous-access` 플래그가 없으면 로그인 화면에서 토큰이 필요하다.
> anonymous 모드를 비활성화하려면 이 플래그를 제거하거나 처음부터 추가하지 않는다.

### 2. ServiceAccount 토큰으로 로그인

#### 2-A. 단기 토큰 발급 (human-approved local admin)

```bash
# headlamp-admin ServiceAccount가 없으면 생성
kubectl -n headlamp get sa headlamp-admin 2>/dev/null || \
  kubectl -n headlamp create serviceaccount headlamp-admin

# ClusterRoleBinding 생성 (cluster-admin 권한, 필요에 따라 조정)
# human-approved local admin bootstrap only
kubectl create clusterrolebinding headlamp-admin \
  --clusterrole=cluster-admin \
  --serviceaccount=headlamp:headlamp-admin \
  --dry-run=client -o yaml | kubectl apply -f -

# 단기 토큰 발급 (1시간)
kubectl -n headlamp create token headlamp-admin --duration=1h
```

#### 2-B. Long-lived Token Secret (Kubernetes 1.24+에서는 비권장, break-glass only)

```bash
# Long-lived token Secret 생성
# human-approved break-glass only
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: headlamp-admin-token
  namespace: headlamp
  annotations:
    kubernetes.io/service-account.name: headlamp-admin
type: kubernetes.io/service-account-token
EOF

# 토큰 추출
kubectl -n headlamp get secret headlamp-admin-token \
  -o jsonpath='{.data.token}' | base64 -d
```

#### 2-C. Headlamp UI에서 토큰 입력

1. `https://headlamp.127.0.0.1.nip.io` 접속
2. 로그인 화면에서 토큰 붙여넣기
3. 로그인 완료 후 클러스터 `main` 선택

### 3. OIDC 연동 (Keycloak)

#### 3-A. Keycloak Realm & Client 설정

Keycloak 관리 콘솔(`https://keycloak.example.com/admin`)에서 아래 순서로 설정한다.

**Realm 설정**:

- Realm 이름: `hyhome` (기존 Realm 사용)

**Client 생성**:

```text
Client ID:               headlamp
Client Protocol:         openid-connect
Access Type:             confidential
Valid Redirect URIs:     https://headlamp.127.0.0.1.nip.io/oidc-callback
Web Origins:             https://headlamp.127.0.0.1.nip.io
```

**Client Scopes**:

기본 스코프 외에 `groups` 스코프를 추가한다:

1. Keycloak 좌측 메뉴 → `Client Scopes` → `groups` 스코프 생성
2. Mapper 추가: `Group Membership`, Token Claim Name: `groups`, Full path: off
3. 생성한 `headlamp` Client → `Client Scopes` 탭 → `groups` 추가 (Default)

**Client Secret 확인**:

```text
Credentials 탭 → Secret 복사
```

#### 3-B. OIDC Client Secret을 Vault에 저장

```bash
# external secret operation; human-approved bootstrap only
vault kv put secret/platform/headlamp \
  oidc_client_secret="<keycloak-client-secret>"

# 확인
vault kv get secret/platform/headlamp
```

#### 3-C. ExternalSecret으로 Secret 동기화

`gitops/platform/headlamp/externalsecret-oidc.yaml` 파일 생성:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: headlamp-oidc-secret
  namespace: headlamp
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: vault-backend
    kind: ClusterSecretStore
  target:
    name: headlamp-oidc-secret
    creationPolicy: Owner
  data:
    - secretKey: OIDC_CLIENT_SECRET
      remoteRef:
        key: secret/platform/headlamp
        property: oidc_client_secret
```

#### 3-D. Headlamp Helm values 수정 (GitOps)

ArgoCD Application이 참조하는 Helm values 파일에 OIDC args를 추가한다.

`gitops/platform/headlamp/values.yaml` (또는 해당 App의 values):

```yaml
config:
  args:
    - '-in-cluster'
    - '-in-cluster-context-name=main'
    - '-plugins-dir=/headlamp/plugins'
    - '-session-ttl=86400'
    - '-oidc-client-id=headlamp'
    - '-oidc-client-secret=$(OIDC_CLIENT_SECRET)'
    - '-oidc-idp-issuer-url=https://keycloak.example.com/realms/hyhome'
    - '-oidc-scopes=openid,profile,email,groups'

env:
  - name: OIDC_CLIENT_SECRET
    valueFrom:
      secretKeyRef:
        name: headlamp-oidc-secret
        key: OIDC_CLIENT_SECRET
```

> **주의**: `$(OIDC_CLIENT_SECRET)` 환경변수 참조 형식은 Kubernetes container args에서 지원된다.
> Secret을 직접 args에 평문으로 넣지 않는다.

#### 3-E. ArgoCD Sync

```bash
# GitOps 변경사항 push 후 ArgoCD sync
kubectl -n argocd get app platform-headlamp

# human-approved operator-triggered reconciliation only
kubectl -n argocd patch app platform-headlamp \
  --type merge \
  -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"HEAD"}}}'
```

### 4. RBAC: Keycloak Groups → Kubernetes RBAC 매핑

OIDC 토큰의 `groups` claim을 Kubernetes RBAC Group에 매핑한다.

#### 4-A. Keycloak Group 생성

Keycloak 관리 콘솔:

- `Groups` → 새 그룹 생성 예시: `k8s-admins`, `k8s-viewers`
- 사용자를 각 그룹에 할당

#### 4-B. Kubernetes ClusterRoleBinding 생성

```bash
# k8s-admins 그룹 → cluster-admin
# human-approved RBAC bootstrap only
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: keycloak-k8s-admins
subjects:
  - kind: Group
    name: k8s-admins    # Keycloak group name (groups claim 값)
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: cluster-admin
  apiGroup: rbac.authorization.k8s.io
EOF

# k8s-viewers 그룹 → view (읽기 전용)
# human-approved RBAC bootstrap only
kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: keycloak-k8s-viewers
subjects:
  - kind: Group
    name: k8s-viewers
    apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: view
  apiGroup: rbac.authorization.k8s.io
EOF
```

> **참고**: `groups` claim의 값은 Keycloak Group Mapper의 `Full group path` 설정에 따라 달라진다.
> Full path off → `/k8s-admins` 대신 `k8s-admins`로 매핑된다. RBAC subject name과 일치해야 한다.

#### 4-C. RBAC 검증

OIDC 로그인 후:

```bash
# OIDC 토큰으로 인증된 사용자 확인
kubectl auth whoami

# 특정 권한 확인
kubectl auth can-i list pods --as=<username> --as-group=k8s-admins
```

## Common Pitfalls

### OIDC Redirect URI 불일치

Keycloak Client의 `Valid Redirect URIs`가 정확히 일치해야 한다.

```text
올바름: https://headlamp.127.0.0.1.nip.io/oidc-callback
잘못됨: https://headlamp.127.0.0.1.nip.io/oidc-callback/  (후행 슬래시 주의)
```

### groups claim이 토큰에 없는 경우

Keycloak Client에 `groups` scope가 Default로 추가되지 않으면 토큰에 claim이 포함되지 않는다.

```bash
# 토큰 디코드 확인 (jq 필요)
kubectl -n headlamp create token headlamp-admin | \
  cut -d. -f2 | base64 -d 2>/dev/null | jq '.groups'
```

### 단기 토큰 만료 (session-ttl 초과)

`-session-ttl=86400` (24시간)이 기본값이나, `kubectl create token` 기본 유효시간은 1시간이다.
토큰 만료 시 Headlamp 로그인 화면으로 리다이렉트된다. OIDC 전환 후에는 Keycloak 세션으로 자동 갱신된다.

### ArgoCD App에 ExternalSecret CRD 순서 문제

ExternalSecret이 Secret보다 먼저 sync되면 OIDC Secret이 없는 상태에서 Headlamp Pod가 재기동될 수 있다.
ArgoCD sync wave를 사용해 순서를 보장한다:

```yaml
# ExternalSecret에 annotation 추가
metadata:
  annotations:
    argocd.argoproj.io/sync-wave: '-1'
```

## Related Documents

- **Runbook**: [`../runbooks/0005-headlamp-keycloak-runbook.md`](../runbooks/0005-headlamp-keycloak-runbook.md)
- **ADR-0010**: [`../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md`](../../02.architecture/decisions/0010-headlamp-replaces-dashboard.md)
- **Operations**: [`../policies/0004-rollouts-notifications-headlamp-policy.md`](../policies/0004-rollouts-notifications-headlamp-policy.md)
- **Bootstrap Runbook**: [`../runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../runbooks/0004-rollouts-notifications-headlamp-runbook.md)
- **Headlamp Chart**: [headlamp-k8s.github.io/headlamp](https://headlamp-k8s.github.io/headlamp/)
