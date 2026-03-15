---
layer: "meta"
---
# Contributing Guidelines

## Necessity & Required Content

This document defines the mechanical steps required to successfully merge code into this repository. It enforces the spec-driven contribution model.

**What is Required**:

- **Layer Metadata**: All documentation MUST include `layer:` metadata.
- **Spec-First**: Code without an approved Spec in `docs/specs/` is prohibited.
- **Templates**: All project documents MUST use `templates/`.

## 1. Spec-Driven Core Rule

All development—infrastructure OR application—**MUST** begin with a specification in `docs/specs/`.

> [!CAUTION]
> Pull Requests containing code without an approved, corresponding implementation plan or specification will be **automatically rejected** by the Reviewer Agent.

## 2. Template Enforcement

You **MUST** use the canonical templates in `templates/` for all project documentation.

- **ADR**: Use `templates/adr-template.md`.
- **Runbook**: Use `templates/runbook-template.md`.
- **PRD**: Use `templates/prd-template.md`.
- **Spec**: Use `templates/spec-template.md`.

## 3. Quality Gates (Pre-PR Check)

Before submitting a Pull Request, Ensure:

1. **Tests**: Unit and Integration tests pass (colocated in source or in `tests/`).
2. **Linting**: Run `pre-commit run --all-files`.
3. **Coverage**: Maintain the baseline project coverage (**> 80%**).
4. **Security**: Adhere to `docs/agentic/rules/core.md` regarding secure coding.

## 4. Pull Request Process

1. **Branching**: Use `feature/XXX`, `fix/XXX`, or `docs/XXX`.
2. **Commits**: Follow Conventional Commits via `.gitmessage`.
3. **Traceability**: Every PR MUST reference its approved Spec file in `docs/specs/`.

## 5. AI Reviewer Interaction

Address all comments from the AI Reviewer Agent. If a comment is incorrect due to a spec discrepancy, correct the spec first.

## 6. Essential References

- **Roles**: `AGENTS.md`
- **Handoffs**: `COLLABORATING.md`
- **Architecture**: `ARCHITECTURE.md`
- **Conduct**: `CODE_OF_CONDUCT.md`
