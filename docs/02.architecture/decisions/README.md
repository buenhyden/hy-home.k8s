# 02.architecture/decisions (ADR)

> 아키텍처 선택의 맥락, 대안, 결과를 보존하는 ADR stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

## Overview

이 경로는 중요한 기술/아키텍처 결정을 ADR로 기록하는 canonical stage다.
각 ADR은 하나의 결정, 그 맥락, 대안, 결과를 보존해 이후 Spec과 운영 정책이 같은 근거를 공유하게 한다.

## Audience

이 README의 주요 독자:

- Platform Architects
- Platform Engineers
- Operators
- AI Agents

## Scope

### In Scope

- 중요한 기술 결정 1건을 다루는 ADR
- 맥락, 결정, 비목표, 대안, 결과
- 관련 PRD/ARD/Spec/Plan/Operations 링크

### Out of Scope

- 상세 구현 설계
- 운영 절차와 장애 대응 단계
- 장문의 제품 배경 설명

## Structure

```text
02.architecture/decisions/
├── 0001-k3d-topology-and-network.md
├── 0002-argocd-helm-and-gitops-model.md
├── ...
├── 0012-argo-notifications-slack.md
└── README.md
```

## How to Work in This Area

1. 결정의 상위 요구와 참조 구조를 `01.requirements/`, `02.architecture/requirements/`에서 확인한다.
2. 새 ADR은 `../../99.templates/adr.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/decisions/####-<short-title>.md`다.
3. superseded 결정은 삭제하지 않고 상태와 대체 ADR/운영 기준을 명시한다.
4. `Accepted`는 결정 기록이 보존된다는 뜻이다. 현재 런타임 값은 README 인덱스의 `현재성/후속 기준`, GitOps manifest, 정적 검증 스크립트로 확인한다.
5. ADR이 구현 또는 운영 계약을 바꾸면 `03.specs/`, `05.operations/policies/` 링크를 갱신한다.

## Link Basis

이 README의 링크 기준 위치는 `docs/02.architecture/decisions/`다.

- 같은 폴더의 ADR 문서는 `./`로 시작한다.
- sibling ARD stage는 `../requirements/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../04.execution/`, `../../05.operations/`로 연결한다.
- 새 ADR의 실제 Markdown 링크는 최종 ADR 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

## Document Index

| 문서 | 설명 | 상태 | 현재성/후속 기준 |
| --- | --- | --- | --- |
| [`./0001-k3d-topology-and-network.md`](./0001-k3d-topology-and-network.md) | k3d 토폴로지와 외부 네트워크 기준 결정 | Accepted | Historical `172.19.x` 기록 포함. 현재 repo-backed 외부 서비스 계약은 `172.18.x` GitOps manifest와 `verify-contracts-static.sh`가 우선한다. |
| [`./0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md) | ArgoCD Helm 설치와 GitOps 모델 결정 | Accepted | Current GitOps ownership model. |
| [`./0003-eso-vault-k8s-auth.md`](./0003-eso-vault-k8s-auth.md) | ESO + Vault Kubernetes Auth 시크릿 패턴 결정 | Accepted | Current secret synchronization pattern. |
| [`./0004-external-services-endpoints-and-valkey-backend.md`](./0004-external-services-endpoints-and-valkey-backend.md) | 외부 서비스 접근 모델과 ArgoCD Valkey 백엔드 결정 | Accepted | Historical `172.19.x` 기록 포함. 현재 Service+EndpointSlice 값은 `gitops/platform/external-services/`가 우선한다. |
| [`./0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](./0005-wsl2-ha-baseline-and-external-endpoint-contract.md) | Valkey/TLS/최소권한 계약과 CI 정적 게이트 강화 + CD pull 모델 유지 결정 | Accepted | Historical `172.19.x` 기록 포함. 현재 static contract test는 `172.18.x` 계약을 검증한다. |
| [`./0006-cert-manager-mkcert-ca-issuer.md`](./0006-cert-manager-mkcert-ca-issuer.md) | cert-manager + mkcert rootCA ClusterIssuer 도입 결정 | Accepted | Current TLS automation pattern. Dashboard 언급은 역사적 플랫폼 확장 문맥으로 읽는다. |
| [`./0007-kubernetes-dashboard-v3.md`](./0007-kubernetes-dashboard-v3.md) | Kubernetes Dashboard v3 Helm 설치 및 노출 결정 | Superseded | Superseded by [`./0010-headlamp-replaces-dashboard.md`](./0010-headlamp-replaces-dashboard.md). Dashboard 기록은 삭제하지 않는다. |
| [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md) | Istio 설치와 ingress-nginx 공존 결정 | Accepted | Current mesh installation boundary. |
| [`./0009-kiali-external-observability.md`](./0009-kiali-external-observability.md) | Kiali + 외부 Prometheus/Grafana/Tempo 연동 결정 | Accepted | Historical `172.19.x` observability 주소 포함. 현재 observability EndpointSlice/CIDR는 GitOps manifest가 우선한다. |
| [`./0010-headlamp-replaces-dashboard.md`](./0010-headlamp-replaces-dashboard.md) | K8s Dashboard v3 제거와 Headlamp 교체 결정 | Accepted | Current cluster UI contract. |
| [`./0011-argo-rollouts-progressive-delivery.md`](./0011-argo-rollouts-progressive-delivery.md) | Argo Rollouts 도입과 Rollouts Dashboard 결정 | Accepted | Current progressive delivery contract. |
| [`./0012-argo-notifications-slack.md`](./0012-argo-notifications-slack.md) | Argo Notifications Slack webhook 도입 결정 | Accepted | Current GitOps notification pattern. |

## Related Documents

- [Architecture README](../README.md)
- [02.architecture/requirements](../requirements/README.md)
- [03.specs](../../03.specs/README.md)
- [05.operations/policies](../../05.operations/policies/README.md)
- [99.templates ADR Template](../../99.templates/adr.template.md)
