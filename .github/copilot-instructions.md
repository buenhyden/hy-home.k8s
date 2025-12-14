요약

- 이 저장소는 GitOps 기반 Kubernetes 인프라 저장소입니다 (ArgoCD App-of-Apps, Kustomize overlays).
- 주요 구성: apps/, clusters/, infrastructure/ — Kustomize로 구성된 매니페스트와 ArgoCD로 동기화됩니다.

빠른 아키텍처(한 줄)

- ArgoCD (clusters/docker-desktop/apps.yaml) -> App-of-Apps -> apps/\* 오버레이로 배포; Istio, Argo Rollouts, MetalLB, Kyverno 등 인프라 컴포넌트가 통합되어 있습니다.

핵심 규칙 및 컨벤션

- Kustomize 구조: 각 서비스는 `base/` + `overlays/<env>/` 패턴을 사용합니다. 예: [apps/backend-service-1/base/kustomization.yaml](apps/backend-service-1/base/kustomization.yaml).
- 이미지 태그: `overlays/<env>/kustomization.yaml`의 `images` 항목으로 이미지 태그를 고정합니다. Argo Image Updater가 이미지 태그를 관리합니다. 예: [apps/backend-service-1/overlays/dev/kustomization.yaml](apps/backend-service-1/overlays/dev/kustomization.yaml).
- ArgoCD entry: 클러스터 롤아웃과 전체 동기화는 [clusters/docker-desktop/apps.yaml](clusters/docker-desktop/apps.yaml)에 정의된 root application을 통해 제어됩니다.
- Canary 배포: Argo Rollouts를 사용하고 Istio VirtualService로 트래픽 분할합니다. 예: [apps/backend-service-1/base/rollout.yaml](apps/backend-service-1/base/rollout.yaml).
- 보안 정책: Kyverno가 `:latest` 태그 사용 및 루트 사용자 실행을 금지합니다. 정책 예: [infrastructure/security/kyverno/policies.yaml](infrastructure/security/kyverno/policies.yaml).
- Sealed Secrets / Cert-Manager: 클러스터에서 개인키로만 복호화되므로 `sealed-secrets.yaml` 등 암호화된 시크릿을 Git에 저장합니다.

개발자/Agent가 알아야 할 작업 흐름

- 클러스터 구성(로컬 테스트): `kind`를 사용해 Kind 클러스터 생성 후 하이브리드 네트워크 라우트를 추가합니다 (README의 '하이브리드 네트워크' 섹션 참조).
- ArgoCD Bootstrap: `kubectl -n argocd apply -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml`로 설치.
- ArgoCD UI/CLI로 애플리케이션 동기화: `argocd app sync <name>` 또는 `kubectl apply` 후 ArgoCD에서 자동 동기화.
- 이미지 배포: 이미지 빌드/푸시 후 `overlays/*/kustomization.yaml`에서 `images:`로 태그를 업데이트하거나 Argo Image Updater를 통해 Git에 쓰기(Write-back)합니다.
- 디버깅: `kubectl get rollouts -n <ns>` 및 `kubectl argo rollouts get <rollout>` 또는 `kubectl rollout status`를 사용합니다. Istio 문제는 `istioctl analyze`로 확인.

중요한 통합 지점

- 외부 서비스: PostgreSQL/Redis/Kafka/OpenSearch는 `infrastructure/external-services/*`에서 정의되며, 일부는 ServiceEntry 또는 Headless Service로 Kind 네트워크와 연결됩니다.
- MetalLB: 로컬 LoadBalancer 제공자 (상태 및 IP 풀은 `infrastructure/controllers/metallb/pool-config.yaml` 등 참조).
- Argo Image Updater: [clusters/docker-desktop/applications/\*](clusters/docker-desktop/applications)에 적용된 주석(annotation)으로 동작합니다. 예: `argocd-image-updater.argoproj.io/image-list`.

패턴 & 금지 사항 (구체적)

- 금지: `:latest` 이미지를 사용하지 마세요 — Kyverno가 enforcement 모드로 차단합니다.
- 패턴: 모든 애플리케이션은 `runAsNonRoot`를 적용해야 합니다 (Pod securityContext), 시스템 네임스페이스는 Kyverno 예외로 지정되어 있습니다.
- 배포 단위: 각 애플리케이션은 `kustomize` base를 사용하는 단일 앱으로 구성되며, 환경별 override는 `overlays/<env>`에서 처리됩니다.

참고용 파일들(가장 유용한 예시)

- Root Application: [clusters/docker-desktop/apps.yaml](clusters/docker-desktop/apps.yaml)
- Argo Application 예: [clusters/docker-desktop/applications/backend-1.yaml](clusters/docker-desktop/applications/backend-1.yaml)
- Rollout 예: [apps/backend-service-1/base/rollout.yaml](apps/backend-service-1/base/rollout.yaml)
- Kustomize overlay: [apps/backend-service-1/overlays/dev/kustomization.yaml](apps/backend-service-1/overlays/dev/kustomization.yaml)
- Kyverno 정책: [infrastructure/security/kyverno/policies.yaml](infrastructure/security/kyverno/policies.yaml)
- 추가 예시 및 스크립트: [.github/copilot-additional.md](.github/copilot-additional.md)
- CI/CD workflow example: [.github/workflows/ci-cd-unified.yml](.github/workflows/ci-cd-unified.yml)
- Kind template: [kind-config.yaml](kind-config.yaml)
- Credentials guide: [docs/credentials.md](docs/credentials.md)

간단한 예시 변경(에이전트 작업 흐름)

1. 새 이미지 빌드 및 푸시: `docker build -t <registry>/service-1:v1.2.3 .` && `docker push <registry>/service-1:v1.2.3`
2. `overlays/dev/kustomization.yaml`의 images 섹션 업데이트 (혹은 Argo Image Updater에 푸시 및 Git write-back 위임).
3. ArgoCD에서 앱 동기화: `argocd app sync backend-service-1` 또는 `kubectl -n argocd rollout restart application backend-service-1` (대체 커맨드).

검증/테스트 접근

- 클러스터 상태: `kubectl get pods -A`, `kubectl get svc -A`, `kubectl get rollouts -A`.
- 로그: `kubectl logs -n <ns> <pod>`에서 컨테이너별 로그 확인. Istio 사이드카 로그는 pod에서 동일하게 확인.
- 정책 위반: Kyverno 이벤트 확인: `kubectl get events -n kyverno`.

요청 & 피드백

- 변경 사항이 복잡하거나 다른 외부 레포(예: 이미지 레포)와의 연동이 필요하면 알려주세요. 더 구체적인 CI/CD/개발자 가이드(빌드 스크립트, 이미지 레포 자격 증명 등)를 추가로 작성할 수 있습니다.
