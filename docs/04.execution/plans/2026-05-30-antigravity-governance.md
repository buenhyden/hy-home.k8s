---
title: 'Antigravity Governance Implementation Plan'
type: sdlc/plan
status: done
owner: platform
updated: 2026-06-02
---

# Antigravity Governance Implementation Plan

---

## Overview

This document is the implementation plan for reviewing and updating the common
AI Agent governance defined under `docs/00.agent-governance/**` against the
workspace purpose, then using that result to reorganize Antigravity-specific
harness and tool surfaces such as `.agents/**` and `GEMINI.md`.

## Context

The purpose is to give Gemini (Antigravity) agents a specialized harness for
the `hy-home.k8s` repository that matches the workspace purpose. The key focus
is clarifying the model policy (Gemini 3.1 Pro / Gemini 3.5 Flash) and
Template Contract routing.

## Goals & In-Scope

- **Goals**: Align Antigravity (Gemini) workspace rules and workflows with common governance.
- **In Scope**:
  - Update `docs/00.agent-governance/providers/gemini.md`
  - Update `.agents/GEMINI.md`
  - Create `.agents/rules/workspace-rules.md`
  - Create `.agents/workflows/qa-cicd-workflow.md`

## Work Breakdown

| Task    | Description | Files / Docs Affected | Target REQ | Validation Criteria |
| ------- | ----------- | --------------------- | ---------- | ------------------- |
| PLN-001 | Update common governance | `docs/00.agent-governance/providers/gemini.md` | GOV-01 | Harness structure and policy added |
| PLN-002 | Update the local baseline | `.agents/GEMINI.md` | GOV-02 | Template Contract and workflow documented |
| PLN-003 | Create dedicated rules | `.agents/rules/workspace-rules.md` | GOV-03 | Template-first content written |
| PLN-004 | Create dedicated workflow | `.agents/workflows/qa-cicd-workflow.md` | GOV-04 | QA/CI/CD phases defined |

## Verification Plan

| ID          | Level      | Description | Command / How to Run | Pass Criteria |
| ----------- | ---------- | ----------- | -------------------- | ------------- |
| VAL-PLN-001 | Structural | File existence | `ls -l .agents/rules/` | `workspace-rules.md` is present |
| VAL-PLN-002 | Content | Model policy is documented | `grep "Gemini 3.1 Pro" .agents/GEMINI.md` | Output exists |

## Completion Criteria

- [x] Scoped work completed
- [x] Verification passed
- [x] Required docs updated

### Current-State Closure (2026-06-02)

This plan is closed as done. Its scoped Gemini/Antigravity files exist, and
the current workspace-wide adapter contract is owned by ADR-0013 and the Stage
00 canonical adapter workstream. No remaining redesign scope is carried here.

## Related Documents

- **Tasks**: `[../tasks/2026-05-30-antigravity-governance.md]`

## Non-Goals & Out-of-Scope

- N/A

## Risks & Mitigations

- N/A
