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
├── 0002-argocd-helm-and-gitops-model.md
├── 0003-eso-vault-k8s-auth.md
├── 0006-cert-manager-mkcert-ca-issuer.md
├── 0008-istio-install-and-ingress-coexist.md
├── 0009-kiali-external-observability.md
├── 0011-argo-rollouts-progressive-delivery.md
├── 0012-argo-notifications-slack.md
├── 0013-stage-00-canonical-adapter-model.md
├── 0014-current-local-gitops-platform-contract.md
└── README.md
```

## How to Work in This Area

1. 결정의 상위 요구와 참조 구조를 `01.requirements/`, `02.architecture/requirements/`에서 확인한다.
2. 새 ADR은 `../../99.templates/adr.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/decisions/####-<short-title>.md`다.
3. 현재 구현과 상충하는 superseded/deprecated-only 결정은 `../../98.archive/README.md`에 Tombstone으로 이동한다.
4. `Accepted` ADR의 현재 런타임 값은 GitOps manifest, 정적 검증 스크립트, current baseline ADR과 일치해야 한다.
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
| [`./0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md) | ArgoCD Helm 설치와 GitOps 모델 결정 | Accepted | Current GitOps ownership model. |
| [`./0003-eso-vault-k8s-auth.md`](./0003-eso-vault-k8s-auth.md) | ESO + Vault Kubernetes Auth 시크릿 패턴 결정 | Accepted | Current secret synchronization pattern. |
| [`./0006-cert-manager-mkcert-ca-issuer.md`](./0006-cert-manager-mkcert-ca-issuer.md) | cert-manager + mkcert rootCA ClusterIssuer 도입 결정 | Accepted | Current TLS automation pattern for Headlamp, Kiali, and local ingress endpoints. |
| [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md) | Istio 설치와 ingress-nginx 공존 결정 | Accepted | Current mesh installation boundary. |
| [`./0009-kiali-external-observability.md`](./0009-kiali-external-observability.md) | Kiali + 외부 Prometheus/Grafana/Tempo 연동 결정 | Accepted | Current external observability contract through GitOps Service/EndpointSlice and NetworkPolicy. |
| [`./0011-argo-rollouts-progressive-delivery.md`](./0011-argo-rollouts-progressive-delivery.md) | Argo Rollouts 도입과 Rollouts Dashboard 결정 | Accepted | Current progressive delivery contract. |
| [`./0012-argo-notifications-slack.md`](./0012-argo-notifications-slack.md) | Argo Notifications Slack webhook 도입 결정 | Accepted | Current GitOps notification pattern. |
| [`./0013-stage-00-canonical-adapter-model.md`](./0013-stage-00-canonical-adapter-model.md) | Stage 00 canonical core, provider adapter, validation evidence ownership 결정 | Accepted | Current workspace AI Agent governance contract. |
| [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md) | Current local GitOps platform baseline and archive replacement decision | Accepted | Current Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer contract. |

## Related Documents

- [Architecture README](../README.md)
- [02.architecture/requirements](../requirements/README.md)
- [03.specs](../../03.specs/README.md)
- [05.operations/policies](../../05.operations/policies/README.md)
- [99.templates ADR Template](../../99.templates/adr.template.md)
- [Archive Index](../../98.archive/README.md)
