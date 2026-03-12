# Documentation Hub (`docs/`)

This directory contains long-term, human-readable project documentation used across planning, design, and reference delivery. It is architected for **Lazy Loading** to preserve AI context windows.

## 1. Necessity and Purpose

This directory acts as the stable knowledge base for the system. It isolates product/design knowledge from executable logic, serving as the primary reference point for Human Developers and AI Agents.

## 2. Document Categories (Lazy Loading Required)

Each sub-directory serves a distinct, non-overlapping purpose. Agents MUST query these ONLY when task-relevant.

### Core Documentation

- `adr/` — **Architecture Decision Records**: Context, decision, and consequences for technical choices.
- `ard/` — **Architecture Reference Documents**: Deep structural diagrams and global behavioral flows.
- `prd/` — **Product Requirements Documents**: Success metrics, target personas, and GWT scenarios.

### Lifecycle & Operations

- `plans/` — **Execution Plans**: Phase-based implementation strategies for major features.
- `specs/` — **Technical Specifications**: Low-level implementation details and data models.
- `incidents/` — **Incident Logs**: Post-mortems and technical debt resulting from outages.
- `runbooks/` — **Operational Procedures**: Step-by-step guides for deployment and recovery.

### Standards & Manuals

- `guides/` — **Agentic & Human Lifecycle Procedures**: Checklists for Pre, During, and Post-Development.
- `manuals/` — **Process Manuals**: Collaboration agreements, SLA definitions, and QA standards.

## 3. Explicit Boundaries & Anti-Patterns

1. **NO EXECUTABLE CODE**: Do NOT place scripts or source code here. Those belong in `/scripts/` or root directories.
2. **NO LOCAL AI WORKFLOWS**: High-level AI behavioral guidelines go in root `.agent/workflows/`. Docs here are project-specific.
3. **TEMPLATE MANDATORY**: Any new document MUST be generated from its respective template in the `templates/` directory.
4. **DOCUMENTATION PILLAR**: All content is subject to [.agent/rules/2100-documentation-pillar.md](file:///home/hy/projects/hy-home.k8s/.agent/rules/2100-documentation-pillar.md).
5. **OVERRIDE PRIORITIZATION**: AI Agents prioritize instructions in `guides/` and `manuals/` over generic behavioral rules.

---
*Last Updated: March 2026*
