---
title: 'Reference: Agent Reference Index'
type: content/reference
status: active
owner: platform
updated: 2026-07-03
---

# Reference: Agent Reference Index

## Overview

이 문서는 기능 하나에 묶이지 않는 Agent 관련 참고 자료의 data-category
경계를 정의한다. Agent 메모리, 컨텍스트, 오케스트레이션 같은 durable
concept는 reference data로 관리할 수 있지만, runtime policy와 provider
execution rule은 Stage 00 governance가 소유한다.

기능 또는 서비스에 종속된 Agent 설계는 이 문서가 아니라
`docs/03.specs/<feature-id>/agent-design.md`가 정본 위치다.

## Purpose

이 문서는 `90.references/data/` 아래에 둘 수 있는 Agent reference data와
Stage 00 또는 Stage 03으로 라우팅해야 하는 Agent runtime contract를
구분한다.

## Reference Type

- Type: durable-concept / data-catalog
- Source checked: 2026-07-03
- Refresh trigger: Agent reference document addition, runtime roster movement,
  provider adapter change, or Stage 00 routing change.

## Authority Boundary

- **Authoritative for**:
  - Durable Agent reference data category boundaries.
  - Routing reusable Agent concepts away from active runtime policy.
  - Identifying canonical owners for runtime roster and feature-local design.
- **Not authoritative for**:
  - Runtime roster, provider behavior, hook permissions, model routing, or
    execution rules.
  - Feature-local Agent behavior contracts.
  - Subagent dispatch, tool permission, or live runtime enforcement.

## Scope

- Covers reusable Agent memory, context, orchestration, and reference-catalog
  concepts that are not tied to one feature.
- Excludes runtime policy, provider notes, hook wiring, model policy,
  execution permissions, and task-specific implementation evidence.

## Definitions / Facts

- **Runtime governance owner**: `docs/00.agent-governance/**`.
- **Runtime roster owner**: `docs/00.agent-governance/harness-catalog.md`.
- **Feature-local Agent design owner**: `docs/03.specs/<feature-id>/agent-design.md`.
- **Repo-changing progress owner**: `docs/00.agent-governance/memory/progress.md`.
- **Reference data owner**: `docs/90.references/data/**` for durable lookup
  facts that do not redefine runtime behavior.

## Sources

- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [Document Stage Routing Rules](../../00.agent-governance/rules/document-stage-routing.md)
- [Template Routing](../../99.templates/support/template-routing.md)
- [Data README](./README.md)

## Review and Freshness

- Review cadence: on Agent reference addition, provider adapter change, or
  Stage 00 runtime governance change.
- Last reviewed: 2026-07-03.
- Next review trigger: a PR that changes `.claude/agents/**`,
  `.codex/agents/**`, `.agents/agents/**`, `docs/00.agent-governance/**`, or
  `docs/03.specs/**/agent-design.md` routing.

## Related Documents

- [90.references README](../README.md)
- [Data README](./README.md)
- [Agent Governance Hub](../../00.agent-governance/README.md)
- [Harness Catalog](../../00.agent-governance/harness-catalog.md)
- [03.specs README](../../03.specs/README.md)
- [Reference Maintenance Runbook](../../05.operations/runbooks/0011-reference-maintenance-runbook.md)
