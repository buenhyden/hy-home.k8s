---
layer: "meta"
---
# Spec: Documentation System Implementation

## 1. Scope

This spec defines the mechanical changes required to implement the flattened documentation taxonomy and modular agent instruction model.

## 2. Implementation Details

### 2.1 Directory Structure

- **Target**: Ensure `docs/` contains only: `ard`, `adr`, `prd`, `specs`, `plans`, `runbooks`, `operations`.
- **Migration**: Move `docs/operations/incidents` to `docs/runbooks/` or handle according to the final taxonomy (user listed `operations` and `runbooks`).
- **Cleanup**: Delete all `.gitkeep` files in these directories once populated. Move human-facing guides from `docs/guides/` to `docs/manuals/`.

### 2.2 Metadata Enforcement

- **Action**: Update all existing `.md` files in `docs/` to include:

  ```yaml
  ---
  layer: "[infra|gitops|app|meta]"
  ---
  ```

### 2.3 Agentic Instruction Refactor

- **AGENTS.md**: Update the "Documentation Scope Map" to use absolute paths to `docs/agentic/scopes/`.
- **docs/agentic/agent-instructions.md**:
  - Centralize rule imports.
  - Formalize the "Lazy Loading" behavior description.

### 2.4 Governance Files

- **CONTRIBUTING.md**: Add a check for `layer:` metadata in the PR requirements.
- **ARCHITECTURE.md**: Update links to point to flattened `docs/` paths.

## 3. Verification

- `grep -r "layer:" docs/` must return a match for every markdown file.
- `ls docs/guides/` must fail.
