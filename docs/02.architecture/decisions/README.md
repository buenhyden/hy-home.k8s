---
title: "02.architecture/decisions (ADR)"
version: "0.5.14"
type: "common/readme-collection-index"
status: "active"
owner: "platform"
updated: "2026-09-23"
layer: "architecture"
---
# 02.architecture/decisions (ADR)

> 아키텍처 선택의 맥락, 대안, 결과를 보존하는 ADR stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../../.agents/README.md).

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

## Item Index

```text
02.architecture/decisions/
├── 0002-argocd-helm-and-gitops-model.md
├── 0006-cert-manager-mkcert-ca-issuer.md
├── 0008-istio-install-and-ingress-coexist.md
├── 0009-kiali-external-observability.md
├── 0011-argo-rollouts-progressive-delivery.md
├── 0012-argo-notifications-slack.md
├── 0014-current-local-gitops-platform-contract.md
├── 0026-argo-cd-source-integrity-non-adoption.md
├── 0028-pod-security-admission-per-namespace-adoption.md
├── 0029-mutable-target-revision-retention.md
├── 0030-authority-first-sdlc-and-agent-governance-convergence.md
├── 0031-current-corpus-retention-and-validation-ownership.md
├── 0033-common-document-contract-v9.md
├── 0036-common-knowledge-and-prompt-surfaces.md
├── 0037-kiali-operator-installation.md
├── 0039-unit-archive-retention-and-citation-table.md
├── 0040-archive-reappraisal-and-verifiable-sources.md
├── 0041-openbao-secret-backend.md
├── 0042-linux-server-single-host-baseline.md
├── 0043-dedicated-k8s-ingress-router.md
├── 0044-stateful-data-stores-stay-external.md
├── 0045-in-cluster-telemetry-collection.md
├── 0046-external-services-over-host-addresses.md
└── README.md
```

## Add and Find

