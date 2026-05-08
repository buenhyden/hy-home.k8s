# 03. ADR (Architecture Decision Records)

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../00.agent-governance/README.md).

## 목적

이 폴더는 아키텍처 결정 기록(Architecture Decision Record, ADR)을 저장한다. ADR은 중요한 기술·아키텍처 결정 1건을 1문서로 기록한다.

## 포함할 내용

- 맥락(Context)
- 결정(Decision)
- 비목표(Non-goals)
- 대안(Alternatives)
- 결과(Consequences)
- 관련 PRD/ARD/Spec/Plan/기타 ADR 링크

## 포함하지 말아야 할 내용

- 상세 구현 설계
- 운영 절차
- 장문의 제품 배경 설명

## Agent 관련 ADR 예시

- 모델 선택
- Tool Gating
- Guardrail 전략
- Planner-Executor 채택 여부
- Fallback 모델 정책

## Templates

- `../99.templates/adr.template.md`

## 문서 인덱스

| 문서                                                                                                                   | 설명                                                                                                             | 상태     | 최종 수정  |
| ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | -------- | ---------- |
| [`0001-k3d-topology-and-network.md`](./0001-k3d-topology-and-network.md)                                               | k3d 토폴로지와 외부 네트워크 기준 결정                                                                           | Accepted | 2026-05-09 |
| [`0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md)                                       | ArgoCD Helm 설치와 GitOps 모델 결정                                                                              | Accepted | 2026-03-27 |
| [`0003-eso-vault-k8s-auth.md`](./0003-eso-vault-k8s-auth.md)                                                           | ESO + Vault Kubernetes Auth 시크릿 패턴 결정                                                                     | Accepted | 2026-03-27 |
| [`0004-external-services-endpoints-and-valkey-backend.md`](./0004-external-services-endpoints-and-valkey-backend.md)   | 외부 서비스 접근 모델(PostgreSQL EndpointSlice, Valkey ExternalName, Vault 외부 URL)과 ArgoCD Valkey 백엔드 결정 | Accepted | 2026-05-09 |
| [`0005-wsl2-ha-baseline-and-external-endpoint-contract.md`](./0005-wsl2-ha-baseline-and-external-endpoint-contract.md) | Valkey/TLS/최소권한 계약과 CI 정적 게이트 강화 + CD pull 모델 유지 결정을 기록한 ADR                             | Accepted | 2026-05-09 |
| [`0006-cert-manager-mkcert-ca-issuer.md`](./0006-cert-manager-mkcert-ca-issuer.md)                                     | cert-manager + mkcert rootCA ClusterIssuer 도입 결정                                                             | Accepted | 2026-03-29 |
| [`0007-kubernetes-dashboard-v3.md`](./0007-kubernetes-dashboard-v3.md)                                                 | Kubernetes Dashboard v3 Helm 설치 및 k8s-dashboard.127.0.0.1.nip.io 노출 결정                                    | Superseded | 2026-05-09 |
| [`0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md)                             | Istio v1.25.x 설치(IngressGateway 비활성, ingress-nginx 공존) 결정                                               | Accepted | 2026-05-09 |
| [`0009-kiali-external-observability.md`](./0009-kiali-external-observability.md)                                       | Kiali v2.6.x + 외부 Prometheus/Grafana/Tempo 연동 결정                                                           | Accepted | 2026-05-09 |
| [`0010-headlamp-replaces-dashboard.md`](./0010-headlamp-replaces-dashboard.md)                                         | K8s Dashboard v3 제거, Headlamp v0.41.0 교체 결정 (chart repo 비활성화, Kong 의존성 제거)                        | Accepted | 2026-03-30 |
| [`0011-argo-rollouts-progressive-delivery.md`](./0011-argo-rollouts-progressive-delivery.md)                           | Argo Rollouts v1.9.0 도입, Rollouts Dashboard 포함, 수동 promotion 기본 결정                                     | Accepted | 2026-05-09 |
| [`0012-argo-notifications-slack.md`](./0012-argo-notifications-slack.md)                                               | Argo Notifications Slack webhook 도입 (ArgoCD Helm 내장 컨트롤러 활성화, ESO로 token 관리)                       | Accepted | 2026-03-30 |

## 관련 폴더

- `02.ard/`: ADR의 상위 아키텍처 참조
- `04.specs/`: ADR 결정을 반영하는 구현 명세
- `08.operations/`: 운영 정책으로 이어지는 결정 근거

## 예시

- UI 전환 결정은 `0010-headlamp-replaces-dashboard.md`처럼 superseded 대상과 새 운영 기준을 함께 기록한다.
