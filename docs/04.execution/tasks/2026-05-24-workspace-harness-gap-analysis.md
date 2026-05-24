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
- Treat named review skills as additive. `office-hours` was used as a
  problem-framing lens for the input-contract delta, while the direct human
  implementation request and repository P1/P2/P3 safety rules controlled edits.
- Treat `superpowers:brainstorming` as a design-lens review for this already
  approved implementation objective. Its standalone design-doc/user-approval
  default is recorded as a boundary rather than replacing the repository SDD
  artifact flow.
- Treat `gstack-plan-ceo-review` as a HOLD SCOPE plan-quality lens for
  current-state drift. Its external-write preamble and telemetry steps are not
  run; canonical SDD artifacts remain the evidence target.
- Treat `superpowers:executing-plans` as the execution workflow for the CEO
  review plan delta. Record plan review, task execution, verification, and the
  finish boundary in canonical SDD artifacts.

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
| T-021 | Apply office-hours reflection to Hybrid Refresh omissions | doc | VAL-SPC-006-007 | Office-Hours Reflection | Office-Hours Reflection Evidence | Platform | Done |
| T-022 | Update plan and repo-local Skill for named-skill boundary evidence | guardrail | VAL-SPC-006-007 | Office-Hours P1 | repo quality gate and heading check | Platform | Done |
| T-023 | Run Office-Hours follow-up verification bundle | test | VAL-SPC-006-007 | Office-Hours Verification | Office-Hours Verification Summary | Platform | Done |
| T-024 | Apply superpowers brainstorming reflection to remaining initial-contract omissions | doc | VAL-SPC-006-008 | Brainstorming Reflection | Brainstorming Reflection Evidence | Platform | Done |
| T-025 | Update plan and repo-local Skill for canonical SDD routing of named review skills | guardrail | VAL-SPC-006-008 | Brainstorming P1 | repo quality gate and evidence search | Platform | Done |
| T-026 | Run Brainstorming follow-up verification bundle | test | VAL-SPC-006-008 | Brainstorming Verification | Brainstorming Follow-up Verification Summary | Platform | Done |
| T-027 | Apply gstack plan CEO review to initial-contract and Hybrid current-state drift | doc | VAL-SPC-006-010 | CEO Review Follow-up | CEO Review Evidence | Platform | Done |
| T-028 | Add P3 current-state overlay and missing exact skill path evidence | doc | VAL-SPC-006-010 | CEO Review P1 | repo quality gate and targeted evidence search | Platform | Done |
| T-029 | Update reusable audit Skill and progress ledger for stale-deferral overlays | guardrail | VAL-SPC-006-010 | CEO Review P1 | repo quality gate | Platform | Done |
| T-030 | Run CEO follow-up verification bundle | test | VAL-SPC-006-010 | CEO Review Verification | CEO Review Verification Summary | Platform | Done |
| T-031 | Apply superpowers executing-plans to the CEO review plan | doc | VAL-SPC-006-011 | Executing-Plans Follow-up | Executing-Plans Evidence | Platform | Done |
| T-032 | Record executing-plans task execution and finish boundary | doc | VAL-SPC-006-011 | Executing-Plans P1 | targeted evidence search | Platform | Done |
| T-033 | Update reusable audit Skill and progress ledger for named execution-skill evidence | guardrail | VAL-SPC-006-011 | Executing-Plans P1 | repo quality gate | Platform | Done |
| T-034 | Run executing-plans follow-up verification bundle | test | VAL-SPC-006-011 | Executing-Plans Verification | Executing-Plans Verification Summary | Platform | Done |

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

### Phase 6 - Office-Hours Reflection Follow-up

- [x] T-021 Apply office-hours reflection to Hybrid Refresh omissions.
- [x] T-022 Update named-skill boundary evidence in plan and Skill.
- [x] T-023 Run Office-Hours follow-up verification bundle.

### Phase 7 - Superpowers Brainstorming Reflection Follow-up

- [x] T-024 Apply superpowers brainstorming reflection to remaining initial-contract omissions.
- [x] T-025 Update canonical SDD routing evidence for named review skills.
- [x] T-026 Run Brainstorming follow-up verification bundle.

### Phase 8 - GStack Plan CEO Review Follow-up

- [x] T-027 Apply gstack plan CEO review to initial-contract and Hybrid current-state drift.
- [x] T-028 Add P3 current-state overlay and missing exact skill path evidence.
- [x] T-029 Update reusable audit Skill and progress ledger for stale-deferral overlays.
- [x] T-030 Run CEO follow-up verification bundle.

### Phase 9 - Superpowers Executing-Plans Follow-up

- [x] T-031 Apply superpowers executing-plans to the CEO review plan.
- [x] T-032 Record executing-plans task execution and finish boundary.
- [x] T-033 Update reusable audit Skill and progress ledger for named execution-skill evidence.
- [x] T-034 Run executing-plans follow-up verification bundle.

## Hybrid Refresh Evidence

