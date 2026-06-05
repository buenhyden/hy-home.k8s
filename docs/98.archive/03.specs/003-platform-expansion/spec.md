---
title: 'Archive Tombstone: Platform Expansion Technical Specification'
type: archive-tombstone
status: archived
owner: platform
updated: 2026-06-02
---

# Archive Tombstone: Platform Expansion Technical Specification

## Overview

이 문서는 현재 구현과 맞지 않는 old 문서를 archive로 이동했음을 기록하는 Tombstone이다.
원문 본문은 보존하지 않으며, 현재 구현 기준은 아래 replacement 문서가 소유한다.

## Original Document

- Original path: `docs/03.specs/003-platform-expansion/spec.md`
- Original title: Platform Expansion Technical Specification
- Original type: spec

## Archive Decision

- Archived on: 2026-06-02
- Reason: Mixed expansion spec contained old UI and endpoint assumptions; current scope is covered by the current platform spec.
- Currentness rule: The old body is intentionally not retained because active stages must reflect current repo-backed implementation.

## Current Replacement

- Current owner document: [docs/03.specs/008-current-local-gitops-platform/spec.md](../../../03.specs/008-current-local-gitops-platform/spec.md)
- Current active index: [008-current-local-gitops-platform](../../../03.specs/008-current-local-gitops-platform/spec.md)

## Current Implementation Evidence

- `bash infrastructure/tests/verify-contracts-static.sh`
- `bash scripts/validate-gitops-structure.sh`
- `bash scripts/validate-k8s-manifests.sh .`
- `bash scripts/validate-repo-quality-gates.sh .`

## Archive Index

- [Archive README](../../README.md)

## Related Documents

- [Current replacement](../../../03.specs/008-current-local-gitops-platform/spec.md)
