---
title: 'Documentation and Agent Instruction Refactor Execution Plan'
status: 'Proposed'
version: 'v1.0.0'
layer: 'common'
---

# Documentation and Agent Instruction Refactor Execution Plan

## 1. Overview

This document defines the atomic steps required to execute the documentation refactor and instruction optimization.

## 2. Phase 1: Directory & Metadata Hardware

1. **[ ]** Verify existance of `docs/operations/incidents/` and `docs/operations/postmortems/`.
    - `mkdir -p docs/operations/incidents docs/operations/postmortems`
2. **[ ]** Add `layer: "meta"` to:
    - `index.md`
    - `ARCHITECTURE.md`
    - `CONTRIBUTING.md`
    - `COLLABORATING.md`
    - `CODE_OF_CONDUCT.md`
    - `OPERATIONS.md`
3. **[ ]** Update all internal links in root MDs to use plural paths (e.g., `docs/plans/` instead of `docs/plan/`).

## 3. Phase 2: Instruction Refactor (Lazy Loading)

1. **[ ]** Optimize `AGENTS.md` and root `CLAUDE.md`/`GEMINI.md`.
2. **[ ]** Refactor `docs/agentic/agent-instructions.md` with the new intent-to-scope mapping.
3. **[ ]** Review and condense `docs/agentic/rules/` and `docs/agentic/scopes/` files.

## 4. Phase 3: Final Verification

1. **[ ]** Validate all relative links.
2. **[ ]** Verify template adherence.
3. **[ ]** Confirm `layer` metadata presence.
