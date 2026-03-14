---
layer: "meta"
---
# Spec: Documentation and Agent Instruction Refactor

## 1. Overview

This specification details the technical changes required to implement the new documentation taxonomy and the AI agent lazy-loading instruction system.

## 2. Technical Requirements

### Folder Structure

- Ensure `docs/[prd, adr, ard, specs, plans, runbooks, operations, manuals]` exist.
- Remove `docs/guides/` after migration.

### Metadata Compliance

- Every file in the above folders MUST match:

```yaml
---
layer: "[layer-name]"
---
```

### Agent Instruction Registry

- `AGENTS.md` and `docs/agentic/agent-instructions.md` will become registries.
- Loading mechanism:
  - Instructions will use explicit "LOAD WHEN" comments.
  - Agents are instructed to only read scope files when their current working directory or task name matches the scope.

## 3. Verification Logic

- **Metadata check**: `grep -L "layer:" docs/**/*.md` should return no results (excluding READMEs).
- **Instruction check**: Agent should stop if a task outside its loaded scope is requested without loading the new scope.
