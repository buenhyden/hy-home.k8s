# 02.architecture/decisions (ADR)

> 아키텍처 선택의 맥락, 대안, 결과를 보존하는 ADR stage다.

> [!NOTE]
> All AI agent interactions with this stage must comply with the [Agent Governance Hub](../../00.agent-governance/README.md).

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
├── 0003-eso-vault-k8s-auth.md
├── 0006-cert-manager-mkcert-ca-issuer.md
├── 0008-istio-install-and-ingress-coexist.md
├── 0009-kiali-external-observability.md
├── 0011-argo-rollouts-progressive-delivery.md
├── 0012-argo-notifications-slack.md
├── 0013-stage-00-canonical-adapter-model.md
├── 0014-current-local-gitops-platform-contract.md
├── 0015-declarative-document-contract-registry.md
├── 0016-program-to-tranche-document-lineage.md
├── 0017-program-follow-up-lineage-semantics.md
├── 0018-full-body-archive-record-and-retention.md
├── 0019-provider-native-agent-harness-and-loop-model.md
├── 0020-document-lifecycle-program-closure-evidence.md
├── 0021-canonical-surface-routing-and-evidence-depth.md
├── 0022-direct-approval-standalone-execution-lineage.md
├── 0023-work-unit-document-taxonomy-and-governance-authority.md
├── 0024-terminal-artifact-identity-and-archive-layout.md
├── 0025-four-digit-document-path-identity.md
├── 0026-argo-cd-source-integrity-non-adoption.md
├── 0027-pod-security-standards-staged-adoption.md
├── 0028-pod-security-admission-per-namespace-adoption.md
├── 0029-mutable-target-revision-retention.md
├── 0030-authority-first-sdlc-and-agent-governance-convergence.md
└── README.md
```

## Add and Find

1. 결정의 상위 요구와 참조 구조를 `01.requirements/`, `../descriptions/`에서 확인한다.
2. 새 ADR은 `../../99.templates/templates/architecture/adr.template.md`에서 시작하고, canonical target pattern은 `docs/02.architecture/decisions/####-<short-title>.md`다.
3. Superseded ADR은 Stage 02 decision log에 유지하고 predecessor/successor를 상호 연결한다. 본문 복제본을 Archive에 만들지 않는다.
4. `Accepted` ADR의 현재 런타임 값은 GitOps manifest, 정적 검증 스크립트, current baseline ADR과 일치해야 한다.
5. ADR이 구현 또는 운영 계약을 바꾸면 `03.specs/`, `05.operations/policies/` 링크를 갱신한다.

### Relative Link Rules

이 README의 링크 기준 위치는 `docs/02.architecture/decisions/`다.

- 같은 폴더의 ADR 문서는 `./`로 시작한다.
- sibling AD stage는 `../descriptions/`로 연결한다.
- upstream/downstream docs stage는 `../../01.requirements/`, `../../03.specs/`, `../../04.execution/`, `../../05.operations/`로 연결한다.
- 새 ADR의 실제 Markdown 링크는 최종 ADR 파일 위치 기준으로 다시 계산하고, placeholder target은 code literal로 남긴다.

### Current ADR Index

