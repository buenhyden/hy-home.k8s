# Agent Framework Contract

Shared cross-agent contract for the `hy-home.k8s` repository. This file is the **Explicit Trigger** for all AI Agent rules.

## 1. Lazy Loading Protocol

Agents MUST NOT load all instructions into memory. Identify the **Intent** and load the corresponding **Scope**.

- **Instruction Gateway**: [agent-instructions.md](docs/00.agent/agent-instructions.md)
- **Global Persona**: [global-persona.md](docs/00.agent/rules/global-persona.md)

## 2. Shared Directives

- **Spec-First**: Code changes require an approved spec in `docs/04.specs/`.
- **Metadata**: All docs MUST include `layer:` metadata.
- **Verification**: Run `pre-commit run --all-files` before commit.

## 3. Scope Index

- **PRD/ARD**: `docs/00.agent/scopes/prd.md`
- **Specs/Plans**: `docs/00.agent/scopes/specs.md`
- **Ops/Incidents**: `docs/00.agent/scopes/operations.md`
