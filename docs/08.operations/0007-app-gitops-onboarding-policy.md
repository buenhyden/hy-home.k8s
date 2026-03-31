# 앱 GitOps 온보딩 정책

## 문서 유형

`운영 정책 — WSL2 k3d/k3s GitOps 앱 온보딩`

## 목적

이 문서는 `hy-home.k8s` 클러스터에 새로운 애플리케이션을 온보딩할 때 따라야 하는
플랫폼 운영 정책을 정의한다.

---

## 1. 배포 리소스 정책

### 1-1. Rollout 필수 (Deployment 금지)

apps namespace의 모든 워크로드는 `argoproj.io/v1alpha1/Rollout`을 사용해야 한다.
Deployment는 `appproject-apps` whitelist에 포함되어 있으나, 플랫폼 정책상 허용하지 않는다.

**이유**: canary 전략으로 점진적 트래픽 전환과 자동 rollback을 보장하기 위함.

```yaml
# 올바른 패턴
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: <appname>
  namespace: apps
spec:
  strategy:
    canary:
      steps:
        - setWeight: 20
        - analysis: ...
        - pause: { duration: 30s }
        - setWeight: 60
        - pause: { duration: 30s }
        - setWeight: 100
```

### 1-2. AnalysisTemplate 필수

모든 Rollout은 canary 단계에서 AnalysisTemplate을 참조해야 한다.

- **Prometheus 주소**: `http://prometheus-external.platform.svc.cluster.local:9090`
- **기본 측정 지표**: `kube_pod_container_status_restarts_total` (컨테이너 재시작 횟수)
- **측정 주기**: 30s, failureLimit: 1

### 1-3. 이미지 태그

| 항목       | 정책                                                |
| ---------- | --------------------------------------------------- |
| 태그       | 고정 버전 태그 사용 (`v1.0.0`, SHA) — `latest` 금지 |
| 레지스트리 | GitHub Container Registry(`ghcr.io`) 권장           |
| 가시성     | Public 패키지로 설정 (홈랩 환경)                    |

---

## 2. 네트워킹 정책

### 2-1. Istio 포트 명명 규칙

Service의 port 이름은 반드시 `http-` 접두사를 포함해야 한다.

```yaml
# 올바른 패턴
ports:
  - name: http-<appname>    # ← http- 접두사 필수
    port: 8080

# 잘못된 패턴
ports:
  - name: web               # ← Istio가 프로토콜을 감지하지 못함
    port: 8080
```

**이유**: Istio가 HTTP 프로토콜로 자동 인식하여 올바른 메트릭과 트레이싱을 수집한다.

### 2-2. Ingress 설정

```yaml
# 필수 어노테이션
annotations:
  cert-manager.io/cluster-issuer: mkcert-ca-issuer
  nginx.ingress.kubernetes.io/ssl-redirect: 'true'

# 필수 설정
spec:
  ingressClassName: nginx # ← nginx 고정
  rules:
    - host: <appname>.127.0.0.1.nip.io # ← nip.io 패턴 고정
```

### 2-3. Traefik 연동 필수

모든 `*.127.0.0.1.nip.io` 도메인은 외부 Traefik router 설정이 있어야 한다.

- **위치**: `hy-home.docker/infra/01-gateway/traefik/dynamic/<appname>-k3d.yaml`
- **패턴**: `examples/sample-app/traefik-k3d.yaml.example` 참조

---

## 3. 보안 정책

### 3-1. Istio mTLS

`apps` namespace에 PeerAuthentication STRICT가 적용되어 있다.

- **신규 앱**: 별도 PeerAuthentication 불필요 (namespace 정책 자동 적용)
- **전제**: Pod에 Istio sidecar가 주입되어야 함 (`apps` namespace에 `istio-injection: enabled` 라벨)

### 3-2. NetworkPolicy

현재 `apps` namespace 전체에 egress 정책이 적용된다:

- postgres (172.18.0.15:15432, 15433) egress 허용
- kube-dns egress 허용
- Istiod egress 허용

**신규 외부 서비스 연결 필요 시**: `gitops/platform/network-policies/apps-egress.yaml`에 egress 규칙을 추가하고 Platform 팀(운영자 본인)에 변경 요청한다.

