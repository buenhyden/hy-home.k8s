---
layer: "meta"
---
# Root Instruction Refactor Plan

> **Status**: Completed
> **Scope**: domain

**Overview (KR):** 이 계획은 루트 에이전트 지침 파일을 점검해 중복을 줄이고, 공통 규칙은 `.claude/` 계층으로 위임하며, 루트 파일은 빠른 진입점과 우선순위만 남기도록 정리하기 위한 것이다.

## Context & Introduction

This repository already uses `.claude/` as the shared detailed instruction layer and scoped instruction files under `docs/` for subtree-specific behavior. The root `CLAUDE.md` and `GEMINI.md` are already thin loaders, while `AGENTS.md` still carries duplicated material that overlaps with `.claude/governance.md`, `.claude/repo-navigation.md`, and `.claude/rules/*`.

This plan records the refactor so the resulting root files stay concise, preserve verified repo facts, and keep progressive disclosure intact.

## Tasks

| Task | Description | Files Affected | Target REQ | Validation Criteria |
| ---- | ----------- | -------------- | ---------- | ------------------- |
| TASK-001 | Audit root instruction files against existing `.claude/` guidance and identify root-only essentials | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.claude/README.md`, `.claude/governance.md`, `.claude/repo-navigation.md`, `.claude/rules/core.md`, `.claude/rules/docs-map.md`, `.claude/rules/personas.md`, `.claude/rules/repo-navigation.md` | REQ-001 | Duplication and missing cross-links identified from inspected files only |
| TASK-002 | Refactor `AGENTS.md` into a concise cross-agent index with verified commands, precedence, and durable links | `AGENTS.md` | REQ-002 | Root file remains concise and preserves repo-specific universal rules |
| TASK-003 | Tighten `CLAUDE.md` and `GEMINI.md` so they stay as minimal runtime loaders with explicit root-contract links | `CLAUDE.md`, `GEMINI.md` | REQ-003 | Both loaders remain minimal and clearly delegate to `.claude/` entrypoints |
| TASK-004 | Verify the edited files for path correctness and linkable references | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | REQ-004 | All referenced repo-relative paths exist and no invented commands are introduced |

## Verification

- `[VAL-001]` Re-read `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` to confirm the files preserve repo-specific constraints and use repo-relative links only.
- `[VAL-002]` Run `rg --files` checks for referenced `.claude/` and `docs/` targets to confirm the links resolve.
- `[VAL-003]` Confirm the root files do not introduce unverified build, test, or package-manager commands.

## References

- `[../../AGENTS.md]`
- `[../../CLAUDE.md]`
- `[../../GEMINI.md]`
- `[../agentic/README.md]`
- `[../agentic/governance.md]`
- `[../agentic/lifecycle.md]`
- `[../agentic/repo-navigation.md]`
