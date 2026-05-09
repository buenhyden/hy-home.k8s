# Argo Rollouts, Notifications & Headlamp Runbook

## Runbook Type

`WSL2 k3d/k3s 운영 핫픽스 및 부트스트랩`

## Overview (KR)

이 런북은 Argo Rollouts, Argo Notifications(Slack), Headlamp의 초기 부트스트랩, 복구, 검증 절차를 제공한다.

## When to Use

- Rollouts Controller가 기동하지 않거나 CRD가 없을 때
- Notifications Slack 알림이 전달되지 않을 때
- Headlamp에 접근 불가 (404/502) 상황
- 초기 플랫폼 부트스트랩 후 신규 컴포넌트 검증 시

---

## Procedure 1: Vault Notifications Secret 준비 (최초 1회)

```bash
# Slack Bot Token 준비 후 Vault에 저장
export VAULT_TOKEN='<redacted>'
# external secret operation; human-approved bootstrap only
vault kv put secret/platform/notifications \
  slack_token="xoxb-your-slack-bot-token"

# 확인
vault kv get secret/platform/notifications
```

> **주의**: token은 반드시 Vault에 저장. 평문 커밋 금지.

---

## Procedure 2: ArgoCD Notifications 활성화 확인

```bash
# notifications controller pod 확인
kubectl -n argocd get pods | grep notification

# notifications-cm 확인
kubectl -n argocd get cm argocd-notifications-cm -o yaml | head -20

# notifications-secret (ESO 동기화 확인)
kubectl -n argocd get secret argocd-notifications-secret 2>/dev/null && echo "OK" || echo "Missing"

# notifications controller 로그 (Slack 전송 확인)
kubectl -n argocd logs deploy/argocd-notifications-controller --tail=100 | grep -i 'slack\|sent\|error'
```

### 복구: ESO 재동기화

```bash
kubectl -n argocd annotate externalsecret argocd-notifications-secret \
  force-sync=$(date +%s) --overwrite
```

---

## Procedure 3: Argo Rollouts 상태 확인

```bash
# Rollouts controller 및 dashboard pod 확인
kubectl -n argo-rollouts get pods

# CRD 확인
kubectl get crd | grep argoproj.io

# 전체 Rollout 목록
kubectl argo rollouts list rollouts --all-namespaces

# Rollout 상세 상태
kubectl argo rollouts get rollout <name> -n <namespace> --watch
```

### Rollout 수동 프로모션

```bash
# canary 다음 단계로 진행
kubectl argo rollouts promote <rollout-name> -n <namespace>

# 전체 즉시 프로모션
kubectl argo rollouts promote <rollout-name> -n <namespace> --full

# 롤백 (이전 버전으로)
kubectl argo rollouts undo <rollout-name> -n <namespace>
```

---

## Procedure 4: Headlamp 접근 검증

```bash
# Pod 및 Ingress 상태 확인
kubectl -n headlamp get pods,ingress,svc

# TLS Secret 확인 (cert-manager 발급)
kubectl -n headlamp get certificate headlamp-tls 2>/dev/null || \
kubectl -n headlamp get secret headlamp-tls 2>/dev/null

# HTTP 응답 확인
curl -ksS -o /dev/null -w '%{http_code}' https://headlamp.127.0.0.1.nip.io/
```

### 복구: Headlamp 재시작

```bash
kubectl -n headlamp rollout restart deployment headlamp
```

### Traefik artifact 적용 확인

```bash
# Traefik 컨테이너에서 headlamp-k3d 라우터 상태 확인
# (Traefik 관리 UI 또는 API에서 확인)
# Kubernetes 사이드에서는 ingress 상태만 확인 가능
kubectl -n headlamp get ingress headlamp -o yaml
```

---

## Procedure 5: Rollouts Dashboard 접근 검증

```bash
# Pod 및 Ingress 상태
kubectl -n argo-rollouts get pods
kubectl -n argo-rollouts get ingress

# HTTP 응답 확인
curl -ksS -o /dev/null -w '%{http_code}' https://rollouts.127.0.0.1.nip.io/
```

---

## Verification Checklist

- [ ] `argo-rollouts` namespace에 controller + dashboard Pod Running
- [ ] `argo-rollouts` Rollout CRD 존재
- [ ] `argocd-notifications-controller` Pod Running
- [ ] `argocd-notifications-secret` ESO 동기화 완료
- [ ] `argocd-notifications-cm` ConfigMap 존재
- [ ] `headlamp` namespace에 Pod Running, Ingress Ready
- [ ] `https://headlamp.127.0.0.1.nip.io/` → 200 응답
- [ ] `https://rollouts.127.0.0.1.nip.io/` → 200 응답
- [ ] Traefik artifact (`headlamp-k3d.yaml`, `rollouts-k3d.yaml`) 외부 Traefik 레포에 적용됨

## Troubleshooting Signatures

- `Error syncing application: slack token is empty` → Vault secret 미등록 또는 ESO 미동기화
- Headlamp 404 → ingress-nginx 미시작 또는 TLS secret 미발급
- Rollouts `CRD not found` → `installCRDs: true` 확인 또는 ArgoCD sync wave 순서 문제
- Rollouts Dashboard 502 → dashboard Pod 미기동, service port 3100 확인

## Related Documents

- **Operations**: [`../08.operations/0004-rollouts-notifications-headlamp-policy.md`](../08.operations/0004-rollouts-notifications-headlamp-policy.md)
- **ADR-0010**: [`../03.adr/0010-headlamp-replaces-dashboard.md`](../03.adr/0010-headlamp-replaces-dashboard.md)
- **ADR-0011**: [`../03.adr/0011-argo-rollouts-progressive-delivery.md`](../03.adr/0011-argo-rollouts-progressive-delivery.md)
- **ADR-0012**: [`../03.adr/0012-argo-notifications-slack.md`](../03.adr/0012-argo-notifications-slack.md)
