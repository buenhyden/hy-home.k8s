# Agent Lifecycle

Human-readable lifecycle companion for document work in this repository.

## Pre-Development

- Goal: turn a request into approved requirements, plans, and specifications.
- Main sources: [docs/manuals/collaboration-guide.md](../docs/manuals/collaboration-guide.md), [docs/prd/](../docs/prd/), [docs/specs/](../docs/specs/), [docs/plans/](../docs/plans/), [docs/adr/](../docs/adr/), [docs/ard/](../docs/ard/).

## During-Development

- Goal: implement only against approved specs and document any architectural drift.
- Main sources: [docs/specs/](../docs/specs/), [docs/plans/](../docs/plans/), [docs/manuals/qa-security-guide.md](../docs/manuals/qa-security-guide.md), [.agent/workflows/](../.agent/workflows/).

## Post-Development

- Goal: verify correctness, operational impact, and handoff readiness.
- Main sources: [docs/runbooks/](../docs/runbooks/), [docs/incidents/](../docs/incidents/), [docs/operations/](../docs/operations/), [docs/manuals/operations-guide.md](../docs/manuals/operations-guide.md).

## Handoff Rules

- Plan before complex work.
- Implement against `docs/specs/`, not memory.
- Re-open planning when implementation must materially diverge from approved specs.
- Validate links, imports, and directory placement before completion.
