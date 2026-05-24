---
title: 'Task: Workspace Harness Gap Analysis'
type: task
status: done
owner: 'platform'
updated: 2026-05-24
---

# Task: Workspace Harness Gap Analysis

## Overview (KR)

이 문서는 `hy-home.k8s` 워크스페이스 개선 작업의 구현·검증 증적이다.
전체 Gap 분석은 유지하되 구현은 P1/P2 안전 변경으로 제한하고, P3 고위험 항목은
pre-check와 follow-up으로 남긴다.

## Inputs

- **Parent Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Parent Plan**: [../plans/2026-05-24-workspace-harness-gap-analysis.md](../plans/2026-05-24-workspace-harness-gap-analysis.md)

## Working Rules

- Preserve `AGENTS.md` as a thin gateway.
- Keep governance/runtime files under `docs/00.agent-governance/**`,
  `.claude/**`, and `.codex/**` in English.
- Keep human-facing README files in Korean.
- Do not implement high-risk Kubernetes, ArgoCD, Vault, CI policy, or live
  runtime changes in this task.
- Use previous subagent results as investigation evidence and do not rerun
  subagents unless evidence becomes stale.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T-001 | Create spec and stage index entry | doc | VAL-SPC-006-001 | PLN-001 | repo quality gate | Platform | Done |
| T-002 | Create plan with Coverage Ledger, Integrated Gap Analysis, Implementation Plan, checklist, and Final Report | doc | VAL-SPC-006-001 | PLN-001..PLN-006 | repo quality gate | Platform | Done |
| T-003 | Create task evidence document | doc | VAL-SPC-006-001 | PLN-001 | repo quality gate | Platform | Done |
| T-004 | Correct docs and infra scope bridge drift | guardrail | Governance Contract | PLN-002 | repo quality gate | Platform | Done |
| T-005 | Clarify scratch workspace and task-to-skill routing | guardrail | Governance Contract | PLN-003 | repo quality gate | Platform | Done |
| T-006 | Harden GitOps root app manifest validation and script command contract | test | Edge Cases | PLN-004 | GitOps structure check and shell syntax | Platform | Done |
| T-007 | Record P3 high-risk deferrals | doc | Failure Modes | PLN-005 | plan deferred table | Platform | Done |
| T-008 | Run verification bundle | test | Verification Commands | PLN-006 | Verification Summary | Platform | Done |
| T-009 | Append progress memory | memory | Memory Strategy | PLN-001 | progress entry | Platform | Done |

## Suggested Types

- `doc`
- `guardrail`
- `test`
- `memory`

## Agent-specific Types (If Applicable)

- `guardrail`
- `memory`

## Phase View (Optional)

### Phase 1 - Evidence and Planning

- [x] T-001 Create spec.
- [x] T-002 Create plan.
- [x] T-003 Create task.
- [x] T-007 Record P3 deferrals.

### Phase 2 - Limited Implementation

- [x] T-004 Correct scope bridge drift.
- [x] T-005 Clarify scratch and routing boundaries.
- [x] T-006 Harden GitOps validation.
- [x] T-009 Append progress memory.

### Phase 3 - Verification

- [x] T-008 Run verification bundle.

## Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .` - PASS.
  - `bash scripts/generate-llm-wiki-index.sh --check` - PASS.
  - `bash scripts/validate-gitops-structure.sh` - PASS; root app manifest count: 17.
  - `bash scripts/validate-k8s-manifests.sh .` - PASS for YAML syntax; optional `kube-linter` skipped because it is not installed locally.
  - `bash scripts/check-secret-handling.sh .` - PASS.
  - `bash infrastructure/tests/verify-contracts-static.sh` - PASS.
  - `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` - PASS.
  - `python3 -m json.tool .claude/settings.json` - PASS.
  - `python3 -m json.tool .codex/hooks.json` - PASS.
  - `.env.example` and `.env` key-name-only comparison - PASS; key names match without printing values.
  - `git diff --check` - PASS.
- **Eval Commands**: N/A. No model, prompt, or runtime behavior changed.
- **Logs / Evidence Location**: this document and the linked plan.
- **Skipped / Deferred Verification**:
  - live k3d, ArgoCD, Vault, ESO, PostgreSQL, Valkey, TLS, and NetworkPolicy
    checks require explicit live validation approval.
  - optional `kube-linter` is not installed locally; YAML syntax validation and
    static contract verification were used as the local alternative.

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../plans/2026-05-24-workspace-harness-gap-analysis.md](../plans/2026-05-24-workspace-harness-gap-analysis.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Scripts README**: [../../../scripts/README.md](../../../scripts/README.md)
