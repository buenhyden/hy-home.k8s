---
layer: "meta"
---
# Runbook: Documentation Maintenance

## 1. Purpose

Ensure the repository's documentation remains compliant with the flattened taxonomy and layer-aware metadata standards.

## 2. Procedures

### 2.1 Adding a New Document

1. Identify the correct category (PRD, ADR, Spec, etc.).
2. Select the corresponding template from `templates/`.
3. Create the file in the appropriate `docs/` subdirectory.
4. **MANDATORY**: Set the `layer:` metadata in the frontmatter.
   - `infra`: Base cluster, OS, hardware.
   - `gitops`: ArgoCD, reconciliation, track-revision.
   - `app`: User-facing services or application logic.
   - `meta`: Documentation system, agent rules, governance.

### 2.2 Auditing Documentation

1. Run the metadata check:

   ```bash
   find docs/ -name "*.md" -exec grep -l "layer:" {} +
   ```

2. Verify all files are in the correct flattened directory.
3. Check for broken cross-links using `markdown-link-check` or similar tools.

### 2.3 Updating Agent Instructions

1. When a new documentation category is added, update `docs/agentic/agent-instructions.md` and `AGENTS.md`.
2. Create a new scope file in `docs/agentic/scopes/` if necessary.
