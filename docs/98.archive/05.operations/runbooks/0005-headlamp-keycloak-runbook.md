---
title: 'Archive Tombstone: Headlamp Keycloak OIDC Runbook'
type: archive-tombstone
status: archived
owner: platform
updated: 2026-06-02
---

# Archive Tombstone: Headlamp Keycloak OIDC Runbook

## Overview (KR)

이 문서는 현재 repo-backed Headlamp 구현과 맞지 않는 old Keycloak OIDC
runbook을 `98.archive`로 이동했음을 기록하는 Tombstone이다.

## Original Document

- Original path: `docs/05.operations/runbooks/0005-headlamp-keycloak-runbook.md`
- Original title: Headlamp Keycloak OIDC 전환 Runbook
- Original type: runbook

## Archive Decision

- Archived on: 2026-06-02
- Reason: The runbook treated Headlamp Keycloak OIDC as an active operating
  procedure, but the current repository has no GitOps desired state for
  `headlamp-oidc-secret`, `externalsecret-oidc.yaml`, Keycloak client config, or
  OIDC-enabled Headlamp values.
- Currentness rule: The old body is intentionally not retained because active
  runbooks must describe executable procedures backed by current repo artifacts.

## Current Replacement

- Current owner document: [Rollouts, Notifications & Headlamp Runbook](../../../05.operations/runbooks/0004-rollouts-notifications-headlamp-runbook.md)
- Current active index: [Operations Runbooks README](../../../05.operations/runbooks/README.md)

## Current Implementation Evidence

- `gitops/apps/root/platform-headlamp-app.yaml` owns Headlamp chart version
  `0.41.0`, namespace `headlamp`, and current Helm values.
- `gitops/platform/headlamp/headlamp-ingress.yaml` owns the current
  `headlamp.127.0.0.1.nip.io` route.
- `docs/05.operations/policies/0004-rollouts-notifications-headlamp-policy.md`
  owns the current Headlamp operations boundary.

## Archive Index

- Archive index: [Archive README](../../README.md)

## Related Documents

- [Rollouts, Notifications & Headlamp Operations Policy](../../../05.operations/policies/0004-rollouts-notifications-headlamp-policy.md)
- [ADR-0014: Current Local GitOps Platform Contract](../../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
