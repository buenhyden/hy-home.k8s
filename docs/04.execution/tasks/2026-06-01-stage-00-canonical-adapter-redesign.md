---
title: 'Task: Stage 00 Canonical Adapter Redesign'
type: task
status: done
owner: platform
updated: 2026-06-01
---

# Task: Stage 00 Canonical Adapter Redesign

---

## Overview (KR)

이 문서는 Stage 00 canonical adapter 재설계 Phase 3의 구현·검증 증적을 추적한다.
작업 범위는 공통 governance, provider adapter, template contract, hook/QA contract,
model policy, skill/workflow routing, local runtime evidence를 같은 canonical adapter
모델로 정합화하는 것이다.

Live cluster, secret, deployment, destructive git action은 이 작업 범위 밖이다.

## Inputs

- **Parent Spec**: N/A. This is a governance and harness alignment workstream.
- **Parent Plan**: [../plans/2026-06-01-stage-00-canonical-adapter-redesign.md](../plans/2026-06-01-stage-00-canonical-adapter-redesign.md)

## Working Rules

- Preserve existing staged work unless it directly conflicts with this task.
- Keep governance/control documents in English and human-facing README files in Korean.
- Keep root gateway files thin; move durable policy to `docs/00.agent-governance/**`.
- Use static repository validation as evidence. Live probes remain skipped unless explicitly approved.
- Record unavailable tools and skipped checks honestly.

## Task Table

| Task ID | Description | Type | Parent Spec / Section | Parent Plan / Phase | Validation / Evidence | Owner | Status |
| ------- | ----------- | ---- | --------------------- | ------------------- | --------------------- | ----- | ------ |
| T-001 | Create Phase 3 task record and freeze implementation scope | doc | N/A | PLN-001 | This file exists, links the parent plan, and records no-live-cluster boundaries | platform | Done |
| T-002 | Define Stage 00 canonical ownership map | doc | N/A | PLN-002 | `README.md`, `common-governance.md`, and `harness-catalog.md` define canonical core, adapter, and validation ownership | platform | Done |
| T-003 | Consolidate Template Contract routing | doc | N/A | PLN-003 | `docs-stage-routing` requires `status: draft`, `owner: platform`, required headings, README sync, and validation evidence | platform | Done |
| T-004 | Normalize provider gateway and adapter loading semantics | doc | N/A | PLN-004 | `AGENTS.md`, `.claude/CLAUDE.md`, `.agents/GEMINI.md`, `.codex/CODEX.md`, and provider notes describe adapter boundaries | platform | Done |
| T-005 | Reconcile hook path and event wiring drift | guardrail | N/A | PLN-005 | Active hook references use `docs/00.agent-governance/hooks/*.sh`; validator checks active drift files | platform | Done |
| T-006 | Reconcile subagent, skill, workflow, and output-style support vocabulary | doc | N/A | PLN-006 | `common-governance.md`, `harness-catalog.md`, and `qa-cicd-workflow.md` distinguish native, symlink/mirror, wired, and behavioral support | platform | Done |
| T-007 | Normalize model policy and tier vocabulary after official verification | doc | N/A | PLN-007 | `model-policy.md` records 2026-06-01 OpenAI source check and aligns with `harness-catalog.md` | platform | Done |
| T-008 | Harden QA/CI static gates for adapter drift | test | N/A | PLN-008 | Validator parses `.agents/hooks.json`, checks shared hook paths, pre-commit hook coverage, and stale `shell-static` guide drift | platform | Done |
| T-009 | Update template lifecycle and metadata contract | doc | N/A | PLN-009 | Templates use `owner: platform`; `docs/99.templates/README.md` documents default status/owner and optional lifecycle additions | platform | Done |
| T-010 | Integrate branch completion strategy into Stage 00 workflow | doc | N/A | PLN-010 | `git-workflow.md` and `postflight-checklist.md` include verification, PR/merge/keep/discard, and destructive confirmation boundaries | platform | Done |
| T-011 | Investigate local runtime PATH and RTK availability | eval | N/A | PLN-011 | `command -v rtk` failed; `/home/hy/.local/bin/rtk --version` returned `rtk 0.34.3`; `/home/hy/.local/bin/rtk gain` failed with DB open error | platform | Done |
| T-012 | Reconcile active/stale plans and tasks without rewriting history | doc | N/A | PLN-012 | 2026-05-30 plan/task are marked superseded and link to this canonical adapter stream | platform | Done |
| T-013 | Update traceability records after implementation | memory | N/A | PLN-013 | README indexes and `memory/progress.md` record the new task, superseded work, checks, and limitations | platform | Done |
| T-014 | Run final static verification and completion audit | test | N/A | Verification Plan | `git diff --check`, `bash scripts/generate-llm-wiki-index.sh --check`, `bash -n ...`, and `bash scripts/validate-repo-quality-gates.sh .` pass | platform | Done |

