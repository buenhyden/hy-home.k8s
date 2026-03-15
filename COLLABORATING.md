---
layer: "meta"
---
# Collaborating in this Framework

## Necessity & Required Content

This document defines the operational handoff between Human Developers and the Multi-Agent System. While `AGENTS.md` defines agent roles, this file defines how humans manage and collaborate with those agents.

**Handoff Protocols**:

- **Intent-First**: Humans define the "What" and "Why" in PRDs.
- **Spec-Driven**: Agents define the "How" in Specs.
- **Validation-Locked**: No code is generated without human approval of the Implementation Spec.

## 0. Mandatory Project Kickoff

Before major development starts, the team (Human + Planner Agent) MUST establish working agreements.

- **Action**: Use `templates/collaboration-guide-template.md` to create `docs/guides/collaboration-guide.md`.
- **Enforcement**: AI Agents will verify the existence of this guide during initialization.

## 1. Requesting Work (Pre-Development)

Humans primarily interact with the **Planner Agent**.

- **Human**: Defines business needs in an Issue or prompt.
- **AI (Planner)**: Generates a PRD in `docs/prd/`.
- **AI (Planner)**: Once approved, generates an Implementation Spec in `docs/specs/`.
- **Human**: MUST approve the final spec before execution.

## 2. Implementation Workflow (During-Development)

- **AI (Coder Agents)**: Implement code and tests EXACTLY as specified in `docs/specs/`.
- **Rule of Thumb**: Agents should never invent undocumented edge cases; if missing, they must STOP and ASK.
- **Human**: Periodically review progress and provide domain context only.

## 3. Review & Deployment (Post-Development)

- **AI (Reviewer)**: Performs automated linting, security checks, and spec-compliance verification.
- **Human**: Final merge approval, focusing on logic and business value.
- **AI (DevOps)**: Generates or updates runbooks in `docs/runbooks/` for deployment.

## 4. Conflict Resolution (AI Hallucinations)

If an agent hallucinates or loops:

1. **Stop**: Terminate the agent session.
2. **Adjust**: Manually correct the specification in `docs/specs/`.
3. **Resume**: Re-prompt the agent, pointing to the exact line in the spec it disregarded.

## 5. Evolving the Rules

- **Project Scoped**: Define overrides in project-specific files.
- **Global Rules**: Update files in `docs/agentic/` (e.g., `docs/agentic/rules/core.md`) to evolve the standard.
- **Flagging**: Agents will flag human instructions that contradict established rules.
