---
title: 'Documentation and Agent Instruction Refactor Spec'
status: 'Validated'
version: 'v1.0.0'
layer: 'meta'
---

# Documentation and Agent Instruction Refactor Spec

**Overview (KR):** 리포지토리의 기본 구조와 AI 에이전트가 준수해야 할 기술적 파운데이션에 대한 명세를 정의합니다.

## 1. Goal

Technically implement the refactoring of root documentation and the transition to a low-token Lazy Loading instruction system.

## 2. Specification

### 2.1 Instruction Gateway Refactor

- **File**: `docs/agentic/agent-instructions.md`
- **Change**: Implement a condensed mapping table.
- **Rules**:
  - Remove redundant explanations.
  - Standardize intent naming.

### 2.2 Root File Hardening

- **Targets**: `index.md`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `COLLABORATING.md`, `CODE_OF_CONDUCT.md`, `OPERATIONS.md`.
- **Change**:
  - Verify all internal links against plural paths.
  - Insert missing `layer: "meta"` metadata where absent.
  - Consolidate common "Necessity" and "Required Content" sections.

### 2.3 Directory Structure Cleanup

- **Action**: Create subdirectories `docs/operations/incidents/` and `docs/operations/postmortems/` if missing.
- **Action**: Move existing incident/postmortem logs into these directories.

### 2.4 Entry Point Optimization

- **Files**: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`.
- **Change**: Reduce to absolute minimum pointers to the Gateway.

## 3. Verification Logic

| Step | Command / Check | Expected Result |
| --- | --- | --- |
| 1 | `ls docs/plans/` | `2026-03-16-refactor-baseline-plan.md` exists |
| 2 | `grep "layer:" ARCHITECTURE.md` | Match found |
| 3 | `grep "/plans/" index.md` | Correct relative link found |
| 4 | Token Count | `agent-instructions.md` + 1 Rule + 1 Scope < 15k tokens |

## 4. Traceability

- **REQ-REF-01** (Lazy Loading) -> Section 2.1
- **REQ-REF-02** (Plural Paths) -> Section 2.2
- **REQ-REF-03** (Layer Meta) -> Section 2.2
