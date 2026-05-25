# traefik

> k3d 로컬 환경에서 ingress-nginx 뒤의 플랫폼 UI를 보조 노출하기 위한 Traefik dynamic config 예시를 관리한다.

## Overview

이 경로는 ArgoCD, Headlamp, Kiali, Argo Rollouts 같은 로컬 플랫폼 UI를 `hy-home.docker` 쪽 Traefik gateway에 연결할 때 참고하는 dynamic config를 담는다. 이 저장소의 canonical 배포 경로는 여전히 `gitops/`와 ArgoCD이며, `traefik/`은 k3d 로컬 접근성을 높이기 위한 보조 경로다.

Ingress NGINX는 2026-03-24 이후 upstream retired 상태이므로 cloud target에서는 이 경로를 확장하지 않는다. AWS/Azure 예시는 각각 ALB/Gateway API/AGC 같은 cloud-native ingress 경로로 분리하고, 이 디렉터리는 현재 로컬 k3d 계약을 설명하는 참조로 유지한다.

이 파일들은 ArgoCD가 동기화하는 Kubernetes manifest가 아니다. `hy-home.docker` Traefik dynamic config와 대조하거나 로컬 gateway에 반영할 때 쓰는 보조 참조로만 다룬다.

## Port Contract

- 외부 Traefik은 `websecure/443`에서 요청을 받고 Docker 네트워크에서 접근
  가능한 ingress-nginx `LoadBalancer` IP(`172.18.0.240:443`)로 전달한다.
- `infrastructure/bootstrap-local.sh`의 k3d host port fallback은 k3d
  serverlb host binding용이며, MetalLB가 할당한 ingress-nginx
  `LoadBalancer` IP 검증 경로와 혼동하지 않는다.
- `ARGOCD_FALLBACK_PORT`를 직접 지정하지 않으면 live TLS 검증은
  ingress-nginx `LoadBalancer` IP와 host/SNI resolve를 사용한다. 직접
  host port fallback을 검증할 때만 `ARGOCD_FALLBACK_PORT=8443`처럼 명시한다.
- 이 디렉터리의 파일은 외부 Traefik dynamic config 참조 복사본이므로,
  live gateway 반영은 `hy-home.docker` 운영 절차에서 별도로 승인하고
  증적을 남긴다.
- `CHECK_TRAEFIK_443=true bash infrastructure/tests/verify-ingress-tls.sh`가
  실패하고 Docker에 외부 Traefik gateway 컨테이너가 없다면, 이는 k3d
  GitOps desired state 실패가 아니라 `hy-home.docker` gateway runtime 또는
  dynamic config 반영이 아직 증명되지 않은 상태다.

## Traefik Route Inventory

이 표는 `traefik/*.yaml` dynamic config의 repo-static 계약이다. 모든 행은
ingress-nginx `LoadBalancer` backend를 가리키며, live gateway 반영 여부는
`hy-home.docker` 운영 절차에서 별도로 증명한다.

| Config | Router host | Backend URL | Boundary | Validation |
| --- | --- | --- | --- | --- |
| `argocd-k3d.yaml` | `argocd.127.0.0.1.nip.io` | `https://172.18.0.240:443` | Reference-only external Traefik dynamic config for local ArgoCD UI. | `validate-repo-quality-gates.sh` checks host, backend, TLS, and `websecure`. |
| `headlamp-k3d.yaml` | `headlamp.127.0.0.1.nip.io` | `https://172.18.0.240:443` | Reference-only external Traefik dynamic config for local Headlamp UI. | `validate-repo-quality-gates.sh` checks host, backend, TLS, and `websecure`. |
| `kiali-k3d.yaml` | `kiali.127.0.0.1.nip.io` | `https://172.18.0.240:443` | Reference-only external Traefik dynamic config for local Kiali UI. | `validate-repo-quality-gates.sh` checks host, backend, TLS, and `websecure`. |
| `rollouts-k3d.yaml` | `rollouts.127.0.0.1.nip.io` | `https://172.18.0.240:443` | Reference-only external Traefik dynamic config for local Argo Rollouts UI. | `validate-repo-quality-gates.sh` checks host, backend, TLS, and `websecure`. |

## Audience

이 README의 주요 독자:

- Operators
- Developers
- Documentation Writers
- AI Agents

## Scope

### In Scope

- k3d 로컬 플랫폼 UI용 Traefik dynamic config 예시
- `hy-home.docker` gateway와 연결되는 파일 배치 힌트
- ArgoCD, Headlamp, Kiali, Argo Rollouts 로컬 노출 경로 설명

### Out of Scope

- Kubernetes ingress controller 교체
- cloud 환경용 ALB, AGC, Gateway API 구현
- live cluster mutation 또는 Traefik 런타임 직접 변경
- 외부 TLS 인증서나 secret material 저장

## Structure

```text
traefik/
├── argocd-k3d.yaml      # ArgoCD UI 로컬 노출 dynamic config
├── headlamp-k3d.yaml    # Headlamp UI 로컬 노출 dynamic config
├── kiali-k3d.yaml       # Kiali UI 로컬 노출 dynamic config
├── rollouts-k3d.yaml    # Argo Rollouts UI 로컬 노출 dynamic config
└── README.md            # This file
```

## How to Work in This Area

1. 로컬 플랫폼 UI 노출이 필요한지 먼저 [gitops/README.md](../gitops/README.md)와 [infrastructure/README.md](../infrastructure/README.md)에서 현재 경계를 확인한다.
2. dynamic config를 수정할 때는 대상 서비스명, 포트, host rule이 현재 GitOps manifest와 일치하는지 확인한다.
3. cloud target 예시는 이 디렉터리에 추가하지 않고 [examples/README.md](../examples/README.md)와 각 cloud 문서에 둔다.
4. 변경 후에는 direct push 예시와 secret material이 들어가지 않았는지 repository quality gate로 확인한다.

## Link Basis

이 README의 링크 기준 위치는 `traefik/`다.

- 같은 폴더의 파일과 하위 경로는 현재 README 위치 기준 상대 링크로 연결한다.
- 상위 저장소 문서나 다른 stage 문서는 필요한 만큼 `../`로 올라가서 연결한다.
- 다른 README의 상대 링크를 그대로 복사하지 말고, 이 파일 위치 기준으로 다시 계산한다.

## Related Documents

- [Root README](../README.md)
- [GitOps README](../gitops/README.md)
- [Infrastructure README](../infrastructure/README.md)
- [Tech Stack Version Inventory](../docs/90.references/versions/tech-stack-version-inventory.md)
- [Ingress NGINX retirement statement](https://kubernetes.io/blog/2026/01/29/ingress-nginx-statement/)
