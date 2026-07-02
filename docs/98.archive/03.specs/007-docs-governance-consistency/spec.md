---
title: 'Archive Tombstone: Documentation Governance Consistency Spec'
type: content/archive-tombstone
status: archived
owner: platform
updated: 2026-06-02
---

# Archive Tombstone: Documentation Governance Consistency Spec

## Overview

이 문서는 완료된 docs governance cleanup snapshot을 current active Spec에서
제외하고 `98.archive`로 이동했음을 기록하는 Tombstone이다.

## Original Document

- Original path: `docs/03.specs/007-docs-governance-consistency/spec.md`
- Original title: Documentation Governance Consistency Technical Specification
- Original type: spec

## Archive Decision

- Archived on: 2026-06-02
- Reason: The spec is a completed cleanup snapshot and still referenced old hook
  paths that no longer match the current shared hook SSoT under
  `docs/00.agent-governance/hooks/`.
- Currentness rule: The old body is intentionally not retained because active
  Specs must define current implementation contracts.

## Current Replacement

- Current owner document: [Docs 01-05 Current Implementation Alignment Plan](../../../04.execution/plans/2026-06-02-docs-01-05-current-implementation-alignment.md)
- Current active index: [Specs README](../../../03.specs/README.md)

## Current Implementation Evidence

- `docs/00.agent-governance/rules/document-stage-routing.md` owns current stage
  routing.
- `docs/99.templates/README.md` owns current template mapping.
- `scripts/validate-repo-quality-gates.sh` owns current repo quality gates.

## Archive Index

- Archive index: [Archive README](../../README.md)

## Related Documents

- [Current Implementation Docs Alignment Plan](../../../04.execution/plans/2026-06-02-current-implementation-docs-alignment.md)
- [Docs 01-05 Current Implementation Alignment Task](../../../04.execution/tasks/2026-06-02-docs-01-05-current-implementation-alignment.md)
