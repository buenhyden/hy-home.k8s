---
title: 'Argo Rollouts Progressive Delivery Technical Specification'
type: spec
status: active
owner: platform-team
updated: 2026-05-18
---

# Argo Rollouts Progressive Delivery Specification

## Overview (KR)

이 문서는 Argo Rollouts 기반 점진적 배포의 현재 repo-backed 기술 계약을 정의한다.
`platform-rollouts` Application, AppProject 권한, dashboard route, metrics, workload consumption 경계를 구현과 검증의 기준으로 고정한다.

## Strategic Boundaries & Non-goals

- **Owns**: Rollouts chart 설치, namespace, dashboard, metrics, AppProject 권한, validation evidence.
- **Does Not Own**: 개별 애플리케이션 rollout 전략, Slack credential, ArgoCD Notifications template.
- **Non-goals**: 기본 자동 promotion, 멀티클러스터 delivery, Rollouts chart notifications 활성화.

## Related Inputs

- **PRD**: [`../../01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md`](../../01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md)
- **ARD**: [`../../02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md`](../../02.architecture/requirements/0004-argo-rollouts-progressive-delivery.md)
- **Related ADRs**: [`../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md`](../../02.architecture/decisions/0011-argo-rollouts-progressive-delivery.md), [`../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md`](../../02.architecture/decisions/0002-argocd-helm-and-gitops-model.md)

## Contracts

- **Config Contract**:
  - ArgoCD Application: `gitops/apps/root/platform-rollouts-app.yaml`
  - Chart repo: `https://argoproj.github.io/argo-helm`
  - Chart name: `argo-rollouts`
  - Chart target revision: `2.40.9`
  - Namespace: `argo-rollouts`
  - Dashboard host: `rollouts.127.0.0.1.nip.io`
  - Dashboard TLS secret: `rollouts-dashboard-tls` # pragma: allowlist secret
  - Rollouts chart notifications: `notifications.enabled: false`
- **Data / Interface Contract**:
  - CRDs: `Rollout`, `AnalysisTemplate`, `ClusterAnalysisTemplate`, `AnalysisRun`
  - Metrics: controller port `8090`, NodePort service `argo-rollouts-metrics-np` on `30092`
  - Dashboard ingress uses ingress-nginx and cert-manager `mkcert-ca-issuer`
  - External Traefik artifact: `traefik/rollouts-k3d.yaml`
- **Governance Contract**:
  - AppProject `platform` owns controller/dashboard deployment.
  - AppProject `apps` owns application workload consumption of Rollout resources.
  - Promotion, abort, and undo commands are operator actions documented in runbooks, not automated agent actions.

## Core Design

- **Component Boundary**:
  - `platform-rollouts` installs shared controller/dashboard components.
  - `apps` workloads consume Rollout and Analysis resources through ApplicationSet-managed workload paths.
  - Observability is provided through metrics NodePort and external Prometheus.
- **Key Dependencies**:
  - ArgoCD App-of-Apps root application.
  - ingress-nginx, cert-manager, and external Traefik routing.
  - Optional Istio routing for mesh-aware workloads.
- **Tech Stack**:
  - Argo Rollouts Helm chart, Kubernetes CRDs, ingress-nginx, cert-manager, Prometheus, ArgoCD.

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
  - Rollout state is Kubernetes API state.
  - Analysis state is represented by `AnalysisTemplate` and `AnalysisRun`.
  - No external database or secret is introduced by the Rollouts platform component.
- **Migration / Transition Plan**:
  - Application teams migrate individual workloads from `Deployment` to `Rollout`.
  - Existing Services must be split into stable/canary targets when a canary strategy is used.
  - Traffic policy changes must be reviewed with the matching ingress/Istio resources.

## Interfaces & Data Structures

### Core Interfaces

```yaml
rollouts:
  application: gitops/apps/root/platform-rollouts-app.yaml
  namespace: argo-rollouts
  chart:
    repoURL: https://argoproj.github.io/argo-helm
    chart: argo-rollouts
    targetRevision: 2.40.9
  dashboard:
    host: rollouts.127.0.0.1.nip.io
    tlsSecret: rollouts-dashboard-tls
  metrics:
    port: 8090
    nodePort: 30092
  chartNotifications:
    enabled: false
```

## API Contract (If Applicable)

This feature does not expose a repository-owned external API.
The public contract is Kubernetes CRDs and dashboard/metrics endpoints.

## Agent Role & IO Contract (If Applicable)

