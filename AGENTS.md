# Agent Framework Contract

Shared cross-agent contract for the `hy-home.k8s` repository. This file serves as the **Explicit Trigger** for all AI Agent rules.

## 1. Rule-Based Entrypoint

This repository uses a **Lazy Loading Protocol**. Agents MUST NOT load all instructions into memory. Instead, identify the relevant **Rule** or **Scope** based on the current user intent.

- **Unified Gateway**: [agent-instructions.md](docs/00.agent/agent-instructions.md)
- **Detailed Guidelines**:
  - [Coding Conventions & Standards](docs/00.agent/conventions.md)
  - [Development Workflows](docs/00.agent/workflows.md)

## 2. Core Directives

- **Greedy Autonomy**: Use any available skill proactively to fulfill requests.
- **Metadata Compliance**: All docs MUST include `layer:` metadata.
- **Spec-First**: Code changes require an approved spec in `docs/specs/`.
- **Validation**: Run `pre-commit run --all-files` before commit.

## 3. Documentation Architecture

All documentation follows a **type-first, flattened hierarchy** in `docs/`. Execution documents use **plural paths** (`specs/`, `plans/`, `runbooks/`).
