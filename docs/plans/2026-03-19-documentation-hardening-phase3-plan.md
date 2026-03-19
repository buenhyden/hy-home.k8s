---
layer: "meta"
---
# Documentation Hardening Phase 3 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Achieve 100% documentation integrity across all core folders by fixing links, normalizing metadata, and ensuring template compliance.

**Architecture:** Systematic batch remediation using `sed` and `multi_replace_file_content` to apply surgical fixes. Verified by a Python-based link integrity scanner.

**Tech Stack:** Markdown, Shell (sed), Python (verification script)

---

### Task 1: Fix Persistent Broken Links

**Files:**
- Modify: `docs/agentic/lifecycle.md`
- Modify: `docs/manuals/README.md`
- Modify: `docs/runbooks/2026-03-15-documentation-maintenance.md`

**Step 1: Fix lifecycle.md malformed links**
Replace corrupted bracket/parentheses links with clean targets.

**Step 2: Fix manuals/README.md root reference**
Correct `../AGENTS.md` to `../../AGENTS.md`.

**Step 3: Fix documentation-maintenance.md regex string**
Remove `.*.md` and link to `2026-03-15-documentation-validation.md`.

**Step 4: Verify links**
Run: `python3 -c "import os; print(os.path.exists(\"docs/operations/2026-03-19-incident-management.md\"))"`
Expected: True

**Step 5: Commit**
`git commit -m "docs: fix persistent broken links in lifecycle and manuals"`

---

### Task 2: ADR Metadata Normalization (Redundancy Cleanup)

**Files:**
- Modify: `docs/adr/0000-lazy-loading-implementation.md`
- Modify: `docs/adr/0001-k3d-local-cluster.md`
- Modify: `docs/adr/0002-argocd-gitops.md`
- Modify: `docs/adr/0003-documentation-taxonomy-standard.md`
- Modify: `docs/adr/0004-documentation-refactor-decision.md`
- Modify: `docs/adr/0005-documentation-normalization.md`

**Step 1: Remove redundant layer tags**
Ensure only one `layer:` tag exists in the YAML frontmatter and the H1 block follows the `Owner`/`Last Reviewed` standard.

**Step 2: Consolidate Authors/Deciders**
Move individual author/decider fields to a single `Owner` field in the Markdown block to match the project standard.

**Step 3: Commit**
`git commit -m "docs: normalize ADR metadata and remove redundant tags"`

---

### Task 3: Template Compliance (Missing Sections)

**Files:**
- Modify: `docs/ard/2026-03-16-agent-instruction-system-ard.md`

**Step 1: Add Overview (KR)**
Inject the missing Korean overview section after the metadata block.

**Step 2: Final Verification Scan**
Run the full Python link audit script.

**Step 3: Commit**
`git commit -m "docs: add missing Korean overview and finalize template compliance"`