- **Agent Role**: 유지보수 보조자는 repo-backed manifests/docs를 정적 검증하고, live promotion은 수행하지 않는다.
- **Inputs**: PRD/ARD/ADR, GitOps manifests, operations policy/runbook.
- **Outputs**: 문서 정합화, manifest diff, validation evidence.
- **Success Definition**: Rollouts 계약이 PRD -> ARD -> Spec -> Plan -> Task -> Operations로 추적된다.

## Tools & Tool Contract (If Applicable)

- **Tool List**: `rg`, `bash scripts/validate-gitops-structure.sh`, `bash scripts/validate-k8s-manifests.sh .`, `kubectl argo rollouts` for human/operator runtime checks.
- **Permission Boundary**: Agents must not promote, abort, undo, or apply live resources without explicit human approval.
- **Failure Handling**: static mismatch is fixed through PR; runtime failure routes to the runbook.

## Prompt / Policy Contract (If Applicable)

- Rollouts chart `notifications.enabled: false` must not be “fixed” when adding Slack notifications.
- Slack notifications are owned by ArgoCD Notifications and `docs/03.specs/005-argo-notifications-slack/spec.md`.

## Memory & Context Strategy (If Applicable)

- Backfill lessons are recorded in `docs/00.agent-governance/memory/progress.md`.
- No standalone memory file is required for this feature.

## Guardrails (If Applicable)

- **Input Guardrails**: confirm chart repo, namespace, dashboard host, and AppProject allow-list from repo files.
- **Output Guardrails**: do not introduce plaintext secrets or direct cluster mutation instructions.
- **Blocked Conditions**: missing AppProject allow-list or missing dashboard ingress requires PR correction before runtime validation.
- **Escalation Rule**: changing promotion defaults or disabling analysis requires platform owner approval.

## Evaluation (If Applicable)

- **Eval Types**: static contract validation, GitOps structure validation, runtime readiness checks.
- **Metrics**: validation gate pass/fail; controller Pod readiness; dashboard HTTP status.
- **Datasets / Fixtures**: `gitops/workloads/adminer/` as the reference Rollout workload.
- **How to Run**: use verification commands below and the related runbook for live checks.

## Edge Cases & Error Handling

- Rollouts Dashboard 502 usually indicates dashboard Pod or Service mismatch.
- `CRD not found` indicates chart CRD installation or sync-wave failure.
- AppProject denial indicates missing `argoproj.io` namespace resource allow-list.
- Metrics target down indicates NodePort or Prometheus scrape contract drift.

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**: controller unavailable.
  - **Fallback**: check ArgoCD Application health, chart sync, and controller Pod events.
  - **Human Escalation**: resource budget or chart version change requires PR review.
- **Failure Mode**: rollout stuck during promotion.
  - **Fallback**: operator uses runbook rollback/undo path.
  - **Human Escalation**: production-like promotion policy change requires platform owner approval.

## Verification Commands

```bash
bash scripts/validate-gitops-structure.sh
bash scripts/validate-k8s-manifests.sh .
bash infrastructure/tests/verify-contracts-static.sh
kubectl -n argo-rollouts get pods
kubectl argo rollouts list rollouts --all-namespaces
curl -ksS -o /dev/null -w '%{http_code}' https://rollouts.127.0.0.1.nip.io/
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**: `platform-rollouts` Application is present in root kustomization.
- **VAL-SPC-002**: `argo-rollouts` namespace destination and chart repo are allowed in AppProject `platform`.
- **VAL-SPC-003**: `argoproj.io` Rollout and Analysis resources are allowed where needed.
- **VAL-SPC-004**: Dashboard ingress/TLS contract points to `rollouts.127.0.0.1.nip.io`.
- **VAL-SPC-005**: Controller metrics are exposed for external Prometheus.

## Related Documents

- **Plan**: [`../../04.execution/plans/2026-05-18-argo-rollouts-progressive-delivery.md`](../../04.execution/plans/2026-05-18-argo-rollouts-progressive-delivery.md)
- **Tasks**: [`../../04.execution/tasks/2026-05-18-argo-rollouts-progressive-delivery.md`](../../04.execution/tasks/2026-05-18-argo-rollouts-progressive-delivery.md)
- **Runbook**: [`../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md`](../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md)
- **Operations Policy**: [`../../05.operations/policies/0004-rollouts-notifications-headlamp-policy.md`](../../05.operations/policies/0004-rollouts-notifications-headlamp-policy.md)
