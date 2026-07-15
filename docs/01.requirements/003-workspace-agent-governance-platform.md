---
title: 'Workspace Agent Governance Platform Product Requirements'
type: sdlc/prd
status: active
owner: platform
updated: 2026-07-14
---

# Workspace Agent Governance Platform Product Requirements

## Overview

이 문서는 `hy-home.k8s` 워크스페이스의 AI Agent 거버넌스 플랫폼 요구사항을 정의한다.
Stage 00을 워크스페이스 전체의 공통 governance SSoT로 두고, Claude, Codex 및
local/Antigravity adapter가 동일한 규칙, 스킬 라우팅, QA/CI/CD, Template Contract,
Model Policy를 따르도록 하는 것이 목적이다. Gemini CLI native surface는
`.gemini/**`이며 현재 absent/`DEFER`이므로 `.agents/**`에서 추론하지 않는다.

## Vision

모든 AI Agent가 하나의 공통 거버넌스를 기준으로 조사, 계획, 구현, 검증을 수행하며, provider별
runtime 차이는 얇은 adapter로만 표현되는 워크스페이스 운영 체계를 만든다.

### Current adapter-surface contract

| Surface | Current classification | Runtime claim |
| --- | --- | --- |
| `.claude/agents/*.md` | Claude native role definitions | Repo-static shape is verified; runtime discovery remains a separate canary. |
| `.codex/agents/*.toml` | Codex native role definitions | Repo-static shape is verified; runtime discovery remains a separate canary. |
| `.claude/CLAUDE.md`, `.codex/CODEX.md` | Repository-local runtime baselines | Instruction baselines, not native role registries. |
| `.agents/{skills,workflows,output-styles}/` | Shared SSoT with Claude/Codex symlink views | Shared repository assets; no Gemini CLI native claim. |
| `.agents/agents/*.md`, `.agents/hooks.json` | Local/Antigravity role and context/validation wiring | Repository-local only; not Gemini CLI native agents or permission hooks. |
| `.codex/hooks.json` | Codex context/validation wiring | Not a Claude-equivalent permission gate. |
| `.gemini/agents/**`, `.gemini/settings.json` | Gemini CLI native surface | Absent and `DEFER`; requires a separate approved design and canary evidence. |

## Problem Statement

Stage 00 canonical adapter 작업 전에는 Agent, Skill, Rule, Hook, Workflow, Memory, QA/CI/CD,
Template Contract, Model Policy가 여러 문서와 provider surface에 분산되어 있었다. 그 결과
새 Agent나 스킬 축을 도입할 때 어느 문서가 정본인지 불분명하고, Phase 1 조사 결과가
`docs/01.requirements`와 `docs/02.architecture`의 upstream 요구/아키텍처로 추적되지 않았다.

## Personas

- **Platform Maintainer**: Stage 00 정책과 provider adapter가 서로 충돌하지 않도록 관리해야 한다.
- **AI Agent Operator**: Claude, Codex, local/Antigravity adapter가 같은 작업 기준과 완료 기준을 따르는지 확인하고 Gemini CLI native gap을 별도로 추적해야 한다.
- **Documentation Writer**: 새 governance, plan, task 문서를 canonical stage와 template에 맞게 작성해야 한다.
- **QA / DevOps Reviewer**: Agent 작업이 repo-static 검증, GitOps-first, no-live-mutation 경계를 지키는지 검토해야 한다.

## Key Use Cases

- **STORY-01**: 운영자는 Stage 00에서 Agent, Skill, Rule, Hook, Workflow, Memory, QA/CI/CD, Template Contract, Model Policy의 공통 정의를 확인한다.
- **STORY-02**: Claude/Codex native role adapters와 local/Antigravity adapter는 공통 Stage 00 규칙을 중복 정의하지 않고 surface-specific 차이만 설명하며, Gemini CLI native 지원을 주장하지 않는다.
- **STORY-03**: Agent는 작업 유형에 맞는 repo-local skill 또는 외부 requested skill을 `harness-catalog.md`의 routing 기준으로 선택한다.
- **STORY-04**: 문서 생성 작업은 `docs/99.templates`와 stage routing 규칙을 따라 `docs/01`부터 `docs/05`까지 추적성을 유지한다.
- **STORY-05**: 완료 전 검증은 provider별 별도 정책이 아니라 repository quality gate와 task evidence를 통해 증명된다.

