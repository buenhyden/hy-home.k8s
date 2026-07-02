---
title: 'Task: Current Implementation Docs Alignment'
type: sdlc/task
status: done
owner: platform
updated: 2026-06-02
---

# Task: Current Implementation Docs Alignment

## Overview

This document tracks implementation and verification tasks for current
implementation docs alignment. The evidence covers active docs cleanup,
archive Tombstone creation, validator hardening, and regression checks. The
follow-up currentness pass extended through `docs/05.operations` is owned by
the [Docs 01-05 Current Implementation Alignment Task](./2026-06-02-docs-01-05-current-implementation-alignment.md).

## Inputs

- **Parent Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Parent Plan**: [../plans/2026-06-02-current-implementation-docs-alignment.md](../plans/2026-06-02-current-implementation-docs-alignment.md)

## Working Rules

- Compare docs against current repo-backed implementation, not link-chain pass status.
- Keep scope by adding current replacements before archiving old docs.
- Do not preserve old document bodies in Tombstones.
- Keep active docs linked to archive through the archive index only.
- Run static verification before handoff.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create current baseline PRD/ARD/ADR/Spec chain | doc | Related Inputs | PLN-001 | Template coverage and link validation passed | platform | Done |
| T-002 | Add archive Tombstone stage and template | doc | Governance Contract | PLN-002 | Archive template mapping validation passed | platform | Done |
| T-003 | Move old conflicting docs to Tombstones | doc | Migration / Transition Plan | PLN-003 | Active stale-contract scan passed | platform | Done |
| T-004 | Update active README indexes and related links | doc | Related Documents | PLN-004 | Markdown link validation passed | platform | Done |
| T-005 | Harden repo quality gate, hook trigger, and PR QA checklist | test | Verification Commands | PLN-005 | `bash scripts/validate-repo-quality-gates.sh .` passed | platform | Done |
| T-006 | Run regression checks | test | Success Criteria | PLN-001..005 | Required regression commands passed | platform | Done |

## Suggested Types

- `doc`
- `test`
- `guardrail`

## Agent-specific Types (If Applicable)

- `guardrail`
- `eval`

## Phase View (Optional)

### Phase 1

- [x] T-001 Create current baseline chain
- [x] T-002 Add archive stage

### Phase 2

- [x] T-003 Move old docs
- [x] T-004 Update links
- [x] T-005 Harden validator
- [x] T-006 Run regression checks

## Verification Summary

- **Test Commands**:
  - `bash -n scripts/validate-repo-quality-gates.sh` — PASS
  - `bash -n docs/00.agent-governance/hooks/k8s-pre-edit.sh` — PASS
  - `bash -n docs/00.agent-governance/hooks/post-validate.sh` — PASS
  - `git diff --check` — PASS
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS
  - `bash infrastructure/tests/verify-contracts-static.sh` — PASS
  - `bash scripts/validate-gitops-structure.sh` — PASS
  - `bash scripts/validate-k8s-manifests.sh .` — PASS
  - `bash scripts/check-secret-handling.sh .` — PASS
  - `bash scripts/validate-policy-gates.sh .` — PASS
- **Eval Commands**: not applicable.
- **Logs / Evidence Location**: this task document, current baseline docs, and final command output in the implementation handoff.

## Related Documents

- **Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Plan**: [../plans/2026-06-02-current-implementation-docs-alignment.md](../plans/2026-06-02-current-implementation-docs-alignment.md)
- **Follow-up Task**: [./2026-06-02-docs-01-05-current-implementation-alignment.md](./2026-06-02-docs-01-05-current-implementation-alignment.md)
- **Archive Index**: [../../98.archive/README.md](../../98.archive/README.md)
