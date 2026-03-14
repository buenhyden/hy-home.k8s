---
layer: "meta"
---
# PRD: Documentation and Agent Instruction System

## 1. Goal

Establish a high-trust, low-overhead documentation and automation framework that enables both human operators and AI agents to maintain a complex Kubernetes homelab with zero ambiguity.

## 2. Requirements

- **REQ-001: Flattened Taxonomy**: All documentation MUST reside in type-specific directories under `docs/` (e.g., `docs/prd/`, `docs/specs/`).
- **REQ-002: Layer Metadata**: Every markdown file MUST include `layer:` in its YAML frontmatter (e.g., `infra`, `gitops`, `app`, `meta`).
- **REQ-003: Rule-Based Lazy Loading**: AI agents MUST load instructions based on the active `rule` defined in `docs/agentic/rules/`. Each rule maps to a specific `scope` in `docs/agentic/scopes/`.
- **REQ-004: Proactive and Absolute Skill Use**: Agents MUST proactively use any available skill in the runtime without restriction. Skill selection should be guided by the task, not by restricted lists.
- **REQ-005: Taxonomy Alignment**: Documentation MUST be organized into exactly `adr, ard, prd, specs, plans, runbooks, operations` directories under `docs/`.
- **REQ-006: Layer Metadata**: Every markdown file MUST include `layer:` in its YAML frontmatter.

## 3. Success Criteria

- [ ] No files in retired directories (e.g., `docs/guides/`).
- [ ] All `docs/**/*.md` files contain `layer:` metadata.
- [ ] `AGENTS.md` correctly maps all `docs/` subtrees to their respective instruction scopes.
- [ ] `pre-commit` hooks verify documentation compliance.