## Functional Requirements

- **REQ-PRD-FUN-01**: Stage 00은 Agent, Skill, Rule, Hook, Subagent, Output Style, Workflow, Memory, QA, CI/CD, Model Policy, Template Contract의 공통 정의와 소유 경계를 제공해야 한다.
- **REQ-PRD-FUN-02**: Claude, Codex, local/Antigravity adapter surface는 공통 governance를 구현해야 하며, 별도 governance, 별도 QA policy, 별도 Template Contract, 별도 Model Policy를 만들면 안 된다. Gemini CLI native files는 `.gemini/**`에 대한 별도 승인과 검증 없이는 구현된 것으로 간주하지 않는다.
- **REQ-PRD-FUN-03**: 공통 skill routing은 repo-local skills, shared `.agents` assets, 명시적으로 요청된 외부 `SKILL.md` 경로를 구분하고, 누락된 skill은 gap으로 기록해야 한다.
- **REQ-PRD-FUN-04**: Phase 1에서 확인한 process, branch, documentation, QA, DevOps, CI/CD, security, Kubernetes skill axes는 governance/process guide에 strategy lens로 반영되어야 한다.
- **REQ-PRD-FUN-05**: 모든 repo-changing Agent 작업은 관련 Plan/Task 또는 `docs/00.agent-governance/memory/progress.md`에 검증 증거와 한계를 남겨야 한다.
- **REQ-PRD-FUN-06**: 문서 stage와 template mapping은 `docs/99.templates`와 Stage 00 routing rules를 정본으로 삼아야 한다.
- **REQ-PRD-FUN-07**: Agent governance 변경은 GitOps-first, no plaintext secret, no direct live cluster mutation, no destructive git action without explicit approval 경계를 유지해야 한다.

## Success / Acceptance Criteria

- **REQ-PRD-MET-01**: Stage 00 governance hub, common governance, harness catalog, model policy, provider notes, hook docs, template rules가 서로 모순 없이 연결된다.
- **REQ-PRD-MET-02**: `docs/01.requirements`, `docs/02.architecture/requirements`, `docs/02.architecture/decisions`, `docs/04.execution` 사이에 workspace agent governance PRD/ARD/ADR/Plan/Task 추적 체인이 존재한다.
- **REQ-PRD-MET-03**: Tracked adapter files remain thin and point to Stage 00 rather than duplicating durable policy; native and repository-local surfaces are reported separately.
- **REQ-PRD-MET-04**: Repository static validation passes after governance traceability changes.
- **REQ-PRD-MET-05**: HADS or any other external documentation format is not treated as a replacement for the repository template contract unless a separate template-policy plan approves it.

## Scope and Non-goals

- **In Scope**:
  - Stage 00 common governance requirements.
  - Claude/Codex native role adapter와 local/Antigravity adapter의 일관성,
    그리고 Gemini CLI native adoption gap의 명시적 관리.
  - Skill-axis routing and evidence requirements.
  - Template Contract, Model Policy, QA/CI/CD, and memory/progress requirements.
  - Upstream traceability for the existing Stage 00 canonical adapter plan/task.
- **Out of Scope**:
  - Live k3d, ArgoCD, Vault, External Secrets, PostgreSQL, Valkey mutation.
  - Secret value reading, writing, logging, or committing.
  - GitHub Actions topology changes.
  - Provider-specific independent governance models.
  - Immediate HADS migration.
- **Non-goals**:
  - Rewriting historical PRD/ARD/ADR evidence.
  - Adding a new provider runtime.
  - Replacing existing `docs/99.templates` with a different documentation standard.

