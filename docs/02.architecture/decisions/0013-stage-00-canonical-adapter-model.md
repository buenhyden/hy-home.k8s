---
title: "Stage 00 Canonical Adapter Model"
version: "1.0.0"
type: "sdlc/architecture-decision"
status: "superseded"
owner: "platform"
updated: "2026-08-28"
layer: "architecture"
artifact_id: "ADR-0013"
superseded_by: "ADR-0030"
---

# ADR-0013: Stage 00 Canonical Adapter Model

## Overview

Superseded by [ADR-0030](0030-authority-first-sdlc-and-agent-governance-convergence.md).
The historical decision below is retained; its provider and custom-hook model
is no longer current authority.

이 ADR은 `hy-home.k8s`의 AI Agent governance를 Stage 00 단일 공통 governance로 유지하고,
provider별 native adapter, local adapter, 또는 symlink view를 명시적으로 구분한다는 결정을 기록한다.

## Context

Claude, Codex, local/Antigravity adapter는 같은 워크스페이스에서 같은 SDD lifecycle,
QA/CI/CD, Template Contract, Model Policy, GitOps-first guardrail을 따라야 한다. 이 ADR의
최초 승인 시점에는 Gemini native project 파일이 없었으나, 현재 저장소에는
`.gemini/agents/**`와 `.gemini/settings.json`이 tracked repo-static adapter surface로
존재한다. 이 파일 존재는 Gemini가 이를 native하게 발견·파싱하거나 event/tool policy를
강제했다는 증거가 아니며, 인증·실행·model resolution을 포함한 provider-runtime lane은
계속 `DEFER`이다. 각 runtime은 서로 다른 native/local file format, hook support,
agent config, permission surface를 가진다. Surface별 문서가 durable
policy를 복제하면 같은 규칙이 서로 다른 표현으로 drift될 수 있으므로, 정본과 adapter 책임을
분리하는 결정이 필요하다.

## Decision

- Stage 00 (`docs/00.agent-governance/**`)을 workspace-wide canonical governance core로 둔다.
- Durable policy, scope rules, checklist, template routing, model/tier vocabulary, QA/CI/CD contract는 Stage 00이 소유한다.
- Shared skills, workflows, and output styles는 `.agents/{skills,workflows,output-styles}/`를 SSoT로 둔다.
- `.claude/skills`, `.claude/workflows`, `.claude/output-styles`, `.codex/skills`, `.codex/workflows`, `.codex/output-styles`는 `.agents/**` symlink view로 유지한다.
- 역할 파일은 surface별 real files로 유지하되 native capability를 과장하지 않는다:
  - Claude: `.claude/agents/*.md`
  - Codex: `.codex/agents/*.toml`
  - Local/Antigravity: `.agents/agents/*.md`
- Gemini용 project adapter surface는 `.gemini/agents/**`와
  `.gemini/settings.json`에 tracked real file로 유지한다. 이는 현재 repo-static
  configuration evidence일 뿐이다. 최초 승인 시점의 native project surface 부재는
  historical observation으로 보존하며, 현재 파일의 native discovery/parsing,
  event/tool enforcement, authentication, execution, model resolution은 관찰되지
  않았으므로 provider-runtime lane에서 계속 `DEFER`한다. `.agents/**`도 Gemini CLI
  native consumption의 증거가 아니다.
- Hook scripts are shared under `docs/00.agent-governance/hooks/*.sh`;
  `.codex/hooks.json` and local `.agents/hooks.json` are context/validation
  wiring, while Claude native settings/hooks retain their documented runtime
  behavior. None establishes Gemini CLI native event delivery.
- Work evidence belongs in `docs/03.specs/tasks/**` and `docs/00.agent-governance/memory/progress.md`, not in provider-specific hidden ledgers.

### Agent decision application

- Model selection is governed by Stage 00 model policy and harness catalog, not provider-local preference.
- Tool gating is provider-native where supported and behavioral otherwise; all providers still follow the same approval boundaries.
- Guardrail strategy favors static validation and task evidence before final handoff.
- Planner/executor separation follows SDD stage routing: requirements and architecture upstream, plan/task execution downstream.
- Fallback model or skill choices require explicit gap recording when the requested external capability is missing.

## Explicit Non-goals

- Creating independent Claude, Codex, or Gemini governance models.
- Replacing `docs/99.templates` with HADS or another external documentation standard.
- Changing Kubernetes desired state, live cluster state, or external service runtime state.
- Changing GitHub Actions topology as part of this decision.
- Rewriting historical plan/task evidence.

## Consequences

- **Positive**:
  - One Stage 00 governance model controls common policy and reduces provider drift.
  - Adapter surfaces remain thin and can express surface-specific syntax without duplicating durable rules.
  - Shared skills/workflows/output styles stay byte-identical through `.agents` SSoT and symlink views.
  - Repository validators can check catalog, hook, template, and provider config drift as static evidence.
- **Trade-offs**:
  - Native support differs; Codex와 local/Antigravity surface는 일부 계약을
    Claude의 native permission/output-style과 다른 방식으로 적용한다. Gemini용
    tracked project adapter가 있더라도 native consumption과 provider-runtime
    readiness에는 별도의 discovery/authenticated canary evidence가 필요하다.
  - Updating shared assets can affect multiple provider views and therefore requires careful validation.
  - External requested skills must be recorded as strategy lenses or gaps rather than assumed to be local durable assets.

## Alternatives

### Provider-specific independent governance

- Good:
  - Each provider could optimize its own files and workflows independently.
- Bad:
  - Durable policy would drift across `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.codex/**`, and `.agents/**`.
  - QA/CI/CD and template contracts would become ambiguous for cross-provider work.

### Claude-centered single-provider model

- Good:
  - Claude-native settings, agents, hooks, and output styles have richer native enforcement.
- Bad:
  - Codex와 local/Antigravity adapter가 secondary copies가 되고, Gemini CLI
    native gap도 숨겨질 수 있다.
  - The workspace would no longer express a provider-agnostic governance core.

### Docs-only policy without validation evidence

- Good:
  - Simpler documentation structure.
- Bad:
  - No objective guard against stale hook paths, model IDs, template routing, or provider mirror drift.
  - Completion would rely on intent instead of repo-backed evidence.

## Traceability

### Lifecycle Traceability

| Decision lineage | Replacement relation | Affected Spec |
| --- | --- | --- |
| [ADR-0030](0030-authority-first-sdlc-and-agent-governance-convergence.md) | Superseded by ADR-0030. | [Spec 0054](../../03.specs/0054-sdlc-document-and-agent-governance-consolidation/spec.md) |

- **PRD**: [../../01.requirements/003-workspace-agent-governance-platform.md](../../01.requirements/0003-workspace-agent-governance-platform.md)
- **ARD**: [../requirements/0006-workspace-agent-governance-platform.md](../descriptions/0006-workspace-agent-governance-platform.md)
- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/0006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../../04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md](../../98.archive/README.md#document-index)
- **Task**: [Archive Index](../../98.archive/README.md#document-index)
- **Governance Hub**: [Current common governance](../../../.agents/README.md)
- **Agent Registry**: [Current role registry](../../../.agents/roles/registry.json)
