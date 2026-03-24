---
layer: "meta"
---
# Agent Lifecycle

Guidelines for managing documents throughout the development lifecycle.

## Pre-Development

- Goal: turn a request into approved requirements, plans, and specifications.
- Main sources: [collaboration-guide.md](../operations/collaboration-guide.md), [docs/prd/](../prd/), [docs/specs/](../specs/), [docs/plans/](../plans/), [docs/adr/](../adr/), [docs/ard/](../ard/).

## During-Development

- Goal: implement only against approved specs and document any architectural drift.
- Main sources: [docs/specs/](../specs/), [docs/plans/](../plans/), [qa-security-guide.md](../operations/qa-security-guide.md), [.agent/workflows/](../../.agent/workflows/).

## Post-Development

- Goal: verify correctness, operational impact, and handoff readiness.
- **Collaborative Writing**: [collaboration-guide.md](../operations/collaboration-guide.md).
- **Quality Assurance**: [docs/specs/](../specs/), [docs/plans/](../plans/), [qa-security-guide.md](../operations/qa-security-guide.md).
- **Documentation Validation**: [2026-03-15-documentation-validation.md](../runbooks/2026-03-15-documentation-validation.md).
- **Incident Management**: [2026-03-19-incident-management.md](../operations/2026-03-19-incident-management.md).

## Handoff Rules

- Plan before complex work.
- Implement against `docs/specs/`, not memory.
- Re-open planning when implementation must materially diverge from approved specs.
- Validate links, imports, and directory placement before completion.
