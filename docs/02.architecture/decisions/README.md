---
title: "02.architecture/decisions (ADR)"
version: "0.7.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-10-05"
layer: "architecture"
---
# 02.architecture/decisions (ADR)

> 아키텍처 선택의 맥락, 대안, 결과를 보존하는 ADR stage다.

> [!NOTE]
> 이 stage에서 이루어지는 모든 AI 에이전트 작업은 [Agent Governance Hub](../../../.agents/README.md)를 따른다.

## Overview

이 경로는 중요한 기술/아키텍처 결정을 ADR로 기록하는 canonical stage다.
각 ADR은 하나의 결정, 그 맥락, 대안, 결과를 보존해 이후 Spec과 운영 정책이 같은 근거를 공유하게 한다.

### Collection Readers

이 README의 주요 독자:

- Platform Architects
- Platform Engineers
- Operators
- AI Agents

## Scope

### In Scope

- 중요한 기술 결정 1건을 다루는 ADR
- 맥락, 결정, 비목표, 대안, 결과
- 관련 PRD/AD/Spec/Plan/Operations 링크

### Out of Scope

- 상세 구현 설계
- 운영 절차와 장애 대응 단계
- 장문의 제품 배경 설명

## Structure

각 ADR의 승인·대체 상태는 해당 문서의 frontmatter가 소유한다. 이 표는 결정의 역할과 후속 경로를 안내한다.

| Path | Purpose |
| --- | --- |
|   [`./0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md) | ArgoCD Helm 설치와 GitOps 모델 결정 |
|   [`./0006-cert-manager-mkcert-ca-issuer.md`](./0006-cert-manager-mkcert-ca-issuer.md) | cert-manager + mkcert rootCA ClusterIssuer 도입 결정 |
|   [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md) | Istio 설치와 ingress-nginx 공존 결정 |
|   [`./0009-kiali-external-observability.md`](./0009-kiali-external-observability.md) | Kiali + 외부 Prometheus/Grafana/Tempo 연동 결정 |
|   [`./0011-argo-rollouts-progressive-delivery.md`](./0011-argo-rollouts-progressive-delivery.md) | Argo Rollouts 도입과 Rollouts Dashboard 결정 |
|   [`./0012-argo-notifications-slack.md`](./0012-argo-notifications-slack.md) | Argo Notifications Slack webhook 도입 결정 |
|   [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md) | Current local GitOps platform baseline and archive replacement decision |
|   [`./0026-argo-cd-source-integrity-non-adoption.md`](./0026-argo-cd-source-integrity-non-adoption.md)               | Argo CD source-integrity 미채택 결정                                  |
|   [`./0028-pod-security-admission-per-namespace-adoption.md`](./0028-pod-security-admission-per-namespace-adoption.md) | Pod Security Admission 네임스페이스별 도입 결정 |
|   [`./0029-mutable-target-revision-retention.md`](./0029-mutable-target-revision-retention.md) | 가변 targetRevision 유지 결정 |
|   [`./0030-authority-first-sdlc-and-agent-governance-convergence.md`](./0030-authority-first-sdlc-and-agent-governance-convergence.md) | Authority-first SDLC document, agent governance, Archive, template, and script convergence decision |
|   [`./0031-current-corpus-retention-and-validation-ownership.md`](./0031-current-corpus-retention-and-validation-ownership.md) | Current corpus retention, package-local execution lineage, and validation routing ownership decision |
|   [`./0033-common-document-contract-v9.md`](./0033-common-document-contract-v9.md) | Common document contract v9 and governed router envelope decision |
|   [`./0036-common-knowledge-and-prompt-surfaces.md`](./0036-common-knowledge-and-prompt-surfaces.md) | Common knowledge and prompt surface adoption |
|   [`./0037-kiali-operator-installation.md`](./0037-kiali-operator-installation.md) | Kiali operator 설치 결정 |
|   [`./0039-unit-archive-retention-and-citation-table.md`](./0039-unit-archive-retention-and-citation-table.md) | Unit archive retention and citation table decision |
|   [`./0040-archive-reappraisal-and-verifiable-sources.md`](./0040-archive-reappraisal-and-verifiable-sources.md) | Archive reappraisal and verifiable sources decision |
|   [`./0041-openbao-secret-backend.md`](./0041-openbao-secret-backend.md) | OpenBao 런타임 시크릿 backend 전환 결정 |
|   [`./0042-linux-server-single-host-baseline.md`](./0042-linux-server-single-host-baseline.md) | Linux server single-host baseline 결정 |
|   [`./0043-dedicated-k8s-ingress-router.md`](./0043-dedicated-k8s-ingress-router.md) | Dedicated Kubernetes ingress router 결정 |
|   [`./0044-stateful-data-stores-stay-external.md`](./0044-stateful-data-stores-stay-external.md) | Stateful data store placement 결정 |
|   [`./0045-in-cluster-telemetry-collection.md`](./0045-in-cluster-telemetry-collection.md) | In-cluster telemetry collection 결정 |
|   [`./0046-external-services-over-host-addresses.md`](./0046-external-services-over-host-addresses.md) | External service transport 결정 |
|   [`./0047-agent-contract-and-resource-ownership.md`](./0047-agent-contract-and-resource-ownership.md) | Agent 계약과 resource 소유 경계의 한정 개정 |

## Usage

1. 결정의 상위 요구와 참조 구조를 `01.requirements/`, `../descriptions/`에서 확인한다.
2. 새 ADR은 `../../99.templates/templates/architecture/decision.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/decisions/####-<short-title>.md`다.
3. Superseded ADR은 predecessor/successor를 상호 연결한다. [ADR-0040](./0040-archive-reappraisal-and-verifiable-sources.md)에 따라 다른 family와 같이 `98.archive/superseded/`로 옮기고 이 log는 predecessor를 identifier로 명명한다. 처분이 승인된 대체 ADR은 이 log를 떠나 Archive에 보존한다. ADR-0039는 ADR-0040에 의해 대체되었지만 별도 처분 승인 전까지 이 log에 남는다. ADR-0013, ADR-0015부터 ADR-0025, ADR-0027, ADR-0032, ADR-0034, ADR-0035, ADR-0038은 [Archive index](../../98.archive/README.md)의 Retention Catalog가 명명한다. redirect나 본문 복제본을 만들지 않는다.
4. `Accepted` ADR의 현재 런타임 값은 GitOps manifest, 정적 검증 스크립트, current baseline ADR과 일치해야 한다.
5. ADR이 구현 또는 운영 계약을 바꾸면 `03.specs/`, `05.operations/policies/` 링크를 갱신한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/decisions/`다.

- 같은 폴더의 ADR 문서는 `./`로 시작한다.
- sibling AD stage는 `../descriptions/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../05.operations/`로 연결한다. Retired Stage 04 execution route는 current link target으로 사용하지 않는다.
- 새 ADR의 실제 Markdown 링크는 최종 ADR 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

## Related Documents

- [Architecture README](../README.md)
- [02.architecture/descriptions](../descriptions/README.md)
- [03.specs](../../03.specs/README.md)
- [05.operations/policies](../../05.operations/policies/README.md)
- [99.templates ADR Template](../../99.templates/templates/architecture/decision.template.md)
- [Archive Index](../../98.archive/README.md)
