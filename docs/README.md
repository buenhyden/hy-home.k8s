---
layer: "meta"
---
# Documentation Hub (`docs/`)

This directory contains the durable project knowledge for the `hy-home.k8s` repository.

## Documentation Structure (Flattened)

Documentation is organized by type at the root level. Use the `layer:` metadata in the frontmatter to distinguish between infrastructure, GitOps, and other domains.

- [PRDs](./prd/): Product Requirements Documents (The **What**)
- [Specs](./specs/): Implementation Specifications (The **Exact How**)
- [Plans](./plans/): Execution Roadmaps
- [ADRs](./adr/): Architecture Decision Records (The **Why**)
- [ARDs](./ard/): Architecture Reference Documents
- [Runbooks](./runbooks/): Operator Procedures
- [Manuals](./manuals/): System manuals, Collaboration, and Governance
- [Incidents](./incidents/): Incident Reports
- [Postmortems](./postmortems/): System Postmortems

## Guidelines

Refer to [AGENTS.md](../AGENTS.md) for the root contract governing AI agent behavior in this repository.
