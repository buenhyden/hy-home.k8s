---
title: 'ADR 0002: GitOps Controller Selection (ArgoCD)'
status: 'Accepted'
date: '2026-02-27'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', 'gitops']
layer: "gitops"
---

# ADR: GitOps Controller Selection (ArgoCD) - 0002

- **Status**: Accepted
- **Date**: 2026-02-27
- **layer:** gitops
- **Authors:** buenhyden
- **Deciders:** buenhyden

**Overview (KR):** ArgoCD를 활용한 GitOps 컨트롤러 선택 및 Sealed Secrets를 통한 보안 강화 결정.

## 1. Metadata

- **ADR Number**: 0002
- **Status**: Accepted
- **Date**: 2026-02-27
- **Deciders**: buenhyden
- **layer**: gitops

## 2. Context & Problem Statement

The cluster currently relies on manual application of Kubernetes manifests. As the infrastructure footprint grows, manual workflows become non-repeatable. We need a GitOps controller for reconciliation and secure secret management.

## 3. Decision Drivers (Senior)

- **Developer Experience**: Clear `Synced/Healthy` feedback.
- **Security**: No plaintext secrets (`BAN-GPT-01`); Reproducible private repo access.
- **Determinism**: Manifest pinning for bootstate reproducibility.

## 4. Decision Outcome

**Chosen option: "ArgoCD (App-of-Apps) + Sealed Secrets"**

### Rationale
Provides strong reconciliation and path to securely manage credentials without plaintext commits. The "App-of-Apps" pattern simplifies management of complex dependencies.

### Consequences
- **Positive**: Repeatable convergence, automated remediation.
- **Negative**: Bootstrap "chicken/egg" complexity for initial credentials.

## 5. Technical Debt & Risk Assessment (Senior)

- **Debt Incurred**: Initial setup uses port-forwarding rather than a formal Ingress, which limits remote management scalability.
- **Risk Score**: Medium
- **Mitigation Plan**: Transition to Ingress-Nginx with dedicated subdomains once the Gateway tier is fully stabilized.

## 6. Deferred Decisions (ADL - Architecture Decision Log)

- **External Secrets Integration**: Deferred until Vault or AWS Secrets Manager is required for cross-cloud consistency.
- **Argo Rollouts**: Deferred until production traffic necessitates advanced canary analytics.

## 7. Related Artifacts
- **ARD Reference**: `[../ard/2026-03-07-argocd-gitops-ard.md]`
- **Spec Reference**: `[../specs/2026-03-16-gitops-spec.md]`