### 3-3. 시크릿 관리

| 항목            | 정책                                                 |
| --------------- | ---------------------------------------------------- |
| 시크릿 저장     | Vault (`secret/apps/<appname>/config`)               |
| k8s Secret 생성 | ExternalSecret(ESO)만 사용, 직접 Secret 생성 금지    |
| 환경변수        | `envFrom.secretRef` 사용 (개별 `env.valueFrom` 지양) |
| Vault 경로 규칙 | `secret/apps/<appname>/config`                       |

---

## 4. GitOps 워크플로우 정책

### 4-1. 파일 배치 규칙

```
gitops/workloads/<appname>/          ← apps-generator 자동 감지
├── kustomization.yaml               ← 진입점 (필수)
├── rollout.yaml                     ← 배포 (필수)
├── service.yaml                     ← 서비스 (필수)
├── ingress.yaml                     ← 외부 접근 (필수)
├── analysis-template.yaml           ← canary 분석 (필수)
└── external-secret.yaml             ← Vault 연동 (선택)
```

### 4-2. 네이밍 규칙

| 항목        | 규칙                           | 예시                        |
| ----------- | ------------------------------ | --------------------------- |
| `<appname>` | 소문자, 하이픈 구분            | `my-api`                    |
| 도메인      | `<appname>.127.0.0.1.nip.io`   | `my-api.127.0.0.1.nip.io`   |
| TLS Secret  | `<appname>-tls`                | `my-api-tls`                |
| Vault 경로  | `secret/apps/<appname>/config` | `secret/apps/my-api/config` |

### 4-3. 커밋 메시지 규칙

```
feat: add <appname> to GitOps         ← 최초 온보딩
chore: bump <appname> to v1.1.0       ← 이미지 업데이트
fix: fix <appname> config             ← 설정 수정
```

### 4-4. 금지 사항

- `kubectl apply`로 직접 클러스터 변경 (AppProject 변경, 긴급 hotfix 제외)
- `latest` 태그 이미지 사용
- Git 없이 ArgoCD UI에서만 변경
- `namespace: default` 사용 (반드시 `apps` 또는 플랫폼 지정 namespace)

---

## 5. 온보딩 체크리스트

새 앱 온보딩 전 아래 항목을 확인한다:

```
[ ] GitHub 레포에 CI workflow 추가 (ghcr.io push)
[ ] ghcr.io 패키지를 Public으로 설정
[ ] examples/sample-app/ 복사 후 플레이스홀더 교체
[ ] rollout.yaml: 고정 이미지 태그, AnalysisTemplate 참조
[ ] service.yaml: http- 포트 명명 규칙 준수
[ ] ingress.yaml: ingressClassName=nginx, mkcert-ca-issuer
[ ] analysis-template.yaml: <appname> 교체 완료
[ ] Traefik dynamic config 추가 (hy-home.docker 레포)
[ ] (선택) Vault 시크릿 등록 + 정책 갱신 + external-secret.yaml 활성화
[ ] git commit & push
[ ] ArgoCD Application Synced / Healthy 확인
[ ] Pod 2/2 Running 확인 (Istio sidecar 주입)
[ ] https://<appname>.127.0.0.1.nip.io 접속 확인
```

---

## Related Documents

- **Guide**: [`../07.guides/0008-github-app-gitops-onboarding-guide.md`](../07.guides/0008-github-app-gitops-onboarding-guide.md)
- **Runbook**: [`../09.runbooks/0010-github-app-gitops-onboarding-runbook.md`](../09.runbooks/0010-github-app-gitops-onboarding-runbook.md)
- **예시 템플릿**: [`../../examples/sample-app/`](../../examples/sample-app/)
- **참조 구현**: [`../../gitops/workloads/adminer/`](../../gitops/workloads/adminer/)
- **AppProject**: [`../../gitops/clusters/local/appproject-apps.yaml`](../../gitops/clusters/local/appproject-apps.yaml)
- **NetworkPolicy**: [`../../gitops/platform/network-policies/apps-egress.yaml`](../../gitops/platform/network-policies/apps-egress.yaml)
