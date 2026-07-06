---
title: 'Archive Tombstone: WSL2 k3d/k3s ArgoCD HA Platform Architecture Reference Document'
type: content/archive-tombstone
status: archived
owner: platform
updated: 2026-06-02
original_path: docs/02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md
archived_on: 2026-06-02
archive_reason: superseded
replacement: docs/02.architecture/requirements/0007-current-local-gitops-platform.md
---

# Archive Tombstone: WSL2 k3d/k3s ArgoCD HA Platform Architecture Reference Document

## Overview

이 문서는 현재 구현과 맞지 않는 old 문서를 archive로 이동했음을 기록하는 Tombstone이다.
원문 본문은 보존하지 않으며, 현재 구현 기준은 아래 replacement 문서가 소유한다.

## Original Document

- Original path: `docs/02.architecture/requirements/0002-wsl2-k3d-argocd-ha-platform.md`
- Original title: WSL2 k3d/k3s ArgoCD HA Platform Architecture Reference Document
- Original type: ard

## Archive Decision

- Archived on: 2026-06-02
- Reason: Old HA architecture contained non-current endpoint assumptions; current scope is covered by the current platform ARD.
- Currentness rule: The old body is intentionally not retained because active stages must reflect current repo-backed implementation.

## Current Replacement

- Current owner document: [docs/02.architecture/requirements/0007-current-local-gitops-platform.md](../../../02.architecture/requirements/0007-current-local-gitops-platform.md)
- Current active index: [requirements](../../../02.architecture/requirements/0007-current-local-gitops-platform.md)

## Current Implementation Evidence

- `bash infrastructure/tests/verify-contracts-static.sh`
- `bash scripts/validate-gitops-structure.sh`
- `bash scripts/validate-k8s-manifests.sh .`
- `bash scripts/validate-repo-quality-gates.sh .`

## Archive Index

- [Archive README](../../README.md)

## Related Documents

- [Current replacement](../../../02.architecture/requirements/0007-current-local-gitops-platform.md)
