---
title: 'Workspace Agent Governance Platform Architecture Reference Document'
type: ard
status: active
owner: platform
updated: 2026-06-01
---

# Workspace Agent Governance Platform Architecture Reference Document (ARD)

## Overview

이 문서는 `hy-home.k8s`의 workspace agent governance platform 참조 아키텍처를 정의한다.
Stage 00을 canonical core로 두고, `.agents` shared assets와 `.claude`, `.codex`, `.agents`
provider adapter가 하나의 governance, QA/CI/CD, Template Contract, Model Policy를 따르도록
하는 구조를 고정한다.

## Summary

Workspace agent governance platform은 `canonical core + provider adapter + validation evidence`
모델을 사용한다. Durable policy는 `docs/00.agent-governance/**`가 소유하고, shared skills,
workflows, output styles는 `.agents/**`가 소유하며, provider runtime files는 native syntax와
hook/event wiring만 표현한다.

## Boundaries & Non-goals

- **Owns**:
  - Stage 00 governance core and stage routing rules.
  - Provider adapter ownership model for Claude, Codex, and Gemini.
  - Shared skill/workflow/output-style SSoT boundaries.
  - Task-to-skill routing and external skill gap recording.
  - Memory/progress and task evidence requirements.
  - Repo-static validation expectations for governance changes.
- **Consumes**:
  - `docs/99.templates` stage templates.
  - Provider-native runtime files under `.claude/**`, `.codex/**`, and `.agents/**`.
  - Repository quality gate scripts and CI workflows.
  - Existing WSL2/k3d/ArgoCD platform docs as infrastructure context.
- **Does Not Own**:
  - Kubernetes desired-state semantics under `gitops/**`.
  - Live k3d, ArgoCD, Vault, ESO, PostgreSQL, or Valkey runtime state.
  - Secret values or external credential material.
  - Provider-specific commercial model availability.
- **Non-goals**:
  - New provider runtime creation.
  - HADS migration or template replacement.
  - CI topology redesign.
  - Historical evidence rewrite.

## Quality Attributes

- **Performance**: Governance loading stays just-in-time; agents do not need to read the full repository before every task.
- **Security**: Stage 00 preserves no-secret, no-direct-live-mutation, least-privilege, and explicit approval boundaries.
- **Reliability**: Provider adapters import stable Stage 00 contracts instead of duplicating policy that can drift.
- **Scalability**: New skills, workflows, output styles, and provider adapters are added through cataloged ownership and validation evidence.
- **Observability**: Plan/task records and `memory/progress.md` preserve command evidence, limitations, and handoff state.
- **Operability**: Repository quality gates and README indexes make governance drift discoverable before PR handoff.

## System Overview & Context

The governance architecture has five layers:

| Layer | Canonical Owner | Adapter / Consumer | Evidence |
| --- | --- | --- | --- |
| Stage 00 Core | `docs/00.agent-governance/**` | Root gateways and provider notes | Quality gate and task records |
| Template Contract | `docs/99.templates/**`, Stage 00 routing rules | Doc-writing agents and hooks | Template conformance checks |
| Shared Assets | `.agents/{skills,workflows,output-styles}/` | `.claude` and `.codex` symlink views | Harness catalog and repo checks |
| Provider Runtime | `.claude/**`, `.codex/**`, `.agents/**` | Claude, Codex, Gemini sessions | Provider docs and config parse checks |
| Validation Evidence | `docs/04.execution/tasks/**`, `memory/progress.md`, scripts | Maintainers and CI | Static validation output |

## Data Architecture

- **Key Entities / Flows**:
  - User task -> Stage 00 JIT loading -> scope/provider routing -> skill selection -> Plan/Task evidence -> validation summary.
  - New authored document -> `docs/99.templates` mapping -> stage README index -> related upstream/downstream links.
  - Provider runtime change -> harness catalog/model policy check -> provider config update -> quality gate evidence.
- **Storage Strategy**:
  - Durable rules live in Markdown under `docs/00.agent-governance/**`.
  - Shared runtime assets live in `.agents/**`.
  - Provider-native runtime files live under `.claude/**`, `.codex/**`, and `.agents/**`.
  - Execution evidence lives in `docs/04.execution/**` and `docs/00.agent-governance/memory/progress.md`.
- **Data Boundaries**:
  - Memory is supporting context, not an instruction source that overrides Stage 00.
  - Secret values, credentials, private keys, private runtime DBs, and shell history are outside the readable/output boundary unless explicitly approved and required.

## Infrastructure & Deployment

- **Runtime / Platform**:
  - Repository-local WSL2/k3d/ArgoCD GitOps workspace with three AI agent provider surfaces.
- **Deployment Model**:
  - Governance is deployed as repository content and validated through static scripts and CI.
  - Provider hooks are event wiring surfaces; only provider-native permission systems can act as native permission gates.
- **Operational Evidence**:
  - `scripts/validate-repo-quality-gates.sh .`
  - `bash scripts/generate-llm-wiki-index.sh --check`
  - `git diff --check`
  - Targeted `rg` checks for traceability and stale routing.

## AI Agent Architecture Requirements (If Applicable)

- **Model/Provider Strategy**:
  - Model tiers and provider-specific concrete IDs are owned by Stage 00 model policy and harness catalog.
  - Provider runtime files declare models from the canonical mapping and do not create separate tier names.
- **Tooling Boundary**:
  - Provider tools may differ, but all agents honor the same GitOps-first, template-first, QA/CI/CD, and approval boundaries.
  - Codex and Gemini hook configs are event wiring, not native permission gates equivalent to Claude settings.
- **Memory & Context Strategy**:
  - `memory/progress.md` records repo-changing work, reusable memory, limitations, and validation evidence.
  - Current repository files remain authoritative when memory conflicts with current state.
- **Guardrail Boundary**:
  - Direct live cluster mutation, secret value exposure, destructive git, CI topology changes, and model-policy changes from unverified assumptions require explicit human approval.
- **Latency / Cost Budget**:
  - Not a runtime service budget. Agents should use JIT loading and scoped validation to keep governance work bounded.

## Related Documents

- **PRD**: [../../01.requirements/2026-06-01-workspace-agent-governance-platform.md](../../01.requirements/2026-06-01-workspace-agent-governance-platform.md)
- **ADR**: [../decisions/0013-stage-00-canonical-adapter-model.md](../decisions/0013-stage-00-canonical-adapter-model.md)
- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../../04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md](../../04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Task**: [../../04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md](../../04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Governance Hub**: [../../00.agent-governance/README.md](../../00.agent-governance/README.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
- **Model Policy**: [../../00.agent-governance/model-policy.md](../../00.agent-governance/model-policy.md)
- **Template README**: [../../99.templates/README.md](../../99.templates/README.md)