| 문서 | 설명 | 상태 | 현재성/후속 기준 |
| --- | --- | --- | --- |
| [`./0002-argocd-helm-and-gitops-model.md`](./0002-argocd-helm-and-gitops-model.md) | ArgoCD Helm 설치와 GitOps 모델 결정 | Accepted | Current GitOps ownership model. |
| [`./0003-eso-vault-k8s-auth.md`](./0003-eso-vault-k8s-auth.md) | ESO + Vault Kubernetes Auth 시크릿 패턴 결정 | Accepted | Current secret synchronization pattern. |
| [`./0006-cert-manager-mkcert-ca-issuer.md`](./0006-cert-manager-mkcert-ca-issuer.md) | cert-manager + mkcert rootCA ClusterIssuer 도입 결정 | Accepted | Current TLS automation pattern for Headlamp, Kiali, and local ingress endpoints. |
| [`./0008-istio-install-and-ingress-coexist.md`](./0008-istio-install-and-ingress-coexist.md) | Istio 설치와 ingress-nginx 공존 결정 | Accepted | Current mesh installation boundary. |
| [`./0009-kiali-external-observability.md`](./0009-kiali-external-observability.md) | Kiali + 외부 Prometheus/Grafana/Tempo 연동 결정 | Accepted | Current external observability contract through GitOps Service/EndpointSlice and NetworkPolicy. |
| [`./0011-argo-rollouts-progressive-delivery.md`](./0011-argo-rollouts-progressive-delivery.md) | Argo Rollouts 도입과 Rollouts Dashboard 결정 | Accepted | Current progressive delivery contract. |
| [`./0012-argo-notifications-slack.md`](./0012-argo-notifications-slack.md) | Argo Notifications Slack webhook 도입 결정 | Accepted | Current GitOps notification pattern. |
| [`./0013-stage-00-canonical-adapter-model.md`](./0013-stage-00-canonical-adapter-model.md) | Stage 00 canonical core와 native/local adapter-surface ownership 결정 | Accepted | Earlier agent-governance tranche를 지배한 accepted historical predecessor다. Current decision은 accepted ADR-0019이며 이 record의 original context는 보존한다. |
| [`./0014-current-local-gitops-platform-contract.md`](./0014-current-local-gitops-platform-contract.md) | Current local GitOps platform baseline and archive replacement decision | Accepted | Current Headlamp, ingress-nginx, ArgoCD App-of-Apps, ESO/Vault, external services, Kiali/Istio, Rollouts, Notifications, monitoring, adminer contract. |
| [`./0015-declarative-document-contract-registry.md`](./0015-declarative-document-contract-registry.md) | Declarative document contract registry 결정 | Accepted | ADR-0030이 fixed metadata/profile/transition clauses만 부분 대체하며, Stage 99 registry의 단일 document-machine-owner 원칙은 유지한다. |
| [`./0016-program-to-tranche-document-lineage.md`](./0016-program-to-tranche-document-lineage.md) | Program-to-tranche document lineage 결정 | Accepted | PRD 005와 Spec 026-032의 명시적 one-program-to-many-tranche 계보 및 번호 예외를 정의한다. |
| [`./0017-program-follow-up-lineage-semantics.md`](./0017-program-follow-up-lineage-semantics.md) | Original tranche와 program follow-up 계보 분리 결정 | Accepted | ADR-0016의 seven-tranche 사실을 보존하면서 Spec 033과 이후 follow-up의 별도 관계를 정의한다. |
| [`./0018-full-body-archive-record-and-retention.md`](./0018-full-body-archive-record-and-retention.md) | Full-body archive record와 provenance 결정 | Accepted | ADR-0030이 mandatory full-body 및 parallel deletion-ledger 금지 terminal design을 대체한다. Non-authoritative history, secret exception, provenance와 recovery 목적은 유지한다. |
| [`./0019-provider-native-agent-harness-and-loop-model.md`](./0019-provider-native-agent-harness-and-loop-model.md) | Provider-native agent harness, bounded loop, model/evidence 전이 결정 | Accepted | ADR-0030이 four-provider/12-role/48-adapter/harness-owner design을 대체한다. Provider-native delta, evidence class, bounded execution과 least privilege는 유지한다. |
| [`./0020-document-lifecycle-program-closure-evidence.md`](./0020-document-lifecycle-program-closure-evidence.md) | PRD-0006 / AD-0009 문서 수명주기 프로그램 closure evidence 결정 | Accepted | 2026-07-28 exact terminal closure commit `c5adc27b13893d7cbd1266c9225372cfb7df79e9`에서 AD-0009와 reciprocal same-diff accepted role-decision evidence를 제공한다. ADR-0017/0018은 변경 없는 accepted history이며 reviewed digest `e146fb13fb3a62db014e6317992a4f519b79ba330253c4c5fe89834dc67e1888`은 terminal requirements/quality/security approval을 받았다. Parent `35d8552ba423e3e2d92294ddeb81674392b8f333`부터 closure까지 explicit-ref와 clean-tree aggregate는 PASS이며 evidence-update commit 자체와 hosted/provider/remote/live 결과는 주장하지 않는다. |
| [`./0021-canonical-surface-routing-and-evidence-depth.md`](./0021-canonical-surface-routing-and-evidence-depth.md) | Canonical affected-surface references, GitHub projections, and layered platform evidence decision | Accepted | Existing platform topology and validation-surface owners are preserved; active Spec 047 and planned Specs 048–051 implement the reference-based projections and evidence-depth model without remote/live mutation. |
| [`./0022-direct-approval-standalone-execution-lineage.md`](./0022-direct-approval-standalone-execution-lineage.md) | Direct human-approved standalone Spec/Plan/Task lineage decision | Accepted | Registry schema v8 owns the closed optional standalone relation while preserving every existing PRD/AD-backed program-lineage rule. |
| [`./0023-work-unit-document-taxonomy-and-governance-authority.md`](./0023-work-unit-document-taxonomy-and-governance-authority.md) | Work-unit document topology, stable Stage 05, and governance-authority decision | Accepted | ADR-0030이 Task/agent/archive clauses를 부분 대체하며 Stage 03 co-location, retired Stage 04, stable Stage 05, no Release와 transition safety는 유지한다. |
| [`./0024-terminal-artifact-identity-and-archive-layout.md`](./0024-terminal-artifact-identity-and-archive-layout.md) | Architecture Description activation, complete legacy-form retirement, two-gate authored API Spec retirement, closed mandatory/prohibited artifact identity, virtual Stage 98 change identity, stable archive, and exact script-disposition successor | Accepted | ADR-0030이 terminal form/archive/census/SHA/script design을 대체한다. AD/ADR 의미, native interface, identity, consumer-zero, provenance와 recovery 목적은 유지한다. |
| [`./0025-four-digit-document-path-identity.md`](./0025-four-digit-document-path-identity.md) | Four-digit current document path identity and lowercase Incident directory grammar | Accepted | ADR-0030이 old family table만 부분 대체하며 four-digit identity, lowercase Incident, atomic migration과 immutable history는 유지한다. |
| [`./0026-argo-cd-source-integrity-non-adoption.md`](./0026-argo-cd-source-integrity-non-adoption.md)               | Argo CD source-integrity 미채택 결정                                  | Accepted | 서명 검증은 가변 `targetRevision: main`의 tip 커밋만 인증하므로 기록된 identity gap의 원인을 해결하지 못한다. 선호 대안은 commit-SHA 핀이며 실행하지 않는다. Helm/OCI 범위 확장, warn 모드 문서화, 또는 독립적 이유의 commit signing 도입 시 재검토한다. |
| [`./0027-pod-security-standards-staged-adoption.md`](./0027-pod-security-standards-staged-adoption.md) | Pod Security Standards 단계 도입 결정 | Accepted | 라벨을 지금 붙이지 않는다. Baseline capabilities 제어가 initContainers를 포함하고 `NET_ADMIN`·`NET_RAW`를 허용하지 않는 반면 `istio-cni` 없는 Istio 1.25.2는 `istio-init`에 그 둘을 요구하므로, 구속 조건은 워크로드가 아니라 mesh 네트워킹이다. 도입 순서는 CNI → warn/audit=baseline → 네임스페이스별 enforce로 기록한다. |
| [`./0028-pod-security-admission-per-namespace-adoption.md`](./0028-pod-security-admission-per-namespace-adoption.md) | Pod Security Admission 네임스페이스별 도입 결정 | Accepted | ADR-0027의 역전 조건 발화 후 재판단이다. 네임스페이스마다 자체 증거가 뒷받침하는 최대 강도를 부여한다: `istio-system`은 CNI DaemonSet 때문에 영구 `privileged`, `monitoring`/`platform`은 `enforce=restricted`, Helm 소유 4곳은 차트 버전 종속이라 `audit`/`warn`만, 주입 2곳은 CNI 라이브 미검증이라 `baseline` warn/audit을 검증 신호로 쓴다. `enforce`만 버전 고정한다. |
| [`./0029-mutable-target-revision-retention.md`](./0029-mutable-target-revision-retention.md) | 가변 targetRevision 유지 결정 | Accepted | ADR-0026이 선호 통제로 남긴 commit-SHA 핀을 기각한다. 12개 선언은 모두 이 저장소 자신을 가리키며 외부 차트는 이미 버전 핀이다. 핀은 하드닝이 아니라 자동 reconcile을 수동 promotion으로 바꾸는 배포 모델 변경이고, 핀 커밋은 자기 자신을 참조할 수 없어 구조적으로 한 커밋 뒤처진다. 운영자 추가·환경 추가·force-push 워크플로 도입 시 재검토한다. |
| [`./0030-authority-first-sdlc-and-agent-governance-convergence.md`](./0030-authority-first-sdlc-and-agent-governance-convergence.md) | Authority-first SDLC document, agent governance, Archive, template, and script convergence decision | Accepted | Spec 0054의 terminal authority다. WP-004 foundation, WP-003 agent convergence, WP-010 ownership graph, WP-014 fixed point 순서를 지배한다. |

## Related Documents

- [Architecture README](../README.md)
- [02.architecture/descriptions](../descriptions/README.md)
- [03.specs](../../03.specs/README.md)
- [05.operations/policies](../../05.operations/policies/README.md)
- [99.templates ADR Template](../../99.templates/templates/architecture/adr.template.md)
- [Archive Index](../../98.archive/README.md)
