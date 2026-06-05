---
title: 'Argo Rollouts Progressive Delivery Architecture Reference Document'
type: ard
status: active
owner: platform
updated: 2026-06-04
---

# Argo Rollouts Progressive Delivery Architecture Reference Document

## Overview

이 문서는 Argo Rollouts 기반 점진적 배포의 참조 아키텍처와 품질 속성을 정의한다.
현재 GitOps 리소스는 이미 저장소에 존재하므로, 이 ARD는 미래 구현 계획이 아니라 repo-backed 실행계약을 추적 가능한 아키텍처 입력으로 정리하는 backfill 문서다.

## Summary

Argo Rollouts는 `argo-rollouts` namespace에서 controller와 dashboard를 제공하고, 애플리케이션 팀이 `Rollout`, `AnalysisTemplate`, Istio routing, ingress-nginx, cert-manager TLS를 조합해 점진적 배포를 수행할 수 있게 한다.
플랫폼은 controller 설치, dashboard 접근, AppProject 권한, 관측성 노출, 안전한 수동 promotion 경계를 소유한다.

## Boundaries & Non-goals

- **Owns**:
  - Argo Rollouts Helm chart 배포 경계
  - `argo-rollouts` namespace와 controller/dashboard runtime boundary
  - AppProject allow-list와 `apps` namespace Rollout 사용 경계
  - Rollouts Dashboard `rollouts.127.0.0.1.nip.io` 접근 경로
  - Prometheus가 수집할 controller metrics 노출
- **Consumes**:
  - ArgoCD App-of-Apps reconciliation
  - ingress-nginx와 cert-manager `mkcert-ca-issuer`
  - 외부 Prometheus 및 관측성 스택
  - 애플리케이션별 Rollout manifest
- **Does Not Own**:
  - 개별 애플리케이션의 배포 전략 선택
  - 애플리케이션 이미지 빌드/릴리스 정책
  - Slack 알림 template와 credential 관리
- **Non-goals**:
  - 기본 자동 promotion 강제
  - 멀티클러스터 Rollouts
  - 앱별 Analysis metric 표준화

## Quality Attributes

- **Performance**: controller와 dashboard는 WSL2/k3d 자원 예산 안에서 동작하도록 request/limit을 고정한다.
- **Security**: Rollouts 관련 CRD와 namespace 권한은 AppProject allow-list로 제한한다.
- **Reliability**: GitOps source는 `platform-rollouts` Application이 소유하고, 재시도와 self-heal을 사용한다.
- **Scalability**: controller는 플랫폼 공용으로 유지하고, 앱별 rollout 수평 확장은 `apps` namespace의 workload 계약으로 분리한다.
- **Observability**: controller metrics는 NodePort와 Prometheus scrape 계약으로 노출한다.
- **Operability**: dashboard, CLI, runbook 검증을 통해 진행률, promotion, abort, rollback 경로를 확인한다.

## System Overview & Context

- Platform root app includes `gitops/apps/root/platform-rollouts-app.yaml`.
- The Rollouts chart source is `https://argoproj.github.io/argo-helm`, chart `argo-rollouts`, target revision `2.40.9`.
- The controller and dashboard run in `argo-rollouts`.
- Dashboard traffic uses ingress-nginx TLS inside the cluster and an external Traefik dynamic config file for browser access.
- Application teams consume the CRDs through workload manifests, for example `gitops/workloads/adminer/rollout.yaml`.

## Data Architecture

- **Key Entities / Flows**:
  - `Rollout`: application deployment state machine.
  - `AnalysisTemplate` / `AnalysisRun`: application-level metrics-driven safety checks; the current app onboarding pattern requires an `AnalysisTemplate` during canary rollout steps.
  - `Service` stable/canary pair: traffic targets for rollout steps.
  - `VirtualService` / `DestinationRule`: Istio routing for mesh-aware workloads.
- **Storage Strategy**:
  - Rollouts state is Kubernetes API state. No separate database is introduced.
  - Controller metrics are exposed for external Prometheus scraping.
- **Data Boundaries**:
  - No credentials are introduced by Rollouts itself.
  - Notifications are intentionally handled by ArgoCD Notifications, not Rollouts chart notifications.

## Infrastructure & Deployment

- **Runtime / Platform**:
  - WSL2 + k3d/k3s local platform managed by ArgoCD.
  - Namespace: `argo-rollouts`.
  - Dashboard host: `rollouts.127.0.0.1.nip.io`.
- **Deployment Model**:
  - `platform-rollouts` ArgoCD Application installs the Helm chart.
  - `gitops/apps/root/kustomization.yaml` includes the Application.
  - AppProject `platform` allows the chart repo and destination namespace.
  - AppProject `apps` allows application workloads to use Rollout and Analysis resources.
- **Operational Evidence**:
  - Static GitOps checks validate application and kustomization structure.
  - Manifest checks validate YAML syntax.
  - Runtime checks are deferred to the runbook when a live cluster is intentionally available.

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**: Agents may update docs and manifests only through repo-backed GitOps flow.
- **Tooling Boundary**: Direct `kubectl apply` or live promotion is not allowed without explicit human approval.
- **Memory & Context Strategy**: Reusable backfill lessons belong in `docs/00.agent-governance/memory/progress.md`.
- **Guardrail Boundary**: Agents must distinguish Rollouts chart `notifications.enabled: false` from ArgoCD Notifications.
- **Latency / Cost Budget**: Not applicable.

## Related Documents

- **PRD**: [`../../01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md`](../../01.requirements/2026-05-17-argo-rollouts-progressive-delivery.md)
- **Spec**: [`../../03.specs/004-argo-rollouts-progressive-delivery/spec.md`](../../03.specs/004-argo-rollouts-progressive-delivery/spec.md)
- **Plan**: [`../../04.execution/plans/2026-05-18-argo-rollouts-progressive-delivery.md`](../../04.execution/plans/2026-05-18-argo-rollouts-progressive-delivery.md)
- **ADR**: [`../decisions/0011-argo-rollouts-progressive-delivery.md`](../decisions/0011-argo-rollouts-progressive-delivery.md)
