---
title: 'Product Requirements Document (PRD): Documentation and Agent Instruction System'
status: 'Approved'
target_version: 'v1.0.0'
owner: 'buenhyden'
stakeholders: ['buenhyden']
tags: ['prd', 'meta']
layer: 'meta'
---

# Product Requirements Document (PRD): Documentation and Agent Instruction System

- **Status**: Approved
- **Target Version**: v1.0.0
- **Owner**: buenhyden
- **Stakeholders**: buenhyden
- **Scope**: master
- **layer:** meta

**Overview (KR):** AI 에이전트와 인간 운영자 간의 원활한 협업을 위한 저장소 문서 체계 및 자동화 지침 시스템의 요구사항을 정의합니다.

## 1. Goal

Establish a high-trust, low-overhead documentation and automation framework that enables both human operators and AI agents to maintain a complex Kubernetes homelab with zero ambiguity.

## 2. Requirements

- **REQ-001: Flattened Taxonomy**: All documentation MUST reside in type-specific directories under `docs/` (e.g., `docs/prd/`, `docs/specs/`).
- **REQ-002: Layer Metadata**: Every markdown file MUST include `layer:` in its YAML frontmatter (e.g., `infra`, `gitops`, `app`, `meta`).
- **REQ-003: Rule-Based Lazy Loading**: AI agents MUST load instructions based on the active `rule` defined in `docs/agentic/rules/`. Each rule maps to a specific `scope` in `docs/agentic/scopes/`.
- **REQ-004: Proactive and Absolute Skill Use**: Agents MUST proactively use any available skill in the runtime without restriction. Skill selection should be guided by the task, not by restricted lists.
- **REQ-005: Taxonomy Alignment**: Documentation MUST be organized into exactly `adr, ard, prd, specs, plans, runbooks, operations` directories under `docs/`.
- **REQ-006: Layer Metadata**: Every markdown file MUST include `layer:` in its YAML frontmatter.

## Related Documents

- [docs/ard/2026-03-16-documentation-system-ard.md](../ard/2026-03-16-documentation-system-ard.md)
- [docs/specs/2026-03-16-documentation-system-spec.md](../specs/2026-03-16-documentation-system-spec.md)