1. 결정의 상위 요구와 참조 구조를 `01.requirements/`, `../descriptions/`에서 확인한다.
2. 새 ADR은 `../../99.templates/templates/architecture/decision.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/decisions/####-<short-title>.md`다.
3. Superseded ADR은 predecessor/successor를 상호 연결한다. [ADR-0040](./0040-archive-reappraisal-and-verifiable-sources.md)에 따라 다른 family와 같이 `98.archive/superseded/`로 옮기고 이 log는 predecessor를 identifier로 명명한다. 대체된 ADR은 모두 이 log를 떠났다. ADR-0013, ADR-0015부터 ADR-0025, ADR-0027, ADR-0032, ADR-0034, ADR-0035, ADR-0038은 [Archive index](../../98.archive/README.md)의 Retention Catalog가 명명한다. redirect나 본문 복제본을 만들지 않는다.
4. `Accepted` ADR의 현재 런타임 값은 GitOps manifest, 정적 검증 스크립트, current baseline ADR과 일치해야 한다.
5. ADR이 구현 또는 운영 계약을 바꾸면 `03.specs/`, `05.operations/policies/` 링크를 갱신한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/decisions/`다.

- 같은 폴더의 ADR 문서는 `./`로 시작한다.
- sibling AD stage는 `../descriptions/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../05.operations/`로 연결한다. Retired Stage 04 execution route는 current link target으로 사용하지 않는다.
- 새 ADR의 실제 Markdown 링크는 최종 ADR 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

### Current ADR Index

| 문서 | 설명 | 상태 | 현재성/후속 기준 |
| --- | --- | --- | --- |
| [`./0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md) | ArgoCD Helm 설치와 GitOps 모델 결정 | Accepted | Current GitOps ownership model. |
| [`./0006-cert-manager-mkcert-ca-issuer.md`](./0006-cert-manager-mkcert-ca-issuer.md) | cert-manager + mkcert rootCA ClusterIssuer 도입 결정 | Accepted | Current TLS automation pattern for Headlamp, Kiali, and local ingress endpoints. |
| [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md) | Istio 설치와 ingress-nginx 공존 결정 | Accepted | Current mesh installation boundary. |
| [`./0009-kiali-external-observability.md`](./0009-kiali-external-observability.md) | Kiali + 외부 Prometheus/Grafana/Tempo 연동 결정 | Accepted | External observability boundary(Service/EndpointSlice, NetworkPolicy)는 현재 계약이다. 설치 방식 조항(`kiali-server`, v2.6.x, operator 비채택)은 구현과 다르며 ADR-0037이 후속 결정으로 제안되어 있다. |
| [`./0011-argo-rollouts-progressive-delivery.md`](./0011-argo-rollouts-progressive-delivery.md) | Argo Rollouts 도입과 Rollouts Dashboard 결정 | Accepted | Current progressive delivery contract. |
| [`./0012-argo-notifications-slack.md`](./0012-argo-notifications-slack.md) | Argo Notifications Slack webhook 도입 결정 | Accepted | Current GitOps notification pattern. |
| [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md) | Current local GitOps platform baseline and archive replacement decision | Accepted | Current Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer contract. |
| [`./0026-argo-cd-source-integrity-non-adoption.md`](./0026-argo-cd-source-integrity-non-adoption.md)               | Argo CD source-integrity 미채택 결정                                  | Accepted | 서명 검증은 가변 `targetRevision: main`의 tip 커밋만 인증하므로 기록된 identity gap의 원인을 해결하지 못한다. 선호 대안은 commit-SHA 핀이며 실행하지 않는다. Helm/OCI 범위 확장, warn 모드 문서화, 또는 독립적 이유의 commit signing 도입 시 재검토한다. |
| [`./0028-pod-security-admission-per-namespace-adoption.md`](./0028-pod-security-admission-per-namespace-adoption.md) | Pod Security Admission 네임스페이스별 도입 결정 | Accepted | ADR-0027의 역전 조건 발화 후 재판단이다. 네임스페이스마다 자체 증거가 뒷받침하는 최대 강도를 부여한다: `istio-system`은 CNI DaemonSet 때문에 영구 `privileged`, `monitoring`/`platform`은 `enforce=restricted`, Helm 소유 5곳(argocd 포함)은 차트 버전 종속이라 `audit`/`warn`만, 주입 2곳은 CNI 라이브 미검증이라 `baseline` warn/audit을 검증 신호로 쓴다. `enforce`만 버전 고정한다. |
| [`./0029-mutable-target-revision-retention.md`](./0029-mutable-target-revision-retention.md) | 가변 targetRevision 유지 결정 | Accepted | ADR-0026이 선호 통제로 남긴 commit-SHA 핀을 기각한다. 12개 선언은 모두 이 저장소 자신을 가리키며 외부 차트는 이미 버전 핀이다. 핀은 하드닝이 아니라 자동 reconcile을 수동 promotion으로 바꾸는 배포 모델 변경이고, 핀 커밋은 자기 자신을 참조할 수 없어 구조적으로 한 커밋 뒤처진다. 운영자 추가·환경 추가·force-push 워크플로 도입 시 재검토한다. |
| [`./0030-authority-first-sdlc-and-agent-governance-convergence.md`](./0030-authority-first-sdlc-and-agent-governance-convergence.md) | Authority-first SDLC document, agent governance, Archive, template, and script convergence decision | Accepted | Spec 0054의 terminal authority다. ADR-0031(validation layout), ADR-0032(종단 문서 보존), ADR-0033(router envelope), ADR-0034→0035→0036(agent governance 위치)이 일부 조항을 범위 한정 개정했고, `scripts/` 재배치 조항은 실행되지 않았다. |
| [`./0031-current-corpus-retention-and-validation-ownership.md`](./0031-current-corpus-retention-and-validation-ownership.md) | Current corpus retention, package-local execution lineage, and validation routing ownership decision | Accepted | ADR-0016/0017/0020/0021/0022의 current instance-roster 및 validation-routing 권위를 대체하고 ADR-0030의 두 validation-layout 조항만 lifecycle supersession 없이 범위 한정 개정한다. Spec 0054가 통합 수용을 소유하며, 위임된 validation-tooling 실행은 완료된 Spec 0066이 소유했다. |
| [`./0033-common-document-contract-v9.md`](./0033-common-document-contract-v9.md) | Common document contract v9 and governed router envelope decision | Accepted | snake_case v9 public model, identity-free README envelope, 단일 placeholder grammar, external release evidence, generation-aware frozen Archive validation을 현재 문서 계약으로 채택한다. |
| [`./0036-common-knowledge-and-prompt-surfaces.md`](./0036-common-knowledge-and-prompt-surfaces.md) | Common knowledge and prompt surface adoption | Accepted | ADR-0035의 미채택 디렉터리 조항만 개정해 `.agents/knowledge/`와 `.agents/prompts/`를 채택하고, memory·rule·evaluation·script 디렉터리는 각각의 이유로 미채택을 유지한다. 나머지 정본 위치·스킬 라우팅·게이트웨이·보존·검증 조항은 그대로 승계한다. |
| [`./0037-kiali-operator-installation.md`](./0037-kiali-operator-installation.md) | Kiali operator 설치 결정 | Proposed | 현재 GitOps 구현(`kiali-operator` chart, operator 생성 CR, service DNS 연동)을 결정 기록으로 제안한다. 수락 시 ADR-0009 설치 조항을 대체한다. |
| [`./0039-unit-archive-retention-and-citation-table.md`](./0039-unit-archive-retention-and-citation-table.md) | Unit archive retention and citation table decision | Superseded | 보존 단위(Spec package, Incident bundle, 단독 문서)를 원본 Git object 그대로 보존하고 단위 anchor 상태로 class를 정하며, 단위마다 catalog 행 하나, registry의 순서 있는 인용 결정표 하나, identity 계보로 추적하는 활성 stage 간 이동을 결정했다. ADR-0038 전체를 대체했고, 2026-09-17에 ADR-0040이 이 결정 전체를 대체했다. 별도 처분 승인 전까지 이 log에서 기다린다. |
| [`./0040-archive-reappraisal-and-verifiable-sources.md`](./0040-archive-reappraisal-and-verifiable-sources.md) | Archive reappraisal and verifiable sources decision | Accepted | 보존 단위를 승인 없는 변경으로부터 동결하되 승인된 단위 전체 제거(`git-history-only`)를 허용하고, 현재 증거 가치를 catalog 옆 `Retention Assessment` 표로 판정하며, envelope 도달 가능성을 default branch 기준으로 검증한다. ADR-0039 전체를 대체하며, SPEC-0085가 registry·Archive index·검증기·테스트를 전환했다. |
| [`./0041-openbao-secret-backend.md`](./0041-openbao-secret-backend.md) | OpenBao 런타임 시크릿 backend 전환 결정 | Accepted | Current secret synchronization pattern. ESO와 Kubernetes Auth 패턴은 대체된 ADR-0003에서 이어받는다. |
| [`./0042-linux-server-single-host-baseline.md`](./0042-linux-server-single-host-baseline.md) | Linux server single-host baseline 결정 | Accepted | 플랫폼 host를 WSL2가 아닌 Linux server와 native Docker Engine으로 기록하고, `hy.home.arpa` DNS와 host firewall을 operator 소유로 둔다. ADR-0014의 host 조항만 이어받으며 나머지 조항은 ADR-0014에 남는다. |
| [`./0043-dedicated-k8s-ingress-router.md`](./0043-dedicated-k8s-ingress-router.md) | Dedicated Kubernetes ingress router 결정 | Accepted | k8s host를 `<name>.hy-k8s.home.arpa`(ArgoCD는 `argo`)로 옮기고 `hy-k8s.home.arpa/<name>`은 301로 넘긴다. 전용 host IP `192.168.0.14`에 bind한 k3d serverlb가 외부 Traefik과 분리된 진입점이며 `traefik/` reference 파일을 폐지한다. |
| [`./0044-stateful-data-stores-stay-external.md`](./0044-stateful-data-stores-stay-external.md) | Stateful data store placement 결정 | Accepted | `postgresql-cluster`와 `valkey-cluster`를 k8s로 옮기지 않고 외부 workspace에 둔다. PostgreSQL 계약은 `pg-router`, Valkey 계약은 `mng-valkey`다. |
| [`./0045-in-cluster-telemetry-collection.md`](./0045-in-cluster-telemetry-collection.md) | In-cluster telemetry collection 결정 | Accepted | 관측 저장과 조회(Prometheus, Loki, Tempo, Grafana, Alertmanager)는 외부 workspace에 두고, k8s 메트릭과 로그 수집은 cluster 안 Alloy가 맡아 외부 backend로 push한다. `172.18.0.2` static NodePort scrape는 검증 뒤 폐지한다. |
| [`./0046-external-services-over-host-addresses.md`](./0046-external-services-over-host-addresses.md) | External service transport 결정 | Proposed | 외부 서비스 계약을 `k3d-hyhome` container 주소에서 host 주소 `192.168.0.13`과 host 공개 port로 옮긴다. ESO는 외부 Traefik의 `https://openbao.hy.home.arpa`로 닿고 `vault-external` HTTP 예외를 폐지한다. |

## Related Documents

- [Architecture README](../README.md)
- [02.architecture/descriptions](../descriptions/README.md)
- [03.specs](../../03.specs/README.md)
- [05.operations/policies](../../05.operations/policies/README.md)
- [99.templates ADR Template](../../99.templates/templates/architecture/decision.template.md)
- [Archive Index](../../98.archive/README.md)
