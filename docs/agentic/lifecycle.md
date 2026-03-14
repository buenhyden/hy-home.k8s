# Agent Lifecycle

Human-readable lifecycle companion for document work in this repository.

## Pre-Development

- Goal: turn a request into approved requirements, plans, and specifications.
- Main sources: [collaboration-guide.md](../manuals/collaboration-guide.md), [docs/prd/](../prd/), [docs/specs/](../specs/), [docs/plans/](../plans/), [docs/adr/](../adr/), [docs/ard/](../ard/).

## During-Development

- Goal: implement only against approved specs and document any architectural drift.
- Main sources: [docs/specs/](../specs/), [docs/plans/](../plans/), [qa-security-guide.md](../manuals/qa-security-guide.md), [.agent/workflows/](../.agent/workflows/).

## Post-Development

- Goal: verify correctness, operational impact, and handoff readiness.
- Main sources: [docs/runbooks/](../runbooks/), [docs/incidents/](../incidents/), [docs/operations/](../operations/), [operations-guide.md](../manuals/operations-guide.md).

## Handoff Rules

- Plan before complex work.
- Implement against `docs/specs/`, not memory.
- Re-open planning when implementation must materially diverge from approved specs.
- Validate links, imports, and directory placement before completion.
