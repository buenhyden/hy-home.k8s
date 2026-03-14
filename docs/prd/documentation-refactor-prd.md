---
layer: "meta"
---
# PRD: Documentation Taxonomy and Agent Instruction Refactor

## 1. Product Overview

Refactor the project's documentation structure to ensure scalability, ease of navigation, and deterministic AI agent behaviors. This includes flattening the taxonomy and implementing a lazy-loading instruction system.

## 2. Success Metrics

- 100% of documents in `docs/` have `layer` metadata.
- Zero "retired" guides remain in `docs/guides/` (moved to `docs/manuals/`).
- AI Agent instruction loading follows explicit trigger rules.

## 3. User Stories

- **As an operator**, I want a clear documentation structure so that I can easily find the information I need.
- **As an AI Agent**, I want modular instructions so that I can stay focused on the task without being overwhelmed by irrelevant context.

## 4. Features & Requirements

- **Flat Taxonomy**: Use `docs/prd`, `docs/specs`, etc. as flat directories.
- **Metadata Enforcement**: Mandatory `layer` key in all files.
- **Lazy Loading**: Instructions in `docs/agentic/` are loaded based on rules defined in a root dispatcher.
- **Retired Content Migration**: Move checklists from `docs/guides/` to `docs/manuals/`.

## 5. Scope

- Root documentation files (`README.md`, `ARCHITECTURE.md`, etc.)
- All subdirectories under `docs/`.
- Instruction layer in `docs/agentic/`.
- Root agent contract `AGENTS.md`.
