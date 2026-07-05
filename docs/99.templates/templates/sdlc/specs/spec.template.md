---
title: '{Feature Name} Technical Specification'
type: sdlc/spec
status: draft
owner: platform
updated: YYYY-MM-DD
---

<!-- Target: docs/03.specs/<###-Numbering>-<feature-id>/spec.md -->

# [Feature Name] Technical Specification (Spec)

> Use this template for `docs/03.specs/<###-Numbering>-<feature-id>/spec.md`.
>
> Rules:
>
> - Every active spec must declare PRD and ARD references or make the absence explicit.
> - Verification is mandatory.
> - If this feature exposes an external API, link a dedicated API Spec.
> - Use relative links only, calculated from the final authored document location.
> - Write this spec in English.
> - This document is the parent design doc; API contracts live in `api-spec.md` under the same feature directory.

---

## Overview

This document defines the technical design and implementation contract for
[Feature Name]. It turns upstream requirements into implementation and
verification criteria.

## Strategic Boundaries & Non-goals

[What this spec owns, and what it does not.]

## Related Inputs

Use this section for upstream requirement, architecture, and decision inputs.

- **PRD**: `[../../01.requirements/<###-Numbering>-<feature-or-system>.md]`
- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Related ADRs**: `[../../02.architecture/decisions/####-<short-title>.md]`

## Contracts

- **Config Contract**:
- **Data / Interface Contract**:
- **Governance Contract**:

## Core Design

- **Component Boundary**:
- **Key Dependencies**:
- **Tech Stack**:

## Data Modeling & Storage Strategy

- **Schema / Entity Strategy**:
- **Migration / Transition Plan**:

## Interfaces & Data Structures

### Core Interfaces

```typescript
interface ExampleContract {
  id: string;
  name: string;
}
```

## API Contract (If Applicable)

Contract-first rule: if this feature exposes an external API, define the
detailed API contract in a dedicated API Spec document.

- **API Spec**: `[./api-spec.md]`
- **Policy**: Keep API Specs under the current feature directory, not under a
  separate top-level path such as `docs/api/`.
- **Machine-readable Contract**:
  - `./contracts/openapi.yaml`
  - `./contracts/service.proto`
  - `./contracts/schema.graphql`

## Agent Role & IO Contract (If Applicable)

- **Agent Role**:
- **Inputs**:
- **Outputs**:
- **Success Definition**:

## Tools & Tool Contract (If Applicable)

- **Tool List**:
- **Permission Boundary**:
- **Failure Handling**:

## Prompt / Policy Contract (If Applicable)

- **System / Instruction Contract**:
- **Policy Constraints**:
- **Versioning Rule**:

## Memory & Context Strategy (If Applicable)

- **Short-term Context**:
- **Long-term Memory**:
- **Retrieval Boundary**:

## Guardrails (If Applicable)

- **Input Guardrails**:
- **Output Guardrails**:
- **Blocked Conditions**:
- **Escalation Rule**:

## Evaluation (If Applicable)

- **Eval Types**:
- **Metrics**:
- **Datasets / Fixtures**:
- **How to Run**:

## Edge Cases & Error Handling

- **Error 1**:
- **Error 2**:

## Failure Modes & Fallback / Human Escalation

- **Failure Mode**:
- **Fallback**:
- **Human Escalation**:

## Verification Commands

List the required commands, manual checks, or evidence capture steps.

```bash
[command 1]
[command 2]
pytest tests/[feature]_test.py
python evals/run_[feature]_eval.py
```

## Success Criteria & Verification Plan

- **VAL-SPC-001**:
- **VAL-SPC-002**:

## Related Documents

Target-relative examples below assume the authored file will be created at
`docs/03.specs/<###-Numbering>-<feature-id>/spec.md`.

Use this section for both upstream traceability and downstream or peer documents
created from this spec. `Related Inputs` may summarize the same upstream inputs,
but it does not replace this required `Related Documents` traceability section.

- **PRD**: `[../../01.requirements/<###-Numbering>-<feature-or-system>.md]`
- **ARD**: `[../../02.architecture/requirements/####-<system-or-domain>.md]`
- **Related ADRs**: `[../../02.architecture/decisions/####-<short-title>.md]`
- **Plan**: `[../../04.execution/plans/YYYY-MM-DD-<feature>.md]`
- **Tasks**: `[../../04.execution/tasks/YYYY-MM-DD-<feature-or-stream>.md]`
- **Runbook**: `[../../05.operations/runbooks/####-<topic>.md]`
