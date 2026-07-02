---
title: 'Archive Tombstone: Platform Expansion: cert-manager, Headlamp, Istio/Kiali Product Requirements'
type: content/archive-tombstone
status: archived
owner: platform
updated: 2026-06-02
---

# Archive Tombstone: Platform Expansion: cert-manager, Headlamp, Istio/Kiali Product Requirements

## Overview

이 문서는 현재 구현과 맞지 않는 old 문서를 archive로 이동했음을 기록하는 Tombstone이다.
원문 본문은 보존하지 않으며, 현재 구현 기준은 아래 replacement 문서가 소유한다.

## Original Document

- Original path: `docs/01.requirements/2026-03-29-platform-expansion-dashboard-mesh.md`
- Original title: Platform Expansion: cert-manager, Headlamp, Istio/Kiali Product Requirements
- Original type: prd

## Archive Decision

- Archived on: 2026-06-02
- Reason: Mixed expansion PRD contained old UI and endpoint assumptions; current scope is covered by the current platform PRD.
- Currentness rule: The old body is intentionally not retained because active stages must reflect current repo-backed implementation.

## Current Replacement

- Current owner document: [docs/01.requirements/2026-06-02-current-local-gitops-platform.md](../../01.requirements/2026-06-02-current-local-gitops-platform.md)
- Current active index: [01.requirements](../../01.requirements/2026-06-02-current-local-gitops-platform.md)

## Current Implementation Evidence

- `bash infrastructure/tests/verify-contracts-static.sh`
- `bash scripts/validate-gitops-structure.sh`
- `bash scripts/validate-k8s-manifests.sh .`
- `bash scripts/validate-repo-quality-gates.sh .`

## Archive Index

- [Archive README](../README.md)

## Related Documents

- [Current replacement](../../01.requirements/2026-06-02-current-local-gitops-platform.md)
