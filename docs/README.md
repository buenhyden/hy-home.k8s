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

- `specs/` — **Technical Specifications**: Low-level implementation details and data models. Every feature begins here.
- `runbooks/` — **Operational Procedures**: Step-by-step guides for deployment, maintenance, and recovery.
- `incidents/` — **Incident Logs**: Post-mortems and technical debt resulting from outages.
- `plans/` — **Execution Plans**: Phase-based implementation strategies for major features.

### Standards & Manuals

- `manuals/` — **Process Manuals**: Collaboration agreements, SLA definitions, and QA standards.
- `operations/` — **Operational Infrastructure**: Definitions for environment hierarchy and baseline readiness.

## 3. Explicit Boundaries & Anti-Patterns

1. **NO EXECUTABLE CODE**: Do NOT place scripts or source code here. Those belong in root `/scripts/` or implementation directories.
2. **TEMPLATE MANDATORY**: Any new document MUST be generated from its respective template in the root `templates/` directory.
3. **DOCUMENTATION PILLAR**: All content is subject to [.agent/rules/2100-documentation-pillar.md](../.agent/rules/2100-documentation-pillar.md).
4. **LINK TO ROOT**: For host setup and prerequisites, always refer to the root [README.md](../README.md).

---
*Last Updated: March 2026*
