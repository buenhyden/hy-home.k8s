# Headlamp Keycloak OIDC 전환 Runbook

## Runbook Type

`WSL2 k3d/k3s 운영 핫픽스 및 부트스트랩`

## Overview (KR)

이 런북은 Headlamp Kubernetes UI의 인증 전환 및 복구 절차를 제공한다.
ServiceAccount 토큰 로그인, Keycloak OIDC 전환(GitOps via ArgoCD), Keycloak 설정 체크리스트,
그리고 OIDC 관련 오류 트러블슈팅을 다룬다.

## When to Use

- Headlamp에서 ServiceAccount 토큰으로 로그인이 필요할 때
- anonymous 모드에서 OIDC 인증으로 전환할 때
- OIDC redirect URI 오류, 토큰 만료, 403 RBAC 오류가 발생했을 때
- Keycloak Client 설정을 검증해야 할 때

---

## Procedure 1: ServiceAccount 토큰으로 Headlamp 로그인

### 1-1. ServiceAccount 및 ClusterRoleBinding 확인/생성

```bash
# ServiceAccount 존재 확인
kubectl -n headlamp get sa headlamp-admin 2>/dev/null && echo "EXISTS" || echo "NOT FOUND"

# 없으면 생성
kubectl -n headlamp create serviceaccount headlamp-admin

# ClusterRoleBinding 생성 (멱등)
kubectl create clusterrolebinding headlamp-admin \
  --clusterrole=cluster-admin \
  --serviceaccount=headlamp:headlamp-admin \
  --dry-run=client -o yaml | kubectl apply -f -

# 확인
kubectl get clusterrolebinding headlamp-admin
```

### 1-2. 단기 토큰 발급

```bash
# 1시간 유효 토큰 (기본 권장)
kubectl -n headlamp create token headlamp-admin --duration=1h

# 24시간 유효 토큰 (필요 시)
kubectl -n headlamp create token headlamp-admin --duration=24h
```

### 1-3. Headlamp UI 로그인

```text
1. https://headlamp.127.0.0.1.nip.io 접속
2. 로그인 화면에서 토큰 붙여넣기
3. 클러스터 "main" 선택 → 로그인 완료
```

### 1-4. 접근 검증

```bash
curl -ksS -o /dev/null -w '%{http_code}' https://headlamp.127.0.0.1.nip.io/
# 출력: 200
```

---

## Procedure 2: OIDC 전환 (GitOps via ArgoCD)

### 2-1. Vault에 OIDC Client Secret 저장

```bash
export VAULT_TOKEN="<token>"
export VAULT_ADDR="https://vault.127.0.0.1.nip.io"

vault kv put secret/platform/headlamp \
  oidc_client_secret="<keycloak-client-secret>"

# 확인
vault kv get secret/platform/headlamp
```

> **주의**: Client Secret은 반드시 Vault에 저장. 평문 커밋 금지.

### 2-2. ExternalSecret 생성 (GitOps)

`gitops/platform/headlamp/externalsecret-oidc.yaml`:

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: headlamp-oidc-secret
  namespace: headlamp
  annotations:
    argocd.argoproj.io/sync-wave: '-1'
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

### 2-3. Headlamp Helm values 수정 (GitOps)

ArgoCD Application이 참조하는 values 파일에 OIDC args 추가:

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

또는 Helm chart native OIDC 설정 형식:

```yaml
config:
  oidc:
    clientID: 'headlamp'
    clientSecret: '<from-vault>'
    issuerURL: 'https://keycloak.example.com/realms/hyhome'
    scopes: 'openid profile email groups'
```

### 2-4. 변경사항 커밋 & ArgoCD Sync

```bash
# Git push
git add gitops/platform/headlamp/
git commit -m "feat: enable headlamp OIDC via keycloak"
git push

# ArgoCD sync 대기
kubectl -n argocd get app platform-headlamp --watch

# 수동 sync (필요 시)
kubectl -n argocd patch app platform-headlamp \
  --type merge \
  -p '{"operation":{"initiatedBy":{"username":"admin"},"sync":{"revision":"HEAD"}}}'
```

### 2-5. OIDC 전환 후 검증

```bash
# Pod 재기동 확인
kubectl -n headlamp rollout status deployment headlamp

# OIDC 환경변수 주입 확인
kubectl -n headlamp get deployment headlamp \
  -o jsonpath='{.spec.template.spec.containers[0].env}' | jq .

# ExternalSecret 동기화 확인
kubectl -n headlamp get externalsecret headlamp-oidc-secret
kubectl -n headlamp get secret headlamp-oidc-secret
```

브라우저에서 `https://headlamp.127.0.0.1.nip.io` 접속 시 Keycloak 로그인 페이지로 리다이렉트되어야 한다.

---

## Procedure 3: Keycloak 설정 체크리스트

Keycloak 관리 콘솔(`https://keycloak.example.com/admin`) 접속 후 확인.

### 3-1. Realm 확인

```text
[ ] Realm 이름: hyhome (존재 확인)
[ ] Realm 활성화 상태: Enabled
```

### 3-2. Client 설정 확인

```text
[ ] Client ID: headlamp
[ ] Client Protocol: openid-connect
[ ] Access Type: confidential
[ ] Standard Flow Enabled: ON
[ ] Direct Access Grants: OFF (권장)
[ ] Valid Redirect URIs: https://headlamp.127.0.0.1.nip.io/oidc-callback
[ ] Web Origins: https://headlamp.127.0.0.1.nip.io
[ ] Client Secret: Credentials 탭에서 확인 및 Vault 저장 여부 검증
```

### 3-3. Groups Scope 확인

