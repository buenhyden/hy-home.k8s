---
title: 'Archive Tombstone: Headlamp Auth OIDC Guide'
type: archive-tombstone
status: archived
owner: platform
updated: 2026-06-02
---

# Archive Tombstone: Headlamp Auth OIDC Guide

## Overview (KR)

이 문서는 현재 repo-backed Headlamp 구현과 맞지 않는 old OIDC guide를
`98.archive`로 이동했음을 기록하는 Tombstone이다.

## Original Document

- Original path: `docs/05.operations/guides/0004-headlamp-auth-oidc-guide.md`
- Original title: Headlamp 인증 & OIDC 연동 Guide
- Original type: guide

## Archive Decision

- Archived on: 2026-06-02
- Reason: The guide described Headlamp Keycloak OIDC migration artifacts that do
  not exist in the current GitOps SSoT, including `headlamp-oidc-secret`,
  `externalsecret-oidc.yaml`, and a feature-local Headlamp values file.
- Currentness rule: The old body is intentionally not retained because active
  operations docs must reflect current repo-backed implementation.

## Current Replacement

- Current owner document: [Rollouts, Notifications & Headlamp Runbook](../../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md)
- Current active index: [Operations Guides README](../../../05.operations/guides/README.md)

## Current Implementation Evidence

- `gitops/apps/root/platform-headlamp-app.yaml` owns the current Headlamp Helm
  chart contract.
- `gitops/platform/headlamp/kustomization.yaml` currently owns only the
  Headlamp ingress resource.
- `gitops/platform/headlamp/headlamp-ingress.yaml` owns the current Headlamp
  ingress/TLS route.

## Archive Index

- Archive index: [Archive README](../../README.md)

## Related Documents

- [Rollouts, Notifications & Headlamp Operations Policy](../../../05.operations/policies/0004-rollouts-notifications-headlamp-policy.md)
- [ADR-0014: Current Local GitOps Platform Contract](../../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
