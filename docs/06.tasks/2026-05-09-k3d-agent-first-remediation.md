---
title: 'Task: k3d Workspace and Agent-first Remediation'
type: task
status: done
owner: 'platform'
updated: 2026-05-09
---

<!-- Target: docs/06.tasks/YYYY-MM-DD-<feature-or-stream>.md -->

# Task: k3d Workspace and Agent-first Remediation

> Use this template for `docs/06.tasks/YYYY-MM-DD-<feature-or-stream>.md`.
>
> Rules:
>
> - Task documents are traceability-first.
> - Core behavior should default to TDD.
> - Agent work must include eval tasks where applicable.
> - This is the canonical execution-tracking location; feature-local task notes under `04.specs/` are secondary.

---

## Overview (KR)

이 문서는 k3d 운영 문서와 Agent-first 실행 계약 보정 작업의 구현·검증 작업 목록이다.
Plan에서 파생된 작업을 추적 가능하게 기록한다.

2026-05-09 gateway/runtime audit 보정은 새 plan/task 문서를 만들지 않고 이 작업 문서에 누적한다. 현재 구조는 이미 thin gateway와 local harness runtime을 갖추고 있으므로, 보정 범위는 catalog clarity와 regression gate 강화로 제한한다.

## Inputs

- **Parent Spec**: not applicable; this remediation does not introduce a new technical contract.
- **Parent Plan**: [`../05.plans/2026-05-09-k3d-agent-first-remediation.md`](../05.plans/2026-05-09-k3d-agent-first-remediation.md)

## Working Rules

- Documentation-only work still needs validation evidence.
- No Kubernetes manifest change is included unless a new human-approved plan expands scope.
- Direct cluster mutation guidance must be marked as human-approved bootstrap/break-glass only.
- Agent execution must remain repo-backed and GitOps-first by default.
- This document remains the execution-tracking source of truth for this remediation.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Add remediation plan and task documents | doc | n/a | PLN-001 | Stage README indexes include new docs | Platform | Done |
| T-002 | Clarify direct `kubectl apply/patch` guidance as bootstrap/break-glass only | ops | n/a | PLN-002 | `rg` review plus repo quality gate | Platform | Done |
| T-003 | Strengthen current-contract language for Headlamp and `172.18.x` where touched | doc | n/a | PLN-003 | stale contract gate remains PASS | Platform | Done |
| T-004 | Add harness readiness matrix and Agent-first execution boundary | guardrail | n/a | PLN-004 | harness catalog checks remain PASS | Platform | Done |
| T-005 | Run repo-backed validation bundle | test | n/a | PLN-005 | validation command output reviewed | Platform | Done |
| T-006 | Clarify Claude permission hooks versus Codex context hook in the harness catalog | doc | n/a | PLN-006 | repo quality gate validates hook-boundary wording | Platform | Done |
| T-007 | Mark historical harness memory as an initial snapshot with current-source pointers | doc | n/a | PLN-006 | repo quality gate validates historical/current-source wording | Platform | Done |
| T-008 | Add gateway/runtime regression checks to repo quality gate | test | n/a | PLN-007 | gateway thinness, English-only governance/runtime, and hook-boundary checks pass | Platform | Done |

## Suggested Types

- `impl`
- `test`
- `eval`
- `doc`
- `ops`

## Agent-specific Types (If Applicable)

- `prompt`
- `tool`
- `memory`
- `guardrail`
- `eval`
- `observability`

## Phase View (Optional)

### Phase 1

- [x] T-001 Add remediation tracking documents
- [x] T-002 Clarify direct mutation boundaries
- [x] T-003 Strengthen current-contract language where touched
- [x] T-004 Add harness readiness matrix

### Phase 2

- [x] T-005 Run and record repo-backed validation bundle
- [x] T-006 Clarify hook boundary in harness catalog
- [x] T-007 Clarify historical memory current-source pointers
- [x] T-008 Add gateway/runtime regression checks

## Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +`
  - Legacy external harness source-label scan across root gateways, `.claude`, `.codex`, and `docs/00.agent-governance`
- **Eval Commands**: not applicable; no prompt/model behavior is changed.
- **Logs / Evidence Location**: conversation validation output for this implementation turn. `kube-linter` was skipped by `validate-k8s-manifests.sh` because it is not installed locally.

## Related Documents

- **Plan**: [`../05.plans/2026-05-09-k3d-agent-first-remediation.md`](../05.plans/2026-05-09-k3d-agent-first-remediation.md)
- **Governance**: [`../00.agent-governance/harness-catalog.md`](../00.agent-governance/harness-catalog.md)
- **Agent-first Rules**: [`../00.agent-governance/rules/agentic.md`](../00.agent-governance/rules/agentic.md)
