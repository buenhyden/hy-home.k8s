---
layer: "meta"
---
# Architecture Reference Document: Documentation System

## 1. System Overview

The documentation system is a flattened, type-based taxonomy designed for high discoverability and optimized AI agent context management.

## 2. Directory Structure

All documents are organized by type at the root `docs/` level:

- `adr/`: Architecture Decision Records
- `ard/`: Architecture Reference Documents
- `prd/`: Product Requirements Documents
- `specs/`: Technical Specifications
- `plans/`: Phased Execution Plans
- `runbooks/`: Operational Procedures
- `operations/`: Operational Strategies and Team Manuals

## 3. Mandatory Metadata

Every markdown file MUST include YAML frontmatter with a `layer` key identifying its domain (e.g., `infra`, `gitops`, `app`, `ops`, `meta`).

## 4. Agent Integration

AI agents use a lazy-loading protocol defined in `AGENTS.md` to load instructions scoped to the active documentation path, minimizing token usage and cross-task pollution.