| Evidence item | Status | Location |
| --- | --- | --- |
| Six fresh read-only subagent reviews | complete | linked plan `Hybrid Raw Subagent Output Preservation` |
| Path-level external `SKILL.md` check | complete; all paths present | linked plan `Hybrid Path-Level External Skill Check` |
| P1/P2 implementation mapping | complete | linked plan `Hybrid Implementation Plan` |
| P3 deferred items | complete | linked plan `Hybrid Integrated Gap Analysis` and `Hybrid Implementation Plan` |
| Fresh verification bundle | complete | this task `Hybrid Refresh Verification Summary` |

## Office-Hours Reflection Evidence

| Evidence item | Status | Location |
| --- | --- | --- |
| `office-hours` application boundary | complete; used as review lens only | linked plan `Office-Hours Reflection Follow-up` |
| Initial-contract delta ledger | complete | linked plan `Initial Contract Delta Ledger` |
| Low/medium/high risk treatment | complete; existing P1/P2/P3 kept | linked plan `Office-Hours Delta Gap Analysis` and `Hybrid Implementation Plan` |
| Template-change impact rule | complete; no `docs/99.templates/` changes made | linked plan `Initial Contract Delta Ledger` |
| Named-skill future guardrail | complete | `.claude/skills/workspace-harness-audit/skill.md` |

## Brainstorming Reflection Evidence

| Evidence item | Status | Location |
| --- | --- | --- |
| `superpowers:brainstorming` application boundary | complete; used as design lens only | linked plan `Superpowers Brainstorming Reflection Follow-up` |
| Alternatives and selected approach | complete | linked plan `Brainstorming Alternatives` and `Brainstorming Selected Design` |
| Canonical SDD routing decision | complete | linked plan `Brainstorming Deferred Items`; `.claude/skills/workspace-harness-audit/skill.md` |
| Low/medium/high risk treatment | complete; existing P1/P2/P3 kept | linked plan `Brainstorming Delta Gap Analysis` and `Hybrid Implementation Plan` |
| Template-change impact rule | complete; no `docs/99.templates/` changes made | linked plan `Brainstorming Selected Design` |

## CEO Review Follow-up Evidence

| Evidence item | Status | Location |
| --- | --- | --- |
| `gstack-plan-ceo-review` application boundary | complete; used as HOLD SCOPE review lens only | linked plan `CEO Review Follow-up` |
| Missing exact `brainstorming` path check | complete; path present | linked plan `Hybrid Path-Level External Skill Check` |
| Current `gstack-plan-ceo-review` path check | complete; path present | linked plan `Hybrid Path-Level External Skill Check` |
| P3 current-state overlay | complete | linked plan `CEO P3 Current-State Overlay` |
| Stale-deferral future guardrail | complete | `.claude/skills/workspace-harness-audit/skill.md` |

## Executing-Plans Follow-up Evidence

| Evidence item | Status | Location |
| --- | --- | --- |
| `superpowers:executing-plans` application boundary | complete; used to execute the CEO review plan delta | linked plan `Executing-Plans Follow-up` |
| Plan critical review | complete; one branch/worktree concern recorded | linked plan `Executing-Plans Critical Review` |
| Task execution table | complete | linked plan `Executing-Plans Task Execution` |
| Finish boundary | complete; normal repo on `main`, no linked worktree | linked plan `Executing-Plans Verification Results` |
| Reusable guardrail | complete | `.claude/skills/workspace-harness-audit/skill.md` |

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

## Office-Hours Follow-up Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .` - PASS.
  - `bash scripts/generate-llm-wiki-index.sh --check` - PASS.
  - `bash scripts/validate-gitops-structure.sh` - PASS.
  - `bash scripts/validate-k8s-manifests.sh .` - PASS for YAML syntax; optional `kube-linter` skipped because it is not installed locally.
  - `bash scripts/check-secret-handling.sh .` - PASS.
  - `bash infrastructure/tests/verify-contracts-static.sh` - PASS.
  - `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` - PASS.
  - `python3 -m json.tool .claude/settings.json` - PASS.
  - `python3 -m json.tool .codex/hooks.json` - PASS.
  - `.env.example` and `.env` key-name-only comparison - PASS without printing values.
  - `rg -n "^# " docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md` - PASS; only the document title remains as an H1.
  - `git diff --check` - PASS.
- **Skipped / Deferred Verification**:
  - `office-hours` preamble was not run because it writes to `~/.gstack`
    outside the workspace and is unnecessary for this repository-static delta.
  - live k3d, ArgoCD, Vault, ESO, PostgreSQL, Valkey, TLS, and NetworkPolicy
    checks remain deferred pending explicit approval.
- **Implementation Decisions**:
  - No new runtime, Kubernetes, ArgoCD, Vault, secret/env policy, or CI/CD
    semantics were changed.
  - `workspace-harness-audit` now requires named-skill application boundary
    evidence for future broad audits.

## Brainstorming Follow-up Verification Summary

