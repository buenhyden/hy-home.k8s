---
title: 'Claude Agent Surface Restoration Implementation Plan'
type: plan
status: done
owner: 'platform'
updated: 2026-06-01
---

# Claude Agent Surface Restoration Implementation Plan

## Overview (KR)

이 문서는 `.claude/agents`를 실제 Claude 전용 agent 파일 디렉터리로 복원하기 위한 실행 계획과 완료 증적이다. Phase 1 조사에서 확인된 provider surface drift를 바탕으로, 복원 순서와 완료 판단 검증을 정의하고 실행 결과를 기록한다.

## Context

Phase 1 조사 시점의 `.claude/agents`는 `../.agents/agents`를 가리키는 symlink였다. 이 때문에 Claude agent surface가 Gemini frontmatter(`Gemini 3.1 Pro`, `Gemini 3.5 Flash`)를 노출하고, `docs/00.agent-governance/subagent-protocol.md`가 요구하는 Claude-native `tools:` frontmatter도 제공하지 않았다.

이 상태는 `.claude/CLAUDE.md`, `docs/00.agent-governance/harness-catalog.md`, `docs/00.agent-governance/subagent-protocol.md`의 provider-specific agent contract와 충돌했다. 기존 `scripts/validate-repo-quality-gates.sh .`는 PASS할 수 있었지만, 검증 범위가 `.claude/agents` symlink 여부와 Claude model/tool frontmatter 존재를 증명하지 못했다.

## Goals & In-Scope

- **Goals**:
  - `.claude/agents`를 symlink가 아닌 실제 디렉터리로 복원한다.
  - 여덟 개 Claude agent 파일이 `name`, `description`, `model`, `tools` frontmatter를 갖도록 한다.
  - Claude supervisor는 `opus 4.8`, worker agents는 `sonnet 4.6` tier를 사용하도록 한다.
  - `.agents/agents/*.md`는 Gemini 전용 reference index로 유지하고, `.codex/agents/*.toml`은 GPT/Codex mirror로 유지한다.
  - repo quality gate가 `.claude/agents` symlink 회귀와 Claude frontmatter drift를 잡도록 강화한다.
- **In Scope**:
  - `.claude/agents/*.md`
  - `scripts/validate-repo-quality-gates.sh`
  - `docs/00.agent-governance/harness-catalog.md`
  - `docs/00.agent-governance/subagent-protocol.md`
  - `.claude/CLAUDE.md`
  - Phase 3 execution evidence in `docs/04.execution/tasks/`

## Non-Goals & Out-of-Scope

- **Non-goals**:
  - `.agents/skills`, `.agents/workflows`, `.agents/output-styles` symlink 구조 변경
  - Kubernetes manifest, live cluster, ArgoCD, Vault, or External Secrets 변경
  - 외부 `/home/hy/.agents/skills/*` 설치 경로 정리
- **Out of Scope**:
  - direct cluster mutation
  - model policy baseline 변경
  - root `AGENTS.md`, root `CLAUDE.md`, root `GEMINI.md`의 광범위한 재작성

## Work Breakdown

| Task | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| --- | --- | --- | --- | --- |
| PLN-001 | Confirm current drift and freeze Phase 3 target contract | `.claude/agents`, `.agents/agents`, `.codex/agents`, `docs/00.agent-governance/*` | REQ-001 | Evidence shows `.claude/agents` is currently a symlink and the intended final state is a real Claude-only directory |
| PLN-002 | Replace `.claude/agents` symlink with real Claude agent files | `.claude/agents/*.md` | REQ-002 | `test -d .claude/agents && test ! -L .claude/agents` passes; all eight expected files exist |
| PLN-003 | Add Claude-native model and least-privilege tool frontmatter | `.claude/agents/*.md` | REQ-003 | Supervisor has `model: opus 4.8`; workers have `model: sonnet 4.6`; read-only agents use `tools: Read, Grep, Glob, Bash`; authoring agents use `tools: Read, Write, Edit, Grep, Glob, Bash` |
| PLN-004 | Preserve mirror parity without collapsing provider-specific models | `.agents/agents/*.md`, `.codex/agents/*.toml`, `.claude/agents/*.md` | REQ-004 | Matching stems, scope imports, runtime bootstrap, guardrails, handoff, and postflight remain aligned across providers |
| PLN-005 | Harden repository validation for this drift class | `scripts/validate-repo-quality-gates.sh` | REQ-005 | Gate fails if `.claude/agents` is a symlink, if Claude files lack `tools:`, or if Claude models do not match the catalog tier |
| PLN-006 | Reconcile governance/readiness text only where needed | `.claude/CLAUDE.md`, `docs/00.agent-governance/harness-catalog.md`, `docs/00.agent-governance/subagent-protocol.md` | REQ-006 | Readiness matrix and provider capability matrix no longer overstate unverified state; current disk layout and docs agree |
| PLN-007 | Record execution evidence and close stale references | `docs/04.execution/tasks/2026-06-01-claude-agent-surface-restoration.md`, relevant README indexes, `docs/00.agent-governance/memory/progress.md` | REQ-007 | Task evidence records commands, limitations, and the stale 2026-05-30/2026-05-31 relationship without treating prior memory as current truth |

