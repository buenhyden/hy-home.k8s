---
title: 'Task: scripts Inventory Remediation'
type: task
status: done
owner: 'platform'
updated: 2026-05-17
---

# Task: scripts Inventory Remediation

## Overview (KR)

이 문서는 `scripts/` 폴더의 사용 여부 조사와 인벤토리 보정 작업의 구현·검증 작업 목록이다.
Plan에서 파생된 작업을 추적 가능하게 기록한다.

## Inputs

- **Parent Spec**: not applicable; this remediation does not introduce a new technical contract.
- **Parent Plan**: [`../plans/2026-05-09-scripts-inventory-remediation.md`](../plans/2026-05-09-scripts-inventory-remediation.md)

## Working Rules

- Documentation-only work still needs validation evidence.
- Do not delete, rename, or merge scripts unless a future plan finds concrete unused code.
- Keep the public command contract unchanged.
- Clarify existing optional arguments as repo root only; do not add arbitrary subpath scan mode.
- Keep `scripts/README.md` as the current script inventory entry point.
- This document remains the execution-tracking source of truth for this remediation.

## 2026-05-17 Evidence Refresh

The 2026-05-09 task context recorded the initial four-script snapshot.
Current inventory is maintained in `scripts/README.md`; as of 2026-05-17 it contains five `*.sh` scripts.

Retention now uses the Tier A/B/C standard:
Tier A is a directly executed CI job or post-edit hook gate and counts as retention evidence.
Tier B is an indirect dependency of a required quality gate that owns a generated artifact or check contract and counts as indirect retention evidence.
Tier C is a README, PR template, docs, allowlist, or manual command surface and does not count as retention evidence by itself.

`generate-llm-wiki-index.sh` is Tier B indirect because `validate-repo-quality-gates.sh` runs it with `--check` and it owns the generated `docs/90.references/llm-wiki/wiki-index.md` contract.
No Tier C-only, unused, or one-off deletion candidates are present as of 2026-05-17.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Add remediation plan and task documents | doc | n/a | PLN-001 | Stage README indexes include new docs | Platform | Done |
| T-002 | Rewrite `scripts/README.md` using the repository README template structure | doc | n/a | PLN-002 | README contains Overview, Audience, Scope, Structure, work rules, and references | Platform | Done |
| T-003 | Mark the 2026-05-09 four-script snapshot as `Keep` and refresh current inventory with Tier A/B/C retention evidence | doc | n/a | PLN-003 | Current scripts listed with usage contracts and no deletion candidates | Platform | Done |
| T-004 | Add a current-inventory note to historical governance memory | doc | n/a | PLN-004 | Historical note remains intact and points to `scripts/README.md` | Platform | Done |
| T-005 | Run repo-backed validation bundle | test | n/a | PLN-005 | validation command output reviewed | Platform | Done |
| T-006 | Clarify repo-root argument contract and fail invalid manifest/secret scan roots | impl | n/a | PLN-006 | canonical commands pass and subpath negative checks fail clearly | Platform | Done |
| T-007 | Refresh 2026-05-17 retention evidence and command-contract allowlist | doc | n/a | 2026-05-17 Evidence Refresh | quality gate and generated-index checks run before handoff | Platform | Done |

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
- [x] T-002 Rewrite `scripts/README.md`
- [x] T-003 Document `Keep` decisions
- [x] T-004 Add current-inventory note to historical memory
- [x] T-007 Refresh 2026-05-17 retention evidence and command-contract allowlist

### Phase 2

- [x] T-005 Run and record repo-backed validation bundle
- [x] T-006 Clarify repo-root argument contract for manifest and secret scan scripts

## Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `git diff --check`
  - `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +`
  - `bash infrastructure/tests/verify-contracts-static.sh`
  - `bash scripts/validate-gitops-structure.sh`
  - `bash scripts/validate-k8s-manifests.sh .`
  - `bash scripts/check-secret-handling.sh .`
  - `bash scripts/validate-k8s-manifests.sh gitops` (expected failure)
  - `bash scripts/check-secret-handling.sh gitops` (expected failure)
- **Eval Commands**: not applicable; no prompt/model behavior is changed.
- **Logs / Evidence Location**: conversation validation output for this implementation turn. If `kube-linter` is not installed locally, `validate-k8s-manifests.sh` reports the skip and still validates YAML syntax.

## Related Documents

- **Plan**: [`../plans/2026-05-09-scripts-inventory-remediation.md`](../plans/2026-05-09-scripts-inventory-remediation.md)
- **Scripts README**: [`../../../scripts/README.md`](../../../scripts/README.md)
- **Root README**: [`../../README.md`](../../README.md)
