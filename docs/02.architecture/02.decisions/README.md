---
title: "02.architecture/02.decisions (Product ADR)"
version: "1.0.1"
type: "common/readme"
status: "active"
owner: "platform"
updated: "2026-11-20"
---

# 02.architecture/02.decisions (Product ADR)

## 문서 개요

### 목적과 독자

이 README는 docs/02.architecture/02.decisions에서 현재 소유 문서를 찾는 작성자와 검토자를 안내한다. 이 컬렉션의 목적은 [Purpose](#purpose)에 기록한다.

### 책임과 적용 범위

platform은 docs/02.architecture/02.decisions의 탐색 경로를 유지한다. 소유 파일은 [Paths](#paths), 진입 방법은 [Usage](#usage)에 연결하며 개별 문서의 계약은 해당 정본이 소유한다.

## 내용 계약

### 입력과 전제

입력과 전제는 아래 역할별 본문의 해당 절에 기록한다.

### 본문과 규칙

#### Responsibility

##### Purpose

> 제품(로컬 k8s GitOps 플랫폼) 아키텍처 선택의 맥락, 대안, 결과를 보존하는 ADR collection이다.

이 경로는 플랫폼의 런타임·배포·네트워크·보안·관측 결정을 ADR로 기록하는 canonical collection이다.
문서 체계, 에이전트 거버넌스, QA·CI, Git·릴리스처럼 작업 방식 자체에 대한 결정은
[작업 시스템 ADR](../../00.workspace/02.architecture/02.decisions/README.md)이 소유한다.
각 ADR은 하나의 결정, 그 맥락, 대안, 결과를 보존해 이후 Spec과 운영 정책이 같은 근거를 공유하게 한다.

###### Collection Readers

이 README의 주요 독자:

- Platform Architects
- Platform Engineers
- Operators

###### Inputs and Outputs

<a id="in-scope"></a>

**In Scope**

- 중요한 기술 결정 1건을 다루는 ADR
- 맥락, 결정, 비목표, 대안, 결과
- 관련 Requirement Package/AD/Spec/Plan/Operations 링크

<a id="out-of-scope"></a>

**Out of Scope**

- 상세 구현 설계
- 운영 절차와 장애 대응 단계
- 장문의 제품 배경 설명

##### Excluded Responsibilities

이 collection은 상세 구현 설계, 운영 절차와 장애 대응 단계, 장문의 제품 배경 설명을 소유하지 않는다. 각 ADR은 중요한 기술 결정 1건만 다루며, 각 ADR의 승인·대체 상태는 해당 문서의 frontmatter가 소유한다.

#### Current Contents

##### Paths

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
| [`./0037-kiali-operator-installation.md`](./0037-kiali-operator-installation.md) | Kiali operator 설치 결정 |
| [`./0041-openbao-secret-backend.md`](./0041-openbao-secret-backend.md) | OpenBao 런타임 시크릿 backend 전환 결정 |
| [`./0042-linux-server-single-host-baseline.md`](./0042-linux-server-single-host-baseline.md) | Linux server single-host baseline 결정 |
| [`./0043-dedicated-k8s-ingress-router.md`](./0043-dedicated-k8s-ingress-router.md) | Dedicated Kubernetes ingress router 결정 |
| [`./0044-stateful-data-stores-stay-external.md`](./0044-stateful-data-stores-stay-external.md) | Stateful data store placement 결정 |
| [`./0045-in-cluster-telemetry-collection.md`](./0045-in-cluster-telemetry-collection.md) | In-cluster telemetry collection 결정 |
| [`./0046-external-services-over-host-addresses.md`](./0046-external-services-over-host-addresses.md) | External service transport 결정 |
| [`./0049-external-data-service-contract-alignment.md`](./0049-external-data-service-contract-alignment.md) | 외부 데이터 서비스의 management/development 및 현행 K8s 소비 경계 한정 개정 |
| [`./0050-ingress-nginx-replacement-with-traefik.md`](./0050-ingress-nginx-replacement-with-traefik.md) | 은퇴한 ingress-nginx를 Traefik ingress-nginx provider로 교체 |
| [`./0051-istio-supported-release-upgrade.md`](./0051-istio-supported-release-upgrade.md) | Istio 1.31.2 이상으로 재구축하는 결정. 재구축은 미실행 상태이며 현재 GitOps 선언은 1.25.2다. |
| [`./0054-platform-decision-current-state-amendment.md`](./0054-platform-decision-current-state-amendment.md) | 플랫폼 ADR(0011, 0012, 0014, 0026, 0041, 0050)의 현행 불일치 조항을 운영자 승인으로 한정 개정 |

##### Owners

이 README는 분류 표를 따로 두지 않는다. 분류 표를 두게 되면 여기에 둔다.

#### Usage

##### Entry Points

1. 결정의 상위 요구와 참조 구조를 `01.requirements/`, `../01.descriptions/`에서 확인한다.
2. 새 ADR은 `../../99.templates/02.templates/02.architecture/decision.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/02.decisions/####-<short-title>.md`다.
3. `Accepted` ADR의 승인 목표, GitOps manifest의 현재 선언, 관측한 런타임 결과를 구분한다. 목표와 선언이 다르면 현재 구현과 미적용 범위를 표시하고, 런타임 판단은 관측 근거에 연결한다.
4. ADR이 구현 또는 운영 계약을 바꾸면 `03.specs/`, `05.operations/02.policies/` 링크를 갱신한다.
5. 현재 기준선에서는 삭제된 결정을 포함한 ADR 번호를 보존하고 재사용을 금지한다. 번호 체계의 초기화는 별도로 승인된 최종 기준선 전환에서 해당 범위의 조건이 충족된 때에만 적용한다.

###### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/02.decisions/`다.

- 같은 폴더의 ADR 문서는 `./`로 시작한다.
- sibling AD stage는 `../01.descriptions/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../05.operations/`로 연결한다. Retired Stage 04 execution route는 current link target으로 사용하지 않는다.
- 새 ADR의 실제 Markdown 링크는 최종 ADR 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

###### Upstream and Downstream

- [Architecture README](../README.md)
- [02.architecture/descriptions](../01.descriptions/README.md)
- [03.specs](../../03.specs/README.md)
- [05.operations/policies](../../05.operations/02.policies/README.md)
- [Archive Index](../../98.archive/README.md)

###### Policy and Templates

- [99.templates ADR Template](../../99.templates/02.templates/02.architecture/decision.template.md)

##### Checks

1. 이 log에는 superseded·retired·deprecated 상태의 ADR을 두지 않는다. 결정 전체를 대체할 때는 새 ADR의 `supersedes`와 Traceability에 이전 ID를 적고, 해당 AD의 `Archived Lineage`에 요약한다. [문서 수명주기 정책](../../00.workspace/03.process/document-lifecycle.md)의 처분 조건을 확인한 뒤 같은 변경에서 삭제한다. 일부 조항만 개정할 때는 기존 ADR을 보존하고 새 ADR에 개정 범위를 적는다.
2. ADR-0056과 ADR-0057의 보존·복구 조건은 일상 문서 처분과 완료 패키지 종료에 적용한다. 별도로 승인된 Q07 최종 전환의 제거 범위와 조건은 문서 수명주기 정책에서 확인한다.

## 적용과 확인

### 적용 방법

아래 역할별 본문에 기록된 사용 조건과 절차를 적용한다.

### 확인 기준

아래 역할별 본문의 검증·확인 조건과 그 한계에 따른다.

## 관계와 출처

### 관련 문서

관련 문서와 정본 링크는 아래 역할별 본문에서 확인한다.

### 외부 근거

외부 근거가 사용된 경우 아래 역할별 본문의 출처와 적용 범위에서 확인한다.
