# Agentic Architecture

This directory is the shared detailed instruction layer for agent-facing work in this repository.

## Runtime Entry Points

- [claude-provider.md](claude-provider.md): Claude-native detailed instructions
- [gemini-provider.md](gemini-provider.md): Gemini-native detailed instructions
- [agent-instructions.md](agent-instructions.md): Intent-to-Scope mapping gateway
- [rules/](rules/): modular runtime rules (`bootstrap.md`, `persona-matrix.md`)
- [scopes/](scopes/): functional context scopes (backend, frontend, infra, etc.)

## Usage & Governance

- Root files (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`) stay thin and delegate here.
- Runtime-critical instructions live in the provider files and `rules/`.
- All internal documentation in this directory MUST be in English for model compatibility.

## Document Lifecycle

1. **Pre-Development**: Turn request into PRD (`01.prd`), Spec (`04.specs`), and Plan (`05.plans`).
2. **Implementation**: Implement against approved specs. Use TDD and frequent commits.
3. **Verification**: Verify against the Plan and requirements. Document evidence in `06.tasks`.

## Canonical Paths

- PRDs: `docs/01.prd/`
- ARDs: `docs/02.ard/`
- ADRs: `docs/03.adr/`
- Specs: `docs/04.specs/`
- Plans: `docs/05.plans/`
- Tasks: `docs/06.tasks/`
- Guides: `docs/07.guides/`
- Operations: `docs/08.operations/`
- Runbooks: `docs/09.runbooks/`
- Incidents: `docs/10.incidents/`
- Postmortems: `docs/11.postmortems/`

## Compliance

All documentation in this project follows the **01-11 Stage-Gate Taxonomy**.