## Suggested Types

- `doc`
- `test`
- `eval`
- `guardrail`
- `memory`

## Phase View

### Phase 3

- [x] T-001 Create Phase 3 task record and freeze implementation scope.
- [x] T-002 Define Stage 00 canonical ownership map.
- [x] T-003 Consolidate Template Contract routing.
- [x] T-004 Normalize provider gateway and adapter loading semantics.
- [x] T-005 Reconcile hook path and event wiring drift.
- [x] T-006 Reconcile support vocabulary.
- [x] T-007 Normalize model policy and tier vocabulary.
- [x] T-008 Harden QA/CI static gates.
- [x] T-009 Update template lifecycle and metadata contract.
- [x] T-010 Integrate branch completion strategy.
- [x] T-011 Investigate local runtime PATH and RTK availability.
- [x] T-012 Reconcile active/stale plans and tasks.
- [x] T-013 Update traceability records.
- [x] T-014 Run final static verification and completion audit.

## Verification Summary

- **Test Commands**:
  - `git diff --check` — PASS.
  - `bash -n docs/00.agent-governance/hooks/post-validate.sh docs/00.agent-governance/hooks/lifecycle-guard.sh scripts/validate-repo-quality-gates.sh` — PASS.
  - `bash scripts/generate-llm-wiki-index.sh --check` — PASS.
  - `bash scripts/validate-repo-quality-gates.sh .` — PASS.
- **Eval Commands**:
  - `command -v rtk` — exit 1; `rtk` is not on PATH in this shell.
  - `/home/hy/.local/bin/rtk --version` — PASS, `rtk 0.34.3`.
  - `/home/hy/.local/bin/rtk gain` — exit 1, tracking database initialization failed with `unable to open database file`.
- **Logs / Evidence Location**:
  - This task document.
  - `docs/00.agent-governance/memory/progress.md`

## Handoff and Limitations

- **Completed Scope**: Stage 00 canonical adapter docs, provider baselines, shared hook path references, template owner defaults, branch completion strategy, validator coverage, stale plan/task reconciliation, and task/progress evidence.
- **Known Limitations**: Live k3d, ArgoCD, Vault, and GitHub CI were not executed. This work is repo-static governance and validation only.
- **Skipped Checks and Reason**: No live cluster probes were run because the session startup reported live probes skipped and the task did not request approved live operations.
- **Next Owner / Follow-up**: Maintainer review should decide whether to commit this work together with the already staged Claude agent surface restoration changes or split commits by task unit.

## Related Documents

- **Plan**: [../plans/2026-06-01-stage-00-canonical-adapter-redesign.md](../plans/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Prior Active Plan**: [../plans/2026-05-30-common-agent-governance-refactoring.md](../plans/2026-05-30-common-agent-governance-refactoring.md)
- **Prior Active Task**: [./2026-05-30-governance-refactoring.md](./2026-05-30-governance-refactoring.md)
- **Governance Hub**: [../../00.agent-governance/README.md](../../00.agent-governance/README.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Model Policy**: [../../00.agent-governance/model-policy.md](../../00.agent-governance/model-policy.md)
- **Template README**: [../../99.templates/README.md](../../99.templates/README.md)
