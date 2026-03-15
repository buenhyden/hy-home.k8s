---
title: 'Documentation Refactor Specification'
status: 'Canonical'
version: '1.0'
owner: 'buenhyden'
scope: 'master'
prd_reference: '../prd/documentation-refactor-prd.md'
arch_reference: '../ard/documentation-architecture-ard.md'
decision_reference: '../adr/0001-documentation-refactor-decision.md'
tags: ['spec','implementation']
layer: 'meta'
---

# Documentation Refactor Specification

> **Status**: Canonical
> **Scope**: master
> **layer:** meta
> **Related PRD**: `[../prd/documentation-refactor-prd.md]`
> **Related Architecture**: `[../ard/documentation-architecture-ard.md]`
> **Decision Record**: `[../adr/0001-documentation-refactor-decision.md]`

**Overview (KR):** 기존 루트 문서와 AI Agent 설정 파일들을 March 2026 기준의 통합 지침으로 개편하는 기술 명세서입니다.

## Technical Baseline

The baseline consists of several root markdown files (`ARCHITECTURE.md`, `README.md`, etc.) and a nascent instruction set in `docs/agentic/`.

## Contracts

- **Metadata Contract**: Every markdown file MUST contain `layer: "meta" | "infra" | "gitops" | "app" | "ops"`.
- **Path Contract**: Execution plans MUST live in `docs/plans/`; Specs in `docs/specs/`.

## Verification

```bash
# Verify metadata
grep -r "layer:" .

# Verify plural paths
ls docs/plans
ls docs/specs
```

## 1. Technical Overview

This refactor involves overwriting root files to remove bloat and consolidate behavioral logic into `docs/agentic/agent-instructions.md`.

## 5. Component Breakdown

- **`AGENTS.md`**: Lightweight rule trigger.
- **`CLAUDE.md` / `GEMINI.md`**: Model-specific gateway triggers.
- **`docs/agentic/agent-instructions.md`**: Rule-to-scope mapping table.
- **`ARCHITECTURE.md`**: Policy for SDD and flattened structure.
