---
layer: 'meta'
---

# Project Documentation Templates

This directory contains standardized templates for all documentation in the `hy-home.k8s` project. These templates ensure consistency, maintainability, and alignment with the project's agentic documentation standards.

## 1. Governance Standards

All documentation in this repository MUST adhere to the following standards established in `docs/manuals/README.md`:

- **Flattened Directory Structure**: All documentation is stored in dedicated root-level folders: `docs/manuals/`, `docs/incidents/`, `docs/postmortems/`, `docs/specs/`, `docs/plans/`, `docs/adr/`, `docs/ard/`, `docs/prd/`.
- **Mandatory Layer Metadata**: Every document MUST include a `layer:` metadata field in its YAML frontmatter.
    - **Allowed Values**: `meta | infra | gitops | app | ops`
- **Bilingual Context**: Documents MUST include an `Overview (KR)` section at the top (1-2 sentences in Korean).
- **Relative Linking**: Always use relative links (e.g., `[ARD](../ard/YYYY-MM-DD-feature.md)`) for cross-references.
- **Elite Architecture Standards**: All core templates (ARD, PRD, Spec, Manuals) now include mandatory sections for **FinOps**, **Disaster Recovery (DR)**, **Compliance (GRC)**, and **Developer Experience (DX)**.

## 2. Template Categories (Updated)

| Category | Templates | Target Directory |
| :--- | :--- | :--- |
| **Architecture** | `adr`, `ard`, `prd` | `docs/adr/`, `docs/ard/`, `docs/prd/` |
| **Development** | `spec`, `api-spec`, `plan` | `docs/specs/`, `docs/plans/` |
| **Operations** | `runbook`, `incident`, `postmortem` | `docs/runbooks/`, `docs/incidents/`, `docs/postmortems/` |
| **Manuals** | `operations-manual`, `service-manual`, `tier-manual`, `collaboration-manual` | `docs/manuals/` |
| **Reference** | `readme` | Project Root |

> [!NOTE]
> **Consolidation**: The `qa-security-guide` has been merged into the `operations-manual-template.md` to reduce redundancy.

## 3. Large Document Patterns (Index Pattern)

For documents exceeding ~500 lines (e.g., Service/Tier Manuals), use the **Index Pattern**:

1. Create a directory for the manual (e.g., `docs/manuals/my-service/`).
2. Use the template as the `README.md` (the Index).
3. Split technical sections (Architecture, Config, Troubleshooting) into separate files in the same directory and link them from the `README.md`.

## 4. Usage

To create a new document:
1. Copy the relevant template from this directory.
2. Place it in the correct directory (e.g., `docs/manuals/`).
3. Replace all placeholders (`<...>` or `[...]`).
4. Update the `layer:` metadata to match the document's scope.