## Verification Plan

| ID | Level | Description | Command / How to Run | Pass Criteria |
| --- | --- | --- | --- | --- |
| VAL-PLN-001 | Repo/static | Confirm `.claude/agents` is real directory | `test -d .claude/agents && test ! -L .claude/agents` | Exit code 0 |
| VAL-PLN-002 | Repo/static | Confirm expected Claude agent files exist | `find .claude/agents -maxdepth 1 -type f -name '*.md' \| sort` | Eight expected agent files are listed |
| VAL-PLN-003 | Repo/static | Confirm Claude frontmatter model/tools contract | Focused parser or validator check in `scripts/validate-repo-quality-gates.sh` | Supervisor and worker model tiers plus least-privilege `tools:` are enforced |
| VAL-PLN-004 | Mirror parity | Confirm Claude/Codex/Gemini mirror contract | `bash scripts/validate-repo-quality-gates.sh .` | Quality gate passes after new checks are added |
| VAL-PLN-005 | Search regression | Confirm no Gemini model frontmatter remains under Claude agents | `rg -n "model: Gemini\|Gemini 3\\." .claude/agents` | No matches |
| VAL-PLN-006 | Documentation | Confirm Plan/Task/README template conformance | `bash scripts/validate-repo-quality-gates.sh .` | No structural template or README index failures |

## Risks & Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Symlink replacement accidentally changes shared `.agents/agents` files | High | Inspect `ls -l .claude/agents .agents/agents` before edits; replace only the symlink path and preserve `.agents/agents` as-is |
| Validator continues to pass despite semantic drift | High | Add explicit symlink, Claude model, and Claude `tools:` checks to the quality gate |
| Claude and Codex mirrors diverge in role or scope text | Medium | Preserve body text from current mirror contracts while changing only provider-specific bootstrap/model/tool frontmatter |
| Documentation claims are updated without disk evidence | Medium | Require command evidence in the task record before moving status from draft/active to done |

## Agent Rollout & Evaluation Gates (If Applicable)

- **Offline Eval Gate**: Repo-static validation, focused frontmatter parsing, and search regression must pass.
- **Sandbox / Canary Rollout**: Not applicable; this change only affects repository agent definitions.
- **Human Approval Gate**: Work proceeded under the active goal continuation for restoring `.claude/agents`; no live runtime action was performed.
- **Rollback Trigger**: If Claude agent files cannot preserve mirror parity or validation cannot be hardened, restore the pre-change symlink state and keep the gap open.
- **Prompt / Model Promotion Criteria**: No model promotion is planned; this work restores the existing `opus 4.8` / `sonnet 4.6` policy.

## Completion Criteria

- [x] `.claude/agents` is a real directory, not a symlink.
- [x] Eight Claude agent files exist with Claude model and least-privilege `tools:` frontmatter.
- [x] `.agents/agents` remains Gemini-specific and `.codex/agents` remains GPT/Codex-specific.
- [x] Repository quality gate catches this drift class and passes after remediation.
- [x] Plan/Task/README/memory evidence records what was changed and what was not verified.
- [x] No live cluster, secret, or deployment action was performed.

## Related Documents

- **Task**: [../tasks/2026-06-01-claude-agent-surface-restoration.md](../tasks/2026-06-01-claude-agent-surface-restoration.md)
- **Runtime Baseline**: [../../../.claude/CLAUDE.md](../../../.claude/CLAUDE.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Subagent Protocol**: [../../00.agent-governance/subagent-protocol.md](../../00.agent-governance/subagent-protocol.md)
- **Model Policy**: [../../00.agent-governance/model-policy.md](../../00.agent-governance/model-policy.md)
- **Previous Related Plan**: [./2026-05-31-codex-governance-harness-alignment.md](./2026-05-31-codex-governance-harness-alignment.md)
