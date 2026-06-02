---
title: 'Archive Tombstone: ADR-0005: WSL2 HA Baseline and External Endpoint Contract'
type: archive-tombstone
status: archived
owner: platform
updated: 2026-06-02
---

# Archive Tombstone: ADR-0005: WSL2 HA Baseline and External Endpoint Contract

## Overview (KR)

이 문서는 현재 구현과 맞지 않는 old 문서를 archive로 이동했음을 기록하는 Tombstone이다.
원문 본문은 보존하지 않으며, 현재 구현 기준은 아래 replacement 문서가 소유한다.

## Original Document

- Original path: `docs/02.architecture/decisions/0005-wsl2-ha-baseline-and-external-endpoint-contract.md`
- Original title: ADR-0005: WSL2 HA Baseline and External Endpoint Contract
- Original type: adr

## Archive Decision

- Archived on: 2026-06-02
- Reason: Old HA endpoint decision contained non-current endpoint assumptions; current contract is consolidated in ADR-0014.
- Currentness rule: The old body is intentionally not retained because active stages must reflect current repo-backed implementation.

## Current Replacement

- Current owner document: [docs/02.architecture/decisions/0014-current-local-gitops-platform-contract.md](../../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
- Current active index: [decisions](../../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)

## Current Implementation Evidence

- `bash infrastructure/tests/verify-contracts-static.sh`
- `bash scripts/validate-gitops-structure.sh`
- `bash scripts/validate-k8s-manifests.sh .`
- `bash scripts/validate-repo-quality-gates.sh .`

## Archive Index

- [Archive README](../../README.md)

## Related Documents

- [Current replacement](../../../02.architecture/decisions/0014-current-local-gitops-platform-contract.md)
