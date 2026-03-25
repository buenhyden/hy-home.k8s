# AI Agent Governance Optimization Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Refactor and optimize the `docs/00.agent-governance/` folder to ensure consistent paths, complete documentation, and alignment with March 2026 "Thin Root" standards.

**Architecture:** Centralized "Thin Root" approach using `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md` as shims that point to a modular governance hub in `docs/00.agent-governance/`.

**Tech Stack:** Markdown, JIT Loading Protocol, AGENTic Persona-Matrix.

---

### Task 1: Update Persona-Matrix Rule Paths

**Files:**
- Modify: `docs/00.agent-governance/rules/persona-matrix.md`

**Step 1: Update rule paths**
Ensure all mandatory rules point to the correct prefixed directories in `.agent/rules/`.

```markdown
| Persona | Mandatory Rules (JIT) |
| :--- | :--- |
| **Product Manager** | `.agent/rules/0100-Standards/` |
| **System Architect** | `.agent/rules/1900-Architecture_Patterns/` |
| **Frontend Engineer** | `.agent/rules/1000-Frontend/` |
| **Backend Engineer** | `.agent/rules/0900-Backend/` |
| **Infra/DevOps Miner** | `.agent/rules/0300-DevOps_and_Infrastructure/` |
| **Security Officer** | `.agent/rules/2200-Security/` |
| **QA Engineer** | `.agent/rules/0700-Testing_and_QA/` |
```

---

### Task 2: Fill Content for Documentation Scope (`docs.md`)

**Files:**
- Modify: `docs/00.agent-governance/scopes/docs.md`

**Step 1: Write Documentation Scope content**
Define responsibilities for Technical Writers and Researchers.

```markdown
# Documentation & Research Scope

This scope defines the standards for the Writer and Researcher personas.

## 1. Core Responsibilities

- Curate and maintain project documentation in `docs/`.
- Ensure alignment with the 01-99 stage-gate taxonomy.
- Conduct deep research and document findings in `docs/90.references/`.
- Maintain standard templates in `docs/99.templates/`.
- **SSoT**: `docs/07.guides/`, `docs/90.references/`, `docs/99.templates/`.

## 2. Standard Taxonomy (SSoT)

- **Guides**: `docs/07.guides/` (User/Technical manuals).
- **Postmortems**: `docs/11.postmortems/` (RCA/Lessons learned).
- **Templates**: `docs/99.templates/` (Boilerplate for new docs).

## 3. Required Metadata

```markdown
---
layer: docs
stage: [07|11|90|99]
---
\```

## 4. Skills Engagement

- `api-documentation`
- `tutorial-engineer`
- `deep-research`
-technical-writing`
```

---

### Task 3: Fix Path References in Scope Files

**Files:**
- Modify: `docs/00.agent-governance/scopes/backend.md`
- Modify: `docs/00.agent-governance/scopes/frontend.md`
- Modify: `docs/00.agent-governance/scopes/architecture.md`
- Modify: `docs/00.agent-governance/scopes/infra.md`
- Modify: `docs/00.agent-governance/scopes/security.md`
- Modify: `docs/00.agent-governance/scopes/qa.md`

**Step 1: Update `.agent/rules/` paths to use numbered prefixes**
Example: Change `.agent/rules/backend/` to `.agent/rules/0900-Backend/`.

**Step 2: Fix formatting in `security.md`**
Remove duplicate headers and fix malformed lists.

---

### Task 4: Finalize Root Shims

**Files:**
- Modify: `AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `GEMINI.md`

**Step 1: Ensure minimal contents and consistent links**
Verify that all shims point to `docs/00.agent-governance/agent-instructions.md` as the primary gateway.

---

## Verification Plan

### Manual Verification
- [ ] Check all Markdown links in `docs/00.agent-governance/` using `ls` to verify file existence.
- [ ] Verify that `CLAUDE.md` correctly instructions me to load `agent-instructions.md`.
- [ ] Verify that `docs.md` is no longer empty.
- [ ] Cross-check `persona-matrix.md` paths with actual `.agent/rules/` directory listing.