```text
[ ] Client Scopes → "groups" 스코프 존재
[ ] groups 스코프에 Group Membership mapper 포함
    - Token Claim Name: groups
    - Full group path: OFF (off일 경우 "k8s-admins", on일 경우 "/k8s-admins")
[ ] headlamp Client → Client Scopes → groups가 Default로 추가됨
```

### 3-4. 사용자 & 그룹 확인

```bash
# Keycloak Admin API로 headlamp client well-known 확인
curl -s "https://keycloak.example.com/realms/hyhome/.well-known/openid-configuration" | \
  jq '{issuer, authorization_endpoint, token_endpoint}'
```

```text
[ ] hyhome Realm well-known endpoint 응답 정상
[ ] 사용자가 Keycloak Group(k8s-admins 등)에 할당됨
```

### 3-5. Kubernetes RBAC Binding 확인

```bash
# Keycloak group → Kubernetes ClusterRoleBinding
kubectl get clusterrolebinding | grep keycloak

# 특정 binding 확인
kubectl get clusterrolebinding keycloak-k8s-admins -o yaml
```

---

## Troubleshooting

### OIDC Redirect URI 오류

**증상**: Keycloak에서 `Invalid redirect_uri` 또는 `redirect_uri mismatch` 오류

**확인**:

```bash
# Headlamp OIDC args에서 issuer URL 확인
kubectl -n headlamp get deployment headlamp \
  -o jsonpath='{.spec.template.spec.containers[0].args}' | tr ',' '\n' | grep oidc
```

**수정**:

Keycloak Client `Valid Redirect URIs`가 정확히 아래와 일치하는지 확인:

```text
https://headlamp.127.0.0.1.nip.io/oidc-callback
```

후행 슬래시(`/`) 및 오타에 주의한다.

---

### Token Expiry (토큰 만료)

**증상**: Headlamp에서 인증이 갑자기 끊기거나 로그인 화면으로 리다이렉트됨

**확인**:

```bash
# Headlamp session-ttl 확인 (초 단위, 기본 86400 = 24h)
kubectl -n headlamp get deployment headlamp \
  -o jsonpath='{.spec.template.spec.containers[0].args}' | grep session-ttl
```

**조치**:

- 토큰 로그인: `kubectl -n headlamp create token headlamp-admin --duration=24h` 재발급
- OIDC 사용 시: Keycloak 세션 정책에서 `SSO Session Max` 시간 확인

  ```text
  Keycloak 콘솔 → Realm Settings → Sessions → SSO Session Max
  ```

---

### 403 RBAC 오류

**증상**: Headlamp 로그인은 되었으나 리소스 조회 시 `403 Forbidden` 또는 접근 불가

**확인**:

```bash
# OIDC 로그인한 사용자의 group claim 확인
# (Headlamp UI → Settings → User Info에서 groups 확인 가능)

# ClusterRoleBinding 존재 확인
kubectl get clusterrolebinding | grep keycloak

# 권한 확인
kubectl auth can-i list pods --as-group=k8s-admins --as=test-user
```

**조치**:

1. Keycloak groups claim이 토큰에 포함되었는지 확인 (3-3 체크리스트 참조)
2. ClusterRoleBinding의 `subjects[].name`이 groups claim 값과 정확히 일치하는지 확인

```bash
# ClusterRoleBinding 수정 예시 (group name 불일치 시)
kubectl edit clusterrolebinding keycloak-k8s-admins
# subjects[0].name을 Keycloak group claim 값으로 수정
```

---

### OIDC Secret 미주입 (Pod CrashLoopBackOff)

**증상**: OIDC 설정 후 Headlamp Pod가 `CrashLoopBackOff` 또는 환경변수 없음 오류

**확인**:

```bash
# ExternalSecret 동기화 상태 확인
kubectl -n headlamp get externalsecret headlamp-oidc-secret -o jsonpath='{.status.conditions}'

# Secret 존재 확인
kubectl -n headlamp get secret headlamp-oidc-secret

# Pod 로그 확인
kubectl -n headlamp logs deployment/headlamp --previous
```

**조치**:

```bash
# ESO 재동기화 강제
kubectl -n headlamp annotate externalsecret headlamp-oidc-secret \
  force-sync=$(date +%s) --overwrite

# Secret 생성 확인 후 Pod 재시작
kubectl -n headlamp rollout restart deployment headlamp
```

---

## Verification Checklist

- [ ] `headlamp` namespace에 Pod Running
- [ ] `https://headlamp.127.0.0.1.nip.io/` → 200 응답
- [ ] ServiceAccount 토큰 로그인 성공 (Procedure 1 완료 시)
- [ ] OIDC 활성화 시: Keycloak 로그인 페이지로 리다이렉트됨
- [ ] OIDC 활성화 시: `headlamp-oidc-secret` ExternalSecret 동기화 완료
- [ ] OIDC 활성화 시: Keycloak groups claim → Kubernetes RBAC 적용 확인
- [ ] `secret/platform/headlamp` Vault 경로에 `oidc_client_secret` 저장됨

## Related Documents

- **Guide**: [`../07.guides/0004-headlamp-auth-oidc-guide.md`](../07.guides/0004-headlamp-auth-oidc-guide.md)
- **Operations**: [`../08.operations/0004-rollouts-notifications-headlamp-policy.md`](../08.operations/0004-rollouts-notifications-headlamp-policy.md)
- **ADR-0010**: [`../03.adr/0010-headlamp-replaces-dashboard.md`](../03.adr/0010-headlamp-replaces-dashboard.md)
- **Bootstrap Runbook**: [`../09.runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../09.runbooks/0004-rollouts-notifications-headlamp-runbook.md)
