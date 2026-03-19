---
title: 'ADR 0005: Normalized Documentation and Agent Entrypoints'
status: 'Accepted'
date: '2026-03-15'
authors: ['buenhyden']
deciders: ['buenhyden']
tags: ['adr', 'architecture']
layer: 'architecture'
---

# ADR: Normalized Documentation and Agent Entrypoints - 0005

- **Status**: Active
- **Owner**: buenhyden
- **Last Reviewed**: 2026-03-16
- **layer:** meta

**Overview (KR):** 파편화된 문서들을 하나의 표준(Flat hierarchy, Metadata compliance, Naming convention)으로 통합하고 검증하는 최종 프로세스를 정의합니다.

## Context

The repository had fragmented documentation paths and bloated agent entrypoints (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`). To improve AI agent performance and maintainability, a more structured and modular approach was needed.

## Decision

1. **Directory Normalization**:
   - `docs/incidents/` moved to `docs/operations/incidents/`.
   - `docs/operations/postmortems/` established.
   - Strictly unified documentation directories: `adr`, `ard`, `prd`, `specs`, `plans`, `runbooks`, `operations`.
2. **Metadata Enforcement**:
   - Mandatory `layer:` metadata in all markdown files frontmatter.
3. **Agent Shimming**:
   - Root `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` are now lightweight shims that delegate to `docs/agentic/`.
   - Implement Lazy Loading of instructions based on task scope.

## Rationale

- Modular instructions reduce token consumption and context bloat.
- Consistent paths enable reliable search and automation by both humans and agents.
- `layer:` metadata allows for easier documentation categorization and automated linting.

## Consequences

- Agents must now identify their task scope to load the correct instructions.

## Related Documents

- [ADR 0001: k3d Local Cluster](./0001-k3d-local-cluster.md)
- [ADR 0002: ArgoCD GitOps](./0002-argocd-gitops.md)