## Risks, Dependencies, and Assumptions

- Stage 00 must stay the governance SSoT; root gateway files are not policy stores.
- Existing completed Phase 2/Phase 3 plan/task documents remain historical evidence and are linked forward rather than rewritten.
- External skill paths may change outside the repository; missing external skills must be recorded as gaps rather than silently substituted.
- Repo-static validation is required for this governance work; live runtime validation is outside scope unless separately approved.

### Agent execution and approval requirements

- **Allowed Actions**:
  - Read and update repository governance, requirements, architecture, plan, task, and memory documents according to templates.
  - Record current-state overlays when historical documents need traceability without semantic rewrite.
  - Run repo-static validation commands.
- **Disallowed Actions**:
  - Create provider-specific governance that conflicts with Stage 00.
  - Mutate live clusters or external services without explicit approval.
  - Read or expose secret values, credentials, private keys, shell history, or private runtime databases.
  - Replace the repository template contract with HADS without a separate approved migration plan.
- **Human-in-the-loop Requirement**:
  - Required before destructive git operations, live mutation, secret handling, CI topology changes, provider model-policy changes based on unverified sources, or template-standard migration.
- **Evaluation Expectation**:
  - `git diff --check`, `bash scripts/generate-llm-wiki-index.sh --check`, and `bash scripts/validate-repo-quality-gates.sh .` pass or limitations are recorded.

## Traceability

### Lifecycle Traceability

| Requirement ID | Acceptance criterion | Downstream owner |
| --- | --- | --- |
| REQ-PRD-FUN-01 | Stage 00에서 공통 Agent, Skill, Rule, Hook, Workflow, Memory, QA/CI/CD, Model Policy, Template Contract의 소유 경계를 확인할 수 있다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-FUN-02 | Claude/Codex native surface와 local/Antigravity adapter가 Stage 00을 참조하고 Gemini CLI native gap을 구현으로 오인하지 않는다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-FUN-03 | harness catalog가 repo-local, shared, 외부 요청 skill의 routing과 누락 gap을 구분한다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-FUN-04 | process, branch, documentation, QA, DevOps, CI/CD, security, Kubernetes skill 축이 공통 strategy lens로 연결된다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-FUN-05 | repo-changing 작업의 Plan/Task 또는 progress ledger에 검증 증거와 한계가 남는다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-FUN-06 | 문서 stage와 form 선택이 Stage 99 및 Stage 00 routing authority와 일치한다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-FUN-07 | Agent 변경이 GitOps-first, no-plaintext-secret, no-direct-live-mutation 및 명시적 승인 경계를 유지한다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-MET-01 | governance hub, harness catalog, model policy, provider notes, hook docs 및 template rules가 모순 없이 연결된다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-MET-02 | PRD, ARD, ADR, Plan, Task로 이어지는 workspace governance 추적 체인이 존재한다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-MET-03 | tracked adapters가 durable policy를 복제하지 않고 native surface와 repository-local wiring을 분리해 설명한다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-MET-04 | governance traceability 변경 후 repository static validation이 PASS한다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |
| REQ-PRD-MET-05 | 별도 template-policy 승인 없이 HADS 등 외부 형식을 repository template contract의 대체물로 취급하지 않는다. | [ARD 0006](../02.architecture/requirements/0006-workspace-agent-governance-platform.md) |

- **ARD**: [../02.architecture/requirements/0006-workspace-agent-governance-platform.md](../02.architecture/requirements/0006-workspace-agent-governance-platform.md)
- **ADR**: [../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md](../02.architecture/decisions/0013-stage-00-canonical-adapter-model.md)
- **Spec**: N/A — no single current Spec owns the Stage 00 platform; completed tranches remain historical evidence
- **Plan**: [../04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md](../04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Task**: [../04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md](../04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Governance Hub**: [../00.agent-governance/README.md](../00.agent-governance/README.md)
