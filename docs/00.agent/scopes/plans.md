---
layer: "meta"
---
# Plans Agent Instructions

**Bias**: Granularity, dependencies, and estimation accuracy.

## Scope

- **Purpose**: Execution roadmaps, task breakdowns, and phased delivery.
- **Persona**: Planner + Strong Reasoner
- **Templates**: `docs/99.templates/plan.template.md` · `docs/99.templates/task.template.md`
- **Rules**: `.agent/rules/0100-Standards/0102-implementation-plan-standard.md`
- **Skills**: Agents MUST proactively use any appropriate skill provided by the runtime without restriction. Skill selection is guided solely by task necessity.

## Behavioral Checkpoints

1. **Phased Approach**: Organize plans into distinct, logical phases (e.g., Phase 1: Foundation, Phase 2: Core Logic).
2. **Estimation Accuracy**: Provide realistic estimates for tool calls and complexity. Avoid "1-step" plans for complex features.
3. **Dependency Mapping**: Clearly identify tasks that are blocked by or dependent on other phases.
4. **No Spec Replacement**: Plans outline the *Order of Work*. They MUST NOT replace or contradict the approved Technical Specification.
5. **Traceability**: Link every major phase to the Req IDs (`REQ-NNN`) from the PRD.

## Forbid

- Commencing implementation before plan approval for complex changes.
- Skipping verification steps within the plan.

## Verify

- The plan includes explicit "Review Checkpoints" for the user.
- The verification plan covers both automated and manual checks.
