---
title: "02.architecture/decisions (ADR)"
version: "0.12.0"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-13"
layer: "architecture"
---

# 02.architecture/decisions (ADR)

## Stage Responsibility

### Purpose and Readers

> 아키텍처 선택의 맥락, 대안, 결과를 보존하는 ADR stage다.

이 경로는 중요한 기술/아키텍처 결정을 ADR로 기록하는 canonical stage다.
각 ADR은 하나의 결정, 그 맥락, 대안, 결과를 보존해 이후 Spec과 운영 정책이 같은 근거를 공유하게 한다.

#### Collection Readers

이 README의 주요 독자:

- Platform Architects
- Platform Engineers
- Operators

### Inputs and Outputs

#### In Scope

- 중요한 기술 결정 1건을 다루는 ADR
- 맥락, 결정, 비목표, 대안, 결과
- 관련 Requirement Package/AD/Spec/Plan/Operations 링크

#### Out of Scope

- 상세 구현 설계
- 운영 절차와 장애 대응 단계
- 장문의 제품 배경 설명

## Contents

### Current Items

각 ADR의 승인·대체 상태는 해당 문서의 frontmatter가 소유한다. 이 표는 결정의 역할과 후속 경로를 안내한다.

| Path | Purpose |
| --- | --- |
| [`./0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md) | ArgoCD Helm 설치와 GitOps 모델 결정 |
| [`./0006-cert-manager-mkcert-ca-issuer.md`](./0006-cert-manager-mkcert-ca-issuer.md) | cert-manager + mkcert rootCA ClusterIssuer 도입 결정 |
| [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md) | Istio 설치와 ingress controller 공존 결정(현재 controller는 Traefik, ADR-0050) |
| [`./0009-kiali-external-observability.md`](./0009-kiali-external-observability.md) | Kiali + 외부 Prometheus/Grafana/Tempo 연동 결정 |
| [`./0011-argo-rollouts-progressive-delivery.md`](./0011-argo-rollouts-progressive-delivery.md) | Argo Rollouts 도입과 Rollouts Dashboard 결정 |
| [`./0012-argo-notifications-slack.md`](./0012-argo-notifications-slack.md) | Argo Notifications Slack(app token) 알림 도입 결정 |
| [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md) | Current local GitOps platform baseline and agent application of the current authority chain |
| [`./0026-argo-cd-source-integrity-non-adoption.md`](./0026-argo-cd-source-integrity-non-adoption.md) | Argo CD source-integrity 미채택 결정 |
| [`./0028-pod-security-admission-per-namespace-adoption.md`](./0028-pod-security-admission-per-namespace-adoption.md) | Pod Security Admission 네임스페이스별 도입 결정 |
| [`./0029-mutable-target-revision-retention.md`](./0029-mutable-target-revision-retention.md) | 가변 targetRevision 유지 결정 |
| [`./0030-authority-first-sdlc-and-agent-governance-convergence.md`](./0030-authority-first-sdlc-and-agent-governance-convergence.md) | Authority-first SDLC document, agent governance, Archive, template, and script convergence decision |
| [`./0031-current-corpus-retention-and-validation-ownership.md`](./0031-current-corpus-retention-and-validation-ownership.md) | Current corpus retention, package-local execution lineage, and validation routing ownership decision |
| [`./0033-common-document-contract-v9.md`](./0033-common-document-contract-v9.md) | Common document contract v9 and governed router envelope decision |
| [`./0036-common-knowledge-and-prompt-surfaces.md`](./0036-common-knowledge-and-prompt-surfaces.md) | Common knowledge and prompt surface adoption |
| [`./0037-kiali-operator-installation.md`](./0037-kiali-operator-installation.md) | Kiali operator 설치 결정 |
| [`./0041-openbao-secret-backend.md`](./0041-openbao-secret-backend.md) | OpenBao 런타임 시크릿 backend 전환 결정 |
| [`./0042-linux-server-single-host-baseline.md`](./0042-linux-server-single-host-baseline.md) | Linux server single-host baseline 결정 |
| [`./0043-dedicated-k8s-ingress-router.md`](./0043-dedicated-k8s-ingress-router.md) | Dedicated Kubernetes ingress router 결정 |
| [`./0044-stateful-data-stores-stay-external.md`](./0044-stateful-data-stores-stay-external.md) | Stateful data store placement 결정 |
| [`./0045-in-cluster-telemetry-collection.md`](./0045-in-cluster-telemetry-collection.md) | In-cluster telemetry collection 결정 |
| [`./0046-external-services-over-host-addresses.md`](./0046-external-services-over-host-addresses.md) | External service transport 결정 |
| [`./0047-agent-contract-and-resource-ownership.md`](./0047-agent-contract-and-resource-ownership.md) | Agent 계약과 resource 소유 경계의 한정 개정 |
| [`./0048-local-qa-and-semver-release-ownership.md`](./0048-local-qa-and-semver-release-ownership.md) | 로컬 QA 단계별 책임과 단일 SemVer 릴리스 생산자 결정 |
| [`./0049-external-data-service-contract-alignment.md`](./0049-external-data-service-contract-alignment.md) | 외부 데이터 서비스의 management/development 및 현행 K8s 소비 경계 한정 개정 |
| [`./0050-ingress-nginx-replacement-with-traefik.md`](./0050-ingress-nginx-replacement-with-traefik.md) | 은퇴한 ingress-nginx를 Traefik ingress-nginx provider로 교체 |
| [`./0051-istio-supported-release-upgrade.md`](./0051-istio-supported-release-upgrade.md) | Istio 1.25.2를 지원 release 1.31로 재구축 upgrade |
| [`./0052-single-main-trunk-branch-strategy.md`](./0052-single-main-trunk-branch-strategy.md) | `main` 하나만 장기 branch로 두고 짧은 feature branch로 통합 |
| [`./0053-unvalidated-archive.md`](./0053-unvalidated-archive.md) | `docs/98.archive`를 검증하지 않고 Git history로만 복구 |
| [`./0054-platform-decision-current-state-amendment.md`](./0054-platform-decision-current-state-amendment.md) | 플랫폼 ADR(0011, 0012, 0014, 0026, 0041, 0050)의 현행 불일치 조항을 운영자 승인으로 한정 개정 |
| [`./0055-governance-decision-current-state-amendment.md`](./0055-governance-decision-current-state-amendment.md) | 거버넌스 ADR(0030, 0031, 0033, 0036, 0047, 0048, 0053)의 현행 불일치 조항을 운영자 승인으로 한정 개정 |
| [`./0056-manual-document-disposition-review.md`](./0056-manual-document-disposition-review.md) | 현재 문서 처분 전 소비자·보존·권한·Git 원문 복구를 수동으로 확인하는 개정안 |
| [`./0057-package-exit-shape-check.md`](./0057-package-exit-shape-check.md) | 끝난 Stage 03 package가 잘못된 모양으로 tree를 떠나는 것을 staged commit에서 막도록 ADR-0056 Decision 6을 좁히는 개정 |
| [`./0058-repository-vocabulary-in-knowledge-surface.md`](./0058-repository-vocabulary-in-knowledge-surface.md) | `.agents/knowledge/glossary.md` 하나만 용어 의미를 소유하는 Repository Vocabulary로 허용하도록 ADR-0036 Decision 3의 포인터 전용 조항을 좁히는 개정 |
| [`./0059-registry-common-form-model.md`](./0059-registry-common-form-model.md) | Stage 99 registry(generation 10 유지)에 선택 키를 더해 역할별 공통 문서 양식, 문서 역할, TemplateDefinition, 공유 계약 승인 필드를 담도록 ADR-0033의 현재 상태 키 목록을 개정 |

### Classification

이 README에는 분류 표가 없다.

## Workflow

### Create and Review

1. 결정의 상위 요구와 참조 구조를 `01.requirements/`, `../descriptions/`에서 확인한다.
2. 새 ADR은 `../../99.templates/templates/architecture/decision.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/decisions/####-<short-title>.md`다.
3. `Accepted` ADR의 현재 런타임 값은 GitOps manifest, 정적 검증 스크립트, current baseline ADR과 일치해야 한다.
4. ADR이 구현 또는 운영 계약을 바꾸면 `03.specs/`, `05.operations/policies/` 링크를 갱신한다.
5. ADR 번호는 재사용하지 않는다. 삭제된 ADR의 번호도 다시 쓰지 않으며, 기존 번호의 의미나 원래 승인·이력을 새 번호로 고쳐 쓰지 않는다.

#### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/decisions/`다.

- 같은 폴더의 ADR 문서는 `./`로 시작한다.
- sibling AD stage는 `../descriptions/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../05.operations/`로 연결한다. Retired Stage 04 execution route는 current link target으로 사용하지 않는다.
- 새 ADR의 실제 Markdown 링크는 최종 ADR 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

### Transition and Exit

1. 이 log에는 superseded·retired·deprecated 상태의 ADR을 두지 않는다. 결정 전체를 대체할 때는 새 ADR의 `supersedes`와 Traceability에 이전 ID를 적고, 해당 AD의 `Archived Lineage`에 요약한다. [문서 수명주기 정책](../../../.agents/governance/document-lifecycle.md)의 처분 조건을 확인한 뒤 같은 변경에서 삭제한다. 일부 조항만 개정할 때는 기존 ADR을 보존하고 새 ADR에 개정 범위를 적는다.

## Related Documents

### Upstream and Downstream

- [Architecture README](../README.md)
- [02.architecture/descriptions](../descriptions/README.md)
- [03.specs](../../03.specs/README.md)
- [05.operations/policies](../../05.operations/policies/README.md)
- [Archive Index](../../98.archive/README.md)

### Policy and Templates

- [99.templates ADR Template](../../99.templates/templates/architecture/decision.template.md)
