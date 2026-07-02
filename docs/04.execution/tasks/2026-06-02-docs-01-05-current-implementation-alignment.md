---
title: 'Task: Docs 01-05 Current Implementation Alignment'
type: task
status: done
owner: platform
updated: 2026-06-02
---

# Task: Docs 01-05 Current Implementation Alignment

## Overview

This document tracks work units and verification evidence for `docs/01-05`
current implementation alignment. The work removes or archives active
documents that conflict with the current repo SSoT, adjusts active contracts,
and hardens QA/CI stale gates.

## Inputs

- **Parent Plan**: [Docs 01-05 Current Implementation Alignment Plan](../plans/2026-06-02-docs-01-05-current-implementation-alignment.md)
- **Current Platform Spec**: [../../03.specs/008-current-local-gitops-platform/spec.md](../../03.specs/008-current-local-gitops-platform/spec.md)
- **Harness Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)

## Working Rules

- Compare active docs against repo-backed implementation evidence, not only link/template pass status.
- Archive old documents through `docs/98.archive` Tombstones when their body conflicts with current implementation or is superseded-only.
- Active docs must link archived material only through `docs/98.archive/README.md`.
- Do not add archive wording to `docs/99.templates/templates/common/reference.template.md`.
- Do not inspect secrets, credentials, tokens, private keys, private RTK DBs, or shell history.
- Repo-static validation must not be reported as live runtime readiness.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Move Headlamp OIDC/Keycloak docs to 05.operations archive Tombstones | doc | Current Ops Contract | PLN-001 | Active Headlamp OIDC stale scan returns no active hits | platform | Done |
| T-002 | Move superseded 007 governance consistency Spec/Plan/Task to archive Tombstones | doc | Harness governance | PLN-002 | Active indexes no longer link moved docs; archive index lists them | platform | Done |
| T-003 | Rewrite active stale hook/CI/HA wording to current implementation | doc | Verification Commands | PLN-003 | Active stale hook and CI job scans return no active contract hits | platform | Done |
| T-004 | Add Plan/Task evidence and sync README indexes | doc | Execution traceability | PLN-005 | Plans/Tasks README include this Plan/Task and omit moved 2026-05-28 docs | platform | Done |
| T-005 | Harden repo quality currentness gates and QA/CI guidance | guardrail | QA/CI | PLN-004 | `bash scripts/validate-repo-quality-gates.sh .` passes with new checks | platform | Done |
| T-006 | Run required local static verification and targeted semantic scans | eval | Verification Plan | PLN-006 | Required commands pass or limitations are recorded | platform | Done |

## Suggested Types

- `doc`
- `guardrail`
- `eval`

## Agent-specific Types (If Applicable)

- `memory`
- `guardrail`
- `eval`

## Phase View (Optional)

### Phase A

- [x] T-001 Headlamp OIDC/Keycloak Tombstones
- [x] T-002 Superseded governance snapshot Tombstones
- [x] T-003 Active current contract rewrite

### Phase B

- [x] T-004 Execution index sync
- [x] T-005 Currentness gate hardening
- [x] T-006 Static verification and semantic scans

## Verification Summary

- **Test Commands**:
  - `git diff --check` — PASS.
  - `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS.
  - `bash scripts/validate-gitops-structure.sh` — PASS.
  - `bash scripts/validate-k8s-manifests.sh .` — PASS; optional kube-linter was not installed, so YAML syntax validation ran.
  - `bash scripts/check-secret-handling.sh .` — PASS.
  - `bash scripts/validate-policy-gates.sh .` — PASS through built-in fallback; optional conftest was not installed.
- **Eval Commands**:
  - Targeted active stale scan for archived Headlamp OIDC docs, moved governance consistency docs, stale hook paths, stale CI job wording, and missing Headlamp GitOps files — PASS; no active hits.
  - Targeted archive Tombstone scan for `type: archive-tombstone`, `status: archived`, and metadata-only body shape — PASS through repo quality gate.
  - Targeted README index scan for added Plan/Task and removed moved docs — PASS through repo quality gate and direct scan.
- **Logs / Evidence Location**:
  - This task document after final verification.
  - [Progress ledger](../../00.agent-governance/memory/progress.md).

## Related Documents

- [Docs 01-05 Current Implementation Alignment Plan](../plans/2026-06-02-docs-01-05-current-implementation-alignment.md)
- [Current Platform Spec](../../03.specs/008-current-local-gitops-platform/spec.md)
- [Harness Spec](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- [Archive Index](../../98.archive/README.md)
- [CI/CD & QA Guide](../../05.operations/guides/0010-ci-cd-qa-reference-guide.md)
- [Task Template](../../99.templates/templates/sdlc/execution/task.template.md)