- **Test Commands**:
  - `bash scripts/validate-repo-quality-gates.sh .` - PASS.
  - `bash scripts/generate-llm-wiki-index.sh --check` - PASS.
  - `bash scripts/validate-gitops-structure.sh` - PASS.
  - `bash scripts/validate-k8s-manifests.sh .` - PASS for YAML syntax; optional `kube-linter` skipped because it is not installed locally.
  - `bash scripts/check-secret-handling.sh .` - PASS.
  - `bash infrastructure/tests/verify-contracts-static.sh` - PASS.
  - `find infrastructure scripts .claude/hooks -type f -name '*.sh' -exec bash -n {} +` - PASS.
  - `python3 -m json.tool .claude/settings.json` - PASS.
  - `python3 -m json.tool .codex/hooks.json` - PASS.
  - `.env.example` and `.env` key-name-only comparison - PASS without printing values.
  - `rg -n "Superpowers Brainstorming Reflection Follow-up|Brainstorming Alternatives|Brainstorming Selected Design" docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md` - PASS.
  - `rg -n "^# " docs/04.execution/plans/2026-05-24-workspace-harness-gap-analysis.md` - PASS; only the document title remains as an H1.
  - `git diff --check` - PASS.
- **Skipped / Deferred Verification**:
  - Separate `docs/superpowers/specs/...` design document was not created
    because it would duplicate canonical SDD artifacts for this approved
    implementation objective.
  - live k3d, ArgoCD, Vault, ESO, PostgreSQL, Valkey, TLS, and NetworkPolicy
    checks remain deferred pending explicit approval.
- **Implementation Decisions**:
  - No new runtime, Kubernetes, ArgoCD, Vault, secret/env policy, or CI/CD
    semantics were changed.
  - `workspace-harness-audit` now prefers canonical SDD artifacts over
    off-taxonomy design-doc locations for named review skills unless the human
    explicitly requests a separate design document.

## CEO Review Follow-up Verification Summary

- **Test Commands**:
  - `test -f /home/hy/.agents/skills/brainstorming/SKILL.md` - PASS.
  - `test -f /home/hy/.agents/skills/gstack/plan-ceo-review/SKILL.md` - PASS.
  - Targeted CEO evidence search - PASS after verification.
  - `bash scripts/validate-repo-quality-gates.sh .` - PASS after verification.
  - `bash scripts/generate-llm-wiki-index.sh --check` - PASS after verification.
  - `bash scripts/validate-gitops-structure.sh` - PASS after verification;
    root app manifest count is 18.
  - `git diff --check` - PASS after verification.
- **Skipped / Deferred Verification**:
  - `gstack-plan-ceo-review` preamble, design-doc persistence, and telemetry
    were not run because they write to `~/.gstack` outside the workspace.
  - Live k3d/ArgoCD/Vault/ESO proof remains deferred until `k3d-hyhome` is
    running and read-only metadata checks can connect to the API server.
- **Implementation Decisions**:
  - No new Kubernetes, Vault, CI, secret/env, or runtime semantic change was
    made in this follow-up.
  - Historical Hybrid rows remain as historical evidence; current state is
    recorded through the CEO P3 overlay.

## Executing-Plans Follow-up Verification Summary

- **Test Commands**:
  - `test -f /home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/executing-plans/SKILL.md` - PASS.
  - `test -f /home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/finishing-a-development-branch/SKILL.md` - PASS.
  - `test -f /home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/using-git-worktrees/SKILL.md` - PASS.
  - `test -f /home/hy/.codex/plugins/cache/claude-plugins-official/superpowers/5.1.0/skills/writing-plans/SKILL.md` - PASS.
  - `git rev-parse --abbrev-ref HEAD` - `main`.
  - `git rev-parse --git-dir` and `git rev-parse --git-common-dir` - both `.git`; normal repo.
  - Targeted executing-plans evidence search - PASS after verification.
  - `bash scripts/validate-repo-quality-gates.sh .` - PASS after verification.
  - `bash scripts/generate-llm-wiki-index.sh --check` - PASS after verification.
  - `bash scripts/validate-gitops-structure.sh` - PASS after verification;
    root app manifest count is 18.
  - `git diff --check` - PASS after verification.
- **Skipped / Deferred Verification**:
  - No separate development worktree was created because this task continues
    the repository's existing human-requested task-unit commit flow on `main`.
  - Live k3d/ArgoCD/Vault/ESO proof remains deferred until `k3d-hyhome` is
    running and read-only metadata checks can connect to the API server.
- **Implementation Decisions**:
  - The executing-plans workflow executed the existing CEO review plan section
    rather than creating a duplicate off-taxonomy plan file.
  - The finishing boundary was recorded as a normal-repo finish check, not a
    merge or PR flow, because no feature branch/worktree exists in this pass.

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
  - CEO review current-state overlay - PASS; resolved P3 items link to the P3
    plan/task and unresolved items remain deferred.
  - Executing-plans follow-up - PASS; plan load/review/execution/verification
    and finish boundary are recorded.
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
