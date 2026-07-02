---
title: 'ADR-0013: Stage 00 Canonical Adapter Model'
type: sdlc/adr
status: accepted
owner: platform
updated: 2026-06-01
---

# ADR-0013: Stage 00 Canonical Adapter Model

## Overview

이 ADR은 `hy-home.k8s`의 AI Agent governance를 Stage 00 단일 공통 governance로 유지하고,
provider별 파일은 native adapter 또는 symlink/mirror view로 유지한다는 결정을 기록한다.

## Context

Claude, Codex, Gemini는 같은 워크스페이스에서 같은 SDD lifecycle, QA/CI/CD, Template Contract,
Model Policy, GitOps-first guardrail을 따라야 한다. 그러나 각 provider는 서로 다른 native file
format, hook support, agent config, permission surface를 가진다. Provider별 문서가 durable
policy를 복제하면 같은 규칙이 서로 다른 표현으로 drift될 수 있으므로, 정본과 adapter 책임을
분리하는 결정이 필요하다.

## Decision

- Stage 00 (`docs/00.agent-governance/**`)을 workspace-wide canonical governance core로 둔다.
- Durable policy, scope rules, checklist, template routing, model/tier vocabulary, QA/CI/CD contract는 Stage 00이 소유한다.
- Shared skills, workflows, and output styles는 `.agents/{skills,workflows,output-styles}/`를 SSoT로 둔다.
- `.claude/skills`, `.claude/workflows`, `.claude/output-styles`, `.codex/skills`, `.codex/workflows`, `.codex/output-styles`는 `.agents/**` symlink view로 유지한다.
- Provider-native agent files는 provider별 real files로 유지한다:
  - Claude: `.claude/agents/*.md`
  - Codex: `.codex/agents/*.toml`
  - Gemini: `.agents/agents/*.md`
- Hook scripts are shared under `docs/00.agent-governance/hooks/*.sh`; provider hook configs are event wiring surfaces.
- Work evidence belongs in `docs/04.execution/tasks/**` and `docs/00.agent-governance/memory/progress.md`, not in provider-specific hidden ledgers.

## Explicit Non-goals

- Creating independent Claude, Codex, or Gemini governance models.
- Replacing `docs/99.templates` with HADS or another external documentation standard.
- Changing Kubernetes desired state, live cluster state, or external service runtime state.
- Changing GitHub Actions topology as part of this decision.
- Rewriting historical plan/task evidence.

## Consequences

- **Positive**:
  - One Stage 00 governance model controls common policy and reduces provider drift.
  - Provider adapters remain thin and can express runtime-specific syntax without duplicating durable rules.
  - Shared skills/workflows/output styles stay byte-identical through `.agents` SSoT and symlink views.
  - Repository validators can check catalog, hook, template, and provider config drift as static evidence.
- **Trade-offs**:
  - Provider-native support differs; Codex and Gemini may honor some contracts behaviorally where Claude has native permission or output-style support.
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
  - Codex and Gemini would become secondary copies instead of first-class adapters.
  - The workspace would no longer express a provider-agnostic governance core.

### Docs-only policy without validation evidence

- Good:
  - Simpler documentation structure.
- Bad:
  - No objective guard against stale hook paths, model IDs, template routing, or provider mirror drift.
  - Completion would rely on intent instead of repo-backed evidence.

## Agent-related Example Decisions (If Applicable)

- Model selection is governed by Stage 00 model policy and harness catalog, not provider-local preference.
- Tool gating is provider-native where supported and behavioral otherwise; all providers still follow the same approval boundaries.
- Guardrail strategy favors static validation and task evidence before final handoff.
- Planner/executor separation follows SDD stage routing: requirements and architecture upstream, plan/task execution downstream.
- Fallback model or skill choices require explicit gap recording when the requested external capability is missing.

## Related Documents

- **PRD**: [../../01.requirements/2026-06-01-workspace-agent-governance-platform.md](../../01.requirements/2026-06-01-workspace-agent-governance-platform.md)
- **ARD**: [../requirements/0006-workspace-agent-governance-platform.md](../requirements/0006-workspace-agent-governance-platform.md)
- **Spec**: [../../03.specs/006-workspace-harness-gap-analysis/spec.md](../../03.specs/006-workspace-harness-gap-analysis/spec.md)
- **Plan**: [../../04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md](../../04.execution/plans/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Task**: [../../04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md](../../04.execution/tasks/2026-06-01-stage-00-canonical-adapter-redesign.md)
- **Governance Hub**: [../../00.agent-governance/README.md](../../00.agent-governance/README.md)
- **Harness Catalog**: [../../00.agent-governance/harness-catalog.md](../../00.agent-governance/harness-catalog.md)
