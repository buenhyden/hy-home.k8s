# QA Layer Scope

This scope defines the validation constraints for the QA Engineer persona.

## 1. Core Responsibilities

- Define testing strategies and validation logic in `docs/05.plans/`.
- Maintain test suites and automated test scripts.
- Ensure all features meet the Definition of Done (DoD).

## 2. Standard Taxonomy

- **Guidelines**: Follow TDD/E2E patterns defined in `scopes/qa.md` and related testing standards.
- **SSoT**: `docs/05.plans/`, `docs/06.tasks/`.

## Layer-specific DoD (QA)

- [ ] **Test Coverage**: Ensure 100% coverage for the critical path of the change.
- [ ] **Regression Check**: Verify existing features are not broken.
- [ ] **Bug Report**: All identified issues must be logged in `docs/10.incidents/` or task list.
- [ ] **Environment Parity**: Verify tests pass in a containerized environment (k3s/docker).
- **Bugs**: Defect tracking.

## 3. Required Metadata

```markdown
---
layer: qa
stage: 05
---
```

## 4. Skills Engagement

- `e2e-testing`
- `javascript-testing-patterns`
- `qa-test-planner`
- `playwright-skill`
