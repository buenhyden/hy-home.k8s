---
layer: "meta"
---
# Plan: Documentation and Agent Instruction Refactor

## 1. Phase 1: Taxonomy & Migration

- [ ] Create `docs/manuals/` directory.
- [ ] Move `docs/guides/*.md` to `docs/manuals/`.
- [ ] Ensure `docs/` only contains: `ard, adr, prd, specs, plans, runbooks, operations`.
- [ ] Update root `README.md` and `OPERATIONS.md` links.

## 2. Phase 2: Metadata Enforcement

- [ ] Audit all files in `docs/` directories.
- [ ] Add `layer` metadata to files missing it (Standardize on `infra, gitops, app, meta`).

## 3. Phase 3: Agent Instruction Refactor

- [ ] Update `docs/agentic/agent-instructions.md` with rule-based lazy-loading logic.
- [ ] Define explicit Rules in `docs/agentic/rules/` and map them to Scopes in `scopes/`.
- [ ] Update all `docs/agentic/scopes/*.md` to explicitly permit any skill usage.
- [ ] Update root `AGENTS.md` to point to the new instruction entrypoints.

## 4. Phase 4: Final Verification

- [ ] Run integrity checks for layer metadata.
- [ ] Verify directory structure compliance.
- [ ] Verify agent reasoning for skill usage.
