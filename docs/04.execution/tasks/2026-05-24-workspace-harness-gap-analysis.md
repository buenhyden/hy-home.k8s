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
- Use previous subagent results as investigation evidence unless evidence
  becomes stale. The 2026-05-24 Hybrid Refresh intentionally reran all six
  read-only role reviews for freshness and preserved the fresh tables in the
  linked plan.

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
| T-010 | Audit unreflected input tasks | doc | VAL-SPC-006-004 | PLN-007 | Input Reflection Follow-up | Platform | Done |
| T-011 | Verify exact required external `SKILL.md` paths | guardrail | VAL-SPC-006-004 | PLN-007 | skill path check | Platform | Done |
| T-012 | Add repo-local workspace harness audit skill | guardrail | VAL-SPC-006-005 | PLN-007 | repo quality gate | Platform | Done |
| T-013 | Add row-level required skill evidence to the Implementation Plan | doc | VAL-SPC-006-004 | PLN-007 | repo quality gate | Platform | Done |
| T-014 | Rerun six read-only role reviews for Hybrid Refresh freshness | doc | VAL-SPC-006-006 | Hybrid Refresh | raw role tables in linked plan | Platform | Done |
| T-015 | Record path-level external `SKILL.md` presence results | guardrail | VAL-SPC-006-006 | Hybrid Refresh | path-level ledger in linked plan/task | Platform | Done |
| T-016 | Align Spec status, plan heading hierarchy, and governance metadata | doc | VAL-SPC-006-006 | Hybrid P1 | repo quality gate | Platform | Done |
| T-017 | Clarify meta runtime ownership and per-skill contract type | guardrail | VAL-SPC-006-006 | Hybrid P1 | repo quality gate | Platform | Done |
| T-018 | Refresh scripts/examples evidence wording without semantic changes | doc | VAL-SPC-006-006 | Hybrid P1 | repo quality gate | Platform | Done |
| T-019 | Make SessionStart live probes opt-in and ignore scratch workspaces | guardrail | VAL-SPC-006-006 | Hybrid P2 | shell syntax and repo quality gate | Platform | Done |
| T-020 | Run Hybrid Refresh repo-static verification bundle | test | VAL-SPC-006-006 | Hybrid Verification | Hybrid Refresh Verification Summary | Platform | Done |

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

### Phase 4 - Input Reflection Follow-up

- [x] T-010 Audit unreflected input tasks.
- [x] T-011 Verify exact required external `SKILL.md` paths.
- [x] T-012 Add repo-local workspace harness audit skill.
- [x] T-013 Add row-level required skill evidence to the Implementation Plan.

### Phase 5 - Hybrid Refresh

- [x] T-014 Rerun six read-only role reviews.
- [x] T-015 Record path-level external `SKILL.md` results.
- [x] T-016 Align lifecycle status, heading hierarchy, and metadata.
- [x] T-017 Clarify runtime ownership and skill contract types.
- [x] T-018 Refresh scripts/examples evidence wording.
- [x] T-019 Gate live startup probes and ignore scratch workspaces.
- [x] T-020 Run Hybrid Refresh verification bundle.

## Hybrid Refresh Evidence

| Evidence item | Status | Location |
| --- | --- | --- |
| Six fresh read-only subagent reviews | complete | linked plan `Hybrid Raw Subagent Output Preservation` |
| Path-level external `SKILL.md` check | complete; all paths present | linked plan `Hybrid Path-Level External Skill Check` |
| P1/P2 implementation mapping | complete | linked plan `Hybrid Implementation Plan` |
| P3 deferred items | complete | linked plan `Hybrid Integrated Gap Analysis` and `Hybrid Implementation Plan` |
| Fresh verification bundle | complete | this task `Hybrid Refresh Verification Summary` |

## Hybrid Refresh Path-Level Skill Check

All external `SKILL.md` paths requested by the task contract were checked in the
current WSL environment. Result: PASS; no missing paths. The path-by-path ledger
is stored in the linked plan to keep this task document concise.

## Hybrid Refresh Verification Summary

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
  - `.env.example` and `.env` key-name-only comparison - PASS after Bash rerun; key names match without printing values.
  - `git diff --check` - PASS.
- **Skipped / Deferred Verification**:
  - live k3d, ArgoCD, Vault, ESO, PostgreSQL, Valkey, TLS, and NetworkPolicy checks require explicit live validation approval.
  - optional `kube-linter` is not installed locally; YAML syntax validation and static contract verification were used as local alternatives.
  - remote GitHub Actions status, branch protection, and rulesets were not queried from the worktree.
- **Implementation Decisions**:
  - `SessionStart` live probes now require explicit `HY_HOME_K8S_ENABLE_SESSION_LIVE_PROBES=1`.
  - `_workspace/` and `_workspace_prev/` are ignored as scratch paths.
  - P3 GitOps, Vault, AppProject, bootstrap ownership, CI supply-chain, local settings precedence, graphify cleanup, and live validation items remain deferred.

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
  - required external `SKILL.md` path existence check - PASS; all listed paths present.
  - Implementation Plan row-level `Required skill` check - PASS; P1/P2/P3 rows carry skill evidence.
  - `git diff --check` - PASS.
- **Eval Commands**: No live model or subagent pressure eval was run. The
  repo-local Skill addition was checked through repository quality gates,
  harness catalog inventory, and the skill authoring checklist from the loaded
  skill-writing guidance.
- **Logs / Evidence Location**: this document and the linked plan.
- **Skipped / Deferred Verification**:
  - live k3d, ArgoCD, Vault, ESO, PostgreSQL, Valkey, TLS, and NetworkPolicy
    checks require explicit live validation approval.
  - optional `kube-linter` is not installed locally; YAML syntax validation and
    static contract verification were used as the local alternative.
  - automated `skill-reviewer` loop was not run because the required plugin-dev
    reviewer surface is not part of this repository's current harness.

## Related Documents

- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../plans/2026-05-24-workspace-harness-gap-analysis.md](../plans/2026-05-24-workspace-harness-gap-analysis.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Workspace Harness Audit Skill**: [../../../.claude/skills/workspace-harness-audit/skill.md](../../../.claude/skills/workspace-harness-audit/skill.md)
- **Scripts README**: [../../../scripts/README.md](../../../scripts/README.md)
