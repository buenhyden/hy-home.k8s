# Agent Lifecycle

This manual defines the repo-specific delivery lifecycle for agents. It complements [AGENTS.md](../AGENTS.md) without duplicating the entire `.agent/rules/` corpus.

## Pre-Development

- Goal: turn a request into a reviewable plan and approved specification.
- Required inputs: user request, relevant docs, architecture constraints, and any existing specs.
- Outputs: updated planning artifacts and approved specs under [docs/specs/](../docs/specs/), plus supporting PRD or ADR documents when needed.
- Primary sources: [docs/guides/pre-development-guide.md](../docs/guides/pre-development-guide.md), [docs/prd/](../docs/prd/), [docs/specs/](../docs/specs/), [docs/adr/](../docs/adr/), [docs/ard/](../docs/ard/).

## During-Development

- Goal: implement only what the approved spec requires, with tests and evidence.
- Required inputs: approved spec, relevant workflow docs, and inspected repo context.
- Outputs: code changes, tests, and any required doc updates.
- Primary sources: [docs/guides/during-development-guide.md](../docs/guides/during-development-guide.md), [docs/specs/](../docs/specs/), and repo workflows under [.agent/workflows/](../.agent/workflows/).

## Post-Development

- Goal: verify correctness, protect architectural integrity, and hand off operational impact cleanly.
- Required inputs: implemented change set, verification results, review feedback, and deployment or runbook context if relevant.
- Outputs: validated change, review-ready documentation, and updated runbooks when operations change.
- Primary sources: [docs/guides/post-development-guide.md](../docs/guides/post-development-guide.md), [docs/runbooks/](../docs/runbooks/), and [docs/incidents/](../docs/incidents/).

## Persona Map

- Planner / Reasoner / Architect: frame requirements, constraints, and approach before implementation.
- Implementer / Refactorer: execute the approved scope with minimal, evidence-backed changes.
- Reviewer / Security / DevOps / QA: verify behavior, risks, release readiness, and operational impact.

## Handoff Rules

- Plan before starting complex or multi-file work.
- Implement against approved artifacts in `docs/specs/`, not against memory or assumptions.
- Re-open planning if the implementation must diverge materially from the approved spec.
- Verify with concrete commands or inspection before claiming completion.
- Update linked docs when the change alters project-facing behavior, structure, or operations.
